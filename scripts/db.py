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
  python3 scripts/db.py soegeplan               hvad der skal søges nu, med cutoff pr. platform (JSON)
  python3 scripts/db.py eksport-lamper FIL      skriv lamper fra databasen som lampelisten (JSON)
  python3 scripts/db.py eksport-side FIL        skriv kategorier, targets og fund fra databasen som siden (JSON)

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
AD_FIELDS = ("title", "type", "description", "note", "city", "direct", "price", "available", "color")


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def connect():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys = ON")
    return db


def migrate_user_actions(db):
    """Handlinger på brugerne: 'favorit' og 'skjult' (på et fund eller en lampe).
    user_action_type viser, hvilke handlinger der findes. Skjul og arkivér er samme handling: 'skjult'."""
    cols_t = [r[1] for r in db.execute("PRAGMA table_info(user_action_type)")]
    cols_a = [r[1] for r in db.execute("PRAGMA table_info(user_actions)")]
    if "beskrivelse" in cols_t and "niveau" not in cols_t and "target_id" in cols_a:
        return  # allerede på den nye form
    db.execute("""CREATE TABLE user_action_type_ny (
        name TEXT PRIMARY KEY,
        beskrivelse TEXT NOT NULL)""")
    db.executemany("INSERT INTO user_action_type_ny (name, beskrivelse) VALUES (?, ?)",
                   [("favorit", "Godt fund, på et fund"),
                    ("skjult", "Skjult: ikke interessant, på et fund, eller arkiveret, på en lampe")])
    db.execute("""CREATE TABLE user_actions_ny (
        id INTEGER PRIMARY KEY,
        find_id TEXT REFERENCES finds(id) ON DELETE CASCADE,
        target_id TEXT REFERENCES targets(id) ON DELETE CASCADE,
        action TEXT NOT NULL REFERENCES user_action_type_ny(name),
        at DATETIME NOT NULL CHECK (datetime(at) IS NOT NULL),
        CHECK ((find_id IS NULL) <> (target_id IS NULL)))""")
    if "target_id" in cols_a:
        db.execute("""INSERT INTO user_actions_ny (id, find_id, target_id, action, at)
                      SELECT id, find_id, target_id, CASE action WHEN 'arkiveret' THEN 'skjult' ELSE action END, at
                      FROM user_actions""")
    else:
        db.execute("INSERT INTO user_actions_ny (find_id, action, at) SELECT find_id, action, at FROM user_actions")
    db.execute("DROP TABLE user_actions")
    db.execute("DROP TABLE IF EXISTS user_action_type")
    db.execute("ALTER TABLE user_action_type_ny RENAME TO user_action_type")
    db.execute("ALTER TABLE user_actions_ny RENAME TO user_actions")
    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_user_actions_find ON user_actions(find_id, action) WHERE find_id IS NOT NULL")
    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_user_actions_target ON user_actions(target_id, action) WHERE target_id IS NOT NULL")


REV_SCHEMA = """
CREATE TABLE IF NOT EXISTS targets_rev (
  rev_id INTEGER PRIMARY KEY,
  target_id TEXT NOT NULL REFERENCES targets(id) ON DELETE CASCADE,  -- targetet, som det var FØR ændringen
  rev_at TEXT NOT NULL,                 -- hvornår ændringen blev synket ind
  tilstand TEXT NOT NULL                -- JSON: felterne og underrækkerne før ændringen
);
CREATE INDEX IF NOT EXISTS idx_targets_rev ON targets_rev(target_id, rev_at);
CREATE TABLE IF NOT EXISTS ads_rev (
  rev_id INTEGER PRIMARY KEY,
  find_id TEXT NOT NULL REFERENCES finds(id) ON DELETE CASCADE,      -- fundet
  rev_at TEXT NOT NULL,                 -- hvornår hændelsen skete (ændring eller tjek)
  "insert" TEXT,                        -- hvornår den version, rækken viser, blev indsat
  kind TEXT NOT NULL DEFAULT 'tjek' CHECK (kind IN ('ændring', 'tjek')),
  title TEXT, type TEXT, description TEXT, note TEXT, city TEXT, direct TEXT,
  price INTEGER, available TEXT, color TEXT
);
CREATE INDEX IF NOT EXISTS idx_ads_rev ON ads_rev(find_id, rev_at);
"""


