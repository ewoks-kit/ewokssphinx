import importlib
import inspect
from typing import Any

from ewokscore.task_discovery import discover_tasks_from_modules
from sphinx.util.typing import stringify_annotation


def discover_tasks(
    module_pattern: str, task_type: str, ignore_import_error: bool
) -> dict[str, dict[str, Any]]:
    tasks = {}
    for task in discover_tasks_from_modules(
        module_pattern,
        task_type=task_type,
        raise_import_failure=not ignore_import_error,
    ):
        task_name = _get_task_name(task["task_identifier"], task["task_type"])

        serialized_task = {
            "task_name": task_name,
            "task_identifier": task["task_identifier"],
            "task_type": task["task_type"],
            "description": _parse_doc(task.get("description")),
            "required_input_names": task.get("required_input_names", []),
            "optional_input_names": task.get("optional_input_names", []),
            "inputs": [],
            "outputs": task.get("output_names", []),
        }

        input_model = task.get("input_model")
        if input_model:
            model_cls = _import_model(input_model)
            for name, field_info in model_cls.model_fields.items():
                serialized_task["inputs"].append(
                    _parse_pydantic_field(name, field_info)
                )

        tasks[task["task_identifier"]] = serialized_task
    return tasks


def _get_task_name(identifier: str, task_type: str) -> str:
    if task_type == "ppfmethod":
        # ppfmethods are all named `run` so use the module name as task name.
        return identifier.split(".")[-2]
    return identifier.split(".")[-1]


def _import_model(input_model_qual_name: str) -> type:
    module_name, _, model_name = input_model_qual_name.rpartition(".")
    mod = importlib.import_module(module_name)
    return getattr(mod, model_name)


def _parse_doc(text) -> str:
    return inspect.cleandoc(text) if text else ""


def _parse_pydantic_field(name, field_info) -> dict[str, str | list[str]]:
    examples = getattr(field_info, "examples", [])
    default = getattr(field_info, "default", None)
    examples = [repr(example) for example in examples]

    return {
        "name": name,
        "annotation": stringify_annotation(field_info.annotation),
        "required": field_info.is_required(),
        "description": _parse_doc(field_info.description),
        "examples": examples,
        "default": str(default),
    }
