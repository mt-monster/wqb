# -*- coding: utf-8 -*-
"""dataset_scan.py —— 数据集级选池扫描（零仿真成本，区域通用）

回答的问题不是「这个字段强不强」，而是**「下一步该开哪个数据集」**。
字段级探针 SOP（references/_probe-sop.md）之前必须先过这一层，否则会在
「已经全跑完的类目」上空转（EUR 2026-10-23 实证：INSTITUTIONS/EARNINGS/
INSIDERS/MACRO 四类合计仅 9 个集且全部跑完 ⇒ 按 category 轮转 = 白玩）。

## 用法

```bash
# ① 从平台拉取（推荐；coverage/alphaCount/valueScore 都是实时的）
#    先让 MCP 的 get_datasets 结果落到文件，例如把返回的 results 存成 JSON：
#    {"results": [ {id, category, coverage, fieldCount, alphaCount, valueScore, ...}, ... ]}
$WQ_PY <skill>/scripts/dataset_scan.py --region DEU --from-json cache/deu_datasets.json

# ② 离线退化模式（读本地 data/wqb.db 的 datasets 表，不看 coverage）
$WQ_PY <skill>/scripts/dataset_scan.py --region DEU --db data/wqb.db

# ③ 直接看有哪些集属于处女地（只要名单）
$WQ_PY <skill>/scripts/dataset_scan.py --region DEU --from-json cache/deu_datasets.json --virgin-only
```

产出：控制台表格 + 可选 `--out scan.json`。

## 分档口径（顺序即优先级）

| 档 | 判据 | 含义 |
|---|---|---|
| **V（virgin）** | `alphaCount <= 10` 且 `valueScore >= 5` | 全站几乎没人挖。**低覆盖是常态，覆盖率闸必须对它放宽** |
| **U（unlit cat）** | 该 category 下我方已提交 <= 3 | 未点亮类目，塔位竞争小 |
| **L（lit cat）** | 我方已提交 > 3 | 已点亮，降权 |
| **X** | `fieldCount < 3` 或 `status == platform_empty` | 不可挖，直接排除 |

✗ 注意：`coverage` 只是**排序权重**，不是硬闸 —— 先按 virgin 选人，再在
字段级用 cov 闸筛字段（两级覆盖门槛，见 references/_dataset-scan-method.md）。
"""
import argparse
import json
import os
import sqlite3
import sys

VIRGIN_AC = 10      # alpha_count <= 此值视为「几乎没人挖」
VIRGIN_VS = 5.0     # 且平台 value_score >= 此值
MIN_FIELDS = 3      # 字段数 < 3 的集不可挖（单字段做不出多族探针）


def _cat(v):
    """平台 category 可能是字符串，也可能是 {"id":..,"name":..} 字典。"""
    if isinstance(v, dict):
        v = v.get("id") or v.get("name") or "?"
    return str(v or "?").upper()


def load_from_json(path):
    j = json.load(open(path, encoding="utf-8"))
    rows = j.get("results") if isinstance(j, dict) else j
    out = []
    for r in rows or []:
        out.append({
            "dataset": r.get("id") or r.get("dataset"),
            "name": r.get("name"),
            "category": _cat(r.get("category")),
            "n_fields": r.get("fieldCount") or r.get("n_fields") or 0,
            "cov": r.get("coverage"),
            "aCnt": r.get("alphaCount"),
            "VS": r.get("valueScore"),
            "users": r.get("userCount"),
        })
    return out


def load_from_db(db, region):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    q = """SELECT d.name dataset, d.category, d.field_count n_fields,
                  d.coverage cov, d.alpha_count aCnt, d.value_score VS, d.status
           FROM datasets d JOIN regions g ON d.region_id = g.id
           WHERE g.name = ?"""
    rows = []
    for r in con.execute(q, (region,)):
        d = dict(r)
        d["category"] = (d["category"] or "?").upper()
        d["n_fields"] = d["n_fields"] or 0
        rows.append(d)
    return rows


def lit_counts(db):
    """我方已提交数（pyramids 派生的缓存，没有就当空）。"""
    for p in ("cache/lit_categories.json",):
        if os.path.exists(p):
            try:
                j = json.load(open(p, encoding="utf-8"))
                for reg, ent in (j or {}).items():
                    return {k.upper(): v for k, v in (ent.get("counts") or {}).items()}
            except Exception:
                pass
    return {}


