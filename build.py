#!/usr/bin/env python3
"""Build the UVA Athletics teardown portal.

Static multi-page site. Shared shell, one content block per page.
All figures read live from UVA's public ticketing stack on Aug 25, 2026.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent

PAGES = [
    ("index.html",     "Teardown",          "Overview"),
    ("audit.html",     "The audit",         "Audit"),
    ("data.html",      "Data architecture", "Data"),
    ("apis.html",      "APIs + templates",  "APIs"),
    ("lifecycle.html", "Lifecycle",         "Lifecycle"),
    ("emails.html",    "The emails",        "Emails"),
]

GAMES = [
    ("NC State",       "NCState",       "Sat Aug 29", "3:30 PM",  7549, 65181),
    ("Norfolk State",  "NorfolkState",  "Fri Sep 11", "7:00 PM", 25816, 65180),
    ("Delaware",       "Delaware",      "Sat Sep 26", "TBD",     24943, 65180),
    ("Syracuse",       "Syracuse",      "Sat Oct 10", "TBD",     25048, 65180),
    ("Duke",           "Duke",          "Fri Oct 23", "7:00 PM", 22999, 65180),
    ("California",     "California",    "Sat Nov 14", "TBD",     25388, 65180),
    ("North Carolina", "NorthCarolina", "Sat Nov 21", "TBD",     25136, 65180),
]
LOGO = "https://s3.us-west-2.amazonaws.com/pachtml-production/www/virginia/images/logos"
UNSOLD = sum(g[4] for g in GAMES)
CAP = sum(g[5] for g in GAMES)
SEASON_PCT = round(100 * (CAP - UNSOLD) / CAP, 1)


def shell(active, title, body):
    CUR = ' aria-current="page"'
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, CUR if h == active else "", lbl)
        for h, _, lbl in PAGES)
    idx = [p[0] for p in PAGES].index(active)
    pager = ""
    prev_ = PAGES[idx - 1] if idx > 0 else None
    next_ = PAGES[idx + 1] if idx < len(PAGES) - 1 else None
    if prev_ or next_:
        parts = ""
        if prev_:
            parts += f'<a href="{prev_[0]}"><div class="k">Previous</div><div class="t">{prev_[1]}</div></a>'
        if next_:
            parts += f'<a href="{next_[0]}"><div class="k">Next</div><div class="t">{next_[1]}</div></a>'
        pager = f'<div class="wrap"><div class="pager">{parts}</div></div>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; UVA Athletics teardown &middot; BRCG</title>
<meta name="description" content="An unsolicited CRM teardown of the UVA Athletics fan email program, built from a real subscriber inbox and public ticketing data by BRCG in Charlottesville.">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/portal.css">
</head>
<body>
<header class="mast">
  <div class="mast-in">
    <img src="assets/brcg-logo-blue.png" alt="Blue Ridge Consulting Group" class="logo">
    <span class="div"></span>
    <span class="who">UVA Athletics teardown</span>
    <nav class="nav">{nav}</nav>
  </div>
</header>
{body}
{pager}
<footer class="foot">
  <div class="foot-in">
    <span>Blue Ridge Consulting Group &middot; Charlottesville, VA</span>
    <span>&middot;</span>
    <a href="https://brcg.co">brcg.co</a>
    <span>&middot;</span>
    <a href="mailto:kodie@brcg.co">kodie@brcg.co</a>
    <span>&middot;</span>
    <span>Built from public sources &middot; figures read Aug 25, 2026</span>
  </div>
</footer>
</body>
</html>'''


def rail(cells):
    out = "".join(
        f'<div class="cell"><div class="lab">{l}</div>'
        f'<div class="val{" hl" if hl else ""}">{v}</div><div class="note">{n}</div></div>'
        for l, v, n, hl in cells)
    return f'<div class="rail">{out}</div>'


def games_table():
    rows = ""
    for opp, slug, date, time, av, cap in GAMES:
        p = round(100 * (cap - av) / cap, 1)
        hl = ' style="background:#FFF6F2"' if opp == "NC State" else ""
        rows += f'''<tr{hl}>
          <td><img src="{LOGO}/{slug}.png" alt="" style="width:26px;height:auto"></td>
          <td><strong>{opp}</strong></td>
          <td class="m">{date} &middot; {time}</td>
          <td style="min-width:130px"><div class="bar"><i style="width:{p}%"></i></div></td>
          <td class="m" style="text-align:right;white-space:nowrap">{p}%</td>
          <td class="m" style="text-align:right;white-space:nowrap">{av:,}</td>
        </tr>'''
    return f'''<div class="tbl-wrap"><table>
      <thead><tr><th></th><th>Opponent</th><th>Kickoff</th><th>Sold</th>
      <th style="text-align:right">%</th><th style="text-align:right">Seats left</th></tr></thead>
      <tbody>{rows}</tbody></table></div>'''


# ─────────────────────────────────────────────────────────── INDEX
index_body = f'''
<div class="wrap">
  <div class="hero">
    <div class="kicker">Unsolicited teardown &middot; built in Charlottesville</div>
    <h1>UVA Athletics runs great campaigns on top of <span class="q">no lifecycle at all.</span></h1>
    <p class="lede">
      Kodie Critzer and Henry Pollard founded BRCG here. Kodie went to UVA. Nobody asked us for this.
      We built it because Virginia Athletics is the client we would most like to work with, and because
      the fan email program is 78 sends in 10 months of genuinely well-run campaign operations with nothing
      underneath them. Every figure on this site was read from UVA&rsquo;s own public systems.
    </p>
    {rail([
      ("Sends mapped", "78", "Oct 22, 2025 &rarr; Aug 24, 2026, one real subscriber inbox", False),
      ("Seats unsold, Week 0", "7,549", "of 65,181 against NC State, four days out", True),
      ("Unsold, full season", "156,879", f"{SEASON_PCT}% of the season sold across seven home games", False),
      ("Lifecycle triggers", "0", "No welcome, abandon, post-attendance, win-back or re-engagement", False),
    ])}
  </div>

  <section>
    <div class="sec-head">
      <h2>The one-paragraph version</h2>
    </div>
    <div class="grid g3">
      <div class="card">
        <div class="kick">What works</div>
        <h3>The campaign operation</h3>
        <p>78 sends in 10 months with no missed week. Real price laddering, real partner revenue,
        a consistent template that never breaks. Somebody is shipping on deadline every single week
        and the offers are good.</p>
      </div>
      <div class="card">
        <div class="kick">What is missing</div>
        <h3>Everything underneath it</h3>
        <p>Not one send in 306 days was triggered by subscriber behaviour. No welcome, no abandon,
        no post-attendance, no win-back. Every email is a manually scheduled broadcast to the whole file.</p>
      </div>
      <div class="card">
        <div class="kick">Why it matters</div>
        <h3>The data is already there</h3>
        <p>Paciolan holds every order, seat, scan and points balance. Eloqua holds first name, zip,
        birthday and twelve sport preferences. None of it reaches a send. This is a plumbing problem,
        not a budget problem.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="dark">
      <div class="kick">Live inventory &middot; read Aug 25, 2026 &middot; four days to kickoff</div>
      <div class="big">7,549</div>
      <p style="margin-top:14px;max-width:64ch">
        Seats still unsold for the NC State home opener, against a capacity of 65,181, with
        <code style="background:rgba(255,255,255,.1);border-color:transparent;color:#fff">SOLD_OUT: false</code>
        and all six price levels open. UVA has been running a campaign called &ldquo;Sell Out Scott&rdquo;
        since July 10. Nothing in the email program reads this number.
      </p>
    </div>
  </section>

  <section>
    <div class="sec-head">
      <h2>The whole season, by how full it is</h2>
      <p class="sub">Per-game availability from <code>pac-api/catalog/eventDetailMPT</code>. NC State is the
      outlier at 88.4%. Every other home game sits around 61%.</p>
    </div>
    {games_table()}
    <p class="sub" style="margin-top:14px;margin-bottom:0">
      Seven home games &middot; {CAP:,} seats &middot; {SEASON_PCT}% sold &middot;
      <strong>{UNSOLD:,} still available across the season</strong>
    </p>
  </section>

  <section>
    <div class="sec-head">
      <h2>What is on this site</h2>
    </div>
    <div class="grid g2">
      <div class="card"><div class="kick">01</div><h3><a href="audit.html">The audit</a></h3>
        <p>All 78 sends, the 22-email run-up to Saturday, the preference centre finding, and the seven
        things the pre-season push left on the table.</p></div>
      <div class="card"><div class="kick">02</div><h3><a href="data.html">Data architecture</a></h3>
        <p>The three sending stacks, what each system holds today, and the shape of the lifecycle layer
        that sits on top without replacing any of them.</p></div>
      <div class="card"><div class="kick">03</div><h3><a href="apis.html">APIs and data templates</a></h3>
        <p>The real Paciolan endpoints, real response payloads, and the merge-field contract a lifecycle
        ESP would bind to.</p></div>
      <div class="card"><div class="kick">04</div><h3><a href="lifecycle.html">Lifecycle</a></h3>
        <p>Eight triggers the ticketing system could already be firing, each mapped to the field behind
        it, with entry, timing, suppression and the measure.</p></div>
      <div class="card"><div class="kick">05</div><h3><a href="emails.html">The emails</a></h3>
        <p>Five sends built on UVA&rsquo;s real Eloqua template, including a full Week 0 email where every
        figure was read live from the ticketing system.</p></div>
      <div class="card tint"><div class="kick">Contact</div><h3>We would love to work with you</h3>
        <p>No gate, no form, no NDA. If anyone at UVA Athletics or the VAF wants the send map or the
        segment definitions, they are yours for the asking.
        <a href="mailto:kodie@brcg.co">kodie@brcg.co</a></p></div>
    </div>
  </section>
</div>
'''

# ─────────────────────────────────────────────────────────── AUDIT
audit_body = f'''
<div class="wrap">
  <div class="hero">
    <div class="kicker">01 &middot; The audit</div>
    <h1>78 emails. One sender. <span class="q">Zero segmentation.</span></h1>
    <p class="lede">
      Pulled from a live UVA Athletics subscriber inbox between Oct 22, 2025 and Aug 24, 2026. Every send
      arrives from <code>updates@go.virginiasports.com</code> on Oracle Eloqua. Cadence is roughly one
      every four days, across eight sports, to one person, regardless of stated interest.
    </p>
    {rail([
      ("Total sends", "78", "306 days. 75 from Eloqua, 2 CavFutures, 1 personal Outlook", False),
      ("Pre-season push", "22", "Jun 1 &rarr; Aug 24. Ten of them in August alone", False),
      ("Personalization", "0%", "First name is a required field and appears in no send", True),
      ("Sending stacks", "3", "Eloqua, personal Outlook, Mailchimp. Zero integration", False),
    ])}
  </div>

  <section>
    <div class="sec-head">
      <h2>The finding that reframes everything</h2>
      <p class="sub">UVA&rsquo;s own preference centre, linked in the footer of all 78 emails, already collects
      the segmentation the program is missing. It writes to Eloqua. Nothing reads it back.</p>
    </div>
    <div class="grid g3">
      <div class="card">
        <div class="kick">Identity collected</div>
        <p><strong>First name</strong> (required)<br><strong>Last name</strong> (required)<br>
        Zip / postal code<br>Birthday (MM/DD/YYYY)</p>
      </div>
      <div class="card">
        <div class="kick">Content categories</div>
        <p>Ticket Information &amp; Special Offers<br>Virginia Athletics Foundation<br>
        Virginia Sports Properties<br>Jeff White &middot; Weekly Hoo Mail<br><strong>Game Day Info</strong></p>
      </div>
      <div class="card">
        <div class="kick">Sport preferences</div>
        <p>All Sports, Football, Baseball, Softball, Volleyball, Men&rsquo;s &amp; Women&rsquo;s Basketball,
        Men&rsquo;s &amp; Women&rsquo;s Lacrosse, Men&rsquo;s &amp; Women&rsquo;s Soccer, All Other Olympic Sports.</p>
        <p class="m" style="margin-top:10px;color:var(--soft)">&rarr; hiddenField&ndash;hiddenField12</p>
      </div>
    </div>
    <div class="note warn" style="margin-top:16px">
      <p><strong>And the one control that does work is the blunt one.</strong> Every footer reads
      &ldquo;by unsubscribing you are opting out of ALL email communications from University of Virginia
      Athletics.&rdquo; Granular preferences on the way in, a single global switch on the way out.</p>
    </div>
  </section>

  <section>
    <div class="sec-head">
      <h2>Seven things the Week 0 run-up left on the table</h2>
      <p class="sub">Between June 1 and August 24 the program sent 22 emails into the highest-intent selling
      window of the year. Here is what was not in them.</p>
    </div>
    <div class="tbl-wrap"><table>
      <thead><tr><th>#</th><th>Gap</th><th>What was missing</th><th>The send</th></tr></thead>
      <tbody>
        <tr><td class="m">01</td><td><strong>Parking</strong></td>
          <td>Parking went digital on Jun 24. Hangtags gone for football, both basketballs and baseball.
          Announced as a news post, 66 days before kickoff. Never mentioned in any of the 22 emails.</td>
          <td>Permit holders only, T&minus;21 and T&minus;5. Screenshot walkthrough and app deep link.</td></tr>
        <tr><td class="m">02</td><td><strong>Gameday</strong></td>
          <td>The preference centre offers a &ldquo;Game Day Info&rdquo; category. Subscribers opt into it.
          As of four days out, the last send was a tailgate upsell.</td>
          <td>Thursday before each home game, ticket holders. Gates, bags, parking retrieval, weather. Zero sell.</td></tr>
        <tr><td class="m">03</td><td><strong>Win-back</strong></td>
          <td>A 2024 season-ticket holder who did not renew got the identical 22 sends as someone who has
          never purchased. Paciolan knows the difference.</td>
          <td>Reference the actual section and row. Same-or-better seat for Week 0.</td></tr>
        <tr><td class="m">04</td><td><strong>Sport</strong></td>
          <td>Men&rsquo;s basketball schedule news went to the whole file on Aug 20, nine days before a
          football home opener. Twelve sport preferences sit unused in Eloqua.</td>
          <td>One trigger, split on the sport-affinity field already on the record.</td></tr>
        <tr><td class="m">05</td><td><strong>Geography</strong></td>
          <td>Zip is collected. A fan in Charlottesville and a fan in Northern Virginia got the same
          Week 0 push for a 3:30 Saturday kickoff.</td>
          <td>Drive-time framing by radius. Inside 30 miles, 60&ndash;120, and beyond.</td></tr>
        <tr><td class="m">06</td><td><strong>Identity</strong></td>
          <td>First name is a required field on the subscription form and appears in zero sends. The
          Aug 18 letter from the Director of Athletics opens &ldquo;Wahoo Nation.&rdquo;</td>
          <td>A one-line template change with no data work behind it.</td></tr>
        <tr><td class="m">07</td><td><strong>Support</strong></td>
          <td>The Aug 24 game-week email routes questions to a ticket office open Monday to Friday,
          9 to 5. The game is Saturday.</td>
          <td>Self-serve block plus a gameday SMS line. Deflect the call rather than route it somewhere closed.</td></tr>
      </tbody>
    </table></div>
  </section>

  <section>
    <div class="sec-head">
      <h2>What the calendar proves</h2>
    </div>
    <div class="grid g4">
      <div class="card"><div class="num">78</div><div class="kick" style="margin:9px 0 0">Sends mapped</div>
        <p style="margin-top:8px">306 days. Two peaks: basketball in Jan&ndash;Feb, football in August.</p></div>
      <div class="card"><div class="num">~3.9d</div><div class="kick" style="margin:9px 0 0">Average gap</div>
        <p style="margin-top:8px">August ran one every 2.3 days, including two on Aug 19 thirteen hours apart.</p></div>
      <div class="card"><div class="num">0</div><div class="kick" style="margin:9px 0 0">Behavioural triggers</div>
        <p style="margin-top:8px">The Aug 19 &ldquo;finish your gift&rdquo; email reached a subscriber with no
        abandoned gift, which makes it a batch send wearing a trigger&rsquo;s copy.</p></div>
      <div class="card"><div class="num">8</div><div class="kick" style="margin:9px 0 0">Sports to one inbox</div>
        <p style="margin-top:8px">Football, both basketballs, both lacrosses, baseball, softball, volleyball.</p></div>
    </div>
  </section>
</div>
'''

# ─────────────────────────────────────────────────────────── DATA
data_body = '''
<div class="wrap">
  <div class="hero">
    <div class="kicker">02 &middot; Data architecture</div>
    <h1>Three systems that hold everything and <span class="q">one that sends everything.</span></h1>
    <p class="lede">
      The fan email program runs on Oracle Eloqua via WMT Digital. VAF major-gift outreach happens one to one
      from personal Outlook. CavFutures NIL is on Mailchimp. Paciolan sits underneath all of it holding the
      transactional truth. The four do not talk.
    </p>
  </div>

  <section>
    <div class="sec-head"><h2>Today</h2>
      <p class="sub">Every arrow that should exist between these boxes is missing. Data flows into them and
      stops.</p></div>
    <div class="grid g4">
      <div class="card">
        <div class="tag live">Paciolan</div>
        <h3 style="margin-top:10px">Ticketing and fundraising</h3>
        <p>Orders, seats, scans, transfers, resale listings, priority points, giving level, parking SKUs,
        membership tier. The richest behavioural data in the building.</p>
        <p class="m" style="margin-top:10px;color:var(--soft)">org VIRGINIA &middot; account 772</p>
      </div>
      <div class="card">
        <div class="tag live">Eloqua</div>
        <h3 style="margin-top:10px">Email sending</h3>
        <p>First name, last name, zip, birthday, six content categories, twelve sport preferences.
        Collected on the public preference form, written to hidden fields, never merged into a send.</p>
        <p class="m" style="margin-top:10px;color:var(--soft)">via WMT Digital</p>
      </div>
      <div class="card">
        <div class="tag gap">Outlook</div>
        <h3 style="margin-top:10px">VAF major gifts</h3>
        <p>One-to-one outreach from a personal mailbox. No record of it reaches the email platform, so a
        major-gift prospect can receive a mass solicitation the same week.</p>
      </div>
      <div class="card">
        <div class="tag gap">Mailchimp</div>
        <h3 style="margin-top:10px">CavFutures NIL</h3>
        <p>A separate list on a separate platform with separate suppression. Invisible to both of the
        other two.</p>
      </div>
    </div>
    <div class="note warn" style="margin-top:16px">
      <p><strong>One exception worth crediting.</strong> Ticketing and fundraising already meet at checkout.
      The NC State event record carries an <code>OFFERS_AND_ROUNDUPS</code> block with a VAF donation at
      $250 / $100 / $50 / $25 / $10 plus a round-up. The silo this teardown describes is an email silo,
      not a systems silo.</p>
    </div>
  </section>

  <section>
    <div class="sec-head"><h2>What a lifecycle layer looks like</h2>
      <p class="sub">Nothing gets replaced. A thin layer reads from Paciolan, resolves identity against
      Eloqua, and writes triggered sends back through the platform UVA already pays for.</p></div>
    <div class="flow">
      <div class="node">
        <div class="tag live">Source</div>
        <h3 style="margin-top:9px">Paciolan + Eloqua</h3>
        <p>Order history, scans, points, transfers, inventory. Plus the preference-centre fields already
        captured against each contact.</p>
      </div>
      <div class="arrow">&rarr;</div>
      <div class="node">
        <div class="tag plan">New</div>
        <h3 style="margin-top:9px">Identity + event layer</h3>
        <p>Reconcile the Paciolan patron ID against the Eloqua contact. Emit behavioural events:
        purchased, scanned, lapsed, listed, upgraded, abandoned.</p>
      </div>
      <div class="arrow">&rarr;</div>
      <div class="node">
        <div class="tag live">Send</div>
        <h3 style="margin-top:9px">Eloqua, unchanged</h3>
        <p>Same platform, same templates, same agency. The only difference is that a send can now be
        entered by a behaviour rather than a calendar.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="sec-head"><h2>The four layers already on a patron record</h2></div>
    <div class="tbl-wrap"><table>
      <thead><tr><th>Layer</th><th>What it holds</th><th>What it unlocks</th><th>State</th></tr></thead>
      <tbody>
        <tr><td><strong>Identity and location</strong></td>
          <td>Account ID, name, email, mailing address and zip, phone, household links.</td>
          <td>First-name merge, drive-time segmentation, household de-duplication.</td>
          <td><span class="tag live">Collected</span></td></tr>
        <tr><td><strong>Transactions</strong></td>
          <td>Every order by event: section, row, seat, price level, promo used, add-ons, purchase date
          relative to the game, channel.</td>
          <td>Win-back on real seats, partial-plan completion, price-tier upgrade paths.</td>
          <td><span class="tag live">Collected</span></td></tr>
        <tr><td><strong>Access and behaviour</strong></td>
          <td>Barcode scans at the gate, digital ticket transfers, resale listings, My Account logins,
          app installs.</td>
          <td>Post-attendance follow-up, no-show recovery, churn detection before renewal.</td>
          <td><span class="tag live">Collected</span></td></tr>
        <tr><td><strong>Giving and priority</strong></td>
          <td>Priority-points balance, giving level, VAF tier, seat and parking eligibility, pledge status.</td>
          <td>Points-threshold nudges, benefit-gated offers, donor onboarding.</td>
          <td><span class="tag gap">Hidden from the fan</span></td></tr>
      </tbody>
    </table></div>
    <div class="note" style="margin-top:16px">
      <p><strong>The priority-points case is the sharpest one.</strong> The patron endpoint returns
      <code>custPriPoints</code>, <code>donPriPoints</code>, <code>orderPriPtsTotal</code> and
      <code>priPtsTotal</code> on every account load. But UVA&rsquo;s live config has
      <code>myprioritypoints.enabled = false</code> and <code>newmygivinghistory.enabled = false</code>,
      so the fan cannot see the balance in My Account either. It is computed continuously and shown to nobody.</p>
    </div>
  </section>

  <section>
    <div class="sec-head"><h2>Platform capability, switched on and unused</h2>
      <p class="sub">Read from the public config endpoint. These are features UVA already pays for.</p></div>
    <div class="grid g2">
      <div class="card">
        <div class="kick">Enabled, never mentioned in email</div>
        <p><code>findPromotions</code> and <code>promos</code> &mdash; a targeted promotion engine.<br>
        <code>donationoffers</code> and <code>donationpages</code> &mdash; giving inside the ticket cart.<br>
        <code>addons</code>, <code>combos</code>, <code>multi.addons</code> &mdash; parking and chairbacks bundled at purchase.<br>
        <code>students</code> with Shibboleth SSO &mdash; student ticketing.</p>
      </div>
      <div class="card">
        <div class="kick">Switched off, or configured onto nothing</div>
        <p><code>myprioritypoints</code> and <code>newmygivinghistory</code> &mdash; both false.<br>
        <code>billplans</code> &mdash; enabled at the platform level, but <code>HAS_BILL_PLANS</code> is false
        on all ten upcoming events.<br>
        <code>maxOrderHistoryMonthRange</code> &mdash; 12 months, shorter than the win-back window it would serve.<br>
        <code>displayallfees</code> &mdash; false, so fees appear late in the flow.</p>
      </div>
    </div>
  </section>
</div>
'''

# ─────────────────────────────────────────────────────────── APIS
apis_body = '''
<div class="wrap">
  <div class="hero">
    <div class="kicker">03 &middot; APIs and data templates</div>
    <h1>The endpoints that already answer <span class="q">every question a send would ask.</span></h1>
    <p class="lede">
      Paciolan&rsquo;s developer documentation is partner-gated. Everything below instead comes from UVA&rsquo;s
      own live implementation: the public catalog endpoints and a network capture of one ordinary logged-in
      fan session. The route names and field names are the real ones. No personal data appears here.
    </p>
  </div>

  <section>
    <div class="sec-head"><h2>The routes</h2>
      <p class="sub">Each one maps to a lifecycle trigger on the next page.</p></div>
    <div class="tbl-wrap"><table>
      <thead><tr><th>Endpoint</th><th>Returns</th><th>Drives</th></tr></thead>
      <tbody>
        <tr><td class="m">pac-api/catalog/eventDetailMPT/{season}/{event}</td>
          <td>Capacity, unsold count, sold-out flag, promo flag, on-sale timestamp, donation offers.</td>
          <td>Inventory-aware sends. Scarcity versus discount.</td></tr>
        <tr><td class="m">pac-api/seat-availability/event-id/{id}/pricelevel</td>
          <td>Availability by price tier, hold codes, platinum markers.</td>
          <td>Tier-targeted offers, upgrade paths.</td></tr>
        <tr><td class="m">pac-api/orderhistory</td>
          <td>Purchase history by event.</td>
          <td>Lapsed win-back, partial-plan completion.</td></tr>
        <tr><td class="m">pac-api/orderhistory/pendingTransfers</td>
          <td>Tickets transferred but not yet accepted.</td>
          <td>Churn signal, guest capture.</td></tr>
        <tr><td class="m">pac-api/order/ballena/upgrades</td>
          <td>Upgrade offers available against seats already owned.</td>
          <td>A personalised, revenue-positive email nobody sends.</td></tr>
        <tr><td class="m">pac-api/memberships</td>
          <td>Membership tier and status.</td>
          <td>Benefit gating, renewal timing.</td></tr>
        <tr><td class="m">app/ws/patron/{id}/myAccount</td>
          <td>Priority points, student flag, exchange / transfer / return rights.</td>
          <td>Points-threshold nudges, eligibility-aware offers.</td></tr>
        <tr><td class="m">pac-api/consumer/gql</td>
          <td>GraphQL. Every upcoming event across every sport in one call.</td>
          <td>Cross-sport pull, dynamic schedule modules.</td></tr>
      </tbody>
    </table></div>
  </section>

  <section>
    <div class="sec-head"><h2>Real payload &middot; event inventory</h2>
      <p class="sub">Trimmed from the live NC State response. This single object contains the seat count, the
      theme, the on-sale time and the entire donation ladder.</p></div>
    <div class="pre-head"><span class="dot"></span>GET pac-api/catalog/eventDetailMPT/F26/F01</div>
    <pre><code>{
  <span class="k">"ITEMCD"</span>: <span class="s">"F01"</span>,
  <span class="k">"EVENTNAME"</span>: <span class="s">"NC State"</span>,
  <span class="k">"FAC_TITLE"</span>: <span class="s">"Scott Stadium"</span>,
  <span class="k">"EVENTDTFAC"</span>: <span class="s">"2026-08-29T15:30:00.000Z"</span>,
  <span class="k">"SALEFROMDT"</span>: <span class="s">"2026-07-01T09:00:00.000Z"</span>,
  <span class="k">"SOLD_OUT"</span>: <span class="n">false</span>,
  <span class="k">"HASPROMO"</span>: <span class="n">true</span>,
  <span class="k">"AVAILABLE"</span>: <span class="n">7549</span>,          <span class="c">// the number no email reads</span>
  <span class="k">"TOTALCAPACITY"</span>: <span class="n">65181</span>,
  <span class="k">"HAS_BILL_PLANS"</span>: <span class="n">false</span>,
  <span class="k">"EVENT_MESSAGE"</span>: <span class="s">"Paint the Town ORANGE! Fan-First discounts
                      available on 4 to 10 seats..."</span>,
  <span class="k">"OFFERS_AND_ROUNDUPS"</span>: [{
    <span class="k">"CATEGORY"</span>: <span class="s">"DO"</span>,
    <span class="k">"OFFER_DETAILS"</span>: {
      <span class="k">"ITEMNAME"</span>: <span class="s">"Virginia Athletics Foundation Donation"</span>,
      <span class="k">"ALLOWCUSTOMERAMOUNT"</span>: <span class="s">"Y"</span>,
      <span class="k">"AMOUNTS"</span>: [<span class="n">25000</span>, <span class="n">10000</span>, <span class="n">5000</span>, <span class="n">2500</span>, <span class="n">1000</span>]  <span class="c">// cents</span>
    }
  }]
}</code></pre>
  </section>

  <section>
    <div class="sec-head"><h2>Real payload &middot; patron record</h2>
      <p class="sub">Shape only, values removed. Note the four points fields, all populated on every account
      load, none of them surfaced to the fan or to a send.</p></div>
    <div class="pre-head"><span class="dot"></span>GET app/ws/patron/{id}/myAccount</div>
    <pre><code>{
  <span class="k">"value"</span>: {
    <span class="k">"custPriPoints"</span>:     <span class="c">// customer priority points</span>
    <span class="k">"donPriPoints"</span>:      <span class="c">// donor priority points</span>
    <span class="k">"orderPriPtsTotal"</span>:  <span class="c">// points from orders</span>
    <span class="k">"priPtsTotal"</span>:       <span class="c">// combined total</span>
    <span class="k">"patronVo"</span>: {
      <span class="k">"fname"</span>, <span class="k">"lname"</span>, <span class="k">"patronId"</span>, <span class="k">"cstmType"</span>,
      <span class="k">"isStudent"</span>,
      <span class="k">"exchfl"</span>, <span class="k">"transferfl"</span>, <span class="k">"returnfl"</span>   <span class="c">// entitlements</span>
    },
    <span class="k">"relatedSites"</span>: [ <span class="c">// seat + parking selection portals</span> ]
  }
}</code></pre>
  </section>

  <section>
    <div class="sec-head"><h2>The merge-field contract</h2>
      <p class="sub">What a lifecycle layer would expose to the template. Everything in the first two groups
      exists today. Nothing here requires new data collection.</p></div>
    <div class="tbl-wrap"><table>
      <thead><tr><th>Field</th><th>Source</th><th>Example</th><th>Used today</th></tr></thead>
      <tbody>
        <tr><td class="m">first_name</td><td>Eloqua preference form</td><td class="m">Kodie</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">sport_affinity[]</td><td>Eloqua hiddenField&ndash;12</td><td class="m">["football","mbb"]</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">zip / drive_time</td><td>Eloqua + patron address</td><td class="m">22932 &middot; 20 min</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">last_seat</td><td>pac-api/orderhistory</td><td class="m">117 / K / 9-10</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">games_attended</td><td>Barcode scans</td><td class="m">4 of 7</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">priority_points</td><td>app/ws/patron myAccount</td><td class="m">84</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">upgrade_offer</td><td>order/ballena/upgrades</td><td class="m">Preferred, +$34</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">event.available</td><td>catalog/eventDetailMPT</td><td class="m">7549</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">event.pct_sold</td><td>Derived</td><td class="m">88.4</td>
          <td><span class="tag gap">No</span></td></tr>
        <tr><td class="m">parking_sku</td><td>Order add-ons</td><td class="m">null</td>
          <td><span class="tag gap">No</span></td></tr>
      </tbody>
    </table></div>
  </section>

  <section>
    <div class="sec-head"><h2>What the template binding looks like</h2>
      <p class="sub">A worked example. The same 600px Eloqua template, entered by a behaviour instead of a
      calendar date.</p></div>
    <div class="pre-head"><span class="dot"></span>trigger: lapsed_buyer_week0</div>
    <pre><code><span class="c"># entry</span>
<span class="k">when</span>:      orderhistory.last_order_season <span class="k">in</span> [<span class="s">"F24"</span>, <span class="s">"F25"</span>]
           <span class="k">and</span> orderhistory.orders_this_season == <span class="n">0</span>
           <span class="k">and</span> event.days_until <span class="k">between</span> <span class="n">3</span> <span class="k">and</span> <span class="n">10</span>

<span class="c"># suppression</span>
<span class="k">unless</span>:    contact.opted_out
           <span class="k">or</span> orderhistory.has_order(event.id)
           <span class="k">or</span> sends.last_7d &gt;= <span class="n">2</span>

<span class="c"># payload</span>
<span class="k">merge</span>:
  first_name:      patron.fname
  last_seat:       orderhistory.last.section + <span class="s">"/"</span> + row
  games_attended:  scans.count(season=<span class="s">"F25"</span>)
  points:          patron.priPtsTotal
  seats_left:      event.AVAILABLE
  pct_sold:        <span class="n">100</span> * (event.TOTALCAPACITY - event.AVAILABLE) / event.TOTALCAPACITY
  upgrade:         upgrades.best(patron.id, event.id)

<span class="c"># measure</span>
<span class="k">against</span>:   holdout <span class="n">10</span>%, orders attributed <span class="n">7</span>-day click / <span class="n">1</span>-day view</code></pre>
  </section>
</div>
'''

# ─────────────────────────────────────────────────────────── LIFECYCLE
TRIGGERS = [
    ("01", "Proximity", "Local, engaged, never bought",
     "zip + orders_lifetime = 0 + opens &gt; 25%",
     "&ldquo;You&rsquo;re 20 minutes from kickoff.&rdquo; One offer at the entry price, plus the parking instruction.",
     "T&minus;5 days, every home game"),
    ("02", "Abandon", "A real trigger, not a batch in trigger's clothing",
     "evenue checkout session with no completed order",
     "UVA already built this creative. The Aug 19 &ldquo;Finish Making Your Impact&rdquo; email exists and looks right. Wire it to the cart event.",
     "T+2 hours, T+24 hours"),
    ("03", "Attendance", "Bought a ticket versus walked through the gate",
     "barcode_scan on first_order",
     "&ldquo;You were 1 of 64,217.&rdquo; Multi-game step-up to attendees. A separate, quieter note to no-shows.",
     "Within 90 minutes of the whistle"),
    ("04", "Lapsed", "Bought last season, nothing this season",
     "last_order_season in F24/F25, no F26 order",
     "Name the real section and row. Same-or-better seat for the next home game.",
     "T&minus;10 days, then once more"),
    ("05", "Partial plan", "Bought two games out of seven",
     "orders_this_season vs home_games_total",
     "Complete the season, priced at the delta. Show what they own, show the gap, charge the difference.",
     "After game two"),
    ("06", "Parking", "Holds tickets, holds no parking pass",
     "has_ticket = true AND parking_sku = null",
     "Attach the pass and explain the new digital system in one email.",
     "T&minus;10 and T&minus;3 days"),
    ("07", "Points", "Sitting just under a benefit threshold",
     "priPtsTotal against the next tier",
     "&ldquo;You&rsquo;re 41 points from priority parking.&rdquo; A progress bar and the exact gift that closes it.",
     "Quarterly, and at renewal"),
    ("08", "Resale", "Listed their seats or transferred them away",
     "pendingTransfers + secondary listings",
     "One game listed: help them sell it. Four or more: that is a renewal at risk, route it to a human at the VAF.",
     "On the listing event"),
]

trigger_rows = "".join(f'''<tr>
  <td class="m">{n}</td>
  <td><strong>{name}</strong><div class="m" style="color:var(--soft);margin-top:3px">{when}</div></td>
  <td><strong>{title}</strong><p style="font-size:13.5px;margin-top:5px">{send}</p></td>
  <td class="m" style="white-space:nowrap">{sig}</td>
</tr>''' for n, name, title, sig, send, when in TRIGGERS)

lifecycle_body = f'''
<div class="wrap">
  <div class="hero">
    <div class="kicker">04 &middot; Lifecycle</div>
    <h1>Eight sends the ticketing system <span class="q">could already be firing.</span></h1>
    <p class="lede">
      Each one names the field that drives it. None require new data collection, a platform migration or
      leaving Eloqua. Seven home games remain after Week 0, which is seven live tests rather than a
      planning cycle.
    </p>
  </div>

  <section>
    <div class="tbl-wrap"><table>
      <thead><tr><th>#</th><th>Trigger &amp; signal</th><th>The send</th><th>Timing</th></tr></thead>
      <tbody>{trigger_rows}</tbody>
    </table></div>
  </section>

  <section>
    <div class="sec-head"><h2>A worked journey</h2>
      <p class="sub">One fan, one season. Every step is entered by something they did, not by a date on a
      marketing calendar.</p></div>
    <div class="grid g3">
      <div class="card"><div class="kick">Week &minus;1</div><h3>Win-back</h3>
        <p>Bought in 2025, nothing yet in 2026. Email names Section 117 and offers the same seats at last
        year&rsquo;s price. Entry: <code>orderhistory</code>.</p></div>
      <div class="card"><div class="kick">Purchase +1h</div><h3>Confirmation that sells nothing</h3>
        <p>Seats, kickoff, how digital parking works now, what to bring. Entry: order created.
        Suppresses every promo for 48 hours.</p></div>
      <div class="card"><div class="kick">Thursday</div><h3>Gameday logistics</h3>
        <p>Gates, bag policy, ticket and parking retrieval, weather, traffic. Zero sell. Entry:
        holds a ticket for a home game in 48 hours.</p></div>
      <div class="card"><div class="kick">Whistle +90m</div><h3>Post-attendance</h3>
        <p>Scanned in, so the recap is true for them. Attendance count, next home game, upgrade offer if
        one exists. Entry: <code>barcode_scan</code>.</p></div>
      <div class="card"><div class="kick">Game +3d</div><h3>Points and progress</h3>
        <p>Balance after this purchase, distance to the next benefit tier. The number Paciolan already
        computes and nobody sees. Entry: points delta.</p></div>
      <div class="card"><div class="kick">Season end</div><h3>Renewal, priced honestly</h3>
        <p>Games attended, what they spent one at a time, what the season plan would have cost. Entry:
        final home game scanned.</p></div>
    </div>
  </section>

  <section>
    <div class="sec-head"><h2>How to run it so the numbers mean something</h2></div>
    <div class="grid g3">
      <div class="card"><div class="kick">Holdout</div><h3>10% of every trigger</h3>
        <p>Withhold a random tenth from each behavioural send. Without it, incrementality is a guess and
        every win gets attributed to the email that happened to arrive last.</p></div>
      <div class="card"><div class="kick">Governance</div><h3>Frequency cap across teams</h3>
        <p>On Aug 19 two emails went out thirteen hours apart from two different teams. A shared cap and a
        priority order stops that without a meeting.</p></div>
      <div class="card"><div class="kick">Suppression</div><h3>Behaviour beats calendar</h3>
        <p>Anyone in a triggered flow drops out of the broadcast for its duration. Buyers stop seeing
        acquisition offers the moment they buy.</p></div>
    </div>
    <div class="note" style="margin-top:16px">
      <p><strong>Sequencing.</strong> Gameday and digital parking ship first because they need no new data
      and they deflect support volume on the first Saturday of a new parking system. Field activation
      (first name, sport, zip) is second because it is a template change. Win-back and the real behavioural
      triggers are third because they carry the largest revenue and the most build.</p>
    </div>
  </section>
</div>
'''

# ─────────────────────────────────────────────────────────── EMAILS
MAILS = [
    ("ncstate.html", "NC State, Week 0", "Returning buyer &middot; live inventory, per-game CTAs, upgrade offer",
     "Every figure read live", 3100),
    ("win.html", "Post-game win", "First-time attendee &middot; multi-game step-up",
     "90 min post-whistle", 1500),
    ("loss.html", "Post-game loss", "Season-ticket holder &middot; loyalty, zero ask",
     "The moment programs go quiet", 1500),
    ("giving.html", "Hoos Giving Day", "Sabre Society donor &middot; live leaderboard and match window",
     "Real-time state beats copy", 1650),
    ("welcome.html", "VAF first gift", "New donor &middot; five-part welcome, 30-day no-ask",
     "T+2 days", 1650),
]

mail_blocks = "".join(f'''
  <section>
    <div class="mail">
      <div class="mail-head">
        <span class="t">{t}</span>
        <span class="s">{s}</span>
        <span class="r">{r}</span>
      </div>
      <iframe src="emails/{f}" title="{t}" loading="lazy" height="{h}"></iframe>
    </div>
  </section>''' for f, t, s, r, h in MAILS)

emails_body = f'''
<div class="wrap">
  <div class="hero">
    <div class="kicker">05 &middot; The emails</div>
    <h1>UVA&rsquo;s own template. <span class="q">Five better sends.</span></h1>
    <p class="lede">
      Every mockup below is built on UVA&rsquo;s real Eloqua template, not an interpretation of it. Same 600px
      table, same Arial, same navy and orange, same 2px buttons, and the live header, nav and footer images
      pulled straight from <code>img.virginiasports.com</code>. Nothing here needs a redesign or a new ESP.
      The only thing that changed is what the email knows about the person opening it.
    </p>
    <div class="note" style="margin-top:24px">
      <p>The dark block at the bottom of each one is BRCG annotation, deliberately styled so it cannot be
      mistaken for part of UVA&rsquo;s template. In the first email, values marked <strong>scenario</strong>
      are a returning-buyer illustration; everything else was read live from the ticketing system.</p>
    </div>
  </div>
  {mail_blocks}
</div>
'''

BODIES = {
    "index.html": index_body,
    "audit.html": audit_body,
    "data.html": data_body,
    "apis.html": apis_body,
    "lifecycle.html": lifecycle_body,
    "emails.html": emails_body,
}

for fn, title, _ in PAGES:
    (ROOT / fn).write_text(shell(fn, title, BODIES[fn]), encoding="utf-8")
    print("wrote", fn)
