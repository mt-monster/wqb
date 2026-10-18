#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闸失败归因 CLI —— 「只差一两闸」时先归因、再定向推闸（零仿真）。

机制来源：用户 2026-10-16 指令「只有一闸或二闸不过时，先做 robustness 归因，
有针对性地再推过闸，而不是盲推」。判定逻辑全在 :mod:`wqb.gate_attribution`，
本文件只负责**取数 + 渲染 + 退出码**。

用法（三种取数模式，都不消耗仿真配额）：

  1) 在线（最常用）：直接按 alpha id 拉平台读数
     python tools/gate_attribution.py --alpha-id bl82VavN

  2) 离线（MCP 已取到 / 单测 / 复用历史读数）：
     python tools/gate_attribution.py --from-json payload.json
     # payload.json = {"detail": <get_alpha_details 整份返回>, "yearly": [...],
     #                "correlation": {...}, "siblings": [...]}

  3) 只算 F 闸可行性（连 yearly / 相关性都不需要，纯闭式）：
     python tools/gate_attribution.py --sharpe 1.62 --returns 0.081 --turnover 0.2819

退出码（给流水线做分支用）：
  0  PUSH_TARGETED           归因出定向杠杆，按 rank 逐条推
  3  SWITCH_AXIS            机制层天花板／剪刀差 ⇒ 换字段或数据集，别刷参数
  4  BLOCKED_BY_CORRELATION  相关性余量 < 0.01，先找 prod 中性杠杆
  5  两闸以上                 不属「只差一两闸」，走常规多轮诊断
  2  参数 / 取数错误

设计约束（与仓库既有纪律一致）：
* **闸线取平台回传的 limit**，不取本仓常量（KOR D1 实测 LOW_SHARPE limit=1.58，
  而 config.PLATFORM_CHECK_LINES 记 1.25 —— 冲突时以平台为准）。
* **WARNING 计入 RA 失败**（平台 getAlphaCheckStates 口径），故 ``fail: []`` 不等于过闸。
* 只读：本工具不发仿真、不写 DB、不改 alpha。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "src"))

from wqb.gate_attribution import attribute, fitness_feasibility  # noqa: E402

EXIT_BY_VERDICT = {
    "READY": 0,
    "PUSH_TARGETED": 0,
    "PUSH_CORRELATION_CORNER": 0,
    "SWITCH_AXIS": 3,
    "BLOCKED_BY_CORRELATION": 4,
}


def _render(r: dict) -> None:
    print(f"=== 闸失败归因：{r.get('alpha_id')} ===")
    gates = r.get("failed_gates") or []
    print(f"失败闸 {r.get('gate_count')} 道（eligible_for_targeted_push="
          f"{r.get('eligible_for_targeted_push')}）：")
    for g in gates:
        print(f"  - {g['name']}: value={g['value']} limit={g['limit']} state={g['state']}")
    if not gates:
        print("  (无)")

    ya = r.get("yearly_attribution")
    if ya:
        print(f"\n逐年归因：sharpe类={ya['class_for_sharpe']} ladder类={ya['class_for_ladder']} "
              f"flags={ya['flags']}")
        print(f"  中位 S={ya['median_sharpe']}｜最差年 {ya['worst_year']}={ya['worst_year_sharpe']}"
              f"｜前段均值={ya['head_mean']}｜末2年均值={ya['tail2_mean']}")
        if not ya.get("sample_ok", True):
            print(f"  ⚠ 样本仅 {ya.get('n_years')} 年（<5）⇒「前段 vs 末2段」对比不成立，"
                  f"该归因按低置信度对待，不要据此换轴")

    ff = r.get("fitness_feasibility") or {}
    print(f"\nF 闸闭式可行性：TO 天花板={ff.get('to_target')}（地板 {ff.get('to_floor')}）"
          f"｜当前 TO={ff.get('current_to')}｜需砍={ff.get('to_cut_pct')}"
          f"｜{ff.get('arithmetic_verdict')}")

    sc = r.get("scissor")
    if sc:
        print(f"剪刀差：n={sc['n']} slope={sc['slope']} ⇒ S=1.58 时 prod={sc['prod_at_sharpe_158']}"
              f" → {sc['verdict']}")

    corr = r.get("correlations") or {}
    if corr.get("measured"):
        for k in ("prod", "self"):
            blk = corr.get(k)
            if isinstance(blk, dict):
                extra = f" headroom={blk['headroom']}" if blk.get("headroom") is not None else ""
                ws = blk.get("white_space_n_ge_0.6")
                ws_s = f" 白空间[0.6,∞) n={ws}" if ws is not None else ""
                print(f"相关性 {k}: max={blk.get('max')} passes={blk.get('passes')}{extra}{ws_s}")

    print("\n--- 逐闸归因与定向杠杆 ---")
    for d in r.get("diagnoses") or []:
        print(f"\n[{d['gate']}] cause={d['cause_class']} feasible={d['feasible']}")
        for lv in d.get("levers") or []:
            print(f"  #{lv['rank']} {lv['lever']}")
            print(f"      理由：{lv['rationale']}")
            print(f"      证据：{lv['evidence']}｜代价：{lv['cost']}")
        if d.get("note"):
            print(f"      注：{d['note']}")

    print(f"\n★ VERDICT: {r['verdict']}")
    print(f"★ STOP RULE: {r['stop_rule']}")
    print(f"★ 本次消耗仿真数：{r['simulations_consumed']}")


def _load_payload(path: str) -> dict:
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    return json.loads(raw)


