---
name: llm-wiki
description: >
  Build, maintain, and query LLM-optimized personal wikis — persistent, interlinked
  markdown knowledge bases backed by local git. Use when the user wants to: create a
  new wiki, ingest sources into a wiki, query/search a wiki, update or lint wiki pages,
  or manage wiki history. Triggers on: 'wiki', 'ingest into wiki', 'create wiki',
  'wiki lint', 'wiki search', 'add to wiki', 'update wiki', references to a wiki/
  directory.
---

# LLM Wiki

Persistent, compounding knowledge bases as interlinked markdown in local git repos.
The LLM writes and maintains all content; the user curates sources and directs analysis.

## Architecture

```
wiki-dir/              # A local git repo
├── WIKI.md            # Schema & conventions (read first when entering a wiki)
├── index.md           # Content catalog with one-line summaries
├── log.md             # Append-only chronological operation log
├── overview.md        # High-level synthesis
├── raw/               # Immutable source documents
├── sources/           # Per-source summary pages
├── concepts/          # Concept pages
└── entities/          # Entity pages
```

## Operations

### 1. Create a Wiki

```bash
bash .claude/skills/llm-wiki/scripts/init_wiki.sh <wiki-dir> [wiki-name]
```

Creates directory structure, scaffold files, and initializes local git.

### 2. Ingest a Source

When the user provides a new source (file, URL, paste):

1. Save raw source to `raw/` (immutable — never modify)
2. Read and analyze the source
3. Create `sources/<source-name>.md` with structured summary
4. Update existing concept/entity pages or create new ones
5. Update `index.md` — add/update entries in appropriate table
6. Update `overview.md` if high-level picture changed
7. Append to `log.md`: `## [YYYY-MM-DD] ingest | <source-name>`
8. Commit: `git add -A && git commit -m "ingest: <source-name>"`

Flag where new information **confirms, extends, or contradicts** existing content.

### 3. Query

1. Read `index.md` to find relevant pages
2. Read those pages, synthesize answer with `[[wikilink]]` citations
3. If the answer is a valuable artifact, offer to save as a new page
4. If saved, update index/log and commit

### 4. Update Pages

1. Make edits
2. Update cross-references if page names change
3. Update `index.md` if summaries changed
4. Append to `log.md`: `## [YYYY-MM-DD] update | <description>`
5. Commit: `git add -A && git commit -m "update: <description>"`

### 5. Lint

Scan for: broken `[[wikilinks]]`, orphan pages, empty stubs, contradictions,
stale claims, missing concept pages. Report findings, fix, log, commit.

### 6. History

`git log --oneline` in the wiki dir. Each operation is a commit.

## Conventions

- **Filenames**: kebab-case `.md`
- **Cross-references**: `[[page-name]]` wikilinks
- **Page header**: `# Title` then `> One-line summary.`
- **References section**: at page bottom, link to source pages
- **Git commits**: `<op>: <brief>` — ops: `ingest`, `update`, `lint`, `query`, `init`
- **All commits local-only. Never push.**

## Context Efficiency

On first visit to a wiki in a session:
1. Read `WIKI.md` + `index.md` for orientation
2. Read `overview.md` only for broad questions
3. Drill into specific pages as needed

For large wikis (50+ pages), use grep to search across pages.
