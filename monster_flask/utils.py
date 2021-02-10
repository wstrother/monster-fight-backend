from flask import jsonify, request


def prepare_response(data):
    res = jsonify(data)
    res.headers.add('Access-Control-Allow-Origin', '*')
    status = 200

    if "error" in data:
        data.update({"request": request.args})
        status = 400

    return res, status
