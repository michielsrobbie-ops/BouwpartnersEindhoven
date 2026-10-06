# Bouwpartners Eindhoven — website

Lichte, rustige opzet. Wit als basis, stone-50 voor de rustige secties, de oranje uit het logo (#FB6A1E) voor dak en aanbouw, emerald-700 voor tuin.

## Opbouw
- `_data.py` bevat alle teksten: diensten (met hun blokken), foto's met alt-teksten, projecten, werkgebied en vragen. Daar pas je de inhoud aan.
- `build.py` zet die inhoud om in de pagina's, plus sitemap.xml, robots.txt en vercel.json. Werkt met Python 3.9 en nieuwer.
- `src/input.css` + `tailwind.config.js` zijn de bron van de stijl; `css/site.css` is het gecompileerde resultaat.
- `js/site.js` doet het menu, het projectfilter, de dienstkeuze en het formulier.
- `assets/fonts/` bevat de lettertypen lokaal: Plus Jakarta Sans (koppen), Outfit (tekst), Space Grotesk (labels).
- `build.py` maakt van elke grote foto een 800px-variant (`naam-800.webp`) voor mobiel en een klein logo (`logo-web.png`). Daarvoor is Pillow nodig; zonder Pillow gebruikt hij de bewaarde maten in `assets/images/maten.json`.

## Opnieuw bouwen
```
npm install                 # eenmalig
python3 build.py
npx tailwindcss -i src/input.css -o css/site.css --minify
python3 serve.py            # lokale preview op http://localhost:8000, met dezelfde nette URL's als Vercel
```
Hoog na een wijziging in CSS of JS het nummer `V` in build.py op, anders zien bezoekers de oude versie uit hun cache.

## Publiceren
- `.vercelignore` werkt als allowlist: alleen html, css, js, assets, robots.txt, sitemap.xml en vercel.json gaan naar Vercel. Bronbestanden, docs, back-ups en het prototype blijven lokaal en in git.
- Controleer na elke deploy dat https://bouwpartnerseindhoven.nl/build.py en /docs/open-vragen-klant.md een 404 geven.
- `vercel.json` zet `X-Robots-Tag: noindex` op alle *.vercel.app-adressen. Previews krijgen dat ook al automatisch van Vercel. Alleen bouwpartnerseindhoven.nl wordt geïndexeerd.
- Interne links zijn schone URL's (`/dakwerken`), canonicals wijzen naar https://bouwpartnerseindhoven.nl.

## Hero-video
- Bron: `videos/hero-loop/` (HyperFrames-project, eigen foto's uit de originele projectmappen). Opnieuw maken: `cd videos/hero-loop && npx hyperframes render -o renders/hero-loop-master.mp4`, daarna met ffmpeg naar `assets/video/hero-loop.mp4` (864x1080, H.264, crf 27, zonder geluid, `+faststart`).
- `assets/video/hero-poster.webp` is het eerste frame. Mobiel en "beweging beperken" krijgen alleen de poster; `site.js` laadt de video pas op schermen vanaf 768px. Er is een pauzeknop.

## Bewuste keuzes
- Geen Google Fonts via CDN en geen Tailwind CDN. Alles staat lokaal, zodat er geen IP-adressen van bezoekers naar Google gaan en het cookiebeleid blijft kloppen.
- Bij foto's staat geen plaats of datum. Foto's die tijdens het werk zijn gemaakt, staan als "tijdens het werk" vermeld.
- Geen prijzen, termijnen, garanties, keurmerken, reviews of "gratis offerte": niets daarvan is bevestigd.
- Geen FAQ-markup: Google toont sinds mei 2026 geen FAQ-rich results meer. De vragen staan wel gewoon zichtbaar op de pagina's.
- Overkappingen en aanbouwtjes delen één pagina, tot er genoeg bevestigde informatie en foto's van aanbouwen zijn voor een eigen pagina.
- Geen losse pagina per plaats; zie docs/seo-paginaoverzicht.md.

## Nog nodig
Zie docs/open-vragen-klant.md.
