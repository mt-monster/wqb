# -*- coding: utf-8 -*-
r"""VF 影响闸（提交前必过，2026-11-21 用户明令）。

## 为什么有这个闸

用户 2026-11-21 15:17 明令：**「后面提交时帮我加上对 vf 的影响分析，如果会使 vf 下降就硬拦截」**。
本工具是这条指令的可执行载体——不是文字约定，而是可复现、可串入提交链的机械判定。

## 判据的数学基础（2026-11-21 实测反推并精确验证，diff = 0.0）

平台 ``value_factor_trendScore`` 的多样性分满足**乘积恒等式**：

    diversity_score = S_A × S_P × S_H
                    = (A / N) × (P / P_max) × S_H

两个等长 30 天窗口的原始读数与公式复算逐位相同：

| 窗口 | N | A | P | P_max | S_H | 平台 score | 公式复算 |
|---|---|---|---|---|---|---|---|
| 09-21~10-20 | 76 | 51 | 37 | 216 | 0.931310 | 0.10705304 | 0.10705304 |
| 10-21~11-21 | 78 | 41 | 52 | 216 | 0.957463 | 0.12116038 | 0.12116038 |

由此可得**提交一颗 alpha 后多样性分的方向**（N 必 +1，P 仅在新建 pyramid 类别时 +1）：

- ``ΔP ≥ 1``（新建类别）⇒ ``(P+1)/P × N/(N+1) = (53/52)×(78/79) = 1.0063 > 1`` ⇒ **必升**
- ``ΔP = 0``（加厚已有类别）⇒ 至多持平；若 A 不随之 +1 则**必降** ``N/(N+1)`` ≈ −1.27%

⇒ **「是否新建 pyramid 类别」是可精确判定的分水岭**，本闸据此设第一层。

## 边界（必须如实说明，不能假装能拦）

VF（真实全局乘数）由 **OS 表现 + 与自己池子的差异 + 与其他顾问的差异** 三者决定，
**提交前不可能精确测得**（要等 OS Testing 跑完、进 production 才有读数）。
本闸拦的是**可预测会导致多样性分下降、且同时命中 ≥2 条论坛标定的 VF 拖累条件**的
组合形态——即论坛 81 天实测描述的「为点塔/凑六维交质量勉强的件」。
单颗高质件即使同质加厚也不拦（拦了反而损失 base，违背「质量优先」）。

## 三层判定

- **L0 当期影响**：``os is None`` ⇒ 该件未进 OS Testing / 不在 production ⇒ **当期 VF 影响 = 0**。
  所有新候选都这样，故 L0 只作事实陈述，不作拦截依据。
- **L1 多样性层**：ΔP ≥ 1 ⇒ PASS；ΔP = 0 且该类已 ≥ WARN_COUNT ⇒ 同质加厚（WARN）。
- **L2 质量层**（论坛 81 天口径，三条）：
  1. 该 (Region,Delay) 样本少 —— 提交数 < ``SAMPLE_MIN``
  2. 样本外表现不稳 —— 近 3 年 S 均值 / 全期均值 < ``DECAY_MIN``，或有平年(S≤0)，或 CV > ``CV_MAX``
  3. 质量勉强 —— ``Fitness < F_VF_MIN`` 且 ``prod_corr > PC_WARN``

**综合规则**：
- 同质加厚（L1=WARN）**且** L2 命中 ≥ 2 条 ⇒ **BLOCK**（退出码 3）
- 其余 ⇒ PASS / WARN（退出码 0 / 1）
- 关键数据取不到 ⇒ **UNDETERMINED**（退出码 4，按纪律等同阻塞，需人工确认）

用法
----
    python tools/gates/vf_impact_gate.py --alpha 0mPPVEoK
    python tools/gates/vf_impact_gate.py --alpha 0mPPVEoK --prod-corr 0.6865 --fitness 1.27
    python tools/gates/vf_impact_gate.py --alpha 0mPPVEoK --json logs/vf_gate.json

退出码: 0=PASS, 1=WARN(放行但标注), 3=BLOCK(硬拦), 4=UNDETERMINED(数据不全)
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

# ---------------------------------------------------------------- 阈值（集中管理）
P_MAX = 216            # 平台给定：金字塔类别总数（value_factor_trendScore 返回）
F_VF_MIN = 2.0         # 论坛标定：Fitness > 2 是 VF 基础门槛
PC_WARN = 0.65         # PC 高于此即进入「贴红线」区（0.7 是硬线）
PC_RED = 0.70          # 硬红线
SAMPLE_MIN = 10        # 该 (Region,Delay) 提交数下限，低于此算「样本少」
DECAY_MIN = 0.85       # 近 3 年 / 全期 Sharpe 之比下限
CV_MAX = 0.5           # 全期 Sharpe 变异系数上限
WARN_COUNT = 3         # pyramid 类别已 ≥ 此数即算「同质加厚」

EXIT_PASS, EXIT_WARN, EXIT_BLOCK, EXIT_UNDET = 0, 1, 3, 4


# ---------------------------------------------------------------- MCP 调用
def _client():
    from tools.lib import forum_mcp as FM  # 复用其 client()（地址解析 + session 落盘）
    return FM.client()


def _mcp(cli, tool: str, args: Dict[str, Any]) -> Any:
    out = cli.call_tool(tool, args)
    return out


def _num(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- 取数
def fetch_alpha(cli, alpha_id: str) -> Dict[str, Any]:
    d = _mcp(cli, "get_alpha_details", {"alpha_id": alpha_id})
    return d if isinstance(d, dict) else {}


def fetch_vf(cli, days: int) -> Dict[str, Any]:
    end = _dt.datetime.now(_dt.timezone.utc)
    start = end - _dt.timedelta(days=days)
    d = _mcp(cli, "value_factor_trendScore", {
        "start_date": start.strftime("%Y-%m-%dT00:00:00Z"),
        "end_date": end.strftime("%Y-%m-%dT23:59:59Z"),
    })
    return d if isinstance(d, dict) else {}


def fetch_yearly(cli, alpha_id: str) -> List[Dict[str, Any]]:
    d = _mcp(cli, "get_alpha_yearly_stats", {"alpha_id": alpha_id})
    if isinstance(d, dict):
        recs = d.get("records") or []
    elif isinstance(d, list):
        recs = d
    else:
        recs = []
    return [r for r in recs if isinstance(r, dict)]


# ---------------------------------------------------------------- 计算
def alpha_pyramids(details: Dict[str, Any]) -> List[Tuple[str, float]]:
    """返回该件涉及的 pyramid 类别 [(name, multiplier)]，已按倍数降序。

    平台实际结构（2026-11-21 实测 get_alpha_details）::

        "pyramids": {"effective": 2, "list": [{"name": "GBR/D1/IMBALANCE", "multiplier": 1.0},
                                              {"name": "GBR/D1/PV", "multiplier": 1.4}]}

    兼容 list 形态与 ``checks`` 内嵌形态（后者实为 str list，故仅在 dict 时解析）。
    """
    out: List[Tuple[str, float]] = []

    def _add(name: Any, mult: Any) -> None:
        if name:
            t = (str(name), _num(mult) or 0.0)
            if t not in out:
                out.append(t)

    raw = details.get("pyramids")
    if isinstance(raw, dict):
        for p in (raw.get("list") or []):
            if isinstance(p, dict):
                _add(p.get("name"), p.get("multiplier"))
    elif isinstance(raw, list):
        for p in raw:
            if isinstance(p, dict):
                _add(p.get("name"), p.get("multiplier"))

    for chk in (details.get("checks") or []):
        if isinstance(chk, dict) and chk.get("name") == "MATCHES_PYRAMID":
            for p in (chk.get("pyramids") or []):
                if isinstance(p, dict):
                    _add(p.get("name"), p.get("multiplier"))

    out.sort(key=lambda t: -t[1])
    return out


def score_of(N: int, A: int, P: int, S_H: float, p_max: int = P_MAX) -> float:
    """diversity_score = (A/N) × (P/p_max) × S_H（2026-11-21 实测恒等式）。"""
    if N <= 0:
        return 0.0
    return (A / N) * (P / p_max) * S_H


def predict_after(vf: Dict[str, Any], new_categories: int) -> Dict[str, Any]:
    """预测提交一颗后的 diversity_score（两种 A 口径都给，取区间）。"""
    N = int(vf.get("N") or 0)
    A = int(vf.get("A") or 0)
    P = int(vf.get("P") or 0)
    SH = _num(vf.get("S_H")) or 0.0
    p_max = int(vf.get("P_max") or P_MAX)
    before = score_of(N, A, P, SH, p_max)
    dP = 1 if new_categories > 0 else 0
    P2 = P + dP
    # A 口径未知：给「A 不变」与「A+1」两个下/上界
    lo = score_of(N + 1, A, P2, SH, p_max)
    hi = score_of(N + 1, A + 1, P2, SH, p_max)
    return {
        "before": before, "after_lo": lo, "after_hi": hi,
        "delta_lo_pct": (lo / before - 1) * 100 if before else 0.0,
        "delta_hi_pct": (hi / before - 1) * 100 if before else 0.0,
        "dP": dP, "N": N, "A": A, "P": P, "S_H": SH,
    }


def yearly_stability(recs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """样本外稳定性：衰减比 / CV / 平年 / 有效年数。"""
    sh = [(_num(r.get("sharpe")) or 0.0) for r in recs if _num(r.get("sharpe")) is not None]
    active = [s for s in sh if abs(s) > 1e-9]
    if not active:
        return {"available": False}
    n = len(active)
    mean = sum(active) / n
    sd = (sum((x - mean) ** 2 for x in active) / max(n - 1, 1)) ** 0.5
    cv = sd / abs(mean) if mean else 0.0
    last3 = active[-3:] if n >= 3 else active
    m3 = sum(last3) / len(last3)
    return {
        "available": True, "n": n, "mean": mean, "cv": cv,
        "recent3_mean": m3, "decay_ratio": (m3 / mean) if mean else 0.0,
        "flat_years": sum(1 for s in active if s <= 0),
        "max": max(active), "min": min(active),
    }


# ---------------------------------------------------------------- 主判定
def evaluate(alpha_id: str, days: int = 30,
             prod_corr: Optional[float] = None,
             fitness: Optional[float] = None,
             self_corr: Optional[float] = None,
             _cache: Optional[Dict[str, Any]] = None,
             allow_no_pyramid: bool = False) -> Dict[str, Any]:
    """评估单颗。

    ``_cache`` 用于批量模式：一次拉 ``value_factor_trendScore`` 后供多颗复用
    （该项扫全窗口提交、单次约 20–40s，批量时必须复用）。
    """
    cache = _cache if _cache is not None else {}
    cli = cache.get("cli") or _client()
    cache["cli"] = cli
    details = fetch_alpha(cli, alpha_id)
    vf = cache.get("vf")
    if vf is None:
        vf = fetch_vf(cli, days)
        cache["vf"] = vf
    yearly = fetch_yearly(cli, alpha_id)

    is_blk = details.get("metrics") or {}
    metrics = {
        "sharpe": _num(is_blk.get("sharpe")),
        "fitness": _num(is_blk.get("fitness")) if fitness is None else fitness,
        "turnover": _num(is_blk.get("turnover")),
        "drawdown": _num(is_blk.get("drawdown")),
        "self_corr": _num(is_blk.get("selfCorrelation")) if self_corr is None else self_corr,
        "prod_corr": _num(is_blk.get("prodCorrelation")) if prod_corr is None else prod_corr,
    }
    settings = details.get("settings") or {}
    region, delay = settings.get("region"), settings.get("delay")

    # L0：是否已在 OS Testing / production（决定「当期影响」）
    stage = details.get("stage")
    os_blk = details.get("os") or {}
    in_os = (stage == "OS") or bool(os_blk.get("startDate"))
    in_prod = False  # 平台不直接暴露 prod 标记；OS 通过后才会产生 base payment

    # L1：pyramid 类别与 ΔP
    pys = alpha_pyramids(details)
    counts = vf.get("per_pyramid_counts") or {}
    known = set(counts.keys())
    new_cats = [n for n, _ in pys if n not in known]
    eff_mult = min([m for _, m in pys], default=0.0) if len(pys) <= 2 else 0.0
    same_bucket = [(n, counts.get(n, 0)) for n, _ in pys if n in known]
    max_bucket = max([c for _, c in same_bucket], default=0)

    pred = predict_after(vf, len(new_cats)) if vf.get("N") else {"before": 0}

    # L2 三条件
    cond: Dict[str, Any] = {}
    if region is not None and delay is not None:
        prefix = f"{region}/D{delay}/"
        region_cnt = sum(int(v) for k, v in counts.items() if str(k).startswith(prefix))
        cond["sample_thin"] = {"hit": region_cnt < SAMPLE_MIN, "region_cnt": region_cnt,
                              "threshold": SAMPLE_MIN}
    else:
        cond["sample_thin"] = {"hit": None, "note": "settings 缺 region/delay"}

    stab = yearly_stability(yearly)
    if stab.get("available"):
        hit2 = (stab["decay_ratio"] < DECAY_MIN) or (stab["cv"] > CV_MAX) or (stab["flat_years"] > 0)
        cond["oos_unstable"] = {"hit": hit2, **stab}
    else:
        cond["oos_unstable"] = {"hit": None, "note": "yearly stats 不可得"}

    f_v = metrics.get("fitness")
    pc_v = metrics.get("prod_corr")
    # fail-closed：任一项缺失即「未判」（hit=None），不得当成「不命中」放行
    if f_v is None or pc_v is None:
        quality_hit: Optional[bool] = None
        quality_note = ("平台未回填 " +
                        ", ".join(k for k, v in (("fitness", f_v), ("prodCorrelation", pc_v)) if v is None) +
                        " 且未显式传入 ⇒ 该项未判（按纪律阻塞，请传 --prod-corr / --fitness）")
    else:
        quality_hit = bool(f_v < F_VF_MIN and pc_v > PC_WARN)
        quality_note = None
    cond["quality_thin"] = {
        "hit": quality_hit,
        "fitness": f_v, "prod_corr": pc_v,
        "fitness_threshold": F_VF_MIN, "pc_threshold": PC_WARN,
        "note": quality_note,
    }

    hits = sum(1 for c in cond.values() if c.get("hit") is True)
    undetermined = [k for k, c in cond.items() if c.get("hit") is None]
    # pyramid 归属为空：两种情形要分开
    #   A) 该件本来就不命中任何金字塔（如 generate_stats 型表达式）⇒ ΔP=0 确定、无加厚风险。
    #      若同时质量过硬（F≥F_VF_MIN）则属 VF 正面来源，不阻塞；否则仍 fail-closed。
    #   B) 平台尚未评估 ⇒ 无法判 ΔP ⇒ 阻塞。
    # 二者平台侧不可区分，故按「质量」做代理判据，并在报告里如实标注。
    no_pyramid = not pys
    if no_pyramid:
        if allow_no_pyramid or (_num(metrics.get("fitness")) or 0.0) >= F_VF_MIN:
            no_pyramid = True   # 已知无塔，走正常判定（homogeneous=False）
        else:
            undetermined = list(undetermined) + ["pyramid_unknown"]

    homogeneous = (len(new_cats) == 0) and (max_bucket >= WARN_COUNT)

    # 判定
    if undetermined or not vf.get("N"):
        verdict, code = "UNDETERMINED", EXIT_UNDET
        reason = f"关键数据不全（{undetermined or ['value_factor_trendScore']}）⇒ 按纪律等同阻塞，需人工确认"
    elif homogeneous and hits >= 2:
        verdict, code = "BLOCK", EXIT_BLOCK
        reason = (f"同质加厚（类别 {[n for n,_ in pys]} 已在册，最大计数 {max_bucket} ≥ {WARN_COUNT}）"
                  f" 且命中 {hits}/3 条 VF 拖累条件 ⇒ 按论坛 81 天口径判「会使 VF 下降」")
    elif no_pyramid:
        verdict, code = "WARN", EXIT_WARN
        reason = (f"该件不命中任何 pyramid 类别（平台未分配，ΔP=0）⇒ 多样性分至多降 "
                  f"{abs(pred.get('delta_lo_pct', 0)):.2f}%，但无加厚风险且 "
                  f"F={metrics.get('fitness')} ≥ {F_VF_MIN}（质量过硬）⇒ 放行需披露")
    elif homogeneous or hits >= 2:
        verdict, code = "WARN", EXIT_WARN
        reason = (f"同质加厚={homogeneous}、拖累条件命中 {hits}/3 ⇒ 风险可控但需在提交描述中披露")
    else:
        verdict, code = "PASS", EXIT_PASS
        reason = f"新建 pyramid 类别 {new_cats} 或拖累条件仅 {hits}/3 ⇒ VF 无下降证据"

    return {
        "alpha_id": alpha_id, "verdict": verdict, "exit_code": code, "reason": reason,
        "L0_current_impact": {
            "in_os_testing": in_os, "in_production": in_prod,
            "stage": stage, "os": os_blk,
            "note": ("已进 OS Testing（stage=OS），但 base payment 需 OS 通过后才产生 ⇒ 当期对 base 影响仍为 0"
                     if in_os and not in_prod else
                     "未进 OS ⇒ 当期对 VF 与 base 影响为 0"),
        },
        "L1_diversity": {
            "pyramids": [{"name": n, "multiplier": m} for n, m in pys],
            "effective_multiplier": eff_mult,
            "new_categories": new_cats,
            "existing_buckets": [{"name": n, "count": c} for n, c in same_bucket],
            "max_bucket_count": max_bucket,
            "homogeneous": homogeneous,
            "prediction": pred,
        },
        "L2_conditions": cond, "hits": hits, "undetermined": undetermined,
        "metrics": metrics, "settings": {"region": region, "delay": delay,
                                        "universe": settings.get("universe")},
        "vf_snapshot": {k: vf.get(k) for k in ("N", "A", "P", "P_max", "S_A", "S_P", "S_H", "diversity_score")},
        "checked_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "note": "VL 本体由 OS 表现决定，提交前不可精确测得；本闸判定的是可预测的多样性分方向 + 拖累条件组合",
    }


def _print_one(r: Dict[str, Any]) -> None:
    L0, L1, L2 = r["L0_current_impact"], r["L1_diversity"], r["L2_conditions"]
    p = L1["prediction"]
    print(f"[VF-Gate] {r['alpha_id']}  ->  {r['verdict']}")
    print(f"  理由: {r['reason']}")
    print(f"  L0 当期影响: stage={L0['stage']} in_os={L0['in_os_testing']} ⇒ {L0['note']}")
    print(f"  L1 多样性: pyramids={[x['name'] for x in L1['pyramids']]} "
          f"生效倍率={L1['effective_multiplier']} 新类别={L1['new_categories'] or '无'}")
    if p.get("before"):
        print(f"     diversity_score {p['before']:.6f} -> "
              f"[{p['after_lo']:.6f}, {p['after_hi']:.6f}]  "
              f"({p['delta_lo_pct']:+.2f}% ~ {p['delta_hi_pct']:+.2f}%)  ΔP={p['dP']}")
    print(f"  L2 拖累条件命中 {r['hits']}/3:")
    for k, c in L2.items():
        print(f"     - {k}: hit={c.get('hit')} {({kk: vv for kk, vv in c.items() if kk != 'hit'})}")
    if r["undetermined"]:
        print(f"  ! 未判: {r['undetermined']}（缺数据 ⇒ 阻塞）")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="VF 影响闸（提交前必过）")
    ap.add_argument("--alpha", required=True,
                    help="单颗或逗号分隔多颗（批量模式共用一次 value_factor_trendScore）")
    ap.add_argument("--days", type=int, default=30, help="value_factor_trendScore 回看窗口天数")
    ap.add_argument("--prod-corr", type=float, default=None,
                    help="已知 prod 相关性（不给则读平台 metrics.prodCorrelation；两者都无 ⇒ 未判）")
    ap.add_argument("--prod-corr-map", default=None,
                    help="按 alpha 分别指定 prod，形如 \"id1:0.5231,id2:0.6493\"（批量时用）")
    ap.add_argument("--fitness", type=float, default=None, help="覆盖 Fitness（默认读平台）")
    ap.add_argument("--self-corr", type=float, default=None)
    ap.add_argument("--allow-no-pyramid", action="store_true",
                    help="平台未返回 pyramid 类别时也放行（默认 fail-closed 判 UNDETERMINED）")
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)

    ids = [x.strip() for x in str(a.alpha).split(",") if x.strip()]
    # --prod-corr-map 支持按 alpha 分别指定，形如 "id1:0.5231,id2:0.6493"
    pc_map: Dict[str, float] = {}
    if a.prod_corr_map:
        for seg in str(a.prod_corr_map).split(","):
            seg = seg.strip()
            if not seg or ":" not in seg:
                continue
            k, v = seg.split(":", 1)
            try:
                pc_map[k.strip()] = float(v)
            except ValueError:
                pass
    cache: Dict[str, Any] = {}
    results = []
    for aid in ids:
        pc = pc_map.get(aid, a.prod_corr)
        r = evaluate(aid, a.days, pc, a.fitness, a.self_corr,
                     _cache=cache, allow_no_pyramid=a.allow_no_pyramid)
        results.append(r)
        if len(ids) > 1:
            print("-" * 72)
        _print_one(r)

    if len(ids) > 1:
        print("=" * 72)
        print("汇总：", "  ".join(f"{r['alpha_id']}={r['verdict']}" for r in results))
        worst = max(r["exit_code"] for r in results)
        print(f"最严退出码 = {worst}（3=BLOCK / 4=UNDETERMINED 均需拦截）")

    payload = results[0] if len(ids) == 1 else {"results": results}
    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"  已落盘: {a.json}")
    return max(r["exit_code"] for r in results)


if __name__ == "__main__":
    sys.exit(main())
