# AI Gateway — observe, cache, rate-limit & route AI provider calls

> A proxy you put **in front of any AI provider** (OpenAI, Anthropic, Workers AI, Google, Groq,
> 24 provider integrations). One URL change buys you analytics, caching, rate-limiting, retries/fallback,
> cost tracking, and guardrails — no SDK rewrite.

## Contents
- When to use
- How to wire (change the base URL)
- Key features
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You call **any** AI provider and want **observability**: requests, tokens, latency (p50/p95/p99),
  cost, cache-hit rate — per request, with custom metadata.
- **Cost control:** cache deterministic prompts (free), rate-limit to stop abuse, track spend.
- **Resilience:** automatic **retries / fallback** across models or providers (routing: Auto Router, model aliases, dynamic routes).
- **Governance:** guardrails (content filtering) and DLP (PII detection) on prompts/responses.
- **Simpler keys:** Unified Billing (pay through Cloudflare, no provider key) or BYOK (store keys).
- **Not** a model host — that's Workers AI. AI Gateway sits *in front of* providers, including Workers AI.

## How to wire (change the base URL)
The whole product is "point your existing client at the gateway." Entry shapes:
- **🚨 New gateways require authentication (changelog 2026-11-03).** Creating via API: `authentication` defaults
  to `true`; `false` → HTTP `400`. Once on it **cannot be turned off** (update with `false` → `400`
  "Authentication cannot be disabled once enabled."). Existing gateways with auth off keep working; turn on
  in Settings or `{"authentication": true}`. Unauthenticated HTTP calls to a new gateway fail (missing
  authorization): REST API → `Authorization: Bearer <CF token>`; `gateway.ai.cloudflare.com` endpoints →
  `cf-aig-authorization`; Workers bindings are pre-authenticated. Tokens (`AI Gateway Run`) are account-scoped,
  not per-gateway. → `ai-gateway/configuration/authentication/`
- **REST API (preferred for single-model calls)** — base `https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai`,
  auth = Cloudflare API token with **Account → Workers AI → Read** (an AI-Gateway-only token returns `401`
  code `10000`). Endpoints: `/ai/run` (any model/modality), `/ai/v1/chat/completions`, `/ai/v1/responses`,
  `/ai/v1/messages` (Anthropic schema, **no `@cf/` models**). Third-party ids are `author/model`; `@cf/`
  models over REST also need `cf-aig-gateway-id`. Point the OpenAI SDK's `baseURL` at `…/ai/v1` with the
  Cloudflare token as `apiKey` — no provider key needed (billed via Unified Billing).
- **Unified / OpenAI-compatible** — `…/{gateway_id}/compat/chat/completions`, `model: "{provider}/{model}"`,
  `cf-aig-authorization: Bearer <token>` on authenticated gateways. **Deprecated for standard single-model
  chat completions** (still works for existing integrations).
