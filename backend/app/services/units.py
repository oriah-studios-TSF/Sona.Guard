from app.extensions import db

from app.models import Unit

# Retrieve all units belonging to a specific property
def get_units_by_property(property_id):
    return Unit.query.filter_by(property_id=property_id).order_b(Unit.unit_number.asc()).all()

# Create a new unit
def create_unit(property_id, unit_number, unit_type='house'):
    # Remove extra spaces from the unit number
    unit_number = unit_number.strip()

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