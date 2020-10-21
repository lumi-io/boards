import os
import logging

from flask import Flask, request
# from flask_migrate import Migrate

# why we use application factories http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
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

    # import and register blueprints
    from api.views import main
    # from api.views import filename here

    # Why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    app.register_blueprint(main.main)

    # register error Handler
    # app.register_error_handler(Exception, all_exception_handler)

    return app
