# API reference — pages

> Exact REST endpoints for **pages**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 26 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/pages/projects` — List Cloudflare Pages projects  · required: account_id
- `POST /accounts/{account_id}/pages/projects` — Create a Cloudflare Pages project  · required: account_id  · body: name:string, production_branch:string
- `GET /accounts/{account_id}/pages/projects/{project_name}` — Get a Cloudflare Pages project  · required: project_name, account_id
- `PATCH /accounts/{account_id}/pages/projects/{project_name}` — Update a Cloudflare Pages project  · required: project_name, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/pages/projects/{project_name}` — Delete a Cloudflare Pages project  · required: project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/deployments` — List Pages deployments  · required: project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments` — Create a Pages deployment  · required: project_name, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}` — Get a Pages deployment  · required: deployment_id, project_name, account_id
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}` — Delete a Pages deployment  · required: deployment_id, project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/history/logs` — Get Pages deployment logs  · required: deployment_id, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/retry` — Retry a Pages deployment  · required: deployment_id, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/rollback` — Roll back a Pages deployment  · required: deployment_id, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/tails` — Create deployment tail  · required: deployment_id, project_name, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/tails/{tail_id}` — Delete deployment tail  · required: tail_id, deployment_id, project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/domains` — List Pages custom domains  · required: project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/domains` — Add a Pages custom domain  · required: project_name, account_id  · body: name:string
- `GET /accounts/{account_id}/pages/projects/{project_name}/domains/{domain_name}` — Get a Pages custom domain  · required: domain_name, project_name, account_id
- `PATCH /accounts/{account_id}/pages/projects/{project_name}/domains/{domain_name}` — Retry custom domain validation  · required: domain_name, project_name, account_id
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/domains/{domain_name}` — Delete a Pages custom domain  · required: domain_name, project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/purge_build_cache` — Purge the Pages build cache  · required: project_name, account_id
- `POST /accounts/{account_id}/pages/projects/{project_name}/source` — Connect a Git repository  · required: project_name, account_id  · body: config:object, type:string
- `DELETE /accounts/{account_id}/pages/projects/{project_name}/source` — Disconnect a Git repository  · required: project_name, account_id
- `GET /accounts/{account_id}/pages/projects/{project_name}/upload-token` — Get upload token  · required: project_name, account_id
- `POST /pages/assets/check-missing` — Check missing assets  · required:   · body: hashes:string[]
- `POST /pages/assets/upload` — Upload asset  · required:   · body: (no required fields)
- `POST /pages/assets/upsert-hashes` — Upsert asset hashes  · required:   · body: hashes:string[]
