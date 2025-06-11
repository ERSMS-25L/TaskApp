import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ['DATABASE_URL'] = 'sqlite:///./test_task.db'

from database import Base, engine, get_db
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

def test_create_and_read_task():
    resp = client.post('/api/tasks/', json={'title': 'test', 'description': 'desc', 'user_id': 1})
    assert resp.status_code == 200
    task_id = resp.json()['id']

    resp = client.get(f'/api/tasks/{task_id}')
    assert resp.status_code == 200
    assert resp.json()['title'] == 'test'
