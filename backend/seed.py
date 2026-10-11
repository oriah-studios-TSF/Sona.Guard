# Database Seeding Script
#
# In software development, "seeding" refers to populating an empty database with initial sample
# or default data so developers and testers can run the system immediately.
from app import create_app
from app.extensions import db
from app.models import Property, Entrance, Resident, User

# Create a Flask application instance using our factory function.
app = create_app()

# Establish an Application Context:
# In Flask, extensions like SQLAlchemy require an active application context to know which
# application configuration and database connection to use when running outside of an HTTP request.
with app.app_context():
    # Inspects all registered SQLAlchemy model classes and creates missing tables in the database.
    # Note: If tables already exist, `db.create_all()` does not modify or drop them.
    db.create_all()

    # Idempotent Seeding Pattern:
    # Query for existing records first using unique codes before inserting new rows.
    # This ensures that running this seed script multiple times won't create duplicate records
    # or throw unique constraint database errors.

    # 1. Create one fictional gated estate (Property).
    property = Property.query.filter_by(property_code='SONA-EST-001').first()

    if property is None:
        property = Property(
            name='Sona Gardens',
            property_code='SONA-EST-001',
            address='123 Example Road, Johannesburg',
        )
        db.session.add(property)
        # `db.session.flush()` sends the pending INSERT statement to the database without finalizing
        # the transaction. This forces the database to generate the autoincrementing `property.id`,
        # allowing us to use `property.id` as a foreign key in the child records below.
        db.session.flush()

    # 2. Create the estate's main vehicle entrance (Entrance) linked to the property.
    entrance = Entrance.query.filter_by(entrance_code='SONA-GATE-001').first()

    if entrance is None:
        entrance = Entrance(
            property_id=property.id,
            name='Main Vehicle Gate',
            entrance_code='SONA-GATE-001',
            entrance_type='vehicle',
        )
        db.session.add(entrance)

    # 3. Create one resident (Resident) for access-verification testing.
    resident = Resident.query.filter_by(resident_code='SONA-RES-001').first()

    if resident is None:
        resident = Resident(
            property_id=property.id,
            resident_code='SONA-RES-001',
            unit_number='A-101',
            full_name='Alex Morgan',
            phone_number='0710000000',
            email='alex@example.com',
        )
        db.session.add(resident)

    # 4. Create one initial security officer (User) who can log in.
    user = User.query.filter_by(staff_code='SONA-STAFF-001').first()

    if user is None:
        user = User(
            staff_code='SONA-STAFF-001',
            full_name='Molefe Ramotsepane',
            role='security_officer',
        )
        # Uses the model's secure hashing method to hash the password before storage.
        user.set_password('Ramotsepane.02')
        db.session.add(user)

    # Commit all staged additions as a single atomic database transaction.
    db.session.commit()

    print('Sona.Guard seed completed successfully.')
    print('Estate: Sona Gardens')
    print('Resident code: SONA-RES-001')
    print('Security staff code: SONA-STAFF-001')
    print('Temporary password: ChangeMe123!')