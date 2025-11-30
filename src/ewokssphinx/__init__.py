from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util.osutil import copyfile

from .ewoks_task_directive import EwoksTaskDirective


def setup(app: Sphinx):
    app.add_directive("ewokstasks", EwoksTaskDirective)

    app.add_config_value(
        "ewokssphinx_json_path",
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

    app.add_css_file("ewokssphinx.css")
    app.connect("build-finished", _copy_css)

    return {
        "version": "1.0",
        "parallel_read_safe": False,  # Reading source files
        "parallel_write_safe": True,  # Writing output files
    }


def _copy_css(app, exception):
    if app.builder.name != "html" or exception:
        return
    static_dir = Path(app.builder.outdir) / "_static"
    copyfile(Path(__file__).parent / "ewokssphinx.css", static_dir / "ewokssphinx.css")
