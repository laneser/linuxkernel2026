#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "playwright"]
# ///
"""Look up Chinese dictionary definitions from 教育部重編國語辭典 via moedict.tw API,
with optional Playwright-based lookup from the official MoE dictionary site."""

import argparse
import json
import subprocess
import sys
import urllib.parse

import requests


MOE_API = "https://www.moedict.tw/raw/{word}"
MOE_SEARCH = "https://dict.revised.moe.edu.tw/search.jsp?word={word}"
MOE_ENTRY = "https://dict.revised.moe.edu.tw/dictView.jsp?ID={entry_id}&q=1&word={word}"


def fetch_moedict(word: str) -> dict | None:
    """Fetch definition from moedict.tw raw API."""
    url = MOE_API.format(word=urllib.parse.quote(word))
    resp = requests.get(url, timeout=10)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def format_moedict(data: dict) -> str:
    """Format moedict JSON into readable text."""
    lines = []
    title = data.get("title", "")
    radical = data.get("radical", "")
    stroke = data.get("stroke_count", "")
    if radical or stroke:
        lines.append(f"【{title}】 部首：{radical}  總筆畫：{stroke}")
    else:
        lines.append(f"【{title}】")
    lines.append("")

    for het in data.get("heteronyms", []):
        bopomofo = het.get("bopomofo", "")
        pinyin = het.get("pinyin", "")
        pron = f"  {bopomofo}" + (f"  ({pinyin})" if pinyin else "")
        lines.append(pron)

        for i, defn in enumerate(het.get("definitions", []), 1):
            pos = defn.get("type", "")
            pos_tag = f"[{pos}] " if pos else ""
            lines.append(f"  {i}. {pos_tag}{defn['def']}")
            for ex in defn.get("example", []):
                lines.append(f"     例：{ex}")
            for q in defn.get("quote", []):
                lines.append(f"     引：{q}")
        lines.append("")

    return "\n".join(lines)


