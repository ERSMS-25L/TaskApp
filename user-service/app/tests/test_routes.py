import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

os.environ['DATABASE_URL'] = 'sqlite:///./test_user.db'

from database import engine, get_db
from models import Base
from main import app

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_and_list_user():
    resp = client.post('/api/users/', params={'username': 'john', 'email': 'john@example.com', 'password': 'pass'})
    assert resp.status_code == 200
    user_id = resp.json()['user_id']
    resp = client.get('/api/users/')
    assert resp.status_code == 200
    assert any(u['id'] == user_id for u in resp.json())
