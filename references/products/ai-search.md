# AI Search — fully managed RAG pipeline (formerly AutoRAG)

> The **managed RAG answer**. Point it at your docs and it runs the *entire* pipeline for you:
> ingest → Markdown conversion → chunking → Workers AI embeddings → vector + keyword index →
> (optional) rerank → (optional) LLM generation. You don't hand-roll any of it.

## Contents
- When to use (and when not)
- The pipeline (what it replaces)
- Binding & config
- Wiring: search() vs chatCompletions()
- Per-tenant isolation
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You need **RAG over a corpus** (docs, support KB, policies, product content) and don't want to own
  embeddings/vector DB/chunking glue. AI Search is the zero-ops path.
- Data lives in **R2**, a **website** (crawl), or you **upload** files (built-in storage / Items API).
  R2 objects **without a filename extension** index only with an explicit supported `Content-Type`
  (2026-09-11); missing, malformed or `application/octet-stream` is skipped.
- Want a ready answer → `chatCompletions()`. Want raw chunks for your own UI/LLM → `search()`.
- **Not** for: real-time freshness (connected sources re-index on a cycle, not instantly); when you
  need full control of embeddings/chunking/index → hand-roll with **Vectorize** + **Workers AI**;
  simple generation with no retrieval → **Workers AI** directly.

## The pipeline (what it replaces)
Hand-rolling RAG means wiring: doc parsing → chunking → embeddings → Vectorize upserts → query embedding
→ vector search → (rerank) → prompt assembly → LLM. **AI Search does all of it.**
- **Indexing (async):** ingest → Workers AI Markdown conversion (incl. images via object-detection +
  vision-to-language) → chunk → embeddings → vector + BM25 index → storage. Connected sources auto
  re-index; uploads index on arrival.
- **Querying (sync):** optional query rewrite → embed query → vector search (+ optional BM25 →
  fusion) → optional cross-encoder rerank → retrieve chunks → (`chatCompletions` only) generate.

## Binding & config (`wrangler.jsonc`)
The `ai_search_namespaces` binding **replaces** the previous `env.AI.autorag()` API (changelog wording;
the old AutoRAG REST endpoints "will continue to be fully supported"). Use the dedicated bindings:
```jsonc
{
  // Bind one instance directly (deploy-time name, "default" namespace):
  "ai_search": [{ "binding": "MY_SEARCH", "instance_name": "my-docs" }],
  // OR bind a whole namespace (create/list/get/delete instances at runtime):
  "ai_search_namespaces": [{ "binding": "AI_SEARCH", "namespace": "default" }]
}
```
Instance binding → call methods directly: `env.MY_SEARCH.search(...)`.
Namespace binding → get a handle first: `env.AI_SEARCH.get("my-docs").search(...)`.
**If your code calls `create()` at runtime you MUST use `ai_search_namespaces`** — the single-instance
`ai_search` binding can't provision. Add `"remote": true` so `wrangler dev` proxies to the deployed
instance: **AI Search does not run locally**.
Also available: REST API, **Wrangler CLI** (instances, namespaces, sync jobs — e.g. `wrangler ai-search
jobs create <instance>` from CI/CD), public endpoint (hosted search UI/API), and MCP.

## Wiring: search() vs chatCompletions()
```typescript
const inst = env.AI_SEARCH.get("my-docs");

// Raw retrieval — returns scored chunks, no LLM (~fast). Build your own UI/answer.
const { search_query, chunks } = await inst.search({
  query: "How do I configure caching?",            // or messages: [{ role, content }]
  ai_search_options: { retrieval: { retrieval_type: "hybrid", max_num_results: 5 } },
});

// Full RAG — retrieves + generates an answer with a Workers AI model.
const res = await inst.chatCompletions({
  messages: [{ role: "user", content: "How do I configure caching?" }],
  model: "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  ai_search_options: {
    retrieval: { max_num_results: 5 },
    query_rewrite: { enabled: true },               // fix typos / vague input
    reranking: { enabled: true, model: "@cf/baai/bge-reranker-base" },
  },
});
```
Key `ai_search_options.retrieval`: `retrieval_type` (`vector`|`keyword`|`hybrid`; docs state **no** default
— hybrid requires keyword indexing enabled on the instance),
`match_threshold` (0–1, default 0.4), `max_num_results` (1–50, default 10), `filters`, `context_expansion`
(0–3, default 0), `fusion_method` (`rrf`|`max`), `keyword_match_mode` (`and`|`or`, default `and`),
`boost_by` (max 3 fields). Stream with `{ stream: true }` on `chatCompletions()`.

## Per-tenant isolation
- **Instance per tenant** (strongest isolation): namespace binding + `env.TENANTS.create({ id: \`tenant-${id}\` })`,
  then `.get(\`tenant-${id}\`).search(...)`. Separate storage + index per tenant; `.delete()` for offboarding.
  Namespace `chatCompletions()` fans out via `ai_search_options.instance_ids: [...]` (**max 10** per request).
