# API reference — waiting-room

> Exact REST endpoints for **waiting-room**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 24 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/waiting_rooms` — List waiting rooms for account  · required: account_id
- `GET /zones/{zone_id}/waiting_rooms` — List waiting rooms for zone  · required: zone_id
- `POST /zones/{zone_id}/waiting_rooms` — Create waiting room  · required: zone_id  · body: host:string, name:string, new_users_per_minute:integer, total_active_users:integer
- `POST /zones/{zone_id}/waiting_rooms/preview` — Create a custom waiting room page preview  · required: zone_id  · body: custom_html:string
- `GET /zones/{zone_id}/waiting_rooms/settings` — Get zone-level Waiting Room settings  · required: zone_id
- `PUT /zones/{zone_id}/waiting_rooms/settings` — Update zone-level Waiting Room settings  · required: zone_id  · body: (no required fields)
- `PATCH /zones/{zone_id}/waiting_rooms/settings` — Patch zone-level Waiting Room settings  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/waiting_rooms/{waiting_room_id}` — Waiting room details  · required: waiting_room_id, zone_id
- `PUT /zones/{zone_id}/waiting_rooms/{waiting_room_id}` — Update waiting room  · required: waiting_room_id, zone_id  · body: host:string, name:string, new_users_per_minute:integer, total_active_users:integer
- `PATCH /zones/{zone_id}/waiting_rooms/{waiting_room_id}` — Patch waiting room  · required: waiting_room_id, zone_id  · body: host:string, name:string, new_users_per_minute:integer, total_active_users:integer
- `DELETE /zones/{zone_id}/waiting_rooms/{waiting_room_id}` — Delete waiting room  · required: waiting_room_id, zone_id  · body: (spec carries no schema — check the docs)
- `GET /zones/{zone_id}/waiting_rooms/{waiting_room_id}/events` — List events  · required: waiting_room_id, zone_id
- `POST /zones/{zone_id}/waiting_rooms/{waiting_room_id}/events` — Create event  · required: waiting_room_id, zone_id  · body: event_end_time:string, event_start_time:string, name:string
- `GET /zones/{zone_id}/waiting_rooms/{waiting_room_id}/events/{event_id}` — Event details  · required: event_id, waiting_room_id, zone_id
- `PUT /zones/{zone_id}/waiting_rooms/{waiting_room_id}/events/{event_id}` — Update event  · required: event_id, waiting_room_id, zone_id  · body: event_end_time:string, event_start_time:string, name:string
- `PATCH /zones/{zone_id}/waiting_rooms/{waiting_room_id}/events/{event_id}` — Patch event  · required: event_id, waiting_room_id, zone_id  · body: event_end_time:string, event_start_time:string, name:string
- `DELETE /zones/{zone_id}/waiting_rooms/{waiting_room_id}/events/{event_id}` — Delete event  · required: event_id, waiting_room_id, zone_id  · body: (spec carries no schema — check the docs)
- `GET /zones/{zone_id}/waiting_rooms/{waiting_room_id}/events/{event_id}/details` — Preview active event details  · required: event_id, waiting_room_id, zone_id
- `GET /zones/{zone_id}/waiting_rooms/{waiting_room_id}/rules` — List Waiting Room Rules  · required: waiting_room_id, zone_id
- `POST /zones/{zone_id}/waiting_rooms/{waiting_room_id}/rules` — Create Waiting Room Rule  · required: waiting_room_id, zone_id  · body: action:string, expression:string
- `PUT /zones/{zone_id}/waiting_rooms/{waiting_room_id}/rules` — Replace Waiting Room Rules  · required: waiting_room_id, zone_id  · body: (no required fields)
- `PATCH /zones/{zone_id}/waiting_rooms/{waiting_room_id}/rules/{rule_id}` — Patch Waiting Room Rule  · required: rule_id, waiting_room_id, zone_id  · body: action:string, expression:string
- `DELETE /zones/{zone_id}/waiting_rooms/{waiting_room_id}/rules/{rule_id}` — Delete Waiting Room Rule  · required: rule_id, waiting_room_id, zone_id  · body: (spec carries no schema — check the docs)
- `GET /zones/{zone_id}/waiting_rooms/{waiting_room_id}/status` — Get waiting room status  · required: waiting_room_id, zone_id