def tier(d, lit, threshold=3):
    if (d.get("n_fields") or 0) < MIN_FIELDS:
        return "X"
    if (d.get("status") or "") == "platform_empty":
        return "X"
    cov = d.get("cov")
    # coverage 恰为 0 = 该 universe 内根本没有数据（不是「覆盖低」）。EUR/DEU 均实测：
    # 这类集开批必然空跑，必须在选池阶段就排除，否则会被 virgin 档误纳。
    if cov is not None and float(cov) <= 0.0:
        return "X"
    ac, vs = d.get("aCnt"), d.get("VS")
    if ac is not None and vs is not None and ac <= VIRGIN_AC and vs >= VIRGIN_VS:
        return "V"
    if lit.get(d["category"], 0) <= threshold:
        return "U"
    return "L"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--from-json", dest="src", default=None)
    ap.add_argument("--db", default="data/wqb.db")
    ap.add_argument("--out", default=None)
    ap.add_argument("--virgin-only", action="store_true")
    ap.add_argument("--virgin-cov", type=float, default=0.35,
                    help="处女地集的覆盖率放宽闸（仅作提示列，不做硬过滤）")
    a = ap.parse_args()

    if a.src:
        rows = load_from_json(a.src)
        src_desc = a.src
    else:
        if not os.path.exists(a.db):
            sys.exit(f"找不到 {a.db}，也没有 --from-json")
        rows = load_from_db(a.db, a.region)
        src_desc = f"{a.db}（离线；coverage 可能为 0，勿据此判覆盖）"
        zero = sum(1 for r in rows if not r.get("cov"))
        if zero > len(rows) * 0.5:
            print(f"⚠ {zero}/{len(rows)} 个集 coverage 为空/0 —— 离线表未扫描，"
                  f"选池请改用 --from-json 走平台实时画像\n")

    lit = lit_counts(a.db)
    for r in rows:
        r["tier"] = tier(r, lit)

    order = {"V": 0, "U": 1, "L": 2, "X": 3}
    rows.sort(key=lambda r: (order[r["tier"]],
                             r.get("aCnt") if r.get("aCnt") is not None else 9999,
                             -(r.get("VS") or 0),
                             -(r.get("cov") or 0)))

    if a.virgin_only:
        rows = [r for r in rows if r["tier"] == "V"]

    print(f"=== {a.region} 数据集扫描（来源 {src_desc}）===")
    print(f"总数 {len(rows)}｜V={sum(1 for r in rows if r['tier']=='V')}"
          f"｜U={sum(1 for r in rows if r['tier']=='U')}"
          f"｜L={sum(1 for r in rows if r['tier']=='L')}"
          f"｜X={sum(1 for r in rows if r['tier']=='X')}\n")
    print(f"{'档':<3}{'数据集':<28}{'类别':<14}{'字段':>5}{'覆盖':>7}{'全站α':>7}{'VS':>5}  建议")
    for r in rows:
        cov = r.get("cov")
        covs = f"{cov:.2f}" if isinstance(cov, (int, float)) else "—"
        ac = r.get("aCnt")
        acs = str(ac) if ac is not None else "—"
        vs = r.get("VS")
        vss = f"{vs:.0f}" if isinstance(vs, (int, float)) else "—"
        if r["tier"] == "X":
            if isinstance(cov, (int, float)) and cov <= 0:
                sug = "跳过（该 universe 无覆盖）"
            else:
                sug = "跳过（字段不足/平台空）"
        elif r["tier"] == "V":
            sug = ("开（低覆盖可接受）"
                   if (cov or 0) < 0.6 else "开（覆盖充足）")
        elif r["tier"] == "U":
            sug = "次优先（未点亮类目）"
        else:
            sug = "降权（已点亮类目）"
        print(f"{r['tier']:<3}{r['dataset']:<28}{r['category']:<14}"
              f"{r['n_fields']:>5}{covs:>7}{acs:>7}{vss:>5}  {sug}")

    if a.out:
        json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nsaved {a.out}")


if __name__ == "__main__":
    main()
