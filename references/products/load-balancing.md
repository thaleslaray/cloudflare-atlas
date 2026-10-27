# Load Balancing — distribute traffic across origins/pools with health checks & failover

> Spread traffic across multiple origin servers (pools) for availability and performance. Active
> health monitors take unhealthy origins out of rotation; steering policies pick *which* pool/origin
> gets each request (failover, geo, latency, proximity). **Paid add-on** — not part of the free plan.

## Contents
- When to use (and when not)
- Core model: load balancers → pools → endpoints → monitors
- Proxy modes (L7 / DNS-only / L4)
- Steering policies (global + local)
- Session affinity
- Config (API / Terraform — no Workers binding)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You have **multiple origins** (data centers, cloud regions, on-prem) and want automatic **failover**
  when one goes unhealthy.
- **Geo-steering / proximity / latency routing** — send users to the closest or fastest origin.
- Active-active (load spread) or active-passive (hot standby) origin topologies.
- **Not** for app-level / path-based routing logic *inside* one origin — that's a **Worker** (route by
  URL, A/B, header rewriting). LB picks an origin; Workers run code. They compose: a Worker can sit in
  front, LB behind it.
- **Not** a replacement for DNS failover alone, the WAF, or Argo Smart Routing (intra-network path
  optimization). **Not** for balancing across Workers — Workers already run on every PoP.

## Core model: load balancers → pools → endpoints → monitors
- **Load balancer** — bound to a hostname (e.g. `app.example.com`). Creating a public LB auto-creates
  an **LB DNS record**. Holds the global steering policy + ordered list of pools + fallback pool.
- **Pool** — a group of one or more **endpoints**, usually = one region/data center. Has its own
  *local* steering policy, a **Health Threshold** (min healthy endpoints before the pool goes
  Critical), and an attached monitor.
- **Endpoint** — an origin: IP, hostname, VIP, server. Has a **weight** (default 1) controlling its
  share of pool traffic: `share = weight ÷ sum(weights in pool)`. Weight `0` = no traffic but still
  health-probed.
- **Monitor** — issues health-check requests at an interval; flips endpoints/pools healthy↔unhealthy.

## Proxy modes
- **Layer 7 (proxied / orange-cloud)** — most common. Routes per HTTP request; hides origin IPs (DDoS
  protection), fast & accurate failover, integrates with cache/Workers/WAF, supports session affinity.
- **DNS-only (grey-cloud)** — returns origin IPs in DNS answers. Needed for MX/SRV hostnames. Slower &
  less accurate failover (record TTL is **30s**, but resolvers may cache past it); no session affinity (use DNS
  persistence), no WAF/cache, exposes origin IPs. Supports EDNS Client Subnet for geo/proximity.
- **Layer 4 (TCP)** — only via **Cloudflare Spectrum**; no affinity/rules/cache at this layer.

## Steering policies
**Global (load balancer → pool):**
- **Off – Failover** *(non-Ent)* — pool order = failover priority; spill to next healthy pool, then
  fallback pool. Classic active-passive.
- **Random** *(non-Ent)* — pick a healthy pool at random; weightable → active-active / round-robin.
- **Geo** *(Ent / add-on)* — map countries/regions (Ent: data centers) to pools. ⚠️ incompatible with
  custom LB rules.
- **Dynamic** *(Ent / add-on)* — route to fastest pool by RTT (EWMA from health probes); allow ~10 min
  to build an RTT profile.
- **Proximity** *(Ent / add-on)* — route to physically closest pool; requires GPS coords per pool.
- **Least Outstanding Requests (LOR)** *(Ent / add-on)* — favor pools with fewest in-flight requests.

**Local (pool → endpoint):** **Random** (weighted), **Hash** *(Ent — sticky by client IP)*, **LOR**
*(Ent)*. Session affinity & Hash override plain weight distribution.

