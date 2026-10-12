from flask import Blueprint, render_template
from flask_login import login_required
from app.services.auth import role_required

# The dashboard blueprint handles the primary operations overview and administrative views.
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Endpoint: GET /dashboard/
# Renders the main operations overview dashboard where staff view system statistics and shortcuts.
@dashboard_bp.route('/')
# Security measure: Restricts access to authenticated staff members.
@login_required
def index():
    return render_template(
        'dashboard/index.html',
        title='Dashboard',
        title_description='Monitor and manage access across your facility.',
        icon='tachometer-alt'
    )

# Endpoint: GET /dashboard/admin-test
# Test endpoint demonstrating Role-Based Access Control (RBAC).
@dashboard_bp.route('/admin-test')
# Security measure: `@role_required('admin')` ensures only users whose `role` attribute is exactly 'admin'
# can view this endpoint. Security officers attempting to access this route receive an HTTP 403 Forbidden error.
@role_required('admin')
def admin_test():
    return 'Admin authorization successful'



