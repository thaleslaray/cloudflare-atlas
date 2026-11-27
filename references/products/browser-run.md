# Browser Run — headless Chrome on Workers (automation, screenshots, scraping, PDFs)

> Programmatically control headless Chrome on Cloudflare's edge for browser automation, web
> scraping, testing, and content generation (screenshots, PDFs, markdown). **Formerly "Browser
> Rendering"** — same product, renamed; the old name still appears in API paths and permissions.

## Contents
- Name: Browser Run vs Browser Rendering
- When to use (and when not)
- Two integration models
- Binding & config
- API patterns
- Concepts
- Gotchas
- Pricing & limits
- Going deeper

## Name: Browser Run vs Browser Rendering
**Same product.** "Browser Run" is the current name; "Browser Rendering" is the old name (and what
the *official `cloudflare` skill's* `references/browser-rendering/` covers). The rename is cosmetic
but the legacy name persists in: the REST path (`/browser-rendering/...`; the live Quick Actions pages now
show `/browser-run/...`) and the SDK namespace (`client.browserRendering`). The API token permission is now
`Browser Run - Edit`. Treat docs/skill content
labeled "browser-rendering" as authoritative for this product.

## When to use
- Render dynamic/JS-heavy pages a plain `fetch()` can't: SPAs, client-rendered content.
- **Screenshots** of pages/HTML; **PDF generation** (invoices, reports, OG images).
- **Scraping / data extraction** — including AI-driven structured extraction and site crawling.
- **Browser testing & automation** — drive Puppeteer/Playwright scripts at the edge.
- **AI agents that browse** — LLMs drive a browser via Playwright MCP / Stagehand / CDP+MCP.
- **Not** for: simple static fetches (just use `fetch()`); long-running desktop browser sessions
  (sessions idle out — see limits); plain HTML→PDF where a JS lib in-Worker suffices.

## Two integration models
1. **Quick Actions** — stateless, single-shot HTTP/binding calls. No script to deploy. Endpoints:
   `screenshot`, `pdf`, `content` (HTML), `markdown`, `accessibilityTree` (a11y tree),
   `links`, `scrape` (HTML elements), `json` (AI structured extraction via prompt; uses Workers AI),
   `snapshot` (several of these formats in ONE call, 2026-11-19 — see below),
   `crawl` (async multi-page; per-URL `outcome` e.g. `robots_disallowed`/`timeout`/`page_error`, job-level `robots[]` state
   for ≤50 origins — `browser-run/quick-actions/crawl-endpoint/`). Billed for **browser hours only**. Cloudflare manages session lifecycle.
2. **Browser Sessions** — full scripted browser control via **Puppeteer**, **Playwright**, **CDP**
   (WebSocket, drive from anywhere — local/CI/external), **Stagehand** (AI finds elements by
   intent, not selectors), or **Custom scripts** (`/script`, 2026-11-20 — submit code over HTTP, below).
   Billed for **browser hours + concurrent browsers**.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "browser": { "binding": "MYBROWSER" },
  "compatibility_flags": ["nodejs_compat"] // required for Browser Sessions (Puppeteer/Playwright)
}
```
- **Quick Actions via binding:** `env.MYBROWSER.quickAction("screenshot", { url })` →
  requires `compatibility_date` ≥ `2026-03-24`.
- **Quick Actions via REST:** `POST .../accounts/<id>/browser-rendering/screenshot` with a
  `Browser Run - Edit` API token. No Worker needed.
- **Browser Sessions:** `npm i -D @cloudflare/puppeteer`, then
  `const browser = await puppeteer.launch(env.MYBROWSER)`.

## API patterns
```js
// Quick Action (REST) — screenshot, no code deploy
curl -X POST '.../accounts/<id>/browser-rendering/screenshot' \
  -H 'Authorization: Bearer <token>' -d '{"url":"https://example.com"}' --output shot.png

