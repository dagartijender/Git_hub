# GitOps Repository

This directory represents the separate repository watched by ArgoCD. In a real
installation, copy `gitops/` into its own Azure Repos or Git repository and
protect its `main` branch.

The application pipeline changes only `environments/<environment>/values.yaml`.
ArgoCD renders the shared chart with that values file and reconciles AKS.

## Layout

```text
gitops/
├── argocd/
│   ├── project.yaml
│   └── applications/
├── charts/gitops-calculator/
└── environments/
    ├── dev/values.yaml
    ├── staging/values.yaml
    └── prod/values.yaml
```

Replace all `REPLACE_*` placeholders before applying the ArgoCD resources.

```bash
kubectl apply -f argocd/project.yaml
kubectl apply -f argocd/applications/dev.yaml
kubectl apply -f argocd/applications/staging.yaml
kubectl apply -f argocd/applications/prod.yaml
```

For a private Azure Repos repository, register repository credentials with
ArgoCD using a secret or workload-appropriate credential mechanism. Do not
commit a personal access token into this repository.
