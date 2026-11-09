---
name: find-used-design-lamps
description: Search selected second-hand marketplaces for design lamps matching every row in the project's Excel sheet Søgeliste. Use when the user has confirmed marketplace platforms and listing recency for a search run.
---

# Find Used Design Lamps

## Purpose

Find newly listed second-hand design lamps for the user's store. Use the project's Excel workbook as the source of truth for what to search for. Use the browser to inspect marketplace search results and individual listings.

## Preconditions

Before this skill is run, the project start-of-run gate must be complete:

- Excel workbook access has been verified for this run.
- The `Søgeliste` sheet has been read successfully.
- The user has specified the marketplaces.

If any precondition is missing, stop and ask for it. Do not begin searching.

## Roles

This run uses a main agent and one subagent per selected platform.

- **Main agent:** runs the start-of-run gate, reads the workbook (section 1), builds the search list (section 2), starts the subagents, deduplicates (section 6), checks the results and writes the final report (section 7).
- **Platform subagent:** searches one platform in the browser (section 3), applies the inclusion rules (section 4), determines direct purchase (section 5), and returns candidates in the format in `agents/platform-searcher.md`. It follows section 8 as well.

The subagent brief is `agents/platform-searcher.md`. The rules stay in this file only. Do not copy them into the brief.

### Checking subagent results

Before a find goes in the report, the main agent confirms that it has a listing URL, a price, and evidence of listing date. A find missing any of these is moved to `Tjek selv` or dropped, with the reason in `Søgedækning og begrænsninger`. If a result looks doubtful, the main agent opens the listing itself before deciding. A platform that a subagent could not search is reported as not searched. It is never reported as having no finds.

## 1. Read and interpret the workbook

Read every populated data row in the sheet `Søgeliste`. Each row is a separate search target. Do not skip rows.

Interpret columns as follows:

- `Model`: lamp model/name. If empty, search at designer or manufacturer level.
- `Type`: lamp type, such as pendant, table, floor, or wall lamp. If empty, accept all types.
- `Designer`: use as a search term and as evidence when identifying the lamp.
- `Producent`: use as a search term and as evidence when identifying the lamp.
- `Søgeord`: additional search terms. Split multiple values on semicolons (`;`).
- `Fravalgte søgeord`: reject a listing if its title or description contains any of these terms, allowing for case differences and obvious inflections.
- `Tilladte farver`: if empty, all colours are allowed. Otherwise, accept only listed colours or clearly equivalent descriptions.
- `Fravalgte farver`: reject listings in these colours.
- `Maks pris`: if empty, there is no price ceiling. Otherwise, reject listings above this amount. Do not assume a currency conversion unless the listing currency and conversion source are clear.
- `Billede reference`: filenames of reference images in the project. Match filenames to project files and inspect the images when available.

Split semicolon-separated cells into individual values, trim whitespace, and ignore empty values.

If a column is missing, renamed, or ambiguous, do not guess. Report the issue and ask the user how to interpret it before searching.

Keep the source row number for every target so the final report can preserve one section per Excel row.

## 2. Build searches for each row

Search every row on every user-selected platform, except rows whose checkbox for that platform is not ticked in the sheet. Unticked or empty means not searched.

### Rows with a Model value

Create searches for:
- The model name.
- Each individual value in `Søgeord`.

Where useful, combine the model with designer or manufacturer to improve precision. Do not replace the required individual searches with only one broad combined query.

### Rows without a Model value

Search using the designer or manufacturer, preferably together with `Type` where present. For example: `Jo Hammerborg gulvlampe`.

If both Designer and Producent are present, search both where useful.

### Platform-specific wording

On Vinted and Tradera, add the word `lampe` to broad searches to reduce irrelevant clothing and non-lamp results. Adapt the word to the platform's language where necessary, but preserve the identifying model/designer terms.

## 3. Search using the browser

