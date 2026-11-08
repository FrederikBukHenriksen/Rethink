# Siden

Siden er artefaktet, hvor brugeren ser fund. Kildekoden er `page/rethink-soegerapport.html`. Al tekst på siden er dansk.

## Hvor dataene kommer fra

- **Fund, targets og kategorier** kommer fra `database.db`. Agenten skriver dem til artefaktets samlinger efter hver kørsel, med `eksport-side`. Siden må ikke ændre dem.
- **Brugerens handlinger** skrives af siden til samlingen `feedback`, med `action` `favorit` eller `skjult`. Agenten læser dem ind i databasen før hver søgning, med `import-feedback`.

## Knapperne på hvert fund

- **Stjerne (favorit):** markerer fundet som favorit. Tryk igen for at fjerne den.
- **Skraldespand (skjult):** skjuler fundet. Skjulte fund vises ikke, før brugeren vælger "Vis skjulte". Tryk igen for at vise dem.

Tommelfinger op, tommelfinger ned, Købt og årsager er fjernet. Databasen gemmer ikke dem.

## Ændringer

Ret kun `page/rethink-soegerapport.html` for designændringer. Udgiv den igen til samme URL. Ændres dataformen i `eksport-side` eller handlingerne, skal siden også ændres.
