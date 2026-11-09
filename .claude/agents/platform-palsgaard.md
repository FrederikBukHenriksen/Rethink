---
name: platform-palsgaard
description: Platform specialist for Palsgaard. Holds the search wording, listing date, direct-purchase rule and known pitfalls for Palsgaard. Use when searching, checking availability or verifying listings on Palsgaard.
---

Denne fil er al platformsspecifik viden for Palsgaard. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# Palsgaard

Platformsfil for platform-søgeagenten. Testet 2026-11-09 med curl og Playwright. Palsgaards egen side (palsgaardkunstauktioner.dk) er en vitrine: alle genstande sælges på Auctionet (auctionet.com, `company_id=404`).

## Søgning

- Søg på Auctionet: `https://auctionet.com/da/search?company_id=404&q=<søgning>` for aktive genstande. Tilføj `&is=ended` for afsluttede.
- Paginering: `&page=2`, `&page=3` osv. Aktive søgninger viser 20 pr. side, afsluttede 48. Stop, når siden er tom eller antallet er nået.
- Sortering: `order=` (menu: "Relevans", "Senest modtaget", "Kortest tid tilbage" m.fl.). `order=recent` blev accepteret, men det er ikke verificeret, at den sorterer efter oprettelse.
- Listen er JavaScript-renderet. curl finder ingen annoncelinks, så brug Playwright og vent på `a.item-thumb__link`.
- Kørt 2026-11-09 (resultater i alt / læst):
  - "Verner Panton stol": aktive 0 / 0, afsluttede 20 / 20.
  - "Severin Hansen bord": aktive 4 / 4, afsluttede 137 / 137.
  - "Fritz Hansen": aktive 20 / 20, afsluttede 476 / 476.
  - "Hans J. Wegner": aktive 4 / 4, afsluttede 312 / 309 unikke. Nogle kort optrådte flere gange, og tallet varierede mellem kørsler.
- Login er ikke nødvendigt for at søge og læse. Cookie-banneret: vælg "Nødvendige cookies" eller "Afvis alle". Der sås ingen bot-tjek eller CAPTCHA.

## Dato

- Kort og annonce viser kun slutteid, ikke oprettelsesdato. Aktive: "Slutter om 4 dage" og "13 nov 2026 kl. 04:20 CST". Afsluttede: "Opnåede hammerslag 25 mar 2026".
- Det er ikke annoncedato. Skriv `Dato/aktualitet: ikke synlig`, og nævn sluttidspunktet i Forbehold. Gæt aldrig en oprettelsesdato, og brug ikke cutoff på slutteid.

## Direkte køb

- `Nej`. Palsgaard skriver på siden /koeb, at alle genstande sælges på netauktion via Auctionet. Annoncen (én aktiv genstand tjekket) viser kun "Afgiv bud", ingen købsknap.

## Faldgruber

- Tom aktiv søgning viser "Vi har desværre ingen genstande, der matcher din søgning" og derefter op til fem arkivkort på side 2 og videre. Tæl kun de kort, der står i den viste total.
- Priser vises i USD, fordi sessionen er sat til USD. Annoncens oprindelige valuta er DKK (`original_currency`). Brug DKK-beløbet, hvis det vises, ellers angiv beløbet som vist og konvertér ikke.
- Startpris: "Byd mindst". "Vurdering" vises, når der ikke er bud. "Opnåede hammerslag" er slutpris. Købers salær (25 % og 70 kr. hammerslagsgebyr, ifølge /koeb) er ikke med i tallene.
- By: "Genstanden findes i <by>", fx Copenhagen. Huset ligger på Midtager 33, 2605 Brøndby, men det er ikke genstandens by.
- Søgeord rammer også bøger og magasiner og tilskrevne værker ("TILSKREVET"). Kortenes titler er afkortet med "…", så læs den fulde titel og beskrivelse.
- Tryk aldrig på "Afgiv bud", "Overvåg søgning" eller "Søg efter pris".
- Ikke verificeret: om afsluttede genstande uden hammerslag findes, og om der er en genstand, der er "ikke solgt".