ADS_FIELDS = ("title", "type", "description", "note", "city", "direct", "price", "available", "color")


def migrate_ads(db):
    """ads holder den aktuelle tilstand pr. fund. Alle tidligere versioner flyttes til ads_rev,
    så historikken bevares."""
    cols = [r[1] for r in db.execute("PRAGMA table_info(ads)")]
    if "insert" not in cols:
        return
    cols_rev = " , ".join(ADS_FIELDS)
    db.execute(f"""INSERT INTO ads_rev (find_id, rev_at, "insert", kind, {", ".join(ADS_FIELDS)})
                   SELECT find_id, "insert", "insert", 'ændring', {cols_rev} FROM ads""")
    db.execute("""CREATE TABLE ads_ny (
        find_id TEXT PRIMARY KEY NOT NULL REFERENCES finds(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        type TEXT REFERENCES lamp_types(name),
        description TEXT,
        note TEXT,
        city TEXT,
        direct TEXT NOT NULL,
        price INTEGER NOT NULL,
        available TEXT NOT NULL DEFAULT 'ukendt',
        color TEXT REFERENCES color_type(name))""")
    db.execute(f"""INSERT INTO ads_ny (find_id, {cols_rev})
                   SELECT a.find_id, {", ".join("a." + f for f in ADS_FIELDS)} FROM ads a
                   WHERE a."insert" = (SELECT MAX(b."insert") FROM ads b WHERE b.find_id = a.find_id)""")
    db.execute("DROP TABLE ads")
    db.execute("ALTER TABLE ads_ny RENAME TO ads")


REV_DDL = {
    "targets_rev": ("target_id", "targets", """CREATE TABLE targets_rev_ny (
        rev_id INTEGER PRIMARY KEY,
        target_id TEXT NOT NULL REFERENCES targets(id) ON DELETE CASCADE,
        rev_at TEXT NOT NULL,
        tilstand TEXT NOT NULL)""",
        "INSERT INTO targets_rev_ny (rev_id, target_id, rev_at, tilstand) SELECT rev_id, target_id, rev_at, tilstand FROM targets_rev",
        "CREATE INDEX IF NOT EXISTS idx_targets_rev ON targets_rev(target_id, rev_at)"),
    "ads_rev": ("find_id", "finds", """CREATE TABLE ads_rev_ny (
        rev_id INTEGER PRIMARY KEY,
        find_id TEXT NOT NULL REFERENCES finds(id) ON DELETE CASCADE,
        rev_at TEXT NOT NULL,
        "insert" TEXT,
        kind TEXT NOT NULL DEFAULT 'tjek' CHECK (kind IN ('ændring', 'tjek')),
        title TEXT, type TEXT, description TEXT, note TEXT, city TEXT, direct TEXT,
        price INTEGER, available TEXT, color TEXT)""",
        """INSERT INTO ads_rev_ny (rev_id, find_id, rev_at, "insert", kind, title, type, description, note, city, direct, price, available, color)
           SELECT rev_id, find_id, rev_at, "insert", kind, title, type, description, note, city, direct, price, available, color FROM ads_rev""",
        "CREATE INDEX IF NOT EXISTS idx_ads_rev ON ads_rev(find_id, rev_at)"),
}


def migrate_rev_fk(db):
    """Historiktabellerne peger på deres hovedtabel med en fremmednøgle. Ældre databaser bygges om."""
    for tbl, (col, parent, ddl, copy_sql, index_sql) in REV_DDL.items():
        fks = db.execute(f"PRAGMA foreign_key_list({tbl})").fetchall()
        if any(fk[2] == parent and fk[3] == col for fk in fks):
            continue
        db.execute(ddl)
        db.execute(copy_sql)
        db.execute(f"DROP TABLE {tbl}")
        db.execute(f"ALTER TABLE {tbl}_ny RENAME TO {tbl}")
        db.execute(index_sql)


