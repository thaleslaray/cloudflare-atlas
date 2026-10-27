# Workers AI — run AI models on serverless GPUs at the edge

> Run open-source AI models (LLMs, embeddings, image, speech, translation) on Cloudflare's
> GPU network via a native Worker binding — no GPU to manage, pay only for what you use.

## Contents
- When to use (and when not)
- Binding & config
- The `env.AI.run` API
- Model catalog
- `toMarkdown` — document/PDF → text (no model, free)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- **Inference at the edge**: text generation (chat/completion), embeddings (RAG), image gen,
  speech-to-text, text-to-speech, translation, classification — all from a Worker, no API keys.
- You want one binding + pay-per-use Neurons, not to rent/scale GPUs or sign up with a model host.
- Pairs with: **Vectorize** (embeddings → vector search → RAG), **AI Search/AutoRAG** (managed
  RAG pipeline), **Workers/Pages/Agents** (compute), **Workflows** (durable multi-step AI).
- **Not** for: routing to *any* external provider (OpenAI, Anthropic, etc.) with caching, retries,
  and analytics → that's **AI Gateway** (can also front Workers AI). Storing vectors → Vectorize.

## Binding & config (`wrangler.jsonc`)
```jsonc
{ "ai": { "binding": "AI" } }
```
TypeScript: `interface Env { AI: Ai }` — generate it with `wrangler types` into
`worker-configuration.d.ts` and re-run it whenever the config changes.
```ts
const r = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{ role: 'user', content: 'What is Cloudflare?' }]
});
return Response.json(r); // r.response holds the text
```
Also reachable via **REST** (`POST .../accounts/{id}/ai/run/{model}`) and an **OpenAI-compatible**
endpoint (`.../ai/v1`) for existing SDKs. There are no local GPUs: Workers AI **always** reaches your
Cloudflare account to run a model, so local development **incurs usage charges** like production.

**Unified with AI Gateway (2026-08-07):** the same `env.AI.run()` binding and shared `/ai/` REST
endpoints now also reach **supported third-party providers**, not just Cloudflare-hosted models.
Add a gateway to get observability, logging, caching, security and billing controls over both:
```ts
await env.AI.run('@cf/zai-org/glm-5.2', { messages: [...] }, { gateway: { id: 'default' } });
```
`id: 'default'` auto-creates a gateway on the first authenticated request. → `products/ai-gateway.md`.

## The `env.AI.run` API
- **Text gen**: `{ messages, temperature, max_tokens, stream }` → `{ response }`. `temperature: 0`
  for deterministic output.
- **Streaming**: `{ ...input, stream: true }` returns a `ReadableStream`; pipe as SSE
  (`text/event-stream`) — iterate `for await (const chunk of stream)`.
- **Embeddings**: `{ text: [...] }` → `{ data: number[][] }`; batch many texts in one call.
- **Function calling**: pass `tools: [{ type:'function', function:{...} }]`; check `tool_calls`.
- **Image**: `{ prompt, num_steps, guidance }` → PNG bytes. **Speech**: `{ audio }` → `{ text }`.
- **Skip the capacity queue**: `options: { rejectIfBusy: true }` (3rd arg to `env.AI.run`, or in the
  REST/OpenAI-compat body) makes a *synchronous* request fail fast instead of queueing — it returns
  `429` / internal `3040` when capacity is unavailable. OpenAI clients that strip unknown fields
  silently ignore it, and the request queues normally.

## Model catalog
69 Cloudflare-hosted models (measured 2026-10-03), each addressed by a `@cf/...` ID; they share the
unified `ai/models/` catalog with 164 third-party models — vendor index in `products/ai.md`. Full
catalog (capabilities, schemas, pricing) lives as JSON under
`raw/github-repos/cloudflare-docs/src/content/workers-ai-models/` — one file per model — and at
`developers.cloudflare.com/workers-ai/models/`. Examples: `@cf/meta/llama-3.1-8b-instruct` (chat),
`@cf/baai/bge-base-en-v1.5` (embeddings), `@cf/black-forest-labs/flux-1-schnell` (image),
`@cf/openai/whisper` (STT), `@cf/meta/m2m100-1.2b` (translation). Recent additions:
`@cf/zai-org/glm-5.2` (agentic-coding text gen — function calling + reasoning, 262K-token context)
and `@cf/moondream/moondream3.1-9B-A2B` (vision language / image-to-text).

