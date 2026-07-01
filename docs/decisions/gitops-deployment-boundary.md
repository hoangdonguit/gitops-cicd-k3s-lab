# Decision Record: GitOps Deployment Boundary

## Decision

GitHub Actions must not deploy directly to Kubernetes using `kubectl apply`.

Instead:

- GitHub Actions builds and pushes Docker images.
- GitHub Actions updates Kubernetes manifests in Git.
- ArgoCD syncs the desired state from Git into K3s.

## Reason

This keeps Git as the source of truth. The Kubernetes cluster state is reconciled from Git by ArgoCD instead of being mutated directly by CI.

## Consequences

Benefits:

- Clear audit trail in Git.
- Easier rollback by reverting or changing image tags.
- Separation between CI and CD responsibilities.
- Better alignment with GitOps practices.

Trade-offs:

- Requires ArgoCD bootstrap Application.
- Deployment is eventually consistent; ArgoCD may take a short time to reconcile after Git changes.
- AppProject permissions must be configured carefully.

