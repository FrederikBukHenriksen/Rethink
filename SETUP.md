# Opsætning på en ny computer

Listerne (en fane pr. kategori: lamper, møbler) er ét artefakt: https://claude.ai/artifact/7SKsryS5G4DTBDGXmLm3ZF. Alt andet gemmes i `database.db` i denne mappe. Der er ingen Excel-fil.

## Mappen

- `CLAUDE.md`: hvad hovedagenten gør i en kørsel. Start her.
- `agents/`: briefs til underagenterne, reglerne for et kvalificeret fund, og `platforms.md` med én sektion pr. platform.
- `templates/FIND_SCHEMA.md`: tabellerne, kommandoerne og JSON-filerne til databasen.
- `scripts/db.py`: det eneste, der skriver til databasen.
- `database.db`: lamper, annoncer, brugerens vurderinger og kørsler.
- `page/`: sidens kildekode og `PAGE.md`. Siden viser ikke nye fund, men brugeren vurderer fund der.

## Trin

1. Kopiér hele mappen til den nye computer, inklusive `database.db`.
2. Installér Claude-desktop-appen og log ind. Forbind mappen til en opgave. Installér udvidelsen Claude in Chrome, og log ind på markedspladserne i den Chrome.
3. I claude.ai: lav et Project med navnet "Rethink søgeagent". Sæt denne instruktion ind:
   `At the start of every new run, before doing anything else, open and read the project file CLAUDE.md in full, and follow it exactly. If you cannot open it, stop and tell me; do not start any search.`
4. Kontoen skal kunne læse lampelisten og siden. Er det en ny konto, skal de deles med den.
5. Kontrollér databasen: `python3 scripts/db.py status`. Den skal vise rækker i tabellerne.
6. Test: skriv "Kør en søgning". Agenten synker listen, importerer vurderingerne, søger og gemmer resultatet.

## Senere

- Ny platform: tilføj et afsnit i `agents/platforms.md`. Uden afsnit kører agenten med hovedbriefen alene, og det noteres i dækningen.
- Ny kategori (fx keramik eller kunst):
  1. Tilføj en række i `KATEGORIER` i `scripts/db.py` (id, navn, orden, samling, titel og ark, tillægsord, reglerfil). Kør derefter `python3 scripts/db.py status`, så tabellen `produkt_kategori` opdateres.
  2. Tilføj kategoriens typer i `TYPER` i `scripts/db.py` (nøglen er kategoriens id). Kør `python3 scripts/db.py status` igen, så typerne skrives til `produkt_type`.
  3. Lav en reglerfil i `agents/` (fx `qualification-rules-keramik.md`), og et afsnit i `agents/platforms.md` for hver platform, der søges.
  4. Tilføj en fane i `CATS` i listens kode (artefaktet `7SKs…`), med samme id og samling som i `produkt_kategori`, og udgiv listen igen til samme URL.
  5. Skriv kategoriens række til siden (`categories`) med `eksport-side` og `batch`, som i trin 6 i `CLAUDE.md`.
- Møbler: reglerne i `agents/qualification-rules-moebler.md` er et udkast. Gennemgå dem og typerne, før møbler søges.
