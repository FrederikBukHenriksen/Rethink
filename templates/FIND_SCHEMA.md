# Databasen: `database.db`

En SQLite-fil i mappen. Alt, der gemmes, går igennem `scripts/db.py`. En fjernet annonce får `tilgaengelig` = `nej`. Et fund slettes kun med `slet-fund`, når brugeren beder om det.

## Kommandoer

```
python3 scripts/db.py init                    # opret tabeller, hvis de mangler
python3 scripts/db.py sync-lampe FIL          # lampelisten ind i lampe
python3 scripts/db.py import-feedback FIL     # brugerens vurderinger ind i user_actions
python3 scripts/db.py ny-koersel KATEGORI     # start en kørsel; udskriver kørslens id
python3 scripts/db.py cutoff LAMPE PLATFORM   # cutoff for en lampe på en platform; 'ingen' hvis ingen
python3 scripts/db.py gem-resultat FIL        # resultatet af søgningen på én lampe
python3 scripts/db.py slet-fund FUND_ID       # slet ét fund med alt, der hører til det, fx dba-26284641
python3 scripts/db.py status                  # antal rækker pr. tabel
```

Alle kommandoer kører i én transaktion. Fejler noget, skrives intet.

## Cutoff

Cutoff gælder for én lampe på én platform. Den er starttidspunktet for den seneste gennemførte søgning på netop det par. Lampen Jo Hammerborg på DBA har sin egen cutoff, og Jo Hammerborg på Vinted har en anden. En søgning, der fejlede, flytter ikke cutoff. Databasen udregner cutoff, når `gem-resultat` gemmer en søgning. Agenten henter den først med `cutoff`.

`slet-fund` sletter annoncen, alle dens versioner, alle brugerhandlinger for den, og produktet, hvis ingen andre annoncer bruger det. Lampelisten (`lampe`), platformene og kørslerne (`koersel`, `soegning`) røres ikke. Fund-id'et gemmes i `slettede_fund`. Et slettet fund bliver ikke gemt igen af `gem-resultat`, og dets vurderinger bliver ikke importeret igen fra siden. `gem-resultat` svarer med, hvor mange der blev sprunget over af den grund.

## Tabeller

| Tabel | Hvad en række er |
|---|---|
| `produkt_kategori` | Et søgeområde. Lige nu kun `lamper`. |
| `platform` | En markedsplads: DBA, Vinted, Tradera, Facebook. |
| `lampe` | En række fra lampelisten. Holdes synkron med listen. |
| `produkt` | En lamp, som den står i en konkret annonce. Har `lampe_id`, hvis den kan kobles til listen. |
| `produkt_lampe` | Lampetypen for et produkt. |
| `annonce` | En annonce på én platform, identificeret ved `ekstern_id`. |
| `annonce_content` | En version af en annonce. Ny række kun, når indholdet ændrer sig. |
| `user_actions` | Brugerens vurderinger af fund, som hændelser. |
| `koersel` | En kørsel: tidspunkt og kategori. |
| `soegning` | Én søgning i en kørsel på én lampe og én platform: starttid, cutoff, status og dækning. |
| `slettede_fund` | Fund-id'er, der er slettet med `slet-fund`. De bliver ikke gemt igen. |

Visningen `annonce_nu` viser den seneste version af hver annonce. Brug den til at læse fund. Brug `annonce_content` til historik.

## Felter

**`lampe`** (fra listen)

- `id`: listens id, fx `l01`. `listen_order`: listens `order`.
- `model`, `type`, `designer`, `producent`, `soegeord`, `fravalgte_soegeord`, `tilladte_farver`, `fravalgte_farver`, `billede`: tekst fra listen.
- `maks_pris`: heltal i kr., eller tom, hvis der ingen grænse er.
- `sites`: platforme, adskilt med `; `.
- `aktiv`, `archived`: 0 eller 1. Mangler `aktiv` på listen, er den 0.
- `i_listen`: 0, hvis rækken ikke længere står på listen. Den slettes ikke.
- `listen_opdateret`: `updatedAt` fra listen. `synket`: hvornår rækken blev læst.

**`soegning`**

- `koersel_id`, `lampe_id`, `platform_id`: hvilken kørsel, lampe og platform. `lampe_id` er tom ved ad hoc-søgninger. `platform_id` er tom, når en lampe springes over uden platform.
- `tidspunkt`: hvornår søgningen startede.
- `cutoff`: kun annoncer publiceret efter dette tidspunkt. Tom = ingen grænse.
- `status`: `gennemfoert`, `fejlet` eller `sprunget_over`.
- `daekning`: én tekst om hvad der blev søgt, gennemgået og ikke gjort.

**`annonce_content`**

