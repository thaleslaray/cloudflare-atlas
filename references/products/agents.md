# Agents — the Agents SDK for building AI agents

> Build stateful AI agents on Cloudflare. Each agent is a **Durable Object**: durable identity,
> per-instance SQLite, real-time WebSockets, scheduled tasks, and recoverable execution — with
> Workers AI (or any provider) for the model. Deploy once; scales to tens of millions of instances.

## Contents
- When to use (and when not)
- The memory model (per-instance, by name)
- Tools & MCP
- Harnesses & model providers
- Binding & config
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Stateful AI agents: chat, voice, email, Slack, webhook-driven — anything needing **persistent
  memory + real-time connections + long-running/scheduled work** tied to one logical actor.
  Voice (`@cloudflare/voice` ≥0.4.0, 2026-09-11): every turn emits a `turnmetrics` event with an
  `outcome` (`completed`, `no_output`, `model_error`, `tts_error`, `aborted`…) and per-stage timings —
  overlapping, **not additive**. Documented in the changelog only so far.
- One agent instance **per user / conversation / entity**, addressed by a stable name.
- Pairs with: Workers AI (models), Workflows (durable steps), Browser Rendering, MCP tools, Vectorize (RAG).
- **Not** for: stateless request/response (→ plain Workers); a managed cross-conversation memory
  service you don't want to build (→ **agent-memory**, see note below); raw key-value (→ kv).

## The memory model (per-instance, by name)
- An agent is a Durable Object. `idFromName("user-123")` → the **same** instance every time, so its
  state and SQLite **are** its memory. Different name = different isolated instance.
- **`this.state` + `this.setState({...})`** — JSON state, auto-synced to connected clients
  (`agents/react` `useAgent`). Use immutable updates; never mutate `this.state` directly.
- **`this.sql`** (tagged template) — per-agent embedded SQLite for structured/large data; create tables in `onStart()`.
- **Session API** (`agents/experimental/memory/session`) — `Session.create(this)`: tree-structured
  conversation history, context blocks, compaction, full-text search. DO-SQLite by default (or Postgres).
  Newer: experimental `Sessions` capability (`agents/sessions`) — already in Think and `AIChatAgent`.
- ⚠️ **This built-in memory is SEPARATE from the Agent Memory product.** Agents SDK memory = state/SQL
  you manage inside one instance. **Agent Memory** = a managed auto-extract/recall service across
  conversations. See `products/agent-memory.md`.

## Tools & MCP
- Agents call tools in their harness loop (**Code Mode** = model orchestrates by writing code); built-in tool
  surfaces: Browser (persistent tabs/logins; **internal hostnames** such as `preview.internal` route to your
  Durable Object, ≥0.31.0), Sandbox, AI Search, Payments, `web_search` (≥0.27.0), `web_fetch` (≥0.28.0), file
  system below. **Agent Skills** (experimental): Think `getSkills()` with `skills.workspace()` / `skills.r2()`.
- **MCP** — an Agent can be an MCP server (expose tools) or an MCP client. Client connections **do not
  survive hibernation** — re-register in `onStart()`.
- **🚨 MCP servers went STATELESS (SDK v0.20.0, 2026-07-27).** `createMcpHandler` now takes a **factory**
  returning an `McpServer` from `@modelcontextprotocol/server`, building an isolated server **per request** —
  tools, prompts, resources, elicitation with **no transport session and no Durable Object**:
  `createMcpHandler(() => new McpServer({name,version}))(request, env, ctx)`. One route serves new *and*
  legacy clients (`legacy: "reject"` for stateless-only; `route` defaults to `/mcp`). **`McpAgent` is
  deprecated + feature-frozen**; **`createMcpHandler(v1Server, options)` is removed in the next major**.
  Sessionful servers run both lanes behind `isLegacyRequest()`, then drain the legacy one →
  `agents/model-context-protocol/guides/migrate-to-mcp-sdk-v2/`. Import from `agents/mcp/server` to keep
  `McpAgent`/SDK-v1 out of the bundle.
- **Protocol deltas (2026-07-28 revision):** no `initialize` handshake (`server/discover` optional) · no
  `Mcp-Session-Id` · server input via a returned `input_required` + client retry, **not** pushed JSON-RPC ·
  list-changes via `subscriptions/listen`, **no `Last-Event-ID` replay** · raw stateless results need
  `resultType`. Spec also deprecates Roots, Sampling, Logging, HTTP+SSE, Dynamic Client Registration.
- **Client side:** `@modelcontextprotocol/client` probes `server/discover` per connection, falling back to
  the legacy handshake — existing `addMcpServer` calls need no protocol-version flag and no second client;
  converted schemas are cached per live connection (2026-07-22, perf only).
- **MCP elicitation (2026-07-13):** `this.mcp.configureElicitationHandlers({...})` answers server-initiated
  elicitation — **form mode** (structured non-sensitive input) and **URL mode** (consent before an
  out-of-band auth/payment flow). Advertised modes persist with the registration across hibernation;
  callbacks reattach in `onStart()`. On the stateless path this arrives as `input_required` (see above).
