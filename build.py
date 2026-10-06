#!/usr/bin/env python3
"""Bouwt alle pagina's van bouwpartnerseindhoven.nl.
Teksten, diensten en projecten staan in _data.py. Na een wijziging:
    python3 build.py && npx tailwindcss -i src/input.css -o site/css/site.css --minify
"""
import html, json
from pathlib import Path

exec(open(Path(__file__).resolve().parent / "_data.py", encoding="utf-8").read())

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
V = "7"

TEL, TEL_LINK = "06 45072792", "+31645072792"
MAIL = "bouwpartnerseindhoven@gmail.com"
BEDRIJF, ADRES, KVK = "Bouwpartners Eindhoven B.V.", "Haakske 5, 5721 RC Asten", "98387561"
DOMEIN = "https://bouwpartnerseindhoven.nl"

# Welke accentkleur hoort bij welke groep
ACCENT = {"dak": "merk", "tuin": "tuin", "aanbouw": "merk"}


def e(s):
    return html.escape(str(s), quote=True)


PIJL = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
        '<path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

LD = json.dumps({
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
    "name": "Bouwpartners Eindhoven", "legalName": BEDRIJF, "url": DOMEIN + "/",
    "logo": DOMEIN + "/assets/logo/logo.png", "telephone": "+31645072792", "email": MAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "Haakske 5", "postalCode": "5721 RC",
                "addressLocality": "Asten", "addressCountry": "NL"},
    "areaServed": {"@type": "City", "name": "Eindhoven"},
    "identifier": {"@type": "PropertyValue", "propertyID": "KvK", "value": KVK},
    "knowsAbout": [d["naam"] for d in DIENSTEN],
}, ensure_ascii=False)


# ---------------------------------------------------------------------------
def kop(titel, omschrijving, pad, noindex=False, ld=False):
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(omschrijving)}">
<link rel="canonical" href="{DOMEIN}/{pad}">{'<meta name="robots" content="noindex">' if noindex else ''}
<meta property="og:title" content="{e(titel)}"><meta property="og:description" content="{e(omschrijving)}">
<meta property="og:type" content="website"><meta property="og:locale" content="nl_NL">
<meta name="theme-color" content="#ffffff">
{'<script type="application/ld+json">' + LD + '</script>' if ld else ''}
<link rel="icon" href="assets/logo/favicon.png">
<link rel="stylesheet" href="css/site.css?v={V}">
</head>
<body>
<a href="#inhoud" class="sr-only focus:not-sr-only focus:absolute focus:left-6 focus:top-6 focus:z-50 focus:rounded-xl focus:bg-ink focus:px-5 focus:py-3 focus:text-white">Naar inhoud</a>
"""


def navigatie(home="index.html"):
    items = [(f"{home}#diensten", "Diensten"), ("ons-werk.html", "Ons werk"), (f"{home}#aanpak", "Werkwijze"), (f"{home}#contact", "Contact")]
    desktop = "".join(f'<a href="{h}" class="text-[0.9375rem] text-ink-soft transition-colors hover:text-ink">{t}</a>' for h, t in items)
    mobiel = "".join(f'<a href="{h}" class="border-b border-line-soft py-4 text-[1.0625rem] text-ink">{t}</a>' for h, t in items)
    return f"""<header class="sticky top-0 z-40 border-b border-line-soft bg-white/85 backdrop-blur-md">
  <div class="frame flex min-h-[4.5rem] items-center gap-8">
    <a href="{home}" class="shrink-0" aria-label="Bouwpartners Eindhoven, naar de homepage">
      <img src="assets/logo/logo.png" alt="Bouwpartners Eindhoven" width="974" height="254" class="h-9 w-auto">
    </a>
    <nav class="ml-auto hidden items-center gap-9 lg:flex" aria-label="Hoofdmenu">{desktop}</nav>
    <a href="{home}#contact" class="btn btn-ink ml-auto hidden lg:ml-2 lg:inline-flex">Bespreek je project</a>
    <button type="button" id="menu-knop" aria-expanded="false" aria-controls="mobiel-menu"
      class="ml-auto rounded-xl border border-line px-4 py-2.5 text-[0.9375rem] text-ink lg:hidden">Menu</button>
  </div>
  <div id="mobiel-menu" hidden class="border-t border-line-soft bg-white lg:hidden">
    <nav class="frame flex flex-col pb-6" aria-label="Hoofdmenu mobiel">{mobiel}
      <a href="{home}#contact" class="btn btn-ink mt-6">Bespreek je project</a>
    </nav>
  </div>
</header>
<main id="inhoud">
"""


def voet(home="index.html"):
    kolom = lambda groep, kleur: "".join(
        f'<li><a href="{d["slug"]}.html" class="block py-1.5 text-[0.9375rem] text-ink-soft transition-colors hover:text-{kleur}">{e(d["naam"])}</a></li>'
        for d in DIENSTEN if d["groep"] == groep)
    return f"""</main>
