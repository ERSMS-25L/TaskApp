import sys
import os
import importlib.util
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

# Load modules from this service explicitly to avoid name collisions
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
spec_main = importlib.util.spec_from_file_location("notif_main", os.path.join(BASE_DIR, "main.py"))
notif_main = importlib.util.module_from_spec(spec_main)
spec_main.loader.exec_module(notif_main)

app = notif_main.app

@pytest.mark.asyncio
async def test_send_notification():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post('/send-notification', json={'message': 'hi', 'recipient': 'a@b.c', 'notification_type': 'email'})
            assert resp.status_code == 200
            assert resp.json()['message'] == 'hi'

@pytest.mark.asyncio
async def test_health():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get('/api/health')
            assert resp.status_code == 200
