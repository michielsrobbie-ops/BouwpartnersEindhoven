#!/usr/bin/env python3
"""Bouwt alle pagina's van bouwpartnerseindhoven.nl (werkt met Python 3.9+).
Teksten, diensten, foto's en projecten staan in _data.py. Na een wijziging:
    python3 build.py && npx tailwindcss -i src/input.css -o css/site.css --minify
Hoog V op bij elke wijziging in CSS of JS, anders zien bezoekers de oude versie.
"""
import html, json
from pathlib import Path

exec(open(Path(__file__).resolve().parent / "_data.py", encoding="utf-8").read())

ROOT = Path(__file__).resolve().parent
OUT = ROOT
V = "9"

TEL, TEL_LINK = "06 45072792", "+31645072792"
MAIL = "bouwpartnerseindhoven@gmail.com"
BEDRIJF, STRAAT, POSTCODE, KVK = "Bouwpartners Eindhoven B.V.", "Haakske 5", "5721 RC", "98387561"
ADRES = STRAAT + ", " + POSTCODE + " " + VESTIGING
DOMEIN = "https://bouwpartnerseindhoven.nl"
NAAM = "Bouwpartners Eindhoven"

# Welke accentkleur hoort bij welke groep
ACCENT = {"dak": "merk", "tuin": "tuin", "aanbouw": "merk"}


def e(s):
    return html.escape(str(s), quote=True)


ALLE_FOTOS = "Alle foto's"
PIJL = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
        '<path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
VINK = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true" class="mt-1 shrink-0">'
        '<path d="M4 9.5l3 3 7-7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ---------------------------------------------------------------------------
# Afbeeldingen: echte afmetingen in de HTML en een kleinere variant voor mobiel.
BEELDEN = ROOT / "assets" / "images"
MATEN_BESTAND = BEELDEN / "maten.json"


def beelden_voorbereiden():
    """Leest afmetingen en maakt 800px-varianten. Zonder Pillow wordt de bewaarde lijst gebruikt."""
    try:
        from PIL import Image
    except ImportError:
        return json.loads(MATEN_BESTAND.read_text()) if MATEN_BESTAND.exists() else {}
    maten = {}
    for naam in FOTO:
        bron = BEELDEN / (naam + ".webp")
        with Image.open(bron) as im:
            maten[naam] = list(im.size)
            klein = BEELDEN / (naam + "-800.webp")
            if im.size[0] > 900 and not klein.exists():
                h = round(im.size[1] * 800 / im.size[0])
                im.convert("RGB").resize((800, h), Image.LANCZOS).save(klein, "WEBP", quality=78, method=6)
    logo = ROOT / "assets" / "logo"
    if not (logo / "logo-web.png").exists():
        with Image.open(logo / "logo.png") as im:
            im.resize((400, round(im.size[1] * 400 / im.size[0])), Image.LANCZOS).save(logo / "logo-web.png", optimize=True)
    MATEN_BESTAND.write_text(json.dumps(maten, indent=0, sort_keys=True))
    return maten


MATEN = beelden_voorbereiden()


def img(naam, cls, sizes="100vw", eager=False):
    """Een projectfoto met alt-tekst uit FOTO, afmetingen en srcset."""
    alt = FOTO[naam][0]
    w, h = MATEN.get(naam, (1400, 1050))
    srcset = ""
    if (BEELDEN / (naam + "-800.webp")).exists():
        srcset = f' srcset="/assets/images/{naam}-800.webp 800w, /assets/images/{naam}.webp {w}w" sizes="{sizes}"'
    laden = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    return f'<img src="/assets/images/{naam}.webp"{srcset} alt="{e(alt)}" width="{w}" height="{h}"{laden} class="{cls}">'


def in_uitvoering(naam):
    return FOTO[naam][1] == "uitvoering"


# ---------------------------------------------------------------------------
# Gestructureerde gegevens. Alleen wat zichtbaar op de site staat.
BEDRIJF_ID = DOMEIN + "/#bedrijf"
ADRES_LD = {"@type": "PostalAddress", "streetAddress": STRAAT, "postalCode": POSTCODE,
            "addressLocality": VESTIGING, "addressRegion": "Noord-Brabant", "addressCountry": "NL"}
GEBIED_LD = [{"@type": "City", "name": p} for p in PLAATSEN]


def bedrijf_ld():
    return {
        "@type": "HomeAndConstructionBusiness", "@id": BEDRIJF_ID,
        "name": NAAM, "legalName": BEDRIJF, "url": DOMEIN + "/",
        "logo": DOMEIN + "/assets/logo/logo.png", "image": DOMEIN + "/assets/images/dakwerk.webp",
        "telephone": TEL_LINK, "email": MAIL, "address": ADRES_LD, "areaServed": GEBIED_LD,
        "identifier": {"@type": "PropertyValue", "propertyID": "KvK", "value": KVK},
        "knowsAbout": [d["naam"] for d in DIENSTEN],
    }


def kruimel_ld(stappen):
    """stappen: [(naam, pad)], de laatste is de huidige pagina."""
    items = []
    for i, (naam, pad) in enumerate(stappen, 1):
        item = {"@type": "ListItem", "position": i, "name": naam}
        if i < len(stappen):
            item["item"] = DOMEIN + "/" + pad
        items.append(item)
    return {"@type": "BreadcrumbList", "itemListElement": items}


