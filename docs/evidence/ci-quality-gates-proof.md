# CI Quality Gates Proof

This document records the verified CI quality gates added to the `gitops-cicd-k3s-lab` project.

## Goal

Improve the CI/CD pipeline so that a new container image is only built and pushed after validation succeeds.

## Added Quality Gates

The `ci-gitops` workflow now validates the project before building the image:

- Install Python runtime and development dependencies.
- Run Flask unit tests with `pytest`.
- Compile Python files with `compileall`.
- Render the Kustomize dev overlay.
- Check that the rendered manifest contains a Deployment and Service.
- Upload the rendered manifest as a GitHub Actions artifact.

## Verified Commits

- CI quality gates commit: `3fca754`
- GitOps manifest update commit: `504834d`
- Deployed image tag: `sha-3fca754`

## Runtime Verification

After CI passed, GitHub Actions built and pushed:

- Image: `hoangdonguit/gitops-cicd-demo-app:sha-3fca754`

Then GitHub Actions updated the GitOps manifests:

- `k8s/base/kustomization.yaml`
- `k8s/base/deployment.yaml`

ArgoCD synced the new desired state into K3s.

Expected runtime result:

- ArgoCD Application: `Synced / Healthy`
- Deployment rollout: successful
- `/version`: `sha-3fca754`
- `/healthz`: `ok`

## Why This Matters

The pipeline now has a quality gate before image publication. If tests or manifest rendering fail, the image is not pushed and the GitOps desired state is not updated.
