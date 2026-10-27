# Ruleset Engine — the shared rules engine (expressions + phases)

> The underlying engine that powers Rules, WAF, DDoS, Cache Rules, Transform Rules, and more. One
> Wireshark-like **expression language** + a set of request/response **phases** + one **Rulesets API**.
> You rarely use it as a "product" — you touch it directly when API-driving rule management.

## Contents
- When to use (and when not)
- Core model (rules → rulesets → phases)
- Rules language (expressions, fields, operators, actions)
- Rulesets API (key patterns)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **API/Terraform-driven rule management** across WAF custom rules, rate limiting, Transform Rules,
  Cache Rules, Origin Rules, Single/Bulk Redirects, Config Rules, DDoS overrides, Snippets, etc. —
  all share this engine, so the same API/expression syntax configures every one.
- Deploying or overriding **managed rulesets** (e.g. WAF Managed Rules, DDoS managed rulesets).
- Building **custom rulesets** (currently WAF only) and deploying them to a phase.
- **Not** a thing you provision/bind in a Worker. For per-request logic in code → Snippets or Workers.
  For the product UIs, see each product (`waf`, `rules`, `ddos`). This file is the engine itself.

## Core model (rules → rulesets → phases)
- **Rule** = filter **expression** + **action**. If the expression evaluates `true`, the action runs.
- **Ruleset** = an *ordered* set of rules. A ruleset belongs to exactly one phase and is **versioned**
  (every edit bumps the version; old versions remain referenceable).
- **Phase** = a stage in the request/response lifecycle (defined by Cloudflare, immutable). Each phase
  has at most one **entry point ruleset** per level (account or zone). Account-level rules run before
  zone-level rules in the same phase. Account-level phases are Enterprise-only.
- **Deploying** = adding a rule with the `execute` action to a phase entry point that runs a managed
  or custom ruleset.
