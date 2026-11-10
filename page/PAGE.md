# The page

The page is the only place the user reads the finds. Its source is `page/rethink-soegerapport.html`. It is one self-contained HTML file. All text on it is Danish.

## What it shows

- Title "Søgerapport" with a small RETHINK wordmark on top. Below it one line: latest run, platforms, number of online listings, number of search rows.
- One tab per category (from `categories`). The tab shows the number of listings that are not removed.
- Filters: free text, then a "Produkt" group (Model, Designer, Producent, Type, Farve, max price) and an "Annonce" group (Platform, Tid, "Kan købes direkte", "Kun favoritter"). Sorting and a reset button.
- A flat list. Each listing is a row: name (links to the listing) and price, then one detail line (type, colours, platform, city, status, direct purchase, date, last checked). Open the row for the note, `check` text, price history and last-checked time. A find with `check` shows "Skal tjekkes". A find with `available: "nej"` (sold or removed) is never shown on the page. The agent marks it `nej` on every run, so sold items drop off the page by themselves; the record stays in the database.
- A star button per row marks a find as a favourite. Only the owner can click it (other viewers see it disabled). Favourites are written to the collection `favorites` (doc id = find id, field `findId`, `at`). "Kun favoritter" shows only favourites.
- The rating buttons (Godt fund, Ikke interessant, Købt, Skraldespand) are removed. They are to be re-introduced later if needed. The existing `feedback` records stay in the database and are not deleted.
- At the bottom, "Søgedækning og begrænsninger": one block per run, newest first.

## Data and settings

- The page reads the collections `finds`, `targets`, `categories`, `runs` and `favorites`. The fields are in `templates/FIND_SCHEMA.md`.
- It is published with the `db` capability (read: anyone who can view, write: owner only) and the `user` capability.
- Style: calm green-grey palette, light and dark mode, fonts Bricolage Grotesque, IBM Plex Sans and IBM Plex Mono, readable on a phone.

## Changing the page

Edit `page/rethink-soegerapport.html`, then republish it to the same URL. Do not republish to add finds: finds go in the database.
