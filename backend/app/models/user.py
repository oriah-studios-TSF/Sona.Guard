from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


# The User model represents security guards, supervisors, and system administrators.
# It inherits from two classes:
# 1. `UserMixin`: Provided by Flask-Login. It gives standard implementations for user session
#    properties such as `is_authenticated`, `is_active`, `is_anonymous`, and `get_id()`.
# 2. `db.Model`: The SQLAlchemy base class that maps this Python class to a database table.
class User(UserMixin, db.Model):
    # Specifies the exact table name inside the database.
    __tablename__ = 'users'

    # Primary key: A unique integer assigned to each user row for database indexing and joins.
    id = db.Column(db.Integer, primary_key=True)

    # Identifier used by guards and administrators to log in (e.g. 'SONA-STAFF-001').
    # `unique=True` ensures two users cannot register with the identical staff code.
    staff_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    # Full display name of the staff member.
    full_name = db.Column(db.String(120), nullable=False)

    # Cryptographic hash of the user's password.
    # Storing a one-way hash instead of plaintext ensures that even if the database is compromised,
    # raw passwords remain protected against attackers.
    password_hash = db.Column(db.String(255), nullable=False)

    # Role-Based Access Control (RBAC) identifier.
    # Expected values include 'admin' and 'security_officer'.
    # Used by route protection decorators (like `@role_required`) to restrict sensitive actions.
    role = db.Column(
        db.String(50),
        nullable=False,
        default='security_officer'
    )

    # Account status flag: Allows administrators to deactivate/block a user without deleting
    # their account. This preserves database foreign keys and historical audit log records.
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Timezone-aware audit timestamps.
    # Using a callable lambda (`lambda: datetime.now(timezone.utc)`) ensures that the current UTC time
    # is evaluated dynamically whenever a new record is created or updated, rather than once at module load.
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Hashes the plaintext password with a random salt using Werkzeug's default algorithm (scrypt/pbkdf2).
    # Salting ensures identical passwords generate completely different hashes, thwarting rainbow table attacks.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verifies a supplied candidate password against the stored password hash.
    # Uses constant-time comparison to prevent side-channel timing attacks.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