def init(db):
    db.executescript(REV_SCHEMA)
    for tbl in ("ads", "ads_rev"):
        cols = [r[1] for r in db.execute(f"PRAGMA table_info({tbl})")]
        if "seen_at" in cols:
            db.execute(f'ALTER TABLE {tbl} RENAME COLUMN seen_at TO "insert"')
    if "kind" not in [r[1] for r in db.execute("PRAGMA table_info(ads_rev)")]:
        db.execute("ALTER TABLE ads_rev ADD COLUMN kind TEXT NOT NULL DEFAULT 'tjek' CHECK (kind IN ('ændring', 'tjek'))")
        db.execute("UPDATE ads_rev SET kind = 'ændring'")
    migrate_ads(db)
    migrate_rev_fk(db)
    have = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    missing = [t for t in REQUIRED if t not in have]
    if missing:
        raise ValueError(f"databasen mangler tabeller: {', '.join(missing)}")
    db.execute("INSERT OR IGNORE INTO platforms (name) VALUES ('Facebook')")
    migrate_user_actions(db)


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


def target_state(db, tid):
    row = db.execute("""SELECT list_id, sort_order, model, designer, producer, max_price, aktiv, image_url
                        FROM targets WHERE id = ?""", (tid,)).fetchone()
    if row is None:
        return None
    return {
        "list_id": row[0], "sort_order": row[1], "model": row[2], "designer": row[3], "producer": row[4],
        "max_price": row[5], "aktiv": row[6], "image_url": row[7],
        "types": sorted(r[0] for r in db.execute("SELECT type FROM target_types WHERE target_id = ?", (tid,))),
        "colors": sorted([r[0], r[1]] for r in db.execute("SELECT color, kind FROM target_colors WHERE target_id = ?", (tid,))),
        "terms": sorted([r[0], r[1]] for r in db.execute("SELECT term, kind FROM target_terms WHERE target_id = ?", (tid,))),
        "platforms": sorted(r[0] for r in db.execute("SELECT platform FROM target_platforms WHERE target_id = ?", (tid,))),
    }


def sync_lampe(db, path):
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    ts = now()
    ids = []
    for d in docs:
        data = d.get("data") or {}
        if not any(data.get(k) for k in ("model", "designer", "producent")):
            print(f"springer tom række over: {d['id']}")
            continue
        tid = TARGET_PREFIX + d["id"]
        before = target_state(db, tid)
        arkiveret = data.get("archived") is True
        aktiv = 1 if data.get("aktiv") is True and not arkiveret else 0
        if arkiveret:
            db.execute("INSERT OR IGNORE INTO user_actions (target_id, action, at) VALUES (?, 'skjult', ?)",
                       (tid, now()))
        else:
            db.execute("DELETE FROM user_actions WHERE target_id = ? AND action = 'skjult'", (tid,))
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
        after = target_state(db, tid)
        if before is not None and before != after:
            db.execute("INSERT INTO targets_rev (target_id, rev_at, tilstand) VALUES (?, ?, ?)",
                       (tid, ts, json.dumps(before, ensure_ascii=False)))
    # Targets, der ikke længere står på listen, bliver inaktive. Ingen slettes.
    db.execute("UPDATE targets SET aktiv = 0 WHERE id LIKE ? AND id NOT IN (SELECT value FROM json_each(?))",
               (TARGET_PREFIX + "%", json.dumps(ids)))
    print(f"targets: {len(ids)} rækker synket fra listen")


