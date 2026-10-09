from app import create_app
from app.extensions import db
from app.models import User, Person, Entrance, Permission

from datetime import datetime, timezone, tzinfo


app = create_app()


with app.app_context():
    print('Seeding sona.guard development database...')

    users = [
        {
            'employee_id': 'SG002',
            'full_name': 'Michael Dlamini',
            'password': 'Security123!',
            'role': 'security_officer',
        },
    ]

    for user_data in users:
        existing_user = User.query.filter_by(
            employee_id=user_data['employee_id']
        ).first()

        if existing_user:
            continue

        user = User(
            employee_id=user_data['employee_id'],
            full_name=user_data['full_name'],
            role=user_data['role'],
            is_active=True
        )

        user.set_password(user_data['password'])

        db.session.add(user)

    db.session.commit()

    
    people = [
        {
            'employee_id': 'EMP001',
            'full_name': 'Thabo Mokoena',
            'email': 'thabo.mokoena@orion.example',
            'phone_number': '+27 71 000 1001',
            'nationality': 'South African',
            'department': 'Security Operations',
            'job_title': 'Security Officer',
            'workplace': 'Main Building',
            'credential_expires_at': datetime(2027, 12, 31, tzinfo=timezone.utc),
            'is_active': True
        },
        {
            'employee_id': 'EMP002',
            'full_name': 'Sarah Nkosi',
            'email': 'sarah.nkosi@orion.example',
            'phone_number': '+27 71 000 1002',
            'nationality': 'South African',
            'department': 'Human Resources',
            'job_title': 'HR Coordinator',
            'workplace': 'Main Building',
            'credential_expires_at': datetime(2027, 6, 30, tzinfo=timezone.utc),
            'is_active': True
        },
        {
            'employee_id': 'EMP003',
            'full_name': 'Daniel Naidoo',
            'email': 'daniel.naidoo@orion.example',
            'phone_number': '+27 71 000 1003',
            'nationality': 'South African',
            'department': 'IT',
            'job_title': 'Systems Administrator',
            'workplace': 'Technology Building',
            'credential_expires_at': datetime(2028, 3, 31, tzinfo=timezone.utc),
            'is_active': True
        },
        {
            'employee_id': 'EMP004',
            'full_name': 'Lerato Molefe',
            'email': 'lerato.molefe@orion.example',
            'phone_number': '+27 71 000 1004',
            'nationality': 'South African',
            'department': 'Finance',
            'job_title': 'Accounts Officer',
            'workplace': 'Main Building',
            'credential_expires_at': datetime(2027, 9, 30, tzinfo=timezone.utc),
            'is_active': True
        },
        {
            'employee_id': 'EMP005',
            'full_name': 'Kabelo Dlamini',
            'email': 'kabelo.dlamini@orion.example',
            'phone_number': '+27 71 000 1005',
            'nationality': 'South African',
            'department': 'Warehouse Operations',
            'job_title': 'Warehouse Supervisor',
            'workplace': 'Warehouse',
            'credential_expires_at': datetime(2027, 2, 28, tzinfo=timezone.utc),
            'is_active': True
        },
        {
            'employee_id': 'EMP006',
            'full_name': 'Michael Jacobs',
            'email': 'michael.jacobs@orion.example',
            'phone_number': '+27 71 000 1006',
            'nationality': 'South African',
            'department': 'Facilities',
            'job_title': 'Facilities Technician',
            'workplace': 'Operations Building',
            'credential_expires_at': datetime(2026, 12, 31, tzinfo=timezone.utc),
            'is_active': True
        },
        {
            'employee_id': 'EMP007',
            'full_name': 'Nomsa Khumalo',
            'email': 'nomsa.khumalo@orion.example',
            'phone_number': '+27 71 000 1007',
            'nationality': 'South African',
            'department': 'Security Operations',
            'job_title': 'Security Officer',
            'workplace': 'Warehouse',
            'credential_expires_at': datetime(2026, 8, 31, tzinfo=timezone.utc),
            'is_active': False
        }
    ]


    for person_data in people:
        person = Person.query.filter_by(
            employee_id=person_data['employee_id']
        ).first()
    
        if person:
            # Update the existing employee's profile.
            person.full_name = person_data['full_name']
            person.email = person_data['email']
            person.phone_number = person_data['phone_number']
            person.nationality = person_data['nationality']
            person.department = person_data['department']
            person.job_title = person_data['job_title']
            person.workplace = person_data['workplace']
            person.credential_expires_at = person_data['credential_expires_at']
            person.is_active = person_data['is_active']
    
        else:
            # Create the employee if they don't already exist.
            person = Person(
                employee_id=person_data['employee_id'],
                full_name=person_data['full_name'],
                email=person_data['email'],
                phone_number=person_data['phone_number'],
                nationality=person_data['nationality'],
                department=person_data['department'],
                job_title=person_data['job_title'],
                workplace=person_data['workplace'],
                credential_expires_at=person_data['credential_expires_at'],
                is_active=person_data['is_active']
            )
    
            db.session.add(person)
    
    db.session.commit()
    print('Employee profiles updated successfully.')   

    entrances = [
        {
            'name': 'Main Entrance',
            'entrance_code': 'ENT-M01',
            'entrance_type': 'door',
            'is_active': True
        },
        {
            'name': 'Staff Entrance',
            'entrance_code': 'ENT-S01',
            'entrance_type': 'door',
            'is_active': True
        },
        {
            'name': 'Warehouse Entrance',
            'entrance_code': 'ENT-W01',
            'entrance_type': 'door',
            'is_active': True
        },
        {
            'name': 'Parking Entrance',
            'entrance_code': 'ENT-P01',
            'entrance_type': 'gate',
            'is_active': True
        },
        {
            'name': 'Restricted Server Room',
            'entrance_code': 'ENT-R01',
            'entrance_type': 'door',
            'is_active': True
        },
        {
            'name': 'Warehouse Loading Gate',
            'entrance_code': 'ENT-G02',
            'entrance_type': 'gate',
            'is_active': False
        }
    ]

    for entrance_data in entrances:
        existing_entrance = Entrance.query.filter_by(
            entrance_code=entrance_data['entrance_code']
        ).first()

        if existing_entrance:
            continue

        entrance = Entrance(
            name=entrance_data['name'],
            entrance_code=entrance_data['entrance_code'],
            entrance_type=entrance_data['entrance_type'],
            is_active=entrance_data['is_active']
        )

        db.session.add(entrance)

    db.session.commit()

    admin_user = User.query.filter_by(
        employee_id='SG001'
    ).first()

    permission_data = [
        {
            'person_employee_id': 'EMP001',
            'entrance_code': 'ENT-M01'
        },
        {
            'person_employee_id': 'EMP001',
            'entrance_code': 'ENT-S01'
        },
        {
            'person_employee_id': 'EMP001',
            'entrance_code': 'ENT-W01'
        },
        {
            'person_employee_id': 'EMP002',
            'entrance_code': 'ENT-M01'
        },
        {
            'person_employee_id': 'EMP002',
            'entrance_code': 'ENT-S01'
        },
        {
            'person_employee_id': 'EMP003',
            'entrance_code': 'ENT-M01'
        },
        {
            'person_employee_id': 'EMP003',
            'entrance_code': 'ENT-S01'
        },
        {
            'person_employee_id': 'EMP003',
            'entrance_code': 'ENT-R01'
        },
        {
            'person_employee_id': 'EMP004',
            'entrance_code': 'ENT-M01'
        },
        {
            'person_employee_id': 'EMP005',
            'entrance_code': 'ENT-M01'
        },
        {
            'person_employee_id': 'EMP005',
            'entrance_code': 'ENT-W01'
        },
        {
            'person_employee_id': 'EMP005',
            'entrance_code': 'ENT-G02'
        },
        {
            'person_employee_id': 'EMP006',
            'entrance_code': 'ENT-M01'
        },
        {
            'person_employee_id': 'EMP007',
            'entrance_code': 'ENT-M01'
        }
    ]

    for permission_data_item in permission_data:
        person = Person.query.filter_by(
            employee_id=permission_data_item['person_employee_id']
        ).first()

        entrance = Entrance.query.filter_by(
            entrance_code=permission_data_item['entrance_code']
        ).first()

        if not person or not entrance or not admin_user:
            continue

        existing_permission = Permission.query.filter_by(
            person_id=person.id,
            entrance_id=entrance.id
        ).first()

        if existing_permission:
            continue

        permission = Permission(
            person_id=person.id,
            entrance_id=entrance.id,
            created_by_user_id=admin_user.id,
            is_active=True
        )

        db.session.add(permission)

    db.session.commit()