<footer class="border-t border-line-soft bg-paper-soft">
  <div class="frame grid gap-12 py-20 md:grid-cols-12 lg:gap-16">
    <div class="md:col-span-5">
      <img src="assets/logo/logo.png" alt="Bouwpartners Eindhoven" width="974" height="254" loading="lazy" class="h-10 w-auto">
      <p class="lede mt-6 text-[1rem]">Dak en zolder, tuin en bomen, overkappingen en aanbouwtjes. Vertel wat je wilt aanpakken, dan bespreken we rustig wat er kan.</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="tel:{TEL_LINK}" class="btn btn-stil">{TEL}</a>
        <a href="mailto:{MAIL}" class="btn btn-stil">Mail ons</a>
      </div>
    </div>
    <div class="md:col-span-3">
      <p class="label-merk">Dak &amp; zolder</p>
      <ul class="mt-4">{kolom("dak", "dak")}</ul>
      <p class="label-merk mt-8">Aanbouw</p>
      <ul class="mt-4">{kolom("aanbouw", "dak")}</ul>
    </div>
    <div class="md:col-span-2">
      <p class="label-tuin">Tuin &amp; bomen</p>
      <ul class="mt-4">{kolom("tuin", "tuin")}</ul>
    </div>
    <div class="md:col-span-2">
      <p class="label">Meer</p>
      <ul class="mt-4">
        <li><a href="ons-werk.html" class="block py-1.5 text-[0.9375rem] text-ink-soft transition-colors hover:text-ink">Ons werk</a></li>
        <li><a href="privacybeleid.html" class="block py-1.5 text-[0.9375rem] text-ink-soft transition-colors hover:text-ink">Privacybeleid</a></li>
        <li><a href="cookiebeleid.html" class="block py-1.5 text-[0.9375rem] text-ink-soft transition-colors hover:text-ink">Cookiebeleid</a></li>
      </ul>
    </div>
  </div>
  <div class="border-t border-line-soft">
    <div class="frame flex flex-wrap items-center justify-between gap-x-8 gap-y-3 py-8 text-[0.8125rem] text-ink-faint">
      <span>{BEDRIJF} &middot; {ADRES} &middot; KvK {KVK}</span>
      <span>&copy; 2026 Bouwpartners Eindhoven</span>
    </div>
  </div>
</footer>
<script src="js/site.js?v={V}" defer></script>
</body>
</html>
"""


def sectiekop(label, titel, intro="", rechts="", kleur="label"):
    return f"""<div class="flex flex-col gap-8 md:flex-row md:items-end md:justify-between">
  <div class="max-w-2xl">
    <p class="{kleur}">{e(label)}</p>
    <h2 class="kop-m mt-5">{titel}</h2>
    {f'<p class="lede mt-6">{intro}</p>' if intro else ''}
  </div>{rechts}
</div>"""


def aanpak_sectie():
    items = "".join(f"""<li class="kaart kaart-hover p-8 lg:p-10">
  <span class="label">Stap {nr}</span>
  <h3 class="kop-s mt-5">{e(t)}</h3>
  <p class="mt-3 text-[1rem] leading-relaxed text-ink-soft">{e(o)}</p>
</li>""" for nr, t, o in AANPAK)
    return f"""<section id="aanpak" class="bg-paper-soft py-20 lg:py-28">
  <div class="frame">
    {sectiekop("Werkwijze", "Van een eerst idee<br>naar aanpakken.", "Je hoeft nog geen uitgewerkt plan te hebben. Vertel wat je in gedachten hebt, dan kijken we samen verder.")}
    <ol class="mt-14 grid gap-6 md:grid-cols-3 lg:gap-8">{items}</ol>
  </div>
</section>"""


def vragen_sectie():
    items = "".join(f"""<details class="group border-b border-line-soft">
  <summary class="flex cursor-pointer list-none items-start justify-between gap-8 py-6 text-[1.125rem] font-medium text-ink [&amp;::-webkit-details-marker]:hidden">
    {e(v)}
    <span aria-hidden="true" class="mt-1 shrink-0 text-ink-faint transition-transform duration-200 group-open:rotate-45">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
    </span>
  </summary>
  <p class="max-w-reading pb-6 pr-10 text-[1rem] leading-relaxed text-ink-soft">{e(a)}</p>
</details>""" for v, a in VRAGEN)
    return f"""<section class="bg-white py-20 lg:py-28">
  <div class="frame grid gap-12 md:grid-cols-12 lg:gap-20">
    <div class="md:col-span-5">
      <p class="label">Veelgestelde vragen</p>
      <h2 class="kop-m mt-5">Goed om<br>te weten.</h2>
      <p class="lede mt-6">Staat je vraag er niet bij? Bel gerust, of zet hem in je bericht.</p>
    </div>
    <div class="border-t border-line-soft md:col-span-7">{items}</div>
  </div>
