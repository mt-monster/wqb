# -*- coding: utf-8 -*-
"""submit_ready 队列的规范核心（single source of truth）。

用途
----
把「回测已过闸、但当天配额吃不下」的 alpha 持久化，避免遗忘。

三方共用本模块，保证判定口径与写入逻辑完全一致：
  1. CLI           `tools/submit_queue.py`
  2. 收批自动入队   `tools/harvest_multisim.py`（S3 收批后）
  3. 提交自动退役   `src/wqb/workflow/nodes/submit_alpha.py`（提交成功后）

设计要点
--------
- **提交层硬闸**（严于 IS 层）：未过闸者一律 `status='DEAD'`，不进默认视图。
- **相关性带时效**：`verified_at` + `verify()`，因为提交任何别的 alpha 都会
  改变生产池，旧 PROD 会失效（实证：EUR le8Y68K2 0.6929 → 0.9932）。
  `list_ready` 的每行附 `corr_age_hours`/`corr_stale`/`corr_stale_reason` 标注
  （2026-10-20 P1-4，见 `annotate_corr_freshness`；与 MCP `get_alpha_corr_metrics` 同词表）。
- 所有写操作容错：队列记账失败**绝不能**影响主流程（收批/提交）。
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ._common import default_db_path, _now
from ..db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口：WAL + busy_timeout 60s)

#: 分组轴抽取（表达式层）。导入失败时族签名退回「分组轴未知」档（保守：见 family_signature）。
try:
    from ..expression.skeleton import group_axes as _group_axes
except Exception:  # pragma: no cover - 表达式层不可用时的退化
    _group_axes = None


# 提交层硬门槛（与平台一致；turnover 上限取 config.GATES_PLATFORM，平台口径 1%–70%）
# 2026-09-21 根治：此前硬编码 turnover_hi=0.4 与平台 0.70 不符，把换手 0.45、其余全过的
# GLB 候选 d5bnE8jJ 误判 FAIL:HIGH_TURNOVER→DEAD；单一事实源是 src/wqb/config.py。
try:
    from ..config import GATES_PLATFORM as _GP, PLATFORM_CHECK_LINES as _PL
    _TURNOVER_HI = float(_GP["turnover_range"][1])
    _SHARPE, _FITNESS = float(_GP["sharpe_min"]), float(_GP["fitness_min"])
    _TWO_YEAR = float(_PL["low_2y_sharpe_min"])
except Exception:  # pragma: no cover - config 缺失时回退平台文档值
    _TURNOVER_HI, _SHARPE, _FITNESS, _TWO_YEAR = 0.70, 1.58, 1.0, 1.58
LIM = {
    "sharpe": _SHARPE,
    "fitness": _FITNESS,
    "two_year": _TWO_YEAR,
    "turnover_hi": _TURNOVER_HI,
    "prod": 0.7,
    "self": 0.7,
}

#: verified_by 取值里「来自平台实测」的一组：这些行的 prod/self/verified_at 是权威值，
#: 批量入队（alphas 表来源，verified_by='alphas'）不得覆盖它们（2026-09-20 实测：verify 刚写回
#: 3qX3Mp6O prod 0.6437，并行的 add-many 立刻用 alphas 表旧值 0.4853 覆盖回去）。
PLATFORM_VERIFIED_BY = ("API", "verify", "submit_verdict")

STATUS_READY = "READY"
STATUS_DEAD = "DEAD"
STATUS_EXPIRED = "EXPIRED"
STATUS_SUBMITTED = "SUBMITTED"
#: 同骨架去重时被更优兄弟取代（不是硬闸失败，故与 DEAD 区分）
STATUS_SUPERSEDED = "SUPERSEDED"

SCHEMA = """
CREATE TABLE IF NOT EXISTS submit_ready (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    alpha_id       TEXT    NOT NULL,
    region         TEXT    NOT NULL,
    universe       TEXT,
    delay          INTEGER,
    decay          INTEGER,
    neutralization TEXT,
    -- 2026-10-23（P1-3 族签名修复）：设置档补齐 —— 骨架签名要含**全部设置档**，
    -- 否则 decay=4/truncation=0.08 与 decay=20/truncation=0.05 会被判成同族。
    truncation      REAL,
    nan_handling    TEXT,
    max_trade      REAL,
    expr           TEXT,
    skeleton       TEXT,
    -- 2026-10-23（P1-3 族签名修复）：**族签名**（主体骨架 + 分组轴 + 全部设置档）。
    -- `skeleton` 保持旧口径（仅主体形状），以免破坏其它读方（tools/ledger/scan_backup_ra.py 等）；
    -- 去重/同族判定一律走 `family_sig`。
    family_sig     TEXT,
    suggested_tags TEXT,
    sharpe         REAL,
    fitness        REAL,
    turnover       REAL,
    two_year       REAL,
    sub_universe   REAL,
    cluster_test   REAL,
    -- ---- 2026-10-06：体检卡三层的台账落点（此前只存在于 alphas/backtest_results，
    --   submit_ready 完全没有 → 直连候选的 margin / 约束后表现全库不可见，
    --   体检卡每次只能绕过 DB 打平台 GET）。全部可空，不破坏既有数据。----
    margin         REAL,          -- 每单位换手收益，官方「好 alpha」三线之一（单位=小数，×1e4=bp）
    returns        REAL,          -- judge 六指标之一（年化收益，小数）
    drawdown       REAL,          -- 回报层风险项（最大回撤）
    long_count     INTEGER,       -- 多头持仓数（与 short_count 判多空均衡）
    short_count    INTEGER,       -- 空头持仓数
    -- LOW_INVESTABILITY_CONSTRAINED_SHARPE 是 RA_HARD_FAILS 里的硬闸 → 原始值必须可查。
    investability_constrained_sharpe REAL,
    -- 加钱层（VF 单α表现）：风险中性化后 sharpe，与 backtest_results.risk_neutralized_sharpe 同口径。
    risk_neutralized_sharpe          REAL,
    prod           REAL,
    self           REAL,
    gate           TEXT    DEFAULT 'UNVERIFIED',
    verified_at    TEXT,
    verified_by    TEXT,
    towers         TEXT,
    family         TEXT,
    status         TEXT    DEFAULT 'READY',
    added_at       TEXT,
    note           TEXT,
    UNIQUE(alpha_id, region)
);
CREATE INDEX IF NOT EXISTS ix_sr_region_status ON submit_ready(region, status);
CREATE INDEX IF NOT EXISTS ix_sr_status ON submit_ready(status);
-- 2026-09-28 自愈：P0 迁移「改名→新建同名表」重建 submit_ready 时**丢了 UNIQUE(alpha_id, region)**，
-- 而 `_backtest.py`/`submit_queue` 的入队 upsert 用 `ON CONFLICT(alpha_id,region)` →
-- 报 `ON CONFLICT clause does not match any PRIMARY KEY or UNIQUE constraint`，
-- **过闸候选静默不入队**（影响所有区域）。这里显式建唯一索引，使任何被迁移过的库
-- 一旦经本 store 打开即自动补回该约束（CREATE UNIQUE INDEX IF NOT EXISTS 幂等）。
CREATE UNIQUE INDEX IF NOT EXISTS ux_sr_alpha_region ON submit_ready(alpha_id, region);
"""


# ---------------- 判定 ----------------

#: 2026-09-20 坑 1：平台 RA 硬闸远不止 S/F/2Y/turnover——robust / sub-universe / CW / IS ladder /
#: investability 任一 FAIL 都不可提交。此前 36 条 LOW_ROBUST_UNIVERSE_SHARPE 的 IND 候选进了 READY。
RA_HARD_FAILS = (
    "LOW_ROBUST_UNIVERSE_SHARPE", "LOW_SUB_UNIVERSE_SHARPE", "CONCENTRATED_WEIGHT",
    "IS_LADDER_SHARPE", "LOW_INVESTABILITY_CONSTRAINED_SHARPE", "LOW_ROBUST_UNIVERSE_RETURNS",
    "LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE", "LOW_GLB_AMER_SHARPE", "LOW_GLB_EMEA_SHARPE",
    "LOW_GLB_APAC_SHARPE", "LOW_ASI_JPN_SHARPE", "LOW_RETURNS", "LOW_TURNOVER", "HIGH_TURNOVER",
    "LOW_SHARPE", "LOW_FITNESS", "LOW_2Y_SHARPE", "PROD_CORRELATION", "SELF_CORRELATION",
)


def ra_fail_of(ra_failed_checks) -> Optional[str]:
    """从 ra_failed_checks（list / JSON 字符串 / checks dict / None）取第一个硬闸 FAIL 名；无则 None。
    只认名字在 RA_HARD_FAILS 内的（PENDING/WARNING 不算）。"""
    if not ra_failed_checks:
        return None
    v = ra_failed_checks
    if isinstance(v, str):
        try:
            v = json.loads(v)
            if isinstance(v, str):  # 双重编码
                v = json.loads(v)
        except Exception:
            v = [x.strip().strip('"') for x in v.strip("[]").split(",") if x.strip()]
    if isinstance(v, dict):
        v = [c.get("name") for c in (v.get("fail") or []) if isinstance(c, dict)]
    for name in v or []:
        if isinstance(name, dict):
            name = name.get("name")
        if name in RA_HARD_FAILS:
            return str(name)
    return None


#: 2026-09-20 坑 2：口径**对齐 toolkit gate.py 闸5**（用户 2026-09-13「路线 A」定案）——
#: 判「加权混腿」：任一 add( 的顶层实参中 ≥2 个是「系数腿」（`0.4*x` 星号中缀 / `multiply(0.4, x)` /
#: `multiply(x, 0.4)` 函数式，含嵌套与镜像腿）。等权 add(rank(a),rank(b))、单腿缩放、
#: subtract(rank(A),rank(B))（闸5 列为合规替代）**不拦**，避免队列比流水线更严造成两套口径。
_ADD_OPEN_RE = re.compile(r"\badd\s*\(")
_COEF_PREFIX_RE = re.compile(r"^\s*-?\d*\.?\d+\s*\*")
_MUL_PREFIX_RE = re.compile(r"^\s*multiply\s*\(\s*-?\d*\.?\d+\s*,")
_MUL_SUFFIX_RE = re.compile(r"^\s*multiply\s*\(.*,\s*-?\d*\.?\d+\s*\)\s*$", re.S)


def _top_level_args(expr: str, start: int):
    """从 `add(` 左括号之后开始，括号平衡地切顶层实参。

    与 gate.py 的差异：括号**不平衡时不放弃**，返回已切出的实参（含未闭合的尾段）——
    上游截断的表达式里已经看到的「系数腿」是真实证据，截断不会凭空造出系数腿，
    故按部分实参判定不会误伤，只会少漏。"""
    depth, i, n = 1, start, len(expr)
    args: List[str] = []
    cur: List[str] = []
    while i < n and depth > 0:
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                break
        elif ch == "," and depth == 1:
            args.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    args.append("".join(cur))
    return args


def _is_coef_leg(arg: str) -> bool:
    a = arg.strip()
    if _COEF_PREFIX_RE.match(a) or _MUL_PREFIX_RE.match(a):
        return True
    if _MUL_SUFFIX_RE.match(a):
        inner = _top_level_args(a, a.index("(") + 1)
        return bool(inner) and len(inner) == 2 and re.fullmatch(r"\s*-?\d*\.?\d+\s*\)?\s*", inner[1] or "") is not None
    return False


#: 闸5 的三条正则毒模式（逐字取自 toolkit `config/platform_constraints.json::poison_patterns`，
#: name = weighted_signal_mix / weighted_leg_mix_func_prefix / weighted_leg_mix_func_suffix）。
#: 结构判定需要括号平衡；`alphas.expression` 有 516 条被上游截断到 110 字符（2026-09-20 实测），
#: 截断式括号必不平衡 → 结构判定「宁漏勿误」放行，故正则作兜底，两者取并集 = 闸5 全口径。
_MIX_REGEXES = (
    re.compile(r"\d*\.?\d+\s*\*\s*(?:rank|zscore|ts_rank|group_rank|normalize|scale)\s*\([^)]*\).{0,200}?"
               r"\d*\.?\d+\s*\*\s*(?:rank|zscore|ts_rank|group_rank|normalize|scale)\s*\("),
    re.compile(r"add\s*\(\s*multiply\s*\(\s*\d*\.\d+\s*,"),
    re.compile(r"add\s*\(\s*multiply\s*\([^;]*?\d*\.\d+\s*\)\s*,\s*multiply\s*\("),
)


def is_add_mix(expr: Optional[str]) -> bool:
    """加权混腿判定 = 闸5 全口径（结构判定 ∪ 三条正则），见 gate.py::check_one 闸5 段。"""
    if not expr:
        return False
    for m in _ADD_OPEN_RE.finditer(expr):
        args = _top_level_args(expr, m.end())
        if not args or len(args) < 2:
            continue
        if sum(1 for a in args if _is_coef_leg(a)) >= 2:
            return True
    return any(rx.search(expr) for rx in _MIX_REGEXES)


def is_pass(sharpe, fitness, two_year, turnover, prod, selfc, ra_failed_checks=None, expr=None):
    """提交层达标判定。prod/self 为 None 时该维度跳过（视为待测）。
    ra_failed_checks（平台 checks 的 FAIL 名单）与 expr（add 混腿）为 2026-09-20 新增硬闸。"""
    rf = ra_fail_of(ra_failed_checks)
    if rf:
        return False, "RA:" + rf
    if is_add_mix(expr):
        return False, "ADD_MIX"
    if sharpe is None or sharpe < LIM["sharpe"]:
        return False, "LOW_SHARPE"
    if fitness is None or fitness < LIM["fitness"]:
        return False, "LOW_FITNESS"
    if two_year is not None and two_year < LIM["two_year"]:
        return False, "LOW_2Y_SHARPE"
    if turnover is not None and turnover > LIM["turnover_hi"]:
        return False, "HIGH_TURNOVER"
    if prod is not None and prod >= LIM["prod"]:
        return False, "PROD"
    if selfc is not None and selfc >= LIM["self"]:
        return False, "SELF"
    return True, ""


def gate_of(sharpe, fitness, two_year, turnover, prod, selfc, ra_failed_checks=None, expr=None):
    """返回 (gate, status)。未过闸者一律不进 READY。"""
    ok, why = is_pass(sharpe, fitness, two_year, turnover, prod, selfc, ra_failed_checks, expr)
    if not ok:
        return "FAIL:" + why, STATUS_DEAD
    if prod is None or selfc is None:
        # IS 达标但相关性未测 → 可入队待验，提交前必须 verify
        return "IS_ONLY", STATUS_READY
    return "SUBMIT_LAYER_VERIFIED", STATUS_READY


def priority(row) -> float:
    """优先级 = fitness × 塔倍率 + 相关性余量 × 0.5。"""
    def g(k):
        try:
            return row[k]
        except (KeyError, IndexError, TypeError):
            return None
    fit = g("fitness") or 0.0
    margin = 0.0
    if g("prod") is not None:
        margin += (LIM["prod"] - g("prod"))
    if g("self") is not None:
        margin += (LIM["self"] - g("self"))
    mult = 1.0
    try:
        tw = json.loads(g("towers") or "[]")
        if tw:
            mult = max(float(t.get("multiplier", 1.0)) for t in tw)
    except Exception:
        pass
    return round(fit * mult + margin * 0.5, 4)


# ---------------- 连接与写入 ----------------

def connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    """打开连接。

    并发注意：本表会被多个入口同时写（MCP 服务、CLI、harvest 钩子、提交钩子），
    故必须设 busy timeout，否则并发时直接 `database is locked`。
    """
    con = db_connect(db_path or default_db_path())
    con.row_factory = sqlite3.Row
    try:
        con.execute("PRAGMA busy_timeout=30000")
    except sqlite3.Error:
        pass
    return con


def ensure_table(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA)
    _migrate(con)


def _migrate(con: sqlite3.Connection) -> None:
    """轻量迁移：老库补 `skeleton` 列与索引。

    注意顺序：**必须先补列再建索引** —— SCHEMA 里的 `CREATE TABLE IF NOT EXISTS`
    对已存在的表是 no-op，若把 skeleton 索引写在 SCHEMA 里，老库会因缺列而报
    `no such column: skeleton`（实测踩到）。
    """
    cols = {r[1] for r in con.execute("PRAGMA table_info(submit_ready)")}
    if "skeleton" not in cols:
        try:
            con.execute("ALTER TABLE submit_ready ADD COLUMN skeleton TEXT")
        except sqlite3.Error:
            return
    if "suggested_tags" not in cols:
        try:
            con.execute("ALTER TABLE submit_ready ADD COLUMN suggested_tags TEXT")
        except sqlite3.Error:
            pass
    # 2026-10-23（P1-3）：设置档三列自愈（族签名要含全部设置档）。
    # 与上面 7 列同理：老库只能靠 ALTER 补齐，补列不改既有数据。
    for _col, _ddl in (("truncation", "REAL"), ("nan_handling", "TEXT"), ("max_trade", "REAL"),
                       ("family_sig", "TEXT")):
        if _col not in cols:
            try:
                con.execute(f"ALTER TABLE submit_ready ADD COLUMN {_col} {_ddl}")
            except sqlite3.Error:
                pass
    # 2026-10-06：体检卡三层所需的 7 列（老库自愈）。SCHEMA 的 CREATE TABLE IF NOT EXISTS
    # 对已存在的表是 no-op，故老库只能靠这里 ALTER 补齐；顺序无关（都只补列）。
    for _col, _ddl in (
        ("margin", "REAL"),
        ("returns", "REAL"),
        ("drawdown", "REAL"),
        ("long_count", "INTEGER"),
        ("short_count", "INTEGER"),
        ("investability_constrained_sharpe", "REAL"),
        ("risk_neutralized_sharpe", "REAL"),
    ):
        if _col not in cols:
            try:
                con.execute(f"ALTER TABLE submit_ready ADD COLUMN {_col} {_ddl}")
            except sqlite3.Error:
                pass
    try:
        con.execute("CREATE INDEX IF NOT EXISTS ix_sr_skeleton ON submit_ready(skeleton)")
    except sqlite3.Error:
        pass
    con.commit()


def _tags_for(rec: Dict[str, Any], db_path: Optional[str] = None) -> str:
    """按属性规范生成建议 tags（JSON 字符串），供提交时直接使用。

    规范见 `docs/alpha_properties_spec.md`；生成器 `wqb.alpha_properties.build_tags`。
    ★ `SRC_` 用 `resolve_source_dataset(expr)` **按表达式字段反查**，
      **不用 `alphas.dataset_id`**（那是波次主数据集，实测与字段真实归属不符）。
    生成失败返回 "[]"（不影响入队）。
    """
    try:
        from ..alpha_properties import build_tags, resolve_source_dataset
        ds = resolve_source_dataset(rec.get("expr"), db_path)
        return json.dumps(build_tags(
            alpha_type=rec.get("alpha_type") or "REGULAR",
            dataset=ds,
            wave=rec.get("wave"),
            expr_family=_family_of(rec.get("skeleton") or _sig(rec.get("expr"))),
            prod=rec.get("prod"),
            self_=rec.get("self"),
        ), ensure_ascii=False)
    except Exception:  # noqa: BLE001
        return "[]"


def _family_of(skeleton: str) -> str:
    """骨架签名 → 短族名（供 EXPRFAM_ 用）。

    取签名里最外层的算子序列，做可读的稳定短名；空签名返回空串。
    新格式族签名（`FAM2|…`）先剥外壳再取算子序列（否则会把设置档里的 token 混进来）。
    """
    if not skeleton:
        return ""
    if skeleton.startswith(FAMILY_SIG_PREFIX):
        parts = skeleton.split("|")
        skeleton = parts[1] if len(parts) > 1 else ""
    import re as _re
    ops = _re.findall(r"([a-z_][a-z0-9_]*)\s*(?=\()", skeleton)
    if not ops:
        return ""
    return "_".join(ops[:2])[:24]


def _sig(expr: Optional[str]) -> str:
    """表达式 → 结构骨架签名（**仅主体形状**，不含分组轴/设置档）。

    复用权威实现 `wqb.expression.skeleton::structural_signature`
    （字段/分组变量→F、数字→N、算子按"后紧跟 ("识别），
    口径与 `tools/pool_diversity.py`、`tools/backfill_skeletons.py` 一致。
    导入失败时返回空串（去重降级为不去重，不影响入队）。

    ⚠ **别拿它当"同族"判据**：它会抹掉分组轴与设置档（见 `family_signature`）。
    """
    if not expr:
        return ""
    try:
        from ..expression.skeleton import structural_signature
        return structural_signature(expr)
    except Exception:  # noqa: BLE001
        return ""


# ---------------------------------------------------------------------------
# 族签名（2026-10-23 USA 事故修复；报告 `reports/usa_mining_history_review_20261023.md` P1-3）
# ---------------------------------------------------------------------------
#: 族签名前缀。带此前缀 = 新格式（主体 + 分组轴 + 设置档）；不带 = 旧格式（仅主体）。
FAMILY_SIG_PREFIX = "FAM2|"

#: 设置档成分（提交层「完整设置档」）。**成分集合固定** ⇒ 任意来源的行两两可比。
SETTINGS_COMPONENTS = ("decay", "truncation", "neutralization", "universe",
                       "nan_handling", "max_trade", "delay")

#: 平台 settings 的键名别名（平台 camelCase ↔ 本地 snake_case；`neut` 是本地 payload 的叫法）。
_SETTINGS_ALIASES = {
    "decay": ("decay",),
    "truncation": ("truncation",),
    "neutralization": ("neutralization", "neut"),
    "universe": ("universe",),
    "nan_handling": ("nan_handling", "nanHandling", "nan_handling_mode"),
    "max_trade": ("max_trade", "maxTrade"),
    "delay": ("delay",),
}

#: 未知成分的占位符。**刻意不等于任何真实取值** ⇒ 未知行与已知行判为不同族（保守）。
_UNKNOWN = "?"


def _norm_setting_value(comp: str, v: Any) -> Any:
    """设置档成分值归一（数值转数字、枚举转大写串）。"""
    if comp in ("truncation", "max_trade"):
        try:
            return round(float(v), 6)
        except (TypeError, ValueError):
            return str(v).strip().upper()
    if comp in ("decay", "delay"):
        try:
            return int(v)
        except (TypeError, ValueError):
            pass
        try:
            return round(float(v), 6)
        except (TypeError, ValueError):
            return str(v).strip().upper()
    return str(v).strip().upper()


def normalize_settings(settings: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """设置档 → 归一化字典（**只含取得到的成分**；键名大小写不敏感）。

    接受平台 settings（``nanHandling`` / ``maxTrade``）、本地队列列（snake_case）
    与 payload 的简写（``neut``）。
    """
    if not settings or not isinstance(settings, Mapping):
        return {}
    lower = {str(k).lower(): v for k, v in settings.items()}
    out: Dict[str, Any] = {}
    for comp, aliases in _SETTINGS_ALIASES.items():
        for alias in aliases:
            if alias.lower() not in lower:
                continue
            v = lower[alias.lower()]
            if v is None or (isinstance(v, str) and not v.strip()):
                break
            out[comp] = _norm_setting_value(comp, v)
            break
    return out


def settings_profile(settings: Optional[Mapping[str, Any]]) -> str:
    """设置档 → 规范串（成分集合固定，未知记 ``?``）。

    **一个成分都取不到 ⇒ 返回空串** ⇒ 调用方据此做保守降级（该行判为独立族）。
    """
    norm = normalize_settings(settings)
    if not norm:
        return ""
    return ";".join("%s=%s" % (c, norm.get(c, _UNKNOWN)) for c in SETTINGS_COMPONENTS)


def _settings_of_rec(rec: Mapping[str, Any]) -> Dict[str, Any]:
    """入队记录 → 设置档（顶层列 + ``rec['settings']`` 子字典，平台 camelCase 亦可）。"""
    out: Dict[str, Any] = {c: rec.get(c) for c in SETTINGS_COMPONENTS}
    sub = rec.get("settings")
    if isinstance(sub, Mapping):
        for k, v in normalize_settings(sub).items():
            if out.get(k) is None:
                out[k] = v
    return {k: v for k, v in out.items() if v is not None}


def _settings_of_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    """队列表行 → 设置档（该行自带的列）。"""
    return {c: row.get(c) for c in SETTINGS_COMPONENTS if row.get(c) is not None}


def _json_obj(raw: Any) -> Dict[str, Any]:
    """JSON 文本/dict → dict（解析失败返回空 dict，不抛）。"""
    if isinstance(raw, Mapping):
        return dict(raw)
    if not raw:
        return {}
    try:
        d = json.loads(raw)
    except Exception:  # noqa: BLE001
        return {}
    return d if isinstance(d, dict) else {}


def family_parts(expr: Optional[str], settings: Optional[Mapping[str, Any]] = None,
                 row_key: Optional[str] = None) -> Dict[str, Any]:
    """族签名的**结构化分解**（供同族比较用）。

    Returns: {"body": 主体骨架, "axes": 分组轴元组 or None（未知）, "settings": 归一化设置档,
              "unique": 降级标记（设置档全空时的行级唯一键）}
    """
    body = _sig(expr)
    axes: Optional[Tuple[str, ...]] = None
    if _group_axes is not None:
        axes = tuple(_group_axes(expr or ""))
    norm = normalize_settings(settings)
    unique = ""
    if not norm:
        unique = str(row_key) if row_key else hashlib.sha1(body.encode("utf-8")).hexdigest()[:12]
    return {"body": body, "axes": axes, "settings": norm, "unique": unique}


def _same_family(a: Mapping[str, Any], b: Mapping[str, Any]) -> bool:
    """同族判定（**通配语义**：只有「两侧都知道且不同」才算不同族）。

    为什么用通配而不是字符串全等（2026-10-23 P1-3 落地时的实测）：
    - 严格全等下，**设置档一项都没记到的行**（老队列行、最小 fixture、alphas 镜像缺 decay）
      只能落成「行级唯一标记」⇒ 与所有兄弟判为不同族 ⇒ PROD_SIBLING 保护**整条失效**
      （实测 `test_regrade_ready_applies_new_gates_to_legacy_rows` 因此红）。
    - 通配语义下：**两侧都知道且不同**才分族；一侧未知 ⇒ 放行。
      ⇒ 记账不全的兄弟仍能被连坐（保护不失效），而真正不同族的
      `group_rank(·, subindustry)` vs `group_rank(·, industry)`、
      `neutralization=SUBINDUSTRY` vs `MARKET` 仍被判为不同族（误杀不复发）。

    判别优先级：**主体骨架**必须相同（不同 ⇒ 必然不同族）→ 分组轴 → 设置档逐项。
    """
    if not a.get("body") or not b.get("body"):
        return False
    if a["body"] != b["body"]:
        return False
    ax_a, ax_b = a.get("axes"), b.get("axes")
    if ax_a is not None and ax_b is not None and tuple(ax_a) != tuple(ax_b):
        return False
    for comp in SETTINGS_COMPONENTS:
        va = (a.get("settings") or {}).get(comp)
        vb = (b.get("settings") or {}).get(comp)
        if va is not None and vb is not None and va != vb:
            return False
    return True


def family_signature(expr: Optional[str], settings: Optional[Mapping[str, Any]] = None,
                     row_key: Optional[str] = None) -> str:
    """族签名 = **主体骨架 + 分组轴 + 设置档**（三段缺一不可）。

    为什么必须补这两段（2026-10-23 USA 真实事故，见报告 §9.3）：
    - **分组轴**：``group_rank(x, industry)`` 与 ``group_rank(x, sector)`` 的主体形状
      **完全一样**（分组变量在主体签名里被替换成 ``F``）。只按主体去重 ⇒ 不同信号族
      被当成同族：USA ``d5KzLo7v``（``group_rank(·, subindustry)`` + SUBINDUSTRY 中性化）
      与 ``zqrGqVXo``（``group_rank(·, industry)`` + MARKET 中性化）被判同族，
      前者被误标 ``PROD_SIBLING`` 判死 —— 而它其实是全 USA 唯一同时过 prod/self
      双闸、且落在未点亮塔的候选。
    - **设置档**：``rank(ts_mean(x, 22))`` 在 decay=4/truncation=0.08 与
      decay=20/truncation=0.05 下是**两种持仓行为**，不能算同族。

    ⚠ **字符串签名的口径是「严格」**（去重用）：设置档一个成分都取不到 ⇒ 该行自带唯一
    标记 ⇒ 判为「不同族」。宁可漏去重一次，也不把不同族判成同族（错杀一颗好候选）。
    兄弟连坐（PROD_SIBLING）走 `_same_family` 的**通配**口径，两者刻意不同。

    Args:
        expr: 表达式（主体形状 + 分组轴的来源）
        settings: 该 alpha 的设置档（平台 settings / 队列列 / 片段）
        row_key: 行级唯一键（alpha_id）；降级时用它保证「每行独立一族」
    """
    parts = family_parts(expr, settings, row_key)
    body = parts["body"]
    if not body:
        return ""
    axes = "|".join(parts["axes"]) if parts["axes"] is not None else _UNKNOWN
    prof = settings_profile(settings)
    if not prof:
        prof = "NOSETTINGS#%s" % parts["unique"]
    return "%s%s|%s|%s" % (FAMILY_SIG_PREFIX, body, axes, prof)


def family_signature_of_row(row: Mapping[str, Any]) -> str:
    """队列表行 → 族签名（表达式 + 该行自带的设置档列）。"""
    return family_signature(row.get("expr"), _settings_of_row(row),
                            row_key=row.get("alpha_id"))


def family_parts_of_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    """队列表行 → 族签名的结构化分解（兄弟连坐比较用）。"""
    return family_parts(row.get("expr"), _settings_of_row(row),
                        row_key=row.get("alpha_id"))


def _prod_wall_sibling(con: sqlite3.Connection, region: Optional[str], expr: Optional[str],
                       alpha_id: Optional[str], own_parts: Optional[Mapping[str, Any]] = None):
    """同区域、**同族**（主体 + 分组轴 + 设置档）的其它 alpha 若已实测 prod>=LIM['prod']，
    返回 (alpha_id, prod)；否则 None。

    ⚠ 2026-10-23：族签名从「只有表达式主体形状」升级为「主体 + 分组轴 + 设置档」。
    旧口径把 ``group_rank(·, subindustry)`` 与 ``group_rank(·, industry)`` 判成同族，
    USA ``d5KzLo7v`` 因此被误标 PROD_SIBLING 判死（它与 ``zqrGqVXo`` 只是中性化域不同）。

    判定用 **`_same_family` 通配口径**（不是字符串全等）：一侧设置档未知 ⇒ 放行。
    理由：老队列行 / alphas 镜像普遍缺 decay·truncation ⇒ 全等会把兄弟保护**整条失效**；
    而「两侧都知道且不同」的组（不同分组轴 / 不同中性化）仍被正确分开 ⇒ 误杀不复发。

    Args:
        own_parts: 本条自身的族分解（`family_parts`，须含本条真实设置档）；
                   省略时从 ``expr`` 现算（设置档按未知处理）。
                    数据源 = 队列表自身（prod）+ alphas 表（prod_correlation）；**逐行重算**，
    不依赖存量 ``skeleton`` 列的格式（旧格式行自然不匹配 ⇒ 保守）。
    任何异常降级为 None（不连坐）。
    """
    own = dict(own_parts) if own_parts is not None else family_parts(expr, None)
    if not own.get("body") or not region:
        return None
    try:
        for r in con.execute(
                "SELECT alpha_id, expr, universe, delay, decay, neutralization, "
                "truncation, nan_handling, max_trade, prod FROM submit_ready "
                "WHERE region=? AND alpha_id<>? AND prod IS NOT NULL AND prod>=?",
                (region, alpha_id or "", LIM["prod"])):
            row = dict(r)
            if _same_family(family_parts_of_row(row), own):
                return row["alpha_id"], float(row["prod"])
    except sqlite3.Error:
        return None
    try:
        rid = con.execute("SELECT id FROM regions WHERE name=?", (region,)).fetchone()
        if not rid:
            return None
        for r in con.execute(
                "SELECT alpha_id, expression, universe, delay, neutralization, "
                "prod_correlation FROM alphas WHERE region_id=? AND prod_correlation>=? "
                "AND expression IS NOT NULL LIMIT 2000",
                (rid[0], LIM["prod"])):
            row = dict(r)
            row["expr"] = row.pop("expression", None)
            if row.get("alpha_id") == alpha_id:
                continue
            if _same_family(family_parts_of_row(row), own):
                return row["alpha_id"], float(row["prod_correlation"])
    except sqlite3.Error:
        return None
    return None


def _upsert(con: sqlite3.Connection, rec: Dict[str, Any], note: str = "") -> str:
    gate, st = gate_of(rec.get("sharpe"), rec.get("fitness"), rec.get("two_year"),
                       rec.get("turnover"), rec.get("prod"), rec.get("self"),
                       rec.get("ra_failed_checks"), rec.get("expr"))
    expr = rec.get("expr")
    # 2026-10-23（P1-3）：**族签名** = 主体骨架 + 分组轴 + 全部设置档。
    # 设置档一个成分都取不到 ⇒ 字符串签名里自带行级唯一标记（去重侧保守降级）；
    # 兄弟连坐侧走 `_same_family` 通配口径（见该函数：一侧未知 ⇒ 放行，保护不失效）。
    own_parts = family_parts(expr, _settings_of_rec(rec), row_key=rec.get("alpha_id"))
    fam = family_signature(expr, _settings_of_rec(rec), row_key=rec.get("alpha_id"))
    # 坑 2b：同族兄弟已实测 prod>=0.7 而本条 prod 未测 → 标 DEAD（FAIL:PROD_SIBLING）；
    # verify/add 实测 prod<0.7 时 mark_verified 可复活。避免"裸主腿 0.8 撞墙家族"靠 prod=None 混进 READY。
    # ⚠ 判据必须是**族分解**而非主体骨架：只按主体形状会把不同分组轴/不同中性化的
    #   不同信号族连坐（USA d5KzLo7v 事故，见 reports/usa_mining_history_review_20261023.md §9.3）。
    if st == STATUS_READY and rec.get("prod") is None and expr:
        sib = _prod_wall_sibling(con, rec.get("region"), expr, rec.get("alpha_id"),
                                 own_parts=own_parts)
        if sib:
            gate, st = "FAIL:PROD_SIBLING(%s=%.2f)" % sib, STATUS_DEAD
    vb = rec.get("verified_by") or (
        "API" if (rec.get("prod") is not None or rec.get("self") is not None) else "IS_only")
    con.execute(
        """INSERT INTO submit_ready
        (alpha_id,region,universe,delay,decay,neutralization,truncation,nan_handling,max_trade,
         expr,skeleton,family_sig,suggested_tags,
         sharpe,fitness,turnover,two_year,sub_universe,cluster_test,
         margin,returns,drawdown,long_count,short_count,
         investability_constrained_sharpe,risk_neutralized_sharpe,
         prod,self,
         gate,verified_at,verified_by,towers,family,status,added_at,note)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(alpha_id,region) DO UPDATE SET
          sharpe=excluded.sharpe, fitness=excluded.fitness, turnover=excluded.turnover,
          two_year=excluded.two_year,
          sub_universe=COALESCE(excluded.sub_universe, submit_ready.sub_universe),
          cluster_test=COALESCE(excluded.cluster_test, submit_ready.cluster_test),
          expr=COALESCE(excluded.expr, submit_ready.expr),
          margin=COALESCE(excluded.margin, submit_ready.margin),
          returns=COALESCE(excluded.returns, submit_ready.returns),
          drawdown=COALESCE(excluded.drawdown, submit_ready.drawdown),
          long_count=COALESCE(excluded.long_count, submit_ready.long_count),
          short_count=COALESCE(excluded.short_count, submit_ready.short_count),
          investability_constrained_sharpe=COALESCE(
              excluded.investability_constrained_sharpe,
              submit_ready.investability_constrained_sharpe),
          risk_neutralized_sharpe=COALESCE(
              excluded.risk_neutralized_sharpe, submit_ready.risk_neutralized_sharpe),
          prod=excluded.prod, self=excluded.self,
          gate=excluded.gate, verified_at=excluded.verified_at,
          verified_by=excluded.verified_by, towers=excluded.towers,
          skeleton=COALESCE(excluded.skeleton, submit_ready.skeleton),
          family_sig=COALESCE(excluded.family_sig, submit_ready.family_sig),
          truncation=COALESCE(excluded.truncation, submit_ready.truncation),
          nan_handling=COALESCE(excluded.nan_handling, submit_ready.nan_handling),
          max_trade=COALESCE(excluded.max_trade, submit_ready.max_trade),
          suggested_tags=excluded.suggested_tags,
          family=COALESCE(excluded.family, submit_ready.family),
          status=CASE WHEN submit_ready.status='SUBMITTED' THEN submit_ready.status
                      WHEN submit_ready.status='DEAD' AND excluded.status='READY' THEN 'READY'
                      WHEN submit_ready.status='DEAD' THEN submit_ready.status
                      ELSE excluded.status END,
          note=CASE WHEN submit_ready.status='SUBMITTED' THEN submit_ready.note
                    WHEN submit_ready.status='DEAD' AND excluded.status='READY'
                         THEN COALESCE(excluded.note,'')||' | revived:'||COALESCE(submit_ready.gate,'')
                    WHEN submit_ready.status='DEAD' THEN submit_ready.note
                    ELSE excluded.note END
        """,
        (rec.get("alpha_id"), rec.get("region"), rec.get("universe"), rec.get("delay"),
         rec.get("decay"), rec.get("neutralization"),
         rec.get("truncation"), rec.get("nan_handling"), rec.get("max_trade"),
         expr,
         rec.get("skeleton") or _sig(expr),
         fam,
         rec.get("suggested_tags") or _tags_for(rec),
         rec.get("sharpe"), rec.get("fitness"), rec.get("turnover"),
         rec.get("two_year"), rec.get("sub_universe"), rec.get("cluster_test"),
         rec.get("margin"), rec.get("returns"), rec.get("drawdown"),
         rec.get("long_count"), rec.get("short_count"),
         rec.get("investability_constrained_sharpe"), rec.get("risk_neutralized_sharpe"),
         rec.get("prod"), rec.get("self"), gate, _now(), vb,
         rec.get("towers") or "[]", rec.get("family"), st, _now(), note),
    )
    return gate


def enqueue(con: sqlite3.Connection, rec: Dict[str, Any], note: str = "") -> str:
    """写入单条（外部已持有连接）。返回 gate。"""
    if not rec.get("alpha_id") or not rec.get("region"):
        raise ValueError("alpha_id / region 必填")
    return _upsert(con, rec, note)


def enqueue_from_alphas(
    region: Optional[str] = None,
    min_sharpe: Optional[float] = None,
    min_fitness: Optional[float] = None,
    max_prod: Optional[float] = None,
    db_path: Optional[str] = None,
    dry_run: bool = False,
    note: str = "auto-enqueue",
    dedup: bool = True,
    max_per_skeleton: int = 1,
) -> int:
    """从 `alphas` 表按条件批量入队（离线、零配额）。

    Args:
        dedup: 入队后按骨架去重（默认开），同骨架只留优先级最高的 N 条，
               其余标 `SUPERSEDED`。避免队列堆同族兄弟变体（平台上 SELF 0.9+ 自相残杀）。
        max_per_skeleton: 每个骨架在**同一区域**内保留的条数（默认 1）。

    Returns: 入队条数（去重前）
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        # 数据集列：仅当 `datasets` 表存在时才 JOIN（测试用的最小 fixture 库没有该表；
        # 且只取 category IS NOT NULL 的真实数据集，排除类别占位行）
        has_ds = bool(con.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='datasets'").fetchone())
        ds_col = "d.name AS dataset," if has_ds else "NULL AS dataset,"
        ds_join = ("LEFT JOIN datasets d ON a.dataset_id = d.id AND d.category IS NOT NULL"
                   if has_ds else "")
        # 回测行的两列（RA 名单 / 设置档来源）：**表与列都可能不存在**
        # （最小 fixture 库只有 backtest_results(id, alpha_id, ra_failed_checks)）⇒ 按存在性拼子查询。
        # `payload_json` 里的 universe/delay/neut 是本地唯一能补齐设置档的旁路（族签名用）。
        bt_cols: set = set()
        if con.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                       "AND name='backtest_results'").fetchone():
            bt_cols = {c[1] for c in con.execute("PRAGMA table_info(backtest_results)").fetchall()}
        ra_col = ("(SELECT b.ra_failed_checks FROM backtest_results b "
                  "WHERE b.alpha_id=a.alpha_id ORDER BY b.id DESC LIMIT 1) AS ra_failed_checks"
                  if "ra_failed_checks" in bt_cols else "NULL AS ra_failed_checks")
        payload_col = ("(SELECT b.payload_json FROM backtest_results b "
                       "WHERE b.alpha_id=a.alpha_id ORDER BY b.id DESC LIMIT 1) AS bt_payload"
                       if "payload_json" in bt_cols else "NULL AS bt_payload")
        q = f"""SELECT a.alpha_id, r.name AS region, a.universe, a.delay, a.neutralization,
                      a.expression, a.sharpe, a.fitness, a.turnover, a.two_year_sharpe,
                      a.sub_universe_sharpe, a.cluster_test,
                      a.prod_correlation, a.self_correlation,
                      {ds_col}
                      {ra_col},
                      {payload_col}
               FROM alphas a LEFT JOIN regions r ON a.region_id = r.id
               {ds_join}
               WHERE a.alpha_id IS NOT NULL AND a.alpha_id <> ''
                 AND COALESCE(a.soft_deleted,0)=0
                 AND COALESCE(a.disposition,'') <> 'DEAD'
                 AND a.status IN ('UNSUBMITTED','COMPLETE')
                 AND COALESCE(a.platform_status,'') NOT IN ('ACTIVE','DECOMMISSIONED')
                 AND a.date_submitted IS NULL"""
        ps: List[Any] = []
        if region:
            q += " AND r.name = ?"
            ps.append(region)
        if min_sharpe is not None:
            q += " AND a.sharpe >= ?"
            ps.append(min_sharpe)
        if min_fitness is not None:
            q += " AND a.fitness >= ?"
            ps.append(min_fitness)
        if max_prod is not None:
            q += " AND (a.prod_correlation IS NULL OR a.prod_correlation < ?)"
            ps.append(max_prod)
        rows = con.execute(q, ps).fetchall()
        # 坑 4：已由平台实测/判定过的行（verified_by ∈ PLATFORM_VERIFIED_BY）与终态行不再重写——
        # 批量入队的职责是「捕获」，alphas 表的 prod/self 只会比平台实测更旧
        protected = {
            (x[0], x[1]) for x in con.execute(
                "SELECT alpha_id, region FROM submit_ready WHERE status IN ('SUBMITTED','DEAD') "
                "OR verified_by IN (%s)" % ",".join("?" * len(PLATFORM_VERIFIED_BY)),
                list(PLATFORM_VERIFIED_BY)).fetchall()}
        n = skipped = 0
        for r in rows:
            # 2026-10-23（P1-3）：行工厂是 sqlite3.Row（无 .get）⇒ 统一转 dict 再取键。
            r = dict(r)
            if not r["region"]:
                continue
            if (r["alpha_id"], r["region"]) in protected:
                skipped += 1
                continue
            # 设置档（族签名用）：alphas 镜像缺 decay/truncation 时，从最近一条回测
            # payload 补 universe/delay/neut（本地唯一可得的设置来源）。取不到的成分
            # 一律留 None ⇒ 族签名里记 '?'（未知 ≠ 已知，判不同族）。
            bt = _json_obj(r.get("bt_payload"))
            universe = r.get("universe") or bt.get("universe")
            delay = r.get("delay") if r.get("delay") is not None else bt.get("delay")
            neut = r.get("neutralization") or bt.get("neut") or bt.get("neutralization")
            rec = {
                "alpha_id": r["alpha_id"], "region": r["region"],
                "universe": universe, "delay": delay,
                "decay": bt.get("decay"), "truncation": bt.get("truncation"),
                "neutralization": neut, "expr": r["expression"],
                "dataset": r.get("dataset"),
                "alpha_type": None,
                "sharpe": r["sharpe"], "fitness": r["fitness"], "turnover": r["turnover"],
                "two_year": r["two_year_sharpe"], "sub_universe": r["sub_universe_sharpe"],
                "cluster_test": r["cluster_test"],
                "prod": r["prod_correlation"], "self": r["self_correlation"],
                "ra_failed_checks": r["ra_failed_checks"],
                "towers": "[]", "verified_by": "alphas",
            }
            _upsert(con, rec, note)
            n += 1
        if skipped:
            print(f"[enqueue] 跳过 {skipped} 条已平台实测/终态行（不覆盖）")
        # 坑 3：入队后立刻按本地 alphas 表退役已提交者（同一连接内，dry_run 时随 rollback 撤销）
        try:
            con.execute(
                "UPDATE submit_ready SET status=?, note=COALESCE(note,'')||' | retired:platform-active' "
                "WHERE status='READY' AND alpha_id IN (SELECT a.alpha_id FROM alphas a WHERE "
                "a.alpha_id IS NOT NULL AND (COALESCE(a.platform_status,'') IN ('ACTIVE','DECOMMISSIONED') "
                "OR a.date_submitted IS NOT NULL))" + (" AND region=?" if region else ""),
                [STATUS_SUBMITTED] + ([region] if region else []))
        except sqlite3.Error:
            pass
        if dedup:
            d = dedup_siblings(region=region, max_per_skeleton=max_per_skeleton,
                               con=con, dry_run=False)
            if d.get("superseded"):
                print(f"[dedup] 同族去重：{d['superseded']} 条标 SUPERSEDED"
                      f"（{d['skeletons']} 个族，保留 {d['kept']}）")
        if dry_run:
            con.rollback()
        else:
            con.commit()
        return n
    finally:
        con.close()


