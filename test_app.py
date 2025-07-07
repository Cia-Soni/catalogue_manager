import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testsecret'
    with app.test_client() as client:
        yield client

def login(client):
    return client.post('/', data={
        'username': 'admin',
        'password': 'password'
    }, follow_redirects=True)

def test_login_logout(client):
    rv = login(client)
    assert b'Welcome' in rv.data

    rv = client.get('/logout', follow_redirects=True)
    assert b'Login' in rv.data

def test_get_all_catalogues(client):
    login(client)
    rv = client.get('/catalogues')
    assert rv.status_code == 200
    assert b'data' in rv.data

def test_create_update_delete_catalogue(client):
    login(client)

    # Create
    data = {
        'name': 'TestCat',
        'description': 'TestDesc',
        'effective_from': '2025-01-01',
        'effective_to': '2025-12-31',
        'status': 'active'
    }
    rv = client.post('/catalogues',
                     data=json.dumps(data),
                     content_type='application/json')
    assert rv.status_code == 201
    new_id = rv.get_json()['id']

    # Get by ID
    rv = client.get(f'/catalogues/{new_id}')
    assert rv.status_code == 200
    assert b'TestCat' in rv.data

    # Update
    rv = client.put(f'/catalogues/{new_id}',
                    data=json.dumps({
                        'name': 'UpdatedCat',
                        'description': 'UpdatedDesc',
                        'effective_from': '2025-01-01',
                        'effective_to': '2025-12-31',
                        'status': 'inactive'
                    }),
                    content_type='application/json')
    assert rv.status_code == 200

    # Confirm update
    rv = client.get(f'/catalogues/{new_id}')
    assert b'UpdatedCat' in rv.data

    # Delete
    rv = client.delete(f'/catalogues/{new_id}')
    assert rv.status_code == 200

    # Confirm delete
    rv = client.get(f'/catalogues/{new_id}')
    assert rv.status_code == 404

