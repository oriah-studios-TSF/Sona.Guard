from datetime import datetime, timezone

from app.extensions import db


# A unit represesnt an individual house, aprtment, or townhouse
# inside an estate 
class Unit(db.Model):
    __tablename__ = 'units'

    # Unique identifier for the unit
    id = db.Column(db.Integer, primary_key=True)

    # The property the unit belongs to
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)

    # The unit's identifier within its estate, e.g. A-101.
    unit_number = db.Column(db.String(50), nullable=False)

    # The unit type, e.g. apartment, house, townhouse, etc.
    unit_type = db.Column(db.String(50), nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # The date and time the unit was created
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
        )

    # The date and time the unit was last updated
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # A unit number must be unique within its property
    # but different properties can have the same unit number
    __table_args__ = (
        db.UniqueConstraint('property_id', 'unit_number', name='uq_units_property_unit_number'),
    )

    # The unit's residents
    residents = db.relationship('Resident', back_populates='unit', lazy=True)

    # The property the unit belongs to 
    property = db.relationship('Property', backref='units')


   