</section>"""


def formulier():
    opties = "".join(f"<option>{e(o)}</option>" for o in
                     ["Ik wil mijn plannen bespreken", "Dak & zolder", "Tuin & bomen", "Aanbouw"])
    return f"""<section id="contact" class="bg-paper-soft py-20 lg:py-28">
  <div class="frame grid gap-12 md:grid-cols-12 lg:gap-20">
    <div class="md:col-span-5">
      <p class="label">Contact</p>
      <h2 class="kop-m mt-5">Wat zijn<br>jouw plannen?</h2>
      <p class="lede mt-6">Vertel wat je wilt aanpakken. Een eerste idee is genoeg om het gesprek te beginnen.</p>
      <dl class="mt-10 space-y-6">
        <div>
          <dt class="label">Telefoon</dt>
          <dd class="mt-2"><a href="tel:{TEL_LINK}" class="font-display text-[1.75rem] font-semibold tracking-tight text-ink transition-colors hover:text-merk-ink">{TEL}</a></dd>
        </div>
        <div>
          <dt class="label">E-mail</dt>
          <dd class="mt-2"><a href="mailto:{MAIL}" class="break-all text-[1rem] text-ink-soft transition-colors hover:text-merk-ink">{MAIL}</a></dd>
        </div>
        <div>
          <dt class="label">Werkgebied</dt>
          <dd class="mt-2 text-[1rem] text-ink-soft">Eindhoven en omgeving</dd>
        </div>
      </dl>
    </div>
    <form id="project-form" action="https://formsubmit.co/{MAIL}" method="POST" class="kaart p-8 shadow-lift md:col-span-7 lg:p-12">
      <input type="hidden" name="_subject" value="Nieuwe projectaanvraag via de website">
      <input type="hidden" name="_template" value="table">
      <input type="text" name="_honey" tabindex="-1" autocomplete="off" hidden>
      <div class="grid gap-6 sm:grid-cols-2">
        <div><label for="naam" class="label block">Je naam</label>
          <input id="naam" name="naam" autocomplete="name" required placeholder="Voor- en achternaam" class="veld mt-3"></div>
        <div><label for="email" class="label block">Je e-mailadres</label>
          <input id="email" name="email" type="email" autocomplete="email" required placeholder="naam@voorbeeld.nl" class="veld mt-3"></div>
      </div>
      <div class="mt-6"><label for="dienst" class="label block">Wat wil je aanpakken?</label>
        <select id="dienst" name="dienst" class="veld mt-3">{opties}</select></div>
      <div class="mt-6"><label for="bericht" class="label block">Vertel kort over je project</label>
        <textarea id="bericht" name="bericht" rows="5" required placeholder="Wat wil je veranderen aan je huis of tuin?" class="veld mt-3 resize-y"></textarea></div>
      <div class="mt-8 flex flex-wrap items-center gap-3">
        <button type="submit" class="btn btn-ink">Verstuur je aanvraag {PIJL}</button>
      </div>
      <p id="form-status" role="status" class="mt-5 text-[0.9375rem] text-merk-ink"></p>
      <p class="mt-6 border-t border-line-soft pt-6 text-[0.875rem] leading-relaxed text-ink-faint">
        Je aanvraag komt direct bij ons binnen. We gebruiken je gegevens alleen om op je aanvraag te reageren.
        Zie ons <a href="privacybeleid.html" class="text-ink-soft underline decoration-line underline-offset-4 transition-colors hover:text-merk-ink">privacybeleid</a>.</p>
    </form>
  </div>
</section>"""


def dienstenlijst(actief=None):
    kolommen = ""
    for g, naam in GROEPEN.items():
        k = ACCENT[g]
        rijen = ""
        for d in DIENSTEN:
            if d["groep"] != g:
                continue
            aan = d["slug"] == actief
            rijen += (f'<li><a href="{d["slug"]}.html"{" aria-current=\"page\"" if aan else ""} '
                      f'class="group flex items-center justify-between gap-4 border-b border-line-soft py-4 transition-colors hover:text-{k}">'
                      f'<span class="text-[1rem] {"text-" + k + " font-medium" if aan else "text-ink-soft"} group-hover:text-{k}">{e(d["naam"])}</span>'
                      f'<span class="text-ink-faint transition-all group-hover:translate-x-1 group-hover:text-{k}">{PIJL}</span></a></li>')
        kolommen += f'<div><p class="label-{k}">{e(naam)}</p><ul class="mt-5">{rijen}</ul></div>'
    return f"""<section class="bg-white py-20 lg:py-24">
  <div class="frame">
    {sectiekop("Alle diensten", "Alles wat we<br>voor je aanpakken.")}
    <div class="mt-14 grid gap-10 md:grid-cols-3 lg:gap-16">{kolommen}</div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
