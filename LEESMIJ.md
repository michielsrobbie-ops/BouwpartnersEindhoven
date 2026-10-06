# Bouwpartners Eindhoven — website

Lichte, rustige opzet. Wit als basis, stone-50 voor de rustige secties, de oranje uit het logo (#FB6A1E) voor dak en aanbouw, emerald-700 voor tuin.

## Opbouw
- `_data.py` bevat alle teksten, diensten en projecten. Daar pas je de inhoud aan.
- `build.py` zet die inhoud om in de twaalf pagina's.
- `src/input.css` + `tailwind.config.js` zijn de bron van de stijl; `css/site.css` is het gecompileerde resultaat.
- `js/site.js` doet het menu, het projectfilter en het formulier.
- `assets/fonts/` bevat de lettertypen lokaal: Plus Jakarta Sans (koppen), Outfit (tekst), Space Grotesk (labels).

## Opnieuw bouwen
```
npm install                 # eenmalig
python3 build.py
npx tailwindcss -i src/input.css -o css/site.css --minify
```
Hoog na een wijziging in CSS of JS het nummer `V` in build.py op, anders zien bezoekers de oude versie uit hun cache.

## Bewuste keuzes
- Geen Google Fonts via CDN en geen Tailwind CDN. Alles staat lokaal, zodat er geen IP-adressen van bezoekers naar Google gaan en het cookiebeleid blijft kloppen.
- Bij de projecten staat "Regio Eindhoven", geen jaartallen. De datums van de foto's zeggen alleen wanneer ze zijn doorgestuurd.
- Dak en tuin krijgen op de homepage twee gelijke kolommen; overkappingen en aanbouw vormen de band eronder.

## Nog nodig
- Btw-nummer voor de footer.
- Bevestiging van de bewaartermijn in het privacybeleid (nu een jaar).
- Foto's van afgeronde daken; de dakfoto's tonen nu alleen werk in uitvoering.
- FormSubmit activeren: na de eerste inzending komt er een activatiemail op bouwpartnerseindhoven@gmail.com; daarin op "Activate Form" klikken.
