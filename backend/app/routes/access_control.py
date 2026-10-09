from flask import Blueprint, jsonify, request, render_template
from flask_login import current_user, login_required

from app.models import Person
from app.services.access_control import verify_access

access_control_bp = Blueprint('access_control', __name__, url_prefix='/access')

@access_control_bp.route('/verfication')
@login_required
def verification():
    return render_template(
        'access/verification.html',
        title='Access Verification',
        icon='user-check',
        title_description='Verify whether a person is permitted to access a specific entrance.'
        )

@access_control_bp.route('/person/<employee_id>', methods=['GET'])
@login_required
def get_person(employee_id):
    
    person = Person.query.filter_by(
        employee_id=employee_id.strip().upper()
    ).first()

    if not person:
        return jsonify({
            'success': False,
            'message': 'Person not found.'
        }), 404

    return jsonify({
        'success': True,
        'person': {
            'id': person.id,
            'employee_id': person.employee_id,
            'full_name': person.full_name,
            'email': person.email,
            'phone_number': person.phone_number,
            'photo': person.photo,
            'is_active': person.is_active
        }
    }), 200


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

    