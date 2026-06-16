# GitHub Enterprise Learning Lab

This repository is a hands-on starter project for learning how to run a project on GitHub Enterprise from scratch.

It includes:

- A small Python application
- Unit tests
- GitHub Actions CI
- Issue and pull request templates
- CODEOWNERS
- Security policy
- Enterprise setup notes
- Branch protection and governance checklist

## Project Goal

Use this repo to practice the full GitHub Enterprise lifecycle:

1. Create an organization.
2. Create a repository.
3. Push code.
4. Open issues.
5. Create feature branches.
6. Open pull requests.
7. Run CI checks.
8. Review and merge changes.
9. Apply branch protection rules.
10. Document ownership and security expectations.

## Local Setup

This project uses only the Python standard library.

```bash
python3 -m unittest discover -s tests
```

Run the sample app:

```bash
python3 -m src.app
```

## Suggested Learning Flow

Start with [docs/enterprise-setup.md](docs/enterprise-setup.md), then follow [docs/day-one-checklist.md](docs/day-one-checklist.md).

## Repository Structure

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE/
│   └── workflows/
├── docs/
├── src/
├── tests/
├── CODEOWNERS
├── CONTRIBUTING.md
├── SECURITY.md
└── README.md
```
