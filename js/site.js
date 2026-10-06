// Bouwpartners Eindhoven
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Mobiel menu
  const knop = $('#menu-knop'), menu = $('#mobiel-menu');
  if (knop && menu) {
    const zet = open => {
      menu.hidden = !open;
      knop.setAttribute('aria-expanded', String(open));
      knop.textContent = open ? 'Sluit' : 'Menu';
    };
    knop.addEventListener('click', () => zet(menu.hidden));
    menu.addEventListener('click', e => { if (e.target.closest('a')) zet(false); });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !menu.hidden) { zet(false); knop.focus(); }
    });
  }

  // Dienst alvast invullen in het formulier; de bezoeker kan altijd wisselen
  const select = $('#dienst');
  const kies = naam => {
    if (!select || !naam) return;
    $$('option', select).forEach(o => { if (o.value === naam) select.value = naam; });
  };
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-keuze]');
    if (a) {
      const keuze = a.dataset.keuze;
      if (select) kies(keuze);
      else try { sessionStorage.setItem('bpe-dienst', keuze); } catch (_) {}
    }
  });
  try {
    const bewaard = sessionStorage.getItem('bpe-dienst');
    if (bewaard && select) { kies(bewaard); sessionStorage.removeItem('bpe-dienst'); }
  } catch (_) {}

  // Hero: wisselen tussen de drie disciplines
  const data = $('#hero-data');
  if (data) {
    const items = JSON.parse(data.textContent);
    const foto = $('#hero-foto');
    Object.values(items).forEach(s => { const i = new Image(); i.src = 'assets/images/' + s.foto + '.webp'; });
    $$('[data-hero]').forEach(b => b.addEventListener('click', () => {
      const s = items[b.dataset.hero];
      $$('[data-hero]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      foto.style.opacity = '0';
      const nieuw = new Image();
      nieuw.onload = () => { foto.src = nieuw.src; foto.alt = s.alt; foto.style.opacity = '1'; };
      nieuw.src = 'assets/images/' + s.foto + '.webp';
      $('#hero-label').textContent = s.label;
      $('#hero-diensten').textContent = s.diensten;
      $('#hero-titel').innerHTML = s.titel;
      const actie = $('#hero-actie');
      actie.innerHTML = s.actie + ' <span aria-hidden="true">↙</span>'.replace('↙', '↗');
      actie.dataset.keuze = s.keuze;
    }));
  }

  // Filter op de pagina Ons werk
  const filters = $$('[data-soort]').filter(el => el.tagName === 'BUTTON');
  if (filters.length) {
    filters.forEach(b => b.addEventListener('click', () => {
      filters.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      $$('#werk-raster figure').forEach(f => {
        f.hidden = b.dataset.soort !== 'alles' && f.dataset.soort !== b.dataset.soort;
      });
    }));
  }

  // Formulier: verstuurt de aanvraag via FormSubmit naar onze mailbox
  const form = $('#project-form');
  if (form) {
    const status = $('#form-status');
    const knop = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const d = new FormData(form);
      d.set('_replyto', d.get('email') || '');
      d.set('_subject', 'Projectaanvraag: ' + (d.get('dienst') || '') + ' — ' + (d.get('naam') || ''));
      knop.disabled = true;
      status.textContent = 'Bezig met versturen…';
      try {
        const r = await fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
          method: 'POST', headers: { Accept: 'application/json' }, body: d
        });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || String(j.success) !== 'true') throw new Error(j.message || r.status);
        form.reset();
        status.textContent = 'Bedankt, je aanvraag is verstuurd. We nemen snel contact met je op.';
      } catch (err) {
        console.warn('Formulier niet verstuurd:', err.message);
        status.textContent = /activat/i.test(err.message)
          ? 'Het formulier wordt nog geactiveerd. Mail ons voorlopig via bouwpartnerseindhoven@gmail.com of bel 06 45072792.'
          : 'Versturen lukte niet. Mail ons via bouwpartnerseindhoven@gmail.com of bel 06 45072792.';
      } finally {
        knop.disabled = false;
      }
    });
  }
})();
