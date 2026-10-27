# Privacy Proxy — MASQUE-based forward proxy (privacy + geolocation)

> A managed forward proxy on Cloudflare's network that hides client IP addresses while **preserving
> geolocation accuracy**. Separates user *identity* from user *activity*. **Enterprise-only**, no
> self-serve — powers Microsoft Edge Secure Network and the second hop of iCloud Private Relay.

## Contents
- When to use (and when not)
- How it works
- Deployment models
- Authentication
- Geolocation
- Connect & client libraries
- Observability
- Gotchas
- Availability & limits
- Going deeper

## When to use
- You're building a **privacy-preserving forward proxy / browser VPN** and want destinations to see
  Cloudflare egress IPs instead of the user's real IP — without breaking location-aware services.
- You need **geolocation preserved** (local search results, regional content, local pricing) — the
  differentiator vs traditional VPNs that exit from distant data centers.
- You want to **split trust** so no single party sees both who the user is and where they go (double-hop).
- **Not** for: hiding the client IP from *your own app backend* on a per-request basis → use
  **Privacy Gateway** (Oblivious HTTP / OHTTP). For a consumer device VPN, see **WARP**. For reverse
  proxying / protecting an origin you own, this is the wrong product (that's the core CDN/WAF).
- **Not** self-serve: there is no Worker binding or dashboard toggle — Cloudflare provisions it for you.

## How it works
Uses the [MASQUE](https://datatracker.ietf.org/wg/masque/about/) suite to proxy traffic over HTTP/2
(TLS/TCP) and HTTP/3 (QUIC). Two methods:

| Method        | Transport | Use case                                  |
| ------------- | --------- | ----------------------------------------- |
| HTTP CONNECT  | TCP       | Traditional HTTPS traffic                 |
| CONNECT-UDP   | UDP       | QUIC / real-time apps (RFC 9298)          |

Flow: client opens an H2/H3 connection and authenticates (`Proxy-Authorization`) → sends a `CONNECT`
for `host:port` → proxy replies `200 OK` → proxy dials the destination from a **geolocation-matched
egress IP** → bytes tunnel through end-to-end encrypted. The proxy forwards bytes **without
inspection**: it sees destination host+port, never the request content; the destination sees the
Cloudflare egress IP, never the client's real IP.

## Deployment models
- **Single-hop** — Cloudflare runs everything (auth + proxy + egress). Simplest; the proxy operator
  sees both identity and destination. Example: **Microsoft Edge Secure Network**.
- **Double-hop** — *You* run Proxy A (authenticates users, encrypts destination); Cloudflare runs
  Proxy B (decrypts destination, egresses). No single party sees both identity and destination.
  Example: **iCloud Private Relay** (Apple = Proxy A). Use when threat model / compliance demands
  separation of user data.

## Authentication
Three methods (set in the `Proxy-Authorization` header unless noted):

| Method                | Header / mechanism                              | When                          |
| --------------------- | ----------------------------------------------- | ----------------------------- |
| Pre-shared key (PSK)  | `Proxy-Authorization: Preshared <key>`          | **Testing / PoC only**        |
| Privacy Pass tokens   | `Proxy-Authorization: PrivateToken token=<b64>` | **Production** (client→server)|
| mTLS                  | TLS client certificate in handshake             | Server-to-server integrations |

- **PSK is shared** — same key for all clients, so no per-user revocation/quota, and the proxy can
  link all requests. Never use in production.
- **Privacy Pass** (three-party: Attester / Issuer / Origin) issues **cryptographically unlinkable**
  tokens — the proxy learns only that a token is valid, not who holds it. Cloudflare can run the
  issuer or you integrate a third party. This is what makes the privacy guarantee real.
- In double-hop, auth happens twice: user→Proxy A (your accounts/SSO/tokens/mTLS) and Proxy A→Proxy B
  (TLS, optionally Raw Public Key extension).

## Geolocation
The killer feature: egress IPs are chosen to match the user's region so location-based services work.
- Client (or Proxy A) sends `sec-ch-geohash: <geohash>-<country_code>` (e.g. `9q8yy-US`,
  `u4pruydqqvj-GB`). The country code disambiguates geohashes that straddle borders.
- Reduced-precision geohashes (typically 4–5 chars ≈ city/region) — proxy maps to an egress IP pool
  registered to that area. Achieves **city-level** accuracy by default, **country-level** fallback.
  Users may opt into coarser (country+timezone only).
- **Prefer IPv6** egress (AAAA on your origins) → better geo precision than IPv4. In double-hop the
  geohash is cryptographically protected so clients can't spoof location.
- Smoke test: search "pizza near me" through the proxy — results should be the user's real city.

## Connect & client libraries
Browsers can't be pointed directly (custom auth headers needed). Options:
- **curl** (HTTP/2): `curl --proxy https://your-proxy.example.com --proxy-header "Proxy-Authorization:
  Preshared <PSK>" https://example.com` — verify against `…/cdn-cgi/trace` (check `ip` = egress).
- **Chaussette** — local SOCKS5→CONNECT shim for apps that speak SOCKS5 but not HTTP CONNECT:
  `MASQUE_PRESHARED_KEY=<PSK> chaussette --listen 127.0.0.1:1987 --proxy https://…:443 [--geohash 9q8yy-US]`,
  then point the app at `socks5://127.0.0.1:1987`.
- **tokio-quiche** / **quiche** — Cloudflare's Rust QUIC+HTTP/3 libs (CONNECT & CONNECT-UDP); powers
  the proxy itself. **privacypass-ts** (`@cloudflare/privacypass-ts`) — TS Privacy Pass token issue/redeem.

## Observability
Privacy-safe telemetry only (no user IPs, request content, or per-connection raw records):
- **GraphQL Analytics API** (recommended default) — POST to `api.cloudflare.com/client/v4/graphql`
  with an *Account Analytics* read token + `accountTag`. Four aggregate, **adaptively sampled** nodes:
  `privacyProxyRequestMetricsAdaptiveGroups`, `…IngressConnMetrics…`, `…EgressConnMetrics…`,
  `…AuthMetrics…`. Dimensions include `coloCode`, `statusCode`, `proxyStatus`, `authMethod`/`authResult`.
- **OpenTelemetry (OTLP)** — Cloudflare exports metrics + ~1%-sampled traces to a collector endpoint
  you supply during onboarding (bearer/custom-header/mTLS auth). Plus a client-side `Server-Timing:
  proxy;dur=<ms>` response header usable as an SLI.

## Gotchas
- **`proxyStatus`** classifies proxy-level errors (`dns_error`, `connection_refused`,
  `tls_certificate_error`, `rate_limited` = per-origin conn/s cap, `proxy_loop_detected`, …); empty
  string = no proxy error. `403` = auth failed, `502` = couldn't reach destination, `503` = proxy busy.
- Metrics are **sampled** (adaptive groups; OTel traces ~1%) — don't treat counts as exact billing data.
- Several schema fields are marked **"Not yet available"** (e.g. `tunnelType`, `tlsVersion`,
  `connectRequestHandlingDuration*`) — don't depend on them yet.
- PSK gives a false sense of production-readiness — it's explicitly testing-only (see Authentication).
- This is a **forward** proxy (protects users reaching the internet), not a reverse proxy for your origin.

## Availability & limits
> ⚠️ **Enterprise-only, contract-provisioned — there is no public/self-serve pricing.** Verify
> commercial terms with Cloudflare; do not quote a price. Contact: `cloudflare.com/lp/privacy-edge/`.

- Onboarding gives you a **proxy endpoint URL**, a **PSK** (PoC), and the **egress IP ranges**
  destinations will see.
- Operational quota of note: a **per-origin connections-per-second** cap (surfaces as
  `proxyStatus = rate_limited`) — exact value is deployment-specific.

## Going deeper
- No official `cloudflare` skill `references/privacy-proxy/` exists — this file is the primary local reference.
- Live docs: `developers.cloudflare.com/privacy-proxy/` (concepts: how-it-works, deployment-models,
  geolocation, authentication; reference: http-headers, client-libraries, metrics, proxy-status).
- Background: blog "A Primer on Proxies", iCloud Private Relay, Edge Secure Network; RFC 9298
  (CONNECT-UDP); IETF MASQUE & Privacy Pass working groups.
- Related products: **Privacy Gateway** (OHTTP, request-level), **WARP** (consumer VPN).
