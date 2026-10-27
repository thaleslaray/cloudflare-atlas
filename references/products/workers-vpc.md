# Workers VPC — connect Workers to private clouds (cross-cloud apps)

> Reach private APIs, services, and databases in AWS / Azure / GCP / on-prem VPCs from a Worker
> **without exposing them to the public Internet**. Traffic rides a Cloudflare Tunnel (or Mesh/WAN);
> the Worker holds a binding, not a public hostname.

> ⚠️ **Beta** — free during open beta for all Workers plans. APIs may change before GA.

## Contents
- When to use (and when not)
- The two binding flavors (Services vs Networks)
- Binding & config
- Access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- A Worker (API, full-stack app, internal dashboard, MCP server, agent) must call **private** backends
  — auth services, CMS, internal microservices, databases — that have **no public endpoint**.
- API gateway / fan-out: one Worker routes to many internal microservices by URL path.
- **Non-HTTP private services** (Redis, MQTT, custom TCP protocols): open raw TCP with `connect()`
  over a **VPC Network** binding — no longer limited to HTTP `fetch()`.
- **Apply Zero Trust controls to Worker egress**: route a Worker's public-Internet traffic through
  Cloudflare Gateway so DNS/HTTP/Network policies + logs apply to compute (via Mesh, see below).
- **Not** for: exposing on-prem to the Internet *inbound* (→ Cloudflare Tunnel / Access directly).
  Public HTTP egress with no policy needs → plain `fetch()`. Pooled SQL → pair with **Hyperdrive**.

## The two binding flavors
| | **VPC Services** | **VPC Networks** |
|---|---|---|
| Scope | one specific host + port (pre-registered) | a whole Tunnel, or all of Mesh/WAN (`cf1:network`) |
| Config key | `service_id` | `tunnel_id` **or** `network_id: "cf1:network"` |
| Routing | fixed by service config (URL host/port in `fetch` is **ignored**) | URL/address you pass at runtime picks the destination |
| Protocols | HTTP `fetch()`; TCP **only via Hyperdrive** | HTTP `fetch()` **and** raw TCP `connect()` (Redis, MQTT, custom) |
| SSRF | service-scoped — can't reach the rest of the network | broad — you must allowlist destinations yourself |
- Use **Services** for a known, cataloged set of targets; **Networks** for dynamic/network-wide access.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "vpc_services": [
    { "binding": "PRIVATE_API", "service_id": "<UUID>", "remote": true }
  ],
  "vpc_networks": [
    { "binding": "MY_VPC", "network_id": "cf1:network", "remote": true }
    // or bind one tunnel:  { "binding": "MY_VPC", "tunnel_id": "<UUID>", "remote": true }
  ]
}
```
Create a service: `npx wrangler vpc service create <name> --type http --tunnel-id <id> --hostname <host>`
(TCP DB: `--type tcp --tcp-port 5432 --app-protocol postgresql --tunnel-id <id> --ipv4 <ip>`).

## Access patterns
- **`env.BINDING.fetch(url)`** — absolute URL required (`http://internal-api/path`); relative paths fail.
  Returns a standard `Response`. Connection failure **throws**, not a non-2xx response.
- **`env.MY_VPC.connect("host:port")`** — VPC **Networks** only; raw TCP, **plaintext only** for now.
- **Private database** = TCP VPC Service + **Hyperdrive** (pooling/caching) — see Hyperdrive's
  "connect to a private database using Workers VPC" guide. Hyperdrive locates the TCP service via `app_protocol`.
- **Local dev** needs remote bindings: set `"remote": true` or run `wrangler dev --remote` (no local VPC).
- TLS to origin: trusts public CAs + Cloudflare Origin CA only; tune with `--cert-verification-mode`
  (`verify_full` default · `verify_ca` · `disabled`).

## Gotchas
- **First you need a Tunnel.** Workers VPC rides on a Cloudflare Tunnel (`cloudflared`) / Mesh / WAN
  on-ramp that can actually reach the target — fix Security Groups / ACLs / firewall rules on that side.
- **Service `fetch` host/port are cosmetic** — config decides routing; the `fetch` host only sets the
  `Host` header / SNI, and the `fetch` port is ignored entirely.
- **Roles gate everything:** `Connectivity Directory Bind` to bind existing services; `…Admin` to
  create/update services and to bind a Tunnel directly via a VPC Network. Token must carry the role.
- **Networks are broad → SSRF risk:** validate user-controlled destinations against an allowlist.
- `connect()` over VPC Networks is **plaintext TCP only** today (no TLS).
- For databases, prefer Hyperdrive over raw `connect()` — pooling avoids per-request connection overhead.

## Pricing & limits
> ⚠️ Pricing is volatile — verify on the live page (`developers.cloudflare.com/workers-vpc/platform/pricing/`)
> before quoting.

- **Free during open beta** for all Workers plans. Requires a Workers plan; **standard Workers pricing**
  (compute time + requests) still applies to the Worker itself.
- **Limits:** **1,000 VPC Services / account**. Standard Workers limits apply for request size, timeout,
  and subrequests. (Verify on `…/workers-vpc/platform/limits/`.)

## Going deeper
- Official `cloudflare` skill `references/workers-vpc/` — full TCP Sockets (`cloudflare:sockets`) API,
  patterns, and troubleshooting. Note: that ref leans on the **raw `connect()`/TCP Sockets** angle; the
  newer declarative **VPC Services / VPC Networks** bindings are documented here and in the rendered docs.
- Examples: private API, private database (+Hyperdrive), private S3 bucket, route-across-services,
  connect-to-Mesh → `docs-oficiais/pages/workers-vpc/examples/`.
- Related: **Cloudflare Tunnel** (the data path), **Hyperdrive** (private SQL), **Cloudflare Gateway**
  (Zero Trust egress via Mesh), **TCP Sockets** runtime API.
