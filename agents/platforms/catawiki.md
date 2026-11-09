# Catawiki

Platformsfil til søgeagenten. Læses sammen med den generelle brief.

**Status: ikke verificeret.** Catawiki blokerer adgang for denne session. Forsiden, søgesider (`/en/s?q=...`) og `robots.txt` giver Akamai 403 "Access Denied", både med curl og i Playwright (2026-11-09). Ingen søgning er kørt. Alt nedenfor er uprøvet og må ikke bruges som fakta.

## Søgning

- Ikke verificeret. Søgeadressen `https://www.catawiki.com/en/s?q=<søgeord>` er ikke testet.
- Sortering efter nyeste eller slutter-tid: ukendt. Find det i browseren før brug.
- Paginering og om listen stopper tidligt: ukendt. Skriv det i dækningsnoten.

## Dato

- Ikke verificeret. Catawiki er en auktion, så den dato der vises er sandsynligvis slutdato/-tid, ikke oprettelsesdato.
- En slutdato er ikke en annoncedato. Brug kun en dato som "efter cutoff" hvis annoncesiden viser en oprettelses- eller "lagt op"-dato. Ellers skriv slutdatoen som den den er og sæt forbehold.

## Direkte køb

- Ikke verificeret. Catawiki er en auktion, og om der findes en købsknap uden bud er ikke testet.
- Brug `Tjek` indtil en annonceside er læst og købsmuligheden er set. Udled ikke købsbeskyttelse af listingen eller sælgerprofilen.

## Faldgruber

- Adgang blokeret: Akamai 403 på hele domænet. Omgå det ikke med andre headers, proxies, login eller CAPTCHA. Skriv "ikke søgt" i dækningsnoten og stop.
- Valuta: priser er sandsynligvis i EUR, ikke verificeret. Omregn til DKK kun med en klar kilde og kursdato. Ellers ingen omregning.
- Cookie-banner, login-vægge, bot-tjek og markering af solgt/udgået: ikke set. Antag ikke noget om dem.
