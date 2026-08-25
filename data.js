/* UVA Athletics × BRCG portal — content data.
   Every figure below was read from UVA's own public systems on Aug 25, 2026.
   See the Method panel for exactly which source produced which number. */

window.META = { updated: '25 August 2026' };

/* Live per-game inventory: pac-api/catalog/eventDetailMPT/F26/{F01..F07} */
window.GAMES = [
  { code: 'F01', opp: 'NC State',       slug: 'NCState',       date: 'Sat Aug 29', time: '3:30 PM', av: 7549,  cap: 65181 },
  { code: 'F02', opp: 'Norfolk State',  slug: 'NorfolkState',  date: 'Fri Sep 11', time: '7:00 PM', av: 25816, cap: 65180 },
  { code: 'F03', opp: 'Delaware',       slug: 'Delaware',      date: 'Sat Sep 26', time: 'TBD',     av: 24943, cap: 65180 },
  { code: 'F04', opp: 'Syracuse',       slug: 'Syracuse',      date: 'Sat Oct 10', time: 'TBD',     av: 25048, cap: 65180 },
  { code: 'F05', opp: 'Duke',           slug: 'Duke',          date: 'Fri Oct 23', time: '7:00 PM', av: 22999, cap: 65180 },
  { code: 'F06', opp: 'California',     slug: 'California',    date: 'Sat Nov 14', time: 'TBD',     av: 25388, cap: 65180 },
  { code: 'F07', opp: 'North Carolina', slug: 'NorthCarolina', date: 'Sat Nov 21', time: 'TBD',     av: 25136, cap: 65180 }
];

window.EMAILS = [
  {
    tab: 'NC State', file: 'ncstate.html', h: 3120,
    stage: 'Win-back · Week 0',
    name: 'The full Week 0 send',
    subj: 'Kodie, Section 117 is still open for Saturday',
    why: 'The complete argument in one email. Live seat count, a per-game sellout table across the whole ' +
         'season, the recipient’s own seat history and points balance, an upgrade offer, add-ons, ' +
         'renewal maths and the VAF ask. Every figure except the account scenario was read live.',
    trigger: 'last_order_season in F24/F25 AND no order this season AND event.days_until between 3 and 10',
    timing: 'T−5 days, once. Suppressed on purchase.',
    audience: 'Lapsed football buyers inside a drive-time radius',
    fields: ['patron.fname', 'orderhistory.last.section', 'scans.count(F25)', 'priPtsTotal',
             'event.AVAILABLE', 'event.TOTALCAPACITY', 'upgrades.best()', 'parking_sku'],
    caveat: 'Seat history, attendance, points balance and the upgrade price are a returning-buyer ' +
            'scenario. The account this was built from has never purchased. Inventory, pricing, the ' +
            'donation ladder and the opponent logos are all live.'
  },
  {
    tab: 'Post-game win', file: 'win.html', h: 1520,
    stage: 'Post-attendance',
    name: 'Win, to a first-time attendee',
    subj: 'Daniel, you were 1 of 64,217',
    why: 'The moment a first-timer is most likely to buy again, and the moment the current program sends ' +
         'one generic “Hoos Win!” blast to the entire file including the 60,000 people who were not there.',
    trigger: 'barcode_scan on first_order AND result = win',
    timing: 'Within 90 minutes of the final whistle',
    audience: 'Attendees only, first game of their lifetime',
    fields: ['patron.fname', 'scan.event', 'orderhistory.buyer_type', 'next_event']
  },
  {
    tab: 'Post-game loss', file: 'loss.html', h: 1520,
    stage: 'Retention',
    name: 'Loss, to a season holder',
    subj: 'Tough one. We’re not done.',
    why: 'A loss is the moment most programs go quiet. No email in the audited 306 days was ever triggered ' +
         'by a result going the wrong way. This one sells nothing and spends the moment on the person least ' +
         'likely to churn.',
    trigger: 'home_loss AND plan = season_holder',
    timing: 'Within 90 minutes of the final whistle',
    audience: 'Season ticket holders who scanned in',
    fields: ['patron.fname', 'orderhistory.seats', 'scans.streak', 'next_event']
  },
  {
    tab: 'Giving Day', file: 'giving.html', h: 1660,
    stage: 'Fundraising',
    name: 'Hoos Giving Day, mid-event',
    subj: 'You moved Women’s Lacrosse past 80%',
    why: 'Giving Day is the one day of the year where real-time state beats copy. Rank, sport, gift size and ' +
         'the match window are all live values that change hourly. The same send currently goes to every ' +
         'donor with none of them filled in.',
    trigger: 'gift_posted AND match_window_open',
    timing: 'Hourly recompute during the 35-hour window',
    audience: 'Donors who have already given today',
    fields: ['patron.fname', 'gift.amount', 'gift.designation', 'leaderboard.rank', 'match.expires_at']
  },
  {
    tab: 'First gift', file: 'welcome.html', h: 1660,
    stage: 'Donor onboarding',
    name: 'VAF first-gift welcome',
    subj: 'Your $50 funded 11 hours of a real scholarship',
    why: 'A first gift is the highest-risk moment in donor lifecycle and the cheapest to fix. There is no ' +
         'welcome series today, so a first-time VAF donor drops straight into the same broadcast file as a ' +
         'twenty-year Sabre Society member.',
    trigger: 'first_gift posted',
    timing: 'T+2 days, then 7/14/21/30. No ask for 30 days.',
    audience: 'First-time VAF donors',
    fields: ['patron.fname', 'gift.amount', 'gift.designation', 'athlete_match', 'suppression.no_ask_30d']
  }
];
