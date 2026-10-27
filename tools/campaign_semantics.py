# -*- coding: utf-8 -*-
"""campaign_semantics.py — 全模板战役的**字段语义层**（2026-10-24 从 full_template_campaign.py 拆出）

职责边界（单一职责）：
  · 字段形态分类（field_form / FORM_FAMILIES）
  · 字段透明度分档（field_tier / BLACKBOX_*）
  · 收益来源暴露（field_exposure_hint / FAMILY_EXPOSURE）
  · 机制概念 8 问（field_concepts / CONCEPT_FAMILIES）
  · preprocessing 受控词表（parse/load/apply）
  · 选池判据（is_virgin / exposure_profile / classify_desc）

**全是纯函数或本地 DB 读，无平台 IO、无仿真、无落盘** ⇒ 可独立单测，
也可被 skill 脚本（如 wq-brain-ra-deu/scripts/dataset_scan.py）与分析脚本复用，
消除「同一逻辑两处实现」的第二事实源。

上游/下游：被 full_template_campaign.build_exprs / all_datasets 导入；
数据源 = data/wqb.db 的 fields/datasets 表 + cache/field_form_llm.json + cache/field_form_overrides.json。

⚠ 可变模块级状态（跨模块共享同一对象，import 时按引用传递，勿重新赋值）：
  FORM_EVIDENCE  —— field_form() 写入的判定证据（print_form_audit 读）
  EXPR_EXPOSURE —— build_exprs() 写入的 表达式→暴露 映射
"""
import collections
import json
import os
import re
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- 数据集与字段

LIT_CACHE = os.path.join(ROOT, "cache", "lit_categories.json")
LIT_THRESHOLD = 3   # 铁律：同一 category 下我方已提交 > 3 个 alpha ⇒ 该 category「已点亮」，不优先

# 2026-10-23 用户指令「算力全部转到流水线 + 优先未点亮」的落地：
# 平台 alpha_count 是**全站**该数据集已出 alpha 数（本地库与平台实测完全一致）。
# alpha_count 极低 + value_score 高的集 = 真正的处女地，其低覆盖是被 cov>=0.8 门槛挡住的
# 主要原因（equity_forum_data VS6.0/aCnt0/cov0.41、stock_cluster_dl VS6.0/aCnt1/cov0.46 …）。
# ⇒ 对这类集放宽覆盖门槛并提到队首，比按 category 轮转更能挖到新东西。
VIRGIN_AC = 10      # alpha_count <= 10 视为「几乎没人挖」
VIRGIN_VS = 5.0     # 且平台 value_score >= 5（平台自带的信号价值评分）
VIRGIN_MIN_COV = 0.35   # 处女地覆盖门槛（常规 0.8）


# 字段预算 / 探针常量（被 build_exprs、select_fields、exposure_profile 三方共用 ⇒ 归语义层）
POSTPROC_Q = (0.8, 0.85, 0.9)
PER_DIM = 2            # 每维代表字段数（2026-10-22 用户裁决 3→2，表达式量约 -30%，提速 ~1.7x）
MIN_FIELDS_TOTAL = 3   # 单集最少字段数，低于此判 SKIPPED_TOO_FEW_FIELDS
# 2026-10-23 提速（用户批准 A 方案）：每集表达式预算上限。
# 实测 news38 19 字段×12 族=72 条 → 8 批 → 约 2h/集；146 集需 6-12 天。
FULL_FIELD_CAP = 8     # 全族字段上限（按「每维先各留 1 + 覆盖率补满」挑选）


def is_virgin(r):
    return (r.get("ac") or 0) <= VIRGIN_AC and (r.get("vs") or 0) >= VIRGIN_VS

