# -*- coding: utf-8 -*-
"""骨架库 + 语义填槽协议（skeleton mode 核心模块）。

设计动机：模板展开器时代的病根是约束全在语法层（占位符白名单/算子白名单），
零语义层约束 → LLM 产出裸字段/恒零/元数据腿表达式。本模块把"经济学意义"
拆为 骨架（算子组合拓扑，程序化枚举）× 槽位（字段选择，LLM 决定）× 方向（符号）。

LLM 只输出结构化填槽 JSON，表达式由代码组装 —— 语法合法性构造保证。

十二族骨架（MATRIX 版模板；VECTOR 字段先 vec_avg({x}) 聚合再入槽）：
  cs_rel      截面相对：rank({x}) - rank({y}) / group_rank({x}, subindustry)
  ts_chg      时序变化：rank(ts_delta({x},{W})) / rank({x}/(ts_mean({x},{W})+eps)-1)
  anomaly     异常度：  rank(ts_zscore({x},{W})) / 手写 z-score 版
  decay       衰减加权：rank(decay_linear({x},{W}))
  interact    双因子合成：{w}*rank({x}) + {1-w}*rank({y})
  vol_adj     波动调整：rank({x}) / (ts_std_dev(returns,{W})+eps)
  group_neut  行业中性：group_neutralize({x}, subindustry)
  ts_corr     时序相关：ts_corr(rank({x}), rank({y}), {W})
  event_gate  事件门控：trade_when(greater(ts_count({x},{W}),0), rank({x}), 0)
  conditional 条件组合：if_else(greater({x}, 0), rank({x}), rank({y}))
  outlier     稳健化：  rank(winsorize({x}, std=4))
  ts_reg      时序回归：rank(ts_regression({y}, {x}, {W}))

配套：字段分层（signal/scale/metadata/date + VECTOR/GROUP 类型感知）、
窗口分层（infer_freq）、生成端闸0 lint（恒等式/裸字段/元数据腿）、
region priors 加载（P2 共用）。
"""
from __future__ import annotations

import json
import os
import re
import sys

#: 技能根解析单源（同目录 skill_roots.py；顺序见其模块头，2026-09-11 收敛）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_roots import candidate_paths_under_skill  # noqa: E402


def _warn(msg: str) -> None:
    """统一告警出口（模块内不使用 logging 以保持无副作用）。"""
    print(f"[skeletons] WARN {msg}", file=sys.stderr, flush=True)


def _resolve_wqb_tools_dir() -> str | None:
    """解析工作区 tools 目录（经济 KB / 字段评分器所在），供可选增强导入。

    探测顺序：WQB_TOOLS_DIR → WQB_ROOT/WQ_PROJECT_ROOT 下 tools → 已知默认路径。
    找不到返回 None（增强项静默降级，不阻断主流程）。
    """
    for env_name in ("WQB_TOOLS_DIR",):
        v = (os.environ.get(env_name) or "").strip()
        if v and os.path.isdir(v):
            return v
    root = (os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or "").strip()
    if root:
        cand = os.path.join(root, "tools")
        if os.path.isdir(cand):
            return cand
    for cand in (r"D:\coding\traeCN_project\wqb\tools",):
        if os.path.isdir(cand):
            return cand
    return None


def _ensure_wqb_tools_path() -> None:
    """确保工作区 tools 目录在 sys.path（供可选增强模块导入）。"""
    td = _resolve_wqb_tools_dir()
    if td and td not in sys.path:
        sys.path.insert(0, td)


def _field_prefix(fid: str) -> str:
    """字段簇前缀（数据集编码段，如 anl39_agrosmgn2 → anl39）。"""
    return str(fid).split("_", 1)[0] if "_" in str(fid) else str(fid)


# ---------------------------------------------------------------------------
# 字段分层
# ---------------------------------------------------------------------------

# 元数据字段：只描述"这条记录是什么"，不含 alpha 信号 —— 永不应入表达式
_METADATA_SUFFIX_RE = re.compile(
    r"(periodend|periodtype|fyearend|periodnum|analyststart|"
    r"curfperiod|curperiod|_date$|^.*_dt$|fiscalend|reportdate)",
    re.IGNORECASE,
)

# 规模字段：可作分母/辅助腿，单独成腿会被 size 因子主导 —— 不给 LLM 作主槽
_SCALE_KEYWORDS = (
    "shares outstanding", "share outstanding", "market cap", "market value",
    "enterprise value", "total assets", "total equity", "sharesout",
)

_DATE_KEYWORDS = ("date", "period end", "fiscal year end", "announcement")


