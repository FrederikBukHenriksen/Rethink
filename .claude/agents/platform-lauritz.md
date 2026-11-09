---
name: platform-lauritz
description: Platform specialist for Lauritz. Holds the search wording, listing date, direct-purchase rule and known pitfalls for Lauritz. Use when searching, checking availability or verifying listings on Lauritz.
---

Denne fil er al platformsspecifik viden for Lauritz. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# Lauritz

Platformsfil til platformssøgeagenten. Læses sammen med den generelle brief.

## Søgning

- Adresse: `https://www.lauritz.com/da/auctions/search/<søgeord>`, mellemrum som `%20` (fx `Verner%20Panton%20stol`). Søgning kræver ikke login.
- Standardfiltret viser kun aktive auktioner (`isBuyNow=false`). "Severin Hansen bord" og "Severin Hansen" gav 0 varer.
- Sortering: `sortType=endsOn&sortDirection=desc` svarer til "Udløbstid (Faldende)". Der findes ingen "Nyeste"-sortering. Standard er Relevans.
- Sider: `take=60`. Over 60 varer bruges `skip=60`, fx "lampe" gav 82 varer. Dette er kun kontrolleret i data, ikke ved at klikke videre i listen.

## Dato

- Kortet viser kun slutdato uden år (fx "12. nov."). Detaljesiden viser "AUKTIONEN AFSLUTTES" med år og klokkeslæt.
- Det er slutdato, ikke oprettelsesdato. Startdato findes kun i sidens data (`auctionStart`) og er ikke synlig. Brug den ikke som listedato.
- Skriv derfor `Dato/aktualitet: ikke synlig (slutter DD. MMM)`. Cutoff kan ikke afgøres sikkert, så skriv det i Usikkerhed.

## Direkte køb

- Alle 57 varer i de fire søgninger var auktioner: detaljesiden viser "Afgiv bud" og "Næste bud", og `isBuyNow` var false uden `buyNowPrice`. Svar `Nej` for auktioner.
- Lauritz har også "Køb nu"-varer, men standardsøgningen skjuler dem. Filteret "Vis Køb nu varer" fandt jeg ikke i filterpanelet. Ikke verificeret.
- `Ja` kun hvis detaljesiden viser en købsknap med fast pris og intet budfelt. Ellers `Tjek`, hvis du er i tvivl.

## Faldgruber

- Cookiebot-banner: klik "Afvis", ikke "Tillad alle".
- "Vurdering" er et estimat, ikke en pris. Kortet viser "Næste bud"; detaljesiden viser også "Inkl. salær og gebyr". Startpris og slutpris vises ikke.
- Søgeresultater viser ikke solgt eller udgået. Afsluttede auktioner er skjult.
- Samme titel kan være flere separate varer med forskelligt lotId, fx to "Seks Myren". Nævn dubletter i Usikkerhed.
- Brug aldrig "Dit bud" eller "Afgiv bud". Log ikke ind.
