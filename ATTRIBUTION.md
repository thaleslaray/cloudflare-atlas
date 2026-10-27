# Attribution & licenses

The `cloudflare-atlas` skill is built on Cloudflare's own publicly published, open-source
materials. This file gives the required credit and notes how the content was used.

## Sources

| Source | What was used here | License |
|--------|--------------------|---------|
| [cloudflare/skills](https://github.com/cloudflare/skills) | The reference structure (5-file pattern) and product gotchas/patterns that our `references/products/*.md` adapt and condense | **Apache License 2.0** |
| [cloudflare/cloudflare-docs](https://github.com/cloudflare/cloudflare-docs) | `references/code-review/` (adapted from `.agents/skills/workers-code-review`); the adversarial fact-check technique (adapted from the `.agents/skills/eli5` review step); product facts/limits/pricing distilled from the published docs | Docs/content: **CC BY 4.0** · Code: **MIT** |
| Cloudflare Developer Docs (`developers.cloudflare.com`) | Product descriptions, limits, pricing, API endpoints (sliced from the public OpenAPI spec at [cloudflare/api-schemas](https://github.com/cloudflare/api-schemas)), changelog | Docs: **CC BY 4.0** |

## How the content was used

- **Adapted, not copied verbatim.** References were re-grounded against the live Cloudflare docs and,
  in many cases, **corrected** where the upstream curated content was out of date (e.g., KV `cacheTtl`
  minimum, Containers account limits, Images file-size caps, WAF phase order).
- Per the licenses above, this skill may be used, modified, and redistributed **with attribution**.
- This skill is an independent, community-built complement and is **not affiliated with or endorsed by
  Cloudflare or OpenAI**.

## Changes indicated (CC BY / Apache requirement)

Content was condensed, re-structured into this skill's catalog/architecture format, augmented with
pricing/cost-estimation and an offline API reference, verified against current docs, and corrected
where upstream was stale.

_Last updated: 2026-06-26._
