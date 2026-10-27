# Agent setup — wiring a coding agent to Cloudflare

> Cloudflare's official guides for connecting **your coding agent** (Claude Code, Codex, Cursor, Copilot,
> OpenCode, Windsurf, VS Code, Bionic/LM Studio) to Cloudflare, via two things: **Skills** (prompt packages that teach the
> agent how Cloudflare works) and **MCP servers** (let it call the Cloudflare API). This is about the
> agent *you* code with — not about building agents, which is `products/agents.md`.

## Contents
- When to use (and when not)
- The two pieces: Skills vs MCP
- One-step setup
- Per-agent config (the table that actually matters)
- The MCP servers
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You (or a teammate) want an agent that can **read Cloudflare docs, inspect an account, and deploy**
  without you pasting docs into the prompt.
- You're diagnosing "my agent hallucinates Cloudflare config" → it has no Skills and no MCP wired.
- **Not** for: building a product that *is* an agent (→ `products/agents.md`), remote MCP servers **you**
  author for your own users (→ `products/agents.md` MCP section), or MCP governance/policy (→ Cloudflare One).

## The two pieces: Skills vs MCP
| | Skills | MCP servers |
|---|---|---|
| What | Prompt packages: instructions + slash commands | Protocol letting the agent call external tools/APIs |
| Gives you | Persistent Cloudflare *knowledge* in the agent | Live *action* on your account (read config, deploy, query) |
| Source | `github.com/cloudflare/skills` | `mcp.cloudflare.com` + domain-specific hosts |
| Auth | none | OAuth, triggered on first Cloudflare tool use |

**Every agent Cloudflare lists supports both.** They are complementary — Skills without MCP means the
agent knows but cannot act; MCP without Skills means it can act but guesses at how.

## One-step setup
Cloudflare ships a machine-readable installer prompt. Paste into any agent:
```
Fetch https://developers.cloudflare.com/agent-setup/prompt.md
```
It branches per agent and runs the right installer. Source of truth for the commands below — re-fetch it
rather than trusting a copy, including this file.

**Claude Code is the exception, and the doc is emphatic:** use the plugin commands, **not** `npx skills`
and **not** `claude mcp add` — the plugin handles both halves.
```
claude plugin marketplace add cloudflare/skills
claude plugin install cloudflare@cloudflare
```
(the web guide shows the same two as in-Claude slash commands: `/plugin marketplace add …`, `/plugin
install cloudflare@cloudflare`.) Then `/reload-plugins` inside Claude to activate.

**Everything else** — skills first, then register MCP servers:
```
npx -y skills add cloudflare/skills --skill '*' --yes --global
```

## Per-agent config (the table that actually matters)
The config **file path and the root JSON key differ per agent**. This is the single most common way a
setup silently does nothing.

| Agent | Config location | Root key / mechanism |
|---|---|---|
| **Claude Code** | plugin marketplace | `claude plugin install` (do **not** hand-edit) |
| **Codex** | CLI-managed | `codex mcp add <name> --url <endpoint>` |
| **Cursor** | `.cursor/mcp.json` | `mcpServers` |
| **GitHub Copilot** | VS Code: `.vscode/mcp.json`; Copilot CLI: `~/.copilot/mcp-config.json`, `.mcp.json` or `.github/mcp.json` | `mcpServers` — **except** inside VS Code, where the same file uses `servers` |
| **VS Code** | `.vscode/mcp.json` | **`servers`** — see gotcha |
| **OpenCode** | `.opencode.jsonc` (project) / `~/.config/opencode/opencode.jsonc` (global) | `mcp`, entries `"type": "remote"` |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | `mcpServers` — value key is **`serverUrl`**, not `url` |
| **Bionic** (LM Studio) | see `pages/agent-setup/bionic/index.md` | — |

VS Code example (workspace folder):
```json
{ "servers": { "cloudflare-api": { "type": "http", "url": "https://mcp.cloudflare.com/mcp" } } }
```
After saving, VS Code shows a **Start** CodeLens on the server definition — select it and complete OAuth.
Then Copilot Chat (**Cmd/Ctrl+Shift+I**) in **agent mode**.

