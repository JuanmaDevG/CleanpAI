from flask import Blueprint, request, jsonify

config_bp = Blueprint('config', __name__)

@config_bp.route('/preferences/<user_id>', methods=['GET'])
def get_user_preferences(user_id):
    return jsonify({
        "user_id": user_id,
        "notifications": True,
        "alert_threshold": "medium",
        "language": "es",
        "notification_channels": ["email", "sms"]
    }), 200

@config_bp.route('/preferences/<user_id>', methods=['PUT'])
def update_user_preferences(user_id):
    preferences = request.json
    return jsonify({
        "user_id": user_id,
        "updated_preferences": preferences,
        "message": "Preferences updated successfully"
    }), 200

@config_bp.route('/threshold/<user_id>', methods=['PUT'])
def update_alert_threshold(user_id):
    threshold_data = request.json
    return jsonify({
        "user_id": user_id,
        "new_threshold": threshold_data.get('threshold'),
        "message": "Alert threshold updated"
    }), 200

@config_bp.route('/notifications/<user_id>', methods=['PUT'])
def toggle_notifications(user_id):
    notification_status = request.json
    return jsonify({
        "user_id": user_id,
        "notifications_enabled": notification_status.get('enabled'),
        "message": "Notifications status updated"
    }), 200
