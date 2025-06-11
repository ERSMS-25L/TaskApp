import os
import sys
import tempfile
import importlib.util
import pytest
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

# Load modules from this service explicitly to avoid name collisions
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
db_fd, db_path = tempfile.mkstemp(prefix="test_user", suffix=".db")
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
spec_db = importlib.util.spec_from_file_location("user_database", os.path.join(BASE_DIR, "database.py"))
user_database = importlib.util.module_from_spec(spec_db)
spec_db.loader.exec_module(user_database)
sys.modules['database'] = user_database

spec_models = importlib.util.spec_from_file_location("user_models", os.path.join(BASE_DIR, "models.py"))
user_models = importlib.util.module_from_spec(spec_models)
spec_models.loader.exec_module(user_models)
sys.modules['models'] = user_models

spec_routes = importlib.util.spec_from_file_location("user_routes", os.path.join(BASE_DIR, "routes.py"))
user_routes = importlib.util.module_from_spec(spec_routes)
spec_routes.loader.exec_module(user_routes)
sys.modules['routes'] = user_routes

spec_main = importlib.util.spec_from_file_location("user_main", os.path.join(BASE_DIR, "main.py"))
user_main = importlib.util.module_from_spec(spec_main)
spec_main.loader.exec_module(user_main)

engine = user_database.engine
get_db = user_database.get_db
Base = user_models.Base
app = user_main.app

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
