import os
import json
import datetime
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(test_config=None):
    app = Flask(__name__)
    jwt = JWTManager(app)
    flask_bcrypt = Bcrypt(app)

    # MongoDB Configuration
    print("Retrieving configuration variables.")
    app.config.from_pyfile('config.py')
    print("Connecting to MongoDB instance.")

    app.config["MONGO_URI"] = "mongodb+srv://"+app.config["MONGODB_USERNAME"] + \
        ":"+app.config["MONGODB_PASSWORD"]+"@"+app.config["MONGODB_HOST"]
    try:
        mongo.init_app(app)
    except Exception as e:
        print(e)

    print("MongoDB connected.")

    # import and register blueprints
    from api.views import main
    from api.views import admin_auth
    # from api.views import filename here

    # Why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    print("Registering Flask Blueprints.")
    app.register_blueprint(main.main)
    app.register_blueprint(admin_auth.admin_auth)

    # register error Handler
    # app.register_error_handler(Exception, all_exception_handler)

    return app
