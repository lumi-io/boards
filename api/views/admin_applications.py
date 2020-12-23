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
    pass


@admin_applications.route('/admin/postings/<posting_id>/applications/<applicant_id>', methods=['GET'])
def read_specific_application(posting_id, applicant_id):
    """ Endpoint that gets a specific application of a posting """
    pass

@admin_applications.route('/admin/postings/<posting_id>/applications/<applicant_id>', methods=['PATCH'])
def edit_specific_application(posting_id, applicant_id):
    """ Endpoint that edits a specific application of a posting """
    pass

@admin_applications.route('/admin/postings/<posting_id>/applications/<applicant_id>', methods=['DELETE'])
def delete_specific_application(posting_id, applicant_id):
    """ Endpoint that deletes a specific application of a posting """
    pass