from flask import Blueprint, jsonify, request, make_response
from bson.objectid import ObjectId
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.application import validate_application
from api import mongo, flask_bcrypt, jwt
from api.views.upload_testing import get_bucket, get_buckets_list
import boto3

application = Blueprint("application", __name__)  # initialize blueprint
applications = mongo.db.applications
"how to applications connect with job_posting"

def return_exception(e):
    response_object = {
        "status": False,
        "message": str(e)
    }
    return jsonify(response_object)

@application.route('/user/applications/upload', methods=['POST'])
def upload(acl="public-read"):
    resume_file = request.files['resume']
    profile_pic_file = request.files['profile-pic']
    video_file = request.files['elevator-pitch']
    s3_client = boto3.client('s3')
    success = 'files uploaded.'
    if resume_file:
        try:
            file = resume_file
            s3_client.upload_fileobj(
                file, 
                'resume-testing-ats', 
                'resume/{}'.format(file.filename), 
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                })
        except Exception as e:
            return make_response(return_exception(e), 400)
    if profile_pic_file:
        try:
            file = profile_pic_file
            s3_client.upload_fileobj(
                file, 
                'resume-testing-ats', 
                'profile-pic/{}'.format(file.filename), 
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                })
        except Exception as e:
            return make_response(return_exception(e), 400)
    if video_file:
        try:
            file = video_file
            s3_client.upload_fileobj(
                file, 
                'resume-testing-ats', 
                'elevator-pitch/{}'.format(file.filename), 
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                })
            response_object = {
                        "status": True,
                        "message": success
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