#!/usr/bin/env python3
"""Databasen database.db: skema og synkronisering.

Kommandoer:
  python3 scripts/db.py init                    opret tabeller, hvis de mangler
  python3 scripts/db.py sync-lampe FIL          læs lampelisten (JSON fra ArtifactData) ind i tabellen lampe
  python3 scripts/db.py import-feedback FIL     læs brugerens vurderinger fra siden (JSON) ind i user_actions
  python3 scripts/db.py gem-resultat FIL        gem resultatet af søgningen på én lampe (JSON, se templates/FIND_SCHEMA.md)
  python3 scripts/db.py slet-fund FUND_ID       slet ét fund med alt, der hører til det (fx dba-26284641)
  python3 scripts/db.py ny-koersel KATEGORI     start en kørsel; udskriver kørslens id
  python3 scripts/db.py cutoff LAMPE PLATFORM   cutoff for en lampe på en platform; 'ingen' hvis ingen
  python3 scripts/db.py status                  vis antal rækker

FIL er en JSON-liste med objekter som {"id": "...", "data": {...}}, som ArtifactData returnerer dem.
Alle skrivninger sker i én transaktion: fejler noget, skrives intet.
"""
import json
import os
import sqlite3
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "database.db")
TZ = ZoneInfo("Europe/Copenhagen")

SCHEMA = """
CREATE TABLE IF NOT EXISTS lampe (
  id TEXT PRIMARY KEY,                  -- id fra lampelisten, fx 'l01'
  listen_order INTEGER,                 -- 'order' på listen
  model TEXT, type TEXT, designer TEXT, producent TEXT,
  soegeord TEXT, fravalgte_soegeord TEXT,
  tilladte_farver TEXT, fravalgte_farver TEXT,
  maks_pris INTEGER,                    -- NULL = ingen grænse
  billede TEXT,
  sites TEXT,                           -- platforme, adskilt med '; '
  aktiv INTEGER NOT NULL DEFAULT 0 CHECK (aktiv IN (0,1)),
  archived INTEGER NOT NULL DEFAULT 0 CHECK (archived IN (0,1)),
  i_listen INTEGER NOT NULL DEFAULT 1 CHECK (i_listen IN (0,1)),  -- 0 = findes ikke længere på listen
  listen_opdateret TEXT,                -- 'updatedAt' fra listen
  synket TEXT NOT NULL                  -- hvornår rækken sidst blev læst fra listen
);

CREATE TABLE IF NOT EXISTS user_actions (
  id INTEGER PRIMARY KEY,
  feedback_id TEXT NOT NULL,            -- fundets id på siden, fx 'dba-26284641'
  annonce_id INTEGER REFERENCES annonce(id),   -- NULL, hvis annoncen ikke findes i databasen
  handling TEXT NOT NULL CHECK (handling IN ('godt','nej','koebt','fjernet')),
  aarsager TEXT,                        -- årsager, adskilt med '; '
  tidspunkt TEXT,                       -- hvornår brugeren gjorde det (ISO-tid)
  snapshot TEXT,                        -- JSON-kopi af fundet på vurderingstidspunktet
  importeret TEXT NOT NULL              -- hvornår det blev læst ind i databasen
);
CREATE INDEX IF NOT EXISTS idx_user_actions_feedback ON user_actions(feedback_id, id);

CREATE TABLE IF NOT EXISTS koersel (
  id INTEGER PRIMARY KEY,
  tidspunkt TEXT NOT NULL,              -- hvornår kørslen startede
  kategori_id INTEGER REFERENCES produkt_kategori(id)
);

-- Én række pr. lampe og platform i en kørsel. Cutoff gælder kun for den lampe og den platform.
CREATE TABLE IF NOT EXISTS soegning (
  id INTEGER PRIMARY KEY,
  koersel_id INTEGER REFERENCES koersel(id),
  lampe_id TEXT REFERENCES lampe(id),           -- NULL ved ad hoc-søgninger
  platform_id INTEGER REFERENCES platform(id),  -- NULL, hvis lampen blev sprunget over uden platform
  tidspunkt TEXT NOT NULL,                      -- hvornår denne søgning startede
  cutoff TEXT,                                  -- kun annoncer publiceret efter denne tid; NULL = ingen grænse
  status TEXT NOT NULL CHECK (status IN ('gennemfoert','fejlet','sprunget_over')),
  daekning TEXT                                 -- hvad der blev søgt, gennemgået og ikke gjort
);
CREATE INDEX IF NOT EXISTS idx_soegning_lampe_platform ON soegning(lampe_id, platform_id, status, tidspunkt);

CREATE TABLE IF NOT EXISTS slettede_fund (
  fund_id TEXT PRIMARY KEY,             -- fundets id, fx 'dba-26284641'
  slettet TEXT NOT NULL                 -- hvornår det blev slettet
);
"""


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def connect():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init(db):
    db.executescript(SCHEMA)
    cols = [r[1] for r in db.execute("PRAGMA table_info(produkt)")]
    if "lampe_id" not in cols:
        db.execute("ALTER TABLE produkt ADD COLUMN lampe_id TEXT REFERENCES lampe(id)")
    db.execute("INSERT OR IGNORE INTO platform (navn, base_url, note) VALUES "
               "('Facebook', 'https://www.facebook.com/marketplace', 'Ingen platformsfil endnu')")
    # Den gamle koersel-tabel havde cutoff, platforme og dækning på kørslen. Det ligger nu i soegning.
    kol = [r[1] for r in db.execute("PRAGMA table_info(koersel)")]
    if "daekning" in kol:
        db.execute("""INSERT INTO soegning (koersel_id, lampe_id, platform_id, tidspunkt, cutoff, status, daekning)
                      SELECT k.id, NULL, (SELECT id FROM platform WHERE navn = k.platforme), k.tidspunkt, NULL,
                             'gennemfoert', k.daekning
                      FROM koersel k WHERE k.daekning IS NOT NULL""")
    for col in ("cutoff", "platforme", "daekning"):
        if col in kol:
            db.execute(f"ALTER TABLE koersel DROP COLUMN {col}")


