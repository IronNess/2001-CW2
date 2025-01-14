from config import connex_app, db
from flask import request, jsonify
from models import User
import bcrypt

# Function to check password against the stored hash
def check_password(provided_password, stored_hash):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

# Route for user login
@connex_app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(Email=email).first()
    if user and check_password(password, user.PasswordHash):
        # Successful login
        return jsonify({"message": "Login successful", "user_id": user.UserID}), 200
    else:
        # Failed login
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    # Load the API definition for Connexion based on the Swagger.yml
    connex_app.add_api(
        "swagger.yml",
        base_path="/api",  
        options={"swagger_ui": True},
        arguments={"title": "Trail Application REST API"},
    )

    # Run the Connexion+Flask app
    connex_app.run(host="0.0.0.0", port=8000)
