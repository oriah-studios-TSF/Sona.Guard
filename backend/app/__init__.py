from flask import Flask

from app.config import Config
from app.extensions import db, csrf, migrate, login_manager
from app.models import User
from app.routes import main_bp, auth_bp, dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'main.home'
    login_manager.login_message = 'Please login to access the Sona.Guard dashboard.'
    login_manager.login_message_category = 'error'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    return app
