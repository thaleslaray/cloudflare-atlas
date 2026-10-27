# Privacy Pass — anonymous cryptographic tokens (IETF RFC 9576)

> Let a client **prove a claim** (passed a CAPTCHA, is of age, holds a subscription) to a server
> **without revealing an identifier** and without being linkable across requests. Cloudflare runs
> the **Issuer**. **Not self-serve** — production deployments are a managed engagement.

## Contents
- When to use (and when not)
- The four roles
- Issuance & redemption flow
- Endpoints, headers & key API
- Deployment models
- Self-serve demos (what you *can* do today)
- Gotchas
- Pricing & availability
- Going deeper

## When to use
- You need to gate access on a **verified attribute**, but storing/linking that attribute to the user
  is a product-level non-goal: age or subscription checks, "human, not bot", entitlement proofs.
- **Privacy-preserving bot management** — Apple's Private Access Tokens (PATs) use this to auto-reduce
  CAPTCHAs for iOS 16+ users on Safari, participating apps and third-party browsers; **Turnstile**
  uses Privacy Pass tokens as a challenge signal.
- **Auth layer for other privacy products** — Privacy Proxy and Cloudflare OHTTP Relay (formerly
  Privacy Gateway) authenticate users with Privacy Pass tokens.
- **Rate limiting / metering without identity** — still IETF drafts (Batched Tokens, ARC, Reverse
  Flow). **Not production**; do not design a shipping product on it.
- **Not** for: ordinary authn/authz (→ Access / Zero Trust), hiding the client IP from your backend
  (→ **ohttp-relay**, OHTTP), a privacy forward proxy (→ **privacy-proxy**), or plain bot
  mitigation you just want to *work* (→ **turnstile**, which already benefits from it for free).

## The four roles
| Role | Responsibility | Typically operated by |
|---|---|---|
| **Client** | Requests access; runs issuance + redemption | End-user software (browser, app, device) |
| **Origin** | Sends token challenges, verifies redeemed tokens | The site/app being reached; **Cloudflare** if redemption runs at the edge |
| **Attester** | Deployment-specific verification of the Client | **You** (the customer) — the role that varies most |
| **Issuer** | Signs blinded token requests for attested clients | **Cloudflare** (public, RFC 9578-compliant) |

Cloudflare issuers use **publicly verifiable Blind RSA — token type `2`**.

Information split (**unlinkability**): Attester knows *who*, not *where*; Issuer knows only that a
client was attested; Origin knows only that the client is verified. Cryptography alone is not
enough — the **anonymity set must stay large**; anything that gives clients different setups splits
them into smaller groups and shrinks privacy.

## Issuance & redemption flow
```txt
 Origin              Client              Attester            Issuer
   │                   │                    │                  │
   │- TokenChallenge ─>│   (WWW-Authenticate)                  │
   │                   │<=== Attestation ==>│                  │
   │                   │                    │── TokenRequest ─>│  (blinded, mTLS-authenticated)
   │                   │                    │<─ TokenResponse ─│
   │                   │<── TokenResponse ──│                  │
   │<─ Request+Token -─│ [finalize/unblind] │                  │  (Authorization: PrivateToken …)
   │────- 200 OK ────->│                    │                  │
```
1. **Issuance** — Client attests with the Attester → sends a **blinded** token request (masked, so the
   finalized token cannot be linked back) → Issuer signs → Client **finalizes/unblinds**.
2. **Redemption** — Client sends the token with its request in the `Authorization` header → Origin
   verifies the signature against the issuer public key → `200 OK`.

In Cloudflare Issuer deployments the **Client never contacts the Issuer directly** — the Attester
proxies the token request.

## Endpoints, headers & key API
- Directory (public, unauthenticated): **`GET /.well-known/private-token-issuer-directory`**
```json
{
  "issuer-request-uri": "/token-request",
  "token-keys": [
    { "token-type": 2, "token-key": "<base64url public key>", "not-before": 1700000000 }
  ]
}
```
- Token request endpoint: **`/token-request`** (Attester → Issuer, authenticated e.g. via **mTLS
  client certificate**).
- Challenge header from the Origin: **`WWW-Authenticate`** · redemption header: **`Authorization`**
  (`PrivateToken token=…`).

Client side (`@cloudflare/privacypass-ts`):
```ts
import { publicVerif } from '@cloudflare/privacypass-ts';
const { BlindRSAMode, Client } = publicVerif;

const client = new Client(BlindRSAMode.PSS);
const tokenRequest = await client.createTokenRequest(tokenChallenge, issuerPublicKey);
const bytes = await sendToAttester(tokenRequest.serialize()); // YOUR transport — not in the library
const token = await client.finalize(client.deserializeTokenResponse(bytes));
```
Libraries: **TypeScript** `cloudflare/privacypass-ts` · **Go** `cloudflare/pat-go` (reference,
experimental/interop) · **Rust** `raphaelrobert/privacypass` (**not independently audited**).
Reference services: `cloudflare/privacypass-issuer` (Workers, key rotation) and
`cloudflare/privacypass-attester` (attestation via Turnstile, proxies to an issuer).

