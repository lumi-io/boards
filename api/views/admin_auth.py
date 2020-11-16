from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.models.user import validate_user
from api import mongo, flask_bcrypt

admin_auth = Blueprint("admin_auth", __name__)  # initialize blueprint


@admin_auth.route('/admin/register', methods=['POST'])
def register():
    """ Endpoint to register users """
    # Validates if the format is correct
    data = validate_user(request.get_json())

    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(
            data['password']
        )

        mongo.db.users.insert_one(data)
        response_object = {
            "status": True,
            "message": 'User created successfully.'
        }
        return make_response(jsonify(response_object), 200)

    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'.format(data['message'])
        }
        return make_response(jsonify(response_object), 400)


@admin_auth.route('/admin/auth', methods=['POST'])
def auth_user():
    """ Endpoint to authorize users """
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({
            "email": data["email"]
        })

        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token
            
            response_object = {"status": True, "data": user}
            return make_response(jsonify(response_object), 200)
        else:
            response_object = {"status": False, "message": "Invalid username or password"}
            return make_response(jsonify(response_object), 401)
    else:
        response_object = {"status": False, "message": 'Bad request parameters: {}'.format(data['message'])}
        return make_response(jsonify(response_object), 400)
