#!/usr/bin/env python3
"""pagediff — detect NEW doc subtrees inside already-known Cloudflare products.

Why this exists: `update-check` only diffs top-level product slugs from the master
llms.txt. Big launches ship as a subtree *inside* an existing product — Project Think
landed as 14 pages under `agents/harnesses/think/` while the slug `agents` never
changed. That launch stayed invisible to the skill for three months.

This walks every product's own llms.txt, folds the page list into directory prefixes
with page counts, and diffs those against a baseline.

Noise control (the whole point):
  - Report only the SHALLOWEST new prefix of a subtree. A new product area shows up
    once as `agents/harnesses/think (+14)`, not 14 times for every child directory.
  - Prefixes at/below MIN_PAGES are folded into a single "routine docs" tally, so a
    lone new tutorial page never competes with a real launch for attention.

Usage:
  pagediff.py --baseline <file> [--init] [--jobs N] [--min-pages N]
    --init   write the baseline instead of diffing (first run / after curating)
"""
import argparse
import concurrent.futures as cf
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request

MASTER = "https://developers.cloudflare.com/llms.txt"
UA = {"User-Agent": "Mozilla/5.0 (cloudflare-atlas update-check)"}
PAGE_RE = re.compile(r"https://developers\.cloudflare\.com/([^\s)\]]+?)/index\.md")
PROD_RE = re.compile(r"https://developers\.cloudflare\.com/([^/)\s]+)/llms\.txt")
NESTED_RE = re.compile(r"https://developers\.cloudflare\.com/([^)\s]+?)/llms\.txt")


class ShortRead(OSError):
    """A 200 that delivered fewer bytes than it promised."""


def fetch(url, timeout=30, attempts=3):
    """Fetch a URL, refusing to return a body the server said would be longer.

    The failure this guards against is NOT a raised exception — it is a 200 whose
    connection dropped mid-body. `read()` returns the short prefix, no error, and the
    caller cannot tell it from a genuinely small page. On 2026-08-31 that recorded
    `workers-ai` as 3 pages instead of 61, and the next weekly run reported the missing
    58 back as a launch. Compare against Content-Length and retry instead.
    """
    last = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                declared = r.headers.get("Content-Length")
                if declared is not None and len(raw) < int(declared):
                    raise ShortRead(f"{url}: got {len(raw)} of {declared} bytes")
            return raw.decode("utf-8", "replace")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            last = e
            if attempt + 1 < attempts:
                time.sleep(1.5 * (attempt + 1))
    raise last


def product_slugs():
    return sorted(set(PROD_RE.findall(fetch(MASTER))))


def looks_like_llms_txt(body, slug):
    """Reject a 200 that is not actually this product's page index.

    A short read is not the only way to get a plausible-but-wrong body. A soft 404, an
    edge error page, a redirect landing — all arrive complete, with status 200, and parse
    to zero pages, which is indistinguishable from a product that simply has none. Every
    real product llms.txt is a markdown index that links at least its own pages, so
    "contains no page link at all" is the signature to refuse.
    """
    if not body or len(body) < 40:
        return False
    if not PAGE_RE.search(body):
        return False
    lowered = body[:400].lower()
    return not any(m in lowered for m in ("<!doctype", "<html", "404 not found", "page not found"))


