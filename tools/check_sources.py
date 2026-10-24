#!/usr/bin/env python3
"""Online check: every catalog entry on this branch points at a real plugin on GitHub.

    python -I tools/check_sources.py

For each Claude and Codex entry it fetches the plugin manifest at the entry's repo, ref and path
(raw.githubusercontent.com) and checks that the name matches. Run it before pushing. It needs
network access, and the plugin repos must be public and already pushed. Exit 0 ok, 1 problems.
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def repo_of(src: dict) -> str:
    r = src.get("repo") or src.get("url") or ""
    return r.removeprefix("https://github.com/").removesuffix(".git").strip("/")


def fetch(repo: str, ref: str, path: str):
    url = f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.loads(r.read().decode("utf-8")), url
    except (urllib.error.URLError, ValueError) as e:
        return None, f"{url}: {e}"


def main() -> int:
    problems, checked = [], 0
    for label, manifest_rel, plugin_manifest in (
            ("claude", ".claude-plugin/marketplace.json", ".claude-plugin/plugin.json"),
            ("codex", ".agents/plugins/marketplace.json", ".codex-plugin/plugin.json")):
        cat = json.loads((ROOT / manifest_rel).read_text(encoding="utf-8"))
        for p in cat["plugins"]:
            src = p["source"]
            sub = (src.get("path") or "").removeprefix("./").strip("/")
            target = f"{sub}/{plugin_manifest}" if sub else plugin_manifest
            data, where = fetch(repo_of(src), src.get("ref") or "main", target)
            checked += 1
            if data is None:
                problems.append(f"{label} {p['name']}: {where}")
            elif data.get("name") != p["name"]:
                problems.append(f"{label} {p['name']}: manifest name is {data.get('name')!r} ({where})")
            else:
                print(f"ok  {label:6} {p['name']:20} {data.get('version')}  {where}")
    for line in problems:
        print("FAIL", line)
    print(f"{checked} entries checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
