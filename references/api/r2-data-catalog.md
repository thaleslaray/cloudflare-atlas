# API reference — r2-data-catalog

> Exact REST endpoints for **r2-data-catalog**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 15 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: the REST prefix is `r2-catalog`, not `r2-data-catalog`. The Iceberg REST catalog itself
> (the endpoint your query engine talks to) is a **different API** from these management endpoints —
> do not conflate them; see `products/r2-data-catalog.md` for the catalog URI and warehouse name.

- `GET /accounts/{account_id}/r2-catalog` — List R2 catalogs  · required: account_id
- `GET /accounts/{account_id}/r2-catalog/{bucket_name}` — Get R2 catalog details  · required: account_id, bucket_name
- `POST /accounts/{account_id}/r2-catalog/{bucket_name}/credential` — Store catalog credentials  · required: account_id, bucket_name  · body: token:string
- `POST /accounts/{account_id}/r2-catalog/{bucket_name}/delete` — Delete R2 catalog metadata  · required: account_id, bucket_name
- `POST /accounts/{account_id}/r2-catalog/{bucket_name}/disable` — Disable R2 catalog  · required: account_id, bucket_name
- `POST /accounts/{account_id}/r2-catalog/{bucket_name}/enable` — Enable R2 bucket as a catalog  · required: account_id, bucket_name
- `GET /accounts/{account_id}/r2-catalog/{bucket_name}/maintenance-configs` — Get catalog maintenance configuration  · required: account_id, bucket_name
- `POST /accounts/{account_id}/r2-catalog/{bucket_name}/maintenance-configs` — Update catalog maintenance configuration  · required: account_id, bucket_name  · body: (no required fields)
- `GET /accounts/{account_id}/r2-catalog/{bucket_name}/namespaces` — List namespaces in catalog  · required: account_id, bucket_name
- `GET /accounts/{account_id}/r2-catalog/{bucket_name}/namespaces/{namespace}/tables` — List tables in namespace  · required: account_id, bucket_name, namespace
- `GET /accounts/{account_id}/r2-catalog/{bucket_name}/namespaces/{namespace}/tables/{table_name}` — Get table details  · required: account_id, bucket_name, namespace, table_name
- `GET /accounts/{account_id}/r2-catalog/{bucket_name}/namespaces/{namespace}/tables/{table_name}/maintenance-configs` — Get table maintenance configuration  · required: account_id, bucket_name, namespace, table_name
- `POST /accounts/{account_id}/r2-catalog/{bucket_name}/namespaces/{namespace}/tables/{table_name}/maintenance-configs` — Update table maintenance configuration  · required: account_id, bucket_name, namespace, table_name  · body: (no required fields)
- `POST /accounts/{account_id}/r2-catalog/{bucket_name}/namespaces/{namespace}/tables/{table_name}/maintenance-configs/{configuration_type}/queue` — Queue table maintenance  · required: account_id, bucket_name, namespace, table_name, configuration_type  · body: (no required fields)
- `GET /accounts/{account_id}/r2-catalog/{bucket_name}/namespaces/{namespace}/tables/{table_name}/maintenance-runs` — List table maintenance runs  · required: account_id, bucket_name, namespace, table_name
