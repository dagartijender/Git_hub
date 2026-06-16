# Git Cheatsheet

## Start Work

```bash
git status
git checkout main
git pull
git checkout -b feature/my-change
```

## Save Work

```bash
git add .
git commit -m "Describe the change"
git push -u origin feature/my-change
```

## Review History

```bash
git log --oneline --decorate --graph
```

## Sync Branch

```bash
git checkout main
git pull
git checkout feature/my-change
git merge main
```

## Fix Last Commit Message

```bash
git commit --amend
```

