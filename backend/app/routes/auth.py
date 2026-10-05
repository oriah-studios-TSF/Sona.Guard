from flask import Blueprint, jsonify, request
from flask_login import login_user

from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/sign-in', methods=['POST'])
def sign_in():
    
    data = request.get_json()
    
    employee_id = data.get('employee_id', '').strip()
    password = data.get('password', '').strip()
    
    user = User.query.filter_by(employee_id=employee_id).first()
    
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid credentials. Make sure your employee ID and password are correct.'}), 401
    
    if not user.is_active:
        return jsonify({'success': False, 'message': 'This account has been blocked. Please contact your system administrator.'}), 403
    
    login_user(user)
    
    return jsonify({'success': True, 'message': 'Sign in successful.'}), 200