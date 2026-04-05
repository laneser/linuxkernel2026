#!/usr/bin/env bash
# Initialize a new LLM wiki at the given path.
# Usage: init_wiki.sh <wiki-dir> [wiki-name]
set -euo pipefail

WIKI_DIR="${1:?Usage: init_wiki.sh <wiki-dir> [wiki-name]}"
WIKI_NAME="${2:-$(basename "$WIKI_DIR")}"
DATE=$(date +%Y-%m-%d)

if [ -d "$WIKI_DIR/.git" ]; then
    echo "Error: $WIKI_DIR is already a git repo." >&2
    exit 1
fi

mkdir -p "$WIKI_DIR/raw"

# index.md — content catalog
cat > "$WIKI_DIR/index.md" << EOF
# ${WIKI_NAME} — Index

> Auto-maintained by LLM. Lists every wiki page with a one-line summary.

## Sources

| Page | Summary | Date |
|------|---------|------|

## Concepts

| Page | Summary |
|------|---------|

## Entities

| Page | Summary |
|------|---------|
EOF

# log.md — chronological record
cat > "$WIKI_DIR/log.md" << EOF
# ${WIKI_NAME} — Log

> Append-only chronological record of wiki operations.

## [${DATE}] init | Wiki created
- Name: ${WIKI_NAME}
- Path: ${WIKI_DIR}
EOF

# overview.md — high-level synthesis
cat > "$WIKI_DIR/overview.md" << EOF
# ${WIKI_NAME} — Overview

> High-level synthesis of the wiki's content. Updated as new sources are ingested.

*No sources ingested yet.*
EOF

# WIKI.md — schema / conventions (the LLM reads this to understand the wiki)
cat > "$WIKI_DIR/WIKI.md" << 'WIKIEOF'
# Wiki Schema

## Directory Layout

```
.
├── WIKI.md          # This file — conventions and schema
├── index.md         # Content catalog (LLM-maintained)
├── log.md           # Chronological operation log (append-only)
├── overview.md      # High-level synthesis
├── raw/             # Immutable source documents
├── sources/         # Per-source summary pages (auto-created)
├── concepts/        # Concept pages
└── entities/        # Entity pages
```

## Page Format

Every wiki page (except index/log) uses this structure:

```markdown
# Title

> One-line summary.

Body text with [[wikilinks]] to other pages.

## References
- [source-name](../sources/source-name.md)
```

## Wikilinks

Use `[[page-name]]` syntax for cross-references. Page names are kebab-case.
When creating or updating a page, ensure all outbound links point to existing
pages or flag them as stubs to create later.

## Git Conventions

- Every wiki operation (ingest, update, lint) produces a git commit.
- Commit messages: `<op>: <brief description>` (e.g., `ingest: add chapter-3-notes`).
- All commits are local-only. Never push.
WIKIEOF

mkdir -p "$WIKI_DIR/sources" "$WIKI_DIR/concepts" "$WIKI_DIR/entities"

# Initialize git
cd "$WIKI_DIR"
git init -q
git add -A
git commit -q -m "init: create ${WIKI_NAME} wiki"

echo "Wiki initialized at ${WIKI_DIR}"
