from jsonschema import validate, ValidationError

TICKET_CREATE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 5},
        "description": {"type": "string"},
        "priority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]}
    },
    "required": ["title", "description"]
}

def validate_ticket_request(data):
    try:
        validate(instance=dict(data), schema=TICKET_CREATE_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, e.message