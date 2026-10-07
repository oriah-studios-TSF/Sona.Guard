from datetime import datetime, timezone

from app.extensions import db

class AccessAttempt(db.Model):
    __tablename__ = 'access_attempts'

    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    entrance_id = db.Column(db.Integer, db.ForeignKey('entrances.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=True)

    result = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    person = db.relationship('Person', backref='access_attempts')
    
    entrance = db.relationship('Entrance', backref='access_attempts')
    
    user = db.relationship('User', backref='access_attempts')
    
    permission = db.relationship('Permission', backref='access_attempts')

    

    



    