def link_produkt_to_lampe(db):
    """Kobl fundne lamper til listen via modelnavn, hvor der ikke allerede er en kobling."""
    db.execute("""
        UPDATE produkt SET lampe_id = (
            SELECT l.id FROM lampe l
            WHERE lower(l.model) = lower(produkt.model) AND l.i_listen = 1
            LIMIT 1)
        WHERE lampe_id IS NULL AND model IS NOT NULL AND model <> ''""")


def sync_lampe(db, path):
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    ts = now()
    ids = []
    for d in docs:
        data = d.get("data") or {}
        sites = data.get("sites") or []
        if isinstance(sites, str):
            sites = [s.strip() for s in sites.split(";") if s.strip()]
        maks = data.get("maksPris")
        values = (
            d["id"], data.get("order"), data.get("model") or "", data.get("type") or "",
            data.get("designer") or "", data.get("producent") or "",
            data.get("soegeord") or "", data.get("fravalgteSoegeord") or "",
            data.get("tilladteFarver") or "", data.get("fravalgteFarver") or "",
            maks if isinstance(maks, (int, float)) and not isinstance(maks, bool) else None,
            data.get("billede") or "", "; ".join(sites),
            1 if data.get("aktiv") is True else 0,
            1 if data.get("archived") is True else 0,
            1, data.get("updatedAt"), ts,
        )
        db.execute("""
            INSERT INTO lampe (id, listen_order, model, type, designer, producent, soegeord,
                               fravalgte_soegeord, tilladte_farver, fravalgte_farver, maks_pris,
                               billede, sites, aktiv, archived, i_listen, listen_opdateret, synket)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
              listen_order=excluded.listen_order, model=excluded.model, type=excluded.type,
              designer=excluded.designer, producent=excluded.producent, soegeord=excluded.soegeord,
              fravalgte_soegeord=excluded.fravalgte_soegeord, tilladte_farver=excluded.tilladte_farver,
              fravalgte_farver=excluded.fravalgte_farver, maks_pris=excluded.maks_pris,
              billede=excluded.billede, sites=excluded.sites, aktiv=excluded.aktiv,
              archived=excluded.archived, i_listen=1, listen_opdateret=excluded.listen_opdateret,
              synket=excluded.synket""", values)
        ids.append(d["id"])
    # Rækker, der ikke længere er på listen, slettes ikke. De markeres.
    db.execute("UPDATE lampe SET i_listen = 0 WHERE i_listen = 1 AND id NOT IN (SELECT value FROM json_each(?))",
               (json.dumps(ids),))
    link_produkt_to_lampe(db)
    print(f"lampe: {len(ids)} rækker synket fra listen")


