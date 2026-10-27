# Challenges — verify visitors are human

> Lightweight, privacy-preserving challenges that confirm a visitor is a real human (not a bot/script)
> by evaluating browser signals — and only asking for interaction (a checkbox/button) when needed.
> **No** CAPTCHA puzzles. Most humans pass automatically. The challenge *action* you attach to a
> WAF / Bots / rate-limiting rule; the underlying engine that also powers Turnstile.

## Contents
- When to use (and when not)
- Challenge types
- Where challenges come from (which products trigger them)
- Clearance & `cf_clearance` cookie
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You want to **challenge suspicious traffic** (high threat score, bad IP reputation, low bot score)
  instead of hard-blocking it — humans pass, bots abandon.
- As the **action** on a WAF custom rule, rate-limiting rule, IP access rule, or Bot Fight Mode.
- **Under Attack Mode** (`Managed Challenge` on all traffic) during an active L7 attack.
- For challenging a *specific form action* (login/signup) inline without a full-page interstitial →
  use **Turnstile** (embedded widget) instead of a Challenge Page.
- **Not** for: protecting AJAX/XHR/API endpoints with an interstitial page (breaks fetch — use
  Turnstile Pre-clearance); native mobile / websocket traffic; replacing real authn/authz.

## Challenge types
Three challenge *actions* / mechanisms. Cloudflare recommends **Managed Challenge** for almost everything.
- **Managed Challenge (recommended):** Cloudflare dynamically picks the right check from browser
  signals. Most humans verify with **no interaction**; suspicious ones may get a checkbox. Avoids
  CAPTCHAs. Use this unless you have a specific compatibility reason not to.
- **Non-Interactive (JS) Challenge:** full-page interstitial that runs injected JavaScript only —
  no user action, visitor waits (typically <5s) while the browser processes it.
- **Interactive Challenge:** full-page interstitial requiring the visitor to interact (e.g. click a
  box/button) to pass. Highest friction; Cloudflare steers you toward Managed instead.
- **Turnstile:** embedded **widget** (not a full-page gate) — runs the same challenge engine in the
  background on part of the page, issues a token you must verify server-side (Siteverify). Widget
  modes: Managed / Non-Interactive / Invisible. See `products/turnstile.md`.
- **JavaScript Detections:** a *separate* Bot Management feature — an invisible JS snippet on every
  HTML page (not a gate, never interrupts). Populates a pass/fail field you then act on in a rule.

## Where challenges come from (which products trigger them)
A challenge is an **action**, almost never configured standalone — a rule attaches it.
| Product / feature | What it issues |
| --- | --- |
| WAF (custom rules, rate-limiting rules, IP access rules) | Interstitial Challenge Page |
| Bot Fight Mode / Super Bot Fight Mode | Interstitial Challenge Page |
| Bot Management | JavaScript Detections (pass/fail field) |
| Turnstile | Embedded widget |
| HTTP DDoS managed ruleset | Any challenge |
| Under Attack Mode | Managed Challenge (zone-wide) |

JavaScript Detections does **not** block on its own — enable it, then write a WAF custom rule on
`cf.bot_management.js_detection.passed` (Workers: `request.cf.botManagement.jsDetection.passed`)
with a **Managed Challenge** action (legit users may fail it for network/adblock/JS-off reasons).

## Clearance & `cf_clearance` cookie
- Solving a challenge sets a `cf_clearance` cookie proving the visitor passed; it's bound to the
  visitor+device (not freely transferable). Stores JS-detection results too. **Max 4096 bytes.**
- **Clearance levels** are tiered — a higher-level cookie bypasses challenges at or below it:
  | Level | Bypasses |
  | --- | --- |
  | Interactive (high) | Interactive + Managed + Non-Interactive |
  | Managed (medium) | Managed + Non-Interactive |
  | Non-Interactive (low) | Non-Interactive only |
- **Challenge Passage:** zone-level cookie lifetime, default **30 min** (recommend 15–45). Does
  **not** apply to rate-limiting rules. Clearance stays valid for that duration *unless Precursor
  determines the session is suspicious*.