def exposure_profile(con, ds, field_min_cov=0.35, cap=None):
    """数据集级暴露画像（2026-10-24）：(暴露种数, 分布 dict, 主导占比)。

    回答「这个集能贡献几种收益来源」。**单暴露集与既有同源 alpha 必然高相关**，
    S/2Y 再高也难独立过 prod —— 这是选池的第二维，与 alpha_count（开采度）正交。
    只读本地 fields 表，不调平台。

    ⚠ 两个坑（2026-10-24 修）：
      ① 覆盖率阈值要**自适应**：低覆盖处女地（cov 0.20–0.25）在 0.35 下取不到字段，
         会返回 0 种暴露被误判成「最差」，实际是「未知」；
      ② 必须 `ORDER BY coverage DESC` 再截断：无 ORDER BY 时按表序取前 N 个是有偏样本。
    """
    cap = cap or FULL_FIELD_CAP * 2
    q = """SELECT f.field_name, COALESCE(f.description,'') AS descr
           FROM fields f JOIN datasets d ON f.dataset_id=d.id JOIN regions r ON d.region_id=r.id
           WHERE r.name='EUR' AND d.name=? AND f.coverage>=? AND f.field_type!='GROUP'
           ORDER BY f.coverage DESC LIMIT ?"""
    rows = []
    for mc in (field_min_cov, 0.1, 0.0):
        rows = [dict(x) for x in con.execute(q, (ds, mc, cap))]
        if len(rows) >= 3:
            break
    if not rows:
        return (0, {}, 0.0)
    c = collections.Counter(field_exposure_hint(r) for r in rows)
    tot = sum(c.values())
    return (len(c), dict(c), (c.most_common(1)[0][1] / tot) if tot else 0.0)


def all_datasets(con, only=None, limit=None, priority_cats=None, lit_cats=None,
                 skip_lit=False):
    q = """SELECT dataset, category, n_fields, n_untested, avg_field_coverage cov,
                  value_score vs, alpha_count ac
           FROM dataset_profile WHERE region='EUR' AND n_fields>=3
           ORDER BY COALESCE(value_score,0)*COALESCE(avg_field_coverage,0)
                          *CAST(n_untested AS REAL)/NULLIF(n_fields,1)
                          /(1.0+COALESCE(alpha_count,0)/1000.0) DESC"""
    rows = [dict(r) for r in con.execute(q)]
    if only:
        rows = [r for r in rows if r["dataset"] in set(only)]
    lit = {c.upper() for c in (lit_cats or {})}
    if skip_lit and lit:
        before = len(rows)
        rows = [r for r in rows if (r["category"] or "").upper() not in lit]
        print(f"[lit] 跳过已点亮类别 {sorted(lit)}：{before} → {len(rows)} 个集")
    if priority_cats or lit:
        # 铁律排序：未点亮类别一律优先于已点亮类别；再「零开采处女地」优先；
        # 同层内按 --priority-cats 顺序，**再按暴露多样性**，最后按 EV。
        # 暴露多样性 = 该集能贡献几种收益来源（2026-10-24 接入选池）：
        # 单暴露集与既有同源 alpha 必然高相关，是 prod 相关性结构性风险，压到多暴露集之后。
        order = {c.upper(): i for i, c in enumerate(priority_cats or [])}
        for r in rows:
            r["n_expo"], r["expo_dist"], r["expo_dom"] = exposure_profile(con, r["dataset"])
        # n_expo == 0 = 「未知」（字段取不到），不是「零多样性」⇒ 按中位数 1.5 排，不罚
        rows.sort(key=lambda r: (1 if (r["category"] or "").upper() in lit else 0,
                                 0 if is_virgin(r) else 1,
                                 order.get((r["category"] or "").upper(), 99),
                                 -(r["n_expo"] if r["n_expo"] else 1.5),
                                 -(r["vs"] or 0) * (r["cov"] or 0)))
        hit = [r["dataset"] for r in rows if (r["category"] or "").upper() in order]
        print(f"[priority] 类别 {priority_cats} 命中 {len(hit)} 个集: {hit}")
        virgin = [r["dataset"] for r in rows if is_virgin(r)]
        print(f"[virgin] 零开采优先（aCnt<={VIRGIN_AC} 且 VS>={VIRGIN_VS}）{len(virgin)} 个集: {virgin}")
        poor = [(r["dataset"], r["n_expo"]) for r in rows if 0 < r["n_expo"] <= 2]
        if poor:
            print(f"[expo] 低多样性（<=2 种暴露，prod 相关性风险，已压到同类多暴露集之后）: {poor}")
    if limit:
        rows = rows[:limit]
    return rows


PLAT_CACHE = {}

NAME_META = ("symbol", "isin", "timestamp", "status", "exchange", "quarter",
             "passcode", "url", "link", "_currency", "time_zone", "company_name",
             "wqreceive", "board_of_directors", "split_ratio", "div_freq",
             "time_of_day", "transcript", "conferencecall", "goto_broadcast",
             "mtg_type", "fiscal_year", "_split", "ed_fiscal",
             # 2026-10-23（sentiment26 实战补充）：域名后缀 / 落库时间戳 也是元数据，
             # 旧表没拦住 ⇒ dltcc、wq_pit 混进了「经济字段」，白占代表位
             "dltcc", "tld", "wq_pit", "append_time", "point_in_time")


