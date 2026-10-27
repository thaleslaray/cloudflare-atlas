# Containers — serverless containers attached to Workers

> Run any language/runtime as a Linux container, spun up on-demand and controlled from your
> Worker. Each container is backed by a **Durable Object** — no Kubernetes, no infra to manage.
> Use it when a Worker isn't enough: full OS/filesystem, heavy runtimes, existing images.

## Contents
- When to use (and when not)
- Binding & config
- Access patterns
- `durable_object` scheduling policy & snapshots (beta)
- Deploying (machine & Workers Builds)
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You need a **full container/OS**: a real filesystem, system deps, specific runtime, or a
  Linux-like environment a Worker can't give you (Worker = V8 isolate, no fs, JS/Wasm only).
- **Heavy compute** (multi-core, big memory/disk, long-running) or **existing images** (any language, ffmpeg, browsers).
- **Stateful, long-lived processes**: sessions, games, WebSockets, per-user/job isolation.
- **Not** for: stateless request/response, sub-ms cold starts, scale-to-zero-instantly — that's a
  plain **Worker**. Container cold starts take **on the order of seconds** (docs give no fixed number —
  it depends on image size and what the entrypoint does) and deploys are rolling, not instant.

## Binding & config (`wrangler.jsonc`)
A container is a Durable Object that extends the `Container` class. You declare BOTH a `containers`
entry (the image) and a `durable_objects` binding (the addressable handle), plus a migration.
```jsonc
{
  "main": "src/index.ts",
  "containers": [
    { "class_name": "MyContainer", "image": "./Dockerfile",
      "instance_type": "standard-1", "max_instances": 10 }
  ],
  "durable_objects": {
    "bindings": [ { "class_name": "MyContainer", "name": "MY_CONTAINER" } ]
  },
  "migrations": [ { "new_sqlite_classes": ["MyContainer"], "tag": "v1" } ]
}
```
```typescript
import { Container, getContainer } from "@cloudflare/containers";
export class MyContainer extends Container {
  defaultPort = 8080;     // port your app listens on
  sleepAfter = "30m";     // idle window before stopping (class default: "10m")
}
export default {
  async fetch(request: Request, env: Env) {
    // session affinity: same id → same container instance
    const container = getContainer(env.MY_CONTAINER, "session-1");
    return container.fetch(request);   // forwards to defaultPort
  }
};
```
- `image`: path to a Dockerfile/dir, built for **`linux/amd64`** — or a pushed image from an external
  registry, including **Google Artifact Registry**. `instance_type`: named (see limits) or custom
  `{vcpu, memory_mib, disk_mb}`. Optional class props: `entrypoint`, `envVars`, lifecycle hooks.
- This is the **`default` scheduling policy** (omitting `scheduling_policy` selects it): one app-wide
  image/size, changed via rollouts. The policy is **immutable** — switching means a new application.

## Access patterns
- **All traffic flows Worker → Durable Object → container.** The Worker is the front door (best-latency
  datacenter); the DO is the globally-addressable handle; the container VM runs the image. DO and its
  container may run in **different locations** — placement is optimized for startup speed.
- **Routing helpers** (decide how requests map to instances):
  - `getContainer(env.MY_CONTAINER, id)` / `.getByName(id)` — **session affinity**, same id → same instance.
  - `.getRandom()` — **stateless load-balancing** (no autoscaling; you spread load manually).
  - `getByName("singleton")` — single global instance; `getByName(jobId)` — one container per job.
- Container methods: `fetch()` (HTTP/WebSocket), `exec()` (run a command inside the running container),
  `startAndWaitForPorts()`, `start()`, `stop()`, `destroy()`, `schedule()` (uses DO `alarm()`).
  Lifecycle hooks: `onStart` / `onStop` / `onError` / `onActivityExpired`.

## `durable_object` scheduling policy & snapshots — public beta, 2026-09-30
- `"scheduling_policy": "durable_object"` + named images (`containers[].images.base.dockerfile`):
  each DO picks image and size at runtime via `ctx.container.start()` with `image` from `ctx.container.images.base`
  and `instance: "standard-2"` (omit `instance` → `lite`), or `image: "cloudflare/debian-trixie"` (managed
  image, Node.js 24.20.0) with no named image. `start()` returns before the app is ready — add a readiness check.
- **Not** with the `Container` class — use the Durable Object Container API (`ctx.container`) directly.
  No `max_instances`, no app-wide rollouts (your code restarts instances onto a new image), no `basic`
  size; named `image` refs must be digest-pinned in the Cloudflare registry (no Docker Hub/ECR/GAR direct).
- **Snapshots** (this policy only): `await ctx.container.snapshotContainer({})` saves the writable root
  filesystem (no memory/processes); restore with `start({ containerSnapshot })` (mutually exclusive with
  `image`), even from another DO. Immutable, tied to the source image, ≤20 GB, 30-day TTL refreshed on
  restore. No list API — store the handle. Guides: `developers.cloudflare.com/containers/guides/snapshots/`,
  `developers.cloudflare.com/containers/examples/durable-object-interface/`.

