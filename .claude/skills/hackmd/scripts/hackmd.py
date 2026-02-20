#!/usr/bin/env python3
"""HackMD CLI — minimal client using stdlib only.

Usage:
    hackmd.py auth login          Prompt for API token, verify, and save
    hackmd.py auth status         Show current authentication status
    hackmd.py notes list          List your notes
    hackmd.py notes get <id>      Print note content (Markdown)
    hackmd.py notes create        Create a new note (--title, --content or stdin)
    hackmd.py notes update <id>   Update note content (--content or stdin)
    hackmd.py notes delete <id>   Delete a note (requires --yes)

Configuration:
    Token is stored at ~/.config/hackmd/token (mode 0600).
    Obtain a token from https://hackmd.io/settings#api
"""

from __future__ import annotations

import argparse
import json
import os
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


def _api(method: str, path: str, *, token: str, data: dict | None = None) -> dict | list | str:
    """Perform an API request. Returns parsed JSON or empty string on 204."""
    url = f"{API_BASE}{path}"
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if body is not None:
        req.add_header("Content-Type", "application/json")

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

    # Verify by calling /me
    me = _api("GET", "/me", token=token)
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
    me = _api("GET", "/me", token=token)
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
    notes = _api("GET", "/notes", token=token)

    if not notes:
        print("No notes found.")
        return

    # Table output
    print(f"{'ID':<22} {'Title':<50} {'Updated'}")
    print("-" * 90)
    for n in notes:
        nid = n.get("id", "?")
        title = (n.get("title") or "(untitled)")[:50]
        updated = n.get("lastChangedAt", n.get("createdAt", "?"))
        # Truncate ISO timestamp to date+time
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
    note = _api("GET", f"/notes/{args.id}", token=token)
    content = note.get("content", "")
    print(content)


def cmd_notes_create(args: argparse.Namespace) -> None:
    """Create a new note."""
    token = _require_token()
    content = args.content
    if content is None:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            print("Error: provide --content or pipe content via stdin", file=sys.stderr)
            sys.exit(1)

    payload: dict = {"readPermission": "owner", "writePermission": "owner"}
    if args.title:
        payload["title"] = args.title
    if content is not None:
        payload["content"] = content

    note = _api("POST", "/notes", token=token, data=payload)
    nid = note.get("id", "?")
    url = note.get("publishLink", f"https://hackmd.io/{nid}")
    print(f"Created note: {nid}")
    print(f"URL: {url}")


def cmd_notes_update(args: argparse.Namespace) -> None:
    """Update note content."""
    token = _require_token()
    content = args.content
    if content is None:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            print("Error: provide --content or pipe content via stdin", file=sys.stderr)
            sys.exit(1)

    _api("PATCH", f"/notes/{args.id}", token=token, data={"content": content})
    print(f"Updated note: {args.id}")


def cmd_notes_delete(args: argparse.Namespace) -> None:
    """Delete a note."""
    if not args.yes:
        print("Error: pass --yes to confirm deletion", file=sys.stderr)
        sys.exit(1)

    token = _require_token()
    _api("DELETE", f"/notes/{args.id}", token=token)
    print(f"Deleted note: {args.id}")


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hackmd.py",
        description="Minimal HackMD API client (stdlib only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              hackmd.py auth login
              hackmd.py notes list
              hackmd.py notes create --title "My Note" --content "# Hello"
              hackmd.py notes get <note-id>
              echo "# Draft" | hackmd.py notes create --title "Draft"
              hackmd.py notes update <note-id> --content "# Updated"
              hackmd.py notes delete <note-id> --yes
        """),
    )
    sub = parser.add_subparsers(dest="group", help="Command group")

    # -- auth --
    auth = sub.add_parser("auth", help="Authentication")
    auth_sub = auth.add_subparsers(dest="command")
    auth_sub.add_parser("login", help="Save and verify API token")
    auth_sub.add_parser("status", help="Show auth status")

    # -- notes --
    notes = sub.add_parser("notes", help="Note operations")
    notes_sub = notes.add_subparsers(dest="command")

    notes_sub.add_parser("list", help="List your notes")

    get_p = notes_sub.add_parser("get", help="Get note content")
    get_p.add_argument("id", help="Note ID")

    create_p = notes_sub.add_parser("create", help="Create a note")
    create_p.add_argument("--title", help="Note title")
    create_p.add_argument("--content", help="Note content (or pipe via stdin)")

    update_p = notes_sub.add_parser("update", help="Update a note")
    update_p.add_argument("id", help="Note ID")
    update_p.add_argument("--content", help="New content (or pipe via stdin)")

    delete_p = notes_sub.add_parser("delete", help="Delete a note")
    delete_p.add_argument("id", help="Note ID")
    delete_p.add_argument("--yes", action="store_true", help="Confirm deletion")

    return parser


DISPATCH = {
    ("auth", "login"): cmd_auth_login,
    ("auth", "status"): cmd_auth_status,
    ("notes", "list"): cmd_notes_list,
    ("notes", "get"): cmd_notes_get,
    ("notes", "create"): cmd_notes_create,
    ("notes", "update"): cmd_notes_update,
    ("notes", "delete"): cmd_notes_delete,
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
