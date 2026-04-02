from pydantic import BaseModel

from ewokssphinx.ewoks_task_utils import _extract_submodels


class Type1(BaseModel):
    pass


class Type2(BaseModel):
    pass


class Type3a(BaseModel):
    pass


class Type3b(BaseModel):
    var: dict[str, Type3a]


class Type3(BaseModel):
    var: tuple[Type3b | Type2]


Annotation = Type1 | list[Type2] | dict[str, list[int | Type3]]


def test_extract_type():

    assert sorted(_extract_submodels(Annotation).keys()) == [
        "ewokssphinx.tests.test_utils.Type1",
        "ewokssphinx.tests.test_utils.Type2",
        "ewokssphinx.tests.test_utils.Type3",
        "ewokssphinx.tests.test_utils.Type3a",
        "ewokssphinx.tests.test_utils.Type3b",
    ]


def test_extract_type_inputs():
    from ewokssphinx.tests.dummy_tasks_nested import Inputs

    assert sorted(_extract_submodels(Inputs)) == [
        "ewokssphinx.tests.dummy_tasks_nested.Coordinates",
        "ewokssphinx.tests.dummy_tasks_nested.Planet",
    ]
