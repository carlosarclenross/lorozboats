#!/usr/bin/env python3
"""Loroz site debug harness. Loads every page in headless Chromium and reports:
- console errors / pageerrors
- failed resource requests
- horizontal overflow (mobile + desktop)
- unloaded / 0-size images
- broken internal links (crawl all hrefs, /pages + /assets)
- duplicate DOM ids
- missing alt attributes
Usage: python debug_site.py [base_url]
"""
import sys, re
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8060"
PAGES = ["/", "/boats.html", "/repair.html", "/financing.html", "/contact.html"]
VIEWPORTS = {"desktop": (1440, 900), "mobile": (390, 844)}

def _benign_abort(request):
    """ERR_ABORTED on media is the browser cancelling a metadata range request."""
    if request.failure == "net::ERR_ABORTED" and re.search(r"\.(mp4|webm|mp3|ogg|mov)$", request.url, re.I):
        return True
    return False

def main():
    problems = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, (w, h) in VIEWPORTS.items():
            print(f"\n===== {name.upper()} ({w}x{h}) =====")
            ctx = browser.new_context(viewport={"width": w, "height": h})
            page = ctx.new_page()
            errors, failed, overflow, imgs = [], [], [], []
            page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
            page.on("requestfailed", lambda r: failed.append(f"{r.method} {r.url} -> {r.failure}") if not _benign_abort(r) else None)

            for path in PAGES:
                url = urljoin(BASE, path)
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(400)
                over = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if over > 2:
                    overflow.append(f"{path}: horizontal overflow +{over}px")
                bad_imgs = page.evaluate("""() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src)""")
                for s in bad_imgs:
                    imgs.append(f"{path}: image failed to load {s}")
                # missing alts
                no_alt = page.evaluate("""() => [...document.images].filter(i => !(i.alt || i.getAttribute('aria-label'))).length""")
                if no_alt:
                    imgs.append(f"{path}: {no_alt} image(s) missing alt text")

            ctx.close()

            seen = set()
            for e in errors:
                if e not in seen:
                    seen.add(e); print("  [ERR] " + e); problems += 1
            for f in failed:
                print("  [NET] " + f); problems += 1
            for o in overflow:
                print("  [OVERFLOW] " + o); problems += 1
            for i in imgs:
                print("  [IMG] " + i); problems += 1
            if not (errors or failed or overflow or imgs):
                print("  clean: no console errors, no failed requests, no overflow, no image issues")

        # ---- link crawl (desktop only) ----
        print("\n===== LINK CRAWL =====")
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        all_links = {}
        for path in PAGES:
            page.goto(urljoin(BASE, path), wait_until="networkidle", timeout=30000)
            links = page.eval_on_selector_all("a[href]", """els => els.map(a => a.href)""")
            for l in links:
                u = urlparse(l)
                if u.scheme in ("http", "https") and u.netloc == urlparse(BASE).netloc:
                    all_links.setdefault(u.path or "/", 0)
        for path in sorted(all_links):
            page.goto(urljoin(BASE, path), wait_until="networkidle", timeout=30000)
            code = page.evaluate("document.title") and page.status() if False else None
            # check via fetch status
            status = page.evaluate("""async u => (await fetch(u, {method:'HEAD'})).status""", urljoin(BASE, path))
            if status != 200:
                print(f"  [LINK] {path} -> HTTP {status}"); problems += 1
        # external links present?
        ext = set()
        for path in PAGES:
            page.goto(urljoin(BASE, path), wait_until="networkidle", timeout=30000)
            for l in page.eval_on_selector_all("a[href]", """els => els.map(a => a.href)"""):
                u = urlparse(l)
                if u.scheme in ("http", "https") and u.netloc != urlparse(BASE).netloc:
                    ext.add(u.netloc)
        print("  external links:", ", ".join(sorted(ext)) or "none")
        ctx.close()

        # ---- duplicate ids ----
        print("\n===== DOM IDS =====")
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        for path in PAGES:
            page.goto(urljoin(BASE, path), wait_until="networkidle", timeout=30000)
            dups = page.evaluate("""() => { const m = {}; [...document.querySelectorAll('[id]')].forEach(el => m[el.id] = (m[el.id]||0)+1); return Object.entries(m).filter(([k,v]) => v > 1); }""")
            for k, v in dups:
                print(f"  [DUPID] {path}: id='{k}' appears {v}x"); problems += 1
        ctx.close()
        browser.close()

    print(f"\n===== RESULT: {problems} problem(s) =====")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
