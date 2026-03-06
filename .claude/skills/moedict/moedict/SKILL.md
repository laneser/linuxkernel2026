---
name: moedict
description: "Look up Chinese dictionary definitions from 教育部重編國語辭典修訂本 and academic terminology from 國家教育研究院樂詞網 (NAER). Use when needing Chinese character/word definitions, etymology, pronunciation (注音/拼音), part-of-speech, or bilingual academic terminology lookups. Triggers on: Chinese dictionary lookup, 查字典, 定義是什麼, word etymology, 教育部辭典, moedict, 樂詞網, NAER, academic terminology, 學術名詞, look up the definition of, character radical/stroke information."
---

# Chinese Dictionary & Terminology Lookup

Two data sources:
1. **教育部重編國語辭典修訂本** — fast moedict.tw API → optional official MoE site via Playwright
2. **國家教育研究院樂詞網 (NAER)** — bilingual academic terminology via Playwright

## Usage

```bash
# Basic lookup (fast, uses moedict.tw raw API)
uv run <skill-dir>/scripts/moedict.py 串

# Raw JSON output
uv run <skill-dir>/scripts/moedict.py 串 --json

# Include official MoE dictionary (slower, uses Playwright)
uv run <skill-dir>/scripts/moedict.py 串 --official

# Search NAER academic terminology (Chinese or English)
uv run <skill-dir>/scripts/moedict.py 串列 --naer
uv run <skill-dir>/scripts/moedict.py "linked list" --naer

# Combine all sources
uv run <skill-dir>/scripts/moedict.py 串列 --official --naer
```

Replace `<skill-dir>` with the actual path to this skill directory.

## Data Sources

**教育部重編國語辭典修訂本:**
- **moedict.tw** — community mirror with clean JSON API; fast, no JS needed
- **dict.revised.moe.edu.tw** — official first-hand source; JS-rendered, requires Playwright

**國家教育研究院樂詞網 (NAER):**
- **terms.naer.edu.tw** — bilingual academic terminology database; JS-rendered, requires Playwright

When citing in reports, reference official URLs (printed by default) as primary sources.

## Output

Default (moedict API) output includes:
- Character/word with radical and stroke count
- All heteronyms (異讀) with 注音 and 拼音
- Numbered definitions with part-of-speech tags, examples, and literary quotes
- Official MoE dictionary search URL

With `--official`: additionally fetches the full entry from the official site, along with related compound words and their direct URLs.

With `--naer`: tabular results showing English term, Chinese translation, and academic field.

## Playwright Setup

The `--official` and `--naer` flags require Playwright with Chromium. On first use, the script auto-installs browsers. To install manually:

```bash
uv run python3 -c "
# /// script
# dependencies = ['playwright']
# ///
import subprocess, sys
subprocess.run([sys.executable, '-m', 'playwright', 'install', '--with-deps', 'chromium'], check=True)
"
```

## Limitations

- Moedict API only has single-character and common compound entries; not all compounds are indexed
- Official site lookup is slower (~3-5s per query due to headless browser)
- NAER lookup is slower (~5-8s due to JS rendering and form submission)
- NAER returns first page of results only (up to ~20 entries)
