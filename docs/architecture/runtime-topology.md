# Runtime Topology

This document explains where each part of the `gitops-cicd-k3s-lab` project runs.

## Local Development Machine

Local machine:

- Hostname/user context: `DoneGitOps` / `XuanDong`
- Repository path: `~/Projects/gitops-cicd-k3s-lab`

Local Docker is used for quick validation:

- `docker build` builds the image locally.
- `docker run` runs the container locally for smoke testing.

This local Docker test is separate from the Kubernetes runtime.

## GitHub Actions Runtime

GitHub Actions runs on a temporary GitHub-hosted runner.

It performs CI/CD tasks:

- checkout source code
- build Docker image
- login to Docker Hub using GitHub Secrets
- push image to Docker Hub
- update Kubernetes manifest image tag
- commit manifest changes back to Git

The GitHub Actions runner is temporary and does not host the application after the job finishes.

## Docker Hub

Docker Hub stores the application image:

- Repository: `hoangdonguit/gitops-cicd-demo-app`
- Tags use immutable commit SHA format, for example `sha-be95c88` and `sha-9a1d923`.

## K3s Cluster

The application runtime target is a K3s cluster.

Cluster endpoint:

- `https://100.65.255.2:6443`

Nodes observed in the lab:

- `vm1-gateway`
- `vm2-mesh`
- `vm3-gitops`

The K3s cluster uses `containerd` as the container runtime, not Docker daemon.

## ArgoCD Runtime

ArgoCD is already installed in the K3s/OpenStack lab cluster.

- Namespace: `argocd`
- Portfolio AppProject: `portfolio-lab`
- Portfolio Application: `portfolio-gitops-cicd-demo`

This project reuses the existing ArgoCD instance but stays isolated from other applications through a dedicated project, namespace, and repository.

## Application Runtime

The portfolio application runs in a dedicated Kubernetes namespace:

- Namespace: `gitops-cicd-demo`
- Deployment: `gitops-cicd-demo-app`
- Service: `gitops-cicd-demo-app`
- Service type: `ClusterIP`

Observed rollback runtime state:

- Running pod: `gitops-cicd-demo-app-5b9955c5f6-j6vmt`
- Running node: `vm2-mesh`
- Pod IP: `10.42.1.248`
- Image: `hoangdonguit/gitops-cicd-demo-app:sha-9a1d923`

## End-to-End Runtime Flow

1. Developer pushes code to GitHub.
2. GitHub Actions builds and pushes a Docker image to Docker Hub.
3. GitHub Actions updates the desired image tag in Git.
4. ArgoCD detects the Git change.
5. ArgoCD syncs the Deployment and Service into K3s.
6. K3s schedules the Pod onto a node.
7. containerd on that node pulls and runs the image.

## Useful Inspection Commands

Check cluster nodes:

    kubectl get nodes -o wide

Check ArgoCD pods:

    kubectl get pods -n argocd -o wide

Check application pod placement:

    kubectl get pods -n gitops-cicd-demo -o wide

Check live Deployment image:

    kubectl get deploy gitops-cicd-demo-app -n gitops-cicd-demo -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'

Check live APP_VERSION:

    kubectl get deploy gitops-cicd-demo-app -n gitops-cicd-demo -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="APP_VERSION")].value}{"\n"}'

