from datetime import datetime, timezone

from app.extensions import db


class Person(db.Model):
    __tablename__= 'people'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(30), unique=True, nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    nationality = db.Column(db.String(80), nullable=True)
    department = db.Column(db.String(120), nullable=True)
    job_title = db.Column(db.String(120), nullable=True)
    workplace = db.Column(db.String(150), nullable=True)
    credential_expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    
    