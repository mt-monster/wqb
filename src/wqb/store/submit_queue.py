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
- 所有写操作容错：队列记账失败**绝不能**影响主流程（收批/提交）。
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ._common import default_db_path, _now
from ..db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口：WAL + busy_timeout 60s）

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
#: 模拟层全过、仅 prod/self 撞 0.7 墙（2026-09-30 用户定调）。与 DEAD 区分：可随生产池变化恢复，
#: 单独追踪；**不直接 POST**（提交会进一步污染池子、废掉同族兄弟）。
STATUS_PROD_BLOCKED = "PROD_BLOCKED"

SCHEMA = """
CREATE TABLE IF NOT EXISTS submit_ready (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    alpha_id       TEXT    NOT NULL,
    region         TEXT    NOT NULL,
    universe       TEXT,
    delay          INTEGER,
    decay          INTEGER,
    neutralization TEXT,
    expr           TEXT,
    skeleton       TEXT,
    suggested_tags TEXT,
    sharpe         REAL,
    fitness        REAL,
    turnover       REAL,
    two_year       REAL,
    sub_universe   REAL,
    cluster_test   REAL,
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
    """返回 (gate, status)。未过闸者一律不进 READY。

    2026-09-30 新增 PROD_BLOCKED：**模拟层全过（S/F/2Y/T + RA 硬闸全 PASS），仅 prod/self
    撞 0.7 墙** 的候选。这类 alpha 与真正参数不达标的 DEAD 语义不同——它是「本来可提交、
    只是当前生产池太挤」，会随生产池变化（新提交/退市）而恢复。用户 2026-09-30 定调：
    这类候选应单独追踪、不直接 POST（POST 会进一步污染生产池），等池子有空间再提。
    """
    ok, why = is_pass(sharpe, fitness, two_year, turnover, prod, selfc, ra_failed_checks, expr)
    if not ok:
        if why in ("PROD", "SELF"):
            return "FAIL:" + why, STATUS_PROD_BLOCKED
        return "FAIL:" + why, STATUS_DEAD
    if prod is None or selfc is None:
        # IS 达标但相关性未测 → 可入队待验，提交前必须 verify
        return "IS_ONLY", STATUS_READY
    return "SUBMIT_LAYER_VERIFIED", STATUS_READY


def normalize_towers(raw) -> List[Tuple[str, Optional[float]]]:
    """``towers`` 列归一为 ``[(塔名, 倍率)]``（无倍率则为 None）。

    2026-10-05 实测该列**三种格式并存**，且旧 ``priority`` 只认其中一种：
      * ``'["USA/D1/MODEL"]'``   —— JSON list of str（tools/submit_queue.py add 产出）
      * ``'{"name":..,"multiplier":..}'`` 元素 —— JSON list of dict（原 priority 期望）
      * ``'USA/D1/MODEL'``       —— **裸字符串**（无引号无括号，json.loads 抛错静默退化）
      * ``'[]'`` / ``None``      —— harvest 时 pyramids 缺失（UNSUBMITTED alpha 无 pyramids）
    旧实现三态里两态全部退化为 1.0 ⇒ 塔倍率被静默丢弃、优先级排序失真。本函数统一解析。
    """
    if not raw:
        return []
    if isinstance(raw, (list, tuple)):
        items = list(raw)
    else:
        s = str(raw).strip()
        if not s:
            return []
        items = None
        try:
            v = json.loads(s)
            if v is None:
                return []  # JSON "null" ⇒ 空
            if isinstance(v, (list, tuple)):
                items = list(v)
            elif isinstance(v, dict):
                items = [v]
        except (ValueError, TypeError):
            pass
        if items is None:
            # 裸字符串："USA/D1/MODEL"，或逗号/空白分隔的多塔
            parts = [p.strip() for p in re.split(r"[,;\s]+", s) if p.strip()]
            items = [p for p in parts if "/" in p] or parts
    out: List[Tuple[str, Optional[float]]] = []
    for it in items:
        if isinstance(it, str):
            nm = it.strip()
            if nm:
                out.append((nm, None))
        elif isinstance(it, dict):
            nm = it.get("name") or it.get("id") or it.get("pyramid")
            if not nm:
                # {"region": "USA", "delay": 1, "category": {"id": "MODEL"}} 形态
                rg, dl = it.get("region"), it.get("delay")
                cat = it.get("category")
                cid = cat.get("id") if isinstance(cat, dict) else cat
                if rg and cid:
                    nm = f"{rg}/D{dl if dl is not None else '?'}/{cid}"
            if not nm:
                continue
            m = it.get("multiplier")
            try:
                m = float(m) if m is not None else None
            except (TypeError, ValueError):
                m = None
            out.append((str(nm).strip(), m))
    return out


def _towers_multiplier(raw, default: float = 1.0) -> float:
    """取 towers 里的最大倍率；解析不出任何倍率时返回 default（保留旧行为）。"""
    tw = normalize_towers(raw)
    ms = [m for _n, m in tw if m is not None]
    return max(ms) if ms else default


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
    mult = _towers_multiplier(g("towers"))
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
    """
    if not skeleton:
        return ""
    import re as _re
    ops = _re.findall(r"([a-z_][a-z0-9_]*)\s*(?=\()", skeleton)
    if not ops:
        return ""
    return "_".join(ops[:2])[:24]


