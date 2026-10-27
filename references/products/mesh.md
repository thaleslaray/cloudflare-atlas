# Cloudflare Mesh — private IP networking between devices and servers

> Every enrolled server, laptop and phone gets a private **Mesh IP**; any participant reaches any
> other by IP over TCP/UDP/ICMP, routed through Cloudflare. Post-quantum encrypted. **Beta.**
> Formerly **WARP Connector** / "peer-to-peer connectivity" — existing deployments keep working,
> no migration. The WARP client is now the **Cloudflare One Client**.

## Contents
- When to use (and when not)
- Participants & Mesh IPs
- Setup
- Routes (CIDR & hostname)
- High availability
- Containers
- Gotchas
- Pricing & limits
- Going deeper

## When to use
- Devices/servers need to reach **each other** by private IP, bidirectionally.
- Workloads that break on connection interruption: database replication, SAP/ERP, RDP, SSH,
  long-lived TCP. Mesh is L3/L4 and preserves connections end-to-end — the recommended software
  on-ramp for interruption-sensitive traffic.
- Reaching gear that cannot run the client (printers, IoT, appliances) via a subnet route.
- Replacing Tailscale / WireGuard / a traditional VPN, with Gateway policies and device posture
  enforced on every connection (all traffic transits Cloudflare).

**Mesh vs Tunnel** — the decision:

|  | Mesh | Tunnel |
|---|---|---|
| Direction | bidirectional, any participant initiates | inbound to origin only |
| Addressing | every participant gets a Mesh IP | server-side only, no IPs |
| Connector | `warp-cli` (Cloudflare One Client) | `cloudflared` |
| Protocols | TCP, UDP, ICMP (L3/L4) | HTTP/S, TCP, SSH, RDP, SMB (proxied over WebSocket) |
| Use for | private IP connectivity between participants | publishing specific apps/hostnames/IP routes |

**Not** for publishing a public hostname (→ `tunnel`), and not a Workers feature — a Worker reaches
Mesh only through Workers VPC bindings (→ `workers-vpc`).

## Participants & Mesh IPs
Two participant types:

|  | Mesh nodes | Client devices |
|---|---|---|
| Runs on | Linux servers, VMs, containers | laptops, phones, desktops |
| Client | Cloudflare One Client (`warp-cli`), headless | same client, with UI |
| Subnet routing | can advertise CIDR routes | no — reach subnets through a node |
| High availability | active-passive replicas | n/a |

- Mesh IPs come from `100.96.0.0/12` (CGNAT space, so no clash with `10.x`/`172.16.x`/`192.168.x`).
  Elsewhere in Cloudflare One docs these are called **device IPs**. Custom subnet configurable.
- **Client-to-client works with zero nodes** — two enrolled laptops reach each other directly.
  Nodes exist to run headless on a server or to route a subnet behind it.

## Setup
Prerequisites: a Zero Trust organization (Free plan included).

```sh
# 1. IP forwarding (only needed if the node will advertise CIDR routes)
printf 'net.ipv4.ip_forward = 1\nnet.ipv6.conf.all.forwarding = 1\nnet.ipv6.conf.all.accept_ra = 2\n' \
  | sudo tee /etc/sysctl.d/99-zzz-cloudflare-warp-connector.conf && sudo sysctl --system

# 2. Install cloudflare-warp (Debian/Ubuntu shown; RHEL/Fedora use the .repo + yum, plus epel-release)
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor \
  -o /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(. /etc/os-release && echo $VERSION_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/cloudflare-client.list
sudo apt-get update -qq && sudo apt-get install -y -qq cloudflare-warp

# 3. Enroll the node
sudo warp-cli --accept-tos connector new <TOKEN> && sudo warp-cli --accept-tos connect
```

Node host requirements: RHEL 9/10, Debian 12/13, Fedora 43/44, Ubuntu 22.04/24.04/26.04 LTS;
AMD64 or ARM64; **3 vCPU min (4 rec.)**; RAM 1 GB min / 2 GB rec. headless (4 / 8 GB with a desktop);
disk 250 MiB min / 500 MiB rec.; **MTU 1381 recommended** (1281 minimum with PMTUD).
RHEL 9+ needs `sudo dnf install epel-release` first.

API (note the legacy path — see Gotchas):
```
POST   /accounts/{account_id}/warp_connector                      # create node
GET    /accounts/{account_id}/warp_connector/{node_id}/token      # enrollment token
GET    /accounts/{account_id}/warp_connector/{node_id}/connections # replicas + ha_status
PUT    /accounts/{account_id}/warp_connector/{node_id}/failover   # manual promote (client_id)
```

