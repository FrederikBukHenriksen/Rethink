import json, glob, os, datetime as dt
from collections import defaultdict

def parse(ts):
    if not ts: return None
    ts = ts.replace('Z', '+00:00')
    try:
        d = dt.datetime.fromisoformat(ts)
    except Exception:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone(dt.timedelta(hours=1)))
    return d

ORDER = ["DBA","Tradera","Vinted","Klein Anzeigen","Lauritz","Palsgaard","Woxholt","Bidstrup","Sikö","Catawiki","Gul og Gratis","Reshopper","Facebook Marketplace"]

# targets
targets = {}
for f in glob.glob('targets/targets/*.json'):
    d = json.load(open(f))
    doc = d.get('data', d)
    tid = os.path.basename(f)[:-5]
    targets[tid] = doc

# runs
runs = []
for f in glob.glob('runs/runs/*.json'):
    d = json.load(open(f))
    doc = d.get('data', d)
    runs.append((os.path.basename(f)[:-5], doc))

# platform keys present in targets
plat_true = defaultdict(list)   # platform -> [tid]
plat_all = set()
for tid, t in targets.items():
    if t.get('active') is False: continue
    for p, v in (t.get("platforms") or {}).items():
        p = "Catawiki" if p == "Catawicki" else p
        plat_all.add(p)
        if v is True:
            plat_true[p].append(tid)

def cutoff(tid, plat, cat):
    rownum = tid.split('-row-')[1]
    best = None
    for rid, doc in runs:
        c = doc.get('category')
        if c not in (cat, 'alle'): continue
        s = doc.get('searched') or {}
        rows = doc.get('rows')
        cands = []
        if f"{plat}|{rownum}" in s: cands.append(s[f"{plat}|{rownum}"])
        if plat in s and (rows is None or int(rownum) in [int(x) for x in rows if str(x).isdigit()]):
            cands.append(s[plat] if isinstance(s[plat], str) else None)
        for c2 in cands:
            d = parse(c2)
            if d and (best is None or d > best[0]):
                best = (d, rid, c2)
    return best

out = {"platformsInTargets": sorted(plat_all), "platforms": {}}
for p in ORDER:
    lst = []
    for tid in sorted(plat_true.get(p, []), key=lambda x: (x.split('-')[0], int(x.split('-row-')[1]))):
        cat = tid.split('-row-')[0]
        b = cutoff(tid, p, cat)
        lst.append({"target": tid, "cutoff": b[2] if b else "ingen", "cutoffRun": b[1] if b else None})
    out["platforms"][p] = lst
out["unknownPlatforms"] = sorted(p for p in plat_all if p not in ORDER)
json.dump(out, open('plan.json','w'), ensure_ascii=False, indent=1)
for p in ORDER:
    lst = out["platforms"][p]
    print(p, len(lst), "rows; no-cutoff:", sum(1 for x in lst if x["cutoff"]=="ingen"))
print("platform keys in targets:", out["platformsInTargets"])
print("not in ORDER:", out["unknownPlatforms"])