def is_name_metadata(name):
    n = (name or "").lower()
    return any(k in n for k in NAME_META)


def classify_desc(desc, name=""):
    """按平台 description 做语义分组（用户明令 2026-10-22：先分组再挑代表字段）。

    `field_semantic_type` 表里大量字段是 unknown（earnings6 66 个里 53 个），
    旧逻辑把它们并成一个 unknown 组 ⇒ 代表字段按覆盖率随便挑，挑进 ticker/URL/timestamp 这类垃圾。
    这里用 description 关键词兜底分类，并显式识别 metadata（应整组丢弃，不参与代表挑选）。
    """
    d = (desc or "").lower()
    n = (name or "").lower()
    if is_name_metadata(n):
        return "metadata"
    # 语义表已判为标识符/时间元数据的，也归元数据
    # 元数据：标识符 / 文本链接 / 时间戳 / 状态标志 / 标签，无经济含义
    META = ("ticker symbol", "name of the company", "website link", "link to", "the link",
            "passcode", "phone number", "time zone", "letter “q”", 'letter "q"',
            "possible values", "denotes whether", "unique security identifier", "isin",
            "timestamp", "time of day", "currency", "payment frequency", "fiscal quarter",
            "indicator for the", "quarter or half year", "transcript applies",
            "conference call", "split parameters", "status", "company name",
            "the exchange the stock is traded", "identifies whether",
            "time when", "update time", "time of the", "ingestion")
    for k in META:
        if k in d:
            return "metadata"
    if "dividend" in d:
        return "dividend"
    if "preliminary" in d:
        return "eps_preliminary"
    if "estimize" in d or "estimate" in d:
        return "eps_estimate"
    if "change in earnings per share" in d:
        return "eps_change"
    if "earnings per share" in d or " eps" in " " + d or "eps " in d:
        return "eps_actual"
    if "earnings date" in d or "scheduled" in d:
        return "event_date"
    if any(k in d for k in ("amount", "value", "percent", "ratio", "score", "level")):
        return "numeric_other"
    return "unknown"

# 字段形态分类 → 模板族白名单（2026-10-23：模板选择此前是「全交叉」，语义只用来选字段、不参与配对）
FORM_FAMILIES = {
    # 变化/修正量：记忆铁律「只有变化量/修正量有信号」⇒ 差分族必跑，水平族不浪费
    "change":          {"d1_rk", "d2_rk", "ed_rk", "pp", "lvl_rk"},
    # 水平量/比率：差分族常无信号 ⇒ 跳过 d1/d2
    "level_ratio":     {"lvl_rk", "lvl_zs", "lvl_tr", "lvl_sc", "lvl_qt", "pp", "dw"},
    # 事件日期：做时序平滑无意义 ⇒ 只留事件族 + 1 条基线
    "event_date":      {"ed_rk", "lvl_rk"},
    # 计数/覆盖
    "count":           {"lvl_rk", "dw", "pp"},
    # 离散评分：禁 signed_power / tail 这类隐含连续排序的变体
    "discrete_rating": {"lvl_rk", "lvl_zs", "lvl_qt"},
    # 非经济字段（文本、时间戳、顺序索引、分类编码）：LLM 打标判出来后直接跳过，0 条表达式
    "skip":            set(),
    "other":           None,          # 未知形态：保持全交叉（不冒险丢族）
}

# 只有这些类别开「稀疏门控」一等模板（pp=双窗门控 / tl=单窗 tail 门控）；sentiment26 实证 tl 最强
GATED_CATS = {"SENTIMENT", "SOCIALMEDIA"}
GATE_Q = 0.85

# ============================================================
# 2026-10-24 三项落地（借鉴 brain-data-feature-engineering skill）
#   ① 字段透明度分档  ② Expected Exposure 第二维  ③ preprocessing 受控词表并真正执行
# 实证依据见 .workbuddy/memory/2026-10-23.md「00:30 skill 拆解」与「00:20 形态×模板矩阵」。
# ============================================================

