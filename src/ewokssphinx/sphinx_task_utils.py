from typing import Any
from typing import Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective


def task_nodes(
    directive: SphinxDirective,
    tasks: Sequence[dict[str, Any]],
) -> list[nodes.section]:
    """
    Convert a list of JSON Ewoks task descriptions into Sphinx/Docutils
    document node trees.

    Returns a list of <section> nodes.
    """
    return [_task_section(directive, task) for task in tasks]


def _task_section(directive: SphinxDirective, task: dict[str, Any]) -> nodes.section:
    section = nodes.section(
        "",
        ids=[task["task_identifier"]],
        classes=["ewokssphinx-task"],
    )

    # Title
    section.append(nodes.title(text=task["task_name"]))

    # Description
    if task["description"]:
        section.extend(_rst_to_nodes(directive, task["description"]))

    # Identifier + task type
    section.append(
        nodes.field_list(
            "",
            _field_node("Identifier", nodes.literal(text=task["task_identifier"])),
            _field_node("Task type", nodes.Text(task["task_type"])),
        )
    )

    if task["inputs"]:
        # Detailed pydantic-style input definitions
        input_parameters = _parameter_nodes(
            directive,
            title="Inputs:",
            css_classes=["field-odd"],
            parameters=task["inputs"],
            is_outputs=False,
        )
    else:
        # Simple inputs from name lists
        input_parameters = _parameter_nodes_only_names(
            title="Inputs:",
            css_classes=["field-odd"],
            required_names=task.get("required_input_names", []),
            optional_names=task.get("optional_input_names", []),
        )

    if task["outputs"]:
        # Detailed pydantic-style output definitions
        output_parameters = _parameter_nodes(
            directive,
            title="Outputs:",
            css_classes=["field-even"],
            parameters=task["outputs"],
            is_outputs=True,
        )
    else:
        # Simple outputs from name lists
        output_parameters = _parameter_nodes_only_names(
            title="Outputs:",
            css_classes=["field-even"],
            required_names=[],  # outputs are never “required”
            optional_names=task.get("output_names", []),
        )

    # Combine inputs + outputs in a container so that
    # Sphinx does not attach the "simple" CSS class.
    io_def = nodes.container("")
    io_def.append(input_parameters)
    io_def.append(output_parameters)

    section.append(
        nodes.definition_list(
            "",
            io_def,
            classes=["ewokssphinx-field-list"],
        )
    )

    return section


def _field_node(name: str, body: nodes.Element) -> nodes.field:
    """Construct a Sphinx field like:  Identifier: my.module.Task"""
    return nodes.field(
        "",
        nodes.field_name(text=name),
        nodes.field_body("", body),
    )


def _term_node(name: str, is_required: bool) -> nodes.term:
    """
    Create a term:

        my_input
        my_input*
    """
    if not is_required:
        return nodes.term(text=name)

    # Required input -> add "*"
    return nodes.term(
        "",
        name,
        nodes.strong("", "*", classes=["ewokssphinx-required"]),
    )


def _parameter_nodes_only_names(
    title: str,
    css_classes: list[str],
    required_names: Sequence[str],
    optional_names: Sequence[str],
) -> nodes.definition_list_item:

    dl = nodes.definition_list()

    # Required items
    for name in required_names:
        dl.append(
            nodes.definition_list_item(
                "",
                _term_node(name, True),
                nodes.definition(),
            )
        )

    # Optional items
    for name in optional_names:
        dl.append(
            nodes.definition_list_item(
                "",
                _term_node(name, False),
                nodes.definition(),
            )
        )

    return nodes.definition_list_item(
        "",
        nodes.term(text=title, classes=css_classes),
        nodes.definition("", dl),
        classes=["field-list"],
    )


def _parameter_nodes(
    directive: SphinxDirective,
    title: str,
    css_classes: list[str],
    parameters: dict[str, str | list[str] | None],
    is_outputs: bool,
) -> nodes.definition_list_item:

    dl = nodes.definition_list()
    for parameter in parameters:
        dl.append(_parameter_node(directive, parameter, is_outputs))

    return nodes.definition_list_item(
        "",
        nodes.term(text=title, classes=css_classes),
        nodes.definition("", dl),
        classes=["field-list"],
    )


def _parameter_node(
    directive: SphinxDirective, parameter: dict[str, Any], is_output: bool
) -> nodes.definition_list_item:
    """
    Full parameter description structure:

        name* : annotation = default
        Description...

        Examples:
            'foo'
            'bar'
    """

    # Build the term
    #
    #   name* : annotation = default
    #
    is_required = parameter["required"] and not is_output
    term = _term_node(parameter["name"], is_required)

    if parameter["annotation"]:
        term.extend([nodes.Text(" : "), nodes.literal(text=parameter["annotation"])])

    has_default = not parameter["required"] and not is_output
    if has_default:
        term.append(
            nodes.literal(
                text=f"= {parameter['default']}",
                classes=["ewokssphinx-default"],
            )
        )

    # Description
    definition = nodes.definition()
    if parameter["description"]:
        definition.extend(_rst_to_nodes(directive, parameter["description"]))

    # Examples
    examples = parameter.get("examples")
    if examples:
        definition.append(_examples_node(examples))

    return nodes.definition_list_item("", term, definition)


def _examples_node(examples: list[Any]) -> nodes.container:
    bl = nodes.bullet_list()
    for example in examples:
        bl.append(nodes.list_item("", nodes.Text(example)))

    return nodes.container(
        "",
        nodes.Text("Examples:"),
        bl,
        classes=["ewokssphinx-examples"],
    )


def _rst_to_nodes(directive: SphinxDirective, text: str) -> list[nodes.Node]:
    # TODO: directives like ".. note::" still appear as plain text.
    return directive.parse_text_to_nodes(text)
