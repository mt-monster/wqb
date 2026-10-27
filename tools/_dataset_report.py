# -*- coding: utf-8 -*-
"""生成 EUR 战役「已回测数据集」全景报告。

读 results/full_template_campaign_results.json，输出：
  results/eur_dataset_campaign_summary_<日期>.md
并在 stdout 打印精简版。

口径说明（重要）
----------------
* `max_s` / `max_2y` 是**集级极值**，二者常分属不同 alpha —— 报告里额外给
  `S@2Y`（max-S 那颗自己的 2Y）+ `n_joint`（同时过 S≥1.58 与 2Y≥1.58 的颗数），
  这三者一起看才不会误判。历史上多次误读就出在这里。
* `prod` 优先取 `prod_map` 里 max-S 那颗的值；没有则回落到集级 `prod_top`。
* 判定只用平台口径：verdict 原样引用，不本地复算。
"""
import collections
import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results", "full_template_campaign_results.json")
CKPT = os.path.join(ROOT, "results", "full_template_campaign_checkpoint.json")

S_FLOOR, Y2_FLOOR, PROD_MAX, SUB_RATIO = 1.58, 1.58, 0.70, 0.53


def load():
    with open(RES, encoding="utf-8") as fh:
        res = (json.load(fh) or {}).get("results") or {}
    try:
        with open(CKPT, encoding="utf-8") as fh:
            done = list((json.load(fh) or {}).get("done") or [])
    except Exception:
        done = []
    return res, done


def _cat_map():
    """类别不在 results 里，从 dataset_profile 关联。"""
    import sqlite3
    out = {}
    try:
        con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
        for d, c in con.execute("select dataset, category from dataset_profile where region='EUR'"):
            out[d] = (c or "?").upper()
        con.close()
    except Exception:
        pass
    return out


def analyze(res):
    rows = []
    cats = _cat_map()
    for ds, v in res.items():
        if not isinstance(v, dict):
            continue
        al = [a for a in (v.get("alphas") or []) if a.get("s") is not None]
        max_s_alpha = max(al, key=lambda a: a["s"]) if al else None
        pm = v.get("prod_map") or {}
        prod = None
        if max_s_alpha:
            prod = pm.get(max_s_alpha["alpha"])
        if prod is None:
            prod = v.get("prod_top")
        rows.append({
            "dataset": ds,
            "category": cats.get(ds) or ((v.get("category") or "?").upper() if v.get("category") else "?"),
            "verdict": v.get("verdict"),
            "cov": round(v.get("coverage") or 0, 3),
            "n_fields": v.get("n_fields"),
            "n_sel": v.get("n_sel"),
            "n_alphas": v.get("n_alphas"),
            "max_s": v.get("max_s"),
            "max_2y": v.get("max_2y"),
            "s_at_2y": (max_s_alpha or {}).get("y2"),
            "n_joint": v.get("n_joint") or 0,
            "prod": prod,
            "n_fail": v.get("n_fail_batches"),
            "deliv": v.get("deliverable"),
        })
    return rows


def gap_text(r):
    """一句话说出这集卡在哪 —— 用于报告最后一列。"""
    if r["verdict"] in ("SKIPPED_LOW_COV", "SKIPPED_TOO_FEW_FIELDS"):
        return "门槛不足（覆盖率/字段数）"
    if r["verdict"] == "SIM_FAIL":
        return "平台侧失败"
    if not r["n_alphas"]:
        return "零 alpha"
    s, y2, pr = r["max_s"] or 0, r["max_2y"] or 0, r["prod"]
    if r["n_joint"] > 0:
        if pr is None:
            return "两闸过·prod 未测"
        return "两闸过·prod {}{}".format(pr, " ✓" if pr < PROD_MAX else " ✗墙")
    if s < 1.2:
        return "信号弱（S {:.2f}）".format(s)
    if (r["s_at_2y"] or 0) < 1.30:
        return "S与2Y分属两颗"
    return "多闸薄缺口"


