from pathlib import Path

import sphinx
from sphinx.application import Sphinx
from sphinx.config import Config

from .ewoks_task_directive import EwoksTaskDirective

_STATIC_DIR = Path(__file__).parent / "static"


def setup(app: Sphinx):
    app.add_directive("ewokstasks", EwoksTaskDirective)

    app.add_config_value(
        "ewokssphinx_task_cache_path",
        default=None,
        types=str,
        rebuild="env",
        description="JSON path to cache Ewoks task descriptions. "
        "Task discovery overrides the cached descriptions. "
        "Useful when task discovery needs to be done in different python environments.",
    )

    app.add_config_value(
        "ewokssphinx_ignore_discovery_error",
        default=False,
        types=bool,
        rebuild="env",
        description="Ignore Ewoks task discovery errors. ",
    )

    if sphinx.version_info >= (9, 1):
        app.add_static_dir(_STATIC_DIR)
    else:
        app.connect("config-inited", _add_static_path)
    app.add_css_file("ewokssphinx.css")
    app.add_js_file("ewokssphinx.js")

    return {
        "version": "1.0",
        "parallel_read_safe": False,  # Reading source files
        "parallel_write_safe": True,  # Writing output files
    }


def _add_static_path(app: Sphinx, config: Config) -> None:
    config.html_static_path.append(str(_STATIC_DIR))
