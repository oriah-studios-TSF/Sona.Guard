from datetime import datetime, timezone

from app.extensions import db


# The Property model represents a physical residential estate, commercial complex, or gated facility.
# In the Sona.Guard domain, properties serve as the top-level container for both access points
# (Entrances) and authorized inhabitants (Residents).
class Property(db.Model):
    __tablename__ = 'properties'

    # Primary key: Unique identifier for each property record.
    id = db.Column(db.Integer, primary_key=True)

    # Human-readable name of the facility (e.g. 'Sona Gardens').
    name = db.Column(db.String(150), nullable=False)

    # Unique external identifier used for estate-level referencing (e.g. 'SONA-EST-001').
    property_code = db.Column(db.String(50), unique=True, nullable=False)

    # Physical street address of the property.
    address = db.Column(db.String(255), nullable=True)

    # Operational status: When set to False, access verification across the entire property
    # is denied, allowing security administrators to lock down or suspend an estate facility.
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Audit timestamps recording when the property was created and last updated.
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

    # DATABASE RELATIONSHIPS:
    # -----------------------
    # 1. One-to-Many relationship: One Property -> Many Entrances.
    # Connects this Property to all physical gate checkpoints located on its perimeter.
    # - `backref='property'`: Automatically attaches a `.property` attribute to child Entrance objects,
    #   allowing navigation from an entrance directly to its owning property without manual queries.
    # - `lazy=True`: "Lazy loading" means child entrances are only queried from the database when
    #   the `property.entrances` attribute is explicitly accessed in Python code, avoiding unnecessary SQL joins.
    entrances = db.relationship('Entrance', backref='property', lazy=True)

    # 2. One-to-Many relationship: One Property -> Many Residents.
    # Connects this Property to all resident profiles registered at this estate.
    # - `backref='property'`: Gives each Resident object a direct `.property` reference.
    # - Why it matters: Crucial for multi-tenant isolation, ensuring security guards at Gate A of Estate 1
    #   cannot mistakenly verify or grant entry to a resident from Estate 2.
    residents = db.relationship('Resident', backref='property', lazy=True)



    