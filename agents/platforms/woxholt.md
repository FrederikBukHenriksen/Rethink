# Woxholt

Platformsfil for platformssøgeagenten. Læses sammen med den generelle brief.

**Status: ikke verificeret.** Woxholt kunne ikke nås den 2026-11-09. Både `www.woxholt.dk` og `woxholt.dk` gav `connect_unreachable` (502 ved CONNECT) via agent-proxyen, også i Playwright. Afsnittene nedenfor er derfor forsigtige standardregler, ikke observeret adfærd. Når siden kan nås, skal de verificeres og rettes, før filen bruges.

## Søgning

- Kør de givne søgninger, som de står. Søgeadresse og parametre er ikke verificeret, så brug søgefeltet på siden.
- Sortér efter nyeste, hvis siden tilbyder det. Hvis ikke, gennemgå resultaterne fra toppen og noter det i dækningsnoten.
- Ved login-krav, bot-tjek eller tomme sider: stop, og skriv "ikke søgt" med årsagen. Skriv aldrig "ingen fund".

## Dato

Ikke verificeret. Brug annoncens oprettelsesdato, hvis den vises. Hvis siden kun viser en slut- eller auktionsdato, skal den skrives som "slutter: <dato>" i `Dato/aktualitet`. Den må ikke bruges som udtryk for, hvor ny annoncen er. Hvis ingen dato vises, skriv "ikke synlig" og noter begrænsningen. Gæt aldrig alder.

## Direkte køb

Standard: `Tjek`. Woxholt er et auktionshus, og der er ikke verificeret nogen købsknap uden auktion.

- `Ja` kun ved en tydelig "køb nu" eller fastpris-knap på annoncen.
- `Nej` kun hvis siden tydeligt viser, at annoncen kun kan bydes på.
- Ellers `Tjek`. Vurder ikke købsbeskyttelse ud fra sælgerprofilen.

## Faldgruber

- **Utilgængelighed:** Siden kunne ikke nås den 2026-11-09. Tjek først, om den kan åbnes, og skriv i dækningsnoten, hvis den stadig ikke kan.
- **Pris:** Det er ikke verificeret, om prisen er startpris, nuværende bud eller slutpris. Angiv feltet, som det vises, eller skriv "Tjek".
- **Auktionsstatus:** Afsluttede, solgte og udgåede lots kan stå synlige. Tjek status, før en annonce tages med som kandidat.
- **Ukendt opbygning:** Cookie-bannere, login-vægge og paginering er ikke kendt. Stop ved login eller CAPTCHA, og omgå det ikke.
