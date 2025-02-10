from sphinx.testing import restructuredtext
from docutils import nodes

from .conftest import assert_node, assert_field_node


def test_ewokstasks(app):
    parsed_nodes = restructuredtext.parse(
        app, ".. ewokstasks:: ewokssphinx.tests.dummy_tasks"
    )

    assert len(parsed_nodes) == 3
    assert_node(parsed_nodes[0], nodes.title, "MyTask")
    assert_node(parsed_nodes[1], nodes.paragraph, "My task documentation")
    assert_node(parsed_nodes[2], nodes.field_list)
    assert_field_node(
        parsed_nodes[2][0],
        name="Identifier",
        value="ewokssphinx.tests.dummy_tasks.MyTask",
    )
    assert_field_node(
        parsed_nodes[2][1],
        name="Task type",
        value="class",
    )
    assert_field_node(
        parsed_nodes[2][2],
        name="Required inputs",
        value="a, b, c",
    )
    assert_field_node(
        parsed_nodes[2][3],
        name="Optional inputs",
        value="d, e",
    )
    assert_field_node(
        parsed_nodes[2][4],
        name="Outputs",
        value="error, result",
    )
