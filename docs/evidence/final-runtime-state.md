# Final Runtime State

This document records the final verified runtime state after the rollback and roll-forward test.

## Final Desired State

After proving rollback to `sha-9a1d923`, the application was rolled forward again to the latest verified version.

- Final image tag: `sha-be95c88`
- Image: `hoangdonguit/gitops-cicd-demo-app:sha-be95c88`
- Deployment: `gitops-cicd-demo-app`
- Namespace: `gitops-cicd-demo`
- GitOps controller: ArgoCD
- Runtime target: K3s

## Expected Runtime Verification

The final application version should return:

- `/version`: `sha-be95c88`
- `/healthz`: `ok`
- `/`: `Hello from GitOps CI/CD K3s Lab - deployed by ArgoCD`

## GitOps Meaning

The final state was restored by changing the desired image tag in Git and letting ArgoCD reconcile the K3s cluster. No direct `kubectl set image` or manual Deployment edit was used.
