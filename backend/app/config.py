import os

# python-dotenv reads key-value pairs from a local `.env` file and adds them to environment variables.
# This follows the 12-Factor App methodology: keeping sensitive configuration (like database credentials
# and secret keys) out of source control.
from dotenv import load_dotenv

load_dotenv()


# The Config class centralizes all configuration parameters for Flask and its extensions.
# Flask can load these settings using `app.config.from_object(Config)`.
class Config:
    # SECRET_KEY is used by Flask and its extensions to cryptographically sign session cookies
    # and generate CSRF tokens. Without a strong, secret key, attackers could tamper with session data.
    SECRET_KEY = os.getenv('SECRET_KEY')

    # SQLALCHEMY_DATABASE_URI defines the database connection string (e.g. 'sqlite:///instance/sona_guard.db').
    # It tells SQLAlchemy which database engine to connect to and where it is hosted.
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    # Setting this to False disables Flask-SQLAlchemy's event modification tracking system,
    # which uses significant extra memory and is not needed for standard operations.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security measure: Restricts the session cookie so that client-side JavaScript (e.g. `document.cookie`)
    # cannot read it. This mitigates the risk of session hijacking via Cross-Site Scripting (XSS).
    SESSION_COOKIE_HTTPONLY = True

    # Security measure: Restricts when session cookies are sent with cross-site requests.
    # 'Lax' provides a balance of user convenience and security, helping prevent Cross-Site Request
    # Forgery (CSRF) attacks by blocking cookie transmission on third-party cross-site requests.
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Fail-fast principle: If critical environment variables are absent, abort application startup
    # immediately rather than failing silently or running in an insecure state during production.
    if not SECRET_KEY:
        raise RuntimeError('SECRET_KEY is missing from the environment.')

    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError('DATABASE_URI is missing from the environment.')