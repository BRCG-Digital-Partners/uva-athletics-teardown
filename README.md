# UVA Athletics teardown

An unsolicited CRM teardown of the University of Virginia Athletics fan email
program, built by [BRCG](https://brcg.co) in Charlottesville.

Nobody asked for this. Kodie Critzer grew up in Charlottesville and went to UVA;
Henry Pollard helped build BRCG here. Virginia Athletics is the client we would
most like to work with, and this is the argument for why.

## Pages

| Page | What it covers |
| --- | --- |
| `index.html` | Overview, live inventory, season sellout table |
| `audit.html` | 78 sends mapped, the preference-centre finding, seven gaps in the Week 0 run-up |
| `data.html` | The three sending stacks, four layers on a patron record, the lifecycle layer |
| `apis.html` | Real Paciolan endpoints, real payloads, the merge-field contract |
| `lifecycle.html` | Eight triggers, a worked journey, how to measure it |
| `emails.html` | Five sends on UVA's real Eloqua template |

## Sourcing

Everything is built from public sources and one real subscriber inbox.

- **Send map** — a live UVA Athletics subscriber inbox, Oct 22 2025 to Aug 24 2026.
- **Inventory and pricing** — the public Paciolan catalog on `virginiasports.evenue.net`
  (org `VIRGINIA`, account `772`), read Aug 25 2026.
- **Endpoint and field names** — a network capture of one ordinary logged-in fan
  session. No personal data from that session appears anywhere on the site.
- **Preference centre** — the public form at `app.virginiasports.com/preferences`.
- **Email chrome** — UVA's own header, nav and footer images from `img.virginiasports.com`,
  and opponent logos from UVA's own S3 bucket.

Account values marked **scenario** in the NC State email are a returning-buyer
illustration; each maps to a Paciolan field that would populate it in production.

## Build

Static. No dependencies, no build step at deploy time.

```bash
python3 build.py     # regenerates the six HTML pages from build.py
```

Page content lives in the `*_body` strings in `build.py`. The shared shell,
nav and footer are in `shell()`. Styles are in `assets/portal.css`
(BRCG craft system: IBM Plex Sans + Mono, royal blue #0542BF, hairline borders,
no emoji, no decorative pills).

Email mockups in `emails/` are generated separately and copied in.

## Deploy

Vercel project `uva-athletics-teardown` on the BRCG scope. Link explicitly
before deploying — the folder is named `portal`, and `vercel deploy --yes` from
a generic folder name will link to the wrong project.

```bash
vercel link --yes --project uva-athletics-teardown
vercel deploy --prod --yes
```
