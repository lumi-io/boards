from flask import Blueprint, jsonify, request, make_response
from api import mongo, flask_bcrypt, jwt
from api.middlewares import upload_file

import PyPDF2
import base64

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
    pdfFileObj = open('resume.pdf', 'rb')           # Creating a pdf file object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)    # Creating a pdf reader object

    # Convert a pdf file into base64Binary
    with open("resume.pdf", "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
    pass

