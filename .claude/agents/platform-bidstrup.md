---
name: platform-bidstrup
description: Platform specialist for Bidstrup. Holds the search wording, listing date, direct-purchase rule and known pitfalls for Bidstrup. Use when searching, checking availability or verifying listings on Bidstrup.
---

Denne fil er al platformsspecifik viden for Bidstrup. Den generelle protokol ligger i `agents/platform-searcher.md` (søgning), `agents/availability-checker.md` (tilgængelighed), `agents/verifier.md` (verifikation) og `agents/qualification-rules.md` (regler). Følg den protokol, der svarer til din opgave, og brug denne fil til alt, der er platformsspecifikt.

# Bidstrup

Bidstrups Auktioner (bidstrupauktioner.com, Køge) har ingen egen søgning. Alle lots ligger hos Auctionet, og bud og betaling går via Auctionet. Søg derfor på Auctionet, filtreret på Bidstrup med `company_id=566`. Verificeret 2026-11-09. Brug ikke bistrup.dk, som er en parkeringsside.

## Søgning

- Igangværende: `https://auctionet.com/da/search?company_id=566&q=<søgeord>`.
- Afsluttede (arkiv): tilføj `&is=ended`. Kør begge dele for hver søgning.
- Sortering: `order=recent` ("Senest modtaget") er nærmest nyeste, men er ikke verificeret som nyeste først. Brug standardsortering og dæk med flere søgeord.
- Paginering: klikbare sider med `&page=N`, 48 lots pr. side. Stop ved en tom side. Tæl unikke lot-numre og sammenlign med "N genstande" øverst.
- Ved 0 igangværende fund viser siden arkivlots under "Her er genstande fra vores arkiv". Tæl kun, hvis der ikke står "desværre ingen genstande".
- Cookiebanner: vælg "Afvis alle".
- Kørsel 2026-11-09: "Fritz Hansen" afsluttet 142 af 142 læst. "Hans J. Wegner" afsluttet 107 opgivet, kun 92 unikke læst, fordi sider gav dubletter. "Verner Panton stol" 4 afsluttede, 0 igangværende. "Severin Hansen bord" 21 afsluttede, 1 igangværende.

## Dato

- Afsluttede lots: kortet viser "Opnåede hammerslag <dato>". Lotsiden viser "Solgt".
- Igangværende lots: kortet viser tid tilbage. Lotsiden viser "Slutter om" med dato og klokkeslæt, fx "16 nov 2026 kl. 15:51 CST".
- Datoen er auktionens slut. Der findes ingen start- eller oprettelsesdato. Skriv `Dato/aktualitet: slut <dato>, ikke oprettelse`.

## Direkte køb

- Set på en afsluttet og en igangværende lot-side: kun budgivning ("Afgiv bud", "Log ind eller opret konto for at afgive et bud"). Ingen "Køb nu"-knap.
- Svar `Nej`, når lotsiden kun viser budgivning. Svar `Tjek`, hvis noget andet vises.
- Antag ikke købsbeskyttelse ud fra Auctionets eller Bidstrups navn.

## Faldgruber

- Login: bud kræver konto. Søgning og lotsider kan læses uden login. Log ikke ind og byd ikke.
- Pris: kortet viser højeste bud. Uden bud viser det vurderingen. Prisen står i USD som standard. Skriv valutaen og konvertér ikke.
- Navnefælde: "Severin Hansen" finder kun ERIK SEVERIN RISAGER-HANSEN (Haslev Møbelsnedkeri). "Fritz Hansen" finder 21 af 142 lots uden Fritz Hansen i titlen. Læs titlen, før du giver `Bekræftet`.
- Søgningen matcher dele af ord, så søgeord kan give ukendte designere.
- Afsluttet uden bud: kortet kan vise "Opnåede hammerslag" selv uden salg. Skriv forbehold om solgt-status.
- Ingen bot-tjek eller CAPTCHA er set. "Kontakt supporten" og "Få en gratis vurdering" hører ikke til lots. Brug dem ikke.
