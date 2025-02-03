from .ewoks_task_directive import EwoksTaskDirective


def setup(app):
    app.add_directive("ewokstasks", EwoksTaskDirective)
