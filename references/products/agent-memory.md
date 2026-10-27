# Agent Memory — persistent, AI-powered memory for agents

> Managed service that gives agents durable memory across conversations, **without** building your own
> extract → store → search → summarize pipeline. Ingest raw conversations and it auto-extracts
> structured memories; recall them later as a synthesized answer.

> 🔒 **Status: private beta** — not self-serve. The docs only state "You also need access to Agent
> Memory" (Get started → Prerequisites); no waitlist URL is published, so ask Cloudflare for access.
> **Verify you actually have access** with `npx wrangler agent-memory namespace create <name>` (the
> only agent-memory CLI command in the docs). Not billed during beta; Cloudflare gives ≥30 days
> notice before charging.

## Contents
- When to use (and when not)
- Agent Memory vs the Agents SDK (they are separate)
- The 4 memory types
- Binding & config
- The API (ingest / remember / recall + management)
- Namespaces, profiles, sessions
- Gotchas
- Limits & pricing
- Going deeper

## When to use
- Agents that must **remember users/orgs across conversations**: preferences, identities, company
  operating rules, support history, project/object state, long-running tasks.
- You want extraction + storage + semantic/full-text search + summarization as a **managed service**,
  not hand-rolled over a vector DB.
- **Not** for: ephemeral per-session scratch state (use the Agents SDK's own DO storage), raw vector
  search you control (→ vectorize), relational data (→ d1), generic KV (→ kv).

## Agent Memory vs the Agents SDK (IMPORTANT — separate things)
- **Agent Memory is a standalone managed service.** It is **NOT part of the Agents SDK**. You can call
  it from any framework, or even from outside Workers via the HTTP API.
- The **Agents SDK has its own, different memory**: per-agent state in **Durable Object SQLite**
  (`this.state` / `this.sql`, Session API). That is local, agent-scoped conversation state.
- They compose: the Get-started guide wires Agent Memory's `recall()` into the Agents SDK Session API
  as a `search_context` tool — but that is integration, not membership. Use Agent Memory when you need
  **cross-conversation, cross-agent durable knowledge**; use DO-SQLite for the live session.

## The 4 memory types
Every extracted memory is auto-classified into one:
- **Facts** — stable knowledge (preferences, identities, relationships, goals). Evolve via
  **supersession**: a newer fact on the same topic key marks the old one superseded; latest surfaces
  in recall, full history preserved.
- **Events** — completed, time-anchored actions (deployments, decisions, milestones). **Accumulate**,
  never conflict.
- **Instructions** — reusable procedures/workflows/conventions. Like facts, **support supersession**.
- **Tasks** — short-lived, session-scoped items (active investigations, follow-ups). **Deprioritized**
  after the session ends; NOT embedded for semantic search (full-text only).

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "agent_memory": [
    { "binding": "MEMORY", "namespace": "<NAMESPACE_NAME>" }
  ]
}
```
Create the namespace first: `npx wrangler agent-memory namespace create my-agent`.
Run `npx wrangler types` → `interface Env { MEMORY: AgentMemoryNamespace }`. Bind multiple namespaces
with multiple array entries.

## The API
**Namespace methods** (on the binding):
- `getProfile(name)` → `AgentMemoryProfile` — auto-creates if missing (first call is slower).
- `deleteProfile(name)` → marks profile + all its memories/messages for deletion.

**Profile methods** (the core):
- `ingest(messages, { sessionId? })` → `void` — extract memories from a conversation automatically.
  Messages are `{ role: "system"|"user"|"assistant", content, timestamp? }`. **Idempotent** (content-
  addressed). Pipeline: extraction → classification → dedup/supersession → storage (full-text +
  vector embeddings for non-task memories; raw messages stored verbatim too).
- `remember({ content, sessionId? })` → `AgentMemoryMemory` — store ONE memory explicitly when you
  already know what to save (service classifies + summarizes it).
- `recall(query, { thinkingLevel?, responseLength?, referenceDate? })` → `{ count, answer,
  candidates[] }` — runs parallel retrieval (keyword + topic-key + semantic vectors + raw messages),
  scores/ranks, then synthesizes a grounded NL `answer`. Returns **empty answer** (no hallucination)
  if nothing matches. `thinkingLevel` low/medium/high = retrieval breadth; `responseLength`
  short/medium/long.
- `list({ limit?, cursor?, sessionId?, type? })` → `{ memories[], cursor? }` — list entries **omit
  `content`**; paginate via `cursor`. `get(memoryId)` → full memory (throws if missing).
- `delete(memoryId)` → removes memory + its source messages, returns it.
- `deleteSession(sessionId)` / `getSummary({ sessionId? })` → markdown summary of a profile (for
  inspecting what's remembered).

Memory shape: `{ id, type, summary, content, sessionId, createdAt, updatedAt }`.

Also available: **HTTP API** for non-Workers services (`POST .../accounts/<ID>/agent-memory/
namespaces/.../profiles/.../{ingest|remember|recall|summary}`), Bearer API token, standard CF V4
response envelope (`success`/`errors`).

## Namespaces, profiles, sessions
Isolation is `namespace > profile > memory` — **no data crosses these boundaries**.
- **Namespace** — top-level container (separate apps, environments, tenants, or memory layers).
- **Profile** — isolated memory store for ONE entity (user, agent, team, tenant, object). `recall()` on
  Alice's profile NEVER returns Bob's memories. Choose profile names matching your app scope.
- **Session** — optional grouping of memories from one interaction; scoped to a profile (two profiles
  can reuse the same session ID). If omitted, a deterministic session is derived from message content.

## Gotchas
- **Do NOT `ingest()` every turn.** Batch at natural checkpoints — after the user goes idle, on Session
  compaction, or end of conversation. Per-turn ingestion wastes extraction work and is the #1 misuse.
  (Get-started schedules ingest ~10s after idle, with a cursor so each batch only sends new messages.)
- **Recall is eventually consistent.** After ingest, extraction/classification/indexing take time —
  memories aren't instantly recallable (guide waits ≥30s in its test).
- **Binding ≠ model access.** A memory binding does nothing on its own; you must expose `recall()` as a
  tool AND prompt the model when to call it.
- **Treat recalled memory as helpful context, not guaranteed truth** — confirm before irreversible
  actions (supersession means an old value can still appear in history).
- **`list()`/HTTP list omit `content`** — call `get(id)` for the body.
- Facts/instructions **supersede** on matching topic key (no duplicate); events just accumulate.

## Limits & pricing
> 🔒 Private beta — **not billed**; ≥30 days notice before any charging.

**Limits:** messages per `ingest()` **500** · message content **32 KB** (32,768 bytes UTF-8) · `recall()`
query **1 KB** (1,024 bytes) · session ID **64 chars** · profile name **100 chars** · namespace name
**32 chars** · list page size **1–1,000** (default 20; Workers `list()` max 500). Verify on
`developers.cloudflare.com/agent-memory/platform/limits/`.

## Going deeper
- Overview & how-it-works: `developers.cloudflare.com/agent-memory/` and `/concepts/how-agent-memory-works/`.
- Workers API (full): `/agent-memory/api/workers-api/`; HTTP API: `/agent-memory/api/http-api/`.
- Get-started (Agents SDK + Session integration): `/agent-memory/get-started/`.
- Doc index for LLMs: `developers.cloudflare.com/agent-memory/llms.txt`.
