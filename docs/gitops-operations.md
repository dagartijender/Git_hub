# GitOps Operations Guide

## Promotion

The sample pipeline can update dev, staging, or production through its
`gitOpsEnvironment` parameter. For production use, prefer promotion by pull
request:

1. CI deploys the immutable image tag to dev.
2. Validation runs against dev.
3. A pull request copies the tested tag into staging.
4. A separately approved pull request copies the same tag into production.

This guarantees that promotion reuses the scanned artifact rather than
rebuilding source code.

## Drift

ArgoCD self-heal is enabled. A manual change made with `kubectl` will be
reverted to the state in Git. Emergency changes should still be committed to
Git immediately so the desired state and audit trail remain authoritative.

## Rollback

Revert the GitOps commit that introduced the problematic image:

```bash
git log -- environments/prod/values.yaml
git revert <commit>
git push origin main
```

Do not rebuild an old commit merely to roll back. Reuse the existing immutable
image tag in ACR.

## Disaster Recovery

- Back up the GitOps repository and ArgoCD configuration.
- Retain released images in ACR according to the recovery policy.
- Recreate AKS, install ArgoCD, register the repository, and reapply the
  `AppProject` and `Application` resources.
- ArgoCD will reconstruct the application state from Git.