- **Code Mode invocable WITHOUT the AI SDK (2026-07-22):** `@cloudflare/codemode` (latest) adds `execute()`,
  `search()`, `describe()` to the durable runtime handle — any non-AI-SDK host drives it, **no longer
  Think-only**. Protected connector methods come back `requiresApproval: true`; resolve with `approve()`/`reject()`.
- **MCP server portals (Cloudflare One / Access, 2026-08-07)** — the *operations* answer to "my agent
  needs 9 MCP servers": one HTTP endpoint fronting many upstream servers, Access identity in front.
  Access configuration, not Agents SDK. Per-portal curated tools/prompts with **aliases**; context
  modes `minimize_tools` (adds `portal_query_tools`) and `search_and_execute` (adds `portal_execute`);
  **Code Mode** collapses upstream tools into search + execute in a **Dynamic Worker**; built-ins
  `portal_list_servers` / `portal_toggle_servers` / `portal_toggle_single_server`. Machine clients get
  `401` + `WWW-Authenticate` (managed OAuth) or use an **Access service token**. Transport:
  upstream URL ending `/mcp` → Streamable HTTP only, ending `/sse` → SSE (Streamable HTTP with Gateway routing),
  else probe (only `404`/`405`/`406` fall through). Cloudflare's own product MCP servers dropped `/sse` on
  2026-10-22 (`410 Gone`) — see `products/agent-setup.md`.
  **Gotchas:** sessions die after **24 h of inactivity** · auto-OAuth tool sync only about **every 2
  hours** (and bypasses Gateway) · route through **Gateway** for HTTP logging and DLP.
  → `developers.cloudflare.com/cloudflare-one/access-controls/ai-controls/mcp-portals/`
