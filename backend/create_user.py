# Administrative User Provisioning Script
#
# A standalone command-line script to manually create and persist an initial administrative user.
from app import create_app
from app.extensions import db
from app.models import User

# Initialize the Flask application instance to load configuration and database bindings.
app = create_app()

# Push the application context so that SQLAlchemy operations know which database to target.
with app.app_context():
    # Instantiate a new User object representing an administrator.
    user = User(
        employee_id='SG001',
        full_name='System Administrator',
        role='admin',
    )

    # Hash the plaintext password before writing to the database.
    user.set_password('Ramotsepane.02')

    # Add the user to the session and commit the transaction.
    db.session.add(user)
    db.session.commit()

    print('User created successfully')