#!/usr/bin/env python3
"""HackMD read-only CLI — stdlib only.

Usage:
    hackmd.py auth login          Prompt for API token, verify, save
    hackmd.py auth status         Show current authentication status
    hackmd.py notes list          List your notes
    hackmd.py notes get <id>      Print note content (Markdown)

Writing to HackMD is intentionally unsupported. The HackMD API has a
100KB payload limit which makes it unreliable for real reports, and
the course requires a visible edit history. Instead, edit the report
locally, commit+push to GitHub, and pull from GitHub inside HackMD
(Versions and GitHub Sync → Pull from GitHub).

Configuration:
    Token is stored at ~/.config/hackmd/token (mode 0600).
    Obtain a token from https://hackmd.io/settings#api
"""

from __future__ import annotations

import argparse
import json
import stat
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://api.hackmd.io/v1"
TOKEN_DIR = Path.home() / ".config" / "hackmd"
TOKEN_FILE = TOKEN_DIR / "token"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_token() -> str | None:
    """Return saved token or None."""
    if TOKEN_FILE.is_file():
        return TOKEN_FILE.read_text().strip()
    return None


def _save_token(token: str) -> None:
    """Persist token with restrictive permissions."""
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token + "\n")
    TOKEN_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0600


def _require_token() -> str:
    token = _load_token()
    if not token:
        print("Error: not authenticated. Run: hackmd.py auth login", file=sys.stderr)
        sys.exit(1)
    return token


def _get(path: str, *, token: str) -> dict | list | str:
    """GET request. Returns parsed JSON or empty string on 204."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            if not raw:
                return ""
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        print(f"Error: HTTP {exc.code} — {detail}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Auth commands
# ---------------------------------------------------------------------------

def cmd_auth_login(_args: argparse.Namespace) -> None:
    """Interactively save and verify an API token."""
    print("Obtain a token from: https://hackmd.io/settings#api")
    token = input("Paste your HackMD API token: ").strip()
    if not token:
        print("Error: empty token", file=sys.stderr)
        sys.exit(1)

    me = _get("/me", token=token)
    _save_token(token)
    name = me.get("name", me.get("email", "unknown"))
    print(f"Authenticated as: {name}")
    print(f"Token saved to: {TOKEN_FILE}")


def cmd_auth_status(_args: argparse.Namespace) -> None:
    """Show current auth status."""
    token = _load_token()
    if not token:
        print("Not authenticated. Run: hackmd.py auth login")
        return
    me = _get("/me", token=token)
    name = me.get("name", me.get("email", "unknown"))
    teams = ", ".join(t.get("name", "?") for t in me.get("teams", []))
    print(f"Authenticated as: {name}")
    if teams:
        print(f"Teams: {teams}")


# ---------------------------------------------------------------------------
# Notes commands
# ---------------------------------------------------------------------------

def cmd_notes_list(_args: argparse.Namespace) -> None:
    """List notes in a table."""
    token = _require_token()
    notes = _get("/notes", token=token)

    if not notes:
        print("No notes found.")
        return

    print(f"{'ID':<22} {'Title':<50} {'Updated'}")
    print("-" * 90)
    for n in notes:
        nid = n.get("id", "?")
        title = (n.get("title") or "(untitled)")[:50]
        updated = n.get("lastChangedAt", n.get("createdAt", "?"))
        if isinstance(updated, int):
            from datetime import datetime, timezone
            updated = datetime.fromtimestamp(updated / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        elif isinstance(updated, str):
            updated = updated[:16]
        print(f"{nid:<22} {title:<50} {updated}")

    print(f"\nTotal: {len(notes)} notes")


def cmd_notes_get(args: argparse.Namespace) -> None:
    """Print note content."""
    token = _require_token()
    note = _get(f"/notes/{args.id}", token=token)
    content = note.get("content", "")
    print(content)


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hackmd.py",
        description="Minimal HackMD read-only API client (stdlib only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              hackmd.py auth login
              hackmd.py auth status
              hackmd.py notes list
              hackmd.py notes get <note-id>

            To publish a report, use GitHub Sync (see SKILL.md).
        """),
    )
    sub = parser.add_subparsers(dest="group", help="Command group")

    auth = sub.add_parser("auth", help="Authentication")
    auth_sub = auth.add_subparsers(dest="command")
    auth_sub.add_parser("login", help="Save and verify API token")
    auth_sub.add_parser("status", help="Show auth status")

    notes = sub.add_parser("notes", help="Note operations (read-only)")
    notes_sub = notes.add_subparsers(dest="command")
    notes_sub.add_parser("list", help="List your notes")
    get_p = notes_sub.add_parser("get", help="Get note content")
    get_p.add_argument("id", help="Note ID")

    return parser


DISPATCH = {
    ("auth", "login"): cmd_auth_login,
    ("auth", "status"): cmd_auth_status,
    ("notes", "list"): cmd_notes_list,
    ("notes", "get"): cmd_notes_get,
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.group:
        parser.print_help()
        sys.exit(0)

    key = (args.group, args.command)
    handler = DISPATCH.get(key)
    if handler is None:
        parser.print_help()
        sys.exit(1)

    handler(args)


if __name__ == "__main__":
    main()
