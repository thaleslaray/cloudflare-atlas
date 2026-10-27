# Tunnel — connect origins/services to Cloudflare without a public IP

> Run a lightweight daemon (`cloudflared`) that opens **outbound-only**, post-quantum encrypted
> connections to Cloudflare. Expose private/local services to the internet (or to your private
> network) with no inbound ports, no public IP, no firewall holes. Formerly "Argo Tunnel". Free, all plans.

## Contents
- When to use (and when not)
- How it works & config sources
- Setup & config (`cloudflared` / `config.yml`)
- Routing & supported protocols
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Expose a private/local service (web app, API, SSH, RDP, DB) to the internet **without** a public IP
  or open inbound ports — all traffic enters through Cloudflare (CDN, WAF, Bot Mgmt, DDoS applied).
- Reach **private** resources: replace a VPN with the Cloudflare One Client (formerly WARP) + `warp-routing`
  (route IP CIDRs over the tunnel).
- Let **Workers** reach private databases/APIs/services → see `workers-vpc`.
- Origin endpoints for **Load Balancer** pools (HA, traffic steering).
- **Not** for: serving static assets you can just host on Cloudflare (→ pages / r2 / static-assets);
  public-app docs live under `/tunnel/`, VPN-replacement / Zero Trust private networking under
  `/cloudflare-one/networks/connectors/cloudflare-tunnel/`.
- **Docs moved (2026-09-11):** `/tunnel/` is now self-contained (`configuration/`, `concepts/routing/`,
  `features/locally-managed-tunnels/`, `guides/`, `reference/`, `platform/system-requirements/`).

## How it works & config sources
1. Install `cloudflared` on your server/network → it dials **out** to Cloudflare (no inbound ports).
2. Each replica holds **four** long-lived connections to **≥2** Cloudflare data centers (built-in redundancy).
3. Map a public hostname → local service (`app.example.com` → `http://localhost:8080`). The dashboard
   creates a proxied CNAME to `<UUID>.cfargotunnel.com`, which only proxies for DNS records **in the same
   account** — a leaked tunnel UUID can't be pointed at from another account.

Two **config sources** (where ingress rules live):
| Source | Storage | Updates | Use case |
|--------|---------|---------|----------|
| **Cloudflare** (token-based) | Dashboard / API | Instant, no restart | Production, centralized — *recommended* |
| **Local** (locally-managed) | `config.yml` file | Edit + restart | Dev, multi-env, version control |

## Setup & config
```bash
# Token-based (dashboard config) — Cloudflare dashboard > Networking > Tunnels > Create, copy token:
cloudflared tunnel --no-autoupdate run --token <TOKEN>

# Locally-managed:
cloudflared tunnel login
cloudflared tunnel create my-tunnel
cloudflared tunnel route dns my-tunnel app.example.com
cloudflared tunnel run my-tunnel
```
Local config (`~/.cloudflared/config.yml`) — ingress rules are evaluated **top-to-bottom, first match wins**; a catch-all is **required**:
```yaml
tunnel: <UUID>
credentials-file: /path/to/<UUID>.json
ingress:
  - hostname: app.example.com
    service: http://localhost:8000
  - hostname: api.example.com
    service: https://localhost:8443
    originRequest:
      noTLSVerify: true          # dev only — prefer caPool for self-signed
  - service: http_status:404     # required catch-all
```
Validate before deploy: `cloudflared tunnel ingress validate` · test a URL: `cloudflared tunnel ingress rule https://app.example.com`.
**Firewall:** allow egress to Cloudflare on port **7844** (TCP/UDP, http2/quic). Block all ingress.
Blocked UDP → `cloudflared` retries QUIC with backoff (2 → 64s), then falls back to HTTP/2 over TCP.
Port 443 egress is optional (auto-update checks, Access JWT validation).

## Routing & supported protocols
Published-application services: **HTTP, HTTPS, UNIX(+TLS), TCP, SSH, RDP, SMB, HTTP_STATUS, BASTION, HELLO_WORLD**
(`HELLO_WORLD` is locally-managed tunnels only; `BASTION` makes `cloudflared` a jump host to any local address).
IPv6 literals must be bracketed (`http://[2001:db8::1]:8000`).
Non-HTTP (TCP/SSH/RDP/SMB) stream over WebSocket — end users run `cloudflared access <proto>` to connect,
or use Client-to-Tunnel (Cloudflare One Client) for long-lived sessions. Private network:
`warp-routing: { enabled: true }` + `cloudflared tunnel route ip add 10.0.0.0/8 my-tunnel`
(dashboard equivalent: **Networking → Routes → Create route → Tunnel CIDR**).
gRPC works over private subnet routing only — **not** supported on published/public hostnames.

## Gotchas
- **Debug with live logs in the dashboard before SSHing anywhere (2026-08-10).** **Networking →
  Tunnels →** your tunnel **→ Live logs** streams in real time, and on a multi-replica tunnel it
  **aggregates every connector into one stream** — the fastest way to see which replica a request
  actually landed on. Previously only in the Cloudflare One dashboard; now in the main one, so
  reaching for `cloudflared tail` on the box is usually the slower path.
