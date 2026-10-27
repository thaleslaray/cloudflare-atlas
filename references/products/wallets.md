# Cloudflare Wallets — programmable wallet + payment identity for agents

> ⚠️ **Not launched.** Today the product is *handle reservation only* — a name that will later
> become a payment identity. No funds, no API, no binding. Announced 2026-08; docs landed 2026-08-19.
> When it ships: stablecoin wallets that let a Cloudflare account **delegate a capped spend budget
> to its AI agents**, so an agent can pay for APIs and content without per-purchase approval.

## Contents
- What exists today (and what does not)
- The two wallet types (announced design)
- Binding & config
- Gotchas
- Pricing & limits
- Going deeper

## What exists today
- Reserve **one handle per Cloudflare account** at `cloudflare.pay`. Free.
- A reserved handle: associates the name with the account, publishes a page at
  `HANDLE.cloudflare.pay` showing only the handle, and registers the account for launch notification.
- **A reserved handle cannot send, receive, or hold funds.** Nothing else in the product is live.

## The two wallet types (announced design, not yet shippable)
| Type | For | Model |
|------|-----|-------|
| **Account Wallet** | humans who own/use a Cloudflare account | add funds, **delegate spend** to virtual wallets, remove funds; may carry the `cloudflare.pay` identifier |
| **Virtual Wallet** | agents | operates via **API keys**; spends within its permissions, **capped by the limit the Account Wallet owner sets** |

The point of the split: an agent acts without constant manual approval, but cannot overspend.
First asset class at launch is **stablecoins** (send / receive / hold).

## Binding & config
**None.** There is no Worker binding, no `wrangler.jsonc` entry, and no REST API surface for Wallets
today — do not invent one. Handle reservation is a web flow at `cloudflare.pay`, not an API call.

For agent-side payments that DO work today, the shipped mechanism is **x402** via
`agents/tools/payments/` — charge for HTTP content and MCP tools, or pay for them from an agent.
Wallets is the future funding source for that flow, not a replacement for it.

## Gotchas
- **First come, first served, and effectively permanent.** Cloudflare offers **no way to change,
  release, or transfer** a handle once reserved — explicitly including after a rebrand. Only route
  is a support ticket.
- **Reserving ≠ access.** The docs state plainly that a reservation does not guarantee access to a
  Cloudflare Wallet on release.
- **Cloudflare may reject or reclaim** any handle reservation, for any reason.
- One handle per account — a multi-brand operator needs separate Cloudflare accounts.
- Trademark/abuse complaints go through `abuse.cloudflare.com`, not support.

## Pricing & limits
> ⚠️ Pre-launch product — verify on the live page (`developers.cloudflare.com/wallets/`) before
> quoting anything. There is **no published pricing** for the wallet itself; fee structure for
> holding or moving stablecoins has not been announced.

- **Handle reservation: free.**
- **Limit:** 1 handle per Cloudflare account. No other quotas published.

## Going deeper
- Live docs: `developers.cloudflare.com/wallets/` (2 pages: overview + FAQ) — canonical, fetch as Markdown.
- Announcement (the only full description of the design): `blog.cloudflare.com/wallets/`.
- Agentic payments that work today → `products/agents.md` and `developers.cloudflare.com/agents/tools/payments/`.
- No `references/api/wallets.md` — the product has no REST surface in the OpenAPI spec.