- **Shared instance + metadata filter**: one instance, filter by folder/metadata at query time. Filters are
  MongoDB-style, keyed by field: `filters: { folder: { $gte: \`tenants/${id}/\`, $lt: \`tenants/${id}0\` } }`
  — a range pair is how you do "starts with" (`0` follows `/` in ASCII). Also `$eq/$ne/$gt/$lt/$lte/$in`.

## Public endpoints — serving search to real users (2026-08-06)
Everything here is **opt-in**; previous behaviour stays the default.
- **Public endpoint** — a URL a site/app queries directly with no auth in front. Default host is a
  generated name on `search.ai.cloudflare.com`.
- **Custom domain** — serve that same endpoint from a hostname in a zone you own
  (`https://search.example.com/search`).
- **Cloudflare Access in front of it** — once on your own domain. Agents authenticate with an Access
  **service token**; humans opening it in a browser sign in through your IdP. Use this to keep `/mcp`
  restricted to specific agents instead of anyone who finds the URL.
- **Namespace endpoint** — one URL fanning out across chosen instances, with `/search`,
  `/chat/completions` and `/mcp` paths:
  ```bash
  curl https://ns-<NAMESPACE_ENDPOINT_ID>.search.ai.cloudflare.com/search \
    -H "Content-Type: application/json" \
    -d '{"messages":[{"content":"...","role":"user"}],
         "ai_search_options":{"instance_ids":["docs","support"]}}'
  ```
- **`discover` parse type** for website data sources — starts at the source URL and collects pages
  from sitemaps **and** links found while crawling. This is the answer when a site has no complete
  `sitemap.xml` (see the crawl gotcha below).

## Gotchas
- **Not real-time.** Connected R2/website sources re-index on a cycle — don't expect sub-minute
  freshness. Built-in-storage uploads index on arrival.
- **File size cap 4 MB** — larger files "will not be indexed and will show up in the error logs". Supported
  list is broad (plain text + code + rich formats: .pdf .html .xml .docx .xlsx .ods/.odt .csv .numbers,
  images). **`.doc` is NOT supported** — only `.docx`.
- **`timestamp` metadata is a Unix timestamp in milliseconds**; "comparisons round down to seconds".
  The `or`-only-`eq` / no-nesting restriction belongs to the **legacy** AutoRAG filter format, not the current one.
- **Website crawl** only works on a domain "onboarded onto the same Cloudflare account", and Bot
  Management/WAF/Turnstile rules apply to the crawler — allowlist it (Bot Detection ID `122933950`;
  Radar id `cloudflare-ai-search`). No `sitemap.xml`? Use the `discover` parse type (sitemaps **and** links).
- **Similarity cache freshness:** cached answers expire per the instance's `cache_ttl` (default **48h**,
  configurable 10 min–6 days); `POST .../instances/{name}/purge_cache` clears them when content goes stale.
- **`create()` throws if the instance exists** — not idempotent. Guard it (`read()` in a try/except
  `NotFoundError`, or a plain try/catch) if the code path can run more than once.
- **`upload()` only queues the file.** Indexing runs in the background; poll `items.get(id).info()` while
  `status` is `queued`/`running` before the first query, or it searches an empty index.
- **Empty results?** Drop filters, lower `match_threshold` to ~0.1, confirm indexing finished.

## Pricing & limits
> ⚠️ Generally available (GA) as of 2026-10-01 — verify on the live page (`developers.cloudflare.com/ai-search/platform/limits-pricing/`).
- **AI Search is generally available (GA) and FREE** within plan limits. **Workers AI + AI Gateway bill
  separately** (embeddings, rerank, generation); storage/vector indexing/crawl are included (managed
  infra). Pricing announced ≥30 days before billing starts.

**Limits (Free / Paid):** instances per account **100 / 5,000** · files per instance **100K / 1M
(500K hybrid)** · max file size **4 MB** · queries/month **20K / unlimited** · pages crawled/day
**500 / unlimited** · custom metadata fields **5** · metadata value len **500 chars**. Verify live.

## Going deeper
- Official `cloudflare` skill ref — `references/ai-search/` (README, api/configuration/patterns/gotchas).
  Prefer it for full API — but it documents the **legacy** `env.AI.autorag()` binding; use `ai_search` /
  `ai_search_namespaces` (above) instead.
- Concepts: `pages/ai-search/concepts/how-ai-search-works/` · retrieval tuning:
  `pages/ai-search/configuration/retrieval/` (reranking, query-rewriting, cache, filtering).
- **From agent frameworks (2026-07-30):** `pages/ai-search/agent-sdks/` — **Agents SDK** (expose `search()`
  as a tool; `AIChatAgent` needs its class in `new_sqlite_classes`), **AI SDK** (`ai-search-provider`,
  requires `ai@^6`), **LangChain** (`CloudflareAISearchRetriever` in `langchain-cloudflare` — retrieves
  only; pair with the `cloudflare` Python SDK to provision, and the token needs **both** `AI Search:Edit`
  and `AI Search:Run`). These use an instance; provisioning still goes through the API/binding above.
