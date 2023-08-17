import os
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv('ENVIRONMENT')
channel = os.getenv('CHANNEL')
project_id = os.getenv('PROJECT_ID')
api_token = os.getenv('AUTH_TOKEN')
