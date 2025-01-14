
from functools import wraps
from flask import request, jsonify
from models import User, Role
from flask import session



AUTHENTICATOR_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"


def authenticate_user(email, password):
    """Authenticate a user using the hashed password."""
    user = User.query.filter_by(Email=email).first()
    if user and user.check_password(password):
        role = Role.query.filter_by(RoleID=user.RoleID).first()
        return {'email': user.Email, 'role': role.RoleName} if role else None
    return None



from flask import request, jsonify
from functools import wraps
from models import User, Role

from flask import request, jsonify
from functools import wraps
from models import User, Role

def require_role(allowed_roles):
    """Decorator to enforce role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the Authorization header
            auth = request.headers.get("Authorization")
            if not auth:
                return jsonify({"message": "Authentication required"}), 401
            
            try:
                email, password = auth.split(":")
            except ValueError:
                return jsonify({"message": "Invalid Authorization header format. Expected 'email:password'"}), 400
            
            # Authenticate the user
            user = User.query.filter_by(Email=email).first()
            if not user or not user.check_password(password):
                return jsonify({"message": "Invalid credentials"}), 401

            # Fetch user's role
            role = Role.query.filter_by(RoleID=user.RoleID).first()
            if not role or role.RoleName not in allowed_roles:
                return jsonify({"message": f"Access denied for role: {role.RoleName}"}), 403

            # Pass the request to the actual route function
            return f(*args, **kwargs)
        return decorated_function
    return decorator