# ---- ① 字段透明度分档（skill 第 0 步）----
# 裁决序：黑盒 > 半透明 > 透明（宁可多分析，也不让形态分类器在黑盒集上假装懂）。
# 病因：实测矩阵里 `other` 形态样本量 37–66/模板，而具体形态只有 5–30
#       ⇒ 形态分类器在黑盒集（other*/model*/ai_*）上大面积失效，却仍在做「减法」。
_BLACKBOX_NAME_PREFIX = ("other", "model", "ai_", "ml_", "dl_", "mmp_", "techindi")
_TRANSPARENT_CATS = {"FUNDAMENTAL", "ANALYST", "EARNINGS", "INSIDERS",
                     "SHORTINTEREST", "INSTITUTIONS", "MACRO"}
_FIN_VOCAB = ("eps", "revenue", "ebitda", "estimate", "revision", "holder", "margin",
              "roe", "roa", "cash", "debt", "dividend", "profit", "earnings", "sales",
              "asset", "liability", "equity", "guidance", "payout", "yield", "book")
# 黑盒集不信形态分类，改用「无先验多样族」——按 1,364 条实测矩阵中 `other` 形态的 maxS 取前 7：
#   lvl_rk 1.62 > pp 1.60 > ed_rk 1.53 > lvl_tr 1.49 > lvl_qt 1.44 > lvl_sc 1.43 > dw 1.32
#   （被剔除的 d2_rk 0.73 / dsp_rk 1.13 / ir_pl 1.14 / d1_* 1.00 实测最弱）
# 附带效果：黑盒字段表达式量 12 → 8，成本 −33%，且覆盖 value/momentum/event/sentiment/lowvol 五种暴露。
BLACKBOX_FAMILIES = {"lvl_rk", "lvl_zs", "lvl_qt", "lvl_tr", "lvl_sc", "dw", "pp"}


def field_tier(r, cat=None, ds=None):
    """字段透明度分档 → blackbox / semi / transparent。

    2026-10-24 补充数据集级判据：只按字段名前缀会漏 —— `other250` 的字段叫
    `oth250_price_range_max`、`news_sentiment_dl` 的叫 `avg_syllables_per_word_inferess`，
    都带语义词，实测全落 semi。**数据集名前缀才是黑盒的可靠信号**（other*/model*/ai_*/ml_*）。
    """
    name = (r.get("field_name") or "").lower()
    desc = clean_desc(r.get("descr")) or ""
    dsn = (ds or "").lower()
    if any(dsn.startswith(p) for p in _BLACKBOX_NAME_PREFIX):
        return "blackbox"
    if any(name.startswith(p) for p in _BLACKBOX_NAME_PREFIX):
        return "blackbox"
    if not re.search(r"[a-z]{4,}", name):        # 字段名无语义（q1s3_x87 之类）
        return "blackbox"
    if len(desc) < 30:                            # 描述太短，语义不可信
        return "blackbox"
    if (cat or "").upper() in _TRANSPARENT_CATS and any(v in name for v in _FIN_VOCAB):
        return "transparent"
    if len(desc) >= 120:
        return "transparent"
    return "semi"


# ---- ② Expected Exposure 受控词表（skill 第 4 步的 **Expected Exposure** 行）----
# ⚠ 2026-10-24 修正：第一版把 exposure 建在**模板族**上（`FAMILY_EXPOSURE`），那是错的——
#   `ts_rank` 是归一化方法，不是收益来源。skill 的 Expected Exposure 从**概念/机制**推出。
#   正确规则：**字段语义优先**，模板只在字段本身无特定暴露（纯水平量）时才决定暴露。
FAMILY_EXPOSURE = {          # 仅作「字段无特定暴露时」的兜底
    "lvl_rk": "value", "lvl_zs": "value", "lvl_qt": "value", "lvl_tr": "value",
    "lvl_sc": "lowvol",
    "d1_rk": "momentum", "d1_va": "momentum", "d2_rk": "momentum", "dw": "momentum",
    "ed_rk": "event", "ir_pl": "risk", "dsp_rk": "liquidity",
    "pp": "sentiment", "tl": "sentiment",
}
# 字段语义 → 暴露关键词（顺序即优先级，先命中先返回；对标 skill 的 _EXPOSURE_KEYWORDS）
_EXPOSURE_KW = (
    ("sentiment", ("sentiment", "emotion", "opinion", "text", "nlp", "news", "headline",
                   "transcript", "linguistic", "word", "sentence", "readability",
                   "complexity", "inferess", "topic", "subjectivity", "polarity")),
    ("growth",    ("estimate", "revision", "forecast", "guidance", "consensus", "surprise")),
    ("quality",   ("rating", "grade", "quality", "governance", "esg", "score")),
    ("flow",      ("holding", "institution", "insider", "ownership", "buy", "sell",
                   "transaction", "filing")),
    ("liquidity", ("volume", "turnover", "trade", "liquidity", "bid", "ask", "spread",
                   "imbalance", "order book")),
    ("risk",      ("volatility", "beta", "risk", "drawdown", "var", "correlation",
                   "variance", "std dev", "stddev")),
    ("momentum",  ("momentum", "trend", "change", "delta", "growth")),
    ("value",     ("ratio", "yield", "margin", "book", "price", "valuation", "per share")),
)


