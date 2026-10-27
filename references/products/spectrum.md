# Spectrum — proxy & protect any TCP/UDP app (not just HTTP)

> A global Layer 4 reverse proxy on Cloudflare's edge. Routes **raw TCP/UDP** (SSH, gaming,
> databases, MQTT, SMTP, RDP, custom protocols) through Cloudflare to mask the origin, absorb
> L3/4 DDoS, and accelerate with Argo. The answer when your protocol **isn't HTTP**.

## Contents
- When to use (and when not)
- Protocols & plans
- Config (API — no Worker binding)
- Key concepts
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You need to proxy/protect a **non-HTTP TCP or UDP** service: SSH, RDP, Minecraft/game servers,
  MQTT/IoT brokers, SMTP relays, Postgres/MySQL/Redis, version control, custom binary protocols.
- You want origin IP masking + L3/4 DDoS absorption + (optional) Argo Smart Routing at Layer 4.
- **Not** for HTTP/HTTPS apps — use the normal Cloudflare proxy (orange-cloud) / WAF / CDN instead;
  those give you caching, Workers, Bot Management. Spectrum's HTTP/HTTPS mode only exists to feed
  that L7 pipeline (e.g. to reach a **Tunnel**, which Spectrum can only do in HTTP/HTTPS mode).
- vs **Tunnel/Workers**: those are HTTP-centric. Spectrum is the L4 path for everything else.

## Protocols & plans
| Plan | Spectrum | SSH | RDP | Minecraft | Arbitrary TCP/UDP |
|------|----------|-----|-----|-----------|-------------------|
| Free | No | — | — | — | — |
| Pro | paid add-on | 1 app | — | 1 app | No |
| Business | paid add-on | 1 app | 1 app | 1 app | No |
| Enterprise | included | yes | yes | yes | **all ports, add-on** |

Pro/Business get *named* protocols on fixed ports only. **Arbitrary TCP/UDP and port ranges are
Enterprise-only.** Minecraft = Java Edition only (Bedrock unsupported).

## Config (API — no Worker binding)
Spectrum has **no `wrangler.jsonc` binding** — it's a zone-level proxy configured via dashboard or
`POST /zones/{zone_id}/spectrum/apps`. A Spectrum "app" maps an edge port to an origin:
```jsonc
{
  "protocol": "tcp/22",                       // "udp/..." too; ranges "tcp/1000-2000" (Enterprise)
  "dns": { "type": "CNAME", "name": "ssh.example.com" },
  "origin_direct": ["tcp://192.0.2.1:22"],    // OR origin_dns + origin_port (hostname origin)
  "proxy_protocol": "off",                     // "v1" (TCP) | "v2" (TCP+UDP) | "simple" (UDP) — Enterprise
  "tls": "off",                                // off | flexible | full | full-strict (TCP only)
  "ip_firewall": true,                         // honor IP Access Rules
  "edge_ips": { "type": "dynamic", "connectivity": "all" },
  "argo_smart_routing": true                   // TCP + UDP (beta)
}
```
Origin types: **direct IP** (`origin_direct`), **CNAME/hostname** (`origin_dns`+`origin_port`, zone
must be Cloudflare-authoritative), or **Load Balancer** (HA/failover). Port-range apps map by offset
(edge `:1005` → origin `:3005`). Enterprise can use **BYOIP** or a **Static IP**.

## Key concepts
- **L4 termination, payload passthrough:** Spectrum terminates the TCP/UDP socket at the edge but
  passes L4 payloads as-is — it does not parse the application layer.
- **Edge IPs are anycast & not static:** look them up via the app's DNS name, never hardcode.
- **Proxy Protocol** is how the origin learns the real client IP (otherwise it sees a Cloudflare IP).
  Enterprise-only feature. v1 = TCP plain-text header; v2 = binary header for TCP **and** UDP
  (prepended to the first datagram of a stream); Simple Proxy Protocol = UDP-only, and the origin
  must prepend the same header on packets back to the client.
- **Edge TLS termination** (TCP only): flexible/full/full-strict, like the L7 SSL modes.
- **Virtual network origin:** route `origin_direct` to a *private* origin over a Tunnel/Cloudflare WAN
  via `virtual_network_id` (TCP/UDP, single IP+port, no Proxy Protocol).

## Gotchas
- **Tunnel only works in HTTP/HTTPS mode** — pointing a TCP app at `<UUID>.cfargotunnel.com` fails.
  For private L4 origins use `virtual_network_id`, or a Load Balancer with Private Network LB
  (in that on-ramp the `proxy_protocol` setting is **not supported**, whatever the off-ramp).
- **Client IP = Cloudflare IP** unless Proxy Protocol is enabled *and* the origin parses it
  (nginx `listen … proxy_protocol;`, HAProxy `bind … accept-proxy`).
- **SMTP:** Spectrum IPs have **no reverse DNS (PTR)** → many mail servers reject. Inbound mail →
  Email Routing; avoid outbound SMTP through Spectrum.
- **UDP:** no packet fragmentation (fragmented packets dropped); BYOIP-supported but not via Magic
  Transit service bindings.
- **WAF custom rules don't apply** — only **IP Access Rules** (allow/block by IP/CIDR/ASN/country).
- **Universal SSL incompatible** — use an Advanced or Custom certificate. HTTPS apps: no HTTP/3.
- **Listens on all ports** but only proxies ports with a configured app; others complete the TCP
  handshake then immediately close (no origin connection).

## Pricing & limits
> ⚠️ **Spectrum has no public per-unit price list** — it's a **paid add-on** on Pro/Business and an
> Enterprise contract item (priced via your account team). **Verify with Cloudflare sales / your
> account team before quoting** — do not invent a number.

**Cost drivers** (contract-based): plan tier + whether you need arbitrary TCP/UDP (Enterprise) vs the
named per-app protocols (SSH/RDP/Minecraft on Pro/Business). Add-ons that affect cost: BYOIP, Argo
Smart Routing, Load Balancing. **Limits:** Pro/Business = one app each for SSH/RDP/Minecraft, fixed
ports; Enterprise = all TCP/UDP ports (1–65535) + port ranges. TLS modes are TCP-only. Verify on
`developers.cloudflare.com/spectrum/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/spectrum/`) — use it for full API,
  SDK (TS/Python/Go), Terraform/Pulumi config, per-protocol patterns, and gotchas:
  `patterns.md` (SSH, gaming, MQTT, SMTP, DB, RDP) · `configuration.md` · `api.md` · `gotchas.md`.
- Exact REST API: `api.cloudflare.com` → `/zones/{zone_id}/spectrum/apps`.
- Proxy Protocol setup: `developers.cloudflare.com/spectrum/how-to/enable-proxy-protocol/`.
