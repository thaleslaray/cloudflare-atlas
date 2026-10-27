# Zaraz — third-party tags loaded on the edge (server-side tag manager)

> Offload third-party scripts (analytics, ad pixels, chatbots, marketing tools) from the browser to
> Cloudflare's edge. Like GTM, but tools run **server-side** with near-zero client-side JS overhead,
> plus built-in consent management. Dashboard-configured, available on all plans.

## Contents
- When to use (and when not)
- Setup & config (dashboard, not wrangler)
- Web API (`zaraz.*`)
- Triggers & consent
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- A website needs **3rd-party tags** (GA4, Facebook/Meta pixel, Google Ads, TikTok, chatbots, marketing
  automation) but you care about **performance** — scripts run on the edge, not in the user's browser.
- You need **privacy/consent** controls: GDPR/CCPA consent modal, IP anonymization, control over what
  data reaches each third party.
- Non-technical teams should manage tools via a dashboard (GTM-style), not code deploys.
- **Not** for: server-to-server tracking, custom backend logic, auth flows, binary/real-time data →
  use Workers directly. If Zaraz's tool library doesn't cover your tool, build a Managed Component or
  use a Worker.

## Setup & config (dashboard, not wrangler)
Zaraz is **not** wired via `wrangler.jsonc` — there is no Worker binding. Configure per-domain in the
Cloudflare dashboard: **Domain → Zaraz → Start setup**, then add tools, triggers, and consent purposes,
and **Publish**. A single edge endpoint loads all configured tools in one HTTP request.

Optional Worker hooks (configured in Zaraz settings, not a binding):
- **Context Enrichers** — a Worker that mutates the event context before tools fire (e.g. add
  `request.cf?.region`). Returns the modified JSON body.
- **Worker Variables** — compute server-side values, referenced in triggers as `{{worker.name}}`.

## Web API (`zaraz.*`)
Available anywhere inside `<body>`. `track()` and `ecommerce()` are **`async` functions — you can
`await` them** if you need to know they completed before running other code.
```javascript
zaraz.track('button_click', { button_id: 'cta' });   // custom event
zaraz.set('userId', 'u_123');                         // signature: set(key, value, [options])
zaraz.set('product_name', 't-shirt', { scope: 'page' });  // scope: page | session | persist
zaraz.ecommerce('Order Completed', {                  // maps to GA4 / Facebook CAPI etc.
  order_id: 'ORD-789', total: 149.98, currency: 'USD',
  products: [{ product_id: 'SKU123', quantity: 2, price: 49.99 }]
});
```
`zaraz.ecommerce()` only works after **E-commerce tracking** is toggled on in Zaraz Settings.
The 18 supported e-commerce events: `Product List Viewed` · `Products Searched` · `Product Clicked` ·
`Product Added` · `Product Added to Wishlist` · `Product Removed` · `Product Viewed` · `Cart Viewed` ·
`Checkout Started` · `Checkout Step Viewed` · `Checkout Step Completed` · `Payment Info Entered` ·
`Order Completed` · `Order Updated` · `Order Refunded` · `Order Cancelled` · `Clicked Promotion` ·
`Viewed Promotion`.

## Triggers & consent
- **Triggers** (dashboard) decide *when* a tool fires. The six rule types, verbatim: `Match rule`
  (variable + operation + string — this is how you match `Pageview` or a `zaraz.track()` event name),
  `Click listener` (CSS selector or XPath; include the `#`/`.` symbol or it silently never fires),
  `Element Visibility`, `Scroll depth`, `Form submission`, `Timer`. Reference system values like
  `{{system.page.url}}`, `{{system.device.user-agent}}` (note the hyphen).
- **Consent** — define purposes (analytics, marketing…), map tools to them, set "Do not load until
  consent granted":
```javascript
zaraz.consent.set({ analytics: true, marketing: false });  // set() takes {purposeId: boolean}
zaraz.consent.setAll(true);                            // setAll() takes a BOOLEAN, not an object
zaraz.consent.getAll();                                // { purposeId: boolean }
zaraz.consent.modal = true;                            // show consent modal
document.addEventListener('zarazConsentChoicesUpdated', () => { /* react */ });
document.addEventListener('zarazConsentAPIReady', () => { /* API safe to call */ });
```
A new tool gets **no purpose** assigned by default, so it skips consent — assign one explicitly.

## Gotchas
- **Events not firing:** tool must be enabled (green dot), trigger conditions met, **and** consent
  granted for its purpose. Debug mode is a **cookie**, not a flag: copy your **Debug Key** from
  Settings, then run `zaraz.debug("YOUR_DEBUG_KEY")` in the console — a debugger pop-up appears.
  `zaraz.debug()` with no argument removes the cookie and exits.
- **SPA:** there is **no history/route-change rule type** among the six. But Zaraz has built-in
  **Single Page Application support** (Settings toggle): with it on, the `pageview` trigger fires
  "every time the URL changes on a single page application" (virtual page views). For advanced cases
  call `zaraz.spaPageview()` manually. Custom HTML actions re-inject on every SPA pageview — add the
  **Ignore SPA** field to inject once.
- **`set` scope defaults to `persist`** (saved across sessions in `localStorage`), not per-page. Pass
  `{scope: 'page'}` or `{scope: 'session'}` to narrow it. To clear a key, set it to `undefined`
  (not `null`) — it is removed from all scopes.
- **Tool IDs:** GA4 = `G-XXXXXXXXXX`, Facebook = numeric Pixel ID only, Google Ads = `AW-XXX/LABEL`.
- **Performance:** many tools degrade page load; keep event payloads small (no published cap).
- Migrating from GTM: `dataLayer.push` → `zaraz.track`/`zaraz.ecommerce`; `{{Page URL}}` →
  `{{system.page.url}}`.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/zaraz/pricing-info/`) before quoting.

**Cost driver:** billed per **Zaraz Event** (a page view, a `zaraz.track` call, etc.), per account.
- Free tier: **1,000,000 Zaraz Events / month** per account, all features and tools included.
- Zaraz Paid: **$5 / month per additional 1,000,000 Events**.
- Free plan exceeding 1M without enabling Paid → **Zaraz disabled until next billing cycle** (email
  warnings at 50/80/90%). All tiers get every feature.

**Key limits:** none published. A former line here quoted an event-size cap, a consent-purpose count
and an API rate — all three were removed 2026-08-25 as unsourceable in the live docs. Zaraz documents
pricing tiers and event volumes, not per-request limits; measure rather than assume.

## Going deeper
- Covered by the official `cloudflare` skill (`references/zaraz/`) — use it for the full Web API,
  dashboard configuration, patterns (SPA, e-commerce, Worker integration), and troubleshooting.
- Custom tools → Managed Components (`zaraz/advanced/load-custom-managed-component/`).
- "Why server-side tagging / pricing rationale" → the live blog (blog.cloudflare.com), search "Zaraz pricing".
