from app import auth_
from app.models import User
from flask import make_response, jsonify, g


@auth_.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


@auth_.error_handler
def unauthorized_access():
    return make_response(jsonify(error='Unauthorized Access')), 401