# End-to-End GitOps Proof

This document records the verified end-to-end CI/CD and GitOps flow for the `gitops-cicd-k3s-lab` portfolio project.

## Verified Flow

1. A code change was committed to the Flask application.
2. GitHub Actions built a new Docker image.
3. The image was pushed to Docker Hub using an immutable commit SHA tag.
4. GitHub Actions updated the Kubernetes manifests in Git.
5. ArgoCD synced the updated desired state into the K3s cluster.
6. The running application returned the new version and response message.

## Key Commits

- Application code commit: `be95c88`
- GitOps manifest update commit: `3b50f5f`
- Deployed image tag: `sha-be95c88`

## Runtime Verification

ArgoCD Application status:

- Application: `portfolio-gitops-cicd-demo`
- Sync status: `Synced`
- Health status: `Healthy`

Kubernetes workload status:

- Namespace: `gitops-cicd-demo`
- Deployment: `gitops-cicd-demo-app`
- Rollout: successful
- Pod status: `Running`

Application verification through port-forward:

- `/healthz` returned `ok`
- `/version` returned `sha-be95c88`
- `/` returned the updated message: `Hello from GitOps CI/CD K3s Lab - deployed by ArgoCD`

## Notes

- GitHub Actions does not deploy directly to Kubernetes.
- GitHub Actions only builds the image and updates the desired state in Git.
- ArgoCD is responsible for syncing the desired state from Git to the K3s cluster.
- Secrets are not stored in the repository. Docker Hub credentials are stored in GitHub Secrets.
