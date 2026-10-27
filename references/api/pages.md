# API reference — pages

> Exact REST endpoints for **pages**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 26 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/pages/projects` — Get projects  · required: account_id
- `POST /accounts/{account_id}/pages/projects` — Create project  · required: account_id  · body: name:string, production_branch:string
- `GET /accounts/{account_id}/pages/projects/{project_name}` — Get project  · required: project_name, account_id
- `PATCH /accounts/{account_id}/pages/projects/{project_name}` — Update project  · required: project_name, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/pages/projects/{project_name}` — Delete project  · required: project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/deployments` — Get deployments  · required: project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments` — Create deployment  · required: project_name, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}` — Get deployment info  · required: deployment_id, project_name, account_id
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}` — Delete deployment  · required: deployment_id, project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/history/logs` — Get deployment logs  · required: deployment_id, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/retry` — Retry deployment  · required: deployment_id, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/rollback` — Rollback deployment  · required: deployment_id, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/tails` — Create deployment tail  · required: deployment_id, project_name, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/tails/{tail_id}` — Delete deployment tail  · required: tail_id, deployment_id, project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/domains` — Get domains  · required: project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/domains` — Add domain  · required: project_name, account_id  · body: name:string
- `GET /accounts/{account_id}/pages/projects/{project_name}/domains/{domain_name}` — Get domain  · required: domain_name, project_name, account_id
- `PATCH /accounts/{account_id}/pages/projects/{project_name}/domains/{domain_name}` — Patch domain  · required: domain_name, project_name, account_id
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/domains/{domain_name}` — Delete domain  · required: domain_name, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/purge_build_cache` — Purge build cache  · required: project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/source` — Connect project source  · required: project_name, account_id  · body: config:object, type:string
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/source` — Disconnect project source  · required: project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/upload-token` — Get upload token  · required: project_name, account_id
- `POST /pages/assets/check-missing` — Check missing assets  · required:   · body: hashes:string[]
- `POST /pages/assets/upload` — Upload asset  · required:   · body: (no required fields)
- `POST /pages/assets/upsert-hashes` — Upsert asset hashes  · required:   · body: hashes:string[]
