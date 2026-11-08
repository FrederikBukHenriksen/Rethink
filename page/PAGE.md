# Siden

Siden er artefaktet, hvor brugeren ser fund og vurderer dem. Kildekoden er `page/rethink-soegerapport.html`. Al tekst på siden er dansk.

## Hvor dataene kommer fra

- **Fund, targets og kategorier** kommer fra `database.db`. Agenten skriver dem til artefaktets samlinger efter hver kørsel, med `eksport-side`. Siden må ikke ændre dem.
- **Brugerens vurderinger** (Godt fund, Ikke interessant, Købt og årsager) skrives af siden til samlingen `feedback`. Agenten læser dem ind i databasen før hver søgning, med `import-feedback`. Databasen gemmer kun Godt fund (`favorit`) og Ikke interessant (`skjult`). Købt og årsagerne gemmes ikke.

## Ændringer

Ret kun `page/rethink-soegerapport.html` for designændringer. Udgiv den igen til samme URL. Ændres dataformen i `eksport-side`, skal siden også ændres.
