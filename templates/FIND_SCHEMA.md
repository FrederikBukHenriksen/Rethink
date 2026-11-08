# Databasen: `database.db`

SQLite-filen i mappen, med den datamodel brugeren har givet. Alt, der gemmes, går igennem `scripts/db.py`. Skriv aldrig direkte i filen.

## Kommandoer

```
python3 scripts/db.py init                    # tjek at tabellerne findes
python3 scripts/db.py sync-lampe FIL          # lampelisten ind i targets
python3 scripts/db.py import-feedback FIL     # brugerens favoritter og skjulte fund ind i user_actions
python3 scripts/db.py gem-resultat FIL        # fund, versioner og gennemførte søgninger
python3 scripts/db.py cutoff LAMPE PLATFORM   # cutoff for en lampe på en platform; 'ingen' hvis ingen
python3 scripts/db.py slet-fund FUND_ID       # slet ét fund, fx dba-26284641
python3 scripts/db.py soegeplan               # hvad der skal søges nu, med cutoff pr. platform (JSON)
python3 scripts/db.py eksport-lamper FIL      # lamper fra databasen i lampelistens form (JSON)
python3 scripts/db.py eksport-side FIL        # kategorier, targets og fund fra databasen i sidens form (JSON)
python3 scripts/db.py status                  # antal rækker pr. tabel
```

Alle kommandoer kører i én transaktion. Fejler noget, skrives intet.

## Cutoff

Cutoff gælder for én lampe (target) på én platform. Det er tidspunktet for den seneste gennemførte søgning på netop det par. Den findes i `runs`. En søgning, der ikke blev gennemført, bliver ikke gemt i `runs`, og derfor flytter den ikke cutoff.

## Tabeller

| Tabel | Hvad en række er |
|---|---|
| `platforms` | En markedsplads: DBA, Lauritz, Tradera, Vinted, Facebook. |
| `lamp_types` | Lampetyperne: Bordlampe, Loftlampe, Standerlampe, Gulvlampe, Væglampe. |
| `color_type` | Farverne: Hvid, Sort, Grå, Beige, Brun, Rød, Orange, Gul, Grøn, Blå, Lilla, Pink, Guld, Sølv, Messing, Krom, Træ. |
| `targets` | En lampe fra listen. Id'et er `lamper-` plus listens id, fx `lamper-l07`. |
| `target_types` | Lampetyper for en target. |
| `target_colors` | Tilladte (`tilladt`) og fravalgte (`fravalg`) farver for en target. |
| `target_terms` | Søgeord (`tilvalg`) og fravalgte ord (`fravalg`) for en target. |
| `target_platforms` | De platforme, en target søges på. |
| `runs` | En gennemført søgning på en target og en platform, med tidspunktet hvor den blev afsluttet. Bruges til cutoff. |
| `finds` | Et fund: id, platform, target og link. Id'et er `<platform med småt>-<annonce-id>`. |
| `ads` | Fundets aktuelle tilstand: én række pr. fund. |
| `targets_rev` | Historik for targets: hver gang en target ændrer sig ved synk, gemmes den gamle tilstand her med tidspunkt. |
| `ads_rev` | Historik for fund: hver ændring (`kind` = `ændring`) og hvert tjek (`kind` = `tjek`). Prishistorik, første gang set og `lastChecked` læses herfra. |

De to historiktabeller har en fremmednøgle til deres hovedtabel (`targets_rev` til `targets`, `ads_rev` til `ads`). Når hovedrækken slettes, slettes historikken med den.
| `user_action_type` | De handlinger, der findes: `favorit` og `skjult`. Skjult gælder både fund og lamper. |
| `user_actions` | Brugerens handlinger, som den nuværende tilstand: på et fund (favorit, skjult) eller på en lampe (skjult = arkiveret). |

Et fund har altid én target og én platform. Det fund, der kommer tilbage af en søgning, kobles til den target, der blev søgt for.

## Artefakterne

Databasen er den eneste sandhed. Lampelisten og siden er spejlinger af den.

- **Lampelisten** (`lamper`) læses ind før hver kørsel med `sync-lampe`. Efter kørslen skrives den fra `eksport-lamper`. Familiens ændringer i listen går dermed først ind i databasen, og derefter tilbage i listen i den form databasen har. `archived` gemmes som handlingen `skjult` på lampen i `user_actions`, og eksporten skriver feltet ud fra den.
- **Siden** skriver `categories`, `targets` og `finds` fra `eksport-side`. `feedback` skrives af siden og læses ind med `import-feedback`. Siden kender ikke `status` og `listedAt` for ældre fund, fordi de ikke står i databasen. Det vises som "Uklar identitet" og "Dato ukendt".
- Eksporten skriver ikke `runs`, så siden viser ikke søgedækningen. Den står i svaret til brugeren.

## Felter

**`targets`**

