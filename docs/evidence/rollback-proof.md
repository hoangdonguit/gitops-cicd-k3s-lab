# GitOps Rollback Proof

This document records a controlled rollback test for the `gitops-cicd-k3s-lab` project.

## Goal

Verify that the application can be rolled back by changing the desired image tag in Git and allowing ArgoCD to reconcile the K3s cluster state.

## Rollback Strategy

The rollback was performed through GitOps:

1. Update the image tag in `k8s/base/kustomization.yaml`.
2. Update `APP_VERSION` in `k8s/base/deployment.yaml`.
3. Commit and push the manifest change.
4. Let ArgoCD sync the desired state into K3s.
5. Verify the running application version.

No direct `kubectl set image` or manual Deployment edit was used.

## Rollback Evidence

- Rollback commit: `ef2f0f7`
- Previous running tag: `sha-be95c88`
- Rollback target tag: `sha-9a1d923`
- ArgoCD sync revision: `ef2f0f707923fe6c8cbf89b65a0c3bc9e4323d42`
- Live image after rollback: `hoangdonguit/gitops-cicd-demo-app:sha-9a1d923`
- Live `APP_VERSION`: `sha-9a1d923`

## Kubernetes Verification

After rollback:

- ArgoCD Application: `Synced / Healthy`
- Namespace: `gitops-cicd-demo`
- Deployment: `gitops-cicd-demo-app`
- Rollout: successful
- Running pod: `gitops-cicd-demo-app-5b9955c5f6-j6vmt`
- Node: `vm2-mesh`

ReplicaSet state:

- `gitops-cicd-demo-app-5b9955c5f6`: desired/current/ready = `1/1/1`, image `sha-9a1d923`
- `gitops-cicd-demo-app-b554fdc88`: desired/current/ready = `0/0/0`, image `sha-be95c88`

Application verification through port-forward:

- `/healthz` returned `ok`.
- `/version` returned `sha-9a1d923`.
- `/` returned the original message: `Hello from GitOps CI/CD K3s Lab`.

## Why This Matters

This proves that rollback is controlled through Git and ArgoCD rather than direct cluster mutation. Git remains the source of truth and the rollback path is auditable through Git history.

