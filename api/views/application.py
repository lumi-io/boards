from flask import Blueprint, jsonify, request, make_response
from bson.objectid import ObjectId
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.application import validate_application
from api import mongo, flask_bcrypt, jwt
# from api.views.upload_testing import get_bucket, get_buckets_list
import boto3
import json
from time import time, ctime

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
def upload(resume_file, profile_pic_file, video_file, acl="public-read"):
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


def update_filenames(posting_id, applicant_id, urls):
    applications.find_and_modify(
        query={
            "postingKey": ObjectId(posting_id),
            "applications.applicantId": ObjectId(applicant_id)
        },
        update={
            "resume": urls[0],
            "profilePic": urls[1],
            "elevatorPitch": urls[2]
        }
    )
    return True

# upload to mongodb in a correct format
# upload both at the same time
@application.route('/user/applications/submit/<posting_id>', methods=['POST'])
def submit_application(posting_id):
    """ Endpoint to append an application to a job posting """
    # Validates if the format is correct
    json_dump = json.dumps(eval(request.form['json']))
    json_object = json.loads(json_dump)
    data = validate_application(json_object)
    data['data']["application_id"] = ObjectId()
    data['data']['timeApplied'] = ctime(time())


    #required files
    resume_file = request.files['resume']
    profile_pic_file = request.files['profilePic']
    video_file = request.files['elevatorPitch']

    #forming urls for the files
    bucket = 'resume-testing-ats'
    region = 'us-east-2'
    folders = ["resume", "profile-pic", "elevator-pitch"]
    file_names = [resume_file.filename, profile_pic_file.filename, video_file.filename]
    urls = []
    for i in range(len(folders)):   
        urls += [f"https://{bucket}.s3.{region}.amazonaws.com/{folders[i]}/{file_names[i]}"]
    
    data['data']["resume"] = urls[0]
    data['data']["profilePic"] = urls[1]
    data['data']["elevatorPitch"] = urls[2]

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
            #upload files to the s3
            upload(resume_file, profile_pic_file, video_file)
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            return make_response(return_exception(e), 400)

    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'.format(data['message'])
        }
        return make_response(jsonify(response_object), 400)