# API reference — rules

> Exact REST endpoints for **rules**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 76 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/dex/rules` — List DEX Rules  · required: account_id, page, per_page
- `POST /accounts/{account_id}/dex/rules` — Create a DEX Rule  · required: account_id  · body: match:string, name:string
- `GET /accounts/{account_id}/dex/rules/{rule_id}` — Get DEX Rule  · required: account_id, rule_id
- `PATCH /accounts/{account_id}/dex/rules/{rule_id}` — Update a DEX Rule  · required: account_id, rule_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/dex/rules/{rule_id}` — Delete a DEX Rule  · required: account_id, rule_id
- `GET /accounts/{account_id}/gateway/rules` — List Zero Trust Gateway rules  · required: account_id
- `POST /accounts/{account_id}/gateway/rules` — Create a Zero Trust Gateway rule  · required: account_id  · body: action:string, name:string
- `PATCH /accounts/{account_id}/gateway/rules` — Patch multiple Zero Trust Gateway rules  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/gateway/rules/tenant` — List Zero Trust Gateway rules inherited from the parent account  · required: account_id
- `GET /accounts/{account_id}/gateway/rules/{rule_id}` — Get Zero Trust Gateway rule details.  · required: rule_id, account_id
- `PUT /accounts/{account_id}/gateway/rules/{rule_id}` — Update a Zero Trust Gateway rule  · required: rule_id, account_id  · body: action:string, name:string
- `PATCH /accounts/{account_id}/gateway/rules/{rule_id}` — Patch a Zero Trust Gateway rule  · required: rule_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/gateway/rules/{rule_id}` — Delete a Zero Trust Gateway rule  · required: rule_id, account_id
- `POST /accounts/{account_id}/gateway/rules/{rule_id}/reset_expiration` — Reset the expiration of a Zero Trust Gateway Rule  · required: rule_id, account_id
- `GET /accounts/{account_id}/magic/advanced_dns_protection/configs/dns_protection/rules` — List all DNS Protection rules.  · required: account_id
- `POST /accounts/{account_id}/magic/advanced_dns_protection/configs/dns_protection/rules` — Create DNS Protection rule.  · required: account_id  · body: burst_sensitivity:string, mode:string, name:string, profile_sensitivity:string, rate_sensitivity:string, scope:string
- `DELETE /accounts/{account_id}/magic/advanced_dns_protection/configs/dns_protection/rules` — Delete all DNS Protection rules.  · required: account_id
- `GET /accounts/{account_id}/magic/advanced_dns_protection/configs/dns_protection/rules/{rule_id}` — Get DNS Protection rule.  · required: account_id, rule_id
- `PATCH /accounts/{account_id}/magic/advanced_dns_protection/configs/dns_protection/rules/{rule_id}` — Update DNS Protection rule.  · required: account_id, rule_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/magic/advanced_dns_protection/configs/dns_protection/rules/{rule_id}` — Delete DNS Protection rule.  · required: account_id, rule_id
- `GET /accounts/{account_id}/magic/advanced_tcp_protection/configs/syn_protection/rules` — List all SYN Protection rules.  · required: account_id
- `POST /accounts/{account_id}/magic/advanced_tcp_protection/configs/syn_protection/rules` — Create SYN Protection rule.  · required: account_id  · body: burst_sensitivity:string, mode:string, name:string, rate_sensitivity:string, scope:string
- `DELETE /accounts/{account_id}/magic/advanced_tcp_protection/configs/syn_protection/rules` — Delete all SYN Protection rules.  · required: account_id
- `GET /accounts/{account_id}/magic/advanced_tcp_protection/configs/syn_protection/rules/{rule_id}` — Get SYN Protection rule.  · required: account_id, rule_id
- `PATCH /accounts/{account_id}/magic/advanced_tcp_protection/configs/syn_protection/rules/{rule_id}` — Update SYN Protection rule.  · required: account_id, rule_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/magic/advanced_tcp_protection/configs/syn_protection/rules/{rule_id}` — Delete SYN Protection rule.  · required: account_id, rule_id
- `GET /accounts/{account_id}/magic/advanced_tcp_protection/configs/tcp_flow_protection/rules` — List all TCP Flow Protection rules.  · required: account_id
- `POST /accounts/{account_id}/magic/advanced_tcp_protection/configs/tcp_flow_protection/rules` — Create TCP Flow Protection rule.  · required: account_id  · body: burst_sensitivity:string, mode:string, name:string, rate_sensitivity:string, scope:string
- `DELETE /accounts/{account_id}/magic/advanced_tcp_protection/configs/tcp_flow_protection/rules` — Delete all TCP Flow Protection rules.  · required: account_id
- `GET /accounts/{account_id}/magic/advanced_tcp_protection/configs/tcp_flow_protection/rules/{rule_id}` — Get TCP Flow Protection rule.  · required: account_id, rule_id
- `PATCH /accounts/{account_id}/magic/advanced_tcp_protection/configs/tcp_flow_protection/rules/{rule_id}` — Update TCP Flow Protection rule.  · required: account_id, rule_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/magic/advanced_tcp_protection/configs/tcp_flow_protection/rules/{rule_id}` — Delete TCP Flow Protection rule.  · required: account_id, rule_id
- `GET /accounts/{account_id}/mnm/rules` — List rules  · required: account_id
- `POST /accounts/{account_id}/mnm/rules` — Create rules  · required: account_id  · body: automatic_advertisement:boolean, name:string, prefixes:string[], type:string
- `PUT /accounts/{account_id}/mnm/rules` — Update rules  · required: account_id  · body: automatic_advertisement:boolean, name:string, prefixes:string[], type:string
- `POST /accounts/{account_id}/mnm/rules/bulk` — Create rules in bulk  · required: account_id  · body: (no required fields)
- `PUT /accounts/{account_id}/mnm/rules/bulk` — Update rules in bulk  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/mnm/rules/{rule_id}` — Get rule  · required: rule_id, account_id
- `PATCH /accounts/{account_id}/mnm/rules/{rule_id}` — Update rule  · required: rule_id, account_id  · body: automatic_advertisement:boolean, name:string, prefixes:string[], type:string
- `DELETE /accounts/{account_id}/mnm/rules/{rule_id}` — Delete rule  · required: rule_id, account_id  · body: (spec carries no schema — check the docs)
- `PATCH /accounts/{account_id}/mnm/rules/{rule_id}/advertisement` — Update advertisement for rule  · required: rule_id, account_id  · body: (spec carries no schema — check the docs)
- `GET /accounts/{account_id}/rules/lists` — Get lists  · required: account_id
- `POST /accounts/{account_id}/rules/lists` — Create a list  · required: account_id  · body: kind:any, name:string
- `GET /accounts/{account_id}/rules/lists/bulk_operations/{operation_id}` — Get bulk operation status  · required: operation_id, account_id
- `GET /accounts/{account_id}/rules/lists/{list_id}` — Get a list  · required: list_id, account_id
- `PUT /accounts/{account_id}/rules/lists/{list_id}` — Update a list  · required: list_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/rules/lists/{list_id}` — Delete a list  · required: list_id, account_id
- `GET /accounts/{account_id}/rules/lists/{list_id}/items` — Get list items  · required: list_id, account_id
- `POST /accounts/{account_id}/rules/lists/{list_id}/items` — Create list items  · required: list_id, account_id  · body: (no required fields)
- `PUT /accounts/{account_id}/rules/lists/{list_id}/items` — Update all list items  · required: list_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/rules/lists/{list_id}/items` — Delete list items  · required: list_id, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/rules/lists/{list_id}/items/{item_id}` — Get a list item  · required: item_id, list_id, account_id
- `GET /zones/{zone_id}/cloud_connector/rules` — Rules  · required: zone_id
- `PUT /zones/{zone_id}/cloud_connector/rules` — Put Rules  · required: zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/managed_headers` — List Managed Transforms  · required: zone_id
- `PATCH /zones/{zone_id}/managed_headers` — Update Managed Transforms  · required: zone_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/managed_headers` — Delete Managed Transforms  · required: zone_id
- `GET /zones/{zone_id}/snippets` — List zone snippets  · required: zone_id
- `GET /zones/{zone_id}/snippets/snippet_rules` — List zone snippet rules  · required: zone_id
- `PUT /zones/{zone_id}/snippets/snippet_rules` — Update zone snippet rules  · required: zone_id  · body: rules:object[]
- `DELETE /zones/{zone_id}/snippets/snippet_rules` — Delete zone snippet rules  · required: zone_id
- `GET /zones/{zone_id}/snippets/{snippet_name}` — Get a zone snippet  · required: zone_id, snippet_name
- `PUT /zones/{zone_id}/snippets/{snippet_name}` — Update a zone snippet  · required: zone_id, snippet_name  · body: files:any, metadata:object
- `DELETE /zones/{zone_id}/snippets/{snippet_name}` — Delete a zone snippet  · required: zone_id, snippet_name
- `GET /zones/{zone_id}/snippets/{snippet_name}/content` — Get a zone snippet content  · required: zone_id, snippet_name
- `GET /zones/{zone_id}/token_validation/rules` — List token validation rules  · required: 
- `POST /zones/{zone_id}/token_validation/rules` — Create a token validation rule  · required:   · body: action:string, description:string, enabled:boolean, expression:string, selector:object, title:string
- `POST /zones/{zone_id}/token_validation/rules/bulk` — Create token validation rules  · required:   · body: (no required fields)
- `PATCH /zones/{zone_id}/token_validation/rules/bulk` — Edit token validation rules  · required:   · body: (no required fields)
- `POST /zones/{zone_id}/token_validation/rules/preview` — Preview a token validation rule  · required:   · body: (no required fields)
- `GET /zones/{zone_id}/token_validation/rules/{rule_id}` — Get a token validation rule  · required: 
- `PATCH /zones/{zone_id}/token_validation/rules/{rule_id}` — Edit a token validation rule  · required:   · body: (no required fields)
- `DELETE /zones/{zone_id}/token_validation/rules/{rule_id}` — Delete a token validation rule  · required: 
- `GET /zones/{zone_id}/url_normalization` — Get URL Normalization settings  · required: zone_id
- `PUT /zones/{zone_id}/url_normalization` — Update URL Normalization settings  · required: zone_id  · body: scope:string, type:string
- `DELETE /zones/{zone_id}/url_normalization` — Delete URL Normalization settings  · required: zone_id
