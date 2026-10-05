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