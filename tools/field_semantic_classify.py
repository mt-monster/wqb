#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""field_semantic_classify.py — 数据集字段的经济含义归类（S1 补做环节）。

背景（2026-09-28 KOR/fundamental17 实证）：
  步 3 只做了 scan_fields（typed catalog = 类型/覆盖/users），**没做语义归类**，
  直接进 GEM。结果 348 条产物里 49.4% 落在「货币代码 / 汇率叉乘」这类
  **非信号字段**上（三角套汇恒等式、字符串分类码），71% 是废产物。
  typed catalog 只回答「这字段是什么类型、覆盖多少」，不回答
  「这字段能不能当信号」——后者必须由语义归类给出。

用途：
  1. 产出**信号字段白名单 / 非信号黑名单**（供 GEM 字段池约束、表达式过滤）；
  2. 按经济大类分桶，供后续「每类至少N槽」的多样性配给；
  3. ⚠ 产出是**字段池**，不是 ideas —— 禁止当 ideas.md 注入 GEM
     （SOP 2026-09-17 P3-11：确定性模板渲染会让 GEM 退化为「每字段套 rank」）。

用法:
    python tools/field_semantic_classify.py --region KOR --dataset fundamental17
    python tools/field_semantic_classify.py --region KOR --dataset fundamental17 --write-ledger

    # 批量补跑（2026-10-01 新增）：默认只跑「有 catalog ∧ 有字段 ∧ 未判死」的活跃集
    python tools/field_semantic_classify.py --region KOR --all --write-ledger
    python tools/field_semantic_classify.py --region KOR --all --dry-run      # 只列清单
    python tools/field_semantic_classify.py --region KOR --all --force        # 连已有台账也重跑

背景（--all 动机）：全库 catalog 697 个 vs `s1_semantic` 33 个（4.7%），EUR/IND/GLB/JPN
为 0 —— 步 5 闸 SEM 在多数区域只能靠「阻断」而非「过滤」生效。批量入口把历史欠账一次清掉。
⚠ 选取口径必须排除**幽灵键**：实测 249 个 `cache_*` 前缀 catalog 键在 fields 表零字段，
只按「有 catalog 键」选会把 37% 的批量工作量浪费在跑不出结果的键上。

