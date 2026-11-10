# Vinted

Platform file for the platform search agent. Read together with the general brief.

## Søgning

- Add the word `lampe` to broad searches to reduce irrelevant results such as clothing. Keep the model and designer terms.
- Sort by newest where the platform supports it.

## Dato

On the listing page, Vinted shows a relative age under "Uploadet", for example "Uploadet 2 dage siden". Use that as the evidence of recency and set the listing date to the approximate day. Say in `Forbehold` that the date is relative and approximate. If no age is shown, do not guess how old it is. Report the limitation.

## By

Vinted listings often show no city. To read the seller's city:

1. First look at the seller's profile page. Use the location shown there.
2. If it is not shown, open the message screen from the listing ("Send besked"). The city is shown there. Read it, type nothing, send nothing, and close the screen.

This is the only time you may open the message screen. Never write in it, never send anything, never make an offer, and never press a button that sends or reserves. If the screen asks for anything beyond showing the city, close it and report `ikke synlig`. If you are unsure whether you are about to send something, stop and report `ikke synlig`.

Report the city exactly as shown. Do not guess it from the seller's name, the photos or the listing text.

## Direkte køb

`Ja` where the normal Vinted checkout (payment and shipping) is available.
If the information is not visible or is ambiguous: `Tjek`.

## Adgang og Cloudflare

Vinted sits behind a Cloudflare check. Observed on 2026-11-10:

- The first page load can show the title "Just a moment..." with HTTP 403. This is the automatic browser check, not a CAPTCHA and not a ban.
- Wait for the check to finish before you read the page. Wait up to about 20 seconds after the page loads, then read the URL, title and results again. In a test on 2026-11-10 the check finished on its own after about 8 seconds, and the search page returned HTTP 200 with results.
- If the check is still showing after about 20 seconds, stop on Vinted. Write "ikke søgt" for Vinted in the coverage note, with the reason "Cloudflare-tjek blev ikke færdigt". Do not retry in a loop.
- Never solve a CAPTCHA, never change headers or fingerprints to get past the check, and never use proxies. Those are not allowed.
- Do not treat one 403 as proof that Vinted blocks this session. A later run may succeed, so state what was seen and when.

Search URL that worked on 2026-11-10: `https://www.vinted.dk/catalog?search_text=<søgeord>&order=newest_first`. Results are links of the form `/items/<id>-<slug>`.

## Faldgruber

- The Cloudflare check described above. A 403 on the first load is often not final.
- The search page shows many irrelevant results (for example tools and cosmetics for "ph 4/3"). Check title and photos for each candidate. Do not report a listing just because the search returned it.
- Relisted or renewed listings can look new. Check the listing date shown on the page itself.
- The listing page shows a "Køb nu" button and a "Giv et tilbud" button. Do not press either one. Only "Køb nu" as a sign of checkout belongs in `Direkte køb`, and only as the platform file describes.
