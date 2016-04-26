from genologics.config import BASEURI
import os
import inspect
import importlib
import clarity_ext.utility.pathing as pathing

URI_WASTE_PART = "/api/"
MOCK_RELATIVE_PATH = r'test\unit\clarity_ext\mock\repository'
MODULE_LOCATION = "test.unit.clarity_ext.mock.repository."


class URIParser:
    """ A class to take an URI and find contents in mock repository
    """

    def __init__(self):
        pass

    @staticmethod
    def parse_mock_identifier(uri):
        resource = uri[len(BASEURI) + len(URI_WASTE_PART):].replace("/", "_")
        resource = resource.replace("-", "")
        resource = resource.rsplit("?state", 1)[0]
        return resource

    def get_xml(self, uri, mock_dictionary):
        key = self.parse_mock_identifier(uri)
        return mock_dictionary[key]
