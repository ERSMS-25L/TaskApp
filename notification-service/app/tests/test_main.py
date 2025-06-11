from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_send_notification():
    resp = client.post('/send-notification', json={'message': 'hi', 'recipient': 'a@b.c', 'notification_type': 'email'})
    assert resp.status_code == 200
    assert resp.json()['message'] == 'hi'

def test_health():
    resp = client.get('/api/health')
    assert resp.status_code == 200