def classify_fields(field_ids: list, descriptions: dict | None = None,
                    types: dict | None = None) -> dict:
    """把字段分层：signal / scale / metadata / date + VECTOR/GROUP 类型感知。

    Args:
        field_ids: 字段 id 列表（如 ["anl39_agrosmgn2", ...]）。
        descriptions: {field_id: description}（来自 dataset CSV，可为 None）。
        types: {field_id: 平台 type 字符串}（如 MATRIX/VECTOR/GROUP，可为 None）。
            类型感知仅用于 prompt 标注与拥挤度提示；字段可用性分层不受影响。

    Returns:
        {"signal": [...], "scale": [...], "metadata": [...], "date": [...],
         "vector": [...],   # type==VECTOR（须 vec_* 聚合后入槽）
         "group": [...],    # type==GROUP（分组键字段，不作 alpha 主腿）
         "prefix_counts": {...}}  # 前缀簇计数（拥挤度标记用）
    """
    descriptions = descriptions or {}
    types = types or {}
    layers = {"signal": [], "scale": [], "metadata": [], "date": [],
              "vector": [], "group": [], "prefix_counts": {}}
    for fid in field_ids:
        desc = (descriptions.get(fid) or "").lower()
        ftype = str(types.get(fid) or "").upper()
        if _METADATA_SUFFIX_RE.search(fid):
            layers["metadata"].append(fid)
        elif any(k in fid.lower() for k in ("date", "_dt")) or any(
            k in desc for k in ("date of", "period end")
        ):
            layers["date"].append(fid)
        elif any(k in fid.lower() for k in ("sharesout", "mktcap", "shares_out")) or any(
            k in desc for k in _SCALE_KEYWORDS
        ):
            layers["scale"].append(fid)
        else:
            layers["signal"].append(fid)
        if ftype == "VECTOR":
            layers["vector"].append(fid)
        elif ftype == "GROUP":
            layers["group"].append(fid)
    for fid in layers["signal"]:
        pfx = _field_prefix(fid)
        layers["prefix_counts"][pfx] = layers["prefix_counts"].get(pfx, 0) + 1
    return layers


# ---------------------------------------------------------------------------
# 窗口分层
# ---------------------------------------------------------------------------

WINDOW_DOMAINS = {
    "daily": [5, 10, 21],
    "low_freq": [63, 126, 252],   # 季度/年度基本面：用长窗对齐披露周期
    "event": [3, 5, 10],          # 事件型（news/announcement）：短窗抓冲击
}

_EVENT_KEYWORDS = ("news", "announcement", "event", "alert", "sentiment")
_LOW_FREQ_KEYWORDS = (
    "quarterly", "annual", "fiscal", "quarter", "year", "fy", "period",
)


def infer_freq(field_id: str, description: str = "") -> str:
    """按字段名/描述推断更新频率 → 窗口域 key。"""
    text = f"{field_id} {description}".lower()
    if any(k in text for k in _EVENT_KEYWORDS):
        return "event"
    if any(k in text for k in _LOW_FREQ_KEYWORDS):
        return "low_freq"
    return "daily"


def resolve_windows(freq: str, dataset_id: str = "",
                    custom_pool: dict | None = None) -> list:
    """解析某频率域的候选窗口池（P2：campaign 可指定窗口池覆盖默认）。

    Args:
        freq: infer_freq 返回的域 key（daily / low_freq / event）。
        dataset_id: 数据集 id（供数据集形状特化，暂预留）。
        custom_pool: campaign 显式指定的窗口池，形如 {"daily": [5, 10, 21]}；
            仅覆盖其存在的域，其余域回退 WINDOW_DOMAINS 默认。

    Returns:
        有序窗口列表（int）。
    """
    if custom_pool and isinstance(custom_pool, dict):
        override = custom_pool.get(freq)
        if override:
            try:
                ws = [int(w) for w in override]
                if ws and all(1 <= w <= 500 for w in ws):
                    return sorted(set(ws))
            except (TypeError, ValueError):
                _warn(f"resolve_windows: bad custom_pool[{freq}]={override}")
    return list(WINDOW_DOMAINS.get(freq, WINDOW_DOMAINS["daily"]))


# ---------------------------------------------------------------------------
# 骨架库
# ---------------------------------------------------------------------------

_EPS_SMALL = "0.0001"
_EPS_VOL = "0.001"

