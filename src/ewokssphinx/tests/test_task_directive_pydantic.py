from docutils import nodes
from sphinx.testing import restructuredtext

from .test_utils import assert_node
from .test_utils import assert_task_preamble


def test_ewokstasks_with_pydantic_input_model(app):
    parsed_nodes = restructuredtext.parse(
        app,
        """.. ewokstasks:: ewokssphinx.tests.dummy_tasks_pydantic
              :task-type: class
        """,
    )

    assert len(parsed_nodes) == 4
    assert_task_preamble(
        parsed_nodes,
        "ewokssphinx.tests.dummy_tasks_pydantic.FindLocation",
        """Finds a location given the GPS coordinates""",
        "class",
    )
    definition_list_node = parsed_nodes[-1]
    container_node = definition_list_node[0]

    input_list = container_node[0]
    input_term, input_definition = input_list
    assert_node(input_term, nodes.term, "Inputs:")
    assert_node(input_definition, nodes.definition)

    assert_node(input_definition[0][0][0], nodes.term, "planet : str= Earth")
    assert_node(input_definition[0][1][0], nodes.term, "latitude* : int")
    assert_node(input_definition[0][2][0], nodes.term, "longitude* : float")

    longitude_definition = input_definition[0][2][1]
    longitude_description, longitude_examples = longitude_definition
    longitude_examples_title, longitude_examples = longitude_examples
    assert_node(longitude_description, nodes.paragraph)
    assert_node(longitude_description[0], nodes.Text, "Longitude of the GPS point. ")
    assert_node(longitude_description[1], nodes.strong, "In degrees.")
    assert_node(longitude_examples_title, nodes.Text, "Examples:")
    for longitude_example, value in zip(longitude_examples, [-90, 0, 90]):
        assert_node(longitude_example[0], nodes.Text, repr(value))

    output_list = container_node[1]
    output_term, output_definition = output_list
    assert_node(output_term, nodes.term, "Outputs:")
    assert_node(output_definition, nodes.definition)

    assert_node(output_definition[0][0][0], nodes.term, "location : str")
    assert_node(output_definition[0][1][0], nodes.term, "error : Exception | None")

    location_definition = output_definition[0][0][1]
    (location_definition,) = location_definition
    assert_node(
        location_definition[0],
        nodes.Text,
        "Name of the closest city or location to the given coordinates",
    )
