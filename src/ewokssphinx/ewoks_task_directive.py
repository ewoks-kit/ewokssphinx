import inspect

from docutils import nodes
from docutils.parsers.rst import directives
from ewokscore.task_discovery import discover_tasks_from_modules
from sphinx.util.docutils import SphinxDirective

from .utils import field, field_list


def _task_type_option(argument):
    return directives.choice(argument, ("class", "method", "ppfmethod"))


class EwoksTaskDirective(SphinxDirective):
    required_arguments = 1
    option_spec = {
        "task-type": _task_type_option,
        "ignore-import-error": directives.flag,
    }

    def run(self):
        module_pattern = self.arguments[0]
        task_type = self.options.get("task-type")
        ignore_import_error = "ignore-import-error" in self.options

        results = []
        for task in discover_tasks_from_modules(
            module_pattern,
            task_type=task_type,
            raise_import_failure=not ignore_import_error,
        ):
            if task["task_type"] == "ppfmethod":
                # ppfmethods are all named `run` so use the module name as task name.
                task_name = task["task_identifier"].split(".")[-2]
            else:
                task_name = task["task_identifier"].split(".")[-1]

            task_section = nodes.section(ids=[task_name])

            task_section += nodes.title(text=task_name)
            if task["description"]:
                task_section += self.parse_text_to_nodes(
                    # Clean up indentation from docstrings so that Sphinx properly parses them
                    inspect.cleandoc(task["description"])
                )

            task_section += nodes.field_list(
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
            )
            task_section += [
                field_list(
                    "Inputs",
                    [
                        *[
                            (input, " [Required]")
                            for input in task["required_input_names"]
                        ],
                        *[(input, "") for input in task["optional_input_names"]],
                    ],
                ),
                field_list(
                    "Outputs", [(output, "") for output in task["output_names"]]
                ),
            ]
            results.append(task_section)
        return results
