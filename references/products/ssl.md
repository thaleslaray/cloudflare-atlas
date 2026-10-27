# SSL/TLS — encrypt traffic; certificates

> Encrypt the two hops of a proxied request — visitor↔Cloudflare (edge cert) and Cloudflare↔origin
> (origin cert). The **encryption mode** is the key decision; **Full (strict)** is the recommended target.

## Contents
- When to use (and the key decision)
- Encryption modes (Off / Flexible / Full / Full strict)
- Edge certificates (Universal / Advanced / Custom)
- Origin certificates & Authenticated Origin Pull
- Client certificates (mTLS)
- Config / API
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Any **proxied (orange-cloud) hostname** gets a free edge cert automatically — TLS is on by default.
- Reach for this product when you need to: harden the Cloudflare→origin hop, bring your own cert
  (OV/EV, specific CA), cover deep subdomains, customize cipher suites / min TLS, or require client
  certs (mTLS) for device/service/API auth.
- **The key decision is the encryption mode.** Edge TLS is handled for you; the mode decides how (and
  whether) Cloudflare validates and encrypts to your origin. Aim for **Full (strict)**.
- Two certs per request: **edge cert** (Cloudflare→client) and **origin cert** (Cloudflare→origin).

## Encryption modes (zone setting `ssl`)
Controls connection 1 (browser↔Cloudflare) and connection 2 (Cloudflare↔origin).

| Mode | Browser→CF | CF→origin | Validates origin cert? | Use when |
| --- | --- | --- | --- | --- |
| **Off** | HTTP only | HTTP | — | almost never (no encryption at all) |
| **Flexible** | HTTPS | **HTTP** | no | origin can't do TLS — last resort, see redirect gotcha |
| **Full** | HTTPS | HTTPS | **no** | origin has a self-signed / invalid cert |
| **Full (strict)** | HTTPS | HTTPS | **yes** (public CA or CF Origin CA) | **recommended** — end-to-end trusted |
| **Strict (SSL-Only Origin Pull)** | HTTP or HTTPS | always HTTPS | yes | force HTTPS to origin even for HTTP visitors |

- **Automatic SSL/TLS** (default, rolling out): the SSL/TLS Recommender probes your origin and picks the
  most secure safe mode, ramping 1%→10%→100% with rollback on `5XX`/TLS errors. It never downgrades.
  Switch to **Custom SSL/TLS** to set the mode manually. Opt a zone out via the `ssl_automatic_mode`
  setting (`value: "custom"`).
- API values: `off`, `flexible`, `full`, `strict` (= Full strict), `origin_pull` (= SSL-Only Origin Pull).
- Per-hostname override: use a [configuration rule] instead of the zone-wide setting.

## Edge certificates (Cloudflare → visitor)
- **Universal SSL** — free, automatic, DV, **90-day** validity (auto-renews 30 days out). Covers apex
  + first-level subdomains on a full setup; per-proxied-hostname on a partial (CNAME) setup. On by
  default; no config.
- **Advanced certificates (ACM add-on)** — paid. Up to 50 hosts/cert (apex must be one), multi-level
  subdomains, **choose the CA / validation method / validity period**, custom cipher suites, per-hostname
  min TLS, delegated DCV, Total TLS. Still DV; single domain only. Enterprise sub: up to 100 certs/zone.
- **Custom certificates** — Business/Enterprise; **upload your own** cert (the only way to get OV/EV or
  a specific CA). You manage issuance, renewal, and expiry monitoring. Grouped into certificate packs
  (one each of SHA-2/RSA, SHA-2/ECDSA, SHA-1/RSA — counts as 1 cert).
- For OV/EV → Custom. For multi-domain certs → Cloudflare for SaaS (custom hostnames), not ACM.
- **Certificate Transparency Monitoring — GA 2026-08-13.** Opt-in, **off by default**: emails you when
  *any* CA logs a cert covering your domain, catching issuance you never requested. **SSL/TLS → Edge
  Certificates** → *Add Email*. Certs Cloudflare issued for you (backup included) are filtered out, so
  every alert deserves a look; the two benign sources are certs you uploaded and shared certs where
  your domain rides as a SAN beside strangers'. It does **not** catch look-alikes (`cloudf1are.com`) —
  not phishing detection. Replaces HPKP, which Cloudflare does not support.

## Origin certificates (Cloudflare → origin)
- **Cloudflare Origin CA** — free cert for the Cloudflare→origin hop, trusted only by Cloudflare (not
  public browsers). Install on the origin; pairs with **Full (strict)**. Requires API Access on the
  account. ⚠️ Cloudflare does **not** send expiry notifications for origin CA certs — track them yourself.
