from flask import has_request_context, request

from app.extensions import db
from app.models import AuditLog


# Centralized Audit Service:
# In backend architecture, isolating audit logging inside a dedicated service prevents duplicate
# database code across route handlers and ensures standardized event recording throughout the app.
def log_event(event_type, description, user_id=None):
    # Context Detection:
    # `has_request_context()` checks if this function was called during an incoming HTTP web request.
    # If yes, we can safely extract `request.remote_addr` (the client's IP address).
    # If no (e.g. executed inside a CLI script, seed script, or background task), `ip_address` defaults
    # to None to avoid raising a RuntimeError outside of a request context.
    ip_address = request.remote_addr if has_request_context() else None

    # Construct the AuditLog model instance with the event details.
    audit_log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        description=description,
        ip_address=ip_address,
    )

    # Stage the new audit log in SQLAlchemy's session and commit it to the database immediately.
    # Committing immediately ensures that security events are saved even if later operations encounter errors.
    db.session.add(audit_log)
    db.session.commit()