# Realtime — WebRTC video/audio/data (RealtimeKit, SFU, TURN)

> Build real-time audio, video, and data apps on WebRTC over Cloudflare's edge. Three layers:
> **RealtimeKit** (managed SDK + UI), **SFU** (raw media-routing server), **TURN** (NAT-traversal relay).
> Lowest-latency interactive media — distinct from Stream (VOD/broadcast) and MoQ (live transport).

## Contents
- When to use (and when not)
- The three products (pick one)
- Config & credentials
- Key API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Interactive** real-time media: video calls, virtual classrooms, webinars, social/voice chat,
  multiplayer presence, data channels — anything where participants both publish *and* subscribe live.
- You want WebRTC (the lowest-latency cross-platform path) without running/scaling your own SFU,
  and Cloudflare's egress economics (300+ PoPs, $0.05/GB after a generous free tier).
- **Not** for: on-demand/recorded video or one-way live broadcast at scale → **Stream** (VOD + LL-HLS).
  Sub-second live *transport* / media-over-QUIC fan-out without full WebRTC → **MoQ** (`moq` ref).
  Plain file/video storage → **R2** / **Stream**. ML on the media (transcription, etc.) → **Workers AI**.

## The three products (pick one)
| | **RealtimeKit** | **SFU** | **TURN** |
|---|---|---|---|
| What | High-level SDKs + pre-built UI on top of the SFU | Low-level WebRTC media server (Selective Forwarding Unit) | Managed relay for NAT/firewall traversal |
| For | Ship video/voice fast, no WebRTC expertise | WebRTC experts wanting full control | Any WebRTC app needing connectivity |
| Effort | Low — a few lines (UI Kit + Core SDK) | High — you manage sessions, tracks, presence | Low — WebRTC libs use it transparently |
| Primitives | Meetings, Sessions, Participants, Presets, Stage, Waiting Room | Sessions (PeerConnections), Tracks — pub/sub, **no rooms** | Allocations, relayed transport addresses |

- **RealtimeKit** abstracts media routing, peer management, recording, chat, polls, breakout rooms,
  virtual backgrounds, transcription. Start here for standard meeting/webinar apps.
- **SFU** is unopinionated: no SDK, no "room" concept — just pub/sub of audio/video/data tracks by ID.
  *You* build the presence protocol (e.g. track IDs in a Durable Object). See Orange Meets demo.
- **TURN** relays media when peers can't connect directly (restrictive NAT/firewall). Used by browsers,
  Pion, libwebrtc automatically — and **free** when paired with Cloudflare SFU/Stream.

## Config & credentials
No Worker binding — Realtime is a backend HTTPS API. Keep secrets server-side; mint short-lived
client creds. Create an **SFU app** (dashboard **Realtime > Serverless SFU** at `/:account/realtime/sfu`,
or API) → **App ID** + **App Secret**. For TURN, create a **TURN key** (`/:account/calls`) → **Key ID** + **API token**.
```jsonc
// wrangler.jsonc — store as vars/secrets, then call the API with fetch()
{
  "vars": { "CALLS_APP_ID": "your-app-id" }
  // wrangler secret put CALLS_APP_SECRET   (App Secret — backend only)
  // wrangler secret put TURN_KEY_API_TOKEN (TURN key token — backend only)
}
```

## Key API / access patterns
**SFU** — base `https://rtc.live.cloudflare.com/v1`, auth `Bearer <App Secret>`:
- `POST /apps/{appId}/sessions/new` → create a session (one PeerConnection)
- `POST /apps/{appId}/sessions/{id}/tracks/new` → push/pull tracks (send SDP offer)
- `PUT  /apps/{appId}/sessions/{id}/renegotiate` → apply SDP answer after track changes
- `PUT  /apps/{appId}/sessions/{id}/tracks/close` · `GET .../sessions/{id}` (state)
- Client uses raw `new RTCPeerConnection(...)` or PartyTracks; your backend brokers SDP + track IDs.

