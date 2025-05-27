from .ewoks_task_directive import EwoksTaskDirective
from .documenters import EwoksClassTaskDocumenter


def setup(app):
    app.add_directive("ewokstasks", EwoksTaskDirective)
    app.setup_extension("sphinx.ext.autodoc")  # Require autodoc extension
    app.add_autodocumenter(EwoksClassTaskDocumenter)
