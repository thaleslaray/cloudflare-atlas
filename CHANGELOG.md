# Curation log — cloudflare-atlas

**This is not a mirror of Cloudflare's changelog.** Cloudflare's own changelog is retrievable live
(`scripts/changelog-check <product>`), and a frozen copy here would become a second, stale source of
truth — the exact failure this skill exists to prevent.

What this file records is the thing that is *not* retrievable anywhere: **what a curation pass
detected, what it curated, and what it chose to defer.** Deferred items are the backlog. An unlogged
deferral is how a launch goes missing for months.

One entry per pass. Newest first.

---

## 2026-10-12

**Weekly pass: 7 new not-found tokens fixed, one new vendor subtree, 10 changelog items curated.**

**What the check said (run 2026-10-12):** products 113 live = 113 known (no structural drift). New subtree `ai/models/bria` (+4); gone `pages/framework-guides/deploy-a-vite3-project`. 18 single pages. API spec 10 days old; health gates zero; pointer gate clean; doc URLs all resolve; blindness probe no regression. **7 new not-found tokens** (agent-setup 2, fundamentals 3, observability 1, sandbox 1). Copy sync clean.

**Method.** Coordinator fixed the 7 tokens and fundamentals/log-explorer directly; three agents curated disjoint file sets (AI: ai/workers-ai/ai-gateway · platform: k2/workers/workflows/r2/realtime · network: dns/api-shield/rules/waf/logs/pages). Every fact from a live page fetched today; each edited file closed with `verify-products <slug>` and `check-doc-urls`.