- **Precursor** (zone setting, Security → Settings): client-side, **session-based** verification that
  keeps re-running in the browser and updates the session state stored in `cf_clearance` — instead of
  a single challenge event. Two modes: **Minimize Friction** (default, no interstitial, best-effort
  session state) and **Maximize Security** (recommended; shows a lightweight interstitial to
  establish a session — requests must then present a valid `cf_clearance`, which breaks non-browser
  API clients like curl/mobile backends unless scoped with **Precursor Rules**).
- **Turnstile Pre-clearance:** opt-in mode where the Turnstile widget *also* issues a `cf_clearance`
  cookie (in addition to its token) at a chosen level (`interactive`/`managed`/`jschallenge`/
  `no_clearance`, default off). Lets a visitor solve once on an HTML page, then hit WAF-protected
  **API/fetch endpoints** without a Challenge-Page response. The fix for SPAs/AJAX. Widget hostname
  must match the zone with the WAF rules.

## Gotchas
- **Interstitial pages break AJAX/XHR/fetch & SPAs** — they return a full HTML page the browser
  can't render mid-fetch. Use **Turnstile Pre-clearance** for API endpoints.
- **CORS preflight (`OPTIONS`) carries no cookies** → `cf_clearance` isn't sent → preflight fails
  the challenge. Account for this in CORS-heavy apps.
- **Challenge loops:** combining challenges with Rules features, or a solve coming from a *different
  IP* than the one challenged (VPN/proxy hopping), causes repeated challenges. Same-IP solve required.
- **No iframes / cross-domain:** Challenge Pages can't be embedded in cross-origin iframes, and one
  domain can't serve a page challenged for another.
- **Browser extensions** that spoof `User-Agent` or patch `Canvas`/`WebGL` break challenges; IE is
  unsupported.
- **`document.referer` is wrong** after a Challenge Page (it becomes your domain) — affects Google
  Analytics; inject tracking into the challenge page to capture the real referer.
- **`401` on `/cdn-cgi/challenge-platform/.../pat/...`** (Private Access Token) is **expected**, not
  a failure — Cloudflare falls back to a standard challenge.
- **CSR (Challenge Solve Rate)** = solved / issued. A *high* CSR can mean your rule is challenging
  too much **legitimate** traffic (false positives) — tune the rule. No direct "failed" metric;
  failures = issued − solved (huge, since bots abandon immediately).

## Pricing & limits
> ⚠️ Pricing changes — verify on the live pricing pages before quoting.
- **Challenges themselves are not a billed line item** — they're an action within WAF / Bots /
  rate-limiting / DDoS, whose plans determine availability and cost. Managed Challenge, JS Challenge,
  and Interactive Challenge are available on all plans (incl. Free) as WAF custom-rule actions — but
  **Rate Limiting (previous version) on Free allows only `Block`** (challenge actions start at Pro);
  **JavaScript Detections
  enforcement via custom rules requires Enterprise Bot Management**.
- **Turnstile is free** for unlimited use (separate product — see `products/turnstile.md`).
- **Key limits:** `cf_clearance` cookie ≤ **4096 bytes** · Challenge Passage default **30 min**
  (recommend 15–45) · JS-detection clearance lifespan **15 min** (re-injected before expiry) ·
  XHR cookie validation gets +1h grace, all get a few min for clock skew.

## Going deeper
- No dedicated official `cloudflare` skill ref for challenges — closest refs: `references/turnstile/`,
  `references/waf/`, `references/bot-management/` in the official skill.
- Live docs: `developers.cloudflare.com/cloudflare-challenges/` (challenge types, clearance,
  troubleshooting) · `developers.cloudflare.com/cloudflare-challenges/precursor/`. Pre-clearance + WAF: search the Cloudflare blog for "Turnstile WAF fetch".
- Related atlas products: `products/turnstile.md` (embedded widget + Siteverify), WAF/Bots refs.
