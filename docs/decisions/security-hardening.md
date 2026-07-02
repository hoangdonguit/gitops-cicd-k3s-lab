# Decision Record: Container and Kubernetes Security Hardening

## Decision

The application workload is hardened using container-level and Kubernetes-level controls:

- Run as a fixed non-root UID/GID: `10001:10001`.
- Disable service account token automount.
- Enable `runAsNonRoot`.
- Use `seccompProfile: RuntimeDefault`.
- Disable privilege escalation.
- Drop all Linux capabilities.
- Use read-only root filesystem.
- Mount `/tmp` as an in-memory `emptyDir`.
- Add an ingress NetworkPolicy that only allows TCP traffic to the application port `8080`.

## Reason

The application is a simple Flask API and does not need root privileges, Kubernetes API access, extra Linux capabilities, or a writable root filesystem.

These settings reduce the impact of a compromised container and make the deployment closer to production Kubernetes practices.

## Notes

`/tmp` is mounted as `emptyDir` because some Python/Gunicorn runtime behavior may require temporary file access. This keeps the root filesystem read-only while preserving runtime compatibility.

The NetworkPolicy is intentionally lightweight. It restricts ingress to the application port but does not yet apply a strict egress deny policy, keeping the lab easier to debug.