def import_feedback(db, path):
    """Sidens feedback er hele tilstanden: ét dokument pr. fund med action 'favorit' eller 'skjult'.
    Et fund uden dokument har ingen handling. Læsningen skal være lykkedes, før den kaldes."""
    with open(path, encoding="utf-8") as f:
        docs = json.load(f)
    ts = now()
    want = {}
    for d in docs:
        data = d.get("data") or {}
        fid = data.get("findId") or d["id"]
        act = data.get("action")
        if act not in ("favorit", "skjult"):
            print(f"springer over, ukendt handling: {fid} ({act})")
            continue
        if not db.execute("SELECT 1 FROM finds WHERE id = ?", (fid,)).fetchone():
            print(f"springer over, fundet findes ikke: {fid}")
            continue
        want[fid] = (act, data.get("at") or ts)
    have = {(r[0], r[1]): r[2] for r in db.execute(
        "SELECT find_id, action, at FROM user_actions WHERE find_id IS NOT NULL")}
    removed = 0
    for (fid, act) in list(have):
        if want.get(fid, (None,))[0] != act:
            db.execute("DELETE FROM user_actions WHERE find_id = ? AND action = ?", (fid, act))
            removed += 1
    added = 0
    for fid, (act, at) in want.items():
        if (fid, act) in have:
            continue
        db.execute("DELETE FROM user_actions WHERE find_id = ? AND action <> ?", (fid, act))
        db.execute("INSERT INTO user_actions (find_id, action, at) VALUES (?, ?, ?)", (fid, act, at))
        added += 1
    print(f"user_actions: {added} sat, {removed} fjernet")


def latest_ad(db, fid):
    row = db.execute(f"SELECT {', '.join(AD_FIELDS)} FROM ads WHERE find_id = ?", (fid,)).fetchone()
    return dict(zip(AD_FIELDS, row)) if row else None


def log_check(db, fid, ts):
    """Hvert tjek af et fund logges, også når intet har ændret sig. Så kender vi sidst tjekket."""
    values = latest_ad(db, fid)
    if values is None:
        return
    since = db.execute("""SELECT "insert" FROM ads_rev WHERE find_id = ? AND kind = 'ændring'
                          ORDER BY rev_at DESC LIMIT 1""", (fid,)).fetchone()
    cols = ", ".join(AD_FIELDS)
    marks = ", ".join("?" for _ in AD_FIELDS)
    db.execute(f"""INSERT INTO ads_rev (find_id, rev_at, "insert", kind, {cols})
                   VALUES (?, ?, ?, 'tjek', {marks})""",
               (fid, ts, since[0] if since else ts, *[values.get(k) for k in AD_FIELDS]))


def write_ad(db, fid, values, ts):
    """Skriv den aktuelle tilstand. Ændres indholdet, gemmes den nye tilstand også i ads_rev."""
    latest = latest_ad(db, fid)
    if latest is not None and all(latest[k] == values.get(k) for k in AD_FIELDS):
        return False
    cols = ", ".join(AD_FIELDS)
    marks = ", ".join("?" for _ in AD_FIELDS)
    row = [values.get(k) for k in AD_FIELDS]
    if latest is None:
        db.execute(f"INSERT INTO ads (find_id, {cols}) VALUES (?, {marks})", (fid, *row))
    else:
        db.execute(f"UPDATE ads SET {', '.join(k + ' = ?' for k in AD_FIELDS)} WHERE find_id = ?", (*row, fid))
    db.execute(f"""INSERT INTO ads_rev (find_id, rev_at, "insert", kind, {cols})
                   VALUES (?, ?, ?, 'ændring', {marks})""", (fid, ts, ts, *row))
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
            log_check(db, fid, ts)
            nye += 1
        else:
            latest = latest_ad(db, fid) or {}
            values = dict(latest, **ad_values(db, f, partial=True))
            if write_ad(db, fid, values, ts):
                versioner += 1
            log_check(db, fid, ts)
    for r in data.get("fjernet", []):
        plat = lookup(db, "platforms", "name", r["platform"], "platform")
        fid = f"{plat.lower()}-{r['ekstern_id']}"
        latest = latest_ad(db, fid)
        if latest and latest["available"] != "nej":
            if write_ad(db, fid, dict(latest, available="nej"), ts):
                versioner += 1
        if latest:
            log_check(db, fid, ts)
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
    n_ads = db.execute("SELECT COUNT(*) FROM ads_rev WHERE find_id = ? AND kind = 'ændring'", (fid,)).fetchone()[0]
    n_act = db.execute("SELECT COUNT(*) FROM user_actions WHERE find_id = ?", (fid,)).fetchone()[0]
    db.execute("DELETE FROM ads_rev WHERE find_id = ?", (fid,))
    db.execute("DELETE FROM finds WHERE id = ?", (fid,))   # ads og user_actions slettes via ON DELETE CASCADE
    print(f"slettet {fid}: {n_ads} ændringer i historikken, {n_act} brugerhandlinger")


