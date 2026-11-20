## 5. Decide what goes on the page

The `write` agent (`RUN.md` section 5) compares each searcher result with the verifier's result for the same link, and decides, using these rules.

| Verifier result | What you do |
|---|---|
| Same status, and price, direct purchase and date agree | Add the find. |
| `Ikke et match`, or `Stadig tilgængelig: Nej` | Leave it out. Note it in the run's coverage. |
| Weaker status than the searcher (for example `Uklar identitet` vs `Bekræftet`) | Add the find with the weaker status and fill `check` with what the user must verify. |
| Price, direct purchase, city or date differ | Add the find and fill `check`. Show both values and say which differ. |
| `Ikke kontrolleret` | Add the find. Put "ikke uafhængigt verificeret" in `note`. |

There is no separate "Tjek selv" list. The page shows a find with `check` as "Skal tjekkes".

In every case:

- A find needs a listing URL, a price and evidence of the listing date (`listedAt`). Without all three, drop it and say why in the run's coverage. Exception: on platforms that show no listing date (Vinted, Facebook Marketplace, Gul og Gratis), follow `RUN.md` section 7. A missing date is never a reason to drop such a find.
- Deduplicate on the find id (`<platform>-<listing id>`). A listing that already exists in `finds` is updated (section 6), never added twice. The same listing can fit several rows: keep it under its best-fitting row.
- A platform that could not be searched is reported as not searched, never as "no finds".
- A row that is not set to `true` for a platform is reported in the coverage as "fravalgt" for that platform, never as "no finds".
- Do not say a platform was exhaustively checked if access, login, sorting or pagination limited the search.
- Do not claim a listing is available unless the verifier or the listing page supports it.
- **Valuta (DKK).** `price`, `priceHistory` og `price` i `priceNote`-logikken skal altid være i DKK. Hvis annoncen oplyser en pris i EUR (fx `295 €`, `EUR 120`, `1.600 € VB`), omregnes med kurs **7,46** (DKK = EUR × 7,46, afrundet til hele kroner). Det oplyste EUR-beløb skrives i `priceNote` (fx `EUR 120, nuværende bud`), og `price` er den omregnede DKK-værdi. Et EUR-beløb må aldrig kopieres direkte til `price`. Svenske kroner (SEK) omregnes med ca. 0,68 DKK pr. SEK og skrives tilsvarende i `priceNote`. Kontroller efter hver skrivning, at `price` ≈ EUR × 7,46.
- **Price fields.** If a price reads as more than one amount (for example `20002000`) or is above 10,000,000 kr., the find is not written with that price. Note the problem in `check`, mark the find for manual review, and do not guess the price.
- **Status "Bekræftet".** Use only when the verifier confirmed all criteria: identity, designer or producer, colour, price, direct purchase and listing date. If any criterion is missing or only seen in a title, the status is "Sandsynlig med forbehold".

## 6. Write to the page database

Use `db_write` with several `ops` in one call where you write more than a couple of documents (up to 50 ops per call, one call at a time, and wait 2 seconds after a large call). Pin every change to an existing document with `ifVersion`. Use the field names in `templates/FIND_SCHEMA.md`.

1. **Targets.** Make sure `targets/<slug>-row-<N>` exists for every row the user has defined. The user edits `targets` on the page; never change a target's search criteria yourself. Only add missing `model`, `designers` or `producers` structure if a document lacks them, and keep a manufacturer (for example `&Tradition`) under `producers`.
2. **New finds.** Create `finds/<id>` as described in `templates/FIND_SCHEMA.md`. Set `image` to the first product photo's URL (see the schema). For every new find on every platform and in every category (lamper, mobler, plakater and any later category), also set `thumb` to a 306 px JPEG thumbnail of that photo (the width of DBA search-result images), as a `data:image/jpeg;base64,...` string (see the schema). A find without a readable photo gets neither field. Set `type` from what the listing shows (bordlampe, loftlampe, standerlampe, væglampe). If the listing does not say, use the target's `types`. When that has several types, pick the one the photos and title support, or say in `check` that the type is unclear. Set `colors` from the listing (plain colour names, main colour first). Set `firstSeen` and `lastChecked` to the run time, `available` to `ja` only if the verifier or the page supports it (otherwise `ukendt`), and `priceHistory` to one entry with today's date.
3. **Known finds (from section 1a and from new searches).**
   - Price: if the current price differs from `price`, set `price` to the new value and append `{"d":"dd.mm","p":<new>}` to `priceHistory`. Never rewrite earlier entries. Update `priceNote` only if the listing says so.
   - Availability: `Ja` → `available: "ja"`; `Nej` → `available: "nej"` and `goneAt` = run time; `Reserveret` → `available: "ukendt"` and say "reserveret" in `note`; `Uklar` → `available: "ukendt"`. If a removed find is online again, set `available: "ja"` and remove `goneAt` (`{"__delete__": true}`).
   - City: if a find has `city` `by ukendt` and an agent reports a city, set `city`.
   - Always set `lastChecked` to the run time when the page was actually opened.
4. **Run note.** Create `runs/<YYYY-MM-DD-HHMM>` with the platforms, the `searched` field (see Time window) and the coverage note: what was searched and checked, what could not be done, uncertainty about dates or buying flow, how many finds were added, which prices changed, which listings were removed, and what was left out and why.

