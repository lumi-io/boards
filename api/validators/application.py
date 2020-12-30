from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

# application_schema = {
#     "type": "object",
#     "properties": {
#         "postingKey": {
#             "type": "string"
#         },
#         "applications": {
#             "type": "array",
#             "items": {
#                 "application_status": {
#                     "type": "string"
#                 },
#                 "time_applied": {
#                     "type": "string" #datatime??
#                 },
#                 "name": {
#                     "type": "string",
#                 },
#                 "profilePic": {
#                     "type": "string"
#                 },
#                 "graduating_year": {
#                     "type": "integer"
#                 },
#                 "phone_number": {
#                     "type": "string"
#                 },
#                 "GPA": {
#                     "type": "number"
#                 },
#                 "major": {
#                     "type": "string",
#                 },
#                 "minor": {
#                     "type": "string"
#                 },
#                 "college": {
#                     "type": "array"
#                 },
#                 "resume": {
#                     "type": "string"
#                 },
#                 "elavatorPitch": {
#                     "type": "string"
#                 },
#                 "other_URL": {
#                     "type": "string"
#                 },
#                 "Q&A": {
#                     "type": "array"
#                 },
#                 "email": {
#                     "type": "string"
#                 },
#                 "role": {
#                     "type": "string"
#                 }
#             },
#         },
#     },
#     "required": ["postingKey"],
#     #, "time_applied", "name", "profile-pic", "graduating_year", "phone_number", "GPA", "major", "college", "resume", "elevator-pitch", "other_URL", "Q&A", "email", "role"
#     "additionalProperties": False
# }

application_schema = {
    "type": "object",
    "properties": {
        "application_status": {
            "type": "string"
        },
        "time_applied": {
            "type": "string" #datatime??
        },
        "name": {
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
            "type": "array"
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
    "required": ["application_status"],
    #, "time_applied", "name", "profile-pic", "graduating_year", "phone_number", "GPA", "major", "college", "resume", "elevator-pitch", "other_URL", "Q&A", "email", "role"
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