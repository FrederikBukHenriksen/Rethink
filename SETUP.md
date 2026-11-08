# Opsætning på en ny computer

Lamperne står i en liste, som er et artefakt: https://claude.ai/artifact/7SKsryS5G4DTBDGXmLm3ZF. Fundene ligger i sidens database: https://claude.ai/artifact/WRGmgJnVgvKhDegpB6q5x8. Der er ingen Excel-fil.

## Mappen

- `CLAUDE.md`: hvad hovedagenten gør i en kørsel. Start her.
- `agents/`: briefs til underagenterne, reglerne for et kvalificeret fund, og `platforms.md` med én sektion pr. platform.
- `templates/FIND_SCHEMA.md`: felterne i sidens database.
- `templates/RESULTATER.md`: hvor resultaterne placeres.
- `resultater/`: søgningerne og resultaterne som HTML, én fil pr. søgning og kørsel.
- `page/`: sidens kildekode og `PAGE.md`.

## Trin

1. Kopiér hele mappen til den nye computer.
2. Installér Claude-desktop-appen og log ind. Forbind mappen til en opgave. Installér udvidelsen Claude in Chrome, og log ind på markedspladserne i den Chrome.
3. I claude.ai: lav et Project med navnet "Rethink søgeagent". Sæt denne instruktion ind:
   `At the start of every new run, before doing anything else, open and read the project file CLAUDE.md in full, and follow it exactly. If you cannot open it, stop and tell me; do not start any search.`
4. Kontoen skal kunne læse og redigere lampelisten. Er det en ny konto, skal artefaktet deles med den.
5. Samme claude.ai-konto som før: siden og fundene findes allerede. Spring til trin 7.
6. Ny konto: bed Claude publicere `page/rethink-soegerapport.html` som et artefakt med navnet "Rethink søgerapport", med `db`-capability (læs: alle der kan se den, skriv: kun ejeren) og `user`-capability. Erstat derefter sidens URL i `CLAUDE.md` og `templates/FIND_SCHEMA.md`. Bed derefter Claude oprette dokumentet `categories/lamper` i sidens database: `{ "name": "Lamper", "order": 1 }`.
7. Test: skriv "Kør en søgning". Agenten læser listen og sidens database, tjekker de gamle fund og søger på platformene.

## Senere

- Ny platform: tilføj den som et afsnit i `agents/platforms.md`, og tilføj platformen til `plat` i `templates/FIND_SCHEMA.md`. Uden afsnit kører agenten med hovedbriefen alene, og det noteres i dækningen.
- Ny kategori: opret et `categories/<slug>`-dokument og en liste, der har samme form som lampelisten.
