from app.services.units import get_units_by_property, get_unit_statistics, get_all_properties, get_all_units, create_unit, update_unit, get_residents_by_unit
from app.models import Unit, Property, Resident
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.auth import role_required

# The units blueprint manages residential units within each estate.
units_bp = Blueprint('units', __name__, url_prefix='/units')

# Endpoint: GET /units
# Displays the unit management page for viewing and managing residential units.
@units_bp.route('/')
@role_required('system_owner', 'estate_admin', 'security_supervisor')
def index():

    # System owners can manage units across estates, so they need to select an estate first.
    # Estate admins and security supervisors can only manage units within their assigned estate.
    if current_user.role == 'system_owner':
        units = get_all_units()
        properties = get_all_properties()

        statistics = {
            'total_units': len(units),
            'occupied_units': sum(
                1 for unit in units
                if unit.is_active and any(
                    resident.is_active for resident in unit.residents
                )
            ),
            'vacant_units': sum(
                1 for unit in units
                if unit.is_active and not any(
                    resident.is_active for resident in unit.residents
                )
            ),
            'inactive_units': sum(1 for unit in units if not unit.is_active),
        }
        
        
        return render_template(
            'units/index.html',
            title='Unit Management',
            title_description='Manage residential units and house assignments within your estate.',
            icon='house-user',
            units=units,
            properties=properties,
            statistics=statistics
        )

    # Estate-scoped usres must have a property assigned to their account
    property_id = current_user.property_id

    
    if property_id is None:
        abort(403)

    # Get all units for the current user's property
    try:
        units = get_units_by_property(current_user.property_id)
        statistics = get_unit_statistics(current_user.property_id)
    except PermissionError:
        abort(403)
    except ValueError:
        abort(403)

    return render_template(
        'units/index.html',
        title='Unit Management',
        title_description='Manage residential units and house assignments within your estate.',
        icon='house-user',
        units=units,
        statistics=statistics,
        properties=None
    )


# Endpoint: POST /units/create
# Create a resedential unit withing an authorized property
@units_bp.route('/create', methods=['POST'])
@role_required('system_owner', 'estate_admin')
def create():
    # System Owners select the property, Estate Admins user their assigned property
    if current_user.role == 'system_owner':
        property_id = request.form.get('property_id', type=int)
    else:
        property_id = current_user.property_id

    unit_number = request.form.get('unit_number', '').strip().upper()
    unit_type = request.form.get('unit_type', '').strip().lower()

    try:
        unit = create_unit(property_id, unit_number, unit_type)
        flash(f'Unit {unit.unit_number} has been created successfully', 'success')
    except (PermissionError, ValueError) as error:
        flash(str(error), 'error')

    return redirect(url_for('units.index'))

# Edit a residential unit within an authorized property
@units_bp.route('/<int:unit_id>/edit', methods=['POST'])
@role_required('system_owner', 'estate_admin')
def edit(unit_id):
    unit_number = request.form.get('unit_number', '').strip().upper()
    unit_type = request.form.get('unit_type', '').strip().lower()
    status_value = request.form.get('is_active', '')

    # Validate the status value, it should be either 'true' or 'false'
    if status_value not in {'true', 'false'}:
        flash('Please select a valid status for the unit', 'error')
        return redirect(url_for('units.index'))

    # Convert the status value to a boolean
    is_active = status_value == 'true'

    try:
        unit = update_unit(unit_id, unit_number, unit_type, is_active)
        flash(f'Unit {unit.unit_number} has been updated successfully', 'success')
    except PermissionError:
        abort(403)
    except ValueError as error:
        flash(str(error), 'error')

    return redirect(url_for('units.index'))

# Retrieve resident assignments for specific unit
@units_bp.route('/<int:unit_id>/residents', methods=['GET'])
@role_required('system_owner', 'estate_admin', 'security_supervisor')
def residents(unit_id):
    # Retieve the residents assigned to this unit 
    try:
        residents = get_residents_by_unit(unit_id)
    except PermissionError:
        abort(403)
    except ValueError:
        abort(404)

    # Convert each Resident model object into a dictionary
    resident_data = [
        {
            'id': resident.id,
            'full_name': resident.full_name,
            'resident_code': resident.resident_code,
            'email': resident.email,
            'phone_number': resident.phone_number,
            'is_active': resident.is_active
        }
        for resident in residents
    ]

    # Send the resident data back to the browser
    return jsonify({'residents': resident_data})

    

    

    