def home():
    # Twee gelijkwaardige pijlers, met de aanbouw als verbindende band eronder
    def pijler(groep, kleur, foto, alt, titel, tekst, slugs):
        links = "".join(
            f'<a href="{s}.html" class="link-pijl rounded-lg px-3 py-2 text-[0.9375rem] text-ink-soft transition-colors hover:bg-{kleur}/5 hover:text-{kleur}">{e(D[s]["naam"])} {PIJL}</a>'
            for s in slugs)
        return f"""<article class="group flex flex-col">
  <div class="overflow-hidden rounded-2xl">
    <img src="assets/images/{foto}.webp" alt="{e(alt)}" width="1400" height="1050" fetchpriority="high"
      class="beeld aspect-[4/5] transition-transform duration-700 ease-out group-hover:scale-[1.02]">
  </div>
  <div class="mt-8 flex flex-1 flex-col">
    <p class="label-{kleur}">{e(GROEPEN[groep])}</p>
    <h2 class="kop-m mt-4">{titel}</h2>
    <p class="lede mt-5 text-[1rem]">{e(tekst)}</p>
    <div class="mt-7 flex flex-wrap gap-1 border-t border-line-soft pt-5">{links}</div>
    <a href="index.html#contact" data-keuze="{e(GROEPEN[groep])}" class="btn btn-{kleur} mt-8 self-start">Bespreek je plannen {PIJL}</a>
  </div>
</article>"""

    diensten_rijen = "".join(f"""<a href="{d["slug"]}.html" class="kaart kaart-hover group flex items-start gap-6 p-7 lg:p-8">
  <span class="label-{ACCENT[d["groep"]]} mt-1 shrink-0">{d["nr"]}</span>
  <span class="min-w-0 flex-1">
    <span class="kop-s block transition-colors group-hover:text-{ACCENT[d["groep"]]}">{e(d["naam"])}</span>
    <span class="mt-2 block text-[0.9375rem] leading-relaxed text-ink-soft">{e(d["kort"])}</span>
  </span>
  <span class="mt-1 shrink-0 text-ink-faint transition-all group-hover:translate-x-1 group-hover:text-{ACCENT[d["groep"]]}">{PIJL}</span>
</a>""" for d in DIENSTEN)

    projecten = "".join(f"""<article class="group">
  <div class="overflow-hidden rounded-2xl">
    <img src="assets/images/{p["foto"]}.webp" alt="{e(p["alt"])}" loading="lazy"
      class="beeld aspect-[4/3] transition-transform duration-700 ease-out group-hover:scale-[1.02]">
  </div>
  <div class="mt-6 flex items-baseline justify-between gap-4">
    <h3 class="kop-s">{e(p["titel"])}</h3>
    <span class="label shrink-0">{e(p["regio"])}</span>
  </div>
  <p class="mt-2 text-[0.9375rem] leading-relaxed text-ink-soft">{e(p["tekst"])}</p>
  <a href="{p["dienst"]}.html" class="link-pijl mt-4 text-[0.9375rem] text-ink hover:text-merk-ink">{e(p["type"])} {PIJL}</a>
</article>""" for p in PROJECTEN)

    body = f"""<section class="bg-white pb-20 pt-16 lg:pb-28 lg:pt-24">
  <div class="frame">
    <div class="max-w-4xl">
      <p class="label">Bouwpartners Eindhoven</p>
      <h1 class="kop-xl mt-6 text-[clamp(2.75rem,6.4vw,5.25rem)]">Vakwerk aan je dak.<br>Rust in je tuin.</h1>
      <p class="lede mt-8 text-[1.125rem] sm:text-[1.25rem]">
        Twee ambachten onder één dak. We pakken je dak en zolder aan, leggen je tuin opnieuw aan en bouwen de ruimte ertussen.</p>
      <div class="mt-10 flex flex-wrap gap-3">
        <a href="#contact" class="btn btn-ink">Bespreek je project {PIJL}</a>
        <a href="#diensten" class="btn btn-stil">Bekijk de diensten</a>
      </div>
    </div>

    <div class="mt-20 grid gap-12 md:grid-cols-2 lg:mt-24 lg:gap-16">
      {pijler("dak", "dak", "dakwerk", "Vakman aan het werk op een dak in opbouw",
              "Alles boven<br>je hoofd.",
              "Van een dak dat aandacht nodig heeft tot een zolder waar je echt iets mee kunt. We beginnen bij het dak en werken naar binnen.",
              ["dakwerken", "dakisolatie", "zolder"])}
      {pijler("tuin", "tuin", "tuin-1", "Tuin met gazon, staptegels en overdekte buitenruimte",
              "Buiten wordt<br>een plek om<br>te blijven.",
              "Een nieuwe tuin, een bestaande tuin die toe is aan vernieuwing, of een boom die weg moet. Aangelegd om er jaren van te genieten.",
              ["tuinaanleg", "tuinrenovatie", "bomen-verwijderen"])}
    </div>

    <article class="kaart kaart-hover mt-12 grid items-center gap-10 overflow-hidden p-8 md:grid-cols-12 lg:mt-16 lg:p-12">
      <div class="md:col-span-5">
        <p class="label-merk">De verbinding</p>
        <h2 class="kop-m mt-4">Overkappingen<br>en aanbouwtjes.</h2>
        <p class="lede mt-5 text-[1rem]">Daar waar het dak de tuin raakt. Beschut buiten zitten of wat extra ruimte aan huis, in hout gebouwd en netjes afgewerkt.</p>
        <a href="overkappingen-aanbouw.html" class="btn btn-stil mt-7">Bekijk overkappingen en aanbouw {PIJL}</a>
      </div>
      <div class="md:col-span-7">
        <img src="assets/images/overkapping-6.webp" alt="Houten overkapping met zitgelegenheid in de tuin" loading="lazy"
          class="beeld aspect-[16/9]">
      </div>
    </article>
  </div>
</section>

<section id="diensten" class="bg-paper-soft py-20 lg:py-28">
  <div class="frame">
    {sectiekop("Diensten", "Zeven dingen<br>die we voor je doen.",
               "Dak, zolder, tuin en aanbouw. Kies waar het bij jou om gaat, dan lees je op die pagina wat handig is om door te geven.",
               f'<a href="ons-werk.html" class="link-pijl shrink-0 text-ink hover:text-merk-ink">Bekijk ons werk {PIJL}</a>')}
    <div class="mt-14 grid gap-5 md:grid-cols-2 lg:gap-6">{diensten_rijen}</div>
  </div>
</section>

<section class="bg-white py-20 lg:py-28">
  <div class="frame">
    {sectiekop("Ons werk", "Uitgevoerd werk,<br>eigen foto's.",
               "Geen stockbeeld. Dit zijn projecten die we zelf hebben gedaan.",
               f'<a href="ons-werk.html" class="link-pijl shrink-0 text-ink hover:text-merk-ink">Alle foto\'s {PIJL}</a>')}
    <div class="mt-14 grid gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">{projecten}</div>
  </div>
</section>

{aanpak_sectie()}
{vragen_sectie()}
{formulier()}"""
    (OUT / "index.html").write_text(
        kop("Bouwpartners Eindhoven — Dakwerken, zolder, tuin en aanbouw",
            "Dakwerken, dakisolatie, zolderafwerking, tuinaanleg, tuinrenovatie, bomen verwijderen en overkappingen in Eindhoven. Bespreek jouw project.",
            "", ld=True) + navigatie() + body + voet(), encoding="utf-8")


