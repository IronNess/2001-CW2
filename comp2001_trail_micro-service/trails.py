from functools import wraps
from flask import request, jsonify
from config import db
from models import Trail, TrailInfo, Location, Tag, TrailTag
from authenticator import authenticate_user


def require_role(allowed_roles):
    """Decorator to enforce role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get Authorization header
            auth = request.headers.get("Authorization")
            if not auth:
                return jsonify({"message": "Authentication required"}), 401

            # Parse email and password from Authorization header
            try:
                email, password = auth.split(":")
            except ValueError:
                return jsonify({"message": "Invalid Authorization header format. Expected 'email:password'"}), 400

            # Authenticate user
            user = authenticate_user(email, password)
            if not user:
                return jsonify({"message": "Invalid credentials"}), 401

            # Check if user's role is allowed
            if user['role'] not in allowed_roles:
                return jsonify({"message": f"Access denied for role: {user['role']}"}), 403

            # Pass control to the actual route function
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@require_role(['Admin', 'User'])
def get_all_trails():
    """Return a JSON list of all trails."""
    trails = Trail.query.all()
    output = [{"TrailID": t.TrailID, "TrailName": t.TrailName, "CreatedAt": t.CreatedAt} for t in trails]
    return jsonify(output)


@require_role(['Admin'])
def create_trail():
    """Create a new trail."""
    data = request.get_json()
    new_trail = Trail(TrailName=data["TrailName"])
    db.session.add(new_trail)
    db.session.commit()
    return jsonify({"TrailID": new_trail.TrailID, "TrailName": new_trail.TrailName, "CreatedAt": new_trail.CreatedAt}), 201


@require_role(['Admin', 'User'])
def get_trail_by_id(trail_id):
    """Return details of a specific trail."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

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
        "RouteType": trail_info.RouteType if trail_info else None,
        "EstimatedTime": trail_info.EstimatedTime if trail_info else None,
        "ElevationGain": trail_info.ElevationGain if trail_info else None,
        "LengthKM": trail_info.LengthKM if trail_info else None,
        "Locations": [
            {"Latitude": loc.Latitude, "Longitude": loc.Longitude, "Sequence": loc.Sequence}
            for loc in locations
        ]
    }
    return jsonify(response)


@require_role(['Admin'])
def update_trail(trail_id):
    """Update an existing trail."""
    data = request.get_json()
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    trail.TrailName = data.get("TrailName", trail.TrailName)
    db.session.commit()
    return jsonify({"TrailID": trail.TrailID, "TrailName": trail.TrailName, "CreatedAt": trail.CreatedAt})


@require_role(['Admin'])
def delete_trail(trail_id):
    """Delete an existing trail."""
    trail = Trail.query.get(trail_id)
    if not trail:
        return jsonify({"message": "Trail not found"}), 404

    db.session.delete(trail)
    db.session.commit()
    return jsonify({"message": "Trail deleted successfully"}), 204


@require_role(['Admin', 'User'])
def get_all_tags():
    """Return a list of all tags."""
    tags = Tag.query.all()
    output = [{"TagID": t.TagID, "Name": t.Name} for t in tags]
    return jsonify(output)


@require_role(['Admin'])
def create_tag():
    """Create a new tag."""
    data = request.get_json()
    new_tag = Tag(Name=data["Name"])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({"TagID": new_tag.TagID, "Name": new_tag.Name}), 201


@require_role(['Admin', 'User'])
def get_tags_for_trail(trail_id):
    """Get all tags associated with a specific trail."""
    tags = (
        db.session.query(Tag)
        .join(TrailTag, Tag.TagID == TrailTag.TagID)
        .filter(TrailTag.TrailID == trail_id)
        .all()
    )
    output = [{"TagID": t.TagID, "Name": t.Name} for t in tags]
    return jsonify(output)


@require_role(['Admin'])
def add_tag_to_trail(trail_id):
    """Associate a tag with a trail."""
    data = request.get_json()
    tag_id = data["TagID"]

    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404

    new_trail_tag = TrailTag(TrailID=trail_id, TagID=tag_id)
    db.session.add(new_trail_tag)
    db.session.commit()
    return jsonify({"message": f"Tag '{tag.Name}' added to trail ID {trail_id}"}), 201