- **Authenticated Origin Pulls (mTLS)** — make the origin verify that requests actually came from
  Cloudflare (client cert on the CF side). Stops attackers bypassing the proxy to hit the origin directly.
  - **Post-quantum (2026-06):** upload an **ML-DSA** client cert for AOP, and an ML-DSA CA to the **Custom
    Origin Trust Store** (validated under Full strict) — post-quantum auth on the CF→origin hop.

## Client certificates (mTLS, account-level)
- mTLS = server also verifies the **client's** cert. Use Cloudflare's managed CA or BYOCA (Enterprise).
- CAs are set at the **account level**, so the same client certs work across all zones in the account —
  but you must enable mTLS per hostname.
- Validation result lands in `cf.tls_client_auth.cert_verified` (`true`/`false`). Enabling mTLS only
  *requests* the cert; you must **enforce** it with a WAF custom rule or API Shield — otherwise traffic
  without a valid cert still passes.
- Workers can present a client cert to upstreams via the [mTLS binding](#config--api).

## Config / API
mTLS Workers binding (`wrangler.jsonc`) — present a client cert when a Worker calls an external service:
```jsonc
{
  "mtls_certificates": [
    { "binding": "MY_CERT", "certificate_id": "<id-from-uploaded-cert>" }
  ]
}
```
Use: `env.MY_CERT.fetch("https://secured-origin.example.com")`.
- Encryption mode via API: `PATCH /zones/{zone_id}/settings/ssl` with `value` ∈ off|flexible|full|strict|origin_pull.
- Order advanced cert packs / manage certs via the SSL `certificate_packs` API (`validity_days` param).

## Gotchas
- **`ERR_TOO_MANY_REDIRECTS`** = the classic **Flexible-mode** trap: origin force-redirects HTTP→HTTPS,
  but Flexible sends it HTTP, so it loops forever. Fix: stop the origin redirect, or use Full / Full (strict).
- **Flexible is insecure** — the CF→origin hop is plaintext; anyone on that path sees traffic. Move the
  origin to TLS and use Full (strict) as soon as possible.
- **Full (not strict) trusts any cert** — including an attacker's. Only Full (strict) actually validates.
- **Origin CA certs aren't publicly trusted** — they only work behind the Cloudflare proxy; a grey-cloud
  (DNS-only) record serving an origin CA cert will show browser errors.
- **Cloudflare renews only Universal/Advanced** — it cannot renew uploaded custom certs, and sends **no
  expiry notification at all for Origin CA certs**. It *does* email 30 and 14 days before a **custom**
  cert expires (to SSL/TLS, Administrator, Super Administrator roles); AOP certs also have 30/14-day
  notifications. Origin CA is the one you must track yourself.
- **Universal covers only first-level subdomains** on a full setup — `a.b.example.com` needs Total TLS
  or an advanced cert.
- **mTLS isn't enforcement** — without a WAF/API Shield rule checking `cert_verified`, unauthenticated
  clients still reach your app.
- Certificate prioritization: Pages / R2 custom domains use Cloudflare for SaaS certs, so advanced certs
  don't apply there.

## Pricing & limits
> ⚠️ Pricing is volatile — verify on the live pricing page / dashboard before quoting.

**Free:** Universal SSL, Cloudflare Origin CA, Authenticated Origin Pull, Cloudflare-managed client certs.
**Paid add-on:** Advanced Certificate Manager (per-zone add-on; price shown in dashboard at purchase —
historically ~$10/month/zone, confirm live). **Custom certificates:** Business/Enterprise plans (Business
includes 1 modern + 1 legacy cert; Enterprise can purchase more).

**Key limits / validity:** Universal cert = **90-day** validity, auto-renew 30 days out · Advanced cert =
**up to 50 hosts** (apex required), selectable validity (90-day default; 1-year only for Enterprise via
SSL.com) · Advanced certs/zone: standard limit, up to 100 on Enterprise sub · Custom cert pack = up to 3
signature algorithms, counts as 1.

## Going deeper
- No dedicated official `cloudflare` skill ref exists for SSL/TLS — this file is the primary reference.
- Encryption modes deep-dive: `developers.cloudflare.com/ssl/origin-configuration/ssl-modes/`.
- mTLS end-to-end: the "mTLS at Cloudflare" learning path (`developers.cloudflare.com/learning-paths/mtls/concepts/`).
- Exact REST API: `references/api/ssl.md` — exact endpoints sliced from the OpenAPI spec (verify shapes live).
