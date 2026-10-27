# Network — zone-level network feature toggles

> Per-zone (per-domain) network settings for proxied traffic: protocol support (WebSockets, gRPC),
> IPv6 handling, visitor-IP/geolocation headers, and Tor/Onion Routing. Mostly on/off toggles on the
> dashboard **Network** page, all editable via one zone-settings API. Available on all plans.

## Contents
- When to use (and when not)
- Configuration (dashboard + API)
- The features
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You run a **proxied** domain on Cloudflare and need to enable/configure a protocol or network
  behavior for it: real-time WebSockets, gRPC APIs, IPv6, passing the visitor's IP/country to origin.
- These are **zone (domain) settings**, not Workers bindings — they affect orange-clouded (proxied)
  DNS records. Grey-clouded (DNS-only) records bypass them entirely.
- **Not** for: building network connectivity between your infra and Cloudflare (→ Magic WAN /
  network-interconnect / cloudflare-one), nor for Workers networking.

## Configuration (dashboard + API)
All toggles live on **dash → your domain → Network**. Every setting is also editable through the
**zone settings edit** endpoint — one API, different `setting name` per feature:

```
PATCH /client/v4/zones/{zone_id}/settings/{setting_name}
{ "value": "on" }   // or "off", or a feature-specific value
```
Setting names: `websockets`, `ip_geolocation`, `ipv6`, `pseudo_ipv4`, `opportunistic_onion`,
`true_client_ip_header`. (gRPC has its own dashboard toggle.) These are zone-level config, **not**
declared in `wrangler.jsonc` — there is no Worker binding for network settings.

## The features
- **WebSockets** — proxy long-lived bidirectional connections to origin. Supported on **all plans**
  without additional configuration. Pairs with Workers / Durable Objects as WebSocket endpoints.
- **gRPC** — protect gRPC APIs on proxied endpoints. When **off**, Cloudflare returns `403` to gRPC
  requests. Requires: origin on **port 443**, TLS + **HTTP/2 advertised over ALPN**, SSL mode ≥ Full,
  `Content-Type: application/grpc[+proto]`.
- **IPv6 Compatibility** — auto-generates `AAAA` records so IPv6 clients can reach proxied hostnames.
  On by default. Only **Enterprise** can turn it off; non-Enterprise instead use Pseudo IPv4.
- **Pseudo IPv4** — for IPv4-only origins that can't parse IPv6. `add_header` (adds `Cf-Pseudo-IPv4`)
  or `overwrite_header` (rewrites `Cf-Connecting-IP`/`X-Forwarded-For`, keeps real IP in
  `CF-Connecting-IPv6`). Uses Class E addresses (e.g. `240.16.0.1`).
- **IP Geolocation** — adds `CF-IPCountry` (country only) to origin requests. For richer fields
  (city, lat/long, continent) prefer the **Add visitor location headers** Managed Transform instead.
- **True-Client-IP Header** — adds end-user IP via `True-Client-IP` header. **Enterprise only**;
  recommended path is the equivalent Managed Transform.
- **Onion Routing** — serve content to Tor users directly via `.onion` (alt-svc header), skipping
  exit nodes. Lets challenges target only malicious bots. Visible domain/SNI stay unchanged; Cloudflare
  issues **no certificate** for the `.onion` name, so it cannot be reached over HTTPS.

## Gotchas
- **gRPC default-off = 403:** if gRPC requests get `403 Forbidden`, the zone toggle is off.
- **gRPC product gaps:** WAF Managed Rules only inspect connection-phase headers (not stream content);
  **Access ignores gRPC** traffic — disable gRPC on Access-protected origins; Tunnel supports gRPC
  only via private-net routing, not public hostnames.
- **IPv6 still leaks when "off":** Tor (Onion Routing) and Workers subrequests use IPv6. To fully
  block, also disable Onion Routing + add a WAF rule for `ip.src in {::/0}` (exclude Workers with
  `cf.worker.upstream_zone == ""`).
- **IPv4 preferred to origin:** for dual-stack origins behind a proxied record, Cloudflare connects
  over IPv4.
- **Partial setup / hosting-partner apex:** IPv6 compatibility does not apply to the apex domain.
- **WebSockets billing (Enterprise):** one connection = one HTTP request (the upgrade); bandwidth is
  CF→client data. Restarts during network code releases drop connections — use a client keepalive.
- **WebSockets + Argo:** not compatible. Behind a Load Balancer, enable **Session affinity** so
  reconnects land on the same origin.

## Pricing & limits
> ⚠️ Verify on the live pricing page before quoting — pricing/availability changes.

- **Network settings themselves are free** and available on **all plans** (Free → Enterprise), except
  **True-Client-IP** and **disabling IPv6 Compatibility**, which are **Enterprise-only**.
- gRPC may incur charges when traffic runs through paid add-ons (**Argo Smart Routing**, **WAF**,
  **Bot Management**) — those products are billed normally.
- **WebSockets idle timeout:** Cloudflare closes connections after a period with no data; Enterprise
  can request a custom idle timeout. Keep alive with client-side ping/pong.

## Going deeper
- No dedicated `cloudflare` skill reference exists for `network` (don't confuse with
  `network-interconnect`, a separate Magic/CNI product).
- Per-feature docs: `developers.cloudflare.com/network/` (gRPC, ip-geolocation, ipv6-compatibility,
  pseudo-ipv4, onion-routing, true-client-ip-header, websockets).
- Zone-settings API: `developers.cloudflare.com/api/` → zones → settings → edit.
- Richer visitor headers → **Managed Transforms** (`rules/transform/managed-transforms/`).