def field_exposure_hint(r, cat=None):
    """字段语义 → 收益来源暴露。**优先于模板族**（模板只作兜底）。

    这是 skill 的 Expected Exposure 推导方式：从字段「测的是什么」出发，
    而不是从套了什么归一化算子出发。news_sentiment_dl 的 `*_inferess`
    文本字段因此正确判为 sentiment，而非被 `ts_rank` 带成 value。
    """
    name = (r.get("field_name") or "").lower()
    desc = clean_desc(r.get("descr")) or ""
    t = f"{name} {desc}".lower()
    for expo, kws in _EXPOSURE_KW:
        if any(k in t for k in kws):
            return expo
    return "value"          # 无特定暴露 ⇒ 交回模板族决定


EXPOSURE_VOCAB = ("momentum", "reversal", "value", "quality", "growth", "lowvol",
                  "liquidity", "sentiment", "flow", "risk", "event", "other")
# 表达式 → 暴露（build_exprs 填充，供数据集末统计；不改 (tpl, expr) 元组契约）
EXPR_EXPOSURE = {}

# ============================================================
# 2026-10-24 机制/概念路径（brain-data-feature-engineering skill 第 3 步）
#   8 问 → 机制概念 → 模板族。这是比 FORM_FAMILIES（7 类粗形态）细一个量级的
#   **机制驱动**选路：黑盒集与 form=other 的字段不再吃固定先验，改吃概念推导。
#   预算（沿用 skill）：每字段 ≤2 个概念；每概念贡献的族去做重，总量仍受
#   FULL_FIELD_CAP × 8 的表达式预算约束。
# ============================================================
CONCEPT_FAMILIES = {
    # ① 不变（稳定性）：水平量 + 相对自身历史位置 + 双窗确认
    "invariance":  {"lvl_rk", "lvl_tr", "dw"},
    # ② 变化（速率/加速度/波动）：差分族
    "change":      {"d1_rk", "d2_rk", "d1_va"},
    # ③ 异常（偏离幅度与显著性）：zscore / scale / 事件衰减
    "anomaly":     {"lvl_zs", "lvl_sc", "ed_rk"},
    # ④ 交互（条件/分组/同源离散）：组内离散度 + 分位
    "interaction": {"dsp_rk", "lvl_qt"},
    # ⑤ 结构（构成/比例）：分位 + 离散
    "structure":   {"lvl_qt", "dsp_rk"},
    # ⑥ 累积（记忆/衰减）：双窗 + 时序 + 事件衰减
    "accumulation": {"dw", "lvl_tr", "ed_rk"},
    # ⑦ 相对（排名/归一/相对位置）
    "relative":    {"lvl_rk", "lvl_tr", "dw"},
    # ⑧ 本质（第一性原理）：基线 + 变化 + 双窗
    "essence":     {"lvl_rk", "d1_rk", "dw"},
}
# 概念 → 中文名（汇报用）
CONCEPT_ZH = {
    "invariance": "不变/稳定性", "change": "变化/速率", "anomaly": "异常/偏离",
    "interaction": "交互/离散", "structure": "结构/构成", "accumulation": "累积/衰减",
    "relative": "相对/位置", "essence": "本质/第一性",
}
# description 关键词 → 概念（顺序即优先级；先命中先返回，最多取 2 个）。
# 2026-10-24 用 6 个集 700+ 字段的 description 高频实词校准过（见当条记忆），
# 补入 article/words/sentiment/news/text/number/metric/concentration/participants/
# trades/market/estimated/regression/ranked 等实测高频词 —— 初版只凭想象列词，
# 命中率仅 ~30%，校准后见下。
_CONCEPT_KW = (
    ("change", ("change", "delta", "growth", "revision", "surprise", "momentum",
                "trend", "increase", "decrease", "qoq", "yoy", "w/w", "m/m",
                "estimated", "forward", "estimate")),
    ("anomaly", ("volatility", "variance", "std dev", "stddev", "deviation",
                 "z-score", "outlier", "dispersion", "spread", "beta", "regression",
                 "residual", "range", "lower", "upper", "maximum", "minimum")),
    ("accumulation", ("cumulative", "accumulated", "moving average", "decay",
                      "memory", "trailing", "average", "mean", "sum of", "window",
                      "historical", "time series")),
    ("structure", ("concentration", "hhi", "herfindahl", "share of", "proportion",
                   "composition", "breakdown", "ratio of", "mix", "market value",
                   "capitalization", "participants", "trades", "ownership",
                   "order", "index")),
    ("interaction", ("correlation", "co-movement", "versus", "relative to",
                     "compared", "among", "across", "dispersion")),
    ("relative", ("rank", "ranked", "percentile", "quartile", "decile", "position",
                  "relative", "vs peers", "cross-sectional", "style", "factor")),
    ("invariance", ("stability", "stable", "persistent", "consistent", "level of",
                    "level", "score", "rating", "metric", "custom", "derived",
                    "output", "analysis", "analytics", "value")),
    ("essence", ("likelihood", "probability", "expected", "forecast",
                 "prediction", "model output", "signal", "sentiment", "news",
                 "article", "text", "words", "domains", "earnings", "dividend")),
)


