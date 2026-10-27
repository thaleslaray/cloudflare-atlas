# WAF — Web Application Firewall (filter HTTP traffic, block web attacks)

> Inspect incoming web/API requests and **block, challenge, or throttle** malicious traffic using
> rules written in the Rules language. Covers custom rules, managed rulesets, and rate limiting.
> The successor to the now-deprecated **Firewall Rules**.

## Contents
- When to use (and when not)
- Rule types
- Config (Rulesets API)
- Key concepts & patterns
- Gotchas
- Pricing & plan-gating
- Going deeper

## When to use
- Block/challenge malicious HTTP at the edge: SQLi, XSS, RCE, path traversal, credential stuffing.
- **Custom rules** — your own block/challenge logic on request properties (IP, path, headers, body).
- **Managed Rules** — turnkey, Cloudflare-maintained signature rulesets (OWASP Top 10, CVEs, zero-days).
- **Rate Limiting Rules** — throttle by request rate (brute-force, scraping, API abuse).
- **Not** for: L3/4 volumetric floods (→ DDoS Protection, always-on), bot management (→ Bots /
  Super Bot Fight Mode), client-side/script security (→ Client-side Security, formerly Page Shield).
- **Migrating off Firewall Rules?** Deprecated since 2025-06-15 — rewrite to **custom rules** via the
  Rulesets API. Rule IDs differ, so update any automation keyed on specific IDs.

## Rule types
| Type | Phase | What it does |
|------|-------|--------------|
| **Custom rules** | `http_request_firewall_custom` | Your block/challenge/skip/log logic |
| **Rate limiting rules** | `http_ratelimit` | Count requests per characteristic, throttle |
| **Managed Rules** | `http_request_firewall_managed` | Deploy Cloudflare-maintained rulesets via `execute` |

Managed ruleset IDs: Cloudflare Managed `efb7b8c949ac4650a09736fc376e9aee` (OWASP+CVEs) ·
OWASP Core Ruleset `4814384a9e5d4991b9815dcfc25d2f1f` · Exposed Credentials Check
`c2e184081120413c86c3ab7e14069605` (**deprecated** — use leaked credentials detection) ·
**Free Managed Ruleset** (free plan, high-impact CVEs) · Sensitive Data Detection (Enterprise).

## Config (Rulesets API)
WAF has **no Worker binding** — it's zone/account config managed via the **Rulesets API** (the
ruleset-engine), Dashboard, Terraform, or Pulumi. Deploy a managed ruleset with an `execute` action:
```typescript
import Cloudflare from 'cloudflare';
const cf = new Cloudflare({ apiToken: process.env.CF_API_TOKEN });

await cf.rulesets.create({                       // custom rules
  zone_id, kind: 'zone', phase: 'http_request_firewall_custom',
  name: 'Custom WAF Rules',
  rules: [{ action: 'block', expression: 'cf.waf.score lt 20', enabled: true }],
});
```
Each phase is a separate ruleset (entrypoint) per zone — you cannot mix phases or actions in one.

## Key concepts & patterns
- **Ruleset engine**: WAF is one consumer of the shared ruleset-engine — same Rules-language
  expressions, phases, and `kind: 'zone' | 'root'` model as Transform Rules, Redirects, etc.
- **Detection vs mitigation**: detections (attack score `cf.waf.score`, leaked credentials, bot
  score) only *score* traffic — they never block. Reference the score in a custom/rate-limiting
  rule to act. Attack score is 1 (malicious) → 99 (clean).
- **Failed detections (2026-10-09, all plans)**: `cf.appsec.request.failed_detections` (`Array<String>`, default
  `[]`) = IDs of detections that *reported a failure* (attack score, signatures, content scan, leaked creds e.g.
  `waf_credential_check`, AI prompt detections) → choose fail-open/closed: `len(cf.appsec.request.failed_detections) gt 0`.
  Zone/account custom + rate limiting, zone Request Header Transforms; grants no detection your plan lacks.
- **Attack Signature Detection (2026-09, Early Access — account team):** the Managed Rules signature
  catalog run as a *detection* — same signatures, released to both at once, but it only populates fields
  and never acts. `cf.waf.signature.request.confidence` (`high` = the Managed Rules enabled-by-default
  set, `low` = the disabled-by-default set), `.categories` (e.g. `sqli`, CVE ids), `.refs` (≤10; a Ref
  **equals the Managed Rule public Rule ID**) — all arrays, so test with
  `any(cf.waf.signature.request.categories[*] eq "sqli")`. Review in **Security Analytics → Attack
  Analysis** (sampled — Log Explorer for 100%), then act with a scoped custom rule. It does **not** inherit
  Managed Rules overrides and doesn't replace them; no latency unless a rule references a field. Compare
  safely: custom rule on the fields with *Log*, Managed Rules left on *Block*. A match ≠ blocked.
  Logpush: `wafRequestSignatureRefs` / `wafRequestSignatureCategories` only (no confidence).
