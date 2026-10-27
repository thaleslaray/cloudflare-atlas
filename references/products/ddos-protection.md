# DDoS Protection — autonomous L3/4 + L7 mitigation (always-on)

> Cloudflare automatically detects and mitigates DDoS attacks across the network (L3/4) and
> application (L7) layers via autonomous managed rulesets. **On by default, on every plan,
> unmetered/free.** You mostly tune sensitivity, not turn it on.

## Contents
- When to use (and when not)
- How it's structured (rulesets & phases)
- Overrides & config (sensitivity / action)
- Adaptive DDoS Protection
- Gotchas
- Plan-gating, pricing & limits
- Going deeper

## When to use
- **Always-on by default** — any zone proxied through Cloudflare (orange-cloud) gets L7 HTTP DDoS
  protection; any traffic to Cloudflare IPs gets L3/4 protection. No setup to "enable" it.
- Reach for the controls when you need to **tune**: suppress false positives, raise sensitivity on
  a targeted attack, or `log`-test rules (Enterprise Advanced) before blocking.
- Pairs with: **WAF** (custom app rules, rate limiting), **Bot Management**, **Magic Transit /
  Spectrum** (extends L3/4 + advanced TCP/DNS protection to non-HTTP and BYOIP traffic).
- **Not** a substitute for the WAF or rate limiting — DDoS rulesets target *volumetric/known-vector*
  attacks. Application-logic abuse and per-endpoint limits belong in WAF / Rate Limiting.

## How it's structured (rulesets & phases)
Two managed rulesets, configured via the **Rulesets API** (same engine as WAF):
- **HTTP DDoS (L7)** — phase `ddos_l7`, configurable at **zone or account** level. HTTP/HTTPS floods.
- **Network DDoS (L3/4)** — phase `ddos_l4`, **account level only**. UDP/SYN/DNS/ACK floods etc.

You don't author detection rules — Cloudflare ships hundreds of managed rules. You attach an
**override** to a managed ruleset to change behavior, scoped by category/tag or individual rule ID.

## Overrides & config (sensitivity / action)
Override two things per rule (or category):
- **Action**: `block` · `managed_challenge` · `challenge` · `log` (log = Enterprise Advanced only,
  for validating before blocking). Some internal actions (e.g. connection-close) can't be set.
- **Sensitivity** (`sensitivity_level`): `default` (= High, the default) · `medium` · `low` ·
  `eoff` (Essentially Off). Higher sensitivity = lower threshold = mitigates sooner.

Override via Rulesets API (sketch):
```jsonc
{ "action": "execute",
  "action_parameters": { "id": "<managed-ruleset-id>",
    "overrides": { "sensitivity_level": "medium", "action": "managed_challenge" } },
  "expression": "true",            // custom expressions = Enterprise Advanced only
  "enabled": true }
```
Recommended rollout: `log` + `medium` → watch 24–48h → add exceptions for false positives →
raise to `default` and `log` → `managed_challenge` → `block`.

## Adaptive DDoS Protection
Learns a **7-day rolling traffic baseline** (95th-percentile rates) and flags deviations. Four
profile dimensions: **Origins** (origin error rate), **User-Agents** (network-wide UA profile),
**Locations** (client country/region), **Protocols** (IP protocol, plus client country/region for
UDP). HTTP adaptive rules also factor Bot ML scores. Gating: Origins/User-Agents/Locations are for
**WAF/CDN customers on Enterprise *with the Advanced DDoS Protection subscription***; Protocols is
for **Magic Transit / Spectrum BYOIP customers on Enterprise**. Free/Pro/Business **and plain
Enterprise** get error-rate adaptive rules only. Adaptive rules default to `log` — review flagged
traffic before mitigating.

## Gotchas
- **Cannot be turned off.** Always-on. The minimum is `sensitivity_level: "eoff"` — and even then,
  exceptionally large attacks are still mitigated to protect Cloudflare's network.
- **Zone overrides beat account overrides** for L7; if a zone override exists it takes precedence.
  Conflicts usually mean an unexpected zone-level override is shadowing the account config.
- **Custom expressions & `log` action are Enterprise-Advanced-only.** On other plans use
  `expression: "true"`; combine conditions with `and`/`or` to fit the 1-rule override cap.
  (API error codes for this were dropped — not found in the live docs.)
- **Only Magic Transit / Spectrum customers on Enterprise can customize the L3/4 ruleset** — the
  ruleset protects every plan, but overrides on `ddos_l4` are limited to those customers.
- **Adaptive needs ≥7 days of traffic** (and minimum rps) to build a profile — quiet/new zones see
  nothing. For **SSL-for-SaaS** zones the zone-level profile aggregates all custom hostnames, so
  per-hostname adaptive accuracy is poor.
- L3/4 (`ddos_l4`) is **account-scoped only** — no per-zone L3/4 override.
- Don't over-tune. Keep overrides minimal; lean on `default` sensitivity unless you have a reason.

## Plan-gating, pricing & limits
> ⚠️ Verify on the live pricing/plans page before quoting — `developers.cloudflare.com/ddos-protection/`.

**Standard, unmetered L3–L7 DDoS protection is FREE on every plan** (Free included) — no traffic
billing for absorbed attacks. What's gated is *tuning depth*, not protection:

| Capability | Free / Pro / Business | Enterprise | Ent + Advanced DDoS add-on |
|---|---|---|---|
| L7 + L3/4 mitigation (unmetered) | ✓ | ✓ | ✓ |
| Override rules per ruleset | 1 | 1 | **10** |
| Custom expressions / `log` action | ✗ | ✗ | ✓ |
| Adaptive DDoS | error-rate rules only | error-rate rules only | ✓ (all signals + ML) |
| Proactive false-positive detection | ✗ | ✓ | ✓ |
| Alerts | basic | basic | advanced (filtering) |

**Advanced TCP / Advanced DNS / Programmable Flow Protection** are available to **Magic Transit**
customers only (not part of the standard HTTP/CDN offering; for Spectrum and HTTP services
Cloudflare leverages the reverse proxy instead). Don't confuse this with Adaptive-for-Protocols,
which *is* Magic Transit / Spectrum BYOIP.

## Going deeper
- Covered by the official `cloudflare` skill (`references/ddos/`) — use it for the full Rulesets
  API flow, ruleset-ID discovery (`rulesets.list()`), SDK snippets, error codes, and tuning patterns.
- Exact Rulesets API: exact endpoints: the live API docs (`developers.cloudflare.com/api/`).
- L3/4 beyond HTTP (BYOIP, on-prem) → see `magic-transit` / `spectrum` references.
