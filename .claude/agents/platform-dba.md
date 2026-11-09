---
name: platform-dba
description: Platform specialist for DBA. Holds the search wording, listing date, direct-purchase rule and known pitfalls for DBA. Use when searching, checking availability or verifying listings on DBA.
---

Denne fil er al platformsspecifik viden for DBA. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# DBA

Platform file for the platform search agent. Read together with the general brief.

## Søgning

- Søg på dba.dk under brugt/recommerce (annoncer med adressen `/recommerce/forsale/item/<id>`). Brug hver søgning fra briefen.
- Sortér efter nyeste: tilføj `sort=PUBLISHED_DESC` til søgeadressen. Det blev brugt i de seneste kørsler.
- Gå alle resultatsider igennem, til en side er tom. Det samlede antal øverst på siden har vist sig ustabilt, så brug det ikke til at afgøre, om du er færdig.
- Første gang på en række: søg hele markedet. Ingen cutoff.
- Cookie-banneret: vælg "Kun nødvendige". Det påvirker ikke søgelisterne.
- Hent siderne som rå HTML (curl). Playwright har i flere kørsler givet en tom side på dba.dk. Læs annoncedata fra HTML eller de indlejrede JSON-LD-data: titel, pris, by, stand, designer- og mærkefelt, "Sidst redigeret" og tilgængelighed.

## Dato

- Søgekortet viser en kort dato eller en relativ alder ("8 t.", "3 dage", "1. nov.", "2.6.25"). Nogle datoer mangler årstal.
- Annoncesiden viser kun "Sidst redigeret". DBA viser ikke oprettelsesdato.
- Skriv derfor altid datoen som "sidst redigeret" og sæt `dateKind: redigeret`. Gamle annoncer kan være genoptaget, og en ny dato betyder ikke, at annoncen er ny.
- Hvis kun en relativ alder vises, så skriv den som evidens, og sæt `dateApprox: true` i fundet.

## Direkte køb

- `Ja` kun når Fiks færdig er tilbudt eksplicit, fx med Fiks færdig-badge og "Tryg handel" på annoncen.
- Knappen "Bed om Fiks færdig" alene er ikke et tilbud, så den giver `Nej`.
- "Send besked", "Gå til varen" og "Fragt tilbydes" giver `Nej`.
- Er det uklart, så `Tjek`.

## Faldgruber

- Søgningen "Panton Chair" stoppede tidligt: 80 af 118 kort blev vist. Ellers dækkede de andre søgninger de manglende annoncer, men det er ikke dokumenteret. Skriv det i dækningsnoten, når en søgning viser færre kort end antallet af resultater.
- Professionelle sælgere (fx Cph-Classic, Nordic Retro, Antik Pjot) genopretter gamle annoncer. Kortdatoen kan se ny ud. Skriv det som forbehold.
- Brede søgninger på et producentnavn (fx "Haslev") giver annoncer, der ikke er designet af den søgte person. Læs annoncen, før du giver `Bekræftet`.
- Ombetræksservice-annoncer ("ombetræk", "polstring") er ikke et møbel til salg. Afvis dem.
- Reserverede eller solgte annoncer er ikke set i de seneste kørsler. Tjek alligevel tilgængeligheden i annoncen.
- Annoncetekst kan være afkortet på søgekortet. Læs fuld beskrivelse, før du vurderer identitet.
