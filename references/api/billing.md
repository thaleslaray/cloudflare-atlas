# API reference — billing

> Exact REST endpoints for **billing**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 15 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/billing/bad-debt` — Get Account Bad Debt  · required: account_id
- `GET /accounts/{account_id}/billing/credits` — Get Account Credits  · required: account_id
- `GET /accounts/{account_id}/billing/history` — Get Account Billing History  · required: account_id
- `GET /accounts/{account_id}/billing/profile` — Get Billing Profile  · required: account_id
- `POST /accounts/{account_id}/billing/profile` — Create Billing Profile  · required: account_id  · body: (no required fields)
- `PUT /accounts/{account_id}/billing/profile` — Update Billing Profile  · required: account_id  · body: (no required fields)
- `PATCH /accounts/{account_id}/billing/profile` — Update Billing Email  · required: account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/billing/profile` — Delete Billing Profile  · required: account_id
- `POST /accounts/{account_id}/billing/profile/payment-method` — Create Payment Intent for Billing Profile  · required: account_id
- `GET /accounts/{account_id}/billing/unpaid-invoice` — Get Unpaid Invoices  · required: account_id
- `GET /accounts/{account_id}/billing/usage` — Get account billing usage  · required: 
- `POST /billing/address-validation` — Validate Billing Address  · required:   · body: (no required fields)
- `GET /billing/rate_plans/{public_key}` — Get Rate Plan by Public Key  · required: public_key
- `GET /user/billing/history` — Billing History Details  · required: 
- `GET /user/billing/profile` — Billing Profile Details  · required: 