def ld_script(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return '<script type="application/ld+json">' + data.replace("</", "<\\/") + "</script>"


# ---------------------------------------------------------------------------
def kop(titel, omschrijving, pad, noindex=False, ld="", ogbeeld="dakwerk"):
    canon = DOMEIN + "/" + pad
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    canon_tag = "" if noindex else f'\n<link rel="canonical" href="{canon}">'
    og_url = "" if noindex else f'<meta property="og:url" content="{canon}">'
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(omschrijving)}">{canon_tag}{robots}
<meta property="og:title" content="{e(titel)}"><meta property="og:description" content="{e(omschrijving)}">
<meta property="og:type" content="website"><meta property="og:locale" content="nl_NL"><meta property="og:site_name" content="{NAAM}">
{og_url}<meta property="og:image" content="{DOMEIN}/assets/images/{ogbeeld}.webp">
<meta name="theme-color" content="#ffffff">
{ld}
<link rel="icon" href="/assets/logo/favicon.png">
<link rel="preload" href="/assets/fonts/jakarta-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css?v={V}">
</head>
<body>
<a href="#inhoud" class="sr-only focus:not-sr-only focus:absolute focus:left-6 focus:top-6 focus:z-50 focus:rounded-xl focus:bg-ink focus:px-5 focus:py-3 focus:text-white">Naar inhoud</a>
"""


def navigatie():
    items = [("/#diensten", "Diensten"), ("/ons-werk", "Ons werk"), ("/werkgebied", "Werkgebied"),
             ("/#aanpak", "Werkwijze"), ("/#contact", "Contact")]
    desktop = "".join(f'<a href="{h}" class="text-[0.9375rem] text-ink-soft transition-colors hover:text-ink">{t}</a>' for h, t in items)
    mobiel = "".join(f'<a href="{h}" class="border-b border-line-soft py-4 text-[1.0625rem] text-ink">{t}</a>' for h, t in items)
    return f"""<header class="sticky top-0 z-40 border-b border-line-soft bg-white/85 backdrop-blur-md">
  <div class="frame flex min-h-[4.5rem] items-center gap-8">
    <a href="/" class="shrink-0" aria-label="{NAAM}, naar de homepage">
      <img src="/assets/logo/logo-web.png" alt="{NAAM}" width="400" height="104" class="h-9 w-auto">
    </a>
    <nav class="ml-auto hidden items-center gap-8 lg:flex" aria-label="Hoofdmenu">{desktop}</nav>
    <a href="/#contact" class="btn btn-ink ml-auto hidden lg:ml-2 lg:inline-flex">Bespreek je project</a>
    <button type="button" id="menu-knop" aria-expanded="false" aria-controls="mobiel-menu"
      class="ml-auto rounded-xl border border-line px-4 py-2.5 text-[0.9375rem] text-ink lg:hidden">Menu</button>
  </div>
  <div id="mobiel-menu" hidden class="border-t border-line-soft bg-white lg:hidden">
    <nav class="frame flex flex-col pb-6" aria-label="Hoofdmenu mobiel">{mobiel}
      <a href="/#contact" class="btn btn-ink mt-6">Bespreek je project</a>
    </nav>
  </div>
</header>
<main id="inhoud">
"""


def voet():
    kolom = lambda groep, kleur: "".join(
        f'<li><a href="/{d["slug"]}" class="block py-1.5 text-[0.9375rem] text-ink-soft transition-colors hover:text-{kleur}">{e(d["naam"])}</a></li>'
        for d in DIENSTEN if d["groep"] == groep)
    meer = [("/ons-werk", "Ons werk"), ("/werkgebied", "Werkgebied"), ("/privacybeleid", "Privacybeleid"), ("/cookiebeleid", "Cookiebeleid")]
    meer_links = "".join(f'<li><a href="{h}" class="block py-1.5 text-[0.9375rem] text-ink-soft transition-colors hover:text-ink">{t}</a></li>' for h, t in meer)
    return f"""</main>
<footer class="border-t border-line-soft bg-paper-soft">
  <div class="frame grid gap-12 py-20 md:grid-cols-12 lg:gap-16">
    <div class="md:col-span-5">
      <img src="/assets/logo/logo-web.png" alt="{NAAM}" width="400" height="104" loading="lazy" class="h-10 w-auto">
      <p class="lede mt-6 text-[1rem]">Dak en zolder, tuin en bomen, overkappingen en aanbouwtjes. Gevestigd in {VESTIGING}, actief in {PLAATSEN_TEKST} en omgeving.</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="tel:{TEL_LINK}" class="btn btn-stil">{TEL}</a>
        <a href="mailto:{MAIL}" class="btn btn-stil">Mail ons</a>
      </div>
    </div>
    <div class="md:col-span-3">
      <p class="label-merk">Dak &amp; zolder</p>
      <ul class="mt-4">{kolom("dak", "merk-ink")}</ul>
      <p class="label-merk mt-8">Aanbouw</p>
      <ul class="mt-4">{kolom("aanbouw", "merk-ink")}</ul>
    </div>
    <div class="md:col-span-2">
      <p class="label-tuin">Tuin &amp; bomen</p>
      <ul class="mt-4">{kolom("tuin", "tuin")}</ul>
    </div>
    <div class="md:col-span-2">
      <p class="label">Meer</p>
      <ul class="mt-4">{meer_links}</ul>
    </div>
  </div>
  <div class="border-t border-line-soft">
    <div class="frame flex flex-wrap items-center justify-between gap-x-8 gap-y-3 py-8 text-[0.8125rem] text-ink-faint">
      <span>{BEDRIJF} &middot; {ADRES} &middot; KvK {KVK}</span>
      <span>&copy; 2026 {NAAM} &middot; Website door <a href="https://maxxmarketing.eu" target="_blank" rel="noopener" class="underline underline-offset-4 hover:text-ink">maxxmarketing.eu</a></span>
    </div>
  </div>
</footer>
<script src="/js/site.js?v={V}" defer></script>
</body>
</html>
"""


def kruimelpad(stappen):
    """stappen: [(naam, href)], de laatste zonder link."""
    delen = []
    for i, (naam, href) in enumerate(stappen):
        if i < len(stappen) - 1:
            delen.append(f'<a href="{href}" class="transition-colors hover:text-ink">{e(naam)}</a><span aria-hidden="true">/</span>')
        else:
            delen.append(f'<span class="text-ink" aria-current="page">{e(naam)}</span>')
    return ('<nav class="mb-8 flex flex-wrap items-center gap-2 text-[0.875rem] text-ink-faint" aria-label="Kruimelpad">'
            + "".join(delen) + "</nav>")


def sectiekop(label, titel, intro="", rechts="", kleur="label"):
    intro_html = f'<p class="lede mt-6">{intro}</p>' if intro else ""
    return f"""<div class="flex flex-col gap-8 md:flex-row md:items-end md:justify-between">
  <div class="max-w-2xl">
    <p class="{kleur}">{e(label)}</p>
    <h2 class="kop-m mt-5">{titel}</h2>
    {intro_html}
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
    {sectiekop("Werkwijze", "Van een eerste idee<br>naar aanpakken.", "Je hoeft nog geen uitgewerkt plan te hebben. Vertel wat je in gedachten hebt, dan kijken we samen verder.")}
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
    opties = '<option value="Weet ik nog niet of meerdere werkzaamheden">Weet ik nog niet of meerdere werkzaamheden</option>'
    for d in DIENSTEN:
        opp = f' data-opp="{d["oppervlakte"]}"' if d["oppervlakte"] else ""
        opties += f'<option value="{e(d["naam"])}"{opp}>{e(d["naam"])}</option>'
    schatting = ""
    for soort, (label, waarden) in OPPERVLAKTE.items():
        keuzes = '<option value="">Kies een schatting</option>' + "".join(f"<option>{e(w)}</option>" for w in waarden)
        schatting += f"""
      <div class="mt-6" data-opp-veld="{soort}" hidden><label for="opp-{soort}" class="label block">{label} (optioneel)</label>
        <select id="opp-{soort}" name="{label}" disabled class="veld mt-3">{keuzes}</select></div>"""
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
          <dt class="label">Vestiging en werkgebied</dt>
          <dd class="mt-2 text-[1rem] leading-relaxed text-ink-soft">Gevestigd in {VESTIGING}. We werken in {PLAATSEN_TEKST} en omgeving.
            <a href="/werkgebied" class="lnk">Bekijk het werkgebied</a></dd>
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
        <div><label for="postcode" class="label block">Postcode van het project</label>
          <input id="postcode" name="postcode" autocomplete="postal-code" required maxlength="7" placeholder="1234 AB" class="veld mt-3"></div>
        <div><label for="plaats" class="label block">Plaats (optioneel)</label>
          <input id="plaats" name="plaats" autocomplete="address-level2" placeholder="Bijvoorbeeld Helmond" class="veld mt-3"></div>
      </div>
      <div class="mt-6"><label for="dienst" class="label block">Wat wil je aanpakken?</label>
        <select id="dienst" name="dienst" class="veld mt-3">{opties}</select></div>{schatting}
      <div class="mt-6"><label for="bericht" class="label block">Vertel kort over je project</label>
        <textarea id="bericht" name="bericht" rows="5" required placeholder="Wat wil je laten doen, en hoe ziet de situatie er nu uit?" class="veld mt-3 resize-y"></textarea>
        <p class="mt-3 text-[0.875rem] leading-relaxed text-ink-faint">Foto's helpen ons veel. Je kunt ze na je aanvraag mailen naar {MAIL}.</p></div>
      <div class="mt-8 flex flex-wrap items-center gap-3">
        <button type="submit" class="btn btn-ink">Verstuur je aanvraag {PIJL}</button>
      </div>
      <p id="form-status" role="status" class="mt-5 text-[0.9375rem] text-merk-ink"></p>
      <p class="mt-6 border-t border-line-soft pt-6 text-[0.875rem] leading-relaxed text-ink-faint">
        Je aanvraag komt direct bij ons binnen. We gebruiken je gegevens alleen om op je aanvraag te reageren.
        Zie ons <a href="/privacybeleid" class="text-ink-soft underline decoration-line underline-offset-4 transition-colors hover:text-merk-ink">privacybeleid</a>.</p>
    </form>
  </div>
