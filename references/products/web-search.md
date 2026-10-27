# Web Search API — live web search for agents, through AI Gateway

> One call returns structured search results (URL, title, description) to ground a model in live
> information instead of guessing URLs or relying on its training cutoff. Runs **through AI Gateway**
> (logs, analytics, billing, access control). **Open beta** — launched 2026-10-02.

## Contents
- When to use (and when not)
- Binding & config
- Key API / access patterns
- Providers
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- An agent/app needs **current** web context (recent events, changing APIs, news) to put into a
  model's context — query in, normalized results out.
- You want search requests in the **same AI Gateway logs/analytics/billing** as your inference.
- You want to switch search backends (Ceramic.ai / Exa / Linkup) by changing one `provider` field.
- **Not** the same as **provider-native web search tools** (Anthropic `web_search_20250305`, OpenAI
  `web_search_preview`, xAI, Alibaba `enable_search`) or the Perplexity/Parallel proxies — those are
  AI Gateway's `ai-gateway/usage/web-search/` page, where the *model provider* runs the search
  → `products/ai-gateway.md`.
- **Not** for: fetching/rendering a known page (→ Browser Run), crawling your own site for RAG
  (→ AI Search).

## Binding & config (`wrangler.jsonc`)
Uses the existing **AI binding** — no new binding type:
```jsonc
{ "ai": { "binding": "AI" } }
```
```ts
const response = await env.AI.websearch({
  gatewayId: "default",            // required — the AI Gateway to route through
  query: "…",                      // required, 1–1,024 chars
  provider: "exa",                 // optional: ceramic (default) | exa | linkup
  limit: 5,                        // optional: 1–10, default 10
  // byokAlias: "default",         // optional: stored provider key alias
});
const results = await response.json();  // websearch() returns a standard Response
```

## Key API / access patterns
- **REST:** `POST https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/websearch/`
  Body: `query`, `provider`, `limit`, `byokAlias`, and a required **`options`** object holding
  `"gateway": { "id": "default" }` — REST nests the gateway, the binding uses top-level `gatewayId`.
- **Token permissions (both):** Account › **Workers AI** › Read **and** Account › **AI Gateway** › Read.
- **Response:** `{ "items": [{ "url", "title", "description", … }], "metadata": { "query",
  "requestId", "latencyMs" } }`. Each item may also carry image, favicon and last-modified date —
  optional fields appear only when the provider returns them.
- **Prerequisites:** an AI Gateway (every account has one named `default`) **and** either AI Gateway
  credits loaded or a provider key stored on the gateway.
- **As a model tool:** define a `web_search` function tool on `env.AI.run(...)`; when the model calls
  it, run `env.AI.websearch({ gatewayId, query: toolCall.arguments.query })` and send the JSON back
  as a `role: "tool"` message (docs example uses `@cf/google/gemma-4-26b-a4b-it`).

### Bring your own key (BYOK)
Dashboard: **AI Gateway** › your gateway › **Provider Keys** › add a Ceramic.ai/Exa/Linkup key with an
alias. Keys are never sent in the request; AI Gateway stores them encrypted with Secrets Store.
- **`byokAlias` set** → that stored key is used; if provider/alias isn't configured the request
  fails with **`400`** — it does **not** fall back to credits.
- **`byokAlias` omitted** → a stored key with alias `default` for that provider is used if present;
  otherwise the search bills your **AI Gateway credits**.

## Providers
| `provider` | Zero Data Retention | List price | Notes |
|---|---|---|---|
| `ceramic` (default) | Yes | $0.25 / 1,000 requests | Own index of 40B+ pages; low latency/cost; descriptions up to 8,000 chars |
| `exa` | **No** (per providers page) | $7.00 / 1,000 requests | Exa `auto` search type; page highlights returned as `description` |
| `linkup` | Yes | $5.00 / 1,000 requests | `fast` search depth, raw results (no generated answer) |

Every provider commits to Cloudflare's **verified bot** requirements (identify the crawler, respect
`robots.txt`) and returns a source link for every result.

## Gotchas
- **ZDR conflict in the docs:** the 2026-10-02 changelog says all three providers support Zero Data
  Retention for requests through Cloudflare; the providers page lists **Exa = No**. Trust the
  providers page and confirm before routing sensitive queries to `exa`.
- **Endpoint host:** it is `api.cloudflare.com/client/v4/accounts/{account_id}/ai/websearch/` — not
  a `gateway.ai.cloudflare.com` provider URL.
- **Default provider is Ceramic.ai** — omit `provider` and you get `ceramic`, not Exa.
- **Max 10 results** per request (default is also 10 — set `limit` lower to save context).
- **`byokAlias` is strict** — a typo is a `400`, not a silent switch to credits; omitting it can
  silently use a `default`-aliased stored key instead of credits.
- **Results are search snippets, not page content** — fetch/render pages separately if you need bodies.

## Pricing & limits
> ⚠️ Open beta — verify on the live providers page (`developers.cloudflare.com/web-search/providers/`)
> before quoting.
- **Cost driver: requests**, at each provider's **list API price with no Cloudflare markup**, drawn
  from your AI Gateway credit balance (Unified Billing) — or billed by the provider directly under BYOK.
- Prices above are per 1,000 requests (Ceramic $0.25 · Linkup $5.00 · Exa $7.00).
- **Limits:** query length **1,024** characters · **10** results per request.

## Going deeper
- Live docs (canonical): `https://developers.cloudflare.com/web-search/` — `how-to-use/`, `providers/`,
  `about/` (crawler standards). No official `cloudflare` skill ref exists — this file is primary.
- Gateway features it inherits (logging, Unified Billing, BYOK): `products/ai-gateway.md`.
- Running models next to it: `products/workers-ai.md`.
