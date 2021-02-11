from flask import Blueprint, jsonify, request, make_response
from bson.objectid import ObjectId
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.job_post import validate_job
from api import mongo, flask_bcrypt, jwt

import json
import boto3

job_post = Blueprint("job_post", __name__)  # initialize blueprint
postings = mongo.db.postings
applications = mongo.db.applications


def return_exception(e):
    response_object = {
        "status": False,
        "message": str(e)
    }
    return jsonify(response_object)


@job_post.route('/admin/postings/create', methods=['POST'])
# @jwt_required
def create_posting():
    """ Endpoint to create a new job posting """
    # Validates if the format is correct
    data = validate_job(request.get_json())

    if data['ok']:
        data = data['data']

        # By default, there should be no applications inside a job post
        try:
            # Inserts new posting doc in posting collection
            posting_id = postings.insert_one(data)
            # Creates corresponding application data with posting doc id
            app_doc = {"postingKey": ObjectId(posting_id.inserted_id), "applications": []}
            # Inserts corresponding application doc in applications collection
            applications.insert_one(app_doc)

            # Creates a new folder in the S3 bucket corresponding to a posting
            s3 = boto3.client('s3')
            bucket_name = "resume-testing-ats"
            folder_name = str(posting_id.inserted_id)
            s3.put_object(Bucket=bucket_name, Key=(folder_name+'/'))
            s3.put_object(Bucket=bucket_name, Key=(folder_name+'/resume/'))
            s3.put_object(Bucket=bucket_name, Key=(folder_name+'/profile-pic/'))
            s3.put_object(Bucket=bucket_name, Key=(folder_name+'/elevator-pitch/'))

            response_object = {
                "status": True,
                "message": 'New job post created successfully.'
            }
            return make_response(jsonify(response_object), 200)
        except Exception as e:
            return make_response(return_exception(e), 400)

    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'.format(data['message'])
        }
        return make_response(jsonify(response_object), 200)


@job_post.route('/admin/postings', methods=['GET'])
# @jwt_required
def read_all_postings():
    """ Endpoint that gets all titles to be read by the default page """
    all_postings = []
    try:
        for posting in postings.find():
            all_postings.append(posting)

        response_object = {
            "status": True,
            "allPostings": all_postings,
            "message": 'All postings received.'
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)


@job_post.route('/admin/postings/<posting_id>', methods=['GET'])
# @jwt_required
def read_specific_posting(posting_id):
    """ Endpoint that gets information of specific job post based on id """
    try:
        posting_info = postings.find_one({"_id": ObjectId(posting_id)})
        if not posting_info:
            response_object = {
                "status": False,
                "message": 'Posting ID not found.'
            }
            return make_response(jsonify(response_object), 200)

        response_object = {
            "status": True,
            "postingInfo": posting_info,
            "message": 'Posting found.'
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)

@job_post.route('/admin/postings/<posting_id>', methods=['PATCH'])
# @jwt_required
def edit_specific_posting(posting_id):
    """ Endpoint that edits a specific posting """
    try:
        updated_data = request.get_json()
        update_response = postings.update_one(
            # Finds posting doc based on posting_id
            {
                "_id": ObjectId(posting_id)
            },
            # Updates field in doc with given value
            { 
                "$set": updated_data 
            } 
        )


        if update_response is None:
            response_object = {
                "status": False,
                "message": 'Posting with id ' + posting_id + ' not found.'
            }
            return make_response(jsonify(response_object), 200)

        response_object = {
            "status": True,
            "message": 'Posting updated.'
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)

@job_post.route('/admin/postings/<posting_id>', methods=['DELETE'])
@jwt_required
def delete_specific_posting(posting_id):
    """ Endpoint that deletes a specific posting """
    try:
        # Finds and deletes posting doc with given id
        deleted_doc = postings.delete_one(
            { "_id": ObjectId(posting_id) }
        )
        if deleted_doc is None:
            response_object = {
                "status": False,
                "message": 'Posting with id ' + posting_id + ' not found.'
            }
            return make_response(jsonify(response_object), 200)

        response_object = {
            "status": True,
            "message": 'Posting deleted.'
        }
        return make_response(jsonify(response_object), 200)
    
    except Exception as e:
        return make_response(return_exception(e), 400)
