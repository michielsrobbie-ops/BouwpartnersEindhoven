# Nieuwe homepage

Bewerk index.html, css/studio.css en js/studio.js rechtstreeks. build.py controleert de lokale verwijzingen en genereert niets. De oude generator en homepage staan in _backups.

De hero is een gegenereerde architecturale illustratie met een introductie- en scrollanimatie, geen interactief 3D-model. De foto’s eronder komen uit de bestaande projectmap.

Het contactformulier opent een vooraf ingevulde e-mail; er wordt niets automatisch verzonden. De eerdere formulierkoppeling is niet bevestigd. Voor directe verzending moet een gecontroleerde backend worden aangesloten. Bellen en e-mail zijn beschikbaar.

Controleer bedrijfsfeiten en privacybeleid vóór publicatie. Nog niet gepubliceerd.

## Vervolgpagina's (3 okt 2026)

Zeven dienstpagina's, ons-werk.html, privacybeleid.html en 404.html worden gemaakt door `python3 paginas.py`. Teksten en foto's per dienst staan bovenaan dat script. Stijl: css/paginas.css bovenop studio.css; script: js/pagina.js. index.html blijft handwerk en wordt door paginas.py niet aangeraakt.

De knoppen op de dienstpagina's gaan naar index.html?dienst=…#contact; studio.js zet die dienst alvast in het formulier.
