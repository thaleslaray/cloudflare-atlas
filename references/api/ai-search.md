# API reference — ai-search

> Exact REST endpoints for **ai-search**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 56 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/ai-search/instances` — List AI Search instances.  · required: account_id
- `POST /accounts/{account_id}/ai-search/instances` — Create an AI Search instance.  · required: account_id  · body: id:string
- `GET /accounts/{account_id}/ai-search/instances/{id}` — Get an AI Search instance.  · required: account_id, id
- `PUT /accounts/{account_id}/ai-search/instances/{id}` — Update an AI Search instance.  · required: account_id, id  · body: (no required fields)
- `DELETE /accounts/{account_id}/ai-search/instances/{id}` — Delete an AI Search instance.  · required: account_id, id
- `POST /accounts/{account_id}/ai-search/instances/{id}/chat/completions` — Chat Completions  · required: id, account_id  · body: messages:object[]
- `GET /accounts/{account_id}/ai-search/instances/{id}/jobs` — List Jobs  · required: id, account_id
- `POST /accounts/{account_id}/ai-search/instances/{id}/jobs` — Create new job  · required: id, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/ai-search/instances/{id}/jobs/{job_id}` — Get a Job Details  · required: id, job_id, account_id
- `PATCH /accounts/{account_id}/ai-search/instances/{id}/jobs/{job_id}` — Cancel an indexing job.  · required: id, job_id, account_id  · body: action:string
- `GET /accounts/{account_id}/ai-search/instances/{id}/jobs/{job_id}/logs` — List Job Logs  · required: id, job_id, account_id
- `POST /accounts/{account_id}/ai-search/instances/{id}/search` — Search  · required: id, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/ai-search/instances/{id}/stats` — Get instance statistics.  · required: id, account_id
- `GET /accounts/{account_id}/ai-search/namespaces` — List namespaces  · required: account_id
- `POST /accounts/{account_id}/ai-search/namespaces` — Create a namespace  · required: account_id  · body: name:string
- `GET /accounts/{account_id}/ai-search/namespaces/{name}` — Get a namespace  · required: account_id, name
- `PUT /accounts/{account_id}/ai-search/namespaces/{name}` — Update a namespace  · required: account_id, name  · body: (no required fields)
- `DELETE /accounts/{account_id}/ai-search/namespaces/{name}` — Delete a namespace  · required: account_id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/chat/completions` — Multi-Instance Chat Completions  · required: account_id, name  · body: ai_search_options:object, messages:object[]
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances` — List AI Search instances.  · required: account_id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/instances` — Create an AI Search instance.  · required: account_id, name  · body: id:string
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}` — Get an AI Search instance.  · required: account_id, id, name
- `PUT /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}` — Update an AI Search instance.  · required: account_id, id, name  · body: (no required fields)
- `PATCH /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}` — Move an instance to a different namespace.  · required: account_id, name, id  · body: new_namespace:string
- `DELETE /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}` — Delete an AI Search instance.  · required: account_id, id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/chat/completions` — Chat Completions  · required: id, account_id, name  · body: messages:object[]
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items` — Items List.  · required: id, account_id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items` — Upload Item.  · required: id, account_id, name  · body: file:string
- `PUT /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items` — Create or Update Item.  · required: id, account_id, name  · body: key:string, next_action:string
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items/{item_id}` — Get Item.  · required: id, item_id, account_id, name
- `PATCH /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items/{item_id}` — Sync Item.  · required: id, item_id, account_id, name  · body: next_action:string
- `DELETE /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items/{item_id}` — Delete Item.  · required: id, item_id, account_id, name
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items/{item_id}/chunks` — List Item Chunks.  · required: id, item_id, account_id, name
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items/{item_id}/download` — Download Item Content.  · required: id, item_id, account_id, name
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/items/{item_id}/logs` — Item Logs.  · required: id, item_id, account_id, name
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/jobs` — List Jobs  · required: id, account_id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/jobs` — Create new job  · required: id, account_id, name  · body: (no required fields)
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/jobs/{job_id}` — Get a Job Details  · required: id, job_id, account_id, name
- `PATCH /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/jobs/{job_id}` — Cancel an indexing job.  · required: id, job_id, account_id, name  · body: action:string
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/jobs/{job_id}/logs` — List Job Logs  · required: id, job_id, account_id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/purge_cache` — Purge search cache.  · required: account_id, id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/search` — Search  · required: id, account_id, name  · body: (no required fields)
- `GET /accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/stats` — Get instance statistics.  · required: id, account_id, name
- `POST /accounts/{account_id}/ai-search/namespaces/{name}/search` — Multi-Instance Search  · required: account_id, name  · body: ai_search_options:object
- `GET /accounts/{account_id}/ai-search/tokens` — List tokens  · required: account_id
- `POST /accounts/{account_id}/ai-search/tokens` — Create a token  · required: account_id  · body: cf_api_id:string, cf_api_key:string, name:string
- `GET /accounts/{account_id}/ai-search/tokens/{id}` — Get a token  · required: account_id, id
- `PUT /accounts/{account_id}/ai-search/tokens/{id}` — Update a token  · required: account_id, id  · body: cf_api_id:string, cf_api_key:string, name:string
- `DELETE /accounts/{account_id}/ai-search/tokens/{id}` — Delete a token  · required: account_id, id
- `POST /accounts/{account_id}/autorag/rags/{id}/ai-search` — AI Search  · required: id, account_id  · body: query:string
- `GET /accounts/{account_id}/autorag/rags/{id}/files` — Files  · required: id, account_id
- `GET /accounts/{account_id}/autorag/rags/{id}/jobs` — List Jobs  · required: id, account_id
- `GET /accounts/{account_id}/autorag/rags/{id}/jobs/{job_id}` — Get a Job Details  · required: id, job_id, account_id
- `GET /accounts/{account_id}/autorag/rags/{id}/jobs/{job_id}/logs` — List Job Logs  · required: id, job_id, account_id
- `POST /accounts/{account_id}/autorag/rags/{id}/search` — Search  · required: id, account_id  · body: query:string
- `PATCH /accounts/{account_id}/autorag/rags/{id}/sync` — Sync  · required: id, account_id
