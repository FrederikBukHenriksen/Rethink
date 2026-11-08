# Hvor resultaterne placeres

Hver kørsel skriver til to steder. Hvad der skrives til databasen, står i `CLAUDE.md`, afsnit 6, og felterne i `templates/FIND_SCHEMA.md`. Denne fil viser de HTML-filer, der ligger i `resultater/`.

| Fil | Indhold | Eksempel |
|---|---|---|
| `resultater/<YYYY-MM-DD-HHMM>-<platform>-soegning.html` | Det der blev søgt: adresse, søgeord, sortering, antal resultater, cutoff, trin, åbnede annoncer med udfald og begrænsninger | `resultater/ph5-dba-soegning.html` |
| `resultater/<YYYY-MM-DD-HHMM>-resultater.html` | Fund, prisændringer, fjernede annoncer, fravalgte annoncer med årsag og søgedækning | `resultater/ph5-dba-resultater.html` |

Skriv begge filer også ved en kørsel uden fund. Under "Fund" står der så `Ingen nye fund`, og dækningen udfyldes altid. En tom kørsel er ikke det samme som en, der ikke blev kørt.

## Skabelon for resultatfilen

Kopiér skabelonen, udfyld den, og gem den som HTML under navnet i tabellen. Teksten er den, brugeren læser.

```md
# Kørsel <YYYY-MM-DD HH.MM> · <kategori>

Platforme: <platform, platform>
Søgt i: `resultater/<fil>-soegning.html`
Lamper på listen: <antal aktive> af <antal rækker>. Sprunget over: <id-liste og grund>.

## Fund
- <Navn> · <pris> kr. · <by> · <platform> · <status> · Kan købes direkte: <Ja/Nej/Tjek> · <link>
  Note: <én linje om identifikation og det der mangler>
  Tjek: <kun hvis noget skal verificeres>

## Prisændringer
- <Navn>: <gammel pris> → <ny pris>

## Fjernet
- <Navn>: <grund eller "fjernet på siden">

## Fravalgt
- <Navn> · <platform> · <pris> · <link>: <årsag>

## Søgedækning og begrænsninger
Gennemført: <hvad der blev søgt og tjekket>
Ikke gennemført: <hvad der ikke blev gjort, og hvorfor>
Begrænsninger: <datoer, login, paginering, sortering, cookies>
Verifikation: <uafhængigt verificeret / ikke uafhængigt verificeret, og hvorfor>
```
