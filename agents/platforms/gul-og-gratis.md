# Gul og Gratis

Platformsfil for platform-søgeagenten. Læses sammen med den generelle brief. Adresse: guloggratis.dk (gulogratis.dk redirigerer hertil).

## Søgning

- Søgeadresse: `https://www.guloggratis.dk/kategori/q-<søgeord>`, fx `q-Verner%20Panton%20stol`. Søgefeltet er JavaScript-baseret; `?q=` giver 404.
- Nyeste først: tilføj `?sort=created` (menuen "Sortér" → "Sidst oprettet"). Rækkefølgen er faldende efter dato.
- Paginering: `&side=2` og `&side=3` gav identiske resultater med side 1. Ukendt om der findes flere annoncer.
- Testede søgninger: "Verner Panton stol" 7 annoncer, "Severin Hansen bord" 9, "Fritz Hansen" 60, "Hans J. Wegner" 60. De 60 er trolig en øvre grænse; scroll gav ikke flere.
- Smalle søgninger blander irrelevante annoncer ind (fx "New Balance", "EGLO"). Filtrer på titel.

## Dato

- Listen viser dato som "i dag", "i går", ugedag, "10. jul." eller "9. jun. 2025". Manglende år tolkes som indeværende år. Det er en udledning, ikke en label.
- Detaljesiden viser ingen oprettelsesdato. "Medlem siden" og "Følgere" er sælgerens profil, ikke annoncens dato.
- Om datoen er oprettelses- eller redigeringsdato, er ikke bevist. Sorteringen "Sidst oprettet" tyder på oprettelse.

## Direkte køb

- Annoncesiden har ingen købsknap for varen. "Køb fragt" og "Send med priser fra 45 kr." linker til `/pakkepost`, som er en fragttjeneste, ikke et køb af annoncen.
- Ingen betalingsfunktion er synlig for annoncen. "Skriv besked" er kontakt til sælgeren og er ikke brugt.
- Brug `Tjek` som standard. `Ja` kun ved en tydelig købsknap eller købsfunktion for denne annonce. Købsbeskyttelse er ikke bevist af noget på siden.

## Faldgruber

- Cookiebanner ved første besøg ("Cookieindstillinger"). Ikke undersøgt, om den skjuler listen.
- "Opret / log ind" står øverst. Søgning og annoncesider kan læses uden login; login er ikke forsøgt.
- "Fremhævet" og "Ny" annoncer kan stå øverst uden at følge datorækkefølgen.
- Reserveret og solgt: ingen markering fundet i de testede søgninger eller på detaljesiden. Det betyder ikke, at markeringen mangler.
- Annoncer fra forhandlere og reklamer (fx PriceRunner) blandes ind. Filtrer dem fra, hvis de ikke er private annoncer.
- Ingen CAPTCHA eller bot-tjek observeret (HTTP 200 med curl og Playwright).
