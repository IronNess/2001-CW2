from flask import Blueprint, jsonify

people_bp = Blueprint('people', __name__)

@people_bp.route('/people', methods=['GET'])
def get_people():
    return jsonify({"message": "People endpoint"})

