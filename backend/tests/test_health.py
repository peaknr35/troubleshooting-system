def test_health_get(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_health_head(client):
    r = client.head("/health")
    assert r.status_code == 200


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "health" in r.json()


def test_providers_catalog(client):
    r = client.get("/providers")
    assert r.status_code == 200
    ids = {p["id"] for p in r.json()["providers"]}
    assert ids == {"openai", "anthropic", "kimi"}
    for p in r.json()["providers"]:
        assert p["default_model"]
        assert isinstance(p["models"], list) and p["models"]
