# API reference — vectorize

> Exact REST endpoints for **vectorize**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 24 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/vectorize/indexes` — List Vectorize Indexes (Deprecated)  · required: account_id
- `POST /accounts/{account_id}/vectorize/indexes` — Create Vectorize Index (Deprecated)  · required: account_id  · body: config:object, name:string
- `GET /accounts/{account_id}/vectorize/indexes/{index_name}` — Get Vectorize Index (Deprecated)  · required: account_id, index_name
- `PUT /accounts/{account_id}/vectorize/indexes/{index_name}` — Update Vectorize Index (Deprecated)  · required: account_id, index_name  · body: description:string
- `DELETE /accounts/{account_id}/vectorize/indexes/{index_name}` — Delete Vectorize Index (Deprecated)  · required: account_id, index_name
- `POST /accounts/{account_id}/vectorize/indexes/{index_name}/delete-by-ids` — Delete Vectors By Identifier (Deprecated)  · required: account_id, index_name  · body: (no required fields)
- `POST /accounts/{account_id}/vectorize/indexes/{index_name}/get-by-ids` — Get Vectors By Identifier (Deprecated)  · required: account_id, index_name  · body: (no required fields)
- `POST /accounts/{account_id}/vectorize/indexes/{index_name}/insert` — Insert Vectors (Deprecated)  · required: account_id, index_name  · body: (no required fields)
- `POST /accounts/{account_id}/vectorize/indexes/{index_name}/query` — Query Vectors (Deprecated)  · required: account_id, index_name  · body: vector:number[]
- `POST /accounts/{account_id}/vectorize/indexes/{index_name}/upsert` — Upsert Vectors (Deprecated)  · required: account_id, index_name  · body: (no required fields)
- `GET /accounts/{account_id}/vectorize/v2/indexes` — List Vectorize Indexes  · required: account_id
- `POST /accounts/{account_id}/vectorize/v2/indexes` — Create Vectorize Index  · required: account_id  · body: config:object, name:string
- `GET /accounts/{account_id}/vectorize/v2/indexes/{index_name}` — Get Vectorize Index  · required: account_id, index_name
- `DELETE /accounts/{account_id}/vectorize/v2/indexes/{index_name}` — Delete Vectorize Index  · required: account_id, index_name
- `POST /accounts/{account_id}/vectorize/v2/indexes/{index_name}/delete_by_ids` — Delete Vectors By Identifier  · required: account_id, index_name  · body: (no required fields)
- `POST /accounts/{account_id}/vectorize/v2/indexes/{index_name}/get_by_ids` — Get Vectors By Identifier  · required: account_id, index_name  · body: (no required fields)
- `GET /accounts/{account_id}/vectorize/v2/indexes/{index_name}/info` — Get Vectorize Index Info  · required: account_id, index_name
- `POST /accounts/{account_id}/vectorize/v2/indexes/{index_name}/insert` — Insert Vectors  · required: account_id, index_name  · body: (no required fields)
- `GET /accounts/{account_id}/vectorize/v2/indexes/{index_name}/list` — List Vectors  · required: account_id, index_name
- `POST /accounts/{account_id}/vectorize/v2/indexes/{index_name}/metadata_index/create` — Create Metadata Index  · required: account_id, index_name  · body: indexType:string, propertyName:string
- `POST /accounts/{account_id}/vectorize/v2/indexes/{index_name}/metadata_index/delete` — Delete Metadata Index  · required: account_id, index_name  · body: propertyName:string
- `GET /accounts/{account_id}/vectorize/v2/indexes/{index_name}/metadata_index/list` — List Metadata Indexes  · required: account_id, index_name
- `POST /accounts/{account_id}/vectorize/v2/indexes/{index_name}/query` — Query Vectors  · required: account_id, index_name  · body: vector:number[]
- `POST /accounts/{account_id}/vectorize/v2/indexes/{index_name}/upsert` — Upsert Vectors  · required: account_id, index_name  · body: (no required fields)
