from ewokscore import Task


class XrfTask(Task, output_names=["result"], tags=["xrf", "imaging"]):
    """XRF task"""

    def run(self):
        pass


class XasTask(Task, output_names=["result"], tags=["xas"]):
    """XAS task"""

    def run(self):
        pass


class UntaggedTask(Task, output_names=["result"]):
    """Untagged task"""

    def run(self):
        pass
