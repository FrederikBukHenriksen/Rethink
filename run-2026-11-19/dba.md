# DBA

Platform file for the platform search agent. Read together with the general brief.

## Søgning

- Søg på dba.dk under brugt/recommerce (annoncer med adressen `/recommerce/forsale/item/<id>`). Brug hver søgning fra briefen.
- Sortér efter nyeste: tilføj `sort=PUBLISHED_DESC` til søgeadressen. Det blev brugt i de seneste kørsler.
- Gå alle resultatsider igennem, til en side er tom. Det samlede antal øverst på siden har vist sig ustabilt, så brug det ikke til at afgøre, om du er færdig.
- Første gang på en række: søg hele markedet. Ingen cutoff.
- Cookie-banneret: vælg "Kun nødvendige". Det påvirker ikke søgelisterne.
- Søg og åbn siderne i brugerens egen Chrome. Headless Chromium, Playwright og curl bruges ikke, fordi de har givet tomme sider på dba.dk. Læs annoncedata fra selve annoncen: titel, pris, by, stand, designer- og mærkefelt, "Sidst redigeret" og tilgængelighed.

## Scriptlæsning af søgeresultater (DBA, testet 2026-11-20)

Læs søgelisterne med scriptet `tools/dba_scan.js` i stedet for at læse siderne som tekst. Det sparer langt de fleste tokens og giver et eksakt antal læste kort.

- Hent en dba.dk-fane i brugerens Windows-Chrome, og indsæt scriptet med javascript_tool. Det henter alle resultatsider med same-origin `fetch` (`.../recommerce/forsale/search?q=<søgning>&sort=PUBLISHED_DESC&page=<n>`) og læser pris, titel, by, dato og sælger fra hvert kort.
- `dbaScan(q,{cutoff,maxPrice})` returnerer `total` (antal resultater, som siden viser), `read` (unikke annoncer læst), `pages`, `ended` (en side uden kort er nået), `older` (før cutoff), `unparsedDate` og de kandidater, der er nyere end cutoff og ikke over maksprisen.
- Kør højst 2-3 søgninger pr. kald (timeout 45 sekunder). Ellers start dem i baggrunden og hent resultatet bagefter.
- Skriv i dækningsnoten `læst <read> af <total>, <pages> sider, slut nået ja/nej`. En søgning er komplet, når `ended` er ja og `read` er lig `total`. Ved forskel skal den forklares.
- Filtrér kandidaterne på titel mod target (model, designer, producent), og åbn kun dem, der passer, for at læse by, beskrivelse og tilgængelighed (se Placering og åbning). Scriptet erstatter ikke læsning af selve annoncen.
- Filtret på titel finder ikke annoncer, hvor modelnavnet kun står i beskrivelsen. Skriv det som forbehold, når en søgning er afsluttet kun på titler.
- Kortets datoer viser ikke altid årstal: relative aldre ("3 t.", "2 dage") og "1. nov." tolkes af scriptet. En dato på selve cutoff-dagen regnes med, fordi klokkeslæt ikke vises.
- Brug aldrig scriptet til at kontakte sælgere, og det må ikke bruge andet end læsning.

## Dato

- Søgekortet viser en kort dato eller en relativ alder ("8 t.", "3 dage", "1. nov.", "2.6.25"). Nogle datoer mangler årstal.
- Annoncesiden viser kun "Sidst redigeret". DBA viser ikke oprettelsesdato.
- Skriv derfor altid datoen som "sidst redigeret" og sæt `dateKind: redigeret`. Gamle annoncer kan være genoptaget, og en ny dato betyder ikke, at annoncen er ny.
- Hvis kun en relativ alder vises, så skriv den som evidens, og sæt `dateApprox: true` i fundet.

## Placering og åbning af annoncen (skal altid gøres)

- Når et fund noteres, skal annoncen åbnes, og genstandens placering (by og postnummer) aflæses fra selve annoncen. Et søgekort eller en titel er ikke nok.
- Skriv byen i `city`. Hvis den ikke kan aflæses fra annoncen, skriv "by ukendt" og forklar hvorfor i `check`.
- Samme gælder, om annoncen allerede har "Fiks færdig"-muligheden: den skal læses fra selve annoncen, ikke fra søgekortet.

## Direkte køb

- `Ja` kun når Fiks færdig er tilbudt eksplicit, fx med Fiks færdig-badge og "Tryg handel" på annoncen. Det er købe-muligheden på DBA.
- Knappen "Bed om Fiks færdig" alene er ikke et tilbud, så den giver `Nej`.
- `Nej` når annoncen tydeligt ikke tilbyder køb (fx kun "Send besked" eller "Gå til varen").
- `Ukendt` når det ikke kan ses på annoncen eller er tvetydigt.
- "Send besked", "Gå til varen" og "Fragt tilbydes" giver `Nej`.
- Er det uklart, så `Tjek`.

## Faldgruber

- Søgningen "Panton Chair" stoppede tidligt: 80 af 118 kort blev vist. Ellers dækkede de andre søgninger de manglende annoncer, men det er ikke dokumenteret. Skriv det i dækningsnoten, når en søgning viser færre kort end antallet af resultater.
- Professionelle sælgere (fx Cph-Classic, Nordic Retro, Antik Pjot) genopretter gamle annoncer. Kortdatoen kan se ny ud. Skriv det som forbehold.
- Brede søgninger på et producentnavn (fx "Haslev") giver annoncer, der ikke er designet af den søgte person. Læs annoncen, før du giver `Bekræftet`.
- Ombetræksservice-annoncer ("ombetræk", "polstring") er ikke et møbel til salg. Afvis dem.
- Reserverede eller solgte annoncer er ikke set i de seneste kørsler. Tjek alligevel tilgængeligheden i annoncen.
- Annoncetekst kan være afkortet på søgekortet. Læs fuld beskrivelse, før du vurderer identitet.

## Dækningsgrænse

- DBA viser højst 50 sider pr. søgning med ca. 53 kort pr. side, altså ca. 2650 annoncer. Søgninger med op til ca. 2600 resultater kan læses til ende (testet: "Louis Poulsen loftlampe" 1756/1756, "Pan" 2644/2644). Søgninger med flere resultater er ufuldstændige og skal opdeles (model, type, farve, pris, dato). "Kina" gav kun 2650 af 3972.
- Den tidligere angivelse "ca. 1.000 resultater" og "ca. 54 af 1755" var en fejltolkning, fordi siderne blev læst som tekst og kun første side blev læst.
