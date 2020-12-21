from flask import Blueprint, jsonify, request, make_response
from api import mongo, flask_bcrypt, jwt
from api.middlewares import upload_file

resume_parser_test = Blueprint("resume_parser_test", __name__)

@resume_parser_test.route("/test/parse", methods=["POST"])
def resume_parser():
    """
    1. Recieve resume as a file
    2. Convert resume (PDF) into binary
    3. Submit a POST request of binary data to https://emk9i3070g.execute-api.us-east-2.amazonaws.com/test/
       in the format of
       { 
           "body": {
               "content": resume binary data here
           }
       }
    4. Return payload

    """
    pass

