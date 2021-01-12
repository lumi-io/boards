from flask import Blueprint, jsonify, request, make_response
from api import mongo, flask_bcrypt, jwt
from api.middlewares import upload_file

import PyPDF2
import base64
import requests
import json

resume_parser_test = Blueprint("resume_parser_test", __name__)

""" resumer_parser(): A test function to receive a resume as a file and submit a POST request to appropriate lambda function in base64 
"""
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
    # Receive resume as a PDF file
    pdf_file_obj = request.files['resume'].read()

    # Convert resume into base64
    base64_resume = base64.b64encode(pdf_file_obj)

    # Submit a POST request of base64 to lambda function 
    url = "https://emk9i3070g.execute-api.us-east-2.amazonaws.com/test/"
    payload = "{ \r\n           \"body\": {\r\n               \"content\": \"" + str(base64_resume)[2:]  +"\"\r\n           }\r\n       }"
    headers = {
        'Content-Type': 'application/json'
    }
    
    # extraction of info from the returned payload
    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()["body"]
    summary_keys = ['names', 'emails', "phones", 'schools', 'links', 'summary', 'positions']
    res = json.loads(response) 
    summary = {}
    for i in summary_keys:
        summary[i] = res[i] 
    return json.dumps(summary)