def pages_for(slug, expect=0):
    """Return the set of page paths a product's llms.txt lists.

    Two failure modes, neither of which raises:

    - **Short read.** The docs site answers chunked, so a stream that dies mid-body has no
      Content-Length to fail against — `read()` just returns less, HTTP 200. On 2026-08-31
      that turned `workers-ai` from 61 pages into 3.
    - **Complete but wrong.** A soft 404 or error page arrives whole, parses to zero pages,
      and reads as "this product has no docs". `looks_like_llms_txt` refuses those.

    `expect` is the count the baseline already knows for this slug. A read delivering less
    than half of it is treated as failed and retried, so the floor scales with the product
    instead of sitting at a flat 2 — which is what let the 3-page truncation through. The
    largest result across attempts wins; a product that genuinely shrank still reports its
    real (smaller) count once the retries agree, and the --init guard decides what to do
    about that.
    """
    url = f"https://developers.cloudflare.com/{slug}/llms.txt"
    floor = max(2, int(expect * 0.5))
    best = None
    for _ in range(3):
        try:
            body = fetch(url)
        except Exception:
            continue
        if not looks_like_llms_txt(body, slug):
            continue
        pages = set(PAGE_RE.findall(body))
        # Nested indices. On 2026-09-14 `cloudflare-one/llms.txt` stopped listing its pages and
        # started linking eleven sub-indices (`cloudflare-one/networks/llms.txt`, …) instead. Read
        # flat, the product fell from 731 pages to 107, the check reported 28 subtrees "gone", and
        # the --init collapse guard never fired because the shrink happened in the index format,
        # not in a fetch. Follow every sub-index under this product; if any one fails, the whole
        # read is unusable — a partial union is exactly the silent shrink this function exists to refuse.
        nested = sorted({n for n in NESTED_RE.findall(body) if n.startswith(slug + "/")})
        try:
            for n in nested:
                sub = fetch(f"https://developers.cloudflare.com/{n}/llms.txt")
                if not looks_like_llms_txt(sub, n):
                    raise ShortRead(f"{n}/llms.txt is not a page index")
                pages |= set(PAGE_RE.findall(sub))
        except Exception:
            continue
        if best is None or len(pages) > len(best):
            best = pages
        if len(best) >= floor:
            return slug, best
    return slug, best  # None only if every attempt failed or was refused


def prefixes(pages):
    """Fold page paths into {directory prefix: page count}.

    `agents/harnesses/think/actions` contributes to `agents`, `agents/harnesses`
    and `agents/harnesses/think` — so a new subtree is detectable at every depth
    and we can later keep only the shallowest.
    """
    counts = {}
    for path in pages:
        parts = path.split("/")
        for i in range(1, len(parts) + 1):
            counts[("/".join(parts[:i]))] = counts.get("/".join(parts[:i]), 0) + 1
    return counts


def shallowest(new_prefixes):
    """Drop any prefix whose ancestor is also new — keeps one line per launch."""
    keep = []
    for p in sorted(new_prefixes):
        if not any(p.startswith(a + "/") for a in keep):
            keep.append(p)
    return keep


