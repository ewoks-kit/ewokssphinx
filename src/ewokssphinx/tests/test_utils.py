from pydantic import BaseModel

from ewokssphinx.ewoks_task_utils import extract_submodels


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

    assert extract_submodels("ewokssphinx.tests.test_utils.Annotation") == set(
        [
            "ewokssphinx.tests.test_utils.Type1",
            "ewokssphinx.tests.test_utils.Type2",
            "ewokssphinx.tests.test_utils.Type3",
            "ewokssphinx.tests.test_utils.Type3b",
            "ewokssphinx.tests.test_utils.Type3a",
        ]
    )


def test_extract_type_inputs():
    assert extract_submodels("ewokssphinx.tests.dummy_tasks_nested.Inputs") == set(
        [
            "ewokssphinx.tests.dummy_tasks_nested.Coordinates",
            "ewokssphinx.tests.dummy_tasks_nested.Planet",
        ]
    )
