import unittest
from clarity_ext.utility.uri_parser_mock import URIParser
from clarity_ext.context import ExtensionContextXMLExtracter
from clarity_ext.context import FakingXMLMonkey
from test.unit.clarity_ext.mock.xml.process_243643_sn1 import contents as mock_dictionary

TEST_PROCESS_URI = "https://lims-staging.snpseq.medsci.uu.se/api/v2/processes/24-3643"
TEST_PROCESS_ID = "24-3643"
FIRST_INPUT_ARTIFACT = "https://lims-staging.snpseq.medsci.uu.se/api/v2/artifacts/ENG54A32PA1?state=3902"
FIRST_OUTPUT_ARTIFACT = "https://lims-staging.snpseq.medsci.uu.se/api/v2/artifacts/2-7107?state=3908"


class SaveMockTests(unittest.TestCase):

    def setUp(self):
        self.mock = FakingXMLMonkey(mock_dictionary)
        self.mockify = ExtensionContextXMLExtracter(TEST_PROCESS_ID)
        self.parser = URIParser()
        self.entity_xml_dict = self.mockify.generate_contents_dict()

    def tearDown(self):
        self.mock.reset()

    def test_has_process(self):
        key = self.mockify.current_step.get_mock_identifier()
        self.assertTrue(self.entity_xml_dict.has_key(key))

    def test_dict_number_entries(self):
        self.assertEqual(len(self.entity_xml_dict), 10)

    def test_has_one_input_artifact(self):
        key = self.parser.parse_mock_identifier(FIRST_INPUT_ARTIFACT)
        self.assertTrue(self.entity_xml_dict.has_key(key), key)

    def test_has_one_output_artifact(self):
        key = self.parser.parse_mock_identifier(FIRST_OUTPUT_ARTIFACT)
        self.assertTrue(self.entity_xml_dict.has_key(key), key)


if __name__ == "__main__":
    unittest.main()