def dienstpagina(d):
    k = ACCENT[d["groep"]]
    punten = "".join(f"""<li class="kaart p-8">
  <span class="label-{k}">0{i + 1}</span>
  <h3 class="kop-s mt-5">{e(t)}</h3>
  <p class="mt-3 text-[1rem] leading-relaxed text-ink-soft">{e(o)}</p>
</li>""" for i, (t, o) in enumerate(d["punten"]))

    hoofdfoto = ""
    if d["fotos"]:
        n, alt = d["fotos"][0]
        hoofdfoto = (f'<div class="md:col-span-6"><img src="assets/images/{n}.webp" alt="{e(alt)}" width="1400" height="1050" '
                     f'fetchpriority="high" class="beeld aspect-[4/5] shadow-lift"></div>')

    galerij = ""
    if len(d["fotos"]) > 1:
        fig = "".join(f'<figure class="overflow-hidden rounded-2xl"><img src="assets/images/{n}.webp" alt="{e(alt)}" loading="lazy" '
                      'class="beeld aspect-[4/3] transition-transform duration-700 ease-out hover:scale-[1.02]"></figure>'
                      for n, alt in d["fotos"][1:])
        galerij = f"""<section class="bg-white py-20 lg:py-24">
  <div class="frame">
    {sectiekop("Eigen werk", "Zo ziet<br>het eruit.", "",
               f'<a href="ons-werk.html" class="link-pijl shrink-0 text-ink hover:text-{k}">Alle foto\'s {PIJL}</a>', f"label-{k}")}
    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{fig}</div>
  </div>
</section>"""

    body = f"""<section class="bg-white py-16 lg:py-24">
  <div class="frame grid items-center gap-12 md:grid-cols-12 lg:gap-20">
    <div class="min-w-0 {'md:col-span-6' if hoofdfoto else 'md:col-span-9'}">
      <nav class="mb-8 flex flex-wrap items-center gap-2 text-[0.875rem] text-ink-faint" aria-label="Kruimelpad">
        <a href="index.html" class="transition-colors hover:text-ink">Home</a><span>/</span>
        <span>{e(GROEPEN[d["groep"]])}</span><span>/</span><span class="text-{k}">{e(d["naam"])}</span>
      </nav>
      <p class="label-{k}">Dienst {d["nr"]}</p>
      <h1 class="kop-l mt-5">{d["h1"].replace("<br>", " ")}</h1>
      <p class="lede mt-7 text-[1.125rem]">{e(d["intro"])}</p>
      <div class="mt-10 flex flex-wrap gap-3">
        <a href="index.html#contact" data-keuze="{e(GROEPEN[d["groep"]])}" class="btn btn-{k}">{e(d["actie"])} {PIJL}</a>
        <a href="tel:{TEL_LINK}" class="btn btn-stil">Bel {TEL}</a>
      </div>
    </div>
    {hoofdfoto}
  </div>
</section>

<section class="bg-paper-soft py-20 lg:py-28">
  <div class="frame">
    {sectiekop("Zo begin je", e(d["kop"]) + ".", "Met deze drie punten heb je alles voor een eerste bericht.", "", f"label-{k}")}
    <ol class="mt-14 grid gap-6 md:grid-cols-3">{punten}</ol>
  </div>
</section>

{galerij}

<section class="bg-paper-soft py-20 lg:py-24">
  <div class="frame flex flex-col items-start gap-10 md:flex-row md:items-center md:justify-between">
    <div class="max-w-xl">
      <p class="label-{k}">Jouw idee is het begin</p>
      <h2 class="kop-m mt-4">Een eerste idee<br>is genoeg.</h2>
    </div>
    <a href="index.html#contact" data-keuze="{e(GROEPEN[d["groep"]])}" class="btn btn-{k} shrink-0">{e(d["actie"])} {PIJL}</a>
  </div>
</section>

{dienstenlijst(d["slug"])}"""
    (OUT / f'{d["slug"]}.html').write_text(
        kop(f'{d["naam"]} in Eindhoven — Bouwpartners Eindhoven', d["meta"], d["slug"]) + navigatie() + body + voet(),
        encoding="utf-8")


