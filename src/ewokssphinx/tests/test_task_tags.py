from docutils import nodes
from sphinx.testing import restructuredtext


def test_ewokstasks_tags(app):
    parsed_nodes = restructuredtext.parse(
        app,
        """.. ewokstasks:: ewokssphinx.tests.dummy_tasks_tags
              :task-type: class
        """,
    )

    assert _task_tags(parsed_nodes) == {
        "XrfTask": ["imaging", "xrf"],
        "XasTask": ["xas"],
        "UntaggedTask": [],
    }


def _task_tags(document: nodes.document) -> dict[str, list[str]]:
    """Map task names to their tags."""
    tags = {}
    for field_list in document.findall(nodes.field_list):
        task_name = field_list.parent.next_node(nodes.title).astext()
        tags[task_name] = [
            node.astext()
            for node in field_list.findall(nodes.literal)
            if "ewokssphinx-tag" in node["classes"]
        ]
    return tags
