import os
import json

from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

from .ewoks_utils import discover_tasks
from .sphinx_utils import task_nodes


def _task_type_option(argument):
    return directives.choice(argument, ("class", "method", "ppfmethod"))


class EwoksTaskDirective(SphinxDirective):
    required_arguments = 1
    option_spec = {
        "task-type": _task_type_option,
        "ignore-import-error": directives.flag,
    }

    def run(self):
        module_pattern = self.arguments[0]
        task_type = self.options.get("task-type")
        ignore_import_error = "ignore-import-error" in self.options

        tasks = discover_tasks(module_pattern, task_type, ignore_import_error)

        filename = os.environ["EWOKSSPHINX_JSON_PATH"]

        nodes = task_nodes(self, list(tasks.values()))

        return nodes