Use Claude in Chrome or the browser available in Claude Cowork. Do not use ordinary web search as a substitute for marketplace search.

For each selected platform:

1. Open the marketplace.
2. Run the relevant searches for every Excel row.
3. Sort by newest/recently listed where the platform supports it.
4. Go through the results without a time limit.
5. Open promising listings and read both title and description.
6. Inspect listing images when text does not establish model or colour, and compare them with the Excel reference images where available.
7. Record the listing date or the strongest available evidence of recency.
8. Record the listing URL and details needed for the report.

If the platform does not expose a reliable listing date, do not guess how old it is. Mark it `Tjek` or exclude it from confirmed new finds, explaining the limitation.

Do not claim that all listings on a platform were exhaustively checked if search pagination, login restrictions, sorting, or access limitations prevented that.

## 4. Apply the inclusion and exclusion rules

A listing qualifies only if it passes all applicable checks:

- It is a complete lamp, not merely a loose shade, spare part, or component.
- It is not described as defective, broken, or for repair.
- It is not reserved.
- It is the correct lamp model or a defensible match to the designer/manufacturer target.
- It matches `Type` when a type is specified.
- It complies with allowed and excluded keywords.
- It complies with allowed and excluded colours.
- It does not exceed `Maks pris`.

### Identification confidence

Use the title, description, seller-provided details, and images together.

- **Confirmed match:** model/identity and type are supported by the listing evidence.
- **Likely match with caveat:** most evidence fits, but a small discrepancy or missing detail remains. Include it under the closest matching lamp/type and state the caveat briefly.
- **Uncertain identity:** you cannot determine whether it is the correct lamp. Put it in the final `Tjek selv` section.
- **Not a match:** wrong model, type, colour, condition, price, date, or excluded term. Do not include it as a find.

Do not infer authenticity from appearance alone. If authenticity is not established, do not claim that the item is authentic.

## 5. Determine whether it can be bought directly

Use exactly `Ja`, `Nej`, or `Tjek`.

- **DBA:** `Ja` only when the listing explicitly offers `Fiks færdig`; otherwise `Nej`.
- **Vinted:** `Ja` for listings where the normal Vinted checkout/payment-and-shipping flow is available.
- **Tradera:** `Ja` only when the listing shows `Betaling via Tradera`.
- If the relevant information is not visible or is ambiguous, use `Tjek`.

Do not infer platform protection from the existence of a listing or a seller profile.

## 6. Avoid duplicates

The same listing may appear in multiple searches or match more than one Excel row.

- Deduplicate identical listing URLs within the report.
- If one listing plausibly matches multiple rows, place it under the best-fitting row and add a short cross-reference or caveat where useful.
- Do not count the same listing twice as two separate finds.

## 7. Final report

Produce one heading for every data row in `Søgeliste`, preserving the Excel row order.

Under each heading, include one line per qualifying find with:

- Lamp name/model.
- Price and currency.
- City/location, if visible.
- Platform.
- `Kan købes direkte: Ja/Nej/Tjek`.
- Direct listing link.
- A short caveat where relevant.

Use this format:

`Lamp/model — price — city — platform — Kan købes direkte: Ja/Nej/Tjek — link — note (if needed)`

If a row has no qualifying new listings, write exactly:

`Ingen nye fund`

At the end, include a `Tjek selv` section containing only listings whose identity could not be determined. Explain briefly what the user needs to verify.

If there are no uncertain listings, omit the `Tjek selv` section.

Also include a short `Søgedækning og begrænsninger` note listing:
- Platforms searched.
- Any platforms or searches that could not be completed.
- Any uncertainty about listing dates or access.

## 8. Hard boundaries

Never:
- Contact sellers.
- Send messages or offers.
- Negotiate.
- Reserve or buy items.
- Share the user's information.
- Change the Excel search criteria without permission.

You may navigate, search, open listings, inspect descriptions and images, and compile findings only.
