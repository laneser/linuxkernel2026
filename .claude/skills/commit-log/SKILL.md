---
name: commit-log
description: Write high-quality git commit messages following the seven rules from cbea.ms/git-commit. Use when committing code changes, drafting commit messages, or when the user invokes /commit-log. Analyzes staged changes and produces well-structured commit messages with imperative subject lines and explanatory bodies.
---

# Commit Log

Write git commit messages following the seven rules convention. See [references/seven-rules.md](references/seven-rules.md) for the full rule set.

## Workflow

1. Run `git diff --cached` to inspect staged changes; if nothing is staged, run `git diff` and `git status` to understand what could be staged
2. Run `git log --oneline -10` to match the repository's existing commit style
3. Analyze the changes: determine the nature (new feature, bug fix, refactor, docs, test, etc.) and the motivation behind the change
4. Draft the commit message applying all seven rules

## Rules (quick reference)

1. Separate subject from body with a blank line
2. Subject line <= 50 chars (72 hard limit)
3. Capitalize the subject line
4. No period at end of subject line
5. Imperative mood in subject line ("Add feature" not "Added feature")
6. Wrap body at 72 characters
7. Body explains **what** and **why**, not how

## Subject line self-check

The subject must complete: _"If applied, this commit will **{subject}**"_

## Commit message format

```
<Subject line in imperative mood, <=50 chars>

<Body: what changed and why, wrapped at 72 chars.
 Omit body if the change is trivially self-explanatory.>

<Optional trailers: Resolves: #N, See also: #N, Co-Authored-By: ...>
```

## Commit execution

Use a HEREDOC to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
Subject line here

Body text here, wrapped at 72 characters.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

## Important

- Commit messages in this project are written in **English** (per project convention)
- Focus on the "why" — the diff already shows the "how"
- For trivial changes (typo fix, single-line change), a subject-only message is fine
- Do NOT commit unless the user explicitly asks
