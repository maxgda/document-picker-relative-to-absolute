import json

from configuration import channel, api_token

# this is the path from which pages are going to be exported.
# Change this path if you want a smaller scope for example.
batch_export_source_path = f"/content/documents/{channel}/pages/"

# the absolute prefix which will be appended to each path
prefix = f"/content/documents/{channel}/"

# request body for a batch export of pages from the CMS
batch_export_request_body = json.dumps({
    "sourcePath": batch_export_source_path,
    "dataTypes": [
        "page"
    ],
    "branch": "core"
})

# simple json headers
app_json_headers = {
    'Content-Type': 'application/json',
    'x-auth-token': api_token,
}

# simple auth headers
auth_token_headers = {
    'x-auth-token': api_token,
}

