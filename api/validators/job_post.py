from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

job_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "info": {
            "type": "string"
        },
        "application": {
            "type": "array"
        },

        "createdBy": {
            "type": "string",
        },
        "isVisible": {
            "type": "boolean"
        }

    },
    "required": ["title", "info", "createdBy", "isVisible"],
    "additionalProperties": False
}


def validate_job(data):
    try:
        validate(data, job_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}