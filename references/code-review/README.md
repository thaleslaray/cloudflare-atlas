# Code Review — Workers, wrangler & bindings

The review process, rules, anti-patterns, and output format for reviewing Cloudflare Workers and Developer Platform code. Load this when reviewing TypeScript/JavaScript that uses Workers APIs, `wrangler.jsonc`/`wrangler.toml` config, or Cloudflare bindings (KV, R2, D1, Durable Objects, Queues, Vectorize, AI, Hyperdrive).

## Contents

- [Reference sources](#reference-sources) — where to verify types and config
- [Review process](#review-process) — context, categorize, validate, check, risk
- [Quick-reference rules](#quick-reference-rules)
- [Anti-patterns to flag](#anti-patterns-to-flag)
- [What NOT to flag](#what-not-to-flag)
- [Output format](#output-format)
- Detailed rules: [`patterns.md`](./patterns.md) · [`types.md`](./types.md) · [`wrangler.md`](./wrangler.md)

Your knowledge of Workers APIs, types, and wrangler config may be outdated. **Prefer retrieval over pre-training** for any Workers review task.

## Reference Sources

Verify against the project's own installed packages when present; otherwise fall back to the live Cloudflare docs. Do **not** run `npm pack` or install packages to fetch types.

| Source                 | Where to find it                                                                                                              | Use for                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| Workers types          | Read `node_modules/@cloudflare/workers-types/index.d.ts` IF present; otherwise verify against the live Cloudflare docs.      | API usage, handler signatures, binding types  |
| Wrangler config schema | Read `node_modules/wrangler/config-schema.json` IF present; otherwise verify against the live Cloudflare docs.               | Config fields, binding shapes, allowed values |
| Cloudflare docs        | The live documentation at developers.cloudflare.com (or a docs search tool if one is available).                            | API reference, compatibility dates/flags      |

Read these directly when you need to confirm a type, config field, or API signature. The guides here describe *what* to validate, not how to fetch packages.

## Review Process

### 1. Build context

Read full files, not just diffs or isolated snippets. Code that looks wrong in isolation may be correct given surrounding logic.

- Identify the purpose: complete Worker, snippet, or configuration example?
- Check git history for context: `git log --oneline -5 -- <file>`
- Understand which bindings, types, and patterns the code depends on.

### 2. Categorize the code

Review each block **in the context** of its category.

| Category          | Definition                                                  | Expectations                                         |
| ----------------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| **Illustrative**  | Demonstrates a concept; uses comments for most logic       | Correct API names, realistic signatures              |
| **Demonstrative** | Functional but incomplete; works in the right context      | Syntactically valid, correct APIs and binding access |
| **Executable**    | Standalone and complete; runs without modification         | Compiles, runs, includes imports and config          |

### 3. Validate with tools

Tool output is evidence, not opinion. Run what the project supports:

```bash
npx tsc --noEmit          # TypeScript errors
npx eslint <files>        # Lint issues
```

For config files, validate against the wrangler config schema (see [`wrangler.md`](./wrangler.md)) and confirm fields, binding types, and values conform.

### 4. Check against rules

See [`patterns.md`](./patterns.md) for API/runtime patterns, [`types.md`](./types.md) for type-system rules, and [`wrangler.md`](./wrangler.md) for config validation.

### 5. Assess risk

| Risk       | Triggers                                                                                                    |
| ---------- | ---------------------------------------------------------------------------------------------------------- |
| **HIGH**   | Auth, crypto, external calls, value transfer, validation removal, access control, binding misconfiguration |
| **MEDIUM** | Business logic, state changes, new public APIs, error handling, config changes                             |
| **LOW**    | Comments, logging, formatting, minor style                                                                 |

Focus deeper analysis on HIGH risk; check blast radius on critical paths. **Security escalation:** for crypto/auth/timing-sensitive code, do not stop at verifying API calls are correct — examine the surrounding logic for flaws that undermine the security property (see the Security section in [`patterns.md`](./patterns.md)).

## Quick-reference Rules

| Rule                    | Detail                                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Binding access          | `env.X` in module export handlers; `this.env.X` in classes extending platform base classes. See `patterns.md`.               |
| No `any`                | Never use `any` for binding types, handler params, or API responses. Use proper generics. See `types.md`.                    |
| No type-system cheats   | Flag `as unknown as T`, unjustified `@ts-ignore`, unsafe assertions. See `types.md`.                                         |
| Config-code consistency | Binding names in wrangler config must match `env.X` usage in code. See `wrangler.md`.                                        |
| Required config fields  | Verify against the wrangler config schema — do not assume which fields are required. See `wrangler.md`.                      |
| Concise examples        | Focus on core logic. Minimize boilerplate that distracts from what the code teaches.                                         |
| Floating promises       | Every `Promise` must be `await`ed, `return`ed, `void`ed, or passed to `ctx.waitUntil()`. See `patterns.md`.                  |
| Serialization           | Data crossing Queue, Workflow step, or DO storage boundaries must be structured-clone serializable. See `patterns.md`.       |
| Streaming               | Large/unknown payloads must stream, not buffer. Flag `await response.text()` on unbounded data. See `patterns.md`.           |
| Error handling          | Minimal but present — null checks on nullable returns, basic fetch error handling. Avoid verbose try/catch. See `patterns.md`. |

## Anti-patterns to Flag

| Anti-pattern                                                                  | Why it matters                                                             |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `any` on `Env` or handler params                                              | Defeats type safety for every binding access downstream                    |
| `as unknown as T` double-cast                                                 | Hides real type incompatibilities — fix the underlying design              |
| `@ts-ignore` / `@ts-expect-error` without explanation                         | Masks errors silently; require a comment justifying each suppression       |
| Buffering unbounded data (`await res.text()`/`.json()` on streams)            | Memory exhaustion on large payloads; use streaming                         |
| Hardcoded secrets or API keys                                                 | Use `env` bindings and `wrangler secret put`                               |
| `blockConcurrencyWhile` on every request                                      | Only for initialization; blocks all concurrent requests                    |
| Single global Durable Object                                                  | Creates a bottleneck; shard by coordination atom                           |
| In-memory-only state in DOs                                                   | Lost on eviction; persist to SQLite storage                                |
| Missing DO migrations in config                                               | New DO classes require migration entries or deployment fails               |
| Floating promises (`step.do()`, `fetch()` without `await`)                    | Silent bugs — drops results, breaks Workflow durability, ignores errors    |
| Non-serializable values across boundaries (`Response`, `Error` in step/queue) | Compiles but fails at runtime; extract plain data before crossing boundary |
| `implements` instead of `extends` on platform base classes                    | Legacy pattern — loses `this.ctx`, `this.env` access from base class       |

## What NOT to Flag

- Style not enforced by linters
- "Could be cleaner" when code is correct and clear
- Theoretical performance concerns without evidence
- Missing features not in scope of the example
- Pre-existing issues in unchanged code

## Output Format

```
**[SEVERITY]** Brief description
`file.ts:42` — explanation with evidence (tool output, type error, config mismatch)
Suggested fix: `code` (if applicable)
```

Severity: **CRITICAL** (security, data loss, crash) | **HIGH** (type error, wrong API, broken config) | **MEDIUM** (missing validation, edge case, outdated pattern) | **LOW** (style, minor improvement)

End with a summary count by severity. If no issues are found, say so directly.

**Principles:** Be certain — investigate before flagging. Provide evidence (line numbers, tool output, schema fields, type defs). Correctness over completeness. Respect existing patterns. Code in docs gets pasted into production — treat it accordingly.

---

*Adapted from cloudflare/cloudflare-docs .agents/skills/workers-code-review (check its LICENSE).*
