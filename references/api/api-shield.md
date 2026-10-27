# API reference — api-shield

> Exact REST endpoints for **api-shield**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 44 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /zones/{zone_id}/api_gateway/configuration` — Get session identifier settings  · required: 
- `PUT /zones/{zone_id}/api_gateway/configuration` — Update session identifier settings  · required:   · body: auth_id_characteristics:any[]
- `GET /zones/{zone_id}/api_gateway/discovery` — Export discovered API operations as OpenAPI schemas  · required: 
- `GET /zones/{zone_id}/api_gateway/discovery/operations` — List discovered web and API operations  · required: 
- `PATCH /zones/{zone_id}/api_gateway/discovery/operations` — Edit discovered web and API operations  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/api_gateway/discovery/operations/{discovery_id}` — Get a discovered web or API operation  · required: 
- `PATCH /zones/{zone_id}/api_gateway/discovery/operations/{discovery_id}` — Edit a discovered web or API operation  · required:   · body: (no required fields)
- `POST /zones/{zone_id}/api_gateway/expression-template/fallthrough` — Generate a fallthrough WAF expression template  · required:   · body: hosts:string[]
- `GET /zones/{zone_id}/api_gateway/labels` — List operation labels  · required: 
- `GET /zones/{zone_id}/api_gateway/labels/managed/{name}` — Get a managed operation label  · required: 
- `PUT /zones/{zone_id}/api_gateway/labels/managed/{name}/resources/operation` — Replace operations attached to a managed label  · required:   · body: selector:object
- `POST /zones/{zone_id}/api_gateway/labels/user` — Create user-defined operation labels  · required:   · body: (no required fields)
- `DELETE /zones/{zone_id}/api_gateway/labels/user` — Delete user-defined operation labels  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/api_gateway/labels/user/{name}` — Get a user-defined operation label  · required: 
- `PUT /zones/{zone_id}/api_gateway/labels/user/{name}` — Update a user-defined operation label  · required:   · body: (no required fields)
- `PATCH /zones/{zone_id}/api_gateway/labels/user/{name}` — Edit a user-defined operation label  · required:   · body: (no required fields)
- `DELETE /zones/{zone_id}/api_gateway/labels/user/{name}` — Delete a user-defined operation label  · required: 
- `PUT /zones/{zone_id}/api_gateway/labels/user/{name}/resources/operation` — Replace operations attached to a user-defined label  · required:   · body: selector:object
- `GET /zones/{zone_id}/api_gateway/operations` — List web and API operations  · required: 
- `POST /zones/{zone_id}/api_gateway/operations` — Create web or API operations  · required:   · body: (no required fields)
- `DELETE /zones/{zone_id}/api_gateway/operations` — Delete web or API operations  · required:   · body: (no required fields)
- `POST /zones/{zone_id}/api_gateway/operations/item` — Create a web or API operation  · required:   · body: endpoint:string, host:string, method:string
- `POST /zones/{zone_id}/api_gateway/operations/labels` — Attach labels to web or API operations  · required:   · body: selector:object
- `PUT /zones/{zone_id}/api_gateway/operations/labels` — Replace labels on web or API operations  · required:   · body: managed:object, selector:object, user:object
- `DELETE /zones/{zone_id}/api_gateway/operations/labels` — Remove labels from web or API operations  · required:   · body: selector:object
- `PATCH /zones/{zone_id}/api_gateway/operations/schema_validation` — Update multiple operation-level schema validation settings  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/api_gateway/operations/{operation_id}` — Get a web or API operation  · required: 
- `DELETE /zones/{zone_id}/api_gateway/operations/{operation_id}` — Delete a web or API operation  · required: 
- `POST /zones/{zone_id}/api_gateway/operations/{operation_id}/labels` — Attach labels to a web or API operation  · required:   · body: (no required fields)
- `PUT /zones/{zone_id}/api_gateway/operations/{operation_id}/labels` — Replace labels on a web or API operation  · required:   · body: (no required fields)
- `DELETE /zones/{zone_id}/api_gateway/operations/{operation_id}/labels` — Remove labels from a web or API operation  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/api_gateway/operations/{operation_id}/schema_validation` — Retrieve operation-level schema validation settings  · required: 
- `PUT /zones/{zone_id}/api_gateway/operations/{operation_id}/schema_validation` — Update operation-level schema validation settings  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/api_gateway/schemas` — Export web and API operations as OpenAPI schemas  · required: 
- `GET /zones/{zone_id}/api_gateway/settings/schema_validation` — Retrieve zone level schema validation settings  · required: 
- `PUT /zones/{zone_id}/api_gateway/settings/schema_validation` — Update zone level schema validation settings  · required:   · body: validation_default_mitigation_action:string
- `PATCH /zones/{zone_id}/api_gateway/settings/schema_validation` — Update zone level schema validation settings  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/api_gateway/user_schemas` — Retrieve information about all schemas on a zone  · required: 
- `POST /zones/{zone_id}/api_gateway/user_schemas` — Upload a legacy schema  · required:   · body: file:string, kind:string
- `GET /zones/{zone_id}/api_gateway/user_schemas/hosts` — Retrieve schema hosts in a zone  · required: 
- `GET /zones/{zone_id}/api_gateway/user_schemas/{schema_id}` — Retrieve information about a specific schema on a zone  · required: 
- `PATCH /zones/{zone_id}/api_gateway/user_schemas/{schema_id}` — Enable validation for a schema  · required:   · body: (no required fields)
- `DELETE /zones/{zone_id}/api_gateway/user_schemas/{schema_id}` — Delete a schema  · required: 
- `GET /zones/{zone_id}/api_gateway/user_schemas/{schema_id}/operations` — Retrieve all operations from a schema  · required: 