async def _fetch(alpha_id: str, want_corr: bool) -> dict:
    import _pyenv

    # 注意：`_pyenv` 暴露的是 `bootstrap_paths()`（把 src/ 与 MCP 目录塞进 sys.path），
    # 没有 `_bootstrap()`。写错会在 --alpha-id 路径上直接抛 AttributeError。
    _pyenv.bootstrap_paths()
    from brain_api import BrainApiClient  # noqa: E402

    brain = BrainApiClient()
    await brain.ensure_authenticated()
    detail = await brain.get_alpha_details(alpha_id)
    payload: dict = {"alpha_id": alpha_id, "detail": detail}

    # 逐年（缺失不致命，只少一类归因）
    try:
        ys = await brain._request("GET", f"{brain.base_url}/alphas/{alpha_id}/recordsets/yearly-stats")
        if ys.status_code == 200 and ys.text:
            body = ys.json()
            payload["yearly"] = body.get("records") or body.get("yearly") or []
    except Exception as exc:  # noqa: BLE001 - 取数失败只降级不崩
        print(f"[warn] 逐年统计取数失败（降级，不影响其他归因）：{exc}", file=sys.stderr)

    if want_corr:
        corr: dict = {}
        for kind in ("production", "self"):
            got = await _poll_correlation(brain, alpha_id, kind)
            if got:
                corr[kind] = got
        if corr:
            payload["correlation"] = corr
        else:
            print("[warn] 相关性未取到（异步队列超时）；--correlation 会在"
                  "『RA 全过』时把裁决降级为 PUSH_TARGETED 而非 READY。", file=sys.stderr)
    return payload


async def _poll_correlation(brain, alpha_id: str, kind: str, attempts: int = 8) -> dict | None:
    """轮询相关性端点。

    ⚠ 该端点是**异步队列**：未就绪时返回 202 + ``Retry-After``（不是 200）。
    只判 ``status_code == 200`` 会静默拿不到值——2026-10-17 真实取数实证，
    表现为「加了 --correlation 但输出里没有相关性段」。
    """
    import asyncio

    url = f"{brain.base_url}/alphas/{alpha_id}/correlations/{kind}"
    for i in range(attempts):
        try:
            r = await brain._request("GET", url)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] {kind} 相关性请求异常：{exc}", file=sys.stderr)
            return None
        if r.status_code == 200 and r.text:
            try:
                return r.json()
            except Exception:  # noqa: BLE001
                return None
        if r.status_code != 202:
            print(f"[warn] {kind} 相关性返回 {r.status_code}：{r.text[:160]}", file=sys.stderr)
            return None
        wait = 1.0
        try:
            wait = min(float(r.headers.get("Retry-After") or 1.0), 5.0)
        except Exception:  # noqa: BLE001
            pass
        await asyncio.sleep(wait)
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="闸失败归因：只差一两闸时先归因再定向推闸")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--alpha-id", help="按 alpha id 在线取数（零仿真）")
    src.add_argument("--from-json", help="离线：payload JSON 文件路径（- = stdin）")
    src.add_argument("--sharpe", type=float, help="只做 F 闸闭式可行性：S")
    ap.add_argument("--returns", type=float, help="F 闸：returns")
    ap.add_argument("--turnover", type=float, help="F 闸：TO")
    ap.add_argument("--correlation", action="store_true", help="尝试在线拉相关性（裸 API 无此端点，失败会降级）")
    ap.add_argument("--prod-corr", type=float,
                    help="prod 相关性实测值（从 MCP check_correlation 抄；推荐用法）")
    ap.add_argument("--self-corr", type=float,
                    help="self 相关性实测值（从 MCP check_self_correlation 抄）")
    ap.add_argument("--json", action="store_true", help="末行追加机器可读 JSON")
    a = ap.parse_args()

    if a.sharpe is not None:
        if a.returns is None or a.turnover is None:
            print("--sharpe 需同时给 --returns 与 --turnover", file=sys.stderr)
            return 2
        feas = fitness_feasibility(a.sharpe, a.returns, a.turnover, target=1.0)
        print(json.dumps(feas, ensure_ascii=False, indent=2))
        return 0 if feas["arithmetic_verdict"] != "need_more_returns_or_sharpe" else 3

    try:
        if a.alpha_id:
            import asyncio

            payload = asyncio.run(_fetch(a.alpha_id, a.correlation))
        else:
            payload = _load_payload(a.from_json)
    except FileNotFoundError:
        print(f"读不到文件：{a.from_json}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"JSON 解析失败：{exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"取数失败：{exc}", file=sys.stderr)
        return 2

    # 手工喂入的相关性优先于在线取数（裸 API 无 /correlations 端点，只能本地算）
    if a.prod_corr is not None or a.self_corr is not None:
        corr = dict(payload.get("correlation") or {})
        if a.prod_corr is not None:
            corr["production"] = {"max_correlation": a.prod_corr,
                                  "passes_check": a.prod_corr < 0.70}
        if a.self_corr is not None:
            corr["self"] = {"max_correlation": a.self_corr,
                            "passes_check": a.self_corr < 0.70}
        payload["correlation"] = corr

    result = attribute(payload)
    _render(result)
    if a.json:
        print("\n---JSON---")
        print(json.dumps(result, ensure_ascii=False))
    if result.get("gate_count", 0) > 2:
        return 5
    return EXIT_BY_VERDICT.get(result["verdict"], 0)


if __name__ == "__main__":
    sys.exit(main())