</section>"""


def dienstenlijst(actief=None, titel="Alle diensten", kop_html="Alles wat we<br>voor je aanpakken."):
    kolommen = ""
    for g, naam in GROEPEN.items():
        k = ACCENT[g]
        rijen = ""
        for d in DIENSTEN:
            if d["groep"] != g:
                continue
            aan = d["slug"] == actief
            huidig = ' aria-current="page"' if aan else ""
            naamklasse = "text-" + k + " font-medium" if aan else "text-ink-soft"
            rijen += (f'<li><a href="/{d["slug"]}"{huidig} '
                      f'class="group flex items-center justify-between gap-4 border-b border-line-soft py-4 transition-colors hover:text-{k}">'
                      f'<span class="text-[1rem] {naamklasse} group-hover:text-{k}">{e(d["naam"])}</span>'
                      f'<span class="text-ink-faint transition-all group-hover:translate-x-1 group-hover:text-{k}">{PIJL}</span></a></li>')
        kolommen += f'<div><p class="label-{k}">{e(naam)}</p><ul class="mt-5">{rijen}</ul></div>'
    return f"""<section class="bg-white py-20 lg:py-24">
  <div class="frame">
    {sectiekop(titel, kop_html)}
    <div class="mt-14 grid gap-10 md:grid-cols-3 lg:gap-16">{kolommen}</div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Blokken voor de dienstpagina's. Teksten uit _data.py zijn eigen HTML (soms met een link).
P = 'class="mt-4 max-w-reading text-[1.0625rem] leading-[1.8] text-ink-soft"'


def sectie(bg, inhoud):
    return f'<section class="{bg} py-20 lg:py-24">\n  <div class="frame">{inhoud}</div>\n</section>'


def blok_kaarten(b, k):
    _, label, titel, intro, items = b
    cols = "md:grid-cols-2 lg:grid-cols-4" if len(items) == 4 else ("md:grid-cols-3" if len(items) == 3 else "md:grid-cols-2")
    kaarten = "".join(f"""<li class="kaart p-8">
  <h3 class="kop-s">{e(t)}</h3>
  <p class="mt-3 text-[1rem] leading-relaxed text-ink-soft">{o}</p>
</li>""" for t, o in items)
    return sectiekop(label, e(titel), e(intro) if intro else "", "", f"label-{k}") + f'<ul class="mt-12 grid gap-6 {cols}">{kaarten}</ul>'


def lijst_html(items, k):
    return "".join(f'<li class="flex gap-3 border-b border-line-soft py-4 text-[1.0625rem] leading-relaxed text-ink-soft"><span class="text-{k}">{VINK}</span><span>{e(i)}</span></li>' for i in items)


def blok_lijst(b, k):
    _, label, titel, intro, items = b
    intro_html = f'<p class="lede mt-6">{e(intro)}</p>' if intro else ""
    return f"""<div class="grid gap-12 md:grid-cols-12 lg:gap-20">
  <div class="md:col-span-5"><p class="label-{k}">{e(label)}</p><h2 class="kop-m mt-5">{e(titel)}</h2>{intro_html}</div>
  <ul class="border-t border-line-soft md:col-span-7">{lijst_html(items, k)}</ul>
</div>"""


def blok_prijs(b, k):
    _, label, titel, intro, items = b
    intro = intro or "Een prijs noemen we pas als we jouw situatie kennen. Deze punten bepalen de kosten:"
    return blok_lijst(("lijst", label, titel, intro, items), k)


def blok_vergelijk(b, k):
    _, label, titel, intro, kolommen = b
    kaarten = "".join(f"""<div class="kaart p-8 lg:p-10">
  <h3 class="kop-s">{e(t)}</h3>
  <p class="mt-3 text-[1rem] leading-relaxed text-ink-soft">{e(o)}</p>
  <ul class="mt-6 border-t border-line-soft">{lijst_html(items, k)}</ul>
</div>""" for t, o, items in kolommen)
    return sectiekop(label, e(titel), e(intro) if intro else "", "", f"label-{k}") + f'<div class="mt-12 grid gap-6 md:grid-cols-2">{kaarten}</div>'


def blok_tekst(b, k):
    _, label, titel, alineas = b
    tekst = "".join(f"<p {P}>{a}</p>" for a in alineas)
    return f"""<div class="grid gap-12 md:grid-cols-12 lg:gap-20">
  <div class="md:col-span-5"><p class="label-{k}">{e(label)}</p><h2 class="kop-m mt-5">{e(titel)}</h2></div>
  <div class="md:col-span-7">{tekst}</div>
</div>"""


def blok_regio(b, k):
    _, label, titel, tekst = b
    return blok_tekst(("tekst", label, titel, [e(tekst), 'Zet je postcode en de geschatte oppervlakte in je aanvraag. <a href="/werkgebied" class="lnk">Bekijk het werkgebied</a>.']), k)


