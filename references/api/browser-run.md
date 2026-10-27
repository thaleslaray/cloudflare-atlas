# API reference — browser-run

> Exact REST endpoints for **browser-run**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 30 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `POST /accounts/{account_id}/browser-rendering/accessibilityTree` — Get accessibility tree page  · required: account_id  · body: url:string
- `POST /accounts/{account_id}/browser-rendering/content` — Get HTML content.  · required: account_id  · body: url:string
- `POST /accounts/{account_id}/browser-rendering/crawl` — Crawl websites.  · required: account_id  · body: url:string
- `GET /accounts/{account_id}/browser-rendering/crawl/{job_id}` — Get crawl result.  · required: account_id, job_id
- `DELETE /accounts/{account_id}/browser-rendering/crawl/{job_id}` — Cancel a crawl job.  · required: account_id, job_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser` — Acquire and connect to browser session.  · required: account_id
- `POST /accounts/{account_id}/browser-rendering/devtools/browser` — Get a browser session ID.  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}` — Connect to browser session.  · required: account_id, session_id
- `DELETE /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}` — Close browser session.  · required: account_id, session_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json` — List targets.  · required: account_id, session_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json/activate/{target_id}` — Activate a browser target.  · required: session_id, account_id, target_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json/close/{target_id}` — Close a browser target.  · required: session_id, account_id, target_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json/list` — List targets.  · required: account_id, session_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json/list/{target_id}` — Get a target by ID.  · required: account_id, session_id, target_id
- `PUT /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json/new` — Open a new browser tab.  · required: account_id, session_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json/protocol` — Get Chrome DevTools Protocol schema.  · required: account_id, session_id
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/json/version` — Get browser version metadata.  · required: account_id, session_id
- `POST /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/live_view` — Mint live view URLs for a browser session  · required: account_id, session_id  · body: (no required fields)
- `GET /accounts/{account_id}/browser-rendering/devtools/browser/{session_id}/page/{target_id}` — Connect to a specific Chrome DevTools page.  · required: account_id, session_id, target_id
- `GET /accounts/{account_id}/browser-rendering/devtools/session` — List sessions.  · required: account_id
- `GET /accounts/{account_id}/browser-rendering/devtools/session/{session_id}` — Get session details.  · required: account_id, session_id
- `POST /accounts/{account_id}/browser-rendering/json` — Get json.  · required: account_id  · body: url:string
- `POST /accounts/{account_id}/browser-rendering/links` — Get Links.  · required: account_id  · body: url:string
- `POST /accounts/{account_id}/browser-rendering/markdown` — Get markdown.  · required: account_id  · body: url:string
- `POST /accounts/{account_id}/browser-rendering/pdf` — Get PDF.  · required: account_id  · body: url:string
- `GET /accounts/{account_id}/browser-rendering/recording/{session_id}` — Get recording data.  · required: account_id, session_id
- `GET /accounts/{account_id}/browser-rendering/recording/{session_id}/network` — Get network recording data.  · required: account_id, session_id, target
- `POST /accounts/{account_id}/browser-rendering/scrape` — Scrape elements.  · required: account_id  · body: url:string
- `POST /accounts/{account_id}/browser-rendering/screenshot` — Get screenshot.  · required: account_id  · body: url:string
- `POST /accounts/{account_id}/browser-rendering/snapshot` — Get HTML content and screenshot.  · required: account_id  · body: url:string