**DataChannels** (SFU, non-media payloads — chat, game state, telemetry, control events):
- `POST .../sessions/{id}/datachannels/establish` (transport, after SDP) → then
  `POST .../sessions/{id}/datachannels/new` with `location: "local"` on the publisher and
  `"remote"` (+ publisher's `sessionId`, same `dataChannelName`) on each subscriber.
- In the browser, `pc.createDataChannel(name, { negotiated: true, id })` using the **id the API
  returned** — IDs are negotiated, so the browser never learns the settings from the remote peer.
  **Repeat the same reliability fields on publisher, every subscriber, and every client call.**
- **Delivery control (2026-08-13):** `ordered` (default `true`; `false` = a late message stops
  blocking later ones), `maxRetransmits` (`0` = fire-and-forget), `maxPacketLifeTime` (ms).
  `maxRetransmits` and `maxPacketLifeTime` are **mutually exclusive** — never both on one channel.
  Reliable-but-unordered = `ordered: false` with neither limit set.
- `waitForAck: true` (remote only) holds delivery until the subscriber sends any first message;
  the SFU eats that message. Miss the **30s** window and the channel is torn down — recreate it.
- `canReply: true` (remote only) lets **exactly one** subscriber answer back to the publisher;
  granting it to another subscriber silently revokes the first. Other subscribers never see replies.

**TURN** — backend generates expiring ICE servers from your TURN key:
```bash
curl https://rtc.live.cloudflare.com/v1/turn/keys/$KEY_ID/credentials/generate-ice-servers \
  -H "Authorization: Bearer $TURN_KEY_API_TOKEN" -d '{"ttl": 86400}'
# → { iceServers: [...] } — pass to new RTCPeerConnection({ iceServers }); revoke via .../revoke
```
**RealtimeKit** — `npm i @cloudflare/realtimekit-react @cloudflare/realtimekit-react-ui`
(also web-components / Angular / Flutter / mobile); backend mints meeting + participant auth tokens.

## Gotchas
- **SFU is not a presence protocol** — it only knows tracks. Persist who's in a "room" + their track
  IDs yourself (Durable Objects are the canonical store).
- **Track timeout: 30s** of no media packets → track is GC'd. Reconnect window is also ~30s.
- **Renegotiate** any time you add/remove tracks — push the SDP answer back via the renegotiate call.
- **Session must be `connected`** before track ops (blocks ≤5s, then times out).
- **TURN port 53** is blocked by browsers — filter it out without trickle ICE to avoid a timeout wait.
- TURN credentials are short-lived: refresh mid-call via `RTCPeerConnection.setConfiguration()`.
- App Secret / TURN key are long-term secrets — never ship to the client; only mint scoped creds.
- **RealtimeKit keeps artifacts 7 days** (composite/track recordings, transcripts, chat without
  `persist_chat`) — copy them out; meetings, participants and persisted chat stay indefinitely,
  call analytics 6 months, webhook logs 1 month.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live pages (`developers.cloudflare.com/realtime/sfu/platform/pricing/`,
> `.../realtimekit/pricing/`) before quoting.

**Cost drivers** (as of 2026-06):
- **SFU & TURN: $0.05 / GB** egress (Cloudflare → client). Push-to-Cloudflare is free.
  **Free tier: first 1,000 GB/mo shared** across SFU + TURN (one line item, not two). TURN↔SFU/Stream
  traffic isn't double-charged. TURN is **free** when used with Cloudflare SFU.
- **RealtimeKit: Beta — free now.** At GA, per-minute: A/V participant **$0.002/min**, audio-only
  **$0.0005/min**, recording/RTMP/HLS export **$0.010/min** (audio-only export **$0.003/min**),
  raw-RTP→R2 **$0.0005/min**,
  real-time transcription via Workers AI model pricing.

**SFU limits:** 50 API calls/s per **session** (no per-app limit) · ≤64 tracks per API call · unlimited
tracks/session (bandwidth-bound) · track inactivity timeout 30s · DataChannel `waitForAck` window
**30s** (a historical "15s" was removed — unsourceable in the current docs). Codecs:
H264/H265/VP8/VP9/AV1 video, Opus/G.711 audio.

## Going deeper
- Official `cloudflare` skill splits this — use those for full API/patterns:
  `references/realtimekit/`, `references/realtime-sfu/`, `references/turn/`
  (each has `api.md` · `configuration.md` · `patterns.md` · `gotchas.md`).
- SFU full HTTPS API, DataChannels, simulcast, media-transport adapters: `pages/realtime/sfu/`.
- Demos: Orange Meets (`github.com/cloudflare/orange`), echo example, `realtimekit-web-examples`.
- Stream (VOD/live broadcast) → `stream.md`; live media transport → `moq.md`.
