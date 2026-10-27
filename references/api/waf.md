# API reference — waf

> Exact REST endpoints for **waf**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 79 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/firewall/access_rules/rules` — List IP Access rules  · required: account_id
- `POST /accounts/{account_id}/firewall/access_rules/rules` — Create an IP Access rule  · required: account_id  · body: configuration:object, mode:string
- `GET /accounts/{account_id}/firewall/access_rules/rules/{rule_id}` — Get an IP Access rule  · required: rule_id, account_id
- `PATCH /accounts/{account_id}/firewall/access_rules/rules/{rule_id}` — Update an IP Access rule  · required: rule_id, account_id  · body: allowed_modes:string[], configuration:object, id:string, mode:string
- `DELETE /accounts/{account_id}/firewall/access_rules/rules/{rule_id}` — Delete an IP Access rule  · required: rule_id, account_id
- `GET /accounts/{account_id}/rulesets` — List account rulesets  · required: account_id
- `POST /accounts/{account_id}/rulesets` — Create an account ruleset  · required: account_id  · body: id:object, kind:string, last_updated:string, name:string, phase:string, version:object
- `GET /accounts/{account_id}/rulesets/phases/{ruleset_phase}/entrypoint` — Get an account entry point ruleset  · required: ruleset_phase, account_id
- `PUT /accounts/{account_id}/rulesets/phases/{ruleset_phase}/entrypoint` — Update an account entry point ruleset  · required: ruleset_phase, account_id  · body: id:object, last_updated:string, version:object
- `GET /accounts/{account_id}/rulesets/phases/{ruleset_phase}/entrypoint/versions` — List an account entry point ruleset's versions  · required: ruleset_phase, account_id
- `GET /accounts/{account_id}/rulesets/phases/{ruleset_phase}/entrypoint/versions/{ruleset_version}` — Get an account entry point ruleset version  · required: ruleset_version, ruleset_phase, account_id
- `GET /accounts/{account_id}/rulesets/{ruleset_id}` — Get an account ruleset  · required: ruleset_id, account_id
- `PUT /accounts/{account_id}/rulesets/{ruleset_id}` — Update an account ruleset  · required: ruleset_id, account_id  · body: id:object, last_updated:string, version:object
- `DELETE /accounts/{account_id}/rulesets/{ruleset_id}` — Delete an account ruleset  · required: ruleset_id, account_id
- `POST /accounts/{account_id}/rulesets/{ruleset_id}/rules` — Create an account ruleset rule  · required: ruleset_id, account_id  · body: last_updated:string, version:string
- `PATCH /accounts/{account_id}/rulesets/{ruleset_id}/rules/{rule_id}` — Update an account ruleset rule  · required: rule_id, ruleset_id, account_id  · body: last_updated:string, version:string
- `DELETE /accounts/{account_id}/rulesets/{ruleset_id}/rules/{rule_id}` — Delete an account ruleset rule  · required: rule_id, ruleset_id, account_id
- `GET /accounts/{account_id}/rulesets/{ruleset_id}/versions` — List an account ruleset's versions  · required: ruleset_id, account_id
- `GET /accounts/{account_id}/rulesets/{ruleset_id}/versions/{ruleset_version}` — Get an account ruleset version  · required: ruleset_version, ruleset_id, account_id
- `DELETE /accounts/{account_id}/rulesets/{ruleset_id}/versions/{ruleset_version}` — Delete an account ruleset version  · required: ruleset_version, ruleset_id, account_id
- `GET /accounts/{account_id}/rulesets/{ruleset_id}/versions/{ruleset_version}/by_tag/{rule_tag}` — List an account ruleset version's rules by tag  · required: rule_tag, ruleset_version, ruleset_id, account_id
- `GET /user/firewall/access_rules/rules` — List IP Access rules  · required: 
- `POST /user/firewall/access_rules/rules` — Create an IP Access rule  · required:   · body: configuration:object, mode:string
- `GET /user/firewall/access_rules/rules/{rule_id}` — Get an IP Access rule  · required: rule_id
- `PATCH /user/firewall/access_rules/rules/{rule_id}` — Update an IP Access rule  · required: rule_id  · body: (no required fields)
- `DELETE /user/firewall/access_rules/rules/{rule_id}` — Delete an IP Access rule  · required: rule_id
- `GET /zones/{zone_id}/firewall/access_rules/rules` — List IP Access rules  · required: zone_id
- `POST /zones/{zone_id}/firewall/access_rules/rules` — Create an IP Access rule  · required: zone_id  · body: configuration:object, mode:string
- `PATCH /zones/{zone_id}/firewall/access_rules/rules/{rule_id}` — Update an IP Access rule  · required: zone_id, rule_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/firewall/access_rules/rules/{rule_id}` — Delete an IP Access rule  · required: zone_id, rule_id  · body: (no required fields)
- `GET /zones/{zone_id}/firewall/lockdowns` — List Zone Lockdown rules  · required: zone_id
- `POST /zones/{zone_id}/firewall/lockdowns` — Create a Zone Lockdown rule  · required: zone_id  · body: configurations:object[], urls:string[]
- `GET /zones/{zone_id}/firewall/lockdowns/{lock_downs_id}` — Get a Zone Lockdown rule  · required: lock_downs_id, zone_id
- `PUT /zones/{zone_id}/firewall/lockdowns/{lock_downs_id}` — Update a Zone Lockdown rule  · required: lock_downs_id, zone_id  · body: configurations:object[], urls:string[]
- `DELETE /zones/{zone_id}/firewall/lockdowns/{lock_downs_id}` — Delete a Zone Lockdown rule  · required: lock_downs_id, zone_id
- `GET /zones/{zone_id}/firewall/rules` — List firewall rules  · required: zone_id
- `POST /zones/{zone_id}/firewall/rules` — Create firewall rules  · required: zone_id  · body: action:object, filter:object
- `PUT /zones/{zone_id}/firewall/rules` — Update firewall rules  · required: zone_id  · body: id:string
- `PATCH /zones/{zone_id}/firewall/rules` — Update priority of firewall rules  · required: zone_id  · body: id:string
- `DELETE /zones/{zone_id}/firewall/rules` — Delete firewall rules  · required: zone_id  · body: id:string
- `GET /zones/{zone_id}/firewall/rules/{rule_id}` — Get a firewall rule  · required: rule_id, zone_id
- `PUT /zones/{zone_id}/firewall/rules/{rule_id}` — Update a firewall rule  · required: rule_id, zone_id  · body: action:object, filter:object, id:string
- `PATCH /zones/{zone_id}/firewall/rules/{rule_id}` — Update priority of a firewall rule  · required: rule_id, zone_id  · body: id:string
- `DELETE /zones/{zone_id}/firewall/rules/{rule_id}` — Delete a firewall rule  · required: rule_id, zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/firewall/ua_rules` — List User Agent Blocking rules  · required: zone_id
- `POST /zones/{zone_id}/firewall/ua_rules` — Create a User Agent Blocking rule  · required: zone_id  · body: configuration:object, mode:string
- `GET /zones/{zone_id}/firewall/ua_rules/{ua_rule_id}` — Get a User Agent Blocking rule  · required: ua_rule_id, zone_id
- `PUT /zones/{zone_id}/firewall/ua_rules/{ua_rule_id}` — Update a User Agent Blocking rule  · required: ua_rule_id, zone_id  · body: configuration:object, id:string, mode:string
- `DELETE /zones/{zone_id}/firewall/ua_rules/{ua_rule_id}` — Delete a User Agent Blocking rule  · required: ua_rule_id, zone_id
- `GET /zones/{zone_id}/firewall/waf/overrides` — List WAF overrides  · required: zone_id
- `POST /zones/{zone_id}/firewall/waf/overrides` — Create a WAF override  · required: zone_id  · body: urls:string[]
- `GET /zones/{zone_id}/firewall/waf/overrides/{overrides_id}` — Get a WAF override  · required: overrides_id, zone_id
- `PUT /zones/{zone_id}/firewall/waf/overrides/{overrides_id}` — Update WAF override  · required: overrides_id, zone_id  · body: id:string, rewrite_action:object, rules:object, urls:string[]
- `DELETE /zones/{zone_id}/firewall/waf/overrides/{overrides_id}` — Delete a WAF override  · required: overrides_id, zone_id
- `GET /zones/{zone_id}/firewall/waf/packages` — List WAF packages  · required: zone_id
- `GET /zones/{zone_id}/firewall/waf/packages/{package_id}` — Get a WAF package  · required: package_id, zone_id
- `PATCH /zones/{zone_id}/firewall/waf/packages/{package_id}` — Update a WAF package  · required: package_id, zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/firewall/waf/packages/{package_id}/groups` — List WAF rule groups  · required: package_id, zone_id
- `GET /zones/{zone_id}/firewall/waf/packages/{package_id}/groups/{group_id}` — Get a WAF rule group  · required: group_id, package_id, zone_id
- `PATCH /zones/{zone_id}/firewall/waf/packages/{package_id}/groups/{group_id}` — Update a WAF rule group  · required: group_id, package_id, zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/firewall/waf/packages/{package_id}/rules` — List WAF rules  · required: package_id, zone_id
- `GET /zones/{zone_id}/firewall/waf/packages/{package_id}/rules/{rule_id}` — Get a WAF rule  · required: rule_id, package_id, zone_id
- `PATCH /zones/{zone_id}/firewall/waf/packages/{package_id}/rules/{rule_id}` — Update a WAF rule  · required: rule_id, package_id, zone_id  · body: (no required fields)
- `GET /zones/{zone_id}/rulesets` — List zone rulesets  · required: zone_id
- `POST /zones/{zone_id}/rulesets` — Create a zone ruleset  · required: zone_id  · body: id:object, kind:string, last_updated:string, name:string, phase:string, version:object
- `GET /zones/{zone_id}/rulesets/phases/{ruleset_phase}/entrypoint` — Get a zone entry point ruleset  · required: ruleset_phase, zone_id
- `PUT /zones/{zone_id}/rulesets/phases/{ruleset_phase}/entrypoint` — Update a zone entry point ruleset  · required: ruleset_phase, zone_id  · body: id:object, last_updated:string, version:object
- `GET /zones/{zone_id}/rulesets/phases/{ruleset_phase}/entrypoint/versions` — List a zone entry point ruleset's versions  · required: ruleset_phase, zone_id
- `GET /zones/{zone_id}/rulesets/phases/{ruleset_phase}/entrypoint/versions/{ruleset_version}` — Get a zone entry point ruleset version  · required: ruleset_version, ruleset_phase, zone_id
- `GET /zones/{zone_id}/rulesets/{ruleset_id}` — Get a zone ruleset  · required: ruleset_id, zone_id
- `PUT /zones/{zone_id}/rulesets/{ruleset_id}` — Update a zone ruleset  · required: ruleset_id, zone_id  · body: id:object, last_updated:string, version:object
- `DELETE /zones/{zone_id}/rulesets/{ruleset_id}` — Delete a zone ruleset  · required: ruleset_id, zone_id
- `POST /zones/{zone_id}/rulesets/{ruleset_id}/rules` — Create a zone ruleset rule  · required: ruleset_id, zone_id  · body: last_updated:string, version:string
- `PATCH /zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}` — Update a zone ruleset rule  · required: rule_id, ruleset_id, zone_id  · body: last_updated:string, version:string
- `DELETE /zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}` — Delete a zone ruleset rule  · required: rule_id, ruleset_id, zone_id
- `GET /zones/{zone_id}/rulesets/{ruleset_id}/versions` — List a zone ruleset's versions  · required: ruleset_id, zone_id
- `GET /zones/{zone_id}/rulesets/{ruleset_id}/versions/{ruleset_version}` — Get a zone ruleset version  · required: ruleset_version, ruleset_id, zone_id
- `DELETE /zones/{zone_id}/rulesets/{ruleset_id}/versions/{ruleset_version}` — Delete a zone ruleset version  · required: ruleset_version, ruleset_id, zone_id
- `GET /zones/{zone_id}/rulesets/{ruleset_id}/versions/{ruleset_version}/by_tag/{rule_tag}` — List a zone ruleset version's rules by tag  · required: rule_tag, ruleset_version, ruleset_id, zone_id
