---
name: platform-sikoe
description: Platform specialist for Sikö. Holds the search wording, listing date, direct-purchase rule and known pitfalls for Sikö. Use when searching, checking availability or verifying listings on Sikö.
---

Denne fil er al platformsspecifik viden for Sikö. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# Sikö

Platformsfil for søgeagenten. Læses sammen med den generelle brief. Filen er endnu ikke verificeret: adressen til Sikö-markedspladsen er ikke kendt. Brug den generelle brief, og noter hullet i dækningsnoten.

## Søgning

Ikke undersøgt endnu. Adressen til Sikö er ikke fundet i repoet. `siko.dk` er Samvirkende Idrætsklubber i Odense og `sikoe.com` er en parkeringsside, så ingen af dem er markedspladsen. Søgeadresse, parametre og sortering skal verificeres, før denne sektion udfyldes.

## Dato

Ikke undersøgt endnu. Brug annoncedatoen, hvis den vises. Hvis den ikke vises, må alderen ikke gættes. Angiv begrænsningen.

## Direkte køb

Ikke undersøgt endnu. Sæt `Tjek`, indtil det er verificeret, om der findes en købsknap uden auktion.

## Faldgruber

Ikke undersøgt endnu. Tilføj kendte problemer, når siden er undersøgt, fx cookie-bannere, login-vægge, paginering, bot-tjek og markering af solgte eller udgåede annoncer.
