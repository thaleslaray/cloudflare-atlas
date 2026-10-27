# API reference — tenant

> Exact REST endpoints for **tenant**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 9 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /tenants/{tenant_id}` — Get tenant  · required: tenant_id
- `GET /tenants/{tenant_id}/account_types` — Get tenant account types  · required: tenant_id
- `GET /tenants/{tenant_id}/accounts` — List tenant accounts  · required: tenant_id
- `GET /tenants/{tenant_id}/entitlements` — List tenant entitlements  · required: tenant_id
- `GET /tenants/{tenant_id}/memberships` — List tenant memberships  · required: tenant_id
- `GET /tenants/{tenant_tag}/custom_ns` — List Tenant Custom Nameservers  · required: tenant_tag
- `POST /tenants/{tenant_tag}/custom_ns` — Add Tenant Custom Nameserver  · required: tenant_tag  · body: ns_name:string
- `DELETE /tenants/{tenant_tag}/custom_ns/{custom_ns_id}` — Delete Tenant Custom Nameserver  · required: custom_ns_id, tenant_tag
- `GET /user/tenants` — List user tenants  · required: 
