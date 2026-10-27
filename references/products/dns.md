# DNS — authoritative DNS + record management

> Fast, resilient, DDoS-protected **authoritative DNS** for your domain. Manage records (A, CNAME,
> MX, TXT…), toggle Cloudflare proxying per record, and use CNAME flattening to put a CNAME at the
> zone apex. Available on all plans.

## Contents
- When to use (and when not)
- Onboarding & nameservers
- DNS record types
- Proxy status (proxied vs DNS-only)
- CNAME flattening
- API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You need authoritative DNS: map names to IPs/services, set MX/TXT for email, run a domain.
- You want to **proxy** web traffic through Cloudflare (caching, WAF, DDoS) — DNS is the on/off switch.
- You need a CNAME at the apex (`example.com`) — **CNAME flattening** makes this work (e.g. Pages root domain).
- Relation to **Registrar**: Registrar sells/renews the *domain*; DNS *resolves* it. Buy via Registrar
  and your zone auto-uses Cloudflare nameservers. Bring a domain from elsewhere → add it to DNS, then
  point the registrar's nameservers at Cloudflare. DNS works regardless of who the registrar is.
- **Not** for: a private recursive resolver for browsing (→ 1.1.1.1) or internal-only zones unless
  Enterprise (→ Internal DNS, Enterprise-only, GA).

## Onboarding & nameservers
- **Full (primary) setup** (most common): add domain → import/review records → update nameservers at
  your registrar to the two assigned `*.ns.cloudflare.com` names. Activation can take up to 24h; until
  then records stay **DNS-only** and protection is *pending*.
- Review records *before* switching nameservers — a wrong/missing record can make the domain unreachable.
- Also supports **secondary DNS** (Cloudflare as secondary via zone transfer) and **partial (CNAME) setup**.
- Enterprise + Foundation DNS → advanced nameservers, account-unique DNSSEC keys, custom SOA/NS TTL.

## DNS record types
- **IP resolution (proxiable):** `A`, `AAAA` (IPv4/IPv6), `CNAME` (alias to another name). At least one
  is required per zone. **Only these three can be proxied.**
- **Email:** `MX`, plus `TXT`-based `SPF` / `DKIM` / `DMARC` (always DNS-only).
- **Specialized:** `TXT`, `CAA`, `SRV`, `SVCB`/`HTTPS`, `PTR`, `NS`, `SOA`, `DS`/`DNSKEY` (DNSSEC).
- Wildcards (`*.example.com`) supported. Name labels ≤63 chars, FQDN ≤253 chars.
- Enable **DNSSEC** (cryptographic signing) from the dashboard; add the `DS` record at your registrar.

## Proxy status (proxied vs DNS-only)
- **Proxied** ("orange cloud"): DNS answers with Cloudflare anycast IPs; HTTP/HTTPS routes *through*
  Cloudflare → DDoS protection, caching, WAF, redirect rules, HTTP analytics. Origin IP hidden.
  TTL is forced to **Auto = 300s** (not editable).
- **DNS-only** ("grey cloud"): answers with your real origin IP; Cloudflare does not proxy. Origin IP
  is exposed; only DNS analytics. Use for records that must resolve to the origin directly (e.g. SSH,
  mail server, domain-verification CNAMEs).
- Proxying is **on by default** when onboarding via the dashboard. Cloudflare *recommends* proxying all
  web-serving A/AAAA/CNAME; do **not** proxy verification or non-HTTP records.
- Mixed names: if any A/AAAA on a name is proxied, **all** records on that name are treated as proxied.
  A proxied hostname anywhere in a CNAME chain makes the whole chain proxied.

## CNAME flattening
- Cloudflare follows the CNAME chain, finds the final IP, and returns an **A/AAAA** instead of the CNAME
  — faster resolution and a CNAME at the **zone apex** (which raw DNS forbids). Powers Pages root domains.
- Proxied CNAMEs are flattened **by default**. Paid plans can opt to flatten **all** CNAMEs (apex only is default).
- **Dangling target gotcha:** if the final target has no A/AAAA, flattening returns NODATA (empty) — looks
  like the record "isn't propagating." Ensure targets resolve.

## API / access patterns
Endpoint: `https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records`. Token needs **`DNS Write`**.
```bash
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  --request POST \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --json '{ "type":"A", "name":"www.example.com", "content":"192.0.2.1", "ttl":3600, "proxied":false }'
```
- `proxied: true|false` is the proxy toggle. `ttl: 1` means **Auto** (and is forced for proxied records).
- **Batch** (`.../dns_records/batch`): DELETES, PATCHES, PUTS, POSTS in one request — executed in *that
  order*, in a single DB transaction. Note: propagation is **not atomic** (KV is per-record).
- **Import/Export**: standard **BIND zone files** via dashboard/API (use FQDNs with trailing dot for
  CNAME/MX/NS/PTR/SRV). Also manageable via Terraform.
- For exact field schemas per record type, see the API docs (record-type-specific request body).

## Gotchas
- **CNAME cross-account banned:** a proxied CNAME pointing into a *different* Cloudflare account →
  **Error 1014**. Keep proxied CNAME chains within one account.
- **Can't proxy some CNAMEs:** Cloudflare blocks proxying records tied to other CDNs or DKIM, to prevent
  misconfig/connectivity errors — leave those DNS-only.
- **Other-record-type queries don't follow a proxied CNAME:** a TXT query on a name that's a proxied
  CNAME won't return the target's TXT.
- **`flatten all CNAMEs` breaks third-party verification** that reads the CNAME itself — keep apex-only.
- **NS delegation limit:** ≤10 NS records per delegation name (RFC best practice is ≤7).
- Record wire format ≤4,096 bytes; same-name+type combined content ≤8,192 chars.

## Pricing & limits
> ⚠️ Verify on the live pricing page (`www.cloudflare.com/plans` / `developers.cloudflare.com/dns/`)
> before quoting.

**Cost drivers:** Authoritative DNS and record management are **included free on all plans** — there is
no per-query or per-record charge. Paid value is plan-based (Pro/Business/Enterprise) and add-ons:
**Foundation DNS** (Enterprise), advanced nameservers, DNSSEC keys. No public per-unit DNS metering.

**Key limits (records per zone):**
- Free zones created **before 2024-09-01**: 1,000 · Free created **on/after**: **200**
- Pro / Business: **3,500** · Enterprise: per-**account** quota instead (default **1,000,000** records;
  public and internal zones counted separately).
- Since 2026-10-06 the dashboard DNS records page **warns at 85%** of the applicable quota (zone's own,
  or account-level usage across all zones).
- **Batch** request max records: Free 200 · Pro/Business/Enterprise 3,500.
- **TTL:** proxied = Auto (300s, fixed). DNS-only = **30s** (Enterprise) / **60s** (non-Ent) up to **1 day**.
- Secondary DNS: ≤30 linked peers per zone.

## Going deeper
- No dedicated official `cloudflare` skill ref for DNS — this file is the primary reference.
- Full record-type fields & examples: `docs-oficiais/pages/dns/manage-dns-records/reference/dns-record-types/`.
- Proxy behavior/limits: `.../proxy-status/` · CNAME flattening setup: `.../cname-flattening/`.
- Exact REST API: Cloudflare API docs → `resources/dns/subresources/records` (create/batch/import/export).
- Related: **Registrar** (domain ownership), **DNSSEC**, **Foundation DNS** (Enterprise), **1.1.1.1** (resolver).