// Browser Session (Puppeteer in a Worker)
import puppeteer from "@cloudflare/puppeteer";
const browser = await puppeteer.launch(env.MYBROWSER);
const page = await browser.newPage();
await page.goto("https://example.com");
const img = await page.screenshot();
await browser.close(); // ALWAYS — wrap in try/finally
```
- Playwright: Cloudflare ships its own fork; same API, connects to the binding.
- Pairs with: **KV/R2** (cache screenshots/PDFs), **Durable Objects** (persist a long-lived
  browser, route users to a specific instance), **Queues** (async jobs), **Agents/Workers AI**.

### `/snapshot` — many formats, one request (2026-11-19)
`POST .../browser-run/snapshot` (or `env.BROWSER.quickAction("snapshot", {...})`), body needs `url` **or** `html`. `formats`
(default `["content","screenshot"]`; also `markdown`, `accessibilityTree`, `pdf`, `links`, `scrape`, `json`) must name **≥2 distinct
formats** (else use the single endpoint). Each format fills `result.<name>` and reuses that endpoint's options (`pdfOptions`,
`screenshotOptions`, `elements` — **required** for `scrape`, `prompt` — **required** for `json`, plus `response_format`/`custom_ai`).
Gotchas: **all-or-nothing** (one failed format fails the request); formats are captured in a fixed order, not array order, and a live
page can change between captures; `json` incurs **Workers AI** usage and one `actionTimeout` (default 60 s, max 120 s) covers
navigation + captures + retries + the AI call. Billing is Quick Actions browser hours.

### `/script` — run your own code in one HTTP call (2026-11-20)
Docs list it under **Custom scripts** (`browser-run/script/`), **not** Quick Actions: it is a Browser Session, so billed browser
hours **+ concurrent browsers**, and it does **not** close the session afterwards (you pay until `keep_alive` idle timeout).
- `POST .../browser-run/script` body `{ code, library?, timeout? }` — `code` = a JS **function expression**; `library` `"playwright"` |
  `"puppeteer"` | omitted = **CDP** (`async ({ send, on, off }) => …`; Playwright/Puppeteer get `{ page, browser, … }`). Runs in an
  isolated Worker — no deploy. Query: `keep_alive` 10000–1200000 ms (default 60000), `lab`, `recording`, `browser=kitesurf`.
- Response carries `cf-browser-session-id` + `cf-browser-target-id`; continue with `POST .../script/<sessionId>` (body adds
  `targetId`; no query params, session keeps its launch options). Binding: `env.BROWSER.script(code, { library, timeout, keepAlive, sessionId, targetId })`
  returns a `Response`; **not supported in local `wrangler dev`** (use `--remote` or `"remote": true`).
- **Close it yourself**: `browser.close()` in the last script or `DELETE .../devtools/browser/<sessionId>`; disconnecting does not close.
- Limits: body **10 MiB**; `timeout` default **60 s**, max **120 s** (excludes acquisition); same rate/concurrency limits as
  `POST /devtools/browser`. Errors: `408` timeout, `422` compile/runtime error, `410` session closed, `404` bad session/`targetId`.
  `timeout` below the library's 30 s default → `408`; above it → library error `422`. Kitesurf: CDP only, `library`/`keep_alive`/
  `recording`/`lab` → `400`, no reusable session. Concurrent runs on one page interfere — create a separate target per run.
- A returned JSON value → `{ success: true, result }`; non-2xx `Response` is rewritten to the error format.

## Kitesurf — the agent-first browser (beta, 2026-08-06)
A **second browser engine** on the same Browser Run endpoints — stateless, running entirely on
Workers, built for AI agents rather than for full web-app fidelity.
- **3–7× less CPU and memory than Chromium** on common agentic tasks (screenshots, HTML extraction)
  → more concurrent sessions, better behaviour under bursty AI-driven load.
- **Free while in beta**, behind per-account limits.
- **Opt in per request** — existing clients work unchanged; just add `browser=kitesurf` to any CDP or
  Quick Action endpoint:
  ```sh
  curl -X POST 'https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/browser-run/screenshot?browser=kitesurf' \
    -H 'Authorization: Bearer <API_TOKEN>' -H 'Content-Type: application/json' \
    -d '{"url":"https://example.com"}' --output screenshot.png
  ```
- Also via CDP (`wss://.../browser-run/devtools/browser?browser=kitesurf`) and MCP clients; Kitesurf
  does **not** accept `keep_alive`. Can't yet: video/WebGL, bot-challenge TLS fingerprints, long-running
  authenticated stateful sessions → use Chromium. Try without code: the playground at `kitesurf.dev`.
- **WebMCP (2026-09-28):** pages register tools via `document.modelContext`; works on Kitesurf and on
  Chrome **Lab** sessions (`lab=true` / `wrangler browser create --lab`; experimental, not for
  production). Agents: Chrome DevTools MCP with `--category-experimental-webmcp`
  (`list_webmcp_tools`, `execute_webmcp_tool`); CDP clients: the `WebMCP` domain. Docs: `features/webmcp/`.
- **Choose deliberately:** Kitesurf is not Chromium. For agent scraping/screenshots it is the cheaper,
  more scalable default; for pixel-faithful rendering of heavy web apps, stay on Chromium.
- **Open source (2026-11-12):** Kitesurf is on GitHub (Apache 2.0; "still experimental and under heavy development"
  per the post) — run locally with Wrangler (`pnpm run dev`) or deploy your own instance. It has **no built-in auth**
  (protect with Cloudflare Access or similar) and needs **Dynamic Workers → Workers Paid plan**. Via the binding:
  `quickAction("screenshot", { url, browser: "kitesurf" })` (any other engine name fails validation).
- Docs: `developers.cloudflare.com/browser-run/kitesurf/`.