- **Application Profiles (2026-08, closed beta)**: a *positive*-security detection — instead of matching
  attack signatures, it models what a request to an operation is *supposed* to look like and flags
  anything outside it. Only profile type today is a **Schema Profile** (fields, types, formats, ranges,
  enums). Source is either learned traffic or an uploaded OpenAPI schema. Detection is **always-on and
  never mitigates** — you act via a custom rule on `cf.schema_validation.learned.violated` or
  `cf.schema_validation.uploaded.violated`, e.g.
  `cf.schema_validation.learned.violated and cf.waf.score lt 20`. Review in **Security > Analytics >
  Profile Analysis** (statuses: Conforms / Violates / Not evaluated) before enforcing. An *operation*
  = method + hostname pattern + path pattern, discovered by Web Assets or added manually; profiling
  starts only when you pick **Learn profile**.
- **Cloudforce One threat intel** (2026-06, needs a Cloudforce One sub + WAF on the zone): matches the
  client IP against the threat-intel DB (rolling 7-day window; IPs age out silently) and populates
  `cf.intel.ip.*` — `datasets` (`ddos`/`waf`), `attacker_names`, `attacker_countries`,
  `target_industries`, `target_countries` — via `any(cf.intel.ip.…[*] == …)`.
- **Execution order** (terminating action stops all later rules): IP Access rules → Firewall Rules
  (deprecated) → **custom rules → rate limiting → managed rules**.
- **`skip`** action bypasses later evaluation: `ruleset: 'current'` skips the rest of *this*
  ruleset; `phases: [...]` skips whole downstream phases (e.g. allowlist an IP past managed rules).
- **Overrides**: tune a managed ruleset without forking — whole-ruleset action (e.g. `log`), per-category, or per-rule ID.

## Gotchas
- **`update()` replaces the entire rule list** — GET the ruleset, spread existing rules, then update,
  or you wipe other rules.
- **Rate limiting behind NAT** — many users on one IP trip limits; add characteristics (session
  cookie, User-Agent, auth header) beyond `ip.src`. Counting happens before mitigation.
- **Expression syntax**: quote strings (`ip.src.country eq "US"`), use `gt`/`lt` not `>`/`<`,
  `http.request.uri.path` (not `.path`), escape regex. Test in Security Events before deploying.
- **False positives**: deploy managed rules in `log` mode first, review Security Events, then
  override the noisy rule IDs before flipping to `block`.
- **Application Profile learning is slow and partial**: weekly runs over the previous 7 days, only
  `2xx` responses qualify — **1,000** qualifying requests to learn fields, **10,000** to learn
  boundaries (ranges, lengths); first profile can take 7 days after the threshold. Unsupported:
  multipart forms, GraphQL, XML. Not a complete allowlist — successful traffic can include bots and
  scanners, so review the learned schema first. Each weekly run can *change* the profile; for a
  fixed contract, export it as OpenAPI and upload it for Schema Validation instead.
- **Perf**: prefer string operators (`starts_with`) over `matches` regex; `skip` static assets early.

## Pricing & plan-gating
> ⚠️ Plan-gating changes — verify on the live page (`developers.cloudflare.com/waf/`) before quoting.

WAF itself has no per-request charge; capability and quotas are **gated by zone plan**
(as of 2026-08):
- **Custom rules**: Free 5 · Pro 20 · Business 100 · Enterprise 1000.
- **Rate limiting rules**: Free 1 · Pro 2 · Business 5 · Enterprise 100 (Ent needs app security
  on contract). **Advanced Rate Limiting** (more characteristics, complex expressions,
  complexity-based counting) is an Enterprise paid add-on.
- **Managed Rules**: Free → *Free Managed Ruleset only*; Pro+ → full Cloudflare Managed + OWASP CRS.
- **Detections**: attack score Business+ (one field) / Enterprise (full); malicious uploads &
  AI Security for Apps are Enterprise paid add-ons; leaked credentials available from Free.
- **Application Profiles**: API Security customers already have Schema Profiles; everyone else needs
  the **closed beta for invited Enterprise** (account team) — implies nothing about future pricing.
- **Account-level WAF config** (deploy to many zones): Enterprise only.
- **Custom rulesets per zone**: Free 1 · Pro 2 · Business 5 · Ent 10 (rules count toward the cap
  above). **Expression length: 4,096 characters max; 64 regexes per rule** — both apply on every plan
  and are documented in the PARENT product, `ruleset-engine`, not in the WAF docs (search there too).
  Rules-per-ruleset 75/400/1000 stays dropped — absent from the engine docs.

## Going deeper
- Official `cloudflare` skill (`references/waf/`): SDK methods, Wrangler/Terraform/Pulumi config,
  end-to-end patterns (deploy managed, override, skip).
- Ruleset engine & Rules language: `references/products/` siblings + `developers.cloudflare.com/ruleset-engine/`.
- Exact REST API: `references/api/waf.md` — endpoints sliced from the OpenAPI spec (verify live).
