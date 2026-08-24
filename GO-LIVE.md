# GO LIVE: Replacing the Wix site

Goal: lorozboats.com serves the new site, Wix gets cancelled. Dad keeps the domain.
Do these IN ORDER. Do not cancel Wix until step 3 is verified.

---

## Step 1. Deploy the new site (30 min, done together)

Pick a host. Recommended: **Netlify** (free, forms built in, drag-and-drop).

Option A (easiest, no account needed to start):
1. Go to https://app.netlify.com/drop
2. Sign in (or create free account)
3. Drag the ENTIRE `E:\lorozboats` folder onto the page
4. Netlify gives you a URL like `https://random-name.netlify.app` and it's live

Option B (better long term): put the folder in a GitHub repo, connect to Netlify,
every push auto-deploys. I can set this up.

## Step 2. Point the domain at the new site (15 min, dad does this)

The domain is registered at Wix (that's why DNS shows wixdns.net). You do NOT need
to move the domain. Just change where it points.

1. Log in to his Wix account (the one from this session)
2. Go to the Domains section: wix.com -> account -> Domains -> lorozboats.com
3. Find "Advanced" or "DNS records" (may be under Manage DNS / Advanced Settings)
4. Delete the current A record (the one pointing at Wix IPs)
5. Add these records (Netlify values, replace <your-site> with the Netlify site name):
   - Type A, Host @, Value 75.2.60.5
   - Type CNAME, Host www, Value <your-site>.netlify.app
6. Save. Wait up to 24-48h for it to spread (usually 1-2h)

The new _redirects file already maps old Wix URLs (blank-1, blank-9, etc.) to the
new pages, so old links and Google results keep working.

## Step 3. Verify, then cancel Wix (do NOT skip the wait)

1. After DNS updates, visit https://www.lorozboats.com from his phone AND a computer
   on different networks. You should see the NEW site.
2. Test every page, the phone link, the video on the boats page.
3. Only then: Wix account -> Subscriptions -> cancel the site plan.
   - KEEP the domain registration. Cancelling the site plan is fine, the domain
     stays registered at Wix. If Wix offers to release/transfer the domain, decline
     unless you want to move registrars (optional, later).
4. Optional cleanup: Wix -> site -> Archive/Delete the old website so it stops
   showing as a draft in his account.

## Step 4. Email decision (before or right after launch)

The old site showed `info@LorozCustomBoats.onmicrosoft.com`. The new site shows
`info@lorozboats.com`.

- His M365 mailbox keeps working regardless (it's on Microsoft servers, not Wix).
- To make `info@lorozboats.com` actually receive mail, his M365/GoDaddy needs the
  domain added as a custom domain (adds MX + TXT records to DNS, which can live at
  Wix Domains or wherever the DNS ends up).
- Easiest v1: use Netlify Forms for the inquiry form (delivers to any inbox,
  no domain email needed) and keep the visible address as info@lorozboats.com
  once it's real, or swap the visible address to the onmicrosoft one until then.
- Ask dad which inbox he actually checks. I'll wire it.

## Step 5. Optional: move the domain registration away from Wix

Transfer the domain to Cloudflare Registrar or Namecheap (~$10-15/yr vs Wix
renewal pricing). Takes 5-7 days, requires an authorization code from Wix Domains.
Not required. Do it later if Wix renewal prices annoy him.

---

## Files that matter
- `_redirects`   -> old Wix URL redirects (Netlify)
- `sitemap.xml`  -> new pages for Google
- `robots.txt`   -> allow all
- `README.md`    -> project notes, image map, TODOs
- `debug_site.py`-> browser test harness: `python debug_site.py`
