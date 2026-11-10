import json, sys
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
ids = {f.get("id") for f in (d.get("results") or [])}
want = []
for m in ["ni","ebit","fcf","atot","aacr","srev","itli"]:
    for s in ["mae","mada","madp","predict"]:
        want.append("oth432_%s_trkdpitdeltapredict_funda_%s" % (m,s))
for w in want:
    print(("OK  " if w in ids else "MISS"), w)