- Ruleset `kind`: `root` (account entry point), `zone` (zone entry point), `managed`, `custom`.
- **Execution order across products** is fixed by the phase order. Request phases, in order:
  `http_request_dynamic_redirect` (Single Redirects) → `http_request_sanitize` (URL normalization) →
  `http_request_transform` (URL Rewrite) → `http_config_settings` (Configuration Rules) →
  `http_request_origin` (Origin Rules) → `ddos_l7`\* → `http_request_firewall_custom` (WAF custom rules)
  → `http_ratelimit` → `http_request_firewall_managed` (WAF Managed) → `http_request_sbfm` (Super Bot
  Fight Mode) → `http_request_redirect` (Bulk Redirects) → `http_request_late_transform` (Request Header
  Transform) → `http_request_cache_settings` (Cache Rules) → `http_request_snippets` →
  `http_request_cloud_connector`. (\* `ddos_l7` and `http_request_api_gateway_early` are
  configuration-only phases — rules aren't executed at that stage.)
  Response phases, in order: `http_custom_errors` → `http_response_headers_transform` → `http_ratelimit`
  (when rate limiting uses response info) → `http_response_compression` → `http_response_firewall_managed`
  (Sensitive Data Detection) → `http_log_custom_fields`. Network-layer: `ddos_l4`, `magic_transit`,
  `magic_transit_managed`, `magic_transit_ratelimit`, `magic_transit_ids_managed`. Full Phases list below.

## Rules language (Wireshark-style)
- **Simple expression**: `<field> <operator> <value>` — e.g. `http.request.uri.path matches "/admin"`.
- **Compound**: combine with `and` / `or` / `not` + parentheses — e.g.
  `http.host eq "www.example.com" and not cf.edge.server_port in {80 443}`. `true` = match every request.
- **Fields**: request fields (`http.host`, `http.request.uri.path`, `ip.src`, `http.cookie`…), dynamic
  fields (threat intel, e.g. `cf.threat_score`, `cf.bot_management.score`), response fields, and **raw
  fields** (`raw.http.request.uri.path`) that preserve original values across phases. Full list in the
  Fields reference.
- **Operators**: `eq` `ne` `lt` `gt` `le` `ge`, `contains`, `in {…}` (also CIDR sets:
  `ip.src in {1.2.3.0/24}` — Wireshark's `ip.src == 1.2.3.0/24` is *not* supported), `matches` (regex —
  **Business/Enterprise only**), `wildcard` (case-insensitive) / `strict wildcard` (case-sensitive), where
  each `*` matches zero or more chars and the **entire** field value must match. String comparison is
  case-sensitive by default (use `lower()`); English operators must be lowercase. `starts with` /
  `ends with` / `is in list` exist only in the dashboard — write them as the `starts_with()` / `ends_with()`
  functions or `<field> in $<LIST>`.
- **Actions** (availability depends on the phase). Terminating: `block`, `managed_challenge`, `js_challenge`,
  `challenge`, `redirect`, `serve_error`, `log_custom_field`. Non-terminating: `skip` (skips *some* rules,
  per config), `log` (Enterprise only), `execute` (run another ruleset), `rewrite` (Transform Rules),
  `route` (Origin Rules), `set_config` (Config Rules), `set_cache_settings` (Cache Rules),
  `compress_response` (Compression Rules). Last non-terminating change in a phase wins; first terminating wins.

## Rulesets API (key patterns)
Base URL `https://api.cloudflare.com/client/v4`, Bearer token. Scope is `/zones/{zone_id}` or
`/accounts/{account_id}`. Phase entry points have a shortcut endpoint that takes the **phase name**
instead of a ruleset ID:
```
GET    /zones/{zone_id}/rulesets                                         # list rulesets
GET    /zones/{zone_id}/rulesets/{ruleset_id}                            # view latest version (+ versions/{n})
PUT    /zones/{zone_id}/rulesets/phases/{phase_name}/entrypoint          # deploy/replace a phase's rules
POST   /zones/{zone_id}/rulesets/{ruleset_id}/rules                      # add one rule
PATCH  /zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}            # update/reorder one rule
DELETE /zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}            # delete one rule
```
Deploy a managed ruleset to a phase (note: PUT **replaces** all rules in that entry point):
```bash
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rulesets/phases/http_request_firewall_managed/entrypoint" \
  --request PUT --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --json '{ "rules": [ { "action": "execute",
      "action_parameters": { "id": "efb7b8c949ac4650a09736fc376e9aee" },
      "expression": "true", "description": "Execute Cloudflare Managed Ruleset" } ] }'
```
Managed rulesets are tuned with **overrides** (change default action/status per rule, tag, or whole
ruleset) and **exceptions/skip rules**, not by editing them directly.

## Gotchas
- **PUT to an entry point is destructive** — it replaces *all* rules in that phase. To touch one rule,
  use the add/update/delete-rule endpoints instead.
- **Fields are immutable within a phase.** A URL-rewrite rule's change isn't visible to a later rule in
  the same phase; values can change *between* phases. Use `raw.*` fields to read original values.
- **`matches` (regex) needs Business/Enterprise.** Lower plans must use `wildcard`/`contains`/`starts_with()`.
- **Expression caps: 4,096 characters and 64 regexes per rule** (across all Rules-language rule types;
  existing rules over the regex cap keep working but can't be modified until simplified).
- Use the `ref` field (user-defined external id) to keep stable rule IDs across edits — important for
  Terraform so it doesn't recreate rules.
- **Super Bot Fight Mode rulesets must not be edited via the Rulesets API** — it's unsupported and can break.
- Account-level `skip` only affects account-level rules/phases; zone-level needs a zone-level skip rule.
- `name`, `kind` and `phase` are immutable for the life of a ruleset — omit them from update requests.

## Pricing & limits
> ⚠️ Verify on the live pricing pages before quoting — pricing is volatile.

The Ruleset Engine itself has **no separate price** — it's the shared infrastructure. What you pay is
determined by the **product** you configure with it (WAF, Rate Limiting, Transform Rules, Cache Rules,
etc.) and your plan. Notable plan gates: account-level phases and `log` action are **Enterprise-only**;
the `matches` regex operator needs **Business/Enterprise**. Engine-wide expression limits (all plans):
**4,096 characters** per rule expression, **64 regular expressions** per rule. Per-product rule counts and
ruleset sizes vary by plan — check each product's "Plans"/"Availability" page and the WAF/Rules limits pages.

## Going deeper
- No dedicated official `cloudflare` skill ref exists for the engine itself — see the related product
  refs (`waf`, `rules`, `ddos`) and the live docs.
- **Phases list** (full execution order + which product owns each phase):
  `developers.cloudflare.com/ruleset-engine/reference/phases-list/`
- **Fields reference** (every field): `developers.cloudflare.com/ruleset-engine/rules-language/fields/reference/`
- **Rulesets API** (all endpoints + JSON object schema): `developers.cloudflare.com/ruleset-engine/rulesets-api/`
- Local rendered docs: `raw/docs-oficiais/pages/ruleset-engine/` (about/, rules-language/, rulesets-api/).
