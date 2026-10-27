# API Shield — discover and protect your APIs

> Edge-side API security suite: discover endpoints, validate request/response **schemas**,
> enforce **JWT** tokens and **mTLS** client certs, rate-limit by user, and detect abuse
> (BOLA, volumetric, sequence). Runs on Cloudflare's proxy — no code in your origin.

## Contents
- When to use (and when not)
- How it's wired (no binding — it's a proxy feature)
- Key features & access patterns
- Gotchas
- Plan-gating, pricing & limits
- Going deeper

## When to use
- Securing an API behind Cloudflare: schema/endpoint validation, mTLS client certs, JWT/token
  validation, rate limiting by authenticated user, shadow-API discovery.
- You want enforcement **at the edge** (the proxy blocks bad requests before they reach origin) —
  no SDK, no binding, configured per-**zone** in the dashboard / API / Terraform.
- Pairs with: WAF (managed rules), Rate Limiting, Bot Management, Workers (read `request.cf.tlsClientAuth`;
  JWT claims via WAF fields).
- **Not** for: arbitrary edge compute (→ workers); secrets/token *minting* (you bring the IdP's
  JWKS); protecting non-proxied origins (traffic must flow through Cloudflare's proxy/orange-cloud).

## How it's wired (no binding — it's a proxy feature)
There is **no `wrangler.jsonc` binding**. API Shield is zone-level config:
- **Session identifiers** first (header/cookie that uniquely IDs a user, e.g. `Authorization` or a
  JWT `sub` claim) — prerequisite for Discovery, BOLA, Sequence, Auth Posture, rate-limit recs.
- Features set via dashboard (`Security > API Shield`), the API (`/zones/{zone_id}/api_gateway/*`),
  or Terraform (`cloudflare_api_shield`, `cloudflare_api_shield_operation`, rulesets).
- Enforcement actions are **Log** (observe) or **Block**/Challenge — start in Log, then flip.

## Key features & access patterns
- **Endpoint Management + API Discovery** — inventory endpoints; ML discovers "shadow" APIs from
  traffic (needs 500+ reqs/10d, 2xx from edge). Path-normalized (`/profile/238` → `/profile/{var1}`).
- **Schema Validation 2.0** — upload OpenAPI v3.0; auto-adds endpoints; validates body/params.
  (Classic Schema Validation is **deprecated** — migrate.)
- **Schema Learning** — runs **weekly** on prior-7-day `2xx` traffic (fields need 1,000 qualifying reqs,
  boundaries 10,000). Since 2026-10-12: **Ad-hoc learn schema** (Web Assets → Operations → More options)
  runs on demand, **zone-wide**, from observed traffic only (generates none); thresholds still apply.
- **JWT Validation** — register a token config (location + JWKS from your IdP); enforce in WAF via
  `is_jwt_valid(http.request.jwt.claims["{config_id}"][0])`; rate-limit on a claim with
  `lookup_json_string(...,"sub")`.
- **mTLS** — CF-managed CA (all plans) or upload custom CA; rule on `cf.tls_client_auth.cert_verified`.
- **Vulnerability Scanner** — Enterprise API Shield only; scans your API for known weaknesses.
- **Risk detections** — BOLA (`cf-risk-bola-enumeration` / `-pollution`), Auth Posture
  (`cf-risk-missing-auth` / `-mixed-auth`), Volumetric Abuse, Sequence Mitigation, GraphQL limits.
- **Workers** — read `request.cf.tlsClientAuth` for app logic. (JWT claims are exposed as WAF
  fields `http.request.jwt.claims[...]`; a `request.cf.jwt` object is **not** documented.)

## Gotchas
- **Log first.** Enabling features has zero traffic impact until you move a setting Log → Block.
  Tune false positives in `Security > Events` before blocking.
- **Session IDs must be unique per user.** Shared tokens break BOLA/Sequence and cause false
  positives. Auto-set to `Authorization` if it appears on >1% of successful requests.
- **Detections need traffic + time:** Discovery 500+ reqs/10d (2xx from the edge, not originating from Workers);
  volumetric usa janela de 7 dias e exige 50+ sessões distintas em 24h; Auth Posture rotula
  diariamente. (Removidos "BOLA 1000+ reqs/dia" e "risk labels 24–48h" — sem fonte.)
- **JWT pitfalls:** JWKS must match IdP; header/cookie name must match config. Tokens only from
  headers/cookies — **not** query params or body (POST body: contact your account team).
  (Removidos: "±5 min clock skew" e "nesting de claim 10 níveis" — sem fonte na doc atual.)
- **Schema:** OpenAPI **v3.0.x** (a v3.1 upload is accepted only if it uses v3.0-compatible semantics;
  2.0 unsupported), local `$ref` only (bundle external refs first); no `content`/object-param validation.
  Body inspected per plan: Free 1 KiB, Pro/Business 8 KiB, Enterprise 128 KiB (separate from the WAF
  body limit).
  Disable origin MIME sniffing so body-inspection bypasses can't slip through.
- **Classic Schema Validation is deprecated:** you can edit existing classic settings but not add schemas;
  migrate manually by uploading your schemas to Schema Validation 2.0.

## Plan-gating, pricing & limits
> ⚠️ Plan tiers & limits change — verify on the live page
> (`developers.cloudflare.com/api-shield/plans/`) before quoting. API Shield is an **Enterprise
> add-on** (contact your account team); preview access available for evaluation.

**Available without an API Shield subscription** (Free/Pro/Business/Enterprise): only **Endpoint
Management** + **Schema Validation**. Everything else — **API Discovery, JWT, BOLA, Auth Posture,
Volumetric Abuse, GraphQL Protection** — requires the **Enterprise API Shield** add-on.
**Sequence Mitigation** is **closed beta** (Enterprise, contact team). **Schema Profiles**: API Security
customers already have them via Schema Learning + Schema Validation; Enterprise **without** API Security
gets an invite-only closed beta (**Web Assets** page → operation → *Learn profile*). mTLS with a CF-managed CA is
the exception: self-service on **all plans**.

**Endpoint/schema limits by zone plan** (plans page, last updated 2026-09-29):

| Plan | Saved endpoints | Enabled schemas | Combined schema size | Rule action |
|------|----------------|---------|-------------|-------------|
| Free | 100 | 5 | 200 KiB | Block only |
| Pro | 250 | 5 | 500 KiB | Block only |
| Business | 500 | 10 | 2 MiB | Block only |
| Enterprise (no API Shield) | 3,000 | 10 | 5 MiB | Log or Block |
| Enterprise + API Shield | 10,000 | 10 | 10+ MiB | Log or Block |

Other limits: OpenAPI **v3.0.x** (total schema size = column above) · custom mTLS CAs **max 5** per
Enterprise account, quota shared with Workers mTLS and Gateway (CF-managed CA on all plans) ·
**10,000** total operations across enabled schemas (Enterprise + API Shield) · GraphQL: parsing only on
`POST` bodies up to 20 KiB, content-type `application/json`/`application/graphql`, paths ending in
case-sensitive `/graphql`; no fragments or multiple operations; depth/size are set by YOU in rules over `cf.api_gateway.graphql.query_depth` / `query_size`.
(Removidos: "5 MB upload", "JWT nesting 10 levels", "GraphQL depth 1–50 default 10, size 1KB–1MB" — sem fonte.)

## Going deeper
- Covered by the official `cloudflare` skill (`references/api-shield/`) — use it for full setup,
  API endpoints, firewall fields, OWASP API Top-10 mapping, and troubleshooting.
- Exact REST API: `developers.cloudflare.com/api/resources/api_gateway/`.
- OWASP API Security Top 10 → mapped in the official skill's `patterns.md`.
