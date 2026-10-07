from datetime import datetime, timezone

from app.extensions import db

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    entrance_id = db.Column(db.Integer, db.ForeignKey('entrances.id'), nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    valid_from = db.Column(db.DateTime(timezone=True), nullable=True)
    valid_until = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    
    updated_by = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    person = db.relationship('Person', backref='permissions')
    entrance = db.relationship('Entrance', backref='permissions')
    created_by = db.relationship('User', foreign_keys=[created_by_user_id], backref='created_permissions')


    
    