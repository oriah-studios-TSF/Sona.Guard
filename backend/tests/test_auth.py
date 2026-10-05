from app.models import AuditLog

def test_dashboard_requires_auth(client):
    response = client.get('/dashboard/')
    assert response.status_code == 302
    
    assert '/?next=' in response.headers['Location']
    
def test_valid_login(client, admin_user):
    response = client.post('/auth/login', json={
        'employee_id': 'TEST001',
        'password': 'password'
    })

    assert response.status_code == 200
    assert response.json['success'] is True

def test_invalid_login(client, admin_user):
    response = client.post('/auth/login', json={
        'employee_id': 'TEST001',
        'password': 'WrongPassword123!'
    })

    assert response.status_code == 401
    assert response.json['success'] is False
    assert response.json['message'] == 'Invalid credentials. Make sure your employee ID and password are correct.'

def test_blocked_user_cannot_login(client, blocked_user):
    response = client.post('/auth/login', json={
        'employee_id': 'TEST003',
        'password': 'password'
    })

    assert response.status_code == 403
    assert response.json['success'] is False
    assert response.json['message'] == 'This account has been blocked. Please contact your system administrator.'

def test_logout(client, admin_user):
    login_response = client.post('/auth/login', json={
        'employee_id': 'TEST001',
        'password': 'password'
    })

    assert login_response.status_code == 200

    logout_response = client.post('/auth/logout')

    assert logout_response.status_code == 200
    assert logout_response.json['success'] is True

    dashboard_response = client.get('/dashboard/')

    assert dashboard_response.status_code == 302
    
def test_security_officer_cannot_access_admin_route(client, security_officer):
    with client.session_transaction() as session:
        session['_user_id'] = str(security_officer.id)
        session['_fresh'] = True

    response = client.get('/dashboard/admin-test')

    assert response.status_code == 403

def test_admin_can_access_admin_route(client, admin_user):
    with client.session_transaction() as session:
        session['_user_id'] = str(admin_user.id)
        session['_fresh'] = True

    response = client.get('/dashboard/admin-test')

    assert response.status_code == 200
    assert response.data == b'Admin authorization successful'

def test_login_rate_limit(client, admin_user):
    for _ in range(5):
        response = client.post('/auth/login', json={
            'employee_id': 'TEST001',
            'password': 'WrongPassword123!'
        })

        assert response.status_code == 401

    response = client.post('/auth/login', json={
        'employee_id': 'TEST001',
        'password': 'WrongPassword123!'
    })

    assert response.status_code == 429
    assert response.json['success'] is False
    assert response.json['message'] == 'Too many login attempts. Please wait a moment before trying again.'

def test_successful_login_creates_audit_log(client, admin_user):
    response = client.post('/auth/login', json={
        'employee_id': 'TEST001',
        'password': 'password'
    })

    assert response.status_code == 200

    audit_log = AuditLog.query.filter_by(
        event_type='LOGIN_SUCCESS',
        user_id=admin_user.id
    ).first()

    assert audit_log is not None
    assert audit_log.description == 'User logged in successfully.'

def test_invalid_login_creates_audit_log(client, admin_user):
    response = client.post('/auth/login', json={
        'employee_id': 'TEST001',
        'password': 'WrongPassword123!'
    })

    assert response.status_code == 401

    audit_log = AuditLog.query.filter_by(
        event_type='LOGIN_FAILURE',
        user_id=admin_user.id
    ).first()

    assert audit_log is not None
    assert audit_log.description == 'Invalid credentials supplied.'

def test_blocked_login_creates_audit_log(client, blocked_user):
    response = client.post('/auth/login', json={
        'employee_id': 'TEST003',
        'password': 'password'
    })

    assert response.status_code == 403

    audit_log = AuditLog.query.filter_by(
        event_type='LOGIN_BLOCKED',
        user_id=blocked_user.id
    ).first()

    assert audit_log is not None
    assert audit_log.description == 'Blocked account attempted to login.'

def test_logout_creates_audit_log(client, admin_user):
    login_response = client.post('/auth/login', json={
        'employee_id': 'TEST001',
        'password': 'password'
    })

    assert login_response.status_code == 200

    logout_response = client.post('/auth/logout')

    assert logout_response.status_code == 200

    audit_log = AuditLog.query.filter_by(
        event_type='LOGOUT_SUCCESS',
        user_id=admin_user.id
    ).first()

    assert audit_log is not None
    assert audit_log.description == 'User logged out successfully.'