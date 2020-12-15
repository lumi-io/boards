# Flask Configuration file
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_DB = os.getenv('MONGODB_DB')
MONGODB_HOST = os.getenv('MONGODB_HOST')
MONGODB_PORT = int(os.getenv('MONGODB_PORT'))
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

# class ProdConfig(Config):
#     FLASK_ENV = 'production'
#     DEBUG = False
#     TESTING = False
#     DATABASE_URI = environ.get('PROD_DATABASE_URI')


# class DevConfig(Config):
#     FLASK_ENV = 'development'
#     DEBUG = True
#     TESTING = True
#     DATABASE_URI = environ.get('DEV_DATABASE_URI')
