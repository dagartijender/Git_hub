# GitHub Enterprise Setup Guide

This guide explains the GitHub Enterprise side of the project.

## 1. Create or Choose an Enterprise

If your company or school already has GitHub Enterprise, ask an administrator for access.

If you are learning personally, you can still practice most repository workflows on a normal GitHub account. Enterprise-only areas include enterprise policies, SAML/SSO, audit logs, managed users, and organization-wide restrictions.

## 2. Create an Organization

Suggested organization name:

```text
github-enterprise-learning
```

Recommended initial teams:

- `maintainers`: repository admins and reviewers
- `developers`: contributors with write access
- `security`: security reviewers
- `readers`: read-only access

## 3. Create the Repository

Suggested repository name:

```text
enterprise-learning-lab
```

Recommended settings:

- Visibility: private for enterprise practice
- Default branch: `main`
- Issues: enabled
- Projects: optional
- Wiki: disabled unless needed
- Discussions: optional

## 4. Push This Local Repository

After creating the empty remote repository in GitHub Enterprise, connect this local repo:

```bash
git branch -M main
git remote add origin https://github.example.com/YOUR_ORG/enterprise-learning-lab.git
git push -u origin main
```

Replace `github.example.com` with your GitHub Enterprise Server hostname or use `github.com` for GitHub Enterprise Cloud.

## 5. Configure Branch Protection

Protect `main` with:

- Require a pull request before merging
- Require approvals
- Require review from Code Owners
- Require status checks to pass
- Require branches to be up to date before merging
- Restrict force pushes
- Restrict deletions

## 6. Configure Repository Access

Use teams instead of adding people directly:

- `maintainers`: admin or maintain
- `developers`: write
- `security`: maintain or triage
- `readers`: read

## 7. Practice Workflow

1. Create an issue.
2. Create a branch from `main`.
3. Make a small code change.
4. Push the branch.
5. Open a pull request.
6. Watch CI run.
7. Request review.
8. Merge after approval.

