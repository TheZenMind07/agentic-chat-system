# Contributing

## Branch & PR workflow

**Direct pushes to `main` are blocked** by branch protection. All changes must go through a pull request.

### Flow

```bash
git checkout -b feat/<short-name>     # or fix/, chore/, refactor/, docs/
git commit -m "..."
git push -u origin feat/<short-name>
gh pr create --fill                   # opens PR against main
gh pr merge --squash --delete-branch  # after CI / review passes
```

### Branch naming

| Prefix | Use |
|---|---|
| `feat/` | new feature |
| `fix/` | bug fix |
| `refactor/` | code change with no behavior change |
| `docs/` | docs only |
| `chore/` | tooling, deps, CI |

### Commit messages

Use a short imperative summary (≤72 chars), then an optional body explaining *why*.

Examples:
- `feat: add driver details sub-agent`
- `fix: handle empty booking id in /chat`
- `refactor: split vision.py into per-task helpers`

### PR rules

- Keep PRs small and focused.
- Reference the plan / docs section your change implements.
- PR title mirrors the commit summary; description lists what & why.
- Squash-merge to keep `main` linear.

### What's blocked

- `git push origin main` → rejected (admin enforcement is on).
- Force-push to any protected branch → rejected.
- Deleting `main` → rejected.
- Merge commits on `main` → blocked (linear history required).