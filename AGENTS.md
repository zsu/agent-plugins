# agent-plugins (maintainers)

This repo is a catalog. It holds no plugin code. Two marketplaces live on two branches, and each keeps its manifests at the repo root:

| Branch | Marketplace | Added as |
|---|---|---|
| `main` (default) | `zsu` | `zsu/agent-plugins` |
| `dev` (orphan) | `zsu-dev` | `zsu/agent-plugins@dev` |

`main` must stay the default branch. claude.ai organization sync reads only the default branch.

## Rules

- **Two manifests, kept identical.** Each branch has a Claude manifest (`.claude-plugin/marketplace.json`) and a Codex manifest (`.agents/plugins/marketplace.json`). Both have the same `name`, list the same plugins, and point each one at the same repo, path and ref. `tests/test_catalog.py` enforces this.
- **Install from GitHub only.** Every source is remote, normally `git-subdir` pointing at `plugins/<name>` of the plugin's repo.
  - Claude: `url: "owner/repo"`, with `path` written without `./`.
  - Codex: `url: "https://github.com/owner/repo.git"`, with `path` starting with `./`.
  - Never use relative sources.
- **Versions live in the plugin repos only** (`plugin.json`, plus `.codex-plugin/plugin.json`). Never put `version` in a catalog entry. A plugin release is a version bump in its own repo; this catalog changes only to add, remove, re-point or pin a plugin.
- **Entries carry their own display fields** (`description`, `category`; for Codex also `interface`). Both harnesses show only these before install.
- **Plugin names are unique across `main` and `dev`.** If two enabled plugins share a name, one of them loses its hooks.
- **Plugin repos keep no marketplace of their own**, so no one can register the same plugin twice. For local development use `claude --plugin-dir plugins/<name>` or a local `codex plugin marketplace add <path>`.

## Before pushing

```bash
python -I tests/run_all.py
```

```bash
claude plugin validate .
```

```bash
python -I tools/check_sources.py
```

`check_sources.py` needs network access, and the plugin repos must already be pushed.
