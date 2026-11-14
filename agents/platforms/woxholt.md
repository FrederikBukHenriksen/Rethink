# Woxholt

Platformsfil for platformssøgeagenten. Læses sammen med den generelle brief.

**Status: verificeret 2026-11-14** i brugerens egen Chrome. Woxholt kan nu nås på `woxholtauktioner.dk`. Siden er et ikke-selvstændigt udstillingsvindue: alle lots ligger på Auctionet.

## Søgning

- Woxholt har ingen egen søgning på `woxholtauktioner.dk`. Siden lister kun et udvalg af lots og linker til Auctionet.
- Søg i stedet på Auctionets sælgerside for Woxholt: `https://auctionet.com/da/search?company_id=526` (236 genstande i alt, 2026-11-14).
- Søg med søgeord i den adresse: `https://auctionet.com/da/search?company_id=526&q=<søgeord>`. Eksempel: `&q=bent+karlby`.
- Sortér efter nyeste, hvis Auctionet tilbyder det. Ellers gennemgå resultaterne og skriv i dækningsnoten, at sorteringen ikke er bekræftet.
- Åbn hvert lot, der matcher en række. Læs selve lotsiden, ikke kun søgeresultatet.
- Ved login-krav, bot-tjek eller tomme sider: stop, og skriv "ikke søgt" med årsagen. Skriv aldrig "ingen fund".

## Dato

Auctionet viser slutdato, ikke oprettelsesdato. Skriv `Dato/aktualitet: slutter <dato>` ud fra "Slutter om" eller "Solgt" på lotsiden. Den må ikke bruges som udtryk for, hvor ny annoncen er. Hvis der står "Solgt" eller "Afsluttet", er lottet ikke en kandidat.

## Direkte køb

Woxholt er et auktionshus. Alle lots på Auctionet er auktioner.

- `Nej`, når lotsiden viser "Højeste bud" og "Slutter om" uden købsknap.
- `Ja` kun ved en tydelig "Køb nu"-knap på lotsiden.
- Ellers `Tjek`.

## Priser

Auctionet viser "Vurdering" (auktionshusets estimat), "Højeste bud" og "Byd mindst". Skriv det, der bruges som pris på fundet, og angiv i `priceNote` hvilken type det er. Vurderingen er ikke en pris.

## Faldgruber

- **Solgte og afsluttede lots:** Søgeresultater kan vise solgte lots. Tjek status på lotsiden, før et lot tages med.
- **Tilskrevne designere:** Woxholt bruger ofte "TILSKREVET" i titlen. Det er en tilskrivning, ikke en bekræftet designer. Brug `Sandsynlig med forbehold`, medmindre andet er dokumenteret.
- **Fuzzy søgning:** Auctionets søgning matcher ord løst. Et søgeord som "space age" gav ét ikke-relevant resultat (kommode). Læs hvert resultat, og afvis det, der ikke matcher målet.
- **Login og bud:** Der bydes og logges ikke ind. Stop ved login-krav, og omgå dem ikke.

## Kørsel 2026-11-14 (dækning)

Søgt via Auctionet `company_id=526`:

- Række 2 (PH 4/3): "ph 4/3", "poul henningsen", "pendel". Fund: en hvid PH 4/3 (afvist, farve hvid, mangler dækplade). Ingen orange eller blå.
- Række 20 (Brylle): "brylle". Ingen resultater.
- Række 21 (Bent Karlby): "bent karlby". Fund: 2 lots (se nedenfor).
- Række 23 (Panton magasinholder): "panton", "magasinholder". To Panton-magasinstativer, begge solgt (afvist).
- Række 24 (Kartell ur): "kartell", "vægur". Ingen Kartell-ur.
- Række 25 og 26 (Space Age): "space age", "pendel", "lampe" (35 lamper). Ingen Space Age-lamper.
- Række 27 (Panum/Koppel ur): "vægur". Ingen Koppel-ur.
- Møbler række 5 (1-2-3): ikke søgt på Woxholt endnu.

Ikke søgt: sortering efter nyeste er ikke bekræftet. Alle 35 lamper er ikke gennemgået enkeltvis, kun de søgeord, der matcher målene.

## Fund 2026-11-14 (ikke skrevet til artefakt-DB, se note nedenfor)

- **Auctionet 5525853, Bent Karlby tilskrevet væglampe (Lyfa, 1950-60'erne):** række 21. Vurdering 800 DKK, ingen bud, slutter 20.11.2026 kl. 18:32. Status `Sandsynlig med forbehold`, da designeren er tilskrevet. Link: https://auctionet.com/da/5525853
- **Auctionet 5558030, Bent Karlby tilskrevet bordlampe (antageligvis Lyfa, midten af 1900-tallet):** række 21. Vurdering 3.000 DKK, højeste bud 402 DKK, slutter 20.11.2026 kl. 21:54. Status `Sandsynlig med forbehold`. Rød skærm, afkortet ledning, "fejl og mangler kan forekomme". Link: https://auctionet.com/da/5558030

Afviste Woxholt-lots: 5547804 (PH 4/3 hvid, 800 DKK vurdering, slutter 18.11) og Panton-magasinstativerne 4963500 og 4495690 (solgt).

Note: Skrivning til artefakt-DB blev afvist den 2026-11-14 med `network_off`. Fundene ligger i denne fil og i projektets dokument `claude/pending-finds-2026-11-14.md`, til de kan skrives.
