# Loroz Custom Boats — Website

Rebuilt site for Loroz Custom Boats LLC (Bradenton, FL). Static HTML/CSS/JS, no build step.
Deployable to any static host (Netlify, Vercel, Cloudflare Pages, GitHub Pages).

## Pages
- `index.html` — Home (hero, boats, services, mission, contact strip)
- `boats.html` — LOROZ 17 + LOROZ 21 with spec charts and video
- `repair.html` — Fiberglass repair & restoration services
- `financing.html` — LightStream / BoatsLoans / Truist
- `contact.html` — Service inquiry form, address, hours

## Assets
- `assets/img/` — photos pulled from the old Wix site (compressed to web JPEG)
  - `hero-home.jpg` = video poster frame (1920x1080)
  - `boat-17-main.jpg` / `boat-21-main.jpg` / `boat-17-alt.jpg` / `boat-21-alt.jpg` = boat photos
  - `spec-17.jpg` / `spec-21.jpg` = spec charts (from old site)
  - `repair-1.jpg` / `repair-2.jpg` = shop / service photos
  - `hero-alt.jpg` = AI render candidate (1.8MB, swap in if the hero photo is preferred)
  - `brand-candidate-1.jpg` / `brand-candidate-2.jpg` = site-wide images from old site (logo candidates)
  - `gallery-1..6.jpg` = extra images from old site (currently unused, for future gallery)
- `assets/video/loroz-boat-video.mp4` = boat video (720p, 8.8MB)

## Notes / TODOs before launch
1. **Email**: forms + footer currently point to `info@lorozboats.com`.
   The old site exposed `info@LorozCustomBoats.onmicrosoft.com`.
   Decide the real inbox: set up an alias `info@lorozboats.com` on the M365/GoDaddy
   mailbox (or use a forwarding rule) so leads actually arrive.
2. **Forms**: no backend yet. On submit they open a mailto to info@lorozboats.com.
   For production, wire to Netlify Forms (add `data-netlify="true"` + name attr) or Formspree.
3. **Images**: verify the boat photos are the right models (17 vs 21) and swap as needed.
4. **Domain**: registered via Wix DNS. To go live, change nameservers (or DNS records)
   to the new host, then the old Wix site can be cancelled. Do NOT touch Wix until the
   new site is deployed and tested.
5. **JSON-LD**: schema.org BoatDealer structured data on index.html for local SEO.
6. Phone: `941-313-2191`, address `1315 27th Ave West, Unit 112, Bradenton, FL 34205`.
