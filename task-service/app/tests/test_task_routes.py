import os
import sys
import importlib.util
import pytest
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

# Load modules from this service explicitly to avoid name collisions
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
os.environ['DATABASE_URL'] = 'sqlite:///./test_task.db'
spec_db = importlib.util.spec_from_file_location("task_database", os.path.join(BASE_DIR, "database.py"))
task_database = importlib.util.module_from_spec(spec_db)
spec_db.loader.exec_module(task_database)
sys.modules['database'] = task_database
spec_models = importlib.util.spec_from_file_location("task_models", os.path.join(BASE_DIR, "models.py"))
task_models = importlib.util.module_from_spec(spec_models)
spec_models.loader.exec_module(task_models)
sys.modules['models'] = task_models
spec_routes = importlib.util.spec_from_file_location("task_routes", os.path.join(BASE_DIR, "routes.py"))
task_routes = importlib.util.module_from_spec(spec_routes)
spec_routes.loader.exec_module(task_routes)
sys.modules['routes'] = task_routes

spec_main = importlib.util.spec_from_file_location("task_main", os.path.join(BASE_DIR, "main.py"))
task_main = importlib.util.module_from_spec(spec_main)
spec_main.loader.exec_module(task_main)

Base = task_database.Base
engine = task_database.engine
get_db = task_database.get_db
app = task_main.app

Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_and_read_task():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post('/api/tasks/', json={'title': 'test', 'description': 'desc', 'user_id': 1})
            assert resp.status_code == 200
            task_id = resp.json()['id']

            resp = await client.get(f'/api/tasks/{task_id}')
            assert resp.status_code == 200
            assert resp.json()['title'] == 'test'
