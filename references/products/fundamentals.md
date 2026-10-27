# Fundamentals — cross-product basics (accounts, auth, request flow)

> The platform-wide concepts every Cloudflare product builds on: how resources are organized
> (account → zone), how you authenticate to the API, how requests flow through Cloudflare, and the
> **Markdown for Agents** edge feature. Orientation, not a product — read this first, then the product refs.

## Contents
- Resource model (profile / account / zone)
- Account setup & IDs
- API auth (tokens, keys)
- API deprecations (live watch list)
- Request flow (reverse proxy)
- Markdown for Agents
- Gotchas
- Going deeper

## Resource model
Three nested concepts decide where a setting lives:
- **User profile** — per-person: email, language, notification/communication prefs. Not where products live.
- **Account** — an org container: holds users (members), zones, billing, and **account-level products**
  (Workers, Pages, R2, KV, D1, Security Center, bulk redirects…). Most developer-platform bindings are
  account-scoped. A user can belong to many accounts.
- **Zone** — a domain/subdomain added to Cloudflare. Holds **zone-level products** (DNS, WAF, cache rules,
  load balancing, SSL/TLS). A zone setting affects only that domain, even if other zones share the account.

- **Organization** (GA 2026-10-07; Enterprise + MSSP/Distributor only) — optional top-level container over
  many accounts. `Organization Super Administrators` get implicit access to every account in it, no per-account
  membership. Enterprise = single tier; MSSP/Distributor = nested sub-organizations. Type is fixed at creation.

Rule of thumb: building on the dev platform → you mostly work at the **account** level (account ID + token).
Configuring a website's edge behavior → **zone** level (zone ID).

## Account setup & IDs
1. Create an account / log in at `dash.cloudflare.com`. 2. (For zone products) add a domain and update its
nameservers to Cloudflare; zone becomes **active** once nameservers authenticate. 3. Grab IDs for API/Wrangler:
- **Account ID** — dashboard **Search** (`CMD/CTRL + K`) → type `Copy account ID` → select the result.
- **Zone ID** — the **domain's Overview** page → **API** section near the bottom → copy button (Account ID is here too).

## API auth
Base REST endpoint: `https://api.cloudflare.com/client/v4/`. Three credential types (use **scoped tokens**, not the global key):

| Credential | Prefix (2026 format) | Use for |
| --- | --- | --- |
| **User API Token** | `cfut_` | Scoped, tied to a user. Best for ad-hoc scripting / personal automation. |
| **Account API Token** | `cfat_` | Owned by the account, acts as a service principal. Best for CI/CD & durable integrations (survives the creator leaving). `Super Administrator` **or** the `API Token Provisioning` role creates (2026-10-01) — only with permissions ≤ the creator's own; non-admins see only tokens they created. |
| **Global API Key** | `cfk_` | Full account access tied to your user. **Avoid** — legacy, no scoping. |

Auth header (tokens): `Authorization: Bearer <TOKEN>`. Verify a token:
```sh
curl "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  --header "Authorization: Bearer <API_TOKEN>"
```
Create in dash: **My Profile → API Tokens** (user) or **Manage Account → Account API Tokens** (account-owned).
OAuth clients with the `account_api_tokens:create` scope (starting with the Cloudflare CLI) can also mint account tokens (changelog 2026-10-01).
Pick a **template** (e.g. *Edit zone DNS*) or build a custom token, grant `Edit` (full CRUDL) or `Read`,
scope it to specific accounts/zones, optionally restrict by client IP + TTL. The secret is **shown once**.

## API deprecations (live watch list)
Cloudflare publishes every REST deprecation, its enforcement date and its replacement on one page:
`developers.cloudflare.com/fundamentals/api/reference/deprecations/` — **with an RSS feed**
(`.../deprecations/index.xml`). That page is the source of truth; check it before wiring an account/IAM
integration rather than trusting this list. Two recent ones worth knowing:

- **Account Roles API deprecated (2026-07-21, no EOL date set)** → replaced by the **Permission Groups
  API**. Dead: `GET /accounts/{account_id}/roles` and `.../roles/{role_id}`. Use
  `GET /accounts/{account_id}/iam/permission_groups` (+ `/{permission_group_id}`). **The response shape
  differs** — the legacy Role returns a top-level `description` plus a `permissions` object keyed by
  resource type with `edit`/`read` flags; a PermissionGroup returns a `meta` object with `label` and
  `scopes` and does **not** return individual permissions. Integrations that **persisted legacy Role IDs
  must remap**: fetch Permission Group IDs from the new API and pass them in the **Account Members API**
  policies request shape. The new API accepts the API Token scheme (legacy Email + API Key still works
  for backwards compatibility). Note the old API only ever returned *account*-level roles; Permission
  Groups is what enumerates account, zone and resource-level grants.