def ons_werk():
    knop = ('class="rounded-xl border border-line bg-white px-5 py-2.5 text-[0.9375rem] text-ink-soft transition-all '
            'hover:border-ink/25 aria-pressed:border-ink aria-pressed:bg-ink aria-pressed:text-white"')
    knoppen = f'<button type="button" data-soort="alles" aria-pressed="true" {knop}>Alles</button>'
    knoppen += "".join(f'<button type="button" data-soort="{s}" aria-pressed="false" {knop}>{n}</button>' for s, n, _ in WERK)
    kolommen = [[(s, n, f) for f in fs] for s, n, fs in WERK]
    volgorde = []
    while any(kolommen):
        for k in kolommen:
            if k:
                volgorde.append(k.pop(0))
    fig = "".join(f"""<figure data-soort="{s}" class="group">
  <div class="overflow-hidden rounded-2xl">
    <img src="assets/images/{f}.webp" alt="{n}, eigen werk van Bouwpartners Eindhoven" loading="lazy"
      class="beeld aspect-square transition-transform duration-700 ease-out group-hover:scale-[1.03]">
  </div>
  <figcaption class="mt-4 flex items-center justify-between gap-3">
    <span class="text-[0.9375rem] text-ink">{n}</span><span class="label">Regio Eindhoven</span>
  </figcaption>
</figure>""" for s, n, f in volgorde)
    body = f"""<section class="bg-white py-16 lg:py-24">
  <div class="frame">
    <nav class="mb-8 flex flex-wrap items-center gap-2 text-[0.875rem] text-ink-faint" aria-label="Kruimelpad">
      <a href="index.html" class="transition-colors hover:text-ink">Home</a><span>/</span><span class="text-ink">Ons werk</span>
    </nav>
    <div class="max-w-3xl">
      <p class="label">Ons werk</p>
      <h1 class="kop-l mt-5">Werk dat we zelf hebben gedaan.</h1>
      <p class="lede mt-7 text-[1.125rem]">Daken, zolders, tuinen en overkappingen. Alle foto's op deze pagina komen uit onze eigen projecten.</p>
    </div>
    <div class="mt-12 flex flex-wrap gap-3">{knoppen}</div>
    <div class="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3 lg:gap-10" id="werk-raster">{fig}</div>
  </div>
</section>

<section class="bg-paper-soft py-20 lg:py-24">
  <div class="frame flex flex-col items-start gap-10 md:flex-row md:items-center md:justify-between">
    <div class="max-w-xl"><p class="label">Jouw idee is het begin</p><h2 class="kop-m mt-4">Zoiets ook<br>bij jou?</h2></div>
    <a href="index.html#contact" class="btn btn-ink shrink-0">Bespreek je project {PIJL}</a>
  </div>
</section>

{dienstenlijst()}"""
    (OUT / "ons-werk.html").write_text(
        kop("Ons werk — Bouwpartners Eindhoven",
            "Foto's van eigen werk van Bouwpartners Eindhoven: daken, zolders, tuinen en overkappingen.", "ons-werk")
        + navigatie() + body + voet(), encoding="utf-8")


