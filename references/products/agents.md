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
- ⚠️ **This built-in memory is SEPARATE from the Agent Memory product.** Agents SDK memory = state/SQL
  you manage inside one instance. **Agent Memory** = a managed auto-extract/recall service across
  conversations. See `products/agent-memory.md`.

## Tools & MCP
- Agents call tools in their harness loop (**Code Mode** = model orchestrates by writing code); built-in
  tool surfaces: Browser, Sandbox (code exec), AI Search, Payments.
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
  `/mcp` → Streamable HTTP, `/sse` → SSE, else probe (only `404`/`405`/`406` fall through).
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

## Harnesses & model providers (beta, 2026-10-02)
**Runtime vs harness:** the runtime (`Agent`, state, sessions, fibers) answers *where the agent lives
and stays durable*; the **harness** is the per-turn loop (prompt, model call, tools, persistence,
recovery). Options per `agents/harnesses/`: build your own on `Agent`, **Project Think**
(`products/think.md`), or **Pi** — `PiHarness` from `agents/harness/pi` (import path singular), a
"Lifecycle capability" registered with `this.lifecycle.use(harness)`. Pi Durable owns the loop,
transcript and recovery; it stores in the DO's SQLite (tables prefixed `pi_`), and a Lifecycle job
alarm restarts an evicted object mid-run. You choose the transport (WebSockets/HTTP/RPC). Needs
`@earendil-works/pi-durable` + `@earendil-works/pi-ai` ≥1.0 (optional peers of `agents`), a
SQLite-backed DO, `nodejs_compat`. Tools/prompt sections come via Pi's own extensions. Expect API churn.
**Model providers** (`agents/models/`): `agents/models/ai-sdk` (AI SDK v7 provider — needs `ai@^7` +
`@ai-sdk/provider@^4`; works with Think) and `agents/models/pi-ai` (needs `@earendil-works/pi-ai@^1.0.0`).
Both: `createAI({ binding: env.AI })`. A `@cf/` id runs via `env.AI.run()`; a third-party model is
built by the vendor's own package (e.g. `@ai-sdk/anthropic`) and routed through AI Gateway
(`env.AI.gateway(id).run()`) — **no provider API keys in the Worker** (**Unified Billing** or BYOK), fallback
lists mixing both, gateway log id/cache status on every result. (ai-sdk) a non-`@cf/` string throws `TypeError`.

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
`agents/mcp`, `agents/workflows`, `agents/email`, `agents/harness/pi`, `agents/models/ai-sdk`,
`agents/models/pi-ai`. There is no ai-react subpath.
**`useAgentChat` is NOT in `agents/react`** → `@cloudflare/ai-chat/react`; `AIChatAgent` ships in
`@cloudflare/ai-chat`, not `agents`. **AI SDK peer range (2026-07-23):** `agents`, `@cloudflare/ai-chat`,
`@cloudflare/codemode`, `@cloudflare/think` accept `ai@^6` with `@ai-sdk/react@^3` or `ai@^7` with
`@ai-sdk/react@^4` — **pair the majors**; no forced v6→v7 migration, but `agents/models/ai-sdk` is **v7-only**.
**Quickstart:** `npx create-cloudflare@latest --template cloudflare/agents-starter` (no API key — Workers AI default).

## Observability: agent traces (2026-08-04)
Traces show each **agent turn** with its model calls, tool runs, approvals, token usage and Workers
runtime operations. Enable `traces` (`enabled: true`) under `observability` in `wrangler.jsonc`;
**Think and Flue apps emit agent traces automatically**; for **direct AI SDK calls** wrap the namespace
once with `wrapAISDK()` (AI SDK v6 and v7; the v7 form also carries the agent identity).

## `@cloudflare/computer` — agent runtime (early preview, 2026-08-03)
Open-source npm package `@cloudflare/computer`: gives **each agent its own computer** — a
SQLite-backed virtual filesystem (from cloud storage, source control or your files) where agents
read/write/edit, run shell and Git; every operation gated, audited, observed. `new Workspace({ storage:
this.ctx.storage })` inside any Durable Object. **Two backends:** *isolate* (`just-bash` + Dynamic
Workers — fast, scalable, file/data work) and *container* (full Linux via Containers over FUSE — native
binaries, package managers). AI SDK-compatible toolkit (`read`, `write`, `edit`, `ls`, `exec`).
**vs Sandbox SDK:** Sandbox isolates *untrusted* code; computer gives a *trusted* agent a persistent
workspace and picks isolate-vs-container per operation. Preview — `github.com/cloudflare/computer`;
no production without a fallback.

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
- Starter to build on / tear apart: `cloudflare/agents-starter` repo.
- Durable Objects internals → `products/durable-objects.md`; managed memory → `products/agent-memory.md`.
- **Don't hand-roll the chat loop** → `products/think.md`. Project Think (`@cloudflare/think`,
  ⚠️ experimental) is the opinionated chat harness over this same SDK (Pi is the other — see above). Only three of its primitives work on the
  bare `Agent` — fibers (`runFiber`/`startFiber`), sub-agents (`subAgent`), Session; Actions, Channels,
  Messengers, `runTurn` and extensions are Think-only (Code Mode is **not** — see Tools & MCP above).
  The Session path above (`agents/experimental/memory/session`) is the **bare-`Agent`** one; Think exports
  its own `Session` via `configureSession()`. Don't mix the two import paths.
