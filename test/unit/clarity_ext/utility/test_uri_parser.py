import unittest
from test.unit.clarity_ext.mock.repository.process_243643_sn1 import contents as mock_dictionary

from clarity_ext.utility.uri_parser_mock import URIParser

TEST_PROCESS_URI = "https://lims-staging.snpseq.medsci.uu.se/api/v2/processes/24-3643"


class URIParserTests(unittest.TestCase):

    def setUp(self):
        self.parser = URIParser()

    def test_fetch_xml(self):
        xml = self.parser.get_xml(TEST_PROCESS_URI, mock_dictionary)
        self.assertEqual(1,1, xml)

if __name__ == '__main__':
    unittest.main()
