# Final Project Summary

## Project Name

`gitops-cicd-k3s-lab`

## Project Type

DevOps / Cloud-Native / GitOps portfolio lab.

## Goal

Build and verify an end-to-end CI/CD and GitOps workflow for a containerized Flask application deployed to a K3s cluster using GitHub Actions, Docker Hub, Kustomize, and ArgoCD.

## Final Architecture

Developer pushes code to GitHub. GitHub Actions validates the code, runs unit tests, renders Kubernetes manifests, builds a Docker image, pushes the image to Docker Hub, updates the desired image tag in Git, and commits the manifest update. ArgoCD then syncs the desired state from Git into the K3s cluster.

## Main Technologies

- Python Flask
- Docker
- Docker Hub
- GitHub Actions
- Kubernetes / K3s
- Kustomize
- ArgoCD
- NetworkPolicy
- Kubernetes securityContext

## Verified Capabilities

- Local Flask and Docker smoke testing.
- GitHub Actions CI/CD pipeline.
- Unit testing with `pytest`.
- Kustomize manifest rendering validation.
- Docker image push with immutable commit SHA tags.
- GitOps manifest update by GitHub Actions.
- ArgoCD deployment to K3s.
- End-to-end runtime verification through `/version` and `/healthz`.
- GitOps rollback and roll-forward.
- Isolated ArgoCD Application and AppProject.
- Non-root container runtime.
- Read-only root filesystem.
- Dropped Linux capabilities.
- Disabled privilege escalation.
- Disabled service account token automount.
- RuntimeDefault seccomp profile.
- Ingress NetworkPolicy for the application pod.
- Evidence and runbook documentation.

## Final Verified Runtime

- Image: `hoangdonguit/gitops-cicd-demo-app:sha-c73671f`
- ArgoCD Application: `portfolio-gitops-cicd-demo`
- Namespace: `gitops-cicd-demo`
- Runtime: K3s
- Node observed: `vm2-mesh`
- ArgoCD status: `Synced / Healthy`
- Application health: `/healthz` returned `ok`
- Application version: `/version` returned `sha-c73671f`

## Important Evidence Files

- `docs/evidence/e2e-gitops-proof.md`
- `docs/evidence/rollback-proof.md`
- `docs/evidence/ci-quality-gates-proof.md`
- `docs/evidence/security-hardening-proof.md`
- `docs/evidence/final-runtime-state.md`
- `docs/architecture/architecture-overview.md`
- `docs/architecture/runtime-topology.md`
- `docs/runbook/gitops-runbook.md`
- `docs/decisions/gitops-deployment-boundary.md`
- `docs/decisions/security-hardening.md`

## CV Description

Built an end-to-end CI/CD and GitOps lab using GitHub Actions, Docker Hub, Kustomize, ArgoCD, and K3s. Implemented immutable image tagging, automated manifest updates, ArgoCD-based deployment, rollback/roll-forward verification, CI quality gates, and Kubernetes workload hardening with non-root runtime, read-only filesystem, dropped capabilities, and NetworkPolicy.

## Interview Talking Points

- Why GitHub Actions does not deploy directly with `kubectl apply`.
- How ArgoCD keeps Git as the source of truth.
- Why immutable image tags are better than `latest`.
- How rollback is done by changing Git desired state.
- How AppProject and namespace isolation avoid conflicts with other ArgoCD apps.
- Why non-root containers and restricted securityContext matter.
- Why read-only root filesystem requires a writable `/tmp`.
- How CI quality gates prevent bad code or broken manifests from being deployed.
