---
name: platform-tradera
description: Platform specialist for Tradera. Holds the search wording, listing date, direct-purchase rule and known pitfalls for Tradera. Use when searching, checking availability or verifying listings on Tradera.
---

Denne fil er al platformsspecifik viden for Tradera. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# Tradera

Platform file for the platform search agent. Read together with the general brief.

## Søgning

- Add the word `lampe` to broad searches to reduce irrelevant results. Keep the model and designer terms.
- Sort by newest where the platform supports it.

## Dato

Not filled in yet. Use the listing date if it is shown. If it is not shown, do not guess how old it is. Report the limitation.

## Direkte køb

`Ja` only if the listing shows `Betaling via Tradera`.
If the information is not visible or is ambiguous: `Tjek`.

## Faldgruber

Not filled in yet. Add known problems here, for example cookie banners, login walls, pagination limits, or relisted ads that look new.