def blok_info(b, k, d):
    _, label, titel, intro, items = b
    rijen = "".join(f'<li class="flex gap-4 border-b border-line-soft py-4 text-[1.0625rem] leading-relaxed text-ink-soft"><span class="label-{k} mt-1.5 w-6 shrink-0">{i:02d}</span><span>{e(t)}</span></li>'
                    for i, t in enumerate(items, 1))
    return f"""<div class="grid gap-12 md:grid-cols-12 lg:gap-20">
  <div class="md:col-span-5">
    <p class="label-{k}">{e(label)}</p><h2 class="kop-m mt-5">{e(titel)}</h2>
    <p class="lede mt-6">Je hoeft niet alles te weten. Wat je wel weet, helpt om je aanvraag goed te beoordelen. Foto's kun je na je aanvraag mailen.</p>
    <a href="/#contact" data-keuze="{e(d["naam"])}" class="btn btn-{k} mt-8">{e(d["actie"])} {PIJL}</a>
  </div>
  <ol class="border-t border-line-soft md:col-span-7">{rijen}</ol>
</div>"""


def blok_combi(b, k):
    _, label, titel, items = b
    kaarten = "".join(f"""<a href="/{s}" class="kaart kaart-hover group flex flex-col p-8">
  <span class="kop-s transition-colors group-hover:text-{ACCENT[D[s]["groep"]]}">{e(D[s]["naam"])}</span>
  <span class="mt-3 flex-1 text-[1rem] leading-relaxed text-ink-soft">{e(waarom)}</span>
  <span class="link-pijl mt-6 text-[0.9375rem] text-ink">Lees meer over {e(D[s]["naam"].lower())} {PIJL}</span>
</a>""" for s, waarom in items)
    return sectiekop(label, e(titel), "", "", f"label-{k}") + f'<div class="mt-12 grid gap-6 md:grid-cols-2">{kaarten}</div>'


def blok_vragen(b, k):
    _, label, titel, items = b
    rijen = "".join(f"""<div class="border-b border-line-soft py-7">
  <h3 class="text-[1.125rem] font-medium text-ink">{e(v)}</h3>
  <p class="mt-3 max-w-reading text-[1rem] leading-relaxed text-ink-soft">{a}</p>
</div>""" for v, a in items)
    return f"""<div class="grid gap-12 md:grid-cols-12 lg:gap-20">
  <div class="md:col-span-5"><p class="label-{k}">{e(label)}</p><h2 class="kop-m mt-5">{e(titel)}</h2></div>
  <div class="border-t border-line-soft md:col-span-7">{rijen}</div>
</div>"""


BLOKKEN = {"kaarten": blok_kaarten, "lijst": blok_lijst, "prijs": blok_prijs, "vergelijk": blok_vergelijk,
           "tekst": blok_tekst, "regio": blok_regio, "combi": blok_combi, "vragen": blok_vragen}


