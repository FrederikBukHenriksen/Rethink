---
name: platform-vinted
description: Platform specialist for Vinted. Holds the search wording, listing date, direct-purchase rule and known pitfalls for Vinted. Use when searching, checking availability or verifying listings on Vinted.
---

Denne fil er al platformsspecifik viden for Vinted. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# Vinted

Platform file for the platform search agent. Read together with the general brief.

## Søgning

- Add the word `lampe` to broad searches to reduce irrelevant results such as clothing. Keep the model and designer terms.
- Sort by newest where the platform supports it.

## Dato

Not filled in yet. Use the listing date if it is shown. If it is not shown, do not guess how old it is. Report the limitation.

## By

Vinted listings often show no city. To read the seller's city:

1. First look at the seller's profile page. Use the location shown there.
2. If it is not shown, open the message screen from the listing ("Send besked"). The city is shown there. Read it, type nothing, send nothing, and close the screen.

This is the only time you may open the message screen. Never write in it, never send anything, never make an offer, and never press a button that sends or reserves. If the screen asks for anything beyond showing the city, close it and report `ikke synlig`. If you are unsure whether you are about to send something, stop and report `ikke synlig`.

Report the city exactly as shown. Do not guess it from the seller's name, the photos or the listing text.

## Direkte køb

`Ja` where the normal Vinted checkout (payment and shipping) is available.
If the information is not visible or is ambiguous: `Tjek`.

## Faldgruber

Not filled in yet. Add known problems here, for example cookie banners, login walls, pagination limits, or relisted ads that look new.
