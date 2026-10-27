# MoQ — Media over QUIC (low-latency live media transport)

> A **beta** protocol service for delivering **live** media (video/audio/data) over QUIC
> with very low latency. Cloudflare runs a MoQ **relay** on its network. Think "HTTP for content,
> WebRTC for calls, **MoQ for live media fan-out**." Pub/sub of media tracks, not a managed
> encoder/player like Stream.

## Contents
- What it is
- When to use (and when not)
- How it's wired
- Key concepts / API surface
- Gotchas
- Status, pricing & limits
- Going deeper

## What it is
MoQ (Media over QUIC) is an **IETF working-group protocol** (`draft-ietf-moq-transport`) for
scalable, low-latency live media. Cloudflare operates a **relay**: publishers push media tracks to
the relay, subscribers pull them, and Cloudflare's network handles fan-out/distribution. It rides on
**QUIC** (via **WebTransport** in browsers), gaining 0-RTT setup, stream multiplexing, no
head-of-line blocking, connection migration, and built-in encryption. It is a **transport-level
service** (move media bits), NOT a turnkey product: you bring your own encoding, packaging,
and playback. You provision your **own relay** per account (dashboard or API); each relay is an
isolated scope for your namespaces, tracks and objects.

## When to use (and when not)
- **Use for:** live, latency-sensitive fan-out — live streaming to many viewers, real-time
  contribution/ingest, interactive/low-latency broadcast, sub-second "near real-time" experiences
  where HLS/DASH latency (seconds) is too high.
- **vs Stream** (`stream`): Stream is the managed product for **VOD + live** (encode, package,
  adaptive HLS/DASH, player, storage). Use Stream for normal streaming. Reach for MoQ only when you
  need lower latency than HLS/LL-HLS and are willing to build the media pipeline yourself.
- **vs Realtime / WebRTC** (`realtime`): WebRTC is the mature path for **bidirectional**
  conferencing (calls, sub-200ms peer media). MoQ targets **one-to-many live distribution** at scale
  over CDN infrastructure. Today, because Safari lacks production WebTransport, many MoQ apps still
  need a **WebRTC (or WebSocket) fallback**.
- **Not for:** VOD/on-demand (→ `stream`, `r2`), two-way calls today (→ `realtime`/WebRTC), generic
  file delivery (→ `r2`/CDN), request/response APIs (→ `workers`).

## How it's wired
**No `wrangler` binding is documented** — MoQ is a standalone relay you provision and then connect
to as a protocol endpoint:
0. **Provision a relay:** dashboard (**Media > Realtime > MoQ Relay**) or REST API
   `POST /accounts/{account_id}/moq/relays` with `{"name": "..."}`. The response returns a relay ID
   and two default tokens (publish+subscribe, and subscribe-only); **token secrets are shown once
   and never stored**. More tokens / expirations via `developers.cloudflare.com/api/resources/moq`.
1. **Transport:** open a **WebTransport** (HTTP/3 over QUIC) session from the browser, or a native
   QUIC/WebTransport client, to your relay endpoint —
   `https://draft-16.cloudflare.mediaoverquic.com/<token>` (draft-16, **auth required**, token in
   the URL path) or `https://draft-14.cloudflare.mediaoverquic.com/` (draft-14).
2. **Publish:** announce a namespace, then publish media as **tracks** (objects grouped into
   groups/subgroups) to the relay. Reference tooling: `github.com/cloudflare/moq-rs`
   (`moq-pub` / `moq-sub`, fed by ffmpeg fragmented-MP4).
3. **Subscribe:** another client subscribes to a track namespace/name; the relay fans out objects.
4. **Media stack is yours:** capture → encode (e.g. WebCodecs/AV1/H.264/Opus) → packetize into MoQ
   objects → publish; on the receive side, reassemble → decode → render. Cloudflare moves the bits;
   it does not transcode or package for you.

## Key concepts / API surface
- **Relay** — Cloudflare-operated server that routes published tracks to subscribers (the fan-out).
- **Namespace / Track** — addressing: a publisher announces a **namespace**; media flows as named
  **tracks** within it.
- **Group / Subgroup / Object** — delivery units. Objects carry media payloads; groups bound
  decode/recovery; subgroups order delivery within a group. Priorities drive QUIC scheduling.
