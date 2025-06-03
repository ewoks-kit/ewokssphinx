from typing import Optional, Type
from docutils.nodes import Node
from docutils import nodes
import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.fixture(scope="session")
def app(tmp_path_factory):
    srcdir = tmp_path_factory.mktemp("root")
    with open(srcdir / "conf.py", "w") as conf:
        conf.write('extensions = ["ewokssphinx"]')
    app = SphinxTestApp("html", srcdir=srcdir)

    return app


def assert_node(node, cls: Type[Node], text: Optional[str] = None):
    assert isinstance(node, cls)
    if text is not None:
        assert node.astext() == text


def assert_field_node(node, name: str, value: str):
    assert isinstance(node, nodes.field)
    assert_node(node[0], nodes.field_name, name)
    assert_node(node[1], nodes.field_body, value)


def assert_inputs(node, required_inputs, optional_inputs):
    assert_node(node[0], nodes.field_name, "Inputs")
    assert_node(node[1][0], nodes.bullet_list)

    n_required = len(required_inputs)
    for i in range(n_required):
        assert_node(
            node[1][0][i], nodes.list_item, f"{required_inputs[i]}\n\n [Required]"
        )

    n_optional = len(optional_inputs)
    for i in range(n_optional):
        assert_node(
            node[1][0][n_required + i], nodes.list_item, f"{optional_inputs[i]}\n\n"
        )


def assert_outputs(node, outputs):
    assert_node(node[0], nodes.field_name, "Outputs")
    assert_node(node[1][0], nodes.bullet_list)
    for i, node_item in enumerate(node[1][0]):
        assert_node(node_item, nodes.list_item, f"{outputs[i]}\n\n")


def assert_task_nodes(
    parsed_nodes, name, doc, task_type, required_inputs, optional_inputs, outputs
):
    assert_node(parsed_nodes[0], nodes.title, name)
    if doc is not None:
        assert_node(parsed_nodes[1], nodes.paragraph, doc)
        next_nodes = parsed_nodes[2:]
    else:
        next_nodes = parsed_nodes[1:]
    field_list_nodes = next_nodes[0]
    assert_node(field_list_nodes, nodes.field_list)
    assert_field_node(
        field_list_nodes[0],
        name="Identifier",
        value=(
            "ewokssphinx.tests.dummy_tasks.run"
            if task_type == "ppfmethod"
            else f"ewokssphinx.tests.dummy_tasks.{name}"
        ),
    )
    assert_field_node(
        field_list_nodes[1],
        name="Task type",
        value=task_type,
    )
    assert_inputs(
        next_nodes[1], required_inputs=required_inputs, optional_inputs=optional_inputs
    )
    assert_outputs(next_nodes[2], outputs=outputs)
