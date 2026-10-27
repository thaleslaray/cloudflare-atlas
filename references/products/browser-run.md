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
but the legacy name persists in: the REST path (`/browser-rendering/...`; newer pages also show
`/browser-run/...`), the API token permission (`Browser Rendering - Edit`). Treat docs/skill content
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
   `screenshot`, `pdf`, `content` (HTML), `markdown`, `snapshot`, `accessibilityTree` (a11y tree),
   `links`, `scrape` (HTML elements), `json` (AI structured extraction via prompt),
   `crawl` (async multi-page). Billed for
   **browser hours only**. Cloudflare manages session lifecycle.
2. **Browser Sessions** — full scripted browser control via **Puppeteer**, **Playwright**, **CDP**
   (WebSocket, drive from anywhere — local/CI/external), or **Stagehand** (AI finds elements by
   intent, not selectors). Billed for **browser hours + concurrent browsers**.

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
  `Browser Rendering - Edit` API token. No Worker needed.
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
- Docs: `developers.cloudflare.com/browser-run/kitesurf/`.

## Concepts
- **Browser hours** — wall-clock time a browser is alive; shared across all methods (Quick Actions
  and Sessions both draw from it).
- **Concurrent browsers** — only Browser Sessions count; billed as monthly avg of daily peaks.
- **Idle timeout** — a session closes after **60s of inactivity** by default; extend with
  `keep_alive` (ms, up to 10 min): `puppeteer.launch(env.MYBROWSER, { keep_alive: 600000 })`. This
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
- Local dev: `wrangler dev --remote` (or `remote: true` binding) to hit a real headless browser.

## Pricing & limits
> ⚠️ Pricing/limits change — verify live (`developers.cloudflare.com/browser-run/pricing/` &
> `/limits/`) before quoting. **Status: GA, on Free and Paid plans.**

**Cost drivers (as of 2026-06):**
- Browser hours: **Free** 10 min/day · **Paid** 10 hrs/month included, then **$0.09/hr**.
- Concurrent browsers (Sessions only): **Free** 3 · **Paid** 10 included (monthly-averaged), then
  **$2.00/browser**.
- Failed Quick Actions (e.g. `waitForTimeout`) are **not** billed. Each Quick Actions response
  returns `X-Browser-Ms-Used` (time used, ms).

**Key limits (limits page, updated 2026-09-26):** new instances **Free** 1/20s · **Paid** 3/s
(default, raisable). Concurrent browsers/account **Free** 3 · **Paid** default 200 (request more).
Quick Actions requests **Free** 1/10s · **Paid** 30/s. Browser idle timeout 60s (→10 min via
`keep_alive`). `/crawl` on Free:
5 jobs/day, 100 pages/crawl. Verify on the limits page.

## Going deeper
- Official `cloudflare` skill covers this as **`references/browser-rendering/`** — use it for
  full Puppeteer/Playwright/CDP API and patterns (note the legacy name).
- Quick Actions endpoint specs, Stagehand, Playwright MCP, session recording / live view /
  human-in-the-loop → `developers.cloudflare.com/browser-run/`.
- Exact REST API: `references/api/browser-run.md` — exact endpoints sliced from the OpenAPI spec (verify shapes live).