def _sig(expr: Optional[str]) -> str:
    """表达式 → 结构骨架签名。

    复用权威实现 `wqb.expression.skeleton::structural_signature`
    （字段/分组变量→F、数字→N、算子按"后紧跟 ("识别），
    口径与 `tools/pool_diversity.py`、`tools/backfill_skeletons.py` 一致。
    导入失败时返回空串（去重降级为不去重，不影响入队）。
    """
    if not expr:
        return ""
    try:
        from ..expression.skeleton import structural_signature
        return structural_signature(expr)
    except Exception:  # noqa: BLE001
        return ""


def _prod_wall_sibling(con: sqlite3.Connection, region: Optional[str], expr: Optional[str],
                       alpha_id: Optional[str]):
    """同区域、同骨架签名的其它 alpha 若已实测 prod>=LIM['prod']，返回 (alpha_id, prod)；否则 None。
    数据源 = 队列表自身（prod）+ alphas 表（prod_correlation）。任何异常降级为 None。"""
    sig = _sig(expr)
    if not sig or not region:
        return None
    try:
        rows = con.execute(
            "SELECT alpha_id, prod FROM submit_ready WHERE region=? AND skeleton=? "
            "AND alpha_id<>? AND prod IS NOT NULL AND prod>=?",
            (region, sig, alpha_id or "", LIM["prod"])).fetchall()
        if rows:
            return rows[0][0], float(rows[0][1])
        rid = con.execute("SELECT id FROM regions WHERE name=?", (region,)).fetchone()
        if not rid:
            return None
        for r in con.execute(
                "SELECT alpha_id, expression, prod_correlation FROM alphas WHERE region_id=? "
                "AND prod_correlation>=? AND expression IS NOT NULL LIMIT 2000",
                (rid[0], LIM["prod"])):
            if r[0] != alpha_id and _sig(r[1]) == sig:
                return r[0], float(r[2])
    except sqlite3.Error:
        return None
    return None