def dedup_siblings(region: Optional[str] = None, max_per_skeleton: int = 1,
                   db_path: Optional[str] = None, con: Optional[sqlite3.Connection] = None,
                   dry_run: bool = False) -> Dict[str, int]:
    """同族去重：每个 `(region, 族签名)` 只保留优先级最高的 N 条。

    族签名 = **主体骨架 + 分组轴 + 全部设置档**（`family_signature`）。
    2026-10-23（P1-3）起不再只按表达式主体形状去重 —— `group_rank(x, industry)` 与
    `group_rank(x, subindustry)` 主体形状一样却是**不同信号族**（USA `d5KzLo7v`
    事故，见 `reports/usa_mining_history_review_20261023.md` §9.3）。
    设置档取不到的行**保守降级**为独立族（宁可少去重一次，也不误杀不同族）。

    仅作用于 `status='READY'` 的行；被淘汰者标 `SUPERSEDED`（不是硬闸失败，
    故与 `DEAD` 区分，便于审计）。族签名算不出来的行跳过去重（无法判定）。

    Returns: {'kept': 保留数, 'superseded': 淘汰数, 'skeletons': 参与去重的族数}
    """
    own = con is None
    con = con or connect(db_path)
    try:
        ensure_table(con)
        q = "SELECT * FROM submit_ready WHERE status='READY'"
        ps: List[Any] = []
        if region:
            q += " AND region = ?"
            ps.append(region)
        rows = [dict(r) for r in con.execute(q, ps).fetchall()]

        # 2026-10-23（P1-3）：去重键从「主体骨架」换成**族签名**（主体 + 分组轴 + 全部设置档）。
        # `skeleton` 列保持旧口径（仅主体形状，不动其它读方），族签名另存 `family_sig`。
        # 设置档取不到的行**保守降级**为独立族（宁可少去重一次，也不误杀不同族）。
        groups: Dict[Any, List[Dict[str, Any]]] = {}
        for r in rows:
            body = _sig(r.get("expr"))
            if not r.get("skeleton") and body and not dry_run:
                con.execute("UPDATE submit_ready SET skeleton=? WHERE id=?",
                            (body, r["id"]))
                r["skeleton"] = body
            sig = family_signature_of_row(r)
            if sig and not dry_run and r.get("family_sig") != sig:
                con.execute("UPDATE submit_ready SET family_sig=? WHERE id=?",
                            (sig, r["id"]))
                r["family_sig"] = sig
            if not sig:
                continue
            groups.setdefault((r["region"], sig), []).append(r)

        kept = superseded = 0
        for (_reg, sig), items in groups.items():
            items.sort(key=priority, reverse=True)
            for i, it in enumerate(items):
                if i < max_per_skeleton:
                    kept += 1
                else:
                    superseded += 1
                    if not dry_run:
                        con.execute(
                            "UPDATE submit_ready SET status=?, "
                            "note=COALESCE(note,'')||? WHERE id=?",
                            (STATUS_SUPERSEDED,
                             f" | superseded-by:{items[0]['alpha_id']}", it["id"]))
        if not dry_run and own:
            con.commit()
        return {"kept": kept, "superseded": superseded,
                "skeletons": len(groups)}
    finally:
        if own:
            con.close()


