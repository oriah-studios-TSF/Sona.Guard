# This module declares Flask extension instances in a standalone file without binding them
# directly to a specific Flask app instance yet.
# In Flask architecture, this pattern avoids "circular import" dependencies: models and routes
# can safely import `db`, `limiter`, or `login_manager` without needing to import `create_app` or `app`.
# The extensions are later bound to the actual Flask app in `app/__init__.py` using their `.init_app()` methods.

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# SQLAlchemy is the Object-Relational Mapper (ORM). It allows us to interact with our SQL database
# using Python classes and objects instead of raw SQL queries.
db = SQLAlchemy()

# CSRFProtect provides protection against Cross-Site Request Forgery (CSRF).
# It ensures that state-changing HTTP requests (POST, PUT, DELETE) contain a valid secret token
# issued to the user's session, preventing unauthorized commands from external sites.
csrf = CSRFProtect()

# LoginManager handles user session management (logging in, logging out, remembering sessions)
# and provides helpers like the `@login_required` decorator and the `current_user` proxy.
login_manager = LoginManager()

# Migrate integrates Alembic database migrations with Flask, allowing schema changes to be tracked
# and applied incrementally across environments without dropping existing data.
migrate = Migrate()

# Limiter provides rate limiting for endpoints.
# `key_func=get_remote_address` tracks request counts per client IP address,
# protecting against brute-force password guessing and denial-of-service abuse.
limiter = Limiter(key_func=get_remote_address)

