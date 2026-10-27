# Web3 — gateways to IPFS and Ethereum networks

> HTTP-accessible gateways to decentralized networks, so you can serve content from **IPFS** or
> read/write **Ethereum** without running your own node. A paid add-on, not a Workers binding.

## Contents
- When to use (and when not)
- How it works (DNS + gateway)
- IPFS Gateway
- Ethereum Gateway
- Config & management (API)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Serve IPFS content over HTTP** — host a static site/dApp frontend on IPFS, point a custom domain
  at it, and let end users reach it via plain `https://` with no IPFS client.
- **Read/write Ethereum** — query chain state (balances, blocks, logs) or broadcast signed
  transactions via JSON-RPC, without operating or syncing an Ethereum node.
- You want Cloudflare's anycast network in front (caching, DDoS protection, TLS) of a Web3 backend.
- **Not** for: running consensus/validator infra, pinning/storing data on IPFS (it's a read-only
  *gateway*, not a pinning service), or signing transactions (you sign client-side; the gateway only
  relays). For general object storage use **r2**; for app hosting use **pages/workers**.

## How it works
A gateway is a **hostname** (subdomain of one of your Cloudflare zones) bound to a network target.
Creating one auto-provisions a **proxied CNAME** (→ `ipfs.cloudflare.com` or `ethereum.cloudflare.com`),
an SSL/TLS cert, and (for IPFS DNSLink) a `_dnslink` TXT record. Requests route to a Cloudflare Worker
that talks to Cloudflare's own IPFS/Ethereum nodes.
- **Reads** are cached at the nearest data center; cache miss → fetched from Cloudflare's node, cached, returned.
- **Writes** (EVM chains only) forward your signed transaction to a Cloudflare Ethereum node's mempool;
  you get back a transaction ID to track.
- Note: creating a gateway on a hostname with existing DNS records **overwrites** those records.

## IPFS Gateway (read-only)
Access content via `https://<your-gateway>/<path>`:
- `/ipfs/<CID>` — content addressed by CID; immutable, never changes.
- `/ipns/<DOMAIN>` — resolves a CID from DNS (DNSLink); mutable — update the record to publish new content.

Two gateway types:
- **DNSLink (restricted)** — pinned to one CID/IPNS name via a `_dnslink` TXT record (e.g.
  `dnslink=/ipns/onboarding.ipfs.cloudflare.com`). Good for serving *your* site at a custom domain.
- **Universal Path** — open gateway, serves *any* CID/IPNS path. Enterprise-only. Open by default, so
  use the **blocklist** (CIDs or `/ipfs/` `/ipns/` content paths) to deny specific content.

## Ethereum Gateway (read + write)
POST JSON-RPC to `https://<your-gateway>/v1/<network>` (`/v1/mainnet`, `/v1/sepolia`):
```bash
curl https://your-gateway/v1/mainnet -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x2244",true],"id":1}'
```
- **Read**: `eth_getBalance`, `eth_getBlockByNumber`, `eth_call`, `eth_getLogs`, `eth_estimateGas`, etc.
  Two have documented caps: `eth_getLogs` — "Max block range of 800 blocks"; `eth_feeHistory` —
  "Max block count of 10".
- **Trace**: `trace_filter` is supported (block range limited to **800 blocks**, `count` limited to **200**).
- **Write**: only `eth_sendRawTransaction` (you sign client-side with your own wallet key, then relay
  the hex-encoded signed tx). The gateway never holds keys.
- Unsupported methods return `403`. Blocked groups: key-holding (`eth_accounts`, `eth_sign`,
  `eth_sendTransaction`, `eth_coinbase`), node/peer state (`net_peerCount`, `eth_protocolVersion`,
  `eth_hashrate`), **the whole filter family** (`eth_newFilter`, `eth_newBlockFilter`,
  `eth_newPendingTransactionFilter`, `eth_uninstallFilter`, `eth_getFilterChanges`, `eth_getFilterLogs`
  — poll with `eth_getLogs` instead), the legacy compilers (`eth_getCompilers`, `eth_compile*`), and
  `eth_submitWork`/`eth_submitHashrate`. Note `eth_mining` and `eth_getWork` *are* ✅.
- Public test gateway exists at `cloudflare-eth.com` (e.g. `https://web3-trial.cloudflare-eth.com/v1/mainnet`).

## Config & management (API)
No `wrangler.jsonc` binding — gateways are zone resources managed via dashboard or REST API
(`/zones/{zone_id}/web3/hostnames`):
```bash
curl "https://api.cloudflare.com/client/v4/zones/{zone_id}/web3/hostnames" \
  -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  --data '{"name":"gateway.example.com","target":"ipfs","dnslink":"/ipns/onboarding.ipfs.cloudflare.com"}'
```
- `target`: `ipfs` (DNSLink), `ipfs_universal_path`, or `ethereum`.
- **Edit** (PATCH): only the description and (IPFS) the DNSLink value are mutable. To change hostname
  or target, delete and recreate.
- **Refresh** (PATCH, empty body): re-creates DNS records when a gateway is stuck in `Error` status.
- **Delete**: removes associated DNS records; cannot be undone.
- **Restrict access**: gateways are public by default. For internal-only use, layer Cloudflare Access
  policies + service tokens (or WAF custom rules) in front.

## Gotchas
- **Read-only IPFS** — you cannot upload/pin via the gateway; pin elsewhere (your node or a pinning
  service) and point DNSLink at the CID.
- **Auto-overwrites DNS** — creating a gateway clobbers pre-existing records on that hostname.
- **Hostname/target are immutable** — plan the subdomain up front; changes mean delete + recreate.
- **Ethereum writes need client-side signing** — the gateway relays only `eth_sendRawTransaction`;
  key-holding RPC methods are blocked (`403`).
- **No JSON-RPC filters** — the `eth_*Filter*` family is `403`; use `eth_getLogs` (≤800-block range).
- **Networks**: only Ethereum Mainnet + Sepolia testnet (Rinkeby/Ropsten deprecated).
- **Universal Path is Enterprise-only** and open by default — set a blocklist.

## Pricing & limits
> ⚠️ Paid **add-on** with **usage-based billing**. Pricing is volatile — verify on the live page
> (`cloudflare.com/application-services/products/web3/` and the dash) before quoting.

- **Cost drivers**: IPFS billed per **data transfer (GB)**; Ethereum billed per **HTTP request**.
  Overages beyond the included amounts are metered.
- **Enterprise preview**: available as a non-contract preview service — full access, free of metered
  fees/limits — so confirm whether the customer is on preview vs. metered billing.
- **Included (no extra cost)**:
  - IPFS data transfer: **50 GB** (Free/Pro/Business), **100 GB** (Enterprise). No file-size limit.
  - Ethereum: **500,000** HTTP requests (Free/Pro/Business), **1,000,000** (Enterprise).
- **Gateways per account**: **15** (Free/Pro/Business), **Unlimited** (Enterprise).
- **Universal Path IPFS gateway**: Enterprise plan only (others get DNSLink only).

## Going deeper
- No dedicated official `cloudflare` skill ref exists for Web3 — this file is the primary reference.
- Full JSON-RPC method support matrix: `docs-oficiais/pages/web3/ethereum-gateway/reference/supported-api-methods/`.
- API (hostnames CRUD, blocklist entries): `developers.cloudflare.com/api/` → `web3` resource.
- Concepts (IPFS, DNSLink, node types): `docs-oficiais/pages/web3/{ipfs-gateway,ethereum-gateway}/concepts/`.
