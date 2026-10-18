# -*- coding: utf-8 -*-
"""sweep_unsampled.py — 未采样族高覆盖字段扫描器（带断点续跑）

用法：
    python cache/sweep_unsampled.py --build          # 生成下一批（默认 10 条）
    python cache/sweep_unsampled.py --status         # 查看进度
    python cache/sweep_unsampled.py --reset          # 重置状态（慎用）

状态文件：cache/deu_sweep_state.json（已消费的「数据集|类别|族」组）
工作表  ：cache/deu_truly_unsampled_groups.json
输出    ：cache/deu_sweep_batch.txt / .labels.txt
"""
import argparse, json, os, re, sys, importlib.util, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS = os.path.join(ROOT, 'cache', 'deu_truly_unsampled_groups.json')
STATE = os.path.join(ROOT, 'cache', 'deu_sweep_state.json')
OUT = os.path.join(ROOT, 'cache', 'deu_sweep_batch.txt')
OUTL = os.path.join(ROOT, 'cache', 'deu_sweep_batch.labels.txt')


def load_api():
    spec = importlib.util.spec_from_file_location("api_client", os.path.join(ROOT, "tools", "lib", "api_client.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    api = m.Api(); api.login(*m.load_creds())
    return api


def structure(field, agg, use_core=False):
    b = "ts_backfill(%s(%s), 1008)" % (agg, field) if agg else "ts_backfill(%s, 1008)" % field
    if use_core:
        return ("group_neutralize(group_zscore(ts_decay_linear(quantile(add(ts_mean(%s, 5), ts_mean(%s, 200))), 8), sector), "
                "bucket(rank(ts_mean(%s, 252)), range=\"0,1,0.05\"))" % (b, b, b))
    return ("group_neutralize(group_rank(add(ts_mean(%s, 1), ts_mean(%s, 210)), sector), "
            "bucket(rank(ts_mean(%s, 252)), range=\"0,1,0.05\"))" % (b, b, b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--reset', action='store_true')
    ap.add_argument('--n', type=int, default=10)
    a = ap.parse_args()

    groups = json.load(open(GROUPS, encoding='utf-8'))
    state = json.load(open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {"done": []}
    if a.reset:
        state = {"done": []}; json.dump(state, open(STATE, 'w', encoding='utf-8')); print("已重置")

    done = set(state["done"])
    keys = [k for k in groups if k not in done]

    if a.status or not a.build:
        print("总组数 %d | 已完成 %d | 剩余 %d ⇒ 剩余约 %d 批" % (len(groups), len(done), len(keys), -(-len(keys)//a.n)))
        return

    # 字段类型缓存（按数据集）
    api = load_api()
    tcache, fc = {}, {}
    def fieldtype(ds, fn):
        if ds not in tcache:
            seen = []; o = 0
            while o < 800:
                try:
                    j = json.loads(api.get("/data-fields?instrumentType=EQUITY&region=DEU&delay=1&universe=TOP500&dataset.id=%s&limit=50&offset=%d" % (ds, o)).read().decode())
                except Exception:
                    break
                r = j.get("results", [])
                if not r: break
                seen += r; o += 50
            tcache[ds] = {x["id"]: x.get("type") for x in seen}
        return tcache[ds].get(fn)

    # 关键词（排除非信号/轴字段）
    BAD = ('_time', '_date', '_id', 'timestamp', 'epoch', 'country', 'currency', 'code', 'name', 'title', 'text',
           'headline', 'num_fields', 'divisor', 'flag', 'type', 'category', 'topic')
    picked = []
    for k in keys:
        if len(picked) >= a.n: break
        ds, cat, fam = k.split("|")
        cands = [f for f in groups[k] if not any(b in f.lower() for b in BAD)]
        if not cands: continue
        fn = cands[0]
        t = fieldtype(ds, fn)
        if t not in ("MATRIX", "VECTOR"): continue
        agg = "vec_avg" if t == "VECTOR" else None
        # 交替使用两种结构：偶数槽用 A 级框架，奇数槽用 DEU 核心（跨结构覆盖）
        expr = structure(fn, agg, use_core=(len(picked) % 2 == 1))
        picked.append((k, "%s|%s|%s" % (ds, fam, fn[:28]), expr))
        fc[fn] = t

    if not picked:
        print("没有可生成的组（全部完成或全被过滤）"); return
    with open(OUT, 'w', encoding='utf-8') as fo, open(OUTL, 'w', encoding='utf-8') as fl:
        for _, lab, e in picked:
            fo.write(e + "\n"); fl.write(lab + "\n")
    state["done"] = list(done | {k for k, _, _ in picked})
    json.dump(state, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False)
    print("本批 %d 条（累计完成 %d/%d 组）:" % (len(picked), len(state["done"]), len(groups)))
    for _, lab, _ in picked:
        print("   ", lab)
    print("写出:", OUT)


if __name__ == '__main__':
    main()
