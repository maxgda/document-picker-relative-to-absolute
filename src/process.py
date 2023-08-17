import json

import requests

from configuration import environment, project_id, channel, api_token
from src.constants import app_json_headers, prefix
from src.get_data import get_component_groups, get_components


def get_all_relative_pickers():
    matching_components = {}
    groups = get_component_groups()
    for group in groups:
        components = get_components(group)
        get_link_picker_parameters(components, matching_components)
    return matching_components


def batch_component_config_to_absolute(matching_components):
    for matching_component in matching_components.items():
        component_id = matching_component[0]
        pre_matched_parameters = matching_component[1]
        # get_component - to get its x-resource-id
        group_name, component_name = component_id.split('/')
        get_component_url = (f"https://{environment}.bloomreach.io/management/site/v1/channels/"
                             f"{channel}-{project_id}/component_groups/{group_name}/components/{component_name}")
        response = requests.get(get_component_url, headers=app_json_headers)
        x_resource_version = response.headers.get('x-resource-version')

        component = response.json()
        parameters = component.get('parameters')
        for parameter in parameters:
            if parameter.get('name') in pre_matched_parameters:
                picker_configuration = parameter.get('config')
                picker_configuration['relative'] = False
                # change intial path
                # change root path

        put_component_url = (f"https://{environment}.bloomreach.io/management/site/v1/channels/"
                             f"{channel}-{project_id}/component_groups/{group_name}/components/{component_name}")

        put_component_data = json.dumps(component)
        put_component_headers = {
            'Content-Type': 'application/json',
            'X-Resource-Version': x_resource_version,
            'x-auth-token': api_token
        }

        response = requests.put(put_component_url, headers=put_component_headers, data=put_component_data)

        print(response.text)


def is_relative(parameter):
    component_picker_field = "cms-pickers/documents-only"
    config = parameter.get('config')
    if config:
        is_picker = config.get('pickerConfiguration') == component_picker_field
        is_picker_relative = config.get('relative')
        return is_picker and is_picker_relative


def to_absolute(page, matching_components):
    for container in page.get('containers', []):
        components = container.get('components', [])

        for component in components:
            component_definition = component.get('componentDefinition', '')
            component_configurations = component.get('componentConfigurations', [])

            if component_definition in matching_components:
                print("Matching Component:")
                print("Component Definition:", component_definition)

                predefined_params = matching_components[component_definition]

                for config in component_configurations:
                    parameters = config.get('parameters', {})
                    for param in parameters:
                        param_name = param.get('name')
                        print("Parameter Name:", param_name)
                        if param_name in predefined_params:
                            param_value = param.get('value')
                            print("Parameter Value:", param_value)
                            if not param_value.startswith(prefix):
                                prefixed_param_value = prefix + param_value
                                param['value'] = prefixed_param_value
                                print("Parameter Value after modify:", prefixed_param_value)
                        print("---")

                print("====")
    return page


def get_link_picker_parameters(data, matching_components):
    for component in data:
        matching_parameters = []
        component_id = component.get('id')
        parameters = component.get('parameters')
        for parameter in parameters:
            if is_relative(parameter):
                if param_name := parameter.get('name'):
                    matching_parameters.append(param_name)
        if matching_parameters:
            matching_components[component_id] = matching_parameters
    print("Components and their matching parameters with pickerConfiguration")
    print(json.dumps(matching_components, indent=4))
    return matching_components
