
# Bloomreach Content Batch Script
## Converting Document Pickers from Relative to Absolute Paths

This script facilitates the conversion of existing document pickers within a channel, transitioning them from relative paths to absolute paths.

To maintain compatibility with shared content, it is currently necessary to utilize absolute pickers.

For comprehensive instructions on sharing content between channels, refer to the official Bloomreach documentation: [Share Content Between Channels](https://documentation.bloomreach.com/content/docs/share-content-between-channels).

As outlined in the documentation:

"_If you have previously displayed documents on a page and subsequently modify the component configuration, it becomes imperative to re-select those documents to update the associated links._"

The provided script streamlines this process by automating the task.

### How to run
Make sure you have python and pip installed.

Create .env file in the same directory as this readme(root) and specify in it the 4 required environment variables:


```
AUTH_TOKEN = ""
ENVIRONMENT =  "profserv01"
CHANNEL = "max-test"
PROJECT_ID = "vL0tK"
```
for example:
```
AUTH_TOKEN = "very-secret-api-key-generated-in-the-cms"
ENVIRONMENT =  "profserv"
CHANNEL = "max-test"
PROJECT_ID = "vL0tK"
```
activate the venv (virtual environment), sometimes activated automatically by IDE:
```
source ./venv/bin/activate
```
install the requirements in the venv for the script, usually done with the following command:
```
pip3 install -r requirements.txt
```
run the script and follow the prompt.
```
python3 main.py
```

Easiest way is to open this repository in an IDE (PyCharm, IntelliJ with python plugin) and run it through the IDE.

You can also install the required dependencies in requirements.txt to your global python but this is not suggested, 
it is better to use a virtual envrionment to keep your machine clean.
### Features
* Automatically batch exports content from the CMS
* Identifies relative pickers in all component groups of the specified channel
* Can update identified component configuration to absolute
* Updates path of already selected documents in existing pickers on exported pages
* Can export updated export to file
* Can import updated export to specified CMS project.

