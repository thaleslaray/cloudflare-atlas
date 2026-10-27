# China Network — serve visitors inside mainland China

> Run selected Cloudflare performance/security products on data centers **inside Mainland China**
> (operated by partner **JD Cloud**), so users in China get low latency instead of crossing China's
> network boundary. Enterprise-only add-on. **Requires a valid ICP filing/license** per apex domain.

## Contents
- When to use (and when not)
- How it works
- Setup / onboarding
- DNS (in-China nameservers)
- Available products & notable exclusions
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You have real traffic from **Mainland China** and the cross-border latency/reliability hit (the
  "Great Firewall" boundary) is hurting performance. Serving from outside China is slow and flaky.
- You want one dashboard/config for both global and in-China delivery, plus WAF/DDoS/bot management
  in China.
- **Not** for: low China traffic (the ICP + Enterprise + content-vetting overhead isn't worth it);
  any zone without an ICP filing/license (legally required — no exceptions). For dynamic content,
  Cloudflare One, or extending R2/global services into China, see **Global Acceleration** (add-on).

## How it works
- A separate paid subscription on top of an **Enterprise** plan. China PoPs are run by JD Cloud,
  which holds the MIIT licenses Cloudflare (a US company) lacks.
- Same Cloudflare account, dashboard, and configurations as the global network.
- JD Cloud must **content-vet every domain** before it can be onboarded — they can approve or reject
  based on content. All in-China traffic is monitored by local authorities and must comply with
  local regulations.
- **IPv6 is mandatory** in Mainland China and is auto-enabled on your domains; you cannot disable it.

## Setup / onboarding
1. Have an Enterprise plan; add the China Network package; sign the **China Service Supplemental Terms**
   (contact your sales team).
2. Obtain an **ICP filing or license** for each apex domain (see below). Present valid ICP and display
   the ICP number in each site's footer.
3. Provide JD Cloud the content-vetting info (company/domain name, ICP number, content description,
   signed self-attestation letter).
4. Add domains to Cloudflare. **First-time zone enablement: ~24–48h.** After that you toggle China
   Network on/off per zone in the dashboard.

**ICP (Internet Content Provider)** — government permission to operate a site reachable in China,
required whether hosted in China or merely served there via CDN:
- **ICP filing** ("Bei'An") — non-commercial/informational sites.
- **ICP license** ("ICP Zheng") — commercial/transactional sites; requires a filing first.
- **Processing time: four to eight weeks**, depending on site type and the province where the
  company is registered (docs give one range, not a per-type split).
- Neither Cloudflare nor JD Cloud files it for you (they can refer ICP partners). Apply via your
  hosting/cloud provider. If your ICP is revoked, JD Cloud may suspend the China Service and
  Cloudflare reroutes that traffic to the nearest PoPs outside China.

## DNS (in-China nameservers)
- **Default:** DNS resolves at the PoP closest to the client (global PoP outside China, JD Cloud PoP
  inside).
- **In-China Authoritative DNS** (optional, improves TTFB): resolve at JD Cloud PoPs. Enabled by
  sales, not self-serve. **Only enable if >90% of traffic is from China** — once on, *all* DNS
  (including non-China users) routes to JD Cloud, raising latency for everyone else.
- Partial setup uses CNAMEs: `…cdn.cloudflarecn.net` (In-China DNS) vs `…cdn.cloudflareanycast.net`
  (global default).

## Available products & notable exclusions
**Available:** Authoritative DNS · CDN/Cache (static cache only) · Image Transformations · L7 DDoS ·
WAF (managed + custom rules, rate limiting, content scanning) · Client-side Security · Bot Management
(limited ML models) · Argo Smart Routing · Rules · Load Balancing · Workers · Workers KV · R2 (with
caveats) · static Assets · Images · mTLS · Secrets · Service bindings · Tail Workers · Workers for
Platforms · SSL/TLS · HTTP/3 · WebSockets · Instant Logs · Logpush.

**Not available / limited in Mainland China:**
- **Turnstile** — not supported (affects both China and global zones with China visitors).
- **Pages** — not available (`pages.dev` cert not in China); a global-zone Pages project may be
  extended in via Global Acceleration.
- **Cache** — no Cache Reserve, no Tiered Cache (static cache only).
- **R2** — buckets can't be created in China and public-bucket custom domains aren't supported; extend
  R2 in via Global Acceleration instead.
- **Origin Rules** — need China Network enabled on *both* origin and target zones, else visitors get
  error 1016 / HTTP 530.

## Gotchas
- **No ICP = no service.** China-based providers shut down un-filed sites, often without notice.
- **Content vetting can reject** your domain; budget time and possible back-and-forth.
- **IPv6 can't be disabled** — make sure origins/clients tolerate it.
- **In-China DNS is all-or-nothing** — penalizes non-China users; gate on the >90% rule.
- **Firewall the JD Cloud origin IPs:** pull `GET /client/v4/ips?networks=jdcloud` (`jdcloud_cidrs`)
  and refresh allowlists **at least every 30 days** — new IPs are announced 30 days ahead.
- These are the IPs Cloudflare uses to reach your origin, *not* the IPs returned to visitors.

## Pricing & limits
> ⚠️ China Network is an **Enterprise-only add-on with no public pricing** — it's a separate
> subscription negotiated with sales. There is no free tier or self-serve signup.
> Verify current terms with your Cloudflare account team before quoting.

- **Cost drivers:** the China Network package subscription (custom/Enterprise pricing) on top of your
  Enterprise plan; ICP filing/license processing fees (charged by your provider; MIIT registration
  itself is free); optional **Global Acceleration** add-ons (CDN, Cloudflare One Client, Cloudflare
  WAN, ICP/MLPS services, Travel SIM) priced separately via partners.
- **Key prerequisites/limits:** Enterprise plan · valid ICP per apex domain · JD Cloud content vetting
  · ~24–48h first-time onboarding · mandatory IPv6 · partner-operated (JD Cloud) infrastructure.

## Going deeper
- No dedicated official `cloudflare` skill ref exists for China Network — this file is the primary
  summary. For exact, current details use the live docs: `developers.cloudflare.com/china-network/`.
- Available products table: `china-network/reference/available-products/`.
- ICP details & display rules: `china-network/concepts/icp/`.
- Global Acceleration (dynamic content, Cloudflare One/WAN, R2 extension): `china-network/concepts/global-acceleration/`.
- Origin IP list: `GET https://api.cloudflare.com/client/v4/ips?networks=jdcloud`.
