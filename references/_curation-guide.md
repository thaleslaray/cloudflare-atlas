# Curation guide — products/<slug>.md for cloudflare-atlas

You curate ONE Cloudflare product reference file. Follow this exactly.

## Format
Mirror `<workbench>/references/products/r2.md`:
title + 1-line summary blockquote → `## Contents` (TOC) → When to use (and when not) → Binding & config
(`wrangler.jsonc` if applicable) → Key API / access patterns → Gotchas → Pricing & limits → Going deeper.
Concise, scannable. ≤120 lines for covered products, ≤150 for new ones.

**The cap yields to verified fact — it is a budget, not a gate.** Operator decision, 2026-08-26:
when every line in an over-cap file carries a fact checked against the live docs, do NOT cut to hit
the number. Cutting then trades correctness for tidiness, which is backwards for this skill. The
files below are over cap ON PURPOSE, with the count measured that day. Do not "fix" them by
deleting content; only by finding genuine redundancy.

| file | lines | cap | why it stands |
|------|-------|-----|----------------|
| `sandbox.md` | 152 | 120 | **Rewritten 2026-10-03 around SDK 1.0** (309 → 150). +2 on 2026-10-31: pin `0.12.14` after the eMudhra certificate revocation (what 1.x users must rebuild), `follow-a-background-process` pointer; the unsourced "600 ms" start figure was dropped. 91/91 confirmed. |
| `agents.md` | 180 | 150 | Re-mapped on 2026-10-31 to the restructured Agents docs (`agent-class/`, `runtime/capabilities/`, `runtime/routing/`, `skills/`) at the SAME length: Pi 1.4 (`~1.4.0` peers, no rollback), OpenCode harness, `createAI`, File system (`@cloudflare/computer`), Agent Skills, `/sse` retired; absorbed by compressing the old computer-preview and quickstart text. 143/147 (4 changelog-only tokens, accepted). |
| `think.md` | 178 | 150 | +8 on 2026-10-31: Computer `Workspace` replaces `@cloudflare/shell` (deprecated with `createExecuteTool`), new tool set `read ls find grep write edit delete` (+`exec`/`publish`), breaking migration pointer, `createAI`, `getSkills()`; renamed from "Project Think". 130/130 confirmed. |
| `privacy-pass.md` | 162 | 150 | Verified 2026-08-26: ~30 claims checked, **zero errors, nothing changed**. No redundancy found to cut. |
| `workers-ai.md` | 186 | 120 | Error table + rate limits + paid-model gating, all cited. +12 on 2026-10-31: Clairic extraction model paragraph, `createAI`/Pi AI configuration, `deepseek-v4.1-flash-1017` and `phonellm-mini-alpha-2`, paid-model list (`glm-5.3`); the 20/50 req/min limit now applies to every Workers-Paid model. 99/99 confirmed. |
| `ai-search.md` | 160 | 120 | 30 claims verified; limits table is most of the excess. +2 on 2026-09-15 (extensionless R2 objects need Content-Type). +9 on 2026-11-05: billing starts 2026-12-01 (was "FREE"), included usage 1,000 semantic + 1,000 full-text queries, sync default 24 h and allowed `sync_interval` values, file caps 10 MiB / 4 MiB. 72/76 (4 baseline). |
| `email-service.md` | 148 | 120 | **Fully audited 2026-10-03.** +7 on 2026-10-31: total message size corrected to **25 MiB** incl. attachments (was 5 MiB — no live page says 5 any more), local dev (`wrangler dev` simulates `send_email`, `"remote": true` sends), Queues event subscriptions (6 event types, routing not published), Wrangler `addresses` routing rules. |
| `waf.md` | 147 | 120 | Application Profiles 2026-08-25; Attack Signature Detection 2026-09-15. +13 on 2026-10-31: **Use cases** section (block Worker subrequests via `cf.worker.upstream_zone`, Tor, attack score + country, bad bots), closing backlog #1 of 10-12; `failed_detections` detection IDs added from the ruleset-engine field reference (accepted with evidence). |
| `workers.md` | 152 | 120 | Limits block by plan. +2 on 2026-11-05: defaults flipping at compat date 2026-11-17 (new module registry, `Request.signal`), Vite plugin v2 beta; absorbed by compressing older lines. 121/121. +6 net on 2026-10-31: `connect()` handler, source maps uploaded by default (Wrangler 4.150.0, opt-out), Workers Builds (`packageManager` pin, 90-day retention, eMudhra CAs rejected), `assets.base_path`, BYOIP subrequest context, tracing `spanContext()`/`setStatus()`/`updateName()`, MongoDB gotcha. 108/108 confirmed. |
| `containers.md` | 147 | 120 | GA + instance-type table + 2026-08 reorg path map. +15 on 2026-10-03 for the `durable_object` scheduling policy and filesystem snapshots (public beta 2026-09-30), plus three corrections (disk:memory ratio removed, Version URLs wording, Previews container apps). |
| `tunnel.md` | 150 | 120 | 2026-09-15 docs split + error triage + token rotation + RBAC + sizing. +11 on 2026-10-31: Tunnels for Platforms (1,000 included, $4.50/tunnel/month beyond — replaces a wrong "unlimited"), routes 50,000/account, URL normalization (`cloudflared` ≥2026.10.0, default-on from 2027-01-25), Read And Monitor role GA. |
| `realtime.md` | 143 | 120 | +20 on 2026-10-31: RealtimeKit docs restructured into `humans/` (SDKs, ~630-page reference not mirrored) / `agents/` / `platform/`; **Agent Participant** (server-side, `agent-ws/v1`, receive-only today, billed as a participant), RealtimeKit limits (3,500 req/5 min, SDK per-participant rates), network allowlist; pricing URL moved to `platform/pricing/`, "Beta — free" removed as the live page no longer says it. 60/60 confirmed. |
| `ai-gateway.md` | 168 | 120 | +19 on 2026-11-05: required authentication for new gateways (cannot be disabled once on), Routing section rebuilt for the `features/routing/` reorg (Auto Router, model aliases, dynamic routes with limits/errors), two corrections (dynamic routes not only on `/compat`; `Authorization` vs `cf-aig-authorization` by endpoint). 108/108. +10 on 2026-10-31: `createAI` replaces `ai-gateway-provider` (frozen), Cursor and Android Studio coding agents, `ai_gateway_events` Logpush dataset, UUIDv7 ids; Logpush pricing/limits corrected (all plans; Workers Logs vs Legacy Logs by gateway creation date). 84/84 confirmed. |
| `durable-objects.md` | 127 | 120 | +4 on 2026-10-31: deferred code updates by default (`code_update_strategy`, `max_delay` 300 s default / 86,400 max, per-deploy flag), offset by removing a gotcha that duplicated Lifecycle. |
| `browser-run.md` | 151 | 120 | +2 on 2026-10-31: Chrome 152 default and the Quick Actions `Chrome/152.0.0.0` User-Agent (was 119). |
| `mesh.md` | 173 | 150 | +24 on 2026-10-31: `run-mesh-on-linux` rewritten (RHEL needs CodeReady Builder + EPEL RPM, repo install, dashboard-first node creation), `connect-servers`, `connect-sites` and `troubleshooting` guides folded in, each statement checked live; unverifiable private-range tokens dropped. 51/57 → baseline, no new. |
| `cache.md` | 133 | 120 | Recorded 2026-10-03 (was 124, undocumented). Purge vs `invalidate_cache` (2026-09-28) and the every-purge-forces-Reserve-miss change; duplicates cut. |
| `dynamic-workers.md` | 147 | 150 | New-file cap; unchanged length on 2026-10-03. |
| `logs.md` | 135 | 120 | +14 on 2026-10-03: Logpush usage-based pricing on all plans (2026-09-30, three meters + Workers Logpush unchanged), Transformers GA, `filter_attack_traffic`. 80/80 tokens confirmed. |
| `analytics.md` | 124 | 120 | +2 on 2026-10-31: SQL API introspection `include_attributes=true` (`include_custom_attributes` deprecated). |
| `rules.md` | 122 | 120 | Found at 120 and unrecorded; +2 on 2026-10-31 for the Rules simulator (formerly Cloudflare Trace, `rules/simulator/`). |
| `dns.md` | 134 | 120 | +9 on 2026-11-05: Private origins (beta; Tunnel vs Mesh/WAN setup, return routes). +13 on 2026-10-31: `nameservers.type: "cloudflare.advanced"` rollout, nameserver sets (beta, Enterprise; 2–5 names, immutable), new DNS records page default. |
| `notifications.md` | 125 | 120 | +11 on 2026-10-31: **Monitors** (scheduled SQL API queries; Threshold / Anomaly / SLO detection; 20-email limit); webhooks corrected to all plans (was "Pro or higher"). |
| `cloudflare-challenges.md` | 124 | 120 | +6 on 2026-10-31: Precursor modes Off/Monitor/Armed, Precursor Interstitial + Interstitial Rules replace the gone "Maximize Security"/"Precursor Rules" names; China-native Challenge Pages. |
| `agent-memory.md` 126 · `agent-setup.md` 133 (2026-10-12: MCP section rewritten; +6 on 2026-10-31: 12 agents incl. Droid/Pi/Command Code/Vibe, `/sse` → `410 Gone`) · `cloudflare-for-platforms.md` 129 · `privacy-proxy.md` 126 · `ruleset-engine.md` 124 · `speed.md` 126 · `ssl.md` 135 (+6 on 2026-11-05: Keyless SSL section — Enterprise add-on, `gokeyless`, TLS 1.3 with ECDSA) · `load-balancing.md` 121 (+3 on 2026-11-05: private LB session affinity/hash steering; "39 probes" re-verified, Enterprise-only) | — | 120/150 | **Found over cap and unrecorded on 2026-10-03; not touched this pass.** Recorded at their measured length so the next pass sees them. Created as new files they would sit under the 150 cap; none was audited for padding today. |

