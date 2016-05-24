import unittest
from clarity_ext_scripts.dilution.repeat_dilution import Extension
from test.unit.clarity_ext.mock.repeat_dilution_mock import RepeatDilutionMock


class RepeatDilutionTest(unittest.TestCase):

    def setUp(self):
        self.mock = RepeatDilutionMock()
        self.extension = Extension(self.mock.context)

    def tearDown(self):
        self.mock.clean_up()

    def test_nothing(self):
        self.assertEqual(1,1)