def load_baseline(path):
    base = {}
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                prefix, _, count = line.rpartition("\t")
                if prefix:
                    base[prefix] = int(count)
    except FileNotFoundError:
        return None
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--force", action="store_true",
                    help="record the baseline even if page counts collapsed (real docs shrink)")
    ap.add_argument("--min-pages", type=int, default=2,
                    help="subtrees with fewer pages are tallied as routine docs, not flagged")
    args = ap.parse_args()

    try:
        slugs = product_slugs()
    except Exception as e:
        print(f"⚠️  could not fetch the master product list: {e}")
        return 1

    # Load the baseline BEFORE walking: each product's known page count is what tells the
    # walker how small a result is too small to believe for THAT product.
    base = load_baseline(args.baseline)
    expected = base or {}

    all_pages, failed = set(), []
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for slug, pages in ex.map(lambda sl: pages_for(sl, expected.get(sl, 0)), slugs):
            if pages is None:
                failed.append(slug)
            else:
                all_pages |= pages
    # Union the pages first, THEN fold into prefixes. This used to be `live.update(prefixes(pages))`
    # per product, and indices link each other's pages: when `ai-gateway`'s index cited one
    # `cloudflare-one` page, its {"cloudflare-one": 1} overwrote the 540 counted from cloudflare-one's
    # own index. Every baseline since at least 2026-08-26 recorded `cloudflare-one` as 1 page, so the
    # --init collapse guard (`was >= 3`) could never protect it — which is why the 2026-09-14 shrink
    # to 107 prefixes went into the baseline unchallenged.
    live = prefixes(all_pages)

    if failed:
        # Never let a fetch failure masquerade as "this subtree disappeared".
        print(f"⚠️  {len(failed)} product(s) unreachable, skipped from the diff: {', '.join(sorted(failed)[:8])}"
              + (" …" if len(failed) > 8 else ""))

    if args.init:
        # A baseline is only as good as the run that recorded it. Two guards, both added
        # 2026-09-04 after the 08-31 baseline froze a truncated fetch and the weekly check
        # reported the missing pages back as a Workers AI launch.
        if failed:
            print(f"❌ refusing to record a baseline with {len(failed)} unreachable product(s): "
                  f"{', '.join(sorted(failed))}")
            print("   A baseline written now would bake the gap in and the next run would")
            print("   report those pages as new. Re-run when the docs site answers.")
            return 1
        prior = base
        if prior and not args.force:
            collapsed = []
            for slug in {p.split("/")[0] for p in prior}:
                was, now = prior.get(slug, 0), live.get(slug, 0)
                # Was >=10, which let an 8 → 1 truncation through untouched. Three pages is the
                # smallest count where 'halved' still means something; below that the signal and
                # the noise are the same size.
                if was >= 3 and now < was * 0.5:
                    collapsed.append((slug, was, now))
            if collapsed:
                print("❌ refusing to record a baseline: page counts collapsed vs the current one.")
                for slug, was, now in sorted(collapsed):
                    print(f"   {slug}: {was} → {now} pages")
                print("   This is what a truncated fetch looks like. Investigate, then pass")
                print("   --force if the shrink is a real docs change.")
                return 1
        # Keep the outgoing baseline. Re-recording is the last step of a refresh, and it is what
        # destroys the only record of what that pass saw — a pass whose single-page additions were
        # never named cannot be reconstructed afterwards. Cost: one file.
        if os.path.exists(args.baseline):
            shutil.copy2(args.baseline, args.baseline.replace(".txt", ".prev.txt"))
        with open(args.baseline, "w") as fh:
            fh.write("# cloudflare-atlas page-prefix baseline — regenerate with: update-check --init-baseline\n")
            fh.write("# format: <doc path prefix>\\t<page count>\n")
            for prefix in sorted(live):
                fh.write(f"{prefix}\t{live[prefix]}\n")
        print(f"✅ baseline written: {len(live)} prefixes across {len(slugs) - len(failed)} products")
        return 0

    if base is None:
        print(f"⚠️  no baseline at {args.baseline} — run with --init-baseline first (nothing to diff yet)")
        return 0

    new = shallowest([p for p in live if p not in base])
    # Only treat a prefix as gone if its whole product answered; otherwise it's a fetch gap.
    reachable = {s for s in slugs if s not in failed}
    gone = shallowest([p for p in base if p not in live and p.split("/")[0] in reachable])

    big = [(p, live[p]) for p in new if live[p] >= args.min_pages]
    small = [p for p in new if live[p] < args.min_pages]

    if big:
        print("🚨 NEW doc subtrees (likely a launch inside a known product):")
        for prefix, n in sorted(big, key=lambda x: -x[1]):
            print(f"   + {prefix}  (+{n} pages)")
    if gone:
        print("\n🗑️  Subtrees that disappeared (renamed, merged, or retired):")
        for prefix in gone[:15]:
            print(f"   - {prefix}")
        if len(gone) > 15:
            print(f"   … and {len(gone) - 15} more")
    if small:
        # Name them. Tallying them as a number was a silent cap: a limit change, a new pricing page
        # or a single new endpoint page all arrive as exactly one page and looked like "routine".
        print(f"\n📄 Routine new pages ({len(small)} single-page addition(s) — low signal, but listed):")
        for prefix in sorted(small):
            print(f"   · {prefix}")
    if not (big or gone):
        print("✅ no new doc subtrees — nothing launched inside a known product.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