SKELETONS = [
    {
        "id": "cs_rel.rank_diff",
        "family": "cs_rel",
        "n_fields": 2,
        "needs_window": False,
        "sign_allowed": True,
        "template": "rank({x}) - rank({y})",
        "description": "两字段截面 rank 差（相对强弱/预期修正差）",
    },
    {
        "id": "cs_rel.group_rank",
        "family": "cs_rel",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "group_rank({x}, subindustry)",
        "description": "行业中性化截面 rank（剔除行业 beta）",
    },
    {
        "id": "ts_chg.delta",
        "family": "ts_chg",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_delta({x}, {W}))",
        "description": "字段 {W} 日变化量的截面 rank（边际变化/修正方向）",
    },
    {
        "id": "ts_chg.rel_chg",
        "family": "ts_chg",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank({x} / (ts_mean({x}, {W}) + " + _EPS_SMALL + ") - 1)",
        "description": "相对自身 {W} 日均值的偏离（均值回归/上修幅度）",
    },
    {
        "id": "anomaly.zscore",
        "family": "anomaly",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_zscore({x}, {W}))",
        "description": "字段 {W} 日 z-score 的截面 rank（异常冲击检测）",
    },
    {
        "id": "anomaly.manual_z",
        "family": "anomaly",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(({x} - ts_mean({x}, {W})) / (ts_std_dev({x}, {W}) + " + _EPS_SMALL + "))",
        "description": "手写 z-score（ts_zscore 不存在时的等价替代）",
    },
    {
        "id": "decay.linear",
        "family": "decay",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(decay_linear({x}, {W}))",
        "description": "{W} 日线性衰减加权（近期信息权重更高，降噪）",
    },
    {
        "id": "interact.weighted_mix",
        "family": "interact",
        "n_fields": 2,
        "needs_window": False,
        "sign_allowed": True,
        "template": None,  # 特殊组装：{w} * rank({x}) + {1-w} * rank({y})
        "description": "双字段 rank 加权合成（多源信息互补，w∈{0.3..0.7}）",
    },
    {
        "id": "vol_adj.sharpe_like",
        "family": "vol_adj",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank({x}) / (ts_std_dev(returns, {W}) + " + _EPS_VOL + ")",
        "description": "截面 rank 除以波动率（低风险调整，类 Sharpe 加权）",
    },
    {
        "id": "group_neut.industry",
        "family": "group_neut",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "group_neutralize({x}, subindustry)",
        "description": "行业中性化（剔除行业均值，保留截面相对强弱）",
    },
    {
        "id": "group_zscore.industry",
        "family": "group_zscore",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "group_zscore({x}, subindustry)",
        "description": "行业内 z-score（剔除行业 beta，保留组内相对位置）",
    },
    {
        "id": "ts_corr.price_volume",
        "family": "ts_corr",
        "n_fields": 2,
        "needs_window": True,
        "sign_allowed": True,
        "template": "ts_corr(rank({x}), rank({y}), {W})",
        "description": "两字段 {W} 日 rank 相关（量价协同/背离检测）",
    },
    {
        "id": "event_gate.trade_when",
        "family": "event_gate",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "trade_when(greater(ts_count({x}, {W}), 0), rank({x}), 0)",
        "description": "事件门控（窗口内有数据才交易 rank({x})，无事件则空仓）",
    },
    {
        "id": "conditional.if_else",
        "family": "conditional",
        "n_fields": 2,
        "needs_window": False,
        "sign_allowed": True,
        "template": "if_else(greater({x}, 0), rank({x}), rank({y}))",
        "description": "条件组合（{x} 为正时取 rank({x})，否则取 rank({y})）",
    },
    {
        "id": "momentum_peak.arg_max",
        "family": "momentum_peak",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_arg_max({x}, {W}))",
        "description": "{W} 日内峰值位置 rank（峰值越近尾部=趋势仍在强化）",
    },
    {
        "id": "outlier.winsorize",
        "family": "outlier",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "rank(winsorize({x}, std=4))",
        "description": "4-sigma 截尾后 rank（压制极端值主导，稳健化）",
    },
    {
        "id": "ts_regression.beta",
        "family": "ts_regression",
        "n_fields": 2,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_regression({y}, {x}, {W}))",
        "description": "{y} 对 {x} 的 {W} 日回归敏感度 rank（弹性/联动检测）",
    },
]

INTERACT_WEIGHTS = [0.3, 0.4, 0.5, 0.6, 0.7]

SKELETONS_BY_ID = {s["id"]: s for s in SKELETONS}


def render_skeleton(skel_id: str, field_x: str, field_y: str | None = None,
                    window: int | None = None, sign: int = 1,
                    weight: float | None = None) -> str:
    """按骨架模板组装表达式。sign=-1 → (-1) * (expr)。"""
    skel = SKELETONS_BY_ID.get(skel_id)
    if skel is None:
        raise ValueError(f"unknown skeleton id: {skel_id}")

    if skel["family"] == "interact":
        w = weight if weight is not None else 0.5
        expr = f"{w} * rank({field_x}) + {round(1 - w, 4)} * rank({field_y})"
    else:
        expr = skel["template"].replace("{x}", field_x)
        if "{y}" in expr:
            if not field_y:
                raise ValueError(f"{skel_id} needs field_y")
            expr = expr.replace("{y}", field_y)
        if "{W}" in expr:
            w = window if window is not None else 10
            expr = expr.replace("{W}", str(w))

    if sign == -1:
        if not skel["sign_allowed"]:
            raise ValueError(f"{skel_id} does not allow sign flip")
        expr = f"(-1) * ({expr})"
    return expr


# ---------------------------------------------------------------------------
# 生成端闸 0：语义 lint（与 gate.py 闸0 同规则，生成端前置拦截）
# ---------------------------------------------------------------------------

_BARE_FIELD_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

_KNOWN_NONFIELD_TOKENS = {
    "returns", "close", "open", "high", "low", "volume", "vwap",
    "subindustry", "industry", "sector", "market", "country",
}


