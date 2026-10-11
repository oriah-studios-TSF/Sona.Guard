from flask import Blueprint, jsonify, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User
from app.extensions import limiter
from app.services.audit import log_event


# The auth blueprint handles user authentication and session management under the '/auth' URL prefix.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Endpoint: POST /auth/login
# Authenticates security staff and administrators into the application.
@auth_bp.route('/login', methods=['POST'])
# Security measure: Rate limiting (Flask-Limiter).
# Restricts clients to a maximum of 5 login attempts per minute per IP address.
# This defends against automated brute-force password guessing and credential-stuffing attacks.
@limiter.limit("5 per minute")
def login():
    # Safely parse the incoming JSON payload.
    # `silent=True` prevents Flask from raising an unhandled 400 exception if the body is invalid JSON.
    data = request.get_json(silent=True) or {}
    
    # Sanitize and extract credentials from the request body.
    staff_code = data.get('staff_code', '').strip()
    password = data.get('password', '').strip()

    # Input validation: Ensure both fields are provided before querying the database.
    if not staff_code or not password:
        return jsonify({
            'success': False,
            'message': 'Please enter your staff code and password.'
        }), 400
    
    # Query the user by their unique staff identifier.
    user = User.query.filter_by(staff_code=staff_code).first()
    
    # Authentication check:
    # Verify that the user exists and that the candidate password matches the stored password hash.
    # Security note: Returning the same generic error message whether the staff code was not found
    # OR the password was wrong prevents "username enumeration" (attackers cannot figure out which
    # staff codes exist in the system).
    if not user or not user.check_password(password):
        # Record the failed attempt in our security audit log.
        log_event('LOGIN_FAILURE', 'Invalid credentials supplied.', user_id=user.id if user else None)
        return jsonify({'success': False, 'message': 'Invalid credentials. Make sure your staff code and password are correct.'}), 401
    
    # Check if the account has been disabled/blocked by an administrator.
    if not user.is_active:
        log_event('LOGIN_BLOCKED', 'Blocked account attempted to login.', user_id=user.id)
        return jsonify({'success': False, 'message': 'This account has been blocked. Please contact your system administrator.'}), 403
    
    # Establish the user session:
    # `login_user(user)` registers the user's ID inside Flask's secure, signed session cookie.
    login_user(user)

    # Record the successful login event for auditing and compliance.
    log_event('LOGIN_SUCCESS', 'User logged in successfully.', user_id=user.id)

    flash('You have successfully been logged in.', 'success')
    
    # Return a 200 OK JSON response allowing the frontend JavaScript to redirect to the dashboard.
    return jsonify({'success': True, 'message': 'Login successful.'}), 200

# Endpoint: POST /auth/logout
# Logs out the currently authenticated user and clears their session.
@auth_bp.route('/logout', methods=['POST'])
# Security measure: Enforces that only currently authenticated users can call this endpoint.
@login_required
def logout():
    user_id = current_user.id
    
    # Record the logout event in the audit trail before clearing user session state.
    log_event('LOGOUT_SUCCESS', 'User logged out successfully.', user_id=user_id)
    
    # `logout_user()` removes the user ID from the active session and clears authentication cookies.
    logout_user()

    flash('You have been logged out successfully.', 'success')
    
    return jsonify({'success': True, 'message': 'You have been logged out successfully.'}), 200

# Error Handler for HTTP 429 (Too Many Requests):
# When a client exceeds the `@limiter.limit` threshold, Flask-Limiter triggers a 429 error.
# This custom handler intercepts the error and returns a clean, user-friendly JSON message.
@auth_bp.errorhandler(429)
def rate_limit_handler(error):
    return jsonify({'success': False, 'message': 'Too many login attempts. Please wait a moment before trying again.'}), 429


