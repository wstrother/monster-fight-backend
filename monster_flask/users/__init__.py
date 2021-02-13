from flask import Blueprint, request, current_app
import jwt
import datetime
from functools import wraps

from monster_flask import db
from monster_flask.utils import prepare_response
from monster_flask.users.models import User
from monster_flask.users.controllers import UserController

users = Blueprint('users', __name__)

USERS = UserController(db)
TOKEN_HEADER_NAME = "auth-token"
SECURITY_ALG = 'HS256'


def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "auth-token" not in request.headers:
            return prepare_response({"error": f"'{TOKEN_HEADER_NAME}' header is required"}, 401)

        try:
            data = jwt.decode(
                request.headers[TOKEN_HEADER_NAME], current_app.config["SECRET_KEY"], algorithms=SECURITY_ALG
            )

        except jwt.DecodeError:
            return prepare_response({"error": "Bad token passed"}, 403)

        user_id = data["user_id"]
        user = USERS.get_user_by_id(user_id)

        if not user:
            return prepare_response({"error": f"no user found with id: '{user_id}"})

        return f(user, *args, **kwargs)

    return decorated


def user_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return prepare_response({"error": "Authorization header is required"}, 401)

        if not auth.username:
            return prepare_response({"error": "Username required in Authorization header"}, 401)

        if not auth.password:
            return prepare_response({"error": "Password required in Authorization header"}, 401)

        return f(auth.username, auth.password, *args, **kwargs)

    return decorated


#
# begin user routes
#


@users.route('/new_user', methods=['POST'])
@user_auth
def new_user(username, password):
    try:
        user = USERS.add_user(username, password)
        USERS.commit()

        return prepare_response({
            "username": user.username,
            "user_id": user.id,
            "success": "New user created"
        })

    except AssertionError as e:
        return prepare_response({"error": str(e)})


@users.route('/get_user', methods=['GET'])
def get_user():
    if "user_id" in request.args:
        user_id = request.args["user_id"]
        user = USERS.get_user_by_id(user_id)

        if user:
            return prepare_response({
                "username": user.username
            })

        else:
            return prepare_response({
                "error": "No user found with id: {}".format(user_id)
            })

    else:
        return prepare_response({
            "error": "Please provide a user_id"
        })


@users.route('/get_dashboard', methods=['GET'])
@require_token
def get_dashboard(user):
    return prepare_response({
        "username": user.username,
        "user_id": user.id,
        "success": "Token verified"
    })


@users.route('/login')
@user_auth
def login(username, password):
    data = USERS.check_login(username, password)

    if "error" in data:
        return prepare_response(data, 403)

    else:
        data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        data["auth-token"] = jwt.encode(
            data, current_app.config["SECRET_KEY"], algorithm=SECURITY_ALG
        )

        return prepare_response(data)