def split_top_args(s: str) -> list:
    """按顶层逗号切分函数参数（嵌套括号不切）。"""
    args, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        args.append(tail)
    return args


def _iter_fn_calls(expr: str):
    """遍历表达式中所有 fn(...) 调用的 (fn_name, args_str)。"""
    for m in re.finditer(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr):
        fn = m.group(1)
        # 找配对右括号
        depth = 1
        i = m.end()
        while i < len(expr) and depth > 0:
            if expr[i] == "(":
                depth += 1
            elif expr[i] == ")":
                depth -= 1
            i += 1
        yield fn, expr[m.end():i - 1]


def _is_number(s: str) -> float | None:
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


# 窗口=1 时退化的 ts 统计算子（窗口无统计意义/恒定输出）
_TS_WIN_NO_SINGLE = {
    "ts_min", "ts_max", "ts_mean", "ts_std_dev", "ts_zscore", "ts_median",
    "ts_skewness", "ts_kurtosis", "ts_corr", "ts_covariance",
    "ts_regression", "ts_rank", "ts_sum", "ts_arg_max",
}


def semantic_lint_expr(expr: str, known_fields: set | None = None) -> list:
    """闸 0 语义检查：恒等式 / 裸字段 / 元数据腿 / 恒零 / 退化窗口。

    返回 issue 列表（空=通过）。P5 扩展：双侧恒等元扫描（乘 1/加 0/除 1 任何一侧）、
    恒零/常数检测（乘 0 / x^0）、ts 统计窗口 ≤1 退化检测。
    """
    issues = []

    # EMPTY：空白表达式
    if not expr or not expr.strip():
        return ["EMPTY"]

    # BARE_FIELD：整条表达式就是一个字段名
    if _BARE_FIELD_RE.match(expr.strip()):
        token = expr.strip()
        if token not in _KNOWN_NONFIELD_TOKENS:
            issues.append(f"BARE_FIELD:{token}")

    # 恒等/恒零/常数 + ts 退化窗口（一次遍历）
    for fn, args_str in _iter_fn_calls(expr):
        args = split_top_args(args_str)
        if len(args) >= 2:
            a0, a1 = args[0], args[1]
            # IDENTITY：subtract(x,x) / divide(x,x)
            if fn in ("subtract", "divide") and a0 == a1:
                issues.append(f"IDENTITY:{fn}({a0},{a1})")
            else:
                # 双侧数值恒等元/零值扫描：命中即记一次（防重复 issue）
                for side, arg in ((0, a0), (1, a1)):
                    v = _is_number(arg)
                    if v is None:
                        continue
                    if (fn == "add" and v == 0.0) or (
                            fn == "multiply" and v == 1.0):
                        issues.append(f"NOOP:{fn}({a0},{a1})")
                    elif fn == "subtract" and side == 1 and v == 0.0:
                        issues.append(f"NOOP:{fn}({a0},{a1})")
                    elif fn == "divide" and side == 1 and v == 1.0:
                        issues.append(f"NOOP:{fn}({a0},{a1})")
                    elif fn == "power" and side == 1 and v == 1.0:
                        issues.append(f"NOOP:{fn}({a0},{a1})")
                    elif fn == "multiply" and v == 0.0:
                        issues.append(f"ZERO:{fn}({a0},{a1})")
                    elif fn == "divide" and side == 0 and v == 0.0:
                        issues.append(f"ZERO:{fn}({a0},{a1})")
                    elif fn == "divide" and side == 1 and v == 0.0:
                        issues.append(f"DIV_ZERO:{fn}({a0},{a1})")
                    elif fn == "power" and side == 0 and v in (0.0, 1.0):
                        issues.append(f"CONSTANT:{fn}({a0},{a1})")
                    elif fn == "power" and side == 1 and v == 0.0:
                        issues.append(f"CONSTANT:{fn}({a0},{a1})")
                    break
        # TS 退化窗口：ts 统计算子数值窗口 ≤1（窗口多为末参，如 ts_corr(x,y,W)）
        if fn in _TS_WIN_NO_SINGLE and len(args) >= 2:
            for arg in reversed(args):
                v = _is_number(arg)
                if v is None:
                    continue
                if v == int(v) and v <= 1:
                    issues.append(f"TS_WIN_TOO_SMALL:{fn}({args_str})")
                break

    # META_FIELD：元数据字段出现在表达式任何位置
    if known_fields:
        for token in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr):
            if token in known_fields and _METADATA_SUFFIX_RE.search(token):
                issues.append(f"META_FIELD:{token}")

    return issues


