---
name: cloudflare-atlas
description: >-
  Deep, always-current Cloudflare expertise that goes beyond the official docs. Use this to
  ARCHITECT a product 100% on Cloudflare (pick the right services, wire them, no external stack
  unless genuinely required), and as a build-time guardrail so nothing Cloudflare-specific is
  hallucinated. Reach for it whenever a task needs the right Cloudflare product for a job, an EXACT
  API endpoint/param/limit, a NEW or niche product the official skill misses (agent-memory,
  browser-run, dynamic-workers, moq, email-service, ai-search, realtime, think, privacy-pass),
  CURRENT info that
  pre-trained knowledge gets wrong (limits, pricing, changelog), or a review/AUDIT of Workers code or
  an existing Cloudflare codebase/config. It
  orchestrates the ecosystem — self-sufficient on its own references, treating the `cloudflare-forum`
  skill and the Cloudflare MCP servers as optional complements when present. Use on any non-trivial Cloudflare build,
  architecture, or debugging task, even if no product is named.
---

# Cloudflare Atlas

A retrieval-first orchestrator for building on Cloudflare. Your pre-trained knowledge of Cloudflare
APIs, limits, pricing, and config is probably outdated — Cloudflare ships constantly. **Prefer
retrieval over memory.** This file is a **map**: pick the right product from the catalog, then read
its `references/products/<slug>.md` for depth. Use the live sources to verify specifics.

## Primary workflow: architect a product 100% on Cloudflare

The #1 job: turn a product idea into a complete, correct, **Cloudflare-native** architecture.

1. **Understand the product.** What it does, scale, hard constraints. Ask only the few questions
   that change the architecture.
2. **Map needs → products.** Use the Decision trees, then the Catalog below. Prefer a proven shape
   from `references/products/<slug>.md` over inventing one.
3. **Ground every choice.** Confirm each service exists, is current, and fits (verify limits via the
   live sources). Never invent a Cloudflare product or stretch one past its real capabilities.
4. **Check the boundary.** If a need has no Cloudflare answer (see Boundaries), say so and name the
   external piece explicitly — do not silently mix stacks, and do not force a wrong fit.
5. **Produce the architecture:** components (service + role), data flow, `wrangler.jsonc` bindings,
   rationale per choice (+ the alternative rejected), gotchas.
6. **Estimate the cost.** For each chosen product, state: what's free (free-tier allowance), the
   cost drivers (what you pay per — requests, GB stored, GB egress, rows read, neurons, etc.), and
   a rough **monthly estimate at the user's scale** (translate their numbers — users, requests,
   storage — into each product's billing units). List your assumptions explicitly. Pricing is the
   MOST volatile data here: **verify every number against the live pricing page**
   (`developers.cloudflare.com/<product>/.../pricing/` or `references/products/<slug>.md`) before
   quoting it — the reference is a starting point, the live page wins. Present it as an estimate
   with assumptions, never a hard quote. Then fact-check (below).

## Audit mode (audit a codebase / config 100%)

When the task is to **audit / review** an existing codebase or `wrangler` config (not build new),
run this fixed rite — don't improvise it:

1. **Scope.** Map the code to Cloudflare surfaces: grep bindings in `wrangler.jsonc`/`toml` and
   imports (`cloudflare:*`, `@cloudflare/*`, `env.*`). List the surfaces in play (workers, d1, kv, r2,
   queues, durable-objects, ai, email, stream, etc.).
2. **Audit per surface** (fan out — for big codebases, small sequential groups to respect rate limits).
   Each surface: read `references/code-review/` + `references/products/<slug>.md` + `references/api/<slug>.md`
   + the **real code** + the project's own types (`@cloudflare/workers-types`, `wrangler/config-schema.json`,
   `worker-configuration.d.ts` — primary source for code claims). Check these dimensions:
   - deprecated product/API · limit exceeded or wrong · **invented/nonexistent** service or method
   - **non-CF-native where a CF equivalent exists** (stack leak — e.g. S3→R2, Pinecone→Vectorize,
     a 3rd-party video host→Stream, Resend→Email Service) — see Boundaries
   - security gotchas (auth/crypto/secrets) · config↔code mismatch (binding names, DO migrations)
   - cost surprise (limit/pricing) · the per-product Gotchas
   Emit findings by **severity (CRITICAL → HIGH → MEDIUM → LOW)** + extract the verifiable claims.
