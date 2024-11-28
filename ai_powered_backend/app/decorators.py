# app/decorators.py

from functools import wraps
from flask import request, jsonify
from app.models.user import User


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_token = request.headers.get('Authorization')
            if auth_token:
                user = User.query.filter_by(auth_token=auth_token).first()
                if user and user.role in roles:
                    return f(*args, **kwargs)
                else:
                    return jsonify({"error": "You are not authorized to access this resource"}), 403
            else:
                return jsonify({"error": "Authentication token is missing"}), 401
        return decorated_function
    return decorator
