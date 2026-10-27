# Learning Paths — guided onboarding tutorials

> Guided, module-based **onboarding paths** for getting started with Cloudflare products — step-by-step
> tutorials (Workers, Zero Trust onboarding, account/email security, etc.). A **learning resource**, not a
> product to build on. Use this as a pointer/index; the real content lives in the docs.

## Contents
- When to use (and when not)
- Main paths available
- Going deeper

## When to use
- You want a **structured, start-to-finish walkthrough** of onboarding a product or workflow, rather than
  reference docs you have to stitch together yourself.
- Good for first-time setup: standing up Workers, replacing a VPN with Zero Trust, securing internet
  traffic / email, hardening DNS, course-style intros to Durable Objects / Workflows / R2.
- **Not** a binding, API, or product you deploy — there's no `wrangler` config and nothing to provision.
  Once you know *what* to build, jump to the individual product reference (e.g. `products/workers.md`).

## Main paths available
From `pages/learning-paths/` (developers.cloudflare.com/resources/ — the old
`/learning-paths/` URL now 301s there):

**Developer platform**
- **workers** — get started building on Workers (concepts → dev platform → first deploy).
- **durable-objects-course** — course series intro to Durable Objects.
- **workflows-course** — course series intro to Workflows.
- **r2-intro** — course series intro to R2 object storage.

**Zero Trust / SASE onboarding**
- **replace-vpn** — replace a legacy VPN with Cloudflare Access (connect devices + private network, build policies).
- **secure-internet-traffic** — Gateway setup: DNS / HTTP / network / egress policies, secure SaaS apps.
- **clientless-access** — reach private apps without the device agent.
- **sase-overview-course** · **warp-overview-course** — conceptual course intros to SASE and WARP.
- **cybersafe** · **holistic-ai-security** — security-awareness / AI-security onboarding.

**Account & email security**
- **secure-your-email** — onboard Email Security.
- **mtls** — set up mutual TLS.

**Network & application security / reliability**
- **application-security** · **prevent-ddos-attacks** · **data-center-protection** — WAF / DDoS / origin protection.
- **dns-best-practices** — DNS hardening.
- **load-balancing** · **surge-readiness** — traffic distribution and traffic-spike prep.
- **china-network-overview** — overview of serving traffic in China.

## Going deeper
- Browse live: `developers.cloudflare.com/resources/` (the hub; `/learning-paths/` redirects here).
- Rendered source: `raw/docs-oficiais/pages/learning-paths/<path>/` (each has an `index.md` + step pages;
  course-style paths use a `series/` subfolder).
- For *what to build* after onboarding, see the matching product file in this directory
  (`workers.md`, `r2.md`, `durable-objects.md`, Zero Trust products, etc.).