# ---------------------------------------------------------------------------
def home():
    def pijler(groep, kleur, foto, titel, tekst, slugs, eager):
        links = "".join(
            f'<a href="/{s}" class="link-pijl rounded-lg px-3 py-2 text-[0.9375rem] text-ink-soft transition-colors hover:bg-{kleur}/5 hover:text-{kleur}">{e(D[s]["naam"])} {PIJL}</a>'
            for s in slugs)
        return f"""<article class="group flex flex-col">
  <div class="overflow-hidden rounded-2xl">
    {img(foto, "beeld aspect-[4/5] transition-transform duration-700 ease-out group-hover:scale-[1.02]", "(min-width: 768px) 50vw, 100vw", eager)}
  </div>
  <div class="mt-8 flex flex-1 flex-col">
    <p class="label-{kleur}">{e(GROEPEN[groep])}</p>
    <h2 class="kop-m mt-4">{titel}</h2>
    <p class="lede mt-5 text-[1rem]">{e(tekst)}</p>
    <div class="mt-7 flex flex-wrap gap-1 border-t border-line-soft pt-5">{links}</div>
    <a href="/#contact" class="btn btn-{kleur} mt-8 self-start">Bespreek je plannen {PIJL}</a>
  </div>
</article>"""

    diensten_rijen = "".join(f"""<a href="/{d["slug"]}" class="kaart kaart-hover group flex items-start gap-6 p-7 lg:p-8">
  <span class="label-{ACCENT[d["groep"]]} mt-1 shrink-0">{d["nr"]}</span>
  <span class="min-w-0 flex-1">
    <span class="kop-s block transition-colors group-hover:text-{ACCENT[d["groep"]]}">{e(d["naam"])}</span>
    <span class="mt-2 block text-[0.9375rem] leading-relaxed text-ink-soft">{e(d["kort"])}</span>
  </span>
  <span class="mt-1 shrink-0 text-ink-faint transition-all group-hover:translate-x-1 group-hover:text-{ACCENT[d["groep"]]}">{PIJL}</span>
</a>""" for d in DIENSTEN)

    projecten = "".join(f"""<article class="group">
  <div class="overflow-hidden rounded-2xl">
    {img(p["foto"], "beeld aspect-[4/3] transition-transform duration-700 ease-out group-hover:scale-[1.02]", "(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw")}
  </div>
  <h3 class="kop-s mt-6">{e(p["titel"])}</h3>
  <p class="mt-2 text-[0.9375rem] leading-relaxed text-ink-soft">{e(p["tekst"])}</p>
  <a href="/{p["dienst"]}" class="link-pijl mt-4 text-[0.9375rem] text-ink hover:text-merk-ink">{e(D[p["dienst"]]["naam"])} {PIJL}</a>
</article>""" for p in PROJECTEN)

    plaatsen = "".join(f'<li class="rounded-xl border border-line bg-white px-5 py-3 text-[1rem] text-ink">{e(p)}</li>' for p in PLAATSEN)
    alle_fotos_link = f'<a href="/ons-werk" class="link-pijl shrink-0 text-ink hover:text-merk-ink">{ALLE_FOTOS} {PIJL}</a>'
    ons_werk_link = f'<a href="/ons-werk" class="link-pijl shrink-0 text-ink hover:text-merk-ink">Bekijk ons werk {PIJL}</a>'

    body = f"""<section class="bg-white pb-20 pt-16 lg:pb-28 lg:pt-24">
  <div class="frame">
    <div class="grid items-center gap-12 md:grid-cols-12 lg:gap-16">
      <div class="md:col-span-7">
        <p class="label">{NAAM} &middot; {VESTIGING}</p>
        <h1 class="kop-xl mt-6 text-[clamp(2.75rem,5.4vw,4.75rem)]">Vakwerk aan je dak.<br>Rust in je tuin.</h1>
        <p class="lede mt-8 text-[1.125rem] sm:text-[1.25rem]">
          Dakwerken, dakisolatie en zolders. Tuinaanleg, tuinrenovatie en bomen. Overkappingen en aanbouwtjes. Eén aanspreekpunt vanuit {VESTIGING}, voor Eindhoven, Helmond en omgeving.</p>
        <div class="mt-10 flex flex-wrap gap-3">
          <a href="#contact" class="btn btn-ink">Bespreek je project {PIJL}</a>
          <a href="#diensten" class="btn btn-stil">Bekijk de diensten</a>
        </div>
      </div>
      <figure class="md:col-span-5">
        <div class="relative aspect-[4/3] overflow-hidden rounded-2xl bg-paper-warm shadow-lift md:aspect-[4/5]">
          <img src="/assets/video/hero-poster.webp" alt="Schuin dak in opbouw met een vakman op de steiger, eigen werk van {NAAM}" width="864" height="1080" fetchpriority="high" class="absolute inset-0 h-full w-full object-cover">
          <!-- Alleen op desktop en zonder 'beweging beperken' laadt site.js de video -->
          <video id="hero-video" data-src="/assets/video/hero-loop.mp4" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"
            class="absolute inset-0 h-full w-full object-cover opacity-0 transition-opacity duration-700"></video>
          <button type="button" id="hero-video-knop" hidden aria-pressed="false"
            class="absolute bottom-4 right-4 rounded-xl bg-white/85 px-4 py-2 text-[0.875rem] font-medium text-ink shadow-lift backdrop-blur transition-colors hover:bg-white">Pauzeer video</button>
        </div>
        <figcaption class="label mt-4">Eigen werk: dak, zolder, overkapping en tuin</figcaption>
      </figure>
    </div>

    <div class="mt-20 grid gap-12 md:grid-cols-2 lg:mt-24 lg:gap-16">
      {pijler("dak", "merk", "dakwerk", "Alles boven<br>je hoofd.",
              "Van een dak dat aandacht nodig heeft tot een zolder waar je echt iets mee kunt. We beginnen bij het dak en werken naar binnen.",
              ["dakwerken", "dakisolatie", "zolder"], False)}
      {pijler("tuin", "tuin", "tuin-1", "Buiten wordt<br>een plek om<br>te blijven.",
              "Een nieuwe tuin, een bestaande tuin die toe is aan vernieuwing, of een boom die weg moet. Voor grotere tuinprojecten komen we ook buiten de regio.",
              ["tuinaanleg", "tuinrenovatie", "bomen-verwijderen"], False)}
    </div>

    <article class="kaart kaart-hover mt-12 grid items-center gap-10 overflow-hidden p-8 md:grid-cols-12 lg:mt-16 lg:p-12">
      <div class="md:col-span-5">
        <p class="label-merk">De verbinding</p>
        <h2 class="kop-m mt-4">Overkappingen<br>en aanbouwtjes.</h2>
        <p class="lede mt-5 text-[1rem]">Daar waar het huis de tuin raakt. Beschut buiten zitten onder een overkapping, of wat extra ruimte aan huis met een aanbouwtje.</p>
        <a href="/overkappingen-aanbouw" class="btn btn-stil mt-7">Overkappingen en aanbouwtjes {PIJL}</a>
      </div>
      <div class="md:col-span-7">
        {img("overkapping-6", "beeld aspect-[16/9]", "(min-width: 768px) 55vw, 100vw")}
      </div>
    </article>
  </div>
</section>

<section id="diensten" class="bg-paper-soft py-20 lg:py-28">
  <div class="frame">
    {sectiekop("Diensten", "Zeven dingen<br>die we voor je doen.",
               "Op elke dienstpagina lees je voor welke situaties de dienst bedoeld is, welke keuzes er spelen, waar de prijs van afhangt en wat je in je aanvraag kunt zetten.",
               ons_werk_link)}
    <div class="mt-14 grid gap-5 md:grid-cols-2 lg:gap-6">{diensten_rijen}</div>
  </div>
</section>

<section class="bg-white py-20 lg:py-28">
  <div class="frame">
    {sectiekop("Ons werk", "Eigen werk,<br>eigen foto's.",
               "Geen stockbeelden. Deze foto's komen uit onze eigen projecten, een deel is gemaakt tijdens de uitvoering.",
               alle_fotos_link)}
    <div class="mt-14 grid gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">{projecten}</div>
  </div>
</section>

<section class="bg-paper-soft py-20 lg:py-24">
  <div class="frame grid items-center gap-12 md:grid-cols-12 lg:gap-20">
    <div class="md:col-span-6">
      <p class="label">Werkgebied</p>
      <h2 class="kop-m mt-5">Vanuit {VESTIGING},<br>in de regio Eindhoven.</h2>
      <p class="lede mt-6">Ons vaste werkgebied, plus de plaatsen daaromheen in Noord-Brabant. Grotere projecten verder weg zijn bespreekbaar, vooral voor tuinaanleg en tuinrenovatie.</p>
      <a href="/werkgebied" class="btn btn-stil mt-8">Bekijk het werkgebied {PIJL}</a>
    </div>
    <ul class="flex flex-wrap gap-3 md:col-span-6">{plaatsen}</ul>
  </div>
</section>

{aanpak_sectie()}
{vragen_sectie()}
{formulier()}"""
    ld = ld_script([bedrijf_ld(), {"@type": "WebSite", "@id": DOMEIN + "/#website", "url": DOMEIN + "/", "name": NAAM,
                                   "inLanguage": "nl-NL", "publisher": {"@id": BEDRIJF_ID}}])
    (OUT / "index.html").write_text(
        kop("Dak, tuin en overkapping in regio Eindhoven | Bouwpartners Eindhoven",
            f"{NAAM} uit {VESTIGING}: dakwerken, dakisolatie, zolders, tuinaanleg, tuinrenovatie, bomen en overkappingen. Eén aanspreekpunt in de regio Eindhoven.",
            "", ld=ld) + navigatie() + body + voet(), encoding="utf-8")


