import importlib
import inspect
import json
from pathlib import Path
from typing import Any

from ewokscore.task_discovery import discover_tasks_from_modules
from pydantic import BaseModel
from sphinx.util.typing import stringify_annotation


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

        inputs = _parse_pydantic_model(task.get("input_model"))
        outputs = _parse_pydantic_model(task.get("output_model"))

        serialized_task = {
            "task_name": task_name,
            "task_identifier": task["task_identifier"],
            "task_type": task["task_type"],
            "description": _parse_doc(task.get("description")),
            "required_input_names": task.get("required_input_names", []),
            "optional_input_names": task.get("optional_input_names", []),
            "output_names": task.get("output_names", []),
            "inputs": inputs,
            "outputs": outputs,
        }

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


def _parse_pydantic_model(model: BaseModel | None) -> list[dict[str, str | list[str]]]:
    parameters = []
    if model is None:
        return parameters

    model_cls = _import_model(model)
    for name, field_info in model_cls.model_fields.items():
        parameters.append(_parse_pydantic_field(name, field_info))
    return parameters


def _import_model(input_model_qual_name: str) -> type:
    module_name, _, model_name = input_model_qual_name.rpartition(".")
    mod = importlib.import_module(module_name)
    return getattr(mod, model_name)


def _parse_doc(text) -> str:
    return inspect.cleandoc(text) if text else ""


def _parse_pydantic_field(name, field_info) -> dict[str, str | list[str] | None]:
    examples = getattr(field_info, "examples", None)
    default = getattr(field_info, "default", None)
    examples = [repr(example) for example in examples or []]

    return {
        "name": name,
        "annotation": stringify_annotation(field_info.annotation),
        "required": field_info.is_required(),
        "description": _parse_doc(field_info.description),
        "examples": examples,
        "default": None if default is None else str(default),
    }
