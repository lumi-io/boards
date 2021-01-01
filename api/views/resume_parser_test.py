from flask import Blueprint, jsonify, request, make_response
from api import mongo, flask_bcrypt, jwt
from api.middlewares import upload_file

import PyPDF2
import base64
import requests
import json


resume_parser_test = Blueprint("resume_parser_test", __name__)


@resume_parser_test.route("/test/parse", methods=["POST"])
def resume_parser():
    """
    1. Recieve resume as a file
    2. Convert resume (PDF) into base64
    3. Submit a POST request of base64 to https://emk9i3070g.execute-api.us-east-2.amazonaws.com/test/
       in the format of
       { 
           "body": {
               "content": resume binary data here
           }
       }
    4. Return payload
    """
    # Receiving Resume as a PDF file
    pdf_file_obj = request.files['resume'].read()

    # Convert resume into base64
    base64_resume = base64.b64encode(pdf_file_obj)
    url = "https://emk9i3070g.execute-api.us-east-2.amazonaws.com/test/"


    payload = "{ \r\n           \"body\": {\r\n               \"content\": \"" + str(base64_resume)[2:]  +"\"\r\n           }\r\n       }"

    headers = {
        'Content-Type': 'application/json'
    }
    print("hit")

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)
