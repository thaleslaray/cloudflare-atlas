# Version Management — safe zone config changes (versioning, staging, rollback)

> Test, deploy, and roll back **zone configuration** changes safely on Cloudflare's network using
> immutable **versions** promoted through **environments** (Development → Staging → Production).
> **Enterprise-only**. Versions themselves are **dashboard-only**; environments have a public API.
> Also called *Zone Versioning*.

## Contents
- When to use (and when not)
- Core concepts (versions, environments, traffic filters)
- The workflow (test → promote → roll back)
- Requirements & enablement
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- You want to **stage/version/roll back** zone-level config (WAF custom rules, Cache, Rules, etc.)
  with **no risk to live traffic** — make changes in an isolated version, validate, then promote.
- You need a **fast rollback** when a deployed config change causes problems.
- You want to **diff** two versions (e.g. staging vs production) before promoting.
- **Not** for: Worker code/deploys (→ Workers gradual deployments/versions), DNS, Load Balancing,
  Spectrum, Zero Trust/Access, or SSL certs — these are **excluded** from versioning (see below).
- **Not** if you use **Terraform** to manage the zone — Version Management and Terraform are
  mutually exclusive; pick one.

## Core concepts
- **Version** — an immutable snapshot of a zone's *versionable* configurations. You don't edit a
  version in place once promoted to a read-only env; you **Clone** an existing version (copies all
  its config), edit the clone, then promote it. Versions are never deleted (audit/rollback trail).
- **Version Zero** — auto-created on enablement; equals your current live zone config. Permanently
  editable, auto-deployed to all default environments so enabling causes **no disruption**. If you
  disable versioning, the zone reverts to Version Zero.
- **Global Configuration** — holds everything *not* versionable. ⚠️ Changes here apply
  **immediately to live traffic and all versions** — there is no staging for these.
- **Environment** — a ranked place to run a version (default: **Development** → **Staging** →
  **Production**). Each has a **traffic filter** controlling which requests it serves. You can create
  extra environments and set their rank ("Initial position").
- **Traffic filter** — pattern (Edge Server IP, Cookie, Hostname, User Agent, `cf.zone.name`) that
  routes matching requests to an environment so you can test it with real traffic. Production's
  filter is just `cf.zone.name == <zone>` and is not editable.
- **Read-only environment** — a version promoted into a read-only env becomes **permanently
  read-only**. **Production is read-only by default** (prevents accidental edits to live config).
  Many orgs also make **Staging** read-only so a validated version can't be changed before promotion.
  Version Zero is always editable, exempt from this.

## The workflow
1. **Clone** an existing version → edit configs in the new version (changes auto-save).
2. **Apply** it to the lowest-ranked environment (Development) and send matching traffic via its
   traffic filter; check the version's **Metrics** to confirm requests land and behave as expected.
3. **Promote** up one rank at a time (Dev → Staging → Production). Promote is only offered when the
   lower env differs from the higher one. **Compare versions** (Comparisons tab) to diff side-by-side
   before promoting.
4. **Roll back** — reverts an environment to the version previously assigned to it (fast recovery).
5. To "delete" a bad version: clone a good one, fix it, and stop using the old one (versions are
   immutable and can't be deleted).

## Requirements & enablement
Enable in dash: **Account → zone → Version Management → Enable versioning**. All must hold:
- Zone on **Enterprise** plan and in an **active** state.
- Zone uses **WAF managed rules** and has migrated from Firewall Rules → **custom rules**; account on
  the **new WAF**.
- User has **Super Administrator** or **Administrator** role (a "Zone Versioning" role can use but
  **cannot create** versions), an API Key provisioned, and API Access enabled.
- Versions managed **only through the dashboard**.

## Gotchas
- **API covers environments only.** Environments — including routing expressions and version
  assignments — are managed through the public Environments API
  (`/zones/{zone_id}/environments`). **Creating, cloning and editing versions** (the config
  snapshots) is **dashboard-only**.
- **No Terraform, no Wrangler safety.** Terraform is unsupported (use one or the other). With
  Wrangler: a version's Worker route can disappear on `wrangler deploy`; two versions sharing custom
  domains make the Worker pick randomly.
- **Global Configuration is live.** Editing anything non-versionable hits production instantly across
  all versions — there's no staging for those settings.
- **Excluded from versioning:** DNS, Spectrum, Load Balancing / Waiting Rooms / Health Checks,
  Zero Trust & Access, SSL certificates. Also **not cloned** into new versions: some API Shield
  config, Image Transformations, Network Error Logging, WAF Attack Score. **Unsupported:** Snippets,
  Compression Rules, Workers Cache API, Authenticated Origin Pull (returns 520), Client-side
  security / Page Shield.
- **Cache:** purging Production purges **all** environments; Cache Reserve is production-only.
  Cache Rules' `additional_cacheable_ports` + Image Resizing under versioning re-resizes every
  request (low performance).
- **Security Insights** are not shown once versioning is on and the first version hits production;
  dashboard **analytics** stay zone-level and may not break down per version/environment.
- **China:** traffic in China always targets the root zone regardless of the deployed version.
- **Waiting Room:** enabling/promoting can re-queue active users or lose their place; traffic may
  exceed limits.
- **Domain-scoped Roles** apply only to the root zone and don't carry into new versions.
- **Disabling** reverts the zone to Version Zero — first use Compare to make Version Zero match
  current Production, promote it, verify, then delete environments + HTTP applications via API.

## Pricing & limits
> ⚠️ **Enterprise-only feature** — no public/self-serve pricing. Cost is part of your Enterprise
> contract; confirm inclusion with your account team. Verify on the live docs/pricing before quoting.

**Availability:** Free / Pro / Business = **No**; Enterprise = **Yes** (requires enabling per zone).
**Key limits:** versions are immutable (never deleted); Production environment cannot be deleted and
is read-only by default; version create/clone/edit has no API (dashboard only); no Terraform support.

## Going deeper
- No official `cloudflare` skill reference exists for this product — this file is the primary source.
- Official docs: `developers.cloudflare.com/version-management/` (About, How-to: enable / environments
  / versions / compare; Reference: available-configurations, read-only-environments, traffic-filters).
- For staging Worker **code** changes instead, see Workers versions & gradual deployments.
- Full excluded-config list: `reference/available-configurations/` (check the dashboard for the
  current list — it changes).
