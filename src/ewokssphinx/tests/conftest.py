import json

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.fixture(scope="session")
def app(tmp_path_factory):
    srcdir = tmp_path_factory.mktemp("app")
    with open(srcdir / "conf.py", "w") as conf:
        conf.write('extensions = ["ewokssphinx"]')
    app = SphinxTestApp(
        "html", srcdir=srcdir, docutils_conf="[readers]\ndocinfo_xform: no"
    )

    return app


@pytest.fixture(scope="session")
def app_with_cache(tmp_path_factory):
    srcdir = tmp_path_factory.mktemp("app_with_cache")
    json_cache_path = srcdir / "discovered_ewoks_tasks.json"
    with open(srcdir / "conf.py", "w") as conf:
        conf.write('extensions = ["ewokssphinx"]\n')
        conf.write(f'ewokssphinx_task_cache_path = "{json_cache_path}"\n')
        conf.write("ewokssphinx_ignore_discovery_error = True\n")

    task = {
        "task_name": "MyNonExistingTask",
        "task_identifier": "ewoksnoexisting.tasks.MyNonExistingTask",
        "task_type": "class",
        "description": "My non-existing task documentation",
        "required_input_names": ["a", "b", "c"],
        "optional_input_names": ["d", "e"],
        "output_names": ["error", "result"],
        "inputs": [],
        "outputs": [],
    }
    cache = {"ewoksnoexisting.tasks.MyNonExistingTask": {"class": [task]}}
    with open(json_cache_path, "w") as fp:
        json.dump(cache, fp)

    app = SphinxTestApp(
        "html", srcdir=srcdir, docutils_conf="[readers]\ndocinfo_xform: no"
    )

    return app
