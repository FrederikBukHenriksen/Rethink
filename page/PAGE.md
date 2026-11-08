# Siden

Siden er den artefakt-side, hvor brugeren vurderer fund. Kildekoden er `page/rethink-soegerapport.html`. Al tekst på siden er dansk.

## Hvad den gør nu

- Viser fundene fra artefaktets egen database. De bliver ikke opdateret af agenterne. Fundene står nu i `database.db`.
- Brugeren kan vurdere et fund med Godt fund, Ikke interessant eller Købt, og vælge årsager. Vurderingerne skrives til samlingen `feedback`.
- Agenten læser `feedback` før hver søgning og importerer den til `database.db`, tabellen `user_actions`. Se `CLAUDE.md`, trin 2.

## Ændringer

Hvis siden skal vise fund fra `database.db`, skal den have en anden datakilde. Der er ingen måde at læse SQLite direkte fra artefaktet. Det kræver en eksport af databasen, som siden kan læse. Afklar det, før siden ændres.

Ret kun `page/rethink-soegerapport.html` for designændringer. Udgiv den igen til samme URL.
