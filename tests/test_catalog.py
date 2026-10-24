"""Offline checks for the catalog on this branch: the Claude and Codex marketplaces list the same
plugins under the same name, and every plugin installs from GitHub (no relative sources, no versions)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAMES = {"zsu", "zsu-dev"}  # main = zsu, dev = zsu-dev
RESERVED_PLUGIN_PREFIXES = ("claude-", "anthropic-", "openai-")
REMOTE = {"github", "url", "git-subdir"}
LOCAL_PATH = re.compile(r"(?<![A-Za-z])[A-Za-z]:\\[A-Za-z]|/Users/[a-z]|/home/[a-z]|\\Users\\")


def load(*parts):
    return json.loads((ROOT.joinpath(*parts)).read_text(encoding="utf-8"))


class TestCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claude = load(".claude-plugin", "marketplace.json")
        cls.codex = load(".agents", "plugins", "marketplace.json")

    def test_same_marketplace_name(self):
        self.assertIn(self.claude["name"], NAMES)
        self.assertEqual(self.codex["name"], self.claude["name"], "both harnesses must see one marketplace name")
        self.assertTrue(self.claude["owner"]["name"])

    def test_same_plugins_in_both(self):
        c = [p["name"] for p in self.claude["plugins"]]
        x = [p["name"] for p in self.codex["plugins"]]
        self.assertTrue(c)
        self.assertEqual(len(c), len(set(c)), "duplicate plugin names")
        self.assertEqual(sorted(c), sorted(x), "Claude and Codex catalogs list different plugins")
        for n in c:
            self.assertRegex(n, KEBAB)
            self.assertFalse(n.startswith(RESERVED_PLUGIN_PREFIXES), n)

    def test_claude_sources_are_remote(self):
        for p in self.claude["plugins"]:
            src = p["source"]
            self.assertIsInstance(src, dict, f"{p['name']}: relative sources are not allowed; install from GitHub")
            self.assertIn(src["source"], REMOTE, p["name"])
            if src["source"] == "git-subdir":
                self.assertTrue(src["url"] and src["path"], p["name"])
                self.assertFalse(src["path"].startswith(("./", "/")), "Claude git-subdir paths are repo-relative")
            self.assertNotIn("version", p, "versions live in each plugin's plugin.json")
            self.assertTrue(p.get("description"), f"{p['name']}: catalogs show only entry fields before install")

    def test_codex_sources_are_remote(self):
        for p in self.codex["plugins"]:
            src = p["source"]
            self.assertIsInstance(src, dict, p["name"])
            self.assertIn(src["source"], {"url", "git-subdir"}, p["name"])
            self.assertTrue(src["url"].startswith("https://github.com/"), p["name"])
            if src["source"] == "git-subdir":
                self.assertTrue(src["path"].startswith("./"), "Codex paths start with ./")
            self.assertNotIn("version", p)
            self.assertIn(p["policy"]["installation"], ("AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"))
            self.assertTrue(p.get("description"), p["name"])

    def test_sources_agree(self):
        """The two harnesses install the same repo, path and ref for each plugin."""
        cx = {p["name"]: p["source"] for p in self.codex["plugins"]}
        for p in self.claude["plugins"]:
            a, b = p["source"], cx[p["name"]]
            repo = a.get("repo") or a.get("url")
            self.assertIn(repo.removeprefix("https://github.com/").removesuffix(".git"),
                          b["url"].removeprefix("https://github.com/").removesuffix(".git"), p["name"])
            self.assertEqual((a.get("path") or "").strip("/"), (b.get("path") or "").removeprefix("./").strip("/"))
            self.assertEqual(a.get("ref"), b.get("ref"), p["name"])

    def test_no_local_paths(self):
        for f in [ROOT / ".claude-plugin" / "marketplace.json", ROOT / ".agents" / "plugins" / "marketplace.json",
                  ROOT / "README.md", ROOT / "AGENTS.md"]:
            if f.exists():
                for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                    self.assertIsNone(LOCAL_PATH.search(line), f"{f.name}:{i}")


if __name__ == "__main__":
    unittest.main()
