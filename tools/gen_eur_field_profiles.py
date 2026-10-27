#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EUR 全量数据集字段画像生成器

用法：
    python tools/gen_eur_field_profiles.py

输出：
    docs/reference/EUR/datasets/README.md        # 总索引
    docs/reference/EUR/datasets/<dataset>.md     # 每数据集一份画像

画像内容（每个数据集）：
    1. 元信息表（类别 / 覆盖 / 字段数 / alphaCount / valueScore / 金字塔倍率 / 类型 / delay）
    2. 数据集描述
    3. 字段画像汇总（类型分布 / 覆盖率分档 / 更新频率推断 / 可用性评级）
    4. 语义维度地图（按字段名与描述关键词自动归类）
    5. 全字段明细（名称 | 类型 | 覆盖 | 描述）
"""
import os
import re
import json
import sqlite3          # 仅用于 sqlite3.Row（连接本身一律走 db_connect）
import sys
import collections
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "wqb.db")
OUT = os.path.join(ROOT, "docs", "reference", "EUR", "datasets")

# 连接一律走规范工厂（只读：本脚本只生成 markdown 画像）。
sys.path.insert(0, os.path.join(ROOT, "src"))
from wqb.db_conn import connect as db_connect  # noqa: E402

# ---------------------------------------------------------------- 语义族规则
# (族名, 正则)  按顺序优先匹配；正则作用于 "字段名 + 描述" 的小写拼接
FAMILY_RULES = [
    ("修正与预期", r"revision|estimate|consensus|analyst|target price|recommend|upgrade|downgrade"),
    ("盈利与财务", r"earning|revenue|ebit|ebitda|net income|profit|margin|cash flow|accrual|asset|liabilit|equity|debt|dividend|payout"),
    ("价量与波动", r"price|volume|return|volatil|momentum|reversal|vwap|turnover|liquidit|spread|bid|ask|quote|trade"),
    ("情绪与新闻", r"sentiment|news|tone|polarity|emotion|buzz|attention|article|headline|nlp"),
    ("持仓与资金流", r"holding|holding|ownership|institution|insider|fund|flow|position|stake|beneficial|lending|borrow|short interest"),
    ("宏观与行业", r"macro|gdp|inflation|rate|yield|commodit|sector|industry|country|region|oil|currency|fx"),
    ("风险与质量", r"risk|beta|drawdown|default|credit|vol|quality|rank|score|crowding|congestion"),
    ("交易与微观结构", r"order|imbalance|queue|depth|execution|auction|session|intraday|tick|micro"),
    ("搜索与替代数据", r"search|google|web|social|twitter|app|satellite|traffic|alternative"),
    ("元数据与非信号", r"identifier|code|gvkey|isin|sedol|cusip|ticker|currency|datatime|timestamp|date$|_id$|name$"),
]

COV_BUCKETS = [
    ("高 (≥0.90)", 0.90, 1.01),
    ("中 (0.70–0.90)", 0.70, 0.90),
    ("低 (0.50–0.70)", 0.50, 0.70),
    ("稀疏 (<0.50)", -0.01, 0.50),
]


def classify(name: str, desc: str) -> str:
    text = f"{name} {desc or ''}".lower()
    for fam, pat in FAMILY_RULES:
        if re.search(pat, text):
            return fam
    return "其他"


def infer_frequency(ftype: str, desc: str, name: str) -> str:
    d = (desc or "").lower()
    if re.search(r"quarter|13f|annual|yearly", d):
        return "低频（季/年）"
    if ftype == "VECTOR":
        return "事件/逐笔型（VECTOR）"
    if re.search(r"daily|day", d):
        return "日频"
    if re.search(r"intraday|tick|minute|session|interval", d):
        return "日内（分钟/逐笔）"
    return "快照（按库表更新，需实测）"


def availability(avg_cov: float, n: int) -> str:
    if avg_cov >= 0.90:
        return "优（覆盖 ≥90%，可直接做尽）"
    if avg_cov >= 0.70:
        return "良（覆盖 70–90%，sub/robust 需关注）"
    if avg_cov >= 0.50:
        return "中（覆盖 50–70%，截面偏窄）"
    return "低（覆盖 <50%，仅作条件/分组或放弃）"


def md_escape(s: str) -> str:
    return (s or "").replace("|", "/").replace("\n", " ").strip()


def build(con, row) -> str:
    name = row["name"]
    cat = row["category"] or "—"
    fields = list(con.execute(
        """SELECT f.field_name, f.field_type, f.coverage, f.description,
                  p.n_tests, p.best_s, p.best_2y, p.best_sub, p.best_f,
                  p.verdict, p.skeleton_fams
           FROM fields f
           LEFT JOIN field_profile_perf p
                  ON p.region = 'EUR' AND p.dataset = ? AND p.field = f.field_name
           WHERE f.dataset_id = ?
             AND EXISTS (SELECT 1 FROM datasets d JOIN regions g ON g.id = d.region_id
                          WHERE d.id = f.dataset_id AND g.name = 'EUR')
           ORDER BY COALESCE(p.best_s, -99) DESC, f.coverage DESC, f.field_name""",
        (name, row["id"])))

    L = []
    A = L.append
    A(f"# {name} — EUR 字段画像")
    A("")
    A(f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}　|　"
      f"[← 返回索引](README.md)")
    A("")
    A("## 一、数据集元信息")
    A("")
    A("| 项 | 值 |")
    A("|---|---|")
    A(f"| 数据集 ID | `{name}` |")
    A(f"| 名称 | {md_escape(row['title'] or '—')} |")
    A(f"| 类别 | {cat} |")
    cov = row.get('_catcov', row['coverage'])
    ac = row.get('_catac', row['alpha_count'])
    vs = row.get('_catvs', row['value_score'])
    pm = row.get('_catpm', row['pyramid_multiplier'])
    fc = row.get('_catfc', row['field_count'])
    A(f"| 数据字段数(平台) | {fc if fc is not None else '—'} |")
    A(f"| 覆盖率 | {cov if cov is not None else '—'} |")
    A(f"| 平台已有 alpha | {ac or 0} |")
    A(f"| valueScore | {vs if vs is not None else '—'} |")
    A(f"| 金字塔倍率 | {pm if pm is not None else '—'} |")
    A(f"| 数据类型 | {row['data_type'] or '—'} |")
    A(f"| delay | {row['delay'] if row['delay'] is not None else '—'} |")
    A(f"| 状态 | {row['status'] or '—'} |")
    A("")
    desc = row.get("_desc") or ""
    A("## 二、数据集描述（平台原文）")
    A("")
    A("> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。"
      "以「五、全字段明细」的真实字段语义为准。")
    A("")
    A(desc if desc else "（平台目录未返回描述）")
    A("")

    if not fields:
        A("## 三、字段明细")
        A("")
        A("> ⚠️ 本地库未扫描到该数据集的字段目录。需用 `get_datafields(dataset_id=...)` 补拉。")
        return "\n".join(L) + "\n"

    # 汇总
    types = collections.Counter(f["field_type"] or "—" for f in fields)
    covs = [f["coverage"] for f in fields if f["coverage"] is not None]
    avg_cov = sum(covs) / len(covs) if covs else 0.0
    fams = collections.OrderedDict()
    for f in fields:
        fam = classify(f["field_name"], f["description"])
        fams.setdefault(fam, []).append(f)

    A("## 三、字段画像汇总")
    A("")
    A("| 维度 | 结果 |")
    A("|---|---|")
    A(f"| 字段总数 | **{len(fields)}** |")
    A(f"| 类型分布 | " + "　".join(f"{k}×{v}" for k, v in types.most_common()) + " |")
    A(f"| 平均覆盖率 | **{avg_cov:.3f}** |")
    if covs:
        A(f"| 覆盖率区间 | {min(covs):.2f} ~ {max(covs):.2f} |")
    A(f"| 更新频率（推断） | {infer_frequency(fields[0]['field_type'] or '', fields[0]['description'] or '', fields[0]['field_name'])} |")
    A(f"| 可用性评级 | {availability(avg_cov, len(fields))} |")
    A("")
    A("**覆盖率分档**")
    A("")
    A("| 档 | 字段数 | 占比 |")
    A("|---|---:|---:|")
    for label, lo, hi in COV_BUCKETS:
        n = sum(1 for c in covs if lo <= c < hi)
        A(f"| {label} | {n} | {n / len(fields) * 100:.1f}% |")
    A("")

    # 历史实测分布
    verd = collections.Counter((f["verdict"] or "UNTESTED") for f in fields)
    tested = [f for f in fields if (f["n_tests"] or 0) > 0]
    best_s_vals = [f["best_s"] for f in tested if f["best_s"] is not None]
    A("**历史实测分布（field_profile_perf）**")
    A("")
    A("| 判定 | 字段数 | 占比 |")
    A("|---|---:|---:|")
    for v, n in verd.most_common():
        A(f"| {v} | {n} | {n / len(fields) * 100:.1f}% |")
    A("")
    if best_s_vals:
        A(f"- 已实测字段：**{len(tested)}** 个（{len(tested)/len(fields)*100:.0f}%），"
          f"best_sharpe 最高 **{max(best_s_vals):.2f}**，中位 {sorted(best_s_vals)[len(best_s_vals)//2]:.2f}")
        alive = [f for f in fields if (f["verdict"] or "") == "ALIVE"]
        if alive:
            A(f"- ★ ALIVE（历史测出 S≥闸线）字段 **{len(alive)}** 个："
              + "、".join(f"`{a['field_name']}`(S {a['best_s']:.2f})" for a in alive[:8]))
    else:
        n_untested = verd.get("UNTESTED", 0)
        if n_untested == len(fields):
            A("- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽")
        else:
            A(f"- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在"
              f"（UNTESTED {n_untested} / UNUSABLE {verd.get('UNUSABLE',0)} 等）。"
              f"⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。")
    A("")

    # 语义维度地图
    A("## 四、语义维度地图（自动归类）")
    A("")
    A("| 语义族 | 字段数 | 平均覆盖 | 代表字段 |")
    A("|---|---:|---:|---|")
    for fam, fs in sorted(fams.items(), key=lambda kv: -len(kv[1])):
        fc = [x["coverage"] for x in fs if x["coverage"] is not None]
        ac = sum(fc) / len(fc) if fc else 0
        samples = "、".join(x["field_name"] for x in fs[:3])
        A(f"| {fam} | {len(fs)} | {ac:.2f} | {samples} |")
    A("")

    # 全字段明细
    A("## 五、全字段明细")
    A("")
    A("> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`："
      "ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；"
      "UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。")
    A("")
    A("| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |")
    A("|---:|---|---|---:|---|---:|---:|---:|---:|---|---|")
    for i, f in enumerate(fields, 1):
        fam = classify(f["field_name"], f["description"])
        bs = f"{f['best_s']:.2f}" if f["best_s"] is not None else "—"
        b2 = f"{f['best_2y']:.2f}" if f["best_2y"] is not None else "—"
        sb = f"{f['best_sub']:.2f}" if f["best_sub"] is not None else "—"
        A(f"| {i} | `{f['field_name']}` | {f['field_type'] or '—'} | "
          f"{(f['coverage'] or 0):.3f} | {fam} | {f['n_tests'] or 0} | {bs} | {b2} | {sb} | "
          f"{f['verdict'] or 'UNTESTED'} | {md_escape(f['description'])[:140]} |")
    A("")

    # 六、本地回测证据
    bt = list(con.execute(
        """SELECT alpha_id, sharpe, fitness, two_year_sharpe, sub_universe_sharpe,
                  turnover, ra_failed_checks, wave, code
           FROM backtest_results WHERE region='EUR' AND dataset=?
           ORDER BY COALESCE(sharpe,-99) DESC LIMIT 15""", (name,)))
    n_bt = con.execute(
        "SELECT COUNT(*) c FROM backtest_results WHERE region='EUR' AND dataset=?",
        (name,)).fetchone()["c"]
    n_ra = con.execute(
        """SELECT COUNT(*) c FROM backtest_results WHERE region='EUR' AND dataset=?
           AND (ra_failed_checks IS NULL OR ra_failed_checks='' OR ra_failed_checks='[]')""",
        (name,)).fetchone()["c"]
    A("## 六、本地回测证据")
    A("")
    if n_bt:
        A(f"- 本地累计回测 **{n_bt}** 条；其中 `ra_failed_checks` 为空的 **{n_ra}** 条"
          f"（⚠ 空不等于过关，2Y 为 NULL 者需复检）")
        A("")
        A("| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |")
        A("|---|---:|---:|---:|---:|---:|---|---:|---|")
        for b in bt:
            rc = b["ra_failed_checks"]
            rc_n = "0" if (rc is None or rc in ("", "[]")) else str(rc)[:12]
            s = lambda v: f"{v:.2f}" if v is not None else "—"
            A(f"| `{b['alpha_id']}` | {s(b['sharpe'])} | {s(b['fitness'])} | {s(b['two_year_sharpe'])} | "
              f"{s(b['sub_universe_sharpe'])} | {s(b['turnover'])} | {rc_n} | {b['wave'] or '—'} | "
              f"`{md_escape(b['code'] or '')[ :90]}` |")
    else:
        A("本地库无该数据集的回测记录。")
        A("")
        A("> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 "
          + str(con.execute("SELECT COUNT(*) c FROM backtest_results WHERE region='EUR'").fetchone()["c"])
          + " 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。")
    A("")

    # 七、判死记录
    dead = []
    for e in con.execute(
            "SELECT entry_id, family, payload, dead_at FROM registry_empirical "
            "WHERE region='EUR' AND layer='dead_end' ORDER BY dead_at"):
        payload = e["payload"] or ""
        if name in payload:
            dead.append(e)
    A("## 七、判死记录（sealed dead_end）")
    A("")
    if dead:
        for d in dead:
            A(f"- `{d['entry_id']}`（{d['dead_at']}）family={d['family']}：{md_escape(d['payload'])[:400]}")
    else:
        A("无针对本数据集的 `dead_end` 记录。")
    A("")
    return "\n".join(L) + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    con = db_connect(DB, readonly=True)
    con.row_factory = sqlite3.Row

    # 平台目录（名称 / 描述 / 平台口径覆盖与 alphaCount）
    cat_path = os.path.join(ROOT, "tracking", "EUR", "reference", "eur_dataset_catalog.json")
    catalog = {}
    if os.path.exists(cat_path):
        with open(cat_path, encoding="utf-8") as fh:
            catalog = json.load(fh)

    rows = list(con.execute(
        """SELECT d.id, d.name, d.category, d.field_count, d.coverage, d.alpha_count,
                  d.value_score, d.pyramid_multiplier, d.data_type, d.delay, d.status,
                  d.catalog_json
           FROM datasets d JOIN regions r ON d.region_id = r.id
           WHERE r.name = 'EUR' ORDER BY d.category, d.name"""))

    # 每数据集画像
    written = 0
    for row in rows:
        row = dict(row)
        row["title"] = ""
        try:
            cj = json.loads(row["catalog_json"]) if row["catalog_json"] else {}
            row["title"] = cj.get("name") or ""
        except Exception:
            pass
        cat = catalog.get(row["name"]) or {}
        if cat:
            row["title"] = cat.get("name") or row["title"]
            row["_desc"] = cat.get("description") or ""
            row["_catcov"] = cat.get("coverage")
            row["_catac"] = cat.get("alphaCount")
            row["_catfc"] = cat.get("fieldCount")
            row["_catvs"] = cat.get("valueScore")
            row["_catpm"] = cat.get("pyramidMultiplier")
            row["_catcat"] = cat.get("category")
        else:
            row["_desc"] = ""
        text = build(con, row)
        fn = os.path.join(OUT, f"{re.sub(r'[^A-Za-z0-9_.-]', '_', row['name'])}.md")
        with open(fn, "w", encoding="utf-8") as fh:
            fh.write(text)
        written += 1

    # 索引
    cat_stats = collections.defaultdict(lambda: {"ds": 0, "fl": 0, "ac": 0})
    total_fl = 0
    total_ac = 0
    _seen = set()          # 同名多 region 行去重（同名字段集只计一次）
    _maxac = {}            # 同名取 max(alpha_count)
    for row in rows:
        row = dict(row)
        n = con.execute(
            "SELECT COUNT(*) c FROM fields f WHERE f.dataset_id=? "
            "AND EXISTS (SELECT 1 FROM datasets d JOIN regions g ON g.id = d.region_id "
            "             WHERE d.id = f.dataset_id AND g.name = 'EUR')",
            (row["id"],)).fetchone()["c"]
        cat = row["category"] or "—"
        if row["name"] in _seen:
            _maxac[row["name"]] = max(_maxac.get(row["name"], 0), row["alpha_count"] or 0)
            continue
        _seen.add(row["name"])
        _maxac[row["name"]] = row["alpha_count"] or 0
        cat_stats[cat]["ds"] += 1
        cat_stats[cat]["fl"] += n
        total_fl += n
    total_ac = sum(_maxac.values())
    for nm, ac in _maxac.items():
        r0 = next((x for x in rows if x["name"] == nm), None)
        if r0 is not None:
            cat_stats[r0["category"] or "—"]["ac"] += ac

    L = [f"# EUR 全量数据集字段画像（索引）", "",
         f"> 自动生成 {datetime.now().strftime('%Y-%m-%d %H:%M')}　|　"
         f"数据集 **{len(rows)}** 个　|　字段 **{total_fl:,}** 条　|　平台 alpha 累计 {total_ac:,}", "",
         "## 一、类别分布", "",
         "| 类别 | 数据集 | 字段 | 平台 alpha |", "|---|---:|---:|---:|"]
    for cat, s in sorted(cat_stats.items(), key=lambda kv: -kv[1]["fl"]):
        L.append(f"| {cat} | {s['ds']} | {s['fl']:,} | {s['ac']:,} |")
    L += ["", "## 二、数据集清单", "",
          "| 数据集 | 类别 | 字段 | 覆盖 | 已有alpha | valueScore | 金字塔 | 画像 |",
          "|---|---|---:|---:|---:|---:|---:|---|"]
    for row in rows:
        row = dict(row)
        n = con.execute(
            "SELECT COUNT(*) c FROM fields f WHERE f.dataset_id=? "
            "AND EXISTS (SELECT 1 FROM datasets d JOIN regions g ON g.id = d.region_id "
            "             WHERE d.id = f.dataset_id AND g.name = 'EUR')",
            (row["id"],)).fetchone()["c"]
        link = f"[{row['name']}]({row['name']}.md)" if n else f"{row['name']}（未扫描）"
        L.append(f"| {link} | {row['category'] or '—'} | {n or row['field_count'] or '—'} | "
                 f"{row['coverage'] if row['coverage'] is not None else '—'} | "
                 f"{row['alpha_count'] or 0} | {row['value_score'] if row['value_score'] is not None else '—'} | "
                 f"{row['pyramid_multiplier'] if row['pyramid_multiplier'] is not None else '—'} | "
                 f"{'✅' if n else '⚠️'} |")
    L += ["", "## 三、字段画像口径说明", "",
          "- **语义族**：按字段名 + 描述关键词自动归类（10 族 + 其他），用于快速定位可做尽的维度",
          "- **更新频率**：由描述关键词与字段类型推断（VECTOR=事件/逐笔；MATRIX=快照）",
          "- **可用性评级**：基于平均覆盖率（≥90% 优 / 70–90% 良 / 50–70% 中 / <50% 低）",
          "- **覆盖分档**：高 ≥0.90｜中 0.70–0.90｜低 0.50–0.70｜稀疏 <0.50",
          "- ⚠️ 标「未扫描」的数据集本地库无字段目录，需 `get_datafields` 补拉后再做尽",
          "- ⚠️ `field_profile_perf` 的判定是**历史快照**，可能过时：已知 analyst7 的旧判死已被推翻、"
          "部分数据集的 UNUSABLE 来自旧结构。做尽前必须按 current 结构重跑，勿直接引用旧判定。",
          "- ⚠️ 平台目录的「数据集描述」存在错配（insiders1 / imbalance5 已实证），以字段明细语义为准。"]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print(f"written {written} dataset profiles + README.md -> {OUT}")
    print(f"total fields {total_fl}, datasets {len(rows)}")


if __name__ == "__main__":
    main()
