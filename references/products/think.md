# Think — opinionated chat-agent harness (`@cloudflare/think`)

> ⚠️ **EXPERIMENTAL — APIs may change.** ("Experimental" is the docs' own word; they carry no
> product-level "preview" banner.) Announced 2026-04-15 as "Project Think"; docs still say pieces
> "may evolve before Think graduates out of experimental" (Actions, Channels, `runTurn`).
> Never present as GA. `Think` is a base class wiring the Agents SDK primitives (fibers, sub-agents,
> Session, sandboxed execution) into a full chat lifecycle: agentic loop, persistence, streaming, tools,
> recovery. **Three primitives work standalone on the `Agent` base class** — fibers
> (`runFiber`/`startFiber`), sub-agents (`subAgent`), and Session (`agents/experimental/memory/session`,
> itself experimental). Everything else below — Actions, Channels, Messengers, scheduled tasks,
> `runTurn`, `ThinkWorkflow`, extensions, `createExecuteTool` — is Think-only. See `products/agents.md`
> for the SDK itself.

## Contents
- When to use (and when not)
- Binding & config
- Primitives (the real value)
- Key API surface
- Gotchas
- Pricing & limits
- Going deeper

## When to use (and when not)
- **Use `Think`** when you want a chat agent shipped fast: a 3-line subclass (`getModel()` only) gives
  streaming, message persistence, abort/resume, workspace file tools, and the agentic loop.
  Also for: LLM-writable memory (context blocks), long conversations (non-destructive compaction),
  FTS5 conversation search, sub-agent systems (parent↔child RPC streaming), proactive agents
  (scheduled/webhook-triggered turns), durable async submission.
- **Use `AIChatAgent`** (`products/agents.md`) when you need full control of the LLM call — RAG,
  multi-model, custom streaming — or want a `Response` return type for HTTP middleware/testing.
