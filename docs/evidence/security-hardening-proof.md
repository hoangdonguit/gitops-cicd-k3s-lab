# Security Hardening Proof

This document records the verified container and Kubernetes workload security hardening for the `gitops-cicd-k3s-lab` project.

## Goal

Harden the demo application workload without breaking the CI/CD and GitOps deployment flow.

## Security Commit

- Security hardening commit: `c73671f`
- GitOps manifest update commit: `3d866b0`
- Deployed image tag: `sha-c73671f`

## Container Image Hardening

The Docker image was updated to run the application as a fixed non-root user:

- UID: `10001`
- GID: `10001`
- Dockerfile user: `USER 10001:10001`

Gunicorn was also configured to log to stdout/stderr and use `/tmp` as its worker temporary directory:

- `--worker-tmp-dir /tmp`
- `--access-logfile -`
- `--error-logfile -`

## Local Hardened Docker Test

The image was tested locally with Docker runtime restrictions similar to the Kubernetes security settings:

- `--read-only`
- `--tmpfs /tmp:rw,noexec,nosuid,size=64m`
- `--cap-drop ALL`
- `--security-opt no-new-privileges`

The application passed the local smoke test:

- `/` returned HTTP 200.
- `/version` returned `security-local`.
- `/healthz` returned `ok`.
- `docker exec ... id` returned `uid=10001(appuser) gid=10001(appgroup)`.

## Kubernetes Workload Hardening

The Deployment now uses pod-level security settings:

- `automountServiceAccountToken: false`
- `runAsNonRoot: true`
- `runAsUser: 10001`
- `runAsGroup: 10001`
- `fsGroup: 10001`
- `seccompProfile: RuntimeDefault`

The container-level security context includes:

- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: [ALL]`

The workload also mounts `/tmp` as an in-memory `emptyDir` to keep runtime compatibility while preserving a read-only root filesystem.

## NetworkPolicy

A NetworkPolicy named `gitops-cicd-demo-app-ingress` was added.

Observed in the cluster:

- Namespace: `gitops-cicd-demo`
- NetworkPolicy: `gitops-cicd-demo-app-ingress`
- Pod selector: `app=gitops-cicd-demo-app,environment=dev`

The policy restricts ingress to the application port while avoiding strict egress blocking during the lab stage.

## Runtime Verification

After GitHub Actions built the new image and updated the GitOps manifests, ArgoCD synced the hardened workload into K3s.

Verified runtime state:

- ArgoCD Application: `Synced / Healthy`
- Running pod: `gitops-cicd-demo-app-5f89f6c596-kt8wh`
- Runtime node: `vm2-mesh`
- Live image: `hoangdonguit/gitops-cicd-demo-app:sha-c73671f`
- Live `APP_VERSION`: `sha-c73671f`
- `/version`: `sha-c73671f`
- `/healthz`: `ok`

Verified pod security context:

```json
{"fsGroup":10001,"runAsGroup":10001,"runAsNonRoot":true,"runAsUser":10001,"seccompProfile":{"type":"RuntimeDefault"}}
```

Verified container security context:

```json
{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"readOnlyRootFilesystem":true}
```

## Why This Matters

The workload now follows safer Kubernetes runtime practices. The application does not need root privileges, Kubernetes API access, extra Linux capabilities, or a writable root filesystem.

This reduces the impact of a compromised container and makes the project closer to production-style Kubernetes deployment practices.
