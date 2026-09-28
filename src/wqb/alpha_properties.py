# -*- coding: utf-8 -*-
"""Alpha 提交属性规范（name / color / tags）—— 规范的**单一事实源**。

依据 `docs/alpha_properties_spec.md`，全部约束来自**平台实测**（2026-09-20）：

- `color`：平台**硬枚举，仅 5 个合法值**，其余一律 400 `"X" is not a valid choice.`
- `tags` / `name`：平台**零约束**（实测 30 个标签、100 字符标签、含空格/斜杠/中文均可）
  → 一致性只能靠本模块。

设计原则
--------
1. **平台有的，不复用 tag**：塔（`pyramids`）、类型（`classifications`）、区域、作者、
   生命周期（`stage`）、PROD/SELF 数值 —— 平台原生返回，打 tag 是冗余。
2. **`favorite` / `hidden` 能表达的，优先用原生布尔**。
3. **name 不放会变的数值**（PROD 值是提交时快照，写进 name 会骗人）。
4. 一颗 alpha 最多 4–5 个 tag —— 控制台按 tag 筛，越多越难筛。

用法
----
    from wqb.alpha_properties import build_name, build_tags, COLORS

    build_name("IND", "REGULAR", "pvrevgate", 1)   # 'IND_R_pvrevgate_01'
    build_tags(channel="REGULAR", dataset="insiders1", wave="113",
               expr_family="insgate", prod=0.65, self_=0.64)
    # ['CH_REG', 'SRC_insiders1', 'W113', 'EXPRFAM_insgate', 'CORR_NEAR']
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

__all__ = [
    "COLORS",
    "COLOR_PENDING",
    "COLOR_HEALTHY",
    "COLOR_DEGRADED",
    "COLOR_TO_RETIRE",
    "COLOR_PPA",
    "CHANNEL_REGULAR",
    "CHANNEL_PPA",
    "CHANNEL_SUPER",
    "CORR_LOW",
    "CORR_NEAR",
    "CORR_RED_LINE",
    "MAX_TAGS",
    "validate_color",
    "build_name",
    "build_tags",
    "check_tags",
]

# ---------------------------------------------------------------- color

#: 平台合法 color 枚举（实测：其余值均 400）
COLORS = ("GREEN", "BLUE", "RED", "YELLOW", "PURPLE")

COLOR_PENDING = "BLUE"     # 已提交 · 待观察（**提交默认态**）
COLOR_HEALTHY = "GREEN"    # 已提交 · OS 表现正常（须由 OS 结果挣得，禁当默认值）
COLOR_DEGRADED = "YELLOW"  # 已提交 · 指标退化，待复核
COLOR_TO_RETIRE = "RED"    # 已提交 · 待退役
COLOR_PPA = "PURPLE"       # PPA 通道专用

# ---------------------------------------------------------------- 通道

CHANNEL_REGULAR = "CH_REG"
CHANNEL_PPA = "CH_PPA"
CHANNEL_SUPER = "CH_SUPER"

_CHANNEL_BY_TYPE = {
    "REGULAR": CHANNEL_REGULAR,
    "SUPER": CHANNEL_SUPER,
}

# ---------------------------------------------------------------- 相关性档

CORR_LOW = "CORR_LOW"        # 双闸余量充裕（SA 组池优先）
CORR_NEAR = "CORR_NEAR"      # 贴近红线，提交前需复检

CORR_RED_LINE = 0.70         # 平台硬闸
CORR_LOW_MAX = 0.55          # PROD/SELF 均低于此 → CORR_LOW
CORR_NEAR_MIN = 0.65         # 任一达到此 → CORR_NEAR

#: 单颗 alpha 的 tag 数量上限（防膨胀：控制台按 tag 筛，越多越难筛）
MAX_TAGS = 5

_REGION_OK = re.compile(r"^[A-Z]{3}$")
_FAMILY_OK = re.compile(r"^[a-z0-9_]{1,18}$")


def validate_color(color: Optional[str]) -> Optional[str]:
    """校验 color 是否在平台枚举内；非法则抛 ValueError（None 放行=不设置）。"""
    if color is None:
        return None
    c = color.strip().upper()
    if c not in COLORS:
        raise ValueError(
            f"color={color!r} 非法：平台仅接受 {COLORS}（其余 400 'not a valid choice'）")
    return c


# ---------------------------------------------------------------- name

def build_name(region: str, alpha_type: str, family: str, seq: int = 1) -> str:
    """按规范生成 name：`<REGION>_<R|S>_<family>_<seq>`。

    >>> build_name("IND", "REGULAR", "pvrevgate", 1)
    'IND_R_pvrevgate_01'

    禁止把 PROD 数值放进 name（提交时快照，会过期骗人）。
    """
    r = (region or "").strip().upper()
    if not _REGION_OK.match(r):
        raise ValueError(f"region 必须是 3 位大写区域码，收到 {region!r}")
    t = (alpha_type or "REGULAR").strip().upper()
    tag = "S" if t == "SUPER" else "R"
    fam = (family or "alpha").strip().lower()
    fam = re.sub(r"[^a-z0-9_]", "_", fam)[:18] or "alpha"
    if not 1 <= int(seq) <= 99:
        raise ValueError("seq 必须在 1..99")
    return f"{r}_{tag}_{fam}_{int(seq):02d}"


# ---------------------------------------------------------------- tags

def _corr_tag(prod: Optional[float], self_: Optional[float]) -> Optional[str]:
    vals = [v for v in (prod, self_) if v is not None]
    if not vals:
        return None
    if max(vals) >= CORR_RED_LINE:
        return None                      # 已超红线，不属"可提交"态
    if max(vals) >= CORR_NEAR_MIN:
        return CORR_NEAR
    if prod is not None and self_ is not None and prod < CORR_LOW_MAX and self_ < CORR_LOW_MAX:
        return CORR_LOW
    return None


def _sanitize_token(s: str, limit: int = 40) -> str:
    """把任意字符串规范成安全的标签片段：非字母数字→`_`，折叠、去首尾。

    平台虽接受任意字符（实测），但含 `/` 的 tag 在控制台筛选时易歧义，
    故统一净化。净化后为空则返回空串（调用方跳过）。
    """
    t = re.sub(r"[^A-Za-z0-9]+", "_", str(s)).strip("_")
    t = re.sub(r"_{2,}", "_", t)
    return t[:limit]


def build_tags(
    channel: Optional[str] = None,
    alpha_type: Optional[str] = None,
    dataset: Optional[str] = None,
    wave: Optional[str] = None,
    expr_family: Optional[str] = None,
    tool: Optional[str] = None,
    prod: Optional[float] = None,
    self_: Optional[float] = None,
    extra: Optional[List[str]] = None,
    max_tags: int = MAX_TAGS,
) -> List[str]:
    """按规范组装 tags（顺序即优先级，超限截断）。

    组装顺序：`CH_` → `SRC_` → `W` → `EXPRFAM_` → `CORR_` → `TOOL_` → extra

    >>> build_tags(alpha_type="REGULAR", dataset="insiders1", wave="113", expr_family="insgate")
    ['CH_REG', 'SRC_insiders1', 'W113', 'EXPRFAM_insgate']
    """
    out: List[str] = []
    ch = channel
    if not ch and alpha_type:
        ch = _CHANNEL_BY_TYPE.get(str(alpha_type).upper())
    if ch:
        out.append(ch)
    ds = _sanitize_token(dataset) if dataset else ""
    if ds and ds.lower() not in ("unknown", "none", "null"):
        out.append(f"SRC_{ds}")
    if wave:
        out.append(f"W{_sanitize_token(wave, 12)}")
    if expr_family:
        out.append(f"EXPRFAM_{_sanitize_token(expr_family)}")
    ct = _corr_tag(prod, self_)
    if ct:
        out.append(ct)
    if tool:
        out.append(f"TOOL_{_sanitize_token(tool, 20)}")
    if extra:
        out.extend(str(x) for x in extra if x)
    # 去重保序
    seen, dedup = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            dedup.append(t)

    # ★ 截断优先级（2026-09-20 修）：必打标签与人工作为**绝不能**被挤掉。
    #   旧逻辑按顺序硬截断，导致遗留标签多的 alpha（如 vRjqXeWA 带 5 个人工标签）
    #   把 `CH_REG` 挤出预算 → 结果与原文相同 → 被误判"已合规"，永远修不上。
    #   新优先级：必打(CH_/SRC_) > 人工 extra(RETIRE_* 等) > 可选规范(W/EXPRFAM_/CORR_/TOOL_)
    extra_set = {str(x) for x in (extra or []) if x}
    required = [t for t in dedup if t.startswith(("CH_", "SRC_"))]
    manual = [t for t in dedup if t in extra_set and t not in required]
    optional = [t for t in dedup if t not in required and t not in manual]
    keep_n = max(0, max_tags - len(required) - len(manual))
    return required + manual + optional[:keep_n]


def check_tags(tags: List[str]) -> List[str]:
    """返回规范告警列表（空 = 合规）。用于审计而不阻断。"""
    warn: List[str] = []
    if not tags:
        return ["无标签：至少应有 CH_* 与 SRC_*"]
    if not any(t.startswith("CH_") for t in tags):
        warn.append("缺 CH_*（通道）")
    if not any(t.startswith("SRC_") for t in tags):
        warn.append("缺 SRC_*（来源数据集）")
    if len(tags) > MAX_TAGS:
        warn.append(f"标签数 {len(tags)} 超过上限 {MAX_TAGS}")
    for t in tags:
        if re.fullmatch(r"[0-9]+(\.[0-9]+)?", t):
            warn.append(f"疑似把 PROD 数值当 tag：{t}（数值会过期，应放 description）")
    if "PowerPoolSelected" in tags and CHANNEL_PPA not in tags:
        warn.append("PowerPoolSelected 应仅用于真实 PPA 通道；普通提交请用 CH_REG；"
                    "若确为 PPA，请同时补 CH_PPA 以保持通道口径一致")
    return warn


# ---------------------------------------------------------------- SRC 来源解析

_FIELD_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

#: 进程内缓存：field_name → dataset name
_FIELD_DS_CACHE: dict = {}


def fields_of(expr: Optional[str]) -> List[str]:
    """从表达式提取**字段名**（非算子标识符）。

    判定与 `wqb.expression.skeleton` 同口径：token 后（跳过空白）紧跟 `(` 者是算子，否则是字段。

    >>> fields_of("rank(ts_mean(headline_item_count, 66))")
    ['headline_item_count']
    """
    if not expr:
        return []
    out: List[str] = []
    n = len(expr)
    for m in _FIELD_TOKEN.finditer(expr):
        j = m.end()
        while j < n and expr[j] in " \t":
            j += 1
        if j < n and expr[j] == "(":
            continue
        out.append(m.group(0))
    return out


#: 价量"管道"字段黑名单 —— 这些是表达式里的通用胶水，不代表信号来源。
#: 若参与投票会把 SRC_ 带偏到 PV 数据集（实测：触发器用 analyst 字段的 alpha 被标成 pv）。
_PLUMBING_FIELDS = frozenset({
    "close", "open", "high", "low", "volume", "vwap", "returns", "cap", "adv20",
    "sharesout", "dividend", "split", "country", "exchange", "currency", "market",
    "corr_last_trade_price_with_volume", "assets", "liabilities", "equity", "debt",
    "cash", "revenue", "sales", "income", "eps", "bookvalue",
})


def _is_plumbing(fname: str) -> bool:
    """判断字段是否为通用价量/财务管道字段（不参与 SRC_ 投票）。"""
    f = (fname or "").lower()
    if f in _PLUMBING_FIELDS:
        return True
    # session_1430to1430_final_trade_price 之类带 session_ 前缀的也属价量管道
    return f.startswith("session_")


def resolve_source_dataset(expr: Optional[str], db_path: Optional[str] = None) -> Optional[str]:
    """表达式 → 来源数据集名（供 `SRC_` 标签）。

    ★ **不要用 `alphas.dataset_id`** —— 那记的是**波次主数据集**，与字段真实归属常不符。
      实测：`Grb67d6O`（用 news 字段 `headline_item_count`）在本地库被记为
      `intraday_pv_feats`，据此打 `SRC_intraday_pv_feats` 是**错误且更有害**的标签。
    ★ 也**不直接多数投票** —— 表达式里的通用价量管道字段（`close`/`volume`/
      `corr_last_trade_price_with_volume`）数量常多于真正的信号字段，会把结果带偏到 PV 数据集。
      故先剔除管道字段（`_is_plumbing`），再对**剩余字段**多数投票。

    失败（无 fields 表 / 无命中）返回 None（调用方跳过 SRC_）。
    """
    import sqlite3 as _sq
    if not expr:
        return None
    if db_path is None:
        try:
            import os as _os
            here = _os.path.dirname(_os.path.abspath(__file__))
            for _ in range(4):
                cand = _os.path.join(here, "data", "wqb.db")
                if _os.path.isfile(cand):
                    db_path = cand
                    break
                here = _os.path.dirname(here)
        except Exception:
            db_path = None
    if not db_path:
        return None

    con = None
    try:
        con = _sq.connect(db_path, timeout=15)
        con.row_factory = _sq.Row
        if not con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='fields'").fetchone():
            return None

        def _ds(f):
            if f in _FIELD_DS_CACHE:
                return _FIELD_DS_CACHE[f]
            try:
                row = con.execute(
                    """SELECT d.name AS ds FROM fields fi
                       JOIN datasets d ON fi.dataset_id = d.id
                       WHERE fi.field_name = ? AND d.category IS NOT NULL
                       LIMIT 1""", (f,)).fetchone()
                ds = row["ds"] if row else None
            except Exception:
                ds = None
            _FIELD_DS_CACHE[f] = ds
            return ds

        fields = fields_of(expr)
        signal = [f for f in fields if not _is_plumbing(f)]
        pool = signal or fields           # 全是管道字段时退回全量（聊胜于无）
        hits = [d for d in (_ds(f) for f in pool) if d]
        if not hits:
            return None
        from collections import Counter as _C
        return _C(hits).most_common(1)[0][0]
    except Exception:
        return None
    finally:
        if con is not None:
            try:
                con.close()
            except Exception:
                pass


def source_dataset_debug(expr: Optional[str], db_path: Optional[str] = None) -> Dict[str, Any]:
    """诊断：返回字段分类与最终 SRC_ 依据（供人工核对，不参与生成）。"""
    fs = fields_of(expr)
    plumbing = [f for f in fs if _is_plumbing(f)]
    signal = [f for f in fs if not _is_plumbing(f)]
    return {
        "fields": fs,
        "plumbing": plumbing,
        "signal_fields": signal,
        "resolved": resolve_source_dataset(expr, db_path),
    }
