import boto3
from botocore.exceptions import ClientError


def send_confirmation_email(email: str, email_confirmation_id: str):
    SENDER = "JinYoung Bang <jybang@bu.edu>" # For Testing purposes
    RECIPIENT = email
    AWS_REGION = "us-east-2"
    SUBJECT = "Lumi Account Setup"
    BODY_TEXT = "http://127.0.0.1:5000/confirmation/" + email_confirmation_id
    BODY_HTML = "<p> http://127.0.0.1:5000/confirmation/" + email_confirmation_id + "</p>"
    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,

    )


    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
    return