## Concepts
- **Browser hours** — wall-clock time a browser is alive; shared across all methods (Quick Actions
  and Sessions both draw from it).
- **Concurrent browsers** — only Browser Sessions count; billed as monthly avg of daily peaks.
- **Idle timeout** — a session closes after **60s of inactivity** by default; extend with
  `keep_alive` (ms, **up to 20 min**): `puppeteer.launch(env.MYBROWSER, { keep_alive: 1200000 })`. This
  is an *inactivity* timeout, not a max lifetime — keep sending commands to stay alive longer.
- **Reuse sessions** — `browser.disconnect()` (not `.close()`) keeps the browser warm to reconnect
  next request (skips cold start); or persist inside a Durable Object for stateful routing.
- **Concurrent connections (2026-09-29)** — one session now accepts **multiple** clients at once (was
  one at a time); each `puppeteer.connect(env.MYBROWSER, sessionId)` is its own CDP connection — give
  each request its own `createBrowserContext()`, close the context, then `disconnect()`. Needs
  `@cloudflare/puppeteer` ≥ 1.1.0 / `@cloudflare/playwright` ≥ 1.3.0 (older = single-connection).

## Gotchas
- **Always `browser.close()`** in a `try/finally`. A leaked session keeps consuming browser time
  until idle timeout — the #1 cause of surprise usage / hitting the free 10-min/day cap.
- **`429 Too many requests`** — respect `Retry-After`; rate limits are per-second (Paid) or
  per-10s (Free). Distinct from `429 Browser time limit exceeded for today` (daily cap on Free).
- **Free vs Paid mismatch after upgrade** — if still capped at 10 min/day after upgrading,
  **redeploy** the Worker so usage re-associates with the new plan.
- **Session isolation** — when reusing sessions, use incognito browser contexts
  (`createBrowserContext`) to isolate cookies/cache between tasks.
- Audit closures via `puppeteer.history()` — sessions closing as `BrowserIdle` (vs `NormalClosure`)
  mean you forgot to close them. Sessions also close on Browser Run platform releases.
- **Chrome 152** (2026-10-30) is the default. Quick Actions' default User-Agent now says `Chrome/152.0.0.0` (was 119) — don't
  allowlist on it (changes with Chrome); override via `userAgent`. `/links` returns absolute URLs.
- **Local dev (2026-11-13):** under `npx wrangler dev`, Puppeteer, Playwright, CDP and `.quickAction()` run
  against **Chrome on your machine** (before, `.quickAction()` failed locally with `The RPC receiver does not
  implement the method "quickAction"`). Two exceptions: `json` returns **placeholder data** shaped like your
  `response_format.json_schema` (Workers AI isn't local; `const`/`enum`/`default` values are used, else empty
  values) and `browser: "kitesurf"` **throws**. For real `json` results or Kitesurf set `"remote": true` on the
  binding. `X_BROWSER_HEADFUL` env var opens a visible local Chrome (experimental).

## Pricing & limits
> ⚠️ Pricing/limits change — verify live (`developers.cloudflare.com/browser-run/pricing/` &
> `/limits/`) before quoting. **Status: GA, on Free and Paid plans.**

**Cost drivers (as of 2026-06):**
- Browser hours: **Free** 10 min/day · **Paid** 10 hrs/month included, then **$0.09/hr**.
- Concurrent browsers (Sessions only): **Free** 3 · **Paid** 10 included (monthly-averaged), then
  **$2.00/browser**.
- Failed Quick Actions (e.g. `waitForTimeout`) are **not** billed. Each Quick Actions response
  returns `X-Browser-Ms-Used` (time used, ms); `/script` responses return it too, **cumulative** since the session began. Kitesurf
  runs (incl. `/script?browser=kitesurf`) follow Kitesurf pricing, not this table. `/script` and `/snapshot` have no limits row of their own
  (checked 2026-11-27: `/script` shares `POST /devtools/browser` limits, `429` on rate/browser-time/concurrency).

**Key limits (limits page, updated 2026-09-26):** new instances **Free** 1/20s · **Paid** 3/s
(default, raisable). Concurrent browsers/account **Free** 3 · **Paid** default 200 (request more).
Quick Actions requests **Free** 1/10s · **Paid** 30/s. Browser idle timeout 60s (→20 min via
`keep_alive`). `/crawl` on Free:
5 jobs/day, 100 pages/crawl. Verify on the limits page.

## Going deeper
- Official `cloudflare` skill covers this as **`references/browser-rendering/`** — use it for
  full Puppeteer/Playwright/CDP API and patterns (note the legacy name).
- Quick Actions endpoint specs, Stagehand, Playwright MCP, session recording / live view /
  human-in-the-loop → `developers.cloudflare.com/browser-run/`.
- Exact REST API: `references/api/browser-run.md` — exact endpoints sliced from the OpenAPI spec (verify shapes live).