def _tpl_matches_category(tmpl: dict, category: str) -> bool:
    """模板与数据集类别弱匹配（文本线索）。

    templates 条目多为通用机制名，匹配不上不视为错误 —— 由调用方保底取 P0 前几条。
    """
    text = " ".join(str(tmpl.get(k) or "") for k in
                    ("name", "description", "economic_logic")).lower()
    hints = {
        "analyst": ("分析师", "analyst", "修正", "分歧", "盈利预测", "estimate", "recommend"),
        "fundamental": ("基本面", "fundamental", "质量", "盈利", "应计", "quality", "margin"),
        "pv": ("量价", "volume", "反转", "波动", "动量", "流动性", "volatility", "momentum"),
        "news": ("新闻", "情绪", "news", "sentiment", "attention"),
        "model": ("模型", "model", "因子", "打分"),
        "institutions": ("机构", "institution", "持仓", "ownership"),
        "option": ("期权", "option", "隐含", "implied"),
        "risk": ("风险", "risk", "尾部", "tail"),
    }
    return any(h in text for h in hints.get(category, ()))


# ---------------------------------------------------------------------------
# 填槽协议：LLM 输出 JSON → 代码组装
# ---------------------------------------------------------------------------

_SLOTS_JSON_RE = re.compile(r"\[.*\]", re.DOTALL)


def parse_slots_json(text: str) -> list:
    """从 LLM 输出中容错提取填槽 JSON 数组（剥 markdown fence / 前后噪音）。"""
    if not text:
        return []
    cleaned = text.strip()
    # 剥 ```json ... ``` fence
    fence = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1)
    else:
        m = _SLOTS_JSON_RE.search(cleaned)
        if m:
            cleaned = m.group(0)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [d for d in data if isinstance(d, dict)]


def _round_robin_by_family(candidates: list, max_total: int) -> list:
    """family round-robin 截断：逐轮每 family 各取 1 条，直到 max_total 或耗尽。

    P4 多样性：候选超量时按家族轮转取，避免先到先得让尾部截断集中打在
    少数 family 上；每 family 内部保持候选原始顺序（LLM 优先级）。
    """
    by_fam: dict = {}
    fam_order: list = []
    for item in candidates:
        fam = item[1]["family"]
        if fam not in by_fam:
            by_fam[fam] = []
            fam_order.append(fam)
        by_fam[fam].append(item)
    idx = {f: 0 for f in fam_order}
    result = []
    while len(result) < max_total and any(
            idx[f] < len(by_fam[f]) for f in fam_order):
        for fam in fam_order:
            if len(result) >= max_total:
                break
            if idx[fam] < len(by_fam[fam]):
                result.append(by_fam[fam][idx[fam]])
                idx[fam] += 1
    return result


def assign_slots(slots: list, signal_fields: set, max_per_family_field: int = 2,
                 max_total: int = 60, scale_fields: set | None = None) -> tuple:
    """填槽 JSON → (表达式列表, meta 列表, 丢弃统计)。

    过滤规则：
      - skeleton_id 必须存在于骨架库
      - 字段必须在 signal（或 scale，仅 interact 的 y 腿）集合内
      - family+field_x 组合的 window 变体 ≤ max_per_family_field（去重防挤占）

    多样性（P4）：候选 ≤ max_total 时按原序全收（保留 LLM 优先级）；
    超量时按 family round-robin 轮转截断，防止截断集中在个别 family。
    """
    scale_fields = scale_fields or set()
    dropped = {"bad_skeleton": 0, "bad_field": 0, "family_quota": 0,
               "lint": 0, "render_error": 0, "over_cap": 0}
    fam_field_count: dict = {}
    known = set(signal_fields) | set(scale_fields)
    candidates: list = []  # 全部闸通过后的 (expr, meta) 候选

    for s in slots:
        skel_id = str(s.get("skeleton_id", "")).strip()
        fx = str(s.get("field", "")).strip()
        fy = str(s.get("field2", "") or "").strip() or None
        skel = SKELETONS_BY_ID.get(skel_id)
        if skel is None:
            dropped["bad_skeleton"] += 1
            continue
        if fx not in signal_fields:
            dropped["bad_field"] += 1
            continue
        if skel["n_fields"] == 2:
            if not fy or fy not in known or fy == fx:
                dropped["bad_field"] += 1
                continue

        window = s.get("window")
        if skel["needs_window"]:
            try:
                window = int(window)
            except (TypeError, ValueError):
                window = WINDOW_DOMAINS["daily"][1]
        else:
            window = None

        sign = s.get("sign", 1)
        sign = -1 if sign in (-1, "-1") else 1

        weight = s.get("weight")
        if skel["family"] == "interact":
            try:
                weight = float(weight)
            except (TypeError, ValueError):
                weight = 0.5
            weight = min(INTERACT_WEIGHTS, key=lambda w: abs(w - weight))
        else:
            weight = None

        # family 配额：同 family 同主字段 ≤ max_per_family_field 个 window 变体
        key = (skel["family"], fx)
        if fam_field_count.get(key, 0) >= max_per_family_field:
            dropped["family_quota"] += 1
            continue

        try:
            expr = render_skeleton(skel_id, fx, fy, window, sign, weight)
        except ValueError:
            dropped["render_error"] += 1
            continue

        lint_issues = semantic_lint_expr(expr, known_fields=known)
        if lint_issues:
            dropped["lint"] += 1
            continue

        fam_field_count[key] = fam_field_count.get(key, 0) + 1
        candidates.append((expr, {
            "expr": expr,
            "family": skel["family"],
            "skeleton_id": skel_id,
            "window": window,
            "sign": sign,
            "field": fx,
            "field2": fy,
            "weight": weight,
            "rationale": str(s.get("rationale", "")).strip()[:200],
        }))

    # P4：候选 ≤ max_total → 原序全收；超量 → family round-robin 截断
    if len(candidates) <= max_total:
        accepted = candidates
    else:
        accepted = _round_robin_by_family(candidates, max_total)
        dropped["over_cap"] = len(candidates) - len(accepted)

    exprs = [e for e, _ in accepted]
    metas = [m for _, m in accepted]
    return exprs, metas, dropped


