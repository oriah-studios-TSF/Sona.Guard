from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.services.access_control import verify_access

access_control_bp = Blueprint('access_control', __name__, url_prefix='/access')

@access_control_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'success': False,
            'message': 'Request body must contain valid JSON'
        })

    person_id = data.get('person_id')
    entrance_id = data.get('entrance_id')

    if not person_id or not entrance_id:
        return jsonify({
            'success': False,
            'message': 'Person ID and Entrance ID are required'
        }), 400

    result = verify_access(
        person_id=person_id,
        entrance_id=entrance_id,
        user_id=current_user.id
    )

    return jsonify({
        'success': result['result'] == 'GRANTED',
        'result': result['result'],
        'reason': result['reason'],
        'access_attempt_id': result['access_attempt_id']
    }), 200

    