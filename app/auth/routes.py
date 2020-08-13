from app import db, auth_
from app.auth import bp
from app.models import User
from flask import make_response, jsonify


@auth_.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()

    if user is not None and user.check_password(password):
        return user
    return None


@auth_.error_handler
def unauthorized_access():
    return make_response(jsonify(error='Unauthorized Access')), 401