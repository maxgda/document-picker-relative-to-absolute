import io
import sys
import time
import zipfile

import requests

from configuration import environment, channel, project_id
from src.constants import app_json_headers, batch_export_request_body, auth_token_headers


# ABANDONED - Status of a batch job that did not stop properly and can not be restarted.
# COMPLETED - The batch job has successfully completed its execution.
# FAILED    - Status of a batch job that has failed during its execution.
# STARTED   - Status of a batch job that is running.
# STARTING  - Status of a batch job prior to its execution.
# STOPPED   - Status of a batch job that has been stopped by request.
# STOPPING  - Status of batch job waiting for a step to complete before stopping the batch job.
# UNKNOWN   - Status of a batch job that is in an uncertain state.
class Status:
    STARTING = "STARTING"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"


def export():
    export_url = f"https://{environment}.bloomreach.io/management/content-export/v1"

    export_start_response = requests.post(export_url,
                                          headers=app_json_headers,
                                          data=batch_export_request_body)
    export_start_response.raise_for_status()
    if export_start_response.status_code == 201:
        export_operation = export_start_response.json()
        operation_id = export_operation.get("operationId")

        operation_url = f"{export_url}/operations/{operation_id}"
        operation_status = export_operation.get("status")
        while operation_status == Status.STARTING or operation_status == Status.STARTED:
            operation_status_resp = requests.get(operation_url, headers=app_json_headers)
            operation_status = operation_status_resp.json().get("status")
            time.sleep(0.4)  # let the operation complete
        if operation_status == Status.COMPLETED:
            get_exported_file_url = f"{operation_url}/files"
            exported_file_response = requests.get(get_exported_file_url, headers=auth_token_headers)
            exported_file_response.raise_for_status()
            if exported_file_response.status_code == 200:
                octet_stream_data = exported_file_response.content
                zip_stream = io.BytesIO(octet_stream_data)
                with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
                    ndjson_file_name = next(name for name in zip_ref.namelist() if name.endswith('.ndjson'))
                    return zip_ref.read(ndjson_file_name).decode('utf-8').strip().split('\n')


def get_component_groups(): return get_data(api_url_component_group)


def get_components(group):
    group_name = group['name']
    api_url_component = f"{api_url_component_group}/{group_name}/components"
    return get_data(api_url_component)


api_url = f"https://{environment}.bloomreach.io/management/site/v1/channels/"
api_url_component_group = f"{api_url}{channel}-{project_id}/component_groups"


def get_data(url):
    try:
        response = requests.request("GET", url, headers=app_json_headers)
        if response.status_code >= 400:
            response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print("HTTP Error:", http_err)
        sys.exit(1)
    except requests.exceptions.RequestException as req_err:
        print("Request Exception:", req_err)
        sys.exit(1)
    except ValueError as val_err:
        print("JSON Decoding Error:", val_err)
        sys.exit(1)
