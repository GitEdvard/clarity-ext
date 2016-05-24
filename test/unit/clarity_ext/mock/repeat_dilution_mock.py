from genologics.entities import *

from test.unit.clarity_ext.mock.mock_base import MockBase


class RepeatDilutionMock(MockBase):

    def set_up(self):
        _artifact = Artifact(self.lims, id="out_art1")
        _artifact.udf = {"Concentration": 10,
                         "Edvard is dilution ready": 1}
        self.process.all_outputs().append(_artifact)

        _artifact = Artifact(self.lims, id="out_art2")
        _artifact.udf = {"Concentration": 10,
                         "Edvard is dilution ready": 0}
        self.process.all_outputs().append(_artifact)

        _artifact = Artifact(self.lims, id="in_art1")
        self.process.all_inputs().append(_artifact)

        _artifact = Artifact(self.lims, id="in_art2")
        self.process.all_inputs().append(_artifact)

        