- **Workers OAuth Provider v1 (2026-10-01, changelog + GitHub docs only):** `@cloudflare/workers-oauth-provider`
  now splits roles — `OAuthAuthorizationServer` (one Worker signs users in, issues tokens, can serve many
  MCP servers) and `OAuthResourceServer` (the MCP Worker; validates tokens over a **Service Binding**,
  publishes RFC 9728 metadata, `401`-challenges token-less requests, rejects other resources' tokens).
  Implements MCP 2026-07-28 auth (Client ID Metadata Documents, issuer identification; Dynamic Client
  Registration still works); `insufficientScope()` = one-line step-up. Single-Worker `OAuthProvider`
  remains; for most 0.x apps the only required change is `resourceMetadata: { resource }`. A
  `migrate-to-1.0` skill ships inside the npm package.
- Agent classes: `Agent` (full control: WebSockets, email, SQL), `AIChatAgent` (**`@cloudflare/ai-chat`** —
  auto-streaming chat, history, resumable). `@callable()` = RPC-invokable (must return serializable values).
- **Background sub-agents (SDK v0.17.0+):** `runAgentTool(SubAgent, { input, detached: { onFinish:
  "method", maxBudgetMs } })` dispatches a sub-agent **without blocking the turn** — durable, survives
  eviction, calls back on finish. (**`runTurn`** = Think's unified turn-admission entry point, not bare `Agent`.)

## Harnesses & model providers
**Runtime vs harness:** the runtime (Lifecycle from `agents/lifecycle`, `routeAgentRequest()`, capabilities
attached with `lifecycle.use()`, observability) answers *where the agent lives and stays durable*; the
**harness** is the per-turn loop. Per `agents/harnesses/`: **Pi** (the docs' recommended start for a new
agent), **OpenCode** (experimental, `OpenCodeHarness`, `@opencode/sdk@2`), **Think** (`products/think.md`), or
your own loop on the runtime. `PiHarness` is from `agents/harness/pi` (singular), a Lifecycle capability;
Pi Durable owns loop, transcript and recovery in the DO's SQLite (tables prefixed `pi_`); a Lifecycle job
alarm restarts an evicted object. Install `agents` + `@earendil-works/pi-durable` + `@earendil-works/pi-ai`
+ `@earendil-works/chord`: optional peers at `~1.4.0` (agents ≥0.30.0 = Pi 1.4); Pi 1.4 migrates SQLite
storage, **no rollback past it**. Pi Durable is experimental. Needs `nodejs_compat`.
**Model providers** (`agents/models/`): **`createAI`** replaced `workers-ai-provider` and `ai-gateway-provider`
(2026-10-21; both frozen and deprecated). `agents/models/ai-sdk` needs `ai@^7` + `@ai-sdk/provider@^4`;
`agents/models/pi-ai` needs `@earendil-works/pi-ai@~1.4.0`. `createAI({ binding: env.AI })`: a `@cf/` id runs
via Workers AI; catalog models and `dynamic/<route>` go through AI Gateway; a vendor model object (e.g.
`@ai-sdk/anthropic`) is wrapped as `ai(model)`; `fallback` lists, **no provider keys in the Worker**
(**Unified Billing** or BYOK). Any other string throws `TypeError`. AI Search → `ai-search-provider`.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "durable_objects": { "bindings": [{ "name": "MyAgent", "class_name": "MyAgent" }] },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyAgent"] }],
  "ai": { "binding": "AI" }
}
```
Route with `routeAgentRequest(request, env)` (and `routeAgentEmail` for email). Package entry points:
`agents` (server), `agents/react` (`useAgent`, `useAgentToolEvents`), plus `agents/client`,
`agents/mcp`, `agents/workflows`, `agents/email`, `agents/lifecycle`, `agents/sessions`, `agents/harness/pi`,
`agents/models/ai-sdk`, `agents/models/pi-ai`. There is no ai-react subpath.
**`useAgentChat` is NOT in `agents/react`** → `@cloudflare/ai-chat/react`; `AIChatAgent` ships in
`@cloudflare/ai-chat`, not `agents`. **AI SDK peer range (2026-07-23):** `agents`, `@cloudflare/ai-chat`,
`@cloudflare/codemode`, `@cloudflare/think` accept `ai@^6` with `@ai-sdk/react@^3` or `ai@^7` with
`@ai-sdk/react@^4` — **pair the majors**; no forced v6→v7 migration, but `agents/models/ai-sdk` is **v7-only**.
**Quickstart:** `npm create cloudflare@latest -- my-agent --type=hello-world --lang=ts`, then the Pi packages + `@cloudflare/computer`.

## Observability: agent traces (2026-08-04)
Traces show each **agent turn** with its model calls, tool runs, approvals, token usage and Workers
runtime operations. Enable `traces` (`enabled: true`) under `observability` in `wrangler.jsonc`;
**Think and Flue apps emit agent traces automatically**; for **direct AI SDK calls** wrap the namespace
once with `wrapAISDK()` (AI SDK v6 and v7; the v7 form also carries the agent identity).

## File system — `@cloudflare/computer` (`agents/tools/filesystem/`)
`new Workspace({ storage: this.ctx.storage })` in a Durable Object: a persistent SQLite-backed working
directory (`workspace.fs`) with tools `read`, `write`, `edit`, `grep`, `ls`, and `exec` once a backend is added
(`createAITools()`, `createPiTools()`; Think includes them). `WorkerJavaScriptBackend` runs ES modules in a
Dynamic Worker (`LOADER` binding): no shell or native binaries; the container backend is experimental.
`onInterrupt: "replay"` resumes runs after a restart (experimental). All users of one instance share its
workspace; for Linux use Sandbox. `@cloudflare/shell` is deprecated (see `products/think.md`).

## Gotchas
- **`setState` not syncing** → you mutated `this.state` directly; always `setState({...this.state, ...})`.
- **AIChatAgent history grows unbounded** → `this.messages` accumulates forever; trim periodically.
- **SQL injection** → use parameterized `` sql`WHERE id = ${id}` ``, never string-interpolate.
- **WebSocket timeout** → call `conn.accept()` in `onConnect()`.
- **Writing an MCP server as `McpAgent`** → deprecated since v0.20.0. Pre-v0.20.0 training data and most
  blog posts still show it; use the `createMcpHandler(factory)` stateless path unless you need sessions.
- **`@callable` returns undefined** → return JSON-serializable plain objects, not class instances/Dates.
- **Schedule cleanup** → prune stale tasks with `getSchedules()`. (A "1000 tasks/agent" cap is widely
  repeated but is NOT on the live limits page — treat it as unverified, don't quote it as fact.)

## Pricing & limits
> ⚠️ No separate "Agents" SKU — you pay for the underlying **Workers + Durable Objects** (+ Workers AI /
> other tools) usage. Verify on the live Workers & DO pricing pages before quoting.

**Billed as:** Workers requests/CPU + Durable Objects (requests, duration/GB-s, SQLite storage rows/reads/writes)
+ whatever models/tools you call (Workers AI, AI Gateway, Browser Rendering...). **A paid plan is not
required** for a SQLite-backed agent: SQLite-backed Durable Objects run on Workers Free too (free-tier
daily caps apply, and exceeding one fails that operation). Key-value-backed DOs are the paid-only case.

**Key limits:** concurrent agents/account **tens of millions+** · agent definitions/account ~250,000+ ·
state per agent **1 GB** · CPU **30 s** per request/WebSocket-msg/scheduled-task (wall-clock unlimited) ·
script size 10 MB. Many limits inherited from Workers/DO —
verify `developers.cloudflare.com/agents/platform/limits/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/agents-sdk/` — note slug **agents-sdk**):
  `configuration.md`, `api.md`, `patterns.md`, `gotchas.md`. Prefer it for full API/patterns.
- Durable Objects internals → `products/durable-objects.md`; managed memory → `products/agent-memory.md`.
- **Don't hand-roll the chat loop** → `products/think.md`. Think (`@cloudflare/think`) is the opinionated chat
  harness over this SDK (Pi is the other — see above). Only fibers (`runFiber`/`startFiber`), sub-agents
  (`subAgent`) and Session work on the bare `Agent`; Actions, Channels, Messengers, `runTurn` and extensions are
  Think-only (Code Mode is **not** — see Tools & MCP). The Session path above is the **bare-`Agent`** one; Think
  exports its own `Session` via `configureSession()`. Don't mix the two import paths.
