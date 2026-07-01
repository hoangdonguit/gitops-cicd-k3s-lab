import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "gitops-cicd-demo-app")
APP_VERSION = os.getenv("APP_VERSION", "dev-local")


@app.get("/")
def index():
    return jsonify(
        {
            "message": "Hello from GitOps CI/CD K3s Lab",
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
