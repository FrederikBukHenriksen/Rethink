# Klein Anzeigen

Platformfil til platform-søgeagenten. Læses sammen med den generelle brief. Tysk side: priser i EUR, tekst på tysk. Verificeret 2026-11-09.

## Søgning

- Adresse: `https://www.kleinanzeigen.de/s-sortierung:neuste/<slug>/k0`. Slug er søgeordet med små bogstaver og bindestreg, fx `verner-panton-stuhl`, `hans-j-wegner`, `severin-hansen-tisch`.
- Sortering efter nyeste står i stien (`sortierung:neuste`). Den gamle form `/s-suchanfrage.html?keywords=…&sortingField=SORTING_DATE` omdirigeres til stien.
- Side 2 og frem: `/s-sortierung:neuste/seite:N/<slug>/k0`. 25 annoncer pr. side.
- Direkte-køb-filter: `/s-sortierung:neuste/direktkaufen:aktiv/<slug>/k0`.
- Søgningen er bred. "Fritz Hansen" gav 1.273 treff, "Verner Panton Stuhl" 143, "Severin Hansen Tisch" 12 uden side 2. Brug modelnavne.

## Dato

- Kort: "Heute, 14:13" (i dag), "Gestern, 16:47" (i går) eller "DD.MM.YYYY" for ældre. Annoncesiden viser "DD.MM.YYYY" ved stedsnavnet.
- Listen er sorteret nyeste først. Den ældste i testen var fra 2020.
- Ikke verificeret: om datoen er oprettelsen eller seneste fornyelse. Nogle kort i scanningen viste ingen dato i den korte tekst, så åbn annoncen.

## Direkte køb

- `Ja`: badgen "Direkt kaufen" står ved prisen på kortet eller i annoncens egen blok (fx "525 € VB + Versand … Direkt kaufen").
- "Direkt kaufen" kan også stå under "Das könnte dich auch interessieren" på en anden annonce. Læs kun annoncens egen blok.
- `Nej`: ingen badge på annoncen, og den er tydeligt synlig.
- Ikke verificeret: selve købsflowet, betaling og returret. Jeg har ikke klikket på noget. På en direkte-køb-annonce vises "Käuferschutz" som betalt tillæg ("Für nur 24,13 € extra"). Det må ikke overføres til andre annoncer.
- "Versand möglich" og "ab 1,99 €" er fragt, ikke køb.

## Forsendelse (skal med)

- Kun annoncer, der kan sendes, tages med. Det skal stå i annoncen, fx "Versand möglich" eller "Versand" med en fragtpris.
- Udelad annoncer, hvor der står "Nur Abholung", "nur Abholung", "Abholung only" eller "Versand nicht möglich", og annoncer der kun kan afhentes.
- Hvis annoncen ikke nævner forsendelse, udelades den også, og det noteres i dækningsnoten som "udeladt: forsendelse ikke angivet".
- "Versand möglich" og "ab 1,99 €" er fragt, ikke køb (se Direkte køb). Fragt er ikke en bekræftelse af, at annoncen kan sendes til Danmark. Det noteres som ikke verificeret.

## Faldgruber

- Søgning og annoncer kan læses uden login. Et "Hallo!"-login-popup vises på søgesiden, og den kan lukkes med X. På annoncesider ligger et cookie-banner ("Alle akzeptieren") over siden. Jeg har ikke klikket det. Teksten står i DOM.
- Ingen CAPTCHA eller bot-tjek i ca. 35 sideindlæsninger.
- Reserveret eller verkauft: ingen markering set på kortene. "Verkauft" i teksten er sælgerens ord. Ikke verificeret.
- Valuta: "525 € VB". VB = Verhandlungsbasis, forhandlingsbar. Tusindeskiller er punktum: "1.315 €".
- "Gewerblicher Nutzer" og PRO-badge betyder erhvervssælger. "Privatverkauf" betyder ingen returret.
- Paginering: sidetal ud over sidste side giver sidste side igen. Stop når header "X - Y von Z" når Z. Scanningen stoppede på 4 sider, så den dækker ikke alt.
- Facettet "Aktiv 140" ved direkte køb stemmer ikke med de 7 resultater i filteret. Brug listen, ikke tallet.