**Clef — decision models, not chat (2026-10-01; omni 2026-10-09).** `@cf/cloudflare/clef` (27B, 65,536-token
context, `$0.24`/M input tokens), `clef-flash` (9B, **24,576** tokens since the 2026-10-09 cut to `$0.038`/M — cheaper
than Jev) and `clef-omni` (30B MoE, 3B active; 64,000 tokens; `$0.15`/M). All read state as text, JSON, images or
video; **clef-omni adds audio** (WAV/MP3; video MP4/WebM with its soundtrack) as base64 data URLs in `images`/`audio`/
`videos` — max 4 audio + 2 videos per request; media is billed as input tokens, no output-token charge. They return a
**probability for every allowed answer** to typed questions — up to 64 per request: `noul` (yes/no), `choice` (pick
one of your `criteria`), `score` (ordered rubric). Same System One API as `typesafe/jev`: switch by changing endpoint +
model. Input: `{ model: "clef", state, questions }`. Use for routing/triage/policy scoring on the hot path, then hand
off to an LLM. Verify prices on the model pages. Open weights on Hugging Face.

## `env.AI.toMarkdown` — document → text (the native "read a PDF in a Worker" answer)
When the need is **extract text/data from a document** (PDF, docx, images…) inside a Worker, this
is the Cloudflare-native answer — reach for it before a WASM lib (unpdf/LiteParse) or an external
OCR (Mistral/Textract). Same `AI` binding, no extra service.

```jsonc
{ "ai": { "binding": "AI" } }
```
```ts
const obj = await env.R2.get(key);                       // the PDF you already stored
const [out] = await env.AI.toMarkdown([
  { name: "guia.pdf", blob: new Blob([await obj.arrayBuffer()], { type: "application/pdf" }) },
]);
// out = { name, mimeType, format: "markdown" | "error", tokens, data }  (data = the text)
```

- **PDF = NATIVE TEXT extraction, not OCR, not a model.** It walks the PDF's StructTree (ISO 14289
  PDF/UA) and falls back to raw page text. So it costs **zero Neurons**, touches **no rate limit**
  (limits are per-model; this path runs no model), and is fast (~0.5s for a 1-page digital PDF,
  measured). Verified live: `.../markdown-conversion/how-it-works/#pdfs`.
- **Free for PDF.** Docs say "free for most format conversions"; only **image** conversion bills
  Workers AI, because images route through `@cf/facebook/detr-resnet-50` (object detection) +
  `@cf/google/gemma-4-26b-a4b-it` (image-to-text). Cloudflare hedges the wording — don't promise a
  guaranteed $0, but for text-PDFs no model is invoked. `.../markdown-conversion/#pricing`.
- **The catch for form-like docs (invoices, tax slips):** a PDF *without* a StructTree falls back to
  raw reading-order text, where a label and its value can land far apart. Undocumented for
  tables/forms — so **verify on a real sample and checksum the extraction** (e.g. against a known
  total), never trust it blind. In practice, digital PDFs from report generators (JasperReports,
  iText…) DO carry structure and the label sits next to its value.
- **Errors are per-file, not thrown:** a bad/encrypted file comes back as `{ format: "error", error }`
  in the result array next to the good ones — branch on `format`, don't assume `.data`. Encrypted/
  password PDFs: behavior undocumented, handle defensively.
- **Options:** `{ pdf: { metadata: false }, output: { format: "text" } }` — `format` set to `text`
  under `output` (shipped 2026-07-13) drops Markdown syntax, better for regex-scraping a value; `metadata:false`
  removes the PDF header block. `.../markdown-conversion/conversion-options/`.
- **List supported formats at runtime:** `await env.AI.toMarkdown().supported()`.
- **Data posture** (matters for regulated content — tax/PII): your input is *Customer Content* —
  Cloudflare does **not** share it with other customers, does **not** train on it, and does **not**
  store it unless you separately write it to R2/KV/etc. It is NOT sent to a third party (unlike an
  external OCR). But it IS processed on Cloudflare's infra, not inside your isolate. Source:
  `.../workers-ai/platform/data-usage/`. Note the model exception: image conversion routes through
  third-party-licensed models (still on Cloudflare); pure PDF text extraction does not.