## Deploying (machine & Workers Builds) — page added 2026-08-13
- `wrangler deploy` **activates the Worker first**, *then* handles the image and the rollout. The
  steps are **not transactional**: a build/push/rollout failure can land after the new Worker is
  serving, and mid-rollout new Worker code talks to **old-image containers** — design for the overlap.
- Docker is needed **only** when `image` is a Dockerfile path; a registry reference needs none.
- **Workers Builds**: production branch runs `wrangler deploy` (image + rollout); other branches
  default to `wrangler versions upload` — **Worker code only**, no new image, no container rollout.
- **Version URLs are never generated for Containers Workers** (they implement Durable Objects). Test with
  `wrangler dev`, a staging Worker / Wrangler environment, or **Workers Previews** (`npx wrangler preview`,
  2026-09-22): each Preview gets its own container app — declare it under `previews.containers` (not
  inherited from top-level `containers`). Never repoint a non-production build command at the production
  Worker to try an image — it rolls live containers.
- First deploy takes minutes to provision. Worker-only deploy (skip image + instances):
  `--containers-rollout=none`; cut over Worker and image together: `--containers-rollout=immediate`. Inspect with `wrangler containers list` / `images list`.

## Gotchas
- **WebSockets:** `fetch()` is the only method that proxies WebSockets; `containerFetch()` does **not**
  support them (to target another port and keep WebSockets, use `fetch(switchPort(request, port))`).
- **Ports not ready:** `start()` returns when the process starts, not when ports listen → "connection
  refused". Use `await startAndWaitForPorts()` before forwarding (or rely on `fetch()` which starts for you).
- **Disk is ephemeral** — reset to the image on every stop/restart. Persist state in **DO storage**,
  R2 (FUSE mount), external stores, or snapshots (`durable_object` policy only, see above).
- **`sleepAfter` (default `10m`) is reset by incoming requests, not by internal work** — long background
  jobs can be put to sleep. Call `this.renewActivityTimeout()` from that work to reset the timer.
- **Rolling deploys + SIGTERM:** updates roll out gradually; on shutdown you get SIGTERM, then SIGKILL
  after 15 min — handle graceful shutdown.
- **Lifecycle hooks are `async`-aware** — `onStart` / `onStop` / `onError` may return a promise and the
  runtime waits on it, so slow hook logic delays the state transition. `onStop` receives `{ exitCode,
  reason }`, where `reason` is `'exit'` (process ended on its own) or `'runtime_signal'`.

## Pricing & limits
> **GA since 2026-04-13** (changelog entry of that date: GA together with Sandboxes). Workers **Paid**
> plan only — no Free tier. Pricing is volatile — verify on the live page
> (`developers.cloudflare.com/containers/platform/pricing/`) before quoting.

**Billing model:** charged per **10ms actively running** (starts on first request / manual start, stops
when the instance sleeps → scale-to-zero). Cost drivers, on top of the $5/mo Workers Paid plan:
- **Memory:** 25 GiB-hours/mo included, then **$0.0000025 / GiB-s** (billed on *provisioned* memory).
- **CPU:** 375 vCPU-min/mo included, then **$0.000020 / vCPU-s** (billed on *active* usage).
- **Disk:** 200 GB-hours/mo included, then **$0.00000007 / GB-s** (provisioned).
- **Egress:** **$0.025/GB** NA+EU (1 TB incl.), $0.04–0.05 elsewhere (500 GB incl.).
- You're **also billed for the underlying Workers + Durable Objects** usage.

**Instance types:** `lite` (1/16 vCPU, 256 MiB, 2 GB) → `standard-4` (4 vCPU, 12 GiB, 20 GB).
Custom: 1–4 vCPU, ≤12 GiB mem, ≤20 GB disk, ≥3 GiB mem/vCPU — the disk-to-memory ratio cap was
**removed 2026-09-29** (any custom type may take 20 GB; image size limit = instance disk).
**Account limits:** 6 TiB concurrent memory · 1,500 concurrent vCPU · 30 TB concurrent disk ·
50 GB total image storage. Verify on `developers.cloudflare.com/containers/platform/limits/`.

## Going deeper
> **Docs reorganized 2026-08 — old paths are dead:** `pricing/`, `platform-details/limits/` → `platform/`;
> `container-class/` → `reference/`; `deploy/`, `ssh/`, `local-dev/`, `execute-commands/`, `image-management/`,
> `outbound-traffic/` → `guides/`; `architecture/`, `placement/` → `concepts/`; `rollouts/`,
> `scaling-and-routing/`, `workers-connections/`, `environment-variables/` → `configuration/`.

- Covered by the official `cloudflare` skill (`references/containers/`) — use it for the full
  `Container` class API, routing patterns, WebSocket forwarding, and Workflow/Queue integration.
- Lifecycle: `developers.cloudflare.com/containers/concepts/architecture/` · SSH via `wrangler`:
  `developers.cloudflare.com/containers/guides/ssh/` · low-level runtime:
  `developers.cloudflare.com/containers/api/durable-object-container/`.