3. **Adversarial fact-check (mandatory).** A fresh agent (no access to the auditor's reasoning) verifies
   every cited limit / endpoint / availability claim against the LIVE docs (`cloudflare-docs` MCP /
   WebFetch + `scripts/changelog-check`), per `references/fact-check.md`. Drop or qualify anything it refutes.
4. **Report.** Consolidate: per-product verdict · verified findings by severity (with file:line evidence)
   · **CF-native opportunities** (what could move onto Cloudflare) · concrete `wrangler.jsonc` fixes.
   Never assert a number you didn't verify live.

## Decision trees (pick by need)

```
Run code?      → workers · full-stack w/ git: pages · stateful/realtime: durable-objects
               · long multi-step: workflows · containers · multi-tenant: cloudflare-for-platforms
               · scheduled: workers (cron) · on-demand isolates: dynamic-workers
Store data?    → key-value: kv · SQL (SQLite): d1 · object/files: r2 · existing PG/MySQL: hyperdrive
               · queue: queues · vectors/RAG: vectorize · per-entity state: durable-objects
               · streaming ETL→R2: basin-pipelines · Iceberg lakehouse on R2: basin-catalog
               · SQL over R2/Iceberg: basin-sql · durable logs/streams: k2 · secrets: secrets-store
AI?            → inference: workers-ai · vector DB: vectorize · agents: agents · agent memory:
               agent-memory · any-provider gateway: ai-gateway · managed RAG: ai-search
               · web search for agents/LLMs: web-search · model catalog (all vendors): ai
               · extract text from PDF/doc in a Worker: workers-ai `env.AI.toMarkdown` (native
                 text extraction, no model, free for PDF — before unpdf/LiteParse or external OCR)
Realtime/media?→ video: stream · images: images · WebRTC/live: realtime · live media: moq
               · headless browser: browser-run
Networking?    → expose origin: cloudflare-tunnel · L4 proxy: spectrum · LB: load-balancing
               · private IP between devices/servers (VPN replacement): mesh
Security?      → WAF: waf · CAPTCHA: turnstile · bots: bots · DDoS: ddos-protection
Email?         → SEND transactional: email-service · RECEIVE/route: email-routing
Edge logic?    → request rules: rules · lightweight snippets: workers (snippets)
Analytics?     → custom metrics: analytics (Analytics Engine) · cross-product: graphql or SQL API (analytics) · web RUM: web-analytics
               · logs/traces/OTel export across products: observability
```

When in doubt, scan the full Catalog. **Atlas's own references are self-sufficient — use them.** For
deeper detail than a reference holds, the **live docs** (`developers.cloudflare.com/<product>/`) are
canonical (fetch as Markdown). The official `cloudflare` skill is an optional extra *if installed* —
never subordinate Atlas's own refs to it.

## Product catalog (all 96 — the map)

Pick a product, then read `references/products/<slug>.md` for depth. If nothing here fits, that's a Boundary signal.
### Application performance
- **Argo Smart Routing** — Route web traffic across the fastest, most reliable network paths → products/argo-smart-routing.md
- **Automatic Platform Optimization** — Improve WordPress site performance by serving it from Cloudflare's global network → products/automatic-platform-optimization.md
- **Cache / CDN** — Make websites faster by caching content across our global server network → products/cache.md
- **China Network** — Fast, global network serving visitors inside and outside of China → products/china-network.md
- **DNS** — Deliver excellent performance and reliability to your domain → products/dns.md
- **Google tag gateway for advertisers** — Add a layer of data security and privacy controls when using Google Tag Manager → products/google-tag-gateway.md
- **Health Checks** — Monitor IPs or hostnames and get notified of issues → products/health-checks.md
- **Load Balancing** — Maximize application performance and availability → products/load-balancing.md
- **Smart Shield** — Safeguard your origin with just a few clicks. → products/smart-shield.md
- **Spectrum** — Secure and accelerate any TCP or UDP-based application → products/spectrum.md
- **Speed** — Improve the performance of your website or web application → products/speed.md
- **SSL/TLS** — Encrypt your web traffic to prevent data theft and other tampering → products/ssl.md
- **Waiting Room** — Create a virtual waiting room to manage peak traffic → products/waiting-room.md
- **Cloudflare Web Analytics** — Get vital web analytics for your website → products/web-analytics.md
- **Web3** — Gateways to networks to help you develop applications without worrying about running infrastructure → products/web3.md

### Application security
- **API Shield** — Identify and address your API vulnerabilities → products/api-shield.md
- **Bots** — Protect your domain from bad bot traffic → products/bots.md
- **Client-side security** — Provide client-side protection for your website visitors → products/client-side-security.md
- **Challenges** — Verify visitors are not bots with lightweight challenges → products/cloudflare-challenges.md
- **DDoS Protection** — Protect against DDoS attacks automatically with uncompromised performance → products/ddos-protection.md
- **DMARC Management** — Protect your email domain and stop brand impersonation → products/dmarc-management.md
- **Key Transparency Auditor** — Secure the distribution of public keys in E2EE messaging systems → products/key-transparency.md
- **Privacy Pass** — Anonymous cryptographic tokens (IETF RFC 9576) that prove an attribute without revealing identity → products/privacy-pass.md
- **Secrets Store** — Encrypt and store sensitive information as secrets that are securely reusable across an account → products/secrets-store.md
- **Security Center** — Enhance your security posture with a range of security products and one-click solutions → products/security-center.md
- **Turnstile** — Turnstile is Cloudflare's smart CAPTCHA alternative → products/turnstile.md
- **WAF** — Filter incoming traffic and protect against web app vulnerabilities → products/waf.md

### Core platform
- **AI Crawl Control** — Analyze and control third-party AI crawlers in your website → products/ai-crawl-control.md
- **Analytics** — Visualize the performance, security, and reliability data collected by Cloudflare products → products/analytics.md
- **Observability** — Cross-product hub for logs, traces and OpenTelemetry export (Workers + Cloudflare services) → products/observability.md
- **Billing** — Manage billing, plans, and subscriptions for your account → products/billing.md
- **Cloudflare Fundamentals** — Learn about using Cloudflare and features that span across Cloudflare products → products/fundamentals.md
- **Log Explorer** — Store and explore your logs in the Cloudflare dashboard or API → products/log-explorer.md
- **Logs** — Logpush (usage-based on every plan since 2026-09-30), Transformers, Instant Logs, Logpull → products/logs.md
- **Network** — Manage Cloudflare network settings for your website → products/network.md
- **Notifications** — Define what you want to be notified about and how → products/notifications.md
- **Pulumi** — Create, deploy, and manage Cloudflare resources in various programming languages → products/pulumi.md
- **Randomness Beacon** — Explore drand, a distributed service providing randomness to applications → products/randomness-beacon.md
- **Reference Architecture** — Guides and diagrams explain Cloudflare products and how to integrate with IT architectures → products/reference-architecture.md
- **Registrar** — Buy and renew your domain at cost, add another layer of security to your DNS records for free → products/registrar.md
- **Resource Tagging** — Attach key-value metadata to Cloudflare resources for organization, access control, and billing attribution → products/resource-tagging.md
- **Rules** — Modify incoming requests, change Cloudflare settings, or trigger actions → products/rules.md
- **Ruleset Engine** — Create rulesets and rules for different Cloudflare products → products/ruleset-engine.md
- **Support** — Cloudflare Support-focused documentation → products/support.md
- **Cloudflare Mesh** — Private IP networking between servers, laptops and phones (formerly WARP Connector); post-quantum encrypted, bidirectional → products/mesh.md
- **Tenant** — Provision and manage Cloudflare accounts and services for your team or customers → products/tenant.md
- **Terraform** — Define and store Cloudflare configurations in source code repositories like GitHub → products/terraform.md
- **Time Services** — Cloudflare's suite of time services: NTP, NTS, and Roughtime → products/time-services.md
- **Cloudflare Tunnel** — Connect your origin servers, APIs, and services to Cloudflare without a publicly routable IP address → products/tunnel.md
- **Version Management** — Safely manage configurations on Cloudflare's global network with versioning, staging, and rollbacks → products/version-management.md

### Developer platform
- **Agent Lee** — An AI co-pilot built into the Cloudflare dashboard that helps you navigate, configure, and take actions on… → products/agent-lee.md
- **Agent Memory** — Persistent AI-powered memory for agents and applications — automatically extract, classify, and recall… → products/agent-memory.md
- **Agent setup** — Wire your own coding agent (Claude Code, Codex, Cursor, Copilot, VS Code, OpenCode, Windsurf) to Cloudflare via Skills + MCP servers → products/agent-setup.md
- **Agents** — Build AI-powered agents to perform tasks, persist state, browse the web, and communicate in real-time → products/agents.md
- **Think (Project Think)** — ⚠️ preview. Opinionated chat-agent harness inside the Agents SDK (`@cloudflare/think`): durable execution (fibers), sub-agents, tree-structured sessions, sandboxed code execution → products/think.md
- **AI** — Run AI models on Cloudflare's global network → products/ai.md
- **AI Gateway** — Observe and control your AI applications → products/ai-gateway.md
- **Web Search API** — Web search results for AI agents and LLM apps, via AI Gateway (launched 2026-10-02) → products/web-search.md
- **AI Search** — Create fully managed RAG pipelines for your AI applications → products/ai-search.md
- **Artifacts** — Store, version, and share filesystem artifacts across Workers, APIs, and git-compatible tools → products/artifacts.md
- **Browser Run** — Control and interact with headless browser instances programmatically → products/browser-run.md
- **Cloudflare for Platforms** — Build your own multi-tenant platform using Cloudflare as infrastructure → products/cloudflare-for-platforms.md
- **Containers** — Enhance your Workers with serverless containers → products/containers.md
- **D1** — Create managed, serverless databases with SQL semantics → products/d1.md
- **Durable Objects** — A special kind of Cloudflare Worker combining compute with storage → products/durable-objects.md
- **Dynamic Workers** — Spin up isolated Workers on demand to execute code → products/dynamic-workers.md
- **Email Service** — Send transactional emails at scale with Cloudflare Email Service → products/email-service.md
- **Flagship** — Feature flags evaluated at the edge for Cloudflare Workers → products/flagship.md
- **Hyperdrive** — Accelerate database queries to make databases fast globally → products/hyperdrive.md
- **Cloudflare Images** — Store, transform, optimize, and deliver images at scale → products/images.md
- **KV** — Global, low-latency, key-value data storage → products/kv.md
- **MoQ** — Protocol for live media → products/moq.md
- **Pages** — Build full-stack, serverless applications globally with minimal configuration → products/pages.md
- **Basin Pipelines** — Streaming ingestion + SQL transforms + delivery to R2 as Iceberg/Parquet/JSON (GA 2026-10-01, formerly Cloudflare Pipelines) → products/basin-pipelines.md
- **OHTTP Relay** (formerly Privacy Gateway) — Implement the Oblivious HTTP IETF standard to hide client IPs from app backends → products/ohttp-relay.md
- **Privacy Proxy** — A MASQUE-based forward proxy that protects user privacy while preserving geolocation accuracy → products/privacy-proxy.md
- **Queues** — Reliably send and receive messages without the egress fees → products/queues.md
- **R2** — Store large amounts of unstructured data without egress fees → products/r2.md
- **Basin Catalog** — Managed Apache Iceberg REST catalog in R2; zero egress for external engines (GA 2026-10-01, formerly R2 Data Catalog) → products/basin-catalog.md
- **Basin SQL** — Serverless distributed SQL over Iceberg tables in Basin Catalog (GA 2026-10-01, formerly R2 SQL) → products/basin-sql.md
- **Basin** — End-to-end serverless analytics platform: Pipelines + Catalog + SQL on R2 (GA 2026-10-01) → products/basin.md
- **Cloudflare CLI (cf)** — Unified CLI for Cloudflare API + Workers projects; typed config, agent-friendly (beta 2026-09-28) → products/cf.md
- **K2** — Serverless durable logs; decoupled producers/consumers with configurable retention (public beta) → products/k2.md
- **Monetization Gateway** — Per-request payments via x402 protocol inline in HTTP flow (closed beta, US-only) → products/monetization-gateway.md
- **Realtime** — RealtimeKit, SFU and TURN → products/realtime.md
- **Sandbox SDK** — Isolated Linux sandboxes driven from your own Durable Object (SDK 1.0, 2026-09-30) → products/sandbox.md
- **Stream** — Store, encode, deliver, and play videos on sites and applications → products/stream.md
- **Vectorize** — Store, query, and manage high-dimensional vector databases → products/vectorize.md
- **Wallets** — ⚠️ pre-launch. Reserve a wallet handle today; later, stablecoin wallets that let an account delegate a capped spend budget to its AI agents → products/wallets.md
- **Workers** — Build, deploy, and scale serverless applications globally with low latency and minimal configuration → products/workers.md
- **Workers AI** — Run AI models in Workers, Pages, or via API → products/workers-ai.md
- **Workers VPC** — Connect Cloudflare Worker's Virtual Private Cloud to your private clouds to build cross-cloud apps. → products/workers-vpc.md
- **Workflows** — Build durable, multi-step applications using the Workers platform → products/workflows.md
- **Zaraz** — Run third-party tools and services on the cloud for improved speed and security → products/zaraz.md

### Docs collections
- **Learning Paths** — Guided modules and projects to help you get started with Cloudflare → products/learning-paths.md

### Other
- **Use cases** — Discover what's possible with Cloudflare. → products/use-cases.md

## Coverage boundary — the 18 live products this skill does NOT curate

The catalog above is 96 files against **112 live products** (`scripts/update-check`, 2026-10-27). The other 18 have no reference file here,
and until 2026-09-04 the skill never said so: a question about Access hit silence, and silence is
where pre-trained guessing fills in. Say "atlas does not cover this" and route, rather than answering
from memory.

**Zero Trust / SASE family — covered by SIBLING SKILLS, not by atlas.** Do not answer these from
this skill's references; load the dedicated skill, which is current and substantially deeper than a
product file would be:

| Need | Go to |
|------|-------|
| Access (apps, policies, service tokens, mTLS, SaaS SSO), Gateway, WARP/device posture, tunnels-as-ZT | the **`cloudflare-one`** skill |
| Migrating onto Cloudflare One from another SASE/ZTNA vendor | the **`cloudflare-one-migrations`** skill |

`cloudflare-one` alone is 732 doc pages — larger than any product file in this catalog and larger
than most of them combined. Duplicating it here would create the second, staler source of truth this
skill exists to prevent.

**Network / connectivity products with no atlas file and no sibling skill** — answer ONLY from live
docs (`developers.cloudflare.com/<slug>/llms.txt`), never from memory:
`1.1.1.1` · `byoip` · `cloudflare-network-firewall` · `cloudflare-wan` · `data-localization` ·
`firewall` · `magic-transit` · `multi-cloud-networking` · `network-error-logging` · `network-flow` ·
`network-interconnect` · `radar` · `security` · `warp-client`

**Not products** (Cloudflare doc-site infrastructure, nothing to curate): `docs-for-agents` ·
`migration-guides` · `style-guide`

`scripts/check-pointers` keeps the catalog's own cross-references honest; this section is what keeps
its *silences* honest.

## Boundaries — what Cloudflare does NOT do (so you know when external is legit)

Keep everything on Cloudflare **except** these. When one applies, name the external piece explicitly.

- **Payment processing** — no Cloudflare product. Use Stripe / Mercado Pago / Adyen / etc.
- **Identity provider for "SSO with X"** — Google/Microsoft/etc. are the external IdP. You still
  build the auth server on Workers (sessions in KV/D1) — do NOT reach for Auth0/Clerk/Cognito.
- **Hosted Postgres/MySQL as a managed DB** — D1 is SQLite. For Postgres/MySQL you connect to an
  EXTERNAL db, accelerated by **Hyperdrive** (the external db is the only off-CF piece).
  EXCEPTION — full migration OFF the external db: to actually move a Supabase/Postgres project
  onto Cloudflare (Postgres→D1, Storage→R2, Edge Functions→Workers), use the `supabase2d1`
  skill if installed — there is NO official Cloudflare path (the D1 docs explicitly say Postgres
  dumps cannot be imported), and that skill carries the battle-tested converter + validation.
- **Always-on VMs / long-lived servers** — Workers/Containers are request-scoped; no persistent VM.
- **Model training** — Workers AI is inference only.

NOT a boundary (common hallucinations to avoid):
- **Sending email IS native** → `email-service` (transactional send). Do NOT reach for Resend/SES/Postmark.
- **Managed RAG IS native** → `ai-search` (AutoRAG). Do NOT reach for an external RAG service.
- **Vector DB IS native** → `vectorize`. Do NOT reach for Pinecone/Weaviate.
- **Realtime coordination IS native** → `durable-objects`. Do NOT reach for Redis/Socket.io.

## Retrieval sources (live — work today)

| Need | Source |
|------|--------|
| Product docs (any page) | `developers.cloudflare.com/<product>/llms.txt` (index) · any page via `Accept: text/markdown` or `index.md` |
| Exact API endpoints | `references/api/<slug>.md` (exact REST paths/methods/required params, sliced from the OpenAPI spec) — then `references/products/<slug>.md` for usage; verify shapes live |
| Newest/limits/pricing | live changelog — `scripts/changelog-check <product>` |
| Live doc search | the `cloudflare-docs` MCP server (if available) |
| Workers types / wrangler schema | the project's `node_modules` (`@cloudflare/workers-types`, `wrangler/config-schema.json`) |
| Design rationale / tradeoffs ("why") | the live blog — `blog.cloudflare.com/<slug>` (any post via `Accept: text/markdown`); no blog corpus is bundled |

## Core rule: retrieval-first, verify before asserting

Before stating any specific number, API signature, config field, or limit: retrieve the current
source; if it disagrees with memory, **the live source wins**; if you cannot verify, mark it
uncertain rather than inventing it. A confident wrong limit is worse than an honest "let me check."

When the official sources (docs/changelog/API) don't resolve a **behavior or error** — an obscure
5xx/1020, an undocumented edge case, a suspected bug — don't stop at "uncertain": escalate to the
`cloudflare-forum` skill (real-world community reports and workarounds) before giving up. Official
sources own limits/pricing/signatures; the forum owns lived experience.

### If a gate says a term is NOT FOUND, that is not permission to edit

`scripts/verify-products` reports each quotable token in a product file as CONFIRMED or NOT FOUND
against the live docs. **NOT FOUND is a prompt to look, never a verdict that the file is wrong.**
Before changing anything on the strength of one:

1. **Check the parent and sibling corpora.** A product file legitimately cites APIs documented one
   level up. On 2026-08-25 the gate accused four correct names in `think.md` — `ctx.stash`,
   `ctx.snapshot`, `onFiberRecovered`, `parent_id` — because its corpus was scoped to the
   `think` subtree while all four live under `agents/runtime/execution/durable-execution/`. A
   replacement was already being drafted when the parent page was opened.
2. **Check whether the file is asserting the absence.** "There is no `agents/ai-react` subpath" and
   "`createSandboxTools` does not exist today" both read as NOT FOUND. The gate cannot tell a
   missing term from a term the file correctly reports as missing.
3. **Check the live blog (`blog.cloudflare.com`) and the OpenAPI spec** before concluding a term is invented — endpoints and
   preview-product APIs often live in neither the docs prose nor the product's own pages.

**A false accusation from this gate is more dangerous than a missed one.** A miss leaves the file
as it was; acting on a false accusation turns correct content into fabricated content — and the
next run reports green, because the invention was copied from a real page. Only edit when the term
is absent from *every* source above.

## Adversarial fact-check (anti-hallucination backstop)

For substantial answers — an architecture, or code/config the user will deploy, or several
verifiable claims, or when asked "are you sure?" — spawn a **fresh subagent** (no access to your
reasoning) with the prompt in `references/fact-check.md`. It extracts every technical claim, sources
each against the live docs/changelog, and returns a `claim → source → status` table. Fix or qualify
anything flagged before finalizing. Skip it for quick one-off lookups.

## Optional complements (use if present — Atlas does not depend on them)

Atlas is standalone. These are *extra* tools to reach for when available, not requirements:
- Community error / undocumented behavior / suspected bug / "has anyone hit this" → the
  `cloudflare-forum` skill (real-world reports + workarounds; handles the forum's Managed Challenge —
  do NOT reimplement that). This is the escalation target when official sources can't confirm a
  behavior (see Core rule).
- Live ops (deploy, inspect bindings, read logs) → the Cloudflare MCP servers (builds/bindings/observability).
- The official `cloudflare` skill, *if installed* → extra curated patterns on covered products. Optional —
  Atlas's own references already cover the job; for more depth prefer the live docs.
- Migrating a Supabase/Postgres project INTO Cloudflare (D1/R2/Workers) → the `supabase2d1` skill
  (full dump incl. auth users + Postgres→SQLite conversion + mandatory count/integrity validation).

## Reviewing Workers code

Load `references/code-review/` when reviewing TS/JS using Workers APIs, `wrangler.jsonc`, or bindings.
It covers binding access (`env.X` vs `this.env.X`), floating promises, serialization across
Queue/Workflow/DO boundaries, DO anti-patterns, and config validation. Verify specifics against the
project's actual types and schema, not memory.

## Staying current (this skill goes stale — manage it)

Cloudflare ships constantly, so the bundled references are a **snapshot**, not the truth.

- **Content drift** (a limit/price/API changed): handled at runtime — retrieval-first + the verify-live
  rule + `scripts/changelog-check <product>`. The live page always wins over a reference file.
- **Structural drift** (a NEW product appeared, or one was renamed/removed): run
  **`scripts/update-check`**. It diffs the live product directory + recent changelog against what this
  skill knows (`references/_known-products.txt`) and reports what's new/gone/changed. Run it when you
  suspect the skill is behind, or on a schedule.
- **Sub-product drift** (a launch landed INSIDE an existing product, so no new slug appeared): also
  `scripts/update-check` — it walks every product's own `llms.txt` and diffs the doc subtrees against
  `references/_known-pages.txt`, reporting only the shallowest new prefix per subtree so one launch is
  one line. This is not hypothetical: Project Think shipped as 14 pages under `agents/harnesses/think/`
  and the top-level slug list never moved, so it stayed invisible for three months. Use `--shallow` to
  skip this pass; re-record the baseline with `--init-baseline` after curating.
- **Run a refresh with `scripts/refresh`, not from memory.** `scripts/refresh` detects and reports;
  `scripts/refresh --close [--spec <openapi.json>]` closes the pass in the only safe order and
  **refuses to re-record the page baseline until `CHANGELOG.md` has an entry for today containing a
  Deferred section** — because that re-record is what erases the evidence of what the pass saw.
  Do not add a bypass flag. The manual steps below are what it automates, kept for when it breaks.
- **Refresh procedure** when `update-check` finds a new product: curate it with
  `references/_curation-guide.md`, add its slug to `references/_known-products.txt` and the catalog
  above, then re-slice `references/api/` with `scripts/slice-api <spec.json>` (fetch the current spec
  from `raw.githubusercontent.com/cloudflare/api-schemas/main/openapi.json`). Run
  `scripts/slice-api --validate <spec>` first — it fails if any slug would lose coverage. A brand-new
  product needs its slice seeded by hand once; the matcher is derived from a slug's existing slice, so
  it has nothing to derive from on the first pass.
- **Log every pass in `CHANGELOG.md`** — what was detected, what got curated, and above all what was
  *deferred*. Product changelogs are retrievable live and must never be mirrored here; curation
  decisions are not retrievable anywhere, and an unlogged deferral is exactly how a launch goes
  missing for months.
- **True automation** (self-update without a human): out of the skill's own scope — a skill is static
  files. Wire `scripts/update-check` into a cron/CI job (or a scheduled agent) to get periodic drift
  alerts; the refresh itself still wants a review pass.

## Notes

References and scripts are accelerators, not the source of truth. When a reference and the live docs
disagree, trust the docs. Cite the page or changelog entry when a claim could be questioned.
