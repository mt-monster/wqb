"""Wave-1 selector: stratified sampling by skeleton style for KOR pattern_scores campaign."""
import json
import re
from collections import defaultdict

SRC = r"D:\coding\traeCN_project\wqb\tracking\KOR\candidates\kor_pattern_scores_valid_exprs.json"
OUT = r"D:\coding\traeCN_project\wqb\tracking\KOR\candidates\kor_wave1_exprs.json"

def first_fields(expr: str) -> str:
    # collect all field identifiers to favor field diversity
    return "|".join(sorted(set(re.findall(r"[a-z][a-z0-9_]+(?:_\d+)?", expr)) - {
        'add','subtract','multiply','divide','rank','ts_delta','ts_delay','min','max','abs'}))

exprs = json.load(open(SRC, encoding="utf-8"))
groups = defaultdict(list)
for e in exprs:
    # coarse style bucket by leading operator pattern
    if e.startswith("add(multiply(rank(ts_delta"):
        b = "C9_linear_mix_blend"
    elif e.startswith("divide(subtract"):
        b = "C6_conviction_zscore"
    elif e.startswith("subtract(rank"):
        b = "C2_C8_rank_diff"
    elif e.startswith("multiply(rank"):
        b = "C3_contrarian_reversal"
    elif e.startswith("subtract(ts_delta"):
        b = "C4_acceleration"
    elif e.startswith("ts_delta"):
        b = "C1_breakout_momentum"
    elif e.startswith("subtract"):
        b = "C5_C9_raw_spread"
    else:
        b = "other"
    groups[b].append(e)

PER_BUCKET = 8  # 8 per bucket -> ~8 buckets * 8 = up to 64; we cap at 48
wave = []
for b in sorted(groups):
    lst = groups[b]
    # favor field diversity: skip expressions reusing an already-seen exact field set
    seen_fields, picked = set(), []
    for e in lst:
        ff = first_fields(e)
        if ff in seen_fields:
            continue
        seen_fields.add(ff)
        picked.append(e)
        if len(picked) >= PER_BUCKET:
            break
    # backfill from remaining pool if field-unique supply ran short
    if len(picked) < PER_BUCKET:
        for e in lst:
            if e not in picked:
                picked.append(e)
                if len(picked) >= PER_BUCKET:
                    break
    wave.extend(picked)
    print(f"{b}: pool={len(lst)} picked={len(picked)}")

json.dump(wave, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"TOTAL WAVE1 = {len(wave)}")
