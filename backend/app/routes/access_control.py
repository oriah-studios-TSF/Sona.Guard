from flask import Blueprint, jsonify, request, render_template
from flask_login import current_user, login_required

from app.models import Resident
from app.services.access_control import verify_access

# The access_control blueprint manages checkpoint interfaces and gate verification APIs.
access_control_bp = Blueprint('access_control', __name__, url_prefix='/access')

# Endpoint: GET /access/verification
# Renders the HTML checkpoint interface used by guards at the estate entrance.
@access_control_bp.route('/verification')
# Security measure: Restricts checkpoint access to logged-in users only.
@login_required
def verification():
    return render_template(
        'access/verification.html',
        title='Access Verification',
        icon='user-check',
        title_description='Verify whether a resident or visitor is permitted to access a specific entrance.'
        )


# Endpoint: GET /access/resident/<resident_code>
# Looks up a resident by their scanned or entered code to display their profile on the guard's screen.
@access_control_bp.route('/resident/<resident_code>', methods=['GET'])
@login_required
def get_resident(resident_code):
    # Sanitize the input by trimming whitespace and converting to uppercase to match stored format.
    resident = Resident.query.filter_by(
        resident_code=resident_code.strip().upper()
    ).first()

    # If no resident matches the provided code, return an HTTP 404 Not Found error response.
    if not resident:
        return jsonify({
            'success': False,
            'message': 'Resident verification failed. No matching resident record was found.',
            'icon': '<i class="fa fa-triangle-exclamation-mark"></i>'
        }), 404

    # Data Serialization:
    # Convert the SQLAlchemy model attributes into a plain Python dictionary suitable for JSON transmission.
    return jsonify({
        'success': True,
        'resident': {
            'id': resident.id,
            'resident_code': resident.resident_code,
            'full_name': resident.full_name,
            'unit_number': resident.unit_number,
            'email': resident.email,
            'phone_number': resident.phone_number,
            'property_id': resident.property_id,
            'is_active': resident.is_active,
            'status': 'Active' if resident.is_active else 'Inactive',
        }
    }), 200


# Endpoint: POST /access/verify
# Evaluates and records an access verification decision at a specific entrance.
@access_control_bp.route('/verify', methods=['POST'])
@login_required
def verify():
    # Safely parse incoming JSON body.
    data = request.get_json(silent=True) or {}

    resident_id = data.get('resident_id')
    entrance_id = data.get('entrance_id')

    # Input Validation Step 1: Ensure required parameters are present in the request.
    if not resident_id or not entrance_id:
        return jsonify({
            'success': False,
            'message': 'Resident ID and entrance ID are required.',
            'icon': '<i class="fa fa-triangle-exclamation-mark"></i>'
        }), 400

    # Input Validation Step 2: Validate and coerce types to integers to prevent errors or unexpected inputs.
    try:
        resident_id = int(resident_id)
        entrance_id = int(entrance_id)
    except (TypeError, ValueError):
        return jsonify({
            'success': False,
            'message': 'Resident ID and entrance ID must be valid numbers.',
            'icon': '<i class="fa fa-triangle-exclamation-mark"></i>'
        }), 400

    # Delegation to the Service Layer:
    # The route handler delegates business rule evaluation to `verify_access()` in `services.access_control`.
    # Notice we pass `user_id=current_user.id`: this attributes the checkpoint check to the logged-in guard.
    result = verify_access(
        resident_id=resident_id,
        entrance_id=entrance_id,
        user_id=current_user.id
    )

    # Return standard JSON response to the front-end client with the verification outcome.
    return jsonify({
        'success': result['result'] == 'GRANTED',
        'result': result['result'],
        'reason': result['reason'],
        'access_attempt_id': result['access_attempt_id']
    }), 200

