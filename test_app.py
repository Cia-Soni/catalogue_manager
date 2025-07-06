from app import app

def test_get_catalogues():
    client = app.test_client()
    response = client.get('/catalogues')
    assert response.status_code == 200

def test_create_catalogue():
    client = app.test_client()
    payload = {
        "name": "New Cat",
        "description": "Test Desc",
        "effective_from": "2025-07-04",
        "effective_to": "2025-12-31",
        "status": "active"
    }
    response = client.post('/catalogues', json=payload)
    assert response.status_code == 201

def test_get_catalogue_by_id():
    client = app.test_client()
    response = client.get('/catalogues/1')
    assert response.status_code == 200

def test_update_catalogue():
    client = app.test_client()
    payload = {"name": "Updated Name"}
    response = client.put('/catalogues/1', json=payload)
    assert response.status_code == 200

def test_delete_catalogue():
    client = app.test_client()
    response = client.delete('/catalogues/1')
    assert response.status_code == 200
