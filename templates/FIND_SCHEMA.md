# Datastruktur for sidens database

Siden `https://claude.ai/artifact/WRGmgJnVgvKhDegpB6q5x8` læser fire samlinger fra sin database: `categories`, `targets`, `finds` og `runs`. `feedback` skrives af siden. Agenterne læser den kun. Skriv med `ArtifactData` og `url` = sidens URL. Publicér aldrig siden igen for at tilføje fund. Ret kun sidens fil ved designændringer.

Al tekst på siden er dansk.

## `categories/<slug>`: en søgeområde-fane

`{ "name": "Lamper", "order": 1 }`

Slugs er små bogstaver, tal og bindestreger, fx `lamper`. Slugen er fanens adresse (`#lamper`). Slet aldrig en kategori, der har fund.

Alle `finds`, `targets` og `runs` har feltet `category` med slugen. Mangler det, tæller dokumentet som `lamper`.

## `finds/<id>`: ét fund pr. annonce

Id'et er `<platform med småt>-<annonce-id>`, fx `dba-26284641`. Slet aldrig et fund. En fjernet annonce bliver liggende med `available: "nej"`.

| Felt | Betydning |
|---|---|
| `category` | Kategoriens slug, fx `lamper` |
| `row` | Lampens `order` på listen (1, 2, 3 …). Siden bruger den til at knytte fund til `targets` |
| `name` | Kort navn, fx `Flowerpot VP3, mat hvid` |
| `type` | Én dansk type: `Bordlampe`, `Loftlampe`, `Standerlampe`, `Gulvlampe` eller `Væglampe` |
| `colors` | Liste med danske farver med stort begyndelsesbogstav, hovedfarven først, fx `["Hvid", "Orange"]`. Brug disse navne: Hvid, Sort, Grå, Beige, Brun, Rød, Orange, Gul, Grøn, Blå, Lilla, Pink, Guld, Sølv, Messing, Krom, Træ |
| `plat` | `DBA`, `Vinted` eller `Tradera`. Andre platforme tilføjes her, når de bruges |
| `city` | By, eller `by ukendt` |
| `direct` | `Ja`, `Nej` eller `Tjek` |
| `status` | `Bekræftet`, `Sandsynlig med forbehold` eller `Uklar identitet` |
| `link` | Direkte link til annoncen |
| `listedAt` | ISO-tid med offset, fx `2026-10-30T09:39:00+01:00`. Vises kun en relativ alder ("22 t. siden"), beregnes tiden, og `dateApprox` sættes til `true` |
| `dateKind` | `redigeret` (DBA viser kun sidst redigeret) eller `uploadet` |
| `dateApprox` | `true` eller `false` |
| `note` | Hvad der understøtter identifikationen, og hvad der mangler. Kort |
| `check` | Kun når brugeren skal verificere noget. Skriv hvad der afviger. Udelad feltet ellers |
| `price` | Aktuel pris i kr. som tal |
| `priceNote` | Valgfrit, fx `for begge` |
| `priceHistory` | `[{"d":"30.10","p":900}, ...]`. Én post pr. kørsel, hvor prisen ændrede sig. Første post er prisen, da fundet blev set første gang |
| `firstSeen` | ISO-tid for kørslen, der fandt fundet første gang |
| `lastChecked` | ISO-tid for seneste tilgængelighedstjek |
| `available` | `ja`, `nej` eller `ukendt` |
| `goneAt` | ISO-tid for kørslen, der fandt fundet fjernet. Kun når `available` er `nej` |

## `targets/<slug>-row-<N>`: én pr. række på listen

Fx `lamper-row-5`, hvor `N` er listens `order`. `{ "category": "lamper", "row": N, "model": "...", "designers": ["..."], "producers": ["..."] }`. `model` er en tom streng, når rækken ikke har model. Synkronisér med lampelisten. Sidens filtre bygges ud fra disse.

## `runs/<YYYY-MM-DD-HHMM>`: én pr. kørsel

```
{ "category": "lamper", "date": "<ISO-tid>", "platforms": ["DBA", "Vinted"],
  "sections": [ { "title": "Gennemført", "items": ["..."] }, ... ] }
```

Foreslåede sektionstitler: `Gennemført`, `Ikke gennemført`, `Begrænsninger`, `Tilgængelighed`, `Prisændringer`, `Fravalgt`, `Sælgere`. Hvert punkt er én almindelig sætning.

## `feedback/<find-id>`: brugerens vurdering af et fund

Skrives af siden, når brugeren trykker på en vurdering. Id'et er fundets id. Agenterne læser kun.

```
{ "findId": "dba-26284641",
  "verdict": "godt" | "nej" | "koebt",
  "reasons": ["For dyrt", "For langt væk"],
  "at": "<ISO-tid for vurderingen>",
  "snapshot": { name, type, plat, city, row, link, model, designers, producers,
                price, firstPrice, direct, status, available, listedAt, ageHours } }
```

- `verdict`: `godt` = Godt fund, `nej` = Ikke interessant, `koebt` = Købt.
- Årsager ved `nej`: `For dyrt`, `Dårlig stand`, `For langt væk`, `Forkert model`, `Forkert farve`, `Mistanke om kopi`, `Ikke vores stil`. Ved `godt`: `God pris`, `Sjælden model`, `Flot stand`. Flere kan vælges. `koebt` har ingen årsager.
- `snapshot` er en kopi af fundet på vurderingstidspunktet. Senere prisændringer ændrer ikke, hvad vurderingen handlede om.
- Et fund uden dokument her er ikke vurderet. Behandl det som ukendt, aldrig som et "nej".
- `Forkert model`, `Forkert farve`, `Dårlig stand` og `Mistanke om kopi` betyder, at søgningen missede. `For dyrt`, `For langt væk` og `Ikke vores stil` betyder, at lampen var rigtig, men ikke en god handel for butikken.