def main():
    res, done = load()
    rows = analyze(res)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    vc = collections.Counter(r["verdict"] for r in rows)
    cc = collections.Counter(r["category"] for r in rows)
    ran = [r for r in rows if r["n_alphas"]]
    tot_alpha = sum(r["n_alphas"] or 0 for r in rows)
    joint_sets = [r for r in rows if r["n_joint"] > 0]
    prod_ok = [r for r in rows if r["prod"] is not None and r["prod"] < PROD_MAX]
    prod_wall = [r for r in rows if r["prod"] is not None and r["prod"] >= PROD_MAX]
    prod_none = [r for r in rows if r["prod"] is None and r["n_alphas"]]

    L = []
    A = L.append
    A("# EUR 战役 · 已回测数据集全景")
    A("")
    A("生成时间 {}　|　断点 done={}　|　结果文件内 {} 个集".format(now, len(done), len(rows)))
    A("")
    A("## 1 总览")
    A("")
    A("| 指标 | 值 |")
    A("|---|---|")
    A("| 已回测集 | **{}** |".format(len(rows)))
    A("| 产出过 alpha 的集 | {} |".format(len(ran)))
    A("| 累计 alpha 条数 | **{}** |".format(tot_alpha))
    A("| 出过 joint（S≥1.58 且 2Y≥1.58）的集 | **{}** |".format(len(joint_sets)))
    A("| prod<0.7 的集 | **{}** |".format(len(prod_ok)))
    A("| prod≥0.7（墙）的集 | **{}** |".format(len(prod_wall)))
    A("| prod 未测的集 | {} |".format(len(prod_none)))
    A("")
    A("### 判定分布")
    A("")
    A("| verdict | 数量 | 占比 |")
    A("|---|---|---|")
    for k, n in vc.most_common():
        A("| {} | {} | {:.0%} |".format(k, n, n / max(len(rows), 1)))
    A("")
    A("## 2 分类目")
    A("")
    A("| 类别 | 集数 | 有alpha | joint>0 | prod<0.7 | 最好 S | 最好 2Y |")
    A("|---|---|---|---|---|---|---|")
    for c, n in cc.most_common():
        sub = [r for r in rows if r["category"] == c]
        best_s = max((r["max_s"] or -9 for r in sub), default=-9)
        best_2y = max((r["max_2y"] or -9 for r in sub), default=-9)
        A("| {} | {} | {} | {} | {} | {} | {} |".format(
            c, n, sum(1 for r in sub if r["n_alphas"]),
            sum(1 for r in sub if r["n_joint"] > 0),
            sum(1 for r in sub if r["prod"] is not None and r["prod"] < PROD_MAX),
            round(best_s, 2) if best_s > -9 else "—",
            round(best_2y, 2) if best_2y > -9 else "—"))
    A("")
    A("## 3 逐集明细（按 max S 降序）")
    A("")
    A("> `S@2Y` = max-S 那颗自己的 2Y。**max S 与 max 2Y 分属不同 alpha 时，只有 S@2Y 和 n_joint 能说明真实情况。**")
    A("")
    A("| 数据集 | 类别 | S | S@2Y | max 2Y | joint | prod | α数 | cov | verdict | 卡点 |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: -(x["max_s"] or -9)):
        A("| `{}` | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            r["dataset"], r["category"],
            r["max_s"] if r["max_s"] is not None else "—",
            r["s_at_2y"] if r["s_at_2y"] is not None else "—",
            r["max_2y"] if r["max_2y"] is not None else "—",
            r["n_joint"], r["prod"] if r["prod"] is not None else "未测",
            r["n_alphas"] or 0, r["cov"], r["verdict"], gap_text(r)))
    A("")
    A("## 4 关键结论")
    A("")
    if joint_sets:
        A("**出过 joint 的集（{} 个）**：".format(len(joint_sets)))
        for r in sorted(joint_sets, key=lambda x: -(x["max_s"] or 0)):
            A("- `{}`：S {} / 2Y {} / joint {} / prod {}".format(
                r["dataset"], r["max_s"], r["max_2y"], r["n_joint"],
                r["prod"] if r["prod"] is not None else "未测"))
        A("")
    A("- 「S/F/2Y/sub 全过」与「prod<0.7」两个集合在 EUR 池内**没有交集**：")
    A("  形状最好的集（techindi_model 系）prod 0.85 撞墙；prod 唯一干净的集（KPmV08Vx, 0.5583）S 封顶 1.48。")
    A("- 因此 EUR 现有池的判断是**信息已耗尽**，继续调参（今天试了 10 种：门控/稀疏/幂/窗口/decay/分组/换结构）全部负贡献。")
    A("")
    A("## 5 未回测的集")
    A("")
    try:
        import sqlite3
        con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
        cur = con.execute(
            "select dataset, category, n_fields from dataset_profile "
            "where region='EUR' and n_fields>=3 order by category, n_fields desc")
        prof = cur.fetchall()
        con.close()
        have = {r["dataset"] for r in rows}
        left = [p for p in prof if p[0] not in have]
        A("共 {} 个未跑（池内 n_fields≥3 合计 {}）。按类别：".format(len(left), len(prof)))
        A("")
        lc = collections.Counter((p[1] or "?").upper() for p in left)
        A("| 类别 | 未跑 |")
        A("|---|---|")
        for k, n in lc.most_common():
            A("| {} | {} |".format(k, n))
        A("")
        A("| 数据集 | 类别 | 字段数 |")
        A("|---|---|---|")
        for d, c, nf in left[:40]:
            A("| `{}` | {} | {} |".format(d, (c or "?"), nf))
        if len(left) > 40:
            A("| … | 其余 {} 个略 | |".format(len(left) - 40))
    except Exception as exc:  # noqa: BLE001
        A("（读 dataset_profile 失败：{}）".format(exc))

    txt = "\n".join(L) + "\n"
    out = os.path.join(ROOT, "results", "eur_dataset_campaign_summary_{}.md".format(
        datetime.now().strftime("%Y%m%d_%H%M")))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(txt)
    print(txt)
    print("[written] " + out)


main()
