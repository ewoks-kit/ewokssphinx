from pydantic import BaseModel

from ewokssphinx.ewoks_task_utils import _extract_submodels


class Type1(BaseModel):
    pass


class SubType1(BaseModel):
    pass


class SubSubType(BaseModel):
    pass


class SubType2(BaseModel):
    var: dict[str, SubSubType]


class Type2(BaseModel):
    var: tuple[SubType2 | SubType1]


Annotation = Type1 | list[SubType2] | dict[str, list[int | Type2]]


def test_extract_type():

    assert list(_extract_submodels(Annotation).keys()) == [
        "ewokssphinx.tests.test_utils.Type1",
        "ewokssphinx.tests.test_utils.SubType2",
        "ewokssphinx.tests.test_utils.SubSubType",
        "ewokssphinx.tests.test_utils.Type2",
        "ewokssphinx.tests.test_utils.SubType1",
    ]


def test_extract_type_inputs():
    from ewokssphinx.tests.dummy_tasks_nested import Inputs

    assert list(_extract_submodels(Inputs).keys()) == [
        "ewokssphinx.tests.dummy_tasks_nested.Coordinates",
        "ewokssphinx.tests.dummy_tasks_nested.Planet",
    ]
