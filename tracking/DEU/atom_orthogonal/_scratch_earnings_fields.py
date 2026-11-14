
import csv, json, os, re, collections
BASE = r"D:\coding\traeCN_project\wqb\tracking\DEU\atom_orthogonal"
ROOT = r"D:\coding\traeCN_project\wqb\tracking\DEU"
BT = chr(96)

# --- 严格口径：真实表达式 tokens ---
EXPR_HINT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*\s*\(')
exprs = []
def walk(o, d=0):
    if d > 12: return
    if isinstance(o, dict):
        for v in o.values(): walk(v, d+1)
    elif isinstance(o, list):
        for v in o: walk(v, d+1)
    elif isinstance(o, str):
        if len(o) < 4000 and EXPR_HINT.search(o) and ')' in o: exprs.append(o)

# --- 宽松口径：全部文本 tokens ---
loose_text = []
for dirpath, _, fns in os.walk(ROOT):
    for fn in fns:
        low = fn.lower(); fp = os.path.join(dirpath, fn)
        try: sz = os.path.getsize(fp)
        except OSError: continue
        if sz > 8_000_000: continue
        if low.endswith(".json"):
            try: txt = open(fp, encoding="utf-8", errors="replace").read()
            except OSError: continue
            loose_text.append(txt)
            try: walk(json.loads(txt))
            except Exception:
                for m in re.findall(r'"([^"\\]{8,3800})"', txt):
                    if EXPR_HINT.search(m) and ')' in m: exprs.append(m)
        elif low.endswith(".md"):
            try: txt = open(fp, encoding="utf-8", errors="replace").read()
            except OSError: continue
            loose_text.append(txt)
            for line in txt.splitlines():
                s = line.strip().strip(BT)
                if len(s) < 4000 and EXPR_HINT.search(s) and ')' in s and not s.startswith('#'):
                    exprs.append(s)

strict = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", "\n".join(exprs)))
loose  = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", "\n".join(loose_text)))

def num(x, d=0.0):
    try: return float(x)
    except: return d

for ds in ["earnings6", "earnings_sent_matrix"]:
    fp = os.path.join(BASE, ds + "_fields.csv")
    rows = []
    with open(fp, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if r.get("id"): rows.append(r)
    print(f"\n================ {ds} : {len(rows)} fields ================")
    ns = nl = 0
    for r in rows:
        fid = r["id"]
        s = fid in strict; l = fid in loose
        ns += s; nl += l
        print("  %-38s %-7s cov=%.2f uc=%-3d ac=%-4d %s%s | %s" % (
            fid, r.get("type",""), num(r.get("cov")), num(r.get("uc")), num(r.get("ac")),
            "STRICT" if s else "      ", "  LOOSE" if (l and not s) else "       ",
            (r.get("desc") or "")[:78]))
    print(f"  --> 已测（严格）{ns}/{len(rows)} ; （宽松）{nl}/{len(rows)}")
