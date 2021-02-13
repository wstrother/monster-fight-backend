from flask import jsonify, request, current_app


def prepare_response(data, status=None):
    res = jsonify(data)

    # !!!
    # DO NOT INCLUDE THIS IN PRODUCTION ENVIRONMENT
    # !!!
    if current_app.config['DEBUG']:
        res.headers.add('Access-Control-Allow-Origin', '*')

    if "error" in data:
        data.update({"request": request.args})
        if not status:
            status = 400

    if not status:
        status = 200

    return res, status


def password_strength(password):
    capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    numerals = "1234567890"

    has_caps = any([c in password for c in capitals])
    has_lower = any([c in password for c in lowercase])
    has_numeral = any([n in password for n in numerals])
    has_other = any([p not in capitals + lowercase + numerals for p in password])

    return has_caps and has_lower and has_numeral and has_other


class ModelController:
    def __init__(self, db):
        self.db = db

    def add(self, item):
        self.db.session.add(item)

    def add_all(self, items):
        self.db.session.add_all(items)

    def commit(self):
        self.db.session.commit()
