
from clarity_ext.extensions import GeneralExtension


class Extension(GeneralExtension):
    """
    Make marked samples to go through the same step again. Samples are marked for repetition
    by a udf value.
    """

    def execute(self):
        print("Hello repeat")

    def integration_tests(self):
        # The step used during design/last iteration of this extension:
        yield "24-4770"
