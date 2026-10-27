# Monetization Gateway

> Cloudflare gateway that charges per request on proxied HTTP traffic (APIs, MCP tools, sites, datasets) using the x402 protocol (version 2) inline — no checkout redirect. Settled through the Coinbase x402 Facilitator. **Closed beta since 2026-09-30.**

## Contents

- [When to use (and when not)](#when-to-use-and-when-not)
- [Key API / access patterns](#key-api--access-patterns)
- [Gotchas](#gotchas)
- [Pricing & limits](#pricing--limits)
- [Going deeper](#going-deeper)

## When to use (and when not)

**Use when:**

- You sell API access, MCP tool calls, site content or datasets per request to agents and want payment enforced at the edge without a checkout flow.
- Seller and buyers are US-based (current eligibility) and you have a receiving wallet.

**Do not use when:**

- Buyer or seller is outside the US.
- You need a traditional subscription/checkout UX with hosted payment pages.
- Your origin cannot validate a JWT (strongly recommended) or, for variable pricing, report the actual amount.
- You need body / body-size matching and are not on Enterprise.

## Key API / access patterns

### Payment flow

1. Buyer requests the protected resource → gateway returns `402 Payment Required` with a `PAYMENT-REQUIRED` header (Base64 JSON; its `accepts` array lists `scheme`, `network` (CAIP-2), `asset`, `amount`, `payTo`, `maxTimeoutSeconds`).
2. Buyer signs an authorization and retries with `PAYMENT-SIGNATURE` (Base64 JSON) — build it with an x402 client library.
3. Gateway verifies the authorization, then forwards to your origin with a `PAYMENT-CONTEXT` header (a signed JWT).
4. Origin validates the JWT and serves the response; for variable pricing it reports the real charge in `PAYMENT-SETTLEMENT`.
5. Gateway settles through the Coinbase x402 Facilitator and returns the origin response. If verification or settlement fails, the resource is not served.

### Rules

Each rule defines domain, URL, price, audience (**Everyone** or **Verified Bots** via BotBase) and HTTP methods (default `GET`; several allowed). Advanced conditions: header, URI query string, user agent, `X-Forwarded-For`, source IP, continent, country, EU status, cookie value; body and body size are **Enterprise only**.

### Price modes

- Fixed → x402 `exact`: gateway settles the signed amount. Do **not** set `PAYMENT-SETTLEMENT`.
- Variable → x402 `upto`: `amount` is the authorized maximum; origin reports `0 <= actual <= max`.

### Headers reference

| Header | Direction | Purpose |
|---|---|---|
| `PAYMENT-REQUIRED` | gateway → client | Price and accepted payment options on the 402 |
| `PAYMENT-SIGNATURE` | client → gateway | Signed payment authorization |
| `PAYMENT-CONTEXT` | gateway → origin | Signed JWT (Ed25519) carrying the verified authorization |
| `PAYMENT-SETTLEMENT` | origin → gateway | Actual charge for `upto`, e.g. `{ "amount": "1000000" }`; stripped before the buyer sees the response |

### Access

Closed beta — request access in the dashboard (`/:account/monetize/monetization-gateway`).

## Gotchas

- **Eligibility is strict:** US-based seller, Service-Specific Terms accepted, credit card on file, verified email, account **older than 60 days**, passing account security checks; zone proxied, **older than 30 days**, passing zone checks.
- **Validate `PAYMENT-CONTEXT` properly:** use only the pinned JWKS (`payments.cloudflare.com/certs`), require Ed25519, cache keys per the endpoint's `Cache-Control`, never parse without verifying. Recommended libs: `jose` (JS/TS/Workers), `PyJWT` + `cryptography`, Nimbus JOSE + JWT, `golang-jwt/jwt/v5`, `jsonwebtoken` (Rust).
- **No `PAYMENT-CONTEXT` = unpaid and unverified.** Don't serve paid content and don't set `PAYMENT-SETTLEMENT`.
- **Settlement rules for `upto`:** set `PAYMENT-SETTLEMENT` only on a successful response, before headers are sent, never when status ≥ `400`; amount is a string in atomic units. Above the maximum → the maximum is settled; zero → nothing is settled. Don't create a `PAYMENT-RESPONSE` header (the gateway makes the receipt).
- **Never hand-roll x402 payloads** — the signed payload binds to the selected requirements; use an x402 client library (Cloudflare Agents can pay via the Agents SDK x402 tools).

## Pricing & limits

- Prices are in atomic units: 1 unit = $0.000001.
- Minimum: $0.001 (1,000 units). Maximum price: $100 (100,000,000 units).

**Closed beta — verify on the live pricing page before quoting.** No Cloudflare fee schedule for the gateway is published in the docs; confirm current terms after enrollment.

## Going deeper

No official `cloudflare` skill reference exists for this product yet. Docs (6 pages, re-checked 2026-10-03): `developers.cloudflare.com/monetization-gateway/` — `eligibility/`, `get-started/`, `x402/`, `configuration/rules/`, `configuration/payment-validation/`. Buyer side: `agents/tools/payments/x402/`.
