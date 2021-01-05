from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity,
                                get_raw_jwt)
from api.validators.user import validate_user
from api import mongo, flask_bcrypt, jwt, blacklist

admin_auth = Blueprint("admin_auth", __name__)  # initialize blueprint
users = mongo.db.users


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@jwt.unauthorized_loader
def unauthorized_response(callback):
    response_object = {
        "status": False,
        "message": "Missing authorization header."
    }
    return make_response(jsonify(response_object), 401)


@admin_auth.route('/admin/register', methods=['POST'])
def register():
    """ Endpoint to register users """
    # Validates if the format is correct
    data = validate_user(request.get_json())

    if data['ok']:
        data = data['data']
        email = data["email"]
        user = users.find_one({
            "email": email
        })
        if user:
            response_object = {
                "status": False,
                "message": "User already exists."
            }
            return make_response(jsonify(response_object), 400)

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


@admin_auth.route('/admin/login', methods=['POST'])
def login_user():
    """ Endpoint to authorize users """
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = users.find_one({
            "email": data["email"]
        })
        if user is None:
            response_object = {"status": False,
                               "message": "Email does not exist."}
            return make_response(jsonify(response_object), 401)

        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token

            response_object = {"status": True, "data": user}
            return make_response(jsonify(response_object), 200)
        else:
            response_object = {"status": False, "message": "Invalid password"}
            return make_response(jsonify(response_object), 401)
    else:
        response_object = {
            "status": False, "message": 'Bad request parameters: {}'.format(data['message'])}
        return make_response(jsonify(response_object), 400)


@admin_auth.route('/admin/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    response_object = {"status": True, "data": ret}
    return make_response(jsonify(response_object), 200)


@admin_auth.route('/admin/logout', methods=['DELETE'])
@jwt_required
def logout():
    try:
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        response_object = {
            "status": True,
            "message": "Succesfully logged out"
        }
        return make_response(jsonify(response_object), 200)

    except Exception as e:
        print(e)
