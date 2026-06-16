# Repository Governance

## Roles

| Role | Responsibility |
| --- | --- |
| Maintainer | Owns repository settings and merge policy |
| Developer | Contributes code through pull requests |
| Reviewer | Reviews code, tests, and documentation |
| Security Reviewer | Reviews sensitive or security-related changes |

## Pull Request Rules

Recommended minimum rules:

- One approving review
- Passing CI
- No unresolved review conversations
- Up-to-date branch before merge

## Release Practice

For learning, use lightweight tags:

```bash
git tag v0.1.0
git push origin v0.1.0
```

For real projects, define a release owner and changelog process.

