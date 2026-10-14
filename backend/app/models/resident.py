from datetime import datetime, timezone

from app.extensions import db


# The Resident model represents an authorized tenant, homeowner, or inhabitant of a property.
# In Sona.Guard, access can be verified directly against a Resident's unique code, and residents
# are also the individuals authorized to create visitor passes for incoming guests.
class Resident(db.Model):
    __tablename__ = 'residents'

    # Primary key: Unique integer identifying this resident record.
    id = db.Column(db.Integer, primary_key=True)

    # FOREIGN KEY:
    # `db.ForeignKey('properties.id')` links this resident to a specific row in the `properties` table.
    # Why it matters: In a multi-tenant estate management system, every resident must belong to
    # an estate. During gate verification, the system compares the resident's `property_id` with the
    # gate's `property_id` to ensure residents from one estate cannot access another estate.
    property_id = db.Column(
        db.Integer,
        db.ForeignKey('properties.id'),
        nullable=False
    )

    # The specific house or unit where this resident lives
    unit_id = db.Column(db.Integer,db.ForeignKey('units.id'), nullable=True)

    # Unique identifier presented at gate checkpoints (e.g. on an RFID tag, mobile app, or barcode).
    # Guard interfaces query by this code to retrieve resident details quickly.
    resident_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    # Apartment, house, or unit identifier within the property (e.g. 'A-101').
    unit_number = db.Column(db.String(50), nullable=False)

    # Resident's full legal name.
    full_name = db.Column(db.String(120), nullable=False)

    # Primary contact telephone number used for gate notifications or visitor authorization calls.
    phone_number = db.Column(db.String(30), nullable=False)

    # Optional contact email address.
    email = db.Column(db.String(120), nullable=True)

    # Status flag: If set to False, access verification is denied.
    # Soft deactivation allows estates to revoke access (e.g. lease ended or security suspension)
    # without deleting historical access logs that reference this resident.
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Timezone-aware audit timestamps tracking record creation and last update in UTC.
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

    # The unit this resident is associated with
    unit = db.relationship('Unit', back_populates='residents', lazy=True) 

