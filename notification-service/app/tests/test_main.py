import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from main import app

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