# ---------------------------------------------------------------------------
# Prompt 构建（skeleton mode）
# ---------------------------------------------------------------------------

def build_skeleton_prompt(dataset_id: str, region: str, delay: int,
                          field_layers: dict, descriptions: dict,
                          n_slots: int = 40, region_priors: str = "",
                          window_pool: dict | None = None,
                          enable_econ_kb: bool = True,
                          enable_field_scoring: bool = True,
                          enable_market_regime: bool = True) -> tuple:
    """构建填槽协议 prompt。返回 (system_prompt, user_prompt)。

    Args:
        window_pool: campaign 显式指定的窗口池（如 {"daily": [10, 22]}），
            覆盖 WINDOW_DOMAINS 默认；只覆盖列出的域。
        enable_econ_kb: 启用经济机制知识库
        enable_field_scoring: 启用字段质量评分
        enable_market_regime: 启用市场状态适配
    """
    skel_lines = []
    for s in SKELETONS:
        win = "W required" if s["needs_window"] else "no window"
        nf = "2 fields (field, field2)" if s["n_fields"] == 2 else "1 field"
        skel_lines.append(
            f"- skeleton_id=\"{s['id']}\" | family={s['family']} | {nf} | {win}\n"
            f"  shape: {s['template'] or '{w}*rank(x) + (1-w)*rank(y)'}\n"
            f"  meaning: {s['description']}"
        )
    skel_block = "\n".join(skel_lines)

    # 字段质量评分（P1 优化）
    field_scores = {}
    if enable_field_scoring:
        try:
            _ensure_wqb_tools_path()
            from field_quality_scorer import FieldQualityScorer
            scorer = FieldQualityScorer()
            field_scores = scorer.score_fields(
                field_layers["signal"], dataset_id, region, descriptions
            )
        except Exception as e:
            _warn(f"Field quality scoring failed: {e}")

    # 窗口池：campaign 指定 → 覆盖默认（P2）
    window_domains = {f: resolve_windows(f, dataset_id, window_pool)
                      for f in ("daily", "low_freq", "event")}
    vector_set = set(field_layers.get("vector", []))
    prefix_counts = field_layers.get("prefix_counts", {}) or {}

    sig_lines = []
    for fid in field_layers["signal"]:
        desc = (descriptions.get(fid) or "").strip()
        freq = infer_freq(fid, desc)
        win = window_domains[freq]
        pfx = _field_prefix(fid)

        # 拥挤度标记：同前缀簇字段数 ≥5 时标注（提示 LLM 避免同族扎堆）
        crowd = f" [同簇{prefix_counts.get(pfx, 0)}]" if prefix_counts.get(pfx, 0) >= 5 else ""

        # VECTOR 类型感知：需要 vec_* 聚合后才可入普通骨架
        vec_mark = " [VECTOR-需vec_avg聚合]" if fid in vector_set else ""

        # 添加质量评分标记
        quality_mark = ""
        if fid in field_scores:
            score = field_scores[fid]["score"]
            if score >= 0.8:
                quality_mark = " [HIGH-QUALITY]"
            elif score >= 0.6:
                quality_mark = " [RECOMMENDED]"
            elif score < 0.4:
                quality_mark = " [LOW-QUALITY]"

        sig_lines.append(f"- {fid}{quality_mark}{vec_mark}{crowd}  [{freq}, windows {win}]  {desc[:120]}")
    sig_block = "\n".join(sig_lines) if sig_lines else "(none)"

    scale_lines = []
    for fid in field_layers["scale"]:
        desc = (descriptions.get(fid) or "").strip()
        scale_lines.append(f"- {fid}  {desc[:100]}")
    scale_block = "\n".join(scale_lines) if scale_lines else "(none)"

    # 经济机制知识库（P3 优化：区域特化 + 数据集形状感知裁剪）
    econ_kb_block = ""
    if enable_econ_kb:
        try:
            _ensure_wqb_tools_path()
            from economic_mechanism_kb import get_mechanisms_by_family, format_mechanism_for_prompt
            # 根据数据集类别获取相关机制
            category = _infer_category_from_dataset(dataset_id)
            mechanisms = get_mechanisms_by_family(category)
            if mechanisms:
                econ_lines = ["## Economic Mechanisms (validated, with citations)"]
                # 数据集形状感知：候选字段少 → 少塞机制（防 prompt 稀释、防机制与字段脱节）
                take_n = 3 if len(field_layers["signal"]) >= 12 else 2
                for mech in mechanisms[:take_n]:
                    econ_lines.append(format_mechanism_for_prompt(mech["id"], region))
                    econ_lines.append("")
                econ_kb_block = "\n".join(econ_lines)
        except Exception as e:
            _warn(f"Economic mechanism KB failed: {e}")

    # 经济学机制模板库（P3 优化：category-aware 选择 + 空集保底）
    econ_templates_block = ""
    if enable_econ_kb:
        try:
            _ensure_wqb_tools_path()
            from economic_mechanism_templates import (
                get_all_p0_templates,
                get_all_p1_templates,
                get_backfill_alternatives,
            )

            # 根据数据集类别选择相关模板（文本弱匹配；未命中 → 保底 P0 前 2 条）
            category = _infer_category_from_dataset(dataset_id)
            p0_templates = get_all_p0_templates()
            p1_templates = get_all_p1_templates()
            relevant_templates = [t for t in p0_templates
                                  if _tpl_matches_category(t, category)]
            relevant_templates += [t for t in p1_templates
                                   if _tpl_matches_category(t, category)]
            if not relevant_templates:
                relevant_templates = p0_templates[:2]

            # ts_backfill 替代方案
            backfill_alts = get_backfill_alternatives()
            
            if relevant_templates or backfill_alts:
                tmpl_lines = ["## Economic Mechanism Templates (complex, with citations)"]
                tmpl_lines.append("")
                tmpl_lines.append("### High-Priority Mechanisms (P0)")
                for i, tmpl in enumerate(relevant_templates[:5], 1):  # 取前5个
                    tmpl_lines.append(f"{i}. {tmpl['name']}")
                    tmpl_lines.append(f"   Expression: `{tmpl['expression']}`")
                    tmpl_lines.append(f"   Logic: {tmpl['economic_logic']}")
                    tmpl_lines.append("")
                
                if backfill_alts:
                    tmpl_lines.append("### ts_backfill Alternatives (reduce overuse)")
                    for i, alt in enumerate(backfill_alts[:3], 1):  # 取前3个
                        tmpl_lines.append(f"{i}. {alt['name']}")
                        tmpl_lines.append(f"   Expression: `{alt['expression']}`")
                        tmpl_lines.append(f"   Use Case: {alt['use_case']}")
                        tmpl_lines.append("")
                
                econ_templates_block = "\n".join(tmpl_lines)
        except Exception as e:
            _warn(f"Economic mechanism templates failed: {e}")

    # 市场状态适配（P2 优化）
    market_regime_block = ""
    if enable_market_regime:
        try:
            _ensure_wqb_tools_path()
            from market_regime_adapter import MarketRegimeAdapter
            adapter = MarketRegimeAdapter()
            regime = adapter.detect_regime(region)
            market_regime_block = f"""## Market Regime (current)
- Regime: {regime['regime']}
- Volatility: {regime['volatility']:.1%}
- Trend Strength: {regime['trend_strength']:.1%}
- Preferred Sign: {'+' if regime['preferred_sign'] > 0 else '-'}1
- Reason: {regime['reason']}
"""
        except Exception as e:
            _warn(f"Market regime detection failed: {e}")

    # 窗口规则块（P2 动态化：实际生效窗口池随 campaign override 展示）
    win_rule_lines = []
    for freq_key, label in (
        ("low_freq", "low_freq fields (quarterly/annual fundamentals): align to disclosure cycle"),
        ("event", "event fields (news/announcement): capture short-lived shocks"),
        ("daily", "daily fields"),
    ):
        note = " [campaign override]" if (window_pool or {}).get(freq_key) else ""
        win_rule_lines.append(
            f"- {label}: windows {window_domains[freq_key]}{note} — choose ONLY from this pool.")
    win_rule_block = "\n".join(win_rule_lines)

    win_families_str = ", ".join(
        sorted({s["family"] for s in SKELETONS if s["needs_window"]}))
    two_field_ids_str = ", ".join(
        s["id"] for s in SKELETONS if s["n_fields"] == 2)

    system_prompt = f"""You are a quantitative alpha researcher designing economically meaningful alpha expressions for the WorldQuant BRAIN platform.

You do NOT write expression strings directly. You fill SLOTS into pre-validated operator SKELETONS. The code assembles the final expressions, so syntax is guaranteed — your job is ECONOMIC SEMANTICS: pick the right field, the right skeleton family, the right window, and the right direction.

## Available skeletons (operator topologies)
{skel_block}

## Window selection rules
{win_rule_block}
- Prefer the window matching the economic horizon of your hypothesis.

## Output format (STRICT)
Return ONLY a JSON array. Each element:
{{
  "field": "<signal field id>",
  "skeleton_id": "<one of the ids above>",
  "window": <int, required for families: {win_families_str}>,
  "sign": <1 or -1>,
  "field2": "<second field id, required for: {two_field_ids_str}>",
  "weight": <0.3-0.7, only for interact.weighted_mix>,
  "rationale": "<ONE sentence: the economic hypothesis, e.g. 'analysts revising gross-margin upward signal improving profitability'>"
}}

## Hard rules
- "field" MUST come from the SIGNAL field list below. Never use metadata fields (periodend/periodtype/fyearend/...).
- NEVER pick a field marked [VECTOR-需vec_avg聚合] as "field": VECTOR fields need vec_avg()/vec_sum() aggregation first — these skeletons cannot host them directly.
- Fields marked [同簇N] (N≥5) share a crowded prefix cluster: select at most 2 of them in total.
- "window" MUST be one of the values listed for that field's frequency domain.
- "field2" for interact.weighted_mix may come from SIGNAL or SCALE lists.
- Do not produce two entries that differ ONLY by window for the same (family, field) more than twice.
- Diversify across families: aim for coverage of at least 4 different families.
- sign=-1 means you hypothesize the effect is REVERSED (e.g. high X → low future returns). State this in rationale.
- PRIORITIZE fields marked [HIGH-QUALITY] or [RECOMMENDED].
"""

    # 添加经济机制知识库
    if econ_kb_block:
        system_prompt += f"\n{econ_kb_block}\n"

    # 添加经济学机制模板库
    if econ_templates_block:
        system_prompt += f"\n{econ_templates_block}\n"

    # 添加市场状态
    if market_regime_block:
        system_prompt += f"\n{market_regime_block}\n"

    if region_priors:
        system_prompt += f"""
## Region priors (empirical, from prior campaigns in {region})
{region_priors}
"""

    user_prompt = f"""Dataset: {dataset_id} | Region: {region} | Delay: {delay}

## SIGNAL fields (use these as "field")
{sig_block}

## SCALE fields (auxiliary; only allowed as "field2" in interact.weighted_mix)
{scale_block}

Produce {n_slots} slot entries as a single JSON array. Cover at least 4 skeleton families. Prioritize fields whose description suggests economically interpretable quantities (margins, revisions, growth, leverage, valuation ratios) over raw levels."""

    return system_prompt, user_prompt


