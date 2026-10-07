from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    user = User(
        employee_id='SG001',
        full_name='System Administrator',
        role='admin',
    )

    user.set_password('Ramotsepane.02')

    db.session.add(user)
    db.session.commit()

    print('User created successfully')