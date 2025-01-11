from flask import Blueprint, jsonify

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    return jsonify({"message": "Notes endpoint"})
