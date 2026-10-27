# AI — umbrella for running AI models on Cloudflare

> A unified platform for AI workloads on Cloudflare's global network. **This is a landing/router,
> not a single product** — pick the real product below for inference, RAG, vectors, agents, or a
> provider proxy.

## Contents
- What this is (and isn't)
- Pick a product (router)
- Model catalog (`ai/models/`) — one catalog, two hosting modes
- Going deeper

## What this is (and isn't)
"AI" is the documentation umbrella over Cloudflare's AI stack. Its one surface of its own is the
**model catalog** (below); the binding, REST API, limits and prices belong to Workers AI and AI
Gateway. Two ways to run a model: **host it on Cloudflare** (Workers AI) or **proxy to an external
provider** (AI Gateway) — the catalog lists both behind one call path.

## Pick a product (router)
- **Run inference on Cloudflare GPUs** → **Workers AI** — serverless LLMs, embeddings, image/speech
  models via the `AI` binding. See `products/workers-ai.md`.
- **Proxy / observe / control any provider** (OpenAI, Anthropic, etc.) → **AI Gateway** — caching,
  rate limiting, retries, model fallback, analytics, logs. See `products/ai-gateway.md`.
- **Vector database** (store + query embeddings for semantic search) → **Vectorize**.
  See `products/vectorize.md`.
- **Managed RAG pipeline** (index your data → retrieval-augmented answers, end to end) →
  **AI Search** (formerly AutoRAG). See `products/ai-search.md`.
- **Build agents** (stateful, tool-using, durable, real-time) → **Agents** (Agents SDK on Workers +
  Durable Objects). See `products/agents.md`; conversation/state in `products/agent-memory.md`.

**Common pattern:** Agents/Workers run inference via **Workers AI** (or external providers through
**AI Gateway**), retrieve context from **Vectorize** / **AI Search**, and persist state in
**Durable Objects** / **D1**.

Adjacent AI-flavored products (not the core five):
- **Browser Run** (formerly Browser Rendering) — headless browser for AI data extraction
  (`products/browser-run.md`).
- **AI Crawl Control** — analyze/control third-party AI crawlers (`products/ai-crawl-control.md`).
- **Sandbox SDK** — isolated code execution for agents (`products/sandbox.md`).
- **Dynamic Workers** — spin up isolated Workers on demand (`products/dynamic-workers.md`).
- **Cloudflare Agent** (Agent Lee) — AI assistant that navigates, configures, and manages
  Cloudflare itself; an operations tool, not a building block (`products/agent-lee.md`).

## Model catalog (`ai/models/`) — one catalog, two hosting modes
Measured 2026-10-12 on `ai/llms.txt`: **242 model pages** — 70 `@cf` (`Cloudflare-hosted`, Workers AI
GPUs, id `@cf/<author>/<model>`) and 172 `Third-party` (proxied through AI Gateway, id
`<vendor>/<model>`, e.g. `openai/gpt-4.1`). **Same call path for both:**
`env.AI.run(id, input, { gateway: { id } })`; over REST, text models take `/ai/v1/chat/completions`
and every modality takes `/ai/run` with `{ "model", "input" }`. Each model page carries context
window, request formats (`Chat Completions`, `Responses`, `Anthropic Messages`), a zero-data-retention
flag, and per-model pricing — read the page, never quote a price from memory.

**Who pays for a third-party call** (`ai-gateway/features/unified-billing/`): provider key on the
request → stored BYOK key under the `default` alias → **Unified Billing** credits (provider rate,
no markup; 5% fee on credit purchases). Details and gotchas → `products/ai-gateway.md`; `@cf/` models
bill in Neurons → `products/workers-ai.md`.

| vendor slug | pages | what it hosts |
|---|---|---|
| `@cf` | 70 | Workers AI open models: mostly text generation, plus text-to-image, embeddings, ASR, TTS, translation, classification; includes Cloudflare's own `@cf/cloudflare/clef` / `clef-omni` (audio+video decisions) |
| `openai` | 32 | mostly text generation; image, TTS, ASR |
| `google` | 22 | Gemini text generation; Veo video, Nano Banana images, TTS (`gemini-3.8-flash[-lite]-tts`) |
| `alibaba` | 15 | Qwen text generation; Wan / HappyHorse video, Qwen images |
| `xai` | 15 | Grok text generation; image, video, ASR, TTS, a websocket voice model |
| `recraft` | 13 | text-to-image, incl. SVG variants |
| `anthropic` | 13 | Claude text generation (`Anthropic Messages` format) |
| `minimax` | 9 | video, text generation, TTS, music |
| `bytedance` | 8 | text-to-video, text-to-image |
| `pruna` | 8 | `image-to-image`, `image-to-video`, plus one each `text-to-image` / `text-to-video` |
| `black-forest-labs` | 7 | FLUX text-to-image; one text-to-video, one video upscale |
| `elevenlabs` | 5 | TTS; music |
| `bria` | 4 | FIBO generate/edit images; background removal (image RMBG 2.0, video ≤60 s) |
| `inworld` / `krea` | 3 each | TTS / text-to-image |
| `assemblyai`, `pixverse`, `runwayml`, `vidu` | 2 each | ASR; video (other three) |
| `thinkingmachines` | 2 | Inkling open-weights reasoning model |
| `deepseek`, `moonshotai`, `unbiased` | 1 each | text generation |
| `lightricks` | 1 | LTX video |
| `typesafe` | 1 | `typesafe/jev` decision model (typed questions → probabilities; Clef is its drop-in peer) |

Ids and counts drift between passes — use this table to know *what kind* of vendor sits where, then open the
live list (`developers.cloudflare.com/ai/models/`, filter by provider/task) for exact ids.

## Going deeper
- Model catalog (hosted + external): `developers.cloudflare.com/ai/models/` — see the section above.
- Full docs index: `developers.cloudflare.com/ai/llms.txt`.
- **Pricing/limits live on each product**, not here — see the per-product reference and verify on the
  live pricing page before quoting.
