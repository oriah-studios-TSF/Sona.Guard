from datetime import datetime, timezone

from app.extensions import db


# The AccessAttempt model represents an immutable audit log entry created each time someone
# attempts to enter or exit through a property gate.
#
# Security & Forensics Purpose:
# In physical access systems, recording every verification attempt (both 'granted' and 'denied')
# provides non-repudiation and an audit trail. If an unauthorized person attempts to enter
# or a security incident occurs, security officers can review timestamps, gates, and responsible guards.
class AccessAttempt(db.Model):
    __tablename__ = 'access_attempts'

    # Primary key: Unique integer identifying this specific access attempt.
    id = db.Column(db.Integer, primary_key=True)

    # FOREIGN KEY: The Property where the attempt occurred.
    # Enforces that all access attempts belong to a known estate.
    property_id = db.Column(
        db.Integer,
        db.ForeignKey('properties.id'),
        nullable=False
    )

    # FOREIGN KEY: The specific Entrance checkpoint where verification took place.
    # Allows analytics on gate traffic and pinpointing exactly which physical barrier was checked.
    entrance_id = db.Column(
        db.Integer,
        db.ForeignKey('entrances.id'),
        nullable=False
    )

    # FOREIGN KEY (Optional): The logged-in guard (User) who performed the verification.
    # Holds guards accountable by linking every decision directly to their user account.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    # Subject Identification (Nullable Foreign Keys):
    # Depending on whether a resident or a visitor is being checked, one of the two fields below is populated:
    
    # 1. Populated if the person attempting access is a resident.
    resident_id = db.Column(
        db.Integer,
        db.ForeignKey('residents.id'),
        nullable=True
    )

    # 2. Populated if the person attempting access is a visitor holding a temporary pass.
    visitor_authorization_id = db.Column(
        db.Integer,
        db.ForeignKey('visitor_authorizations.id'),
        nullable=True
    )

    # Verification decision: Typically 'granted' or 'denied'.
    result = db.Column(db.String(20), nullable=False)

    # Explanation of the decision (e.g. 'Resident verified. Access permitted.', 'Entrance is inactive.').
    reason = db.Column(db.String(255), nullable=True)

    # Exact UTC timestamp of when the gate check occurred.
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # DATABASE RELATIONSHIPS:
    # -----------------------
    # Relationships enable object-oriented lookup and reverse navigation:

    # Navigates to the Property record. Adds `property.access_attempts`.
    property = db.relationship(
        'Property',
        backref='access_attempts'
    )

    # Navigates to the Entrance record. Adds `entrance.access_attempts`.
    entrance = db.relationship(
        'Entrance',
        backref='access_attempts'
    )

    # Navigates to the User (guard) who verified the entry. Adds `user.access_attempts`.
    user = db.relationship(
        'User',
        backref='access_attempts'
    )

    # Navigates to the Resident if this was a resident verification. Adds `resident.access_attempts`.
    resident = db.relationship(
        'Resident',
        backref='access_attempts'
    )

    # Navigates to the VisitorAuthorization if this was a visitor verification. Adds `visitor_authorization.access_attempts`.
    visitor_authorization = db.relationship(
        'VisitorAuthorization',
        backref='access_attempts'
    )



    

    



    