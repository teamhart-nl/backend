from functools import wraps

from flask import jsonify, request


def validate_json(f):
    """
    wrapper for json posts
    """
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            data = request.json
        except Exception:
            # problem reading in json
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        if data is None:
            # empty while json is expected
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        else:
            return f(*args, **kw)

    return wrapper