def retire(alpha_id: str, status: str = STATUS_SUBMITTED,
           region: Optional[str] = None, db_path: Optional[str] = None) -> int:
    """退役：把队列中该 alpha 置为 SUBMITTED/DEAD/EXPIRED。返回影响行数。

    容错：表不存在或无该行时返回 0，不抛异常（供提交/收批主流程调用）。
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        suffix = f" | retired:{status}"
        if region:
            cur = con.execute(
                "UPDATE submit_ready SET status=?, note=COALESCE(note,'')||? "
                "WHERE alpha_id=? AND region=?",
                (status, suffix, alpha_id, region))
        else:
            cur = con.execute(
                "UPDATE submit_ready SET status=?, note=COALESCE(note,'')||? WHERE alpha_id=?",
                (status, suffix, alpha_id))
        n = cur.rowcount or 0
        con.commit()
        return n
    finally:
        con.close()


def retire_region(region: str, status: str = STATUS_EXPIRED, note: str = "",
                  db_path: Optional[str] = None, dry_run: bool = False,
                  from_statuses: Sequence[str] = (STATUS_READY,)) -> Dict[str, Any]:
    """整区批量退役候选（2026-09-30 补能力）。

    背景：`tools/submit_queue.py add-many` 从本地 `alphas` 镜像批量入队后，镜像陈旧
    （指标/相关性已变差或已 ACTIVE）时会留下整片无效 READY。逐颗 `retire --alpha-id` 不现实，
    所以上层只能“再入队一次”而越清越乱（实测 IND 一次性入队 109 条）。

    幂等：重跑时已是目标状态的行不再匹配（from_statuses 只取非目标状态）。
    返回 {'region','status','matched','dry_run','from_statuses'}。
    """
    if not region:
        raise ValueError("retire_region 必须指定 region（防误操全库）")
    from_statuses = [s for s in (from_statuses or ()) if s != status]
    if not from_statuses:
        return {"region": region, "status": status, "matched": 0,
                "dry_run": dry_run, "from_statuses": []}
    con = connect(db_path)
    try:
        ensure_table(con)
        ph = ",".join("?" * len(from_statuses))
        sel = f"SELECT COUNT(*) FROM submit_ready WHERE region=? AND status IN ({ph})"
        matched = con.execute(sel, [region] + list(from_statuses)).fetchone()[0]
        if dry_run or not matched:
            return {"region": region, "status": status, "matched": int(matched),
                    "dry_run": dry_run, "from_statuses": from_statuses}
        suffix = f" | retired:{status}"
        if note:
            suffix += f"({note})"
        cur = con.execute(
            f"UPDATE submit_ready SET status=?, note=COALESCE(note,'')||? "
            f"WHERE region=? AND status IN ({ph})",
            [status, suffix, region] + list(from_statuses))
        con.commit()
        return {"region": region, "status": status, "matched": int(cur.rowcount or 0),
                "dry_run": dry_run, "from_statuses": from_statuses}
    finally:
        con.close()


def retire_active(active_ids, region: Optional[str] = None, db_path: Optional[str] = None,
                  status: str = STATUS_SUBMITTED) -> int:
    """坑 3：把平台已 ACTIVE/DECOMMISSIONED 的 alpha 从 READY 批量退役（幂等）。返回影响行数。
    调用方传平台 OS 列表的 id（tools/submit_queue.py sync 子命令 / verify 子命令自动调）。"""
    ids = [i for i in (active_ids or []) if i]
    if not ids:
        return 0
    con = connect(db_path)
    try:
        ensure_table(con)
        n = 0
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            q = ("UPDATE submit_ready SET status=?, note=COALESCE(note,'')||' | retired:platform-active' "
                 "WHERE status='READY' AND alpha_id IN (%s)" % ",".join("?" * len(chunk)))
            ps: List[Any] = [status] + chunk
            if region:
                q += " AND region=?"
                ps.append(region)
            n += con.execute(q, ps).rowcount or 0
        con.commit()
        return n
    finally:
        con.close()


def retire_platform_done(region: Optional[str] = None, db_path: Optional[str] = None) -> int:
    """坑 3（离线版，零配额）：本地 alphas 表已标 ACTIVE/DECOMMISSIONED 或有 date_submitted 的 alpha，
    若仍在 READY 则退役为 SUBMITTED。harvest 收批 / CLI list 前都可调，幂等。返回影响行数。"""
    con = connect(db_path)
    try:
        ensure_table(con)
        q = ("UPDATE submit_ready SET status=?, note=COALESCE(note,'')||' | retired:platform-active' "
             "WHERE status='READY' AND alpha_id IN ("
             "  SELECT a.alpha_id FROM alphas a WHERE a.alpha_id IS NOT NULL AND ("
             "    COALESCE(a.platform_status,'') IN ('ACTIVE','DECOMMISSIONED')"
             "    OR a.date_submitted IS NOT NULL))")
        ps: List[Any] = [STATUS_SUBMITTED]
        if region:
            q += " AND region=?"
            ps.append(region)
        n = con.execute(q, ps).rowcount or 0
        con.commit()
        return n
    except sqlite3.Error:
        return 0
    finally:
        con.close()


def regrade_ready(region: Optional[str] = None, db_path: Optional[str] = None,
                  dry_run: bool = False) -> Dict[str, Any]:
    """离线复判：把现有 READY 行按**当前闸门**重算（RA 硬闸 / add 混腿 / prod 兄弟 / 指标）。

    用途：闸门规则升级后清洗历史队列（零配额）。RA FAIL 名单取 backtest_results 最新一条；
    没有回测记录的行只按表达式与已存指标复判。返回
    {'checked', 'dead', 'revived', 'changes': [(id, old_gate, new_gate)]}。

    两处口径（2026-10-24 修复，事故 #88）：

    1. **扫描面含被兄弟闸判死的行**（`FAIL:PROD_SIBLING*`）。那类结论建立在「自身 prod 未测」
       之上，而闸门只在 READY 行上跑过一次就再也不会复查 ⇒ 判死即永久不可申诉。
       实测：`88vXxaqv` / `LL53QVvn` 入队（14:15:24, prod=NULL）被兄弟 `qMEVJPo2` 判死，
       自身 prod 两分钟后才落库（0.6811 / 0.5761，均 < 0.70）—— 结论与事实相反。
    2. **prod/self 以 `alphas` 镜像为准**：队列表里存的是**入队时的快照**，
       `persist_correlation()` 只写 `alphas`、不回写本表，所以快照会长期停在 NULL。
       回填只在队列表该列为空时进行（已测值不被覆盖）。
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        q = ("SELECT * FROM submit_ready WHERE status=? "
             "OR (status=? AND COALESCE(gate,'') LIKE 'FAIL:PROD_SIBLING%')")
        ps: List[Any] = [STATUS_READY, STATUS_DEAD]
        if region:
            q += " AND region=?"
            ps.append(region)
        rows = [dict(r) for r in con.execute(q, ps).fetchall()]
        changes: List[Any] = []
        revived = 0
        for r in rows:
            # —— 相关性以 alphas 镜像为准（空 = 尚未测量，不是「未撞墙」）——
            if r.get("prod") is None or r.get("self") is None:
                try:
                    m = con.execute("SELECT prod_correlation, self_correlation FROM alphas "
                                    "WHERE alpha_id=?", (r["alpha_id"],)).fetchone()
                except sqlite3.Error:
                    m = None
                if m:
                    for k, v in (("prod", m[0]), ("self", m[1])):
                        if r.get(k) is None and v is not None:
                            r[k] = v
                            if not dry_run:
                                con.execute("UPDATE submit_ready SET %s=? WHERE id=?" % k,
                                            (v, r["id"]))
            ra = None
            try:
                bt = con.execute("SELECT ra_failed_checks FROM backtest_results WHERE alpha_id=? "
                                 "ORDER BY id DESC LIMIT 1", (r["alpha_id"],)).fetchone()
                ra = bt[0] if bt else None
            except sqlite3.Error:
                pass
            gate, st = gate_of(r.get("sharpe"), r.get("fitness"), r.get("two_year"), r.get("turnover"),
                               r.get("prod"), r.get("self"), ra, r.get("expr"))
            if st == STATUS_READY and r.get("prod") is None and r.get("expr"):
                # 判据 = 族分解（主体 + 分组轴 + 设置档），不是主体骨架（USA d5KzLo7v 事故）。
                sib = _prod_wall_sibling(con, r.get("region"), r.get("expr"), r.get("alpha_id"),
                                         own_parts=family_parts_of_row(r))
                if sib:
                    gate, st = "FAIL:PROD_SIBLING(%s=%.2f)" % sib, STATUS_DEAD
            old_gate, old_st = r.get("gate"), r.get("status")
            if st != old_st or gate != old_gate:
                changes.append((r["alpha_id"], old_gate, gate))
                if st == STATUS_READY and old_st != STATUS_READY:
                    revived += 1
                    note = " | regrade:revived(%s)" % (old_gate or "")
                elif st != STATUS_READY:
                    note = " | regrade:" + gate
                else:
                    note = ""
                if not dry_run:
                    con.execute("UPDATE submit_ready SET gate=?, status=?, "
                                "note=COALESCE(note,'')||? WHERE id=?",
                                (gate, st, note, r["id"]))
        if not dry_run:
            con.commit()
        return {"checked": len(rows), "revived": revived,
                "dead": sum(1 for c in changes if c[2].startswith("FAIL")),
                "changes": changes}
    finally:
        con.close()


