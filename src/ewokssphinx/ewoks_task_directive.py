import inspect
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from ewokscore.task_discovery import discover_tasks_from_modules


from .utils import field


def _task_type_option(argument):
    return directives.choice(argument, ("class", "method", "ppfmethod"))


class EwoksTaskDirective(SphinxDirective):
    required_arguments = 1
    option_spec = {"task_type": _task_type_option}

    def run(self):
        module_pattern = self.arguments[0]
        task_type = self.options.get("task_type")

        results = []
        for task in discover_tasks_from_modules(module_pattern, task_type=task_type):
            title = task["task_identifier"].split(".")[-1]
            task_section = nodes.section(ids=[title])

            task_section += nodes.title(text=title)
            if task["description"]:
                task_section += self.parse_text_to_nodes(
                    # Clean up indentation from docstrings so that Sphinx properly parses them
                    inspect.cleandoc(task["description"])
                )

            task_section += [
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
                        ", ".join(task["required_input_names"]),
                    ),
                    field(
                        "Optional inputs",
                        ", ".join(task["optional_input_names"]),
                    ),
                    field("Outputs", ", ".join(task["output_names"])),
                ),
            ]
            results.append(task_section)
        return results