## Deployment models
- **Fully split** (Apple PAT): Client = iOS, Attester = Apple (device integrity), Issuer = Cloudflare
  + Fastly, Origin = the site. Most private; needs a natural third-party attester.
- **Joint Attester-Issuer** (attribute attestation): Cloudflare runs both to your spec; you are the
  Origin. Avoids introducing a new third party.
- **Generally do not** combine **Origin + Attester** — that party would know both identity and
  destination, which the docs say makes privacy "significantly harder to guarantee". The docs point to
  **RFC 9576 § Deployment Models** for the additional guidelines that keep joint models sound, so this
  is a strong default, not a prohibition. Cloudflare
  can act as Origin for redemption **at the edge**, then forward to your real origin.

## Self-serve demos (what you *can* do today)
- **Demo tool** `privacypass-demo.cloudflare.app` pointed at the open demo issuer directory
  `https://demo-pat.issuer.cloudflare.com/.well-known/private-token-issuer-directory` → fetch
  directory → create challenge → send token request. Prints `Draft 16 Valid: true` + `PrivateToken
  token=…`.
- **Local example**: clone `cloudflare/privacypass-ts`, `npm ci`, add a runner calling
  `publicVerifiableTokensPSS()` from `examples/pub_verif.example.ts`, then `npx tsc -b examples &&
  node ./lib/examples/run-pub-verif.js` → `Valid token: true`. Real Blind RSA, but one process,
  locally-generated issuer key, **attestation stubbed out**.

## Gotchas
- **Production is not self-serve.** You build the deployment *together with Cloudflare* (commercial
  contact) and they provision the issuer, directory and `/token-request`. Only the demo issuer is open.
- **Production issuers only accept requests from an authenticated Attester.** The demo tool
  therefore **cannot complete a token request** against production — use it only as a *directory
  reachability check* or to validate a production token against a production public key.
- **`sendToAttester` is not part of the library.** The Client↔Attester transport is yours to design;
  the standard does not define that interface. The issuer-facing call must happen **inside your
  Attester**, never in the Client.
- **Most people should just use Turnstile** (editorial judgment, not a docs recommendation). Turnstile
  embeds Privacy Pass tokens as a challenge signal automatically, so you get that benefit without
  writing any Privacy Pass code — you still embed the Turnstile widget itself. Standing up your own
  Attester + Issuer engagement only pays off when "we must not be able to track this user" is an actual
  product requirement.
- **Anonymity set is the real security parameter** — a bespoke setup with few users gives weak
  privacy no matter how correct the crypto is.
- The local example is a protocol demo, **not** a deployment blueprint.

## Pricing & availability
> ⚠️ **There is no public pricing page for Privacy Pass** (`/privacy-pass/pricing/` → 404) and the docs
> state no cost model at all — not even that one is negotiated. **Verify with Cloudflare before quoting**
> any number.

- **Not self-serve and no dashboard toggle.** Request access via `cloudflare.com/lp/privacy-edge/`.
  Cloudflare provisions the issuer endpoint, the directory and `/token-request`. The mTLS client
  certificate your Attester uses is listed under *what you operate or need in place*, not under what
  Cloudflare provisions — do not assume it is handed to you; settle it during the engagement.
- **No Worker binding**, but that is not the same as no Workers involvement: the product overview says
  Workers natively supports **redemption**, and the reference issuer/attester are themselves Workers.
- Free, no-contact paths: demo issuer, demo tool, local example, and the open-source reference
  issuer/attester (both Apache-2.0). Self-hosting is not a docs-endorsed production path, and it is not
  Workers-only — the reference issuer stores keys in **R2**.
- **Indirect availability:** Turnstile, Privacy Proxy and OHTTP Relay already use it internally.
  Privacy Proxy is Enterprise; OHTTP Relay is **closed beta to select partners** — being Enterprise
  is not sufficient to get it.

## Going deeper
- No official `cloudflare` skill `references/privacy-pass/` exists — this file is the primary local
  reference. Live docs: `developers.cloudflare.com/privacy-pass/` (getting-started, concepts/
  privacy-pass-protocol, concepts/deployment-models, production-deployment-testing, references).
- Specs: **RFC 9576** (Architecture) · **RFC 9577** (HTTP Authentication Scheme) · **RFC 9578**
  (Issuance Protocols). Drafts (non-production): Batched Tokens, ARC, Privacy Pass Reverse Flow.
- Related here: **turnstile** (easiest on-ramp), **privacy-proxy** (MASQUE), **ohttp-relay**
  (OHTTP, formerly Privacy Gateway), **cloudflare-challenges**. Background: blogs "Eliminating CAPTCHAs on iPhones and Macs" /
  the Privacy Pass standard post; Apple WWDC22 → `scripts/blog-search "Privacy Pass"`.
