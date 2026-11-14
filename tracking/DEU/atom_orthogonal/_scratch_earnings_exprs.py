
import json, os, re, collections
ROOT = r"D:\coding\traeCN_project\wqb\tracking\DEU"
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
BT = chr(96)
for dirpath, _, fns in os.walk(ROOT):
    for fn in fns:
        low = fn.lower(); fp = os.path.join(dirpath, fn)
        try: sz = os.path.getsize(fp)
        except OSError: continue
        if sz > 8_000_000: continue
        if low.endswith(".json"):
            try: txt = open(fp, encoding="utf-8", errors="replace").read()
            except OSError: continue
            try: walk(json.loads(txt))
            except Exception:
                for m in re.findall(r'"([^"\\]{8,3800})"', txt):
                    if EXPR_HINT.search(m) and ')' in m: exprs.append(m)
        elif low.endswith(".md"):
            try:
                for line in open(fp, encoding="utf-8", errors="replace"):
                    s = line.strip().strip(BT)
                    if len(s) < 4000 and EXPR_HINT.search(s) and ')' in s and not s.startswith('#'):
                        exprs.append(s)
            except OSError: pass

def norm(e): return re.sub(r'\s+', '', e)
seen = set(); uniq = []
for e in exprs:
    k = norm(e)
    if k in seen: continue
    seen.add(k); uniq.append(k)

ERN = re.compile(r'ern6_|preliminary_eps_range')
ESM = re.compile(r'sentiment_probability_3|likelihood_of_neutral_tone|overall_sentiment_score|sentiment_weighting_method')

ern_only, esm_only, both = [], [], []
for e in uniq:
    h_ern = bool(ERN.search(e)); h_esm = bool(ESM.search(e))
    if h_ern and h_esm: both.append(e)
    elif h_ern: ern_only.append(e)
    elif h_esm: esm_only.append(e)

print(json.dumps({"uniq_exprs": len(uniq), "ern_only": len(ern_only), "esm_only": len(esm_only), "both": len(both)}, ensure_ascii=False))

print("\n########## earnings6 侧历史表达式（去重，全部）##########")
for e in sorted(ern_only): print("  ", e)

print("\n########## esm 侧历史表达式（去重，只列结构非重复的前40）##########")
for e in sorted(esm_only)[:40]: print("  ", e)
print("  ... esm 侧共", len(esm_only))

print("\n########## 同塔跨数据集 earnings6 × esm ##########")
for e in sorted(both): print("  ", e)
if not both: print("   （无 —— 从未组合过）")