def _upsert(con: sqlite3.Connection, rec: Dict[str, Any], note: str = "") -> str:
    gate, st = gate_of(rec.get("sharpe"), rec.get("fitness"), rec.get("two_year"),
                       rec.get("turnover"), rec.get("prod"), rec.get("self"),
                       rec.get("ra_failed_checks"), rec.get("expr"))
    # 坑 2b：同骨架兄弟已实测 prod>=0.7 而本条 prod 未测 → 标 PROD_BLOCKED（FAIL:PROD_SIBLING）；
    # verify/add 实测 prod<0.7 时 mark_verified 可复活。避免"裸主腿 0.8 撞墙家族"靠 prod=None 混进 READY。
    if st == STATUS_READY and rec.get("prod") is None and rec.get("expr"):
        sib = _prod_wall_sibling(con, rec.get("region"), rec.get("expr"), rec.get("alpha_id"))
        if sib:
            gate, st = "FAIL:PROD_SIBLING(%s=%.2f)" % sib, STATUS_PROD_BLOCKED
    vb = rec.get("verified_by") or (
        "API" if (rec.get("prod") is not None or rec.get("self") is not None) else "IS_only")
    con.execute(
        """INSERT INTO submit_ready
        (alpha_id,region,universe,delay,decay,neutralization,expr,skeleton,suggested_tags,
         sharpe,fitness,turnover,two_year,sub_universe,cluster_test,prod,self,
         gate,verified_at,verified_by,towers,family,status,added_at,note)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(alpha_id,region) DO UPDATE SET
          sharpe=excluded.sharpe, fitness=excluded.fitness, turnover=excluded.turnover,
          two_year=excluded.two_year, prod=excluded.prod, self=excluded.self,
          gate=excluded.gate, verified_at=excluded.verified_at,
          verified_by=excluded.verified_by, towers=excluded.towers,
          skeleton=COALESCE(excluded.skeleton, submit_ready.skeleton),
          suggested_tags=excluded.suggested_tags,
          status=CASE WHEN submit_ready.status='SUBMITTED' THEN submit_ready.status
                      WHEN submit_ready.status IN ('DEAD','PROD_BLOCKED')
                           AND excluded.status='READY' THEN 'READY'
                      WHEN submit_ready.status='DEAD' THEN submit_ready.status
                      -- PROD_BLOCKED 且新判定仍为 blocked：保留 PROD_BLOCKED（不被 DEAD 降级）
                      WHEN submit_ready.status='PROD_BLOCKED'
                           AND excluded.status='PROD_BLOCKED' THEN 'PROD_BLOCKED'
                      WHEN submit_ready.status='PROD_BLOCKED' THEN 'DEAD'
                      ELSE excluded.status END,
          note=CASE WHEN submit_ready.status='SUBMITTED' THEN submit_ready.note
                    WHEN submit_ready.status IN ('DEAD','PROD_BLOCKED')
                         AND excluded.status='READY'
                         THEN COALESCE(excluded.note,'')||' | revived:'||COALESCE(submit_ready.gate,'')
                    WHEN submit_ready.status='DEAD' THEN submit_ready.note
                    ELSE excluded.note END
        """,
        (rec.get("alpha_id"), rec.get("region"), rec.get("universe"), rec.get("delay"),
         rec.get("decay"), rec.get("neutralization"), rec.get("expr"),
         rec.get("skeleton") or _sig(rec.get("expr")),
         rec.get("suggested_tags") or _tags_for(rec),
         rec.get("sharpe"), rec.get("fitness"), rec.get("turnover"),
         rec.get("two_year"), rec.get("sub_universe"), rec.get("cluster_test"),
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
        q = f"""SELECT a.alpha_id, r.name AS region, a.universe, a.delay, a.neutralization,
                      a.expression, a.sharpe, a.fitness, a.turnover, a.two_year_sharpe,
                      a.sub_universe_sharpe, a.cluster_test,
                      a.prod_correlation, a.self_correlation,
                      {ds_col}
                      (SELECT b.ra_failed_checks FROM backtest_results b
                        WHERE b.alpha_id=a.alpha_id ORDER BY b.id DESC LIMIT 1) AS ra_failed_checks
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
            if not r["region"]:
                continue
            if (r["alpha_id"], r["region"]) in protected:
                skipped += 1
                continue
            rec = {
                "alpha_id": r["alpha_id"], "region": r["region"],
                "universe": r["universe"], "delay": r["delay"], "decay": None,
                "neutralization": r["neutralization"], "expr": r["expression"],
                "dataset": (r["dataset"] if "dataset" in r.keys() else None),
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
                print(f"[dedup] 同骨架去重：{d['superseded']} 条标 SUPERSEDED"
                      f"（{d['skeletons']} 个骨架，保留 {d['kept']}）")
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
    """同骨架去重：每个 `(region, skeleton)` 只保留优先级最高的 N 条。

    仅作用于 `status='READY'` 的行；被淘汰者标 `SUPERSEDED`（不是硬闸失败，
    故与 `DEAD` 区分，便于审计）。骨架为空的行跳过去重（无法判定）。

    Returns: {'kept': 保留数, 'superseded': 淘汰数, 'skeletons': 参与去重的骨架数}
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

        # 补算缺失骨架（并落库，后续免重算）
        for r in rows:
            if not r.get("skeleton"):
                sig = _sig(r.get("expr"))
                r["skeleton"] = sig
                if sig:
                    con.execute("UPDATE submit_ready SET skeleton=? WHERE id=?",
                                (sig, r["id"]))

        groups: Dict[Any, List[Dict[str, Any]]] = {}
        for r in rows:
            sig = r.get("skeleton")
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
    没有回测记录的行只按表达式与已存指标复判。返回 {'checked', 'dead', 'changes': [(id, old_gate, new_gate)]}。
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        q = "SELECT * FROM submit_ready WHERE status='READY'"
        ps: List[Any] = []
        if region:
            q += " AND region=?"
            ps.append(region)
        rows = [dict(r) for r in con.execute(q, ps).fetchall()]
        changes: List[Any] = []
        for r in rows:
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
                sib = _prod_wall_sibling(con, r.get("region"), r.get("expr"), r.get("alpha_id"))
                if sib:
                    gate, st = "FAIL:PROD_SIBLING(%s=%.2f)" % sib, STATUS_PROD_BLOCKED
            if st != STATUS_READY or gate != r.get("gate"):
                changes.append((r["alpha_id"], r.get("gate"), gate))
                if not dry_run:
                    con.execute("UPDATE submit_ready SET gate=?, status=?, "
                                "note=COALESCE(note,'')||? WHERE id=?",
                                (gate, st, " | regrade:" + gate if st != STATUS_READY else "", r["id"]))
        if not dry_run:
            con.commit()
        return {"checked": len(rows), "dead": sum(1 for c in changes if c[2].startswith("FAIL")),
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
                      "cluster_test", "prod", "self", "expr"):
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


def mark_blocked(alpha_id: str, reason: str = "", status: Optional[str] = None,
                 region: Optional[str] = None, note: str = "",
                 db_path: Optional[str] = None) -> Dict[str, Any]:
    """降级队列状态：平台判定不可提交时把该条退出台账（与 ``mark_verified`` 对称）。

    2026-10-05 教训（A1vOb5pE / ZYAWx9J3）：``tools/submit_verdict.py`` 只会在
    「模拟层干净」时升级（``mark_verified``），出 ``BLOCKED`` / ``ALREADY_SUBMITTED``
    时**不写回队列** → 队列行继续挂着上一轮手写的 ``gate=PASS`` 与 ``status=READY``，
    盘点时把已被平台 RA 硬闸拦住的候选当成「可提交」。本函数补上「只升不降」的缺口。

    ``status`` 为 None 时按 ``reason`` 推断：
      - ``ALREADY_SUBMITTED``            → SUBMITTED（平台已 ACTIVE，勿重复 POST）
      - ``FAILED_COUNT_*`` / ``FAIL:*``  → DEAD（候选缺陷，须修复后重新回测再判）
      - 其他 BLOCKED                     → DEAD

    保护：已是 SUBMITTED 的行不动；已是 DEAD 的行只刷新 gate/note（不复活、不降级）。
    容错：表不存在或无该行返回 ``changed=0``，不抛异常（与 ``mark_verified`` 同口径）。
    """
    if status is None:
        status = (STATUS_SUBMITTED if reason == "ALREADY_SUBMITTED"
                  else STATUS_DEAD)
    out: Dict[str, Any] = {"alpha_id": alpha_id, "status": status,
                           "gate": reason, "changed": 0}
    con = connect(db_path)
    try:
        ensure_table(con)
        where = "alpha_id=? AND status<>'SUBMITTED'"
        ps: List[Any] = [alpha_id]
        if region:
            where = "alpha_id=? AND region=? AND status<>'SUBMITTED'"
            ps.append(region)
        row = con.execute(f"SELECT id, status, gate FROM submit_ready WHERE {where}",
                          ps).fetchone()
        if not row:
            out["why"] = "not_found"
            return out
        old_status, old_gate = row["status"], row["gate"]
        # 已 DEAD 且 gate 一致：幂等，只补 recheck note（同 reason 连续跑不再累加）
        same_gate = (not reason) or old_gate == reason
        if old_status == STATUS_DEAD and same_gate:
            note_txt = ""
            if reason:
                old_note = con.execute(
                    "SELECT note FROM submit_ready WHERE id=?", (row["id"],)).fetchone()[0] or ""
                if f"recheck:{reason}" not in old_note:
                    note_txt = f" | recheck:{reason}"
            if note_txt:
                con.execute("UPDATE submit_ready SET note=COALESCE(note,'')||? WHERE id=?",
                            (note_txt, row["id"]))
                con.commit()
            out["changed"] = 1
            out["why"] = "rechecked"
            return out
        con.execute(
            f"UPDATE submit_ready SET status=?, gate=?, verified_at=?, "
            f"note=COALESCE(note,'')||? WHERE id=?",
            (status, reason or old_gate, _now(),
             f" | submit_verdict:{reason}{(' / ' + note) if note else ''}", row["id"]))
        con.commit()
        out.update({"changed": 1, "why": "downgraded",
                    "old_status": old_status, "old_gate": old_gate})
        return out
    except sqlite3.Error:
        out["why"] = out.get("why") or "db_error"
        return out
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


def refresh_family(region: Optional[str] = None, db_path: Optional[str] = None,
                   dry_run: bool = False) -> int:
    """按 `骨架 → 短族名` 重算并回填 `family` 列（与 `refresh_tags` 同一 idiom）。

    为什么回填而不是删列：`_upsert` 一直写 `family`，`_family_of(skeleton)` 是它的规范
    推导实现，但存量行**从未回填**（2026-10-01 实测 218/218 全 NULL）→ 列存在却永不生效，
    既可能被误当成有效分组依据、又白占空间。由于 INSERT 语句显式引用该列，**不能 DROP**
    （会直接写崩入队链路），正确解法是把它补成真实数据。

    Returns: 发生变化的行数
    """
    con = connect(db_path)
    try:
        ensure_table(con)
        q = "SELECT id, skeleton, expr, family FROM submit_ready"
        ps: List[Any] = []
        if region:
            q += " WHERE region = ?"
            ps.append(region)
        changed = 0
        for r in con.execute(q, ps).fetchall():
            sk = r["skeleton"] or _sig(r["expr"])
            new = _family_of(sk) if sk else ""
            if new != (r["family"] or ""):
                changed += 1
                if not dry_run:
                    con.execute("UPDATE submit_ready SET family=? WHERE id=?", (new, r["id"]))
        if not dry_run:
            con.commit()
        return changed
    finally:
        con.close()


def list_ready(region: Optional[str] = None, db_path: Optional[str] = None,
               all_status: bool = False) -> List[Dict[str, Any]]:
    """列出候选（默认仅 READY），按优先级降序。"""
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
        return sorted(rows, key=priority, reverse=True)
    finally:
        con.close()


def list_prod_blocked(region: Optional[str] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """列出「模拟层全过、仅被生产池 prod/self 撞墙」的候选（2026-09-30 用户口径）。

    这类候选不是废品：S/F/2Y/T 与 RA 硬闸全 PASS，只是提交会撞 0.7 相关性墙。
    它们**不应直接 POST**（POST 会进一步污染生产池、废掉同族兄弟），而应等生产池
    有空间（新提交退市 / 池子结构变化）时再复核。按「离 0.7 最近的」优先排序
    ——prod 越接近 0.7 越有希望在池子松动后翻过。"""
    con = connect(db_path)
    try:
        ensure_table(con)
        q = "SELECT * FROM submit_ready WHERE status=?"
        ps: List[Any] = [STATUS_PROD_BLOCKED]
        if region:
            q += " AND region = ?"
            ps.append(region)
        rows = [dict(r) for r in con.execute(q, ps).fetchall()]
        # 按「离墙距离」升序：prod/self 越接近 0.7 越靠前
        def _gap(r):
            vals = [v for v in (r.get("prod"), r.get("self")) if v is not None]
            return min((abs(LIM["prod"] - v) for v in vals), default=9.9)
        return sorted(rows, key=lambda r: (-(r.get("fitness") or 0), _gap(r)))
    finally:
        con.close()
