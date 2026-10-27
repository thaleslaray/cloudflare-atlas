# Time Services — NTP, NTS, Roughtime (secure time)

> Cloudflare's free, anycast time service at `time.cloudflare.com`. Three protocols: **NTP** (plain
> sync), **NTS** (authenticated NTP over TLS), and **Roughtime** (lightweight authenticated time).
> Use NTS or Roughtime when you need time you can *trust*, not just time you can *get*.

## Contents
- When to use (and when not)
- The three protocols
- Endpoints & config
- Roughtime API (Go)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You need clock sync on a server/device and want a fast, free, global anycast source → **NTP**,
  point at `time.cloudflare.com`.
- You need time you can **cryptographically trust** — to stop a man-in-the-middle from rolling your
  clock back (e.g. forcing acceptance of an expired/revoked TLS cert or session ticket) → **NTS**
  (authenticated NTP) or **Roughtime**.
- You want *accurate* (within seconds) authenticated time with a tiny, auditable protocol and no TLS
  handshake per query → **Roughtime** (precision is coarser than NTP, ~10s tolerance is the design point).
- **Not** for: high-precision timing inside a Worker (Workers freeze `Date.now()` per I/O turn for
  side-channel reasons — this is a host/device time service, not a Workers API). Not a binding.

## The three protocols
| Protocol | Auth | Transport | Precision | Use when |
| -------- | ---- | --------- | --------- | -------- |
| **NTP** (RFC 1305/5905) | none | UDP 123 | high | plain clock sync; default for most OSes |
| **NTS** (RFC 8915) | yes (TLS-derived keys) | TLS key exchange, then NTPv4 | high | authenticated NTP, drop-in for modern clients |
| **Roughtime** | yes (Ed25519 signed) | UDP | coarse (~secs) | simple auditable authenticated time |

- **NTS** runs in two phases: (1) a TLS handshake (same web PKI) to exchange key material, then the
  channel closes; (2) NTPv4 packets are authenticated with those keys via NTS extension fields.
- **Roughtime** signs each response with an Ed25519 online key, delegated from a root key (delegation
  acts like an X.509 cert). Responses are *auditable*: chained nonces prove queries happened in order.

## Endpoints & config
**NTP / NTS** — set your client to `time.cloudflare.com`. Cloudflare does **not** do leap smearing
(it sets the NTP Leap Indicator and the kernel applies the leap second; matches `pool.ntp.org`).

```ini
# chrony  (/etc/chrony/chrony.conf)
server time.cloudflare.com iburst
# systemd-timesyncd  (/etc/systemd/timesyncd.conf)
[Time]
NTP=time.cloudflare.com
```
NTS is supported by chrony, NTPsec, and ntpd-rs — point them at `time.cloudflare.com`.
Cloudflare's NTP IPs are also in `pool.ntp.org` (`162.159.200.1`, `162.159.200.123`,
`2606:4700:f1::1`, `2606:4700:f1::123`) — many Linux distros may already use them.

**Roughtime** (beta):
- Address: `roughtime.cloudflare.com:2003` (anycast, IPv4 or IPv6, UDP only)
- Root public key (Ed25519): `0GD7c3yP8xEc4Zl2zeuN2SlLvDVVocjsPSL8/Rl/7zg=`
- Fetch the key programmatically: `dig TXT roughtime.cloudflare.com`

```sh
go install github.com/cloudflare/roughtime/cmd/getroughtime@latest
getroughtime -ping roughtime.cloudflare.com:2003 \
  -pubkey 0GD7c3yP8xEc4Zl2zeuN2SlLvDVVocjsPSL8/Rl/7zg=
```

## Roughtime API (Go — `github.com/cloudflare/roughtime`)
- `roughtime.LoadConfig("roughtime.config")` → `(servers, skipped, err)`; config is JSON listing each
  server's name, `publicKeyType` (only `ed25519`), `publicKey`, and `addresses` (only `udp`).
- `roughtime.Get(&servers[0], attempts, timeout, prev)` → `*roughtime.Roughtime`. Pass a prior result
  as `prev` to chain the nonce.
- `rt.Now()` → `(t1, radius)`: server time + uncertainty radius. Compute `delta := t1.Sub(t0)` and feed
  it into a `crypto/tls` `Config.Time` callback to validate certs against trusted time.
- `roughtime.Do(servers, attempts, timeout, nil)` → query many servers (recommended).
  `roughtime.MedianDeltaWithRadiusThresh(res, t0, thresh)` rejects responses with radius > `thresh`.
- Audit a chain: `roughtime.NewChain(results)` then `chain.Verify(nil)` (cryptographic proof of order).

## Gotchas
- **Roughtime is beta** — the root public key *may change*. Re-fetch via `dig TXT` rather than
  hardcoding forever; check the docs' deprecation table (e.g. `:2002` key was retired 2024-06-30).
- **Don't mix smearing and non-smearing servers** — Cloudflare doesn't smear leap seconds; combining
  with smearing pools gives anomalous results.
- **Roughtime ≠ high precision** — it targets ~10s accuracy to defeat clock-rollback attacks, not
  microsecond sync. Use NTP/NTS where precision matters.
- **Plain NTP is unauthenticated** — anyone on-path can spoof it. If clock integrity is a security
  boundary, use NTS or Roughtime.
- Roughtime transport is **UDP-only**, and only the **Ed25519** signature algorithm is supported.

## Pricing & limits
- **Free.** All three services are offered free over Cloudflare's global anycast network. No account,
  binding, or API key required. Usage is governed by the Cloudflare Website and Online Services Terms.
- ⚠️ No public per-request pricing page exists (it's a free public good); verify the Terms of use
  (`developers.cloudflare.com/time-services/tos/`) before relying on it for production SLAs.
- Roughtime carries a **beta** caveat (see Gotchas).

## Going deeper
- Docs: `developers.cloudflare.com/time-services/` (NTP / NTS / Roughtime / ToS).
- Roughtime client + recipes (TLS sync, desktop skew alerts, multi-source auditing):
  `github.com/cloudflare/roughtime` (`recipes/tls.go`, `recipes/alerter.go`).
- Background blogs: `blog.cloudflare.com/secure-time/` (NTP/NTS) and `blog.cloudflare.com/roughtime/`.
- Specs: NTP RFC 5905 · NTS RFC 8915 · Roughtime `roughtime.googlesource.com/roughtime`.
- Other implementations: C++ (Google), Rust (`int08h/roughenough`), Java (`int08h/nearenough`).
