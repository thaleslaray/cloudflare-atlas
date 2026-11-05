# API reference — kv

> Exact REST endpoints for **kv**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 14 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/storage/kv/namespaces` — List namespaces  · required: account_id
- `POST /accounts/{account_id}/storage/kv/namespaces` — Create a namespace  · required: account_id  · body: title:string
- `GET /accounts/{account_id}/storage/kv/namespaces/{namespace_id}` — Get a namespace  · required: namespace_id, account_id
- `PUT /accounts/{account_id}/storage/kv/namespaces/{namespace_id}` — Rename a namespace  · required: namespace_id, account_id  · body: title:string
- `DELETE /accounts/{account_id}/storage/kv/namespaces/{namespace_id}` — Delete a namespace  · required: namespace_id, account_id
- `PUT /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk` — Write multiple key-value pairs  · required: namespace_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk` — Delete multiple key-value pairs  · required: namespace_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk/delete` — Delete multiple key-value pairs  · required: namespace_id, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk/get` — Get multiple key-value pairs  · required: namespace_id, account_id  · body: keys:string[]
- `GET /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/keys` — List keys in a namespace  · required: namespace_id, account_id
- `GET /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/metadata/{key_name}` — Get a key's metadata  · required: key_name, namespace_id, account_id
- `GET /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}` — Get a key's value  · required: key_name, namespace_id, account_id
- `PUT /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}` — Write a key-value pair with optional metadata  · required: key_name, namespace_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}` — Delete a key-value pair  · required: key_name, namespace_id, account_id