- `observeret`: første gang denne version blev set. `sidst_set`: sidste gang den blev set.
- `pris`: heltal i kr. `pris_note`: fx "for begge".
- `by`: sted, eller `by ukendt`.
- `kan_koebes_direkte`: `Ja`, `Nej` eller `Tjek`.
- `tilgaengelig`: `ja`, `nej` eller `ukendt`.
- `listet_tid`: ISO-tid med offset, fx `2026-10-30T09:39:00+01:00`.
- `dato_type`: `redigeret` (DBA viser kun sidst redigeret) eller `uploadet`.
- `dato_omtrentlig`: 1, når datoen er udregnet fra en relativ alder ("1 t.", "18 t.").
- `tjek`: det brugeren selv skal verificere. Tom, når der ikke er noget.
- `titel`, `beskrivelse`, `side_tekst`: tekst fra annoncen.

**`produkt`**

- `status`: `Bekræftet`, `Sandsynlig med forbehold` eller `Uklar identitet`.
- `farver`: danske farvenavne, hovedfarven først, adskilt med komma: Hvid, Sort, Grå, Beige, Brun, Rød, Orange, Gul, Grøn, Blå, Lilla, Pink, Guld, Sølv, Messing, Krom, Træ.
- `lampe_id`: listens id, hvis produktet kan kobles til en lampe.

**`user_actions`**

- `feedback_id`: fundets id på siden, fx `dba-26284641`.
- `annonce_id`: den annonce, id'et peger på. Tom, hvis annoncen ikke findes i databasen.
- `handling`: `godt`, `nej`, `koebt` eller `fjernet`. `fjernet` betyder, at brugeren har taget sin vurdering tilbage.
- `aarsager`, `tidspunkt`, `snapshot`: årsager, tidspunkt for vurderingen, og en kopi af fundet på det tidspunkt.
- Historikken bevares. Hver ændring er en ny række.

## JSON-filer

### `sync-lampe`

Lampelisten, som `ArtifactData` returnerer den:

```json
[{"id": "l01", "data": {"aktiv": true, "archived": false, "model": "PH 4/3", "order": 1,
                        "type": "loftlampe", "designer": "Poul Henningsen", "producent": "",
                        "soegeord": "ph 4/3; ph4/3", "fravalgteSoegeord": "",
                        "tilladteFarver": "orange; blå", "fravalgteFarver": "",
                        "maksPris": 900, "billede": "", "sites": [], "updatedAt": "..."}}]
```

### `import-feedback`

Samlingen `feedback` på siden. En tom liste er gyldig, men kun hvis læsningen lykkedes:

```json
[{"id": "dba-26546368", "data": {"findId": "dba-26546368", "verdict": "godt",
                                  "reasons": ["God pris"], "at": "2026-11-08T12:00:00+01:00",
                                  "snapshot": {...}}}]
```

`verdict` er `godt`, `nej` eller `koebt`. Årsager ved `nej`: For dyrt, Dårlig stand, For langt væk, Forkert model, Forkert farve, Mistanke om kopi, Ikke vores stil. Ved `godt`: God pris, Sjælden model, Flot stand.

### `gem-resultat`

Resultatet af én lampe. Felter, der ikke står i en `fund`-post, beholdes for en kendt annonce.

```json
{
  "lampe_id": "l07",
  "kategori": "lamper",
  "koersel_id": 2,
  "fund": [
    {"platform": "DBA", "ekstern_id": "26560542",
     "link": "https://www.dba.dk/recommerce/forsale/item/26560542",
     "navn": "PH5 Classic loft lampe i hvid", "model": "PH5", "designer": "Poul Henningsen",
     "producent": "Louis Poulsen", "farver": "Hvid, Rød, Blå", "status": "Bekræftet",
     "note": "Titel og beskrivelse siger PH5 og Louis Poulsen.", "lampetype": "Loftlampe",
     "titel": "PH5 Classic loft lampe i hvid", "beskrivelse": "...",
     "pris": 1800, "pris_note": null, "by": "Vanløse", "kan_koebes_direkte": "Nej",
     "tilgaengelig": "ja", "listet_tid": "2026-11-08T10:28:00+01:00",
     "dato_type": "redigeret", "dato_omtrentlig": 1, "tjek": null, "side_tekst": null}
  ],
  "fjernet": [{"platform": "DBA", "ekstern_id": "26546368"}],
  "soegninger": [
    {"platform": "DBA", "status": "gennemfoert", "tidspunkt": "2026-11-08T16:00:00+01:00",
     "daekning": "Jo Hammerborg gulvlampe, nyeste først: 0 fund"},
    {"platform": null, "status": "sprunget_over", "daekning": "Ikke valgt på listen"}
  ]
}
```

- En ny annonce kræver alle felter i `fund`. `lampetype` er Bordlampe, Loftlampe, Standerlampe eller Væglampe.
- En kendt annonce kræver kun `platform`, `ekstern_id` og de felter, der ændrer sig. Send også uændrede annoncer, du har tjekket, så `sidst_set` opdateres.
- `koersel_id` er påkrævet, når `soegninger` er med. Det er det tal, `ny-koersel` udskrev.
- `soegninger` skriver én række pr. post i `soegning`. Cutoff udregnes af databasen.