运行环境: 任意 Python（只读 DB；--write-ledger 时写库走规范工厂）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
import sys as _sys_pe, os as _os_pe
_sys_pe.path.insert(0, _os_pe.path.dirname(_os_pe.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器解析（tools/_pyenv.py）；作为脚本运行时自动切到 MCP venv，故文档里可写裸 python

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wqb.db_conn import connect as db_connect  # 规范工厂（禁裸 sqlite3.connect）
from wqb.semantic_ledger import ledger_has_l35  # L3.5 判定唯一口径（与 campaign.py 同源）


# 非信号字段：标识符 / 分类码 / 标签 / 汇率换算 / 计数口径 —— 无论覆盖多高都不得当信号输入
#
# ⚠ 2026-09-28 修复（重要）：原规则里 `is_` / `_flag$` 用**未锚定的名字子串**匹配，
# 结果把 `oth466_is_ebit_oper_q`（**Income Statement** EBIT，users=248）这类字段当
# 「布尔标志位」误杀 —— other466 上 39/177（22%）被误判，且被杀的恰是 users 最高的
# 利润表核心字段。教训：**缩写歧义（is = Income Statement vs is_ 标志）不能靠名字判，
# 必须看描述文**。故标志位/分类码改由 `desc` 判定；名字规则只保留无歧义的强标识符。
#
# ⚠ 2026-10-01 第二次同类修复：`isin` 仍是**裸子串**，把 JPN/pattern_scores 的
# `avg_similarity_ri**sin**g_wedge_pattern` 整族 52 个字段误杀（"rising" 里含 "isin"）。
# 同类风险：`ticker` 会咬 `turnover_ticker...`、`cusip` 等。教训与 09-28 完全一致——
# **标识符必须词元锚定（token-anchored），禁裸子串**。改为 `(?:^|_)tok(?:$|_)` 形态。
NON_SIGNAL_PATTERNS = [
    # 2026-10-02：`crncy_iso` / `_crncy` 是 analyst 系的 ISO 货币码写法（实测 anl69 有
    # `anl69_roa_best_crncy_iso` 等），与 `currency_code` 同义但字面不同 → 补入词元锚定形式。
    (r"currency_code|cur_code|(?:^|_)crncy(?:_|$)", "货币/报表币种代码"),
    (r"^fnd17_\d+_(usdtorep|reptoprc|repto|ustorep)", "汇率换算（叉乘多为恒等式）"),
    (r"exrate|exchange_rate", "汇率（叉乘多为恒等式）"),
    (r"^fx_|_fx_|_fx$", "汇率（叉乘多为恒等式）"),
    # 标识符：**词元锚定**（`_isin_` / `_isin$` / `^isin_`），不做裸子串匹配——
    # 裸 `isin` 会命中 "r|isin|g"（rising）、裸 `ticker` 会命中含 ticker 的复合词。
    (r"(?:^|_)(?:gvkey|cusip|isin|sedol|ticker)(?:$|_)|"
     r"(?:^|_)(?:iso_country|country_code|exchange_code|region_code)(?:$|_)",
     "标识符/国别交易所代码"),
    (r"fiscal_year_end|report_date|period_end|"
     # 2026-10-02 补漏（GLB/analyst69 首波归因）：原名规则只认 `report_date` / `_date$` /
     # `_dt$`，把**同一语义的其它后缀写法**漏成"信号字段"——实测 analyst69 的
     # `anl69_*_expected_report_time`（= `*_expected_report_dt` 的时间写法）、
     # `anl69_*_best_cur_fiscal_qtr_period` / `_fiscal_year_period`、`*_fperiod_override`
     # 全部 signal=True → 渗入 GEM 绑定池并霸榜（quality 排序看 alphaCount）。
     # 教训同 09-28/10-01：**语义同族必须按概念而非单个后缀识别**（time≈dt、period≈date）。
     r"report_time|expected_report_time|latest_ann_dt|most_recent_period_end|"
     r"fiscal_qtr_period|fiscal_year_period|fperiod_override|"
     r"_date$|_dt$|_period$", "日期/期间口径"),
    (r"shares_outstanding_class|_share_class_", "股份类别标签"),
]

# 描述文驱动的非信号判定：布尔标志 / 分类标签 / 纯代码（名字规则无法可靠识别时用）
#
# ⚠ 2026-09-28 第二次修复：初版用裸 `\bindicator\b` / `\bflag\b` / `whether`，
# 把「技术分析指标」也误杀 —— model109 的 Bollinger Bands / Negative Volume Index /
# **Altman Z-score** / Chaikin Money Flow / Money Flow Index / Stochastic Oscillator
# 描述里都含 "indicator"，51/539 被误判为布尔标志。
# 正解：**必须出现显式布尔措辞**（"indicator denoting whether"、"equals 1"、
# "dummy variable"、"1 if ... 0 otherwise"），仅出现 indicator/flag 名词不算。
NON_SIGNAL_DESC_PATTERNS = [
    (r"indicator\s+(?:denoting|indicating|that indicates|for)\s+whether|"
     r"flag\s+(?:showing|denoting|indicating|that indicates)\s+whether|"
     r"denotes?\s+whether|"
     r"whether\s+[^.]{0,80}?\b(?:equals?|is)\s+1\b|"
     r"\bdummy\s+variable\b|\bindicator\s+variable\b|\bbinary\s+(?:variable|flag)\b|"
     r"\b1\s+if\b[^.]{0,80}?\b0\s+otherwise\b",
     "布尔标志/指示变量（描述文判定）"),
    (r"three[- ]letter\s+iso\s+(?:currency|country)\s+code|\biso\s+(?:currency|country)\s+code\b|"
     r"compustat\s+global\s+company\s+identifier|\bcompany\s+identifier\b",
     "分类码/标识符（描述文判定）"),
]

# 经济大类（按描述关键词命中，顺序 = 优先级）
ECON_CATEGORIES = [
    # ★ 价格/收益口径必须先于 size_level / valuation（2026-10-02 修复）
    # 背景：GLB/analyst_earnings_ibes 28 字段里 24 个是纯价量（closing/highest/lowest
    # price、N-day total return、vwap），描述含 "D1-delayed / split- and FX-adjusted /
    # point-in-time"，但不含 margin/growth 等词 → 全落 other。这批是价格信号（反转/动量），
    # 经济含义与基本面完全不同，必须可识别（否则字段池全是 other，无法做族级机制推理）。
    ("price_return", r"closing price|opening price|highest (?:traded )?price|"
                     r"lowest (?:traded )?price|session (?:high|low)|"
                     r"trading day return|total return|stock return|"
                     r"volume[- ]weighted average price|\bvwap\b|"
                     r"price for the (?:trading day|security)|as of .*close \(price",
     "价格/收益"),
    ("valuation", r"price[- ]to[- ]|enterprise value|market cap|ev[ /_]|p/[esb]|yield|multiple|ratio of .* to price", "估值倍数"),
    ("profitability", r"margin|return on|roe|roa|roic|roi|profit|ebit|ebitda|net income|earnings per|eps|operating income", "盈利能力"),
    ("growth", r"growth|cagr|trend|percent change|change in .* versus|year[- ]over[- ]year|yoy|qoq", "成长/趋势"),
    ("cash_quality", r"cash flow|free cash|fcf|accrual|cash conversion|cfo", "现金流质量"),
    ("leverage_solvency", r"debt|leverage|solvency|coverage|interest expense|current ratio|quick ratio|debt[- ]to[- ]", "偿债/杠杆"),
    ("efficiency", r"turnover|asset use|inventory|receivable|days (sales|payable|inventory)|working capital", "运营效率"),
    ("liquidity_risk", r"beta|volatility|volume as|liquidity|trading volume", "流动性/风险"),
    ("size_level", r"total assets|revenue|sales|book value|equity|shares outstanding|market value", "规模/水平"),
    ("per_share", r"per share|per[- ]share|/share", "每股口径"),
    ("dividend", r"dividend|payout|buyback|repurchase", "分红/回购"),
]

#: ★ 技术指标大类（2026-10-01 新增，修复「技术指标被误归 growth」）
#: 背景：GBR/model264 演示中 304 个技术指标字段（Bollinger Bands / ADL / Amihud /
#: Money Flow / Stochastic ...）因描述含 "change" / "trend" 被 `growth` 规则先命中，
#: 全部误归到「成长/趋势」。技术指标与经济面指标的经济含义完全不同，必须前置拦截：
#: **顺序 = 优先级**，本表插在 ECON_CATEGORIES 之前匹配。
TECHNICAL_CATEGORIES = [
    ("tech_trend", r"\bmoving average\b|\bema\b|\bsma\b|macd|bollinger|"
                    r"\baverage true range\b|\batr\b|parabolic|\badx\b|directional movement",
     "技术指标·趋势"),
    ("tech_momentum", r"\brsi\b|relative strength index|stochastic|williams %?r|"
                      r"rate of change|\broc\b|momentum indicator|cci|commodity channel",
     "技术指标·动量"),
    ("tech_volume", r"on[- ]balance volume|\bobv\b|money flow|chaikin|"
                    r"volume (?:index|oscillator|weighted)|accumulation/distribution|\badl\b|\bvwap\b",
     "技术指标·量能"),
    ("tech_volatility", r"standard deviation of (?:price|return)|\bbollinger band width\b|"
                        r"historical volatility|\bkeltner\b|donchian|volatility index",
     "技术指标·波动"),
]


def classify(desc: str, name: str):
    d = (desc or "").lower()
    n = (name or "").lower()
    for pat, why in NON_SIGNAL_PATTERNS:
        if re.search(pat, n):
            return None, f"非信号：{why}"
    # 描述文驱动的标志位/分类码判定（名字规则无法可靠区分 is=Income Statement 等歧义缩写）
    for pat, why in NON_SIGNAL_DESC_PATTERNS:
        if re.search(pat, d):
            return None, f"非信号：{why}"
    # ★ 技术指标必须先于经济大类匹配（否则被 growth / liquidity_risk 抢走）
    for cat, pat, label in TECHNICAL_CATEGORIES:
        if re.search(pat, d):
            return cat, label
    for cat, pat, label in ECON_CATEGORIES:
        if re.search(pat, d):
            return cat, label
    return "other", "未归类"


#: ★ 时间朝向提示（2026-10-04 新增；**仅提示，不拦截、不改 signal / blocked 判定**）。
#: 同一数据集里「已实现（事后）」与「预测（前瞻）」是两个完全不同的信号源：GLB/analyst_consensus 前 16 条
#: 全灭，真因是选了 `actual_*`（已实现，事后、无预测力），换成 `mean_estimate_*`（预测）后同结构大幅提升
#: （WorkBuddy 记忆 2026-10-03）。此前被误诊成「窗口不匹配」，白白多烧了一轮。
#: 口径：名字**词元锚定**（`(?:^|_)tok(?:$|_)`，禁裸子串——`best_*` 含 est、`forecasting_*` 含 forecast 都不算）；
#: 名字没命中才看描述**开头**（以 Actual / Reported 起头 = 已实现；以 Mean / Median / Consensus / Forecast /
#: Estimated … 起头 = 预测），不扫整段描述，避免「actual vs estimate」之类的对比句误判。
#: 两类都命中（如 surprise = actual − estimate）记 mixed：那是合法构造，不归任何一边。
_REALIZED_NAME_RE = re.compile(r"(?:^|_)(?:actual|actuals|reported|realized|realised)(?:$|_)")
_FORECAST_NAME_RE = re.compile(
    r"(?:^|_)(?:estimate|estimates|est|forecast|forecasts|consensus|guidance|predicted|projected)(?:$|_)")
_REALIZED_DESC_RE = re.compile(r"^\s*(?:the\s+)?(?:actual|reported|realized|realised)\b")
_FORECAST_DESC_RE = re.compile(
    r"^\s*(?:the\s+)?(?:mean|median|consensus|forecasts?|estimated?|predicted|projected|expected)\b")


def time_orientation(name: str, desc: str = ""):
    """字段 → 'realized'（已实现/事后）/ 'forecast'（预测/前瞻）/ 'mixed' / None（无法判断）。"""
    n = (name or "").lower()
    r, f = bool(_REALIZED_NAME_RE.search(n)), bool(_FORECAST_NAME_RE.search(n))
    if not (r or f):
        d = (desc or "").lower()
        r, f = bool(_REALIZED_DESC_RE.search(d)), bool(_FORECAST_DESC_RE.search(d))
    if r and f:
        return "mixed"
    return "realized" if r else ("forecast" if f else None)


#: ★ 同族后缀：`<前缀>_<后缀>` 的后缀若命中，则该字段属某「结构族」。
#: 用途 = L3.5 族识别（不产信号，只把同源字段聚成族，供 L4 机制推理）。
#: 出处：GBR/model264 演示 `mdl264_<指标族>_<l1|l2|l3>` 三分类概率族。
#: 一个底层指标可能同时有 `_l1/_l2/_l3/_class/_se`，**族键 = 剥离全部后缀后的基名**。
#: 族识别后缀表。**每条必须能说出经济学含义**，否则聚出来的族对 L4 无意义只会制造噪音。
#: 覆盖面实测（2026-10-01）：仅按「三分类/统计」类后缀时，414 个语义台账里只有 77 个
#: （18.6%）产得出非空族——`fundamental*/pv*/news*/risk*` 等**原生集**字段不带这类后缀，
#: L4 五步法的第一步「族」就拿不到输入。故补入期限 / 窗口 / 方向 / 端点四类，它们分别
#: 直接对应 L4 的形态：期限→期限结构、方向 & 端点→H1 净方向价差。
FAMILY_SUFFIX_PATTERNS = [
    (r"_l([123])$", "三分类概率", {1: "P(fall)", 2: "P(neutral)", 3: "P(up)"}),
    (r"_class$", "三分类标签", {}),
    (r"_se$", "预期口径", {}),
    (r"_q([1-5])$", "分位数", {}),
    (r"_mean$|_std$|_min$|_max$|_median$", "统计量", {}),
    # ---- 以下四类为原生集补充（经济学含义明确、噪音低）----
    (r"_fy([1-4])$", "预测期", {1: "FY1", 2: "FY2", 3: "FY3", 4: "FY4"}),
    (r"_([0-9]{1,3})d$", "窗口", {}),               # ret_1d / ret_20d → 期限结构
    (r"_(up|down)$", "方向", {"up": "上行", "down": "下行"}),
    (r"_(high|low|hi|lo)$", "端点", {"high": "高", "hi": "高",
                                     "low": "低", "lo": "低"}),   # H1 净方向价差的两端
]


def _strip_family_suffix(n: str):
    """反复剥离末尾已知后缀 → (基名, 角色列表, 主 kind)。剥不动则基名 = 原名。"""
    roles, kinds = [], []
    cur = n or ""
    while True:
        hit = False
        for pat, kind, rolemap in FAMILY_SUFFIX_PATTERNS:
            m = re.search(pat, cur)
            if m and m.start() > 0:
                role = None
                if rolemap:
                    try:
                        role = rolemap.get(int(m.group(1)))
                    except (IndexError, ValueError):
                        role = None
                roles.append(role or kind)
                kinds.append(kind)
                cur = cur[: m.start()]
                hit = True
                break
        if not hit:
            break
    return cur, roles, kinds


def family_of(name: str):
    """字段名 → (族键, 角色, 说明)；不属任何已知族返回 (field_name, None, None)。

    「族键」= 剥离**全部**已知后缀后的基名（`mdl264_x_l3` 与 `mdl264_x_class`
    同族）；「角色」= 最具信息量的后缀语义（三分类概率 > 标签 > 预期口径）。
    这是 L3.5 结构层的输入，**不改变 classify() 的信号/黑名单判定**。
    """
    n = (name or "").lower()
    base, roles, kinds = _strip_family_suffix(n)
    if not roles or base == n:
        return n, None, None
    # 角色优先级：三分类概率 > 三分类标签 > 分位数 > 统计量 > 预期口径
    for pref in ("三分类概率", "三分类标签", "分位数", "统计量", "预期口径"):
        if pref in kinds:
            idx = kinds.index(pref)
            return base, roles[idx], ("三分类概率" if "三分类概率" in kinds else pref)
    return base, roles[0], kinds[0]


def build_families(fields):
    """把 signal 字段列表聚成族 → dict[族键] = {n, roles, fields[], max_ac, max_users, cats, kinds}。

    只聚「有后缀角色」的字段；无后缀字段不构成族（返回时不收录）。
    """
    fams = {}
    for it in fields:
        base, role, kind = family_of(it["field"])
        if role is None:
            continue
        f = fams.setdefault(base, {"n": 0, "kind": kind, "roles": [],
                                   "fields": [], "max_ac": 0, "max_users": 0,
                                   "cats": set()})
        f["n"] += 1
        f["roles"].append({"field": it["field"], "role": role})
        f["fields"].append(it["field"])
        f["max_ac"] = max(f["max_ac"], it.get("alpha_count") or 0)
        f["max_users"] = max(f["max_users"], it.get("users") or 0)
        f["cats"].add(it.get("cat") or "other")
    for f in fams.values():
        f["cats"] = sorted(f["cats"])
        # 族 kind 升级：只要含三分类概率即标为三分类族
        if any(r["role"].startswith("P(") for r in f["roles"]):
            f["kind"] = "三分类概率"
    return fams


def classify_dataset(region: str, dataset: str, *, write_ledger: bool = False,
                     out_path: str = None, quiet: bool = False, conn=None):
    """对单个 (region, dataset) 做语义归类；返回 (rc, payload)。

    单跑（`--dataset`）与批量（`--all`）共用同一执行体——**禁止两条路径各写一份**，
    否则批量补的台账与单跑口径分叉。rc: 0=成功 / 1=无字段。
    """
    own = conn is None
    if own:
        conn = db_connect(readonly=True)
    data_type = None
    try:
        rows = conn.execute(
            """SELECT f.field_name, f.field_type, f.coverage, f.user_count, f.alpha_count, f.description
               FROM fields f JOIN datasets d ON d.id=f.dataset_id
               WHERE d.name=? AND d.region_id=(SELECT id FROM regions WHERE name=?)
               ORDER BY COALESCE(f.alpha_count,0) DESC, COALESCE(f.user_count,0) DESC""",
            (dataset, region),
        ).fetchall()
        # ---- 数据集级类型闸：GROUP 类不是信号本体，只能当 group_rank 分组轴 ----
        # ⚠ 2026-10-02 DEU/pv30 实证：catalog.data_type == "GROUP"（285/285 字段）时，
        #   平台把每个字段的 field_type 都标成 "signal"，字段级 classify 全部放行
        #   （曾误报 signal_field_count=285 / blocked=0），于是 GEM 拿到 285 个"信号字段"，
        #   生成 days_from_last_change(sign(<pca 组件>)) 这类**分组变更伪信号**，
        #   s2_pv30_d1 165 条过门禁后 132 条 fail。GROUP 类必须在**字段级之前**整集降级。
        # ⚠ 必须在 conn 关闭前取（own 分支下 finally 会关连接）。
        try:
            crow = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?",
                                (region, f"catalog_{dataset}")).fetchone()
            if crow:
                data_type = (json.loads(crow[0]) or {}).get("data_type")
        except Exception:  # noqa: BLE001 — catalog 缺失/坏 JSON 不该阻断归类
            data_type = None
    finally:
        if own:
            conn.close()
    if not rows:
        if not quiet:
            print(f"[WARN] 无字段：{region}/{dataset}")
        return 1, None

    is_group_only = (str(data_type).upper() == "GROUP")
    # ⚠ 2026-10-02 DEU/other455 实证修正：集级 data_type 可能是**混合集**的标签，会误伤。
    #   other455 集级 data_type="GROUP"，但 1500 字段实际 GROUP 1200 + MATRIX 300；
    #   而它恰是本区唯一有希望的方向（锚点 O0NxWZMR 用的就是那 300 个 MATRIX）。
    #   ⇒ 降级必须按**字段级 `fields.field_type`** 判，不能只看集级标签。
    #   集级 GROUP 只作兜底（字段级信息缺失时）。
    n_group_fields = sum(1 for r in rows if str(r[1]).upper() == "GROUP")
    mixed_group = is_group_only and n_group_fields < len(rows)
    if mixed_group:
        if not quiet:
            print(f"[GROUP-MIXED] {region}/{dataset} 集级 data_type=GROUP 但字段级 GROUP 仅 "
                  f"{n_group_fields}/{len(rows)} ⇒ 按字段级 type 判（MATRIX 字段放行）")

    signal, blocked = [], []
    by_cat = defaultdict(list)
    for name, ftype, cov, users, ac, desc in rows:
        cat, label = classify(desc, name)
        item = {"field": name, "cat": cat, "label": label, "type": ftype,
                "cov": round(cov, 4) if cov is not None else None,
                "users": users if users is not None else 0,
                "alpha_count": ac if ac is not None else 0,
                "desc": (desc or "")[:110]}
        if str(ftype).upper() == "GROUP":
            # 字段级降级：GROUP 类字段（聚类/分类标签）仅可作 group_rank 分组轴，不得当信号输入。
            # 判据用**字段级 type**（`fields.field_type`），故混合集里的 MATRIX 字段照常放行。
            item["cat"] = None
            item["label"] = "GROUP 类字段：仅可作 group_rank 分组轴，不得当信号输入"
            blocked.append(item)
        elif cat is None:
            blocked.append(item)
        else:
            item["orientation"] = time_orientation(name, desc)
            signal.append(item)
            by_cat[cat].append(item)

    n = len(rows)
    if not quiet:
        print(f"\n=== {region}/{dataset} 字段经济归类（共 {n}）===")
        print(f"信号字段 {len(signal)} ({100*len(signal)/n:.1f}%)  |  非信号黑名单 {len(blocked)} ({100*len(blocked)/n:.1f}%)")
        print("\n-- 经济大类分布（信号字段）--")
        for cat, items in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
            cold = sum(1 for i in items if i["users"] <= 9)
            print(f"  {cat:<18} {len(items):>4}  (冷门 users<=9: {cold:>3}, {100*cold/len(items):.0f}%)")
        print("\n-- 非信号黑名单（不得当信号输入）--")
        for why in sorted({i["label"] for i in blocked}):
            sub = [i for i in blocked if i["label"] == why]
            print(f"  {why:<28} {len(sub):>3}  例: {', '.join(i['field'] for i in sub[:3])}")

    # ---- 时间朝向提示（仅提示，不拦截；见 time_orientation 注释）----
    ori = {"realized": [], "forecast": [], "mixed": [], "unlabeled": []}
    for i in signal:
        ori[i.get("orientation") or "unlabeled"].append(i["field"])
    if not quiet:
        print(f"\n-- 时间朝向提示（仅提示，不拦截）--")
        print(f"  realized(已实现/事后) {len(ori['realized'])} | forecast(预测/前瞻) {len(ori['forecast'])} | "
              f"mixed {len(ori['mixed'])} | 未标注 {len(ori['unlabeled'])}")
        if ori["realized"] and ori["forecast"]:
            print("  ⚠ 同一数据集同时有已实现与预测两类字段：它们是两个完全不同的信号源，别默认从 actual_* 起手——")
            print("    GLB analyst_consensus 前 16 条全灭的真因就是选了 actual_*（事后、无预测力），"
                  "改 mean_estimate_* 后同结构大幅提升。先各出 1 批探针比较。")

    # ---- L3.5 结构层：族识别（不产信号，只供 L4 机制推理；见 signal-hypothesis-construction.md）----
    fams = build_families(signal)
    tri = {k: v for k, v in fams.items() if v["kind"] == "三分类概率"}
    if not quiet:
        print(f"\n-- L3.5 结构族（共 {len(fams)}，其中三分类概率族 {len(tri)}）--")
        for k, v in sorted(tri.items(), key=lambda kv: -kv[1]["max_ac"])[:10]:
            roles = ",".join(sorted(r["role"] for r in v["roles"]))
            flag = "★完整" if {"P(fall)", "P(neutral)", "P(up)"} <= {r["role"] for r in v["roles"]} else ""
            print(f"  {k:<34} n={v['n']:<3} ac={v['max_ac']:<3} users={v['max_users']:<3} [{roles}] {flag}")
        if len(tri) > 10:
            print(f"  ... 另有 {len(tri) - 10} 个三分类族（完整族 {sum(1 for v in tri.values() if {'P(fall)', 'P(neutral)', 'P(up)'} <= {r['role'] for r in v['roles']})}）")

    out = {
        "region": region, "dataset": dataset, "total_fields": n,
        "data_type": data_type,
        "group_only": is_group_only and not mixed_group,
        "group_mixed": mixed_group,
        "signal_field_count": len(signal),
        "blocked_field_count": len(blocked),
        "signal_fields": [i["field"] for i in signal],
        "blocked_fields": [{"field": i["field"], "reason": i["label"]} for i in blocked],
        "by_category": {k: [i["field"] for i in v] for k, v in by_cat.items()},
        "category_stats": {k: {"n": len(v), "cold_users_le_9": sum(1 for i in v if i["users"] <= 9)}
                           for k, v in by_cat.items()},
        # 时间朝向提示（仅计数 + 各 15 个样例；不改 signal / blocked 判定）
        "orientation_stats": {k: len(v) for k, v in ori.items()},
        "orientation_samples": {k: v[:15] for k, v in ori.items() if k != "unlabeled" and v},
        "families": {k: {"n": v["n"], "kind": v["kind"], "fields": v["fields"],
                         "roles": v["roles"], "max_ac": v["max_ac"],
                         "max_users": v["max_users"], "cats": v["cats"]}
                     for k, v in fams.items()},
        "family_stats": {
            "n_families": len(fams),
            "n_triclass": len(tri),
            "n_triclass_complete": sum(
                1 for v in tri.values()
                if {"P(fall)", "P(neutral)", "P(up)"} <= {r["role"] for r in v["roles"]}),
        },
        "note": "产出是字段池（field pool），不是 ideas —— 禁止当 ideas.md 注入 GEM（SOP 2026-09-17 P3-11）；"
                "families 供 L4 机制推理，形态构建见 wq-brain-ra-pipeline/references/signal-hypothesis-construction.md",
    }
    p = out_path or f"cache/{region.lower()}_{dataset}_semantic.json"
    Path(p).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    if not quiet:
        print(f"\n[写出] {p}")

    if write_ledger:
        key = f"s1_semantic_{dataset}"
        wconn = db_connect()
        try:
            import datetime
            now = datetime.datetime.now().isoformat(timespec="seconds")
            v = json.dumps(out, ensure_ascii=False)
            r = wconn.execute("SELECT id FROM ledger_kv WHERE region=? AND key=?", (region, key)).fetchone()
            if r:
                wconn.execute("UPDATE ledger_kv SET value=?, updated_at=? WHERE id=?", (v, now, r[0]))
            else:
                wconn.execute("INSERT INTO ledger_kv(region,key,value,created_at,updated_at) VALUES(?,?,?,?,?)",
                              (region, key, v, now, now))
            wconn.commit()
            if not quiet:
                print(f"[ledger] {region}/{key}")
        finally:
            wconn.close()
    return 0, out


def _active_catalog_datasets(conn, region: str):
    """「有 catalog 且未判死」的活跃集（`--all` 的选取口径，用户 2026-10-01 定案）。

    三道过滤（缺一不可，实测每条都真会误报）：
      ① **有 catalog**：ledger 存在 `catalog_<ds>` 键；
      ② **有真实字段**：`fields` 表里该集字段数 > 0。**实测 249 个 `cache_*` 前缀的
         catalog 键在 fields 表里零字段**（如 IND/cache_earnings3），只按 ① 选会浪费
         37% 的批量工作量在幽灵键上，且全部返回 rc=1；
      ③ **未判死**：排除 `dead_dataset_index` 的 dataset_dead ∪ saturated
         （复用 `wqb.profile_drift` 的规范实现，禁另写一份判死口径）。

    返回 (selected, skipped) —— skipped 是 {ds: 原因} 便于审计。
    """
    from wqb.profile_drift import dead_dataset_index
    dead = dead_dataset_index(conn, region)
    dead_all = {str(d).strip().lower() for d in (dead["dataset_dead"] | dead["saturated"])}

    cat = {}
    for r in conn.execute("SELECT key FROM ledger_kv WHERE region=? AND key LIKE 'catalog_%'", (region,)):
        cat[r["key"][len("catalog_"):]] = True
    # fields 表里真有字段的集
    has_fields = set()
    for r in conn.execute(
            """SELECT DISTINCT d.name FROM fields f JOIN datasets d ON d.id=f.dataset_id
               JOIN regions rg ON rg.id=d.region_id WHERE rg.name=?""", (region,)):
        has_fields.add(str(r["name"]).lower())

    selected, skipped = [], {}
    for ds in sorted(cat):
        if ds.lower() in dead_all:
            skipped[ds] = "已判死/饱和"
            continue
        if ds.lower() not in has_fields:
            skipped[ds] = "catalog 键存在但 fields 表零字段（幽灵键）"
            continue
        selected.append(ds)
    return selected, skipped


def run_all(args) -> int:
    """`--all`：批量补跑「有 catalog 且未判死」的活跃集的语义台账。"""
    import sqlite3 as _sq
    conn = db_connect(readonly=True, row_factory=_sq.Row)
    try:
        selected, skipped = _active_catalog_datasets(conn, args.region)
        # 已有**完整**台账（含 L3.5 families）的集默认跳过（除非 --force）。
        # ★ 与 `campaign.py::_semantic_coverage_check` 的补做条件同源：台账在但
        # **缺 families** 视为「待补」而非「已有」——L3.5 族是 L4 形态构建的输入，
        # 只提示不补做会导致 L4 在旧版台账上拿不到族（实测 414 个台账仅 76 个带 families）。
        existing, stale = set(), 0
        for r in conn.execute("SELECT key,value FROM ledger_kv WHERE region=? AND key LIKE 's1_semantic_%'",
                              (args.region,)):
            ds_key = str(r["key"][len("s1_semantic_"):]).lower()
            if ledger_has_l35(r["value"]):
                existing.add(ds_key)
            else:
                stale += 1
        todo, already = [], 0
        for ds in selected:
            if ds.lower() in existing and not args.force:
                already += 1
                continue
            todo.append(ds)
    finally:
        conn.close()

    print(f"=== {args.region} 批量语义归类（--all）===")
    print(f"活跃集（有 catalog ∧ 有字段 ∧ 未判死）: {len(selected)}")
    print(f"  跳过：已判死/饱和 {sum(1 for v in skipped.values() if '判死' in v)}"
          f" / 幽灵键 {sum(1 for v in skipped.values() if '幽灵' in v)}")
    print(f"  已有完整台账（含 L3.5 族，默认跳过）: {already}" + ("（--force 覆盖）" if args.force else ""))
    print(f"  旧版台账（缺 L3.5 族，需补做）: {stale}")
    print(f"  待跑: {len(todo)}")
    if not todo:
        print("无待跑数据集。")
        return 0
    if args.dry_run:
        for ds in todo:
            print(f"  would classify: {ds}")
        return 0

    ok = fail = 0
    dropped_sum = 0
    for i, ds in enumerate(todo, 1):
        rc, payload = classify_dataset(args.region, ds, write_ledger=True, quiet=True)
        if rc == 0 and payload:
            ok += 1
            dropped_sum += payload.get("blocked_field_count", 0)
            print(f"  [{i}/{len(todo)}] ok   {ds:<30} 字段{payload['total_fields']:>5} "
                  f"非信号{payload['blocked_field_count']:>4}")
        else:
            fail += 1
            print(f"  [{i}/{len(todo)}] FAIL {ds}（rc={rc}）")
    print(f"\n[完成] 成功 {ok} / 失败 {fail} / 累计剔除非信号 {dropped_sum} 字段")
    return 0 if fail == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", required=False)
    ap.add_argument("--all", action="store_true",
                    help="批量补跑该区「有 catalog 且未判死」的活跃集语义台账"
                         "（默认跳过已有台账；见 --force）")
    ap.add_argument("--force", action="store_true", help="--all 时连已有台账的集也重跑")
    ap.add_argument("--dry-run", action="store_true", help="--all 只列待跑清单，不执行")
    ap.add_argument("--write-ledger", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.all:
        return run_all(args)
    if not args.dataset:
        ap.error("需要 --dataset，或用 --all 批量补跑")
    rc, _ = classify_dataset(args.region, args.dataset,
                             write_ledger=args.write_ledger, out_path=args.out)
    return rc


if __name__ == "__main__":
    _pyenv.reexec_under_venv()
    sys.exit(main())
