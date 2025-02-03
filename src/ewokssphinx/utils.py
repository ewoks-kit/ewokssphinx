from docutils import nodes
from docutils.nodes import Node


def field(name: str, value: str) -> Node:
    return nodes.field(
        "",
        nodes.field_name(text=name),
        nodes.field_body(
            "",
            nodes.paragraph("", text=value),
        ),
    )