def dienstpagina(d):
    k = ACCENT[d["groep"]]
    fotos = d["fotos"]

    hoofdfoto = ""
    if fotos:
        hoofdfoto = (f'<div class="md:col-span-6">{img(fotos[0], "beeld aspect-[4/5] shadow-lift", "(min-width: 768px) 45vw, 100vw", True)}'
                     + ('<p class="label mt-4">Foto tijdens het werk</p>' if in_uitvoering(fotos[0]) else "") + "</div>")

    secties, bg = [], ["bg-paper-soft", "bg-white"]
    for i, b in enumerate(d["blokken"]):
        inhoud = blok_info(b, k, d) if b[0] == "info" else BLOKKEN[b[0]](b, k)
        secties.append(sectie(bg[i % 2], inhoud))
        # Foto's halverwege de pagina, zodat de tekst niet in één blok staat
        if i == 1 and len(fotos) > 1:
            fig = "".join(f"""<figure class="overflow-hidden">
  {img(n, "beeld aspect-[4/3]", "(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw")}
  <figcaption class="mt-3 text-[0.875rem] leading-relaxed text-ink-faint">{e(FOTO[n][0])}{" (tijdens het werk)" if in_uitvoering(n) else ""}</figcaption>
</figure>""" for n in fotos[1:])
            alle = f'<a href="/ons-werk" class="link-pijl shrink-0 text-ink hover:text-{k}">{ALLE_FOTOS} {PIJL}</a>'
            secties.append(f"""<section class="border-t border-line-soft bg-white py-20 lg:py-24">
  <div class="frame">
    {sectiekop("Eigen werk", "Uit onze projecten.", "", alle, f"label-{k}")}
    <div class="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">{fig}</div>
  </div>
</section>""")

    verder = " Voor grotere tuinprojecten komen we ook verder." if d["groep"] == "tuin" else ""
    body = f"""<section class="bg-white py-16 lg:py-24">
  <div class="frame grid items-center gap-12 md:grid-cols-12 lg:gap-20">
    <div class="min-w-0 {'md:col-span-6' if hoofdfoto else 'md:col-span-9'}">
      {kruimelpad([("Home", "/"), ("Diensten", "/#diensten"), (d["naam"], "")])}
      <p class="label-{k}">{e(GROEPEN[d["groep"]])}</p>
      <h1 class="kop-l mt-5">{e(d["h1"])}</h1>
      <p class="lede mt-7 text-[1.125rem]">{e(d["intro"])}</p>
      <div class="mt-10 flex flex-wrap gap-3">
        <a href="/#contact" data-keuze="{e(d["naam"])}" class="btn btn-{k}">{e(d["actie"])} {PIJL}</a>
        <a href="tel:{TEL_LINK}" class="btn btn-stil">Bel {TEL}</a>
      </div>
    </div>
    {hoofdfoto}
  </div>
</section>

{"".join(secties)}

<section class="bg-ink py-20 text-white lg:py-24">
  <div class="frame flex flex-col items-start gap-10 md:flex-row md:items-center md:justify-between">
    <div class="max-w-xl">
      <p class="label text-white/60">Vanuit {VESTIGING}</p>
      <h2 class="kop-m mt-4 text-white">Een eerste idee<br>is genoeg.</h2>
      <p class="mt-5 text-[1rem] leading-relaxed text-white/70">We werken in {PLAATSEN_TEKST} en de plaatsen daaromheen.{verder}
        <a href="/werkgebied" class="text-white underline decoration-white/30 underline-offset-4 hover:decoration-white">Bekijk het werkgebied</a>.</p>
    </div>
    <a href="/#contact" data-keuze="{e(d["naam"])}" class="btn btn-{k} shrink-0">{e(d["actie"])} {PIJL}</a>
  </div>
</section>

{dienstenlijst(d["slug"], "Andere diensten", "Ook voor je huis<br>en tuin.")}"""

    dienst_ld = {"@type": "Service", "@id": DOMEIN + "/" + d["slug"] + "#dienst", "name": d["naam"], "serviceType": d["naam"],
                 "description": d["meta"], "url": DOMEIN + "/" + d["slug"],
                 "provider": {"@type": "HomeAndConstructionBusiness", "@id": BEDRIJF_ID, "name": NAAM, "url": DOMEIN + "/",
                              "telephone": TEL_LINK, "address": ADRES_LD},
                 "areaServed": GEBIED_LD}
    ld = ld_script([dienst_ld, kruimel_ld([("Home", ""), (d["naam"], d["slug"])])])
    (OUT / f'{d["slug"]}.html').write_text(
        kop(d["titel"], d["meta"], d["slug"], ld=ld, ogbeeld=fotos[0] if fotos else "tuin-1") + navigatie() + body + voet(),
        encoding="utf-8")


def werkgebied():
    plaatsen = "".join(f"""<li class="kaart p-7">
  <span class="kop-s">{e(p)}</span>
  {'<span class="label-merk mt-2 block">Vestigingsplaats</span>' if p == VESTIGING else ''}
</li>""" for p in PLAATSEN)
    tuin_links = " en ".join(f'<a href="/{s}" class="lnk">{e(D[s]["naam"].lower())}</a>' for s in ["tuinaanleg", "tuinrenovatie"])
    body = f"""<section class="bg-white py-16 lg:py-24">
  <div class="frame">
    {kruimelpad([("Home", "/"), ("Werkgebied", "")])}
    <div class="max-w-3xl">
      <p class="label">Werkgebied</p>
      <h1 class="kop-l mt-5">Vanuit {VESTIGING} aan het werk in de regio Eindhoven</h1>
      <p class="lede mt-7 text-[1.125rem]">{NAAM} is gevestigd in {VESTIGING}. Van daaruit werken we in de plaatsen hieronder en in de plaatsen daaromheen in Noord-Brabant.</p>
    </div>
    <ul class="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{plaatsen}</ul>
  </div>
</section>

<section class="bg-paper-soft py-20 lg:py-24">
  <div class="frame grid gap-12 md:grid-cols-12 lg:gap-20">
    <div class="md:col-span-5"><p class="label">Daarbuiten</p><h2 class="kop-m mt-5">Net buiten de lijst,<br>of verder weg.</h2></div>
    <div class="md:col-span-7">
      <p {P}>Woon je in een plaats in de buurt die hier niet staat? Vraag het gewoon. De lijst hierboven is ons vaste werkgebied, geen harde grens.</p>
      <p {P}>Projecten verder weg zijn bespreekbaar. Of het kan, hangt af van de locatie en de omvang van het werk. Voor grotere projecten in {tuin_links} rijden we eerder verder.</p>
      <p {P}>Zet de postcode van het project in je aanvraag. Dan laten we weten wat er mogelijk is.</p>
      <a href="/#contact" class="btn btn-ink mt-8">Bespreek je project {PIJL}</a>
    </div>
  </div>
</section>

{dienstenlijst(None, "Diensten in het werkgebied", "Wat we in de regio<br>voor je doen.")}"""
    ld = ld_script([bedrijf_ld(), kruimel_ld([("Home", ""), ("Werkgebied", "werkgebied")])])
    (OUT / "werkgebied.html").write_text(
        kop("Werkgebied Asten, Eindhoven en Helmond | Bouwpartners Eindhoven",
            f"Gevestigd in {VESTIGING}, actief in {PLAATSEN_TEKST} en omgeving in Noord-Brabant. Grotere projecten verder weg zijn bespreekbaar.",
            "werkgebied", ld=ld) + navigatie() + body + voet(), encoding="utf-8")


