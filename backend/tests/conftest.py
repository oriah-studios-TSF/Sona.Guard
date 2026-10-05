import pytest

from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
    })

    with app.app_context():
        db.create_all()

        yield app
    
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(app):
    user = User(
        employee_id='TEST001',
        full_name='Test Admin',
        role='admin',
        is_active=True,
    )

    user.set_password('password')

    db.session.add(user)
    db.session.commit()

    return user

@pytest.fixture
def security_officer(app):
    user = User(
        employee_id='TEST002',
        full_name='Test Security Officer',
        role='security_officer',
        is_active=True,
    )

    user.set_password('password')

    db.session.add(user)
    db.session.commit()

    return user

@pytest.fixture
def blocked_user(app):
    user = User(
        employee_id='TEST003',
        full_name='Test Blocked',
        role='security_officer',
        is_active=False,
    )

    user.set_password('password')

    db.session.add(user)
    db.session.commit()

    return user

    
