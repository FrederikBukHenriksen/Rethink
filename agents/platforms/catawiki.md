# Catawiki

Platformsfil til søgeagenten. Læses sammen med den generelle brief.

**Status: søgbar i brugerens egen Chrome** (verificeret 2026-11-14). Lotsider på `catawiki.com/da/l/<id>` kan åbnes og læses i brugerens Chrome. Akamai-blokken fra 2026-11-09 gælder ikke her. Den gjaldt curl og headless Chromium. Søgning køres kun i brugerens Chrome.

## Søgning

- Søg med Catawikis søgefelt i brugerens Chrome, eller brug søgeadressen fra søgefeltet. Søgeadressen er ikke fastlagt i denne fil, så notér den, du bruger, i dækningsnoten.
- Sortering efter nyeste eller slutter-tid er ikke bekræftet. Skriv det i dækningsnoten, hvis den ikke kan bekræftes.
- Åbn hvert lot, der matcher en række. Læs selve lotsiden, ikke kun søgekortet.
- Lotsiden læses bedst med `main`-teksten (innerText): "Detaljer" med ÆRA, DESIGNER, MATERIALE, MODEL, OPRINDELSESLAND, STAND og ANSLÅET PERIODE. Budhistorik og "Lukker om" står også der.
- Ved login-krav, bot-tjek eller tomme sider: stop, og skriv "ikke søgt" med årsagen. Skriv aldrig "ingen fund".

## Dato

Catawiki er en auktion. Den dato, der vises, er slut-/lukketid, ikke oprettelsesdato. Skriv den som `Dato/aktualitet: slutter <dato>`. Brug kun en "efter cutoff"-dato, hvis lotsiden viser en oprettelses- eller "lagt op"-dato. Ellers skriv slutdatoen som den er, med forbehold.

## Direkte køb

- Nogle lots har et "Køb nu for €X"-beløb, når sælgeren har sat det. Det er en købsmulighed, ikke et bud. Der købes ikke, og der bydes ikke.
- `Nej` på lots, hvor siden kun viser bud og "Lukker om". Brug `Tjek`, hvis der er et "Køb nu"-beløb. Brugeren afgør, om sådanne lots skal tælles som `Ja`. Det er ikke besluttet endnu.
- Udled ikke købsbeskyttelse af listingen eller sælgerprofilen. Catawiki-købsbeskyttelsen er et gebyr, der vises på lotsiden, og den er ikke en garanti.

## Priser og valuta

- Priser er i EUR. Brug `Nuværende bud` eller `Startbud` som pris, og skriv det i `priceNote`, fx "Nuværende bud €97. Køb nu €231".
- Omregn til DKK med EUR × 7,46 (projektets kurs) og skriv den oprindelige EUR-værdi i `priceNote`.
- "Vurdering" og "Estimat" er ikke priser.

## Faldgruber

- Tilskrivninger: "Efter 2000", "ANSLÅET PERIODE" og designerfeltet kan være ukendte eller strides mod Space Age. Brug `Uklar identitet`, hvis dateringen strider mod målet.
- Farvekonflikter: titel og overskrift kan være forskellige. Skriv begge og sæt forbehold.
- Privat sælger: "Denne genstand sælges af en privat sælger. EUs forbrugerrettigheder gælder ikke." Skriv det i noten.
- Akamai eller bot-tjek: omgå det ikke med andre headers, proxyer, login eller CAPTCHA. Skriv "ikke søgt" i dækningsnoten og stop.
- Cookie-banner og login-vægge: afvis cookies med det mest privatlivsvenlige valg. Log ikke ind.