def mark_verified(alpha_id: str, region: Optional[str] = None,
                  gate: str = "SUBMIT_LAYER_VERIFIED", source: str = "submit_verdict",
                  rec: Optional[Dict[str, Any]] = None,
                  db_path: Optional[str] = None) -> int:
    """升级队列状态为「已验证可提交」。

    由提交判定点（`tools/submit_verdict.py` 出 SUBMITTABLE）调用：
    S3 收批入队时可能只有 `IS_ONLY`；判定后升级为 `SUBMIT_LAYER_VERIFIED`
    并刷新 `verified_at`，使队列的可信度与判定权威一致。

    保护：不复活已 SUBMITTED 的行；表不存在/无该行返回 0（容错）。
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        sets = ["gate=?", "verified_at=?", "verified_by=?", "status=?"]
        ps: List[Any] = [gate, _now(), source, STATUS_READY]
        if rec:
            for k in ("sharpe", "fitness", "turnover", "two_year", "sub_universe",
                      "cluster_test", "prod", "self", "expr",
                      # 2026-10-06：体检卡三层新增列也随判定点刷新
                      "margin", "returns", "drawdown", "long_count", "short_count",
                      "investability_constrained_sharpe", "risk_neutralized_sharpe",
                      # 2026-10-23（P1-3）：设置档也随判定点刷新（族签名要含全部设置档）
                      "universe", "delay", "decay", "neutralization",
                      "truncation", "nan_handling", "max_trade"):
                if rec.get(k) is not None:
                    sets.append(f"{k}=?")
                    ps.append(rec[k])
        where = "alpha_id=? AND status<>'SUBMITTED'"
        ps_w: List[Any] = [alpha_id]
        if region:
            where = "alpha_id=? AND region=? AND status<>'SUBMITTED'"
            ps_w.append(region)
        cur = con.execute(
            f"UPDATE submit_ready SET {', '.join(sets)} WHERE {where}", ps + ps_w)
        n = cur.rowcount or 0
        con.commit()
        return n
    finally:
        con.close()


def refresh_tags(region: Optional[str] = None, db_path: Optional[str] = None,
                 dry_run: bool = False) -> int:
    """按当前规范**重算**队列所有行的 `suggested_tags`（回填）。

    用途：规范/解析器升级后（如 `SRC_` 改为按表达式字段反查），把存量行的
    建议标签刷新到最新口径 —— 不必等它们被重新入队（已提交/已冻结的行不会重入队）。

    Returns: 发生变化的行数
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        q = "SELECT id, alpha_id, expr, prod, self, suggested_tags FROM submit_ready"
        ps: List[Any] = []
        if region:
            q += " WHERE region = ?"
            ps.append(region)
        changed = 0
        for r in con.execute(q, ps).fetchall():
            new = _tags_for({"alpha_id": r["alpha_id"], "expr": r["expr"],
                             "prod": r["prod"], "self": r["self"]}, db_path)
            if new != (r["suggested_tags"] or "[]"):
                changed += 1
                if not dry_run:
                    con.execute("UPDATE submit_ready SET suggested_tags=? WHERE id=?",
                                (new, r["id"]))
        if not dry_run:
            con.commit()
        return changed
    finally:
        con.close()


