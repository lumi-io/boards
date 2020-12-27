from flask import Blueprint, jsonify, request, make_response
from bson.objectid import ObjectId
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.job_post import validate_job
from api import mongo, flask_bcrypt, jwt

job_post = Blueprint("job_post", __name__)  # initialize blueprint
postings = mongo.db.postings


def return_exception(e):
    response_object = {
        "status": False,
        "message": str(e)
    }
    return jsonify(response_object)


@job_post.route('/admin/postings/create', methods=['POST'])
def create_job():
    """ Endpoint to create a new job posting """
    # Validates if the format is correct
    data = validate_job(request.get_json())

    if data['ok']:
        data = data['data']

        # By default, there should be no applications inside a job post
        data["application"] = []
        try:
            postings.insert_one(data)
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
        return make_response(jsonify(response_object), 400)


@job_post.route('/admin/postings', methods=['GET'])
def get_all_postings():
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
def get_specific_posting(posting_id):
    """ Endpoint that gets information of specific job post based on id """
    try:
        posting_info = postings.find_one({"_id": ObjectId(posting_id)})
        if not posting_info:
            response_object = {
                "status": False,
                "message": 'Posting ID not found.'
            }
            return make_response(jsonify(response_object), 404)

        response_object = {
            "status": True,
            "postingInfo": posting_info,
            "message": 'Posting found.'
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)

@job_post.route('/admin/postings/<posting_id>', methods=['DELETE'])
def delete_specific_posting(posting_id):
    try:
        delete_response = postings.remove({"postingKey": ObjectId(posting_id)})
        if not delete_response:
            response_object = {
                "status": False,
                "message": 'Delete unsuccessful. Posting ID not found.'
            }
            return make_response(jsonify(response_object), 404)

        response_object = {
            "status": True,
            "message": "Posting " + posting_id + " deleted."
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        return make_response(return_exception(e), 400)
