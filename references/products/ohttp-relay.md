# Cloudflare OHTTP Relay (formerly Privacy Gateway) — managed Oblivious HTTP relay

> Managed OHTTP **relay** on Cloudflare's network that **separates *who* from *what*** — it hides
> the client's IP from your application backend, while staying blind to the request contents.
> **Enterprise-only, closed beta.** Renamed from Privacy Gateway (old docs URLs redirect to `ohttp-relay/`).

## Contents
- When to use (and when not)
- How it works (the three parties)
- Setup (server + client + relay)
- Metrics
- Gotchas
- Pricing & limits / availability
- Going deeper

## When to use
- You run a backend that needs **request data but not the user's IP address**, and you want the
  architecture to make linking the two impossible for any single party.
- The mental model: **decouple identity from content**. The relay (Cloudflare) sees *who* + *which
  server* but never *what*; your gateway sees *what* but only the relay's IP, never the client's.
- **Not** for: hiding *content* from Cloudflare while still revealing identity (that's just TLS),
  general request proxying (→ Tunnel/Spectrum/Workers), a privacy forward proxy for whole devices
  (→ `products/privacy-proxy.md`, MASQUE), or anything where your backend legitimately needs the
  client IP. If requests carry user identifiers in the payload, OHTTP buys you nothing (see Gotchas).

## How it works (three parties)
Implements part of the Oblivious HTTP IETF standard. Messages are encrypted **between client and
gateway server**, so the relay learns nothing of the application data beyond the **length** of the
encrypted message and **which server** the client is talking to.

```
Client  --(encrypted req)-->  Cloudflare OHTTP Relay  --(forwards)-->  Your application gateway server
                               sees: client IP, target app            sees: request content,
                               (DNS name + IP), request metadata,     relay server's IP + metadata
                               timestamp — never content              (not the client's)
```
- **Client** (you operate): encrypts requests, sends them to the relay, decrypts responses. Must
  fetch or otherwise discover the gateway's public key configuration.
- **Relay** (Cloudflare operates): forwards encrypted requests/responses between client and gateway.
- **Application gateway server** (you operate): decrypts incoming requests, forwards the inner
  request to its destination, encrypts the response back; advertises its public key configuration
  (generated securely, served via an API) for clients.

## Setup
There is **no Wrangler binding** — this is not a Workers product. Four steps from the get-started page:

1. **Configure your server** — implement an application gateway (decrypt → forward → encrypt +
   publish key config). Sample: `github.com/cloudflare/privacy-gateway-server-go`. Libraries:
   Go `chris-wood/ohttp-go`, Rust `martinthomson/ohttp` (`ohttp-server`), JS/TS `chris-wood/ohttp-js`.
   Spec detail if you build it yourself: `draft-ietf-ohai-ohttp-05` §3 (public key configuration),
   §4 (message encryption/decryption), §5 (server-specific details).
2. **Configure your client** — samples: Objective-C `cloudflare/privacy-gateway-client-demo`,
   Rust `martinthomson/ohttp` (`ohttp-client`), JS/TS `chris-wood/ohttp-js`.
3. **Review your application** (do not skip) — scrub anything unique to an end user (names, email
   addresses, phone numbers); encourage users to disable crash reporting (crash reports can contain
   email addresses); where possible encrypt app data on-device with a client-only key.
4. **Relay through Cloudflare** — contact Cloudflare (privacy-edge form) with your gateway server
   URL, then forward to the mutually agreed URL:
   ```
   https://privacy-relay.cloudflare.com/<GATEWAY_SERVER_NAME>
   ```

## Metrics
GraphQL Analytics API, token with **Analytics Read**. Both nodes use adaptive sampling and require
the `accountTag` filter; optional `limit` and `orderBy`.
- `ohttpMetricsAdaptive` — per-request rows: `bytesToClient`, `bytesToGateway`, `colo`, `datetime`,
  `gatewayStatusCode`, `relayStatusCode`.
- `ohttpMetricsAdaptiveGroups` — `count` / `dimensions` / `sum`. Dimensions: `colo`, `date`,
  `datetimeMinute`, `datetimeFiveMinutes`, `datetimeFifteenMinutes`, `datetimeHour`, `endpoint`
  (the appId that generated traffic), `gatewayStatusCode`, `relayStatusCode`. Sum fields:
  `bytesToClient`, `bytesToGateway`, `clientRequestErrors`, `gatewayResponseErrors`.

## Gotchas
- **Closed beta, Enterprise-only, no self-serve.** Available to select privacy-oriented companies
  and partners; nothing flows until Cloudflare has your gateway URL and you agree the relay URL.
- **Incompatible Cloudflare products** (the relay can't see URLs or content):
  - **Cache** — no caching of application content (every client↔gateway exchange is end-to-end encrypted).
  - **WAF** — rules based on request content are not supported.
  - **API Shield** — **Schema Validation** and API discovery are not possible.
  Most other Cloudflare products remain compatible.
- **It hides IP, not identity.** Cloudflare cannot ensure your app or service won't send identifying
  data (names, emails, phone numbers) in the payload — that's the Review step.
- **Privacy assumes the relay and gateway don't combine data.** If you operate both, you have
  rebuilt an ordinary proxy (architectural consequence of the three-party design).
- **Cloudflare logs relay-side metadata** ("Cloudflare OHTTP Relay Logs"): connecting device IP,
  the application service used (DNS name + IP), request metadata (browser type, device OS, hardware
  configuration) and timestamp. Retained for the most recent quarter plus one month (**~124 days**).
  Content is never seen. Follows Cloudflare's privacy policy.
- **DIY-heavy.** You build and run both client and gateway; Cloudflare only runs the relay.

## Pricing & limits / availability
> ⚠️ **No public pricing.** Closed beta, Enterprise-only; terms are agreed with Cloudflare during
> onboarding — verify current availability and pricing with Cloudflare before planning around it.
- **Access:** contact form at `cloudflare.com/lp/privacy-edge/`; provide your gateway server URL.
- **Log retention:** ~124 days for Cloudflare OHTTP Relay Logs (metadata only).
- No documented request/throughput limits — discuss during onboarding.

## Going deeper
- No official `cloudflare` skill ref exists — this file is the primary reference. Live docs:
  `https://developers.cloudflare.com/ohttp-relay/` (get-started, plus reference pages for metrics, legal,
  product compatibility and limitations).
- Spec: `draft-ietf-ohai-ohttp-05` (as cited by the get-started page); the overview links the
  original `draft-thomson-http-oblivious-01`.
- Auth for privacy products: `products/privacy-pass.md`. Background: Cloudflare blog "Building
  privacy into Internet standards and how to make your app more private today".
