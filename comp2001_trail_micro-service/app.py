# app.py

from flask import render_template, request, jsonify, session
from functools import wraps
import requests
import config
from models import db, Trail, TrailInfo, Location


app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

AUTHENTICATOR_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def authenticate_user(email, password):
    try:
        response = requests.post(
            f"{AUTHENTICATOR_API_URL}/login",
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        else:
            return None
    except Exception as e:
        print(f"Error connecting to Authenticator API: {e}")
        return None

@app.route("/")
def home():
    trails = Trail.query.all()
    return render_template("home.html", trails=trails)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = authenticate_user(email, password)
    if user:
        session["user"] = {
            "username": user["username"],
            "email": user["email"],
            "roles": user.get("roles", []),
        }
        return jsonify({"message": "Login successful!", "user": session["user"]}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    """Endpoint to log out a user."""
    session.pop("user", None)
    return jsonify({"message": "Logout successful!"}), 200

@app.route("/api/trails", methods=["GET"])
def get_all_trails():
    trails = Trail.query.all()
    return jsonify([
        {
            "TrailID": trail.TrailID,
            "TrailName": trail.TrailName,
            "CreatedAt": trail.CreatedAt
        } for trail in trails
    ])

@app.route("/api/trails/<int:trail_id>", methods=["GET"])
def get_trail_by_id(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    trail_info = TrailInfo.query.get(trail_id)
    locations = Location.query.filter_by(TrailID=trail_id).order_by(Location.Sequence).all()

    return jsonify({
        "TrailID": trail.TrailID,
        "TrailName": trail.TrailName,
        "CreatedAt": trail.CreatedAt,
        "Description": trail_info.Description if trail_info else None,
        "Distance": trail_info.Distance if trail_info else None,
        "Difficulty": trail_info.Difficulty if trail_info else None,
        "Locations": [
            {
                "Latitude": location.Latitude,
                "Longitude": location.Longitude,
                "Sequence": location.Sequence
            } for location in locations
        ]
    })

@app.route("/api/trails", methods=["POST"])
def create_trail():
    data = request.get_json()
    new_trail = Trail(TrailName=data["TrailName"])
    db.session.add(new_trail)
    db.session.commit()

    return jsonify({
        "TrailID": new_trail.TrailID,
        "TrailName": new_trail.TrailName,
        "CreatedAt": new_trail.CreatedAt
    }), 201

@app.route("/api/trails/<int:trail_id>", methods=["PUT"])
def update_trail(trail_id):
    data = request.get_json()
    trail = Trail.query.get(trail_id)

    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    trail.TrailName = data.get("TrailName", trail.TrailName)
    db.session.commit()

    return jsonify({
        "TrailID": trail.TrailID,
        "TrailName": trail.TrailName,
        "CreatedAt": trail.CreatedAt
    })

@app.route("/api/trails/<int:trail_id>", methods=["DELETE"])
def delete_trail(trail_id):
    trail = Trail.query.get(trail_id)

    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    db.session.delete(trail)
    db.session.commit()

    return jsonify({"message": "Trail deleted successfully"}), 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)