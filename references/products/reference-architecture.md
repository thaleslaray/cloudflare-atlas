# Reference Architecture — Cloudflare's own architecture blueprints

> Cloudflare's official, vendor-authored architecture guides + diagrams. **Not a product you build
> with** — a RESOURCE for the architect workflow. Consult these proven blueprints when designing a
> solution (SASE, CDN, security, AI apps, networking, serverless) before inventing your own.

## Contents
- When to use (and when not)
- How the content is organized (4 doc types)
- Topic index: Reference Architectures
- Topic index: Design Guides
- Topic index: Diagrams (by solution area)
- Find by solution
- Going deeper

## When to use
- You're **designing an architecture** and want a proven, Cloudflare-blessed pattern to start from
  or validate against — instead of guessing how the products fit together.
- You need to explain **integration points** between Cloudflare and a customer's existing infra
  (data center, cloud, identity provider, EDR/SASE vendor).
- You want a diagram or thought-leadership narrative for a specific use case (e.g. "secure data in
  transit", "serverless ETL", "protect hybrid cloud networks").
- **Not** for: product config, bindings, API commands, or pricing — these are *conceptual* docs.
  For "how do I wire it up", go to the product reference / official skill instead. There are **no
  bindings, no `wrangler.jsonc`, no pricing** here.

## How the content is organized (4 doc types — increasing specificity)
1. **Reference Architectures** — high-level, conceptual. Map Cloudflare's network/products to a
   typical customer environment. Thought leadership for a broad technology area.
2. **Reference Architecture Diagrams** — one or more diagrams for a *specific* solution/use case,
   with short intro + summary. Quick answer to a focused question.
3. **Design Guides** — prescriptive best practices + guidelines for designing a deployment (a
   subset of a full architecture). Aimed at architects/IT pros. Not product config.
4. **Implementation Guides** — step-by-step deploy instructions (these mostly live under
   `learning-paths/`, e.g. "Replace your VPN", "Secure your Internet traffic").

## Topic index — Reference Architectures (`/architectures/`)
- **sase** — Evolving to a SASE architecture with Cloudflare (the flagship Zero Trust / SSE / SASE doc)
- **cloudflare-sase-with-microsoft** — Cloudflare SASE integrated with Microsoft (Entra, etc.)
- **cloudflare-sase-with-crowdstrike** — unified SASE + CrowdStrike EDR, risk-based protection
- **cloudflare-sase-with-sentinelone** — security posture with SentinelOne + Cloudflare One
- **security** — Cloudflare Security Architecture (broad security platform overview)
- **multi-vendor** — Multi-vendor Application Security & Performance (Cloudflare alongside other CDNs/clouds)
- **cdn** — Content Delivery Network reference architecture
- **load-balancing** — Load Balancing reference architecture
- **magic-transit** — Protect network infrastructure with Magic Transit (DDoS, on-ramp)
- **ai-security-for-apps** — AI Security for Apps (securing AI-powered applications)
- **email-security-deployments** — Understanding Email Security deployment models

## Topic index — Design Guides (`/design-guides/`)
- **designing-ztna-access-policies** — designing ZTNA access policies for Cloudflare Access
- **zero-trust-for-startups** — building Zero Trust into your startup
- **zero-trust-for-saas** — zero trust framework to secure SaaS apps
- **network-vpn-migration** — network-focused migration from VPN concentrators to ZTNA
- **secure-application-delivery** — securely deliver applications with Cloudflare
- **streamlined-waf-deployment-across-zones-and-applications** — WAF at scale across zones
- **securing-guest-wireless-networks** — securing guest wifi
- **leveraging-cloudflare-for-your-saas-applications** — Cloudflare for your SaaS apps
- **extending-cloudflares-benefits-to-saas-providers-end-customers** — SaaS providers extending to end-customers

## Topic index — Diagrams (`/diagrams/`, by solution area)
- **ai** (9) — AI app patterns (RAG, composable AI, multi-vendor AI gateway/observability, asset creation, video captioning, BigQuery→Workers AI, enterprise AI agent workspace, AI vibe coding platform + enterprise variant)
- **sase** (8) — clientless access, DNS filtering, One Appliance, serverless authz, VoIP
- **network** (6) — protect public/hybrid networks, BYOIP, Magic Transit, SP/ISP DDoS
- **serverless** (6) — fullstack apps, A/B testing, serverless ETL, global APIs, image management
- **storage** (5) — UGC storage, multi-cloud egress-free, event notifications, on-demand object migration, Durable Objects control/data plane pattern
- **security** (4) — securing data at rest / in transit / in use, FIPS 140 level 3 compliance
- **content-delivery** (2 — distributed web performance architecture, image resizing + R2) · **bots** (1) · **iot** (1)

## Find by solution
The docs also cross-index everything by solution area (`/by-solution/`): **Connectivity Cloud**,
**Zero Trust / SASE**, **Networking**, **Application Performance**, **Application Security**,
**Developer Platform**, **AI**. Use this when you know the *problem space* but not the doc type.

## Going deeper
- Rendered topic pages live under `docs-oficiais/pages/reference-architecture/<type>/<slug>/`; full
  dump at `docs-oficiais/full/reference-architecture.md`.
- Live index: `developers.cloudflare.com/reference-architecture/` · machine index:
  `developers.cloudflare.com/reference-architecture/llms.txt`.
- Read `how-to-use/` first to pick the right doc type for your task.
- These are **conceptual blueprints** — once a pattern is chosen, drop to the specific product
  references (r2, workers, access, magic-transit, etc.) for bindings, config, and pricing.
