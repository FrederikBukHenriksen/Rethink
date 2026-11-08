# Hvor resultaterne placeres

Hver kørsel efterlader sine resultater fire steder. Denne fil viser, hvad der går hvor. Fundene og kørslen skrives til sidens database med `ArtifactData`, og felterne står i `templates/FIND_SCHEMA.md`. Søgningen og resultaterne gemmes som HTML i mappen, så de kan læses uden at åbne claude.ai.

## 1. Databasen (siden)

| Hvad | Samling | Id | Hvornår |
|---|---|---|---|
| Hvert nyt fund | `finds` | `<platform>-<annonce-id>` | Efter verifikation (`PROJECT_INSTRUCTIONS.md`, afsnit 5) |
| Prisændring, status, by | `finds` | eksisterende id | Kun den opdaterede del |
| Lampe fra listen | `targets` | `<kategori>-row-<order>` | Synkronisér med listen |
| Kørslens dækning | `runs` | `<YYYY-MM-DD-HHMM>` | Én pr. kørsel, også når intet blev fundet |

## 2. Søgningen: `soegning/<YYYY-MM-DD-HHMM>-<platform>.html`

Én fil pr. platform og kørsel. Den viser det, der blev søgt, så det kan efterprøves. Brug `soegning/ph5-dba.html` som eksempel.

Indhold:
- dato og tid, platform, søgeord og den præcise adresse
- sortering, filtre og antal resultater
- cutoff, og om det blev tjekket
- browser og eventuelle begrænsninger
- trin i den rækkefølge, de blev udført
- de annoncer, der blev åbnet, med udfald
- sektionen "Begrænsninger", herunder om søgningen er uafhængigt verificeret

## 3. Resultaterne: `resultater/<YYYY-MM-DD-HHMM>.html`

Én fil pr. kørsel. Den viser de fund, der kom med, og dækningen. Brug `resultater/ph5-dba.html` som eksempel.

Indhold:
- overskrift med kategori og kørslens tid
- fund: navn, pris, by, platform, status, "Kan købes direkte", link og note
- fravalgte annoncer med årsag, så det kan ses, hvorfor de ikke kom med
- sektionen "Søgedækning og begrænsninger"

## 4. Skabelon for en resultatfil

Kopiér skabelonen, og udfyld den. Gem den derefter som HTML i `resultater/`. Hold dig til teksten i skabelonen: det er den, brugeren læser.

```md
# Kørsel <YYYY-MM-DD HH.MM> · <kategori>

Platforme: <platform, platform>
Søgt i: `soegning/<fil>.html`
Lamper på listen: <antal aktive> af <antal rækker>. Sprunget over: <id-liste og grund>.

## Fund
Hvert fund: navn, pris, by, platform, status, Kan købes direkte, link og note.
- <Navn> · <pris> kr. · <by> · <platform> · <status> · Kan købes direkte: <Ja/Nej/Tjek> · <link>
  Note: <én linje, hvad der understøtter identifikationen, og hvad der mangler>
  Tjek: <kun hvis noget skal verificeres>

## Prisændringer
- <Navn>: <gammel pris> → <ny pris>

## Fjernet
- <Navn>: <grund eller "fjernet på siden">

## Fravalgt
- <Navn> · <platform> · <pris> · <link>: <årsag, fx "trænger til ny fatning">

## Søgedækning og begrænsninger
Gennemført: <hvad der blev søgt og tjekket>
Ikke gennemført: <hvad der ikke blev gjort, og hvorfor>
Begrænsninger: <datoer, login, paginering, sortering, cookies>
Verifikation: <uafhængigt verificeret / ikke uafhængigt verificeret, og hvorfor>
```

## 5. Når der ikke er fund

Skriv stadig en `runs`-post og en resultatfil. Under "Fund" står der så: `Ingen nye fund`. Dækningen udfyldes altid, også når intet blev fundet. En tom kørsel er ikke det samme som en, der ikke blev kørt.
