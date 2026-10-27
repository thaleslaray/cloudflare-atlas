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
- **Resilience:** automatic **retries / fallback** across models or providers (dynamic routing).
- **Governance:** guardrails (content filtering) and DLP (PII detection) on prompts/responses.
- **Simpler keys:** Unified Billing (pay through Cloudflare, no provider key) or BYOK (store keys).
- **Not** a model host — that's Workers AI. AI Gateway sits *in front of* providers, including Workers AI.

## How to wire (change the base URL)
The whole product is "point your existing client at the gateway." Entry shapes:
- **REST API (preferred for single-model calls)** — base `https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai`,
  auth = Cloudflare API token with **Account → Workers AI → Read** (an AI-Gateway-only token returns `401`
  code `10000`). Endpoints: `/ai/run` (any model/modality), `/ai/v1/chat/completions`, `/ai/v1/responses`,
  `/ai/v1/messages` (Anthropic schema, **no `@cf/` models**). Third-party ids are `author/model`; `@cf/`
  models over REST also need `cf-aig-gateway-id`. Point the OpenAI SDK's `baseURL` at `…/ai/v1` with the
  Cloudflare token as `apiKey` — no provider key needed (billed via Unified Billing).
- **Unified / OpenAI-compatible** — `…/{gateway_id}/compat/chat/completions`, `model: "{provider}/{model}"`,
  `cf-aig-authorization: Bearer <token>` on authenticated gateways. **Deprecated for standard single-model
  chat completions** (still works for existing integrations) but **required for dynamic routing** —
  `model: "dynamic/{route}"` is only callable here.
- **Provider-specific** — `…/{gateway_id}/{provider}/{endpoint}` (keep the provider's own request shape).
- **Workers AI binding** — pass `{ gateway: { id: 'my-gateway', metadata: {...} } }` to `env.AI.run(...)`.
  **Since 2026-08-07 this is the unified path:** the same `env.AI` binding and the same REST `/ai/`
  endpoints (with Cloudflare auth) call **both** Workers AI models and supported third-party
  providers, with the gateway supplying observability, logging, caching, security and **billing
  controls**. Use `gateway: { id: 'default' }` to auto-create a gateway on the first authenticated
  request, or name one to separate apps/workloads.
- **Vercel AI SDK** — `ai-gateway-provider` pkg; pass a `gateway([modelA, modelB])` array for auto-fallback.

## Key features (controlled via `cf-aig-*` headers or dashboard)
- **Caching** — `cf-aig-cache-ttl` (60s–30d), `cf-aig-skip-cache`, `cf-aig-cache-key`; check
  `cf-aig-cache-status` (`HIT` or `MISS`). Cuts cost+latency on repeat prompts.
- **Rate limiting** — fixed or sliding window; returns `429` when exceeded.
- **Dynamic routing / fallback** — define routes, call `dynamic/{route}` via `/compat/chat/completions`.
- **Guardrails** — flag/block prompts+responses (`@cf/meta/llama-guard-3-8b` on Workers AI, billed as Workers AI tokens).
- **DLP** — **flag or block** (no redaction) PII/financial/health matches; free, shares Cloudflare One profiles.
- **Logging & analytics** — full request logs (prompt, tokens, cost, duration, metadata); Logpush export.
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
- CLI/agent clients: `cloudflared access curl`; per-agent setup in `ai-gateway/integrations/coding-agents/` (now incl.
  Gemini CLI — Access-protected custom domain — and VS Code / Xcode chat via a gateway custom domain).

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
  faster/cheaper model could serve — the same signals the Auto Router (`ai-gateway/features/auto-router/`) uses.

## Gotchas
- **Streaming responses are not cached by default**; caching covers text and image responses only.
- **Cache misses on param drift** — any body difference = different key; use `cf-aig-cache-key` to override.
- **Unified API needs the provider prefix:** `openai/gpt-4o`, NOT `gpt-4o`.
- **Rate limit is per-gateway, not per-user** — for per-user limits use dynamic routing.
- **Credential precedence, not a mix:** provider key on the request → BYOK `default` alias → Unified
  Billing. On Unified Billing paths (`env.AI.run()`, `/ai/v1/chat/completions`) only the `default`
  alias stops fall-through — a key under another alias is ignored and the call **silently bills credits**.
- **401 checklist:** Cloudflare token goes in `cf-aig-authorization` (not `Authorization`) · provider path or
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
- **Logpush** (Paid only): 10M requests/mo, then **$0.05/million**.

**Key limits:** cacheable request **25 MB** · cache TTL **1 month** · custom metadata **5/request** ·
gateways **10/account free, 20 paid** · gateway name **64 chars** · log storage rate **500 logs/s/gateway** ·
logs stored **100k/account free, 10M/gateway paid** · log size **10 MB/log** · datasets **10/gateway** ·
Unified Billing rate **200 req/60s/gateway** (`429`; BYOK exempt) · Logpush jobs **4/account**, **1 MB/log**.

## Going deeper
- Covered by the official `cloudflare` skill (`references/ai-gateway/`) — use it for full
  patterns: `sdk-integration.md` (Vercel/OpenAI/Workers), `configuration.md`, `features.md`,
  `dynamic-routing.md`, `troubleshooting.md`.
- Provider-specific quirks → `developers.cloudflare.com/ai-gateway/usage/providers/`.
