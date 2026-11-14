# Bidstrup

Platformsfil for platform-søgeagenten. Læses sammen med den generelle brief.

**Status: verificeret 2026-11-14** i brugerens egen Chrome. Bidstrup (Bidstrups Auktioner, Køge) sælger udelukkende via Auctionet. Der er ingen egen søgning på `bidstrupauktioner.com`. Brug Auctionet.

## Søgning

- Auktionshusets side `bidstrupauktioner.com` linker til Auctionet: "Se alle aktuelle lots" og "Aktuelle auktioner" peger på `https://auctionet.com/da/search?company_id=566`.
- Søg på Auctionet med Bidstrups `company_id=566`: `https://auctionet.com/da/search?company_id=566&q=<søgeord>`. Eksempel: `&q=ph+4%2F3`.
- Auctionets søgning med husnavnet som fritekst ("bidstrup") giver ingen resultater. Brug `company_id=566` i adressen.
- Sortér efter nyeste, hvis Auctionet tilbyder det. Ellers gennemgå resultaterne og skriv i dækningsnoten, at sorteringen ikke er bekræftet.
- Åbn hvert lot, der matcher en række. Læs selve lotsiden, ikke kun søgeresultatet.
- Ved login-krav, bot-tjek eller tomme sider: stop, og skriv "ikke søgt" med årsagen. Skriv aldrig "ingen fund".

## Dato

Auctionet viser slutdato, ikke oprettelsesdato. Skriv `Dato/aktualitet: slutter <dato>` ud fra "Slutter om" eller "Solgt" på lotsiden. Den må ikke bruges som udtryk for, hvor ny annoncen er. Lots med "Solgt" eller "Afsluttet" er ikke kandidater.

## Direkte køb

Bidstrup sælger på auktion. Alle lots på Auctionet er auktioner.

- `Nej`, når lotsiden viser "Højeste bud" og "Slutter om" uden købsknap.
- `Ja` kun ved en tydelig "Køb nu"-knap på lotsiden.
- Ellers `Tjek`.

## Priser

Auctionet viser "Vurdering" (auktionshusets estimat), "Højeste bud" og "Byd mindst". Skriv det, der bruges som pris på fundet, og angiv i `priceNote` hvilken type det er. Vurderingen er ikke en pris. Beløb er i DKK.

## Faldgruber

- **Solgte og afsluttede lots:** Søgeresultater kan vise solgte lots. I kørslen 2026-11-14 var de fleste PH 4/3-, Bent Karlby- og Panton-lots solgt eller afsluttet. Tjek status på lotsiden.
- **Fuzzy søgning:** Auctionets søgning matcher ord løst. "Pendel" og "bordlampe" gav mange ikke-relevante lots. Læs hvert resultat, og afvis det, der ikke matcher målet.
- **Tilskrevne designere:** Auctionet bruger "TILSKREVET" og "antageligvis udført hos". Det er en tilskrivning, ikke en bekræftet designer. Brug `Sandsynlig med forbehold`, medmindre andet er dokumenteret.
- **Login og bud:** Der bydes og logges ikke ind. Stop ved login-krav, og omgå dem ikke.

## Kørsel 2026-11-14 (dækning)

Søgt via Auctionet `company_id=566`:

- Række 2 (PH 4/3): "ph 4/3". Resultater: to orange PH 4/3-pendler (5526680 solgt 9.11, 5534129 solgt 11.11, derfor ikke kandidater), to hvide (afvist, farve), en PH 4/3-bordlampe fra 1930'erne (afvist, type, solgt). Fundet `bistrup-5534129` i artefakt-DB skal opdateres til `Solgt`.
- Række 20 (Brylle): "brylle". Ingen resultater.
- Række 21 (Bent Karlby): "bent karlby". Fem lots: alle solgte eller afsluttede (5258516, 5259581, 5268824, 4565471, 5514438). Ingen kandidater.
- Række 23 (Panton magasinholder): "magasinholder", "panton". Ingen magasinholder. Panton-lots der kom op var andre objekter.
- Række 24 (Kartell ur): "kartell". Ingen Kartell-ur.
- Række 25 og 26 (Space Age): "space age", "pendel", "bordlampe". Ingen Space Age-lamper. To "par pendler af glas og messing" (5460869) og "sæt af fem pendler" (5534291) er ikke Space Age-mærkede og afvist.
- Række 27 (Panum/Koppel ur): "koppel". Ingen Panum/Koppel-ur. Henning Koppel-lots er ikke Nils eller Eva Koppel.
- Møbler række 5 (1-2-3): "1-2-3". Ingen.

Ikke søgt: sortering efter nyeste er ikke bekræftet. De to hvide PH 4/3 (5461442, 5534209) er afvist ud fra titlen, lotsiden er ikke åbnet. Alle andre lots, der blev vurderet, er åbnet og læst.

## Fund 2026-11-14

Ingen nye kandidater fra Bidstrup i denne kørsel. Alle matchende lots var solgte, afsluttede eller uden for målet.
