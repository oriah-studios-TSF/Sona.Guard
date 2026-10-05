from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required

from app.models import User
from app.extensions import limiter


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    
    data = request.get_json()
    
    employee_id = data.get('employee_id', '').strip()
    password = data.get('password', '').strip()
    
    user = User.query.filter_by(employee_id=employee_id).first()
    
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid credentials. Make sure your employee ID and password are correct.'}), 401
    
    if not user.is_active:
        return jsonify({'success': False, 'message': 'This account has been blocked. Please contact your system administrator.'}), 403
    
    login_user(user)
    
    return jsonify({'success': True, 'message': 'Login successful.'}), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'You have been logged out successfully.'}), 200

@auth_bp.errorhandler(429)
def rate_limit_handler(error):
    return jsonify({'success': False, 'message': 'Too many login attempts. Please wait a moment before trying again.'}), 429