def find_annonce(db, feedback_id):
    row = db.execute("""
        SELECT a.id FROM annonce a JOIN platform p ON p.id = a.platform_id
        WHERE lower(p.navn) || '-' || a.ekstern_id = ?""", (feedback_id,)).fetchone()
    return row[0] if row else None


def import_feedback(db, path):
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    ts = now()
    slettede = {r[0] for r in db.execute("SELECT fund_id FROM slettede_fund")}
    current = {d["id"]: d.get("data") or {} for d in docs if d["id"] not in slettede}
    last = {r[0]: (r[1], r[2], r[3]) for r in db.execute("""
        SELECT feedback_id, handling, aarsager, tidspunkt FROM user_actions u
        WHERE id = (SELECT MAX(id) FROM user_actions WHERE feedback_id = u.feedback_id)""")}
    new = 0
    for fid, data in current.items():
        verdict = data.get("verdict")
        if verdict not in ("godt", "nej", "koebt"):
            continue
        aarsager = "; ".join(data.get("reasons") or [])
        at = data.get("at")
        if last.get(fid) == (verdict, aarsager, at):
            continue
        snap = json.dumps(data.get("snapshot"), ensure_ascii=False) if data.get("snapshot") else None
        db.execute("""INSERT INTO user_actions (feedback_id, annonce_id, handling, aarsager, tidspunkt, snapshot, importeret)
                      VALUES (?,?,?,?,?,?,?)""", (fid, find_annonce(db, fid), verdict, aarsager, at, snap, ts))
        new += 1
    # En vurdering, der er fjernet på siden, skrives som 'fjernet'. Historikken bliver liggende.
    for fid, (handling, _, _) in last.items():
        if fid not in current and handling != "fjernet":
            db.execute("""INSERT INTO user_actions (feedback_id, annonce_id, handling, tidspunkt, importeret)
                          VALUES (?,?,?,?,?)""", (fid, find_annonce(db, fid), "fjernet", ts, ts))
            new += 1
    print(f"user_actions: {new} nye hændelser")


CONTENT_FIELDS = ("titel", "beskrivelse", "pris", "pris_note", "by", "kan_koebes_direkte", "tilgaengelig",
                  "listet_tid", "dato_type", "dato_omtrentlig", "tjek", "side_tekst")


def latest_content(db, annonce_id):
    cur = db.execute(f"""SELECT id, {", ".join(CONTENT_FIELDS)} FROM annonce_content
                         WHERE annonce_id = ? ORDER BY observeret DESC, id DESC LIMIT 1""", (annonce_id,))
    row = cur.fetchone()
    if row is None:
        return None, None
    return row[0], dict(zip(CONTENT_FIELDS, row[1:]))


def write_content(db, annonce_id, values, ts):
    """Ny version kun, når indholdet ændrer sig. Ellers opdateres sidst_set på den seneste version."""
    latest_id, latest = latest_content(db, annonce_id)
    if latest is not None and all(latest[k] == values.get(k) for k in CONTENT_FIELDS):
        db.execute("UPDATE annonce_content SET sidst_set = ? WHERE id = ?", (ts, latest_id))
        return False
    cols = ", ".join(CONTENT_FIELDS)
    marks = ", ".join("?" for _ in CONTENT_FIELDS)
    db.execute(f"""INSERT INTO annonce_content (annonce_id, observeret, sidst_set, {cols})
                   VALUES (?, ?, ?, {marks})""",
               (annonce_id, ts, ts, *[values.get(k) for k in CONTENT_FIELDS]))
    return True


def annonce_id_for(db, platform, ekstern_id):
    row = db.execute("""SELECT a.id FROM annonce a JOIN platform p ON p.id = a.platform_id
                        WHERE p.navn = ? AND a.ekstern_id = ?""", (platform, ekstern_id)).fetchone()
    return row[0] if row else None


