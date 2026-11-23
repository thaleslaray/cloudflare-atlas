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
Measured 2026-11-17 on `ai/llms.txt`: **296 model pages** (excluding the catalog index) in 33 vendor slugs — 75 `@cf` (`Cloudflare-hosted`, Workers AI
GPUs, id `@cf/<author>/<model>`) and 221 `Third-party` (32 vendors, proxied through AI Gateway, id
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
| `@cf` | 75 | Workers AI open models: mostly text generation, plus text-to-image, embeddings, ASR, TTS, translation, classification; includes Cloudflare's own `@cf/cloudflare/clef` / `clef-omni` (decisions) and `clairic` (typed-value extraction, preview), `@cf/daily-co/phonellm-mini-alpha-2` (voice agents), and — new 2026-11-12 — `@cf/google/embeddinggemma-2` (multimodal embeddings) and `@cf/thinkingmachines/inkling-2-small` (reasoning, vision) |
| `openai` | 36 | mostly text generation; image, TTS, ASR |
| `google` | 27 | Gemini text generation (incl. `gemini-4-argon`, `gemini-4-carbon`); video generation/editing with native audio (Veo, `gemini-omni-1.2-flash`), Nano Banana images (incl. `nano-banana-2.1`), TTS (`gemini-3.8-flash[-lite]-tts`) |
| `xai` / `alibaba` | 15 each | Grok text generation, image, video, ASR, TTS, a websocket voice model / Qwen text generation, Wan / HappyHorse video, Qwen images |
| `recraft` | 14 | text-to-image (V4.1 family incl. `recraftv4-1-flash`), incl. SVG variants |
| `anthropic` | 15 | Claude text generation (`Anthropic Messages` format), incl. `claude-haiku-5.5` and `claude-fable-5.2` |
| `minimax` | 16 | video (Hailuo, `h3` family), text generation, TTS, music |
| `pruna` / `bytedance` | 8 each | image/video editing and generation / `text-to-video`, `text-to-image` |
| `black-forest-labs` | 8 | FLUX text-to-image (incl. `flux-3-image-klein`); `flux-3-video`, one video upscale |
| `meta` | 6 | Muse Spark / Muse Wonder agentic and coding models (`muse-spark-open` is open weights) |
| `elevenlabs` / `bria` | 6 / 5 | TTS, music, sound effects / FIBO generate/edit, background removal (image, video), `ad-delayer` (flat ad image to editable layers) |
| `topaz` / `krea` | 4 each | Gigapixel image upscalers, Starlight video enhancement / text-to-image and editing (`krea-3`, beta) |
| `inworld` | 3 | TTS |
| `klingai` | 6 | Kling video (`kling-v3`, `kling-v3-omni`, `kling-v4`, `kling-v4-flash`) and image (`kling-v3-image`, `kling-v4-image`) |
| `assemblyai`, `pixverse`, `runwayml`, `vidu`, `veed` | 2 each | ASR; video (pixverse, runwayml, vidu); `veed/fabric-1.0[-fast]` — **lip-sync talking video** from `image_url` + `audio_url` (priced per second of video) |
| `thinkingmachines` | 2 | third-party `inkling` / `inkling-256k` open-weights reasoning (Inkling 2 Small is the Cloudflare-hosted `@cf/` one) |
| `typesafe` | 2 | `typesafe/jev` / `jev-1.14.0` decision models (typed questions → probabilities; Clef is the drop-in peer) |
| `moonshotai` | 2 | `kimi-k3`, `kimi-k3.1-pro` text generation |
| `deepseek`, `xiaomi`, `unbiased`, `particle`, `reflection-ai`, `fireworks` | 1 each | text generation (`reflection-ai/beam-1.0-501b-a23b` open weights; `fireworks/ember-1` long-context multimodal reasoning) |
| `lightricks` | 3 | LTX video |

Ids and counts drift between passes — use this table to know *what kind* of vendor sits where, then open the
live list (`developers.cloudflare.com/ai/models/`, filter by provider/task) for exact ids.

## Going deeper
- Model catalog (hosted + external): `developers.cloudflare.com/ai/models/` — see the section above.
- Full docs index: `developers.cloudflare.com/ai/llms.txt`.
- **Pricing/limits live on each product**, not here — see the per-product reference and verify on the
  live pricing page before quoting.
