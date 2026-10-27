# API reference — realtime

> Exact REST endpoints for **realtime**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 72 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/calls/apps` — List apps  · required: account_id
- `POST /accounts/{account_id}/calls/apps` — Create a new app  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/calls/apps/{app_id}` — Retrieve app details  · required: app_id, account_id
- `PUT /accounts/{account_id}/calls/apps/{app_id}` — Edit app details  · required: app_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/calls/apps/{app_id}` — Delete app  · required: app_id, account_id
- `GET /accounts/{account_id}/calls/turn_keys` — List TURN Keys  · required: account_id
- `POST /accounts/{account_id}/calls/turn_keys` — Create a new TURN key  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/calls/turn_keys/{key_id}` — Retrieve TURN key details  · required: key_id, account_id
- `PUT /accounts/{account_id}/calls/turn_keys/{key_id}` — Edit TURN key details  · required: key_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/calls/turn_keys/{key_id}` — Delete TURN key  · required: key_id, account_id
- `GET /accounts/{account_id}/realtime/kit/apps` — Fetch all apps  · required: 
- `POST /accounts/{account_id}/realtime/kit/apps` — Create App  · required:   · body: name:string
- `GET /accounts/{account_id}/realtime/kit/apps/{app_id}` — Fetch app details  · required: account_id, app_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/analytics/daywise` — Fetch day-wise session and recording analytics data for an App  · required: account_id, app_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/analytics/livestreams/daywise` — Fetch day-wise analytics data for your livestreams  · required: account_id, app_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/analytics/livestreams/overall` — Fetch complete analytics data for your livestreams  · required: account_id, app_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/livestreams` — Fetch all livestreams  · required: 
- `GET /accounts/{account_id}/realtime/kit/{app_id}/livestreams/sessions/{livestream-session-id}` — Fetch livestream session details using livestream session ID  · required: account_id, app_id, livestream-session-id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/livestreams/{livestream_id}` — Fetch livestream details using livestream ID  · required: account_id, app_id, livestream_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/livestreams/{livestream_id}/active-livestream-session` — Fetch active livestream session details  · required: account_id, app_id, livestream_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/meetings` — Fetch all meetings for an App  · required: account_id, app_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings` — Create a meeting  · required: account_id, app_id  · body: (no required fields)
- `GET /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}` — Fetch a meeting for an App  · required: meeting_id
- `PUT /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}` — Replace a meeting  · required: meeting_id  · body: (no required fields)
- `PATCH /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}` — Update a meeting  · required: meeting_id  · body: (no required fields)
- `GET /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-livestream` — Fetch active livestreams for a meeting  · required: meeting_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-livestream/stop` — Stop livestreaming a meeting  · required: meeting_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-session` — Fetch details of an active session  · required: 
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-session/kick` — Kick participants from an active session  · required: account_id, app_id  · body: participant_ids:any
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-session/kick-all` — Kick all participants  · required: account_id, app_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-session/mute` — Mute participants of an active session  · required: account_id, app_id  · body: participant_ids:any
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-session/mute-all` — Mute all participants  · required: account_id, app_id  · body: (no required fields)
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/active-session/poll` — Create a poll  · required: account_id, app_id  · body: options:string[], question:string
- `GET /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/livestream` — Fetch livestream session details for a meeting  · required: meeting_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/livestreams` — Start livestreaming a meeting  · required: meeting_id  · body: (no required fields)
- `GET /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/participants` — Fetch all participants of a meeting  · required: account_id, app_id, meeting_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/participants` — Add a participant  · required: account_id, app_id, meeting_id  · body: custom_participant_id:string, preset_name:string
- `GET /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/participants/{participant_id}` — Fetch a participant's detail  · required: meeting_id, participant_id
- `PUT /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/participants/{participant_id}` — Replace a participant's detail  · required: meeting_id, participant_id  · body: custom_participant_id:string, preset_name:string
- `PATCH /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/participants/{participant_id}` — Edit a participant's detail  · required: meeting_id, participant_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/participants/{participant_id}` — Delete a participant  · required: meeting_id, participant_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/meetings/{meeting_id}/participants/{participant_id}/token` — Refresh participant's authentication token  · required: account_id, app_id, meeting_id, participant_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/presets` — Fetch all presets  · required: account_id, app_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/presets` — Create a preset  · required: account_id, app_id  · body: config:object, name:string, permissions:object, ui:object
- `GET /accounts/{account_id}/realtime/kit/{app_id}/presets/{preset_id}` — Fetch details of a preset  · required: account_id, app_id, preset_id
- `PUT /accounts/{account_id}/realtime/kit/{app_id}/presets/{preset_id}` — Replace a preset  · required: account_id, app_id, preset_id  · body: config:object, name:string, permissions:object, ui:object
- `PATCH /accounts/{account_id}/realtime/kit/{app_id}/presets/{preset_id}` — Update a preset  · required: account_id, app_id, preset_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/realtime/kit/{app_id}/presets/{preset_id}` — Delete a preset  · required: account_id, app_id, preset_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/recordings` — Fetch all recordings for an App  · required: account_id, app_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/recordings` — Start recording a meeting  · required: account_id, app_id  · body: meeting_id:string
- `GET /accounts/{account_id}/realtime/kit/{app_id}/recordings/active-recording/{meeting_id}` — Fetch active recording  · required: account_id, app_id, meeting_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/recordings/track` — Start recording participant audio tracks  · required: account_id, app_id  · body: meeting_id:string
- `GET /accounts/{account_id}/realtime/kit/{app_id}/recordings/{recording_id}` — Fetch details of a recording  · required: account_id, app_id, recording_id
- `PUT /accounts/{account_id}/realtime/kit/{app_id}/recordings/{recording_id}` — Pause/Resume/Stop recording  · required: account_id, app_id, recording_id  · body: action:string
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions` — Fetch all sessions of an App  · required: account_id, app_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/peer-report/{peer_id}` — Fetch details of peer  · required: account_id, app_id, peer_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}` — Fetch details of a session  · required: account_id, app_id, session_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}/chat` — Fetch all chat messages of a session  · required: account_id, app_id, session_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}/livestream-sessions` — Fetch livestream session details using a session ID  · required: account_id, app_id, session_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}/participants` — Fetch participants list of a session  · required: account_id, app_id, session_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}/participants/{participant_id}` — Fetch details of a participant  · required: account_id, app_id, participant_id, session_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}/summary` — Fetch summary of transcripts for a session  · required: account_id, app_id, session_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}/summary` — Generate summary of Transcripts for the session  · required: account_id, app_id, session_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/sessions/{session_id}/transcript` — Fetch the complete transcript for a session  · required: account_id, app_id, session_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/webhooks` — Fetch all webhooks details  · required: account_id, app_id
- `POST /accounts/{account_id}/realtime/kit/{app_id}/webhooks` — Add a webhook  · required: account_id, app_id  · body: events:string[], name:string, url:string
- `GET /accounts/{account_id}/realtime/kit/{app_id}/webhooks/all` — Fetch all supported webhook events  · required: account_id, app_id
- `GET /accounts/{account_id}/realtime/kit/{app_id}/webhooks/{webhook_id}` — Fetch details of a webhook  · required: account_id, app_id, webhook_id
- `PUT /accounts/{account_id}/realtime/kit/{app_id}/webhooks/{webhook_id}` — Replace a webhook  · required: account_id, app_id, webhook_id  · body: events:string[], name:string, url:string
- `PATCH /accounts/{account_id}/realtime/kit/{app_id}/webhooks/{webhook_id}` — Edit a webhook  · required: account_id, app_id, webhook_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/realtime/kit/{app_id}/webhooks/{webhook_id}` — Delete a webhook  · required: account_id, app_id, webhook_id
- `GET /radar/bgp/routes/realtime` — Get real-time BGP routes for a prefix  · required: 
