from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
from app.services.security import hash_password

def auth_header(app):
    with app.app_context():
        u = User(email='u@x.com', password_hash=hash_password('p'))
        db.session.add(u); db.session.commit()
        tok = create_access_token(identity=u.id, additional_claims={'role':'student'})
        return {'Authorization': f'Bearer {tok}'}

def test_create_and_list_tasks(client, app):
    h = auth_header(app)
    r = client.post('/api/v1/tasks/', headers=h, json={'title':'Test Task'})
    assert r.status_code == 201
    r = client.get('/api/v1/tasks/', headers=h)
    assert r.status_code == 200
    assert len(r.get_json()) == 1
