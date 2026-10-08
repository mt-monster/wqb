# -*- coding: utf-8 -*-
"""perf_max.py — 全闸通过 alpha 的**业绩极致优化**（gate-preserving performance maximization）。

定位（与相邻组件的边界）：
  - tools/submit_verdict.py = 提交前否决闸（判「能不能交」）；
  - workflow nodes/alpha_booster.py = S4 短板修复（把卡闸候选修到通过）；
  - **本工具 = 候选已全闸通过（failed_ra=0）之后**，在「全闸保持绿」的硬约束下
    把业绩指标（fitness / sharpe / returns / margin …）推到极致，产出「更优的同想法变体」。
  - 优化方法论对齐 wq-brain-alpha-optimization-v1 Mode A：等价算子替换优先、
    扫描维度纪律（禁扫 truncation、decay 0/1 留一、nanHandling/maxTrade 是强度闸只做对照）、
    每轮候选上限 8（--max-per-round 可调，multi-sim 硬上限 10）。
  - ★ 零提交路径：本工具不含任何 POST /alphas/{id}/submit；产出候选后仍走
    submit_verdict → 用户逐次授权的既有提交链。

三段式（全部断点续跑：plan.json 原子写 tmp+replace，harvest 只补缺失项）：
  1) plan    拉 baseline（brain_client.get_alpha_details）→ 前置闸校验（须 failed_ra=0）
             → 生成变体梯（表达式杠杆 + 设置杠杆）→ 本地预检（op_arity 元数 / 算子存在性）
             → 写 plan.json + variants_<tag>.txt + dispatch_spec.json（submit_batch --spec 兼容）
             → 打印下一步命令（派发用 tools/submit_batch.py，收割用 tools/harvest_multisim.py，
               二者是仓库仅有的两条回测客户端，本工具不新增第三套）
  2) harvest 把变体的实测指标回填进 plan.json（--alpha-ids 直给 / --from-harvest 收批 JSON
             / --map LABEL=ID 手工映射），逐条判定「闸保持」并按目标指标打分
  3) report  排名表（闸保持者置顶、破闸者 REJECT）、per-metric 冠军、相对 baseline 的改进幅度、
             推荐行；--write-ledger 落挖掘台账（默认 dry-run，--apply 才写）

判定口径（阈值唯一来源 = src/wqb/config.py，本文件不复写数字）：
  - 闸保持 = checks.fail 为空 且 ra_failed_checks 为空 且 turnover ∈ PLATFORM_CHECK_LINES["turnover_range"]
  - 目标指标默认 fitness（平台自有综合指标）；--objective 可选 sharpe/fitness/returns/margin/pnl
  - prod/self 相关性是终验项（>48h 规则），report 只提示、不在此调用（占账号级单并发队列）

用法：
  python tools/perf_max.py plan --alpha-id RR6bv6rz --objective fitness
  python tools/perf_max.py plan --baseline-json baseline.json --region USA   # 离线基线
  python tools/submit_batch.py --spec tracking/USA/perfmax/RR6bv6rz_<ts>/dispatch_spec.json
  python tools/harvest_multisim.py --multisim-id <id> --json-out harvest.json
  python tools/perf_max.py harvest --plan-dir tracking/USA/perfmax/RR6bv6rz_<ts> \
      --from-harvest harvest.json          # 或 --alpha-ids EQ_QUANTILE=AbCd1234 ...
  python tools/perf_max.py report --plan-dir tracking/USA/perfmax/RR6bv6rz_<ts>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

from pathlib import Path as _Path

_REPO = next(_p for _p in _Path(__file__).resolve().parents if (_p / "pyproject.toml").exists() and (_p / "src" / "wqb").is_dir())
sys.path.insert(0, str(_REPO / "tools"))
import _pyenv  # noqa: E402,F401  跨平台解释器/MCP 目录解析（串仓防护）

REPO = str(_REPO)
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.config import PLATFORM_CHECK_LINES  # noqa: E402  阈值唯一来源，禁止本文件复写数字

DEFAULT_OBJECTIVE = "fitness"
MAX_PER_ROUND_DEFAULT = 8          # Mode A 每轮候选上限（multi-sim 硬上限 10）
OPS_BUDGET = 10                    # 算子调用点预算（闸 1b-2 口径：<10）

# ---------------------------------------------------------------------------
# 变体梯（lever ladder）——顺序即优先级；前两级多为「一次动多个闸」的高杠杆
# ---------------------------------------------------------------------------

#: L1 等价算子替换（外层分布变换互换；KOR/USA 实证 signed_power(0.5)↔quantile 是最强一档）
EQ_TRANSFORMS: List[Tuple[str, str]] = [
    ("EQ_QUANTILE", "quantile({x}, sigma=1.0)"),
    ("EQ_SP05", "signed_power({x}, 0.5)"),
    ("EQ_WINS2", "winsorize({x}, std=2)"),
    ("EQ_NORMSTD", "normalize({x}, useStd=true)"),
]

#: L2 幂次网格（基线外层已是 signed_power 时改为指数重扫）
POW_EXPONENTS: List[Tuple[str, str]] = [
    ("POW_05", 0.5), ("POW_07", 0.7), ("POW_15", 1.5), ("POW_20", 2.0),
]

#: L3 平滑窗口微扫倍率（作用于最外层 ts_mean / ts_decay_linear 的窗口）
WIN_FACTORS: List[Tuple[str, float]] = [("WIN_HALF", 0.5), ("WIN_DBL", 2.0)]

#: L4 decay 档倍率（设置杠杆；0/1 重复档已按纪律剔除，上限对齐平台上限）
DECAY_FACTORS: List[Tuple[str, float]] = [("DECAY_HALF", 0.5), ("DECAY_DBL", 2.0)]
DECAY_CAP = 512                    # 平台 decay 上限（实测）

#: L5 强度闸对照（nanHandling/maxTrade 是强度闸不是风格开关——只做 1-2 槽对照）
CTRL_VARIANTS: List[Tuple[str, Dict[str, Any]]] = [
    ("CTRL_NANOFF", {"nanHandling": "OFF"}),
]


# ---------------------------------------------------------------------------
# baseline / 指标解析
# ---------------------------------------------------------------------------

def _mget(d: Dict[str, Any], *names: str) -> Any:
    """多键名兼容取值（平台原始 camelCase 与 MCP processed snake_case 并存）。"""
    for n in names:
        if d.get(n) is not None:
            return d.get(n)
    return None


def _investability_sharpe(val: Any) -> Any:
    """investabilityConstrained 可能是 dict（{sharpe,fitness}）或标量。"""
    if isinstance(val, dict):
        return val.get("sharpe")
    return val if isinstance(val, (int, float)) else None


def _flatten_raw_details(details: Dict[str, Any]) -> Dict[str, Any]:
    """平台原始 get_alpha_details 形态（code 在 regular.code、指标在 is.*、
    is.checks 为 [{name,result,limit,value}…] 列表）→ 统一快照。

    RA 失败/挂起口径一律走 `wqb.config.compute_webdata_failed_counts`（单源，勿复写）。
    """
    from wqb.config import RA_2Y_NAMES, compute_webdata_failed_counts
    isb = details.get("is") or {}
    checks = [c for c in (isb.get("checks") or []) if isinstance(c, dict)]
    counts = compute_webdata_failed_counts(checks)

    def _chk_value(name: str) -> Any:
        for c in checks:
            if c.get("name") == name:
                return c.get("value")
        return None

    two_y = None
    for nm in RA_2Y_NAMES:
        v = _chk_value(nm)
        if v is not None:
            two_y = v
            break

    fail_pairs = [{"name": c.get("name"), "value": c.get("value"), "limit": c.get("limit")}
                  for c in checks if c.get("result") == "FAIL"]
    warn_names = [c.get("name") for c in checks if c.get("result") == "WARNING"]
    metrics = {
        "sharpe": isb.get("sharpe"),
        "fitness": isb.get("fitness"),
        "turnover": isb.get("turnover"),
        "returns": isb.get("returns"),
        "margin": isb.get("margin"),
        "pnl": isb.get("pnl"),
        "drawdown": isb.get("drawdown"),
        "long_count": isb.get("longCount"),
        "short_count": isb.get("shortCount"),
        "investability_constrained_sharpe": _investability_sharpe(
            isb.get("investabilityConstrained")),
        "cluster_test": _chk_value("CLUSTER_TEST"),
        "two_year_sharpe": two_y,
        "sub_universe_sharpe": _chk_value("LOW_SUB_UNIVERSE_SHARPE"),
    }
    return {
        "alpha_id": details.get("id"),
        "code": details.get("code") or (details.get("regular") or {}).get("code"),
        "settings": dict(details.get("settings") or {}),
        "metrics": metrics,
        "sharpe": metrics.get("sharpe"),
        "fitness": metrics.get("fitness"),
        "turnover": metrics.get("turnover"),
        "returns": metrics.get("returns"),
        "margin": metrics.get("margin"),
        "pnl": metrics.get("pnl"),
        "drawdown": metrics.get("drawdown"),
        "long_count": metrics.get("long_count"),
        "short_count": metrics.get("short_count"),
        "investability_constrained_sharpe": metrics.get("investability_constrained_sharpe"),
        "cluster_test": metrics.get("cluster_test"),
        "towers": list(details.get("pyramids") or []),
        "two_year_sharpe": metrics.get("two_year_sharpe"),
        "sub_universe_sharpe": metrics.get("sub_universe_sharpe"),
        "checks_fail": fail_pairs,
        "checks_fail_names": [p["name"] for p in fail_pairs if p.get("name")],
        "checks_warn_names": [n for n in warn_names if n],
        "ra_failed_checks": list(counts.get("ra_failed_names") or []),
        "failed_ra_count": counts.get("failed_ra"),
        "ra_pending_count": counts.get("pending_ra"),
    }


def flatten_details(details: Dict[str, Any]) -> Dict[str, Any]:
    """把 get_alpha_details 的 metrics/checks/ra 摊平成单层快照（便于比较与存储）。

    吃两种形态：平台原始（is/regular）与预摊平（metrics/checks/ra 顶层）。
    """
    if not details.get("metrics") and isinstance(details.get("is"), dict):
        return _flatten_raw_details(details)
    from wqb.config import RA_CHECK_NAMES
    metrics = dict(details.get("metrics") or {})
    checks = details.get("checks") or {}
    ra = details.get("ra") or {}
    fail_names = []
    fail_pairs = []
    for item in checks.get("fail") or []:
        if isinstance(item, dict):
            fail_names.append(item.get("name"))
            fail_pairs.append({"name": item.get("name"), "value": item.get("value"),
                               "limit": item.get("limit")})
        else:
            fail_names.append(item)
    warn_names = []
    for item in checks.get("warning") or []:
        warn_names.append(item.get("name") if isinstance(item, dict) else item)
    return {
        "alpha_id": details.get("id"),
        "code": details.get("code"),
        "settings": dict(details.get("settings") or {}),
        "metrics": metrics,
        "sharpe": metrics.get("sharpe"),
        "fitness": metrics.get("fitness"),
        "turnover": metrics.get("turnover"),
        "returns": metrics.get("returns"),
        "margin": metrics.get("margin"),
        "pnl": metrics.get("pnl"),
        "drawdown": _mget(metrics, "drawdown"),
        "long_count": _mget(metrics, "long_count", "longCount"),
        "short_count": _mget(metrics, "short_count", "shortCount"),
        "investability_constrained_sharpe": _investability_sharpe(
            _mget(metrics, "investability_constrained_sharpe",
                  "investability_sharpe", "investabilityConstrained")),
        "cluster_test": _mget(metrics, "cluster_test", "clusterTest"),
        "towers": list(details.get("towers") or details.get("pyramids") or []),
        "two_year_sharpe": metrics.get("two_year_sharpe"),
        "sub_universe_sharpe": metrics.get("sub_universe_sharpe"),
        "checks_fail": fail_pairs,
        "checks_fail_names": [n for n in fail_names if n],
        "checks_warn_names": [n for n in warn_names if n],
        "ra_failed_checks": list(ra.get("ra_failed_checks") or []),
        "failed_ra_count": ra.get("failed_ra_count"),
        # 只数「名单内」PENDING（SELF/PROD 等名单外不计不卡，口径同 wqb.config）
        "ra_pending_count": sum(
            1 for n in list(ra.get("ra_pending_names") or []) + [
                (i.get("name") if isinstance(i, dict) else i)
                for i in (checks.get("pending") or [])
            ] if n in RA_CHECK_NAMES),
    }


def gate_status(snap: Dict[str, Any]) -> Dict[str, Any]:
    """闸保持判定：fail 空 + ra_failed_checks 空 + turnover 在平台区间内。"""
    broken: List[str] = []
    broken.extend(snap.get("checks_fail_names") or [])
    broken.extend(snap.get("ra_failed_checks") or [])
    tvr = snap.get("turnover")
    trange = PLATFORM_CHECK_LINES.get("turnover_range") or (None, None)
    lo, hi = trange[0], trange[1]
    if tvr is not None and lo is not None and hi is not None:
        if not (float(lo) <= float(tvr) <= float(hi)):
            broken.append(f"TURNOVER_OUT_OF_RANGE({tvr})")
    broken = sorted(set(broken))
    return {"preserved": not broken, "broken": broken}


def score_variant(snap: Dict[str, Any], objective: str) -> Optional[float]:
    """目标指标打分（越大越好）；缺失返回 None（未知不报 0）。"""
    v = snap.get(objective)
    if v is None:
        v = (snap.get("metrics") or {}).get(objective)
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def improvement(baseline: Dict[str, Any], snap: Dict[str, Any], objective: str) -> Optional[float]:
    b = score_variant(baseline, objective)
    v = score_variant(snap, objective)
    if b is None or v is None:
        return None
    return v - b


# ---------------------------------------------------------------------------
# 变体生成（确定性：同一 baseline + 同一参数 ⇒ 同一变体表，便于续跑对齐）
# ---------------------------------------------------------------------------

_OUTER_RE = re.compile(r"^\s*([a-z_][a-z0-9_]*)\s*\(")
_SIGNED_POWER_RE = re.compile(r"^signed_power\s*\((.*)\)\s*$", re.S)
_WIN_RE = re.compile(r"\b(ts_mean|ts_decay_linear)\s*\(")


def _strip_outer(expr: str) -> Tuple[str, Optional[str]]:
    """剥掉最外层调用，返回 (全部实参文本, 外层算子名)；剥不动返回 (原式, None)。"""
    expr = expr.strip()
    m = _OUTER_RE.match(expr)
    if not m:
        return expr, None
    name = m.group(1)
    if not expr.endswith(")"):
        return expr, None
    depth = 0
    for i, ch in enumerate(expr):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and i != len(expr) - 1:
                return expr, None          # 顶层不止一个调用，不剥
    inner = expr[m.end():-1]
    return inner, name


def _split_top_args(argstr: str) -> List[str]:
    """按**顶层逗号**切分实参（跳过括号内的逗号与命名参数整段）。"""
    parts, depth, cur = [], 0, []
    for ch in argstr:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur).strip())
    return [p for p in parts if p]


def _first_positional(argstr: str) -> str:
    """取第一个位置参数（命名参数 name=value 不算）——包裹类变换的 x 位。"""
    for p in _split_top_args(argstr):
        if re.match(r"^[a-z_][a-z0-9_]*\s*=", p):
            continue
        return p
    return argstr.strip()


def _wrap_variants(base_code: str) -> List[Dict[str, Any]]:
    """L1/L2 包裹类变体：按 baseline 外层形态选择等价替换或幂次重扫。"""
    out: List[Dict[str, Any]] = []
    inner, outer = _strip_outer(base_code)
    x_pos = _first_positional(inner) if outer else base_code.strip()
    if outer == "signed_power":
        # 基线已是幂 ⇒ L1 等价替换（换成其它分布变换）+ L2 指数重扫
        for label, tpl in EQ_TRANSFORMS:
            if label == "EQ_SP05":
                continue
            out.append({"label": label, "lever": "EQ",
                        "expr": tpl.format(x=x_pos), "settings_patch": {}})
        m = _SIGNED_POWER_RE.match(base_code.strip())
        if m:
            body = _first_positional(m.group(1).rsplit(",", 1)[0])
            for label, y in POW_EXPONENTS:
                out.append({"label": f"POW_RE_{str(y).replace('.', '')}", "lever": "POW",
                            "expr": f"signed_power({body}, {y})", "settings_patch": {}})
    elif outer == "quantile":
        for label, tpl in EQ_TRANSFORMS:
            if label == "EQ_QUANTILE":
                continue
            out.append({"label": label, "lever": "EQ",
                        "expr": tpl.format(x=x_pos), "settings_patch": {}})
    else:
        for label, tpl in EQ_TRANSFORMS:
            out.append({"label": label, "lever": "EQ",
                        "expr": tpl.format(x=x_pos), "settings_patch": {}})
    return out


def _window_variants(base_code: str) -> List[Dict[str, Any]]:
    """L3 窗口微扫：只改**最外层** ts_mean/ts_decay_linear 的窗口参数（其余冻结）。"""
    out: List[Dict[str, Any]] = []
    for m in _WIN_RE.finditer(base_code):
        start = m.end() - 1
        depth = 0
        end = None
        for i in range(start, len(base_code)):
            ch = base_code[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end is None:
            continue
        call = base_code[m.start():end + 1]
        inner, _ = _strip_outer(call)
        parts = _split_top_args(inner)
        if len(parts) < 2:
            continue
        try:
            win = int(parts[-1].strip())
        except ValueError:
            continue
        head = base_code[:m.start()] + call[:call.rfind(",")]
        tail = base_code[end + 1:]           # 跳过 call 的右括号（head 重组时会补回）
        for label, factor in WIN_FACTORS:
            w2 = max(2, int(round(win * factor)))
            out.append({"label": f"{label}_{w2}", "lever": "WIN",
                        "expr": f"{head}, {w2}){tail}", "settings_patch": {}})
        break    # 只动最外层一处，避免组合爆炸
    return out


def _settings_variants(base_settings: Dict[str, Any]) -> List[Dict[str, Any]]:
    """L4 decay 档（0/1 留一、封顶平台上限）+ L5 强度闸对照。"""
    out: List[Dict[str, Any]] = []
    decay = int(base_settings.get("decay") or 0)
    seen = {decay}
    for label, factor in DECAY_FACTORS:
        d2 = int(round(decay * factor))
        d2 = max(1, min(DECAY_CAP, d2))
        if d2 in seen:
            continue
        seen.add(d2)
        out.append({"label": f"{label}_{d2}", "lever": "DECAY",
                    "expr": None, "settings_patch": {"decay": d2}})
    for label, patch in CTRL_VARIANTS:
        if all(base_settings.get(k) != v for k, v in patch.items()):
            out.append({"label": label, "lever": "CTRL",
                        "expr": None, "settings_patch": patch})
    return out


def count_ops(expr: str) -> int:
    """算子调用点计数（闸 1b-2 口径；以 op_arity 的 call-site 解析为准，失败回退正则）。"""
    try:
        from wqb.expression.op_arity import iter_call_sites
        return len(iter_call_sites(expr))
    except Exception:
        return len(re.findall(r"[a-z_][a-z0-9_]*\s*\(", expr))


def generate_variants(base_code: str, base_settings: Dict[str, Any],
                      max_per_round: int = MAX_PER_ROUND_DEFAULT) -> List[Dict[str, Any]]:
    """生成变体梯（确定性顺序 EQ → POW → WIN → DECAY → CTRL，截断到 max_per_round）。

    - 表达式变体逐个过 op_arity 元数校验，违规者记 broken_reason 并跳过（不进批）；
    - 算子数超预算（>= OPS_BUDGET）者跳过；
    - 与 baseline 表达式完全相同者去重。
    """
    cands: List[Dict[str, Any]] = []
    cands.extend(_wrap_variants(base_code))
    cands.extend(_window_variants(base_code))
    cands.extend(_settings_variants(base_settings))

    out: List[Dict[str, Any]] = []
    seen_exprs = {base_code.strip()}
    for cand in cands:
        if len(out) >= max_per_round:
            break
        expr = cand.get("expr")
        if expr is not None:
            expr = expr.strip()
            cand["expr"] = expr
            if expr in seen_exprs:
                continue
            if count_ops(expr) >= OPS_BUDGET:
                continue
            try:
                from wqb.expression.op_arity import check_expressions
                rep = check_expressions([expr])
                if not rep.get("ok"):
                    continue
            except Exception:
                pass
            seen_exprs.add(expr)
        cand.setdefault("status", "planned")
        cand.setdefault("alpha_id", None)
        cand.setdefault("result", None)
        out.append(cand)
    return out


# ---------------------------------------------------------------------------
# plan.json 读写（原子写；断点续跑只补缺失）
# ---------------------------------------------------------------------------

def atomic_write_json(path: str, payload: Any) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, default=str)
    os.replace(tmp, path)


def load_plan(plan_dir: str) -> Dict[str, Any]:
    with open(os.path.join(plan_dir, "plan.json"), encoding="utf-8") as f:
        return json.load(f)


def save_plan(plan_dir: str, plan: Dict[str, Any]) -> None:
    atomic_write_json(os.path.join(plan_dir, "plan.json"), plan)


def dispatch_groups(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """把变体按 settings_patch 分组为 submit_batch --spec 的批次条目。"""
    groups: Dict[str, Dict[str, Any]] = {}
    for v in plan["variants"]:
        patch = v.get("settings_patch") or {}
        key = json.dumps(patch, sort_keys=True)
        g = groups.setdefault(key, {"tag": v["label"] if not patch else
                                   "_".join(f"{k}{val}" for k, val in sorted(patch.items())),
                                   "settings_patch": patch, "labels": [], "exprs": []})
        g["labels"].append(v["label"])
        if v.get("expr") is not None:
            g["exprs"].append(v["expr"])
        elif v.get("base_expr"):
            g["exprs"].append(v["base_expr"])
    return list(groups.values())


# ---------------------------------------------------------------------------
# submit_ready 入队（可交付必入 —— 用户从 submit_ready 取当日候选比较提交）
# ---------------------------------------------------------------------------

def _fetch_corr_brain(alpha_id: str) -> Tuple[Optional[float], Optional[float]]:
    """实测 prod/self（与 tools/submit_queue.py::add 同口径）：拿得到一律当场落库。"""
    from wqb.workflow._common import get_brain_client, run_async
    client = get_brain_client()
    prod = selfc = None
    try:
        p = run_async(client.get_production_correlation(alpha_id))
        prod = p.get("max") if isinstance(p, dict) else None
    except Exception:
        pass
    try:
        r = run_async(client.check_self_correlation(alpha_id, correlation_type="self"))
        selfc = r.get("max_correlation") if isinstance(r, dict) else None
    except Exception:
        pass
    return prod, selfc


def build_enqueue_record(snap: Dict[str, Any], plan: Optional[Dict[str, Any]] = None
                         ) -> Dict[str, Any]:
    """摊平快照 → submit_ready 全字段记录（入队铁律：拿得到的字段一律带上）。

    阈值与 READY/DEAD 判定**不在此复写**，由 `wqb.store.submit_queue.gate_of` 单源决定。
    """
    from wqb.store.submit_queue import family_of_expr
    s = snap.get("settings") or {}
    expr = snap.get("code")
    return {
        "alpha_id": snap.get("alpha_id"),
        "region": s.get("region") or (plan or {}).get("region") or "USA",
        "universe": s.get("universe"),
        "delay": s.get("delay"),
        "decay": s.get("decay"),
        "neutralization": s.get("neutralization"),
        "expr": expr,
        "alpha_type": "REGULAR",
        "sharpe": snap.get("sharpe"),
        "fitness": snap.get("fitness"),
        "turnover": snap.get("turnover"),
        "two_year": snap.get("two_year_sharpe"),
        "sub_universe": snap.get("sub_universe_sharpe"),
        "cluster_test": snap.get("cluster_test"),
        "margin": snap.get("margin"),
        "returns": snap.get("returns"),
        "drawdown": snap.get("drawdown"),
        "long_count": snap.get("long_count"),
        "short_count": snap.get("short_count"),
        "investability_constrained_sharpe": snap.get("investability_constrained_sharpe"),
        "risk_neutralized_sharpe": snap.get("risk_neutralized_sharpe"),
        "prod": snap.get("prod"),
        "self": snap.get("self"),
        "towers": json.dumps(snap.get("towers") or [], ensure_ascii=False),
        "family": family_of_expr(expr) if expr else None,
    }


def enqueue_deliverables(plan: Dict[str, Any], fetch_corr=None, dry_run: bool = False,
                         note: str = "", db_path: Optional[str] = None
                         ) -> List[Dict[str, Any]]:
    """把 plan 里**闸保持**且已有 alpha_id 的变体入队 submit_ready（可交付必入）。

    - prod/self 用 fetch_corr(alpha_id) 实测注入（默认走平台；测试可注入桩）；
    - 入队后跑列填充审计，缺失列明示不静默；
    - dry_run=True 时事务回滚（演练不落盘）；db_path 仅供测试隔离。
    返回 [{label, alpha_id, gate, status, audit_missing}]。
    """
    from wqb.store import submit_queue as sq
    fetch_corr = fetch_corr or _fetch_corr_brain
    out: List[Dict[str, Any]] = []
    con = sq.connect(db_path)
    try:
        sq.ensure_table(con)
        for v in plan.get("variants") or []:
            r = v.get("result")
            if not r or not r.get("alpha_id"):
                continue
            if not (r.get("gate") or {}).get("preserved"):
                continue
            snap = dict(r)
            try:
                prod, selfc = fetch_corr(snap["alpha_id"])
                snap["prod"], snap["self"] = prod, selfc
            except Exception as e:  # 相关性拿不到不挡入队（gate_of 会标 IS_ONLY）
                print(f"  [queue] {snap['alpha_id']} prod/self 取数失败: {e}")
            rec = build_enqueue_record(snap, plan)
            gate = sq.enqueue(con, rec,
                              note=note or f"perfmax {plan.get('alpha_id')} {v['label']}")
            missing = sq.column_fill_audit(con, rec["alpha_id"], rec["region"]) or []
            status = con.execute(
                "SELECT status FROM submit_ready WHERE alpha_id=? AND region=?",
                (rec["alpha_id"], rec["region"])).fetchone()
            out.append({"label": v["label"], "alpha_id": rec["alpha_id"],
                        "gate": gate, "status": status[0] if status else None,
                        "audit_missing": missing})
            print(f"  [queue] {v['label']} {rec['alpha_id']} → {gate} "
                  f"({status[0] if status else '?'})"
                  + (f" 未填列: {','.join(missing)}" if missing else " 列填充完整"))
        if dry_run:
            con.rollback()
            print("[queue] dry-run，未写入")
        else:
            con.commit()
    finally:
        con.close()
    return out


# ---------------------------------------------------------------------------
# CLI：plan / harvest / report / enqueue
# ---------------------------------------------------------------------------

def _fetch_details_brain(alpha_id: str) -> Dict[str, Any]:
    from wqb.workflow._common import get_brain_client, run_async
    client = get_brain_client()
    return run_async(client.get_alpha_details(alpha_id))


def cmd_plan(args: argparse.Namespace) -> int:
    if args.baseline_json:
        with open(args.baseline_json, encoding="utf-8") as f:
            details = json.load(f)
    elif args.alpha_id:
        details = _fetch_details_brain(args.alpha_id)
        code = (details or {}).get("code") or ((details or {}).get("regular") or {}).get("code")
        if not details or details.get("__error__") or not code:
            print(f"[plan] 拉取 baseline 失败: {str(details)[:200]}")
            return 2
    else:
        print("[plan] 需要 --alpha-id 或 --baseline-json")
        return 2

    snap = flatten_details(details)
    ra_failed = snap.get("failed_ra_count")
    ra_pending = snap.get("ra_pending_count") or 0
    if ra_pending:
        print(f"[plan] 前置闸不满足：baseline 名单内 PENDING={ra_pending} 项未算完"
              "（failed_ra=0 只表示暂无失败；等平台算完再判，不得放行）")
        return 1
    if ra_failed not in (0, "0"):
        print(f"[plan] 前置闸不满足：baseline failed_ra_count={ra_failed} "
              f"（本工具只接受全闸通过的 alpha；卡闸候选走 alpha_booster/Mode B）")
        return 1

    region = (snap.get("settings") or {}).get("region") or args.region or "USA"
    alpha_id = snap.get("alpha_id") or args.alpha_id or "offline"
    plan_dir = args.plan_dir or os.path.join(
        REPO, "tracking", region, "perfmax", f"{alpha_id}_{time.strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(plan_dir, exist_ok=True)

    variants = generate_variants(snap["code"], snap.get("settings") or {},
                                 max_per_round=args.max_per_round)
    for v in variants:
        if v.get("expr") is None:
            v["base_expr"] = snap["code"]
    plan = {
        "tool": "perf_max",
        "alpha_id": alpha_id,
        "region": region,
        "objective": args.objective,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "baseline": snap,
        "variants": variants,
    }
    save_plan(plan_dir, plan)

    # 派生产物：variants_<tag>.txt + dispatch_spec.json（submit_batch --spec 兼容）
    # ⚠ spec 条目须携带**全量 baseline 设置**（submit_batch 按 SETTINGS_PASSTHROUGH
    # 白名单透传进 settings）；只写 patch 会让 decay/neutralization 等退回工具缺省
    # （decay=None 被平台 400 拒收）。
    base_settings = {k: v for k, v in (snap.get("settings") or {}).items() if v is not None}
    spec = []
    for g in dispatch_groups(plan):
        if not g["exprs"]:
            continue
        txt = os.path.join(plan_dir, f"variants_{g['tag']}.txt")
        with open(txt, "w", encoding="utf-8") as f:
            f.write("\n".join(g["exprs"]) + "\n")
        entry: Dict[str, Any] = {"path": txt}
        entry.update(base_settings)
        entry.update(g["settings_patch"] or {})
        spec.append(entry)
    atomic_write_json(os.path.join(plan_dir, "dispatch_spec.json"), spec)

    print(f"[plan] baseline={alpha_id} objective={args.objective}")
    print(f"[plan] variants={len(variants)} -> {plan_dir}")
    for v in variants:
        patch = v.get("settings_patch") or {}
        desc = v.get("expr") if v.get("expr") is not None else f"settings={patch}"
        print(f"  {v['label']:<16} [{v['lever']}] {desc[:110]}")
    print("[next] python tools/submit_batch.py --spec "
          f"{os.path.join(plan_dir, 'dispatch_spec.json')}")
    print(f"[next] python tools/perf_max.py harvest --plan-dir {plan_dir} --alpha-ids L=ID ...")
    return 0


def _match_from_harvest(plan: Dict[str, Any], harvest_rows: List[Dict[str, Any]]) -> Dict[str, str]:
    """收批 JSON → {label: alpha_id} 映射：先按表达式文本匹配，再按批内顺序兜底。"""
    mapping: Dict[str, str] = {}
    rows = []
    for r in harvest_rows:
        if isinstance(r, dict) and r.get("alphas"):
            rows.extend(r["alphas"])
        elif isinstance(r, dict):
            rows.append(r)
    by_expr = {}
    for row in rows:
        code = row.get("code") or row.get("expression") or row.get("expr")
        if code and row.get("alpha_id"):
            by_expr.setdefault(code.strip(), []).append(row["alpha_id"])
    unmatched = []
    for v in plan["variants"]:
        expr = v.get("expr") or v.get("base_expr")
        if expr and by_expr.get(expr.strip()):
            mapping[v["label"]] = by_expr[expr.strip()].pop(0)
        else:
            unmatched.append(v["label"])
    for row, v in zip(rows, [v for v in plan["variants"] if v["label"] in unmatched]):
        if row.get("alpha_id"):
            mapping[v["label"]] = row["alpha_id"]
    return mapping


def cmd_harvest(args: argparse.Namespace) -> int:
    plan = load_plan(args.plan_dir)
    mapping: Dict[str, str] = {}
    if args.from_harvest:
        with open(args.from_harvest, encoding="utf-8") as f:
            harvest_rows = json.load(f)
        mapping.update(_match_from_harvest(plan, harvest_rows))
    for pair in args.alpha_ids or []:
        if "=" not in pair:
            print(f"[harvest] --alpha-ids 项须为 LABEL=ID，收到: {pair}")
            return 2
        label, aid = pair.split("=", 1)
        mapping[label.strip()] = aid.strip()

    fetched = 0
    for v in plan["variants"]:
        aid = mapping.get(v["label"])
        if not aid:
            continue
        if v.get("result") and args.skip_done and not getattr(args, "refresh", False):
            continue                      # 断点续跑：已收割的不重取（--refresh 强制补字段重取）
        details = _fetch_details_brain(aid)
        if not details or details.get("__error__"):
            print(f"[harvest] {v['label']}({aid}) 拉取失败: {str(details)[:120]}")
            continue
        snap = flatten_details(details)
        snap["gate"] = gate_status(snap)
        snap["score"] = score_variant(snap, plan.get("objective") or DEFAULT_OBJECTIVE)
        v["alpha_id"] = aid
        v["result"] = snap
        v["status"] = "harvested"
        fetched += 1
        save_plan(args.plan_dir, plan)              # 每条即存（原子写），中断可续
    print(f"[harvest] fetched={fetched} / planned={len(plan['variants'])}")
    remaining = [v["label"] for v in plan["variants"] if not v.get("result")]
    if remaining:
        print(f"[harvest] 未收割: {', '.join(remaining)}（补 --alpha-ids 或 --from-harvest）")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    plan = load_plan(args.plan_dir)
    base = plan.get("baseline") or {}
    objective = plan.get("objective") or DEFAULT_OBJECTIVE
    rows = []
    for v in plan["variants"]:
        r = v.get("result")
        if not r:
            continue
        gate = r.get("gate") or {}
        rows.append((v["label"], v.get("lever"), r, gate))
    if not rows:
        print("[report] 无已收割结果（先 harvest）")
        return 1

    preserved = [x for x in rows if x[3].get("preserved")]
    rejected = [x for x in rows if not x[3].get("preserved")]

    def _key(row):
        s = score_variant(row[2], objective)
        return (s is not None, s if s is not None else 0.0)

    preserved.sort(key=_key, reverse=True)
    print(f"==== perf_max report ({plan.get('alpha_id')} objective={objective}) ====")
    b_score = score_variant(base, objective)
    print(f"baseline: {objective}={b_score} sharpe={base.get('sharpe')} "
          f"fitness={base.get('fitness')} 2Y={base.get('two_year_sharpe')} "
          f"SUB={base.get('sub_universe_sharpe')} TO={base.get('turnover')}")
    print(f"-- 闸保持 {len(preserved)} / 破闸 {len(rejected)} --")
    hdr = f"{'label':<16} {'lever':<5} {'obj':>7} {'Δobj':>7} {'sharpe':>7} {'fitness':>7} {'2Y':>6} {'SUB':>6} {'TO':>7}"
    print(hdr)
    for label, lever, r, gate in preserved:
        d = improvement(base, r, objective)
        print(f"{label:<16} {lever:<5} {str(score_variant(r, objective)):>7} "
              f"{('%.4f' % d) if d is not None else '—':>7} "
              f"{str(r.get('sharpe')):>7} {str(r.get('fitness')):>7} "
              f"{str(r.get('two_year_sharpe')):>6} {str(r.get('sub_universe_sharpe')):>6} "
              f"{str(r.get('turnover')):>7}")
    for label, lever, r, gate in rejected:
        print(f"{label:<16} {lever:<5} REJECT 破闸: {','.join(gate.get('broken') or [])}")
    if preserved:
        best = preserved[0]
        d = improvement(base, best[2], objective)
        print(f"\n[推荐] {best[0]} (alpha_id={best[2].get('alpha_id')}) "
              f"{objective}={score_variant(best[2], objective)} "
              f"(baseline {b_score}, Δ={('%.4f' % d) if d is not None else '—'})")
        print("[提示] 提交前须 prod/self 终验（check_correlation refresh=True；>48h 规则）"
              "→ submit_verdict → 用户逐次授权；本工具零提交。")
    else:
        print("\n[推荐] 无——所有变体都破坏了闸门，baseline 保持原样即最优。")

    # ★ 可交付必入 submit_ready（2026-10-08 用户指令）：闸保持变体默认自动入队，
    #   用户后续从 submit_ready 取当日候选比较提交。--no-queue 跳过。
    if not getattr(args, "no_queue", False):
        deliverables = [x for x in preserved if x[2].get("alpha_id")]
        if deliverables:
            print(f"\n[queue] 闸保持且有 alpha_id 的 {len(deliverables)} 条 → submit_ready：")
            enqueue_deliverables(plan, dry_run=False)
        else:
            print("\n[queue] 无可入队变体（闸保持但缺 alpha_id，或全部破闸）")

    if args.write_ledger:
        label, lever, r, gate = (preserved[0] if preserved else (None, None, None, None))
        if r and r.get("alpha_id"):
            cmd = [sys.executable, os.path.join(REPO, "tools", "ledger", "mining_ledger.py"),
                   "add", "--alpha-id", r["alpha_id"], "--region", plan.get("region") or "USA",
                   "--wave", f"perfmax_{plan.get('alpha_id')}", "--src", "perf_max",
                   "--state", "SIM_OK"]
            if args.apply:
                import subprocess
                subprocess.run(cmd, check=False)
                print(f"[ledger] added {r['alpha_id']}")
            else:
                print(f"[ledger] DRY-RUN: {' '.join(cmd)}（--apply 才写）")
    return 0


def cmd_enqueue(args: argparse.Namespace) -> int:
    """独立入队入口：把 plan 里闸保持的变体补入 submit_ready（断点/补录用）。"""
    plan = load_plan(args.plan_dir)
    print(f"[enqueue] {plan.get('alpha_id')} → submit_ready"
          + (" (dry-run)" if args.dry_run else ""))
    res = enqueue_deliverables(plan, dry_run=args.dry_run)
    if not res:
        print("[enqueue] 无闸保持变体可入队（先 harvest 收割并确认闸保持）")
        return 1
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="perf_max",
                                description="全闸通过 alpha 的业绩极致优化（零提交）")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="生成优化变体梯与派发材料")
    p_plan.add_argument("--alpha-id")
    p_plan.add_argument("--baseline-json", help="离线 baseline（get_alpha_details 原样 JSON）")
    p_plan.add_argument("--region", default=None)
    p_plan.add_argument("--objective", default=DEFAULT_OBJECTIVE,
                        choices=["fitness", "sharpe", "returns", "margin", "pnl"])
    p_plan.add_argument("--max-per-round", type=int, default=MAX_PER_ROUND_DEFAULT)
    p_plan.add_argument("--plan-dir", default=None)
    p_plan.set_defaults(func=cmd_plan)

    p_h = sub.add_parser("harvest", help="回填变体实测指标并判定闸保持")
    p_h.add_argument("--plan-dir", required=True)
    p_h.add_argument("--alpha-ids", nargs="*", help="LABEL=ID 映射（可多组）")
    p_h.add_argument("--from-harvest", help="harvest_multisim.py --json-out 产物")
    p_h.add_argument("--skip-done", action="store_true", default=True)
    p_h.add_argument("--refresh", action="store_true",
                     help="已收割的也重取（补齐新摊平字段后刷新 plan.json）")
    p_h.set_defaults(func=cmd_harvest)

    p_r = sub.add_parser("report", help="排名表与推荐（默认把闸保持变体入队 submit_ready）")
    p_r.add_argument("--plan-dir", required=True)
    p_r.add_argument("--write-ledger", action="store_true")
    p_r.add_argument("--no-queue", action="store_true",
                     help="跳过「可交付必入 submit_ready」自动入队")
    p_r.add_argument("--apply", action="store_true",
                     help="配合 --write-ledger 真正写台账（默认 dry-run）")
    p_r.set_defaults(func=cmd_report)

    p_q = sub.add_parser("enqueue", help="闸保持变体补入 submit_ready（可交付必入）")
    p_q.add_argument("--plan-dir", required=True)
    p_q.add_argument("--dry-run", action="store_true", help="演练不落盘")
    p_q.set_defaults(func=cmd_enqueue)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