## The MCP servers
- **Cloudflare API MCP server** — `https://mcp.cloudflare.com/mcp` (`github.com/cloudflare/mcp`). The docs
  call it "the only MCP server you need": whole API (~2,500 endpoints) via Code Mode `search()`/`execute()`,
  plus a `docs()` tool. Since 2026-10-10 it also serves **Cloudflare skills** via the Skills over MCP
  extension (`skills/list`, files at `skill://<name>/<path>`) — only for clients that support the extension.
  CI/CD: pass a user or account API token as `Authorization: Bearer`.
- **Product-specific (optional)** — the published table is now just `docs` · `containers` · `browser` ·
  `dex` · `casb` (each `https://<name>.mcp.cloudflare.com/mcp`) plus the Agents SDK docs server at
  `https://agents.cloudflare.com/mcp`. The older servers (`bindings`, `builds`, `observability`, `radar`,
  `logs`…) still answer 401 (measured 2026-10-12) but are **no longer listed** — prefer the API server.
- Transport: Streamable HTTP at `/mcp`; old `/sse` URLs are aliases to the same handler, **not** the
  deprecated HTTP+SSE transport — clients forcing SSE must switch.

`prompt.md` now installs only `mcp.cloudflare.com` (re-checked 2026-10-12; it used to add docs/bindings/
builds/observability).

## Gotchas
- **🚨 `mcpServers` vs `servers`.** In VS Code, `.vscode/mcp.json` uses root key **`servers`** (the doc
  says so explicitly); Cursor, Windsurf, Copilot CLI and Claude Desktop use **`mcpServers`**. A config copied between them **fails silently** — no error, the
  server simply never appears. First thing to check when "MCP isn't working".
- **Claude Code: don't mix installers.** `npx skills` or `claude mcp add` alongside the plugin is
  explicitly called out as wrong. Plugin only, then `/reload-plugins`.
- **OAuth is deferred**, not part of install — it fires on the *first Cloudflare tool call*. A setup that
  "looks done" may be unauthorized. In VS Code you must click **Start** first; nothing happens otherwise.
- **Scope is your whole account.** The docs recommend starting on a **demo account** until you're
  comfortable with what you're granting. Treat this as the real advice it is. Since 2026-08-22 the
  consent dialog has an **Edit Permissions** step — Wrangler and the API MCP server use *optional* OAuth
  scopes, so you can decline some instead of approving everything.
- **Skills ≠ MCP.** Installing one and expecting the other's behavior is the second-most-common
  confusion: knows the docs but can't deploy (skills only), or calls APIs but writes wrong config.
- **This page's contents move fast** — agents get added (VS Code landed 2026-07-31; Bionic/LM Studio is
  now listed too). Re-fetch `prompt.md` rather than trusting a cached command.

## Pricing & limits
> No SKU. Skills and the hosted MCP servers are **free**; you pay only for whatever the agent then does
> on your account (Workers, deploys, API usage). Verify on the live pages before quoting.

The agents themselves are third-party and priced independently — the index page's compare table tracks
pricing model (Subscription / Hybrid / BYOK), model flexibility and context approach per agent.

## Going deeper
- Index + agent comparison table: `pages/agent-setup/index.md` · installer: `pages/agent-setup/prompt.md`
- Per-agent guides: `pages/agent-setup/<agent>/index.md` (8 agents). VS Code additionally has
  `visual-studio-code/detailed-walkthrough/` — screenshots of OAuth, verifying the server runs, and
  creating/deleting a DNS record in natural language. Useful to hand a non-technical teammate.
- **No official `cloudflare`-skill reference exists for this slug** — this file is the primary source.
- Building agents (not configuring one) → `products/agents.md`; authoring your own MCP server → same
  file's MCP section (stateless `createMcpHandler` since SDK v0.20.0).
