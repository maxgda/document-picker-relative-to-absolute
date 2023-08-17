import datetime
import json
import io
import os

import requests

import src.constants
from configuration import environment, project_id, channel
from src.constants import auth_token_headers


def export_to_file(ndjson):
    content_path = src.constants.batch_export_source_path
    content_path = content_path.rsplit('/', 1)  # Split the string into segments using the last '/'
    content_path = content_path[-1]
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%d%m%y-%H%M%S')
    filename = f"{channel}-{project_id}-{content_path}{formatted_time}.ndjson"
    directory_path = "file-exports"
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    file_path = os.path.join(directory_path, filename)
    with open(f"{file_path}", 'w') as json_file:
        for data in ndjson:
            json_string = json.dumps(data)
            json_file.write(json_string + '\n')
        print("JSON data has been modified and saved.")


def import_to_cms(ndjson):
    url = f"https://{environment}.bloomreach.io/management/content-import/v1/project/{project_id}"

    ndjson_lines = [json.dumps(item) for item in ndjson]
    ndjson_payload = '\n'.join(ndjson_lines)
    ndjson_file = io.BytesIO(ndjson_payload.encode('utf-8'))

    files = {
        'file': ('data.ndjson', ndjson_file, 'application/octet-stream')
    }

    response = requests.post(url, headers=auth_token_headers, files=files)
    print(response.json())