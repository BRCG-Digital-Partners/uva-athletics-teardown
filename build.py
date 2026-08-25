#!/usr/bin/env python3
"""Build index.html for the UVA Athletics teardown portal.

Single-page shell, nine panels, same generation as the Rover / IRONMAN portals.
Every figure is read from UVA's own public systems on Aug 25, 2026.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
LOGO = "https://s3.us-west-2.amazonaws.com/pachtml-production/www/virginia/images/logos"

GAMES = [
    ("NC State",       "NCState",       "Sat Aug 29", "3:30 PM",  7549, 65181),
    ("Norfolk State",  "NorfolkState",  "Fri Sep 11", "7:00 PM", 25816, 65180),
    ("Delaware",       "Delaware",      "Sat Sep 26", "TBD",     24943, 65180),
    ("Syracuse",       "Syracuse",      "Sat Oct 10", "TBD",     25048, 65180),
    ("Duke",           "Duke",          "Fri Oct 23", "7:00 PM", 22999, 65180),
    ("California",     "California",    "Sat Nov 14", "TBD",     25388, 65180),
    ("North Carolina", "NorthCarolina", "Sat Nov 21", "TBD",     25136, 65180),
]
UNSOLD = sum(g[4] for g in GAMES)
CAP = sum(g[5] for g in GAMES)
SEASON_PCT = round(100 * (CAP - UNSOLD) / CAP, 1)


def sellout_table():
    rows = ""
    for opp, slug, date, time, av, cap in GAMES:
        p = round(100 * (cap - av) / cap, 1)
        hot = ' class="hot"' if opp == "NC State" else ""
        rows += f'''<tr{hot}>
          <td style="width:34px"><img src="{LOGO}/{slug}.png" alt=""></td>
          <td class="opp">{opp}</td>
          <td class="num">{date} &middot; {time}</td>
          <td style="width:120px"><div class="bar"><i style="width:{p}%"></i></div></td>
          <td class="num" style="text-align:right">{p}%</td>
          <td class="num" style="text-align:right">{av:,}</td>
        </tr>'''
    return f'''<div class="card"><div class="tw"><table class="slt">
      <thead><tr><th></th><th>Opponent</th><th class="num">Kickoff</th><th>Sold</th>
      <th class="num" style="text-align:right">%</th>
      <th class="num" style="text-align:right">Seats left</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
      <p class="note" style="margin-top:14px">Seven home games &middot; {CAP:,} seats &middot;
      {SEASON_PCT}% sold &middot; <b style="color:hsl(var(--foreground))">{UNSOLD:,} still available
      across the season</b>. Read from <code>pac-api/catalog/eventDetailMPT</code>, Aug 25 2026.</p>
    </div>'''


def stat(k, v, s, acc=False):
    return (f'<div class="stat{" acc" if acc else ""}"><div class="k">{k}</div>'
            f'<div class="v">{v}</div><div class="s">{s}</div></div>')


P = {}

P["overview"] = f'''
  <div class="eyebrow">External analysis &middot; nobody asked us for this</div>
  <h2 class="ttl">UVA Athletics runs a great campaign operation<br>on top of no lifecycle at all.</h2>
  <p class="lede">
    Kodie Critzer and Henry Pollard founded BRCG in Charlottesville. Kodie went to UVA. Virginia Athletics is
    the client we would most like to work with, so we built the argument instead of writing a pitch. Everything
    here came from one real subscriber inbox and UVA&rsquo;s own public ticketing systems. No access was
    requested and none was used.
  </p>

  <div class="grid g4 sec">
    {stat("Sends mapped", "78", "Oct 22 2025 to Aug 24 2026. One sender, eight sports, one inbox.")}
    {stat("Unsold, Week 0", "7,549", "Of 65,181 against NC State. Four days out, all six price levels open.", True)}
    {stat("Unsold, season", "156,879", f"{SEASON_PCT}% of the season sold across seven home games.")}
    {stat("Lifecycle triggers", "None", "No welcome, abandon, post-attendance, win-back or re-engagement.", True)}
  </div>

  <div class="sec verdict">
    <div class="eyebrow">The verdict</div>
    <h3>The hard part is already paid for. The easy part is missing.</h3>
    <p>UVA has what most programs never get: a ticketing system that records every order, seat, gate scan,
    transfer and priority-point balance, and a preference centre where fans have already declared their name,
    their zip, their birthday and <strong>which of twelve sports they follow</strong>. All of it is collected.
    All of it is stored. None of it reaches a send.</p>
    <p>What is missing is anything that turns a row in that database into a message. Every one of the 78 emails
    was a manually scheduled broadcast triggered by a calendar date, a game result or an on-sale time.
    <strong>Not one was triggered by something a subscriber did.</strong></p>
    <p>The consequence is specific and measurable this week. Scott Stadium has 7,549 unsold seats for Saturday
    while a campaign called &ldquo;Sell Out Scott&rdquo; runs on. The number is published hourly by UVA&rsquo;s
    own ticketing API to anyone who asks. <strong>The email program has never read it.</strong></p>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">The three moves</div>
      <h3>Ranked by what can ship before the season ends</h3></div>
    <div class="grid g3">
      <div class="card"><span class="tag brand">Days, not weeks</span>
        <h3 style="font-size:16px;margin-top:11px">Gameday and digital parking</h3>
        <p class="note" style="margin-top:9px">Parking went digital in June and has not been mentioned in a
        single email since. Both segments already exist in Paciolan. No new data, no new tooling, one
        template.</p></div>
      <div class="card"><span class="tag brand">Weeks 1&ndash;3</span>
        <h3 style="font-size:16px;margin-top:11px">Turn on the fields you collect</h3>
        <p class="note" style="margin-top:9px">First name into the salutation. Sport preference into routing.
        Zip into drive time. These are Eloqua fields that already hold values.</p></div>
      <div class="card"><span class="tag brand">Weeks 2&ndash;6</span>
        <h3 style="font-size:16px;margin-top:11px">Win-back and real triggers</h3>
        <p class="note" style="margin-top:9px">Lapsed buyers addressed by the seats they actually sat in, then
        post-attendance, first-game welcome and a genuine abandoned-gift flow.</p></div>
    </div>
  </div>

  <div class="sec">
    <div class="banner"><b>Everything here is free and open.</b> No gate, no form, no NDA. If anyone at
    UVA Athletics or the VAF wants the send map, the segment definitions or the email builds, they are yours
    for the asking, whether or not we ever work together. It also means we could have read something wrong.
    If we did, we would genuinely like to know. <a href="mailto:kodie@brcg.co">kodie@brcg.co</a></div>
  </div>
'''

P["inbox"] = '''
  <div class="eyebrow">01 &middot; The inbox</div>
  <h2 class="ttl">78 emails. One sender. Zero segmentation.</h2>
  <p class="lede">
    Pulled from a live UVA Athletics subscriber inbox between Oct 22 2025 and Aug 24 2026. Every send arrives
    from <code>updates@go.virginiasports.com</code> on Oracle Eloqua. Cadence is roughly one every four days,
    across eight sports, to one person, regardless of stated interest.
  </p>

  <div class="grid g4 sec">
    <div class="stat"><div class="k">Total sends</div><div class="v">78</div>
      <div class="s">306 days. 75 from Eloqua, 2 CavFutures, 1 personal Outlook.</div></div>
    <div class="stat"><div class="k">Average gap</div><div class="v">3.9d</div>
      <div class="s">August ran one every 2.3 days, including two on Aug 19 thirteen hours apart.</div></div>
    <div class="stat acc"><div class="k">Personalization</div><div class="v">0%</div>
      <div class="s">First name is required on their own form and appears in no send.</div></div>
    <div class="stat"><div class="k">Sending stacks</div><div class="v">3</div>
      <div class="s">Eloqua, personal Outlook, Mailchimp. Zero integration between them.</div></div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">The finding that reframes everything</div>
      <h3>UVA already collects the segmentation it is not using</h3>
      <p>The public form at <code>app.virginiasports.com/preferences</code>, linked in the footer of all 78
      emails, asks every subscriber for their identity, their interests and their sports. It writes all of it
      to Eloqua. Nothing reads it back.</p></div>
    <div class="grid g3">
      <div class="card"><div class="eyebrow">Identity collected</div>
        <p class="note" style="margin-top:11px;line-height:2">
        <b style="color:hsl(var(--foreground))">First name</b> &mdash; required<br>
        <b style="color:hsl(var(--foreground))">Last name</b> &mdash; required<br>
        Zip / postal code<br>Birthday (MM/DD/YYYY)</p></div>
      <div class="card"><div class="eyebrow">Content categories</div>
        <p class="note" style="margin-top:11px;line-height:2">
        Ticket Information &amp; Special Offers<br>Virginia Athletics Foundation<br>
        Virginia Sports Properties<br>Jeff White &middot; Weekly Hoo Mail<br>
        <b style="color:hsl(var(--foreground))">Game Day Info</b></p></div>
      <div class="card"><div class="eyebrow">Sport preferences stored</div>
        <p class="note" style="margin-top:11px">All Sports, Football, Baseball, Softball, Volleyball,
        Men&rsquo;s &amp; Women&rsquo;s Basketball, Men&rsquo;s &amp; Women&rsquo;s Lacrosse,
        Men&rsquo;s &amp; Women&rsquo;s Soccer, All Other Olympic Sports.</p>
        <p class="note" style="margin-top:10px"><code>hiddenField&ndash;hiddenField12</code></p></div>
    </div>
    <div class="banner warn" style="margin-top:14px"><b>And the one control that does work is the blunt one.</b>
    Every footer reads &ldquo;by unsubscribing you are opting out of ALL email communications from University of
    Virginia Athletics.&rdquo; Granular preferences on the way in, a single global switch on the way out. A donor
    who wants fewer football promos has one lever, and pulling it also ends VAF communications, season-ticket
    renewals and postseason notices.</div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">What the calendar proves</div>
      <h3>Triggers observed, and triggers never observed</h3></div>
    <div class="cmp">
      <div class="col">
        <span class="tag neutral">Observed</span>
        <h3>What fires a send today</h3>
        <ul>
          <li>A game result</li>
          <li>A ticket on-sale date</li>
          <li>A schedule release</li>
          <li>A coach hire</li>
          <li>A date on the marketing calendar</li>
        </ul>
      </div>
      <div class="col next">
        <span class="tag brand">Not observed</span>
        <h3>What never fires a send</h3>
        <ul>
          <li>Signing up</li>
          <li>Abandoning a cart or a gift</li>
          <li>Walking through the gate</li>
          <li>Failing to renew</li>
          <li>Listing or transferring a ticket</li>
          <li>Crossing a priority-points threshold</li>
        </ul>
      </div>
    </div>
  </div>
'''

P["week0"] = f'''
  <div class="eyebrow">02 &middot; Week 0</div>
  <h2 class="ttl">22 sends into kickoff.<br>The best window of the year.</h2>
  <p class="lede">
    Virginia opens the 2026 season at home against NC State on Saturday Aug 29, a Week 0 kickoff with no
    competition for attention. Between June 1 and August 24 the program sent 22 emails into that window, ten
    of them in August alone. This is the highest-intent selling period on the calendar.
  </p>

  <div class="grid g4 sec">
    {stat("Sends, Jun 1 to Aug 24", "22", "84 days, one every 3.8 days. No gap longer than 11 days.")}
    {stat("Sends in August", "10", "23 days, one every 2.3 days. Two on Aug 19, thirteen hours apart.")}
    {stat("Home games on sale", "7 of 7", "Verified on the live Paciolan store. NC State included.", True)}
    {stat("Emails using known data", "0", "No first name, no sport, no zip, no purchase history.", True)}
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Credit where it is due</div>
      <h3>This is a functioning campaign operation and the offer work is good</h3></div>
    <div class="grid g3">
      <div class="card"><p class="note"><b style="color:hsl(var(--foreground))">Real price laddering.</b>
        Mini plans from $99, Family Four Pack from $25 a seat, $50 lower-endzone pairs, 25% and 30% flash
        windows.</p></div>
      <div class="card"><p class="note"><b style="color:hsl(var(--foreground))">Partner revenue delivered.</b>
        REVELxp tailgates, a Papa John&rsquo;s tie-in and Virginia Sports Properties inventory all
        monetised.</p></div>
      <div class="card"><p class="note"><b style="color:hsl(var(--foreground))">Shipping on deadline.</b>
        22 sends in 84 days with no missed week. That is the hard part, and it is already solved.</p></div>
    </div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Live inventory</div>
      <h3>The whole season, by how full it is</h3>
      <p>Saturday is the tightest ticket on the schedule by a wide margin. Every other home game is sitting
      around 61%.</p></div>
    {sellout_table()}
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">The gaps</div>
      <h3>Seven things the run-up left on the table</h3>
      <p>None of these require a new platform, a data purchase or a migration.</p></div>
    <div class="card"><div class="tw"><table>
      <thead><tr><th style="width:104px">Gap</th><th style="width:42%">What was missing</th>
        <th>The send that should have gone</th></tr></thead>
      <tbody>
        <tr><td><span class="tag bad">Parking</span></td>
          <td>Parking went digital on Jun 24. Hangtags gone for football, both basketballs and baseball.
          Announced as a news post, 66 days before kickoff. <strong>Never mentioned in any of the 22
          emails.</strong></td>
          <td>Permit holders only, T&minus;21 and T&minus;5. Screenshot walkthrough, app deep link, transfer
          instructions. The highest-volume support call UVA is about to receive, and entirely preventable.</td></tr>
        <tr><td><span class="tag bad">Gameday</span></td>
          <td>The preference centre offers a &ldquo;Game Day Info&rdquo; category and subscribers opt into it.
          Four days out, the last send was a tailgate upsell.</td>
          <td>Thursday before each home game to ticket holders. Kickoff, gates, bag policy, digital ticket and
          parking retrieval, weather. Zero sell.</td></tr>
        <tr><td><span class="tag bad">Win-back</span></td>
          <td>A 2024 season-ticket holder who did not renew received the identical 22 sends as someone who has
          never purchased. Paciolan knows the difference.</td>
          <td>Name the real section and row. Same-or-better seat for Week 0. Proven intent is the cheapest
          conversion in the file.</td></tr>
        <tr><td><span class="tag bad">Sport</span></td>
          <td>Men&rsquo;s basketball schedule news went to the whole file on Aug 20, nine days before a football
          home opener. Twelve sport preferences sit unused in Eloqua.</td>
          <td>One trigger, split on the sport-affinity field already on the record. A segmentation build, not a
          data build.</td></tr>
        <tr><td><span class="tag bad">Geography</span></td>
          <td>Zip is collected. A fan in Charlottesville and one in Northern Virginia got the same push for a
          3:30 Saturday kickoff.</td>
          <td>Drive-time framing by radius. Inside 30 miles, 60 to 120, and beyond.</td></tr>
        <tr><td><span class="tag bad">Identity</span></td>
          <td>First name is required on the subscription form and appears in zero sends. The Aug 18 letter from
          the Director of Athletics opens &ldquo;Wahoo Nation.&rdquo;</td>
          <td>A one-line template change with no data work behind it. The lowest-effort item on this list.</td></tr>
        <tr><td><span class="tag bad">Support</span></td>
          <td>The Aug 24 game-week email routes questions to a ticket office open Monday to Friday, 9 to 5.
          The game is Saturday.</td>
          <td>Self-serve block with app deep links, plus a gameday SMS line. Deflect the call rather than route
          it somewhere closed.</td></tr>
      </tbody></table></div></div>
  </div>
'''

P["data"] = '''
  <div class="eyebrow">03 &middot; Architecture</div>
  <h2 class="ttl">Three systems that hold everything<br>and one that sends everything.</h2>
  <p class="lede">
    The fan email program runs on Oracle Eloqua via WMT Digital. VAF major-gift outreach happens one to one from
    personal Outlook. CavFutures NIL is on Mailchimp. Paciolan sits underneath all of it holding the
    transactional truth. The four do not talk.
  </p>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Today</div><h3>Every arrow that should exist is missing</h3></div>
    <div class="card"><div class="tw"><table>
      <thead><tr><th style="width:118px">State</th><th style="width:150px">System</th>
        <th>What it holds, and what it does not do with it</th></tr></thead>
      <tbody>
        <tr><td><span class="tag good">Live</span><div style="font-size:12.5px;margin-top:7px">Ticketing</div></td>
          <td><strong>Paciolan</strong></td>
          <td>Orders, seats, gate scans, transfers, resale listings, priority points, giving level, parking
          SKUs, membership tier. The richest behavioural data in the building.
          <code>org VIRGINIA</code> <code>account 772</code></td></tr>
        <tr><td><span class="tag good">Live</span><div style="font-size:12.5px;margin-top:7px">Email</div></td>
          <td><strong>Oracle Eloqua</strong></td>
          <td>First name, last name, zip, birthday, six content categories, twelve sport preferences. Collected
          on the public preference form, written to hidden fields, never merged into a send. Run by WMT
          Digital.</td></tr>
        <tr><td><span class="tag bad">Silo</span><div style="font-size:12.5px;margin-top:7px">Major gifts</div></td>
          <td><strong>Personal Outlook</strong></td>
          <td>One-to-one VAF outreach from a personal mailbox. No record reaches the email platform, so a
          major-gift prospect can receive a mass solicitation the same week.</td></tr>
        <tr><td><span class="tag bad">Silo</span><div style="font-size:12.5px;margin-top:7px">NIL</div></td>
          <td><strong>Mailchimp</strong></td>
          <td>CavFutures on a separate list with separate suppression. Invisible to both of the others.</td></tr>
      </tbody></table></div></div>
    <div class="banner" style="margin-top:14px"><b>One exception worth crediting.</b> Ticketing and fundraising
    already meet at checkout. The NC State event record carries an <code>OFFERS_AND_ROUNDUPS</code> block with a
    VAF donation at $250 / $100 / $50 / $25 / $10 plus a round-up. The silo this teardown describes is an email
    silo, not a systems silo.</div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">What we would build</div>
      <h3>A lifecycle layer that replaces nothing</h3>
      <p>Eloqua stays. Paciolan stays. WMT stays. A thin layer reads behaviour, resolves identity, and lets a
      send be entered by something a fan did rather than a date on a calendar.</p></div>
    <div class="grid g3">
      <div class="card"><span class="tag good">Source</span>
        <h3 style="font-size:16px;margin-top:11px">Paciolan + Eloqua</h3>
        <p class="note" style="margin-top:9px">Order history, gate scans, points, transfers, live inventory,
        plus the preference-centre fields already captured against each contact.</p></div>
      <div class="card"><span class="tag brand">New</span>
        <h3 style="font-size:16px;margin-top:11px">Identity and event layer</h3>
        <p class="note" style="margin-top:9px">Reconcile the Paciolan patron ID against the Eloqua contact.
        Emit behavioural events: purchased, scanned, lapsed, listed, upgraded, abandoned.</p></div>
      <div class="card"><span class="tag good">Send</span>
        <h3 style="font-size:16px;margin-top:11px">Eloqua, unchanged</h3>
        <p class="note" style="margin-top:9px">Same platform, same templates, same agency. The only difference
        is what can start a send.</p></div>
    </div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">The record</div><h3>Four layers already on a patron</h3></div>
    <div class="card"><div class="tw"><table>
      <thead><tr><th style="width:22%">Layer</th><th style="width:36%">What it holds</th>
        <th>What it unlocks</th><th style="width:118px">State</th></tr></thead>
      <tbody>
        <tr><td><strong>Identity and location</strong></td>
          <td>Account ID, name, email, mailing address and zip, phone, household links.</td>
          <td>First-name merge, drive-time segmentation, household de-duplication.</td>
          <td><span class="tag good">Collected</span></td></tr>
        <tr><td><strong>Transactions</strong></td>
          <td>Every order by event: section, row, seat, price level, promo used, add-ons, purchase date
          relative to the game, channel.</td>
          <td>Win-back on real seats, partial-plan completion, tier upgrade paths.</td>
          <td><span class="tag good">Collected</span></td></tr>
        <tr><td><strong>Access and behaviour</strong></td>
          <td>Barcode scans at the gate, digital transfers, resale listings, My Account logins, app installs.</td>
          <td>Post-attendance follow-up, no-show recovery, churn detection before renewal.</td>
          <td><span class="tag good">Collected</span></td></tr>
        <tr><td><strong>Giving and priority</strong></td>
          <td>Priority-points balance, giving level, VAF tier, seat and parking eligibility, pledge status.</td>
          <td>Points-threshold nudges, benefit-gated offers, donor onboarding.</td>
          <td><span class="tag warn">Hidden</span></td></tr>
      </tbody></table></div></div>
    <div class="banner warn" style="margin-top:14px"><b>The priority-points case is the sharpest one.</b>
    The patron endpoint returns <code>custPriPoints</code>, <code>donPriPoints</code>,
    <code>orderPriPtsTotal</code> and <code>priPtsTotal</code> on every account load. But UVA&rsquo;s live config
    has <code>myprioritypoints.enabled = false</code> and <code>newmygivinghistory.enabled = false</code>, so the
    fan cannot see the balance in My Account either. It is computed continuously and shown to nobody.</div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Platform capability</div>
      <h3>Switched on and unused, or switched off entirely</h3>
      <p>Read from the public config endpoint. These are features UVA already pays for.</p></div>
    <div class="cmp">
      <div class="col">
        <span class="tag good">Enabled</span>
        <h3>Never mentioned in an email</h3>
        <ul>
          <li><code>findPromotions</code> + <code>promos</code> &mdash; a targeted promotion engine</li>
          <li><code>donationoffers</code> + <code>donationpages</code> &mdash; giving inside the ticket cart</li>
          <li><code>addons</code>, <code>combos</code> &mdash; parking and chairbacks bundled at purchase</li>
          <li><code>students</code> with Shibboleth SSO &mdash; student ticketing</li>
        </ul>
      </div>
      <div class="col next">
        <span class="tag warn">Off, or configured onto nothing</span>
        <h3>Capability paid for, not used</h3>
        <ul>
          <li><code>myprioritypoints</code>, <code>newmygivinghistory</code> &mdash; both false</li>
          <li><code>billplans</code> &mdash; enabled, but <code>HAS_BILL_PLANS</code> false on all ten upcoming events</li>
          <li><code>maxOrderHistoryMonthRange</code> &mdash; 12 months, shorter than the win-back window</li>
          <li><code>displayallfees</code> &mdash; false, so fees appear late in the flow</li>
        </ul>
      </div>
    </div>
  </div>
'''

P["apis"] = '''
  <div class="eyebrow">04 &middot; API surface</div>
  <h2 class="ttl">The endpoints that already answer<br>every question a send would ask.</h2>
  <p class="lede">
    Paciolan&rsquo;s developer documentation is partner-gated. Everything below instead comes from UVA&rsquo;s own
    live implementation: the public catalog endpoints, and a network capture of one ordinary logged-in fan
    session. The route names and field names are the real ones. No personal data appears anywhere here.
  </p>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">The routes</div><h3>Eight calls the site already makes</h3></div>
    <div class="card"><div class="tw"><table>
      <thead><tr><th style="width:38%">Endpoint</th><th>Returns</th><th style="width:24%">Drives</th></tr></thead>
      <tbody>
        <tr><td><code>pac-api/catalog/eventDetailMPT/{season}/{event}</code></td>
          <td>Capacity, unsold count, sold-out flag, promo flag, on-sale timestamp, donation offers.</td>
          <td>Inventory-aware sends. Scarcity versus discount.</td></tr>
        <tr><td><code>pac-api/seat-availability/event-id/{id}/pricelevel</code></td>
          <td>Availability by price tier, hold codes, platinum markers.</td>
          <td>Tier-targeted offers, upgrade paths.</td></tr>
        <tr><td><code>pac-api/orderhistory</code></td>
          <td>Purchase history by event.</td><td>Lapsed win-back, partial-plan completion.</td></tr>
        <tr><td><code>pac-api/orderhistory/pendingTransfers</code></td>
          <td>Tickets transferred but not yet accepted.</td><td>Churn signal, guest capture.</td></tr>
        <tr><td><code>pac-api/order/ballena/upgrades</code></td>
          <td>Upgrade offers available against seats already owned.</td>
          <td>A personalised, revenue-positive email nobody sends.</td></tr>
        <tr><td><code>pac-api/memberships</code></td>
          <td>Membership tier and status.</td><td>Benefit gating, renewal timing.</td></tr>
        <tr><td><code>app/ws/patron/{id}/myAccount</code></td>
          <td>Priority points, student flag, exchange / transfer / return rights.</td>
          <td>Points-threshold nudges, eligibility-aware offers.</td></tr>
        <tr><td><code>pac-api/consumer/gql</code></td>
          <td>GraphQL. Every upcoming event across every sport in one call.</td>
          <td>Cross-sport pull, dynamic schedule modules.</td></tr>
      </tbody></table></div></div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Real payload</div><h3>Event inventory</h3>
      <p>Trimmed from the live NC State response. One object carries the seat count, the theme, the on-sale
      time and the entire donation ladder.</p></div>
    <div class="card">
      <span class="tag brand">GET</span>
      <div class="code-frame" style="margin-top:11px">pac-api/catalog/eventDetailMPT/F26/F01</div>
      <div class="code-frame" style="margin-top:12px;word-break:normal">{<br>
      &nbsp;&nbsp;"ITEMCD": "F01",&nbsp;&nbsp;"EVENTNAME": "NC State",<br>
      &nbsp;&nbsp;"FAC_TITLE": "Scott Stadium",<br>
      &nbsp;&nbsp;"EVENTDTFAC": "2026-08-29T15:30:00.000Z",<br>
      &nbsp;&nbsp;"SALEFROMDT": "2026-07-01T09:00:00.000Z",<br>
      &nbsp;&nbsp;"SOLD_OUT": false,&nbsp;&nbsp;"HASPROMO": true,<br>
      &nbsp;&nbsp;<b style="color:hsl(var(--im-fg))">"AVAILABLE": 7549,</b>&nbsp;&nbsp;&nbsp;&nbsp;&#47;&#47; the number no email reads<br>
      &nbsp;&nbsp;<b style="color:hsl(var(--im-fg))">"TOTALCAPACITY": 65181,</b><br>
      &nbsp;&nbsp;"HAS_BILL_PLANS": false,<br>
      &nbsp;&nbsp;"EVENT_MESSAGE": "Paint the Town ORANGE! Fan-First discounts...",<br>
      &nbsp;&nbsp;"OFFERS_AND_ROUNDUPS": [{ "CATEGORY": "DO",<br>
      &nbsp;&nbsp;&nbsp;&nbsp;"OFFER_DETAILS": { "ITEMNAME": "Virginia Athletics Foundation Donation",<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ALLOWCUSTOMERAMOUNT": "Y",<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"AMOUNTS": [25000, 10000, 5000, 2500, 1000] } }]&nbsp;&nbsp;&#47;&#47; cents<br>
      }</div>
    </div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Real payload</div><h3>Patron record</h3>
      <p>Shape only, values removed. Note the four points fields, all populated on every account load, none of
      them surfaced to the fan or to a send.</p></div>
    <div class="card">
      <span class="tag brand">GET</span>
      <div class="code-frame" style="margin-top:11px">app/ws/patron/{id}/myAccount</div>
      <div class="code-frame" style="margin-top:12px;word-break:normal">{ "value": {<br>
      &nbsp;&nbsp;<b style="color:hsl(var(--im-fg))">"custPriPoints"</b>,&nbsp;&nbsp;&nbsp;&nbsp;&#47;&#47; customer priority points<br>
      &nbsp;&nbsp;<b style="color:hsl(var(--im-fg))">"donPriPoints"</b>,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#47;&#47; donor priority points<br>
      &nbsp;&nbsp;<b style="color:hsl(var(--im-fg))">"orderPriPtsTotal"</b>,&nbsp;&#47;&#47; points from orders<br>
      &nbsp;&nbsp;<b style="color:hsl(var(--im-fg))">"priPtsTotal"</b>,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#47;&#47; combined total<br>
      &nbsp;&nbsp;"patronVo": { "fname", "lname", "patronId", "cstmType", "isStudent",<br>
      &nbsp;&nbsp;&nbsp;&nbsp;"exchfl", "transferfl", "returnfl" },&nbsp;&nbsp;&#47;&#47; entitlements<br>
      &nbsp;&nbsp;"relatedSites": [ &#47;* seat + parking selection portals *&#47; ]<br>
      } }</div>
    </div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Data template</div><h3>The merge-field contract</h3>
      <p>What a lifecycle layer would expose to the template. Every field below exists today. None require new
      data collection.</p></div>
    <div class="card"><div class="tw"><table>
      <thead><tr><th style="width:22%">Field</th><th style="width:28%">Source</th><th>Example</th>
        <th style="width:104px">In use</th></tr></thead>
      <tbody>
        <tr><td><code>first_name</code></td><td>Eloqua preference form</td><td class="num">Kodie</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>sport_affinity[]</code></td><td>Eloqua hiddenField&ndash;12</td><td class="num">["football","mbb"]</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>drive_time</code></td><td>Eloqua zip + patron address</td><td class="num">20 min</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>last_seat</code></td><td>pac-api/orderhistory</td><td class="num">117 / K / 9-10</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>games_attended</code></td><td>Barcode scans</td><td class="num">4 of 7</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>priority_points</code></td><td>app/ws/patron myAccount</td><td class="num">84</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>upgrade_offer</code></td><td>order/ballena/upgrades</td><td class="num">Preferred, +$34</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>event.available</code></td><td>catalog/eventDetailMPT</td><td class="num">7549</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>event.pct_sold</code></td><td>Derived</td><td class="num">88.4</td><td><span class="tag bad">No</span></td></tr>
        <tr><td><code>parking_sku</code></td><td>Order add-ons</td><td class="num">null</td><td><span class="tag bad">No</span></td></tr>
      </tbody></table></div></div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Data template</div><h3>A worked trigger binding</h3>
      <p>The same 600px Eloqua template, entered by a behaviour instead of a calendar date.</p></div>
    <div class="card">
      <div class="code-frame" style="word-break:normal">
      <span style="color:hsl(var(--muted-foreground)/.7)"># entry</span><br>
      when:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;orderhistory.last_order_season in ["F24", "F25"]<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and orderhistory.orders_this_season == 0<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and event.days_until between 3 and 10<br><br>
      <span style="color:hsl(var(--muted-foreground)/.7)"># suppression</span><br>
      unless:&nbsp;&nbsp;&nbsp;&nbsp;contact.opted_out<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;or orderhistory.has_order(event.id)<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;or sends.last_7d &gt;= 2<br><br>
      <span style="color:hsl(var(--muted-foreground)/.7)"># payload</span><br>
      merge:<br>
      &nbsp;&nbsp;first_name:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patron.fname<br>
      &nbsp;&nbsp;last_seat:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;orderhistory.last.section + "/" + row<br>
      &nbsp;&nbsp;games_attended: scans.count(season="F25")<br>
      &nbsp;&nbsp;points:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;patron.priPtsTotal<br>
      &nbsp;&nbsp;seats_left:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;event.AVAILABLE<br>
      &nbsp;&nbsp;pct_sold:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;100 * (event.TOTALCAPACITY - event.AVAILABLE) / event.TOTALCAPACITY<br>
      &nbsp;&nbsp;upgrade:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;upgrades.best(patron.id, event.id)<br><br>
      <span style="color:hsl(var(--muted-foreground)/.7)"># measure</span><br>
      against:&nbsp;&nbsp;&nbsp;holdout 10%, orders attributed 7-day click / 1-day view
      </div>
    </div>
  </div>
'''

P["lifecycle"] = '''
  <div class="eyebrow">05 &middot; Lifecycle</div>
  <h2 class="ttl">Eight sends the ticketing system<br>could already be firing.</h2>
  <p class="lede">
    Each one names the field that drives it. None require new data collection, a platform migration or leaving
    Eloqua. Seven home games remain after Week 0, which is seven live tests rather than a planning cycle.
  </p>

  <div class="sec">
    <div class="card"><div class="tw"><table>
      <thead><tr><th style="width:104px">Trigger</th><th style="width:30%">Signal</th>
        <th>The send</th><th style="width:124px">Timing</th></tr></thead>
      <tbody>
        <tr><td><span class="tag brand">Proximity</span></td>
          <td><code>zip</code> + <code>orders_lifetime = 0</code> + <code>opens &gt; 25%</code></td>
          <td><strong>&ldquo;You&rsquo;re 20 minutes from kickoff.&rdquo;</strong> One offer at the entry price,
          plus the parking instruction.</td><td class="num">T&minus;5 days</td></tr>
        <tr><td><span class="tag brand">Abandon</span></td>
          <td>evenue checkout session with no completed order</td>
          <td><strong>Wire the existing creative to the actual event.</strong> UVA already built this. The
          Aug 19 &ldquo;Finish Making Your Impact&rdquo; email exists and looks right; it just went out as a
          batch to people with no abandoned gift.</td><td class="num">T+2h, T+24h</td></tr>
        <tr><td><span class="tag brand">Attendance</span></td>
          <td><code>barcode_scan</code> on <code>first_order</code></td>
          <td><strong>&ldquo;You were 1 of 64,217.&rdquo;</strong> Multi-game step-up to attendees, a separate
          quieter note to no-shows.</td><td class="num">Whistle +90m</td></tr>
        <tr><td><span class="tag brand">Lapsed</span></td>
          <td><code>last_order_season</code> in F24/F25, no F26 order</td>
          <td><strong>&ldquo;Section 117 is still open.&rdquo;</strong> Name the real seats, offer
          same-or-better.</td><td class="num">T&minus;10 days</td></tr>
        <tr><td><span class="tag brand">Partial</span></td>
          <td><code>orders_this_season</code> vs <code>home_games_total</code></td>
          <td><strong>Complete the season, priced at the delta.</strong> Show what they own, show the gap,
          charge the difference.</td><td class="num">After game two</td></tr>
        <tr><td><span class="tag brand">Parking</span></td>
          <td><code>has_ticket = true</code> AND <code>parking_sku = null</code></td>
          <td><strong>Attach the pass and explain the new system.</strong> A revenue line and a support-cost
          line at the same time.</td><td class="num">T&minus;10, T&minus;3</td></tr>
        <tr><td><span class="tag brand">Points</span></td>
          <td><code>priPtsTotal</code> against the next tier</td>
          <td><strong>&ldquo;You&rsquo;re 41 points from priority parking.&rdquo;</strong> A progress bar and
          the exact gift that closes it.</td><td class="num">Quarterly</td></tr>
        <tr><td><span class="tag brand">Resale</span></td>
          <td><code>pendingTransfers</code> + secondary listings</td>
          <td><strong>Two branches.</strong> One game listed: help them sell it. Four or more: a renewal at
          risk, route it to a human at the VAF.</td><td class="num">On listing</td></tr>
      </tbody></table></div></div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">A worked journey</div>
      <h3>One fan, one season, entered by behaviour</h3></div>
    <div class="card flow">
      <div class="st"><div class="when">Week &minus;1</div><div class="what">
        <b>Win-back</b><span>Bought in 2025, nothing yet in 2026. The email names Section 117 and offers the
        same seats at last year&rsquo;s price. Entry: <code>orderhistory</code>.</span></div></div>
      <div class="st"><div class="when">Purchase +1h</div><div class="what">
        <b>Confirmation that sells nothing</b><span>Seats, kickoff, how digital parking works now, what to
        bring. Suppresses every promo for 48 hours.</span></div></div>
      <div class="st"><div class="when">Thursday</div><div class="what">
        <b>Gameday logistics</b><span>Gates, bag policy, ticket and parking retrieval, weather, traffic. Zero
        sell. Entry: holds a ticket for a home game in 48 hours.</span></div></div>
      <div class="st"><div class="when">Whistle +90m</div><div class="what">
        <b>Post-attendance</b><span>Scanned in, so the recap is true for them. Attendance count, next home
        game, upgrade offer if one exists. Entry: <code>barcode_scan</code>.</span></div></div>
      <div class="st"><div class="when">Game +3d</div><div class="what">
        <b>Points and progress</b><span>Balance after this purchase and distance to the next benefit tier. The
        number Paciolan already computes and nobody sees.</span></div></div>
      <div class="st"><div class="when">Season end</div><div class="what">
        <b>Renewal, priced honestly</b><span>Games attended, what they spent one at a time, what the season
        plan would have cost. Entry: final home game scanned.</span></div></div>
    </div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Operating rules</div>
      <h3>How to run it so the numbers mean something</h3></div>
    <div class="grid g3">
      <div class="card"><span class="tag brand">Holdout</span>
        <h3 style="font-size:16px;margin-top:11px">10% of every trigger</h3>
        <p class="note" style="margin-top:9px">Withhold a random tenth from each behavioural send. Without it,
        incrementality is a guess and every win gets attributed to whichever email arrived last.</p></div>
      <div class="card"><span class="tag brand">Governance</span>
        <h3 style="font-size:16px;margin-top:11px">A frequency cap across teams</h3>
        <p class="note" style="margin-top:9px">On Aug 19 two emails went out thirteen hours apart from two
        different teams. A shared cap and a priority order stops that without a meeting.</p></div>
      <div class="card"><span class="tag brand">Suppression</span>
        <h3 style="font-size:16px;margin-top:11px">Behaviour beats calendar</h3>
        <p class="note" style="margin-top:9px">Anyone in a triggered flow drops out of the broadcast for its
        duration. Buyers stop seeing acquisition offers the moment they buy.</p></div>
    </div>
  </div>
'''

P["emails"] = '''
  <div class="eyebrow">06 &middot; Email library</div>
  <h2 class="ttl">UVA&rsquo;s own template. Five better sends.</h2>
  <p class="lede">
    Every mockup is built on UVA&rsquo;s real Eloqua template, not an interpretation of it. Same 600px table,
    same Arial, same navy and orange, same 2px buttons, and the live header, nav and footer images pulled
    straight from <code>img.virginiasports.com</code>. Nothing here needs a redesign or a new ESP. The only
    thing that changed is what the email knows about the person opening it.
  </p>
  <div class="banner" style="margin-top:22px"><b>The dark block at the bottom of each email is BRCG
  annotation</b>, deliberately styled so it cannot be mistaken for part of UVA&rsquo;s template.</div>
  <div class="sec">
    <div id="mstrip"></div>
    <div id="mwrap"></div>
  </div>
'''

P["roadmap"] = '''
  <div class="eyebrow">07 &middot; Roadmap</div>
  <h2 class="ttl">Three pilots, ranked by<br>what could ship before the season ends.</h2>
  <p class="lede">
    There are seven home games left after Week 0. That is seven live tests, not a planning cycle. Everything
    below runs on the current stack. Eloqua stays, Paciolan stays, nothing migrates. The order is by
    time-to-value, not by size.
  </p>

  <div class="sec grid" style="gap:12px">
    <div class="card">
      <div style="display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap">
        <div style="display:flex;gap:11px;align-items:center;flex-wrap:wrap">
          <span class="tag brand">Pilot 1</span>
          <h3 style="font-size:16px">Gameday and digital parking</h3></div>
        <span class="tag neutral">Days, not weeks</span></div>
      <p class="note" style="margin-top:12px;max-width:92ch">The Thursday-before logistics email to ticket
      holders, and the digital-parking walkthrough to permit holders. Both segments already exist in Paciolan.
      No new data, no new tooling, one template. Deflects support volume on the first Saturday of a brand-new
      parking system. <b style="color:hsl(var(--foreground))">Lowest effort, fastest payback.</b></p>
    </div>
    <div class="card">
      <div style="display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap">
        <div style="display:flex;gap:11px;align-items:center;flex-wrap:wrap">
          <span class="tag brand">Pilot 2</span>
          <h3 style="font-size:16px">Turn on the fields you already collect</h3></div>
        <span class="tag neutral">Weeks 1&ndash;3</span></div>
      <p class="note" style="margin-top:12px;max-width:92ch">First name into the salutation. Sport preference
      into routing, so basketball news stops landing on football-only fans. Zip into drive-time framing. These
      are Eloqua fields that already hold values, so this is a template and segmentation build, not a data
      project. <b style="color:hsl(var(--foreground))">Highest leverage per hour.</b></p>
    </div>
    <div class="card">
      <div style="display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap">
        <div style="display:flex;gap:11px;align-items:center;flex-wrap:wrap">
          <span class="tag brand">Pilot 3</span>
          <h3 style="font-size:16px">Win-back and the real behavioural triggers</h3></div>
        <span class="tag neutral">Weeks 2&ndash;6, all season</span></div>
      <p class="note" style="margin-top:12px;max-width:92ch">2024 and 2025 purchasers with no 2026 order,
      addressed by the seats they actually sat in. Then the genuine behavioural triggers the program has never
      had: post-attendance follow-up, first-game welcome, and a real abandoned-gift flow for the VAF, one that
      fires on an actual abandoned gift. <b style="color:hsl(var(--foreground))">Biggest revenue line.</b></p>
    </div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">What we would need</div>
      <h3>Light access, no engineering work, no platform changes</h3></div>
    <div class="grid g2">
      <div class="card"><p class="note">
        <b style="color:hsl(var(--foreground))">Eloqua</b> &mdash; read-only campaign and list views<br>
        <b style="color:hsl(var(--foreground))">Paciolan</b> &mdash; ticketing and donor reporting read access<br>
        <b style="color:hsl(var(--foreground))">VAF reporting</b> &mdash; gift records, last 24 months is enough</p></div>
      <div class="card"><p class="note">
        <b style="color:hsl(var(--foreground))">~60 min</b> with whoever owns the email program<br>
        <b style="color:hsl(var(--foreground))">~60 min</b> with VAF annual giving ops<br>
        <b style="color:hsl(var(--foreground))">~30 min</b> with the Virginia Sports app owner</p></div>
    </div>
  </div>

  <div class="sec verdict">
    <div class="eyebrow">Why us</div>
    <h3>We would love to work with you.</h3>
    <p>That is the honest reason this exists. Kodie grew up in Charlottesville and went to UVA. Henry helped
    build BRCG here. Virginia Athletics is a huge part of both of our lives, and it is the client we would most
    like to have. Nobody asked us for this and there is no invoice behind it.</p>
    <p>Everything on this site is free and open. If anyone at UVA Athletics or the VAF wants the send map, the
    segment definitions or the email builds, they are yours for the asking whether or not we ever work
    together. It all came from a public inbox and public pages, which also means we could have read something
    wrong. If we did, we would genuinely like to know.</p>
    <p><strong><a href="mailto:kodie@brcg.co">kodie@brcg.co</a></strong></p>
  </div>
'''

P["method"] = '''
  <div class="eyebrow">08 &middot; Method &amp; sources</div>
  <h2 class="ttl">Where every number came from.</h2>
  <p class="lede">
    This teardown was assembled entirely from outside. No access was requested and none was used. Below is
    exactly which source produced which figure, and which values are illustrative rather than live.
  </p>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Sources</div><h3>Five, all public</h3></div>
    <ol class="steps card">
      <li><b>A real subscriber inbox.</b> 78 sends from <code>updates@go.virginiasports.com</code> between
      Oct 22 2025 and Aug 24 2026, received by one ordinary fan who opted in through the public form.</li>
      <li><b>The public Paciolan catalog</b> on <code>virginiasports.evenue.net</code>, org
      <code>VIRGINIA</code>, account <code>772</code>. Per-game inventory, price levels, the chairback price
      and the donation ladder. Read Aug 25 2026.</li>
      <li><b>A network capture of one ordinary logged-in fan session</b> on the NC State ticket page. This is
      where the endpoint names and field names come from. No personal data from that session appears anywhere
      on this site.</li>
      <li><b>The public preference centre</b> at <code>app.virginiasports.com/preferences</code>, where the
      twelve sport preferences and the required name fields were confirmed.</li>
      <li><b>virginiasports.com news</b>, including the Jun 24 announcement that parking is going digital.</li>
    </ol>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Honesty</div><h3>Live versus illustrative</h3></div>
    <div class="cmp">
      <div class="col">
        <span class="tag good">Live</span>
        <h3>Read from UVA&rsquo;s systems</h3>
        <ul>
          <li>Every per-game seat count and sellout percentage</li>
          <li>Capacity, sold-out flag, promo flag, on-sale timestamps</li>
          <li>The $12 chairback price and the VAF donation ladder</li>
          <li>The six named price levels and two price types</li>
          <li>Every endpoint and field name quoted</li>
          <li>Opponent logos, email header, nav and footer images</li>
          <li>All 78 subject lines, dates and send times</li>
        </ul>
      </div>
      <div class="col next">
        <span class="tag warn">Illustrative</span>
        <h3>Scenario, and labelled as such</h3>
        <ul>
          <li>The seat history, attendance record, points balance and upgrade price in the NC State email</li>
          <li>The names and details in the four other email mockups</li>
          <li>Any revenue framing, modelled from public benchmarks rather than UVA&rsquo;s actuals</li>
        </ul>
        <p class="note" style="margin-top:14px">Each scenario field maps to a Paciolan field that would populate
        it in production. The account this was built from has never actually purchased a ticket.</p>
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="banner warn"><b>One thing deliberately excluded.</b> During this work we found a
    security-relevant detail in a vendor&rsquo;s platform configuration, not UVA&rsquo;s. It has been withheld
    from this site and is being handled by responsible disclosure to the vendor first. It is not a UVA finding
    and nothing about it is published here.</div>
  </div>

  <div class="sec">
    <div class="sec-h"><div class="eyebrow">Corrections</div><h3>Tell us if we got something wrong</h3>
      <p>All of this was read from outside, which means it is possible we have misread something. If any of it
      is wrong we would genuinely like to know, and we will correct it.
      <a href="mailto:kodie@brcg.co">kodie@brcg.co</a></p></div>
  </div>
'''

PANELS = "".join(
    f'<section class="panel{" on" if k == "overview" else ""}" id="p-{k}">{v}</section>'
    for k, v in P.items())

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UVA Athletics &times; BRCG &mdash; CRM &amp; Lifecycle Teardown</title>
<meta name="description" content="An unsolicited CRM and lifecycle teardown of the UVA Athletics fan email program, built from a real subscriber inbox and public ticketing data by BRCG in Charlottesville.">
<meta property="og:title" content="UVA Athletics &times; BRCG &mdash; CRM &amp; Lifecycle Teardown">
<meta property="og:description" content="78 sends in 10 months of great campaign ops with no lifecycle underneath. 7,549 seats unsold for Week 0. Every figure read from UVA's own systems.">
<meta name="robots" content="index,follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;900&family=Roboto:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<button id="mtoggle" aria-expanded="false" aria-label="Toggle navigation">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
    <path d="M3 6h18M3 12h18M3 18h18"/></svg>
</button>

<div id="app">
  <aside id="side">
    <div class="lockup">
      <img class="b" src="assets/brcg-logo-white.png" alt="BRCG">
      <span class="x"></span>
      <span style="font-family:'Public Sans',sans-serif;font-weight:900;font-size:13.5px;letter-spacing:-.01em;color:hsl(var(--im-fg))">VIRGINIA</span>
    </div>
    <div class="subtitle">CRM &amp; lifecycle teardown</div>
    <nav id="nav"></nav>
    <div class="foot">
      <span class="live-dot"></span>Public sources only &middot; read-only<br>
      <span id="upd"></span>
    </div>
  </aside>

  <main>
    {PANELS}
  </main>
</div>

<script src="data.js"></script>
<script src="app.js"></script>
</body>
</html>'''

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print("wrote index.html")
print(f"season: {SEASON_PCT}% sold, {UNSOLD:,} unsold of {CAP:,}")
