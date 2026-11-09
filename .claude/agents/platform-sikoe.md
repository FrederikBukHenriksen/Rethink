---
name: platform-sikoe
description: Platform specialist for Sikö. Holds the search wording, listing date, direct-purchase rule and known pitfalls for Sikö. Use when searching, checking availability or verifying listings on Sikö.
---

Denne fil er al platformsspecifik viden for Sikö. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# Sikö

Sikö Auktioner (sikoauktioner.se) er et svensk auktionshus. Siden er på svensk, og priserne står i "kr". Valutakoden vises ikke, så skriv "kr" og lad være med at konvertere.

## Søgning

- Adresse: `https://www.sikoauktioner.se/sok/<søgeord>/<kategori>/<arkiv>/<side>/<sortering>/<by>`. Brug `0` for alle kategorier, `0` for kun aktive auktioner, og `0` for alle byer. Mellemrum skrives `%20`. Punktum skrives `¬`, så "Hans J. Wegner" bliver `Hans%20J¬%20Wegner`.
- Sortering: `tid` (Kortast tid kvar, sluttid stigende), `nya` (Längst tid kvar, sluttid faldende), `senast` (Senast publicerade), `pris` (Värdering), `hogst` (Högst bud). Standard er `tid`.
- Side 1 viser 24 lots. Gå videre med `<side>` 2, 3 osv. til en side uden lots.
- Kørt 2026-11-09: "Verner Panton stol", "Panton", "Severin Hansen bord", "Severin Hansen", "Hans J. Wegner", "Wegner" og "Haslev bord" gav 0 lots. "Fritz Hansen" gav 2, "Bruno Mathsson" 3 og "stol" 83 (over 4 sider).

## Dato

- Lotsiden viser "Avslutas: 16 NOV 20:12", og søgekortet har sluttiden i `title`. Det er sluttidspunktet, ikke oprettelsesdatoen.
- Publiceringsdato vises ikke på kort eller lotside. Sorteringen "Senast publicerade" er ikke verificeret mod en dato, og den følger hverken lotnummer eller sluttid.
- Skriv derfor `Dato/aktualitet: sluttid <dato>, publicering ikke synlig`, og sæt forbehold. Udled ikke alder af sluttiden.

## Direkte køb

- Alle lots, der er set (på kort og lotside), har kun "Lägg bud" eller "Bjud!", altså auktion. Der er ingen "Köp nu". "Boka transport" er fragt, ikke køb. Sæt `Nej`. Sæt `Tjek`, hvis en købsknap uden budgivning optræder.

## Faldgruber

- Søgesiden viser ikke samlet antal resultater. Sidenavigationen viser altid 8 sider, også når færre har lots: "stol" gav 4 sider med lots, og side 5 var tom. Stop ved første tomme side, ikke ved sidetallet.
- En søgning uden resultater viser bare en tom side uden tekst. Skriv det i dækningsnoten, så det ikke ses som "ingen fund".
- Forbindelsen til sikoauktioner.se afbrydes ofte (`connection reset`). Prøv igen, og notér sider, der ikke kunne hentes.
- "Aktuellt bud" er det aktuelle bud (0 kr = ingen bud). "Värdering" er et skøn, ikke startpris eller salgspris, og startpris vises ikke. Brug ikke Värdering som pris.
- Læsning kræver ikke login. Budgivning kræver login og BankID, og det gør vi ikke.
- Ingen cookiebanner, CAPTCHA eller bot-tjek sås i curl eller Playwright.
- Arkivflaget (`1`) gav samme lots som aktive søgninger for "stol" og "Fritz Hansen". Afsluttede eller solgte lots er ikke set, så status for dem er ikke verificeret.