## Session affinity (L7 / public LB only)
Pin a client to one endpoint so session state survives. Three L7 types: **Cloudflare cookie**
(`__cflb`, default TTL **23h** = 82,800s, range 1800s–604800s, `HttpOnly`, `Secure` when
Always-Use-HTTPS), **cookie + client-IP fallback** (`ip_cookie`), **header** (default TTL 1800s, range
30s–3600s). Affinity takes precedence over weights/steering. DNS-only LBs use **DNS persistence**
instead. **Endpoint drain** lets you stop new sessions to an origin while existing ones finish.

## Config (API / Terraform — no Workers binding)
Load Balancing is **not** a Worker binding — there is no `wrangler.jsonc` entry. Manage via dashboard,
the **Cloudflare API**, or **Terraform**. Account-level resources:
- Monitors: `POST accounts/:id/load_balancers/monitors` (type `HTTP|HTTPS|TCP` on any plan;
  `ICMP-ping|UDP-ICMP|SMTP` are **Enterprise-only**,
  `interval`, `timeout`, `retries`, `expected_codes`, `consecutive_up`/`consecutive_down`).
- Pools: `POST accounts/:id/load_balancers/pools` (origins, weights, monitor, `notification_email`).
- Load balancers: `POST zones/:id/load_balancers` (pools, `steering_policy`, `fallback_pool`,
  `session_affinity`, `random_steering`, `location_strategy`, `rules`).
Health checks come **from Cloudflare's edge to your origin**, so origins must allow Cloudflare probe IPs.

## Gotchas
- **Paid add-on** — account needs a billing profile; only **Off-Failover** & **Random** are available
  without buying *Traffic steering* (or an Enterprise plan).
- **Monitor probes multiply by region:** each selected Health Monitor Region probes from **3 data
  centers**; "All Regions" = 39 probes, "All Data Centers" (Ent) = every PoP. Low intervals + many
  regions can flood your origin. Tune `interval` and region count.
- **DNS caching breaks DNS-only failover** — resolvers may serve stale IPs past the TTL. Prefer L7
  (proxied) for fast, accurate failover.
- **Geo steering ⊕ custom rules don't mix** — rules silently misbehave on geo-steered LBs.
- **Health Threshold:** a pool goes *Critical* (no traffic) once healthy endpoints drop below its
  threshold — unless it's the fallback pool and all pools are down.
- Use `consecutive_up`/`consecutive_down` to avoid flapping on transient blips.
- Endpoint in multiple pools with different weights → actual share differs from any single pool's %.
- Health monitors ≠ **standalone Health Checks** (separate product).

## Pricing & limits
> ⚠️ Pricing is volatile — verify in-dashboard (`dash.cloudflare.com → Traffic → Load Balancing`) and
> `cloudflare.com/plans` before quoting. There is **no public free tier** — it's a metered add-on.

**Cost drivers (self-service add-on):** a monthly base fee plus usage — billed per **DNS query / LB
request** routed and per **active health-check monitor**; steering policies beyond Standard
(Geo/Dynamic/Proximity/LOR/Hash) are extra (or Enterprise). Enterprise can **preview** the product as a
non-contract service (full access, no metered fees/limits).

**Limits:** non-Enterprise — **20** load balancers, **20** pools, **20** endpoints; monitor interval
**15s min** (Ent 10s) / 3600s max; monitors ≈ 1.5× pool count. Enterprise = custom. Verify at
`developers.cloudflare.com/load-balancing/reference/limitations/`.

## Going deeper
- No dedicated official `cloudflare` skill ref exists for Load Balancing — this file is the primary
  reference. For exact request/response shapes use `references/api/load-balancing.md` (endpoints sliced
  from the OpenAPI spec — verify shapes live) or `developers.cloudflare.com/api/` under `load_balancers`.
- Concepts: `developers.cloudflare.com/load-balancing/` — components, traffic-steering, health-details,
  session-affinity, proxy-modes; common topologies under `load-balancers/common-configurations/`.
- Reference architecture: `developers.cloudflare.com/reference-architecture/architectures/load-balancing/`.
