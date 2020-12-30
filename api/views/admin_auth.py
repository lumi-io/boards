from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from api.validators.user import validate_user, validate_email
from api import mongo, flask_bcrypt, jwt
from api.middlewares.confirmation_email import send_confirmation_email
import uuid

admin_auth = Blueprint("admin_auth", __name__)  # initialize blueprint
users = mongo.db.users


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

        email_confirmation_id = str(uuid.uuid4())
        data["email_confirmation_id"] = email_confirmation_id
        data["email_confirmed"] = False

        send_confirmation_email(email, email_confirmation_id)

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


@admin_auth.route('/confirmation/<confirmation_id>', methods=['GET'])
def confirm_registration(confirmation_id):
    """ Endpoint that verifies user's signup process through a confirmation ID from email """
    user = users.update(
        {"email_confirmation_id": confirmation_id},
        {
            "$set": {"email_confirmed": True},
            "$unset": {"email_confirmation_id": ""}
        },
        upsert=False
    )
    if user["nModified"] == 0 and not user["updatedExisting"]:
        response_object = {
            "status": False,
            "message": "Invalid ID. Please register a new user or resend the verification email."
        }
        return make_response(jsonify(response_object), 401)

    response_object = {
        "status": True,
        "message": "Email verified."
    }
    return response_object(jsonify(response_object), 200)


@admin_auth.route('/resend-confirmation', methods=['POST'])
def resend_confirmation():
    """ Endpoint that resends confirmation email to the user with a new ID """
    data = validate_email(request.get_json())

    if data['ok']:
        data = data['data']
        email = data["email"]

        user = users.find_one({
            "email": email
        })

        if not user:
            response_object = {
                "status": False,
                "message": "Email not found. Please register a new account."
            }
            return make_response(jsonify(response_object), 400)
        
        if user["email_confirmed"]:
            response_object = {
                "status": False,
                "message": "User has already been verified."
            }
            return make_response(jsonify(response_object), 400)

        new_confirmation_id = str(uuid.uuid4())

        user = users.update(
            {"email": email},
            {
                "$set": {"email_confirmation_id": new_confirmation_id},
            },
            upsert=False
        )
        send_confirmation_email(email, new_confirmation_id)

        response_object = {
            "status": True,
            "message": 'Resent verification/confirmation email.'
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
        user = users.find_one({
            "email": data["email"]
        })
        if user is None:
            response_object = {"status": False,
                               "message": "Email does not exist."}
            return make_response(jsonify(response_object), 401)

        if not user["email_confirmed"]:
            response_object = {
                "status": False,
                "message": "Registration incomplete. User has not confirmed their email."
            }
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
