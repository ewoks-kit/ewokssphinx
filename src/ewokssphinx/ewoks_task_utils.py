import importlib
import inspect
import json
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Iterator
from typing import Type
from typing import get_args
from typing import get_origin

from ewokscore.task_discovery import discover_tasks_from_modules
from ewoksutils.import_utils import qualname
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from sphinx.util.typing import stringify_annotation

from .type_utils import ParameterDescription
from .type_utils import TaskDescription


def discover_tasks(
    module_pattern: str, task_type: str, ignore_import_error: bool
) -> list[dict[str, Any]]:
    tasks = []
    for task in discover_tasks_from_modules(
        module_pattern,
        task_type=task_type,
        raise_import_failure=not ignore_import_error,
    ):
        task_name = _get_task_name(task["task_identifier"], task["task_type"])

        input_model_name = task.get("input_model")
        if input_model_name is not None:
            input_model = _import_model(input_model_name)
            inputs = _parse_pydantic_model(input_model)
        else:
            input_model = None
            inputs = _parse_parameter_names(
                task.get("required_input_names", []),
                task.get("optional_input_names", []),
            )

        output_model_name = task.get("output_model")
        if output_model_name:
            output_model = _import_model(output_model_name)
            outputs = _parse_pydantic_model(output_model)
        else:
            output_model = None
            outputs = _parse_parameter_names(task.get("output_names", []), [])

        submodels = {
            **_extract_submodels(input_model),
            **_extract_submodels(output_model),
        }
        serialized_task = {
            "task_name": task_name,
            "task_identifier": task["task_identifier"],
            "task_type": task["task_type"],
            "description": _parse_doc(task.get("description")),
            "inputs": inputs,
            "outputs": outputs,
            "submodels": {
                k: _parse_pydantic_model(submodels[k]) for k in sorted(submodels.keys())
            },
        }
        _ = TaskDescription(**serialized_task)

        tasks.append(serialized_task)
    return tasks


def cached_tasks(
    local_tasks: list[dict[str, Any]],
    json_cache_path: str | Path | None,
    module_pattern: str,
    task_type: str,
) -> list[dict[str, Any]]:
    """Save tasks in cache or load task from cache when local tasks are empty."""
    if not json_cache_path:
        return local_tasks

    json_cache_path = Path(json_cache_path)
    if json_cache_path.exists():
        cache = json.loads(json_cache_path.read_text(encoding="utf-8"))
    else:
        cache = {}

    module_pattern_dict = cache.setdefault(module_pattern, {})
    if local_tasks or task_type not in module_pattern_dict:
        module_pattern_dict[task_type] = local_tasks

    json_cache_path.parent.mkdir(parents=True, exist_ok=True)
    json_cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")

    return module_pattern_dict[task_type]


def _get_task_name(identifier: str, task_type: str) -> str:
    if task_type == "ppfmethod":
        # ppfmethods are all named `run` so use the module name as task name.
        return identifier.split(".")[-2]
    return identifier.split(".")[-1]


def _parse_parameter_names(
    required_names: list[str], optional_names: list[str]
) -> list[dict[str, str | list[str]]]:
    parameters = []
    names = required_names + optional_names
    is_required = [True] * len(required_names) + [False] * len(optional_names)
    for name, required in zip(names, is_required):
        parameter = {
            "name": name,
            "annotation": None,
            "required": required,
            "description": None,
            "examples": [],
            "default": None,
            "has_default": False,
        }
        parameters.append(parameter)
    return parameters


def _parse_pydantic_model(model: Type[BaseModel]) -> list[ParameterDescription]:
    return [
        _parse_pydantic_field(name, field_info)
        for name, field_info in model.model_fields.items()
    ]


def _import_model(model_qual_name: str) -> Type[BaseModel]:
    module_name, _, model_name = model_qual_name.rpartition(".")
    mod = importlib.import_module(module_name)
    model = getattr(mod, model_name)
    if not issubclass(model, BaseModel):
        raise ValueError("Not a pydantic model")
    return model


def _parse_doc(text) -> str:
    return inspect.cleandoc(text) if text else ""


def _parse_pydantic_field(name: str, field_info: FieldInfo) -> ParameterDescription:
    examples = getattr(field_info, "examples", None)
    default = getattr(field_info, "default", None)
    if default is PydanticUndefined:
        default = None
        has_default = False
    else:
        has_default = True
    examples = [repr(example) for example in examples or []]

    return {
        "name": name,
        "annotation": stringify_annotation(field_info.annotation),
        "required": field_info.is_required(),
        "description": _parse_doc(field_info.description),
        "examples": examples,
        "default": None if default is None else str(default),
        "has_default": has_default,
    }


def _extract_submodels(model: Any) -> dict[str, Type[BaseModel]]:
    if model is None:
        return {}

    # Need to remove the original model to get only submodels
    return {
        qualname(submodel): submodel
        for submodel in _iter_models(model, seen=set())
        if submodel is not model
    }


def _iter_models(annotation: Any, seen: set[int]) -> Iterator[Type[BaseModel]]:
    annotation_id = id(annotation)
    if annotation_id in seen:
        return
    seen.add(annotation_id)

    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        yield annotation

        # Recurse into model fields
        for field in annotation.model_fields.values():
            yield from _iter_models(field.annotation, seen)

    origin = get_origin(annotation)
    # Handle Annotated[T, ...]
    if origin is Annotated:
        base_type, *_ = get_args(annotation)
        yield from _iter_models(base_type, seen)
        return

    # Recurse into generic arguments (Union, list, dict, etc.)
    for arg in get_args(annotation):
        yield from _iter_models(arg, seen)
