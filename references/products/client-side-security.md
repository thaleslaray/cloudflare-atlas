# Client-side security — protect visitors from client-side threats (formerly Page Shield)

> Monitors the third-party scripts, connections, and cookies that run in your visitors' browsers,
> alerts on new/changed/malicious resources (Magecart skimmers), and can enforce a CSP allowlist.
> The Cloudflare-native defense against client-side supply-chain attacks. Zone-level, not a Worker.

## Contents
- When to use (and when not)
- How it works (CSP-based)
- Config & enabling
- Key API / access patterns
- Detection & scoring
- Gotchas
- Pricing, plans & limits
- Going deeper

## When to use
- You load **third-party scripts** (analytics, ads, chat widgets, payment forms) and want visibility
  into what's actually running in visitors' browsers + alerts when scripts change or look malicious.
- **Detect Magecart / formjacking** — injected JS that skims payment-card data on checkout pages.
- **CSP management without hand-editing headers** — build an allowlist of scripts/connections and let
  Cloudflare emit the `content-security-policy` header, blocking everything else.
- **PCI DSS v4 compliance** — helps satisfy requirements 6.4.3 (script management) and 11.6.1 (change
  detection) on payment pages (requires Advanced).
- **Not** for: server-side / origin protection (→ waf, api-shield), bot mitigation (→ bots/turnstile),
  or rewriting/injecting scripts yourself (→ Workers + HTMLRewriter). This product observes and
  controls via CSP; it does not modify your script contents.

## How it works (CSP-based)
Built entirely on browser-native **Content Security Policy (CSP)** headers — no agent, no SDK:
- **Resource monitoring** auto-adds a `content-security-policy-report-only` header to a **sample** of
  HTML responses. The report-only header blocks nothing; browsers send violation reports to Cloudflare,
  which builds the list of scripts, the connections they make, and cookies seen in HTTP traffic.
- **Content security rules** (Advanced) emit headers on **100% of matching responses** (not sampled):
  - *Log* rules → `content-security-policy-report-only` (reports violations, blocks nothing).
  - *Allow* rules → `content-security-policy` (actively **blocks** resources outside your allowlist).

## Config & enabling
No `wrangler.jsonc` binding — this is a **zone-level** product configured via dashboard or API.
- **Enable monitoring:** dashboard Security → Settings → turn on *Continuous script monitoring*
  (old UI: Security → Client-side security → Settings → Enable). You cannot disable the monitoring
  header while monitoring is on.
- **Reporting endpoint** (Advanced): default is Cloudflare-owned
  (`csp-reporting.cloudflare.com/cdn-cgi/script_monitor/report`); can switch to *Same hostname*
  (`<your-host>/cdn-cgi/script-monitor/report`). If you do, ensure no rate-limiting/custom rules
  match `cdn-cgi/*`.
- **Connection target details:** *Log host only* (default, domain-only check) vs *Log full URI*
  (needed for malicious-URL checks on outgoing connections — logs full URLs in clear text, may
  expose session IDs to dashboard viewers).

## Key API / access patterns
Page Shield API (name unchanged): base `https://api.cloudflare.com/client/v4`, all under
`zones/{zone_id}/page_shield`. Token perms: `Page Shield` / `Page Shield Read` / `Domain Page Shield` / `Domain Page Shield Read`
(or `Zone Settings Write` / `Zone Settings Read`).
- `GET/PUT zones/{zone_id}/page_shield` — get / update settings (enable via `{"enabled": true}`).
- `GET …/page_shield/scripts[/{id}]` · `…/connections[/{id}]` · `…/cookies[/{id}]` — list/get detected
  resources. Lists default to **`active` status only** unless you pass a `status` filter; paginate
  with `page` / `per_page`.
- `GET/POST/PUT/DELETE …/page_shield/policies[/{id}]` — content security rules ("policies" in the API).
  Create example: `{"action":"log","expression":"http.host eq \"app.example.com\"",
  "value":"script-src app.example.com cdnjs.cloudflare.com 'self'"}` — `value` is a raw CSP directive
  string; switch `"action":"allow"` to start blocking.

## Detection & scoring (Advanced)
Three independent malicious checks (domain check is available to all plans; script + URL checks need Advanced):
- **Malicious script detection** — ML (incl. a Workers-AI LLM, open-source models) analyzes JS code,
  tuned to catch Magecart skimmers. Assigns a **JS integrity score 1–99** (lower = riskier); classified
  malicious **below 10**. Also emits per-category scores (Magecart, crypto mining, malware). The
  classifier only runs on scripts **up to 300 KB** — combine with URL/domain feed signals.
- **Malicious URL / domain checks** — looks up script URLs and domains against threat-intel feeds;
  feed updates re-check previously seen resources.
- The `Malicious`/`Not malicious` label is **not a direct API field** — compare `js_integrity_score`
  against the threshold (10) yourself.

## Gotchas
- **Monitoring is sampled**, so a newly deployed script/cookie can take time to appear in dashboards;
  rule headers are *not* sampled.
- **Resource lifecycle:** *Infrequent* (<3 reports) → purged after 5 days; *Active* (>3 reports);
  *Inactive* (no report 7 days) → purged after 30 days. Infrequent/inactive only show in the
  "All Reported" dashboards, not the active view.
- **Always validate Allow rules with a Log rule first** — going straight to *Allow* can block essential
  scripts and break your site. Docs recommend *Log* for **at least seven days** before switching;
  review rule violations, then flip *Log* → *Allow*.
- Third-party providers often require specific CSP directives — check their docs before locking down.
- Disabling monitoring does **not** disable content security rules (and vice versa) — turn off each
  separately.
- *Same hostname* reporting can interfere with other Cloudflare features matching `cdn-cgi/*`.

## Pricing, plans & limits
> ⚠️ Verify on the live pricing/plans page before quoting — availability is plan-gated and changes.
Bundled with your plan (no per-request meter); capabilities scale by tier:
- **All plans (incl. Free):** script monitoring + domain-based threat checks.
- **Business+:** connection & cookie monitoring, page attribution, New Resource / New Domain alerts.
- **Client-Side Security Advanced (add-on):** malicious **script** & **connection** detection +
  alerting, code-change detection, content security rules (**positive blocking**), custom reporting
  endpoint, Logpush, PCI DSS support.

**Key limits (Advanced):** content security rules (positive/allow blocking) **5** · Logpush jobs **4** ·
malicious-script classifier max script size **300 KB** · malicious threshold JS integrity score **10**.
Non-Advanced plans get **0** blocking rules and **0** Logpush jobs.

## Going deeper
- No dedicated official `cloudflare` skill reference exists for this product — this file is the primary
  reference. For exact, current numbers prefer the rendered docs under
  `docs-oficiais/pages/client-side-security/`.
- Full REST API: `developers.cloudflare.com/api/resources/page_shield/` (still named `page_shield`).
- CSP directive support: `client-side-security/rules/csp-directives/`. PCI DSS mapping:
  `client-side-security/reference/pci-dss/`.
