/* UVA Athletics × BRCG portal — nav, email library. */
(function () {
  'use strict';
  const $ = s => document.querySelector(s);
  const el = (t, c, h) => { const n = document.createElement(t); if (c) n.className = c; if (h != null) n.innerHTML = h; return n; };

  /* ---------- icons (lucide-style, 15px stroke) ---------- */
  const I = d => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
                 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>';
  const ICON = {
    overview:  I('<path d="M3 12h4l3 8 4-16 3 8h4"/>'),
    inbox:     I('<path d="M3 12h5l2 3h4l2-3h5"/><path d="M5.5 5h13l2.5 7v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5z"/>'),
    week0:     I('<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>'),
    data:      I('<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>'),
    apis:      I('<path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>'),
    integration: I('<path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>'),
    dataplan:  I('<path d="M4 5h16M4 12h16M4 19h10"/><circle cx="19" cy="19" r="2.5"/>'),
    lifecycle: I('<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/>'),
    emails:    I('<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
    roadmap:   I('<path d="M4 19V6a2 2 0 0 1 2-2h3l2 2h7a2 2 0 0 1 2 2v11"/><path d="M2 19h20"/>'),
    method:    I('<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/>')
  };

  const NAV = [
    { g: 'Analysis' },
    { p: 'overview',  t: 'Overview',       s: 'The verdict, in four numbers' },
    { p: 'inbox',     t: 'The inbox',      s: '78 sends, mapped' },
    { p: 'week0',     t: 'Week 0',         s: 'The run-up to Saturday' },
    { g: 'The data' },
    { p: 'data',      t: 'Architecture',   s: 'Four systems, one silo' },
    { p: 'apis',      t: 'API surface',    s: 'Real endpoints and payloads' },
    { p: 'integration', t: 'Getting it into Eloqua', s: 'The build plan' },
    { p: 'dataplan',  t: 'Data plan',       s: 'Field-by-field spec' },
    { g: 'What it enables' },
    { p: 'lifecycle', t: 'Lifecycle',      s: 'Eight triggers already possible' },
    { p: 'emails',    t: 'Email library',  s: 'Five built emails' },
    { g: 'Next' },
    { p: 'roadmap',   t: 'Roadmap',        s: 'Three pilots, this season' },
    { p: 'method',    t: 'Method & sources', s: 'Live vs illustrative' }
  ];

  /* Public teardown. No gate: every figure came from public sources. */
  $('#app').classList.add('on');
  $('#upd').textContent = 'Updated ' + window.META.updated;

  /* ---------- nav ---------- */
  const nav = $('#nav'), side = $('#side');
  NAV.forEach(n => {
    if (n.g) { nav.appendChild(el('div', 'grp', n.g)); return; }
    const b = el('button', null, ICON[n.p] + '<span><span class="t">' + n.t + '</span><span class="s">' + n.s + '</span></span>');
    b.dataset.p = n.p;
    if (n.p === 'overview') b.setAttribute('aria-current', 'page');
    nav.appendChild(b);
  });

  function go(p) {
    nav.querySelectorAll('button[data-p]').forEach(x => x.removeAttribute('aria-current'));
    const btn = nav.querySelector('button[data-p="' + p + '"]');
    if (btn) btn.setAttribute('aria-current', 'page');
    document.querySelectorAll('.panel').forEach(x => x.classList.remove('on'));
    const panel = $('#p-' + p);
    if (panel) panel.classList.add('on');
    side.classList.remove('open');
    $('#mtoggle').setAttribute('aria-expanded', 'false');
    window.scrollTo(0, 0);
    if (history.replaceState) history.replaceState(null, '', '#' + p);
  }

  nav.addEventListener('click', e => {
    const b = e.target.closest('button[data-p]');
    if (b) go(b.dataset.p);
  });

  /* in-page links to other panels */
  document.addEventListener('click', e => {
    const a = e.target.closest('a[data-go]');
    if (a) { e.preventDefault(); go(a.dataset.go); }
  });

  $('#mtoggle').addEventListener('click', () => {
    $('#mtoggle').setAttribute('aria-expanded', String(side.classList.toggle('open')));
  });

  /* deep link on load */
  const initial = (location.hash || '').replace('#', '');
  if (initial && $('#p-' + initial)) go(initial);

  /* ---------- email library ---------- */
  const strip = $('#mstrip'), wrap = $('#mwrap');
  window.EMAILS.forEach((m, i) => {
    const b = el('button', null, m.tab);
    b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
    b.dataset.i = i;
    strip.appendChild(b);
  });
  strip.addEventListener('click', e => {
    const b = e.target.closest('button[data-i]'); if (!b) return;
    strip.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', 'false'));
    b.setAttribute('aria-pressed', 'true');
    show(+b.dataset.i);
  });

  function show(i) {
    const m = window.EMAILS[i];
    wrap.innerHTML =
      '<div style="margin-bottom:20px">' +
        '<span class="tag brand">' + m.stage + '</span>' +
        '<h3 style="font-size:21px;margin-top:12px;font-weight:900">' + m.name + '</h3>' +
        '<p class="note" style="font-size:14px;margin-top:9px;max-width:80ch">' + m.why + '</p>' +
      '</div>' +
      '<div class="mailgrid">' +
        '<div class="mailframe">' +
          '<div class="chrome">' +
            '<div class="f"><b>From</b><span>updates@go.virginiasports.com</span></div>' +
            '<div class="f"><b>Subj</b><span class="subj">' + m.subj + '</span></div>' +
          '</div>' +
          '<iframe src="emails/' + m.file + '" title="' + m.name + '" loading="lazy" height="' + m.h + '"></iframe>' +
        '</div>' +
        '<div class="mail-spec card">' +
          '<div class="row"><div class="k">Trigger</div><div class="v">' + m.trigger + '</div></div>' +
          '<div class="row"><div class="k">Timing</div><div class="v">' + m.timing + '</div></div>' +
          '<div class="row"><div class="k">Audience</div><div class="v">' + m.audience + '</div></div>' +
          '<div class="row"><div class="k">Fields it reads</div><div class="v" style="margin-top:8px">' +
            m.fields.map(f => '<span class="fld">' + f + '</span>').join('') + '</div></div>' +
          (m.caveat ? '<div class="row"><div class="k" style="color:hsl(var(--brcg-gold))">Data caveat</div>' +
            '<div class="v">' + m.caveat + '</div></div>' : '') +
        '</div>' +
      '</div>';
  }
  show(0);
})();
