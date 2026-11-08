# Data schema for the living page

The page `https://claude.ai/artifact/WRGmgJnVgvKhDegpB6q5x8` reads three collections from its database. Write them with the `ArtifactData` tool (`url` = the page URL). Never publish the page again to add finds. Only change the page file for design changes.

All text shown on the page is Danish.

## `categories/<slug>` — one document per search area (a tab on the page)

`{ "name": "Lamper", "order": 1, "workbook": "DBA-lampesøgning.xlsx", "sheet": "Søgeliste" }`

The slug is lower case ASCII letters, digits and hyphens only, for example `lamper`, `keramik`, `kommoder`, `stole`. It is also the tab's address on the page (`#keramik`). Create a category document when a new search area is set up, with the sheet that holds its search list. The page shows one tab per category document. Never delete one that has finds.

Every `finds`, `targets` and `runs` document has a `category` field with the slug. A document without it counts as `lamper`.

## `finds/<id>` — one document per listing

The id is `<platform lowercase>-<listing id>`, for example `dba-26284641` or `vinted-10582416262`. Never delete a find. A removed listing stays, with `available: "nej"`.

| Field | Meaning |
|---|---|
| `category` | Category slug, for example `lamper` |
| `row` | Excel row number in the category's sheet |
| `name` | Short lamp name, for example `Flowerpot VP3, mat hvid` |
| `type` | One lamp type in Danish, for example `Bordlampe`, `Loftlampe`, `Standerlampe`, `Væglampe` |
| `colors` | List of colours in Danish with a capital letter, main colour first, for example `["Hvid", "Orange"]`. Use plain names: Hvid, Sort, Grå, Beige, Brun, Rød, Orange, Gul, Grøn, Blå, Lilla, Pink, Guld, Sølv, Messing, Krom, Træ |
| `plat` | `DBA`, `Vinted` or `Tradera` |
| `city` | City, or `by ukendt` |
| `direct` | `Ja`, `Nej` or `Tjek` |
| `status` | `Bekræftet`, `Sandsynlig med forbehold` or `Uklar identitet` |
| `link` | Direct listing URL |
| `listedAt` | ISO time with offset, for example `2026-10-30T09:39:00+01:00`. If only a relative age is shown ("22 t. siden"), compute it and set `dateApprox: true` |
| `dateKind` | `redigeret` (DBA shows only last edited) or `uploadet` |
| `dateApprox` | `true` or `false` |
| `note` | What supports the identification and what is missing. Short |
| `check` | Only when something must be verified by the user. Say what differs. Leave the field out otherwise |
| `price` | Current price as a number in DKK |
| `priceNote` | Optional, for example `for begge` |
| `priceHistory` | `[{"d":"30.10","p":900}, ...]`. One entry per run where the price changed. The first entry is the price when first found |
| `firstSeen` | ISO time of the run that first found it |
| `lastChecked` | ISO time of the latest availability check |
| `available` | `ja`, `nej` or `ukendt` |
| `goneAt` | ISO time of the run that found it removed. Only when `available` is `nej` |

## `targets/<slug>-row-<N>` — one document per Excel row

For example `lamper-row-5`. `{ "category": "lamper", "row": N, "model": "...", "designers": ["..."], "producers": ["..."] }`. `model` is an empty string when the row has no model. Keep in sync with `Søgeliste`. The filters on the page are built from these.

## `runs/<YYYY-MM-DD-HHMM>` — one document per run

```
{ "category": "lamper", "date": "<ISO time>", "platforms": ["DBA", "Vinted"],
  "sections": [ { "title": "Gennemført", "items": ["..."] }, ... ] }
```

Suggested section titles: `Gennemført`, `Ikke gennemført`, `Begrænsninger`, `Tilgængelighed`, `Prisændringer`, `Fravalgt`, `Sælgere`. Each item is one plain sentence.

## `feedback/<find id>` — the user's rating of a find

Written by the page when the user taps a rating. The id is the same as the find's id. The agents only read this collection. They never write it.

```
{ "findId": "dba-26284641",
  "verdict": "godt" | "nej" | "koebt",
  "reasons": ["For dyrt", "For langt væk"],
  "at": "<ISO time of the rating>",
  "snapshot": { name, type, plat, city, row, link, model, designers, producers,
                price, firstPrice, direct, status, available, listedAt, ageHours } }
```

- `verdict`: `godt` = Godt fund, `nej` = Ikke interessant, `koebt` = Købt.
- Reasons for `nej`: `For dyrt`, `Dårlig stand`, `For langt væk`, `Forkert model`, `Forkert farve`, `Mistanke om kopi`, `Ikke vores stil`. For `godt`: `God pris`, `Sjælden model`, `Flot stand`. Several can be set. `koebt` has none.
- `snapshot` is a copy of the find when it was rated, so later price changes do not change what the rating was about.
- A find with no document here is not rated. Treat it as unknown, never as a "no".
- `Forkert model`, `Forkert farve`, `Dårlig stand` and `Mistanke om kopi` say the search missed. `For dyrt`, `For langt væk` and `Ikke vores stil` say the lamp was right but not a good deal for the shop.
