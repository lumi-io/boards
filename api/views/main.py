from flask import Blueprint
# from flask import request
# from api.models import db, Person, Email

main = Blueprint("main", __name__)  # initialize blueprint


# function that is called when you visit /
@main.route("/")
def index():
    return "<h1>Hello Worldd!</h1>"


# function that is called when you visit /persons
@main.route("/persons", methods=["GET"])
def get_persons():
    # persons = Person.query.all()
    # return create_response(data={"persons": serialize_list(persons)})
    # pass
    return "test"
