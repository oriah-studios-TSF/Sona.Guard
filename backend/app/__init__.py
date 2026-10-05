from flask import Flask

from app.config import Config
from app.extensions import db, csrf, migrate, login_manager
from app.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
