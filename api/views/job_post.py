from flask import Blueprint, jsonify, request, make_response
# from flask_jwt_extended import (create_access_token, create_refresh_token,
#                                 jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.job_post import validate_job
from api import mongo, flask_bcrypt, jwt

job_post = Blueprint("job_post", __name__)  # initialize blueprint
postings = mongo.db.postings

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
            response_object = {
                "status": False,
                "message": str(e)
            }
            return make_response(jsonify(response_object), 400)

    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'.format(data['message'])
        }
        return make_response(jsonify(response_object), 400)

@job_post.route('/admin/postings', methods=['GET'])
def get_all_titles():
    """ Endpoint that gets all titles to be read by the default page """
    pass
    


# @admin_auth.route('/admin/auth', methods=['POST'])
# def auth_user():
#     """ Endpoint to authorize users """
#     data = validate_user(request.get_json())
#     if data['ok']:
#         data = data['data']
#         user = users.find_one({
#             "email": data["email"]
#         })
#         if user is None:
#             response_object = {"status": False, "message": "Email does not exist."}
#             return make_response(jsonify(response_object), 401)

#         if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
#             del user['password']
#             access_token = create_access_token(identity=data)
#             refresh_token = create_refresh_token(identity=data)
#             user['token'] = access_token
#             user['refresh'] = refresh_token
            
#             response_object = {"status": True, "data": user}
#             return make_response(jsonify(response_object), 200)
#         else:
#             response_object = {"status": False, "message": "Invalid password"}
#             return make_response(jsonify(response_object), 401)
#     else:
#         response_object = {"status": False, "message": 'Bad request parameters: {}'.format(data['message'])}
#         return make_response(jsonify(response_object), 400)

# @admin_auth.route('/admin/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     ret = {
#         'token': create_access_token(identity=current_user)
#     }
#     response_object = {"status": True, "data": ret}
#     return make_response(jsonify(response_object), 200)
