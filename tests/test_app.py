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


def test_metrics_endpoint_exposes_prometheus_metrics():
    client = app.test_client()

    client.get("/healthz")
    response = client.get("/metrics")
    body = response.data.decode("utf-8")

    assert response.status_code == 200
    assert response.content_type.startswith("text/plain")
    assert "gitops_cicd_demo_app_info" in body
    assert "gitops_cicd_demo_http_requests_total" in body
    assert "gitops_cicd_demo_http_request_duration_seconds" in body