def _infer_category_from_dataset(dataset_id: str) -> str:
    """从 dataset_id 推断数据类别."""
    dataset_lower = dataset_id.lower()
    category_map = {
        "analyst": "analyst",
        "model": "model",
        "news": "news",
        "fundamental": "fundamental",
        "pv": "pv",
        "insider": "institutions",
        "option": "option",
        "risk": "risk",
    }
    for key, value in category_map.items():
        if key in dataset_lower:
            return value
    return "other"


# ---------------------------------------------------------------------------
# Region priors 加载（P2：wq-brain-ra-pipeline 区域 profile）
# ---------------------------------------------------------------------------

_PRIORS_BLOCK_RE = re.compile(
    r"^##\s*priors[^\n]*\n(.*?)(?=^##\s|\Z)", re.IGNORECASE | re.MULTILINE | re.DOTALL,
)


def _extract_priors_section(md_text: str) -> str:
    """从 region profile markdown 中提取 priors 段（## priors ... 到下一个 ## 前）。"""
    m = _PRIORS_BLOCK_RE.search(md_text)
    if m:
        body = m.group(1).strip()
        # 限长防爆 token
        return body[:2000]
    return ""


def load_region_priors(region: str) -> str:
    """按优先级探测 region profile 并提取 priors 段。

    探测顺序（2026-09-11 审计补齐主安装位与仓库副本）：
      1. $WQ_RA_PIPELINE_DIR/references/regions/<REGION>.md
      2. ~/.claude/skills/wq-brain-ra-pipeline/references/regions/<REGION>.md
      3. ~/.codex/skills/...（同上）
      4. 历史位 ~/.trae-cn/skills、~/.qoder-cn/skills
      5. 仓库自带 <repo>/Claude/skills/wq-brain-ra-pipeline/references/regions/<REGION>.md
    找不到返回空字符串（不报错，P2 为增强项非硬依赖）。
    """
    region = (region or "").strip().upper()
    if not region:
        return ""

    home = os.path.expanduser("~")  # noqa: F841  (保留：下方 env 覆盖与路径拼接仍用 home)
    candidates = []
    env_dir = os.environ.get("WQ_RA_PIPELINE_DIR", "").strip()
    if env_dir:
        candidates.append(os.path.join(env_dir, "references", "regions", f"{region}.md"))
    candidates.extend(candidate_paths_under_skill(
        "wq-brain-ra-pipeline", "references", "regions", f"{region}.md"))

    for path in candidates:
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                priors = _extract_priors_section(text)
                if priors:
                    return priors
                # 文件存在但无 priors 段：提取 one_liner / static 摘要兜底
                lines = [ln for ln in text.splitlines()
                         if ln.strip().startswith("-") and len(ln) < 200][:8]
                return "\n".join(lines)
        except OSError:
            continue
    return ""
