from flask import Blueprint, jsonify, request, make_response
from bson.objectid import ObjectId
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.job_post import validate_job
from api import mongo, flask_bcrypt, jwt

admin_applications = Blueprint(
    "admin_applications", __name__)  # initialize blueprint
applications = mongo.db.applications
postings = mongo.db.postings


def return_exception(e):
    response_object = {
        "status": False,
        "message": str(e)
    }
    return jsonify(response_object)


@admin_applications.route('/admin/postings/<posting_id>/applications', methods=['GET'])
def read_all_applications(posting_id):
    """ Endpoint that gets all applications of a posting/job """
    try:
        apps = applications.find_one({"postingKey": ObjectId(posting_id)})

        response_object = {
            "status": True,
            "application": apps,
            "message": 'All applications of posting ' + posting_id + ' received.'
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)


@admin_applications.route('/admin/postings/<posting_id>/applications/<applicant_id>', methods=['GET'])
def read_specific_application(posting_id, applicant_id):
    """ Endpoint that gets a specific application of a posting """
    try:
        apps = applications.find_one({"postingKey": ObjectId(posting_id)})
        apps = apps["applications"]
        for app in apps:
            if ObjectId(applicant_id) == app["applicantId"]:
                response_object = {
                    "status": True,
                    "application": app,
                    "message": 'Application with id ' + posting_id + ' found.'
                }

                return make_response(jsonify(response_object), 200)

        response_object = {
            "status": True,
            "application": None,
            "message": "No application found with the id " + applicant_id + "."
        }

        return make_response(jsonify(response_object), 204)

    except Exception as e:
        return make_response(return_exception(e), 400)


@admin_applications.route('/admin/postings/<posting_id>/applications/<applicant_id>', methods=['PATCH'])
def edit_specific_application(posting_id, applicant_id):
    """ Endpoint that edits a specific application of a posting """
    pass


@admin_applications.route('/admin/postings/<posting_id>/applications/<applicant_id>', methods=['DELETE'])
def delete_specific_application(posting_id, applicant_id):
    """ Endpoint that deletes a specific application of a posting """
    try:
        update_response = applications.update(
            {"postingKey": ObjectId(posting_id)},
            {"$pull": {
                "applications": {
                    "applicantId": ObjectId(applicant_id)
                }
            }}
        )

        if update_response["nModified"] == 0:
            response_object = {
                "status": True,
                "message": "Delete unsuccessful. No application found with the id " + applicant_id + "."
            }

            return make_response(jsonify(response_object), 200)

        response_object = {
            "status": True,
            "message": "Applicant " + applicant_id + " removed."
        }

        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)
