# Cloudflare for Platforms — multi-tenant SaaS where YOUR customers deploy code & domains

> Build a platform where your customers (or AI) deploy code and bring their own domains. Two pillars:
> **Workers for Platforms** (run untrusted customer code in isolated Workers) and **Cloudflare for SaaS**
> (extend Cloudflare to customers' custom hostnames). Use them together or separately.

## Contents
- When to use (and when not)
- The two pillars
- Workers for Platforms — architecture & config
- Cloudflare for SaaS — custom hostnames
- Binding & config (`wrangler.jsonc`)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You run a **SaaS platform and your customers deploy their own code/configs** — website builders,
  ecommerce storefronts, AI "vibe coding" app builders, low-code tools, per-customer code snippets.
- Customers need **their own domain** (`app.customer.com`) or **subdomain** (`customer.myplatform.com`)
  pointing at your service, with Cloudflare TLS/WAF/CDN extended to it.
- You want each tenant to get **isolated compute + their own DB/KV/R2** without building the infra yourself.
- **Not** for: running *your own* code (→ plain `workers`); a single app on one domain; SSO/access gating
  for an internal app (→ `cloudflare-one`/Access). If you just need one-off custom domains for *your* app
  (not per-customer at scale), a normal custom domain on a Worker is simpler than Cloudflare for SaaS.

## The two pillars
| Pillar | Solves | Core primitive |
| --- | --- | --- |
| **Workers for Platforms (W4P)** | run untrusted customer/AI code at scale, isolated per tenant | dispatch namespace + dispatch Worker + user Workers |
| **Cloudflare for SaaS** | put customers' custom/vanity domains in front of your origin | custom hostnames on your zone + fallback origin |

Many platforms use **both**: W4P runs the code; Cloudflare for SaaS gives each customer their domain, and
the dispatch Worker routes the hostname → the right user Worker (via KV or custom-hostname metadata).

## Workers for Platforms — architecture & config
Four components (request flow: client → dispatch Worker → user Worker → [outbound Worker] → internet):
1. **Dispatch namespace** — container holding all your customers' Workers (unlimited scripts). Untrusted
   by default: no `request.cf`, `caches.default` disabled.
2. **Dynamic dispatch Worker** — your entry point. Routes each request to a user Worker via
   `env.DISPATCHER.get(name)` then `.fetch(request)`. Add auth, validation, per-tenant limits here.
   Route by **subdomain**, **path**, or **KV/custom-hostname-metadata** lookup.
3. **User Workers** — your customers' code, isolated. Deployed via the **Upload User Worker API**
   (multipart, not Wrangler config). Attach per-tenant **bindings** (KV/D1/R2/DO/Analytics Engine) in the
   `metadata` object — use `keep_bindings` to preserve existing ones on update.
4. **Outbound Worker** (optional) — intercepts user Workers' `fetch()` for egress logging / allowlists /
   injecting credentials. Pass context via `dispatcher.get(name, {}, { outbound: { params } })`.

**Custom limits** — pass per-invocation caps in the dispatch Worker:
`env.DISPATCHER.get(name, {}, { limits: { cpuMs: 10, subRequests: 5 } })`. Key for denial-of-wallet
protection; vary by customer plan. User Worker throws immediately when a limit is hit.

## Cloudflare for SaaS — custom hostnames
Lets customers point `app.customer.com` (vanity) or a subdomain at your zone. Setup:
1. **Fallback origin** — one proxied A/AAAA/CNAME record on your zone; default target for all custom-hostname
   traffic. (Per-hostname overrides via **custom origin server**.)
2. **CNAME target** (recommended) — e.g. `customers.saasprovider.com`; what you tell customers to CNAME to.
3. **Create custom hostname** — `POST` Create Custom Hostname API per customer domain. Cloudflare issues
   certs (ECDSA P-256 + RSA 2048 fallback) and validates ownership.
4. **Customer adds CNAME** at their DNS → your CNAME target.
- **Two independent statuses**: `result.status` (hostname proxying) and `result.ssl.status` (cert issued).
  Treat hostname as production-ready only when **both** are `active`. POST may not return DCV
  `validation_records` — re-GET with a delay.
- **Custom metadata** can be attached per hostname and read in the dispatch Worker for routing decisions.
- Apex domains (customer can't CNAME at root) need **Apex Proxying** or **BYOIP** (Enterprise add-ons).

## Binding & config (`wrangler.jsonc`)
Dispatch namespace binding on the dispatch Worker (optionally with an outbound Worker):
```jsonc
{
  "dispatch_namespaces": [
    {
      "binding": "DISPATCHER",
      "namespace": "my-dispatch-namespace",
      "outbound": { "service": "my-outbound-worker", "parameters": ["params_object"] }
    }
  ]
}
```
Dispatch Worker core:
```js
const userWorker = env.DISPATCHER.get(workerName);     // throws "Worker not found" if missing
return await userWorker.fetch(request);
```
User Worker bindings are set via the **Upload User Worker API** (`metadata.bindings`, not wrangler).
Fastest start: deploy the **Platform Starter Kit** (`worker-publisher-template`) or **VibeSDK** (AI app
builder) — both auto-configure the namespace + routing.

## Gotchas
- **`env.DISPATCHER.get()` always wrap in try/catch** — `"Worker not found"` → return 404; rethrow others.
- **`keep_bindings`** when updating a user Worker, or you'll drop existing bindings.
- **Untrusted by default**: no `request.cf`, `caches.default` disabled. Enable **trusted mode** only if you
  control *all* code in the namespace (it exposes sensitive `cf` fields like `cacheKey`).
- **Outbound Worker disables TCP `connect()`** in user Workers, and does **not** intercept fetches from
  Durable Objects or mTLS bindings — plan egress control around that.
- **Gradual deployments not supported** for user Workers — changes go 100% at once; stage via dispatch logic.
- **Static-asset uploads**: hash = first 16 bytes of SHA-256 (32 hex), Base64 binary, upload+deploy within
  1h token windows.
- **Custom hostnames**: don't create one matching your zone name; A-record-at-apex needs Apex Proxying;
  customers already on Cloudflare lose control of Argo, Early Hints, Page Shield, Spectrum, Wildcard DNS for
  the managed hostname.
- **API rate limit** 1200 req / 5 min per account (cumulative across dashboard/key/token) — exponential backoff.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live pages before quoting:
> `developers.cloudflare.com/cloudflare-for-platforms/workers-for-platforms/reference/pricing/` and
> `.../cloudflare-for-saas/plans/`.

**Workers for Platforms** (paid plan, separate from Workers Paid; verified 2026-08-25 against the live docs):
- **$25/month** base. Included: **20M requests**, **60M CPU-ms**, **1000 scripts**.
- Overage: **$0.30 / additional 1M requests** · **$0.02 / additional 1M CPU-ms** · **$0.02 / additional script**.
- Billed **once per dispatch→user→outbound chain** (1 request, CPU summed). Max 30s CPU/invocation.
- Scripts per namespace: **unlimited**; namespaces, DO namespaces: unlimited; **8 tags/script** max.

**Cloudflare for SaaS** (custom hostnames; bundled on non-Enterprise, add-on on Enterprise):
- **Cost driver = active custom hostnames.** Free/Pro/Business: **100 included**, then **$0.10 / hostname**,
  up to **50,000** max. Enterprise: custom pricing, unlimited (contact sales >50k).
- Enterprise-only: custom certs, CSR, selectable CA, wildcard hostnames, mTLS, custom metadata, Apex
  Proxying/BYOIP (paid add-ons).
- Eligible Enterprise can **preview as a non-contract service** (no metered fees/limits).

## Going deeper
- The official `cloudflare` skill has **`references/workers-for-platforms/`** — narrower than this umbrella
  (it covers the W4P pillar only). Prefer it for the **full dispatch/user-Worker upload API, multi-tenant
  routing patterns, and detailed gotchas**: `configuration.md`, `api.md`, `patterns.md`, `gotchas.md`.
- This file additionally covers the **Cloudflare for SaaS** pillar (custom hostnames) the official ref omits.
- Templates: **Platform Starter Kit** (`worker-publisher-template`) and **VibeSDK** (`github.com/cloudflare/vibesdk`).
- Related products: `workers` (compute), `kv`/`d1`/`r2` (per-tenant bindings), `cloudflare-one` (Access for
  custom hostnames). Reference architectures: "Programmable Platforms" and "AI Vibe Coding Platform".