H2 = 'class="kop-s mt-12 first:mt-0"'
P = 'class="mt-4 max-w-reading text-[1.0625rem] leading-[1.8] text-ink-soft"'
A = 'class="text-ink underline decoration-line underline-offset-4 transition-colors hover:text-merk-ink"'


def tekstpagina(bestand, titel, h1, label, inhoud, noindex=False):
    body = f"""<section class="bg-white py-16 lg:py-20">
  <div class="frame">
    <nav class="mb-8 flex flex-wrap items-center gap-2 text-[0.875rem] text-ink-faint" aria-label="Kruimelpad">
      <a href="index.html" class="transition-colors hover:text-ink">Home</a><span>/</span><span class="text-ink">{e(label)}</span>
    </nav>
    <h1 class="kop-l max-w-3xl">{h1}</h1>
  </div>
</section>
<section class="border-t border-line-soft bg-white pb-24 pt-16">
  <div class="frame grid gap-12 md:grid-cols-12 lg:gap-20">
    <div class="md:col-span-3"><p class="label md:sticky md:top-28">{e(label)}</p></div>
    <div class="min-w-0 md:col-span-9">{inhoud}</div>
  </div>
</section>"""
    (OUT / bestand).write_text(
        kop(titel, titel, bestand.replace(".html", ""), noindex) + navigatie() + body + voet(), encoding="utf-8")


