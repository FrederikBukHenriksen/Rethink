# Databasen: `database.db`

En SQLite-fil i mappen. Alle fund, lamper og kørsler skrives her. Skriv efter reglerne i `CLAUDE.md`, afsnit 6. Slet aldrig rækker.

## Tabeller

| Tabel | Hvad en række er | Vigtige felter |
|---|---|---|
| `produkt_kategori` | En søgeområde, fx lamper | `slug`, `navn`, `raekkefoelge` |
| `platform` | En markedsplads | `navn` (DBA, Vinted, Tradera), `base_url`, `note` |
| `produkt` | En lamp, som den står i en annonce | `kategori_id`, `navn`, `model`, `designer`, `producent`, `farver`, `status`, `note`, `soegeraekke` |
| `produkt_lampe` | Lampetypen for et produkt | `produkt_id`, `lampetype` |
| `annonce` | Én annonce på én platform | `produkt_id`, `platform_id`, `ekstern_id`, `link` |
| `annonce_content` | Én version af en annonce | `annonce_id`, `observeret`, `sidst_set`, `pris`, `by`, `kan_koebes_direkte`, `tilgaengelig`, `listet_tid`, `dato_type`, `dato_omtrentlig`, `tjek` |
| `koersel` | En kørsel | `tidspunkt`, `kategori_id`, `platforme`, `cutoff`, `daekning` |

Felterne i `annonce_content` (de vigtigste):

- `observeret`: første gang denne version blev set. `sidst_set`: sidste gang den blev set.
- `pris`: helt tal i kr. `pris_note`: fx "for begge".
- `by`: sted, eller `by ukendt`.
- `kan_koebes_direkte`: `Ja`, `Nej` eller `Tjek`.
- `tilgaengelig`: `ja`, `nej` eller `ukendt`.
- `listet_tid`: ISO-tid med offset, fx `2026-10-30T09:39:00+01:00`.
- `dato_type`: `redigeret` (DBA viser kun sidst redigeret) eller `uploadet`.
- `dato_omtrentlig`: 1, når datoen er udregnet fra en relativ alder.
- `tjek`: det brugeren selv skal verificere. Tomt, når der ikke er noget.

## Status og værdier

- `produkt.status`: `Bekræftet`, `Sandsynlig med forbehold` eller `Uklar identitet`.
- `produkt_lampe.lampetype`: `Bordlampe`, `Loftlampe`, `Standerlampe` eller `Væglampe`.
- `farver`: danske farvenavne, hovedfarven først, adskilt med komma: Hvid, Sort, Grå, Beige, Brun, Rød, Orange, Gul, Grøn, Blå, Lilla, Pink, Guld, Sølv, Messing, Krom, Træ.

## Læs det nyeste

`annonce_nu` er en visning med én række pr. annonce. Den viser den seneste version og den første observation. Brug den til at læse fund. Brug `annonce_content` til historik.

## Eksempel

De to PH5-fund fra kørslen `2026-11-08 11.28` ligger i databasen. Den fravalgte PH5 Loftlampe står ikke i databasen, men i `koersel.daekning`.
