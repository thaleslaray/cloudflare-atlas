# API reference — queues

> Exact REST endpoints for **queues**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 23 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/queues` — List Queues  · required: account_id
- `POST /accounts/{account_id}/queues` — Create Queue  · required: account_id  · body: queue_name:string
- `GET /accounts/{account_id}/queues/{queue_id}` — Get Queue  · required: queue_id, account_id
- `PUT /accounts/{account_id}/queues/{queue_id}` — Update Queue  · required: queue_id, account_id  · body: (no required fields)
- `PATCH /accounts/{account_id}/queues/{queue_id}` — Update Queue  · required: queue_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/queues/{queue_id}` — Delete Queue  · required: queue_id, account_id
- `GET /accounts/{account_id}/queues/{queue_id}/consumers` — List Queue Consumers  · required: queue_id, account_id
- `POST /accounts/{account_id}/queues/{queue_id}/consumers` — Create a Queue Consumer  · required: queue_id, account_id  · body: script_name:string, type:string
- `GET /accounts/{account_id}/queues/{queue_id}/consumers/{consumer_id}` — Get Queue Consumer  · required: consumer_id, queue_id, account_id
- `PUT /accounts/{account_id}/queues/{queue_id}/consumers/{consumer_id}` — Update Queue Consumer  · required: consumer_id, queue_id, account_id  · body: script_name:string, type:string
- `DELETE /accounts/{account_id}/queues/{queue_id}/consumers/{consumer_id}` — Delete Queue Consumer  · required: consumer_id, queue_id, account_id
- `POST /accounts/{account_id}/queues/{queue_id}/messages` — Push Message  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/ack` — Acknowledge + Retry Queue Messages  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/batch` — Push Message Batch  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/extend` — Extend Message Leases  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/peek` — Peek Queue Messages  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/preview` — Preview Queue Messages  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/preview/ack` — Delete Previewed Queue Messages  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/pull` — Pull Queue Messages  · required: queue_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/queues/{queue_id}/messages/purge` — Purge Peeked Queue Messages  · required: queue_id, account_id  · body: refs:object[]
- `GET /accounts/{account_id}/queues/{queue_id}/metrics` — Get Queue Metrics  · required: queue_id, account_id
- `GET /accounts/{account_id}/queues/{queue_id}/purge` — Get Queue Purge Status  · required: queue_id, account_id
- `POST /accounts/{account_id}/queues/{queue_id}/purge` — Purge Queue  · required: queue_id, account_id  · body: (no required fields)
