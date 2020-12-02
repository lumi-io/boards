# Flask Test Configuration file
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_DB = os.getenv('MONGODB_TEST_DB')
MONGODB_HOST = os.getenv('MONGODB_TEST_HOST')
MONGODB_PORT = int(os.getenv('MONGODB_TEST_PORT'))
MONGODB_USERNAME = os.getenv('MONGODB_TEST_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_TEST_PASSWORD')