def list_ready(region: Optional[str] = None, db_path: Optional[str] = None,
               all_status: bool = False) -> List[Dict[str, Any]]:
    """列出候选（默认仅 READY），按优先级降序。

    2026-10-20 P1-4：每行附相关性新鲜度标注（`corr_age_hours` / `corr_stale` /
    `corr_stale_reason`）——READY 行普遍是 `IS_ONLY`（prod 旧读数、self 未测），
    下游只看数字本身分不出「刚测的」与「两周前的」，提交队列核对必须先看新鲜度。
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        q = "SELECT * FROM submit_ready WHERE 1=1"
        ps: List[Any] = []
        if not all_status:
            q += " AND status='READY'"
        if region:
            q += " AND region = ?"
            ps.append(region)
        rows = [dict(r) for r in con.execute(q, ps).fetchall()]
        annotate_corr_freshness(rows, corr_times=_corr_checked_times(
            con, [r.get("alpha_id") for r in rows]))
        return sorted(rows, key=priority, reverse=True)
    finally:
        con.close()


# ---------------- 相关性新鲜度标注（2026-10-20 P1-4） ----------------

#: 相关性保鲜期（小时）。与 MCP `get_alpha_corr_metrics` 缺省一致（48h）：
#: 平台 prod 池随时变动，实测 2-3 天可从 0.58 漂到 0.98（见该工具 docstring）。
CORR_STALE_AFTER_HOURS = 48.0


def _parse_ts(raw) -> Optional[datetime]:
    """解析时间戳（'YYYY-MM-DDTHH:MM:SS' / 'YYYY-MM-DD HH:MM:SS' / 带时区）；失败返回 None。"""
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(str(raw).strip().replace(" ", "T", 1))
    except ValueError:
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone().replace(tzinfo=None)
    return dt


def _corr_checked_times(con: sqlite3.Connection, alpha_ids) -> Dict[str, Any]:
    """alpha_id → `alphas.corr_checked_at`（相关性最近一次平台检测时刻）。

    缺表 / 缺列（最小 fixture 库）返回 {}，绝不因它影响 list_ready 主流程。
    """
    ids = [i for i in (alpha_ids or []) if i]
    if not ids:
        return {}
    out: Dict[str, Any] = {}
    try:
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            ph = ",".join("?" * len(chunk))
            for aid, ts in con.execute(
                    "SELECT alpha_id, corr_checked_at FROM alphas "
                    f"WHERE corr_checked_at IS NOT NULL AND alpha_id IN ({ph})", chunk):
                out[aid] = ts
    except sqlite3.Error:
        return {}
    return out


def annotate_corr_freshness(rows: List[Dict[str, Any]], corr_times: Optional[Dict[str, Any]] = None,
                            now: Optional[datetime] = None,
                            stale_after_hours: float = CORR_STALE_AFTER_HOURS) -> List[Dict[str, Any]]:
    """就地给队列行补 `corr_age_hours` / `corr_stale` / `corr_stale_reason`（纯本地、零配额）。

    判据（任一命中即 stale=True，reason 按此顺序判定）：
      - prod 或 self 为 None            → 'missing'（相关性未测全，无论多新都不可据以提交）
      - 找不到任何可用检测时刻           → 'no_timestamp'
      - age > stale_after_hours         → 'aged'
    检测时刻优先取 `corr_times[alpha_id]`（平台 `alphas.corr_checked_at`，权威）；
    缺失时退到行内 `verified_at` **且仅当 `verified_by` 属平台实测组** ——
    批量入队（'alphas' / 'IS_only'）的 verified_at 只是入队时刻，不代表测过。

    Args:
        rows: list_ready 行（dict），**就地修改**并返回
        corr_times: {alpha_id: 时间戳}，见 `_corr_checked_times`
        now: 参照时刻（缺省 datetime.now()；测试注入）
        stale_after_hours: 保鲜期小时数（缺省 48）
    """
    now = now or datetime.now()
    corr_times = corr_times or {}
    for r in rows:
        checked = _parse_ts(corr_times.get(r.get("alpha_id")))
        if checked is None and r.get("verified_by") in PLATFORM_VERIFIED_BY:
            checked = _parse_ts(r.get("verified_at"))
        age_h = round((now - checked).total_seconds() / 3600.0, 1) if checked else None
        if r.get("prod") is None or r.get("self") is None:
            r["corr_age_hours"], r["corr_stale"], r["corr_stale_reason"] = age_h, True, "missing"
        elif checked is None:
            r["corr_age_hours"], r["corr_stale"], r["corr_stale_reason"] = None, True, "no_timestamp"
        else:
            r["corr_age_hours"] = age_h
            r["corr_stale"] = age_h > float(stale_after_hours)
            r["corr_stale_reason"] = "aged" if r["corr_stale"] else ""
    return rows


def normalize_towers(raw) -> list:
    """``towers`` 列归一为 ``[(塔名, 倍率)]``（无倍率则为 ``None``）。

    2026-10-05 实测该列**三种格式并存**，且旧 ``priority`` 只认其中一种：
      * ``'["USA/D1/MODEL"]'``   —— JSON list of str（tools/submit_queue.py add 产出）
      * ``'{"name":..,"multiplier":..}'`` 元素 —— JSON list of dict（原 priority 期望）
      * ``'USA/D1/MODEL'``       —— **裸字符串**（无引号无括号，json.loads 抛错静默退化）
      * ``'[]'`` / ``None``      —— harvest 时 pyramids 缺失（UNSUBMITTED alpha 无 pyramids）
    旧实现三态里两态全部退化为 1.0 ⇒ 塔倍率被静默丢弃、优先级排序失真。本函数统一解析。

    注（2026-10-06）：本函数原为工作区未跟踪改动，被外部 ``cline restore transaction``
    一并清除且无 git 历史；此版本依据残留字节码常量重建。
    """
    out = []
    if raw is None:
        return out
    if isinstance(raw, (list, tuple)):
        items = list(raw)
    else:
        s = str(raw).strip()
        if not s:
            return out
        try:
            items = json.loads(s)
        except (ValueError, TypeError):
            items = re.split(r"[,;\s]+", s)
        if isinstance(items, dict):
            items = [items]
        elif not isinstance(items, (list, tuple)):
            items = [items]
    for it in items or []:
        mult = None
        if isinstance(it, dict):
            nm = it.get("name") or it.get("id")
            if not nm:
                pyr = it.get("pyramid")
                if isinstance(pyr, dict) and pyr.get("region") is not None:
                    nm = "%s/D%s/%s" % (pyr.get("region"),
                                        pyr.get("delay") if pyr.get("delay") is not None else "?",
                                        pyr.get("category") or "?")
            mv = it.get("multiplier")
            if mv is not None:
                try:
                    mult = float(mv)
                except (TypeError, ValueError):
                    mult = None
        else:
            nm = str(it).strip() if it is not None else ""
        if nm:
            out.append((str(nm).strip(), mult))
    return out


# ---------------- 入队列填充审计（2026-10-08，memory 铁律「入队必须补齐所有可得字段」） ----------------

#: 入队时**凡平台/本地拿得到就该有值**的列。column_fill_audit 逐列查 None/""/"[]"，
#: 入队后必须跑（perf_max enqueue / enqueue_sweep / submit_queue add 均内置调用）。
AUDIT_FILL_COLS = (
    "universe", "delay", "neutralization", "expr", "skeleton",
    "sharpe", "fitness", "turnover", "two_year", "sub_universe", "cluster_test",
    "margin", "returns", "drawdown", "long_count", "short_count",
    "investability_constrained_sharpe", "risk_neutralized_sharpe",
    "prod", "self", "towers", "family",
)


def family_of_expr(expr: Optional[str]) -> str:
    """表达式 → 短族名（公开入口，与 _upsert 的 skeleton/family 派生同源）。"""
    return _family_of(_sig(expr))


def column_fill_audit(con: sqlite3.Connection, alpha_id: str, region: str) -> Optional[List[str]]:
    """入队后列填充审计：返回该行 AUDIT_FILL_COLS 里仍为空的列名列表。

    返回 ``None`` 表示该 (alpha_id, region) 行不存在。空列表 = 全部填满。
    注意这是**信息性审计**不是闸：prod/self 未实测、risk_neutralized_sharpe 平台不给
    时允许为空，但必须被看见（不许静默 None）。
    """
    row = con.execute("SELECT * FROM submit_ready WHERE alpha_id=? AND region=?",
                      (alpha_id, region)).fetchone()
    if row is None:
        return None
    keys = row.keys()
    missing = []
    for c in AUDIT_FILL_COLS:
        if c not in keys:
            continue
        v = row[c]
        if v is None or v == "" or v == "[]":
            missing.append(c)
    return missing
