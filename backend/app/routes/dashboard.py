from flask import Blueprint, render_template
from flask_login import login_required
from app.services.auth import role_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')

@dashboard_bp.route('/admin-test')
@role_required('admin')
def admin_test():
    return 'Admin authorization successful'


