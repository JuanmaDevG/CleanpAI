from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    return jsonify({"message": "User created"}), 201

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({"message": f"User {user_id} deleted"}), 200

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"user_id": user_id, "data": "user_info"}), 200

@user_bp.route('/', methods=['GET'])
def get_all_users():
    return jsonify({"users": []}), 200
