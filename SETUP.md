# Opsætning på en ny computer

Lamperne står i en liste, som er et artefakt: https://claude.ai/artifact/7SKsryS5G4DTBDGXmLm3ZF. Fundene gemmes i `database.db` i denne mappe. Der er ingen Excel-fil.

## Mappen

- `CLAUDE.md`: hvad hovedagenten gør i en kørsel. Start her.
- `agents/`: briefs til underagenterne, reglerne for et kvalificeret fund, og `platforms.md` med én sektion pr. platform.
- `templates/FIND_SCHEMA.md`: tabellerne i `database.db`.
- `database.db`: fund, lamper, annoncer og kørsler.
- `page/`: sidens kildekode og `PAGE.md`. Siden opdateres ikke af agenterne.

## Trin

1. Kopiér hele mappen til den nye computer, inklusive `database.db`.
2. Installér Claude-desktop-appen og log ind. Forbind mappen til en opgave. Installér udvidelsen Claude in Chrome, og log ind på markedspladserne i den Chrome.
3. I claude.ai: lav et Project med navnet "Rethink søgeagent". Sæt denne instruktion ind:
   `At the start of every new run, before doing anything else, open and read the project file CLAUDE.md in full, and follow it exactly. If you cannot open it, stop and tell me; do not start any search.`
4. Kontoen skal kunne læse og redigere lampelisten. Er det en ny konto, skal artefaktet deles med den.
5. Test: skriv "Kør en søgning". Agenten læser listen og databasen, tjekker de gamle fund og søger på platformene.

## Senere

- Ny platform: tilføj en række i `platform`-tabellen og et afsnit i `agents/platforms.md`. Uden afsnit kører agenten med hovedbriefen alene, og det noteres i dækningen.
- Ny kategori: tilføj en række i `produkt_kategori`, og lav en liste, der har samme form som lampelisten.
