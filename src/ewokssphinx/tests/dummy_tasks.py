from ewokscore import Task


class MyTask(
    Task,
    input_names=["a", "b", "c"],
    optional_input_names=["d", "e"],
    output_names=["result", "error"],
):
    """My task documentation"""

    def run(self):
        pass
