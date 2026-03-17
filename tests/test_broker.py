from fastapi.testclient import TestClient

from yourdesk.broker import create_app
from yourdesk.config import BrokerConfig


def test_session_lifecycle() -> None:
    app = create_app(BrokerConfig(token_ttl_seconds=60))
    client = TestClient(app)

    created = client.post(
        "/api/v1/sessions",
        json={"alias": "host-a", "viewer_url": "http://example.com/vnc.html"},
    )
    assert created.status_code == 200
    payload = created.json()
    code = payload["code"]
    secret = payload["secret"]

    lookup = client.get(f"/api/v1/sessions/{code}")
    assert lookup.status_code == 200
    assert lookup.json()["alias"] == "host-a"

    revoked = client.delete(f"/api/v1/sessions/{code}", params={"secret": secret})
    assert revoked.status_code == 200

    missing = client.get(f"/api/v1/sessions/{code}")
    assert missing.status_code == 404