def ons_werk():
    knop = ('class="rounded-xl border border-line bg-white px-5 py-2.5 text-[0.9375rem] text-ink-soft transition-all '
            'hover:border-ink/25 aria-pressed:border-ink aria-pressed:bg-ink aria-pressed:text-white"')
    knoppen = f'<button type="button" data-soort="alles" aria-pressed="true" {knop}>Alles</button>'
    knoppen += "".join(f'<button type="button" data-soort="{s}" aria-pressed="false" {knop}>{n}</button>' for s, n, _, _ in WERK)
    kolommen = [[(s, n, dienst, f) for f in fs] for s, n, dienst, fs in WERK]
    volgorde = []
    while any(kolommen):
        for k in kolommen:
            if k:
                volgorde.append(k.pop(0))
    fig = "".join(f"""<figure data-soort="{s}" class="group">
  <div class="overflow-hidden rounded-2xl">
    {img(f, "beeld aspect-square transition-transform duration-700 ease-out group-hover:scale-[1.03]", "(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw")}
  </div>
  <figcaption class="mt-4">
    <span class="flex items-center justify-between gap-3"><a href="/{dienst}" class="text-[0.9375rem] font-medium text-ink hover:text-merk-ink">{e(D[dienst]["naam"])}</a>{'<span class="label shrink-0">Tijdens het werk</span>' if in_uitvoering(f) else ''}</span>
    <span class="mt-1 block text-[0.875rem] leading-relaxed text-ink-faint">{e(FOTO[f][0])}</span>
  </figcaption>
</figure>""" for s, n, dienst, f in volgorde)
    body = f"""<section class="bg-white py-16 lg:py-24">
  <div class="frame">
    {kruimelpad([("Home", "/"), ("Ons werk", "")])}
    <div class="max-w-3xl">
      <p class="label">Ons werk</p>
      <h1 class="kop-l mt-5">Werk dat we zelf hebben gedaan.</h1>
      <p class="lede mt-7 text-[1.125rem]">Daken, zolders, tuinen en overkappingen. Alle foto's op deze pagina komen uit onze eigen projecten. Bij foto's die tijdens de uitvoering zijn gemaakt, staat dat erbij.</p>
    </div>
    <div class="mt-12 flex flex-wrap gap-3">{knoppen}</div>
    <div class="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3 lg:gap-10" id="werk-raster">{fig}</div>
  </div>
</section>

<section class="bg-paper-soft py-20 lg:py-24">
  <div class="frame flex flex-col items-start gap-10 md:flex-row md:items-center md:justify-between">
    <div class="max-w-xl"><p class="label">Jouw idee is het begin</p><h2 class="kop-m mt-4">Zoiets ook<br>bij jou?</h2></div>
    <a href="/#contact" class="btn btn-ink shrink-0">Bespreek je project {PIJL}</a>
  </div>
</section>

{dienstenlijst()}"""
    ld = ld_script([kruimel_ld([("Home", ""), ("Ons werk", "ons-werk")])])
    (OUT / "ons-werk.html").write_text(
        kop("Ons werk: foto's van eigen projecten | Bouwpartners Eindhoven",
            f"Foto's van eigen werk van {NAAM}: daken en zolders tijdens de uitvoering, aangelegde tuinen en houten overkappingen.",
            "ons-werk", ld=ld, ogbeeld="overkapping-6")
        + navigatie() + body + voet(), encoding="utf-8")


H2 = 'class="kop-s mt-12 first:mt-0"'
A = 'class="text-ink underline decoration-line underline-offset-4 transition-colors hover:text-merk-ink"'


def tekstpagina(bestand, titel, omschrijving, h1, label, inhoud, noindex=False):
    pad = bestand.replace(".html", "")
    body = f"""<section class="bg-white py-16 lg:py-20">
  <div class="frame">
    {kruimelpad([("Home", "/"), (label, "")])}
    <h1 class="kop-l max-w-3xl">{h1}</h1>
  </div>
</section>
<section class="border-t border-line-soft bg-white pb-24 pt-16">
  <div class="frame grid gap-12 md:grid-cols-12 lg:gap-20">
    <div class="md:col-span-3"><p class="label md:sticky md:top-28">{e(label)}</p></div>
    <div class="min-w-0 md:col-span-9">{inhoud}</div>
  </div>
</section>"""
    ld = "" if noindex else ld_script([kruimel_ld([("Home", ""), (label, pad)])])
    (OUT / bestand).write_text(
        kop(titel, omschrijving, pad, noindex, ld=ld) + navigatie() + body + voet(), encoding="utf-8")


