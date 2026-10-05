from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    user = User(
        employee_id='SG002',
        full_name='Security Officer',
        role='security_officer'
    )

    user.set_password('Officer123!')

    db.session.add(user)
    db.session.commit()

    print('User created successfully')