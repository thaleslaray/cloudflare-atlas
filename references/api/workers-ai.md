# API reference — workers-ai

> Exact REST endpoints for **workers-ai**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 14 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

> Note: the spec used to enumerate 114 per-model paths (`/ai/run/@cf/meta/llama-...`); they were
> collapsed into one parameterized `/ai/run/{model_name}` on 2026-08-08. **The resulting −114 is an
> API change, not data loss from this slice.** Model names come from `GET /ai/models/search` or
> `products/workers-ai.md`, not from this file.

- `GET /accounts/{account_id}/ai/authors/search` — Author Search  · required: account_id
- `GET /accounts/{account_id}/ai/finetunes` — List Finetunes  · required: account_id
- `POST /accounts/{account_id}/ai/finetunes` — Create a new Finetune  · required: account_id  · body: model:string, name:string
- `GET /accounts/{account_id}/ai/finetunes/public` — List Public Finetunes  · required: account_id
- `DELETE /accounts/{account_id}/ai/finetunes/{finetune_id}` — Delete a Finetune  · required: account_id, finetune_id
- `POST /accounts/{account_id}/ai/finetunes/{finetune_id}/finetune-assets` — Upload a Finetune Asset  · required: account_id, finetune_id  · body: file:string, file_name:string
- `GET /accounts/{account_id}/ai/finetunes/{finetune_id}/finetune-assets/{file_name}` — Download a Finetune Asset  · required: account_id, finetune_id, file_name
- `GET /accounts/{account_id}/ai/models/schema` — Get Model Schema  · required: account_id, model
- `GET /accounts/{account_id}/ai/models/search` — Model Search  · required: account_id
- `POST /accounts/{account_id}/ai/run` — Execute AI Model (Generic)  · required: account_id  · body: input:object, model:string
- `POST /accounts/{account_id}/ai/run/{model_name}` — Execute AI model  · required: account_id, model_name  · body: text:string
- `GET /accounts/{account_id}/ai/tasks/search` — Task Search  · required: account_id
- `POST /accounts/{account_id}/ai/tomarkdown` — Convert Files into Markdown  · required: account_id  · body: files:string[]
- `GET /accounts/{account_id}/ai/tomarkdown/supported` — Get all converted formats supported  · required: account_id
