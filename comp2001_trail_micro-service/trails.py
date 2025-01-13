# trails.py

from flask import jsonify, request
from config import db
from models import Trail, TrailInfo, Location

def get_all_trails():
    """Return a JSON list of all trails."""
    trails = Trail.query.all()
    output = [
        {
            "TrailID": t.TrailID,
            "TrailName": t.TrailName,
            "CreatedAt": t.CreatedAt
        } for t in trails
    ]
    return jsonify(output)

def create_trail():
    """Create a new trail from the request JSON body."""
    data = request.get_json()
    new_trail = Trail(TrailName=data["TrailName"])
    db.session.add(new_trail)
    db.session.commit()

    response = {
        "TrailID": new_trail.TrailID,
        "TrailName": new_trail.TrailName,
        "CreatedAt": new_trail.CreatedAt
    }
    return jsonify(response), 201

def get_trail_by_id(trail_id):
    """Return details of a specific trail."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    trail_info = TrailInfo.query.get(trail_id)
    locations = (
        Location.query
        .filter_by(TrailID=trail_id)
        .order_by(Location.Sequence)
        .all()
    )

    response = {
        "TrailID": trail.TrailID,
        "TrailName": trail.TrailName,
        "CreatedAt": trail.CreatedAt,
        "Description": trail_info.Description if trail_info else None,
        "Distance": trail_info.Distance if trail_info else None,
        "Difficulty": trail_info.Difficulty if trail_info else None,
        "Locations": [
            {
                "Latitude": loc.Latitude,
                "Longitude": loc.Longitude,
                "Sequence": loc.Sequence
            } for loc in locations
        ]
    }
    return jsonify(response)

def update_trail(trail_id):
    """Update an existing trail's name."""
    data = request.get_json()
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    trail.TrailName = data.get("TrailName", trail.TrailName)
    db.session.commit()

    response = {
        "TrailID": trail.TrailID,
        "TrailName": trail.TrailName,
        "CreatedAt": trail.CreatedAt
    }
    return jsonify(response)

def delete_trail(trail_id):
    """Delete an existing trail."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    db.session.delete(trail)
    db.session.commit()
    return jsonify({"message": "Trail deleted successfully"}), 204
