from flask import jsonify, request
from config import db
from models import Trail, TrailInfo, Location, Tag, TrailTag

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
        "RouteType": trail_info.RouteType if trail_info else None,
        "EstimatedTime": trail_info.EstimatedTime if trail_info else None,
        "ElevationGain": trail_info.ElevationGain if trail_info else None,
        "LengthKM": trail_info.LengthKM if trail_info else None,
        "Locations": [
            {
                "Latitude": loc.Latitude,
                "Longitude": loc.Longitude,
                "Sequence": loc.Sequence
            } for loc in locations
        ] if locations else []
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

# New Tag Functions
def get_all_tags():
    """Return a list of all tags."""
    tags = Tag.query.all()
    output = [{"TagID": t.TagID, "Name": t.Name} for t in tags]
    return jsonify(output)

def create_tag():
    """Create a new tag."""
    data = request.get_json()
    new_tag = Tag(Name=data["Name"])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({"TagID": new_tag.TagID, "Name": new_tag.Name}), 201

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

def add_tag_to_trail(trail_id):
    """Associate a tag with a trail."""
    data = request.get_json()
    tag_id = data["TagID"]
    # Check if tag exists
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404

    # Associate tag with trail
    new_trail_tag = TrailTag(TrailID=trail_id, TagID=tag_id)
    db.session.add(new_trail_tag)
    db.session.commit()
    return jsonify({"message": f"Tag '{tag.Name}' added to trail ID {trail_id}"}), 201