def gem_resultat(db, path):
    """Gem resultatet af søgningen på én lampe. Fil: se templates/FIND_SCHEMA.md."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    ts = now()
    slug = data.get("kategori", "lamper")
    row = db.execute("SELECT id FROM produkt_kategori WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise ValueError(f"ukendt kategori: {slug}")
    kat = row[0]
    lampe_id = data.get("lampe_id")
    if lampe_id and not db.execute("SELECT 1 FROM lampe WHERE id = ?", (lampe_id,)).fetchone():
        raise ValueError(f"ukendt lampe_id: {lampe_id}")
    nye = versioner = sprunget = 0
    slettede = {r[0] for r in db.execute("SELECT fund_id FROM slettede_fund")}
    for f in data.get("fund", []):
        plat = db.execute("SELECT id FROM platform WHERE navn = ?", (f["platform"],)).fetchone()
        if plat is None:
            raise ValueError(f"ukendt platform: {f['platform']}")
        if f"{f['platform'].lower()}-{f['ekstern_id']}" in slettede:
            sprunget += 1
            continue
        aid = annonce_id_for(db, f["platform"], f["ekstern_id"])
        if aid is None:
            cur = db.execute("""INSERT INTO produkt (kategori_id, navn, model, designer, producent, farver,
                                                     status, note, lampe_id)
                                VALUES (?,?,?,?,?,?,?,?,?)""",
                             (kat, f["navn"], f.get("model"), f.get("designer"), f.get("producent"),
                              f.get("farver"), f["status"], f.get("note"), lampe_id))
            pid = cur.lastrowid
            db.execute("INSERT INTO produkt_lampe (produkt_id, lampetype) VALUES (?, ?)", (pid, f["lampetype"]))
            cur = db.execute("INSERT INTO annonce (produkt_id, platform_id, ekstern_id, link) VALUES (?,?,?,?)",
                             (pid, plat[0], f["ekstern_id"], f["link"]))
            write_content(db, cur.lastrowid, f, ts)
            nye += 1
        else:
            # Kendt annonce: felter, der ikke er med i filen, beholdes fra den seneste version.
            _, latest = latest_content(db, aid)
            values = dict(latest or {}, **{k: f[k] for k in CONTENT_FIELDS if k in f})
            if write_content(db, aid, values, ts):
                versioner += 1
    for r in data.get("fjernet", []):
        aid = annonce_id_for(db, r["platform"], r["ekstern_id"])
        if aid is None:
            continue
        _, latest = latest_content(db, aid)
        if latest is None or latest["tilgaengelig"] == "nej":
            continue
        values = dict(latest, tilgaengelig="nej")
        if write_content(db, aid, values, ts):
            versioner += 1
    soegninger = data.get("soegninger", [])
    if soegninger and data.get("koersel_id") is None:
        raise ValueError("koersel_id mangler")
    for s in soegninger:
        status = s["status"]
        if status not in ("gennemfoert", "fejlet", "sprunget_over"):
            raise ValueError(f"ukendt status: {status}")
        plat_id = None
        if s.get("platform"):
            row = db.execute("SELECT id FROM platform WHERE navn = ?", (s["platform"],)).fetchone()
            if row is None:
                raise ValueError(f"ukendt platform: {s['platform']}")
            plat_id = row[0]
        # Cutoff er starttidspunktet for den seneste gennemførte søgning på netop denne lampe og platform.
        cut = None
        if status == "gennemfoert" and lampe_id and plat_id:
            cut = last_search_start(db, lampe_id, plat_id)
        db.execute("""INSERT INTO soegning (koersel_id, lampe_id, platform_id, tidspunkt, cutoff, status, daekning)
                      VALUES (?,?,?,?,?,?,?)""",
                   (data["koersel_id"], lampe_id, plat_id, s.get("tidspunkt", ts), cut, status, s.get("daekning")))
    print(f"gemt: {nye} nye annoncer, {versioner} nye versioner, {sprunget} sprunget over (slettet før), "
          f"{len(soegninger)} søgninger")


def last_search_start(db, lampe_id, platform_id):
    row = db.execute("""SELECT MAX(tidspunkt) FROM soegning
                        WHERE lampe_id = ? AND platform_id = ? AND status = 'gennemfoert'""",
                     (lampe_id, platform_id)).fetchone()
    return row[0]


def cutoff(db, lampe_id, platform):
    """Den cutoff, der gælder for en lampe på en platform nu. 'ingen' = ingen grænse."""
    row = db.execute("SELECT id FROM platform WHERE navn = ?", (platform,)).fetchone()
    if row is None:
        raise ValueError(f"ukendt platform: {platform}")
    print(last_search_start(db, lampe_id, row[0]) or "ingen")


def ny_koersel(db, slug):
    row = db.execute("SELECT id FROM produkt_kategori WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise ValueError(f"ukendt kategori: {slug}")
    cur = db.execute("INSERT INTO koersel (tidspunkt, kategori_id) VALUES (?, ?)", (now(), row[0]))
    print(cur.lastrowid)


def slet_fund(db, fund_id):
    """Slet ét fund og alt, der hører til netop det: annoncen, dens versioner, brugerhandlinger
    og produktet, hvis intet andet bruger det. Lampelisten, platforme og kørsler røres ikke.
    Fund-id'et gemmes i slettede_fund, så det ikke bliver gemt igen ved næste søgning eller import."""
    row = db.execute("""SELECT a.id, a.produkt_id, p.navn FROM annonce a
                        JOIN platform p ON p.id = a.platform_id
                        WHERE lower(p.navn) || '-' || a.ekstern_id = ?""", (fund_id,)).fetchone()
    if row is None:
        raise ValueError(f"fandt ikke fund: {fund_id}")
    aid, pid, _ = row
    ts = now()
    n_versioner = db.execute("DELETE FROM annonce_content WHERE annonce_id = ?", (aid,)).rowcount
    n_handlinger = db.execute("DELETE FROM user_actions WHERE annonce_id = ? OR feedback_id = ?",
                              (aid, fund_id)).rowcount
    db.execute("DELETE FROM annonce WHERE id = ?", (aid,))
    n_produkt = 0
    if not db.execute("SELECT 1 FROM annonce WHERE produkt_id = ?", (pid,)).fetchone():
        db.execute("DELETE FROM produkt_lampe WHERE produkt_id = ?", (pid,))
        n_produkt = db.execute("DELETE FROM produkt WHERE id = ?", (pid,)).rowcount
    db.execute("INSERT OR REPLACE INTO slettede_fund (fund_id, slettet) VALUES (?, ?)", (fund_id, ts))
    print(f"slettet {fund_id}: 1 annonce, {n_versioner} versioner, {n_handlinger} brugerhandlinger, "
          f"{n_produkt} produkt")