When a NEW file would exceed its cap, still push back: the cap catches padding. This exemption is
for files whose length is measured fact, and it is recorded per-file so the next pass does not
re-litigate it from scratch.

## Source material (all under <workbench>/../raw/)
- Rendered docs: `docs-oficiais/pages/<slug>/`  and  `docs-oficiais/full/<slug>.md`
- Pricing: `docs-oficiais/pages/<slug>/**/pricing*`   ·   Limits: `docs-oficiais/pages/<slug>/**/limits*`
- Official skill ref (may or may not exist): `cloudflare-skills-repo/skills/cloudflare/references/<slug>/`
  (slug may differ — e.g. catalog "agents" → official "agents-sdk"; check nearby names)

## Depth rule (decides how much to write)
- **Official ref EXISTS** → keep LEAN. Cover what's distinctive + bindings/config + top gotchas +
  pricing/limits. In "Going deeper", POINT to the official `cloudflare` skill `references/<slug>/`
  instead of duplicating its full API/patterns.
- **No official ref** → write a FULLER reference (it's the primary source): what it is, when to use,
  how to wire it, key concepts/API, gotchas, pricing/limits.

## Pricing rule (most important — pricing is volatile)
State the cost DRIVERS (what you pay per: requests, GB stored, GB egress, rows, neurons, etc.) + the
free tier, from the docs. ALWAYS add the caveat: "verify on the live pricing page before quoting".
If the product is beta / needs access / has no public pricing, say so prominently. Include key limits.

## Grounding
Prefer the rendered docs (`pages/`) for exact numbers — they're current. If the official skill ref
disagrees with the docs on a number, trust the docs and use the doc value.

## Output
Write to `<workbench>/references/products/<slug>.md`.
Reply with one line: the slug + final line count.
