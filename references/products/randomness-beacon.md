# Randomness Beacon — distributed, publicly verifiable randomness (drand / League of Entropy)

> A public source of **unbiasable, unpredictable, publicly verifiable** random values, produced
> collectively by the **League of Entropy** (Cloudflare + partners) running the **drand** beacon.
> Anyone can fetch a round's randomness and *cryptographically verify* it was not tampered with.

## Contents
- When to use (and when not)
- How it works (1-minute model)
- Access (HTTP / clients)
- Gotchas
- Pricing & availability
- Going deeper

## When to use
- You need randomness that a **third party can independently verify** was fair and unmanipulated:
  lotteries / raffles, public draws, sortition (jury/committee selection), audits, leader election,
  on-chain / smart-contract randomness, fair sharding.
- You want a value that is **the same for everyone** at a given round and **provably unbiased** —
  no single operator (not even Cloudflare) can predict or steer it.
- **NOT for cryptographic secrets** — keys, tokens, nonces, salts, session IDs, password resets.
  The beacon value is **public and shared globally**, so it is the opposite of secret. For local
  secret randomness use `crypto.getRandomValues()` (Workers/browsers) or `crypto.randomBytes()`
  (Node) — a CSPRNG. Use the beacon only when *public verifiability* is the actual requirement.

## How it works (1-minute model)
- The beacon emits a new random value every fixed interval (a **round**), forever, like NTP for randomness.
- Each round's value is a **threshold BLS signature** (curve BLS12-381) over the round message.
  A `t-of-n` set of independent operators must cooperate; fewer than `t` can neither produce nor bias it.
- **Deterministic:** a round has exactly one valid value — no forking, no two answers for round `r`.
- Verify a value against the network's **public key** (distributed-key-generation output) — no node
  ever holds the collective private key.
- Two modes: **chained** (round `r` signs `H(r ‖ σ_{r-1})`, value depends on full history) and
  **unchained** (round `r` signs `H(r)`, so a future round's value is verifiable/precomputable by message).

## Access (HTTP / clients)
There is **no Wrangler binding** — it is a public HTTP service, not a Cloudflare account resource.
Consume it over the drand HTTP API or an official client (Go / JS / Rust). From a Worker just `fetch`:

```js
// Public drand HTTP relay (Cloudflare runs one of the League of Entropy relays).
const base = "https://drand.cloudflare.com";
const info  = await (await fetch(`${base}/info`)).json();          // { public_key, period, genesis_time, hash, groupHash, schemeID }
const latest = await (await fetch(`${base}/public/latest`)).json(); // { round, randomness, signature }
const round42 = await (await fetch(`${base}/public/42`)).json();    // a specific historical round
// ALWAYS verify `signature` against `info.public_key` with a drand client before trusting `randomness`.
```
- `randomness` is the hash of the round signature → use it as your seed / draw value.
- Default chain (verified live): `period` 30s, `schemeID` `pedersen-bls-chained`,
  chain `hash` `8990e7a9…51b2ce`, `genesis_time` 1595431050. Re-fetch `/info`; do not hardcode.
- Multiple interoperable relays exist (Cloudflare, Protocol Labs, others) — pick any; all serve the
  same chain. Endpoint hosts change over time; confirm the current relay URL + chain hash on drand.love.

## Gotchas
- **Verify, don't just trust the relay.** A relay is an HTTP cache, not a trust anchor. Always verify
  the signature against the chain's public key (use an official client) — that is the entire point.
- **Public, not secret.** Never derive keys/secrets from beacon output (see "When to use").
- **Predictability window:** anyone can see past rounds and the schedule; for "commit to a future
  draw" use a round whose time is in the **future** so the value does not yet exist when you commit.
- **Pin the chain hash.** A network can have multiple chains (chained vs unchained, `G1/G2` swaps with
  different signature/key sizes). Verify against the specific chain hash you intend to consume.
- **Availability ≠ guarantee for your app.** It is best-effort public infrastructure; cache the value
  you draw and handle relay outages / round latency in your own logic.

## Pricing & availability
- **Free public good.** drand / League of Entropy is a free, open, distributed service — there is no
  Cloudflare bill, no account, no API key for consuming it. (`fetch`-ing it from a Worker is billed as
  normal Worker egress/requests on your account, nothing beyond that.)
- No SLA — treat it as foundational-but-best-effort Internet infrastructure (like NTP/DNS).
- ⚠️ Endpoints, relay URLs, chain hashes, and round period can change — verify the current
  network details on **drand.love** before hardcoding anything.

## Going deeper
- No dedicated `cloudflare` skill ref exists — this file is the primary pointer.
- Canonical docs & live network info: **drand.love** ( `/developer/` consumers · `/operator/` node ops ).
- Cloudflare's conceptual pages: `developers.cloudflare.com/randomness-beacon/` (about, cryptographic
  background: DKG / Shamir + Feldman VSS / Pedersen DKG, threshold BLS, chained vs unchained).
- Background: "Scalable Bias-Resistant Distributed Randomness" (2017 IEEE S&P); Cloudflare blog
  → the live blog (blog.cloudflare.com), search "League of Entropy".
