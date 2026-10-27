# Sandboxes — run untrusted or generated code in Linux or an isolate

> Run agent-written, user-uploaded or model-generated code where it cannot touch your app. Two
> environments, both driven from a Worker: a Linux **Container** your own Durable Object starts, or a
> **Dynamic Worker** isolate. Sandbox SDK 1.0 shipped 2026-09-30 (changelog: "control every sandbox
> from your own Durable Object"); Containers and Sandboxes went GA together on 2026-04-13.

## Contents
- What 1.0 is · When to use · Binding & config · Key API · Lifetime, persistence & previews
- Security model · Coding agents · Legacy 0.x & migration · Gotchas · Pricing & limits · Going deeper

## What 1.0 is
In 0.x the package's `Sandbox` class *was* your Durable Object and ran an SDK server in the
container. In 1.0 you write the Durable Object class and drive the container directly through
`this.ctx.container` (the Durable Object container API, documented under Containers). Start, exec,
ports, outbound interception and snapshots live there; `@cloudflare/sandbox` keeps only helpers:
- `Files` — read/write/stat/list/`mkdir`/`rename`/`remove` in the running container.
- `S3Mount` — mounts an S3-compatible bucket (R2 via its S3 endpoint) with `s3fs`; `S3Gateway` in
  your Worker signs each request so credentials never enter the container. No R2 binding accepted.
- `DirectoryBackup` — one directory to R2 via `DirectoryBackupGateway`; restores onto newer images.

"The package does not start, stop, or monitor the container", retries nothing and sets no time
limits — lifetime, retries and timeouts are your code. The container uses the `durable_object`
scheduling policy (public beta). Median `start()` to first command: under 600 ms on a prepared
image, vs about 4 s on 0.x.

## When to use
- **Container** — the code expects Linux: `npm test`, a preview server holding a port, native
  binaries, toolchains, any language. Firecracker microVM with its own kernel and network.
- **Dynamic Worker** — the code only calls methods you hand it (JS, Python or Wasm; compile TS
  first). No child processes or native add-ons. API and limits: `products/dynamic-workers.md`.
- One Worker can use both (scoped methods in an isolate, then a Container for the test run). Agent
  needing a shell from its own Durable Object → Agents SDK sandbox tool (`agents/tools/sandbox/`).
- **Not** for your own trusted service (plain `containers`) or first-party logic (`workers`).

## Binding & config (`wrangler.jsonc`)
```jsonc
{
  "compatibility_flags": ["nodejs_compat"],          // needed by @cloudflare/sandbox
  "containers": [{ "class_name": "MyContainer", "scheduling_policy": "durable_object",
                   "images": { "workspace": { "dockerfile": "./Dockerfile" } } }],
  "durable_objects": { "bindings": [{ "class_name": "MyContainer", "name": "MY_CONTAINER" }] },
  "exports": { "MyContainer": { "type": "durable-object", "storage": "sqlite" } }
}
```
- No package needed for a stock image: `cloudflare/debian-trixie` (Node.js 24) — local runs need
  Wrangler `4.141.0` or later and Docker running for `wrangler dev`.
- `Files` / `S3Mount` / `DirectoryBackup` need the `sandbox-shim` helper in your image, from the
  `cloudflare/sandbox` tag matching the installed package (static `linux/amd64`; base e.g. `node:24-trixie-slim`):
  `COPY --from=docker.io/cloudflare/sandbox:1.0.0 /usr/local/bin/sandbox-shim /usr/local/bin/sandbox-shim`
- Instance size is chosen per `start()` with the runtime `instance` property (not `instance_type`).

## Key API / access patterns
```ts
import { DurableObject } from "cloudflare:workers";
export class MyContainer extends DurableObject<Env> {
  async exec(argv: string[]) {
    const c = this.ctx.container!;
    if (!c.running) c.start({ image: "cloudflare/debian-trixie",
                              entrypoint: ["sleep", "infinity"], enableInternet: false });
    const out = await (await c.exec(argv)).output();       // bytes: decode stdout yourself
    return { stdout: new TextDecoder().decode(out.stdout), exitCode: out.exitCode };
  }
}
// Worker: env.MY_CONTAINER.getByName("sandbox").exec(["uname", "-a"])
```
- `exec()` takes argv and runs no shell — start one: `["sh", "-c", "npm ci && npm test"]`. Pass
  `cwd` / `env` on every call (no session). No built-in timeout: wrap in GNU coreutils `timeout`.
- Previews: no public port; your Worker forwards via `getTcpPort(port)`. Listen on `0.0.0.0`.
- Outbound: `enableInternet: false` is the default; `interceptOutboundHttps` routes a hostname to
  Worker code that adds the credential. Snapshots: `snapshotContainer()` (public beta).
- Terminal: `exec` with a `pty` option on a `tmux` session over a WebSocket, xterm.js in the page
  (`sandbox/commands/open-a-terminal-in-the-browser/`).

## Lifetime, persistence & previews
A name → a Durable Object (`getByName()`, permanent) → an instance (temporary).
- An instance runs while its DO is active (request, alarm, streamed response, accepted WebSocket),
  then for `setInactivityTimeout()` — up to 6 hours. Code running inside the instance is NOT
  activity: a build is killed mid-run unless an alarm keeps the DO active.
- The timeout does not survive a DO restart (every deploy restarts DOs) — set it again in the
  constructor when `container.running`.
- Stops: timeout ends (processes get `SIGTERM`), `destroy()` (immediate, no cleanup), or the main
  process exits (kills every `exec()` — hence `sleep infinity` as entrypoint).
- Deploys keep running instances on their old image; `start()` throws while running, so a new image
  means `destroy()` then `start()`. Container rollouts never replace a sandbox.
- Disk, processes and terminals die with the instance. Keep files via snapshot (writable root only —
  not mounts, `/run` or processes; expires 30 days after creation or last restore), `DirectoryBackup`
  (survives image changes and 30 days), or an R2 mount (shared; re-mount on each instance).
- Cloudflare neither wakes the DO when its instance stops nor lists a user's sandboxes — keep your
  own records (`sandbox/manage/`).
- Own-hostname previews: proxied wildcard record + route `*.example-previews.com/*`; Universal SSL
  covers first-level subdomains only (deeper needs Total TLS or an advanced certificate).

## Security model
- The sandbox is the unit of trust: every process has `root`-level capabilities, so a separate Linux
  user protects nothing. One sandbox per user or per job; derive the name from the authenticated caller.
- Anything placed inside (env, args, files, a token in a clone URL saved to `.git/config`, a snapshot)
  is readable by all code there. Keep credentials in an outbound handler, added on HTTPS only.
- If Internet access is on, handlers see only ports 80/443 — other ports go out directly. Keep it off.
- Serve previews on a separate hostname so preview code cannot use your app's cookies/APIs.

## Coding agents (`sandbox/coding-agents/`)
Runner first: `sandbox/get-started/build-a-coding-agent-runner/` — **Claude Code** on a GitHub repo,
returns a diff; model calls go through AI Gateway, the Worker adding `AI_GATEWAY_TOKEN`.
- Agent in your sandbox: **Claude Code**, Codex, OpenCode, Pi (templates under
  `cloudflare/sandbox-sdk/tree/main/examples/coding-agents/`).
- Vendor runs the loop: `Devin Outpost` (template `cloudflare/sandbox-sdk/templates/devin`; cron trigger once a minute,
  `DEVIN_RECONCILE_INTERVAL_MS`, snapshot on suspend), Cursor Cloud Agents, Claude Managed Agents
  (`github.com/cloudflare/claude-managed-agents`; **Workers Paid** plan or an Enterprise account;
  Containers or Dynamic Workers), OpenAI Agents API (`sandbox/coding-agents/openai-agents-api/`;
  idle container kept `EXECUTOR_KEEP_ALIVE_SECONDS`). Devin, Cursor and OpenAI templates put a
  vendor credential inside the sandbox.
- Python `openai-agents[cloudflare]` (`CloudflareSandboxClient`) is a 0.x tutorial
  (`sandbox/sdk/tutorials/openai-agents/`) on the 0.x bridge; 1.0 has no bridge — keep that Worker on 0.x.

## Legacy: Sandbox SDK 0.x and migration
0.x (`getSandbox`, `runCode`, `exposePort`, `proxyToSandbox`, …) lives under `sandbox/sdk/` for
existing apps: bug and security fixes until 2026-12-31, no new features; deployed apps keep running
after. Coding-agent skill for 0.x docs: `sandbox-stable`.
- Until you move, pin `0.12.10` (package and `docker.io/cloudflare/sandbox:0.12.10`); avoid the
  2026-06-09 deprecations: HTTP/WebSocket transports, `exposePort()`, default sessions, streaming methods.
- The deploy moving a class to `scheduling_policy: "durable_object"` cannot be undone, even by
  `wrangler rollback`. In place: one deploy, 0.12 commands end, container files are lost
  (`createBackup()` first). Side by side: both classes in one Worker, move sandboxes one at a time.
- Gradual deployments cannot mix them — use `wrangler versions upload`, then deploy that version at 100%.
- After the switch: pending 0.12 alarms call your `alarm()` once; `schedule()` callbacks never run;
  open WebSockets go silent without a close frame. Old app bills until `wrangler containers delete`.
- Grep inventory + per-API map: `sandbox/sdk/migrate/`, `sandbox/sdk/migrate/api-map/`. 0.x only: each
  HTTP-transport call is a subrequest (Free 50 / Paid 1,000); `SANDBOX_TRANSPORT` `rpc` multiplexes them.

## Gotchas
- `cloudflare/debian-trixie` lacks Python, Git, `curl`, `jq` (the 0.x image had them) — your image
  provides every tool. `python3 -m http.server` exits on startup after deploy (hostname lookup).
- `monitor()` keeps the DO in memory, and misses the stop after the DO leaves memory. After a snapshot
  restore PIDs are reused — a saved PID may name another process.
- The package writes nothing to DO storage: preview tokens, process records, snapshot IDs — you store them.
- `DirectoryBackup` with `interceptAllOutboundHttp()`: call `intercept()` first, or backup/restore
  fail with `BACKUP_TRANSFER`.

## Pricing & limits
> No standalone price — billed as Containers + Workers + Durable Objects (+ Workers Logs if on).
> Verify on the live pricing pages before quoting (`developers.cloudflare.com/containers/platform/pricing/`).
- Plan: **Workers Paid**. Drivers: container vCPU, memory, disk, egress; Worker requests; DO usage.
- Instance types: lite (1/16 vCPU, 256 MiB, 2 GB disk) up to standard-4 (4 vCPU, 12 GiB, 20 GB);
  custom sizes 1–4 vCPU, min 3 GiB memory per vCPU (`start()` fields `vcpu`/`memoryMib`/`diskMb`).
- Snapshots: max 20 GB, retained 30 days from creation or most recent restore.

## Going deeper
- Live docs: `developers.cloudflare.com/sandbox/` · `developers.cloudflare.com/containers/api/durable-object-container/`.
- Atlas: `products/containers.md` (DO container API, limits), `products/dynamic-workers.md`, `products/agents.md`.
