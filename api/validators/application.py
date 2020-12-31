from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

application_schema = {
    "type": "object",
    "properties": {
        "applicant_id": {
        },
        "application_status": {
            "type": "string"
        },
        "time_applied": {
            "type": "string" #datatime??
        },
        "applicant_name": {
            "type": "string",
        },
        "profilePic": {
            "type": "string"
        },
        "graduating_year": {
            "type": "integer"
        },
        "phone_number": {
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
        "elavatorPitch": {
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
    "required": ["application_status", "resume", "elavatorPitch", "profilePic", "applicant_name", "graduating_year", "phone_number", "GPA", "major", "college", "email", "role"],
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