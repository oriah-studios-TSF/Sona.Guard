from flask import Blueprint, render_template

# Re-exporting child blueprints:
# Grouping the individual blueprints here allows the application factory in `app/__init__.py`
# to import all application blueprints from a single, clean import path (`from app.routes import ...`).
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.access_control import access_control_bp

# The `main_bp` Blueprint manages top-level, general routes that do not require a sub-prefix.
main_bp = Blueprint('main', __name__)

# Root Route:
# Handles GET requests to the website's root URL ('/').
# Serves the initial login page template (`templates/auth/login.html`) to users visiting the application.
@main_bp.route('/')
def home():
    return render_template('auth/login.html')