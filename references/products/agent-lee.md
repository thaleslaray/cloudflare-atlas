# Agent Lee — AI co-pilot inside the Cloudflare dashboard

> An AI assistant built into the Cloudflare dashboard. Ask about your account, run diagnostics, and
> take actions (DNS, zone settings, security rules) in plain language — **a tool for OPERATING
> Cloudflare, not a building block you ship a product with.**

## Contents
- When to use (and when not)
- What it can / can't do
- Gotchas
- Availability & pricing
- Going deeper

## When to use
- You're **in the Cloudflare dashboard** and want to navigate, configure, or troubleshoot by asking
  in natural language instead of clicking through menus.
- Open it: log in to the [dashboard](https://dash.cloudflare.com) → **Ask AI** (upper-right of any page).
- Good for: "Add an A record for blog.example.com → 192.0.2.10", "Enable Always Use HTTPS",
  "Set SSL mode to Full (strict)", DNS lookups / cert checks / WHOIS, "chart my traffic last 7 days".
- **NOT a product you build with.** It's a dashboard operator/co-pilot — there's no binding, no API,
  no SDK. If you want to BUILD an AI agent on Cloudflare, that's the **Agents SDK** (`agents`/`agents-sdk`),
  which is what Agent Lee itself is built on — not this.

## What it can / can't do
**Can:** answer from your *actual* account data (zones, DNS, WAF/firewall, Workers routes/bindings,
R2 bucket names, Tunnel config, cache rules, registrar data); create/update/delete resources
(**every write needs your explicit approval** before it runs); run network diagnostics; render inline
charts from your analytics.

**Can't:** write Workers scripts or generate app code · access payment/billing, passwords, or API
tokens · query raw logs / Logpush · operate across multiple accounts (scoped to your authenticated
account) · remember previous conversations (each session starts fresh) · replace Cloudflare Support
for billing/account-recovery/outages.

## Gotchas
- **Beta** — features and behaviors may change.
- **No write executes without your approval** — it shows the plan and waits for confirmation.
- **Stateless across sessions** — it does not reference prior conversations when responding.
- **Opt-in / optional** — if you never open the Ask AI panel, no data is sent to it. Conversations are
  stored per-user in Durable Objects (isolated to your account), retained ~1 year; not used for model
  training as of this writing.

## Availability & pricing
> ⚠️ Beta product — verify current availability/pricing on the live docs before quoting.

- **Beta, Free-plan accounts only** at the time of writing. No separate pricing published for the
  feature itself.
- Built on Cloudflare's own platform: Agents SDK (lifecycle/state), Durable Objects (conversation
  store + approval gate), Workers AI (inference), Cloudflare MCP server (tool definitions).

## Going deeper
- **Naming:** its own docs page is titled **Agent Lee**; the AI product index
  (`developers.cloudflare.com/ai/llms.txt`) lists the same URL as **"Cloudflare Agent"**. Both names
  point to `/agent-lee/`.
- Docs: `developers.cloudflare.com/agent-lee/` · Blog: "Introducing Agent Lee".
- Want to **build** an agent like this? → the `agents` / `agents-sdk` reference + Human-in-the-Loop pattern.
