from flask import Blueprint, jsonify, request, make_response
from bson.objectid import ObjectId
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.application import validate_application
from api import mongo, flask_bcrypt, jwt

application = Blueprint("application", __name__)  # initialize blueprint
applications = mongo.db.applications
"how to applications connect with job_posting"

def return_exception(e):
    response_object = {
        "status": False,
        "message": str(e)
    }
    return jsonify(response_object)


@application.route('/user/applications/create', methods=['POST'])
def create_application():
    """ Endpoint to create a new job posting """
    # Validates if the format is correct
    data = validate_application(request.get_json())

    if data['ok']:
        data = data['data']

        # By default, there should be no applications inside a job post
        try:
            applications.insert_one(data)
            response_object = {
                "status": True,
                "message": 'Application submitted.'
            }
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            return make_response(return_exception(e), 400)

    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'.format(data['message'])
        }
        return make_response(jsonify(response_object), 400)


@application.route('/admin/applications', methods=['GET'])
def get_all_applications():
    """ Endpoint that gets all titles to be read by the default page """
    all_applications = []
    try:
        for application in applications.find():
            all_applications.append(application)

        response_object = {
            "status": True,
            "allApplications": all_applications,
            "message": 'All postings received.'
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)


@application.route('/admin/applications/<application_id>', methods=['GET'])
def get_specific_application(application_id):
    """ Endpoint that gets information of specific application based on id """
    "is id default???"
    try:
        application_info = applications.find_one({"_id": ObjectId(application_id)})
        if not application_info:
            response_object = {
                "status": False,
                "message": 'Application ID not found.'
            }
            return make_response(jsonify(response_object), 404)

        response_object = {
            "status": True,
            "applicationInfo": application_info,
            "message": 'Application found.'
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)