def rest():
    tekstpagina("privacybeleid.html", "Privacybeleid | Bouwpartners Eindhoven",
                "Welke gegevens Bouwpartners Eindhoven ontvangt via het formulier, waarvoor we ze gebruiken, hoe lang we ze bewaren en welke rechten je hebt.",
                "Privacybeleid.", "Privacybeleid", f"""
<p class="label">Laatst bijgewerkt op 6 oktober 2026</p>
<p {P}>{NAAM} vindt het belangrijk dat je weet wat er met je gegevens gebeurt. Deze verklaring legt uit welke gegevens we krijgen, waarom we ze gebruiken en welke rechten je hebt.</p>
<h2 {H2}>Wie verantwoordelijk is</h2>
<p {P}>{BEDRIJF}, {ADRES}, KvK {KVK}, is verwerkingsverantwoordelijke voor de verwerking van je persoonsgegevens. Vragen hierover kun je mailen naar <a href="mailto:{MAIL}" {A}>{MAIL}</a> of bellen via <a href="tel:{TEL_LINK}" {A}>{TEL}</a>.</p>
<h2 {H2}>Welke gegevens we verwerken</h2>
<p {P}>Vul je het formulier op deze website in, dan ontvangen we per e-mail je naam, je e-mailadres, de postcode en eventueel de plaats van het project, de gekozen dienst, een eventuele schatting van de oppervlakte en je bericht. De website zelf slaat niets op. Bel je ons of mail je ons rechtstreeks, dan verwerken we de gegevens die je ons in dat contact geeft, zoals je telefoonnummer, foto's en het adres van het werk.</p>
<h2 {H2}>Waarom we ze gebruiken en op welke grond</h2>
<p {P}>We gebruiken je gegevens alleen om op je aanvraag te reageren, je vraag te beantwoorden en je project met je te bespreken. De postcode gebruiken we om te beoordelen of het project in ons werkgebied ligt. De grondslag daarvoor is de uitvoering van een overeenkomst of de stappen die daaraan voorafgaan op jouw verzoek. Wordt het een opdracht, dan gebruiken we je gegevens ook om die uit te voeren en te factureren; daarvoor geldt daarnaast onze wettelijke administratieplicht. We verkopen je gegevens niet, gebruiken ze niet voor reclame en nemen geen besluiten over je op basis van geautomatiseerde verwerking.</p>
<h2 {H2}>Wie je gegevens nog meer ziet</h2>
<p {P}>Berichten via het formulier worden doorgestuurd door FormSubmit (formsubmit.co) en komen binnen in onze e-mail. Die wordt geleverd door Google (Gmail). Verder delen we je gegevens niet met anderen, behalve wanneer dat nodig is om het werk uit te voeren of wanneer de wet ons daartoe verplicht, bijvoorbeeld tegenover onze boekhouder of de Belastingdienst. Onze website staat op een server binnen de Europese Unie en laadt geen onderdelen van andere websites. Voor zover gegevens via onze e-mail of FormSubmit buiten de Europese Unie worden verwerkt, gebeurt dat op basis van de standaardbepalingen die de Europese Commissie daarvoor heeft vastgesteld.</p>
<h2 {H2}>Hoe lang we ze bewaren</h2>
<p {P}>We bewaren je aanvraag zolang dat nodig is om je te helpen. Wordt het geen opdracht, dan verwijderen we je gegevens uiterlijk een jaar na je aanvraag. Wordt het wel een opdracht, dan bewaren we de administratie zeven jaar, omdat de Belastingdienst dat van ons vraagt.</p>
<h2 {H2}>Hoe we ze beveiligen</h2>
<p {P}>Onze website gebruikt een beveiligde verbinding (https). Je aanvraag komt binnen in een e-mailaccount dat met een wachtwoord en tweestapsverificatie is afgeschermd. Alleen de mensen die aan je project werken hebben toegang tot je gegevens.</p>
<h2 {H2}>Cookies</h2>
<p {P}>Deze website plaatst geen cookies en gebruikt geen analytics of trackers. Lees meer in ons <a href="/cookiebeleid" {A}>cookiebeleid</a>.</p>
<h2 {H2}>Jouw rechten</h2>
<p {P}>Je mag je gegevens inzien, laten aanpassen, laten verwijderen of de verwerking laten beperken. Je mag ook bezwaar maken tegen de verwerking en vragen om je gegevens over te dragen. Mail daarvoor naar <a href="mailto:{MAIL}" {A}>{MAIL}</a>; we reageren binnen een maand. Ben je niet tevreden over hoe we met je gegevens omgaan, dan kun je een klacht indienen bij de Autoriteit Persoonsgegevens via autoriteitpersoonsgegevens.nl.</p>
<h2 {H2}>Wijzigingen</h2>
<p {P}>Verandert er iets aan deze website of aan de manier waarop we met gegevens omgaan, dan passen we deze verklaring aan. Bovenaan staat wanneer dat voor het laatst gebeurd is.</p>
""")
    tekstpagina("cookiebeleid.html", "Cookiebeleid | Bouwpartners Eindhoven",
                "Bouwpartners Eindhoven plaatst geen cookies en gebruikt geen analytics of trackers. Lees wat dat betekent en wat er gebeurt als dat verandert.",
                "Cookiebeleid.", "Cookiebeleid", f"""
<p class="label">Laatst bijgewerkt op 5 oktober 2026</p>
<h2 {H2}>Deze website plaatst geen cookies</h2>
<p {P}>Je kunt deze website bekijken zonder dat er iets op je computer, telefoon of tablet wordt opgeslagen. We gebruiken geen functionele, analytische of trackingcookies. Alleen als je op een dienstpagina op een aanvraagknop klikt, onthoudt je browser tijdelijk welke dienst je koos, zodat die alvast in het formulier staat. Dat wordt gewist zodra je het tabblad sluit en wordt niet naar ons of anderen gestuurd.</p>
<h2 {H2}>Daarom zie je geen cookiemelding</h2>
<p {P}>Een cookiemelding is bedoeld om je toestemming te vragen voor cookies die niet strikt noodzakelijk zijn. Omdat we die niet plaatsen, is er niets om toestemming voor te vragen. Een melding tonen zou alleen maar in de weg zitten.</p>
<h2 {H2}>Geen onderdelen van andere websites</h2>
<p {P}>Alle lettertypen, afbeeldingen en scripts op deze website worden vanaf onze eigen server geladen. Er zijn geen knoppen van sociale media, geen video's van andere websites en geen advertentienetwerken. Daardoor krijgen andere partijen je IP-adres niet te zien als je deze website bezoekt.</p>
<h2 {H2}>Statistieken</h2>
<p {P}>We gebruiken geen Google Analytics of een vergelijkbare bezoekersteller. Onze website is wel aangemeld bij Google Search Console. Daarmee zien we welke zoekopdrachten naar onze website leiden; dat gebeurt aan de kant van Google en plaatst niets in jouw browser.</p>
<h2 {H2}>Als dit verandert</h2>
<p {P}>Gaan we in de toekomst wel statistieken of advertentiepixels gebruiken, dan vragen we daarvoor eerst je toestemming via een cookiemelding en passen we deze pagina aan. Zie ook ons <a href="/privacybeleid" {A}>privacybeleid</a>.</p>
""")
    tekstpagina("404.html", "Pagina niet gevonden | Bouwpartners Eindhoven", "Deze pagina bestaat niet (meer).",
                "Deze pagina bestaat niet.", "Fout 404",
                f'<p {P}>De pagina is verplaatst of het adres klopt niet. Misschien vind je hier wat je zocht:</p>'
                + '<ul class="mt-6 grid gap-x-10 sm:grid-cols-2">'
                + "".join(f'<li><a href="/{d["slug"]}" class="block border-b border-line-soft py-3 text-[1rem] text-ink-soft hover:text-merk-ink">{e(d["naam"])}</a></li>' for d in DIENSTEN)
                + '<li><a href="/werkgebied" class="block border-b border-line-soft py-3 text-[1rem] text-ink-soft hover:text-merk-ink">Werkgebied</a></li></ul>'
                + f'<p class="mt-10"><a href="/" class="btn btn-ink">Naar de homepage {PIJL}</a></p>', True)

    # Alleen de pagina's die in Google moeten staan
    paginas = [""] + [d["slug"] for d in DIENSTEN] + ["werkgebied", "ons-werk"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMEIN}/{p}</loc></url>\n" for p in paginas) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMEIN}/sitemap.xml\n")
    vercel = {
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            # Het vercel.app-adres en previews niet laten indexeren; alleen bouwpartnerseindhoven.nl telt
            {"source": "/(.*)", "has": [{"type": "host", "value": "(?<project>.*)\\.vercel\\.app"}],
             "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]},
            {"source": "/assets/fonts/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/assets/images/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
            {"source": "/assets/video/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
        ],
    }
    (OUT / "vercel.json").write_text(json.dumps(vercel, indent=2) + "\n")


if __name__ == "__main__":
    home()
    for d in DIENSTEN:
        dienstpagina(d)
    werkgebied()
    ons_werk()
    rest()
    print("Gebouwd:", ", ".join(sorted(p.name for p in OUT.glob("*.html"))))