def _cutoff_for(db, tid, plat_name):
    row = db.execute("SELECT MAX(completed_at) FROM runs WHERE target_id = ? AND platform = ?",
                     (tid, plat_name)).fetchone()
    return row[0]


def soegeplan(db):
    """Hvad der skal søges nu: aktive lamper, deres platforme og cutoff pr. platform. Udskrives som JSON."""
    plan = []
    targets = db.execute("""SELECT id, list_id, sort_order, model, designer, producer, max_price, image_url
                            FROM targets WHERE aktiv = 1 ORDER BY sort_order""").fetchall()
    for tid, list_id, order, model, designer, producer, maks, billede in targets:
        types = [r[0] for r in db.execute("SELECT type FROM target_types WHERE target_id = ? ORDER BY type", (tid,))]
        colors = db.execute("SELECT color, kind FROM target_colors WHERE target_id = ?", (tid,)).fetchall()
        terms = db.execute("SELECT term, kind FROM target_terms WHERE target_id = ?", (tid,)).fetchall()
        plats = []
        for (plat_name,) in db.execute("SELECT platform FROM target_platforms WHERE target_id = ? ORDER BY platform", (tid,)):
            plats.append({"platform": plat_name, "cutoff": _cutoff_for(db, tid, plat_name) or "ingen"})
        soeg = []
        tilvalg = [t for t, k in terms if k == "tilvalg"]
        if model:
            soeg = [model] + tilvalg
        else:
            soeg = [" ".join(x for x in [(designer or producer), (types[0].lower() if types else "")] if x)] + tilvalg
        plan.append({
            "lampe_id": list_id, "sort_order": order, "model": model, "designer": designer, "producer": producer,
            "type": types, "soegninger": soeg,
            "tilladte_farver": [c for c, k in colors if k == "tilladt"],
            "fravalgte_farver": [c for c, k in colors if k == "fravalg"],
            "fravalgte_soegeord": [t for t, k in terms if k == "fravalg"],
            "maks_pris": maks, "billede": billede, "platforme": plats,
        })
    print(json.dumps(plan, ensure_ascii=False, indent=2))


def eksport_lamper(db, path):
    """Lamper fra databasen i samme form som listen. Bruges til at opdatere lampelisten fra databasen."""
    docs = []
    for tid, list_id, order, model, designer, producer, maks, aktiv, billede, arkiveret in db.execute(
            """SELECT id, list_id, sort_order, model, designer, producer, max_price, aktiv, image_url,
                      EXISTS (SELECT 1 FROM user_actions u WHERE u.target_id = targets.id AND u.action = 'skjult')
               FROM targets ORDER BY sort_order"""):
        types = [r[0].lower() for r in db.execute("SELECT type FROM target_types WHERE target_id = ? ORDER BY type", (tid,))]
        def cols(kind):
            return "; ".join(r[0].lower() for r in db.execute(
                "SELECT color FROM target_colors WHERE target_id = ? AND kind = ? ORDER BY color", (tid, kind)))
        def terms(kind):
            return "; ".join(r[0] for r in db.execute(
                "SELECT term FROM target_terms WHERE target_id = ? AND kind = ?", (tid, kind)))
        sites = [r[0] for r in db.execute("SELECT platform FROM target_platforms WHERE target_id = ? ORDER BY platform", (tid,))]
        docs.append({"id": list_id, "data": {
            "model": model or "", "type": "; ".join(types), "designer": designer or "",
            "producent": producer or "", "soegeord": terms("tilvalg"), "fravalgteSoegeord": terms("fravalg"),
            "tilladteFarver": cols("tilladt"), "fravalgteFarver": cols("fravalg"),
            "maksPris": maks, "billede": billede or "", "sites": sites,
            "aktiv": bool(aktiv), "archived": bool(arkiveret), "order": order}})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"lamper: {len(docs)} dokumenter skrevet til {path}")


