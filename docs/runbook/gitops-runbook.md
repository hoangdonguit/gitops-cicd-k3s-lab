# GitOps Lab Runbook

This runbook records common verification, troubleshooting, and rollback commands for the `gitops-cicd-k3s-lab` project.

## 1. Check Repository State

Run before making changes:

    git status --short
    git log --oneline --decorate -5
    git rev-list --left-right --count origin/main...HEAD

Expected clean state:

    0 0

## 2. Check ArgoCD Application

    kubectl get applications.argoproj.io -n argocd portfolio-gitops-cicd-demo

Expected:

    Synced   Healthy

For deeper debugging:

    kubectl describe applications.argoproj.io -n argocd portfolio-gitops-cicd-demo

## 3. Check Kubernetes Workload

    kubectl get all -n gitops-cicd-demo
    kubectl get pods -n gitops-cicd-demo -o wide
    kubectl rollout status deployment/gitops-cicd-demo-app -n gitops-cicd-demo --timeout=120s

Expected:

- Deployment `gitops-cicd-demo-app` is `1/1`.
- Pod is `Running`.
- Service is `ClusterIP`.

## 4. Verify Application Through Port Forward

Terminal 1:

    kubectl -n gitops-cicd-demo port-forward svc/gitops-cicd-demo-app 8082:80

Terminal 2:

    curl http://localhost:8082/
    curl http://localhost:8082/version
    curl http://localhost:8082/healthz

Expected:

- `/healthz` returns `ok`.
- `/version` returns the image tag from the manifest.
- `/` returns the current response message.

## 5. Verify Current Image Tag in Git

    awk '/newTag:/ {print $2}' k8s/base/kustomization.yaml
    grep -nA2 'APP_VERSION' k8s/base/deployment.yaml

## 6. Common Troubleshooting

### 6.1 GitHub Actions cannot push to Docker Hub

Check GitHub repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

The Docker Hub token must have read/write permission for pushing images.

### 6.2 GitHub Actions cannot commit manifest changes

Check GitHub repository settings:

- Settings
- Actions
- General
- Workflow permissions
- Read and write permissions

The workflow also needs:

    permissions:
      contents: write

### 6.3 ArgoCD shows Namespace is not permitted

Observed error:

    resource :Namespace is not permitted in project portfolio-lab

Cause:

`CreateNamespace=true` makes ArgoCD create a cluster-scoped `Namespace` resource. The AppProject must explicitly allow it.

Fix in AppProject:

    clusterResourceWhitelist:
      - group: ""
        kind: Namespace

### 6.4 ArgoCD is OutOfSync or Missing

Check:

    kubectl describe applications.argoproj.io -n argocd portfolio-gitops-cicd-demo

Then force refresh if needed:

    kubectl annotate application portfolio-gitops-cicd-demo -n argocd argocd.argoproj.io/refresh=hard --overwrite

### 6.5 Pod has ImagePullBackOff

Check the image tag in Git:

    awk '/newTag:/ {print $2}' k8s/base/kustomization.yaml

Then check Docker Hub image existence:

    docker pull hoangdonguit/gitops-cicd-demo-app:<tag>

## 7. Rollback Strategy

Rollback is performed by changing the desired image tag in Git, not by manually editing the running pod.

Example target rollback tag:

    sha-9a1d923

Files to update:

- `k8s/base/kustomization.yaml`
- `k8s/base/deployment.yaml`

After committing and pushing the rollback manifest, ArgoCD syncs the previous image version into K3s.