- **Tokens** — access control is per-relay tokens scoped to publish and/or subscribe. Draft-16
  carries the token **in the URL path**, so it lands in server access logs (see Gotchas).
- **PUBLISH / SUBSCRIBE / FETCH** — core control messages. Support is **partial** and
  draft-dependent (see Feature Matrix): e.g. `SUBSCRIBE`, `PUBLISH`, `PUBLISH_NAMESPACE`,
  `TRACK_STATUS`, SETUP are supported on both drafts; **`FETCH*`, `GOAWAY`, `SUBSCRIBE_UPDATE`,
  `PUBLISH_ERROR`, `TRACK_STATUS_ERROR`** are **not**, on either draft. `SUBSCRIBE_NAMESPACE*` is
  supported on **draft-16 only** (not on draft-14). `MAX_REQUEST_ID` / `REQUESTS_BLOCKED` are
  **partial** on draft-16 (received/logged; no automatic limit increase) and unsupported on draft-14.
- **Draft versions** — the relay serves **multiple drafts simultaneously**: **draft-14 and draft-16**
  are deployed, and Cloudflare is working on **draft-18** ahead of a global deployment (test it
  meanwhile via `github.com/englishm/moq-interop-runner`). Pin your client's draft to the endpoint
  you connect to — this moves.

## Gotchas
- **Safari/WebKit:** no production WebTransport yet (early flag-gated impl since Safari 18.4,
  2025-03-31; iOS too). Plan a **WebRTC/WebSocket fallback** for Apple clients.
- **Tokens leak via URL:** draft-16 sends the token in the URL path, so it shows up in server
  access logs. Issue one token per client, set short expirations, and rotate on revoke. In-band
  auth (IETF **C4M** and **Privacy Pass for MoQ** drafts) is planned as those mature, not shipped.
- **Token secrets are shown once** in the create-relay response and never stored — capture them.
- **Partial spec support:** many messages are unimplemented (no `FETCH`, no `SUBSCRIBE_UPDATE`, no
  `GOAWAY`). Don't assume a feature from the IETF spec works on the relay — check the
  Feature Matrix, per draft.
- **Draft churn:** the docs previously described a draft-07 relay (with a known Subgroup Header
  `subscribe_id` quirk); draft-07 is no longer listed at all. Interop breaks across draft versions;
  expect to update clients.
- **You own the media pipeline:** no built-in encoding/transcoding/ABR/player. Higher integration
  effort than Stream.
- **Spec is the source of truth:** follow the IETF MoQ working-group drafts for protocol details;
  Cloudflare docs describe only what its relay currently implements.

## Status, pricing & limits
> ⚠️ **VERIFY LIVE — this is the fastest-moving entry here.** MoQ is in a **beta period** (docs'
> own term), not GA. No pricing page, no documented quotas/limits, no SLA, and no `wrangler` binding
> in the current docs (only Overview, Background, Feature Matrix). Treat specifics below as a
> snapshot to re-check on `developers.cloudflare.com/moq/` before relying on them.

- **Maturity:** beta. Relay API, draft support, and endpoints can change without notice. Not for
  production-critical workloads without a fallback.
- **Pricing:** **free to use during the beta period** (docs, Overview, updated 2026-07-31). No
  post-beta pricing published — do not quote a future price.
- **Limits/quotas:** **not documented** — assume undefined and test empirically.
- **Spec target:** subset of `draft-ietf-moq-transport`, **draft-14 and draft-16** deployed;
  **draft-18** in progress. Verify the advertised draft against the live relay.

## Going deeper
- **No official `cloudflare` skill ref exists** for MoQ — this file is the primary reference.
- Official docs (3 pages only): `developers.cloudflare.com/moq/` (Overview, `/about/` Background,
  `/feature-matrix/` supported messages). Index: `developers.cloudflare.com/moq/llms.txt`.
- Relay REST API: `developers.cloudflare.com/api/resources/moq`. Reference client: `cloudflare/moq-rs`.
- Protocol spec (authoritative): IETF MoQ WG — `datatracker.ietf.org/doc/html/draft-ietf-moq-transport-16`.
- Related products: `stream` (managed VOD/live), `realtime` (WebRTC), `r2` (storage).
- "Is MoQ GA / priced yet?" → re-check the live docs and `scripts/blog-search "Media over QUIC"`.
