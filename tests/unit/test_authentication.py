import json
from api import mongo

token = ""
refresh_token = ""
email_confirmation_id = ""


def test_create_user(test_client):
    """ Test for user creation on MongoDB """

    def create_user(client, email, password):
        data = {
            "email": email,
            "password": password
        }
        response = client.post(
            "/admin/register",
            json=data
        )
        return response

    assert create_user(test_client, "abcdefg@test.com",
                       "1234").status_code == 400
    assert create_user(test_client, "abcdefg@test.com",
                       "12345678").status_code == 200
    assert create_user(test_client, "abcdefg@test.com",
                       "12345678").status_code == 400
    user = mongo.db.users.find_one(
        {"email": "abcdefg@test.com"}
    )
    global email_confirmation_id
    email_confirmation_id = user["emailConfirmationId"]



def test_confirm_registration_and_login_user(test_client):
    """ Test for logging in a user """

    def login_user(client, email, password):
        data = {
            "email": email,
            "password": password
        }
        response = client.post(
            "/admin/login",
            json=data
        )
        return response

    def confirm_registration(client, confirmation_id):
        response = client.get(
            "/confirmation/" + confirmation_id,
        )
        return response

    # Test case for short password
    assert login_user(
        test_client,
        "abcdefg@test.com",
        "1234678"
    ).status_code == 401

    assert confirm_registration(
        test_client, "random string").status_code == 401
    assert confirm_registration(
        test_client, email_confirmation_id).status_code == 200
    assert confirm_registration(
        test_client, email_confirmation_id).status_code == 401

    # Test case for short password
    assert login_user(
        test_client,
        "abcdefg@test.com",
        "1234"
    ).status_code == 400

    # Test case for nonexisting user
    assert login_user(
        test_client,
        "nonexistinguser@test.com",
        "12345678"
    ).status_code == 401

    # Test case for successful login
    successful_response = login_user(
        test_client,
        "abcdefg@test.com",
        "12345678"
    )
    assert successful_response.status_code == 200
    response_data = json.loads(successful_response.data)
    assert response_data["status"]
    assert "_id" in response_data["data"]
    assert "email" in response_data["data"]
    assert "refresh" in response_data["data"]
    assert "token" in response_data["data"]

    # Global variables to be used for refreshing token
    global token
    global refresh_token
    token = response_data["data"]["token"]
    refresh_token = response_data["data"]["refresh"]


def test_refresh_users_token(test_client):
    """ Test for refreshing a user's token """
    def refresh(client, token):
        response = client.post(
            "/admin/refresh",
            headers={
                "Authorization": "Bearer " + token
            }
        )
        return response

    # Test case for successful refresh
    assert refresh(
        test_client,
        refresh_token
    ).status_code == 200

    # Test case for wrong token
    assert refresh(
        test_client,
        token
    ).status_code == 422

    # Test case for random string instead of token
    assert refresh(
        test_client,
        "Random string"
    ).status_code == 422


def test_logout_user(test_client):
    """ Test for logging out a user (server-side) """
    def logout(client, token):
        response = client.delete(
            "/admin/logout",
            headers={
                "Authorization": "Bearer " + token
            }
        )
        return response

    # Test case for using refresh token
    assert logout(
        test_client,
        refresh_token
    ).status_code == 422

    # Test case for successful logoutp
    assert logout(
        test_client,
        token
    ).status_code == 200
