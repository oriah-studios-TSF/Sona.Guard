from flask import Blueprint, jsonify, request, render_template
from flask_login import current_user, login_required

from app.models import Resident, Entrance, Property, AccessAttempt
from app.services.access_control import verify_access
from app.extensions import db

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

    # Get the property where the resident is registered. This is used to display the property name on the guard's screen.
    # This is done by querying the Property table using the property_id from the resident record.
    property_record = db.session.get(Property, resident.property_id)

    # Read the entrance selected on the verification page
    entrance_id = request.args.get('entrance_id', type=int)

    # If no entrance is selected, return an HTTP 400 Bad Request error response.
    # This is done to ensure that the guard selects an entrance before retrieving resident details.
    if not entrance_id:
        return jsonify({
            'success': False,
            'message': 'Please select an entrance before retrieving resident details.',
            'icon': '<i class="fa fa-triangle-exclamation-mark"></i>'
        }), 400

    entrance = db.session.get(Entrance, entrance_id)

    # If no entrance matches the provided entrance_id, return an HTTP 404 Not Found error response.
    # This is done to ensure that the guard selects a valid entrance before retrieving resident details.
    if not entrance:
        return jsonify({
            'success': False,
            'message': 'The selected entrance could not be found.',
            'icon': '<i class="fa fa-triangle-exclamation-mark"></i>'
        }), 404

    # Check if this resident can be verified at this entrance
    # This is done to ensure that the guard does not verify a resident at an entrance that is not assigned to them.
    if not resident.is_active:
        eligibility_reason = 'Resident is inactive.'
    elif not property_record or not property_record.is_active:
        eligibility_reason = 'Property is inactive or unavailable.'
    elif not entrance.is_active:
        eligibility_reason = 'Entrance is inactive.'
    elif entrance.property_id != resident.property_id:
        eligibility_reason = 'Resident belongs to a different property.'
    else:
        eligibility_reason = 'Eligible for verification.'

    eligible = eligibility_reason == 'Eligible for verification.'

    # Find the most recent access attempt for this resident
    # This is done to ensure that the guard does not verify a resident who has already been verified.
    last_attempt = AccessAttempt.query.filter_by(resident_id=resident.id).order_by(AccessAttempt.created_at.desc()).first()


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
        },
        'property': {
            'id': property_record.id if property_record else None,
            'name': property_record.name if property_record else 'Unavailable',
            'address': property_record.address if property_record else 'None',
            'is_active': property_record.is_active if property_record else False,
            'status': 'Active' if property_record and property_record.is_active else 'Inactive or Unavailable'
        },
        'entrance': {
            'id': entrance.id,
            'name': entrance.name,
            'is_active': entrance.is_active,
            'status': 'Active' if entrance.is_active else 'Inactive or Unavailable'
        },
        'eligibility': {
            'is_eligible': eligible,
            'reason': eligibility_reason,
        },
        'last_access_attempt': {
            'result': last_attempt.result,
            'created_at': (last_attempt.created_at.isoformat() if last_attempt else 'Never'),
        } if last_attempt else None
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

@access_control_bp.route('/entrances', methods=['GET'])
@login_required
def get_entrances():
    entrances = Entrance.query.filter_by(is_active=True).order_by(Entrance.name.asc()).all()
    return jsonify({
        'success': True,
        'entrances': [
            {
                'id': entrance.id,
                'name': entrance.name,
                'entrance_code': entrance.entrance_code,
                'property_id': entrance.property_id
            }
            for entrance in entrances
        ]
    }), 200
