# Set up the project on a new computer

This folder holds everything except the page's data (the finds), which lives in the page's database on claude.ai.

## Folder

- `PROJECT_INSTRUCTIONS.md`: what the main agent does in a run. Start here.
- `agents/`: the briefs for the subagents, and `agents/platforms/` with one file per marketplace.
- `templates/FIND_SCHEMA.md`: the database fields.
- `page/`: the page source (`rethink-soegerapport.html`) and a short description of it (`PAGE.md`).
- `DBA-lampesøgning.xlsx`: the search list. One sheet per category.

## Steps

1. Copy this whole folder to the new computer.
2. Install the Claude desktop app and sign in. Connect this folder to a task. Install the Claude in Chrome extension and sign in to the marketplaces in that Chrome.
3. In claude.ai, make a Project called "Rethink søgeagent". Put this as its instructions:
   `At the start of every new run, before doing anything else, open and read the project file PROJECT_INSTRUCTIONS.md in full, and follow it exactly. If you cannot open it, stop and tell me; do not start any search.`
4. Same claude.ai account as before: the page and its finds already exist. Skip to step 7.
5. New account: ask Claude to publish `page/rethink-soegerapport.html` as an artifact called "Rethink søgerapport", with the `db` capability (read: view, write: owner) and the `user` capability.
6. Replace the old page URL (`https://claude.ai/artifact/WRGmgJnVgvKhDegpB6q5x8`) with the new one in `PROJECT_INSTRUCTIONS.md` and `templates/FIND_SCHEMA.md`. Then ask Claude to create the document `categories/lamper` in the page database: `{ "name": "Lamper", "order": 1, "workbook": "DBA-lampesøgning.xlsx", "sheet": "Søgeliste" }`.
7. Test: write "Kør en søgning". The agent checks the workbook and the page database, checks the old finds, and searches the platforms.

## Adding things later

- New marketplace: add a column in the sheet and a file in `agents/platforms/`. Without a file it runs with the general brief only.
- New category: add a sheet in the workbook and a `categories/<slug>` document.
