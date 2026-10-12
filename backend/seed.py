# Database Seeding Script
#
# Seeds the database with realistic fictional data for testing sona.guard.
# The script is idempotent: existing records are preserved when rerun.

from app import create_app
from app.extensions import db
from app.models import Property, Entrance, Resident, User

app = create_app()

with app.app_context():
    # Create any missing database tables.
    db.create_all()

    # --------------------------------------------------
    # 1. PROPERTIES
    # --------------------------------------------------

    properties_data = [
        {
            "name": "Sona Gardens",
            "property_code": "SONA-EST-001",
            "address": "123 Example Road, Johannesburg",
        },
        {
            "name": "Oakridge Estate",
            "property_code": "SONA-EST-002",
            "address": "45 Cedar Avenue, Centurion",
        },
        {
            "name": "Willow Creek Estate",
            "property_code": "SONA-EST-003",
            "address": "18 Acacia Street, Pretoria",
        },
    ]

    properties = {}

    for data in properties_data:
        property = Property.query.filter_by(
            property_code=data["property_code"]
        ).first()

        if property is None:
            property = Property(**data)
            db.session.add(property)
            db.session.flush()

        properties[data["property_code"]] = property

    # --------------------------------------------------
    # 2. ENTRANCES
    # --------------------------------------------------

    entrances_data = [
        {
            "property_code": "SONA-EST-001",
            "name": "Main Vehicle Gate",
            "entrance_code": "SONA-GATE-001",
            "entrance_type": "vehicle",
        },
        {
            "property_code": "SONA-EST-001",
            "name": "Pedestrian Entrance",
            "entrance_code": "SONA-GATE-002",
            "entrance_type": "pedestrian",
        },
        {
            "property_code": "SONA-EST-002",
            "name": "North Vehicle Gate",
            "entrance_code": "SONA-GATE-003",
            "entrance_type": "vehicle",
        },
        {
            "property_code": "SONA-EST-002",
            "name": "Service Entrance",
            "entrance_code": "SONA-GATE-004",
            "entrance_type": "service",
        },
        {
            "property_code": "SONA-EST-003",
            "name": "Main Entrance",
            "entrance_code": "SONA-GATE-005",
            "entrance_type": "vehicle",
        },
        {
            "property_code": "SONA-EST-003",
            "name": "Pedestrian Gate",
            "entrance_code": "SONA-GATE-006",
            "entrance_type": "pedestrian",
        },
    ]

    for data in entrances_data:
        entrance = Entrance.query.filter_by(
            entrance_code=data["entrance_code"]
        ).first()

        if entrance is None:
            entrance = Entrance(
                property_id=properties[data["property_code"]].id,
                name=data["name"],
                entrance_code=data["entrance_code"],
                entrance_type=data["entrance_type"],
            )
            db.session.add(entrance)

    # --------------------------------------------------
    # 3. RESIDENTS
    # --------------------------------------------------

    residents_data = [
        # Sona Gardens
        ("SONA-EST-001", "SONA-RES-001", "A-101", "Alex Morgan", "0710000000", "alex@example.com"),
        ("SONA-EST-001", "SONA-RES-002", "A-102", "Thabo Nkosi", "0710000001", "thabo@example.com"),
        ("SONA-EST-001", "SONA-RES-003", "A-103", "Naledi Mokoena", "0710000002", "naledi@example.com"),
        ("SONA-EST-001", "SONA-RES-004", "A-104", "Lerato Dlamini", "0710000003", "lerato@example.com"),
        ("SONA-EST-001", "SONA-RES-005", "B-201", "Sipho Ndlovu", "0710000004", "sipho@example.com"),
        ("SONA-EST-001", "SONA-RES-006", "B-202", "Amara Khumalo", "0710000005", "amara@example.com"),
        ("SONA-EST-001", "SONA-RES-007", "B-203", "Daniel Botha", "0710000006", "daniel@example.com"),
        ("SONA-EST-001", "SONA-RES-008", "C-301", "Zanele Sithole", "0710000007", "zanele@example.com"),
        ("SONA-EST-001", "SONA-RES-009", "C-302", "Kagiso Molefe", "0710000008", "kagiso@example.com"),
        ("SONA-EST-001", "SONA-RES-010", "C-303", "Ayesha Patel", "0710000009", "ayesha@example.com"),

        # Oakridge Estate
        ("SONA-EST-002", "SONA-RES-011", "A-101", "Mpho Ramokgopa", "0710000010", "mpho@example.com"),
        ("SONA-EST-002", "SONA-RES-012", "A-102", "Keitumetse Seabi", "0710000011", "keitumetse@example.com"),
        ("SONA-EST-002", "SONA-RES-013", "A-201", "Pieter van der Merwe", "0710000012", "pieter@example.com"),
        ("SONA-EST-002", "SONA-RES-014", "B-101", "Boitumelo Radebe", "0710000013", "boitumelo@example.com"),
        ("SONA-EST-002", "SONA-RES-015", "B-202", "Refilwe Modise", "0710000014", "refilwe@example.com"),
        ("SONA-EST-002", "SONA-RES-016", "C-101", "Karabo Maseko", "0710000015", "karabo@example.com"),

        # Willow Creek Estate
        ("SONA-EST-003", "SONA-RES-017", "A-101", "Tshepo Seakamela", "0710000016", "tshepo@example.com"),
        ("SONA-EST-003", "SONA-RES-018", "A-102", "Michelle Jacobs", "0710000017", "michelle@example.com"),
        ("SONA-EST-003", "SONA-RES-019", "B-201", "Refentse Mahlangu", "0710000018", "refentse@example.com"),
        ("SONA-EST-003", "SONA-RES-020", "C-301", "Lungelo Zulu", "0710000019", "lungelo@example.com"),
    ]

    for property_code, resident_code, unit_number, full_name, phone_number, email in residents_data:
        resident = Resident.query.filter_by(
            resident_code=resident_code
        ).first()

        if resident is None:
            resident = Resident(
                property_id=properties[property_code].id,
                resident_code=resident_code,
                unit_number=unit_number,
                full_name=full_name,
                phone_number=phone_number,
                email=email,
            )
            db.session.add(resident)

    # --------------------------------------------------
    # 4. SECURITY USERS
    # --------------------------------------------------

    users_data = [
        {
            "staff_code": "SONA-STAFF-001",
            "full_name": "Molefe Ramotsepane",
            "role": "security_officer",
            "password": "Ramotsepane.02",
        },
        {
            "staff_code": "SONA-STAFF-002",
            "full_name": "Thabo Mokoena",
            "role": "security_officer",
            "password": "TestOfficer.2026",
        },
        {
            "staff_code": "SONA-STAFF-003",
            "full_name": "Lerato Nkosi",
            "role": "security_officer",
            "password": "TestOfficer.2026",
        },
        {
            "staff_code": "SONA-STAFF-004",
            "full_name": "Sipho Dlamini",
            "role": "security_officer",
            "password": "TestOfficer.2026",
        },
        {
            "staff_code": "SONA-STAFF-005",
            "full_name": "Naledi Khumalo",
            "role": "security_supervisor",
            "password": "TestSupervisor.2026",
        },
        {
            "staff_code": "SONA-STAFF-006",
            "full_name": "Daniel Botha",
            "role": "security_officer",
            "password": "TestOfficer.2026",
        },
    ]

    for data in users_data:
        user = User.query.filter_by(
            staff_code=data["staff_code"]
        ).first()

        if user is None:
            user = User(
                staff_code=data["staff_code"],
                full_name=data["full_name"],
                role=data["role"],
            )
            user.set_password(data["password"])
            db.session.add(user)

    # --------------------------------------------------
    # 5. SAVE ALL RECORDS
    # --------------------------------------------------

    try:
        db.session.commit()
        print("Database seeding completed successfully.")
        print(f"Properties: {len(properties_data)}")
        print(f"Entrances: {len(entrances_data)}")
        print(f"Residents: {len(residents_data)}")
        print(f"Security users: {len(users_data)}")
    except Exception:
        db.session.rollback()
        raise