def field_concepts(r, cat=None, ds=None, max_n=2):
    """字段 → 机制概念列表（≤max_n 个）。

    三级推导（成本递增、可靠性递增）：
      ① LLM 打标 `cache/field_form_llm.json` 的 `concept` 字段（conf>=0.7 采信）
         —— **尚未生成**，接口先留好；这是把关键词命中率从 36% 提到接近满配的正路。
      ② 关键词 `_CONCEPT_KW`（已用 6 集 700+ 字段高频实词校准，实测命中 ~36%）
      ③ 都不命中 ⇒ [] ⇒ 调用方回退 FORM_FAMILIES / BLACKBOX_FAMILIES

    ⚠ 关键词法是**止损稿**，不是 skill 的原意。skill 第 3 步是逐字段人工 8 问，
    批量化的等价物只能是 LLM 打标，不是正则。
    """
    name = r.get("field_name") or ""
    # ① LLM/规则打标（concept 字段，2026-10-24 起由 gen_llm_field_tags.py 物化）
    if ds:
        rec = _load_llm_tags().get(f"{ds}.{name}")
        if rec and float(rec.get("concept_conf") or 0) >= LLM_CONF_MIN:
            cs = rec.get("concept") or rec.get("concepts")
            if isinstance(cs, str):
                cs = [c.strip() for c in cs.replace(",", "+").split("+") if c.strip()]
            if isinstance(cs, (list, tuple)):
                cs = [c for c in cs if c in CONCEPT_FAMILIES]
                if cs:
                    return cs[:max_n]
    # ② 关键词
    desc = clean_desc(r.get("descr")) or ""
    t = f"{name.lower()} {desc}".lower()
    hits = []
    for con, kws in _CONCEPT_KW:
        if any(k in t for k in kws):
            hits.append(con)
        if len(hits) >= max_n:
            break
    return hits


def concept_families(r, cat=None, ds=None):
    """字段概念 → 模板族并集（去重）；无概念返回 None。"""
    cs = field_concepts(r, cat, ds)
    if not cs:
        return None
    fam = set()
    for c in cs:
        fam |= CONCEPT_FAMILIES.get(c, set())
    return fam or None


# ---- ③ preprocessing 受控词表（skill 的 preprocessing，但改成**可执行**）----
# 断点事实（2026-10-24 grep 证实）：S1 台账的 preprocessing 写了没人执行，
# 且 939 条 s1_* 里仅 90 条带该字段、大半是节点自动生成的同一句通用三件套，
# 真正逐字段的写成 "backfill+rank" / "sparse_event (insider filings; …)" 这类**自然语言**。
# ⇒ 契约即代码：只认受控词表（可 `+` 连接按序套），自由文本一律不采信。
PP_VOCAB = ("backfill", "rank", "zscore", "vec_max", "vec_avg", "group_neutralize")


