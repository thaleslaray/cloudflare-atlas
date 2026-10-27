# API reference — workflows

> Exact REST endpoints for **workflows**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 23 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/workflows` — List all Workflows  · required: account_id
- `GET /accounts/{account_id}/workflows/settings` — Get account settings  · required: account_id
- `PATCH /accounts/{account_id}/workflows/settings` — Update account settings  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/workflows/{workflow_name}` — Get Workflow details  · required: workflow_name, account_id
- `PUT /accounts/{account_id}/workflows/{workflow_name}` — Create/modify Workflow  · required: workflow_name, account_id  · body: class_name:string, script_name:string
- `DELETE /accounts/{account_id}/workflows/{workflow_name}` — Deletes a Workflow  · required: workflow_name, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/instances` — List of workflow instances  · required: workflow_name, account_id
- `POST /accounts/{account_id}/workflows/{workflow_name}/instances` — Create a new workflow instance  · required: workflow_name, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/workflows/{workflow_name}/instances/batch` — Batch create new Workflow instances  · required: workflow_name, account_id  · body: (no required fields)
- `POST /accounts/{account_id}/workflows/{workflow_name}/instances/batch/delete` — Batch delete instances of a workflow  · required: workflow_name, account_id  · body: instances:string[]
- `POST /accounts/{account_id}/workflows/{workflow_name}/instances/batch/terminate` — Batch terminate instances of a workflow  · required: workflow_name, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/workflows/{workflow_name}/instances/terminate` — Get status of the job responsible for terminate all instances of a workflow  · required: workflow_name, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}` — Get logs and status from instance  · required: workflow_name, instance_id, account_id
- `DELETE /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}` — Delete a workflow instance  · required: workflow_name, instance_id, account_id
- `POST /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}/events/{event_type}` — Send event to instance  · required: workflow_name, instance_id, event_type, account_id  · body: (no required fields)
- `PATCH /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}/status` — Change status of instance  · required: workflow_name, instance_id, account_id  · body: status:string
- `GET /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}/step` — Get full step output from instance  · required: workflow_name, instance_id, name, type, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}/subscribe` — Subscribe to workflow instance events  · required: workflow_name, instance_id, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}/subscribe/token` — Create a workflow instance event subscription token  · required: workflow_name, instance_id, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/versions` — List deployed Workflow versions  · required: workflow_name, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/versions/{version_id}` — Get Workflow version details  · required: workflow_name, version_id, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/versions/{version_id}/dag` — Get Workflow version dag  · required: workflow_name, version_id, account_id
- `GET /accounts/{account_id}/workflows/{workflow_name}/versions/{version_id}/graph` — Get Workflow version graph  · required: workflow_name, version_id, account_id