- **Use the bare `Agent` base class + primitives** when you don't want an opinionated pipeline:
  `runFiber()`, `subAgent()`, `Session`, `@cloudflare/codemode`, `@cloudflare/shell` and
  `@cloudflare/worker-bundler` all work without Think — it's a convenience layer, not a prerequisite
  for any capability below. **Not** for stateless request/response (→ plain Workers) or
  cross-conversation managed memory (→ `products/agent-memory.md`).

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "compatibility_date": "2026-06-26",
  "compatibility_flags": ["nodejs_compat"],
  "ai": { "binding": "AI" },
  "durable_objects": { "bindings": [{ "name": "MyAgent", "class_name": "MyAgent" }] },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyAgent"] }],
  "worker_loaders": [{ "binding": "LOADER" }],   // optional: code execution + extensions
  "browser": { "binding": "BROWSER" },           // optional: cdp.* / browser tools
  "r2_buckets": [{ "binding": "R2", "bucket_name": "agent-files" }] // optional: workspace spillover
}
```
`npm i @cloudflare/think @cloudflare/ai-chat agents ai @cloudflare/shell zod workers-ai-provider`.
Peers you provide: `agents`, `ai` (AI SDK **v6 *or* v7** since 2026-07-23 — supported ranges `ai@^6 || ^7`
and `@ai-sdk/react@^3 || ^4`; **match the majors**: v6↔react v3, v7↔react v4), `zod` (**v4**),
`@chat-adapter/telegram` (optional);
bundled: `@cloudflare/shell` (workspace), `@cloudflare/codemode`, `just-bash`. Route with
`routeAgentRequest()`; client = `useAgent` (`agents/react`) + `useAgentChat` (`@cloudflare/ai-chat/react`)
— same `cf_agent_chat_*` protocol as `AIChatAgent`, so existing chat UI works unchanged.
**Upgrading is not forced:** Think normalizes streaming, tool-completion events and telemetry across both
AI SDK majors, so a v6 app can take the latest `@cloudflare/think` without migrating its AI SDK
integration first — and can adopt v7 later without changing any Cloudflare Agents API it calls.

## Primitives (the real value)
- **Durable execution / fibers** — `runFiber(name, fn)` registers the task in SQLite, keeps the agent
  alive, checkpoints via `ctx.stash(data)` (synchronous write — no async gap), recovers via
  `onFiberRecovered(ctx)` reading `ctx.snapshot`; `startFiber()` for fire-and-forget jobs with
  `idempotencyKey`. Think turns are auto-wrapped (`chatRecovery = true`) so an evicted turn resumes;
  `chatStreamStallTimeoutMs` (off by default) routes stalls into the same bounded path.
- **Sub-agents via Facets** — `this.subAgent(ChildClass, "name")` creates a child DO colocated with the
  parent as a **facet**: own isolated SQLite, typed RPC stub, co-located on the same machine. Only the
  top-level parent needs a DO binding/migration; facet-only children do not.
- **Session API** — tree-structured messages (`parent_id`) → forking, **non-destructive** compaction
  (summaries as overlays, full history kept), FTS5 search per- and cross-session. In `configureSession`,
  `.withContext("memory", {maxTokens})` gives memory the model reads *and writes*
  (`set_context`/`load_context`/`search_context`); `.withCachedPrompt()` for prompt caching.
- **Sandboxed execution (Code Mode)** — `createExecuteTool(this)`: the model writes JS that runs in a
  Dynamic Worker isolate (no ambient network; capabilities granted per binding), seeing `tools.*`,
  `state.*` (workspace), `cdp.*` (browser), `codemode.*`. Recorded on a durable runtime →
  abort-and-replay, audit trail (`runtime.executions()`), reusable snippets.
- **Execution ladder** (blog framing; additive, useful at Tier 0 alone): workspace (`@cloudflare/shell`)
  → isolate (`@cloudflare/codemode`) → npm (`@cloudflare/worker-bundler`) → Browser Run → Sandbox.
- **Self-authored extensions** — sandboxed Workers the LLM writes and loads at runtime (`load_extension`/
  `list_extensions`, needs `extensionLoader`); tools namespaced `math_add`, context blocks
  `notes_scratchpad`. (The blog says extension source persists in DO storage; the docs don't state it —
  don't rely on it.) **Actions** (experimental) — `action()`/`getActions()`:
  idempotency ledger, inline or durable approvals, authorization, reply attachments; timeout **30 s**.
- **Channels** (experimental) — `configureChannels()`: per-surface (`web`/`messenger`/`voice`/`custom`)
  instructions, tool narrowing (filter-only), `maxTurns`. **Messengers** — `getMessengers()`; Telegram
  provider ships (`@cloudflare/think/messengers/telegram`), webhook `/messengers/<key>/webhook`, root only.
- **Scheduled tasks** — `getScheduledTasks()`+`defineScheduledTasks()`; timezone-aware DSL (`every day at
  09:00`, `every week on monday at 09:00`). Exactly one of `prompt` (durable submission) or `handler`;
  at-least-once, late alarms run once and do **not** backfill. **Workflows** — `ThinkWorkflow` +
  `step.prompt(name, { prompt, output: zodSchema, timeout: "3 days" })` when the *steps* matter.

## Key API surface
- **Overrides:** `getModel()` (required) · `getSystemPrompt()` · `getTools()` · `getActions()` ·
  `getScheduledTasks()` · `getMessengers()` · `configureSession()` · `configureChannels()` · `getSkills()`
  · `maxSteps` (**10**) · `sendReasoning` (true) · `workspaceBash` (true) · `waitForMcpConnections`
  (false, 10 s) · `includeMcpTools` (true — set **false** to skip Think's automatic `getAITools()` MCP
  exposure when you surface MCP tools through Code Mode or another mechanism; registration, discovery,
  raw catalog, direct calls and Code Mode connectors still work — 2026-07-22) · `messageConcurrency`
  ("queue") · `chatRecovery` (true) · `contextOverflow` (off).
- **Turns:** `runTurn(options)` is the unified entry point — `mode: "wait"` (≡ `saveMessages()`),
  `"submit"` (≡ `submitMessages()`, durable + idempotent), `"stream"` (≡ `chat()`, RPC callback). Plus
  `continueLastTurn()`, `addMessages()` (transcript only, no inference), `cancelChat(requestId)`,
  `abortRequest()`/`abortAllRequests()`, `waitUntilStable({timeout})`. Submission status: pending →
  running → completed / aborted / skipped / error.
- **Lifecycle hooks:** `configureSession` (once at start) → `beforeTurn` → [`beforeStep` → `onChunk` →
  `beforeToolCall` → tool → `afterToolCall` → `onStepFinish`]* → `onChatResponse`; errors go through
  `classifyChatError` then `onChatError`. `beforeToolCall` can `allow` / `block` / `substitute`.
- **Tool merge order** (later wins on name collision): workspace (`read write edit list find grep
  delete bash`) → `getTools()` → extensions → session tools → skill tools → MCP → client tools.
- **Exports:** `@cloudflare/think` (Think, Session, Workspace, `action`, skills) · `/messengers`
  (+`/telegram`) · `/workflows` · `/tools/{workspace,execute,browser,extensions}` · `/extensions`.
  Runtime config: `configure<T>(obj)` / `getConfig<T>()` — typed, in SQLite, survives hibernation.

## Gotchas
- **Blocking modes cannot nest.** `wait`/`stream`/`continuation` from inside an active turn (e.g. a
  tool's `execute`) **throws** — deadlock. Use `runTurn({mode:"submit"})` or `addMessages()` instead.
- **`chat()` `onInterrupted`** — the RPC promise can resolve *cleanly* while a scheduled continuation
  owns the real answer. A consumer keying off the clean resolve will finalize a partial. Implement it.
- **Approval cards must read `pendingExecutions()`**, not the transcript: the `pending` array in the
  paused tool output is a truncated preview (~2 KB/arg) while up to **1 MB** actually executes on approve.
- **Sandbox `needsApproval` ≠ the client-approval flow** — inside Code Mode a function-valued
  `needsApproval` *always* requires approval and pauses the run durably.
- **Context overflow is opt-in** (`contextOverflow.reactive`/`.proactive`) and needs *both*
  `classifyChatError` (use `defaultContextOverflowClassifier`) and `configureSession()` with
  `onCompaction()` — a no-op compaction cannot rescue an over-budget turn.
- **Bash tool caps:** snapshots ≤ **1,000** workspace files, skips files > **1 MB** (skipped files are
  protected from write-back). Tune via `workspaceBash`, or `workspaceBash = false`.
- `AbortSignal` does **not** cross DO RPC boundaries nor survive hibernation — use `cancelChat(requestId)`
  across a sub-agent boundary. Legacy `chat(msg, cb, { tools })` is **ignored** (warns): tools belong to
  the child. `CodemodeRuntime` must be exported from the Worker entry (it lives in a DO facet).
- **The blog is stale in places** (2026-04-15 vs docs 2026-06): there is **no**
  `@cloudflare/think/tools/sandbox` / `createSandboxTools` export today — Tier 4 Sandbox is wired
  separately (`products/sandbox.md`). Blog model ids (`kimi-k2.5`) trail the docs (`kimi-k2.6`); old
  `agents/api-reference/*` paths moved to `agents/runtime/*` and `agents/harnesses/think/*`.

## Pricing & limits
> ⚠️ **No Think-specific pricing SKU and no public preview pricing page.** You pay for the underlying
> **Durable Objects + Workers** plus whatever model/tools you call — verify on the live pricing pages
> before quoting.

**Cost drivers:** DO requests · DO duration (GB-s — the agent is kept alive during fibers/keepAlive, so
long turns bill wall-clock) · DO **SQLite** storage + rows read/written (Session tree, workspace files,
fiber checkpoints and the submission ledger all live there) · Workers requests/CPU · the **model**
(Workers AI neurons or your own provider) · Browser Run, R2, Sandbox.

**Plan:** Think uses `new_sqlite_classes` exclusively, and SQLite-backed Durable Objects are available on
**both Workers Free and Workers Paid** — a paid plan is *not* required to run one, though free-tier daily
caps apply and exceeding one fails that operation. Verify on the live DO pricing page before advising.

**Key limits:** `maxSteps` **10**/turn · action timeout **30 s** · recovery `maxAttempts` **10**,
`stableTimeoutMs` **10,000**, `noProgressTimeoutMs` **300,000** (5 min), `maxRecoveryWork` **1,000**
(raise or set Infinity for long agentic turns) · sandbox approval args **1 MB** (preview ~2 KB) ·
bash snapshot **1,000** files / **1 MB** each. The rest
is inherited from Workers/DO (CPU 30 s per event, 1 GB state) — see `products/durable-objects.md` and
`products/agents.md`.

## Going deeper
- Canonical: `developers.cloudflare.com/agents/harnesses/think/` (fetch as Markdown — subpages:
  getting-started, configuration, tools, actions, channels, lifecycle-hooks, client-tools, messengers,
  scheduled-tasks, workflows, sub-agents, programmatic-submissions, recovery). **Not** in the official
  `cloudflare` skill's `references/agents-sdk/` — that ref covers the base SDK only. ⚠️ The separately
  installed `agents-sdk` skill *does* ship a `references/think.md`, but it is stale (points at the dead
  `agents/harnesses/think/` path, wrong model id) — prefer this file over it.
- Sibling refs: `products/agents.md` (SDK + memory model), `products/durable-objects.md`,
  `products/dynamic-workers.md`, `products/browser-run.md`, `products/sandbox.md`, `products/workflows.md`.
- Examples: `cloudflare/agents` → `examples/assistant` (multi-session, sub-agent routing, shared
  workspace, MCP, chat recovery, GitHub OAuth) and `examples/context-overflow-recovery`.
- Why Think → the live blog (blog.cloudflare.com), search "Project Think" (design inspired by Pi). Preview moves fast →
  `scripts/changelog-check Agents` before relying on any API here.