def parse_preprocessing(v):
    """台账 preprocessing 值 → 受控词表序列；不合规（自由文本）返回 None。"""
    if not isinstance(v, str):
        return None
    toks = [t.strip().lower() for t in v.split("+") if t.strip()]
    if not toks or any(t not in PP_VOCAB for t in toks):
        return None
    return toks


def load_s1_preprocessing(con, ds, delay=1, region="EUR"):
    """本地读 S1 台账（data/wqb.db::ledger_kv）——后台进程可直接 sqlite，不需要 MCP。"""
    try:
        row = con.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?",
                          (region, f"s1_{ds}_d{delay}")).fetchone()
        if not row:
            return {}
        pp = (json.loads(row[0]) or {}).get("preprocessing") or {}
        out = {}
        for k, v in pp.items():
            toks = parse_preprocessing(v)
            if toks:
                out[k] = toks
        return out
    except Exception:
        return {}


def apply_preprocessing(atom, toks, raw, BF, ZW, l2=None):
    """按受控词表给「字段原子表达式」套预处理（有序，带去重 guard）。

    `l2` = 该模板族自己的 L2 归一化（rk/zs/qt/tr/sc）。传入时跳过**重复归一**：
    预处理说 rank 而模板本身就是 rank ⇒ rank(rank(x)) 单调等价，纯浪费还让表达式难读。
    """
    x = atom
    for t in toks:
        if t == "backfill" and "ts_backfill(" not in x:
            x = f"ts_backfill({x}, {BF})"
        elif t == "rank" and l2 != "rk" and not x.startswith("rank("):
            x = f"rank({x})"
        elif t == "zscore" and l2 != "zs" and "ts_zscore(" not in x:
            x = f"ts_zscore({x}, {ZW})"
        elif t == "group_neutralize" and "group_neutralize(" not in x:
            x = f"group_neutralize({x}, subindustry)"
        elif t in ("vec_max", "vec_avg") and raw not in x:
            x = f"{t}({x})"
    return x


# description 里的样板噪声（2026-10-23 实测：几乎每个字段都带 "... on the observation date"，
# 直接用 "date" 关键词会把整集误判成事件日期）
_DESC_NOISE = (
    "on the observation date", "on the observation", "at the observation",
    "on that date", "on data_date", "on the data date", "as of the",
    "for the issuer", "of the issuer", "the issuer’s", "the issuer's",
    "for a given", "in the dataset", "this field", "values are", "is calculated as",
)


def clean_desc(d):
    """清洗 description 的样板噪声，留下真正描述经济含义的部分。"""
    t = (d or "").lower()
    for nz in _DESC_NOISE:
        t = t.replace(nz, " ")
    return re.sub(r"\s+", " ", t).strip()


_OVR_CACHE = None


def _load_form_overrides():
    """人工覆盖表（cache/field_form_overrides.json）：{"数据集.字段": "形态"}。"""
    global _OVR_CACHE
    if _OVR_CACHE is not None:
        return _OVR_CACHE
    try:
        _OVR_CACHE = json.load(open(os.path.join(ROOT, "cache", "field_form_overrides.json"),
                                   encoding="utf-8"))
    except Exception:
        _OVR_CACHE = {}
    return _OVR_CACHE


FORM_EVIDENCE = {}   # field_name -> (form, 命中关键词)，用于审计打印

# ---- LLM 离线打标（2026-10-23）：cache/field_form_llm.json，按 mtime 热加载 ----
LLM_TAG_FILE = os.path.join(ROOT, "cache", "field_form_llm.json")
LLM_CONF_MIN = 0.7          # 低于此置信度不采信，退回正则
_LLM_CACHE = {"mtime": None, "data": {}}


def _load_llm_tags():
    """{"数据集.字段": {"form": "...", "conf": 0.0-1.0, "why": "..."}}，写文件后无需重启即生效。"""
    try:
        mt = os.path.getmtime(LLM_TAG_FILE)
    except OSError:
        return {}
    if _LLM_CACHE["mtime"] != mt:
        try:
            _LLM_CACHE["data"] = json.load(open(LLM_TAG_FILE, encoding="utf-8"))
            _LLM_CACHE["mtime"] = mt
            print(f"[llm-tags] 载入 {len(_LLM_CACHE['data'])} 条字段打标")
        except Exception as e:
            print(f"[llm-tags] 载入失败：{type(e).__name__}: {e}")
            return _LLM_CACHE["data"]
    return _LLM_CACHE["data"]


