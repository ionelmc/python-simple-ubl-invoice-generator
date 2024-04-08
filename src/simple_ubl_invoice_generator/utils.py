import json


def pformat(value):
    return json.dumps(value, indent=4, default=str)