- **Origin settings are now editable in the main dashboard (2026-08-18).** When adding/editing a published
  application route, expand **Additional application settings** for HTTP (Host header, chunked encoding),
  TLS (origin server name, CA pool, TLS timeout, `noTLSVerify`, match SNI, HTTP/2 to origin) and Connection
  (connect/keep-alive timeouts, keep-alive connections, TCP keep-alive, proxy type, Happy Eyeballs) knobs.
  Previously only in the Cloudflare One dashboard or `config.yml`.
- **Quick Tunnels (`trycloudflare.com`) are dev/test only** — no SLA, hard cap of **200 in-flight requests**
  (excess gets `429`), no Server-Sent Events, and they fail if a `config.yaml` exists in `.cloudflared/`.
  Public by default; since 2026-10-02 `--allowed-mail` (repeat, comma list, or `'*@example.com'`) gates
  the URL behind an email one-time PIN — no Cloudflare account needed; access ends when `cloudflared` stops.
- **Which replica served it?** Logpush `zero_trust_network_sessions` now carries `DestinationReplicaID`
  (= the dashboard **Connector ID**; pair with `DestinationTunnelID`) → `cloudflared tail --connector-id`.
  Since 2026-09-29; no backfill.
- **Read the error to find the broken hop:** **1033** = no healthy `cloudflared` reached Cloudflare
  (tunnel down) · **502** "Unable to reach the origin service" = tunnel is up, `cloudflared` can't reach
  the local service · **1016** = DNS record still points at a tunnel that stopped. **`Healthy` only covers
  `cloudflared` ↔ Cloudflare** — it says nothing about whether the origin answers.
- **One `cloudflared` service per machine** — `service is already installed` means add routes to the
  existing tunnel instead of installing a second service.
- **Catch-all required** — every ingress list must end with a service like `http_status:404`, or config is invalid.
- **Self-signed origin certs** → `originRequest.noTLSVerify: true` (dev) or `caPool` (prod); don't ship `noTLSVerify` to prod.
- **Updating `cloudflared` restarts it and drops in-flight traffic** — long-lived WebSocket/SSH/UDP too.
  Use `--no-autoupdate` in prod; roll replicas one at a time or front with a Load Balancer.
- **Token rotation doesn't kill running connectors** — the old token only loses *new* connections. For a
  compromised token also `DELETE /accounts/{id}/cfd_tunnel/{tunnel_id}/connections`, then reinstall every
  replica with the new token. (The old "24h grace window" is gone from the docs; removed 2026-09-15.)
- **`cert.pem` is account-wide, the credentials JSON is one tunnel.** `cert.pem` (from `tunnel login`,
  valid ≥10 years) can create/delete/route **every** tunnel in the account — keep it off shared hosts;
  hand operators only `<UUID>.json` (never expires, runs that tunnel only). Revoke `cert.pem` by deleting
  its **Cloudflare Tunnel API Token** under My Profile → API Tokens.
- **Per-tunnel RBAC (2026-09):** resource-scoped roles can grant a member one specific tunnel
  (Members → policy → Scope: *Specific resources* → *Cloudflare Tunnel instances*). Additive only — an
  account-level `Cloudflare Access` role still sees and edits every tunnel; `GET /cfd_tunnel` and
  `GET /teamnet/routes` are filtered to what the caller can read.
- **HA via replicas, not a single process** — run 2–4 replicas (same tunnel UUID, unique connector IDs); traffic routes to the geographically closest.
  Replicas do **no** steering and a Load Balancer sees one UUID as one endpoint — for steering/affinity
  give each host its **own tunnel**; TCP monitors don't work on tunnel endpoints (monitor an `http_status:200` route).

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/tunnel/`) before quoting.

- **Cost:** Cloudflare Tunnel itself is **free on all plans**, including unlimited tunnels and traffic.
  (Downstream Cloudflare features you layer on — e.g. Load Balancing, Zero Trust seats — bill separately.)
- **Replicas:** up to **25 per tunnel** (100 connections); each replica = 4 connections to ≥2 data centers.
- **Sizing:** 2 dedicated hosts/location, ≥4 GB RAM + 4 cores, **50,000 ports**/host, `ulimit -n` ≥ **70,000**
  — throughput is bound by ports, not hardware.
- Cloudflare supports `cloudflared` versions **within one year of the latest release**.

## Going deeper
- Covered by the official `cloudflare` skill (`references/tunnel/`) — use it for full CLI, ingress/origin
  options, `api.md` (REST + TypeScript SDK for token-based tunnels), Docker/Kubernetes/Terraform patterns,
  and networking/firewall pre-checks. This file is the lean overview.
- Workers → private services: `references/products/workers-vpc.md`. Zero Trust access policies: `access`.
- VPN replacement / private networking: `/cloudflare-one/networks/connectors/cloudflare-tunnel/`.
