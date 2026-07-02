# Final Runtime State

This document records the final verified runtime state after CI quality gates and security hardening.

## Final Desired State

After proving deploy, rollback, roll-forward, CI quality gates, and security hardening, the application is running the latest verified hardened image.

- Final image tag: `sha-c73671f`
- Image: `hoangdonguit/gitops-cicd-demo-app:sha-c73671f`
- Deployment: `gitops-cicd-demo-app`
- Namespace: `gitops-cicd-demo`
- GitOps controller: ArgoCD
- Runtime target: K3s
- Runtime node observed: `vm2-mesh`

## Final Runtime Verification

The final application version returned:

- `/version`: `sha-c73671f`
- `/healthz`: `ok`
- `/`: `Hello from GitOps CI/CD K3s Lab - deployed by ArgoCD`

## Final Security State

The final Deployment includes:

- Non-root runtime with UID/GID `10001`.
- Disabled service account token automount.
- `RuntimeDefault` seccomp profile.
- Disabled privilege escalation.
- Dropped Linux capabilities.
- Read-only root filesystem.
- In-memory `/tmp` mount.
- Ingress NetworkPolicy for the application pod.

## GitOps Meaning

The final state was reached through Git commits and ArgoCD reconciliation. No direct `kubectl set image` or manual Deployment edit was used to change the running application version.
