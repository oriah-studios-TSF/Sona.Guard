from datetime import datetime, timezone

from app.extensions import db


# The AuditLog model provides a centralized audit trail for system-level security events
# (such as login successes, failed password attempts, blocked user actions, and logouts).
#
# Difference between AuditLog and AccessAttempt:
# - `AccessAttempt`: Tracks physical access events at physical estate gates (e.g. resident/visitor checks).
# - `AuditLog`: Tracks software-level security events and administrative actions on the web platform.
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    # Primary key: Unique integer identifying this audit log record.
    id = db.Column(db.Integer, primary_key=True)

    # FOREIGN KEY (Nullable):
    # Links to the User who triggered the event.
    # Why it is nullable: Failed login attempts or requests from unauthenticated clients do not
    # have an authenticated user yet, so `user_id` can be None while still recording the event.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    # Categorical classification of the event (e.g. 'LOGIN_SUCCESS', 'LOGIN_FAILURE', 'LOGIN_BLOCKED').
    # Standardized event types allow security tools and admins to filter and detect brute-force patterns.
    event_type = db.Column(db.String(50), nullable=False)

    # Detailed description of what occurred (e.g. 'Invalid credentials supplied.').
    description = db.Column(db.String(255), nullable=False)

    # Client IP address (supports both IPv4 and IPv6 strings up to 45 characters).
    # Useful for forensic investigations to identify where unauthorized access attempts originated.
    ip_address = db.Column(db.String(45), nullable=True)

    # UTC timestamp of when the event occurred.
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # DATABASE RELATIONSHIP:
    # Connects this log entry to the User model.
    # `backref='audit_logs'` adds a `.audit_logs` attribute to User objects, allowing administrators
    # to query all security logs associated with a particular staff member.
    user = db.relationship(
        'User',
        backref='audit_logs'
    )


