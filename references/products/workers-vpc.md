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
| Config key | `service_id` | `tunnel_id`, `network_id: "cf1:network"` (account default vnet) **or** `cf1:vnet:<VNET_UUID>` (a specific virtual network) |
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
    // or one virtual network:  { "binding": "STAGING", "network_id": "cf1:vnet:<VNET_UUID>", "remote": true }
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
- TLS to origin: trusts public CAs + Cloudflare Origin CA by default; `--cert-verification-mode` (`verify_full` default · `verify_ca` · `disabled`).
- **Custom CA + mTLS client cert (2026-11-18)**: upload, then attach to the service's `tls_settings` (`certificate_authority`, `client_certificate`, `cert_verification_mode`):
  `npx wrangler cert upload certificate-authority --ca-cert ./ca.pem --name private-ca` · `npx wrangler cert upload mtls-certificate --cert ./client.pem --key ./client-key.pem --name private-client` →
  `wrangler vpc service create … --certificate-authority <CA_ID> --client-certificate <CERT_ID> --cert-verification-mode verify_full`. CA, client cert, or both. API upload: `POST /accounts/{id}/mtls_certificates`
  (`ca: true` for CA; `ca: false` + `private_key` for client cert; token needs `Account: SSL and Certificates Write`). Needs Wrangler **4.164.0+**, API, or Terraform provider **5.29.0+**; **no dashboard support yet**.
  Applies to `https` for `http` services and to the TLS connection of `tcp` services (Postgres/RDS CA bundle). Rules: `cert_verification_mode` is **required** with either cert; custom CA can't combine with
  `disabled`; client cert works without a CA. Mismatch fails (`CERTIFICATE_VERIFY_FAILED` in the `fetch()` error) — no fallback. **Updating a service replaces its whole config**: repeat every TLS setting
  you keep or they are cleared (back to default verification). Rotate = upload new cert, update service with new ID (seconds). Removing a reference / deleting the service doesn't delete the cert (`wrangler cert delete`).
  → `workers-vpc/configuration/vpc-services/#custom-ca-and-client-certificates`

## Gotchas
- **First you need a Tunnel.** Workers VPC rides on a Cloudflare Tunnel (`cloudflared`) / Mesh / WAN
  on-ramp that can actually reach the target — fix Security Groups / ACLs / firewall rules on that side.
- **Service `fetch` host/port are cosmetic** — config decides routing; the `fetch` host only sets the
  `Host` header / SNI, and the `fetch` port is ignored entirely.
- **Roles gate everything:** `Connectivity Directory Bind` to bind existing services; `…Admin` to
  create/update services and to bind a Tunnel directly via a VPC Network. Token must carry the role.
- **Networks are broad → SSRF risk:** validate user-controlled destinations against an allowlist.
- **Overlapping private IPs:** one binding per virtual network (`cf1:vnet:<UUID>`), so one Worker can reach
  prod and staging backends that share the same IP (`env.PRODUCTION.fetch("http://10.0.1.50/status")`).
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
