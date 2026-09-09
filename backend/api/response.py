from flask import jsonify


def success(data=None, message=None):
    response = {
        "status": "success"
    }

    if data is not None:
        response["data"] = data

    if message is not None:
        response["message"] = message

    return jsonify(response)


def error(message, code=400):
    return jsonify({
        "status": "error",
        "code": code,
        "message": message
    }), code
