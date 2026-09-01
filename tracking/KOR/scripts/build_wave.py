# -*- coding: utf-8 -*-
"""build_wave.py - 统一选波器（M6/M8），接管所有 wave（select_wave1.py 仅用于 wave1 的退化修正）。

能力:
  - 全历史去重（M6）：对 tracking/KOR 下全部 kor_wave*_exprs.json / candidates/*.json
    建表达式哈希集，重复候选直接丢弃（战役实测 92/854 重复 = 11% 配额浪费）
  - 算子树分桶（M8）：解析表达式根调用 + 第一个函数参数作桶键（如 add>multiply、
    rank>ts_av_diff），取代 select_wave1.py 的 startswith 前缀碰撞分桶
  - 骨架配给制：按 reference/kor_generation_constraints.json 的 skeleton_quota 限制
    linear_mix 占比（默认 ≤50%），强制事件门控/group/ratio 骨架进入候选（直击 CW 墙根因）
  - near-miss 加权：读 reviews/*.json 的 near 池字段，含近门槛字段的候选优先
  - 波内字段去重：同一字段在单波出现次数上限

用法:
  python build_wave.py --file candidates/new_exprs.json --wave 36A [--size 48] [--per-bucket 8]
输出:
  candidates/kor_wave<wave>_exprs.json
"""
import argparse, collections, datetime, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def norm(e):
    return re.sub(r"\s+", "", e)


def history_hashes(exclude_path=None):
    seen = set()
    excl = os.path.normcase(os.path.abspath(exclude_path)) if exclude_path else None
    for f in glob.glob(os.path.join(ROOT, "kor_wave*_exprs.json")) + \
             glob.glob(os.path.join(ROOT, "candidates", "*.json")):
        if excl and os.path.normcase(os.path.abspath(f)) == excl:
            continue  # 输入文件自身不算历史
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        ex = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
        for e in ex:
            if isinstance(e, str):
                seen.add(norm(e))
    return seen


def bucket_key(expr):
    """根调用 + 第一个函数参数，如 rank(ts_av_diff(F,10)) -> 'rank>ts_av_diff'。"""
    m = re.match(r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr)
    if not m:
        return "atom"
    root = m.group(1)
    m2 = re.search(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr[m.end():])
    return f"{root}>{m2.group(1)}" if m2 else f"{root}>atom"


def skeleton(expr):
    if "trade_when(" in expr or "if_else(" in expr:
        return "event_gated"
    if "group_" in expr:
        return "group"
    if "divide(" in expr:
        return "ratio"
    if "add(" in expr or "multiply(" in expr:
        return "linear_mix"
    return "single"


def near_fields():
    """reviews/*.json near 池 + 台账 near_pool 的字段集合（增强优先）。"""
    flds = set()
    for f in glob.glob(os.path.join(ROOT, "reviews", "*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for r in d.get("near", []):
            for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", r.get("code", "")):
                if len(tok) > 6:
                    flds.add(tok)
    return flds


def expr_fields(e):
    return {t for t in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", e) if len(t) > 6}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--size", type=int, default=48)
    ap.add_argument("--per-bucket", type=int, default=8)
    ap.add_argument("--max-field-repeat", type=int, default=3)
    a = ap.parse_args()

    cons_path = os.path.join(ROOT, "reference", "kor_generation_constraints.json")
    quota = {"linear_mix": 0.5}
    if os.path.exists(cons_path):
        quota = json.load(open(cons_path, encoding="utf-8"))["injection_rules"]["skeleton_quota"]
        quota = {k.split("(")[0]: v for k, v in quota.items()}
    lm_cap = quota.get("linear_mix", 0.5)

    d = json.load(open(a.file, encoding="utf-8"))
    exprs = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    exprs = [e for e in exprs if isinstance(e, str)]

    hist = history_hashes(exclude_path=a.file)
    deduped = [e for e in exprs if norm(e) not in hist]
    n_dup = len(exprs) - len(deduped)

    nf = near_fields()
    # near-miss 加权：含 near 字段者优先，其余保持原序
    deduped.sort(key=lambda e: 0 if expr_fields(e) & nf else 1)

    buckets = collections.defaultdict(list)
    for e in deduped:
        buckets[bucket_key(e)].append(e)
    bucket_sizes = {k: len(v) for k, v in sorted(buckets.items())}  # 抽样前记录桶规模

    picked, field_count, lm_count = [], collections.Counter(), 0
    # 轮转分桶抽样：每桶最多 per-bucket；linear_mix 骨架受配额约束
    progress = True
    while progress and len(picked) < a.size:
        progress = False
        for bk in sorted(buckets):
            lst = buckets[bk]
            while lst and len(picked) < a.size:
                e = lst[0]
                sk = skeleton(e)
                if sk == "linear_mix" and lm_count >= max(1, int(a.size * lm_cap)):
                    break  # 该桶剩余留到下轮（linear_mix 已满配额）
                if sum(1 for f in expr_fields(e) if field_count[f] >= a.max_field_repeat) > 0:
                    lst.pop(0)  # 字段超限，弃此式看下一式
                    continue
                lst.pop(0)
                picked.append(e)
                for f in expr_fields(e):
                    field_count[f] += 1
                if sk == "linear_mix":
                    lm_count += 1
                progress = True
                if len([x for x in picked if bucket_key(x) == bk]) >= a.per_bucket:
                    break

    sk_dist = collections.Counter(skeleton(e) for e in picked)
    meta = {
        "wave": a.wave, "source": a.file,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "input": len(exprs), "duplicates_dropped": n_dup, "selected": len(picked),
        "buckets": bucket_sizes,
        "skeleton_distribution": dict(sk_dist),
        "linear_mix_cap": lm_cap,
    }
    out = os.path.join(ROOT, "candidates", f"kor_wave{a.wave}_exprs.json")
    payload = {"meta": meta, "expressions": picked}
    tmp = out + ".tmp"
    json.dump(payload, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, out)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"wave -> {out}")


if __name__ == "__main__":
    main()
