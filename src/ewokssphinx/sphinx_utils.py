from typing import Any, Sequence

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

def _rst_to_nodes(directive: SphinxDirective, text: str) -> list[nodes.Node]:
    return directive.parse_text_to_nodes(text)


def task_nodes(
    directive: SphinxDirective, tasks: Sequence[dict[str, Any]],
) -> list[nodes.section]:
    """Return a list of section nodes, one section for each Ewoks task."""
    return [_task_node(directive, task) for task in tasks]


def _task_node(directive: SphinxDirective, task: dict[str, Any]) -> nodes.section:
    task_section = nodes.section("", ids=[task["task_name"]], classes=["ewokssphinx-task"])

    # Title
    task_section += nodes.title(text=task["task_name"])

    # Description
    if task.get("description"):
        task_section += _rst_to_nodes(directive, task["description"])

    # Identifier / type
    task_section += nodes.field_list(
        "",
        _field_node("Identifier", nodes.literal(text=task["task_identifier"])),
        _field_node("Task type", nodes.Text(task["task_type"])),
    )

    # Inputs / outputs
    if task.get("inputs"):
        input_parameters = _parameter_nodes(
            "Inputs:",
            ["field-odd"],
            task["inputs"],
        )
    else:
        input_parameters = _parameter_nodes_only_names(
            "Inputs:",
            ["field-odd"],
            task.get("required_input_names", []),
            task.get("optional_input_names", []),
        )

    output_parameters = _parameter_nodes_only_names(
        "Outputs:",
        ["field-even"],
        [],
        task.get("outputs", []),
    )

    # Use container to force the field list to be compound so that
    # Sphinx does not attach the "simple" CSS class.
    io_definition = nodes.container("")
    io_definition.append(input_parameters)
    io_definition.append(output_parameters)

    task_section.append(
        nodes.definition_list("", io_definition, classes=["ewokssphinx-field-list"])
    )

    return task_section


def _parameter_nodes_only_names(
    title: str,
    css_classes: list[str],
    required_names: Sequence[str],
    optional_names: Sequence[str],
) -> nodes.definition_list_item:
    input_list = nodes.definition_list()
    for input_name in required_names:
        input_list.append(
            nodes.definition_list_item(
                "", _term_node(input_name, True), nodes.definition()
            )
        )
    for input_name in optional_names:
        input_list.append(
            nodes.definition_list_item(
                "", _term_node(input_name, False), nodes.definition()
            )
        )
    return nodes.definition_list_item(
        "",
        nodes.term(text=title, classes=css_classes),
        nodes.definition("", input_list),
        classes=["field-list"],
    )


def _parameter_nodes(
    title: str, css_classes: list[str], inputs: list[dict[str, Any]]
) -> nodes.definition_list_item:
    parameter_nodes = nodes.definition_list()
    for parameter in inputs:
        parameter_nodes.append(_parameter_node(parameter))
    return nodes.definition_list_item(
        "",
        nodes.term(text=title, classes=css_classes),
        nodes.definition("", parameter_nodes),
        classes=["field-list"],
    )


def _parameter_node(
    parameter: dict[str, str | list[str]],
) -> nodes.definition_list_item:
    """Documentation text:

    .. code-block::

        transformation_type* : ewoksndreg.transformation.types.TransformationType
        Transformation type

        Examples:
            'translation'
            'rigid'
    """

    # Ewoks task input/output parameter name and type

    node = _term_node(parameter["name"], parameter["required"])

    if parameter["annotation"]:
        # For example
        #   transformation_type* : ewoksndreg.transformation.types.TransformationType
        node += [
            nodes.Text(" : "),
            nodes.literal(text=parameter["annotation"]),
        ]

    if not parameter["required"]:
        # For example
        #   shape : Sequence[int] | None= None
        node.append(
            nodes.literal(
                text=f"= {parameter['default']}", classes=["ewokssphinx-default"]
            )
        )

    # Ewoks task input/output parameter description

    node_definition = nodes.definition()
    if parameter.get("description"):
        node_definition.append(nodes.paragraph(text=parameter["description"]))

    # Ewoks task input/output examples

    if parameter.get("examples"):
        node_definition.append(_examples_node(parameter["examples"]))

    return nodes.definition_list_item("", node, node_definition)


def _field_node(name: str, body: nodes.Element) -> nodes.field:
    """Documentation text: "<name>: <body>" """
    return nodes.field(
        "",
        nodes.field_name(text=name),
        nodes.field_body("", body),
    )


def _term_node(name: str, is_required: bool) -> nodes.term:
    """Documentation text: "<name>" or "<name>*" """
    if not is_required:
        return nodes.term(text=name)
    return nodes.term("", name, nodes.strong("", "*", classes=["ewokssphinx-required"]))


def _examples_node(examples: list[Any]) -> nodes.container:
    """Documentation text:

    .. code-block::

        Examples:
            'translation'
            'rigid'
    """
    example_list = nodes.bullet_list()
    for example in examples:
        example_list.append(nodes.list_item("", nodes.Text(repr(example))))

    return nodes.container(
        "",
        nodes.Text("Examples:"),
        example_list,
        classes=["ewokssphinx-examples"],
    )
