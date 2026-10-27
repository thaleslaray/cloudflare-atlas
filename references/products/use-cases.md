# Use cases — scenario → Cloudflare product map (architect resource)

> Cloudflare's own "how to do X on Cloudflare," organized by scenario rather than by product.
> **This is a RESOURCE for the architect workflow, not a product.** Use it to go from a real-world
> goal ("build a RAG app", "stop credential stuffing", "replace our VPN") to the recommended
> Cloudflare products + a starting architecture pattern. Consult it when architecting; then dive into
> each product's own reference for bindings/config/limits.

## Contents
- How to use this (architect workflow)
- Build something new (web-apps · ai · saas · apis)
- Secure & accelerate existing apps (application-security · performance · company-security · media-streaming · e-commerce)
- Cross-product solution guides
- Going deeper

## How to use this (architect workflow)
1. Match the user's intent to a **category** below (build-new vs secure/accelerate-existing).
2. Pick the **scenario** (sub-page) and read its **recommended products**.
3. Use the **architecture pattern** as a skeleton, then open each product's reference here in
   `references/products/<product>.md` for the actual bindings, API, gotchas, and limits.
4. Note the **prereq tells you the deployment model**: account-only (Workers/R2/Stream/AI, account-level)
   vs *domain-proxied-through-Cloudflare* (WAF, cache, Load Balancing, SSL/TLS) vs *Cloudflare One org*
   (Access, Gateway, DLP, CASB, Browser Isolation). This determines whether the user even can use a feature.

## Build something new
Deploy apps/APIs/platforms on Cloudflare from the ground up (account-level; needs Wrangler + Node).

- **`web-apps/`** — Web sites & full-stack apps. Scenarios: deploy-frontend · serverless-backends ·
  store-data · real-time · performance · security.
  Products: **Workers** (frontend+API), **D1** (SQL), **KV** (global k/v), **R2** (objects), **Durable
  Objects** (real-time state/WebSockets), **Queues** (background jobs).
  Patterns: full-stack (Workers+D1+R2) · real-time collab (Durable Objects+Workers+KV+Queues) · static+dynamic.
- **`ai/`** — AI applications. Scenarios: build-and-run · store-and-retrieve-context · control-costs.
  Products: **Workers AI** (edge inference), **AI Gateway** (multi-provider proxy/cache/analytics),
  **Vectorize** (embeddings/RAG), **Workers**, **KV** (response cache), **D1** (session/history).
  Patterns: RAG (Vectorize+Workers+Workers AI) · multi-provider gateway · real-time edge AI.
- **`saas/`** — Multi-tenant SaaS platforms. Scenarios: custom-domains · code-deployment · data-isolation ·
  protect-platform · usage-analytics.
  Products: **Cloudflare for SaaS / SSL for SaaS** (per-customer custom hostnames+certs), **Workers for
  Platforms** + **dispatch namespaces** (isolated tenant code), **D1**/**KV**/**R2** (per-tenant storage),
  **Workers Analytics Engine** + **Logpush** (usage/billing). Note: Workers for Platforms needs a paid plan.
- **`apis/`** — APIs & microservices. Scenarios: deploy-apis · protect-apis · internal-services · monitor-apis.
  Products: **Workers** (edge API handlers), **API Shield** (OpenAPI schema validation, mTLS),
  **Rate Limiting**, **WAF/managed rulesets**, **D1**/**KV** (data), **Queues** (async/webhooks),
  **Cloudflare Tunnel** + **Access** (internal services, no public IPs), **Logpush** + **Analytics Engine**.

## Secure & accelerate existing apps
Add Cloudflare in front of existing infra. Most require the **domain proxied through Cloudflare**;
company-security requires a **Cloudflare One org**.

- **`application-security/`** — Protect an app. Scenarios: block-attacks · ddos · bots · client-side · api-endpoints.
  Products: **WAF / managed rulesets** (SQLi, XSS, OWASP Top 10), **DDoS Protection**, **Bot Management**,
  **API Shield**, **Client-side security** (third-party script monitoring), **Turnstile** (CAPTCHA replacement),
  **SSL/TLS**, **Rate Limiting**, **mTLS**.
- **`performance/`** — Accelerate delivery. Scenarios: caching · image-optimization · connections · web-assets ·
  load-balancing · monitoring.
  Products: **Cache / CDN**, **Images** (+ Polish), **Argo Smart Routing**, **Load Balancing**,
  **speed optimizations**, **Web Analytics** (JS snippet, no proxy needed).
- **`company-security/`** — Company-wide Zero Trust (needs Cloudflare One org). Scenarios: employee-access ·
  internet-access · email-security · data-loss-prevention · device-security.
  Products: **Access** + **Cloudflare Tunnel** (VPN replacement, per-request identity), **Gateway** (SWG: DNS/HTTP
  filtering), **Browser Isolation**, **DLP**, **CASB**, **Email Security** (phishing/BEC/malware), **DMARC management**,
  **Device posture / WARP client**.
- **`media-streaming/`** — Video/images/media at scale. Scenarios: video-delivery · image-optimization ·
  store-media · cache-delivery · secure-content.
  Products: **Stream** (+ Stream Live, adaptive bitrate), **Images** (on-the-fly transforms), **R2** (zero-egress
  storage), **Cache**, **signed URLs / Hotlink Protection**, **Workers** (custom logic).
  Patterns: video platform · on-the-fly image pipeline (R2+Images+Workers) · UGC uploads (R2 presigned+Workers+Stream/Images).
- **`e-commerce/`** — Secure & accelerate storefronts. Scenarios: protect · performance · traffic-at-scale · analytics.
  Products: **WAF/Bot Management** (credential stuffing/fraud), **Cache** + **Images**, **Load Balancing** +
  **Waiting Room** + **Health Checks** (flash sales), **Argo Smart Routing**, **Zaraz** (server-side tags),
  **Cloudflare for SaaS** (orange-to-orange over Shopify/BigCommerce/SFCC), **SSL/TLS**.

## Cross-product solution guides (`solutions/`)
Goal-first walkthroughs that wire several products together (all available on Free/Pro/Business):
- **discover-secure-api-endpoints** — endpoint inventory + WAF/SSL-TLS/bot detection (Free/Pro/Business);
  API Shield discovery, schema validation, JWT validation and sequence analysis are Enterprise callouts.
- **encrypt-all-keep-site-secure** — enforce HTTPS / SSL-TLS hardening.
- **protect-sensitive-forms-fraud-abuse** — Turnstile + Bot Management + WAF on forms.
- **stop-account-takeover-attacks** — bot + credential-stuffing + leaked-credential defenses.
- **stop-malicious-bots** — Bot Management tuned to allow legitimate traffic.
Reach for these when the user states an *outcome* rather than a product.

## Going deeper
- Source pages: `raw/docs-oficiais/pages/use-cases/` (one folder per category, `index.md` lists scenarios
  + architecture patterns); full dump in `raw/docs-oficiais/full/use-cases.md`.
- Each product named above has its own reference in `references/products/` — go there for bindings,
  `wrangler.jsonc`, exact API, gotchas, and current pricing/limits. **This file maps; the product files build.**
- Cloudflare also publishes **Reference architectures**, **Learning paths**, and **Tutorials**
  (`developers.cloudflare.com/reference-architecture/`, `/learning-paths/`, `/tutorials/`) for deeper, diagrammed designs.
- No pricing here by design — pricing is per-product and volatile; quote from each product's reference (and verify live).