def status(db):
    for t in ("produkt_kategori", "platform", "lampe", "produkt", "annonce", "annonce_content", "user_actions",
              "koersel", "soegning", "slettede_fund"):
        n = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")


def main(argv):
    commands = ("init", "sync-lampe", "import-feedback", "gem-resultat", "slet-fund", "ny-koersel", "cutoff", "status")
    if len(argv) < 2 or argv[1] not in commands:
        print(__doc__)
        return 2
    cmd = argv[1]
    usage = {
        "sync-lampe": "sync-lampe FIL", "import-feedback": "import-feedback FIL", "gem-resultat": "gem-resultat FIL",
        "slet-fund": "slet-fund FUND_ID", "ny-koersel": "ny-koersel KATEGORI", "cutoff": "cutoff LAMPE_ID PLATFORM",
    }
    expected = {"sync-lampe": 3, "import-feedback": 3, "gem-resultat": 3, "slet-fund": 3,
                "ny-koersel": 3, "cutoff": 4, "init": 2, "status": 2}
    if len(argv) != expected[cmd]:
        print(f"Brug: python3 scripts/db.py {usage.get(cmd, cmd)}")
        return 2
    db = connect()
    try:
        with db:  # én transaktion
            init(db)
            if cmd == "sync-lampe":
                sync_lampe(db, argv[2])
            elif cmd == "import-feedback":
                import_feedback(db, argv[2])
            elif cmd == "gem-resultat":
                gem_resultat(db, argv[2])
            elif cmd == "slet-fund":
                slet_fund(db, argv[2])
            elif cmd == "ny-koersel":
                ny_koersel(db, argv[2])
            elif cmd == "cutoff":
                cutoff(db, argv[2], argv[3])
            elif cmd == "status":
                status(db)
    except (ValueError, sqlite3.Error) as e:
        print(f"Fejl: {e}. Ingen ændringer er gemt.")
        return 1
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
