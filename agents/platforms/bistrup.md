# Bistrup

Platformsfil for platform-søgeagenten. Læses sammen med den generelle brief. Filen er IKKE verificeret mod auktionshusets side: siden kunne ikke åbnes fra søgemiljøet den 2026-11-09 (se Faldgruber).

## Søgning

Ikke verificeret. Søgeadresse, parametre og sortering er ikke fundet.

- Kør kun de givne søgninger, når en søgeside faktisk kan åbnes og er fundet.
- Sortering efter nyeste: ikke undersøgt. Skriv i dækningsnoten, at sorteringen ikke kunne bekræftes.
- Gæt ikke søgeadresser eller parametre.

## Dato

Ikke verificeret. Det vides ikke, hvor datoen vises, eller om der findes en oprettelsesdato.

- Noter datoen med den præcise tekst fra siden, og skriv hvad den betyder: slutdato, auktionsdato eller oprettelse. På auktionshuse er det normalt slut- eller auktionsdato, ikke oprettelsesdato.
- Kan ingen dato ses: `Dato/aktualitet: ikke synlig`.

## Direkte køb

Ukendt. Der er ikke set nogen købsknap uden auktion, og det kan ikke bekræftes her.

- Brug `Tjek`, indtil en annonce tydeligt viser et direkte køb.
- `Nej` kun, hvis det senere ses, at alle annoncer er auktioner.
- Antag ikke købsbeskyttelse ud fra auktionshusets navn.

## Faldgruber

Ikke verificeret. Cookie-banner, login, bot-tjek og markering af solgt eller udgået er ikke set.

Forsøg den 2026-11-09:

- `https://bistrup.dk/` og `https://bistrup.dk/auktion/`: proxy-fejl 502 "upstream request failed".
- `http://bistrup.dk/`: one.com-parkeringsside ("This one is taken"), ikke auktionshusets side.
- `http://bistrup.dk/auktion/`: 404 fra nginx.
- `bistrup.com` og `www.bistrup.com`: forbindelsen kan ikke oprettes.
- `bistrupauktion.dk` og `bistrup-auktion.dk`: forbindelsen kan ikke oprettes.

Konsekvenser:

- Det rigtige domæne for auktionshuset er ikke fundet. Find det, før platformen søges.
- Pris (startpris, nuværende bud eller slutpris) kan ikke afgøres. Angiv det, der står på annoncen, og skriv hvilken type det er.
- Skriv i dækningsnoten, at Bistrup ikke blev søgt, og kør ikke en søgning på en gætning.
