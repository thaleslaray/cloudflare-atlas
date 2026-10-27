# API reference — notifications

> Exact REST endpoints for **notifications**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 27 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/alerting/v3/available_alerts` — Get Alert Types  · required: account_id
- `GET /accounts/{account_id}/alerting/v3/destinations/eligible` — Get delivery mechanism eligibility  · required: account_id
- `GET /accounts/{account_id}/alerting/v3/destinations/pagerduty` — List PagerDuty services  · required: account_id
- `DELETE /accounts/{account_id}/alerting/v3/destinations/pagerduty` — Delete PagerDuty Services  · required: account_id
- `POST /accounts/{account_id}/alerting/v3/destinations/pagerduty/connect` — Create PagerDuty integration token  · required: account_id
- `GET /accounts/{account_id}/alerting/v3/destinations/pagerduty/connect/{token_id}` — Connect PagerDuty  · required: account_id, token_id
- `GET /accounts/{account_id}/alerting/v3/destinations/webhooks` — List webhooks  · required: account_id
- `POST /accounts/{account_id}/alerting/v3/destinations/webhooks` — Create a webhook  · required: account_id  · body: name:string, url:string
- `GET /accounts/{account_id}/alerting/v3/destinations/webhooks/{webhook_id}` — Get a webhook  · required: account_id, webhook_id
- `PUT /accounts/{account_id}/alerting/v3/destinations/webhooks/{webhook_id}` — Update a webhook  · required: webhook_id, account_id  · body: name:string, url:string
- `DELETE /accounts/{account_id}/alerting/v3/destinations/webhooks/{webhook_id}` — Delete a webhook  · required: webhook_id, account_id
- `GET /accounts/{account_id}/alerting/v3/history` — List History  · required: account_id
- `GET /accounts/{account_id}/alerting/v3/policies` — List Notification policies  · required: account_id
- `POST /accounts/{account_id}/alerting/v3/policies` — Create a Notification policy  · required: account_id  · body: alert_type:string, enabled:boolean, mechanisms:object, name:string
- `GET /accounts/{account_id}/alerting/v3/policies/{policy_id}` — Get a Notification policy  · required: account_id, policy_id
- `PUT /accounts/{account_id}/alerting/v3/policies/{policy_id}` — Update a Notification policy  · required: account_id, policy_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/alerting/v3/policies/{policy_id}` — Delete a Notification policy  · required: account_id, policy_id
- `GET /accounts/{account_id}/alerting/v3/policies/{policy_id}/email/unsubscribe` — Show email unsubscribe details  · required: account_id, policy_id, email, token
- `POST /accounts/{account_id}/alerting/v3/policies/{policy_id}/email/unsubscribe` — Unsubscribe email from a Notification policy  · required: account_id, policy_id, email, token
- `POST /accounts/{account_id}/alerting/v3/policies/{policy_id}/test` — Test a Notification policy  · required: account_id, policy_id  · body: (no required fields)
- `GET /accounts/{account_id}/alerting/v3/silences` — List Silences  · required: account_id
- `POST /accounts/{account_id}/alerting/v3/silences` — Create Silences  · required: account_id  · body: (no required fields)
- `PUT /accounts/{account_id}/alerting/v3/silences` — Update Silences  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/alerting/v3/silences/{silence_id}` — Get Silence  · required: account_id, silence_id
- `DELETE /accounts/{account_id}/alerting/v3/silences/{silence_id}` — Delete Silence  · required: account_id, silence_id
- `GET /zones/{zone_id}/ct/alerting` — Get CT Alerting Subscription  · required: zone_id
- `PATCH /zones/{zone_id}/ct/alerting` — Update CT Alerting Subscription  · required: zone_id  · body: enabled:boolean