def ensure_playwright_browsers() -> bool:
    """Check if Playwright Chromium is installed; install if needed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
        return True
    except Exception:
        print("Installing Playwright Chromium...", file=sys.stderr)
        try:
            subprocess.run(
                [sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"],
                check=True, capture_output=True,
            )
            return True
        except Exception as e:
            print(f"Failed to install Playwright browsers: {e}", file=sys.stderr)
            return False


def fetch_moe_official(word: str) -> dict | None:
    """Fetch from official MoE dictionary using Playwright.
    Returns dict with 'entries' (list of {word, url, id}) and 'definition' (text)."""
    from playwright.sync_api import sync_playwright

    search_url = MOE_SEARCH.format(word=urllib.parse.quote(word))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url, wait_until="networkidle", timeout=15000)

        # Extract search results
        links = page.query_selector_all("a[href*='dictView']")
        entries = []
        for link in links[:10]:
            href = link.get_attribute("href") or ""
            text = link.inner_text().strip()
            if "ID=" in href:
                entry_id = href.split("ID=")[1].split("&")[0]
                entry_url = MOE_ENTRY.format(
                    entry_id=entry_id, word=urllib.parse.quote(word)
                )
                entries.append({"word": text, "url": entry_url, "id": entry_id})

        if not entries:
            browser.close()
            return None

        # Visit first exact-match entry for full definition
        target = entries[0]
        for e in entries:
            if e["word"] == word:
                target = e
                break

        page.goto(target["url"], wait_until="networkidle", timeout=15000)
        body = page.query_selector("body")
        definition = ""
        if body:
            text = body.inner_text()
            # Extract just the definition section
            lines = text.split("\n")
            capture = False
            def_lines = []
            for line in lines:
                if "釋　　義" in line:
                    capture = True
                    continue
                if capture:
                    if "《重編國語辭典修訂本》" in line:
                        break
                    stripped = line.strip()
                    if stripped and stripped != "︿":
                        def_lines.append(stripped)
            definition = "\n".join(def_lines)

        browser.close()
        return {"entries": entries, "definition": definition, "target": target}


def format_moe_official(result: dict) -> str:
    """Format official MoE dictionary result."""
    lines = []
    target = result["target"]
    lines.append(f"教育部重編國語辭典修訂本 —【{target['word']}】")
    lines.append(f"URL: {target['url']}")
    lines.append("")

    if result["definition"]:
        lines.append(result["definition"])
        lines.append("")

    if len(result["entries"]) > 1:
        lines.append("相關詞條：")
        for e in result["entries"]:
            marker = " ←" if e["id"] == target["id"] else ""
            lines.append(f"  {e['word']}: {e['url']}{marker}")

    return "\n".join(lines)


NAER_SEARCH = "https://terms.naer.edu.tw/"


def fetch_naer(word: str) -> list[dict] | None:
    """Fetch academic terminology from NAER 樂詞網 using Playwright.
    Returns list of {index, english, chinese, field} dicts."""
    from playwright.sync_api import sync_playwright
    import time

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(NAER_SEARCH, wait_until="networkidle", timeout=20000)
        time.sleep(1)

        # Find the first visible query_term input
        inputs = page.query_selector_all("input[name='query_term']")
        search_input = None
        for inp in inputs:
            if inp.is_visible():
                search_input = inp
                break
        if not search_input:
            browser.close()
            return None

        search_input.fill(word)
        search_input.press("Enter")
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(3)

        body = page.query_selector("body")
        text = body.inner_text() if body else ""
        browser.close()

        # Parse result rows: "N\tenglish\tchinese\tfield"
        results = []
        for line in text.split("\n"):
            line = line.strip()
            if "下一頁" in line or "最末頁" in line:
                break
            parts = line.split("\t")
            if len(parts) >= 3 and parts[0].strip().isdigit():
                entry = {
                    "index": parts[0].strip(),
                    "english": parts[1].strip(),
                    "chinese": parts[2].strip(),
                    "field": parts[3].strip() if len(parts) > 3 else "",
                }
                if not results or results[-1] != entry:
                    results.append(entry)

        return results if results else None


def format_naer(results: list[dict], word: str) -> str:
    """Format NAER search results."""
    lines = [f"國家教育研究院 樂詞網 — 搜尋「{word}」", ""]
    lines.append(f"{'英文詞彙':<40} {'中文詞彙':<20} {'學術領域'}")
    lines.append("-" * 80)
    for r in results:
        lines.append(f"{r['english']:<40} {r['chinese']:<20} {r['field']}")
    lines.append("")
    lines.append(f"來源：https://terms.naer.edu.tw/")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Look up Chinese dictionary definitions (教育部重編國語辭典) "
        "and academic terminology (國家教育研究院樂詞網)"
    )
    parser.add_argument("word", help="Chinese or English word to look up")
    parser.add_argument(
        "--official", action="store_true",
        help="Also fetch from official MoE dictionary via Playwright"
    )
    parser.add_argument(
        "--naer", action="store_true",
        help="Search NAER 樂詞網 academic terminology via Playwright"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON from moedict API"
    )
    args = parser.parse_args()

    ran_any = False

    # 1. Moedict lookup (fast, always available)
    data = fetch_moedict(args.word)
    if data is not None:
        ran_any = True
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_moedict(data))

        # Print official MoE search URL
        search_url = MOE_SEARCH.format(word=urllib.parse.quote(args.word))
        print(f"教育部重編國語辭典：{search_url}")

    # 2. Optional: official MoE dictionary via Playwright
    if args.official:
        if not ensure_playwright_browsers():
            print("Playwright 未安裝。", file=sys.stderr)
        else:
            print("\n--- 教育部辭典（官方網站） ---\n")
            result = fetch_moe_official(args.word)
            if result:
                ran_any = True
                print(format_moe_official(result))
            else:
                print(f"教育部辭典查無此詞。")

    # 3. Optional: NAER 樂詞網 terminology search
    if args.naer:
        if not ensure_playwright_browsers():
            print("Playwright 未安裝。", file=sys.stderr)
        else:
            print("\n--- 國家教育研究院 樂詞網 ---\n")
            results = fetch_naer(args.word)
            if results:
                ran_any = True
                print(format_naer(results, args.word))
            else:
                print(f"樂詞網查無「{args.word}」相關術語。")

    if not ran_any:
        print(f"找不到「{args.word}」的定義。", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
