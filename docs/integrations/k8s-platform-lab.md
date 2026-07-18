# k8s-platform-lab Integration

## Purpose

This repository provides the application and CI/CD workflow.

The `k8s-platform-lab` repository provides the Kubernetes platform that consumes this application through GitOps.

## Integration boundary

Project 1: `gitops-cicd-k3s-lab`

- owns Flask application code
- owns Dockerfile
- owns unit tests
- owns GitHub Actions CI/CD
- builds and pushes Docker images
- updates the base Kubernetes image tag
- provides reusable Kustomize overlays

Project 2: `k8s-platform-lab`

- owns the Kubernetes platform
- owns ArgoCD App-of-Apps
- installs ingress, monitoring, storage, and policy components
- consumes this repository through the `k8s/overlays/p2-platform` path
- validates runtime health, alerts, metrics, and dashboard evidence

## p2-platform overlay

The `k8s/overlays/p2-platform` overlay adds platform-specific resources:

- namespace: `apps`
- ingress host: `demo.p2.local`
- ServiceMonitor for Prometheus scraping
- PrometheusRule for application alerting
- platform labels used by Kyverno, Prometheus, and Grafana

## Image tag source of truth

The current image tag is managed in:

- `k8s/base/kustomization.yaml`
- `k8s/base/deployment.yaml` through the `APP_VERSION` environment variable

Do not hard-code the image tag in documentation as the CI/CD workflow may update it.

## Observability

The app exposes Prometheus metrics at:

`/metrics`

Important metrics:

- `gitops_cicd_demo_app_info`
- `gitops_cicd_demo_http_requests_total`
- `gitops_cicd_demo_http_request_duration_seconds`

The HTTP metrics use a `route` label, which is consumed by Project 2 dashboards and alert rules.

## Alerting

The p2-platform overlay defines alert rules for:

- scrape target down
- no ready pods
- high 5xx ratio
- high p95 latency

A temporary fire-drill alert was previously added and removed to validate the alerting pipeline. The temporary rule must not remain in the repository.

## Validation

Render both overlays before committing:

- `k8s/overlays/dev`
- `k8s/overlays/p2-platform`

The p2-platform overlay should render:

- Deployment
- Service
- Ingress
- ServiceMonitor
- PrometheusRule
