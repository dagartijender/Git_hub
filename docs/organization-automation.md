# Organization Automation With GitHub Actions

This repository includes a manual GitHub Actions workflow that can create a new repository inside a GitHub organization.

Workflow file:

```text
.github/workflows/create-org-repository.yml
```

## What This Automates

The workflow creates a repository in an organization with:

- Repository name
- Description
- Visibility: `private`, `public`, or `internal`
- Optional initial README
- Issues enabled
- Projects enabled
- Wiki disabled

## Required Secret

Create a repository secret named:

```text
ORG_ADMIN_TOKEN
```

For a learning setup, use a GitHub Personal Access Token that has permission to create repositories in the target organization.

Recommended classic token scopes:

- `repo`
- `admin:org`

Do not commit tokens into the repository.

## Add The Secret

In GitHub:

1. Open this repository.
2. Go to **Settings**.
3. Go to **Secrets and variables**.
4. Select **Actions**.
5. Create a new repository secret.
6. Name it `ORG_ADMIN_TOKEN`.
7. Paste the token value.

## Run The Workflow

1. Open this repository on GitHub.
2. Go to **Actions**.
3. Select **Create organization repository**.
4. Click **Run workflow**.
5. Enter:
   - Organization name
   - Repository name
   - Description
   - Visibility
   - Whether to create an initial README

## Important Notes

- The default `GITHUB_TOKEN` cannot usually create repositories in an organization.
- The user or token owner must have permission to create repositories in that organization.
- If your organization blocks personal access tokens, ask an organization owner to approve the token policy or use a GitHub App instead.
- If the repository already exists, the workflow will fail with a GitHub API validation error.

## Next Learning Step

After the repository creation workflow works, add another workflow to apply branch protection rules to the new repository.

