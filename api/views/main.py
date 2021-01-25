from flask import Blueprint
# from flask import request
# from api.models import db, Person, Email
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)

main = Blueprint("main", __name__)  # initialize blueprint


# function that is called when you visit /
@main.route("/")
def index():
    return "<h1>Hello Worldd!</h1>"