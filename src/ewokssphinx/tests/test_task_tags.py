import pytest
from docutils import nodes
from sphinx.testing import restructuredtext

from ..ewoks_task_utils import filter_tasks_by_tags


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


@pytest.mark.parametrize(
    "options,expected",
    [
        (":include-tags: xrf", {"XrfTask"}),
        (":include-tags: xrf, xas", {"XrfTask", "XasTask"}),
        (":exclude-tags: xrf", {"XasTask", "UntaggedTask"}),
        (":include-tags: xrf, xas\n              :exclude-tags: imaging", {"XasTask"}),
    ],
)
def test_ewokstasks_filter_tags(app, options, expected):
    parsed_nodes = restructuredtext.parse(
        app,
        f""".. ewokstasks:: ewokssphinx.tests.dummy_tasks_tags
              :task-type: class
              {options}
        """,
    )

    assert set(_task_tags(parsed_nodes)) == expected


@pytest.mark.parametrize(
    "include_tags,exclude_tags,expected",
    [
        (None, None, ["a", "b", "c"]),
        (["x"], None, ["a", "b"]),
        (None, ["y"], ["a", "c"]),
        (["x"], ["y"], ["a"]),
    ],
)
def test_filter_tasks_by_tags(include_tags, exclude_tags, expected):
    tasks = [
        {"task_name": "a", "tags": ["x"]},
        {"task_name": "b", "tags": ["x", "y"]},
        {"task_name": "c"},
    ]
    filtered = filter_tasks_by_tags(tasks, include_tags, exclude_tags)
    assert [task["task_name"] for task in filtered] == expected


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
