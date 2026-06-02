from sphinx.testing import restructuredtext

from .utils import assert_task_nodes


def test_cache(app_with_cache):
    parsed_nodes = restructuredtext.parse(
        app_with_cache,
        """
Title
=====

.. ewokstasks:: ewoksnoexisting.tasks.MyNonExistingTask
    :task-type: class
""",
    )
    assert len(parsed_nodes) == 5
    _assert_class_task_nodes(parsed_nodes[1:])


def _assert_class_task_nodes(nodes):
    assert_task_nodes(
        nodes,
        identifier="ewoksnoexisting.tasks.MyNonExistingTask",
        doc="""My non-existing task documentation""",
        task_type="class",
        required_inputs=["a", "b", "c"],
        optional_inputs=["d", "e"],
        outputs=["error", "result"],
    )
