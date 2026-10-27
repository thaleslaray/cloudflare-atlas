# API reference — load-balancing

> Exact REST endpoints for **load-balancing**, sliced from the Cloudflare OpenAPI spec (api.cloudflare.com v4). 62 operations. Base: `https://api.cloudflare.com/client/v4`.

> Body fields below are the **top-level required** ones only — not optional fields, nested
> shapes, enums or responses. Added by scripts/slice-bodies; verify shapes against the live docs.

> ⚠️ Verify shapes/params against the live API docs before relying on them — specs drift.

- `GET /accounts/{account_id}/load_balancers` — List Account Load Balancers  · required: account_id
- `POST /accounts/{account_id}/load_balancers` — Create Account Load Balancer  · required: account_id  · body: default_pools:string[], fallback_pool:string, name:string
- `GET /accounts/{account_id}/load_balancers/monitor_groups` — List Monitor Groups  · required: account_id
- `POST /accounts/{account_id}/load_balancers/monitor_groups` — Create Monitor Group  · required: account_id  · body: description:string, id:object, members:object[]
- `GET /accounts/{account_id}/load_balancers/monitor_groups/{monitor_group_id}` — Monitor Group Details  · required: monitor_group_id, account_id
- `PUT /accounts/{account_id}/load_balancers/monitor_groups/{monitor_group_id}` — Update Monitor Group  · required: monitor_group_id, account_id  · body: description:string, id:object, members:object[]
- `PATCH /accounts/{account_id}/load_balancers/monitor_groups/{monitor_group_id}` — Patch Monitor Group  · required: monitor_group_id, account_id  · body: description:string, id:object, members:object[]
- `DELETE /accounts/{account_id}/load_balancers/monitor_groups/{monitor_group_id}` — Delete Monitor Group  · required: monitor_group_id, account_id
- `GET /accounts/{account_id}/load_balancers/monitor_groups/{monitor_group_id}/references` — List Monitor Group References  · required: monitor_group_id, account_id
- `GET /accounts/{account_id}/load_balancers/monitors` — List Monitors  · required: account_id
- `POST /accounts/{account_id}/load_balancers/monitors` — Create Monitor  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/load_balancers/monitors/{monitor_id}` — Monitor Details  · required: monitor_id, account_id
- `PUT /accounts/{account_id}/load_balancers/monitors/{monitor_id}` — Update Monitor  · required: monitor_id, account_id  · body: (no required fields)
- `PATCH /accounts/{account_id}/load_balancers/monitors/{monitor_id}` — Patch Monitor  · required: monitor_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/load_balancers/monitors/{monitor_id}` — Delete Monitor  · required: monitor_id, account_id
- `POST /accounts/{account_id}/load_balancers/monitors/{monitor_id}/preview` — Preview Monitor  · required: monitor_id, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/load_balancers/monitors/{monitor_id}/references` — List Monitor References  · required: monitor_id, account_id
- `GET /accounts/{account_id}/load_balancers/pools` — List Pools  · required: account_id
- `POST /accounts/{account_id}/load_balancers/pools` — Create Pool  · required: account_id  · body: name:string, origins:object[]
- `PATCH /accounts/{account_id}/load_balancers/pools` — Patch Pools  · required: account_id  · body: (no required fields)
- `GET /accounts/{account_id}/load_balancers/pools/{pool_id}` — Pool Details  · required: pool_id, account_id
- `PUT /accounts/{account_id}/load_balancers/pools/{pool_id}` — Update Pool  · required: pool_id, account_id  · body: name:string, origins:object[]
- `PATCH /accounts/{account_id}/load_balancers/pools/{pool_id}` — Patch Pool  · required: pool_id, account_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/load_balancers/pools/{pool_id}` — Delete Pool  · required: pool_id, account_id
- `GET /accounts/{account_id}/load_balancers/pools/{pool_id}/health` — Pool Health Details  · required: pool_id, account_id
- `POST /accounts/{account_id}/load_balancers/pools/{pool_id}/preview` — Preview Pool  · required: pool_id, account_id  · body: (no required fields)
- `GET /accounts/{account_id}/load_balancers/pools/{pool_id}/references` — List Pool References  · required: pool_id, account_id
- `GET /accounts/{account_id}/load_balancers/preview/{preview_id}` — Preview Result  · required: preview_id, account_id
- `GET /accounts/{account_id}/load_balancers/regions` — List Regions  · required: account_id
- `GET /accounts/{account_id}/load_balancers/regions/{region_id}` — Get Region  · required: region_id, account_id
- `GET /accounts/{account_id}/load_balancers/search` — Search Resources  · required: account_id
- `GET /accounts/{account_id}/load_balancers/usage` — List Load Balancer Usage  · required: account_id
- `GET /accounts/{account_id}/load_balancers/{load_balancer_id}` — Account Load Balancer Details  · required: account_id, load_balancer_id
- `PUT /accounts/{account_id}/load_balancers/{load_balancer_id}` — Update Account Load Balancer  · required: account_id, load_balancer_id  · body: default_pools:string[], fallback_pool:string, name:string
- `PATCH /accounts/{account_id}/load_balancers/{load_balancer_id}` — Patch Account Load Balancer  · required: account_id, load_balancer_id  · body: (no required fields)
- `DELETE /accounts/{account_id}/load_balancers/{load_balancer_id}` — Delete Account Load Balancer  · required: account_id, load_balancer_id
- `GET /user/load_balancers/monitors` — List Monitors  · required: 
- `POST /user/load_balancers/monitors` — Create Monitor  · required:   · body: (no required fields)
- `GET /user/load_balancers/monitors/{monitor_id}` — Monitor Details  · required: monitor_id
- `PUT /user/load_balancers/monitors/{monitor_id}` — Update Monitor  · required: monitor_id  · body: (no required fields)
- `PATCH /user/load_balancers/monitors/{monitor_id}` — Patch Monitor  · required: monitor_id  · body: (no required fields)
- `DELETE /user/load_balancers/monitors/{monitor_id}` — Delete Monitor  · required: monitor_id
- `POST /user/load_balancers/monitors/{monitor_id}/preview` — Preview Monitor  · required: monitor_id  · body: (no required fields)
- `GET /user/load_balancers/monitors/{monitor_id}/references` — List Monitor References  · required: monitor_id
- `GET /user/load_balancers/pools` — List Pools  · required: 
- `POST /user/load_balancers/pools` — Create Pool  · required:   · body: name:string, origins:object[]
- `PATCH /user/load_balancers/pools` — Patch Pools  · required:   · body: (no required fields)
- `GET /user/load_balancers/pools/{pool_id}` — Pool Details  · required: pool_id
- `PUT /user/load_balancers/pools/{pool_id}` — Update Pool  · required: pool_id  · body: name:string, origins:object[]
- `PATCH /user/load_balancers/pools/{pool_id}` — Patch Pool  · required: pool_id  · body: (no required fields)
- `DELETE /user/load_balancers/pools/{pool_id}` — Delete Pool  · required: pool_id
- `GET /user/load_balancers/pools/{pool_id}/health` — Pool Health Details  · required: pool_id
- `POST /user/load_balancers/pools/{pool_id}/preview` — Preview Pool  · required: pool_id  · body: (no required fields)
- `GET /user/load_balancers/pools/{pool_id}/references` — List Pool References  · required: pool_id
- `GET /user/load_balancers/preview/{preview_id}` — Preview Result  · required: preview_id
- `GET /user/load_balancers/regions` — List Regions  · required: 
- `GET /zones/{zone_id}/load_balancers` — List Load Balancers  · required: zone_id
- `POST /zones/{zone_id}/load_balancers` — Create Load Balancer  · required: zone_id  · body: default_pools:string[], fallback_pool:string, name:string
- `GET /zones/{zone_id}/load_balancers/{load_balancer_id}` — Load Balancer Details  · required: zone_id, load_balancer_id
- `PUT /zones/{zone_id}/load_balancers/{load_balancer_id}` — Update Load Balancer  · required: zone_id, load_balancer_id  · body: default_pools:string[], fallback_pool:string, name:string
- `PATCH /zones/{zone_id}/load_balancers/{load_balancer_id}` — Patch Load Balancer  · required: zone_id, load_balancer_id  · body: (no required fields)
- `DELETE /zones/{zone_id}/load_balancers/{load_balancer_id}` — Delete Load Balancer  · required: zone_id, load_balancer_id
