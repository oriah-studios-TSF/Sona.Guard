from flask import Flask

from app.config import Config
from app.extensions import db, csrf, migrate, login_manager, limiter
from app.models import User
from app.routes import main_bp, auth_bp, dashboard_bp, access_control_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevents MIME type sniffing, as in browsers trying to guess the content type
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'  # Prevents clickjacking by only allowing the same origin to load the content
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'  # Prevents leaking the referrer to cross-origin requests
        
        return response

    login_manager.login_view = 'main.home'
    login_manager.login_message = 'Please login to access the Sona.Guard dashboard.'
    login_manager.login_message_category = 'error'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(access_control_bp)

    return app
