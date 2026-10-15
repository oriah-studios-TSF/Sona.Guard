from flask_login import current_user

from app.extensions import db
from app.models import Property, Unit, Resident
from app.services.auth import can_access_property


# Retrieve all units belonging to a specific property
def get_units_by_property(property_id):
    # Check if the user has permission to access the property
    if not can_access_property(property_id):
        raise PermissionError('You do not have permission to access this property.') 
     
    property_record = db.session.get(Property, property_id)
    
    if not property_record:
        raise ValueError('Property not found.')  
     
    return Unit.query.filter_by(property_id=property_id).order_by(Unit.unit_number.asc()).all()

# Create a new unit
def create_unit(property_id, unit_number, unit_type='house'):
    # Only System owners and Estate Administrators can create units

    if current_user.role not in {'system_owner', 'estate_admin'}:
        raise PermissionError('You do not have permission to create units.')

    if not can_access_property(property_id):
        raise PermissionError('You do not have permission to create units for this property.')

    property_record = db.session.get(Property, property_id)
    
    if not property_record:
        raise ValueError('Property not found.')

    if not property_record.is_active:
        raise ValueError('Cannot create units for an inactive property.')

    # Validate and normalise the unit number
    if not isinstance(unit_number, str):
        raise ValueError('Unit number must be text.')

    unit_number = unit_number.strip()

    if not unit_number:
        raise ValueError('Unit number is required.')

    # Validate the unit type against the supported types in V1
    allowed_unit_types = {'house', 'apartment', 'townhouse'}

    if not isinstance(unit_type, str) or unit_type not in allowed_unit_types:
        raise ValueError(f'Invalid unit type. Allowed types are: {", ".join(allowed_unit_types)}')

    # Prevent empty unit numbers
    if not unit_number:
        raise ValueError('Unit number is required.')

    # Prevent duplicate unit numbers within the same property
    existing_unit = Unit.query.filter_by(
        property_id=property_id,
        unit_number=unit_number
    ).first()

    if existing_unit:
        raise ValueError('A unit with this number already exists in this property.')

    # Add unit to the database
    unit = Unit(
        property_id=property_id,
        unit_number=unit_number,
        unit_type=unit_type
    )

    db.session.add(unit)
    db.session.commit()

    return unit

# Calculate unit management statistics for a specific property
def get_unit_statistics(property_id):

    # Retrieve only units the current user is allowed to access
    units = get_units_by_property(property_id)

    total_units = len(units)
    occupied_units = 0
    vacant_units = 0
    inactive_units = 0

    for unit in units:
        # Inactive units arecounted seperately
        if not unit.is_active:
            inactive_units += 1
            continue

        # Check whether the unit has at least one active resident
        has_active_resident = any(
            resident.is_active for resident in unit.residents
        )

        if has_active_resident:
            occupied_units += 1
        else:
            vacant_units += 1

    return {
        'total_units': total_units,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'inactive_units': inactive_units
    }