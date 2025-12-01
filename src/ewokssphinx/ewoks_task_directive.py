import logging

from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

from .ewoks_task_utils import cached_tasks
from .ewoks_task_utils import discover_tasks
from .sphinx_task_utils import task_nodes

logger = logging.getLogger(__name__)


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

        try:
            local_tasks = discover_tasks(module_pattern, task_type, ignore_import_error)
        except Exception as ex:
            if not self.config.ewokssphinx_ignore_discovery_error:
                raise
            logger.error(f"Task discovery '{module_pattern}' failed: {ex}")
            local_tasks = []

        tasks = cached_tasks(
            local_tasks,
            self.config.ewokssphinx_task_cache_path,
            module_pattern,
            task_type,
        )

        task_sections = task_nodes(self, tasks)
        return task_sections
