# API reference — images

> Exact REST endpoints for **images**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 38 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/images/v1` — List images  · required: account_id
- `POST /accounts/{account_id}/images/v1` — Upload an image  · required: account_id  · body: (no required fields)
- `POST /accounts/{account_id}/images/v1/direct_upload` — Create authenticated direct upload URL V1  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/images/v1/keys` — List Signing Keys  · required: account_id
- `PUT /accounts/{account_id}/images/v1/keys/{signing_key_name}` — Create a new Signing Key  · required: signing_key_name, account_id
- `DELETE /accounts/{account_id}/images/v1/keys/{signing_key_name}` — Delete Signing Key  · required: signing_key_name, account_id
- `GET /accounts/{account_id}/images/v1/stats` — Images usage statistics  · required: account_id
- `GET /accounts/{account_id}/images/v1/variants` — List variants  · required: account_id
- `POST /accounts/{account_id}/images/v1/variants` — Create a variant  · required: account_id  · body: id:string, options:object
- `GET /accounts/{account_id}/images/v1/variants/{variant_id}` — Variant details  · required: variant_id, account_id
- `PATCH /accounts/{account_id}/images/v1/variants/{variant_id}` — Update a variant  · required: variant_id, account_id  · body: options:object
- `DELETE /accounts/{account_id}/images/v1/variants/{variant_id}` — Delete a variant  · required: variant_id, account_id
- `GET /accounts/{account_id}/images/v1/variants/{variant_id}/flat` — Variant details (flat)  · required: variant_id, account_id
- `GET /accounts/{account_id}/images/v1/{image_id}` — Image details  · required: image_id, account_id
- `PATCH /accounts/{account_id}/images/v1/{image_id}` — Update image  · required: image_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/images/v1/{image_id}` — Delete image  · required: image_id, account_id
- `GET /accounts/{account_id}/images/v1/{image_id}/blob` — Download image  · required: image_id, account_id
- `GET /accounts/{account_id}/images/v2` — List images V2  · required: account_id
- `POST /accounts/{account_id}/images/v2/direct_upload` — Create authenticated direct upload URL V2  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/images/v2/metadata/keys` — List image metadata keys  · required: account_id
- `GET /accounts/{account_id}/images/v2/sourcingkit/migrations` — List sourcing kit migrations  · required: account_id
- `POST /accounts/{account_id}/images/v2/sourcingkit/migrations` — Create a sourcing kit migration  · required: account_id  · body: sourceId:string
- `GET /accounts/{account_id}/images/v2/sourcingkit/migrations/{migration_id}` — Get sourcing kit migration  · required: account_id, migration_id
- `DELETE /accounts/{account_id}/images/v2/sourcingkit/migrations/{migration_id}` — Delete a sourcing kit migration  · required: account_id, migration_id
- `GET /accounts/{account_id}/images/v2/sourcingkit/migrations/{migration_id}/lifecycle` — Get migration progress  · required: account_id, migration_id
- `PATCH /accounts/{account_id}/images/v2/sourcingkit/migrations/{migration_id}/lifecycle/abort` — Abort a migration  · required: account_id, migration_id
- `PATCH /accounts/{account_id}/images/v2/sourcingkit/migrations/{migration_id}/lifecycle/start` — Start a migration  · required: account_id, migration_id
- `GET /accounts/{account_id}/images/v2/sourcingkit/migrations/{migration_id}/logs` — List migration logs  · required: account_id, migration_id
- `GET /accounts/{account_id}/images/v2/sourcingkit/sources` — List sourcing kit sources  · required: account_id
- `POST /accounts/{account_id}/images/v2/sourcingkit/sources` — Create a sourcing kit source  · required: account_id  · body: bucket:string, name:string, secret:object, vendor:string
- `POST /accounts/{account_id}/images/v2/sourcingkit/sources/connectivity-precheck` — Precheck source connectivity  · required: account_id  · body: bucket:string, secret:object, vendor:string
- `GET /accounts/{account_id}/images/v2/sourcingkit/sources/{source_id}` — Get sourcing kit source  · required: account_id, source_id
- `PATCH /accounts/{account_id}/images/v2/sourcingkit/sources/{source_id}` — Update a sourcing kit source  · required: account_id, source_id  · body: name:string
- `DELETE /accounts/{account_id}/images/v2/sourcingkit/sources/{source_id}` — Delete a sourcing kit source  · required: account_id, source_id
- `GET /accounts/{account_id}/images/v2/sourcingkit/sources/{source_id}/connectivity` — Get source connectivity status  · required: account_id, source_id
- `GET /accounts/{account_id}/settings/transformations` — List Image Resizing configurations for account  · required: account_id
- `GET /accounts/{account_id}/settings/ut-billing` — Get Unique Transformations billing setting  · required: account_id
- `PATCH /accounts/{account_id}/settings/ut-billing` — Change Unique Transformations billing setting  · required: account_id  · body: value:string
