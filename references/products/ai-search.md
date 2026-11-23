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
- Data lives in **R2**, a **website** (crawl), a **D1 database** (beta, rows of a SQL query), or you
  **upload** files (built-in storage / Items API).
  R2 objects **without a filename extension** index only with an explicit supported `Content-Type`
  (2026-09-11); missing, malformed or `application/octet-stream` is skipped.
- Want a ready answer → `chatCompletions()`. Want raw chunks for your own UI/LLM → `search()`.
- **Not** for: real-time freshness (connected sources sync on a schedule, 24 h default); when you
  need full control of embeddings/chunking/index → hand-roll with **Vectorize** + **Workers AI**;
  simple generation with no retrieval → **Workers AI** directly.

## The pipeline (what it replaces)
Hand-rolling RAG means wiring: doc parsing → chunking → embeddings → Vectorize upserts → query embedding
→ vector search → (rerank) → prompt assembly → LLM. **AI Search does all of it.**
- **Indexing (async):** ingest → Workers AI Markdown conversion (incl. images via object-detection +
  vision-to-language) → chunk → embeddings → vector + BM25 index → storage. Connected sources sync
  on a schedule; uploads index on arrival.
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

## Namespaces (2026-11-13 doc subtree `api/namespaces/`)
Every instance belongs to a **namespace** (logical grouping; instance name unique *within* it). A `default`
namespace exists on every account; its description can't be changed, its public endpoint can; it can't be deleted.
- **REST** `/accounts/{id}/ai-search/namespaces[/{name}]` (token needs **AI Search:Edit** + **AI Search:Run**):
  `POST` create · `GET` list (`per_page` default 20, max 100; `search`) · `GET` one · `PUT` update (`description`
  ≤256 chars, `public_endpoint_params`) · `DELETE` (only if empty: error `7066`; `default`: `7065`) ·
  `PATCH .../namespaces/<ns>/instances/<name>` with `{ "new_namespace": ... }` moves an instance.
  `name` = 1–28 lowercase letters/digits/hyphens, start+end alphanumeric, **not renameable**. 100 namespaces max (`7062`).
- Binding needs `@cloudflare/workers-types` ≥ `4.20260304.0` and `wrangler` ≥ `4.68.1`. `get()` is synchronous
  (no network call; resolved on first `search()`). `ai_search` (single instance) has no namespace-level calls (list, create, delete).
- **Terraform** (provider ≥ **v5.29.0** for namespaces on instances): resources `cloudflare_ai_search_namespace`
  (changing `name`/`account_id` replaces it) and `cloudflare_ai_search_instance` (`id` = instance name, `namespace`,
  `type` `r2`|`web-crawler`, `source`); data sources `cloudflare_ai_search_namespace(s)` / `cloudflare_ai_search_instance(s)`.
  **Changing `id`, `account_id`, `namespace` or `type` replaces the instance and wipes its index** (check `must be replaced`).
  Import ids: `<account_id>/<namespace>/<id>` (instance), `<account_id>/<name>` (namespace). Models, `chunk_size`, `token_id` are computed.

## D1 data source (beta, 2026-11-12) — `configuration/data-source/d1/`
Runs **your read-only query** and indexes **each row as one Markdown document**. Create with `type: "d1"`,
`source: <D1 database id>`, `source_params.d1: { query, template }`; `token_id` of a **service API token** is **always
required** (its AI Search Index Engine permission includes D1 Read). Validated at create (bad query → no instance).
- Query: one `SELECT`/`WITH`; **no** `;` `--` `/*`, bound params, `ORDER BY`/`LIMIT`, write keywords, `sqlite_`/`_cf_`/`pragma_`
  names — rejected even inside string literals (so `replace()` fails). Must return unique non-null `id` (all text or all
  integers) and 1–100,000 rows. Columns: `title`, `content`, `meta_<name>` (≤5, becomes custom metadata; number|text)
  and others as labeled fields. `template` (example value `"labelled"`; dashboard offers Labelled, Content only, Key-value, JSON).
- Sync reads the full result ≥2× with your token (counts toward D1 **rows read**); rows no longer returned are deleted,
  but a failed/empty query keeps items. `source` can't change later; a `source_params` object on update replaces
  `include_items`/`exclude_items` (resend them). Limits: query 10,000 chars · `id` 512 bytes · rendered doc 64 KiB/row · metadata value 500 chars.

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
- **Not real-time.** R2/website sources sync on a schedule, **every 24 h by default** (was 6 h; changed
  2026-11-02). `sync_interval` (seconds): `900, 1800, 3600, 7200, 14400, 21600, 43200, 86400`. Trigger now:
  `wrangler ai-search jobs create <instance>` (at most once per 30 s). Built-in-storage uploads index
  immediately. No search for 31 days → scheduled syncs auto-pause (still searchable, source changes not
  picked up until traffic resumes or **Resume indexing**). → `ai-search/configuration/indexing/syncing/`
- **File size caps (not a flat 4 MB):** PDF with OCR / plain text & code **10 MiB**; PDF without OCR and other
  rich formats **4 MiB**. Larger files "are not indexed" (error logs). Rich formats: .pdf .html .xml .docx .xlsx
  .xls .ods/.odt .csv .numbers, images. **`.doc` is not in the supported list** — only `.docx`.
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
- **GA, but billing starts 2026-12-01** (postponed from 2026-11-01; "not charged before December 1, 2026";
  rates and included usage unchanged — changelog 2026-11-02). Until then usage is not billed.
- **Included monthly, every account:** 5M ingestion tokens · 10 GB-month storage · 1,000 semantic + 1,000 full-text queries.
- **Beyond that:** ingestion **$0.75/M tokens** (+**$0.50/M** image processing; `cl100k_base` counted on
  final chunks, overlap counted) · storage **$2.00/GB-month** · semantic/vector/hybrid **$0.75/1K queries** ·
  full-text **$0.10/1K** · instances past 5,000 **$0.10/month** each.
- Workers AI **embedding + reranking are included** in AI Search usage (not on your Workers AI bill/AI Gateway
  logs); **generation, query rewriting and external providers** still bill via your account/gateway.
  Storage, vector indexing and crawl (`Browser Run`) usage are included.

**Limits (Free / Paid):** instances **100 / 5,000 default** (counted across all namespaces; namespaces carry no charge) ·
namespaces **100** · files per instance **100K / 1M (500K hybrid)** · pages per `discover` crawl **100,000** ·
pages crawled/day **500 / unlimited** · instances per cross-instance search **10** ·
custom metadata fields **5** · metadata per vector **10 KiB** · file sizes as in Gotchas. Verify live.

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
