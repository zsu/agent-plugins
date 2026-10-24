# agent-plugins

zsu's plugin catalog for **Claude Code** and **Codex**. The catalog only lists plugins. Each plugin lives
in its own GitHub repo and installs from there.

| Marketplace | Branch | Plugins | Add it with |
|---|---|---|---|
| `zsu` | `main` | [data-analyst](https://github.com/zsu/data-analyst) | `zsu/agent-plugins` |
| `zsu-dev` | `dev` | [rsi-skill](https://github.com/zsu/rsi-skill) | `zsu/agent-plugins@dev` |

## Install

**Claude Code** (terminal; Desktop: **+** > Add plugins):

```
/plugin marketplace add zsu/agent-plugins
/plugin install data-analyst@zsu

/plugin marketplace add zsu/agent-plugins@dev
/plugin install rsi-skill@zsu-dev
```

From a shell, the same commands work as `claude plugin marketplace add …` and `claude plugin install …`.

**Cowork and claude.ai:** Customize > Plugins > Add > Add marketplace, then enter `zsu/agent-plugins`.

**Codex** (CLI and app):

```
codex plugin marketplace add zsu/agent-plugins
codex plugin marketplace add zsu/agent-plugins@dev
```

Then install the plugins from the Plugins directory.

**Updates.** A plugin updates when its `version` is bumped in its own repo. To refresh the catalog, run
`/plugin marketplace update zsu` (or `zsu-dev`) in Claude, or `codex plugin marketplace upgrade` in Codex.

### For a team

Add this to a project's `.claude/settings.json`. Collaborators are offered both marketplaces once they
trust the folder. Plugins from external repos still need `claude plugin install <name>@<marketplace> --scope project`.

```json
{
  "extraKnownMarketplaces": {
    "zsu": {"source": {"source": "github", "repo": "zsu/agent-plugins"}},
    "zsu-dev": {"source": {"source": "github", "repo": "zsu/agent-plugins", "ref": "dev"}}
  },
  "enabledPlugins": {"data-analyst@zsu": true}
}
```

### Moving from the old `zsu/data-analyst` marketplace

The `zsu` marketplace used to live in the data-analyst repo. If you added it from there, remove it and add
it again from this catalog. The plugin id stays `data-analyst@zsu`.

```
/plugin marketplace remove zsu
/plugin marketplace add zsu/agent-plugins
/plugin install data-analyst@zsu
```

In Codex: `codex plugin marketplace remove zsu`, then `codex plugin marketplace add zsu/agent-plugins`.

## Layout

Each branch has its catalog at the repo root, because both CLIs read the manifest from the root of the
ref they are given.

```
.claude-plugin/marketplace.json    Claude Code catalog
.agents/plugins/marketplace.json   Codex catalog (same name, same plugins)
tests/                             offline checks: python -I tests/run_all.py
tools/check_sources.py             online check that every entry resolves on GitHub
```

Every entry is a `git-subdir` source pointing at `plugins/<name>/` in the plugin's repo, at a `ref`.
Add a `sha` to pin a plugin to an exact commit.