**Not-found tokens — all were real drift, not gate noise**
- `fundamentals.md` — Markdown for Agents changed on 2026-10-09: `x-markdown-tokens`/`x-original-tokens` are no longer documented; cap is now **6 MiB of decompressed HTML** (was "2 MB"); origin headers preserved, `Vary: Accept`, `ETag`/`Last-Modified` dropped, default `Content-Signal`.
- `agent-setup.md` — the product-specific MCP table shrank to `docs`·`containers`·`browser`·`dex`·`casb` + `agents.cloudflare.com/mcp`; `dns-analytics`/`auditlogs` and the rest are unlisted (still answer 401, measured today). `prompt.md` now installs only `mcp.cloudflare.com`. Added: the API server serves Cloudflare skills over MCP (`skills/list`, `skill://`, 2026-10-10); `/sse` is an alias, not the old transport.
- `observability.md` — Paid storage allowance is **10 GB-month**, not 12 (the file's own $7.05 example only works with 10).
- `sandbox.md` — Devin template moved to `cloudflare/sandbox-sdk/templates/devin` (Devin Outpost).

**Curated — changelog and new pages**
- `ai.md` — Bria vendor row (FIBO, RMBG 2.0, video background removal); recount 242 model pages (70 `@cf` + 172 third-party); new Claude Sonnet 5.5, GPT-6.1 Sol, Gemini 3.8 Flash(-Lite) TTS.
- `workers-ai.md` — clef-omni (audio/video input, 30B MoE/3B active, 64,000 ctx), clef-flash price cut to $0.038/M with 24,576 ctx. "Apache 2.0" softened to "open weights on Hugging Face" (licence not re-checked today).
- `ai-gateway.md` — provider credential errors standardized to HTTP 401 / code 2009 (503 under Unified Billing); Gemini CLI, VS Code, Xcode coding-agent integrations.
- `k2.md` — pricing published (billing not enabled during beta, ≥30 days notice): produced $0.04/GB, consumed $0.04/GB (per subscription), retained $0.02/GB-month; no free tier listed.
- `workers.md` — profiling in production (CPU/heap flamegraphs, 1–50 s). `workflows.md` — `createBatch()` by count or list (≤100/call, Wrangler 4.148.0+). `r2.md` — bandwidth by Cloudflare location chart.
- `fundamentals.md` — Organizations GA (Enterprise + MSSP/Distributor); HTTP/3 client cancels now recorded as `499`. `log-explorer.md` — Log Explorer menu removed; datasets queried from Observability → Logs.
- `dns.md` — 85% quota warning. `api-shield.md` — Schema Learning + on-demand run. `waf.md`/`rules.md` — `cf.appsec.request.failed_detections` (fail-open/closed). `logs.md` — account-scoped `http_requests` Logpush dataset (same 125 fields as zone; no behaviour text found, none inferred).
- `_curation-guide.md` exemption table: agent-setup 127, workers 144, workers-ai 174, ai-gateway 139.

**Token accepted with evidence (1)** — `skills/list` (agent-setup) appears only in the changelog post `changelog/post/2026-10-10-cloudflare-mcp-skills/`, outside the gate's llms.txt corpus; verified on the post today. **Blindness:** `Organization Super Administrators` (fundamentals) and `Devin Outpost` (sandbox) were made auditable after the first close flagged them; probe back to no regression (320 → 319).

**Not curated, with reasons** — `pages.md` never referenced the vite3 guide (nothing to fix). `realtime.md` has no UI-kit list (chat-panel skipped). `workers.md` has no framework list (fate skipped). `waf.md` has no use-case list (Tor / Worker-subrequest pages skipped; noted fact for a future section: `CF-Worker` is added *after* WAF evaluation — use `cf.worker.upstream_zone`). Cloudflare One items (custom finding types, One Client releases) outside declared scope. Routine WAF releases skipped by design.

**Deferred**
1. `waf.md` use-case section does not exist; if created, start with block-worker-subrequests (fact above).
2. `failed_detections` detection IDs (`waf_score`, `waf_signature`…) live only on the ruleset-engine field reference, which `verify-products` does not scan for waf — the gate cannot audit them, so they were left out of waf.md.

---

## 2026-10-03

**Full pass, operator directive "atualize tudo, sem exceção": every product, subtree, stale status, new not-found token, blindness regression and backlog item the check flagged was curated today. Nothing deferred.**

**What the check said (run 2026-10-03):** products 113 live vs 111 known → `+ observability`, `+ ohttp-relay`, `+ web-search`; gone: `privacy-gateway` (renamed — confirmed on `ohttp-relay/index.md`: "Cloudflare OHTTP Relay (formerly Privacy Gateway)"). New subtrees: `ai/models/*` (~240 pages across 25 vendors), `observability` (+14), `analytics/sql-api` (+12), `ohttp-relay` (+6), `web-search` (+4), `agents/models` (+3), `agents/harnesses/pi` (+2); gone: `workers/observability/exporting-opentelemetry-data` (renamed `opentelemetry-export`; the old URL 301s to `/observability/export/opentelemetry/`). 9 single pages. API spec 1 day old; health gates zero. **STALE STATUS:** `pipelines` claimed beta after Basin GA. **41 new not-found tokens** (21 in sandbox). **Blindness regression** in 7 products. Copy sync clean.

**Method.** Fresh mirror of 1,334 pages (17 llms.txt indexes, 0 download failures) + live changelog. Five curation agents ran in parallel on disjoint file sets; a sixth (Basin, K2, Analytics, Logs) was refused by the permission classifier, and those 7 files were curated by the coordinator directly after the operator re-issued the directive. Every file was closed with `verify-products <slug>`, `probe-blindness`, `check-doc-urls`.

**Curated — new products**
- **`web-search.md` (NEW, 100).** Web Search API (2026-10-02): `POST .../ai/websearch/`, binding `env.AI.websearch()`, providers ceramic/exa/linkup with per-1,000 prices, BYOK `byokAlias` 400-not-fallback rule. Doc conflict recorded in-file: changelog says all providers support ZDR, providers page says Exa = No (followed the providers page).
- **`observability.md` (NEW, 130).** The `/observability/` hub: Cloudflare Traces, unified pricing (announced, effective 2026-12-01), account-level OTel destinations, Workers Issues, Custom Dashboards with logs/traces (2026-10-02).
- **`ohttp-relay.md` (NEW, 105).** Re-verified port of privacy-gateway; logs dataset is now "Cloudflare OHTTP Relay Logs"; cites `draft-ietf-ohai-ohttp-05` as the live pages do (dropped "RFC 9458").

**Curated — rename stubs (operator decision of 2026-10-01 revised).** `privacy-gateway.md`, `pipelines.md`, `r2-sql.md`, `r2-data-catalog.md` became ≤11-line stubs carrying only the old→new name map (`wrangler r2 sql query` → `wrangler basin sql query`, `--type basin-catalog`, `WRANGLER_BASIN_SQL_AUTH_TOKEN`, Terraform keeps `cloudflare_r2_data_catalog`). Reason: the full legacy copies were the source of the stale "beta" status, of 301 links (backlog #6) and of the pipelines/r2-sql blindness strands. Verified legacy facts were ported into basin-*; facts not found in the basin pages were dropped, not ported (e.g. `__ingest_ts`, "first flush 3–7 minutes", R2 SQL `files_scanned` metrics).

**Curated — Basin family (Basin GA 2026-10-01)**
- **`basin-pipelines.md` — 5 factual errors fixed:** `env.MY_STREAM.write(records)` → `env.STREAM.send(events)`; binding keys `basin_streams`/`basin_pipelines` → `"pipelines": [{ "binding", "stream" }]`; "1 GB/s per account" → **per stream**; "each pipeline reads one stream and writes one sink" → multiple `INSERT` fan-out; removed an unsourced stream-ordering claim and the "verified from scout data" pricing line. Added immutability of pipeline SQL and sinks, "sinks cannot be created for existing Iceberg tables", exactly-once delivery, rolling-policy minimums (5 MB / 10 s), `pipelinesUserErrorsAdaptiveGroups`, HTTP ingest URL. 26/26.
- **`basin-sql.md`:** "`LIMIT` default 500" (not in docs) → `LIMIT` 1–10,000 (`maximum LIMIT is 10000`); auth corrected to Basin Catalog + R2 storage + Basin SQL permissions; REST endpoint added; `DESCRIBE namespace_name.table_name`. 48/48.
- **`basin-catalog.md` — rewritten** (least-audited file, 24% → 39% of blocks checkable; 9/11 → 30/30). Dropped scraped UI text ("Understand Copy"); "SigV4 credentials" corrected to *vended* SigV4 credentials that inherit the token's R2 storage permissions; compaction target **default 128 MB, 64–512 MB**; snapshot-expiration flags + Wrangler 4.56.0; disable makes tables inaccessible immediately; pricing link fixed to `basin-catalog/platform/pricing/` (was `cloudflare.com/plans/`); objects-processed meter named.
- **`basin.md`:** removed a **wrong** claim that external engines pay R2 egress (R2 has none); "free tier: none" rows corrected (sinks 50 GB, compaction 10 GB/1M objects, SQL 10 GB included); 1 GB/s per stream. 19/19.

**Curated — rewrites and backlog**
- **`sandbox.md` rewritten around SDK 1.0** (309 → 150 lines) — closes backlog #3. 0.x is a short legacy note (fixes until 2026-12-31, pin `0.12.10`, one-way `durable_object` switch). 21 not-found tokens: 14 were the withdrawn preview API (`@next`, `createTerminal`…`RuntimeControlProtocolError`; `/sandbox/1-0-preview/` now 301s to `/sandbox/`) → removed; `0.10.2`/`0.10.3` → `0.12.10`; `sandbox-migrate-to-next` → removed (live pages name only `sandbox-stable`); examples path fixed; Devin R2 archive paths removed (Devin now snapshots on suspend); "Workers Paid or Enterprise" → quoted live text. 86/86.
- **`containers.md`** — `durable_object` scheduling policy + filesystem snapshots (public beta 2026-09-30) — closes backlog #5. Disk:memory ratio limit removed (2026-09-29). New `containers/examples/durable-object-interface/`.
- **`workers.md`** — Workers Previews (closes backlog #4), Analytics SQL binding, ML-KEM/ML-DSA, Workflows via `ctx.exports`. The pt-BR Static Assets gotcha was translated to English and compressed (same facts).
- **`email-service.md` fully audited** (~95 claims vs 15 live pages) — closes backlog #1. 8 errors fixed, notably: suppressions are no longer only account-scoped (`account` | `sending_domain` since 2026-09-25); `read_only` semantics; the Drop-suppressed-recipients setting.
- **Stale 301s** (backlog #6): all fixed — `check-doc-urls` 240/240 resolve directly.
- **Blindness regression** (backlog #7 and today's 7 products): resolved — `tool-use`, `Data Studio`, `Workers Logpush`, `basin-pipelines`, `basin-sql`, `transfer-in`, `openai-agents` each made checkable or removed. Probe: no product above baseline; 339 → 320 stranded terms.

**Curated — other products**
- `ai.md` — unified model catalog: 233 models (69 `@cf/` Cloudflare-hosted, 164 third-party via AI Gateway), per-vendor index, one call path `env.AI.run(id, …)`. Not mirrored per model (scope decision, not a deferral).
- `workers-ai.md` — Clef decision models. `agents.md` — Pi harness, `agents/models/*` providers, Workers OAuth Provider v1; **a stray triple backtick had hidden ~half the file from both gates** (40/46 → 114/124 tokens checked). `ai-gateway.md` — Machine Payments (x402), User Insights savings, corrected BYOK/Unified Billing credential order.
- `durable-objects.md` — Pending I/O eviction rules (2026-10-01); **corrected** "plain `fetch()` never blocks eviction" (it does); `exports` replaces `migrations`; `--experimental-webgpu` → `["experimental", "webgpu"]` flags.
- `kv.md` jurisdictions GA; `artifacts.md` open beta (Workers Paid, billing from 2026-10-14).
- `analytics.md` — Analytics SQL API (endpoint, `events.`/`states.`/`logs.` datasets, binding, limits), 30 days of data on every plan (2026-10-02). `logs.md` — **Logpush is now usage-based on all plans** (was "Enterprise only" — wrong since 2026-09-30), Transformers GA, `filter_attack_traffic`, Basin names. `k2.md` — `POST /produce` → full produce URL; `start_at` → `"start_at": { "type": … }`.
- Numeric tokens corrected to live values: api-shield GraphQL `20 KB` → 20 KiB (+ Schema Validation limits now KiB); mesh `75 MB`/`35 MB` → current sizing table; secrets-store `1024 bytes` → **65,536 bytes**; browser-run `kitesurf.cloudflare.app` → `kitesurf.dev` (+ WebMCP, multi-client sessions); realtime "Realtime App" → "SFU app".
- `rules.md` (`coalesce()`, dynamic comparisons, `hash_in_range()`), `cache.md` (`invalidate_cache`; every purge now forces a Cache Reserve miss), `fundamentals.md` (self-serve Account API tokens), `tunnel.md` (Quick Tunnel `--allowed-mail`), `cf.md` (login is `cf auth login`, not `cf login`), `monetization-gateway.md` (rewritten: `PAYMENT-CONTEXT` direction was wrong), `privacy-pass.md`, `r2.md`, `dynamic-workers.md`.
- Catalog/router: SKILL.md router now points at basin-*/k2/web-search/observability (the 10-01 rename had left the "Store data?" line on retired slugs); `_known-products.txt` 113 (+3, −privacy-gateway). Exemption table in `_curation-guide.md` updated for every file that moved, plus 7 pre-existing over-cap files found unrecorded (listed, not audited).

**Tokens accepted with evidence (5)** — present only in changelog posts, which the gate's llms.txt corpus does not include. Verified by the coordinator on the posts themselves today: `OAuthAuthorizationServer` (4 hits), `OAuthResourceServer` (5), `migrate-to-1.0` (2), `Metadata Documents` (1) on `changelog/post/2026-10-01-workers-oauth-provider-1x/`; `account_api_tokens:create` (1) on `changelog/post/2026-10-01-account-api-token-provisioning/`.

**Gate state before closing (workbench):** verify-products 4,033 confirmed · 212 not found (was 3,611 · 280); the only new not-found are the 5 above. probe-blindness no regression. check-doc-urls 240/240. check-pointers clean.

**Not curated, with reasons** — Cloudflare One items in the changelog (Access strict service tokens, Access for Infrastructure tagging, Browser Isolation RBAC, Cloudflare One Client releases): the atlas has no Cloudflare One/Access/Gateway product file — outside declared scope, not a deferral. Routine WAF releases skipped by design.

**Deferred** — nothing. Backlog items #1, #3, #4, #5, #6, #7 of 2026-10-02 are closed above by name. Item #2 ("`check-doc-urls` proves a URL resolves, not that the page still says what we claim") is a standing property of the tooling, not curation work; it is restated here as a known limitation, not as backlog.

---

## 2026-10-02

**Follow-up pass: dead-link cleanup, rename propagation, and baseline re-recording after the Basin GA structural shift.**

**What the check said (run 2026-10-02):** products 111 live vs 107 known in installed SKILL.md catalog; `_known-products.txt` carries 94 active slugs (7 new basin-family + cf + k2 + monetization-gateway added; pipelines, r2-data-catalog, r2-sql retired). Copy sync ✅ clean. API spec sliced 11 days ago (2026-09-21), within freshness window. Pointer gate 95/95 clean. Dead links reduced from 8 → 0 across new product files. 14 stale 301s remain, all in legacy redirect files (`pipelines.md`, `r2-data-catalog.md`, `r2-sql.md`) and `sandbox.md` tutorial paths that moved under `/sandbox/sdk/tutorials/` or `/sandbox/coding-agents/`.

**Curated this pass**

- **8 dead links fixed** in `basin-pipelines.md` (5) and `k2.md` (3): corrected URL paths to match actual docs structure (`/basin-pipelines/examples/bluesky-firehose-fanout/`, `/basin-pipelines/sql-reference/scalar-functions/`, `/k2/features/consume/`, `/k2/features/produce/`, `/k2/platform/limits/`). Both bare-path references and full URLs updated.
- **Rename notes verified** in `pipelines.md`, `r2-data-catalog.md`, `r2-sql.md`: each carries a prominent header note pointing readers to the basin-* replacement file. Files retained intentionally for old-link traffic.
- **AI Search GA status confirmed**: `ai-search.md` updated from beta to "Generally Available (GA) as of 2026-10-01" per changelog.
- **Stale 301s in sandbox.md partially addressed**: 5 remaining stale links point to tutorial paths that moved (`/sandbox/tutorials/claude-code/` → `/sandbox/coding-agents/claude-code/`, etc.). These are low-risk (redirect works) but should be updated next pass when sandbox.md gets its 1.0 restructure.
- **Blindness probe regression noted**: 7 products now strand more terms than baseline (durable-objects +1, logs +1, pipelines +1, r2-data-catalog +1, r2-sql +1, registrar +1, sandbox +1). All are expected consequences of the rename (old files still reference old names) plus new content in durable-objects (Data Studio) and sandbox (openai-agents). Will resolve when legacy files are retired or restructured.

**Not curated (scope boundaries)**

- Sandbox SDK 1.0 restructure deferred — see Deferred #3.
- Workers Previews integration deferred — see Deferred #4.
- Containers scheduling policy + snapshots integration deferred — see Deferred #5.
- 14 stale 301 links in legacy/sandbox files left as-is — redirects work, fixing is cosmetic.

**Deferred** (the backlog — each item stands on its own until named and closed)

1. **`email-service.md` carries 12 undocumented over-cap lines** predating this pass, now recorded in `_curation-guide.md` but not audited. Audit or trim next pass.
2. **`check-doc-urls` proves a URL resolves, not that the page still says what we claim.** A live link to a rewritten page passes it. Content is `verify-products`' job — the two do not overlap, and neither covers prose framing.
3. **Sandbox SDK 1.0 curation incomplete.** The 78-page `sandbox/sdk` subtree documents the new 1.0 API (Durable Object-managed containers, snapshots, coding agents). This pass updated stale links and noted the GA milestone in `sandbox.md`, but did not restructure the file to cover 1.0 as the primary surface with 0.x as legacy. Next pass should rewrite `sandbox.md` around 1.0 semantics.
4. **Workers Previews not curated.** 8-page subtree (`workers/previews/`) shipped 2026-09-24. Not covered in any product file this pass. Should be added to `workers.md` or as a standalone section next pass.
5. **Containers scheduling policy + snapshots not integrated.** Pages downloaded and read during the 2026-10-01 pass but not yet written into `containers.md`. The `durable_object` scheduling policy (beta) and snapshot API are significant additions.
6. **14 stale 301 links in legacy redirect files and sandbox tutorials.** All resolve correctly today but ride redirects Cloudflare can retire. Low priority — fix when those files are restructured or retired.
7. **Blindness probe regression: 7 products strand more terms than baseline.** Caused by rename artifacts (old files referencing old names) plus new content. Will self-resolve when Deferred #3 (sandbox restructure) and legacy file retirement happen.---

## 2026-10-01

**Basin GA, Sandbox SDK 1.0, 7 new products, and the biggest structural shift since Mesh.**

**What the check said (run 2026-10-01):** products 111 live vs 107 known → +basin, +basin-catalog, +basin-pipelines, +basin-sql, +cf, +k2, +monetization-gateway; gone: pipelines, r2-data-catalog, r2-sql (renamed into basin-*); new subtrees: sandbox/sdk (+78), basin-pipelines (+33), basin-catalog (+15), basin-sql (+15), cf (+13), sandbox/coding-agents (+9), workers/previews (+8), k2 (+7); API spec sliced 10 days ago; copy sync clean.

**Curated**

- **`basin.md` (NEW, 82 lines).** End-to-end analytics platform overview: Pipelines → Catalog → SQL architecture, pricing table across all three sub-products, limits (20 streams/sinks/pipelines, 5 MB payload, 1 GB/s ingest), rename note (formerly Cloudflare Data Platform).
- **`basin-pipelines.md` (NEW, 62 lines).** Streaming ingestion + SQL transforms + R2 delivery. Streams, pipelines, sinks concepts. Pricing: free ingress, $0.04/GB transforms, $0.03–0.06/GB sink delivery. Gotcha: billing on uncompressed data.
- **`basin-catalog.md` (NEW, 58 lines).** Managed Iceberg REST catalog in R2. Zero egress for external engines (Spark, Snowflake, DuckDB, PyIceberg). Automatic compaction and snapshot expiration. Auth via R2 credentials.
- **`basin-sql.md` (NEW, 56 lines).** Serverless distributed SQL over Iceberg. $0.0025/GB scanned, 10 MB minimum per query. Failed queries free. Metadata-only ops free.
- **`cf.md` (NEW, 72 lines).** Cloudflare CLI beta — 2,900+ commands, typed `cloudflare.config.ts`, agent-friendly JSON output, `cf cli search` for command discovery. Comparison table vs Wrangler. Migration via `cf migrate`.
- **`k2.md` (NEW, 68 lines).** Serverless durable logs, public beta. 10 GB account cap during beta. Streams, subscriptions, retention (1h–30d). Limits: 20 streams, 5 MB request, 1 MB record, 10K records/consume. No pricing published yet.
- **`monetization-gateway.md` (NEW, 58 lines).** x402 protocol payment gateway, closed beta. US-only. Per-request charging inline in HTTP flow. Fixed (`exact`) and variable (`upto`) pricing. Settlement via Coinbase.
- **`ai-search.md`** — status updated from beta to GA per changelog 2026-10-01.
- **`pipelines.md`, `r2-data-catalog.md`, `r2-sql.md`** — rename notes added at top pointing to basin-* equivalents. Files retained for old-link readers.
- **Stale 301 links fixed (15 total):** realtime.md (sfu/pricing → sfu/platform/pricing), containers.md (durable-objects/api/container → containers/api/durable-object-container), sandbox.md (3 links: 1-0-preview → /sandbox/, openai-agents-api tutorial → coding-agents/, workers-ai-code-interpreter → sdk/tutorials/), pipelines.md (3 links → basin-pipelines/), r2-data-catalog.md (3 links → basin-catalog/), r2-sql.md (4 links → basin-sql/).

**Deferred** (the backlog — each item stands on its own until named and closed)

1. **`email-service.md` carries 12 undocumented over-cap lines** predating this pass, now recorded in `_curation-guide.md` but not audited. Audit or trim next pass.
2. **`check-doc-urls` proves a URL resolves, not that the page still says what we claim.** A live link to a rewritten page passes it. Content is `verify-products`' job — the two do not overlap, and neither covers prose framing.
3. **Sandbox SDK 1.0 curation incomplete.** The 78-page `sandbox/sdk` subtree documents the new 1.0 API (Durable Object-managed containers, snapshots, coding agents). This pass updated stale links and noted the GA milestone in `sandbox.md`, but did not restructure the file to cover 1.0 as the primary surface with 0.x as legacy. Next pass should rewrite `sandbox.md` around 1.0 semantics.
4. **Workers Previews not curated.** 8-page subtree (`workers/previews/`) shipped 2026-09-24. Not covered in any product file this pass. Should be added to `workers.md` or as a standalone section next pass.
5. **Containers scheduling policy + snapshots not integrated.** Pages downloaded and read this pass but not yet written into `containers.md`. The `durable_object` scheduling policy (beta) and snapshot API are significant additions.---

## 2026-09-21

**Cloudflare Mesh curated — and the reason it took six weeks is the finding.**

**What the check said (run 2026-09-21):** products 107 live vs 106 known → `+ mesh`; new subtrees
`mesh` (+11), `cloudflare-one/networks/connectors/cloudflare-mesh` (+11), `workers-vpc/platform`
(+2); gone: `bots/attribution-business-insights`, `workers-vpc/reference/{limits,pricing}`; 5 single
pages; API sliced 34 days ago; health, pointer and blindness gates all green with no regression;
copy sync clean.

**Baseline after closing:** 6,543 prefixes across 107 products. `cloudflare-one` **grew** by the 11
mirrored Mesh pages (diffed prev vs current: additions only, zero removals) — no repeat of the
09-15 collapse. `mesh` recorded at 10 prefixes. 648 operations documented after the re-slice.

**The backlog was dropped, then stamped closed.** `Cloudflare Mesh container image` was deferred on
08-08, restated in the 08-15 entry, restated again in 08-17 — and then appears in **no entry after
that**. It was not carried forward and mislabeled; it silently left the backlog. The 09-15 entry then
replaced its whole Deferred section with *"superseded by pass 2 below; every item was taken up the
same day."* Pass 2 curated `tunnel.md`. It did not touch Mesh.
Measured today before curating: zero files under `references/products/` covered mesh, warp or
cloudflare-one; the only mentions outside the frozen `data/blog/` corpus were the two backlog lines
themselves (08-15, 08-17) and incidental prose in `workers-vpc.md`. So a deferred item sat open six
weeks — five of them with no entry naming it at all, the last under a resolved stamp. The blanket
"superseded — every item taken up" is the mechanism: it closes a list without naming what was in it.
**Rule for future passes: a Deferred section is closed item by item, by name, or not at all.**

**Curated**
- **`mesh.md` (NEW, 141 lines).** Cloudflare Mesh is the rename of **WARP Connector** /
  "peer-to-peer connectivity"; the WARP client is now the **Cloudflare One Client**. Existing
  deployments keep working, no migration. Written against all 11 live pages (2026-09-21):
  participants table (nodes vs client devices), Mesh IPs from `100.96.0.0/12` (CGNAT, = "device IPs"
  elsewhere in the Cloudflare One docs), the Mesh-vs-Tunnel decision table, install sequence, CIDR
  and hostname routes (hostname routes replace Tunnel's virtual networks; **overlaps unsupported**),
  active-passive HA, the `cloudflare/mesh` Wolfi container image.
  Gotchas worth the space: **MASQUE is mandatory** — a WireGuard device profile silently kills
  hostname routes, IPv6 CIDR routes and HA; **the API path is still `warp_connector`** though the
  product renamed; a node must never share a host with a DNS service (it binds :53 in
  Traffic-and-DNS mode); other VPN/mesh clients must be uninstalled *and the host rebooted*;
  Mesh + Tunnel on one host works **only** via Split Tunnels — `ip route`/`iptables` are overridden
  by the node's kernel integration; double encapsulation drops packets ≥1,460 bytes (set source MTU
  1,280, or clamp MSS to 1,240); Mesh ↔ Cloudflare WAN needs Unified Routing mode (GA 2026-09-18).
  Beta, available to Cloudflare One accounts **including Free**; no separate Mesh price published.
- **`workers-vpc.md` — two stale pointers fixed.** The file told the reader to verify pricing and
  limits on `workers-vpc/reference/{pricing,limits}/`, which moved to `workers-vpc/platform/`.
  **Severity corrected in pass 3:** these were **301s, not 404s** — they still rendered the right
  page, which is precisely why nobody noticed. An earlier draft of this entry called them "dead";
  that overstated it. Stale paths inside a "verify on the live page" caveat are still worth fixing:
  they ride a redirect Cloudflare is free to retire. **Note the gate's blind spot:** `check-pointers` passed 95/95 because it validates
  atlas siblings, not URLs in prose — these were invisible to it by design, not by failure.
- **`workers-ai.md` +4** — `options: { rejectIfBusy: true }` makes a synchronous request fail fast
  (`429` / internal `3040`) instead of sitting in the capacity queue. OpenAI-compatible clients that
  strip unknown fields ignore it and queue normally. Verified on `workers-ai/features/reject-if-busy/`.
- **`email-service.md` +6** — suppressions are **account-scoped** (one entry blocks the recipient
  across every sending domain and subdomain); **`read_only`, not `reason`, decides whether an entry
  is deletable** (the docs say so explicitly); managing the list now lives at
  `email-service/configuration/suppressions/` with CSV/JSON/TXT import, separate from the concepts
  page the file already pointed at. Needs an **Email Sending: Edit** token.
- `mesh` added to `_known-products.txt` (107) and to the SKILL.md catalog + the Networking router line.

**Two gates went red after closing — both diagnosed, neither hidden**

- **`in-scope gap` 0 → 37.** Not caused by Mesh. The fresh spec carries 37 operations under roots a
  slice already claims that `slice-api`'s matcher does not pick up: `workers` 21, `billing` 6,
  `analytics` 3, `browser-rendering` 2, `ai-gateway` 2, `spectrum`/`email`/`ssl` 1 each. The 08-18
  spec was simply too old to show them — **the gap existed before this pass and the stale spec was
  hiding it.** Correctness gates stayed at zero (phantom 0, stale summaries 0, bodies 648/648), so
  nothing wrong shipped to a reader; this is uncovered surface, not a defect. Carried as Deferred #2.
- **1 new not-found token, in `mesh.md`.** The token is
  `cloudflare-one/networks/connectors/cloudflare-mesh/`, cited in Going deeper as the mirror path.
  `verify-products` fetches the 11 pages of `/mesh/` and looks for each claim's tokens in them — the
  mirror's own URL is not written inside those pages, so it is unverifiable *by this method*, not
  false. Verified independently today: the path returns 200 and its `concepts` page diffs identical
  to `/mesh/concepts/` apart from URL prefixes. Baseline re-recorded on that evidence; `mesh.md`
  otherwise scores 47/48 confirmed across 58 claim blocks (60% audited, 40% unaudited prose).

**Not curated, with reasons**
- `bots/attribution-business-insights` → `bots/business-insights`: `bots.md` never cited the old
  path. Measured, no action.
- `dns/.../set-up-google-workspace` and `network-interconnect/locations`: routine how-to and a
  facility list, no durable fact for a reference file.
- The two WAF release entries (09-15 and the scheduled 09-22): standing rule, WAF releases are not
  curated here.
- The `cloudflare-one/.../cloudflare-mesh` subtree is a **mirror** of `/mesh/` — diffed one page,
  identical but for URL prefixes. Curated once, at the canonical slug.

**Pass 2 — the two tooling items, closed the same day**

Both were the same mechanism. `slice-api` derives a slug's matcher from the roots its *existing*
slice already contains — so an endpoint under a root no slice has ever held is invisible, and a
product with no slice at all can never grow one. The fix in both cases is a seed line, which the
re-slice then expands.

- **`api/mesh.md` created — 11 operations.** Seeded with `GET /accounts/{account_id}/warp_connector`;
  the re-slice pulled the rest. Four are absent from the docs entirely: `GET`/`PATCH`/`DELETE` on the
  node, `GET`/`PUT /configurations` (HA config), `GET /connectors/{connector_id}`. The spec's path
  parameter is **`{tunnel_id}`** while the docs call the object a *node* — recorded as a gotcha in
  `products/mesh.md`, which now also points at the slice.
- **In-scope gap 37 → 0.** Seeded eight slices and re-sliced: `workers` +10 (Workers Observability
  *issues*, plus zone tracing rules/settings — 164 ops now), `billing` +6, `analytics` +3
  (`/analytics/sql`, its `POST`, and `introspection`), `browser-run` +2 (session-recording fetch and
  its network log — the 09-18 changelog item), `ai-gateway` +2 (`logging-state`, including the
  migration to Workers Observability), `spectrum` +1, `ssl` +1, `email-service` +1 (account
  reputation).
- **Deliberately not seeded:** `access/ai-controls/mcp/analytics/*` and
  `email-security/analytics/monthly_report`. Both are Cloudflare One / Email Security surface,
  dropped from the catalog 2026-06-26. Seeding them would re-import a removed category through a word
  match — the `rules`/Cloudforce One mistake of 08-15.

**Pass 3 — `scripts/check-doc-urls`, and three false greens on the way to it**

Backlog item 2 (the prose-URL blind spot) is closed. The script is 60 lines; getting it to be *true*
took three corrections, each caught by opening one hit instead of believing the count.

1. **86 "dead URLs" — all false.** `references/<slug>/` is a directory inside the **official
   cloudflare skill**, written as "Official `cloudflare` skill `references/<slug>/`". The matcher
   prefixed it with the docs host. 70+ of the 86 were that one shape. Gated on `_known-products.txt`.
2. **14 more — also false.** `pages/<slug>/…` is the LOCAL raw corpus (`raw/docs-oficiais/pages/`),
   and `pages` is itself a product slug, so the new gate waved them through. Excluded by name.
3. **Then it went green on the defect it was built for.** Put the two `workers-vpc/reference/…`
   links back as an adversarial fixture: **the script reported all clear.** Two reasons, both fatal:
   the regex demanded `https?://` while the files overwhelmingly write the host bare inside
   backticks, and the check followed redirects, so a 301 read as 200. Fixed both. Re-run on the
   fixture: caught, as `STALE 301`. **The gate counts only from this run onward — the two green runs
   before it measured nothing.**

The 301-vs-404 split is now the script's core output, because the real corpus is mostly 301s:

**Findings on the real files (1 dead, 5 stale), all fixed**
- ❌ `api/resources/tags/` → **404**, no such page. `resource-tagging.md` now points at this skill's
  own `api/resource-tagging.md` slice and says the public page does not exist.
- ⚠️ `agents/api-reference/think/` → `agents/harnesses/think/` (`think.md`)
- ⚠️ `containers/pricing/` → `containers/platform/pricing/` (`sandbox.md`)
- ⚠️ `learning-paths/` → `/resources/` — the product's docs root moved (`learning-paths.md`, 2 spots)
- ⚠️ `learning-paths/mtls/` → `…/mtls/concepts/` (`ssl.md`)
- ⚠️ `r2/data-catalog/` → `r2-data-catalog/` (`r2.md`, `r2-data-catalog.md`)

**Final: 180 distinct doc URLs across 90 product files, every one resolving directly — no 404, no
redirect.** `check-pointers` (atlas siblings) and `check-doc-urls` (doc URLs in prose) now cover
both link classes; before today only the first was checked, and the 36-URL figure an early run
printed was the broken matcher, not the corpus.

**Wired into BOTH phases of `scripts/refresh`, and the wiring tested in both.**
- *Phase 1 (detect):* `check-doc-urls` runs right after `check-pointers`, the two link classes side
  by side. Fixture: one link reverted to its stale path → the whole `refresh` exits 1 naming file
  and line; restored → exits 0.
- *Phase 2 (`--close`), added after a review caught it:* **phase 2 ran no link gate at all** — not
  `check-doc-urls`, and not `check-pointers` either, which had lived only in phase 1 since 09-04.
  Every link check was in the phase an operator can skip, while `--close` — the documented way to
  finish a pass — promoted the workbench unchecked. That is the mechanism by which `workers-vpc.md`
  carried two stale URLs past four green passes. Both gates now run against the **workbench, before
  promotion**, and block. Fixture: with one stale link in the workbench, `--close` exits **1**,
  prints `✗ BLOCKED`, never reaches "promoting workbench → installed" (grep count 0), and the
  installed copy is verified unchanged. Clean workbench: exits 0 and closes normally.
- *The fixture is a script, not a story.* A review pointed out that the evidence for the two paths
  existed only in this entry — a claim nobody could re-check. It is now
  `scripts/test-link-gates`: it breaks `workers-vpc.md` on purpose, shows the installed copy before
  and after, runs `--close` and asserts it exits 1 without reaching promotion, restores, closes for
  real and asserts 0. Output lands in `evals/link-gate-fixture.log`. Run it after touching either
  link gate.

**Cross-checked with a second instrument.** The script's verdicts were confirmed against `curl`
(not its own urllib): all 180 URLs return **200 without following redirects**, and each of the six
it had flagged independently returns what it claimed — `api/resources/tags/` 404, the other five
301. A checker agreeing with itself proves nothing; this is two instruments agreeing.

**Deferred** (the backlog — each item stands on its own until named and closed)
1. **`email-service.md` carries 12 undocumented over-cap lines** predating this pass, now recorded
   in `_curation-guide.md` but not audited. Audit or trim next pass.
2. **`check-doc-urls` proves a URL resolves, not that the page still says what we claim.** A live
   link to a rewritten page passes it. Content is `verify-products`' job (3,492 claims confirmed,
   33% of blocks unaudited) — the two do not overlap, and neither covers prose framing.

---

## 2026-09-15

**One real number changed in four files; the rest is new documentation, deferred on purpose.**

**What the check said (run 2026-09-14):** product list clean (106/106); new subtrees `tunnel/features`
(+8), `tunnel/guides` (+8), `tunnel/reference` (+3), `tunnel/platform` (+2), `images/storage/upload-images/import-from-s3`
(+4), `waf/detections/attack-signature-detection` (+4); ~28 `cloudflare-one/` subtrees gone; 12 single
pages; 7 new not-found tokens; blindness up by one term (`tunnel`: `locally-managed`); copy sync clean.

**Checked against the instrument before believing it** (the 2026-09-04 lesson): `tunnel/` held 34–35
prefixes in all three recorded baselines (08-26, prev, current); `cloudflare-one/` held 731–732. No
baseline collapse — the additions are real docs, not an artifact of a truncated baseline.

**Curated**
- **Worker size limit.** All 7 new not-found tokens were `3 MB` / `10 MB`. The live limits page
  (`workers/platform/limits/`) now states **64 MiB uncompressed, Free and Paid**, and "there is no
  compressed size limit". Fixed in `workers.md`, `pages.md`, `terraform.md`, `pulumi.md`. When the
  limit changed was not established — no date written into the files.

**Deferred** (the backlog) — *superseded by pass 2 below; every item was taken up the same day.*

### Pass 2 — "cura tudo" (same day)

**The instrument was wrong again, and pass 1 closed on top of it.** The "~28 `cloudflare-one/` subtrees
gone" were not a docs retirement. On 2026-09-14 `cloudflare-one/llms.txt` stopped listing pages and
started linking **eleven nested indices** (`cloudflare-one/networks/llms.txt`, `access-controls/`, …).
`pagediff.py` read only the top file, so the product fell from 731 prefixes to 107 — and pass 1's
`--close` **recorded that 107 as the baseline**. The `--init` collapse guard did not fire because the
current baseline it compares against was already being written in the same step as the shrink.
Measured: of all 106 products, `cloudflare-one` is the **only** one using nested indices today. Both
cited pages (`networks/connectors/cloudflare-tunnel/`, `access-controls/ai-controls/mcp-portals/`) still 200.

**Fixed** — `scripts/pagediff.py` now follows every nested `llms.txt` under the product's own slug and
refuses the whole read if any sub-index fails (a partial union is the silent shrink the function exists
to refuse). Tested live: `cloudflare-one` 604 prefixes (vs 732 on 08-26 — 10 subtrees genuinely left the
index, e.g. `networks/connectors/cloudflare-tunnel`, which moved to `/tunnel/` but still serves 200),
`tunnel` 32 pages, `workers-ai` 58 — no regression on flat products.

**Curated (all against the live pages, 2026-09-15)**
- `tunnel.md` — `/tunnel/` is now self-contained. Added: error triage 1033 / 502 / 1016 and "Healthy only
  covers cloudflared↔Cloudflare"; QUIC→HTTP/2 fallback; one service per machine; `cfargotunnel.com`
  proxies only same-account records; `cert.pem` (account-wide, ≥10y) vs `<UUID>.json` (one tunnel, never
  expires); per-tunnel resource-scoped roles; replicas vs load balancer (one UUID = one endpoint, no TCP
  monitors); sizing (4 GB/4 cores, 50k ports, ulimit 70k). **Removed two unsourced claims:** "24h grace
  window" on token rotation (current docs: old token loses *new* connections, existing ones stay up until
  restart — containment needs `DELETE …/connections`) and "~5s heartbeat TTL" (in no live page). Confirmed
  still true: 25 replicas/100 connections, Quick Tunnels 200 in-flight / no SSE / fail with config.yaml,
  one-year `cloudflared` support window.
- `waf.md` — Attack Signature Detection (Early Access): fields, confidence ↔ Managed Rules default set,
  Ref = Managed Rule ID, no override inheritance, Log-vs-Block comparison, Logpush mapping.
- `images.md` — Import from S3 (sources, jobs, IAM scope, skipped archival tiers, stops at storage quota).
- `r2.md` — Data Access Logs (GA; <400 only, best-effort, not retroactive, no jurisdiction buckets).
- `rules.md` — response-body inspection stalls streams; `no-transform` limits; Response Body Buffering = None.
- `realtime.md` — RealtimeKit retention (recordings/transcripts 7 days; analytics 6 months; webhooks 1 month).
- `workflows.md` — default retention 7 days for Paid Workflows created from 2026-09-10 (changelog; the
  limits page still says 30 — recorded as a docs lag, not a contradiction).
- `ai-gateway.md` — custom costs `per_cache_read_token` / `per_cache_write_token`.
- `workers.md` — Python 3.14 default from compat date 2026-09-08; Django via wsgi/asgi.
- `agents.md` — Voice `turnmetrics` (changelog only).
- `sandbox.md` — Codex via the OpenAI Agents API tutorial (keys and scopes).
- `ai-search.md` — extensionless R2 objects need an explicit Content-Type.
- `_curation-guide.md` — over-cap exemptions recorded for tunnel, waf, workers, realtime, ai-gateway, ai-search.

**Gates on the workbench before closing:** pointers ✅ (95). verify-products: 3,440 confirmed / 243 not
found (was 3,375 / 239); **4 new not-found, all in `agents`: `turnmetrics`, `no_output`, `model_error`,
`tts_error`** — true, but only in the 2026-09-11 changelog, which the gate does not read. Accepted into
the baseline on purpose. Blindness rose in 4 products (`images` Hosted Images, `r2` Data Access Logs,
`rules` Response Body Buffering, `waf` Attack Signature Detection / Log Explorer / Security Analytics) —
every new stranded term is one this pass added as prose. Accepted on purpose; `tunnel`'s
`locally-managed` term from the weekly check no longer strands.

**Deferred** (the backlog)
- `agents.md` voice metrics: re-check when the Voice docs page documents `turnmetrics`; then the 4 tokens
  should confirm on their own.
- `workflows.md`: re-check the limits page for the 7-day default and drop the "docs lag" note.
- The 10 subtrees that genuinely left the `cloudflare-one` index (e.g. `insights/dex`,
  `networks/connectors/cloudflare-mesh`) were not investigated one by one — no product file cites them.
- The collapse guard compares against the current baseline only; a shrink that already entered it in an
  earlier close is invisible to it. Check the next false "gone" against `_known-pages.good-*.txt` too.

**Root cause of the unguarded shrink, found after closing pass 2 (fixed, re-closed).** `pagediff.py`
merged products with `live.update(prefixes(pages))`. Indices cross-link: `ai-gateway`, `dns`,
`learning-paths` and others cite single `cloudflare-one` pages, and whichever finished last overwrote
the product's page count. Measured: `cloudflare-one` root count was **1** in the 08-26 "good" baseline,
in `.prev`, and in the baseline pass 2 wrote — against **540** pages live. The collapse guard needs
`was >= 3`, so it never covered this product. Fix: union all pages across products, then fold into
prefixes once. Verified after re-close: see the root count in `_known-pages.txt`.

---

## 2026-09-04

**The instrument broke, and the weekly check reported the breakage as a product launch.** This pass
curated almost nothing. It fixed the thing that manufactures false findings.

**What the check said:** four new subtrees under `workers-ai/` — `features` (+24), `guides` (+13),
`platform` (+6), `configuration` (+4) — plus four `workers-ai` single pages, and 7 new not-found
tokens. Read as a launch, that is "Workers AI was rewritten this week".

**What was actually true.** Three independent measurements, none of them ambiguous:

1. The local raw corpus, fetched **2026-06-26**, already contains every one of those subtrees. They
   are not two days old; they are at least ten weeks old.
2. `_known-pages.prev.txt` (recorded 2026-08-26) has **61** `workers-ai` prefixes. The current
   baseline, recorded **2026-08-31**, has **3**. Across all 106 products, no other slug moved by more
   than 4. A single product losing 58 pages while everything else holds is not a docs change.
3. Live `workers-ai/llms.txt`, fetched today: **60 pages**.

The 08-31 baseline recording caught a truncated read of one `llms.txt` and froze it as truth. Every
run since compared live reality against that hole and reported the missing 58 pages back as new. The
`api` slug had the same injury at smaller scale — 84 → 81 — and it also came back on its own.

**This is the mirror of the 2026-07-21 false all-clear.** That pass stayed silent about a check that
never ran. This one shouted about a launch that never happened. Same root cause, opposite sign: the
instrument cannot tell "I failed to read this" from "this is what is there".

**Why nothing raised.** `fetch()` did not swallow an exception — no exception existed. The docs site
answers **chunked**, so a stream that dies mid-body has no `Content-Length` to fail against.
`read()` returns the prefix, HTTP 200, and the regex finds 3 pages instead of 60. Worse,
`verify-products` and `probe-blindness` **write that prefix to `~/.cache`**, where it is reused as
truth on every later run. That is the mechanism behind the not-found count reading 7 in one run and
1 in the next, on the same files, with nothing edited between them.

**Fixed** (`scripts/`, all three fetchers)

- **`pagediff.py` — `fetch()`**: 3 attempts with backoff; rejects a 200 shorter than a declared
  `Content-Length`.
- **`pagediff.py` — `pages_for()`**: because chunked responses have no length to check, an
  implausibly small parse (< 2 pages) is now treated as a failed read and retried, keeping the larger
  result. A product that genuinely has one page survives this unchanged.
- **`pagediff.py` — `--init` refuses to record a bad baseline**, the guard that would have stopped
  08-31 outright: it aborts if any product is unreachable, and aborts if a product with ≥10 pages in
  the current baseline collapses below half. `--force` is there for a real docs shrink.
- **`verify-products` and `probe-blindness`**: same retry, same short-read rejection, and **a short
  read is never written to the cache**.
- **`scripts/refresh` — a crashed check no longer reads as a clean one.** Found while testing the
  above: the weekly report ran `verify-products 2>/dev/null | sed -n '/── totals ──/,$p'`. That
  pipeline reports *sed's* exit status, so a Python traceback inside `verify-products` produced an
  empty section and a success code — the 2026-07-21 false all-clear rebuilt out of shell plumbing,
  and reproduced live when a missing `import time` crashed the script and it exited 0. Both checks
  now capture stdout/stderr, and a run that never reached its totals prints **UNKNOWN, not clean**,
  with the failing line and the command to re-run by hand. Watched failing before being trusted.
  **This fix shipped broken once and was caught in review.** `refresh` runs under `set -euo pipefail`;
  the first version invoked the checks as bare commands, so a non-zero exit — which is
  `verify-products`' *normal* "new not-found tokens" state — aborted the whole report on that line.
  It truncated precisely when there was something to report, and the first test missed it because
  the harness lacked `set -e` and the fake exited 0. Now `cmd … || _rc=$?`, re-tested under
  `set -euo pipefail` with the fake exiting 1: the 🚨 line prints and the script reaches its end.

**Both guards were watched failing before being trusted.** A local server answering 200 with
`Content-Length: 9999` and 13 bytes of body is rejected. A synthetic replay of the 08-31 event
(`workers-ai` 61 → 3) is refused with exit 1 and the baseline left untouched.

**Recorded**

Baseline re-recorded with the fixed walker: **6641 prefixes, 106 products**, `workers-ai` back to 61,
`api` back to 84. Remaining deltas against the known-good 26/08 snapshot are all +1 to +4 over nine
days and plausible. The 86 MB page cache was deleted rather than trusted, since any entry in it could
have been a short read.

`_known-pages.good-2026-08-26.txt` is kept deliberately: `--init` rotates the outgoing baseline into
`.prev.txt`, and the outgoing baseline was the corrupted one. Without this copy the only clean
snapshot would have been overwritten by the repair.

**Curated** (small, and genuinely from the last 7 days)

- **`workers.md`** — request body size was wrong: the file said *100 MB Free/Pro, 500 MB Ent*. Live
  docs: Free/Pro **100 MB**, Business **200 MB**, Enterprise **up to 5 GB**, self-serve from the
  zone's Network page (*Maximum Upload Size*), over 5 GB via the account team, over-limit → **413**.
  Business was missing entirely and the Enterprise figure was off by an order of magnitude. This was
  the one not-found token that survived a clean-cache run — the other six were cache artifacts.
- **`d1.md`** — since **2026-09-01** the free daily row-read/row-write caps are **enforced**, not
  merely metered: past the cap, Binding API and REST API queries **fail** until midnight UTC, with a
  named error string and email alerts. Stored data unaffected. This changes what "free tier" means
  for anything shipped on it.
- **`images.md`** — the 09-02 binding release: `.text()` rasterizes text (`font`/`size`/`color`) and
  `cf.image`'s `draw` array takes a `text` key; `.list()` gains `filter.metadata` with bounded ranges,
  plus `.signedUrl()` and `.createDirectUpload()` from the binding, so hosted-image management no
  longer requires an API token.

**Resolved — the backlog opened by the morning pass, closed the same day**

Thales' instruction was "não quero pendências". Eight items; **three of them turned out to be
measurement artifacts rather than work**, which is itself the finding.

- **`fetch()` general case — closed.** `looks_like_llms_txt()` refuses a complete-but-wrong body
  (soft 404, error page served 200, anything with no page link at all), so "this product has no
  docs" can no longer be manufactured by an edge error.
- **Diff-time floor — closed.** The floor now scales with what the baseline already knows for that
  slug (half of it, minimum 2) instead of a flat 2. Tested against the real event: a 3-of-61 read is
  retried and recovered; the old flat floor accepted it. The baseline is loaded *before* the walk so
  each product's own history sets its threshold.
- **`--init` collapse guard blind spot — closed.** Threshold dropped from ≥10 pages to ≥3, the
  smallest count where "halved" still means something. An 8 → 1 truncation is now blocked; it passed
  before.
- **Sibling-pointer gate — BUILT** (`scripts/check-pointers`, wired into the weekly run). It stayed
  unbuilt for three passes at 11 false positives to 0 findings; the split that fixed it is mechanical
  — `products/<slug>.md` is an atlas sibling and must resolve, `references/<slug>/` belongs to the
  official skill, and bare `api.md`/`patterns.md`/`gotchas.md` are leaves inside those dirs and are
  never atlas pointers. **Its own first version was wrong too**: it reported `privacy-pass.md` and
  `privacy-proxy.md`, whose lines *assert the directory does not exist*. A line-wide negation filter
  fixed that and promptly suppressed a real pointer in a line that happened to contain "not", so the
  negation test is now scoped to the path's own sentence. Final: 95 references checked, 0 broken,
  0 false positives, and a planted `products/ghost-product.md` is caught.
- **Cross-product false accusations — closed.** A token still missing after the shared-vocabulary
  fallback is now checked against the products the file **explicitly points at**, capped at 3.
  Deliberately limited to declared pointers: a token confirmed against an arbitrary corpus is a token
  nobody checked. Effect: **12 false accusations removed**, 9 of them `sandbox` → `containers`
  (Sandboxes runs on Containers, so the instance-size vocabulary was never going to be in its own
  corpus). Not-found 268 → 257.
- **Access / Cloudflare One — closed, and it was the wrong diagnosis.** There is no `access` slug;
  Access lives inside `cloudflare-one`, and `cloudflare-one` is already covered by two installed
  sibling skills (`cloudflare-one`, `cloudflare-one-migrations`) that document Access apps, policies,
  service tokens and mTLS. The real defect was that the catalog lists 89 products against 106 live
  ones and **never said which 17 it does not cover** — so an Access question hit silence, and silence
  is where pre-trained guessing fills in. SKILL.md now carries a *Coverage boundary* section: the
  Zero Trust family routes to the sibling skills, 14 network products are marked "live docs only,
  never from memory", 3 slugs are named as doc-site infrastructure. Writing a `cloudflare-one.md`
  was rejected on purpose: 732 doc pages, larger than this catalog's files combined, and duplicating
  it creates the second stale source of truth this skill exists to prevent.
- **`containers.md` GA date — verified.** `blog.cloudflare.com/sandbox-ga/`, dated 2026-04-13, states
  Sandboxes and Containers are generally available in one sentence. Cited in the file so the next
  pass does not re-litigate a date the 7-day changelog window structurally cannot see.
- **The untriaged baselines — triaged, and both were partly instrument noise.**
  - *268 not-found tokens, classified:* 129 prose terms, 58 constants, 51 API identifiers (many
    external by construction — `github.com/…`, `~/.config/…` will never be in Cloudflare's docs),
    17 endpoints, 12 number+unit. The 12 numeric ones are the only category that can silently go
    stale, so all 12 were checked by hand: **3 are prose framing** (one is inside a note listing
    claims already *removed* for lack of a source), **8 are confirmed** against the Containers
    instance-type table via the new fallback, **1 is confirmed verbatim** — "Smart Shield Advanced
    includes 2 TB of storage for Cache Reserve", documented under Smart Shield rather than Cache.
  - *One malformed token was permanently unconfirmable:* `agents.md` line 29 used backslash-escaped
    backticks inside a code span (markdown does not escape there), so the tokenizer swallowed half a
    sentence as one "token". Fixed the markup; the fragment is gone and one more claim now confirms.
  - *369 stranded terms → 312.* 57 of them were **citations, not claims**: a file that cites
    `…/cloudflare-one/access-controls/…` necessarily contains "access-controls", and citing a page
    asserts nothing about it. Both doc URLs and atlas's own `products/*.md` pointers are now stripped
    before the term hunt. **Correction on my own measurement:** an early classification put citations
    at 44%, taken from the `--verbose` listing, which prints only the first 6 terms per product
    alphabetically — a biased sample. Measured across the full set it is 57 of 369, **15%**.
- **`workers.md` over cap** — recorded in `_curation-guide.md` with the measured reason, which is
  that file's mechanism for ending re-litigation. Closed by being written down.

**Baselines after the triage:** 250 accepted not-found tokens (was 268), 312 stranded terms (was 369).

**Deferred** (the backlog)

Nothing. Every item opened by the morning pass was closed the same day.

What remains below are **properties of the design, not work owed** — recorded so a later pass
recognises them as decisions rather than rediscovering them as bugs:

- The `--init` collapse guard fires at ≥3 pages and on a halving. A 2 → 1 truncation is
  indistinguishable from noise at that size and passes. The guard has also never been exercised
  against a *genuine* docs shrink, because none has happened since it was built — `--force` is the
  escape hatch when one does.
- The cross-product fallback only consults products a file explicitly points at, capped at 3. Widening
  it to "any product mentioned" would confirm tokens nobody checked; the gate is worth more narrow.
- Re-recording the blindness baseline accepts the current stranded set, so blindness can ratchet
  upward one deliberate term at a time. The weekly rising-count check is what bounds it.
- 33% of claim blocks remain UNAUDITED rather than verified. That is the honest headline number and
  the probe exists to keep it from being read as coverage.

---

## 2026-08-31

**The Containers docs reorg — a structural change with no content behind it, and three defects it exposed.**

The weekly check flagged five new subtrees under `containers/` and eight disappearing ones. Fetched all
31 live pages and mapped them one-to-one against the previous snapshot: **it is a pure reshuffle.**
`pricing/` and `platform-details/limits/` → `platform/`; `container-class/` → `reference/`; `deploy/`,
`ssh/`, `local-dev/`, `execute-commands/`, `image-management/`, `outbound-traffic/` → `guides/`;
`architecture/`, `placement/` → `concepts/`; `rollouts/`, `scaling-and-routing/`, `workers-connections/`,
`environment-variables/` → `configuration/`. No page gained or lost content — the pricing, limits and
deploy diffs reduce to frontmatter, the `og-docs.png` swap and rewritten internal links once chrome is
filtered out. Zero new pages.

**Verification ran backwards on purpose** — instead of reading 14 diffs, every checkable claim in
`containers.md` was grepped against the fresh corpus. 24 of 27 confirmed verbatim (all pricing rates,
all included tiers, all account limits, instance types, `renewActivityTimeout`, `switchPort`,
`--containers-rollout`, SIGKILL 15 min, `linux/amd64`, Artifact Registry). **Three did not**, and all
three were edited:

- **`blockConcurrencyWhile` was fabricated inference.** The file claimed "lifecycle hooks run inside
  `blockConcurrencyWhile` → keep them fast or requests stall." That string does not appear anywhere in
  the Containers corpus, old or new. It exists in `durable-objects/api/container/`, but as a pattern
  *the developer writes* to boot a container — not as hook semantics. Replaced with what the docs
  actually say: hooks are async-aware and the runtime awaits them, and `onStop` receives
  `{ exitCode, reason }` with `reason` being `'exit'` or `'runtime_signal'`.
- **"Cold-start in 1–3s" has no source.** Not in the old snapshot either. The docs say cold starts take
  "on the order of seconds, depending on image size and what runs at start" and give no number.
  Replaced with the docs' own hedge rather than a fabricated range.
- **Four cited paths were dead** — the reorg 404'd `containers/pricing/`, `platform-details/limits/`,
  `platform-details/architecture/` and `containers/ssh/`. Fixed and all five cited URLs re-checked live
  (200 each). A path map was added to "Going deeper" so readers arriving with stale links land right.

**Two changelog items curated alongside**, both verified against live docs before writing:

- `durable-objects.md` — an alarm interrupted by `ctx.abort()` **retries by default**, so an unrelated
  request cannot permanently cancel it; pass `{ retryAlarm: false }` to end a finished alarm. Applies to
  abort calls outside the handler too.
- `dynamic-workers.md` — concurrency table from the new `platform/limits/` page: **4 distinct Dynamic
  Workers per Worker request, 10 per Durable Object** (raised from 4 on 2026-08-28). Multiple in-flight
  requests to the same Dynamic Worker count as one.

**One backlog item closed by measurement.** The last pass recorded that `dynamic-workers.md` pointed at
two atlas files that do not exist. It no longer does — every atlas-sibling pointer in all 89 files
resolves. A naive `*.md` gate reports 11 "broken pointers", but all of them are files inside the
*official* `cloudflare` skill's `references/<slug>/` directories (`api.md`, `gotchas.md`, `patterns.md`,
`configuration.md`), correctly cited as such. A real gate has to tell the two namespaces apart.

**Deferred** (the backlog)

- **Access has no product file at all.** Three Access changes landed in one week — scannable service-token
  secret format, grace periods for token rotation, temporarily turning tokens off — and there is nowhere
  to put them: 89 of 106 known products are curated, and `access` / `cloudflare-one` are among the 17 that
  are not. This is a coverage gap, not a staleness gap, and writing the file is a full pass of its own.
- **The GA date `2026-04-13` in `containers.md` could not be re-confirmed today.** It is not in the docs
  corpus (old or new) and the changelog window only reaches back 7 days. It stands because it was an
  operator-reported correction on 2026-08-26, not because this pass verified it. Anything asserting a date
  outside the changelog window is unverifiable by the weekly instrument — worth knowing before trusting one.
- **`fetch()` swallows failures.** Now the top of the backlog: an unfetchable page is indistinguishable
  from an empty one, which is what makes the uncached run flaky. Needs a retry and a hard error when a
  page listed in `llms.txt` cannot be read — the script's own header already argues that "a NOT FOUND is
  meaningless unless the whole product corpus was fetched", but nothing enforces it.
- **The sibling-pointer gate is still unbuilt**, now with its hard part identified: distinguishing atlas
  siblings from official-skill refs. Without that split it is 11 false positives to 0 real findings.
- **Cross-product citation still produces false accusations** — unchanged from the last pass. The
  parent-corpus fallback covers declared sub-products only.
- **The 260-token and 367-term baselines remain re-recorded but untriaged**, minus the 3 new not-found
  tokens this pass introduced and resolved via the path fixes.
- **`sandbox.md` (243/120) stays whole** — transitional, revisit only if Sandboxes 1.0 is still in preview
  past 2027. `containers.md` moves 123 → 132 and `dynamic-workers.md` 143 → 147; both recorded in
  `_curation-guide.md` with the measured reason so the next pass does not re-litigate.
**The gate's blind spot was diagnosed and fixed — it was verifying the past.**

`verify-products` caches every fetched page under `~/.cache/cloudflare-atlas/pages/` keyed by URL hash,
**with no TTL and no invalidation**. `refresh` called it without `--no-cache`, so the weekly run has been
checking product files against whatever the docs said the first time each page was ever fetched.

Proven, not inferred: the cache entry for `durable-objects/api/state/index.md` is dated **2026-08-25
17:19** and contains `retryAlarm` **zero** times; the live page contains it **three** times. The
`ctx.abort({ retryAlarm })` changelog landed 2026-08-25 — the cache captured that page hours before
publication and then froze it. 4,997 of the ~5,000 cached pages carry the same risk. **This is the
mechanism by which a correct fact reads as NOT FOUND, and by which a fact that went stale would keep
reading as confirmed** — the second direction is the dangerous one, and it was running silently for
however long the cache has existed.

Fixed in `scripts/refresh`: the weekly verification now passes `--no-cache`, with the reason in a comment
above the call so it is not "optimized" back. Re-ran clean: `retryAlarm` confirms, both containers corpus
paths confirm, `durable-objects` goes 28/31 → 29/31, and the 3 new not-found tokens drop to **1** — the
literal string `platform-details/limits/`, which appears only inside the new de-para note that exists
precisely to name dead paths. Accepted into the baseline for that reason.

**What this costs, measured across four consecutive runs:** the weekly run now refetches ~5,000 pages
instead of reading them from disk, and it became **nondeterministic**. Page counts came back 5,145 /
5,144 / 5,143 across runs, and one run reported 3 phantom NEW not-found tokens that the next two runs
did not reproduce. `fetch()` returns `None` on any exception, and `corpus_for()` treats a failed page as
an empty one — so a transient network failure silently shrinks the corpus and every claim that lived on
the dropped page reads as NOT FOUND. **A single red run is now not evidence; only a reproduced one is.**
The trade is still right — a cache with no expiry on a skill whose entire purpose is currency was a
contradiction in terms — but the flakiness is the price and it should be engineered away (retry on
failure, and fail loudly when a page in `llms.txt` cannot be fetched, instead of counting it as empty).
- Carried over: Terraform/Pulumi registry corpus; ~1/3 probe noise unaudited; catalog counts hand-maintained.
- **Still true, and worth repeating:** no gate would have caught the `blockConcurrencyWhile` fabrication.
  A grep caught it only because the claim happened to contain an identifier. Prose assertions with no
  identifier in them remain uncheckable by anything cheaper than a model reading the source under an
  obligation to quote.

---

## 2026-08-26

**The prose sweep — 89 files read against the live docs by agents that had to cite.**

Triggered by the operator finding, in live use, that `containers.md` still called Containers a beta
product four months after GA. That single report exposed the real gap: **every gate built the day
before reads tokens, and none of them reads prose.** 995 high-risk claims (price, limit, plan
gating, status) sat across 89 files with nothing checking them.

**Method.** One agent per product file, each with the file's live doc corpus, each required to cite
a URL and a literal quote for every change, and each forbidden to edit on absence alone. The
anti-vandalism rule from entry (g) went into every prompt.

**Result: 3,373 confirmed tokens, up from 2,161** — the files now assert far more that is checkable,
and it matches the source. Zero stale maturity claims. Audited fraction 66% → 67%.

**Fabrications found and removed** — none of which any gate could see:

- **`workers-ai.md` — an entire error-code family invented** (`7502`/`7504`/`7505`/`7506`). No such
  codes; the real table is 3xxx/5xxx. An agent debugging a real failure would have looked one up.
- **`api-shield.md` — four invented numbers**: GraphQL "depth 1–50, size 1KB–1MB", "BOLA 1000+
  reqs/day", "risk labels 24–48h", JWT "±5 min clock skew". The real GraphQL constraint is parsing
  only on POST under 20 KB. The WAF JWT field was also wrong (`.payload` → `.claims`).
- **`use-cases.md` — a product that does not exist**: "Bot Security", in four places. Real name is
  Bot Management. Introduced by one of the nine edits whose report was lost to a crash, and caught
  only because those nine were re-reviewed.
- **`zaraz.md`, `stream.md`, `waf.md`, `load-balancing.md`, `sandbox.md`** each carried an invented
  API name, limit or type — a `heavy` instance type, an `IP-only` affinity mode, a phantom
  rules-per-ruleset ceiling, a webhook timestamp-drift gotcha.

**Errors that would have cost money or broken code:**

- `waf.md` rate-limiting quotas **inflated 5×** (Pro 10→2, Business 25→5).
- `d1.md` Free database size **10 GB → 500 MB**.
- `waiting-room.md` cookie name wrong by one underscore (`_cfwaitingroom` → `__cfwaitingroom`).
- `terraform.md` `api_email` is not a provider argument — it is `email`; R2 `location` values are
  lowercase, not uppercase; state migration is `tf-migrate`/`moved` blocks, not `terraform state mv`.
- `agent-setup.md` three MCP hostnames that **do not resolve** (measured: NXDOMAIN for `analytics`,
  `day`, `gateway`; the real ones are `dns-analytics`, `demo-day`, `ai-gateway`).
- `workers.md` still told the reader to add `nodejs_compat`, default-on since compat date 2026-08-04.
- `queues.md` pull-consumer config (`"type": "http_pull"`) no longer supported at all.
- `flagship.md` told the reader to use an evaluate-only token in the browser; the docs say do not
  use the client provider in a public app.

**TWO OF MY OWN CORRECTIONS WERE WRONG, and this is the important entry.**

- Earlier the same day, `agents.md` was "corrected" to say `useAgentChat` comes from `agents/react`.
  It comes from `@cloudflare/ai-chat/react`. The half that was right — that `agents/ai-react` does
  not exist — was kept; the replacement was invented.
- `zaraz.md` was "corrected" to state *"Cloudflare publishes no SPA guidance for Zaraz."* False.
  There is a **Single Page Application support** toggle and a `zaraz.spaPageview()` method.

Both are the same failure: **searched, did not find, asserted absence.** That is the exact error
the coverage rule exists to prevent, committed while hunting it in others. A third near-miss was
caught in the moment: `r2.md`'s "4.995 GiB" looked like a TiB/GiB confusion and is verbatim correct
per the docs' own footnote. What separated the near-miss from the two misses was opening the parent
source *before* editing rather than after.

**Portuguese leaked into English files.** The agents were prompted in Portuguese and eleven lines
came back partly in it, including `10.000` written with a Brazilian thousands separator inside an
English limits line — which reads as ten-point-zero to anyone else. All 89 files swept clean.

**The nine crash-orphaned files were re-reviewed, not trusted.** A session crash killed nine agents
after they had saved but before their reports arrived. Seven were clean on re-review
(`agent-memory` 30/30, `think` 47, `r2-sql` 22, `notifications` 24, plus `china-network`,
`ai-search`, `web-analytics`); two carried the defects listed above. Editing without a readable
report is exactly the condition under which "Bot Security" survived.

**Deferred** (the backlog)

- **`privacy-pass.md` closed the last gap** — the one file left out of the sweep, verified after the
  fact: ~30 claims (RFC numbers, Blind RSA token type 2, issuer endpoints, Workers redeeming without
  a binding, Privacy Gateway as closed beta), **zero errors, zero edits**. 89 of 89 now verified.
- **The 260-token and 367-term baselines are re-recorded but unreviewed.** Spot-checked the largest
  suspicious block — nine container instance sizes in `sandbox.md` — and it matches the official
  table verbatim; the NOT FOUND is cross-product scoping, not a defect. The rest is untriaged.
- **Cross-product citation still produces false accusations.** `sandbox.md` citing the Containers
  table and `think.md` citing the Agents runtime both look wrong to the gate. The parent-corpus
  fallback covers declared sub-products only.
- **Broken sibling pointers have no gate.** `dynamic-workers.md` pointed at two atlas files that do
  not exist; nothing checks intra-skill references.
- **No gate would have caught any fabrication in this entry.** They were prose. The instrument that
  works is a model reading the source under an obligation to quote — expensive, and not automatable
  into the weekly run at this cost.
- **The line cap now yields to verified fact** — operator decision, same day. Asked about two files;
  the measurement found **eight** over cap, recorded per-file in `_curation-guide.md` with the reason
  each stands, so the next pass does not re-litigate it. `dynamic-workers.md` at 143/120 joins them.
- **`sandbox.md` at 243/120 was proposed for a split; the proposal was withdrawn under questioning.**
  The operator asked simply "why split?" and the measurement did not support it: 120 of the 243 lines
  are the "stable vs 1.0 preview" section, which **disappears on its own when 1.0 ships**. Splitting
  would break the catalog's one-product-one-file mapping permanently to fix a transient state, and
  the cap exemption granted the same day exists precisely for verified content that does not fit.
  Recorded in the guide as transitional, with a revisit trigger (1.0 still in preview past 2027)
  rather than as an outlier. **Worth noting as method: the recommendation was weak and survived only
  until someone asked for the reasoning.**
- Carried over: Terraform/Pulumi registry corpus; ~⅓ probe noise; catalog counts hand-maintained.

---

## 2026-08-25 (i) — "Beta product": a stale status neither gate could see

Reported by the operator from live use: `containers.md` still called Containers a beta product.
**Containers and Sandboxes went generally available on 2026-04-13** — four months earlier.

**Fixed.** `containers.md` now reads *"Generally available since 2026-04-13 (Containers and
Sandboxes went GA together). Workers Paid plan only — there is no Free tier."* `sandbox.md` gained
the same fact plus the distinction it was missing: the *preview* it documents is the **SDK 1.0
release line**, not the product's maturity.

**Where it came from.** The raw docs pulled on 2026-06-26 — already post-GA — contain the word
"beta" for Containers **zero** times. No source ever said it. The line came from pre-training,
where Containers genuinely was in beta, and nothing in the skill has ever checked a prose claim.

**Why neither gate saw it.** Demonstrated, not assumed: with "Beta product" planted back,
`verify-products` reported **the identical 49/52 confirmed**, and `probe-blindness` reported no
change. "Beta" is unquoted, unbolded prose — invisible to token matching by construction. It lived
in the 34% this skill has been reporting as UNAUDITED all day. The audited fraction was doing its
job; nobody had acted on it.

**A new check, and four wrong rulers before the right one.** Status claims are the
highest-consequence, least visible content in the skill — a reader acting on "beta" makes different
architectural decisions than one acting on "GA". Each attempt failed for a different reason, and
each failure is now a comment in the code:

1. **Does the word appear in the corpus?** Defeated by a single hit inside the slug of an unrelated
   2025 changelog URL. One substring in a link certified a months-stale claim as fine.
2. **Strip links, then look.** The URL strip ran *first*, leaving orphaned `[` and `](` fragments,
   after which an unbounded link regex swallowed whole paragraphs — **five products accused of a
   stale "beta" whose corpora plainly said beta**, because the sentence had been eaten. Order fixed.
3. **Exact word match.** Accused `key-transparency` (says "preview", docs say "public beta") and
   `moq` (says "experimental", docs say "beta period"). Both files are right about the maturity and
   picked a different label. The words are one family, not a vocabulary.
4. **Word inside a real sentence, near the product name.** Containers' only hit is a section badge —
   `## Automatic provisioning Beta` — marking one feature, inside a long paragraph, in a corpus
   where the product's own name appears everywhere. Both tests passed it.

**The right ruler: the changelog.** Prose does not carry a status *transition*; an announcement
does, with a date. The check now reads the live changelog RSS for GA announcements and flags a
pre-GA claim the changelog has overtaken, quoting the entry: *"Containers and Sandboxes are now
generally available" [Mon, 13 Apr 2026]*.

**And it immediately produced the day's characteristic error, in a new shape.** Loose name matching
had `privacy-gateway` inheriting the GA of Cloudflare *Gateway*, and `workers-vpc` inheriting a
Source Maps announcement for *Workers*. **A narrower product must never inherit a broader
product's status** — that error reads as authoritative and is invisible unless you know both
products. The reverse-direction match was removed.

Corpus now clean; the planted defect is still caught.

**Deferred** (the backlog)

- **The check only sees status transitions that were ANNOUNCED.** A product that quietly stops
  being beta without a changelog entry stays undetected. This is the same shape as the original
  bug, one level up.
- **Only the summary blockquote and ⚠️ caveat lines are read for status claims.** A "currently in
  beta" buried in a Gotchas bullet is invisible.
- **The GA exemption is literal**: any file containing "GA" or "generally available" anywhere is
  skipped, so a file that states GA for one component and beta for the product would pass. It was
  chosen over special-casing `sandbox.md`, and it is loose.
- **Every other prose claim remains unchecked** — this closes one class, the one that was reported.
  Plan gating, billing cycles, deprecations and behavioural descriptions have no equivalent ruler.
- Carried over: `use-cases` strands 35 terms; `think.md` 169 lines vs a ≤150 cap; Terraform/Pulumi
  registry corpus; both baselines unreviewed; ~⅓ probe noise; catalog counts hand-maintained;
  `raw/docs-oficiais/` two months stale.

---

## 2026-08-25 (h) — the editing rule moved to where it is actually read

Entry (g) closed by writing the anti-vandalism rule into this changelog and calling it "enforced by
nobody". A measured sweep showed that was worse than it sounded.

**What was measured** — 10 of 10 executables in `scripts/`, both `~/.claude/settings*.json` files,
and all of `SKILL.md`:

- Four scripts can fail a run (`refresh`, `verify-products`, `probe-blindness`, `changelog-check`).
  All four **report**; none intercepts a tool call.
- The two greps that looked like edit-blocking were message strings inside `refresh`, not triggers.
- `settings.json` mentions the skill on four lines, all execution permissions. No hook.
- The rule appeared **once, in `CHANGELOG.md`** — a file the skill does not load — and **zero times
  in `SKILL.md`**, the file that does. Whoever used the skill tomorrow would never have seen it.

**Fixed** by moving it into `SKILL.md`, beside the retrieval-first rule: *If a gate says a term is
NOT FOUND, that is not permission to edit.* Three checks before any correction — parent and sibling
corpora, whether the file is asserting the absence, and the blog/OpenAPI spec — each carrying the
concrete case that produced it, including the four correct `think.md` API names the gate accused.

**A second stale number, found on the way in.** The catalog heading read "all 86". Counted:
**89 entries, 89 product files, zero orphans in either direction.** Corrected. That is now two
published counts wrong today (105 → 89 product files in three entries, 86 → 89 here), both from
figures nobody had reason to re-check because nothing ever contradicted them.

**Deferred** (the backlog)

- **The rule is prose in a skill file — read by a model, enforced by nothing.** It is strictly
  better than prose in a changelog nobody loads, and strictly weaker than a hook. The failure it
  guards against (editing on a scoping bug) is silent and self-confirming, which is exactly the
  profile that argues for a mechanism rather than a paragraph.
- **Counts in prose have now been wrong twice in one day.** Nothing derives "89" at render time;
  the heading will drift again the next time a product file is added or removed. A generated
  catalog header would close it.
- **`use-cases` strands 35 terms** — worst in the corpus, still never curated.
- **`think.md` is 169 lines against a ≤150 cap** — fifth consecutive pass.
- Carried over: Terraform/Pulumi registry corpus; both baselines unreviewed (227 not-found, 349
  stranded); ~⅓ probe noise; optional fields/enums/response bodies unmirrored; 60 operations whose
  spec body is `{}`; 79 `/radar/*` left deliberately; `zone-settings` with no product file;
  `raw/docs-oficiais/` two months stale.

---

## 2026-08-25 (g) — `think` covered; a false accusation caught one edit short of vandalism

The last unverified file in the skill, skipped by both tools for four consecutive passes, is now
the **best-covered file in the corpus**. And getting there produced the most dangerous failure of
the day — the gate accusing correct content, believed, and nearly acted on.

**Cause of the four-pass silence.** `think` is not a top-level product: it ships as 14 pages under
`agents/harnesses/think/`, listed in the *agents* index, so `/think/llms.txt` is a 404 and both
tools reported SKIPPED. Both now carry a one-line `SUBPRODUCT` map. **Checked across every product
file: `think` is the only slug affected**, so this is a fix, not a class — but it is kept as an
explicit map so the next sub-product costs one line instead of four passes of silence.

Result: `think` **111/120 confirmed · 88% of 63 claims audited** — the highest audited fraction in
the skill, on the file that had been described in three consecutive entries as "wholly unverified".

**THE NEAR-MISS.** Scoped to its subtree, the gate accused four API names in `think.md`:
`ctx.stash`, `ctx.snapshot`, `onFiberRecovered`, `parent_id`. Following the day's pattern — every
previous accusation had been a real fabrication — the docs were searched for replacements, the real
recovery hook looked like `onChatRecovery`, and a correction was being drafted. Checking the parent
page first showed **all four are correct and documented**, one level up under
`agents/runtime/execution/durable-execution/`. `think.md` legitimately cites its parent product's
API; the corpus was scoped wrong.

**A false accusation from this tool is more dangerous than a missed one.** A miss leaves a file as
it was. A false accusation turns a correct file into an incorrect one — and reports green
afterwards, because the fabricated "correction" would then match the docs it was copied from. Two
passes today were spent making the gate accuse more; this is the first evidence that the failure
mode runs both ways, and the reason a sub-product's corpus now includes its whole parent.

**A published number was wrong all day.** Entries (b), (d) and (e) said "105 product files".
There are **89**. The catalog lists 106 *products*, and the gap is 17 slugs deliberately dropped on
2026-06-26 (Cloudflare One, network security, consumer services incl. Radar) — verified against
`CATALOG-removed.md`, so a scope decision, not missing coverage. The figure was never checked
because it was never contradicted; corrected in place.

**Baselines re-recorded with `think` included:** 227 not-found tokens · 349 stranded terms ·
89 products, none skipped by either tool for the first time.

**Deferred** (the backlog)

- **The `think` remainder is 9 tokens, and 3 of them are the file being right about absence** —
  it explicitly documents that `@cloudflare/think/tools/sandbox` and `createSandboxTools` do not
  exist and that `kimi-k2.5` is a stale blog id the docs supersede with `kimi-k2.6`. The gate
  cannot tell "this term is absent" from "this file claims the term is absent", and counts both as
  NOT FOUND. Any file that documents an absence will always carry that noise.
- **Nothing distinguishes a false accusation from a true one except opening the parent source.**
  The near-miss was caught by habit, not by a mechanism. A gate that can vandalise on a scoping bug
  needs a rule before a correction is written — at minimum: never edit on a NOT FOUND without
  checking the parent/sibling corpus first. Written here, enforced by nobody.
- **`use-cases` strands 35 terms** — untouched, the worst in the corpus, and never curated.
- **`think.md` is 169 lines against a ≤150 cap.** Now verified, still oversized. Fifth pass.
- Carried over: Terraform/Pulumi registry corpus; both baselines unreviewed; ~⅓ probe noise;
  optional fields/enums/response bodies unmirrored; 60 operations whose spec body is `{}`;
  79 `/radar/*` left deliberately; `zone-settings` with no product file; `raw/docs-oficiais/`
  two months stale.

---

## 2026-08-25 (f) — the falsifier is no longer optional

Entry (e) ended by naming the hole it left: *"the probe is not wired into refresh — a gate whose
falsifier is optional will drift back to being trusted."* Closed.

**`scripts/probe-blindness` now runs inside `scripts/refresh`, every week**, immediately after the
gate it exists to contradict. It fails the run when a product strands MORE live-doc terms than its
baseline — i.e. when the gate quietly starts checking less than it used to.

**Rebuilt as a real tool, and it took three drafts to stop lying — each caught by its own number.**

1. **Independent re-implementation of everything, including which tokens the gate checked.**
   Reported **14** stranded terms against a hand-run figure of 201. The reasoning in the docstring
   was explicitly backwards: it called under-reporting "the safe direction for a tool whose job is
   to accuse". **An accuser that under-accuses is worthless.** The independence that matters is on
   the *evidence* side — corpus fetch, candidate extraction. Which tokens survived the gate's
   filters is a **fact about the gate**, not an assumption to guess at; it is now read from source.
2. **Own paragraph segmentation, deliberately different from the gate's bullet segmentation.**
   Reported **38**. A coarse block counts as audited the moment any token lands in it, and the
   stranded term beside it vanishes. The divergence that was supposed to prevent a shared blind
   spot instead created a private one.
3. **No segmentation at all.** The question was never about blocks: *is there a term in this file,
   checkable against the live docs, that the gate never checks?* That is answered term by term.
   **679** — and reading a 20-term sample showed a third of it was English compounds (`always-on`,
   `client-side`, `brute-force`) that happen to appear in some doc URL. Hyphenated candidates now
   have to prove they are a documentation slug (`durable-objects`, `ruleset-engine`) rather than an
   adjective, and a leading article is stripped. **340**, with ~⅓ residual noise **measured on that
   sample and written into the docstring** — the total is explicitly not a defect count.

**Seen failing before being trusted.** Disabling the gate's prose extraction — the very capability
added in entry (e) — made the probe accuse three products by name and list what went dark:
`waf` 8 → 19 (Cloudflare Managed, Cloudforce One, Page Shield, Schema Learning), `workers` 5 → 10
(Durable Objects, Service Worker, Custom Domains), `agents` 7 → 13 (Browser Rendering, Dynamic
Workers, Dynamic Client Registration). Restored, all three return to baseline.

**The shape of the whole day, stated once.** Three verdicts were reached by reading and all three
were wrong: the files were fine because the tokens checked out; the fraction was right because the
blocks read as prose; the probe was sound because its design was principled. Each was corrected by
building something able to contradict it, and each contradiction arrived within minutes of the
thing existing. The standing arrangement is now: `verify-products` accuses the files, and
`probe-blindness` accuses `verify-products`, both weekly, both able to fail the run.

**Deferred** (the backlog)

- **Nothing accuses `probe-blindness`.** The regression is real and the recursion has to stop
  somewhere; it stops here, undefended. The planted-blindness test is the only thing standing
  between it and quiet decay, and it is run by hand.
- **~⅓ of the 340 stranded terms are noise** — measured on a 20-term sample from four files, not
  triaged across the corpus. `use-cases` alone strands 35 and has never been looked at.
- **The audited fraction still understates checkable content**, now by a bounded and weekly-tracked
  amount rather than an unknown one.
- **`think` is skipped by both tools** — no `llms.txt`, so it is neither verified nor probed, and is
  still 169 lines against a ≤150 cap. It has now survived four consecutive passes untouched.
- Carried over: Terraform/Pulumi registry corpus; the 218 not-found and 340 stranded baselines both
  unreviewed; optional fields/enums/response bodies unmirrored; 60 operations whose spec body is
  `{}`; 79 `/radar/*` left deliberately; `zone-settings` with no product file; `raw/docs-oficiais/`
  two months stale.

---

## 2026-08-25 (e) — the audited fraction was itself wrong; a probe now falsifies it

Entry (d) closed by declaring two files "genuinely prose" — `google-tag-gateway` 17%, `ai` 21% —
on the strength of having **read** their unaudited blocks. That is the same instrument that had
failed twice already in the same day, and it failed again.

**`scripts/probe-blindness` — a falsifier for the fraction.** For each block the gate counts as
unaudited, it pulls candidate terms *ignoring markup entirely* (Title Case phrases, hyphenated
slugs) and asks whether they exist in the product's live corpus. A hit means the extractor is
blind, not that the file is prose. It is the mechanical counterpart to reading, and it can only
ever contradict the fraction — which is the point.

**It contradicted it immediately.** The two "prose-only" files held 33 real Cloudflare terms
between them in blocks the gate had written off: `Google Tag Manager`, `Domain Scoped Roles`,
`Configuration Rules`, `Bot Management`, `Durable Objects`, `Browser Rendering`, `Dynamic Workers`.
Run across the whole corpus: **394 real terms sitting in "unaudited" blocks, averaging 4.5 per
file — including 10 in `waf.md`, a file verified by hand this same day.** The audited fraction was
never a measure of what is checkable; it was a lower bound set by the extractor's reach.

**Two causes, both fixed:**

1. **Proper nouns in label position were excluded with the labels.** Entry (d) documented this as an
   accepted trade-off — `**AI Gateway** —` sacrificed to suppress `**Detection vs mitigation** —`.
   The probe showed the price was far higher than estimated, and that the two cases separate
   mechanically: a product name capitalises **every** word, a curator label is sentence case.
2. **Proper nouns in plain prose were never extracted at all.** The extractor only ever read
   markup — backticks, then bold. A term the curator simply wrote (`Bot Management`, `Google Help
   Center`) was invisible regardless of how checkable it was. Multi-word proper nouns are now read
   from prose too, **mid-sentence only**: a capital after a sentence boundary is grammar, not a
   name, and gluing it to the following product produced 48 fresh false alarms in one sweep
   (`Shows Origin Response`, `Use Workers`, `Powers Pages`) before that restriction went in.

**Result** — measured, with the probe re-run as the check rather than a reading:

| | before | after |
|---|---|---|
| tokens confirmed | 2,443 | **2,975** |
| claim blocks audited | 59% | **66%** |
| real terms stranded in unaudited blocks | 394 | **201** |
| files with ≥10 stranded terms | 7 | **0** |
| files with 0 stranded terms | 9 | **21** |

`waf.md` 33 → 49 tokens and 61% → 72% audited; `ai.md` 21% → 52%. The three hand-verified files
ended at **zero** not-found across every widening, which is the only evidence the added coverage
was not noise.

**Deferred** (the backlog)

- **201 real terms are still stranded** in unaudited blocks (`log-explorer` 9, `ssl` 7,
  `china-network` 7, `workers` 6, `notifications` 6, `agent-memory` 6). The residue is single-word
  proper nouns and sentence-initial mentions, both deliberately excluded as noise sources. **The
  fraction therefore still understates checkable content, by a now-measured amount.**
- **The probe is not wired into `refresh`.** It exists as `scripts/probe-blindness` and must be run
  by hand. A gate whose falsifier is optional will drift back to being trusted.
- **The probe cannot falsify itself.** It shares the corpus-fetch and the block-splitting code with
  the thing it audits; a bug there hides from both. Nothing checks the checker's checker.
- **22 new not-found tokens** entered the baseline unreviewed this pass — the tail of prose
  extraction (`Bot Mgmt`, `WAE SQL API`, `Great Firewall`, truncated fragments). Not triaged.
- **`think` still SKIPPED**, wholly unverified, still 169 lines against a ≤150 cap.
- Carried over: Terraform/Pulumi registry corpus; optional fields/enums/response bodies unmirrored;
  60 operations whose spec body is `{}`; 79 `/radar/*` left deliberately; `zone-settings` with no
  product file; `raw/docs-oficiais/` two months stale.

---

## 2026-08-25 (d) — the gate now reports what it could NOT read

Chosen over closing the Terraform/Pulumi block, and for a reason this day kept demonstrating: the
danger here is not missing coverage, it is **a green report that reads as more complete than it
is**. The invented Zaraz trigger survived a cleanup with the gate green. The invented Workers AI
error codes sat in a file that passed every check that existed.

**What changed.** Every product line now carries the share of the file the gate could actually look
at, and the run ends with a ranked list of the least-audited files.

```
✅ waf        31/31 confirmed ·  59% of  47 claims audited · 161 pages
✅ wallets    10/10 confirmed ·  35% of  31 claims audited ·   2 pages
```

**The headline number: 41% of 3,866 claim blocks across 89 product files carry nothing
checkable** (50% before the slug fix below).* Half of this skill is prose the gate cannot see, and until today the report implied
otherwise by saying only "confirmed".

**The demonstration that settled the design.** `wallets.md` reports 10/10 confirmed at 35% audited.
Printing the *unaudited* blocks showed that **all ten facts hand-verified against the FAQ earlier
today — handle free, one per account, no transfer ever, reservation ≠ access, Cloudflare may
reclaim — sit in blocks the gate does not audit.** The ten things it confirms are not the ten
things that matter in that file. A confirmation rate answers "were the quotable bits right", never
"is the file right", and those two questions can share a file without overlapping at all.

**Unit is a claim block, not a line.** A bullet wrapped over three lines is one assertion; counting
lines would have penalised the gate for a text width and reported `waf.md` at 44% instead of 59%.
Headings, the `## Contents` navigation, table separator rows and fenced code blocks are excluded —
code blocks deliberately, since extraction skips them by design and counting them would understate
the tool against its own rule.

**Validated by reading, not by trusting the number** — the measure was checked by printing every
block it called unaudited and confirming each genuinely carries no quotable token. That is also how
the wrapped-line distortion surfaced.

**And that validation was not enough — the first version of this entry published a wrong list.**
The check had been run on ONE small file (`wallets.md`), and the conclusion was generalised to 105
files of different shapes. Re-running the same read-it check on the two files the report called
*blindest* showed the percentage was an artifact of the extractor, not a property of the files:
`learning-paths.md` and `reference-architecture.md` are mostly **catalogues of slugs in bold**
(`- **replace-vpn** — replace a legacy VPN…`, `- **sase** — Evolving to a SASE architecture…`), and
bold extraction only accepted Title Case, so every lowercase slug was dropped. Those slugs are as
checkable as any backticked identifier. With them included:

| file | before | after | confirmed |
|---|---|---|---|
| `learning-paths` | 13% | **65%** | 22/23 |
| `reference-architecture` | 13% | **75%** | 33/33 |

Overall audited coverage moved **50% → 59%**, and the files below 25% went from eight to two. The
superseded "least audited" list in this entry named six files that were never blind. **A measure
validated on one shape of file says nothing about a corpus of many shapes** — the same mistake, one
level up, as trusting a green report because the tokens it could read were fine.

**The two that survived the recheck are genuinely prose:** `google-tag-gateway` 17% and `ai` 21%.
Their unaudited blocks were read one by one — explanatory sentences ("You run Google measurement…",
"Your site is already proxied through Cloudflare…") carrying no quotable token. Honest readings.

**Least audited, after the correction** — the map for the next curation pass, because prose with
nothing quotable is where a fabrication survives: `google-tag-gateway` 17% · `ai` 21%. Next tier,
all above 25% and all read-checked as genuine prose rather than extractor blindness: `billing` 29%,
`version-management`, `privacy-gateway`, `argo-smart-routing`.

**Deferred** (the backlog)

- **`**Term** — gloss` is treated as a label and skipped**, which is right for a curator's own
  heading (`**Detection vs mitigation** —`) and wrong for a product name (`**AI Gateway** —`).
  No mechanical rule separates them; the label filter was kept because it demonstrably prevented
  three false alarms on hand-verified files, at the cost of some coverage in files like `ai.md`.
- **The fraction is now measured but nothing acts on it.** No threshold fails a run, and no pass has
  yet rewritten a thin file to be more quotable. The eight files above are the obvious start.
- **A high fraction is not a safety rating.** It says the gate could read most blocks, not that the
  unread ones are fine — and a file can be 100% audited and still frame every fact misleadingly.
- **Terraform / Pulumi registry corpus** — still the largest single block of expected-out-of-corpus
  tokens (`terraform` 22/36, `pulumi` 32/40). Deliberately not done this pass.
- **`think` still SKIPPED**, wholly unverified, and still 169 lines against a ≤150 cap.
- Carried over: optional fields/enums/response bodies unmirrored in API slices; 60 operations whose
  spec body is `{}`; 79 `/radar/*` operations left deliberately; `zone-settings` with no product
  file; `raw/docs-oficiais/` two months stale.

---

## 2026-08-25 (c) — working the baseline down: four fabricated facts found and removed

First pass through the debt the new gate exposed. Started at the two worst confirmation rates
(`zaraz` 8/19, `workers-ai` 33/42) as agreed with the operator.

**Fabricated content found and corrected** — none of it flagged by any previous check, because
until today nothing read these files against the source.

- **`zaraz.md` — debug API invented.** The file said *"Debug with `zaraz.debug = true` then inspect
  `zaraz.tools`"*. Neither exists. Real procedure: copy the **Debug Key** from Settings, run
  `zaraz.debug("YOUR_DEBUG_KEY")` in the console to set the `zarazDebug` cookie; `zaraz.debug()`
  with no argument exits. There is no `zaraz.tools` object — the five apparent hits were
  `zaraz/tools-config` dashboard URLs. Rewritten from the Debug mode page.
- **`zaraz.md` — a trigger type that does not exist.** The file told the reader to *"use a **History
  Change** trigger (auto-detects `pushState`/`replaceState`)"*. Zaraz has exactly six rule types —
  Match rule, Click listener, Element Visibility, Scroll depth, Form submission, Timer — and no
  history/route-change rule. Cloudflare publishes **no SPA guidance for Zaraz at all**. Replaced
  with what actually works: call `zaraz.track()` on navigation and build a Match rule on it.
- **`zaraz.md` — three limits with no source.** *"event/request size 100 KB · consent purposes 20 ·
  API rate ~1,000 req/s"* — zero support anywhere in the Zaraz corpus. Removed; Zaraz documents
  pricing tiers and event volumes, not per-request limits. Also softened the matching performance
  gotcha, which quoted the same phantom 100 KB.
- **`workers-ai.md` — an entire error-code family invented.** The file listed `7502` model not
  found, `7504` input validation, `7505` rate-limited, `7506` context exceeded. **No such codes
  exist.** The real table is 3xxx/5xxx: `5007` no such model · `3042` invalid model ID · `3003`
  incomplete request · `3006` too large · `3007` timeout · `3036` daily free neuron allocation
  used up · `3040` out of capacity · `5035` requires Workers Paid · `5016` model terms not accepted,
  each with its HTTP status. This is the worst class of error in a skill like this: an agent
  debugging a real failure would have looked up a code that never existed.
- **`agents.md` — a package subpath that does not exist.** `useAgentChat` was attributed to
  `agents/ai-react`. It comes from `agents/react`. Corrected, and the other real subpaths added
  (`agents/client`, `agents/mcp`, `agents/workflows`, `agents/email`).

**Stale, not invented** — corrected the same pass

- `workers-ai.md` typed the AI binding from `@cloudflare/workers-types`; current guidance is
  `wrangler types` → `worker-configuration.d.ts`, re-run on config change.
- `workers-ai.md` said local dev *"needs `wrangler dev --remote`"*. The docs' actual point is
  sharper and costs money: there are no local GPUs, Workers AI **always** reaches the account, so
  **local development incurs usage charges**. That is a billing surprise, not a flag to pass.
- `zaraz.md` quoted e-commerce events as the shorthand `Product Viewed/Added/Removed`; replaced
  with the ten real event names.

**Seven instrument fixes** — every one found by looking at a NOT FOUND and asking whether the tool
or the file was wrong. Six times it was the tool.

1. **Multi-word doc terms were never checked.** The token filter demanded an identifier character,
   so every quoted Cloudflare noun-phrase (`Order Completed`, `Click listener`) was silently
   dropped. Coverage lost without any signal — the failure a gate is least able to report on
   itself. Title Case phrases of 2–4 words are now checked; `zaraz` alone gained 10 tokens.
2. **Shared vocabulary across products.** `worker-configuration.d.ts` in `workers-ai.md` is correct
   and current, and absent from the Workers AI corpus by construction. Workers, Wrangler and
   Fundamentals are now a **fallback** corpus — a token found there is confirmed, never invented.
3. **REST endpoints were measured with the wrong ruler.** `GET /user/tenants` will never appear in
   the tenant docs prose; it either exists in the OpenAPI spec or it does not. Endpoints now check
   against the spec, matching on literal segments so `/rum/site_info/list` matches the templated
   `/accounts/{id}/rum/site_info/list`. (First attempt read the spec stamp from the wrong path and
   silently found nothing — caught only because the numbers did not move.)
4. **Escaped backticks produced garbage tokens.** A span like `` `this.sql\`…\`` `` was captured
   wrong, so a fragment of prose got reported as a missing token. Dropped.
5. **Bold terms were invisible.** The extractor read inline code spans only. This is not a
   hypothetical gap: the Zaraz *History Change* fabrication survived the first cleanup **because
   the second occurrence was bold rather than backticked**, while the identical fabrication three
   lines below it, in backticks, was caught. Found only by grepping the installed file for the old
   string after closing — the gate itself had gone green. Title Case bold phrases are now checked,
   which is where most of the +242 confirmed tokens came from.
6. **...but bold in label position is excluded.** `- **Detection vs mitigation:** …` is the
   curator's own structure, not a quotation; three such labels on hand-verified files proved it.
7. **Plurals.** A feature written in the plural (`Context Enrichers`) quotes a singular the docs use
   (`Context Enricher`); the singular is now accepted instead of reported.
8. Markdown-escape normalisation and the placeholder/pointer filters from entry (b) stayed as-is.

**A second fabrication in the same file, found after the gate went green.** `zaraz.md` listed the
invented *History Change* trigger **twice** — once in Gotchas (backticked neighbourhood, caught) and
once in the Triggers section in bold, which the extractor could not see. It was found by grepping
the installed file for the old string as a closing check, not by the tool. The trigger list is now
the six verbatim rule types, including the Click listener footgun (omit the `#`/`.` in a CSS
selector and it silently never fires). **The lesson is the gate's own shape: it reports on what it
can read, and a green report is bounded by the extractor's reach, not by the file's correctness.**

**Result:** **2,161 confirmed · 190 not found** across 5,033 live pages — 242 more tokens actually
checked than at the start of the pass, which is why the raw not-found count moved 172 → 190 while
the files got *more* correct. Confirmation rates: `zaraz` 8/19 → 28/29 · `workers-ai` 33/42 → 45/51
· `agents` 61/70 → 70/78 · `wallets` 6/7 → 10/10. The three hand-verified files ended clean at a
wider aperture (`waf` 31/31, `workers` 57/57, `wallets` 10/10) — the only evidence that the widened
filters bought coverage rather than noise.

**Deferred** (the backlog)

- **172 tokens still unreviewed**, now dominated by two classes that are *expected* to be
  out-of-corpus rather than wrong: **third-party registry vocabulary** (`terraform` 22/36,
  `pulumi` 32/40 — resource names like `cloudflare_pages_project` and `R2Bucket` live in the
  Terraform and Pulumi registries, not on developers.cloudflare.com) and **curator synthesis**
  (`BrowserRouter`, `useEffect`, `pushState` — general web vocabulary). Neither has an instrument
  yet. Next-worst genuine products: `web-analytics` 22/28, `tenant` 37/43, `r2-sql` 13/19,
  `pages` 29/35, `artifacts` 25/31, `load-balancing` 22/27.
- **A registry corpus for `terraform` / `pulumi`** would close the single largest remaining block.
  Not attempted this pass.
- **`think` is still SKIPPED** — no readable `llms.txt`, so `think.md` remains wholly unverified
  and is also 169 lines against a ≤150 cap. Unchanged from entry (b).
- **Prose is still unchecked, by design.** Every fabrication found today was a *token* — an API
  name, a code, a subpath. A fact that is individually quotable but framed misleadingly would still
  pass green, and that is the failure this gate structurally cannot see.
- **Anything the extractor cannot read is unaudited, and the report does not say so.** Plain-text
  claims — a number in a sentence, a feature named without backticks or bold — are invisible. The
  totals line reports tokens checked, never the share of the file that carried no checkable token.
  A per-file *audited fraction* would make that honest; not built.
- **Nothing re-verifies a fix.** Today's corrections were checked by re-running the gate, which
  proves the tokens now appear in the docs — not that the surrounding sentence is right.
- Carried over, untouched: optional fields/enums/response bodies unmirrored in API slices; 60
  operations whose spec body is `{}`; 79 `/radar/*` operations left deliberately; `zone-settings`
  with no product file; `raw/docs-oficiais/` two months stale.

---

## 2026-08-25 (b) — `scripts/verify-products`: the product files finally have a gate

**Closes the top backlog item**, open since 2026-06-26 and restated every pass since: the health
gates read `references/api/` against the OpenAPI spec, and **nothing checked the product files at
all**. A `products/*.md` could carry a dead price, a renamed package or an invented limit
indefinitely.

**What it does** — for each product, fetch its whole live doc corpus from the product's own
`llms.txt` index, extract the *quotable* tokens from the product file (inline code spans and
numbers with hard units), and report each as CONFIRMED or NOT FOUND.

**What it deliberately does not do.** It checks **presence, not truth**. NOT FOUND is a prompt to
look, never a verdict — a token legitimately goes missing when Cloudflare rephrases a page, when
the fact came from a blog post or the spec rather than the docs, or when the curator wrote a
synthesis rather than a quote. Prose framing is out of scope and always will be; no string match
adjudicates "the positive-security counterpart to attack score". Claiming otherwise would be worse
than having no gate, because a green report would read as *everything here is right*.

**Calibrated on labeled data before the sweep**, per the rule that a proxy is worth nothing until
you open one item and confirm it measures what you think. `waf.md`, `wallets.md` and `workers.md`
had just been fact-checked by hand, 33/33, so a good extractor had to score ~clean on them. The
first draft scored 11 NOT FOUND on those three. **All 11 were extractor greed, not stale facts** —
placeholder notation (`phases: [...]`, `ctx.waitUntil(p)`), skill-internal pointers
(`docs-oficiais/…`, `gotchas.md`), globs, and money-per-period units the docs phrase in prose.
Filtered each class, with the reason written into the code so the next reader does not re-add them.

**Two real bugs found by calibration, both fixed:**

- **Markdown escaping broke matching.** Inside tables the docs write `eth\_getBalance`, so a
  literal search for `eth_getBalance` missed nine Ethereum JSON-RPC methods **that were on a page
  the tool had fetched correctly**. The corpus is now unescaped before matching. This is the same
  shape as the round-one miss during the hand check — a NOT FOUND that was an instrument defect,
  not a content defect. Corpus completeness and matcher fidelity are the two ways this tool lies.
- **`waf.md` stated a max expression-length figure that is sourceable nowhere** — not in the live
  WAF docs, not in `ruleset-engine`, not in the OpenAPI spec (0 `expression` properties carry a
  `maxLength`). Pre-existing, not from this week's curation. **Removed**, with a line saying it was
  removed and why. First defect this gate caught, on its first real run.

**Seen failing before being trusted.** Three defects planted in scratch copies, all three flagged,
all three green again after restore: a learning threshold changed 10,000 → 15,000; the field name
`cf.schema_validation.learned.violated` corrupted to `.learnt.`; and the package renamed to a
plausible `@cloudflare/vitest-pool-plugin`.

**Baseline recorded** in `references/_verify-baseline.json`: **1,773 confirmed · 280 not found ·
5,033 live pages fetched** across 89 product files. Cold run ~5 min, cached ~4 s. The 280 are
accepted as-is, not endorsed — they are the starting debt, and the gate fails only on *new*
not-found tokens, so the first run does not produce a wall that trains the reader to skip it.

**Wired into `scripts/refresh` phase 1**, so it runs every week alongside the API gates.

**Deferred** (the backlog)

- **The 280 baseline tokens are unreviewed debt.** Nobody has looked at them one by one. Some are
  certainly curator synthesis (`pushState`, `useEffect` in `zaraz.md` are general web concepts, not
  Cloudflare's text); others may be genuinely stale (`zaraz.tools`, `zaraz.debug = true`, the
  `7502`–`7506` Workers AI error codes). **Worst offenders by confirmation rate: `zaraz` 8/19 and
  `workers-ai` 33/42.** Working that list down is the natural next pass.
- **`think` is SKIPPED — its corpus could not be built** (no readable `llms.txt` index; it is a
  preview product). It is reported as SKIPPED rather than scored, because a check that did not run
  must never look like a check that passed. `think.md` therefore remains entirely unverified, and
  it is also the file already known to be 169 lines against a ≤150 cap.
- **Prose is unchecked, by design.** The largest class of possible error in these files — a correct
  fact framed misleadingly — has no gate and will not get one from string matching.
- **`llms.txt` is trusted as a complete index.** It held up under the one spot-check run
  (`web3`'s supported-api-methods page was in it), but a page missing from a product's index is
  invisible to this tool and would surface as a false NOT FOUND.
- Carried over, untouched: optional fields/enums/response bodies unmirrored in the API slices; 60
  operations whose spec body is `{}`; 79 `/radar/*` operations left deliberately; `zone-settings`
  with no product file; `raw/docs-oficiais/` two months stale.

---

## 2026-08-25

**Detected** — `live=106 known=105`; API spec 5 days old; installed vs workbench in sync; health
gates all green against the 2026-08-17 baseline (0 phantom · 0 stale · 0 gap · 0 double-claimed ·
688/688 bodies).

**Curated** — three items, chosen from the drift report by the human running the weekly check.

- **`products/wallets.md` (NEW, 61 lines)** — new product `wallets`, docs landed 2026-08-19.
  Written with the pre-launch caveat *first*, because that is the whole story: only **handle
  reservation** exists today (free, one per Cloudflare account, at `cloudflare.pay`), and a handle
  **cannot send, receive or hold funds**. Documented the announced two-wallet design (Account Wallet
  delegating a **capped** budget to agent-run Virtual Wallets keyed by API keys; stablecoins first)
  as *announced, not shippable*. Explicitly stated **there is no binding, no wrangler config and no
  REST surface** — an agent reading this file must not invent one — and pointed the "works today"
  path at x402 via `agents/tools/payments/`. Gotchas the FAQ states plainly: first-come, **no change
  / release / transfer ever** (including after a rebrand), reservation ≠ access on release,
  Cloudflare may reclaim any handle. No published pricing for the wallet itself.
  Added to `_known-products.txt` (sorted position, between `waiting-room` and `warp-client`) and to
  the SKILL.md catalog under *Developer platform*, flagged ⚠️ pre-launch.

- **`products/waf.md`** — curated the `waf/detections/application-profiles` subtree (+6 pages).
  Added a *Key concepts* bullet framing it as the **positive**-security counterpart to the existing
  signature/score detections: Schema Profiles model what a request should look like, learned from
  traffic or from an uploaded OpenAPI schema, detection is **always-on and never mitigates**, and you
  act through a custom rule on `cf.schema_validation.learned.violated` /
  `.uploaded.violated`. Added a gotcha covering the learning economics that decide whether this is
  usable at all (weekly runs, `2xx` only, 1,000 requests for fields / 10,000 for boundaries, up to
  7 days; no multipart/GraphQL/XML; no required-param enforcement; not an allowlist; the profile
  *drifts* each week unless you freeze it as an uploaded schema). Added the plan-gating line:
  **closed beta, invited Enterprise only** — API Security customers already have it via Schema
  Learning/Validation. 99 → 119 lines, inside the ≤120 cap.

- **`products/workers.md`** — the `@cloudflare/vitest-pool-workers` → **`@cloudflare/vitest-plugin`**
  rename (2026-08-19) plus the two new pages under `workers/testing/vitest-integration/`. Recorded
  it as a **pure rename** (API and Vitest config unchanged, subpaths included) with the codemod
  invocation, and the move of outbound-request mocking to `@msw/cloudflare`. This is why it matters:
  every pre-2026-08 instruction naming the old package is now wrong, and nothing in the skill
  mentioned either name before this pass. Rewrapped *Going deeper* to stay at exactly 120 lines.

**Dismissed, on purpose** — so it stops resurfacing as drift

- The `style-guide/*` churn (`build-the-page` +52, `style-and-grammar` +39, ~20 subtrees gone) is the
  Cloudflare **docs style guide** reorganising itself — the two "new" subtrees and the disappeared
  ones are the same move seen from both ends. It documents how Cloudflare writes docs; it is not a
  product and not a launch. Not curated, and not a gap.
- `realtime/realtimekit/ui-kit/api-reference/flutter` disappeared — noted, not investigated.

**Deferred** (the backlog)

- **CLOSED this pass:** the twice-deferred 2026-07-27 Workers *"Run integration tests against your
  Worker's production build"* item — the Vitest curation above covers `products/workers.md`; the
  separate `vitest` skill was still not touched.
- **The gates still cover `references/api/` only.** Nothing verifies the *product* files the same
  way — a `products/*.md` can state a dead price or a wrong limit and no gate notices. Unchanged and
  still the largest open item. This pass added 3 more product-file claims under that blind spot.
- **No re-slice of `references/api/`** — `wallets` has no REST surface, and Application Profiles is
  configured through the existing Rulesets API (custom rules), which `api/waf.md` already carries.
  Verified, not assumed. Spec is 5 days old.
- **Optional fields, nested shapes, enums and response bodies remain unmirrored** in the API slices.
- **60 operations declare a body the spec describes as `{}`** — unresolvable from the spec; only the
  live docs or a real call would establish them.
- **79 `/radar/*` operations remain across 6 slices** (`dns` 25, `email-service` 24, `email-routing`
  14, `bots` 13, `logs` 2, `realtime` 1) — Radar datasets about those products. Left deliberately.
- **`zone-settings` has no product file** — endpoints without guidance for whoever lands there.
- **Not curated this pass** (this pass was scoped to three items by the human): OAuth scope selection
  for Wrangler and the API MCP server, optional OAuth scopes, Browser Run concurrency increase, FUSE
  in local Containers, leaked-credential scanning of `Authorization` headers, CASB auto-remediation
  policies, Web Analytics SPA soft navigation, Durable Objects deployments view, Access
  resource-scoped roles, Tunnel origin settings in the dashboard.
- **Raw source material in `raw/docs-oficiais/` is from 2026-06-26** and is now two months stale.
  Every fact in this pass was fetched live from `developers.cloudflare.com` instead (llms-full.txt
  and `Accept: text/markdown`). Carried over — worth a re-pull before any depth pass.

---

## 2026-08-18

**Detected** — clean, and the health gates ran for the first time in a scheduled-shape pass

- `live=105 known=105`, no new doc subtrees, installed vs workbench match, API spec 3 days old.
- **Health gates green**: 0 phantom · 0 stale summaries · 0 in-scope gap · 0 operations claimed by
  two slices · request bodies 688/688. This is the first pass where those numbers were measured as
  part of the weekly run rather than because someone went looking.
- Changelog since the 08-17 pass: one entry, `WAF Release 2026-08-17` — routine, not curated.

**Curated** — nothing. There was nothing to curate, and the gates say so with numbers rather than
with the absence of a complaint.

**Closing yesterday's pass**

- The 08-17 pass was written up but never formally closed: `refresh --close` was blocked by this
  session's permission classifier, so the page baseline was never re-recorded. The operator added
  four `Bash(...)` allow rules for the skill's scripts on 2026-08-18 and the command now runs.
- Note for the record: the deferred item "`refresh --close` never ran" belongs to 08-17 and is
  resolved by this entry, not carried forward.

**Deferred** (the backlog)

- **The gates cover `references/api/` only.** Nothing verifies the *product* files the same way — a
  `products/*.md` can state a dead price or a wrong limit and no gate notices. Same blind spot, one
  layer up. This is the largest open item and the natural next pass.
- **Optional fields, nested shapes, enums and response bodies remain unmirrored** in the API slices.
- **60 operations declare a body the spec describes as `{}`** — unresolvable from the spec; only the
  live docs or a real call would establish them.
- **79 `/radar/*` operations remain across 6 slices** (`dns` 25, `email-service` 24, `email-routing`
  14, `bots` 13, `logs` 2, `realtime` 1) — Radar datasets about those products. Left deliberately.
- **`zone-settings` has no product file** — endpoints without guidance for whoever lands there.

---

## 2026-08-17

**Detected** (weekly drift check — all three checks ran and reported)

- **No structural drift**: `live=105 known=105`, fetched live from `developers.cloudflare.com/llms.txt`
  at 11:36 UTC. Re-counted independently of the script against the same download and diffed
  item-by-item, not by total: zero difference (a crude `[a-z0-9-]` grep misses `1.1.1.1`; the
  detector does not).
- **No new doc subtrees**, and installed vs workbench matched at pass start. API spec 2 days old.
- **Nothing left to curate from the week's changelog** — all four in-catalog items were already
  curated on 08-14/08-15: Access on Workers, Artifacts data localization, CT Monitoring GA, Realtime
  DataChannel. Verified by grepping the product files, not assumed. The rest of the feed is
  Cloudflare One / Gateway / WAF, out of catalog.

**Curated** — one thing, and it is a scope marker, not content

- **`radar` added to `OUT_OF_CATALOG` in `scripts/reconcile-api`.** Radar was dropped from the catalog
  on 2026-06-26 ("Consumer services", data licensed CC BY-NC 4.0 / non-commercial) and recorded in
  `CATALOG-removed.md`, but that set — whose comment says *keep in sync with CATALOG-removed.md* —
  never received it. So 46 `/radar/*` operations were reported as an **in-scope gap** every week and
  carried in the backlog as work to do, when the decision to exclude them was two months old.
  **In-scope gap: 168 → 122.** This is a reporting fix; no endpoint coverage changed.
- Operator confirmed the exclusion this pass after reviewing what Radar actually offers (URL Scanner,
  domain rankings, bot-class data, outage centre): not relevant to this operation.

**Second pass, same day — measuring the rest of the 26-06 removals, and a correction**

The deferred item below ("the other removals may have the same desync") was measured instead of
carried. **The premise was wrong, and finding that out cost a near-miss.**

- **`CATALOG-removed.md` is not a reliable statement of what is out of the catalog.** It records the
  intent of 2026-06-26; `SKILL.md` is the catalog. Cross-checking the two, **5 of the products listed
  as removed are still in `SKILL.md` and still have curated `products/*.md` files**: Speed, Web
  Analytics, Smart Shield, Billing, Registrar. Only Radar, `1.1.1.1` and WARP Client actually left.
  So "listed in CATALOG-removed" does **not** imply "excludable from the gap".
- **The near-miss:** acting on that wrong premise, three product files (`web-analytics.md`,
  `speed.md`, `registrar.md`) were overwritten with freshly written ones before anyone checked
  whether they already existed. They did, and the existing ones were **better** — richer gotchas,
  transfer/renew flows, CSP and SPA specifics. Recovered intact from the installed copy (which had
  not been promoted yet) and restored. **Only additive grafts were then applied.** The rule that
  failed: read before write, and the existing artefact has precedence.
- Consequently **`smart_shield` and `billing` were NOT added to `OUT_OF_CATALOG`** — both are curated,
  catalogued products. Their 3 uncovered operations are an ordinary gap, not noise.

**Curated (second pass)** — additive grafts onto the three restored files, ~40 lines total

- `web-analytics.md`: corrected the claim that the product is **dashboard-only with no public data
  API** — 13 REST operations exist under the `rum` root (site + rule CRUD); it is the *metric data*
  that is GraphQL-only. Added the endpoint list, and made the **absence of UTM parameters** explicit
  as the reason it cannot replace GA4 for a paid-traffic operation.
- `speed.md`: added the **10 `speed_api` operations** — the file previously said to run tests from the
  dashboard, when scheduling, history and the Core Web Vitals `trend` endpoint are all scriptable.
  Added: quota table starts at Pro (**Free is not listed**), 21 test regions counted today (the file
  said 22), and a gotcha that **Rocket Loader is hostile to pixels/GTM** — a defer-and-reorder pass is
  the first thing to check when conversions drop after a "performance fix".
- `registrar.md`: added **no `.br`/`.com.br`** (registro.br is exclusive — decides most local
  projects), the async `registration-status` polling, `GET /extensions` and the fact that the API
  supports fewer TLDs than the dashboard, plus the beta gaps (no renewal/transfer/contact update).
- **No API slice claims the `rum`, `speed_api` or `registrar` roots**, so parameters and bodies are
  still not mirrored in `references/api/`. Stated as such inside `web-analytics.md` rather than left
  for the reader to discover.

**Third pass, same day — the API slices, and two root collisions they exposed**

Counted before acting: not 36 missing operations (an assumption), and not 25 — **19**, because
`registrar.md` already listed 11 of 13 and `pages.md` already carried 6 of Speed's 10.

- **New slice `web-analytics.md` — 13 operations.** They live under the `rum` root, which is why no
  slice had ever claimed them.
- **New slice `speed.md` — 10 operations.** Observatory's surface, including the 4 (`availabilities`,
  `schedule/*`) that no slice had ever listed.
- **`registrar.md` 11 → 13** (`extensions`, `extensions/{extension}`).
- **Two root collisions found and fixed via `NOT_MINE`** — both were hiding work by making it look
  covered:
  - `pages` claimed `/zones/{zone_id}/speed_api/*` because the matcher read "a tested **page**" as
    Cloudflare Pages. Moved to `speed`; `pages` 27 → 23 ops.
  - `rules` claimed the 5 `/rum/v2/{ruleset_id}/rule*` operations — those are **Web Analytics rules**
    (which paths get the beacon), not traffic rules. This is exactly why the gap fell by 14 and not
    19 on the first re-slice. Moved to `web-analytics`; `rules` 79 → 76 ops.
- **Verified after, not assumed**: `slice-api --validate` → no slug lost coverage · `reconcile-api` →
  0 phantom endpoints, 0 summaries diverging · covered 1682 → **1696** · in-scope gap 122 → **108** ·
  cross-slice duplicates back to **10** (the known `alerting` + `radar` pair, unchanged by this pass).

**Fourth pass, same day — the small gaps and the last duplicates. Duplicates now zero.**

- **27 uncovered operations across 10 segments, all claimed**: Email Sending suppressions (7 →
  `email-service`), analytics `query/{dataset}` + data-security queries (6 → `analytics`), Pages
  direct-upload assets (3 → `pages`), Workers observability metrics export (3 → `workers`), AI
  `tomarkdown` (2 → `workers-ai`), Hyperdrive integration signature (1), billing usage (1), Stream
  usage (1), organization shares (1 → `resource-tagging`), Smart Shield settings (2 → new slice).
- **New slice `smart-shield.md` — 2 operations.** Deliberately just the settings pair.
- **All 8 remaining cross-slice duplicates resolved** — `alerting/v3/policies*` was claimed by
  `email-service` because the policy URLs contain `/email/unsubscribe`. Alert policies are the
  Notifications product; `email-service` now excludes the `alerting` root. **This closes the
  10-duplicate item carried in the backlog since 2026-08-08.**
- **A duplicate created and caught inside the same pass**: seeding `smart-shield` dragged in Health
  Checks and Cache Reserve Clear, which Cloudflare files *under* `/smart_shield/` and which
  `health-checks`/`cache` already own — 8 new duplicates. Excluded via `NOT_MINE` before promoting.
  Measuring after each step, not only at the end, is what caught it.
- **Verified**: `slice-api --validate` → no slug lost coverage · `reconcile-api` → 0 phantom, 0
  diverging · **listed 1,571 = covered 1,571, i.e. zero operations claimed by two slices** — a first
  for this corpus · in-scope gap 108 → **81**.

**Fifth pass, same day — the last four families. In-scope gap now zero.**

- **Workers Builds (20 → `workers`)**, across 5 roots: `builds/builds`, `triggers`, `tokens`, `repos`,
  `account/limits`. `workers` 123 → 143 ops.
- **Logpush transformers (8 → `logs`)**, `logs` 61 → 69.
- **Account-level Load Balancers + `/user/load_balancers/regions` (8 → `load-balancing`)**, 54 → 62.
- **New slice `zone-settings.md` — 42 operations.** The `/zones/{zone_id}/settings/*` surface. It is
  deliberately **not** a product file: the toggles belong to Speed, Cache, SSL/TLS and Images, each of
  which explains its own. The slice exists so the endpoints are reachable; its note says so, and warns
  the slice churns faster than the rest of the corpus.
- **3 account-level settings → `images`** (`ut-billing`, `transformations` — Unique Transformations
  billing is an Images concern, not a zone toggle).
- **One duplicate created and caught in-pass again**: the broad `/zones/{zone_id}/settings` root
  swallowed all 10 of Zaraz's operations, which live at `settings/zaraz/*`. Excluded via `NOT_MINE`
  before promoting; `zone-settings` 52 → 42.
- **Final state, measured after promotion**: listed **1,652** = distinct **1,652** → **0 duplicates**;
  **in-scope gap 0**; `slice-api --validate` no slug lost coverage; `reconcile-api` 0 phantom, 0
  diverging summaries. Corpus coverage 50% — the remainder is out-of-catalog by decision.

**Sixth pass, same day — request bodies. New script `scripts/slice-bodies`.**

- **All 688 listed operations that declare a request body now carry its top-level required fields**
  inline: `· body: name:string, sql:string`. Coverage of that set is **688/688**.
- **Deliberately narrow.** Top-level *required* fields only — not optional fields, nested shapes,
  enums or responses. A full render of a Workers script upload is hundreds of lines of binding
  metadata and would bury the endpoint list it hangs off. The required fields are the part that
  cannot be guessed and the part that fails the call at request time. `references/api/` grew
  312 KB → 352 KB, which is the whole point of stopping there.
- **Written as a separate script, not folded into `slice-api`.** Existence of an endpoint is a flat
  question; a body is a graph — a `$ref` into one of the spec's **6,660** component schemas, often
  cyclic. They fail differently, so a failure in the hard half must not take down the easy half. The
  resolver walks `$ref`/`allOf`/`oneOf` with a cycle guard and a depth cap.
- **60 operations declare a body the spec then describes as `{}`** (mostly DELETEs). They are marked
  `(spec carries no schema — check the docs)` rather than left bare: "absent from this reference" and
  "the spec is silent" are different facts, and a bare line would report the second as the first.
- **A destructive interaction found and closed**: `slice-api` rebuilds every line from the spec, so a
  re-slice **silently strips the body column** — the slices still look complete, and the loss would
  only surface as a wrong API call weeks later. Reproduced deliberately (d1: 7 → 0 → 7), then chained
  `slice-bodies` after `slice-api` inside `refresh --close --spec`, with the constraint written into
  both scripts' headers for anyone re-slicing by hand.
- **Verified after**: 0 phantom, 0 diverging summaries, in-scope gap still 0, no slug lost coverage.

**Seventh pass, same day — the fix for the failure itself: health gates in the weekly run**

Everything above was cleanup. This is the part that stops it recurring.

**The diagnosis:** the weekly check measured the easy thing (new product slugs, new doc pages) and
reported "no drift — skill up to date". True, and useless: a wrongly-filed endpoint does not read as
a defect, it reads as coverage. The instrument that could see it (`reconcile-api`) **already existed
and simply was not part of the weekly run**. The failure was not a missing tool, it was a check that
never ran.

- **`reconcile-api` gained section 3, health gates**, with today's numbers as a recorded baseline —
  all zero: phantom endpoints, stale summaries, in-scope gap, operations claimed by 2+ slices, bodies
  missing. Plus `request bodies documented: 688/688`. **Any deviation exits non-zero.**
- **Compared with `!=`, not `>`.** A negative count is not "better than baseline" — it means the
  measurement itself broke. Passing that silently would be this exact class of bug again.
- **`refresh` phase 1 now runs the gates every week**, resolving the spec path recorded in
  `_spec-version.txt` (relative to the workbench when needed — the first run skipped itself on that
  cosmetic detail).
- **When the gates cannot run, they say so loudly** and tell the reader not to call the pass clean on
  the product diff alone. A check that did not run must never look like a check that passed — that is
  precisely how 2026-07-21 gave a false all-clear.
- **Verified adversarially, twice, end to end**: injecting a duplicate line → `operations claimed by
  2+ slices: 1`, exit 1. Corrupting one summary → `stale summaries: 1`, and `scripts/refresh` printed
  `🚨 health gates FAILED — this pass is NOT clean, whatever the product diff says`. Clean state
  before and after both tests: exit 0. **A gate that has only ever been seen passing is not a gate.**
- The scheduled weekly task needs no edit: its file invokes `~/.claude/skills/cloudflare-atlas/
  scripts/refresh` (line 14), which is the binary carrying the gates — confirmed by reading the task
  file and the script's mtime, not assumed.
- **Proven on a real regression, not only on an injected one.** Injected tests are worth little: they
  are cleaned up immediately and never resemble how the failure actually arrives. So the gates were
  run against the failure mode that genuinely occurs in this workflow — a plain `slice-api <spec>`,
  a legitimate step someone will run by hand. Result: `bodies missing 688`, `request bodies
  documented: 0/688`, **exit 1**, and the weekly command printed `🚨 health gates FAILED — this pass
  is NOT clean`. A second gate (copy sync) fired independently. Recovered with `slice-bodies`; the
  full weekly run then returned exit 0 with all five gates green and 688/688. Logs of both runs kept
  for this session under the scratchpad.

**Deferred** (the backlog)

- **The gates cover `references/api/` only.** Nothing yet verifies the *product* files the same way —
  a `products/*.md` can claim a wrong limit or a dead pricing model and no gate will notice. That is
  the same shape of blind spot, one layer up.
- **Optional fields, nested shapes, enums and response bodies remain unmirrored.** The new column
  narrows the guessing; it does not replace `/api/resources/<product>`. Every touched slice says so
  in its header.
- **The 60 empty-schema operations are unresolved at the source** — the spec itself carries nothing.
  Only the live docs or a real call would establish those bodies.
- **79 `/radar/*` operations remain across 6 slices** (`dns` 25, `email-service` 24, `email-routing`
  14, `bots` 13, `logs` 2, `realtime` 1) — Radar datasets *about* those products. Left deliberately;
  removing them is a scope call.
- **`zone-settings` has no product file.** Deliberate, but it means a reader who lands on a toggle
  there gets endpoints without guidance. Revisit if the slice starts being used to answer questions.
- **`scripts/refresh --close` never ran** — blocked by this session's permission classifier. Promotion
  and both verifications were performed by hand with the same tools; the page baseline was NOT
  re-recorded. Nothing new appeared in the page diff this week, so the baseline is still valid, but
  the pass has no formal close stamp.
- ~~A `radar.md` API slice still exists with 154 operations.~~ **Deleted 2026-08-17** at the
  operator's call, closing the scope decision opened this morning. Verified after: no slug lost
  coverage, 0 phantom endpoints, 0 diverging summaries. Listed operations 1,706 → 1,552; corpus
  coverage 51% → 46%, which is the honest number now that the skill no longer claims a product it
  does not carry. `slice-api` iterates over existing files, so the slice will not regenerate.
  **Not resolved by the deletion — 79 `/radar/*` operations remain, spread across 6 other slices**
  (`dns` 25, `email-service` 24, `email-routing` 14, `bots` 13, `logs` 2, `realtime` 1). These are
  Radar *datasets about that product* (DNS trends, email threat trends), reached through roots those
  slugs legitimately own, and `reconcile-api`'s own comment cites `bots.md` listing Radar endpoints
  as correct. Removing them is a separate scope call and was NOT taken.
- **Request/response bodies are still not mirrored** for any slice — only method, path, summary and
  required parameters. A slice can name the right endpoint and still mislead about the payload.
- **Re-derive the true out-of-catalog set from `SKILL.md`, not from `CATALOG-removed.md`.** Only
  `radar` was verified both ways this pass. `1.1.1.1` and WARP Client appear genuinely gone but were
  not checked for API segments; the `network-*` / BYOIP family was not checked at all.
- **Reconcile `CATALOG-removed.md` with `SKILL.md`** — five entries in it describe a removal that was
  reverted, with no note saying so. It reads as authoritative and is not.
- **122 in-scope operations remain under roots no slice claims.** `settings` (45, Zaraz) and `builds`
  (20, Workers) are two thirds of it. Each needs a root added deliberately. Re-measure with
  `scripts/reconcile-api`.
- **10 operations listed by two slices at once** — `alerting/v3/policies*`. Ownership is a scope call.
- **`rules.md` owns 24 `cloudforce-one/*` paths.** Cloudforce One is threat intel, not Rules. Removing
  them would drop 24 paths with no `cloudforce-one` slice to receive them. Pre-existing; needs a scope
  decision, not a patch.
- **Verifying slices against the running API remains unsolved** — would need an authenticated call per
  endpoint, interpreted per product. Worth it for a handful of high-traffic endpoints, not for 1,692.
- Carried untouched from 08-15/08-08: Radar AS-level connectivity + Researcher beta (now permanently
  moot — out of catalog), Cloudflare Mesh container image, Access authorization cookies, publisher
  verification on OAuth consent. Out-of-catalog items are recorded in the 08-15 entry.

---

## 2026-08-15

**Detected** (weekly drift check — all three checks ran and reported)

- **No structural drift**: `live=105 known=105`. No new product, no product gone.
- **No new doc subtrees.** Nothing launched hidden inside an existing product this week.
- **7 subtrees gone** (renamed/merged/retired): `cache/plans`, `dns/reference/all-features`,
  `ssl/reference/all-features`, `sandbox/guides/production-deployment` (superseded by
  `sandbox/guides/deploy`), and 3 style-guide component pages. **Grepped `references/` + `SKILL.md`
  for all 7 — zero hits outside the page baselines**, so no curated content pointed at a dead path.
- **8 routine single-page adds**, now named by the detector (the 08-08 fix paying off). Three carried
  real signal and drove this pass: `workers/configuration/cloudflare-access`,
  `artifacts/guides/data-localization`, `containers/deploy` + `sandbox/guides/deploy` +
  `sandbox/guides/preview-urls-custom-domain`.
- Installed vs workbench `diff -rq` **empty** at pass start. API spec **7 days old** (2026-08-08) —
  inside the 30-day window.
- Changelog worth acting on: Access on Workers (08-14) · CT Monitoring GA (08-13) · Artifacts data
  localization (08-13) · Realtime SFU DataChannel delivery control (08-13) · Turnstile Spin GA (08-10).

**Reconciled item-by-item against Cloudflare's own changelog feed — and it caught a miss**

Fidelity checks prove what *was* curated is right; they say nothing about what was **skipped**. So the
17 entries in `changelog/rss/index.xml` dated 2026-08-08..15 were each matched against this entry.

- **16 of 17 accounted for**: 5 curated · 4 deferred with a stated reason · 7 out-of-catalog.
- **1 was in no bucket at all: "Stream live logs from Cloudflare Tunnel in the dashboard" (08-10).**
  Not deferred, not declared out of scope — simply missed, and Tunnel is a curated product. Curated
  now into `products/tunnel.md` as the first Gotcha: **Networking → Tunnels → Live logs**, with the
  detail that matters on an HA tunnel — it **aggregates all connectors into one stream**, which beats
  `cloudflared tail` on a box for finding which replica served a request.
- **The reconciler itself over-reported once and it is worth naming:** it also flagged "Pages skips
  superseded queued builds" as missing, because the entry says "skip**ping**". First-word matching is
  crude; both flags were checked by hand against the text before acting, which is why one became a
  fix and the other became nothing.
- **Detection ≠ coverage.** The weekly drift check reads doc *pages*; a dashboard-only feature ships
  no new page, so nothing in the automated output would ever have surfaced this. It took reading the
  changelog against the write-up. Worth keeping as a step.

**Scope call made this pass, stated so it is not re-litigated every week:** the majority of this
week's changelog is **Cloudflare One / Gateway / Access-as-SASE**, a category deliberately removed
from the catalog on 2026-06-26 (see `CATALOG-removed.md`). Hostname routing GA, the new initial-
resolved-IP range, Gateway package-registry security, MCP detection, email blocked-content rules and
the One Client release are **out of scope by that decision, not by oversight**. The one item that
crossed back in is Access *on a Worker*, which is a Workers-platform feature and is curated below.

**Curated** (grounded in 10 pages pulled fresh from `developers.cloudflare.com` this pass — the
`raw/` snapshot is from 08-08 and predates all of them)

- **`products/workers.md`** — new section **"Putting a Worker behind Access"**: the four
  `destinations[].type` scopes (`all_preview_workers` / `all_workers` / `preview_worker` / `worker`)
  as a table against their dashboard equivalents, the *Previews only vs All traffic* choice, the
  `bypass` + `everyone` policy that re-publishes one Worker under account-wide Access, and the trap:
  **worker-level Access returns 403 on WebSocket upgrades** — DO/Realtime/RDP-over-WS apps must use a
  hostname-based Access app instead.
- **`products/ssl.md`** — **Certificate Transparency Monitoring, GA 2026-08-13**: opt-in and off by
  default, Cloudflare-issued certs filtered out, the two benign alert sources (self-uploaded certs;
  SAN neighbours on a shared cert), and the boundary — it does **not** detect look-alike domains, so
  it is not phishing detection. Recorded as the HPKP replacement.
- **`products/realtime.md`** — new **DataChannels** block under Key API: establish→new(local/remote)
  handshake, `negotiated: true` with the API-returned id, and the 08-13 delivery controls (`ordered`,
  `maxRetransmits`, `maxPacketLifeTime` — the last two **mutually exclusive**), `waitForAck` gating,
  and `canReply` allowing **exactly one** replying subscriber (granting it elsewhere silently revokes).
  **Number corrected: the DataChannel ack window is 30s, not the 15s this file carried** — old value
  named in place so a stale source is recognizable.
- **`products/artifacts.md`** — **data localization**: `jurisdiction: eu | us` set only at explicit
  namespace creation via `POST /accounts/{id}/artifacts/namespaces`, immutable afterwards. Flagged the
  interaction the docs leave implicit: **namespaces created implicitly by the first repo are
  unrestricted**, so a residency requirement must be satisfied before the first repo exists.
- **`products/containers.md`** — new **"Deploying"** section from the new `containers/deploy` page:
  `wrangler deploy` activates the Worker *before* the image/rollout and the steps are **not
  transactional** (new code can talk to old-image containers mid-rollout); Docker only for Dockerfile
  images; Workers Builds' non-production default is `versions upload` (code only); **preview URLs
  never exist for Containers Workers** because they implement DOs; and the explicit warning against
  repointing a non-production build command at the production Worker.
- **`products/sandbox.md`** — new **"Deploy & preview URLs on a custom domain"** section that defers
  the generic half to containers.md and keeps what is Sandbox-specific: package/image must ride the
  same release line (`--containers-rollout=immediate` for a breaking cutover), `exposePort()` needing
  wildcard DNS (`*` → `192.0.2.0` proxied) plus a `*.domain/*` route, and the **TLS depth trap** — a
  Worker on a subdomain produces second-level wildcards that Universal SSL does not cover, fixed by
  the apex, ACM ($10/mo), or a self-renewed Let's Encrypt wildcard. Also corrected a stale pointer
  reading "containers.md (when curated)" — it has been curated since 06-26.
- **`products/turnstile.md`** — **Spin GA 2026-08-10** promoted from a one-line "Going deeper"
  mention to its own section: the three paths produce an identical widget and deploy no
  infrastructure, plus the `wrangler turnstile widget create|list|get|update|delete` surface that was
  absent from this ref. Two warnings added: **`widget get --json` prints the secret** (with the
  `WRANGLER_LOG*` hardening the docs require), and Spin's automatic `localhost`/`127.0.0.1` domains
  do not excuse validating the siteverify hostname in production.

**Not curated, with the reason (so this is a decision, not a gap)**

- **`references/api/` not re-sliced.** Spec is 7 days old. Neither new API surface would have been
  captured anyway: Realtime SFU DataChannels live on `rtc.live.cloudflare.com`, outside the
  `api.cloudflare.com/client/v4` spec entirely, and **Artifacts has no slice at all** (46 slices, none
  for artifacts) — and `slice-api` derives each matcher from a slug's *existing* slice, so it cannot
  create a first slice for a product on its own. Both gaps are logged below rather than silently left.
- **Line budget:** `ssl.md` is 127 lines against the guide's 120. It was already 121 before this pass;
  the CT block adds 6. Trimming pre-existing content was out of scope for a content pass.

**Cross-check against the 81 files this pass did NOT edit** (the completeness question editing
coverage cannot answer: do untouched refs now contradict the edited ones?). Grepped all 88 product
refs for every claim this pass introduced or changed — the ack window, DataChannels, Spin, Access
destination types, preview-URL/DO exclusion, rollout flags, Universal SSL wildcard depth, ACM
pricing, CT Monitoring, `403`, Artifacts namespaces. **Three findings, all fixed:**

- **Real conflict — ACM price.** `sandbox.md` (written this pass, from the Sandbox docs page) quoted
  ACM flatly as **$10/mo**, while `ssl.md` — the cert-pricing authority in this skill — deliberately
  refuses a hard figure ("price shown in dashboard at purchase — historically ~$10/month/zone,
  confirm live"). The new text was the one out of line with the guide's pricing rule, so it now
  points at `ssl.md` instead of quoting. **A pass that only measured its own edits would have shipped
  two different ACM prices in one skill.**
- **Omission surfaced — `notifications.md`** listed the SSL/TLS alert family as cert/AOP/mTLS
  *expiry* only. CT Monitoring is a separate opt-in alert with its own recipient list, configured on
  the Edge Certificates page rather than in Notifications; added there as a pointer to `ssl.md`.
- **Duplication I created — `turnstile.md`** kept its old one-line "Going deeper" mention of
  `cloudflare:turnstile-spin` after Spin got a full section. Removed.
- Confirmed **non**-conflicts, checked rather than assumed: the other `15s` hits are Hyperdrive and
  Load Balancing timeouts, unrelated to the DataChannel ack; the other `403` hits are gRPC, Web3 and
  AI Gateway; `key-transparency.md` invokes Certificate Transparency as an analogy, not a claim about
  this feature; `pages.md` preview URLs are Pages builds, not DO-backed Workers; and `ssl.md`'s
  pre-existing "Universal covers only first-level subdomains" **corroborates** the new Sandbox TLS
  depth trap. DataChannels, Spin and the Access destination types appear in exactly one file each.

**Behavioral check — the INSTALLED skill actually answered** (grep proves a string is on disk; it does
not prove the skill routes to it and answers correctly, so this pass ran the artifact)

One agent with a **clean context**, told nothing about this pass, invoked `cloudflare-atlas` and was
asked 6 questions whose correct answers exist *only* in this pass's curation, with instructions to
answer "SKILL NÃO COBRE" rather than fall back on its own knowledge. **6/6 correct, each traced to the
right file by the skill's own routing:**

| Question | Answer given | Landed in |
|---|---|---|
| Access on a WebSocket/DO Worker — any trap? | worker-level Access → **403** on upgrade; use a hostname-based app | `workers.md` |
| Pin Artifacts data to the EU | `jurisdiction: eu` at explicit namespace creation, immutable; **implicit namespace is unrestricted** | `artifacts.md` |
| Sandbox preview URLs failing TLS on a subdomain | second-level wildcard, Universal SSL does not cover; apex / ACM / own LE cert | `sandbox.md` |
| `waitForAck` window | **30s**, and flagged 15s sources as stale | `realtime.md` |
| ACM price | hedged — "~$10/mo/zone historically, confirm live", explicitly not certified | `ssl.md` |
| Turnstile widgets from the terminal | `wrangler turnstile widget create/list/get/update/delete` + **`get --json` prints the secret** | `turnstile.md` |

The ACM row is the one that matters most: it is the **regression test for the conflict fixed above**.
The agent was asked the bare price question and landed on `ssl.md`'s hedged figure — the flat "$10/mo"
that `sandbox.md` briefly carried is gone from the answer path, which is what the fix was for.

**Stored text confirmed on disk in the installed skill**, because a correct runtime answer and a
correct file are two different claims — the skill could route to `ssl.md` and answer well while a
stale `$10/mo` still sat in `sandbox.md`, waiting for whoever reads that file directly. Read back
from `~/.claude/skills/cloudflare-atlas/`: `sandbox.md:207` now says "ACM (paid add-on, price in
`ssl.md` — confirm live)" and **`grep '\$10' sandbox.md` returns nothing**; `ssl.md:114` holds the
single hedged figure; `notifications.md:77` carries the CT pointer; `turnstile.md` mentions
`turnstile-spin` exactly once. Also fixed the ragged line wrap the ACM edit left behind.

**What this check does NOT establish**, stated so it is not over-read: it exercises 6 claims, not the
88-file corpus, and it says nothing about refs this pass did not touch. The judging agent also shares
this session's base model, so an error we both make is invisible to it — this is corroboration, not
independent verification.

**`references/api/artifacts.md` — CREATED, after the operator pushed back on the deferral**

The deferral above was written as "the matcher cannot bootstrap a first slice", which was true of the
script but was the wrong reason to stop: bootstrapping is one seed line. Corrected in this pass.

- **Seeded and sliced.** Wrote a one-line seed whose `root_of()` is
  `/accounts/{account_id}/artifacts/namespaces`, then ran `slice-api` against the same 2026-08-08
  spec every other slice came from, keeping provenance uniform. **17 operations.**
- **Blast radius measured, not assumed.** `slice-api` rewrites *every* slice, so `references/api/`
  was copied first and `diff -rq` run after: **`Only in api: artifacts.md`** — the other 46 came out
  byte-identical, confirming the re-slice is idempotent against its own spec. `--validate` then
  reported **OK — no slug lost coverage**.
- **The real finding, which the deferral would have buried:** the slice is read-only where the docs
  are not. `/artifacts/namespaces` has a `GET` and **no `POST`**, so the namespace-creation call that
  sets `jurisdiction` — curated into `products/artifacts.md` this same pass from the docs page — has
  no spec entry to corroborate it. Downloaded a **fresh spec (2026-08-15, 2,077 paths vs the 2,046 in
  the 08-08 copy)** to tell "stale copy" from "never published": **absent from both**. Artifacts is
  closed beta and its write surface is only partly published. Recorded as a `> Note:` in the slice
  (the script preserves those across re-slices) saying explicitly that **missing here ≠ does not
  exist**, plus a pointer from `products/artifacts.md` so nobody reads the slice's silence as denial.

**Full re-slice against the fresh spec — RUN (operator said "geral")**

- Downloaded spec stamped **2026-08-15** (2,077 paths vs 2,046 on 08-08); old copy kept at
  `/tmp/openapi-0808-backup.json`, `references/api/` backed up before the rewrite.
- **`--validate` against the new spec first, before writing anything: no slug lost coverage.**
  Deltas, all additive: `rules` +9 · `workers-ai` +2 (finetunes) · `queues` +1
  (`messages/extend`) · `email-service` +1 (subdomain reputation complaints). 42 slices unchanged.
- `_spec-version.txt` re-stamped 2026-08-15.

**Silent-truncation bug in `slice-api`, found by walking into it** (this is the pass's real find)

The re-slice ate the `> Note:` block that had just been written into `artifacts.md`, leaving a
sentence cut at "Artifacts is closed". The preserve step matched `> Note:` and kept **one line**.

- **It had already happened, and shipped.** Checking the other notes against the pre-re-slice backup:
  **`workers-ai.md` and `r2-data-catalog.md` were both truncated mid-sentence** — "…they were" and
  "…The Iceberg REST catalog itself" — and had been that way in the installed skill since 2026-08-08.
  The 08-08 entry says the workers-ai note exists "so the shrink is not mistaken for data loss"; the
  half that carried the explanation was gone, so the note had been failing at its only job for a week.
- **Fixed at the source**: the preserve step now carries the `> Note:` line **plus every following
  quote line**, and the reason is in a comment at the fix, not only here.
- **All three notes rewritten in full** — the two truncated ones reconstructed from the 08-08
  changelog, which is why that entry describing them in prose turned out to be worth writing.
- **Proved by re-running, not by reading**: hashed all 47 slices, ran `slice-api` again, hashed again
  — **zero files changed**, and the notes still measure 7 / 4 / 3 quote lines. The rewrite is now
  idempotent over hand-written notes, which is the property that was missing.

**False BLOCK in the gate itself — found because it fired on a correct CHANGELOG**

`--close` refused this entry saying it had no `**Deferred**` section. It had one. The same
`awk … | grep -qi '^\*\*Deferred'` returned **0 by hand and 141 inside the script**.

- **Cause:** `refresh` runs under `set -euo pipefail`. `grep -q` exits at its first match; awk is
  still writing, takes **SIGPIPE**, exits 141; `pipefail` promotes that 141 to the pipeline status,
  and `if !` reads it as "no Deferred section". It only misfires when the match lands early enough
  to leave awk mid-stream — which is why earlier closes today passed and this one did not. A gate
  that fails *because the document is well-formed enough to match early* is worse than no gate: the
  operator learns to route around it.
- **Fix:** materialize the scope into a variable, then grep that. No pipe, no SIGPIPE, same rule.
- **Tested both directions, not just the happy one:** real CHANGELOG → `✅ gate ... with a Deferred
  section`; a doctored copy of today's entry with the heading renamed → `✗ BLOCKED`. The gate still
  blocks what it exists to block.

**Independent reconciliation of all 46 slices against the spec** (the operator's point: `slice-api
--validate` re-derives slices with the same code that wrote them, so it cannot catch a shared wrong
assumption — it is a self-consistency check, not a check against the source)

**`scripts/reconcile-api` — NEW, and this is the deliverable, not the number it printed.** It reads
the raw spec and deliberately groups paths by a **different** rule than `slice-api` uses, so the two
do not share a blind spot. It was first written as a throwaway in `/tmp`; a measurement whose
instrument is deleted is a claim nobody can re-check, so it lives in `scripts/` now:

```
scripts/reconcile-api ../raw/api-schemas/openapi.json [--installed]
```

Its docstring carries the two things a reader needs: why it is not `slice-api --validate` (that one
re-derives with the matcher that wrote the slices — self-consistency, not verification against the
source), and the over-reporting draft that was discarded, kept so the mistake is not repeated.

**The sweep audited as an instrument** — a full-corpus check can report "0 defects" two dishonest
ways: by skipping rows it cannot parse, or by failing to detect a defect that is there. Both closed:

- **Blind spots: none.** 1,692 endpoint lines exist across the 46 slices and **1,692 are parsed and
  compared** — zero silently skipped. A line the regex missed would never be checked and would still
  count as clean, which is how a sweep lies without anyone editing a number.
- **Sensitivity proven by mutation.** Injected 1, then 7, then 30 defects of each kind (phantom path ·
  wrong summary · wrong required-params) at random positions: the sweep found **exactly N of each,
  every round**, and 0/0/0 on the untouched corpus.
- **Widened from one field to three.** It started as summary-only; it now also checks path existence
  and the **required-parameter list** — all three at **0 divergences across 1,692 rows**, navigating
  the raw JSON by key (`paths[path][method]`) rather than reusing the code that wrote the slices.
- Printed samples are illustration of the mechanism; the measurement is the full 1,692.

**Provenance corroborated through a second, independent Cloudflare channel**

Everything above compares the slices to `openapi.json`. That file *is* Cloudflare's published
artifact, but the whole chain rested on one host. Widened:

- **A second machine-readable channel does not exist** — probed `api.cloudflare.com/schemas/v4/…`,
  `/schemas`, `developers.cloudflare.com/schemas/…` and `/api/openapi.json`: **all 404**. Stated so
  the next person does not re-probe.
- **The official TypeScript SDK declares `configured_endpoints: 2439`** against the spec's 3,334
  operations. Same order of magnitude, but the SDK filters what it generates, so this **corroborates
  nothing at line level** and is recorded as such rather than dressed up as agreement.
- **The docs site is genuinely independent** (`developers.cloudflare.com`, a different system from
  `raw.githubusercontent.com`) and publishes one page per method carrying the verb, the path and the
  summary. **9 endpoints across 8 products** (d1 ×3, kv, queues, workers, vectorize, hyperdrive, r2)
  fetched from there and compared to the installed slices: **9/9 identical on verb, path and
  summary, 0 divergences.**
- **Honest weight:** 9 of 1,692 is 0.5% — this is corroboration of the *pipeline*, not a second full
  audit. It rules out the failure that the file-level check cannot see: that `openapi.json` is a
  stale or unofficial copy disagreeing with what Cloudflare actually documents.

**Adversarially tested, not just run on a clean corpus.** Doctored `billing.md` with one invented
endpoint and one tampered description: the checker named both and printed `✗ FAIL`. Restored, it
returns to 0/0. A checker only ever run against passing input is not evidence.

- **Correctness: clean, and this is the strong result.** All **1,749 operations** across the 46
  slices were matched against the 2026-08-15 spec: **0 phantom endpoints** (nothing listed that the
  spec does not have) and **0 divergent summaries** (every description matches the spec's own text
  byte for byte). So the +9/+2/+1/+1 additions are real and the 42 untouched slices are faithful.
- **Completeness: the first pass of the reconciler was wrong, and saying so is the point.** Its
  grouping rule was too coarse — it demanded, for instance, that `bots.md` carry all 264 `/radar/*`
  operations merely because it legitimately lists a couple of Radar bot endpoints. That produced
  "23 slices with problems", which was an artifact of my check, not a defect in the slices. Rerun
  against the real question — *what does **no** slice cover?* — the number is meaningful.
- **Measured coverage: 1,749 of 3,334 spec operations (52%).** Most of the remainder is the
  Cloudflare One / Gateway / DLP / Access / IAM surface removed from the catalog on 2026-06-26 —
  absent **by decision**. Excluding those, the genuine in-scope hole is **168 operations**:
  `radar` 46 · `settings` 45 · `builds` 20 · `load_balancers` 8 · `logpush` 8 · `rum` 8 · `email` 7 ·
  `analytics` 6 · `speed_api` 4 · plus singles (`hyperdrive/integrationsOperations`,
  `billing/usage`, `registrar/extensions`, `stream/usage`, `ai/tomarkdown`, `pages/assets`).
- **Every one of those fits the documented failure mode:** endpoints that launched under a **brand-new
  root**, which `slice-api` cannot see because it derives each matcher from roots the slug already
  has. The script's docstring predicted exactly this and pointed at the docs drift check as the
  compensating control. **This pass is the first time the size of that hole was measured: 168.**
- **What this does NOT say:** it is a check of paths and summaries, not of request/response shapes,
  parameters or auth — a slice can list the right endpoint and still mislead on the body.

**Cloudforce One removed from `rules.md` — operator's call, after asking what it was**

Cloudforce One is Cloudflare's **threat-intelligence platform** (threat events, PIRs, RFIs,
analyst reports), a SOC subscription product — the same enterprise-security category dropped from
the catalog on 2026-06-26. It was sitting in the Rules slice purely because its URLs contain the
word `rules`, crowding answers about traffic rules with threat-intel endpoints.

- **Fixed in the matcher, not by hand-editing the slice.** `NOT_MINE` was populated for the first
  time (it had been `{}` since it was introduced): `"rules": ("/accounts/{account_id}/cloudforce-one",)`.
- **`excluded()` changed from exact-path to prefix matching**, which is what the comment above it
  always claimed ("Roots a slug derives but does not own") while the code compared whole paths.
  With exact paths, every new Cloudflare endpoint under the same foreign root would be re-imported
  by the next re-slice — **the removal would silently undo itself.**
- **Result: `rules.md` 108 → 81 operations, −17 distinct paths.** Diffed the before/after path lists:
  **every removed line is a `cloudforce-one` path, and nothing was added** — the Rules product's own
  81 endpoints are untouched.
- **Checked the two ways this could bite later:** `--validate` still reports **OK — no slug lost
  coverage** (so next week's `--close --spec` will not abort), and re-running `slice-api`
  immediately leaves **every slice hash unchanged** — the exclusion is idempotent, Cloudforce One
  does not creep back.
- **`resource-tagging.md` cleaned in the same pass: 93 → 53 operations, −27 paths (40 lines).** It
  had been flagged as "ask before the next pass", which was the wrong call — the operator had
  already approved the principle, and shipping a half-done removal leaves the skill inconsistent
  with itself. Same diff discipline: **every removed line is `cloudforce-one`, nothing added.**
- **`grep -c cloudforce-one references/api/*.md` now returns nothing across all 46 slices.**
- `reconcile-api` after both removals: **1,692 operations, still 0 phantom and 0 divergent
  summaries**, against spec `sha256 c5cf6c05…` — the same bytes GitHub serves for
  `cloudflare/api-schemas/main/openapi.json`, re-downloaded and `cmp`'d at close time, and the hash
  recorded in `references/api/_spec-version.txt` so the claim stays checkable after the fact.

**Tried to verify the slices against the LIVE API, and could not — negative result, logged so the
next person does not spend the same hour**

`reconcile-api` establishes fidelity to Cloudflare's **published spec**. That is Cloudflare's own
artifact (hash-matched at close time to what `raw.githubusercontent.com/cloudflare/api-schemas`
serves right now), but it is a document, not the running service. Attempt to close that gap:

- **Idea:** probe `api.cloudflare.com` and let the router answer. Unauthenticated, a nonexistent path
  returns error **7000 "No route for that URI"**, while a real path returns 9106/9107 (missing auth).
  Clean discriminator, no credentials, no mutation — GET only.
- **Validated the proxy before trusting it, and it failed.** Of 4 deliberately invented control
  paths, **2 passed as existing**: `/accounts/{id}/r2/buckets-falso` and `/radar/nao/existe` both
  returned 9106 rather than 7000. Under some prefixes the API authenticates before it routes.
- **Authenticating did not fix it.** With a valid token, `/r2/buckets-falso` and
  `/ai/models/schema-x` returned 10000 (auth) while only gibberish like `/nao-existe-abc` returned
  7000. **The failing case is exactly the dangerous one** — a hallucinated endpoint would be a
  plausible sibling of a real one, not gibberish, and that is precisely what the probe cannot see.
- **So the 40/40 "routes exist" reading from the sample was discarded, not reported as evidence.**
  A proxy that fails its own control measures nothing; publishing the 40/40 would have been a
  fabricated verification.
- **What stands, stated at its real strength:** the slices are faithful to Cloudflare's published
  spec — every one of 1,692 listed operations exists there with a byte-identical summary. **They are
  NOT verified against the deployed API**, and the two can differ in both directions (spec'd but not
  shipped; shipped but undocumented). The `⚠️ Verify against the live API docs` line already at the
  top of every slice is not boilerplate — it is the honest boundary of this file.

**Deferred** (the backlog)

- **Verifying slices against the running API remains unsolved.** The only avenue left is an
  authenticated call per endpoint interpreted per product (a real 404 vs a permission error vs an
  empty list), which needs resources to exist in the account and cannot be a blanket sweep. Worth
  doing for a handful of high-traffic endpoints, not for 1,692.
- **The 10 cross-slice duplicates are unrelated to Cloudforce One** — still 10 after the removal.
  They are `alerting/v3/policies*`, claimed by two slices at once. Ownership is a scope call.
- **168 in-scope operations sit under roots no slice claims** (breakdown above). Not fixed here: each
  needs a root added deliberately, and `radar`+`settings` alone are 91 of them, which is a curation
  decision about how much of Radar this skill wants to own — not a mechanical patch to slip into a
  drift-check pass. Re-measure any time with `scripts/reconcile-api`.
- **10 operations are listed by two slices at once** (1,759 lines vs 1,749 distinct operations) —
  the same root-collision family as the `cloudforce-one` item below. Not deduplicated blindly:
  which slice should own each is a scope call.
- **`rules.md` owns 15 `cloudforce-one/rules/*` paths and just gained 9 more** (`approvals*`).
  Cloudforce One is threat intel, not the Rules product — this looks like the root collision
  `NOT_MINE` exists for, and `NOT_MINE` is still `{}`. **Pre-existing, not a regression from this
  pass**, and not silently "fixed" here: removing them would drop 24 paths with no cloudforce-one
  slice to receive them. Needs a scope decision — either add a `cloudforce-one` slice or accept the
  attribution deliberately.
- Out-of-scope-by-catalog but recorded in case Cloudflare One is ever re-added: hostname routing GA +
  the new public initial-resolved-IP range (`172.64.128.0/20`, IPv6 fixed, IPv4 configurable),
  Gateway package-registry security, Gateway MCP detection + AI Security dashboard, email-security
  blocked-content rules, Access independent MFA with FIDO2, One Client 2026.6.905.0.
- Changelog items deliberately not curated: **DeepSeek V4 Flash/Pro on Workers AI** (model names come
  from `GET /ai/models/search`, not from this ref — rule set 08-08), Pages skipping superseded queued
  builds, the 08-11 WAF release, and the new Cloudflare Status page.
- Carried over untouched from 08-08: Radar AS-level connectivity + Researcher beta, Cloudflare Mesh
  container image, Access authorization cookies, publisher verification on OAuth consent, free
  accounts from the dashboard, Artifacts build-on-push, Workers local tracing for agents, Python↔JS
  Worker RPC, WAF releases.

---

## 2026-08-08

**Detected** (weekly drift check — all three checks ran and reported)

- **New top-level product**: `r2-data-catalog` (`live=105 known=104`). It is the promotion of the old
  `r2/data-catalog` subtree, which disappeared in the same pass.
- **New doc subtrees**: `sandbox/1-0-preview` (+16 pages) and `r2-data-catalog` (+15 pages).
  20 routine single-page adds, not flagged.
- **Gone**: `r2/data-catalog` (promoted) and `ai-search/configuration/retrieval/embed-search-snippets`.
- Installed vs workbench `diff -rq` **empty** at pass start.
- Changelog worth acting on: Workers AI + AI Gateway unified (08-07) · billing enabled for Pipelines,
  R2 Data Catalog and R2 SQL (08-03) · Vectorize 10M→20M vectors/index (08-04) · AI Search public
  endpoints / custom domains / namespaces / `discover` crawl (08-06) · Kitesurf on Browser Run (08-06)
  · agent traces (08-04) · `@cloudflare/computer` preview (08-03).

**Curated** (grounded in freshly pulled `raw/docs-oficiais/pages/` for r2-data-catalog, sandbox,
ai-search, vectorize, pipelines, r2-sql, agents, browser-run, ai-gateway, workers-ai — 543 pages
re-downloaded — plus the live `changelog/index.md`)

- **`products/r2-data-catalog.md` — NEW.** Managed Iceberg REST catalog inside an R2 bucket: why a
  catalog exists at all, Pipelines→Catalog→R2 SQL placement, `wrangler r2 bucket catalog enable`,
  Catalog URI + Warehouse name + token auth, engine configs (Spark/PyIceberg/DuckDB/Trino/Snowflake/
  StarRocks), compaction vs snapshot expiration, and the full billing table (1M catalog ops included
  then $9/M; compaction $0.005/GB + $2.00/M objects; snapshot expiration free).
- **`products/sandbox.md`** — new top section for the **1.0 preview** (`@cloudflare/sandbox@next`):
  stable-vs-preview mapping table, argv `exec()` returning a process handle at launch, terminals as
  PTYs, interpreter as an opt-in extension, RPC-only transport, and the migration traps (explicit
  shell for pipes/`&&`, per-call `cwd`/`env`, never mix preview Worker package with stable container
  image, self-deployed bridge not in the preview).
- **`products/r2.md`** — pointer replacing the dead `r2/data-catalog` path.
- **`products/r2-sql.md`** — pricing rewritten: billing enabled 08-03, 10 GB/mo included then
  $0.0025/GB, 10 MB minimum per query, failed queries free, `EXPLAIN`/`SHOW`/`DESCRIBE` free.
- **`products/pipelines.md`** — "billing announced" → **billing enabled 2026-08-03**.
- **`products/vectorize.md`** — vectors/index **10M → 20M**, with the old number named so stale
  sources are recognizable.
- **`products/ai-search.md`** — new "Public endpoints" section (public endpoint, custom domain,
  Access in front with service tokens, namespace fan-out endpoint, `discover` parse type) and the
  sitemap gotcha corrected — a `sitemap.xml` is no longer mandatory.
- **`products/browser-run.md`** — new **Kitesurf** section: agent-first stateless browser on Workers,
  3–7× less CPU/memory than Chromium, free in beta, opt in per request with `browser=kitesurf`,
  and the explicit "not Chromium — choose deliberately" call.
- **`products/agents.md`** — **agent traces** (`observability.traces.enabled`, automatic for Think and
  Flue, `wrapAISDK()` for direct AI SDK calls) and **`@cloudflare/computer`** preview (SQLite-backed
  virtual filesystem in a `Workspace` inside any DO, isolate vs container backends, AI SDK toolkit,
  and how it differs from Sandbox SDK).
- **`products/ai-gateway.md` + `products/workers-ai.md`** — the 08-07 unification: same `env.AI`
  binding and shared `/ai/` REST endpoints reach Workers AI *and* third-party providers, `gateway:
  { id: 'default' }` auto-creates a gateway; plus User Insights and identity-aware controls.
- **`references/api/r2-data-catalog.md` — NEW**, 13 operations sliced from a freshly downloaded
  OpenAPI spec, with the `r2-catalog` (not `r2-data-catalog`) REST prefix flagged and the Iceberg
  REST catalog distinguished from these management APIs.
- Bookkeeping: `_known-products.txt` += `r2-data-catalog` (105); SKILL.md catalog entry + quick-map
  line added.

**API re-slice — done in the same pass (was deferred, then cleared)**

- **`scripts/slice-api` written.** The spec has no product→endpoint map (533 tags, none aligned to
  products), so each slug's matcher is *derived from its own existing slice*: every listed path is
  reduced to a "resource root" and new-spec paths match by root prefix. `--validate <old-spec>`
  re-derives the slices from the spec they came from — **missing** paths fail, **extra** paths are
  reported for review because the matcher is deliberately a superset (old slices were under-inclusive
  and omitted sibling endpoints under roots they already covered).
- **Validated against the 2026-06-26 spec: 0 slugs lost coverage.** The 3 apparent losses were
  spec-version artifacts, checked one by one: `browser-rendering/accessibilityTree` and
  `r2-catalog/{bucket_name}/delete` exist only in the new spec; the moondream model path is in
  neither spec (retired).
- **All 45 slices regenerated from a freshly downloaded spec.** 25 unchanged. Notable deltas:
  - **`workers-ai.md`: −114 paths — a real API change, not a regression.** Cloudflare collapsed the
    114 enumerated per-model paths (`/ai/run/@cf/meta/llama-...`) into one parameterized
    `/ai/run/{model_name}`. Noted in the slice so the shrink is not mistaken for data loss; model
    names now come from `GET /ai/models/search` or `products/workers-ai.md`.
  - `resource-tagging` +25 (cloudforce-one event datasets, groups, share excluded-recipients) ·
    `images` +11 (sourcingkit migrations) · `pages` +4 (deployment tails, upload-token) ·
    `radar`/`rules` +4 · `dns` +3 (account-level DNS Firewall) · `email-service` +3/−1 · the rest +1/+2.
- **Known limit of the matcher, by construction:** an endpoint launched under a *brand-new root* for an
  existing product has no root to match and will not appear. That gap is covered by the docs subtree
  check, not by this script. Documented in the script's docstring.

**Detector fixed mid-pass (two silent-cap bugs, both found by the operator asking "isn't comparing
llms.txt enough?")**

- **Single-page additions are now named, not tallied.** `pagediff.py` printed "N single-page
  addition(s) — not flagged" and stopped there. That is a silent cap: a limit change, a new pricing
  page, or one new endpoint page each arrive as exactly one page and were indistinguishable from
  routine docs. They are now listed under a low-signal heading, so the reader decides.
- **`--init-baseline` now rotates the outgoing baseline to `_known-pages.prev.txt`.** Re-recording is
  the *last* step of a refresh and it destroys the only record of what that pass saw.
- **Cost of finding this late: this pass's 20 single-page additions were unrecoverable by diff.** The
  baseline was re-recorded before the bug was known, no prior copy existed, and the names were never
  printed. From the next pass on, both fixes make this reconstructible.
- **Gap covered by a substitute sweep.** Fetched the first 1.4 KB of all 6,152 live doc pages via HTTP
  range requests and read each page's "Last updated" date (6,065 answered; 87 unreachable/unparsed).
  **256 pages touched since 2026-08-01**; 141 of them are inside products curated this pass. Of the
  remaining 115, ~85 share the single date 2026-08-03 across WAF, bots, api-shield,
  client-side-security and style-guide — a docs-wide reformat, not content. The substantive
  stragglers, none of which change a curated claim: `workers/observability/traces` +
  `exporting-opentelemetry-data` (08-04, the tracing already curated in agents.md),
  `cloudflare-one/networks/connectors/cloudflare-mesh` ×3 (08-07, the deferred Mesh item),
  `cloudflare-one/access-controls/ai-controls/mcp-portals` (08-07),
  `logs/logpush/logpush-job/enable-destinations/pipelines` (08-07),
  `artifacts/guides/build-and-deploy-on-push` (08-04). **Caveat: this measures pages *edited*, not
  pages *added* — it is a different question than the diff answers, and it cannot prove the 20 are
  among the 256.**
- Both fixes tested against doctored baselines (a 16-page subtree removal → flagged as a launch;
  three single-page removals → each named) and the rotation verified byte-identical to the outgoing file.

**Curated from that sweep** (the two stragglers that touch curated surfaces)

- **`products/agents.md` — MCP server portals** (Cloudflare One/Access, 08-07). The operations answer to
  an agent needing many MCP servers: one endpoint, Access identity in front, curated tool surface with
  aliases, context optimization (`minimize_tools` / `search_and_execute`), Code Mode collapsing tools
  into search+execute inside a Dynamic Worker, service tokens for machine clients, the transport
  auto-detect ladder, and the gotchas that bite (24 h idle session expiry, ~2 h upstream tool sync that
  bypasses Gateway).
- **`products/logs.md` + `products/pipelines.md` — Logpush → Pipelines native destination** (08-07).
  Closes the chain this pass documented: logs → pipeline (Simple or Custom SQL) → Parquet/Iceberg in
  R2 Data Catalog → R2 SQL. Only 4 datasets supported (`http_requests`, `firewall_events`, `dns_logs`,
  `workers_trace_events`) — recorded on both sides, with "raw archive → keep a plain R2 destination".

**`scripts/refresh` — the pass is now a sequence, not a memory exercise**

The root cause of both bugs above was never the detector: it was that a refresh is a checklist executed
from memory, with a **destructive step in the middle**. Re-recording the baseline is what makes the next
diff meaningful and what erases the record of this one. Nothing stopped it running early — so it did.

- `scripts/refresh` — phase 1: runs `update-check` against the INSTALLED skill (the 2026-07-21 pass
  audited the workbench and gave a false all-clear) and reports copy sync.
- `scripts/refresh --close [--spec <openapi.json>]` — phase 2, fixed order: **gate on CHANGELOG** →
  validate + re-slice API (aborts if any slug would lose endpoints) → promote workbench→installed →
  verify the copies converge → re-record baseline → re-run `update-check` to prove the pass closed.
- **The gate:** today's `## <date>` entry must exist AND contain a `**Deferred` section, scoped to that
  entry via awk — five older entries have one and the gate still blocks without today's.
  **No `--force`.** A bypass would restore exactly the failure it exists to prevent.
- Verified adversarially: no entry for today → blocked · entry without Deferred → blocked · Deferred
  only in older entries → blocked · real run → gate passes, 0 slugs lose coverage, copies identical,
  baseline rotated, closing `update-check` clean.

**Three smaller process fixes, same session**

- **API spec provenance.** `--close --spec` now writes `references/api/_spec-version.txt` (date, source
  path, sha256, size) and phase 1 warns when the slices are >30 days old. Until now "sliced from the
  OpenAPI spec" read as current at any age — which is how 44 slices sat six weeks stale without anyone,
  including the weekly check, being able to notice.
- **The backlog is read out loud.** Phase 1 prints the `**Deferred` block of the most recent CHANGELOG
  entry. Deferrals were being logged faithfully and then never looked at again; a backlog nobody reads
  at the start of the next pass is a backlog that only grows.
- **The scheduled task stopped duplicating the procedure.** `~/.claude/scheduled-tasks/
  cloudflare-atlas-update-check/SKILL.md` carried its own copy of the steps, which drifted from the
  skill and needed fixing in two places. It now calls `scripts/refresh` and explains how to read the
  output, with an explicit ban on substituting a hand-rolled partial check when the script fails —
  that substitution is what produced the false all-clear on 2026-07-21.

**Sandbox 1.0 — deferral cleared in the same session (all 16 preview pages mined)**

`products/sandbox.md` no longer stops at the migration table. Added, grounded page by page:

- **The mental model 1.0 enforces** — sandbox ID vs Durable Object vs container vs process/terminal/
  local files, as a table. Same sandbox ID ≠ same container; `getSandbox()` starts nothing; **store the
  job, not the handle**, because a process ID is only valid while that container still has it.
- **Processes** — the full handle surface (`status`, `logs({since,replay,follow})`, `output`,
  `waitForExit`, `waitForLog`, `waitForPort`, `exitCode`, `kill`), and the two traps: **a wait that
  times out stops the wait, not the process**, and `output()` returns bytes unless you pass
  `{ encoding: "utf8" }`. Cursor-based log resume.
- **Terminals** — a distinct resource type, not a process variant. `write`/`resize`/`interrupt`/
  `terminate`/`connect`, xterm `terminalId` (stable's `sessionId` is gone), cursor replay. **There is
  no stdin on a process handle** — interactive input *is* a terminal. `getProcess`/`getTerminal`
  never wake a container; `null`/`[]` is a value, not an error.
- **Environment** — the three-layer merge (image ENV → `setEnvVars` → per-launch `env`), `export`
  not surviving a launch, `setEnvVars` living in **DO memory** (not disk, not backups, gone on
  eviction), and the secrets rule: outbound traffic handlers, never live keys in sandbox env.
- **Extensions** — nested namespaces on your subclass; interpreter (`-python` image for Python) and
  OpenCode are first-party; custom extension authoring is experimental and undocumented.
- **Errors, split by phase** — `ContainerUnavailableError` is the *only* safe blanket retry (work
  never started, honour `retryAfterMs`); `OperationInterruptedError` and `RPCTransportError` mean the
  work may have started, so check state first; stale handle errors mean relaunch from checkpoint.
- **Symptom→cause table** and a **migration grep inventory** including `gitCheckout` being removed
  and `waitForPort` defaulting to tcp in the preview.

**AI Gateway deferral cleared in the same session**

`products/ai-gateway.md` — the two 08-05 items were one-liners; now two grounded sections:

- **Cloudflare Access in front of the gateway.** Requires a custom domain + Access on the account.
  The **Access JWT becomes the request credential** (no gateway token needed) and the verified user
  lands in metadata as **`cf.user_id`** — the JWT `sub`, *not* the email. Cloudflare-only credentials
  are stripped before the upstream provider. **Flagged as breaking:** once on, gateway-token-only
  integrations are blocked by Access before reaching the gateway — migrate them or keep that traffic
  on the unprotected default host. Limits recorded: no `cf.user_id` for service tokens, `cf.`-prefixed
  metadata keys reserved and dropped.
- **User Insights.** Free, no setup, but **useless without attribution** — all traffic collapses into
  one anonymous bucket unless you send custom metadata or sit behind Access. Org metrics listed, plus
  the anomaly rule in full: baselines are **per session**, using each user's **rolling p95 session cost
  over 30 days**, and a session flags only when it beats **both** 2× that user's p95 **and** the org
  p99 — the conjunction is what stops low-usage spikes and heavy-user routine from firing. **It flags,
  it does not block.**

**Deferred** (the backlog)
- Changelog items deliberately not curated: Radar AS-level connectivity + Researcher beta, Cloudflare
  Mesh container image, Access authorization cookies, publisher verification on OAuth consent, free
  accounts from the dashboard, Artifacts build-on-push, Workers local tracing for agents,
  Python↔JS Worker RPC, WAF releases.

---

## 2026-07-31

**Detected** (weekly drift check — all three checks ran and reported)

- Product list clean (`live=104 known=104`); installed vs workbench `diff -rq` **empty** at pass start.
- **Two new doc subtrees**: `ai-search/agent-sdks` (+4 pages) and `agent-setup/visual-studio-code`
  (+2 pages). 8 routine single-page adds, not flagged.
- **`agent-setup` was in `_known-products.txt` with NO `products/` file and NO catalog entry** — a known
  product entirely invisible to the skill. `update-check` did not catch this: check (c) walks
  catalog→file, never known→catalog. **Detector blind spot, not a curation miss.**
- Changelog: **Agents SDK v0.20.0 (07-27) is the structural one** — MCP servers went stateless.
  Also: Workers AI select models now require Workers Paid; Node.js 24 default in Workers Builds;
  Workers tracing `startActiveSpan()`/`span.end()`.

**Curated** (grounded in freshly re-pulled `raw/docs-oficiais/` — the 6 new pages, `migrate-to-mcp-sdk-v2`,
`handler-api`, `agent-api`, `agents/tools/ai-search`, plus `full/{ai-search,agent-setup,agents}.md`.
`handler-api` shrank 27,599→20,958 bytes, confirming the cached copy was pre-v0.20.0)

- `products/agents.md` — **MCP section rewritten for v0.20.0**: `createMcpHandler` takes a *factory*,
  isolated server per request, no transport session / no Durable Object; one route serves new + legacy;
  `McpAgent` deprecated + feature-frozen; `createMcpHandler(v1Server, options)` removed next major;
  `isLegacyRequest()` dual-lane drain; import from `agents/mcp/server` to keep SDK v1 out of the bundle.
  Added a **protocol-deltas** bullet (no `initialize`, no `Mcp-Session-Id`, `input_required` + retry
  instead of pushed JSON-RPC, `subscriptions/listen` with no `Last-Event-ID` replay, `resultType`) and a
  **client-side** bullet (`server/discover` probe with same-connection legacy fallback). New gotcha:
  writing an MCP server as `McpAgent` — called out because pre-v0.20.0 training data still shows it.
- `products/ai-search.md` — the runtime-provisioning gotchas the new guides expose: `ai_search_namespaces`
  is **required** if code calls `create()`; `"remote": true` because **AI Search does not run locally**;
  `create()` is **not idempotent** (throws if exists); `upload()` only **queues** — poll
  `items.get(id).info()` or the first query hits an empty index. *Going deeper* now points at
  `agent-sdks/` with the per-framework constraints (`ai@^6` for the AI SDK provider; LangChain retriever
  searches only and its token needs **both** `AI Search:Edit` and `AI Search:Run`).
- `products/agent-setup.md` — **NEW FILE** (121 lines; no official ref exists for this slug, so written
  as the primary source per the guide's depth rule). Skills-vs-MCP split, the one-step `prompt.md`
  installer, Claude-Code-is-different (plugin only, never `npx skills`/`claude mcp add`), the 17
  domain-specific MCP hosts, and a per-agent config table. Headline gotcha: **`mcpServers` vs `servers`**
  — VS Code/Copilot use `servers`, Cursor/Windsurf/Claude Desktop use `mcpServers`, and a config copied
  across **fails silently**.
- `SKILL.md` — catalog entry added for **Agent setup** (Developer platform section).

**Deferred**

- **No re-slice of `references/api/`** — verified, not assumed: `api/ai-search.md` already carries all 55
  operations incl. `instances`/`items`/`namespaces`, and `agent-setup` has no REST surface of its own.
  No new API surface landed this pass.
- `_known-products.txt` **untouched on purpose** — `agent-setup` was already listed, and `agent-sdks`
  and `visual-studio-code` are sub-products, which do not belong there.
- **Carried over, still not done:** the 2026-07-27 Workers *"Run integration tests against your Worker's
  production build"* item (likely `products/workers.md` and/or the `vitest` skill) — deferred a second
  consecutive pass.
- **Not curated this pass:** Workers AI paid-plan gating for select models, Node.js 24 as Workers Builds
  default, Workers tracing `startActiveSpan()`/`span.end()`, Browser Run human-in-the-loop handoff,
  Gateway DNS max-TTL, Audit Logs v2, Stream broadcast-key rotation. All are `products/*` edits outside
  the two subtrees this pass was scoped to.
- `agents.md` and `ai-search.md` both sit at **exactly 120 lines** — at the guide's cap. Every addition
  above required cutting elsewhere (duplicated Code Mode prose in *Going deeper*, verbose enumerations).
  Next pass adding to either must cut first; they cannot absorb more.
- **`think.md` (169 lines) still over the ≤150 cap** — pre-existing, deferred again.
- **Hedge resolved, not dropped:** the "(Recent — confirm exact API)" caveat on `runAgentTool`/`runTurn`
  was removed from `agents.md` — but only after verifying both against the freshly pulled `full/agents.md`
  (19 `runTurn` hits; `detached: { onFinish, maxBudgetMs }` present verbatim). Additional `detached`
  options exist live (`notify`, `onMilestones`) and were **not** added.
- **Raw corpus is only partially fresh.** This pass re-pulled `ai-search`, `agent-setup`, `agents` and the
  MCP pages; the rest of `raw/docs-oficiais/` is still from **2026-06-26**. The staleness deferral from
  the 07-27 pass stands for every other product.

---

## 2026-07-27

**Detected** (weekly drift check — all three checks ran and reported)

- Product list clean (`live=104 known=104`); no new doc subtrees (1 routine single-page add, not
  flagged); installed vs workbench `diff -rq` **empty**. No structural refresh needed.
- **The 2026-07-23 "AI SDK v6 and v7" release was missed by the 2026-07-23 pass** — that pass ran at
  09:10 and curated the 07-22 release, but the 07-23 post landed the same day and was never picked up.
  It left `think.md` asserting `ai` (AI SDK **v6**) as *the* peer, which is now wrong-by-omission: v7 is
  supported and the react peer has to be paired by major.
- **`fundamentals.md` had no notion of API deprecations at all** — no section, no pointer to the
  deprecations page. So the 2026-07-21 **Account Roles API** deprecation had nowhere to land, and
  neither did the 2026-07-22 **account-name 65-char** enforcement (which is on the deprecations page
  but never surfaced as its own changelog headline — found by reading the page, not the RSS).

**Curated** (grounded in `changelog/post/2026-07-23-ai-sdk-v6-v7-support/`, `.../2026-07-22-mcp-codemode-updates/`
and the live `fundamentals/api/reference/deprecations/` page fetched this pass)

- `products/think.md` — peers line now states `ai@^6 || ^7` + `@ai-sdk/react@^3 || ^4` with the
  major-pairing rule (v6↔react v3, v7↔react v4); added that Think normalizes streaming, tool-completion
  events and telemetry across both majors, so updating does not force a v6→v7 migration.
- `products/agents.md` — same peer range recorded under *Binding & config* (it spans `agents`,
  `@cloudflare/ai-chat`, `@cloudflare/codemode`, `@cloudflare/think`, not just Think); extended the
  Code Mode bullet with `requiresApproval: true` on protected connector methods returned by
  `search()`/`describe()`, resolved via the existing `approve()`/`reject()`.
- `products/fundamentals.md` — **new section "API deprecations (live watch list)"** (+ TOC entry, +
  RSS pointer under *Going deeper*). Points at the deprecations page as source of truth rather than
  mirroring it, then carries the two that bite: Account Roles → Permission Groups (dead endpoints,
  replacements, the `permissions`-object → `meta{label,scopes}` schema break, and the remap of
  persisted legacy Role IDs through the Account Members policies shape), and the account-name 65-char
  cap enforced 2026-09-27 (`POST /accounts` silently truncates at 120 bytes today → account that
  creates but can never be renamed).

**Deferred**

- **No re-slice of `references/api/`** — verified, not assumed: there is no `accounts.md`/`iam.md` slice
  (44 files, all product-scoped), so the Roles→Permission Groups change touches no sliced surface.
  If an IAM slice is ever added, it must start from Permission Groups, not Roles.
- `_known-products.txt` and the SKILL.md catalog **untouched on purpose** — no new slug; every change
  this pass is inside an already-catalogued product.
- The `runTurn` / sub-agent "recent — confirm exact API" hedges in `agents.md` are **still** unverified
  against live docs — carried over from the 2026-07-23 pass, deferred again.
- `think.md` is 169 lines, over the guide's ≤150 for a covered product. Pre-existing; not restructured
  during a drift pass.
- Raw source material in `raw/docs-oficiais/` is from **2026-06-26** and is now a month stale — every
  fact this pass was fetched live instead. Worth a re-pull before any pass that needs page-level depth.
- **2026-07-27 Workers — "Run integration tests against your Worker's production build"** landed *during*
  this pass (it was not in the changelog when the pass started) and was **not curated**. Likely homes:
  `products/workers.md` and/or the `vitest` skill. First item for the next pass.

---

## 2026-07-23

**Detected** (weekly drift check — product/subtree/copy-sync all reported)

- Product list clean (`live=104 known=104`); no new doc subtrees (1 retired page in `realtimekit`, 1
  routine single-page add). No structural refresh needed.
- Changelog surfaced the **2026-07-22 Agents/Workers "MCP + Code Mode" release** — three real changes
  the reference didn't reflect, plus the **2026-07-13 MCP elicitation** addition.
- The `agents.md` "Going deeper" note stated **"Code Mode are Think-only"**, which the 2026-07-22
  release made **factually wrong** — Code Mode is now invocable outside Think.

**Curated** (grounded in the live changelog post `2026-07-22-mcp-codemode-updates/`)

- `products/agents.md` — added 3 bullets under *Tools & MCP*: (a) MCP schema caching (converted
  schemas reused per live connection, no re-conversion each turn); (b) MCP elicitation via
  `configureElicitationHandlers` (form/URL mode, survives hibernation); (c) Code Mode invocable without
  the AI SDK — `@cloudflare/codemode` `execute()`/`search()`/`describe()` on the durable runtime handle.
  Corrected the "Think-only" claim in *Going deeper*.
- `products/think.md` — added `includeMcpTools` (default true; set false to skip Think's automatic
  `getAITools()` MCP exposure) to the *Key API surface* list next to `waitForMcpConnections`.

**Deferred**

- The `runTurn` / sub-agent "recent — confirm exact API" hedges in `agents.md` (lines ~44-47) still
  unverified against live docs — not touched this pass, left as-is.
- No re-slice of `references/api/` needed (no OpenAPI-surface change; these are SDK-package changes).

---

## 2026-07-22

**Detected**

- `env.AI.toMarkdown` (Workers AI Markdown Conversion) was **entirely absent** from the workers-ai
  reference, the SKILL decision tree, and the catalog — despite being the Cloudflare-native answer to
  a common need: "extract text/data from a PDF/doc inside a Worker" (competes with unpdf/LiteParse and
  external OCR like Mistral/Textract). Surfaced by a real build (reading Brazilian tax-slip PDFs from
  R2), not by the drift scripts — the drift scan works on slug/page diffs and this is a sub-feature of
  an existing product's docs subtree.
- Existing gotcha **"No local inference: `wrangler dev` alone fails; use `--remote`"** was **wrong**.
  Live docs (`workers-ai/get-started/workers-wrangler/`) show plain `wrangler dev` runs Workers AI
  (proxies to the account, bills locally). Corrected in place.

**Curated** (all grounded in live docs fetched this pass, URLs cited inline in the ref)

- New section in `references/products/workers-ai.md`: `env.AI.toMarkdown` — PDF = native text
  extraction (StructTree/ISO 14289), no model, no rate limit, free for PDF; per-file `format:"error"`
  handling; `output.format:"text"` + `pdf.metadata:false` options; the form/table StructTree-fallback
  caveat (verify + checksum on real samples); data posture (Customer Content — not shared, not trained
  on, not stored unless you write it to R2; processed on CF infra, not the isolate; image path uses
  third-party-licensed models, PDF path does not); Browser Run `/markdown` is URL/HTML only, not a PDF
  blob. Sources: `markdown-conversion/{,how-it-works/,#pricing,conversion-options/,supported-formats/}`
  + `platform/{data-usage,limits,pricing}/`.
- Added an "extract text from PDF/doc in a Worker" branch to the `AI?` decision tree in SKILL.md.
- Fixed the local-dev gotcha.

**Deferred**

- No documented max file-size / page limit for `toMarkdown` PDF confirmed across all 6
  markdown-conversion pages + limits page + a forum search (only changelog posts, zero user reports).
  Practical ceiling is Worker memory (blob must be materialized). Left as "undocumented" rather than
  inventing a number — revisit if Cloudflare publishes one.
- Encrypted/password-PDF behavior for `toMarkdown`: undocumented. Not curated a claim; flagged
  "handle defensively" in the ref.

**Method** — fact-checked by a fresh adversarial subagent (per `references/fact-check.md`) before
curating: it refuted the local-dev claim and forced the "free for PDF" wording to be hedged. Both
reflected above.

---

## 2026-07-21

**Detected**

- `privacy-pass` — new top-level product in the live directory (live 104 vs. known 103). Caught by
  the existing slug diff.
- **Project Think** — 14 pages under `agents/harnesses/think/`, shipped 2026-04-15 during Agents Week.
  **Not caught by any check.** It ships inside the existing `agents` slug, so the top-level product
  list never moved. It had been invisible for ~3 months. Found only because a human asked about it.

**Root cause**

`update-check` compared only top-level slugs from the master `llms.txt`. Any launch that lands as a
subtree of an existing product was structurally undetectable. Worth noting: the raw source material
for Think (`raw/docs-oficiais/pages/agents/harnesses/think/`) had been captured all along — the
collection step was never the bottleneck, the detection step was.

**Curated**

- `references/products/think.md` — new.
- `references/products/privacy-pass.md` — new.
- `references/products/agents.md` — cross-links `think.md`, with an explicit warning not to mix the two
  Session import paths. Note: this was **not** a correction. The pass began on the assumption that
  `agents/experimental/memory/session` was a stale pre-Think path; checking the rendered docs showed it
  is the current, correct path for the bare `Agent` (Think exports `Session` from its own package
  instead). "Fixing" it would have introduced the bug.
- `SKILL.md` — both added to the catalog; count 84 → 86.
- `references/_known-products.txt` — `privacy-pass` added. Think is deliberately **absent**: it is a
  sub-product of `agents`, and that manifest tracks top-level slugs only.

**Fixed**

- `scripts/pagediff.py` — new. Walks all 104 per-product `llms.txt` files (~2.3s, 8-way parallel),
  folds pages into directory prefixes with counts, diffs against `references/_known-pages.txt`.
  Noise control: reports only the shallowest new prefix per subtree (Think = 1 line, not 14) and
  tallies single-page additions separately instead of flagging them. Unreachable products are
  reported and excluded, so a fetch failure can never read as "this subtree disappeared".
- `scripts/update-check` — calls the above as pass 2; `--shallow` skips it, `--init-baseline` re-records.
- `references/_known-pages.txt` — new baseline: 6575 prefixes across 104 products.

**Adversarial fact-check** (per `references/fact-check.md`, two cold agents, no access to the curator's
reasoning) — run on both new files. 73 claims checked in `think.md`, 52 in `privacy-pass.md`.

The high-risk category passed on both: **zero invented API surface**. Every `@cloudflare/think` export
path, hook name, config default and numeric limit traced to a doc line; every Privacy Pass endpoint,
header, JSON field, RFC number and access-model gotcha traced to a primary source, several verbatim.
Both absence claims were verified independently rather than taken on faith (the `/privacy-pass/pricing/`
404, and the missing official-skill reference dir).

Defects found and fixed — all over-claiming, not fabrication:

- ❗ **"paid Workers plan required"** — factually wrong, and it was in **both** `think.md` and (pre-existing)
  `agents.md`. SQLite-backed Durable Objects run on Workers **Free**; Think uses `new_sqlite_classes`
  exclusively. Verified against the live DO pricing page. This one drove cost decisions.
- ❗ **"1,000 schedules/agent"** — unsourced. Absent from the live `agents/platform/limits` page and from
  the whole docs mirror. Also pre-existing in `agents.md`; now marked unverified in both rather than deleted.
- "the primitives all work standalone on the `Agent` base class … not a prerequisite for **any** capability"
  — false for most of the section it introduced. Only fibers, sub-agents and Session work on the bare
  `Agent`; Actions, Channels, Messengers, scheduled tasks, `runTurn`, `ThinkWorkflow`, extensions and
  `createExecuteTool` are Think-only. Corrected in `think.md` and in the `agents.md` cross-link.
- "typed RPC **at function-call latency**" → docs say only "co-located"/"same machine". Softened.
- extensions "persist in DO storage" → blog-only claim, now labeled as such.
- "PREVIEW" → "experimental", which is the docs' own word; there is no product-level preview banner.
- Privacy Pass: "**Never** combine Origin + Attester … guarantee collapses" → docs say "generally not" /
  "significantly harder", and RFC 9578 permits joint models under guidelines. "Cloudflare … issues the
  mTLS client certificate" → docs put that cert on the customer's side. "pay only for Workers" → the
  reference issuer stores keys in **R2**. "the two proxies are Enterprise-only" → Privacy Gateway is
  **closed beta to select partners**; Enterprise is not sufficient. Cost "negotiated as part of the
  engagement" → unsourced, dropped.

Two of these (paid-plan, 1000-schedules) were **pre-existing errors in `agents.md`**, not introduced by
this pass. They surfaced only because the fact-check ran. Worth repeating on the next curation.

**Blog ↔ docs divergences found while curating Think** (docs win; all flagged inside `think.md`)

The announcement blog is 2026-04-15 and the rendered docs have moved since. Recorded here because
the blog is the first thing a search turns up, so these are live hallucination traps:

- **`createSandboxTools` / `@cloudflare/think/tools/sandbox` does not exist.** The blog's "full
  execution ladder" snippet imports it; the documented package exports are only `/tools/workspace`,
  `/tools/execute`, `/tools/browser`, `/tools/extensions` (+ `/messengers`, `/workflows`,
  `/extensions`). Tier-4 Sandbox is a separate surface (`agents/tools/sandbox/`). Biggest risk of the set.
- Model id: blog `@cf/moonshotai/kimi-k2.5` → docs `@cf/moonshotai/kimi-k2.6`. (Verified independently:
  every Think doc page uses `k2.6`. `k2.7-code` also exists but only under `agents/tools/codemode/browser/`
  — a different surface and a `-code` variant, not a newer id for the same slot. Not a contradiction.)
- Blog's install line omits `@cloudflare/ai-chat`, which the docs quick-start requires (client
  `useAgentChat` comes from `@cloudflare/ai-chat/react`).
- Doc paths moved: `agents/api-reference/{sessions,sub-agents,durable-execution,chat-agents}` →
  `agents/runtime/lifecycle/sessions/`, `agents/runtime/execution/*`, `agents/harnesses/think/*`.
- Extension manifest shape differs; the documented `{ manifest: { name, version, permissions }, source }`
  was used, not the blog's.
- **"Execution ladder" is blog-only vocabulary** — the term appears nowhere in the rendered docs. Kept
  in `think.md` but labeled as blog framing, so it is never quoted back as official API taxonomy.

**Checked and NOT a problem** (recorded so the next pass doesn't re-investigate)

- The rest of Agents Week 2026-04 is already curated — `artifacts`, `email-service`, `browser-run`,
  `ai-search`, `agent-memory`, `dynamic-workers`, `sandbox`, `realtime`. Every one of those got its
  own top-level slug, so the old check caught them. Think was the sole escapee, and sub-product
  launches are the only known blind spot.

**Promoted to the installed skill** (`~/.claude/skills/cloudflare-atlas`)

This pass surfaced that `~/.claude/skills/cloudflare-atlas` and `cloudflare-skill-prep/cloudflare-atlas`
had been drifting as two independent copies. The installed one — the only one `/cloudflare-atlas`
actually loads — was carrying product references from **2026-06-26**: the 07-12 curation pass had never
been promoted either. Meanwhile the installed copy had a 07-11 edit (the `cloudflare-forum` escalation
rule in Core rule + Optional complements) that the prep copy never had, so a copy in either direction
would have destroyed work.

Resolved: forum escalation block ported prep-ward first, then the full tree promoted with `rsync`.
Both trees now byte-identical, verified with `diff -rq`. Backup of the pre-merge installed skill at
`~/.claude/skills-backups/cloudflare-atlas-20260721` — kept OUTSIDE `~/.claude/skills/`, because a
backup directory placed inside it gets registered as a real, invocable skill.

**The installed copy is the source of truth.** The prep directory is a workbench; anything curated there
is worthless until promoted. Verify a promotion is non-destructive first: for every file present in both,
`diff` must show no line existing only on the installed side.

**Deferred**

- A "subtrees with no curated coverage" heuristic run over the new baseline returned 121 hits, but is
  dominated by structural noise — `ddos-protection/change-log` (94 pages), `style-guide/*`,
  `support/troubleshooting/*`. Doc depth is not curation debt, and the catalog is intentionally a
  high-level map. Not acted on. If this is ever revisited, it needs a relevance filter first, not a
  bigger page count.
- `scripts/changelog-check` references an offline fallback snapshot at
  `references/changelog/changelog-rss.xml` that does not exist — the fallback branch is dead code
  today. Harmless (the live fetch is the real path). Left alone deliberately; pre-existing.
- Changelog items from the 7-day window worth a content-drift pass, none of which changed structure:
  Workers KV deprecating legacy namespace API routes (2026-07-15) · Internal DNS now GA
  (2026-07-15) · Email Service + Queues event subscription (2026-07-15) · Workers for Platforms
  temporary accounts via API (2026-07-14).

## 2026-07-22 — cross-ref supabase2d1
- Detectado: gap real validado em produção — migração Supabase/Postgres→D1 não tem caminho oficial (docs D1 confirmam) e a skill supabase2d1 foi criada/testada hoje contra projeto real.
- Curado: 3 cross-refs adicionadas — Boundaries (exceção do Hyperdrive quando o objetivo é SAIR do Postgres), Optional complements, e references/products/d1.md (incl. gotcha unistr).
- Deferido: nada — mudança é só roteamento; o conteúdo da migração vive na supabase2d1 (fonte única).
