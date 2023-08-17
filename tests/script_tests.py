import unittest
from unittest.mock import Mock, patch

import src.constants
from configuration import channel
from src.constants import prefix
from src.get_data import get_component_groups, get_components, get_data
from src.process import to_absolute


class MyTestCase(unittest.TestCase):

    @patch('src.get_data.get_data')
    def test_get_component_groups(self, mock_get_data):
        mock_get_data.return_value = [{'name': 'group1'}, {'name': 'group2'}]
        groups = get_component_groups()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]['name'], 'group1')
        self.assertEqual(groups[1]['name'], 'group2')

    @patch('src.get_data.get_data')
    def test_get_components(self, mock_get_data):
        mock_get_data.return_value = [{'id': 'comp1'}, {'id': 'comp2'}]
        group = {'name': 'group1'}
        components = get_components(group)
        self.assertEqual(len(components), 2)
        self.assertEqual(components[0]['id'], 'comp1')
        self.assertEqual(components[1]['id'], 'comp2')

    @patch('src.get_data.requests.request')
    def test_get_data_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'sample_data'}
        mock_request.return_value = mock_response
        data = get_data('sample_url')
        self.assertEqual(data, {'data': 'sample_data'})

    def test_relative_to_absolute_transformer(self):
        page = {
            'containers': [
                {
                    'components': [
                        {
                            'componentDefinition': 'comp1',
                            'componentConfigurations': [
                                {
                                    'parameters': [{'name': 'param1', 'value': 'value1'}]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        matching_components = {'comp1': ['param1']}
        transformed_page = to_absolute(page, matching_components)
        self.assertEqual(
            transformed_page['containers'][0]['components'][0]['componentConfigurations'][0]['parameters'][0]['value'],
            f'/content/documents/{channel}/value1')


if __name__ == '__main__':
    unittest.main()