def rest():
    tekstpagina("privacybeleid.html", "Privacybeleid — Bouwpartners Eindhoven", "Privacybeleid.", "Privacybeleid", f"""
<p class="label">Laatst bijgewerkt op 5 oktober 2026</p>
<p {P}>Bouwpartners Eindhoven vindt het belangrijk dat je weet wat er met je gegevens gebeurt. Deze verklaring legt uit welke gegevens we krijgen, waarom we ze gebruiken en welke rechten je hebt.</p>
<h2 {H2}>Wie verantwoordelijk is</h2>
<p {P}>{BEDRIJF}, {ADRES}, KvK {KVK}, is verwerkingsverantwoordelijke voor de verwerking van je persoonsgegevens. Vragen hierover kun je mailen naar <a href="mailto:{MAIL}" {A}>{MAIL}</a> of bellen via <a href="tel:{TEL_LINK}" {A}>{TEL}</a>.</p>
<h2 {H2}>Welke gegevens we verwerken</h2>
<p {P}>Vul je het formulier op deze website in, dan ontvangen we je naam, je e-mailadres, de gekozen dienst en je bericht per e-mail. De website zelf slaat niets op. Bel je ons of mail je ons rechtstreeks, dan verwerken we de gegevens die je ons in dat contact geeft, zoals je telefoonnummer en het adres van het werk.</p>
<h2 {H2}>Waarom we ze gebruiken en op welke grond</h2>
<p {P}>We gebruiken je gegevens alleen om op je aanvraag te reageren, je vraag te beantwoorden en je project met je te bespreken. De grondslag daarvoor is de uitvoering van een overeenkomst of de stappen die daaraan voorafgaan op jouw verzoek. Wordt het een opdracht, dan gebruiken we je gegevens ook om die uit te voeren en te factureren; daarvoor geldt daarnaast onze wettelijke administratieplicht. We verkopen je gegevens niet, gebruiken ze niet voor reclame en nemen geen besluiten over je op basis van geautomatiseerde verwerking.</p>
<h2 {H2}>Wie je gegevens nog meer ziet</h2>
<p {P}>Berichten via het formulier worden doorgestuurd door FormSubmit (formsubmit.co) en komen binnen in onze e-mail. Die wordt geleverd door Google (Gmail). Verder delen we je gegevens niet met anderen, behalve wanneer dat nodig is om het werk uit te voeren of wanneer de wet ons daartoe verplicht, bijvoorbeeld tegenover onze boekhouder of de Belastingdienst. Onze website staat op een server binnen de Europese Unie en laadt geen onderdelen van andere websites. Voor zover gegevens via onze e-mail of FormSubmit buiten de Europese Unie worden verwerkt, gebeurt dat op basis van de standaardbepalingen die de Europese Commissie daarvoor heeft vastgesteld.</p>
<h2 {H2}>Hoe lang we ze bewaren</h2>
<p {P}>We bewaren je aanvraag zolang dat nodig is om je te helpen. Wordt het geen opdracht, dan verwijderen we je gegevens uiterlijk een jaar na je aanvraag. Wordt het wel een opdracht, dan bewaren we de administratie zeven jaar, omdat de Belastingdienst dat van ons vraagt.</p>
<h2 {H2}>Hoe we ze beveiligen</h2>
<p {P}>Onze website gebruikt een beveiligde verbinding (https). Je aanvraag komt binnen in een e-mailaccount dat met een wachtwoord en tweestapsverificatie is afgeschermd. Alleen de mensen die aan je project werken hebben toegang tot je gegevens.</p>
<h2 {H2}>Cookies</h2>
<p {P}>Deze website plaatst geen cookies en gebruikt geen analytics of trackers. Lees meer in ons <a href="cookiebeleid.html" {A}>cookiebeleid</a>.</p>
<h2 {H2}>Jouw rechten</h2>
<p {P}>Je mag je gegevens inzien, laten aanpassen, laten verwijderen of de verwerking laten beperken. Je mag ook bezwaar maken tegen de verwerking en vragen om je gegevens over te dragen. Mail daarvoor naar <a href="mailto:{MAIL}" {A}>{MAIL}</a>; we reageren binnen een maand. Ben je niet tevreden over hoe we met je gegevens omgaan, dan kun je een klacht indienen bij de Autoriteit Persoonsgegevens via autoriteitpersoonsgegevens.nl.</p>
<h2 {H2}>Wijzigingen</h2>
<p {P}>Verandert er iets aan deze website of aan de manier waarop we met gegevens omgaan, dan passen we deze verklaring aan. Bovenaan staat wanneer dat voor het laatst gebeurd is.</p>
""")
    tekstpagina("cookiebeleid.html", "Cookiebeleid — Bouwpartners Eindhoven", "Cookiebeleid.", "Cookiebeleid", f"""
<p class="label">Laatst bijgewerkt op 5 oktober 2026</p>
<h2 {H2}>Deze website plaatst geen cookies</h2>
<p {P}>Je kunt deze website bekijken zonder dat er iets op je computer, telefoon of tablet wordt opgeslagen. We gebruiken geen functionele, analytische of trackingcookies, en ook geen local storage of vergelijkbare technieken.</p>
<h2 {H2}>Daarom zie je geen cookiemelding</h2>
<p {P}>Een cookiemelding is bedoeld om je toestemming te vragen voor cookies die niet strikt noodzakelijk zijn. Omdat we die niet plaatsen, is er niets om toestemming voor te vragen. Een melding tonen zou alleen maar in de weg zitten.</p>
<h2 {H2}>Geen onderdelen van andere websites</h2>
<p {P}>Alle lettertypen, afbeeldingen en scripts op deze website worden vanaf onze eigen server geladen. Er zijn geen knoppen van sociale media, geen video's van andere websites en geen advertentienetwerken. Daardoor krijgen andere partijen je IP-adres niet te zien als je deze website bezoekt.</p>
<h2 {H2}>Statistieken</h2>
<p {P}>We gebruiken geen Google Analytics of een vergelijkbare bezoekersteller. Onze website is wel aangemeld bij Google Search Console. Daarmee zien we welke zoekopdrachten naar onze website leiden; dat gebeurt aan de kant van Google en plaatst niets in jouw browser.</p>
<h2 {H2}>Als dit verandert</h2>
<p {P}>Gaan we in de toekomst wel statistieken of advertentiepixels gebruiken, dan vragen we daarvoor eerst je toestemming via een cookiemelding en passen we deze pagina aan. Zie ook ons <a href="privacybeleid.html" {A}>privacybeleid</a>.</p>
""")
    tekstpagina("404.html", "Pagina niet gevonden — Bouwpartners Eindhoven", "Deze pagina bestaat niet.", "Fout 404",
                f'<p {P}>De pagina is verplaatst of het adres klopt niet.</p>'
                f'<p class="mt-8"><a href="index.html" class="btn btn-ink">Naar de homepage {PIJL}</a></p>', True)

    paginas = [""] + [d["slug"] for d in DIENSTEN] + ["ons-werk", "privacybeleid", "cookiebeleid"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMEIN}/{p}</loc></url>\n" for p in paginas) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMEIN}/sitemap.xml\n")
    (OUT / "vercel.json").write_text('{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    home()
    for d in DIENSTEN:
        dienstpagina(d)
    ons_werk()
    rest()
    print("Gebouwd:", ", ".join(sorted(p.name for p in OUT.glob("*.html"))))
