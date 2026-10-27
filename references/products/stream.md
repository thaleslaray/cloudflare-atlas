# Stream — store, encode, deliver & play video (live + on-demand)

> Upload, store, encode, and deliver live and on-demand video with **one API** — no infra.
> Automatic H.264 adaptive-bitrate (360p–1080p), a built-in player, signed URLs, and global delivery.

## Contents
- When to use (and when not)
- Config & access
- Key API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You need a **full video pipeline**: ingest → encode (ABR/HLS+DASH) → store → deliver → play, without
  running FFmpeg/transcoders or a CDN yourself.
- **On-demand**: user-generated uploads, course/VOD libraries, a video platform. Direct Creator Uploads
  let end users upload straight to Stream with a one-time URL (no API token in the browser).
- **Live**: RTMPS/SRT ingest from OBS/FFmpeg, auto-recorded to on-demand, simulcast to YouTube/Twitch.
- **Vs. Stream WebRTC (beta)**: use Stream's WHIP/WHEP for **sub-second** live (sports, auctions, live
  Q&A) to unlimited viewers. Regular HLS/DASH live is ~seconds of latency.
- **Vs. Realtime (WebRTC SFU)**: choose **Realtime** for interactive many-to-many calls (video
  conferencing, where viewers also publish). Stream is one/few-to-many broadcast + storage.
- **Vs. MoQ**: an emerging ultra-low-latency transport experiment — Stream is the production
  store/encode/deliver product; reach for MoQ only for cutting-edge real-time use cases.
- **Not** for: raw file storage with no encoding (→ r2); image resizing (→ images); just transforming an
  existing video URL without storing it (→ Media Transformations, billed like Images).

## Config & access
Stream is an **account-level REST API** + a per-account delivery subdomain
(`customer-<CODE>.cloudflarestream.com`). Call it from a Worker/server with an API token, or let
browsers upload via Direct Creator URLs. There **is** a Workers binding (`env.STREAM`) — add
`{"stream": {"binding": "STREAM"}}` to `wrangler.jsonc` — for upload-from-URL, direct uploads,
list/search, captions/downloads and watermark profiles without exposing API keys. Typical env:
```bash
CF_ACCOUNT_ID=...           # account id
CF_API_TOKEN=...            # Stream:Edit token — server-side only, never in frontend
STREAM_CUSTOMER_CODE=...    # delivery subdomain code (from dashboard)
STREAM_KEY_ID / STREAM_JWK  # signing key for self-signing tokens at high volume
WEBHOOK_SECRET=...          # verify processing webhooks
```
SDKs: `cloudflare` (official), `@cloudflare/stream-react` (player), `tus-js-client` (resumable uploads).

## Key API / access patterns
- **Upload**: TUS resumable (large files), Upload-from-URL (`/stream/copy`), or **Direct Creator Upload**
  (one-time URL with `maxDurationSeconds` — recommended for UGC, keeps tokens off the client).
- **Live**: `POST /stream/live_inputs` → get RTMPS/SRT (and WebRTC WHIP/WHEP) URLs; set
  `recording.mode: "automatic"` to auto-save a VOD; simulcast to up to 50 concurrent destinations
  per live input.
- **Playback**: built-in iframe player (`/<VIDEO_ID>/iframe`) or your own player via HLS/DASH manifests
  (`/<VIDEO_ID>/manifest/video.m3u8`). React: `<Stream>` component.
- **Access control**: `requireSignedURLs` + short-lived signed tokens, `allowedOrigins` to stop
  hotlinking, geo/IP Access Rules inside tokens.
- **Extras**: webhooks on processing, AI-generated or uploaded captions, watermarks, MP4 downloads,
  GraphQL analytics (per-video, per-creator).

## Gotchas
- **Don't poll for `ready`** — large videos sit in `inprogress` for minutes; use a webhook instead.
- **Uploaded but invisible** = `requireSignedURLs: true` with no token. Set false for public, or sign.
- **Player infinite-loading** is usually a missing domain in `allowedOrigins` (CORS).
- **Signed-URL 403**: token expired / wrong JWK / clock skew. **Webhooks**: only **one subscription
  per account**, fired only after processing completes, and never to `localhost`/private IPs — use a
  Quick Tunnel to test locally. Verify failures are usually the wrong signing secret.
- **Never put the API token in the browser** — use Direct Creator Uploads.
- **Billing trap**: client-side preloading/buffering counts as delivered minutes; browser-cached loops
  don't. Direct Creator / TUS uploads reserve `maxDurationSeconds` of storage until completed/expired.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/stream/pricing/`) before quoting.

**Two dimensions only** (on-demand and live billed the same; ingress + encoding always free, egress
included):
- **Stored**: prepaid **$5 / 1,000 minutes** stored (by duration, *not* file size; rounded up to the second).
- **Delivered**: post-paid **$1 / 1,000 minutes** delivered (counted by segment requests; ~4s segments for VOD).
- **Media Transformations** (separate, GA — billing from 2025-11-01): **$0.50 / 1,000** unique ops,
  5,000 free/month (shared with Image Transformations).
- No standalone free tier — storage must be purchased before uploading.

**Key limits**: max file **30 GB** · any input frame rate accepted, re-encoded for max **70 FPS**
playback · resolutions **360p–1080p** (H.264) · simulcast **50 concurrent destinations / live input** ·
caption file **10 MB** · watermark **2 MiB, PNG only** and **not supported on live** · live recordings
truncated at **7 days** · up to **120 videos** queued/encoding concurrently · **1 webhook subscription
/ account** · up to **1,000 signing keys**. (Removed for lack of a doc source: webhook retry
count/timeout, search results-per-page.) Verify on the docs/FAQ.

## Going deeper
- Covered by the official `cloudflare` skill (`references/stream/`) — use it for full API/patterns:
  `configuration.md`, `api.md` (on-demand), `api-live.md` (live/WebRTC/simulcast), `patterns.md`
  (TUS, JWT signing, full-stack flows), `gotchas.md` (error codes).
- Exact REST API: `developers.cloudflare.com/api/resources/stream/`.
- Live ultra-low-latency: WebRTC WHIP/WHEP (`stream/webrtc-beta/`); for calls/conferencing see the
  Realtime product instead.
