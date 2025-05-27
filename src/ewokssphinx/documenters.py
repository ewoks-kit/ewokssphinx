from __future__ import annotations


from typing import Any, Optional
from docutils.statemachine import StringList


from ewokscore import Task
from sphinx.ext.autodoc import ClassDocumenter


class EwoksClassTaskDocumenter(ClassDocumenter):

    objtype = "ewoks_classtask"
    directivetype = ClassDocumenter.objtype
    priority = 10 + ClassDocumenter.priority
    option_spec = dict(ClassDocumenter.option_spec)

    @classmethod
    def can_document_member(
        cls, member: Any, membername: str, isattr: bool, parent: Any
    ) -> bool:
        try:
            return issubclass(member, Task)
        except TypeError:
            return False

    def add_directive_header(self, sig: str) -> None:
        super().add_directive_header(sig)
        self.add_line("   :final:", self.get_sourcename())

    def add_content(
        self,
        more_content: Optional[StringList],
    ) -> None:

        super().add_content(more_content)

        source_name = self.get_sourcename()
        task: Task = self.object
        self.add_line("", source_name)

        self.add_line("Inputs", source_name)
        for input in task.required_input_names():
            self.add_line(f"**{input}**", source_name)

        self.add_line("Outputs", source_name)
        for output in task.output_names():
            self.add_line(f"**{output}**", source_name)
