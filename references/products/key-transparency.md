# Key Transparency Auditor — verifiable public-key distribution for E2EE messaging

> A hosted **auditor** for Key Transparency Logs: it signs/verifies an append-only Log of public
> keys (like Certificate Transparency, but for E2EE messaging keys such as **WhatsApp**), so users
> can confirm keys haven't been tampered with. Very niche — not a general-purpose Worker binding.

## Contents
- When to use (and when not)
- How it works (Log / Auditor / epoch)
- Verify with Plexi (CLI)
- REST API (info / epochs / namespaces)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You operate (or want to **independently audit**) a Key Transparency **Log** for an E2EE messaging
  system, and need a third party to vouch that the Log is append-only and untampered.
- You want to **locally verify** Cloudflare's audit work on a public Log (e.g. WhatsApp) rather than
  trusting it blindly — confirm a signed epoch with the `plexi` CLI.
- **Not** for: storing/serving keys yourself, generic key-value (→ `kv`), secrets (→ `secrets-store`),
  or TLS certificate transparency (that's SSL/Edge Certificates → CT Monitoring). This audits *Logs*,
  it does not host your messaging keys.

## How it works
- **Log** — an append-only, verifiable data structure of public keys, maintained by the messaging
  operator (modeled on Certificate Transparency; uses [facebook/akd](https://github.com/facebook/akd)
  proofs).
- **Auditor** — Cloudflare. It signs **epoch** information (timestamp, epoch height/number, digest)
  and, if the Log provides AKD proofs, verifies them asynchronously. Signatures are distributed by
  the Log to end-users as evidence of integrity.
- **Epoch** — one published state of a Log: `{ epoch, digest, timestamp, signature }`. Epochs are
  strictly increasing, each digest unique, and **cannot be republished**.
- **Namespace** — one Log monitored by the Auditor (e.g. `whatsapp.key-transparency.v1`).

## Verify with Plexi (CLI)
[`plexi`](https://github.com/cloudflare/plexi) is the client for local proof verification. Install with
`cargo install plexi` (Rust 1.81+). It ships **no default remote** — set one per call or via env:
```sh
export PLEXI_REMOTE_URL=https://plexi.key-transparency.cloudflare.com
plexi ls          # list Logs (namespaces) the auditor monitors
plexi audit --namespace 'whatsapp.key-transparency.v1' --long   # verify signature + proof for latest epoch
```
`audit` reports `Signature verification: success` and `Proof verification: success` when valid.

## REST API
Base: `https://plexi.key-transparency.cloudflare.com` (Cloudflare's public auditor remote).
- `GET /info` → auditor `keys` (public keys, with `not_before` for rotation) + monitored `logs`.
- `GET /namespaces` → list public namespaces (each `Online` / `Initialization` / `Disabled`).
- `GET /namespaces/{ns}/audits/{epoch}` → an epoch's `{ digest, timestamp, signature }`.
- `POST /namespaces` → register a Log (`name`, `public`, `root`, `signature_version`, optional
  `log_directory` for proof fetching). **mTLS-authenticated.**
- `POST /namespaces/{ns}/audits` → publish/sign a new epoch (`epoch`, `digest`). **mTLS-authenticated.**
- `PATCH /namespaces/{ns}` `{ "status": "Disabled" }` → mark a corrupted/lost Log read-only. **mTLS.**

## Gotchas
- **Not a Workers binding.** There's no `wrangler.jsonc` entry — it's a hosted API + the `plexi` CLI.
- **Registering a namespace requires contacting Cloudflare** (and mTLS for write ops); reads are open.
- **Digest format:** 32-byte hex string, **length exactly 64**. Epochs strictly increasing
  (2, 3, …); duplicate digests rejected; epochs are immutable (no republish).
- If a `root` is set for the namespace, the **first** epoch must match it (number + digest).
- `signature_version`: `0x0001` = protobuf Ed25519, `0x0002` = bincode Ed25519 — must match what your
  verifier expects.
- Publishing to a `Disabled` namespace → `HTTP 400 Namespace is disabled and read-only`.

## Pricing & limits
> ⚠️ This is a **specialized** core-services product with **no public pricing or self-serve signup** —
> "If you want to register a namespace, contact us" (docs → API → Namespaces). The docs declare **no
> maturity stage** for it (no "beta"/"GA"/"preview" label anywhere in `key-transparency/`; the
> *public beta* label belongs to the separate **Certificate Transparency Monitoring** feature under
> SSL/TLS). Verify current status and any cost before relying on it. No published rate/storage limits.

The **read** side (verifying via `plexi` / public GET endpoints against Cloudflare's auditor) is
openly accessible. The **write** side (registering namespaces, publishing epochs) is gated by mTLS and
onboarding with Cloudflare.

## Going deeper
- No official `cloudflare` skill `references/` entry exists for this product (it's niche).
- Official docs: `developers.cloudflare.com/key-transparency/` (overview, Monitor the Auditor, API).
- Source/spec: [`cloudflare/plexi`](https://github.com/cloudflare/plexi) (CLI + `plexi_core` proto
  types), [`facebook/akd`](https://github.com/facebook/akd) (AKD proofs), and WhatsApp Key
  Transparency background from Meta engineering.
