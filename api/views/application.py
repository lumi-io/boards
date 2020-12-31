from flask import Blueprint, jsonify, request, make_response
from bson.objectid import ObjectId
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.application import validate_application
from api import mongo, flask_bcrypt, jwt
# from api.views.upload_testing import get_bucket, get_buckets_list
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

# @application.route('/user/applications/upload', methods=['POST'])
def upload(acl="public-read"):
    resume_file = request.files['resume']
    profile_pic_file = request.files['profilePic']
    video_file = request.files['elevatorPitch']
    s3_client = boto3.client('s3')
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
                        "message": 'files uploaded.'
            }
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            return make_response(return_exception(e), 400)
    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'
        }
        return make_response(jsonify(response_object), 400)

#should be put in the admin router
@application.route('/user/applications/<bucket_name>', methods=['POST'])    
def delete_all(bucket_name):
    try:
        s3_client = boto3.client('s3')
        files = s3_client.list_objects(Bucket=bucket_name)['Contents']
        for file in files:
            s3_client.delete_objects(Bucket=bucket_name, Key=file["Key"])
    
    except Exception as e:
            return make_response(return_exception(e), 400)


# upload to mongodb in a correct format
# upload both at the same time
@application.route('/user/applications/submit/<posting_id>', methods=['POST'])
def submit_application(posting_id):
    """ Endpoint to append an application to a job posting """
    # Validates if the format is correct
    print(request.form['json'])
    data = validate_application(JSON.stringify(request.form['json']))

    if data['ok']:
        data = data['data']

        # By default, there should be no applications inside a job post
        try:
            applications.update(
                {"postingKey": ObjectId(posting_id)},
                { "$push" : 
                    {"applications": data }
                }
            )
            response_object = {
                "status": True,
                "message": 'Application submitted.'
            }
            # upload()
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            return make_response(return_exception(e), 400)

    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'.format(data['message'])
        }
        return make_response(jsonify(response_object), 400)