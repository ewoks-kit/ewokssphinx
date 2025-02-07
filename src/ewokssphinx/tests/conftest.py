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
