from flask import make_response, jsonify
from app.errors import bp

@bp.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify(error='Not Found'), 404)

@bp.app_errorhandler(400)
def bad_request(error):
    return make_response(jsonify(error='Bad Request'), 400)

@bp.app_errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify(error='Method Not Allowed'), 405)