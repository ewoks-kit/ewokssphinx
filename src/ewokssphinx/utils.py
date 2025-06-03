from typing import Sequence, Tuple

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


def field_list(
    title: str,
    fields: Sequence[Tuple[str, str]],
):
    return nodes.field(
        "",
        nodes.field_name(text=title),
        nodes.field_body(
            "",
            nodes.bullet_list(
                "",
                *(
                    nodes.list_item(
                        "",
                        nodes.strong("", field),
                        nodes.Text(description),
                    )
                    for field, description in fields
                ),
            ),
        ),
    )
