# import os
# import logging

from flask import Flask
from flask_mongoengine import MongoEngine
# from flask import request
# from flask_migrate import Migrate

# why we use application factories
# http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories


def create_app(test_config=None):
    """
    The flask application factory. To run the app somewhere else you can:
    ```
    from api import create_app
    app = create_app()

    if __main__ == "__name__":
        app.run()
    """
    app = Flask(__name__)

    # MongoDB Configuration
    print("Retrieving configuration variables.")
    app.config.from_pyfile('config.py')
    print("Connecting to MongoDB instance.")
    try:
        db = MongoEngine(app)
    except Exception as e:
        print(e)

    print("MongoDB connected.")

    # import and register blueprints
    from api.views import main
    # from api.views import filename here

    # Why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    print("Registering Flask Blueprints.")
    app.register_blueprint(main.main)

    # register error Handler
    # app.register_error_handler(Exception, all_exception_handler)

    return app
