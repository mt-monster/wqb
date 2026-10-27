"""gen_llm_field_tags.py — 用「语义族」生成字段打标 JSON（LLM 判断的固化产物，2026-10-23）

背景：流水线离线运行，不能调 LLM。做法是**离线打标 → 文件集成**：
  1) `export_fields_for_tagging.py` 导出待标字段；
  2) LLM（会话内）读 description，得出「这个字段本质是什么形态」的判断，
     按语义族固化成规则（本脚本），产出 `cache/field_form_llm.json`；
  3) 流水线 `field_form()` 按 overrides > LLM(conf≥0.7) > 正则 > other 取用，热加载。

与正则的关键区别：这里的族是按**语义**划的（例如「情感分 ssc/nip/bam 是连续量」、
「headline/event_text 是文本 ⇒ skip」、「event_index 是发布顺序 ⇒ skip」），
而不是靠字段名里撞到某个词。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "wqb.db")
OUT = os.path.join(ROOT, "cache", "field_form_llm.json")

# 连接一律走规范工厂（只读：本脚本只导字段标签到 JSON）。
sys.path.insert(0, os.path.join(ROOT, "src"))
from wqb.db_conn import connect as db_connect  # noqa: E402

# (form, conf, why, 匹配函数)  —— 顺序即优先级
RULES = [
    # ---------- 非经济：文本 / 时间戳 / 顺序索引 / 分类编码 / 标识 ----------
    ("skip", 0.95, "文本类（标题/正文/摘要），无经济数值",
     r"(_headline|_event_text|event_text$|_text$|_summary$|_description$|_title)"),
    ("skip", 0.95, "时间戳/日期时间，非经济量",
     r"(_time$|_utc|timestamp|_date$|^date_|_datetime)"),
    ("skip", 0.90, "发布顺序索引，非经济量",
     r"(_index$|_seq$|event_index)"),
    ("skip", 0.95, "网址/链接文本",
     r"(website|_url$|_link$|_hyperlink)"),
    ("skip", 0.90, "分类编码/标识（行业码、阶段、类型、地区、ID）",
     r"(_code$|_sic|_category$|_stage$|_stage_|_type$|_flag$|_id$|isin|ticker|_exchange$|_region$|_veic|_ticker)"),

    # ---------- 变化/修正量 ----------
    ("change", 0.95, "变化/修正/超预期语义，差分族为主",
     r"(change|revision|surprise|_delta|growth|_qoq|_yoy|_diff$|chg)"),

    # ---------- 计数 ----------
    ("count", 0.90, "计数/数量语义",
     r"(_count$|_count_|_num$|_num_|number_of|_domains|domains$|_volume|_shares$)"),

    # ---------- 离散分位/阈值 ----------
    ("discrete_rating", 0.90, "分位/阈值/等级语义（不是连续量）",
     r"(top\d+pctranking|_percentile|cutpoint|_rating$|_grade$|_tier$|quartile|decile)"),

    # ---------- 水平量/比率（连续） ----------
    ("level_ratio", 0.90, "连续情感分（-1~1），水平量本体即信号",
     r"(ssc$|_nip$|nip$|_bam$|bam$|_qmb$|qmb$|_qep$|qep$|_qcm$|qcm$|_acb$|acb$|"
     r"_bee$|bee$|ghc_lna|sentiment|_tone)"),
    ("level_ratio", 0.85, "相关度 0-100 连续分",
     r"(relevance$)"),
    ("level_ratio", 0.85, "连续排名数值（DNS/热度排名，是水平量不是分位标签）",
     r"(^|_)rank$|_rank$"),
    ("level_ratio", 0.90, "金额/规模/比率（水平量）",
     r"(_amount|_total$|^total_|total_|_size$|capital|_value|_price|_sales|revenue|profit|"
     r"_salary|bonus|compensation|_fund|_nav|_assets|margin|ratio$|yield|_eps|_cost|_expense|"
     r"_debt|_cash|_equity|_income|_margin)"),
    ("level_ratio", 0.85, "时长/年龄（水平量）",
     r"(age_months|age_years|_months$|_years$|_days$|_duration)"),
]


# (concept, conf, why, 匹配函数) —— 2026-10-24 新增：8 问机制概念（与 form 正交）
# 一个字段可同时有 form 和 concept（例：form=level_ratio 且 concept=structure）。
# 顺序即优先级，最多取 2 个（沿用 brain-data-feature-engineering skill 的概念预算）。
CONCEPT_RULES = [
    # ② 变化（速率/加速度/修正）：差分族
    ("change", 0.92, "变化/修正/超预期/动量语义",
     r"(change|revision|surprise|_delta|growth|_qoq|_yoy|momentum|trend|_diff$|chg|"
     r"_increase|_decrease|_est_change|estimate_change)"),
    # ③ 异常（偏离幅度与显著性）：zscore / scale / 事件衰减
    ("anomaly", 0.90, "波动/离散/偏离/残差语义",
     r"(volatility|variance|std_?dev|deviation|dispersion|_spread|beta|_resid|"
     r"zscore|z-score|outlier|_range$|_max$|_min$|_upper|_lower)"),
    # ⑥ 累积（记忆/衰减）：双窗 + 时序 + 事件衰减
    ("accumulation", 0.88, "均值/累计/窗口/历史语义",
     r"(moving_?average|_avg$|_average|_mean$|cumulative|trailing|_window|historical|"
     r"_ma\d|sma|ema|_decay)"),
    # ⑤ 结构（构成/比例/集中度）：分位 + 组内离散
    ("structure", 0.88, "集中度/构成/占比/规模语义",
     r"(concentration|hhi|herfindahl|share_of|proportion|composition|breakdown|_mix|"
     r"market_?value|capitali[sz]ation|_shares|participants|ownership|_trades|"
     r"_order|_participant)"),
    # ⑦ 相对（排名/归一/横截面位置）
    ("relative", 0.85, "排名/分位/横截面相对位置语义",
     r"((^|_)rank$|_rank$|percentile|quartile|decile|_pct|relative|vs_peers|"
     r"cross_?sectional|_style|_factor)"),
    # ⑧ 本质（第一性：情绪/文本/预测/模型输出）
    ("essence", 0.82, "情绪/文本/预测/模型输出语义",
     r"(sentiment|_tone|news|article|_text|_words|_headline|transcript|likelihood|"
     r"probability|forecast|prediction|_estimate|expected|model_output|_domains|"
     r"_inferess|_nlp)"),
    # ① 不变（稳定性/持续/评分/指标）
    ("invariance", 0.80, "稳定性/持续/评分/指标语义",
     r"(stability|stable|persistent|consistent|_score$|_rating$|_grade$|_index$|"
     r"_metric|_level|_value$)"),
]


def classify_concept(field, desc, max_n=2):
    """字段 → 机制概念列表（≤max_n）。与 classify() 的 form 判据正交。"""
    fn = (field or "").lower()
    dc = (desc or "").lower()
    hits = []
    for con, conf, why, pat in CONCEPT_RULES:
        if re.search(pat, fn) or re.search(pat, dc):
            hits.append((con, conf, why))
        if len(hits) >= max_n:
            break
    return hits


def classify(field, desc):
    """字段名与描述分开匹配：名字里的 `_nip$` 这类锚定模式不能被描述文字污染。"""
    fn = (field or "").lower()
    dc = (desc or "").lower()
    for form, conf, why, pat in RULES:
        if re.search(pat, fn) or re.search(pat, dc):
            return form, conf, why
    return "other", 0.3, "未能确定语义，退回正则/全交叉"


def main():
    con = db_connect(DB, readonly=True)
    con.row_factory = sqlite3.Row
    q = """SELECT d.name ds, COALESCE(d.category,'') cat, f.field_name, f.field_type,
                  f.coverage, COALESCE(f.description,'') descr
           FROM fields f JOIN datasets d ON f.dataset_id=d.id
           JOIN regions r ON d.region_id=r.id
           WHERE r.name='EUR' AND f.coverage>=0.3 AND f.field_type!='GROUP'"""
    rows = [dict(x) for x in con.execute(q)]
    out = {}
    for r in rows:
        form, conf, why = classify(r["field_name"], r["descr"])
        cons = classify_concept(r["field_name"], r["descr"])
        rec = {"form": form, "conf": conf, "why": why}
        if cons:
            rec["concept"] = [c for c, _cf, _w in cons]
            rec["concept_conf"] = min(_cf for _c, _cf, _w in cons)
            rec["concept_why"] = " | ".join(f"{c}:{w}" for c, _cf, w in cons)
        out[f"{r['ds']}.{r['field_name']}"] = rec

    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    import collections
    c = collections.Counter(v["form"] for v in out.values())
    print(f"生成 {len(out)} 条打标 → {OUT}")
    for k, n in c.most_common():
        print(f"  {k:16s} {n}")
    print(f"  其中 conf>=0.7（会被流水线采信）：{sum(1 for v in out.values() if v['conf'] >= 0.7)}")
    cc = collections.Counter()
    for v in out.values():
        for k in (v.get("concept") or []):
            cc[k] += 1
    print(f"  带机制概念的字段：{sum(1 for v in out.values() if v.get('concept'))}"
          f"（概念置信度>=0.7：{sum(1 for v in out.values() if v.get('concept_conf', 0) >= 0.7)}）")
    for k, n in cc.most_common():
        print(f"    {k:14s} {n}")


if __name__ == "__main__":
    main()