- **Provider-specific** — `…/{gateway_id}/{provider}/{endpoint}` (keep the provider's own request shape).
- **Workers AI binding** — pass `{ gateway: { id: 'my-gateway', metadata: {...} } }` to `env.AI.run(...)`.
  **Since 2026-08-07 this is the unified path:** the same `env.AI` binding and the same REST `/ai/`
  endpoints (with Cloudflare auth) call **both** Workers AI models and supported third-party
  providers, with the gateway supplying observability, logging, caching, security and **billing
  controls**. Use `gateway: { id: 'default' }` to auto-create a gateway on the first authenticated
  request, or name one to separate apps/workloads.
- **Vercel AI SDK / Pi AI (2026-10-21)** — `createAI` from `agents/models/ai-sdk` (needs `ai@^7`) or `agents/models/pi-ai`:
  `createAI({ binding: env.AI, id })`, or `{ accountId, apiToken, gateway }` outside a Worker. Takes catalog ids
  (`anthropic/...`), `@cf/` ids, `dynamic/<route>` or a vendor model object (goes to the provider-native endpoint);
  `fallback: [...]` replaces the old model array; also `byokAlias`, `zdr`, `vendorKey`. **`ai-gateway-provider`
  is deprecated and feature frozen** (`createAiGateway(...)` → `createAI(...)`). → `ai-gateway/integrations/vercel-ai-sdk/`, `.../pi-ai/`.

## Key features (controlled via `cf-aig-*` headers or dashboard)
- **Caching** — `cf-aig-cache-ttl` (60s–30d), `cf-aig-skip-cache`, `cf-aig-cache-key`; check
  `cf-aig-cache-status` (`HIT` or `MISS`). Cuts cost+latency on repeat prompts.
- **Rate limiting** — fixed or sliding window; returns `429` when exceeded.
- **Routing** (dashboard: gateway → **Routing**; `ai-gateway/features/routing/`, 2026-11-04 reorg of the old
  `auto-router/` and `dynamic-routing/` roots; no app-code change; `model-aliases`):
  - **Auto Router** (`.../routing/auto-router/`) — model `cloudflare/auto` picks by task vs cost, falls back on
    failure; `Chat Completions` + Responses only (no WebSockets API); headers `cf-aig-routed-model`, `cf-aig-routing-reason`.
  - **Model aliases** (`.../model-aliases/`, 2026-11-04) — a pool called by one name `custom/<name>`, per
    gateway; algorithm `preferred` (default order, fall back on failure) or `smart`; per-request override
    `options.routing` (`algorithm`). Call via `/ai/run` with `cf-aig-gateway-id`. Limits: 100 aliases/gateway,
    1–50 models each, name 1–64 chars, no alias-of-alias, **no x402**. Errors: `404` `Model not found`,
    `400` `has no available models`, `503` temporarily unavailable.
  - **Dynamic routes** (`.../dynamic-routing/`, + `json-configuration/`, `usage/`) — versioned flow of nodes
    (Start, Conditional, Percentage, Model, Rate Limit, Budget Limit, End); `model: "dynamic/{route}"`,
    OpenAI chat-completions shape only (else `400`). Callable via `/ai/v1/chat/completions`, the AI binding or
    `/compat/chat/completions`; **not `/ai/run`** (`400` code `7003`). Scoped per gateway: set `cf-aig-gateway-id`
    (REST/binding) or default gateway → `404`. Needs authentication on + BYOK keys. Response headers `cf-aig-model`, `cf-aig-provider`.
- **Guardrails** — flag/block prompts+responses (`@cf/meta/llama-guard-3-8b` on Workers AI, billed as Workers AI tokens).
- **DLP** — **flag or block** (no redaction) PII/financial/health matches; free, shares Cloudflare One profiles.
- **Logging & analytics** — full request logs (prompt, tokens, cost, duration, metadata); Logpush export (account dataset
  ai_gateway_events, fields at developers.cloudflare.com/logs/logpush/logpush-job/datasets/account/ai_gateway_events/). Log and request IDs are UUIDv7 since 2026-10-08.
- **Custom metadata** — `cf-aig-metadata` (max 5 flat entries) for per-request tagging/filtering.
- **Custom costs** — `cf-aig-custom-cost` with `per_token_in`/`per_token_out`, plus (2026-09-09)
  `per_cache_read_token`/`per_cache_write_token`; one cache rate set → the other defaults to `per_token_in`;
  cache tokens are de-duplicated whether the provider counts them inside input or separately.
- **Machine Payments** (x402, beta, 2026-09-30) — pay per request from a stablecoin wallet instead of
  prepaid credits: send `Payment-Method: x402` (Cloudflare-specific) with a Cloudflare API token to
  `POST /ai/run` (the only eligible endpoint) → `402` (`Payment Required`) + `PAYMENT-REQUIRED` header
  (most models use the `upto` scheme = max charge) → wallet signs → retry with `PAYMENT-SIGNATURE`;
  actual cost settled, never above the authorized max. Eligible: `z-ai/glm-4.7-flash`,
  `google/gemma-4-26b-a4b-it`, `openai/gpt-oss-20b`, `alibaba/qwen3.8-27b`. US-based accounts with a
  card on file only. **Omit the header and credential precedence applies — it may spend Unified
  Billing credits.** → `ai-gateway/features/machine-payments/`.
- **Web Search API** (beta, 2026-10-02) runs through the gateway (`env.AI.websearch(...)`, billed to
  gateway credits) → `products/web-search.md`.

## Cloudflare Access in front of the gateway (identity-aware, 2026-08-05)
Answers "who spent this, who may call the model" **without trusting a client-sent user ID**.
- **Prerequisites:** a **custom domain** on the gateway + Access enabled; the gateway's **Access** tab
  provisions the Access application so non-browser clients can authenticate with a bearer token.
- **How it works:** a valid **Access JWT** *is* the request credential — no AI Gateway token needed.
  The gateway stamps the verified user into metadata as **`cf.user_id`** (the JWT `sub` claim,
  **not** the email), so logs, analytics and spend filter by real identity. Cloudflare-only
  credentials (Access JWT, gateway auth headers) are stripped before the upstream provider sees them.
- **🚨 Breaking once enabled:** every request to that custom domain must pass an Access policy.
  Integrations sending only a gateway token are **blocked by Access before reaching the gateway**.
  Migrate them, or keep that traffic on the unprotected default `gateway.ai.cloudflare.com`.
- **Limits:** no `cf.user_id` without a valid JWT carrying a non-empty subject · **service-token
  requests never carry `cf.user_id`** (no individual user) · you cannot set metadata keys starting
  with `cf.` — reserved and silently dropped.
- CLI/agent clients: `cloudflared access curl`; per-agent setup in `ai-gateway/integrations/coding-agents/` (`Claude Code`,
  Claude Desktop, Codex, OpenCode, Pi, Copilot CLI, Gemini CLI — Access-protected custom domain — VS Code / Xcode via a
  custom domain). **Cursor:** custom OpenAI base URL `…/ai/v1` + Cloudflare token as OpenAI key; endpoint must be public
  (Cursor calls from its servers); chat works with `@cf/` models, agent mode needs a Responses-capable third-party model.
  **`Android Studio`:** built-in assistant or Copilot Chat via `…/compat` (deprecated, but the REST API has no `/v1/models`
  for the model list); token needs **AI Gateway → Run**.

## User Insights — spend attribution & anomaly detection
Free to all AI Gateway customers, **no setup** — it reads traffic already flowing through the gateway.
- **Attribution is the catch:** without an identity, *all* usage collapses into one anonymous bucket.
  Attribute either via **custom metadata** with your own user id, or by putting the gateway behind
  **Access** (above), which supplies a verified one.
- **Org metrics:** active users · total requests · adoption rate (IdP identities with ≥1 request) ·
  median tokens/active user · median spend/active user · share of requests from the top 10% ·
  **users to review** (cost ≥ 2× median) · **identity coverage** (share of requests actually attributed).
- **Anomaly detection** — baselines **per session, not per request**: each user's **p95 session cost
  over 30 days**, rolling. A session is flagged only when it exceeds **both** 2× that user's own p95
  **and** the org-wide p99 session cost. Both thresholds by design — otherwise a low-usage user's small
  spike and a heavy user's routine expensive session would both fire. Catches leaked credentials and
  runaway agents. **It flags; it does not block.**
- Per-user view adds cache hit rate, errored requests, session count, top model/provider, last seen,
  active days.
- **Task analysis (changelog 2026-09-29, not yet on the docs page):** groups conversations by task,
  tracks turns, compares model fit vs cost/latency; a **Potential Savings** view flags requests a
  faster/cheaper model could serve — the same signals the Auto Router (`ai-gateway/features/routing/auto-router/`) uses.

## Gotchas
- **Streaming responses are not cached by default**; caching covers text and image responses only.
- **Cache misses on param drift** — any body difference = different key; use `cf-aig-cache-key` to override.
- **Unified API needs the provider prefix:** `openai/gpt-4o`, NOT `gpt-4o`.
- **Rate limit is per-gateway, not per-user** — for per-user limits use dynamic routing.
- **Credential precedence, not a mix:** provider key on the request → BYOK `default` alias → Unified
  Billing. On Unified Billing paths (`env.AI.run()`, `/ai/v1/chat/completions`) only the `default`
  alias stops fall-through — a key under another alias is ignored and the call **silently bills credits**.
- **401 checklist:** token in `Authorization` on the REST API but `cf-aig-authorization` on `gateway.ai.cloudflare.com` · provider path or
  `{provider}/` model prefix present · BYOK key aliased `default` or named via `cf-aig-byok-alias`.
- **Rejected provider key on REST `POST /ai/run` (changelog 2026-10-06):** now always HTTP `401`, error code `2009` — was
  `403` (ElevenLabs), `500` with retries (Vertex, now no retry), `402`/provider-specific (others). Unified Billing
  credential rejected by the provider → HTTP `503`.
- `cf-aig-collect-log: false` disables logging for a request; `cf-aig-collect-log-payload: false` keeps the log
  but drops bodies. (No log-delay figure is published — the previous "30–60s" here had no source; removed.)
- Metadata is **flat only** (no nesting), max 5 entries.

## Pricing & limits
> ⚠️ Pricing/limits change — verify live (`developers.cloudflare.com/ai-gateway/reference/pricing/`
> and `/reference/limits/`) before quoting.

**Cost** (verified 2026-08-25): core features (analytics, caching, rate limiting) are **free** on all plans.
- **DLP:** free. **Guardrails:** billed as Workers AI token inference.
- **Unified Billing:** provider rates passed through at cost + **5% fee** on credit purchases.
- **Logpush** (all plans): billed per Logpush pricing (volume exported and transformed) — the old "10M requests/mo then $0.05/million" line is gone from the AI Gateway page.
- **Log storage:** first gateway created on/after **2026-09-24** → Workers Logs pricing and retention; earlier gateways → Legacy Logs.

**Key limits:** cacheable request **25 MB** · cache TTL **1 month** · custom metadata **5/request** ·
gateways **10/account free, 20 paid** · gateway name **64 chars** · Legacy Logs only: storage rate **500 logs/s/gateway**,
stored **100k/account free, 10M/gateway paid**, **10 MB/log** (datasets limit no longer on the limits page) ·
Unified Billing rate **200 req/60s/gateway** (`429`; BYOK exempt) · Logpush jobs **4/account**, **1 MB/log**.

## Going deeper
- Covered by the official `cloudflare` skill (`references/ai-gateway/`) — use it for full
  patterns: `sdk-integration.md` (Vercel/OpenAI/Workers; predates `createAI`), `configuration.md`, `features.md`,
  `troubleshooting.md` (official ref still names `dynamic-routing.md` — predates the `routing/` reorg; use the paths above).
- Provider-specific quirks → `developers.cloudflare.com/ai-gateway/usage/providers/`.
