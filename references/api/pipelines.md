# API reference — pipelines

> Exact REST endpoints for **pipelines**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 19 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/pipelines` — [DEPRECATED] List Pipelines  · required: account_id
- `POST /accounts/{account_id}/pipelines` — [DEPRECATED] Create Pipeline  · required: account_id  · body: destination:object, name:string, source:object[]
- `GET /accounts/{account_id}/pipelines/v1/pipelines` — List Pipelines  · required: account_id
- `POST /accounts/{account_id}/pipelines/v1/pipelines` — Create Pipeline  · required: account_id  · body: name:string, sql:string
- `GET /accounts/{account_id}/pipelines/v1/pipelines/{pipeline_id}` — Get Pipeline Details  · required: account_id, pipeline_id
- `DELETE /accounts/{account_id}/pipelines/v1/pipelines/{pipeline_id}` — Delete Pipeline  · required: account_id, pipeline_id
- `GET /accounts/{account_id}/pipelines/v1/sinks` — List Sinks  · required: account_id
- `POST /accounts/{account_id}/pipelines/v1/sinks` — Create Sink  · required: account_id  · body: name:string, type:string
- `GET /accounts/{account_id}/pipelines/v1/sinks/{sink_id}` — Get Sink Details  · required: account_id, sink_id
- `DELETE /accounts/{account_id}/pipelines/v1/sinks/{sink_id}` — Delete Sink  · required: account_id, sink_id
- `GET /accounts/{account_id}/pipelines/v1/streams` — List Streams  · required: account_id
- `POST /accounts/{account_id}/pipelines/v1/streams` — Create Stream  · required: account_id  · body: name:string
- `GET /accounts/{account_id}/pipelines/v1/streams/{stream_id}` — Get Stream Details  · required: account_id, stream_id
- `PATCH /accounts/{account_id}/pipelines/v1/streams/{stream_id}` — Update Stream  · required: account_id, stream_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/pipelines/v1/streams/{stream_id}` — Delete Stream  · required: account_id, stream_id
- `POST /accounts/{account_id}/pipelines/v1/validate_sql` — Validate SQL  · required: account_id  · body: sql:string
- `GET /accounts/{account_id}/pipelines/{pipeline_name}` — [DEPRECATED] Get Pipeline  · required: account_id, pipeline_name
- `PUT /accounts/{account_id}/pipelines/{pipeline_name}` — [DEPRECATED] Update Pipeline  · required: account_id, pipeline_name  · body: destination:object, name:string, source:object[]
- `DELETE /accounts/{account_id}/pipelines/{pipeline_name}` — [DEPRECATED] Delete Pipeline  · required: account_id, pipeline_name
