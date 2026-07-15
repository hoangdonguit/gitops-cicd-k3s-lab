import os
import socket
import time
from datetime import datetime, timezone

from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "gitops-cicd-demo-app")
APP_VERSION = os.getenv("APP_VERSION", "dev-local")

APP_INFO = Gauge(
    "gitops_cicd_demo_app_info",
    "Application build information",
    ["app", "version"],
)
APP_INFO.labels(app=APP_NAME, version=APP_VERSION).set(1)

HTTP_REQUESTS_TOTAL = Counter(
    "gitops_cicd_demo_http_requests_total",
    "Total HTTP requests handled by the application",
    ["method", "route", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "gitops_cicd_demo_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route"],
)


@app.before_request
def start_request_timer():
    g.request_start_time = time.perf_counter()


@app.after_request
def record_request_metrics(response):
    route = request.endpoint or "unknown"

    if route != "metrics":
        duration = time.perf_counter() - getattr(
            g,
            "request_start_time",
            time.perf_counter(),
        )

        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            route=route,
            status=str(response.status_code),
        ).inc()

        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            route=route,
        ).observe(duration)

    return response


@app.get("/")
def index():
    return jsonify(
        {
            "message": "Hello from GitOps CI/CD K3s Lab - deployed by ArgoCD",
            "app": APP_NAME,
            "version": APP_VERSION,
            "hostname": socket.gethostname(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


@app.get("/version")
def version():
    return jsonify(
        {
            "app": APP_NAME,
            "version": APP_VERSION,
        }
    )


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)
