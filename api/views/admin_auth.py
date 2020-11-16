from flask import Blueprint, jsonify, request, make_response
from api.models import user
from api import mongo

admin_auth = Blueprint("admin_auth", __name__)  # initialize blueprint


@admin_auth.route('/admin/register', methods=['POST'])
def register():
    """ Endpoint to register users """
    # Validates if the format is correct
    data = user.validate_user(request.get_json())

    if data['ok']:
        data = data['data']
        # data['password'] = flask_bcrypt.generate_password_hash(
        #     data['password']
        # )

        mongo.db.users.insert_one(data)
        response_object = {
            "status": True,
            "message": 'User created successfully!'
        }
        return make_response(jsonify(response_object), 200)

    else:
        response_object = {
            "status": False,
            "message": 'Bad request parameters: {}'.format(data['message'])
        }
        return make_response(jsonify(response_object), 400)
