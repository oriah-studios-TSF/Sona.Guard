from datetime import datetime, timezone

from app.extensions import db


class Entrance(db.Model):
    __tablename__ = 'entrances'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    entrance_code = db.Column(db.String(50), unique=True, nullable=False)
    entrance_type = db.Column(db.String(50), nullable=False, default='door')
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_by = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))