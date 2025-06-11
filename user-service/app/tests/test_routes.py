import os
import tempfile
import pytest
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

db_fd, db_path = tempfile.mkstemp(prefix="test_user", suffix=".db")
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'

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

@pytest.fixture(autouse=True, scope="module")
def cleanup():
    yield
    os.close(db_fd)
    os.unlink(db_path)

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_and_list_user():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post('/api/users/', params={'username': 'john', 'email': 'john@example.com', 'password': 'pass'})
            assert resp.status_code == 200
            user_id = resp.json()['user_id']
            resp = await client.get('/api/users/')
            assert resp.status_code == 200
            assert any(u['id'] == user_id for u in resp.json())
