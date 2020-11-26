import os
import json
import datetime
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class JSONEncoder(json.JSONEncoder):
    """ extend json-encoder class """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Objects and Instances to be used in other files are placed here
mongo = PyMongo()
app = Flask(__name__)
# https://flask-jwt-extended.readthedocs.io/en/stable/api/
jwt = JWTManager(app)
flask_bcrypt = Bcrypt(app)


def create_app(test_config=None):
    """ Initializes and adds necessary information into the Flask app object """

    app.config['JWT_SECRET_KEY'] = "test"
    app.json_encoder = JSONEncoder
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
    from api.views import job_post
    # from api.views import filename here

    # Why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    print("Registering Flask Blueprints.")
    app.register_blueprint(main.main)
    app.register_blueprint(admin_auth.admin_auth)
    app.register_blueprint(job_post.job_post)

    # register error Handler
    # app.register_error_handler(Exception, all_exception_handler)

    return app
