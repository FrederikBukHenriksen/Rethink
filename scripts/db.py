#!/usr/bin/env python3
"""database.db: skriver til den datamodel, der står i templates/FIND_SCHEMA.md.

Kommandoer:
  python3 scripts/db.py init                    tjek at tabellerne findes
  python3 scripts/db.py sync-lampe FIL          læs lampelisten (JSON fra ArtifactData) ind i targets
  python3 scripts/db.py import-feedback FIL     læs brugerens vurderinger fra siden (JSON) ind i user_actions
  python3 scripts/db.py gem-resultat FIL        gem fund, versioner og gennemførte søgninger (JSON)
  python3 scripts/db.py cutoff LAMPE PLATFORM   cutoff for en lampe på en platform; 'ingen' hvis ingen
  python3 scripts/db.py slet-fund FUND_ID       slet ét fund; annonceversioner og brugerhandlinger slettes med
  python3 scripts/db.py status                  antal rækker pr. tabel

FIL er en JSON-liste med objekter som {"id": "...", "data": {...}}, som ArtifactData returnerer dem.
Alle kommandoer kører i én transaktion. Fejler noget, skrives intet.
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

REQUIRED = ("platforms", "lamp_types", "color_type", "targets", "target_types", "target_colors",
            "target_terms", "target_platforms", "runs", "finds", "ads", "user_actions")
TARGET_PREFIX = "lamper-"          # listens id 'l07' bliver target 'lamper-l07'
FEEDBACK_MAP = {"godt": "favorit", "nej": "skjult"}   # 'koebt' findes ikke i modellen og springes over
AD_FIELDS = ("title", "type", "description", "note", "city", "direct", "price", "available", "color")


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def connect():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init(db):
    have = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    missing = [t for t in REQUIRED if t not in have]
    if missing:
        raise ValueError(f"databasen mangler tabeller: {', '.join(missing)}")
    db.execute("INSERT OR IGNORE INTO platforms (name) VALUES ('Facebook')")


def split(value):
    """Tekst med '; ' eller en liste. Tomt giver en tom liste."""
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [x.strip() for x in str(value or "").split(";") if x.strip()]


def lookup(db, table, col, value, label):
    """Find den kanoniske skrivemåde (uden hensyn til store/små bogstaver). Ukendt = fejl."""
    row = db.execute(f"SELECT {col} FROM {table} WHERE lower({col}) = lower(?)", (value,)).fetchone()
    if row is None:
        raise ValueError(f"ukendt {label}: {value}")
    return row[0]


def sync_lampe(db, path):
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    ids = []
    for d in docs:
        data = d.get("data") or {}
        if not any(data.get(k) for k in ("model", "designer", "producent")):
            print(f"springer tom række over: {d['id']}")
            continue
        tid = TARGET_PREFIX + d["id"]
        aktiv = 1 if data.get("aktiv") is True and data.get("archived") is not True else 0
        maks = data.get("maksPris")
        maks = int(maks) if isinstance(maks, (int, float)) and not isinstance(maks, bool) else None
        db.execute("""
            INSERT INTO targets (id, list_id, sort_order, model, designer, producer, max_price, aktiv, image_url)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET list_id = excluded.list_id, sort_order = excluded.sort_order,
              model = excluded.model, designer = excluded.designer, producer = excluded.producer,
              max_price = excluded.max_price, aktiv = excluded.aktiv, image_url = excluded.image_url""",
                   (tid, d["id"], data.get("order") or 0, data.get("model") or None,
                    data.get("designer") or None, data.get("producent") or None, maks, aktiv,
                    data.get("billede") or None))
        ids.append(tid)
        # Underrækkerne erstattes helt med listens værdier.
        for t in ("target_types", "target_colors", "target_terms", "target_platforms"):
            db.execute(f"DELETE FROM {t} WHERE target_id = ?", (tid,))
        for typ in split(data.get("type")):
            db.execute("INSERT INTO target_types (target_id, type) VALUES (?, ?)",
                       (tid, lookup(db, "lamp_types", "name", typ, "lampetype")))
        for kind, key in (("tilladt", "tilladteFarver"), ("fravalg", "fravalgteFarver")):
            for c in split(data.get(key)):
                db.execute("INSERT INTO target_colors (target_id, color, kind) VALUES (?,?,?)",
                           (tid, lookup(db, "color_type", "name", c, "farve"), kind))
        for kind, key in (("tilvalg", "soegeord"), ("fravalg", "fravalgteSoegeord")):
            for term in split(data.get(key)):
                db.execute("INSERT OR IGNORE INTO target_terms (target_id, term, kind) VALUES (?,?,?)",
                           (tid, term, kind))
        for p in split(data.get("sites")):
            db.execute("INSERT INTO target_platforms (target_id, platform) VALUES (?, ?)",
                       (tid, lookup(db, "platforms", "name", p, "platform")))
    # Targets, der ikke længere står på listen, bliver inaktive. Ingen slettes.
    db.execute("UPDATE targets SET aktiv = 0 WHERE id LIKE ? AND id NOT IN (SELECT value FROM json_each(?))",
               (TARGET_PREFIX + "%", json.dumps(ids)))
    print(f"targets: {len(ids)} rækker synket fra listen")


def import_feedback(db, path):
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    ts = now()
    n_sat = n_ikke = 0
    for d in docs:
        data = d.get("data") or {}
        fid = data.get("findId") or d["id"]
        action = FEEDBACK_MAP.get(data.get("verdict"))
        if not db.execute("SELECT 1 FROM finds WHERE id = ?", (fid,)).fetchone():
            print(f"springer over, fundet findes ikke: {fid}")
            continue
        if action is None:
            print(f"springer over, ingen tilsvarende handling: {fid} ({data.get('verdict')})")
            n_ikke += 1
            continue
        other = "skjult" if action == "favorit" else "favorit"
        db.execute("DELETE FROM user_actions WHERE find_id = ? AND action = ?", (fid, other))
        db.execute("""INSERT INTO user_actions (find_id, action, at) VALUES (?,?,?)
                      ON CONFLICT(find_id, action) DO UPDATE SET at = excluded.at""",
                   (fid, action, data.get("at") or ts))
        n_sat += 1
    print(f"user_actions: {n_sat} sat, {n_ikke} ikke mappet")


def latest_ad(db, fid):
    row = db.execute(f"""SELECT {", ".join(AD_FIELDS)} FROM ads WHERE find_id = ?
                         ORDER BY seen_at DESC LIMIT 1""", (fid,)).fetchone()
    return dict(zip(AD_FIELDS, row)) if row else None


def write_ad(db, fid, values, ts):
    """Ny version kun, når indholdet ændrer sig."""
    latest = latest_ad(db, fid)
    if latest is not None and all(latest[k] == values.get(k) for k in AD_FIELDS):
        return False
    cols = ", ".join(AD_FIELDS)
    marks = ", ".join("?" for _ in AD_FIELDS)
    db.execute(f"INSERT INTO ads (find_id, seen_at, {cols}) VALUES (?, ?, {marks})",
               (fid, ts, *[values.get(k) for k in AD_FIELDS]))
    return True


def ad_values(db, f, partial):
    """Oversæt en fund-post fra søgeagenten til felterne i ads. Ved en ny annonce skal de nødvendige felter være der."""
    m = {}
    if "navn" in f or "titel" in f:
        m["title"] = f.get("titel") or f.get("navn")
    if "lampetype" in f:
        m["type"] = f["lampetype"]
    if "beskrivelse" in f:
        m["description"] = f["beskrivelse"]
    if "note" in f:
        m["note"] = f["note"]
    if "by" in f:
        m["city"] = f["by"]
    if "kan_koebes_direkte" in f:
        m["direct"] = f["kan_koebes_direkte"]
    if "pris" in f:
        m["price"] = int(f["pris"])
    if "tilgaengelig" in f:
        m["available"] = f["tilgaengelig"]
    if "farver" in f:
        first = split(f["farver"])[:1]
        row = db.execute("SELECT name FROM color_type WHERE lower(name) = lower(?)", (first[0],)).fetchone() if first else None
        m["color"] = row[0] if row else None
    if not partial:
        for k in ("title", "type", "direct", "price", "available"):
            if m.get(k) in (None, ""):
                raise ValueError(f"nyt fund {f.get('platform')}-{f.get('ekstern_id')} mangler {k}")
        m.setdefault("description", None)
        m.setdefault("note", None)
        m.setdefault("city", None)
        m.setdefault("color", None)
        # Status og annoncedato har ingen egen kolonne i modellen. De står i note.
        extra = [f"Status: {f['status']}" if f.get("status") else None,
                 f"Farver: {f['farver']}" if f.get("farver") else None,
                 f"Annonceret: {f['listet_tid']}" if f.get("listet_tid") else None,
                 f.get("note")]
        m["note"] = " · ".join(x for x in extra if x) or None
    return m


def gem_resultat(db, path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    ts = now()
    lampe = data.get("lampe_id")
    tid = TARGET_PREFIX + lampe if lampe else None
    if tid and not db.execute("SELECT 1 FROM targets WHERE id = ?", (tid,)).fetchone():
        raise ValueError(f"ukendt lampe_id: {lampe}")
    nye = versioner = 0
    for f in data.get("fund", []):
        plat = lookup(db, "platforms", "name", f["platform"], "platform")
        fid = f"{plat.lower()}-{f['ekstern_id']}"
        exists = db.execute("SELECT 1 FROM finds WHERE id = ?", (fid,)).fetchone()
        if exists is None:
            if tid is None:
                raise ValueError(f"nyt fund {fid} kræver lampe_id")
            if not f.get("link"):
                raise ValueError(f"nyt fund {fid} mangler link")
            db.execute("INSERT INTO finds (id, plat, target_id, link) VALUES (?,?,?,?)",
                       (fid, plat, tid, f["link"]))
            write_ad(db, fid, ad_values(db, f, partial=False), ts)
            nye += 1
        else:
            latest = latest_ad(db, fid) or {}
            values = dict(latest, **ad_values(db, f, partial=True))
            if write_ad(db, fid, values, ts):
                versioner += 1
    for r in data.get("fjernet", []):
        plat = lookup(db, "platforms", "name", r["platform"], "platform")
        fid = f"{plat.lower()}-{r['ekstern_id']}"
        latest = latest_ad(db, fid)
        if latest and latest["available"] != "nej":
            if write_ad(db, fid, dict(latest, available="nej"), ts):
                versioner += 1
    runs = 0
    for s in data.get("soegninger", []):
        if s.get("status") != "gennemfoert":
            print(f"ikke gemt som kørt ({s.get('status')}): {s.get('platform')} {s.get('daekning', '')}")
            continue
        if tid is None or not s.get("platform"):
            print("springer søgning over: kræver lampe_id og platform")
            continue
        plat = lookup(db, "platforms", "name", s["platform"], "platform")
        db.execute("INSERT OR IGNORE INTO runs (target_id, platform, completed_at) VALUES (?,?,?)",
                   (tid, plat, s.get("tidspunkt", ts)))
        runs += 1
    print(f"gemt: {nye} nye fund, {versioner} nye versioner, {runs} gennemførte søgninger")


def cutoff(db, lampe, platform):
    """Cutoff er tidspunktet for den seneste gennemførte søgning på netop denne lampe og platform."""
    plat = lookup(db, "platforms", "name", platform, "platform")
    row = db.execute("SELECT MAX(completed_at) FROM runs WHERE target_id = ? AND platform = ?",
                     (TARGET_PREFIX + lampe, plat)).fetchone()
    print(row[0] or "ingen")


def slet_fund(db, fid):
    if not db.execute("SELECT 1 FROM finds WHERE id = ?", (fid,)).fetchone():
        raise ValueError(f"fandt ikke fund: {fid}")
    n_ads = db.execute("SELECT COUNT(*) FROM ads WHERE find_id = ?", (fid,)).fetchone()[0]
    n_act = db.execute("SELECT COUNT(*) FROM user_actions WHERE find_id = ?", (fid,)).fetchone()[0]
    db.execute("DELETE FROM finds WHERE id = ?", (fid,))   # ads og user_actions slettes via ON DELETE CASCADE
    print(f"slettet {fid}: {n_ads} annonceversioner, {n_act} brugerhandlinger")


def status(db):
    for t in ("platforms", "lamp_types", "color_type", "targets", "target_types", "target_colors",
              "target_terms", "target_platforms", "runs", "finds", "ads", "user_actions"):
        print(f"{t}: {db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")


def main(argv):
    commands = {"init": 2, "sync-lampe": 3, "import-feedback": 3, "gem-resultat": 3,
                "cutoff": 4, "slet-fund": 3, "status": 2}
    if len(argv) < 2 or argv[1] not in commands:
        print(__doc__)
        return 2
    cmd = argv[1]
    if len(argv) != commands[cmd]:
        print(f"Forkert brug af {cmd}. Se: python3 scripts/db.py")
        return 2
    db = connect()
    try:
        with db:
            init(db)
            if cmd == "sync-lampe":
                sync_lampe(db, argv[2])
            elif cmd == "import-feedback":
                import_feedback(db, argv[2])
            elif cmd == "gem-resultat":
                gem_resultat(db, argv[2])
            elif cmd == "cutoff":
                cutoff(db, argv[2], argv[3])
            elif cmd == "slet-fund":
                slet_fund(db, argv[2])
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
