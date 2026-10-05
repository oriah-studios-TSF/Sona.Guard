from flask import Blueprint, render_template


from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('auth/login.html')