## Routes (CIDR & hostname)
A node is reachable only by its own Mesh IP **until you add a route**.
- **CIDR routes** expose the subnet behind the node — for hosts that cannot run the client.
  Requires persistent IP forwarding on the node.
- **Hostname routes** replace Tunnel's *virtual networks*. A hostname is globally unique, so
  **overlapping hostnames are not supported** — one hostname routes to exactly one node or tunnel.
  Under 255 characters; several wildcard forms unsupported. Requires MASQUE.
- The node must be able to resolve the hostname. Unlike Tunnel, **no dedicated DNS server is
  required** — an `/etc/hosts` entry on the node is enough.

## High availability
Active-passive replicas, for **routed** nodes. One token registers many Linux hosts as replicas of
the same node; all advertise the same CIDR routes, one is active, Cloudflare promotes a standby on
disconnect. Manual promotion via the `failover` endpoint. HA has **limited benefit on a node with no
routes** — a bare Mesh IP is tied to the individual replica. Requires MASQUE.

## Containers
`cloudflare/mesh` on Docker Hub runs `warp-svc` headless on a minimal Wolfi base — Docker Compose,
Kubernetes, CI/CD. Docs examples use `cloudflare/mesh:latest`.

## Gotchas
- **MASQUE is mandatory for the good parts.** It is the default device-tunnel protocol, but if a
  node's device profile uses WireGuard, then hostname routes, IPv6 CIDR routes and HA all break.
- **The API still says `warp_connector`, and its path parameter is `{tunnel_id}`** — not `{node_id}`,
  which is what the docs call it. Product and docs renamed; the spec did not. The spec also carries
  four operations the docs never mention: `GET`/`PATCH`/`DELETE` on the node itself,
  `GET`/`PUT /configurations` (HA config) and `GET /connectors/{connector_id}` — see `api/mesh.md`.
- **Never install a node on a DNS server.** Nodes run in Traffic-and-DNS mode and bind port 53 —
  conflicts with AD DNS, Pi-hole, Unbound, BIND, dnsmasq. Put the node on a separate host in the
  same subnet and reach the DNS server by CIDR route.
- **Uninstall the other VPN first.** Tailscale, WireGuard, OpenVPN, AnyConnect, GlobalProtect,
  ZScaler, Netskope all fight for the routing table. Stop/disable, then **reboot** so the client's
  interface wins, then `warp-cli status`.
- **Mesh + Tunnel on one host needs Split Tunnels** — the only supported method. The node captures
  outbound traffic and would starve `cloudflared`; exclude the Tunnel-required hostnames/IPs. Manual
  `ip route add` / `iptables` do **not** work: the node's kernel integration overrides them.
- **Double encapsulation drops big packets.** Participant-to-participant traffic is encapsulated
  twice; packets ≥1,460 bytes can exceed 1,500 and be dropped. Set source-device MTU to **1,280**,
  or clamp MSS to **1,240** for TCP-only. PMTUD-aware apps usually handle it.
- **Updating a node interrupts its routed traffic** — it briefly disconnects. HA fails over.
- **Mesh ↔ Cloudflare WAN requires Unified Routing mode.** Without it the two cannot exchange
  traffic at all. (Unified Routing went GA 2026-09-18.)
- **Cloudflare-originated traffic** (Load Balancing health checks, Workers) arrives from
  `100.64.0.0/12` by default — may need source-IP configuration to avoid conflicts.
- **Logs tell nodes from people (2026-09-29).** Logpush `zero_trust_network_sessions`: `OnrampType`
  / `Offramp` = `MESH`, `DestinationReplicaID` = which node replica served it (Gateway network logs:
  *Traffic Source/Destination* columns). Before that, nodes logged as ordinary clients; no backfill.
- Older installs used `sysctl -w`, which does not survive reboot; a node that loses route
  connectivity after a restart is usually this.

## Pricing & limits
**Beta**, available to Cloudflare One accounts **including the Free plan**. No separate Mesh price
published — it rides the Cloudflare One/Zero Trust subscription. Verify on the live pricing page
before quoting: `developers.cloudflare.com/cloudflare-one/` plans. Mesh IP pool `100.96.0.0/12`;
hostname routes under 255 chars, no overlaps.

## Going deeper
- Docs: `developers.cloudflare.com/mesh/` (canonical; mirrored under
  `cloudflare-one/networks/connectors/cloudflare-mesh/` — same content).
- Endpoints: `api/mesh.md` (11 operations, sliced from the spec).
- Sibling atlas files: `tunnel.md` (the contrast that decides which to use), `workers-vpc.md`
  (reach Mesh from a Worker via the `cf1:network` binding).
