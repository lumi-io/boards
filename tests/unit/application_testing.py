from api import mongo
from flask import json, ObjectId
from pymongo import MongoClient
import boto3

# Create a client instance of MongoClient
client  = MongoClient()
applications = client["applications"]

# Parameters for S3 bucket
BUCKET = 'resume-testing-ats'
REGION = 'us-east-2'
s3_client = boto3.client('s3')

def test_upload_resume(test_client):
    response = test_client.post('/user/portal/upload-resume/<posting_id>', 
                        data = s3_client.upload_fileobj(
                            file,
                            'resume-testing-ats',
                            posting_id + '/resume/{}'.format(filename),
                            ExtraArgs={
                                "ACL": acl,
                                "ContentType": file.content_type
                            }
                        ),
                        content_type='application/json',
                        )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200

# def test_upload_image(test_client):
#     pass

# def test_upload_video(test_client):
#     pass

def test_upload(test_client):
    response = test_client.post('/user/portal/upload-resume/<posting_id>', 
                        data = s3_client.upload_fileobj(
                            file,
                            'resume-testing-ats',
                            posting_id + '/resume/{}'.format(filename),
                            ExtraArgs={
                                "ACL": acl,
                                "ContentType": file.content_type
                            }
                        ),
                        content_type='application/json',
                        )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200

def test_submit_application(test_client):
    payload = json.dumps({
            "firstName": "claire",
            "lastName": "choi",
            "email": "claire@google.com",
            "phone": "234-1234",
            "gradYear": "2022",
            "major": "Computer Science",
            "linkedin": "google.com",
            "website": "microsoft.com",
            "resume": "https://resume-testing-ats.s3.us-east-2.amazonaws.com/602c80c47aa6278332004e6b/resume/BA476 Schedule.pdf",
            "image": "https://resume-testing-ats.s3.us-east-2.amazonaws.com/602c80c47aa6278332004e6b/profile-pic/big_brain.png",
            "video": "https://resume-testing-ats.s3.us-east-2.amazonaws.com/602c80c47aa6278332004e6b/elevator-pitch/Exercise-visualization.ipynb",
            "applicantId": ObjectId('602c8e9934a696f0afa5cc31'),
            "timeApplied": "Tue Feb 16 22:33:45 2021"
        })
    response = test_client.post('/user/portal/submit/602c8e9934a696f0afa5cc31', data=payload)
    assert response.status_code == 200
