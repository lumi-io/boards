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
            "type": "string"
        },
        "applicantName": {
            "type": "string",
        },
        "profilePic": {
            "type": "string"
        },
        "graduatingYear": {
            "type": "integer",
            "maximum": 3000
        },
        "phoneNumber": {
            "type": "string",
            "maxLength": 12
        },
        "GPA": {
            "type": "number",
            "maximum": 4.0
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
            "type": "string",
            "format": "email"
        },
        "role": {
            "type": "string"
        }
    },
    #"required": ["resume", "elevatorPitch", "profilePic", "applicantName", "graduatingYear", "phoneNumber", "GPA", "major", "college", "email", "role"],
    "required": ["applicantName", "graduatingYear", "phoneNumber", "GPA", "major", "college", "email", "role"],
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