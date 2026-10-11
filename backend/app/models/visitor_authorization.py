from datetime import datetime, timezone

from app.extensions import db


# The VisitorAuthorization model represents a time-bounded access pass granted to a visitor.
# In relational database design, this acts as a junction entity connecting visitors, residents,
# properties, entrances, and security officers together.
class VisitorAuthorization(db.Model):
    __tablename__ = 'visitor_authorizations'

    # Primary key: Unique identifier for this authorization record.
    id = db.Column(db.Integer, primary_key=True)

    # FOREIGN KEY: Links to the Visitor being granted access.
    # Why it matters: Identifies the person arriving at the gate.
    visitor_id = db.Column(
        db.Integer,
        db.ForeignKey('visitors.id'),
        nullable=False
    )

    # FOREIGN KEY: Links to the Resident who issued or approved the visit.
    # Why it matters: Enforces accountability; every visitor must be sponsored by a verified tenant.
    resident_id = db.Column(
        db.Integer,
        db.ForeignKey('residents.id'),
        nullable=False
    )

    # FOREIGN KEY: Links to the Property where the visit will take place.
    # Why it matters: Ensures multi-tenant isolation so an authorization cannot be applied to another estate.
    property_id = db.Column(
        db.Integer,
        db.ForeignKey('properties.id'),
        nullable=False
    )

    # FOREIGN KEY (Optional): The specific gate approved for this visit.
    # If set, the visitor is only allowed entry through this entrance (e.g. 'Visitor Gate').
    # If null, the visitor may enter through any valid entrance belonging to the property.
    entrance_id = db.Column(
        db.Integer,
        db.ForeignKey('entrances.id'),
        nullable=True
    )

    # Access validity window:
    # Restricting access between `valid_from` and `valid_until` prevents expired passes
    # from being reused at a later date.
    valid_from = db.Column(
        db.DateTime(timezone=True),
        nullable=False
    )

    valid_until = db.Column(
        db.DateTime(timezone=True),
        nullable=False
    )

    # Lifecycle status: e.g. 'pending', 'approved', 'denied', 'expired', or 'used'.
    status = db.Column(
        db.String(20),
        nullable=False,
        default='pending'
    )

    # Timestamp recording when the hosting resident initially approved the pass.
    authorised_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    # Timestamp recording when the pass was verified at the gate.
    confirmed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    # FOREIGN KEY (Optional): Links to the guard (`users.id`) who handled gate-side verification.
    # Why it matters: Ensures full operator traceability in security audits.
    confirmed_by_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    # Timestamp recording when this authorization record was initially inserted.
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # DATABASE RELATIONSHIPS:
    # -----------------------
    # Each relationship below allows object-oriented navigation between models in Python:

    # Connects to the Visitor model. Adds `visitor.authorizations` backreference list.
    visitor = db.relationship(
        'Visitor',
        backref='authorizations'
    )

    # Connects to the Resident model. Adds `resident.visitor_authorizations` backreference list.
    resident = db.relationship(
        'Resident',
        backref='visitor_authorizations'
    )

    

    # Connects to the Property model. Adds `property.visitor_authorizations` backreference list.
    property = db.relationship(
        'Property',
        backref='visitor_authorizations'
    )

    # Connects to the Entrance model. Adds `entrance.visitor_authorizations` backreference list.
    entrance = db.relationship(
        'Entrance',
        backref='visitor_authorizations'
    )

    # Connects to the User model (the security guard).
    # `foreign_keys=[confirmed_by_user_id]` explicitly informs SQLAlchemy which foreign key column
    # to join on, preventing ambiguity when resolving relationship mappings to User.
    confirmed_by = db.relationship(
        'User',
        foreign_keys=[confirmed_by_user_id],
        backref='confirmed_visitor_authorizations'
    )