**Write as you go, not at the end.** Open each listing as soon as it is found, and run the independent verification for it right away (see section 4). Once a find is verified, write it to the page at once, without waiting for the other searches or platforms. Price changes and `searched` values are written when their search is complete. A run that stops still keeps everything verified so far. An interrupted run then keeps what it had verified.

**Progress.** Every run document has a `progress` field. For each category and platform it says one of `færdig`, `delvis` (with the last row, and the last find if relevant) or `ikke startet`. The next run starts with `ikke startet` and `delvis` combinations, not with the ones already `færdig`, unless the criteria changed (see Time window).

**Completeness is not time-limited.** A platform's search is done only when every search is complete (read equals total, see `agents/platform-searcher.md`, section Completeness). Do not stop a search because of time. Only a real block (403, Cloudflare/Akamai, login, unreachable host) ends a platform early, and it is written as "ikke søgt" with the reason.

**Incomplete runs.** A blocked platform or a search that stays incomplete after splitting does not end the run. Mark the unit `blokeret` or `ufuldstændig` with the reason, and go on (`RUN.md` section 5). `requests/search` stays `kører` until every unit in the queue is `færdig`, `ufuldstændig` or `blokeret`. Only then is it set to `færdig`, with a note listing the units that were not completed.

Finish by writing a short summary into the run document (`runs`), since no user is present: how many finds were added, which prices dropped or rose, which listings disappeared, and which platforms or searches were not done. Do not paste the list of finds. The page has them.

## 7. Boundaries
# Data schema for the living page

The page `https://claude.ai/artifact/4PFuzWt2x5ZqhdzyanGTtA` reads its collections from its database. The artifact slug is `1b66f843-adeb-489c-9560-7328cd988787`. Write with the `db_write` tool (`slug` = the artifact slug, and `ifVersion` on every op that changes an existing document). Read with `db_get` or `db_list`. Never publish the page again to add finds. Only change the page file for design changes. If `db_write` returns `network_off`, the session cannot write to the artifact: keep the finds in the run document and say so in the reply.

All text shown on the page is Danish.

## `categories/<slug>` — one document per search area (a tab on the page)

`{ "name": "Lamper", "order": 1, "platforms": [...] }` (older documents may still carry `workbook` and `sheet`; ignore them, the Excel workbook is no longer used)

The slug is lower case ASCII letters, digits and hyphens only, for example `lamper`, `keramik`, `kommoder`, `stole`. It is also the tab's address on the page (`#keramik`). Create a category document when a new search area is set up, and add its search list as `targets` documents. The page shows one tab per category document. Never delete one that has finds.

Every `finds`, `targets` and `runs` document has a `category` field with the slug. A document without it counts as `lamper`.

## `finds/<id>` — one document per listing

The id is `<platform lowercase>-<listing id>`, for example `dba-26284641`, `vinted-10582416262`, `facebook-1759112305155778` or `catawiki-108326634`. Use the platform's first word in lowercase ASCII: `dba`, `vinted`, `facebook`, `catawiki`, `bidstrup`, `woxholt`, `sikoe`, `palsgaard`. Existing find `bistrup-5534129` has a typo; it should be `bidstrup-5534129` when it is next written. Never delete a find. A removed or sold listing stays, with `available: "nej"`. The page never shows finds with `available: "nej"`, so this is what removes them from view.

| Field | Meaning |
|---|---|
| `category` | Category slug, for example `lamper` |
| `row` | Row number of the target in `targets` |
| `name` | Short lamp name, for example `Flowerpot VP3, mat hvid` |
| `type` | One lamp type in Danish, for example `Bordlampe`, `Loftlampe`, `Standerlampe`, `Væglampe` |
| `colors` | List of colours in Danish with a capital letter, main colour first, for example `["Hvid", "Orange"]`. Use plain names: Hvid, Sort, Grå, Beige, Brun, Rød, Orange, Gul, Grøn, Blå, Lilla, Pink, Guld, Sølv, Messing, Krom, Træ |
| `plat` | The platform's name as the page shows it: `DBA`, `Vinted`, `Tradera`, `Facebook Marketplace`, `Catawiki`, `Bidstrup`, `Woxholt`, `Palsgaard`, `Sikö`, `Lauritz`, `Gul og Gratis`, `Klein Anzeigen` or `Reshopper` |
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
| `price` | Current price as a number in DKK. If the listing shows EUR, convert with 7.46 (DKK = EUR × 7.46) and write the original EUR amount in `priceNote`. Never copy the EUR number into `price` |
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
## 7. Platforms without a listing date

These rules replace the date requirement in `SETUP.md` section 5, for these platforms only.

- **Vinted and Facebook Marketplace.** The relative age ("for 3 dage siden") is the evidence. Set `listedAt` to the run time minus that age, and set `check` to "dato ud fra relativ alder". If only "Sidst set" is shown, set `listedAt` = null and `check` = "oprettelsesdato ikke vist".
- **Gul og Gratis and any other platform with no date.** Set `listedAt` = null and `check` = "oprettelsesdato ikke vist".
- **What counts as new.** A listing is new if its find id is not already in `finds`. Every page is still read to the end.
- A missing date is **not** a reason to drop a find or to call a search incomplete.

## 8. Your own context
