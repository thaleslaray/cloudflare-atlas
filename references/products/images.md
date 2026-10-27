# Images — store, transform, optimize & deliver images at the edge

> Resize, crop, optimize and convert images **on the fly** at Cloudflare's edge — serve the best
> format/size per device without pre-generating copies. Two modes: transform images on **your own
> storage** (e.g. R2), or **host** images in Images itself for a fully managed pipeline.

## Contents
- When to use (and when not) — and Images vs R2
- Two modes (transformations vs storage)
- Binding & config
- Key API / access patterns
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Serve responsive/optimized images: auto AVIF/WebP, resize, crop, blur, sharpen, watermark, rotate.
- Avoid storing N pre-rendered copies (thumbnail/hero/mobile) — generate variants on request, cached.
- Pairs with: **R2** (store originals), Workers (transform via binding), Pages/static sites (`srcset`).
- **Images vs R2:** R2 **stores** bytes (object storage); Images **transforms/optimizes** them on the
  fly. Typical combo = originals in R2 + Images for delivery. Use Images alone only if you also want
  it to host the originals (mode 2 below).
- **Not** for: video (→ stream / media transformations), arbitrary file storage (→ r2).

## Two modes
1. **Transformations (bring your own storage)** — optimize remote images on any origin (R2, S3, your
   web server). Available on **Free and Paid**. Billed only on *Images Transformed*. URL form on a
   zone: `https://<zone>/cdn-cgi/image/<options>/<source-url>`, or in a Worker via the binding.
2. **Storage (host in Images)** — upload originals to Images; it handles storage + optimization +
   delivery. **Paid only**. Served from `https://imagedelivery.net/<account_hash>/<image_id>/<variant>`
   (or a custom domain). Billed on *Images Stored* + *Images Delivered*.

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "images": { "binding": "IMAGES" }
}
```
Transform in a Worker (input is a buffer/stream, max **20 MB**):
```ts
const out = await env.IMAGES.input(buf)
  .transform({ width: 800, height: 600, fit: "cover", format: "avif", quality: 85 })
  .output();
return out.response();
```
`wrangler dev` runs a **low-fidelity offline** version of the binding (only `width`, `height`, `rotate`,
`format`); use `wrangler dev --remote` for the full/high-fidelity API. Local dev incurs no usage charges.
Uploads use the REST API
(`/accounts/{id}/images/v1`) — wrangler has no Images commands.

## Key API / access patterns
- **Workers binding** — `env.IMAGES.input().transform().output()`; `.draw()` overlays a second input
  (watermark). Billed **per unique transformation** — repeat identical transforms within the same
  month count once; `.info()` calls aren't billed.
- **URL transforms** — `…/cdn-cgi/image/width=800,format=auto/<src>` (own zone) or
  `imagedelivery.net/<hash>/<id>/<opts>` (hosted). Format `auto` negotiates AVIF/WebP from `Accept`.
- **Variants** — named presets (e.g. `thumbnail` = `w=200,h=200,fit=cover`) for hosted images;
  defining variants does **not** count toward storage.
- **Direct Creator Upload** — backend mints a one-time `uploadURL` (`/images/v2/direct_upload`);
  client POSTs the file straight to it, so the API token never reaches the browser.
- **Signed URLs** — upload with `requireSignedURLs=true`, then HMAC-sign `path+exp` for private images.
- **Import from S3 (2026-09-10, dashboard: Hosted Images → Import from S3)** — reusable *sources*
  (bucket + IAM keys needing only `s3:Get*`/`s3:List*`) and *import jobs* (optional root path, delivery-path
  prefix, overwrite-or-skip changed files); re-running a source imports only new images. Skips archival
  classes (Glacier tiers except Instant Retrieval, Intelligent-Tiering Deep Archive) and logs them. Jobs
  **stop when hosted storage quota runs out**; abort from the job sidebar.
- **Text rasterization (2026-09-02)** — `.text()` renders a string into its own image, styled with
  `font`, `size` and `color`; the `draw` array in `cf.image` now takes a `text` key, so a caption or
  watermark no longer needs a pre-rendered PNG.
- **Hosted-image management from the binding, no API token (2026-09-02)** — `.list()` accepts
  `filter.metadata` (two operators in one condition give a bounded range, e.g. `priority: {gte: 2, lte: 5}`),
  `.signedUrl()` signs a private image server-side, and `.createDirectUpload()` mints the Direct Creator
  Upload link. Worth knowing: the token-based REST flow above is no longer the only route.

## Gotchas
- **`fit=cover`/`crop` need both `width` AND `height`** — otherwise the crop is undefined.
- **Cache your transforms** — binding responses are *not* automatically cached; enable Workers Cache
  (`"cache": {}` in wrangler + `Cache-Control` on the response) or you re-transform every request
  (repeat transforms don't re-bill, but you still pay the recompute/latency). URL/hosted delivery is
  edge-cached automatically; binding output is not.
- **AVIF is slow to encode** — first request may lag; very large images fall back to WebP/JPEG. AVIF
  output dimension is capped at **1,200 px** (other formats 12,000 px).
- **EXIF metadata** is kept only for JPEG (`metadata=copyright` default | `keep` | `none`); for every other
  output format all metadata is always discarded.
- **`9422`** on Free plan = you passed 5,000 unique transformations; cached ones still serve. Use the
  `onerror=redirect` param to fall back to the original.
- Never ship the API token to clients — use Direct Creator Upload.

## Pricing & limits
> ⚠️ Pricing changes — verify on the live page (`developers.cloudflare.com/images/pricing/`) before quoting.

**Cost drivers** (as of 2026-06):
- *Images Transformed* (BYO storage / binding): first **5,000 unique/month free**, then **$0.50 / 1,000**.
  A "unique transformation" = one image + one set of params per calendar month; `format=auto` counts once.
- *Images Stored* (hosted): **$5 / 100,000 images / month**.
- *Images Delivered* (hosted): **$1 / 100,000 delivered / month**.
- **Free plan:** transformations only (no storage), **5,000 unique/month**, no overage charge (errors instead).
- BYO storage on R2 adds R2 storage/ops costs separately (egress free).

**Key limits** — Remote (BYO): file **100 MB**, area **100 MP** (~10,000×10,000), dimension **12,000 px**
(AVIF **1,200 px**). Hosted upload: file **10 MB**, metadata 1,024 bytes. Binding `.input()`: **20 MB**.
Animated GIF/WebP: 100 MP to deliver, but >50 MP delivered untransformed. `dpr` ≤ 2, `quality` 1-100 (or `high|medium-high|medium-low|low`, default 85),
`blur` 0-250, `sharpen` 0-10. Inputs: PNG/JPEG/GIF/WebP/SVG/HEIC (AVIF input = Enterprise).
Verify on `developers.cloudflare.com/images/optimization/features/`.

## Going deeper
- Covered by the official `cloudflare` skill (`references/images/`) — use it for full API, the
  complete `TransformOptions` set, variant presets, watermarking and caching patterns.
- Exact REST API (`/images/v1`, `/images/v2/direct_upload`, variants): `references/api/images.md` — exact endpoints sliced from the OpenAPI spec (verify shapes live).
- Transform options reference → `developers.cloudflare.com/images/optimization/features/`.
