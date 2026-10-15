from app.services.units import get_units_by_property, get_unit_statistics
from flask import Blueprint, render_template, abort
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
        statistics = {
            'total_units': 0,
            'occupied_units': 0,
            'vacant_units': 0,
            'inactive_units': 0
        }
        
        return render_template(
            'units/index.html',
            title='Unit Management',
            title_description='Manage residential units and house assignments within your estate.',
            icon='house-user',
            units=[],
            properties=None,
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