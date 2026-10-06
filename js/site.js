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

  // Formulier: zet de aanvraag klaar in het eigen e-mailprogramma
  const form = $('#project-form');
  if (form) {
    const status = $('#form-status');
    const tekst = () => {
      const d = new FormData(form);
      return ['Projectaanvraag Bouwpartners Eindhoven', '',
        'Naam: ' + (d.get('naam') || ''), 'E-mail: ' + (d.get('email') || ''),
        'Dienst: ' + (d.get('dienst') || ''), '', (d.get('bericht') || '')].join('\n');
    };
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      location.href = 'mailto:bouwpartnerseindhoven@gmail.com?subject='
        + encodeURIComponent('Mijn project — ' + select.value) + '&body=' + encodeURIComponent(tekst());
      status.textContent = 'Je aanvraag staat klaar in je e-mailprogramma, nog niet verstuurd. Opent er niets? Kopieer de tekst en mail hem zelf.';
    });
    $('#copy').addEventListener('click', async () => {
      if (!form.reportValidity()) return;
      try {
        await navigator.clipboard.writeText(tekst());
        status.textContent = 'Tekst gekopieerd. Plak hem in een e-mail naar bouwpartnerseindhoven@gmail.com.';
      } catch (_) {
        status.textContent = 'Kopiëren lukt hier niet. Selecteer de tekst in het formulier en kopieer hem zelf.';
      }
    });
  }
})();
