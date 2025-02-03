from docutils.parsers.rst import Directive
from docutils import nodes
from ewokscore.task_discovery import (
    _iter_discover_tasks_from_modules,
    _iter_modules_from_pattern,
)

from .utils import field


class EwoksTaskDirective(Directive):
    required_arguments = 1

    def run(self):
        module_pattern = self.arguments[0]
        results = []
        for module in _iter_modules_from_pattern(module_pattern):
            for task in _iter_discover_tasks_from_modules(module, task_type="class"):
                title = task["task_identifier"].split(".")[-1]
                task_section = nodes.section(ids=[title])
                task_section.extend(
                    [
                        nodes.title(text=title),
                        nodes.paragraph(text=task["description"]),
                        nodes.field_list(
                            "",
                            nodes.field(
                                "",
                                nodes.field_name(text="Identifier"),
                                nodes.field_body(
                                    "",
                                    nodes.paragraph(
                                        "",
                                        "",
                                        nodes.literal(text=task["task_identifier"]),
                                    ),
                                ),
                            ),
                            field("Task type", task["task_type"]),
                            field(
                                "Required inputs",
                                ",".join(task["required_input_names"]),
                            ),
                            field(
                                "Optional inputs",
                                ",".join(task["optional_input_names"]),
                            ),
                            field("Outputs", ",".join(task["output_names"])),
                        ),
                    ]
                )
                results.append(task_section)
        return results
