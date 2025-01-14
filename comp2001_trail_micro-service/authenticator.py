
from functools import wraps
from flask import request, jsonify
from models import User, Role



AUTHENTICATOR_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"


def authenticate_user(email, password):
    """Authenticate a user using the hashed password."""
    user = User.query.filter_by(Email=email).first()
    if user and user.check_password(password):
        role = Role.query.get(user.RoleID)
        return {'email': user.Email, 'role': role.RoleName}
    return None

def require_role(role_required):
    """Decorator to enforce role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth = request.authorization
            if not auth:
                return jsonify({"error": "Authentication required"}), 401

            user = authenticate_user(auth.username, auth.password)
            if user and user['role'] == role_required:
                return f(*args, **kwargs)
            return jsonify({"error": "Unauthorized"}), 403
        return decorated_function
    return decorator