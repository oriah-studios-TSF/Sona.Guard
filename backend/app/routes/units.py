from flask import Blueprint, render_template
from flask_login import login_required
from app.services.auth import role_required

# The units blueprint manages residential units within each estate.
units_bp = Blueprint('units', __name__, url_prefix='/units')

# Endpoint: GET /units
# Displays the unit management page for viewing and managing residential units.
@units_bp.route('/units')
@login_required
def index():
    return render_template(
        'units/index.html',
        title='Units',
        title_description='Manage residential units and house assignments within your estate.',
        icon='house-user'
    )