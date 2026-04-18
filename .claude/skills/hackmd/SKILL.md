---
name: hackmd
description: "HackMD read-only API client + writing-conventions checker for homework hackmd.md files. Use when reading HackMD notes, syncing reports via GitHub Sync, or writing/reviewing any file destined for HackMD (typically homework/*/hackmd.md). Triggers on: HackMD, 'publish report', 'sync to HackMD', 'list my notes', editing homework hackmd.md."
---

# HackMD Integration

Two responsibilities:

1. **Read-only API access** — list and fetch HackMD notes via CLI
2. **Writing convention enforcement** — keep `hackmd.md` output compatible with HackMD's KaTeX + Markdown renderer and the course's style rules

**Publishing is always via GitHub Sync** (push to GitHub, pull from HackMD manually). API upload was removed because the 100 KB payload limit makes it unreliable for real reports and it hides edit history.

## When to invoke this skill

- User reads or lists HackMD notes, or mentions syncing/publishing a report
- Any edit to a file that will be synced to HackMD (typically `homework/*/hackmd.md`) — consult `references/writing-conventions.md` before and after editing to avoid HackMD-specific pitfalls

## Writing conventions (must read before editing hackmd.md)

Full checklist: `references/writing-conventions.md`. Highlights below.

### Course style rules

1. **Neutral voice** — no personal tone; subjective reflection goes to `notes/`, not hackmd.md
2. **No `[TOC]`** — HackMD's built-in TOC is sufficient
3. **No CSS / theme overrides**
4. **Math in LaTeX only** (`$...$` inline, `$$...$$` display); escape C operators: `\%`, `\mathbin{\&}`
5. **Code blocks without line numbers** — use ` ```c `, not ` ```c= `
6. **Key snippets only** — full code on GitHub, not pasted in HackMD
7. **No casual `:::info`/`:::success`/`:::warning`**; `:::danger` reserved for instructor
8. **Full-width Chinese punctuation** — 「，」not `,`
9. **Terminology per 〈資訊科技詞彙翻譯〉 and L10N glossary**
10. **No emoji unless required**
11. **AI use disclosed** — and flag inaccuracies in AI output

### HackMD KaTeX pitfalls (avoid these)

HackMD's renderer is KaTeX, which has stricter edge cases than MathJax. The most common traps:

- **`\text{...\_...}` renders the backslash literally** in HackMD. Inside `\text{}` the underscore escape breaks. Workaround: define a short symbol (e.g. $h$) in surrounding prose and keep the math LaTeX-only; or write the identifier with Markdown backticks outside the math
- **C operators collide with LaTeX**: unescaped `%` starts a LaTeX comment (rest of line eaten); unescaped `&` is a table/alignment separator. Always use `\%`, `\&`, or `\mathbin{\&}` for bitwise-AND spacing
- **Double backslash line breaks inside `$$...$$`** need `\\\\` in some contexts — prefer splitting into multiple `$$...$$` blocks
- **`\boxed{...}` works**; prefer over custom framing
- **Chinese in `\text{}` is fine**, but the `\_` trap above still applies

If you must refer to a function name like `hash_64` inside math, define `h := hash_64(·, b)` in prose and use `h` in the math.

## Publishing workflow: GitHub Sync

1. Edit `homework/<topic>/hackmd.md` locally
2. `git add hackmd.md && git commit -m "..." && git push`
3. In HackMD: **Versions and GitHub Sync → Pull from GitHub**

Benefits:

- No 100 KB payload limit
- Every commit is a tracked edit, satisfying the course's edit-history requirement
- GitHub remains the single source of truth; HackMD is just a rendered mirror

## HackMD anchor format (internal links)

HackMD generates anchors from headings as follows:

1. Lowercase English portions
2. Spaces → `-`
3. Chinese and full-width punctuation kept as-is (`：`, `（`, `）`, etc.)
4. Half-width special chars stripped (`()`, `.`, `,` etc.); `-` kept
5. Number prefixes preserved — `#### 2. 為何不使用 quicksort` → `#2-為何不使用-quicksort`

Examples:

| Heading | Anchor |
|---------|--------|
| `### 鏈結串列 O(1) vs 陣列 O(n)：量化分析` | `#鏈結串列-O1-vs-陣列-On：量化分析` |
| `#### 2. 為何不使用 quicksort` | `#2-為何不使用-quicksort` |
| `## Linux 核心原始碼中的搜尋結果` | `#Linux-核心原始碼中的搜尋結果` |

Write internal links as `[顯示文字](#anchor)`.

## Source citations

- Cite Linux kernel code with a version-tagged GitHub URL: `https://github.com/torvalds/linux/blob/v<tag>/<path>#L<line>`
- For homework-repo code (e.g. `golden_inv.c`), link to `https://github.com/<user>/<repo>/blob/main/<file>`
- Snippets must faithfully reproduce the source; if abbreviated, mark what was omitted

## Read-only API commands

```bash
uv run .claude/skills/hackmd/scripts/hackmd.py auth status
uv run .claude/skills/hackmd/scripts/hackmd.py auth login      # first use
uv run .claude/skills/hackmd/scripts/hackmd.py notes list
uv run .claude/skills/hackmd/scripts/hackmd.py notes get <note-id>
```

Obtain an API token from https://hackmd.io/settings#api. Token is stored at `~/.config/hackmd/token` (mode 0600).

## Guidelines

- Before publishing, remind the user to check AI-use disclosure (`docs/references/ai-guidelines.md`)
- HackMD API has rate limits; avoid frequent calls
- Create/update/delete commands are intentionally absent — only GitHub Sync is supported
