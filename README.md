# agent-plugins

zsu's plugin catalog for **Claude Code** and **Codex**. The catalog only lists plugins. Each plugin lives
in its own GitHub repo and installs from there.

| Marketplace | Plugins | Add it with |
|---|---|---|
| `zsu` | [data-analyst](https://github.com/zsu/data-analyst) | `zsu/agent-plugins` |

## Install

**Claude Code** (terminal; Desktop: **+** > Add plugins):

```
/plugin marketplace add zsu/agent-plugins
/plugin install data-analyst@zsu
```

From a shell, the same commands work as `claude plugin marketplace add …` and `claude plugin install …`.

**Cowork and claude.ai:** Customize > Plugins > Add > Add marketplace, then enter `zsu/agent-plugins`.

**Codex** (CLI and app):

```
codex plugin marketplace add zsu/agent-plugins
```

Then install the plugins from the Plugins directory.

**Updates.** A plugin updates when its `version` is bumped in its own repo. To refresh the catalog, run
`/plugin marketplace update zsu` in Claude, or `codex plugin marketplace upgrade` in Codex.

### For a team

Add this to a project's `.claude/settings.json`. Collaborators are offered the marketplace once they
trust the folder. Plugins from external repos still need `claude plugin install <name>@<marketplace> --scope project`.

```json
{
  "extraKnownMarketplaces": {
    "zsu": {"source": {"source": "github", "repo": "zsu/agent-plugins"}}
  },
  "enabledPlugins": {"data-analyst@zsu": true}
}
```

## Layout

The catalog sits at the repo root, because both CLIs read the manifest from the root of the
ref they are given.

```
.claude-plugin/marketplace.json    Claude Code catalog
.agents/plugins/marketplace.json   Codex catalog (same name, same plugins)
tests/                             offline checks: python -I tests/run_all.py
tools/check_sources.py             online check that every entry resolves on GitHub
```

Every entry is a `git-subdir` source pointing at `plugins/<name>/` in the plugin's repo, at a `ref`.
Add a `sha` to pin a plugin to an exact commit.
