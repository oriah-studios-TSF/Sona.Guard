from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User
from app.extensions import limiter
from app.services.audit import log_event


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    
    data = request.get_json()
    
    employee_id = data.get('employee_id', '').strip()
    password = data.get('password', '').strip()
    
    user = User.query.filter_by(employee_id=employee_id).first()
    
    if not user or not user.check_password(password):
        log_event('LOGIN_FAILURE', 'Invalid credentials supplied.', user_id=user.id if user else None)
        return jsonify({'success': False, 'message': 'Invalid credentials. Make sure your employee ID and password are correct.'}), 401
    
    if not user.is_active:
        log_event('LOGIN_BLOCKED', 'Blocked account attempted to login.', user_id=user.id)
        return jsonify({'success': False, 'message': 'This account has been blocked. Please contact your system administrator.'}), 403
    
    login_user(user)

    log_event('LOGIN_SUCCESS', 'User logged in successfully.', user_id=user.id)
    
    return jsonify({'success': True, 'message': 'Login successful.'}), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    user_id = current_user.id
    
    log_event('LOGOUT_SUCCESS', 'User logged out successfully.', user_id=user_id)
    
    logout_user()
    return jsonify({'success': True, 'message': 'You have been logged out successfully.'}), 200

@auth_bp.errorhandler(429)
def rate_limit_handler(error):
    return jsonify({'success': False, 'message': 'Too many login attempts. Please wait a moment before trying again.'}), 429