def _parse_note(note, prefix):
    if not note:
        return None
    for part in note.split(" · "):
        if part.startswith(prefix):
            return part[len(prefix):].strip()
    return None


def eksport_side(db, path):
    """Fund, targets og kategorier fra databasen i formen siden læser. Siden får sine data herfra."""
    out = {"categories": [], "targets": [], "finds": []}
    out["categories"].append({"id": "lamper", "data": {"name": "Lamper", "order": 1,
                                                        "workbook": "Lampelisten", "sheet": "lamper"}})
    for tid, list_id, order, model, designer, producer in db.execute(
            "SELECT id, list_id, sort_order, model, designer, producer FROM targets ORDER BY sort_order"):
        out["targets"].append({"id": f"lamper-row-{order}", "data": {
            "category": "lamper", "row": order, "model": model or "",
            "designers": [designer] if designer else [], "producers": [producer] if producer else []}})
    for fid, plat, tid, link, order in db.execute(
            """SELECT f.id, f.plat, f.target_id, f.link, t.sort_order FROM finds f
               JOIN targets t ON t.id = f.target_id"""):
        versions = db.execute('SELECT "insert", title, type, description, note, city, direct, price, available, color '
                              "FROM ads_rev WHERE find_id = ? AND kind = 'ændring' ORDER BY \"insert\"", (fid,)).fetchall()
        if not versions:
            continue
        seen, title, typ, desc, note, city, direct, price, avail, color = versions[-1]
        first_seen = versions[0][0]
        history = []
        last_price = None
        for v in versions:
            if v[7] != last_price:
                history.append({"d": v[0][8:10] + "." + v[0][5:7], "p": v[7]})
                last_price = v[7]
        status = _parse_note(note, "Status: ") or "Uklar identitet"
        listed = _parse_note(note, "Annonceret: ")
        gone = next((v[0] for v in versions if v[8] == "nej"), None)
        doc = {"category": "lamper", "row": order, "name": title, "type": typ, "plat": plat,
               "colors": [color] if color else [], "city": city or "by ukendt", "direct": direct,
               "status": status, "link": link, "price": price, "priceHistory": history,
               "available": avail, "firstSeen": first_seen, "lastChecked": versions[-1][0]}
        if note:
            doc["note"] = note
        if listed:
            doc["listedAt"] = listed
        if "Ikke uafhængigt verificeret" in (note or ""):
            doc["check"] = "Ikke uafhængigt verificeret"
        if avail == "nej" and gone:
            doc["goneAt"] = gone
        last = db.execute("SELECT MAX(rev_at) FROM ads_rev WHERE find_id = ?", (fid,)).fetchone()[0]
        if last:
            doc["lastChecked"] = last
        out["finds"].append({"id": fid, "data": doc})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"side: {len(out['categories'])} kategori, {len(out['targets'])} targets, {len(out['finds'])} fund skrevet til {path}")


def status(db):
    for t in ("platforms", "lamp_types", "color_type", "targets", "target_types", "target_colors",
              "target_terms", "target_platforms", "runs", "finds", "ads", "ads_rev", "targets_rev",
              "user_action_type", "user_actions"):
        print(f"{t}: {db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")


def main(argv):
    commands = {"init": 2, "sync-lampe": 3, "import-feedback": 3, "gem-resultat": 3,
                "cutoff": 4, "slet-fund": 3, "status": 2, "soegeplan": 2,
                "eksport-lamper": 3, "eksport-side": 3}
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
            elif cmd == "soegeplan":
                soegeplan(db)
            elif cmd == "eksport-lamper":
                eksport_lamper(db, argv[2])
            elif cmd == "eksport-side":
                eksport_side(db, argv[2])
    except (ValueError, sqlite3.Error) as e:
        print(f"Fejl: {e}. Ingen ændringer er gemt.")
        return 1
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
