# Palsgaard

Platformsfil for platform-søgeagenten. Læses sammen med den generelle brief.

**Status: ikke verificeret.** Siden kunne ikke nås fra sessionen (se Faldgruber). Det nedenfor er foreløbige antagelser, ikke observationer. Ret filen, når siden er testet.

## Søgning

- Adresse: ikke fastlagt. Sandsynligvis www.palsgaardauktion.dk. Søgeadresse og parametre er ikke undersøgt.
- Sortering efter nyeste eller slutter-tid: ikke undersøgt.
- Kør de givne søgninger, men notér i dækningsnoten at platformen ikke er søgt, til siden er testet.

## Dato

Ikke undersøgt. Det er en auktion, så en slutdato er ikke en annoncedato. Den siger hvornår auktionen slutter, ikke hvornår lampen blev lagt op. Brug kun en oprettelsesdato, hvis den vises. Ellers skrives `Dato/aktualitet: ikke synlig`, og forbeholdet står i dækningsnoten.

## Direkte køb

Ikke undersøgt. Antag indtil videre at alt er auktion. Brug `Tjek` for alle kandidater, indtil en købsknap uden auktion er fundet. Brug `Nej` først når siden tydeligt viser kun auktion.

## Faldgruber

- Forbindelsen fejlede konsekvent. Proxyen svarede 502 ("host allowed, but gateway could not connect") for www.palsgaardauktion.dk ved flere forsøg over ca. et minut. Det er ikke en politikblokering, men siden blev ikke nået.
- Samme fejl sås for andre danske auktionssider i samme session, så det kan være midlertidigt.
- Ikke undersøgt: cookie-banner, login-vægge, bot-tjek, pagination, markering af solgt eller udgået, og om prisen er startpris, nuværende bud eller slutpris.
- Domænet palsgaardauktioner.dk (med -er) er en parkeret One.com-side og ikke Palsgaard. Brug den ikke.
