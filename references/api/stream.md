# API reference — stream

> Exact REST endpoints for **stream**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 50 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/stream` — List videos  · required: account_id
- `POST /accounts/{account_id}/stream` — Initiate video uploads using TUS  · required: Tus-Resumable, Upload-Length, account_id
- `POST /accounts/{account_id}/stream/clip` — Clip videos given a start and end time  · required: account_id  · body: clippedFromVideoUID:string, endTimeSeconds:integer, startTimeSeconds:integer
- `POST /accounts/{account_id}/stream/copy` — Upload videos from a URL  · required: account_id  · body: input:any
- `POST /accounts/{account_id}/stream/direct_upload` — Upload videos via direct upload URLs  · required: account_id  · body: maxDurationSeconds:integer
- `GET /accounts/{account_id}/stream/keys` — List signing keys  · required: account_id
- `POST /accounts/{account_id}/stream/keys` — Create signing keys  · required: account_id
- `DELETE /accounts/{account_id}/stream/keys/{identifier}` — Delete signing keys  · required: identifier, account_id
- `GET /accounts/{account_id}/stream/live_inputs` — List live inputs  · required: account_id
- `POST /accounts/{account_id}/stream/live_inputs` — Create a live input  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/stream/live_inputs/{live_input_identifier}` — Retrieve a live input  · required: live_input_identifier, account_id
- `PUT /accounts/{account_id}/stream/live_inputs/{live_input_identifier}` — Update a live input  · required: live_input_identifier, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/stream/live_inputs/{live_input_identifier}` — Delete a live input  · required: live_input_identifier, account_id
- `POST /accounts/{account_id}/stream/live_inputs/{live_input_identifier}/disable` — Disable a live input  · required: live_input_identifier, account_id
- `POST /accounts/{account_id}/stream/live_inputs/{live_input_identifier}/enable` — Enable a live input  · required: live_input_identifier, account_id
- `GET /accounts/{account_id}/stream/live_inputs/{live_input_identifier}/outputs` — List all outputs associated with a specified live input  · required: live_input_identifier, account_id
- `POST /accounts/{account_id}/stream/live_inputs/{live_input_identifier}/outputs` — Create a new output, connected to a live input  · required: live_input_identifier, account_id  · body: streamKey:string, url:string
- `PUT /accounts/{account_id}/stream/live_inputs/{live_input_identifier}/outputs/{output_identifier}` — Update an output  · required: output_identifier, live_input_identifier, account_id  · body: enabled:boolean
- `DELETE /accounts/{account_id}/stream/live_inputs/{live_input_identifier}/outputs/{output_identifier}` — Delete an output  · required: output_identifier, live_input_identifier, account_id
- `POST /accounts/{account_id}/stream/live_inputs/{live_input_identifier}/rotate_keys` — Rotate keys for a live input  · required: live_input_identifier, account_id
- `GET /accounts/{account_id}/stream/storage-usage` — Storage use  · required: account_id
- `GET /accounts/{account_id}/stream/usage` — Get account Stream usage  · required: 
- `GET /accounts/{account_id}/stream/watermarks` — List watermark profiles  · required: account_id
- `POST /accounts/{account_id}/stream/watermarks` — Create watermark profiles via basic upload  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/stream/watermarks/{identifier}` — Watermark profile details  · required: identifier, account_id
- `DELETE /accounts/{account_id}/stream/watermarks/{identifier}` — Delete watermark profiles  · required: identifier, account_id
- `GET /accounts/{account_id}/stream/webhook` — View webhook  · required: account_id
- `PUT /accounts/{account_id}/stream/webhook` — Create VOD webhooks  · required: account_id  · body: notificationUrl:any
- `DELETE /accounts/{account_id}/stream/webhook` — Delete webhooks  · required: account_id
- `GET /accounts/{account_id}/stream/{identifier}` — Retrieve video details  · required: identifier, account_id
- `POST /accounts/{account_id}/stream/{identifier}` — Edit video details  · required: identifier, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/stream/{identifier}` — Delete video  · required: identifier, account_id
- `GET /accounts/{account_id}/stream/{identifier}/audio` — List additional audio tracks on a video  · required: account_id, identifier
- `POST /accounts/{account_id}/stream/{identifier}/audio/copy` — Add audio tracks to a video  · required: account_id, identifier  · body: label:string
- `PATCH /accounts/{account_id}/stream/{identifier}/audio/{audio_identifier}` — Edit additional audio tracks on a video  · required: account_id, identifier, audio_identifier  · body: (no required fields)
- `DELETE /accounts/{account_id}/stream/{identifier}/audio/{audio_identifier}` — Delete additional audio tracks on a video  · required: account_id, identifier, audio_identifier
- `GET /accounts/{account_id}/stream/{identifier}/captions` — List captions or subtitles  · required: identifier, account_id
- `GET /accounts/{account_id}/stream/{identifier}/captions/{language}` — List captions or subtitles for a provided language  · required: language, identifier, account_id
- `PUT /accounts/{account_id}/stream/{identifier}/captions/{language}` — Upload captions or subtitles  · required: language, identifier, account_id  · body: file:string
- `DELETE /accounts/{account_id}/stream/{identifier}/captions/{language}` — Delete captions or subtitles  · required: language, identifier, account_id
- `POST /accounts/{account_id}/stream/{identifier}/captions/{language}/generate` — Generate captions or subtitles for a provided language via AI  · required: language, identifier, account_id
- `GET /accounts/{account_id}/stream/{identifier}/captions/{language}/vtt` — Return WebVTT captions for a provided language  · required: language, identifier, account_id
- `GET /accounts/{account_id}/stream/{identifier}/downloads` — List downloads  · required: identifier, account_id
- `POST /accounts/{account_id}/stream/{identifier}/downloads` — Create downloads  · required: identifier, account_id
- `DELETE /accounts/{account_id}/stream/{identifier}/downloads` — Delete downloads  · required: identifier, account_id
- `POST /accounts/{account_id}/stream/{identifier}/downloads/{download_type}` — Create download  · required: identifier, account_id, download_type
- `DELETE /accounts/{account_id}/stream/{identifier}/downloads/{download_type}` — Delete download  · required: identifier, account_id, download_type
- `GET /accounts/{account_id}/stream/{identifier}/embed` — Deprecated: Retrieve legacy embed code HTML  · required: identifier, account_id
- `POST /accounts/{account_id}/stream/{identifier}/token` — Create signed URL tokens for videos  · required: identifier, account_id  · body: (no required fields)
- `GET /zones/{zone_id}/stream/usage` — Get zone Stream usage  · required: 
