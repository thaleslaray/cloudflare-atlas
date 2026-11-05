# API reference — durable-objects

> Exact REST endpoints for **durable-objects**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 3 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/workers/durable_objects/namespaces` — List Durable Object Namespaces  · required: account_id
- `GET /accounts/{account_id}/workers/durable_objects/namespaces/{id}/objects` — List Objects in a Durable Object namespace  · required: account_id, id
- `POST /accounts/{account_id}/workers/durable_objects/namespaces/{id}/query/v2` — Query a Durable Object  · required: account_id, id  · body: durable_object_id:string, queries:object[]
