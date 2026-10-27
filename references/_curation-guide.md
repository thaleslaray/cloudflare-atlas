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
| `sandbox.md` | 150 | 120 | **Rewritten 2026-10-03 around SDK 1.0** (shipped 2026-09-30) — the predicted collapse happened: 309 → 150. Carries the 1.0 surface, the mandatory one-way 0.x migration note (0.x supported until 2026-12-31) and the coding-agents catalog; all 86 checked tokens confirmed. TOC is a 2-line inline list to fit. |
| `agents.md` | 180 | 150 | Verified across the SDK, MCP portals, Code Mode and background sub-agents. 2026-10-03: +Pi harness/model providers and Workers OAuth Provider v1, absorbed by compressing portals/computer/observability (facts dropped are listed in the 2026-10-03 CHANGELOG entry). |
| `think.md` | 170 | 150 | 47 claims verified against the subtree AND the parent runtime docs |
| `privacy-pass.md` | 162 | 150 | Verified 2026-08-26: ~30 claims checked, **zero errors, nothing changed**. No redundancy found to cut. |
| `workers-ai.md` | 174 | 120 | Error table + rate limits + paid-model gating, all cited. +4 on 2026-09-21 for `rejectIfBusy`. +10 on 2026-10-03 for Clef decision models (`@cf/cloudflare/clef`, `clef-flash`), verified on the model pages + changelog. +1 on 2026-10-12: Clef paragraph rewritten for clef-omni and the clef-flash price cut. |
| `ai-search.md` | 151 | 120 | 30 claims verified; limits table is most of the excess. +2 on 2026-09-15 (extensionless R2 objects need Content-Type), verified on the R2 data-source page. |
| `email-service.md` | 141 | 120 | **Fully audited 2026-10-03** (~95 claims vs 15 live pages; 8 errors fixed, 3 redundancies cut) — closes the old "12 unaudited lines" note. +3 net for suppression scope (`account`/`sending_domain`, 2026-09-25) and the Drop-suppressed-recipients setting. |
| `waf.md` | 134 | 120 | Application Profiles added 2026-08-25; Attack Signature Detection added 2026-09-15 (10 lines, every claim checked against its 4 live pages) |
| `workers.md` | 144 | 120 | Limits block (request-body size by Cloudflare plan, all four tiers). +6 on 2026-10-03 for Workers Previews (limits, isolation, config), the Analytics SQL binding, ML-KEM/ML-DSA, Workflows via `ctx.exports`; partly absorbed by compressing the Static Assets gotcha. +1 on 2026-10-12: profiling in production. |
| `containers.md` | 147 | 120 | GA + instance-type table + 2026-08 reorg path map. +15 on 2026-10-03 for the `durable_object` scheduling policy and filesystem snapshots (public beta 2026-09-30), plus three corrections (disk:memory ratio removed, Version URLs wording, Previews container apps). |
| `tunnel.md` | 139 | 120 | 2026-09-15 docs split + error triage + token rotation + RBAC + sizing. +5 on 2026-10-03: Quick Tunnel `--allowed-mail` email auth and `DestinationReplicaID` ↔ Connector ID. |
| `realtime.md` | 123 | 120 | +3 on 2026-09-15 (RealtimeKit retention table), verified live. |
| `ai-gateway.md` | 139 | 120 | +3 on 2026-09-15 (cache-token custom costs); +12 on 2026-10-03 for Machine Payments (x402), User Insights savings, the Web Search pointer and the corrected BYOK/Unified Billing credential order. +4 on 2026-10-12: standardized credential errors (401/2009, 503 on Unified Billing) and Gemini CLI/VS Code/Xcode. |
| `durable-objects.md` | 123 | 120 | Recorded 2026-10-03 (was 122, undocumented). Pending I/O eviction rules (2026-10-01) split into before/after groups, plus `exports` replacing `migrations`. |
| `browser-run.md` | 149 | 120 | Recorded 2026-10-03 (was 139, undocumented). +10 for WebMCP on Kitesurf/Lab (2026-09-28) and multi-client sessions (2026-09-29), verified live. |
| `mesh.md` | 149 | 150 | New-file cap (141 at creation 2026-09-21). +4 on 2026-10-03: node sizing corrected to live figures, Mesh session-log fields. |
| `cache.md` | 133 | 120 | Recorded 2026-10-03 (was 124, undocumented). Purge vs `invalidate_cache` (2026-09-28) and the every-purge-forces-Reserve-miss change; duplicates cut. |
| `dynamic-workers.md` | 147 | 150 | New-file cap; unchanged length on 2026-10-03. |
| `logs.md` | 135 | 120 | +14 on 2026-10-03: Logpush usage-based pricing on all plans (2026-09-30, three meters + Workers Logpush unchanged), Transformers GA, `filter_attack_traffic`. 80/80 tokens confirmed. |
| `analytics.md` | 122 | 120 | +18 on 2026-10-03 for the Analytics SQL API (endpoint, dataset prefixes, Worker binding, limits) and the 30-day retention change, offset by trimming. 53/53 confirmed. |
| `agent-memory.md` 126 · `agent-setup.md` 127 (2026-10-12: MCP section rewritten for the trimmed catalog + skills over MCP) · `cloudflare-for-platforms.md` 129 · `privacy-proxy.md` 126 · `ruleset-engine.md` 124 · `speed.md` 126 · `ssl.md` 129 | — | 120/150 | **Found over cap and unrecorded on 2026-10-03; not touched this pass.** Recorded at their measured length so the next pass sees them. Created as new files they would sit under the 150 cap; none was audited for padding today. |

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
