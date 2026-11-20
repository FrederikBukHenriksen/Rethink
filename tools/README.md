# Søgeværktøjer (tokenbesparende)

dba_scan.js: indsættes i javascript_tool på en dba.dk-fane (Windows-Chrome). Henter alle resultatsider via same-origin fetch,
tolker kort (pris, titel, by, dato, sælger) og returnerer kun tal og kandidater efter cutoff/pris.
- dbaScan(q,{cutoff,maxPrice}) -> {total, read, pages, ended, older, unparsedDate, cand[]}
- Kør højst 2-3 søgninger pr. kald (45 s timeout) eller start i baggrunden (IIFE) og hent window.__res bagefter.
- DBA-grænse: ca. 50 sider x 53 kort = ca. 2650 kort. Over det: del søgningen.
- Filtrér kandidater på titel mod target (model/designer), derefter åbn kun matchene til verificering.
Resultat 2026-11-20: Lyfa 572/572 på 4 s; Louis Poulsen loftlampe 1756/1756 på 10 s. Samme arbejde kostede ca. 120.000 tokens pr. række før.
