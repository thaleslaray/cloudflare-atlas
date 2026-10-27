# API reference — ai-gateway

> Exact REST endpoints for **ai-gateway**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 66 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/ai-gateway/billing/credit-balance` — Get credit balance  · required: account_id
- `GET /accounts/{account_id}/ai-gateway/billing/invoice-history` — Get invoice history  · required: account_id
- `GET /accounts/{account_id}/ai-gateway/billing/invoice-preview` — Get invoice preview  · required: account_id
- `GET /accounts/{account_id}/ai-gateway/billing/spending-limit` — Get spending limit  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/billing/spending-limit` — Set spending limit (deprecated)  · required: account_id  · body: amount:integer, duration:string, strategy:string
- `DELETE /accounts/{account_id}/ai-gateway/billing/spending-limit` — Delete spending limit  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/billing/topup` — Create a top-up  · required: account_id  · body: amount:integer
- `GET /accounts/{account_id}/ai-gateway/billing/topup/config` — Get auto top-up configuration  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/billing/topup/config` — Set auto top-up configuration  · required: account_id  · body: amount:integer, threshold:integer
- `DELETE /accounts/{account_id}/ai-gateway/billing/topup/config` — Delete auto top-up configuration  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/billing/topup/eligibility` — Get top-up eligibility  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/ai-gateway/billing/topup/limits` — Get account top-up limits  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/billing/topup/status` — Check top-up status  · required: account_id  · body: payment_intent_id:string
- `GET /accounts/{account_id}/ai-gateway/billing/usage-history` — Get usage history  · required: account_id, value_grouping_window
- `GET /accounts/{account_id}/ai-gateway/custom-providers` — List Account Providers  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/custom-providers` — Create a new Account Provider  · required: account_id  · body: base_url:string, name:string, slug:string
- `GET /accounts/{account_id}/ai-gateway/custom-providers/costs` — List Account Provider Costs  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/custom-providers/costs` — Create a new Account Provider Cost  · required: account_id  · body: account_provider_id:string, model:string
- `GET /accounts/{account_id}/ai-gateway/custom-providers/costs/{id}` — Fetch a Account Provider Cost  · required: account_id, id
- `PATCH /accounts/{account_id}/ai-gateway/custom-providers/costs/{id}` — Update a Account Provider Cost  · required: account_id, id  · body: (no required fields)
- `DELETE /accounts/{account_id}/ai-gateway/custom-providers/costs/{id}` — Delete a Account Provider Cost  · required: account_id, id
- `GET /accounts/{account_id}/ai-gateway/custom-providers/{id}` — Fetch a Account Provider  · required: account_id, id
- `PATCH /accounts/{account_id}/ai-gateway/custom-providers/{id}` — Update a Account Provider  · required: account_id, id  · body: (no required fields)
- `DELETE /accounts/{account_id}/ai-gateway/custom-providers/{id}` — Delete a Account Provider  · required: account_id, id
- `GET /accounts/{account_id}/ai-gateway/evaluation-types` — List Evaluators  · required: account_id
- `GET /accounts/{account_id}/ai-gateway/gateways` — List Gateways  · required: account_id
- `POST /accounts/{account_id}/ai-gateway/gateways` — Create a new Gateway  · required: account_id  · body: cache_invalidate_on_update:boolean, cache_ttl:integer, collect_logs:boolean, id:string, rate_limiting_interval:integer, rate_limiting_limit:integer
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/custom-domains` — List Custom Domains  · required: account_id, gateway_id
- `POST /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/custom-domains` — Create a custom domain for a gateway  · required: account_id, gateway_id  · body: domain:string, zone_id:string
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/custom-domains/{hostname}` — Fetch a Custom Domain  · required: account_id, gateway_id, hostname
- `DELETE /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/custom-domains/{hostname}` — Delete a Custom Domain  · required: account_id, gateway_id, hostname
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/datasets` — List Datasets  · required: account_id, gateway_id
- `POST /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/datasets` — Create a new Dataset  · required: gateway_id, account_id  · body: enable:boolean, filters:object[], name:string
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/datasets/{id}` — Fetch a Dataset  · required: account_id, gateway_id, id
- `PUT /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/datasets/{id}` — Update a Dataset  · required: account_id, gateway_id, id  · body: enable:boolean, filters:object[], name:string
- `DELETE /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/datasets/{id}` — Delete a Dataset  · required: account_id, gateway_id, id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/evaluations` — List Evaluations  · required: account_id, gateway_id
- `POST /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/evaluations` — Create a new Evaluation  · required: gateway_id, account_id  · body: dataset_ids:string[], evaluation_type_ids:string[], name:string
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/evaluations/{id}` — Fetch a Evaluation  · required: account_id, gateway_id, id
- `DELETE /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/evaluations/{id}` — Delete a Evaluation  · required: account_id, gateway_id, id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/logs` — List Gateway Logs  · required: account_id, gateway_id
- `DELETE /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/logs` — Delete Gateway Logs  · required: account_id, gateway_id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/logs/{id}` — Get Gateway Log Detail  · required: id, gateway_id, account_id
- `PATCH /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/logs/{id}` — Patch Gateway Log  · required: id, gateway_id, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/logs/{id}/request` — Get Gateway Log Request  · required: id, gateway_id, account_id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/logs/{id}/response` — Get Gateway Log Response  · required: id, gateway_id, account_id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/provider_configs` — List Provider Configs  · required: account_id, gateway_id
- `POST /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/provider_configs` — Create a new Provider Configs  · required: account_id, gateway_id  · body: alias:string, default_config:boolean, provider_slug:string
- `PUT /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/provider_configs/{id}` — Update a Provider Configs  · required: account_id, gateway_id, id  · body: secret:string
- `DELETE /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/provider_configs/{id}` — Delete a Provider Configs  · required: account_id, gateway_id, id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes` — List all AI Gateway Dynamic Routes.  · required: account_id, gateway_id
- `POST /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes` — Create a new AI Gateway Dynamic Route.  · required: account_id, gateway_id  · body: elements:object[], name:string
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}` — Get an AI Gateway Dynamic Route.  · required: account_id, gateway_id, id
- `PATCH /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}` — Update an AI Gateway Dynamic Route.  · required: account_id, gateway_id, id  · body: name:string
- `DELETE /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}` — Delete an AI Gateway Dynamic Route.  · required: account_id, gateway_id, id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}/deployments` — List all AI Gateway Dynamic Route Deployments.  · required: account_id, gateway_id, id
- `POST /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}/deployments` — Create a new AI Gateway Dynamic Route Deployment.  · required: account_id, gateway_id, id  · body: version_id:string
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}/versions` — List all AI Gateway Dynamic Route Versions.  · required: account_id, gateway_id, id
- `POST /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}/versions` — Create a new AI Gateway Dynamic Route Version.  · required: account_id, gateway_id, id  · body: elements:object[]
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/routes/{id}/versions/{version_id}` — Get an AI Gateway Dynamic Route Version.  · required: account_id, gateway_id, id, version_id
- `GET /accounts/{account_id}/ai-gateway/gateways/{gateway_id}/url/{provider}` — Get Gateway URL  · required: gateway_id, account_id, provider
- `GET /accounts/{account_id}/ai-gateway/gateways/{id}` — Fetch a Gateway  · required: account_id, id
- `PUT /accounts/{account_id}/ai-gateway/gateways/{id}` — Update a Gateway  · required: account_id, id  · body: cache_invalidate_on_update:boolean, cache_ttl:integer, collect_logs:boolean, rate_limiting_interval:integer, rate_limiting_limit:integer
- `DELETE /accounts/{account_id}/ai-gateway/gateways/{id}` — Delete a Gateway  · required: account_id, id
- `GET /accounts/{account_id}/ai-gateway/logging-state` — Get AI Gateway logging state  · required: account_id
- `PATCH /accounts/{account_id}/ai-gateway/logging-state` — Migrate AI Gateway logging to Workers Observability  · required: account_id
