from datetime import datetime, timezone

from app.extensions import db


# The Visitor model represents an external person (e.g. family guest, delivery driver, contractor)
# requesting temporary entry into a property.
#
# Architectural Design Decision:
# Notice that Visitor does not contain valid dates or gate approvals directly.
# The system separates the *person's identity* (the Visitor model) from the *visit pass*
# (the VisitorAuthorization model). This database normalization allows a recurring visitor to
# maintain one profile while having multiple time-bound authorization records over time.
class Visitor(db.Model):
    __tablename__ = 'visitors'

    # Primary key: Unique integer identifying this visitor profile.
    id = db.Column(db.Integer, primary_key=True)

    # Full name of the visiting individual.
    full_name = db.Column(db.String(120), nullable=False)

    # Mobile contact number used for SMS gate codes or verification callbacks.
    phone_number = db.Column(db.String(30), nullable=False)

    # Optional government ID, national ID, or driver's license reference number.
    # Recorded at the gate according to specific property access policies for security verification.
    identity_reference = db.Column(db.String(100), nullable=True)

    # Audit timestamps recording when this visitor profile was created and last modified.
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

