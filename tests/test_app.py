from app.main import app


def test_healthz_returns_ok():
    client = app.test_client()

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_version_endpoint_returns_app_and_version():
    client = app.test_client()

    response = client.get("/version")
    data = response.get_json()

    assert response.status_code == 200
    assert data["app"] == "gitops-cicd-demo-app"
    assert "version" in data


def test_index_endpoint_contains_required_fields():
    client = app.test_client()

    response = client.get("/")
    data = response.get_json()

    assert response.status_code == 200
    assert data["app"] == "gitops-cicd-demo-app"
    assert "Hello from GitOps CI/CD K3s Lab" in data["message"]
    assert "version" in data
    assert "hostname" in data
    assert "timestamp" in data