- **Alternative for HTML, not for a stored PDF:** Browser Run's `/markdown` takes a `url`/`html`, not
  a PDF blob — different tool, don't confuse them.

## Gotchas
- **`@cloudflare/ai` npm package is DEPRECATED** — use the native `env.AI` binding, never import it.
- **Local dev DOES work** (corrected 2026-07): `wrangler dev` alone runs Workers AI — it proxies to
  your real account and **bills usage even locally** (and counts toward limits). `--remote` is not
  required for AI. `env.AI` is undefined → binding missing from `wrangler.jsonc`. Source:
  `.../workers-ai/get-started/workers-wrangler/`.
- **Model availability**: IDs and the catalog change; a wrong/retired name → internal code `5007`
  ("No such model ${model} or task", HTTP 400) or `3042` (invalid model name, 404). Verify the exact
  ID on the models page before quoting.
- **Streaming output is a stream**, not a string — don't `JSON.stringify` it; iterate chunks.
- **Embedding shape**: result is `data: number[][]` (array of vectors) even for one text — index `[0]`.
- **Cold start** ~1–3s on first request to a model, then ~100–500ms. Cache hot prompts via AI Gateway.
- Common errors (internal code · HTTP, from the errors reference): `3003` incomplete request · 400 ·
  `3006` request too large · 413 · `3007` timeout · 408 · `3036` daily free neuron allocation used up
  · 429 · `3040` out of capacity · 429 · `5035` model requires a Workers Paid plan · 403 · `5016`
  model terms not accepted · 403. Quote only codes from that errors reference — a 75xx-series list once
  written here had no source and was removed 2026-08-25.

## Pricing & limits
> ⚠️ Pricing/models change — verify on `developers.cloudflare.com/workers-ai/platform/pricing/`
> (and the models page) before quoting; rates are per-model.

**The unit is the Neuron** — a normalized measure of GPU compute per request.
- Billed at **$0.011 per 1,000 Neurons**; included in Free and Paid Workers plans.
- **Free allocation: 10,000 Neurons/day** (resets 00:00 UTC); exceed it on Free → requests fail,
  on Paid → billed at the rate above. Per-model rates are quoted in tokens *and* neurons, e.g.
  Llama-3.1-8b ≈ 25.6K neurons / M input tokens; embeddings cents-per-M-tokens; images per tile+step.
- **Some models require a paid billing method** — `@cf/moonshotai/kimi-k2.6`,
  `@cf/moonshotai/kimi-k2.7-code`, `@cf/zai-org/glm-5.2`, `@cf/deepseek-ai/deepseek-v4-flash-0731`,
  `@cf/deepseek-ai/deepseek-v4-pro-0813`. Reachable with the Workers Paid plan **or** prepaid
  AI Gateway credits; on Free they fail with `5035` · 403. `.../platform/pricing/`.

**Rate limits** (per task type, default; some per-model overrides — verify on the limits page):
text generation **300 req/min**, embeddings/image-classification/object-detection **3000**,
text-to-image / STT / translation / image-to-text **720**, summarization **1500**, text
classification **2000**.
- **Frontier models are far tighter — per account, per model: 20 req/min** (kimi-k2.6,
  kimi-k2.7-code, glm-5.2), rising to **50 req/min** if you pay via prepaid AI Gateway credits with
  the gateway's Workers AI billing set to *Unified billing*. Don't plan a fan-out on glm-5.2 at the
  300/min text-gen number. `.../platform/limits/#frontier-models`.

## Going deeper
- Deep-dive: the live docs `developers.cloudflare.com/workers-ai/` (canonical, fetch as Markdown). The official `cloudflare` skill `references/workers-ai/` is an optional extra **if installed**
  (its `README.md` holds a model-selection decision tree), `configuration.md`, `api.md`, `patterns.md` (RAG, streaming,
  retry, fallback), `gotchas.md`.
- RAG pattern (embed → Vectorize query → generate) → `references/products/vectorize.md`.
- Multi-provider routing / caching / analytics → `references/products/ai-gateway.md`.
