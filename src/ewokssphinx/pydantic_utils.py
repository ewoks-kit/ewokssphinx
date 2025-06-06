import importlib

from docutils import nodes
from ewokscore.model import BaseInputModel
from pydantic.fields import FieldInfo
from sphinx.util.typing import stringify_annotation

from .utils import field_term


def _import_model(input_model_qual_name: str) -> type[BaseInputModel]:
    module_name, _, model_name = input_model_qual_name.rpartition(".")

    mod = importlib.import_module(module_name)

    return getattr(mod, model_name)


def _pydantic_field_term(name: str, field_info: FieldInfo) -> nodes.term:
    node_term = field_term(name, field_info.is_required())

    if field_info.annotation is not None:
        node_term += [
            nodes.Text(" : "),
            nodes.literal(text=stringify_annotation(field_info.annotation)),
        ]

    if not field_info.is_required():
        node_term.append(
            nodes.literal(
                text=f"= {field_info.default}", classes=["ewokssphinx-default"]
            )
        )

    return node_term


def _pydantic_field_definition(field_info: FieldInfo) -> nodes.definition:
    node_definition = nodes.definition()
    if field_info.description is not None:
        node_definition.append(nodes.Text(field_info.description))

    if field_info.examples:
        example_list = nodes.bullet_list()
        for example in field_info.examples:
            example_list.append(nodes.list_item("", nodes.Text(repr(example))))
        node_definition.append(
            nodes.container(
                "",
                nodes.Text("Examples:"),
                example_list,
                classes=["ewokssphinx-examples"],
            )
        )

    return node_definition


def pydantic_inputs(input_model_qual_name: str) -> nodes.definition_list_item:
    model = _import_model(input_model_qual_name)

    input_definition_list = nodes.definition_list()
    for field_name, field_info in model.model_fields.items():
        input_definition_list.append(
            nodes.definition_list_item(
                "",
                _pydantic_field_term(field_name, field_info),
                _pydantic_field_definition(field_info),
            )
        )

    return nodes.definition_list_item(
        "",
        nodes.term(text="Inputs:", classes=["field-odd"]),
        nodes.definition("", input_definition_list),
        classes=["field-list"],
    )
