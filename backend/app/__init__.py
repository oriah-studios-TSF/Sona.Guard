from flask import Flask

from app.config import Config
from app.extensions import db, csrf, migrate, login_manager, limiter
from app.models import User
import app.models
from app.routes import main_bp, auth_bp, dashboard_bp, access_control_bp

# The Application Factory function.
# In Flask, using a factory function instead of a single global app instance allows us to:
# 1. Create separate instances for unit testing (e.g. using an in-memory SQLite database).
# 2. Prevent circular imports between extensions, models, and routes.
# 3. Support running multiple configurations (development, testing, production) cleanly.
def create_app():
    # Instantiate the Flask WSGI application object.
    app = Flask(__name__)
    
    # Load configuration settings (such as SECRET_KEY and DATABASE_URI) from our Config class.
    app.config.from_object(Config)

    # Initialize extensions with this specific Flask application instance.
    # This attaches database connections, migration hooks, CSRF validation, and rate limits to the app.
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    # The `@app.after_request` hook executes after each view function finishes handling a request.
    # Here, it appends standard HTTP security headers to every outgoing response to protect users.
    @app.after_request
    def set_security_headers(response):
        # Prevents browsers from "sniffing" (guessing) the MIME type of a file different from the declared
        # Content-Type, mitigating attacks where malicious user uploads are executed as scripts.
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # Mitigates clickjacking attacks by ensuring the application's pages cannot be embedded
        # within <iframe> elements on third-party websites. Only pages from the same origin are allowed.
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'

        # Prevents leakage of full URL query parameters in the Referer header when navigating to external origins.
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

    # Configure Flask-Login behavior:
    # `login_view` specifies the endpoint name to redirect users to when they attempt to access a protected route.
    login_manager.login_view = 'main.home'
    login_manager.login_message = 'Please login to access the Sona.Guard dashboard.'
    login_manager.login_message_category = 'error'

    # The user loader callback is required by Flask-Login.
    # On every incoming request containing a session cookie, Flask-Login extracts the stored user ID
    # and calls this function to load the active User model from the database into `current_user`.
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints:
    # Blueprints organize an application into distinct logical modules with their own routes and URL prefixes.
    # - main_bp: Root landing page and public views
    # - auth_bp: Authentication endpoints (/auth/login, /auth/logout)
    # - dashboard_bp: Guard and admin dashboard pages (/dashboard)
    # - access_control_bp: Gate verification and access check endpoints (/access)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(access_control_bp)

    return app