def field_form(r, ds=None):
    """字段形态打标：**以 description 语义为主、字段名为辅**。

    设计（2026-10-23 二次修正）：
      ① 先清洗样板噪声（"on the observation date" 这类）；
      ② 按语义**强模式**判定，而不是裸关键词 —— 例如 "date" 单独出现不算事件字段，
         必须是 "date of / announcement date / days since" 这类真正指向日期的表述；
         同理排除裸 "score"（很多连续复合分也叫 score），只认 rank/percentile/cutpoint/threshold；
      ③ 字段名只作补充证据（如 `_ed_216`、`next_ed`、`_change`）；
      ④ 命中不了就归 other ⇒ 保持全交叉（宁多跑，不误杀族）；
      ⑤ 支持 `cache/field_form_overrides.json` 人工覆盖：{"数据集.字段": "形态"}。
    """
    name = r.get("field_name") or ""
    ov = _load_form_overrides()
    if ds and f"{ds}.{name}" in ov:
        FORM_EVIDENCE[name] = (ov[f"{ds}.{name}"], "override")
        return ov[f"{ds}.{name}"]

    llm = _load_llm_tags()
    rec = llm.get(f"{ds}.{name}") if ds else None
    if rec and float(rec.get("conf") or 0) >= LLM_CONF_MIN and rec.get("form"):
        FORM_EVIDENCE[name] = (rec["form"], f"llm:{float(rec['conf']):.2f}")
        return rec["form"]

    n = name.lower()
    cd = clean_desc(r.get("descr"))
    t = f"{cd} {n}"

    def hit(form, ev):
        FORM_EVIDENCE[name] = (form, ev)
        return form

    # ① 事件日期：只认真正指向日期的强模式
    m = re.search(r"(date of|announcement date|next earnings|earnings date|report date|"
                  r"release date|days (since|until|to)|fiscal (year|quarter) end|calendar)", cd)
    if m or re.search(r"(^|_)(next_ed|date)(_|$)", n) or re.search(r"_ed_?\d*$", n):
        return hit("event_date", (m.group(0) if m else "name-pattern")[:28])

    # ② 变化/修正量（记忆铁律：只有变化量/修正量常有信号）
    m = re.search(r"\b(change|changes|changed|revision|revised|surprise|delta|growth|"
                  r"increase|decrease|qoq|yoy|momentum)\b", cd)
    if m or any(k in n for k in ("change", "revision", "delta", "growth", "surprise", "chg")):
        return hit("change", (m.group(0) if m else "name-pattern")[:28])

    # ③ 计数/覆盖
    m = re.search(r"\b(number of|count of|total number|how many|total count)\b", cd)
    if m or re.search(r"(count|num_|_num|domains)", n):
        return hit("count", (m.group(0) if m else "name-pattern")[:28])

    # ④ 离散评分：只认真正的等级/分位语义（裸 "score" 不算——很多连续复合分也叫 score）
    #   ⚠ 裸 "rank" 不能要：sentiment26 的 "domain rank distribution"（偏度/峰度）与
    #   "attention breadth score ... top-ranked domains"（连续复合分）都会误判成评分型。
    m = re.search(r"\b(cutpoint|threshold|percentile|quartile|decile|grade|rating|tier)\b", cd)
    if m or re.search(r"(^|_)(rank|ranking|pct|percentile|rating|grade)(_|$)", n):
        return hit("discrete_rating", (m.group(0) if m else "name-pattern")[:28])

    # ⑤ 水平量/比率（差分族在此类字段上常无信号，可省配额）
    m = re.search(r"\b(ratio|percentage|yield|margin|return|price|average|mean|median|"
                  r"level|factor|per share|book value|volatility|beta)\b", cd)
    if m:
        return hit("level_ratio", m.group(0)[:28])

    FORM_EVIDENCE[name] = ("other", "-")
    return "other"


def print_form_audit(ds, sel, limit=14):
    """打印字段形态判定 + 证据，便于人工抽查误判。"""
    lines = []
    for r in sel:
        f = r.get("form") or field_form(r, ds)
        r["form"] = f
        ev = FORM_EVIDENCE.get(r["field_name"], ("", "-"))[1]
        lines.append(f"     {r['field_name'][:40]:42s} {f:16s} ← {ev}")
    print(f"  [form] {ds}: 形态判定 {len(lines)} 个字段（证据见右）")
    for ln in lines[:limit]:
        print(ln)
    if len(lines) > limit:
        print(f"     … 其余 {len(lines) - limit} 个略")
