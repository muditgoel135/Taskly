def test_register_and_login(client):
    r = client.post('/api/v1/auth/register', json={'email':'a@b.com','password':'x'})
    assert r.status_code == 201
    r = client.post('/api/v1/auth/login', json={'email':'a@b.com','password':'x'})
    assert r.status_code == 200
    assert 'access' in r.get_json()
