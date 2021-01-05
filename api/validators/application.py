from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

application_schema = {
    "type": "object",
    "properties": {
        "applicant_id": {
        },
        "applicationStatus": {
            "type": "string"
        },
        "timeApplied": {
            "type": "string" #datatime??
        },
        "applicantName": {
            "type": "string",
        },
        "profilePic": {
            "type": "string"
        },
        "graduatingYear": {
            "type": "integer"
        },
        "phoneNumber": {
            "type": "string"
        },
        "GPA": {
            "type": "number"
        },
        "major": {
            "type": "string",
        },
        "minor": {
            "type": "string"
        },
        "college": {
            "type": "string"
        },
        "resume": {
            "type": "string"
        },
        "elevatorPitch": {
            "type": "string"
        },
        "other_URL": {
            "type": "string"
        },
        "Q&A": {
            "type": "array"
        },
        "email": {
            "type": "string"
        },
        "role": {
            "type": "string"
        }
    },
    "required": ["applicationStatus", "resume", "elevatorPitch", "profilePic", "applicantName", "graduatingYear", "phoneNumber", "GPA", "major", "college", "email", "role"],
    #, "time_applied", "Q&A"
    "additionalProperties": False
}

def validate_application(data):
    try:
        validate(data, application_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}