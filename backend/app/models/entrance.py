from datetime import datetime, timezone

from app.extensions import db


# The Entrance model represents a physical access checkpoint, boom gate, turnstile, or door
# located on a property's perimeter where access checks occur.
class Entrance(db.Model):
    __tablename__ = 'entrances'

    # Primary key: Unique integer identifying this entrance record.
    id = db.Column(db.Integer, primary_key=True)
    
    # Friendly descriptive name for guards and admins (e.g. 'Main Vehicle Gate', 'East Pedestrian Gate').
    name = db.Column(db.String(120), nullable=False)

    # FOREIGN KEY:
    # `db.ForeignKey('properties.id')` establishes a database-level link to the `properties` table.
    # Referential integrity rule: An entrance cannot exist without a valid parent property.
    # In access control, this ensures that every checkpoint is strictly associated with a specific estate.
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    
    # Unique identifier used by gate scanners, guard devices, or terminal kiosks (e.g. 'SONA-GATE-001').
    entrance_code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Classification of gate traffic: Examples include 'vehicle', 'pedestrian', 'visitor', or 'service'.
    entrance_type = db.Column(db.String(50), nullable=False, default='vehicle')

    # Operational status: When False, the gate is marked inactive (e.g. closed for maintenance or locked overnight).
    # The access verification service checks this flag and automatically denies entry if the gate is inactive.
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Timestamps tracking when this checkpoint was added and last modified.
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_by = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))