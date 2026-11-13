# Data schema for the living page

The page `https://claude.ai/artifact/4PFuzWt2x5ZqhdzyanGTtA` reads three collections from its database. Write them with the `ArtifactData` tool (`url` = the page URL). Never publish the page again to add finds. Only change the page file for design changes.

All text shown on the page is Danish.

## `categories/<slug>` — one document per search area (a tab on the page)

`{ "name": "Lamper", "order": 1, "platforms": [...] }` (older documents may still carry `workbook` and `sheet`; ignore them, the Excel workbook is no longer used)

The slug is lower case ASCII letters, digits and hyphens only, for example `lamper`, `keramik`, `kommoder`, `stole`. It is also the tab's address on the page (`#keramik`). Create a category document when a new search area is set up, and add its search list as `targets` documents. The page shows one tab per category document. Never delete one that has finds.

Every `finds`, `targets` and `runs` document has a `category` field with the slug. A document without it counts as `lamper`.

## `finds/<id>` — one document per listing

The id is `<platform lowercase>-<listing id>`, for example `dba-26284641` or `vinted-10582416262`. Never delete a find. A removed or sold listing stays, with `available: "nej"`. The page never shows finds with `available: "nej"`, so this is what removes them from view.

| Field | Meaning |
|---|---|
| `category` | Category slug, for example `lamper` |
| `row` | Row number of the target in `targets` |
| `name` | Short lamp name, for example `Flowerpot VP3, mat hvid` |
| `type` | One lamp type in Danish, for example `Bordlampe`, `Loftlampe`, `Standerlampe`, `Væglampe` |
| `colors` | List of colours in Danish with a capital letter, main colour first, for example `["Hvid", "Orange"]`. Use plain names: Hvid, Sort, Grå, Beige, Brun, Rød, Orange, Gul, Grøn, Blå, Lilla, Pink, Guld, Sølv, Messing, Krom, Træ |
| `plat` | `DBA`, `Vinted` or `Tradera` |
| `city` | City, or `by ukendt` |
| `direct` | `Ja`, `Nej` or `Ukendt`. `Ja` only when the listing offers a direct purchase (on DBA: Fiks færdig is offered explicitly, see `agents/platforms/dba.md`). `Nej` when the listing clearly offers no direct purchase. `Ukendt` when it cannot be seen or is ambiguous |
| `status` | `Bekræftet`, `Sandsynlig med forbehold` or `Uklar identitet` |
| `link` | Direct listing URL |
| `image` | URL of the listing's first product photo: the `og:image` meta tag on the listing page, for example `https://images.dbastatic.dk/dynamic/1280w/item/<id>/<uuid>`. The page shows it as a small thumbnail. Leave the field out if it cannot be read |
| `stand` | Optional. The condition as the listing states it, in the listing's own words (e.g. "som ny", "God, men brugt"). Leave it out if the listing does not state a condition. Shown on the page only when present |
| `thumb` | A 306 px JPEG thumbnail of the same photo (the width of DBA search-result images), as an inline `data:image/jpeg;base64,...` string (made with ImageMagick `convert -thumbnail 306x306^ -gravity center -extent 306x306 -quality 70`). The page shows this first. Written for every new find on every platform, and kept at ~4–25 KB. Leave the field out if the photo cannot be read |
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

## `targets/<slug>-row-<N>` — one document per search-list row

For example `lamper-row-5`. `{ "category": "lamper", "row": N, "model": "...", "designers": ["..."], "producers": ["..."] }`. `model` is an empty string when the row has no model. This is the search list itself and is edited by the user on the page. Its other fields (`types`, `keywords`, `excludeKeywords`, `colorsAllowed`, `colorsRejected`, `maxPrice`, `images`, `platforms`, `active`) are described in `SETUP.md` section 2. The filters on the page are built from these.

## `runs/<YYYY-MM-DD-HHMM>` — one document per run

```
{ "category": "lamper", "date": "<ISO time>", "platforms": ["DBA", "Vinted"], "searched": {"DBA": "<ISO time the DBA search started>", "Vinted": "<ISO time the Vinted search started>"},
  "sections": [ { "title": "Gennemført", "items": ["..."] }, ... ] }
```

Suggested section titles: `Gennemført`, `Ikke gennemført`, `Begrænsninger`, `Tilgængelighed`, `Prisændringer`, `Fravalgt`, `Sælgere`. Each item is one plain sentence.

## `feedback/<find id>` — the user's rating of a find

Written by the page when the user taps a rating. The id is the same as the find's id. The agents only read this collection. They never write it.

```
{ "findId": "dba-26284641",
  "verdict": "godt" | "nej" | "koebt" | "skrald",
  "reasons": ["For dyrt", "For langt væk"],
  "at": "<ISO time of the rating>",
  "snapshot": { name, type, plat, city, row, link, model, designers, producers,
                price, firstPrice, direct, status, available, listedAt, ageHours } }
```

- `verdict`: `godt` = Godt fund, `nej` = Ikke interessant, `koebt` = Købt.
- `skrald` = Skraldespand. The user has thrown the listing away: it never shows on the page again (unless the user filters on "Skraldespand" to restore it). The find stays in `finds` with its id, so agents must remember it exists and never add it again, never re-surface it and never count it as a new find. Keep checking availability as usual or skip it; either way the page hides it. `skrald` has no reasons and says nothing about the search or the lamp, so do not use it as a signal for what to search for.
- Reasons for `nej`: `For dyrt`, `Dårlig stand`, `For langt væk`, `Forkert model`, `Forkert farve`, `Mistanke om kopi`, `Ikke vores stil`. For `godt`: `God pris`, `Sjælden model`, `Flot stand`. Several can be set. `koebt` has none.
- `snapshot` is a copy of the find when it was rated, so later price changes do not change what the rating was about.
- A find with no document here is not rated. Treat it as unknown, never as a "no".
- `Forkert model`, `Forkert farve`, `Dårlig stand` and `Mistanke om kopi` say the search missed. `For dyrt`, `For langt væk` and `Ikke vores stil` say the lamp was right but not a good deal for the shop.