- **Account name capped at 65 characters — enforced 2026-09-27.** `PUT /accounts/{account_id}` already
  enforces it; `POST /accounts` currently **silently truncates** at 120 bytes, which is how you end up
  with an account that creates fine but can never be renamed. After the date, create returns HTTP `400`.

## Request flow (Cloudflare as reverse proxy)
For a `proxied` DNS record on an active zone: client DNS query → Cloudflare returns an **anycast IP** (origin IP
stays hidden) → HTTP(S) request hits the nearest Cloudflare edge → DNS / cache / WAF / Workers run at the edge →
forwarded to your origin only if needed. This is what gives you DDoS protection, caching, SSL termination, and a
place for Workers to run. A record set to **DNS-only** (grey cloud) bypasses the proxy entirely.

## Markdown for Agents
Edge feature that converts a page's HTML to clean Markdown on the fly via content negotiation — built for AI
agents/crawlers to consume pages with far fewer tokens.
- **Request:** add header `Accept: text/markdown`. Cloudflare fetches origin HTML and returns Markdown.
  ```sh
  curl https://developers.cloudflare.com/ -H "Accept: text/markdown"
  ```
- **Response headers:** origin headers (HSTS, CSP, `Set-Cookie`, CORS, `Cache-Control`) survive; `Vary` gains
  `Accept`; `Content-Length`, `Content-Encoding`, `ETag`, `Last-Modified` are dropped (no conditional requests).
  Default `Content-Signal: ai-train=yes, search=yes, ai-input=yes` unless the origin sets `content-signal`.
- **Output shape:** YAML frontmatter (from `<meta>` tags) → body Markdown (nav/scripts/styles stripped) →
  any JSON-LD preserved in a trailing fenced `json` block.
- **Enable** per zone in **AI Crawl Control**, or via API `PATCH .../zones/{zone}/settings/content_converter`
  `{"value":"on"}`; scope to subdomains/paths with a Configuration Rule.
- **Availability:** Pro / Business / Enterprise (+ SSL for SaaS) at no cost. Cap: **6 MiB of decompressed HTML**.
- Need conversion from outside a CF zone? Use Workers AI `AI.toMarkdown()` or Browser Rendering `/markdown`.

## Gotchas
- **Token secret is shown once** — store it in a secret manager, never plaintext/committed. Leaked scannable
  tokens (`cfut_`/`cfat_`/`cfk_`) are detected by GitHub Secret Scanning — in **public** repos Cloudflare
  auto-revokes them; in **private** repos GitHub only notifies you, so you must rotate them yourself.
- Some products don't yet support **account-owned tokens** — check the compatibility matrix before wiring CI/CD.
- **More `499`s on HTTP/3 since 2026-10-09** — client-cancelled HTTP/3 requests are now stopped sooner and
  recorded as `499` (not a rise in failures). Exclude `499` from server-side error rates.
- Zone-level settings never cascade to sibling zones; account-level products can affect all zones in the account.
- Markdown for Agents only converts **HTML** and is limited to 6 MiB (6,291,456 bytes) of *decompressed* HTML — not the compressed size.
- Old (pre-2026) unprefixed tokens still work — only new/rolled tokens get the scannable prefix format.

## Going deeper
- No dedicated official `cloudflare` skill ref for fundamentals — this file is the primary orientation.
- Full REST API: `developers.cloudflare.com/api/` · token permissions/templates: `fundamentals/api/reference/`.
- **Deprecations feed** (subscribe rather than snapshot): `fundamentals/api/reference/deprecations/index.xml`.
- Concepts (accounts/zones, IP addresses, traffic flow): `developers.cloudflare.com/fundamentals/concepts/`.
- **Audit Logs v2** (account change history, ~95% product coverage) now also covers **organization**
  scope — API `GET /organizations/{organization_id}/logs/audit` + dashboard: `fundamentals/account/account-security/audit-logs/`.
- Markdown for Agents detail: `developers.cloudflare.com/fundamentals/reference/markdown-for-agents/`.
- For Worker/binding config (`wrangler.jsonc`), see the individual product refs — fundamentals has no bindings.
