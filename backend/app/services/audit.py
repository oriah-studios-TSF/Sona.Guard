from flask import request

from app.extensions import db
from app.models import AuditLog

def log_event(event_type, description, user_id=None):
    audit_log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        description=description,
        ip_address=request.remote_addr,
    )
    db.session.add(audit_log)
    db.session.commit()