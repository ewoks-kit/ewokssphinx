from pydantic import BaseModel


class TaskParameter(BaseModel, extra="forbid"):
    name: str
    annotation: str | None
    required: bool
    description: str | None
    examples: list[str]
    default: str | None
    has_default: bool


class TaskDescription(BaseModel, extra="forbid"):
    task_name: str
    task_identifier: str
    task_type: str
    description: str
    inputs: list[TaskParameter]
    outputs: list[TaskParameter]
