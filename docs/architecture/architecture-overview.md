# Architecture Overview

This document explains the architecture of the `gitops-cicd-k3s-lab` portfolio project.

## Goal

The goal is to demonstrate an end-to-end CI/CD and GitOps workflow for a small containerized Flask application running on a K3s cluster.

## High-Level Flow

1. Developer pushes code to the `main` branch.
2. GitHub Actions builds a Docker image.
3. The image is pushed to Docker Hub with an immutable commit SHA tag.
4. GitHub Actions updates the Kubernetes manifest image tag in Git.
5. ArgoCD detects the Git change and syncs the desired state to K3s.
6. The application pod is rolled out with the new image version.

## Components

| Component | Role |
|---|---|
| Flask app | Minimal demo API used to verify deployment version and health |
| Docker | Builds the application container image |
| Docker Hub | Stores immutable application images |
| GitHub Actions | CI/CD engine for build, push, and manifest update |
| Kustomize | Manages Kubernetes manifests and image tag updates |
| ArgoCD | GitOps controller that syncs Git state into K3s |
| K3s | Kubernetes runtime target |

## GitOps Boundary

GitHub Actions does not run `kubectl apply` against the application workload.

GitHub Actions only performs CI/CD tasks:

- build image
- push image
- update Git manifests
- commit the desired state back to Git

ArgoCD performs the deployment:

- reads the Git repository
- renders `k8s/overlays/dev`
- applies the desired state into the `gitops-cicd-demo` namespace
- maintains sync and self-healing

## ArgoCD Isolation

This portfolio app reuses an existing ArgoCD instance but is isolated from other projects by:

- AppProject: `portfolio-lab`
- Application: `portfolio-gitops-cicd-demo`
- Namespace: `gitops-cicd-demo`
- Repository: `hoangdonguit/gitops-cicd-k3s-lab`

This avoids conflicts with other ArgoCD applications running in the same K3s cluster.

## Current Verified Deployment

- Verified image tag: `sha-be95c88`
- ArgoCD status: `Synced / Healthy`
- Kubernetes deployment: `gitops-cicd-demo-app`
- Namespace: `gitops-cicd-demo`
- Runtime verification endpoint: `/version`

## Security Notes

- Docker Hub credentials are stored in GitHub Secrets.
- No secret or token is committed to the repository.
- Image tags use commit SHA instead of `latest`.
- The application is exposed internally as a `ClusterIP` service for the current lab stage.