- `list_id`: listens id, fx `l07`. `sort_order`: listens `order`.
- `model`, `designer`, `producer`: tekst fra listen. `producer` er listens `producent`.
- `max_price`: heltal i kr., eller tom, hvis der ingen grænse er.
- `aktiv`: 1 kun, når listen har `aktiv` = sand, og targetet ikke er `skjult`. Targets, der ikke står på listen, bliver 0. De slettes ikke.
- `image_url`: listens `billede`.

**`finds`**

- `plat`: platformens navn. `target_id`: den target, fundet blev fundet for. `link`: annoncens link.

**`ads`** (aktuel tilstand, nøglen er `find_id`)

- Tidligere versioner ligger i `ads_rev`. Der er ingen tidskolonne i `ads`.
- `title`, `description`, `city`: tekst fra annoncen. `city` er `by ukendt`, hvis byen ikke står der.
- `type`: en af lamp_types. `color`: den vigtigste farve, eller tom.
- `direct`: `Ja`, `Nej` eller `Tjek`.
- `price`: heltal i kr.
- `available`: `ja`, `nej` eller `ukendt`.
- `note`: fri tekst. Status, farver og annonceringsdato står her, fordi modellen ikke har egne felter til dem.

**`runs`**

- `completed_at`: ISO-tid med offset. Det er tidspunktet, hvor søgningen blev afsluttet.

**`user_actions`**

- Hver række har enten `find_id` (fund) eller `target_id` (lampe), aldrig begge.
- `action`: en af `user_action_type`. `favorit` og `skjult` kommer fra stjernen og skraldespanden på siden. `skjult` på en lampe kommer fra arkivering på listen.
- `skjult` på en lampe betyder arkiveret. Den sættes, når familien arkiverer en række på listen, og fjernes, hvis de fortryder.
- `favorit` og `skjult` på et fund er den tilstand, siden viser. Når du importerer, erstatter den det, der er i databasen for fund.
- `at`: hvornår handlingen blev lavet.

## JSON-filer

### `sync-lampe`

Lampelisten, som `ArtifactData` returnerer den:

```json
[{"id": "l07", "data": {"aktiv": true, "archived": false, "designer": "Jo Hammerborg",
                        "type": "gulvlampe", "order": 7, "sites": ["DBA"],
                        "soegeord": "", "fravalgteSoegeord": "", "tilladteFarver": "",
                        "fravalgteFarver": "", "maksPris": null, "billede": "", "model": "",
                        "producent": "", "updatedAt": "..."}}]
```

Tomme rækker springes over. Alle værdier i `type`, `tilladteFarver`, `fravalgteFarver`, `sites` skal findes i tabellerne. Ellers stopper kommandoen med en fejl.

### `import-feedback`

Samlingen `feedback` på siden. Hvert dokument er et fund med en handling. Et fund uden dokument har ingen handling:

```json
[{"id": "dba-26278770", "data": {"findId": "dba-26278770", "action": "favorit",
                                  "at": "2026-11-08T17:01:00+01:00"}}]
```

`action` er `favorit` (stjernen) eller `skjult` (skraldespanden). Skjulte fund vises stadig på siden,. Fjernes en handling på siden, mangler dokumentet, og handlingen fjernes også i databasen. En tom liste er gyldig, men kun hvis læsningen lykkedes.

### `gem-resultat`

Resultatet af én lampe:

```json
{
  "lampe_id": "l07",
  "fund": [
    {"platform": "DBA", "ekstern_id": "26568341",
     "link": "https://www.dba.dk/recommerce/forsale/item/26568341",
     "navn": "Flot retro gulvlampe, Jo Hammerborg", "lampetype": "Gulvlampe",
     "farver": "Rød", "status": "Bekræftet", "beskrivelse": "...",
     "pris": 500, "by": "Sorø", "kan_koebes_direkte": "Nej",
     "tilgaengelig": "ja", "listet_tid": "2026-11-08T14:00:00+01:00", "note": null}
  ],
  "fjernet": [{"platform": "DBA", "ekstern_id": "26276621"}],
  "soegninger": [
    {"platform": "DBA", "status": "gennemfoert", "tidspunkt": "2026-11-08T16:00:00+01:00"}
  ]
}
```

- Et nyt fund kræver `navn`, `lampetype`, `pris`, `kan_koebes_direkte`, `tilgaengelig` og `link`. `lampetype` er Bordlampe, Loftlampe, Standerlampe, Gulvlampe eller Væglampe.
- Et kendt fund kræver kun `platform`, `ekstern_id` og de felter, der ændrer sig. Felter, der ikke står i filen, beholdes.
- En ny version gemmes kun, når indholdet ændrer sig.
- `soegninger` bruges kun til søgninger på en lampe. Kun `gennemfoert` gemmes i `runs`. `tidspunkt` er den tid, søgningen blev afsluttet. Standard er nu.
- Søgninger med andre status, og dækningsteksten, står ikke i databasen. De skal med i svaret til brugeren.
