# -*- coding: utf-8 -*-
"""submit_verdict.py - 提交层判定（替代手动 GET/POST /alphas/{id}/submit 探针）。

头部教训（KOR PPA 2026-08-22 实锤）：模拟详情里 LOW_FITNESS/LOW_2Y_SHARPE 显示
WARNING（不挡模拟、不进 fail 列表），但 POST submit 时平台重新评估为 FAIL——只看
get_alpha_details 的 checks.fail=[] 会误判"可提交"。

本工具输出双视图：
  1) 模拟层：get_alpha_details 的 checks fail/warning + WebDataScope Failed RA/PPA 计数
  2) 提交层：GET /alphas/{id}/submit —— **平台恒返 404**（2026-09-26 实测，ACTIVE 者也 404），
     该视图已定性为死端点，200/403 分支只作防御保留；**真闸只有用户确认后的 POST submit**
     （三态响应 + 异步补发，见 worldquant-submit-alpha）。

判定口径 = **否决权威**（只能拦，不能放）：BLOCKED 即不提交；不 BLOCKED 时仍需
「平台 prod<0.7（另跑 check_correlation(refresh=True)）+ 用户明确确认」。
判定逻辑的唯一实现在 ``wqb.submit_verdict_core``（本 CLI、MCP submit_verdict、
tools/batch_submit_verdict.py 共用）。

用法:
  python tools/submit_verdict.py --alpha-id 2rlRAZaZ [--json]

退出码（2026-09-29 起；此前 SUBMITTABLE / UNVERIFIABLE / ALREADY_SUBMITTED 都是 0，
以 `$?==0` 放行的脚本会把「提交层无信息」的 UNVERIFIABLE 当成可提交——不要再这样写）:
  0  = SUBMITTABLE       （现实中不会出现：GET /submit 恒 404）
  1  = BLOCKED           （含未捕获异常：fail closed）
  10 = UNVERIFIABLE      （模拟层干净但提交层无信息；须另跑 check_correlation + 用户确认）
  11 = ALREADY_SUBMITTED （已 ACTIVE/SUBMITTED；勿再 POST）
  2  = 参数错误（argparse）
运行环境: MCP venv（`WQ_PY` 或 world-quant-brain-mcp/.venv，自动 re-exec），依赖 brain_api。
"""
import argparse
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/MCP 目录解析（tools/_pyenv.py）


def _bootstrap():
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()


def _render_checks(checks):
    if not checks:
        return "  (无检查项)"
    return "\n".join(
        f"  [{c.get('name')}] {c.get('result')} value={c.get('value')} limit={c.get('limit')}"
        for c in checks)


async def main():
    ap = argparse.ArgumentParser(description="提交层判定：模拟层 + GET /alphas/{id}/submit 双视图（否决权威）")
    ap.add_argument("--alpha-id", required=True)
    ap.add_argument("--json", action="store_true", help="末行追加机器可读 JSON（含 exit_code / reason_code）")
    a = ap.parse_args()

    _bootstrap()
    from brain_api import BrainApiClient  # noqa: F402
    from wqb.submit_verdict_core import (EXIT_CODES, decide, is_already_submitted,  # noqa: F402
                                         normalize_submit_layer)
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    detail = await brain.get_alpha_details(a.alpha_id)
    status = detail.get("status")
    sim_checks = (detail.get("is") or {}).get("checks") or []
    fails = [c for c in sim_checks if c.get("result") == "FAIL"]
    warns = [c for c in sim_checks if c.get("result") == "WARNING"]
    print(f"=== alpha {a.alpha_id} status={status} ===")
    print(f"--- 模拟层 checks: {len(sim_checks)} 条 "
          f"(FAIL {len(fails)} / WARNING {len(warns)}) ---")
    if fails:
        print(_render_checks(fails))
    if warns:
        print("  [warning 条目不挡模拟，但提交层可能升级为 FAIL，见下]")
        print(_render_checks(warns))
    if not fails and not warns:
        print("  (无 FAIL/WARNING)")

    if is_already_submitted(detail):
        result = decide(a.alpha_id, detail)
        print(f"\nVERDICT: {result['verdict']}（status={status}）")
        print(f"  {result['verdict_note']}")
        return _finish(result, a.json, EXIT_CODES)

    # 提交层：GET /alphas/{id}/submit（零成本；平台恒 404，见头注）
    submit_url = f"{brain.base_url}/alphas/{a.alpha_id}/submit"
    resp = await brain._request("GET", submit_url)
    body = resp.json() if (resp.status_code in (200, 403) and resp.text) else {}
    result = decide(a.alpha_id, detail, resp.status_code, normalize_submit_layer(resp.status_code, body))

    print("\n--- WebDataScope Failed-count 资格门（REGULAR 看 RA / PPA 看 PPA）---")
    print(f"  Failed RA = {result['failed_ra']}；Failed PPA = {result['failed_ppa']}"
          + f"（本候选按 {'PPA' if result['is_ppa'] else 'REGULAR'} 判定）")
    for it in (result["failed_ppa_items"] if result["is_ppa"] else result["failed_ra_items"]):
        print(f"    [{it['name']}] {it['result']} value={it['value']} limit={it['limit']}")

    ss = result["submit_status"]
    print(f"\n--- 提交层 GET /alphas/{a.alpha_id}/submit: HTTP {ss} ---")
    if ss == 200:
        print("  OK：无 403 拦截（防御分支；平台现状恒 404）")
    elif ss == 403:
        print("  BLOCKED：提交层重新评估为 FAIL（模拟 WARNING 升级实锤）")
        print(_render_checks(result["submit_checks"]))
    elif result["prepost_unverifiable"]:
        # 2026-09-01 实证（RR7OWQKd）：处女提交（从未 POST 过）的 alpha，GET /submit 无提交记录 → 404。
        # 不是候选缺陷，是提交层视图本身不可用——403 升级检查只有 POST 之后才存在。
        print("  PREPOST：处女提交无提交记录（404），提交层视图不可用。")
        print("  → 以模拟层（上方 checks）+ 平台 prod 实测为准，不要用 POST 试探。")
    else:
        print(f"  非预期响应 {ss}：{str(resp.text)[:300]}")

    print(f"\nVERDICT: {result['verdict']}  (exit {result['exit_code']}, {result['reason_code']})")
    if result["verdict"] == "BLOCKED":
        print(f"  原因: {result['verdict_note']}")
    elif result["verdict_note"]:
        print(f"  {result['verdict_note']}")
    print(f"  下一步: {result['next_step']}")

    # 队列状态升级：仅 SUBMITTABLE（防御分支）时把待提交队列该条 IS_ONLY → SUBMIT_LAYER_VERIFIED。
    # 容错：绝不影响判定结果与退出码。
    if result["verdict"] == "SUBMITTABLE":
        try:
            from wqb.store.submit_queue import mark_verified
            is_ = detail.get("is") or {}
            n = mark_verified(a.alpha_id, rec={
                "sharpe": is_.get("sharpe"), "fitness": is_.get("fitness"),
                "turnover": is_.get("turnover"),
            })
            print(f"  [queue] 已升级 SUBMIT_LAYER_VERIFIED（{n} 条）" if n
                  else "  [queue] 队列中无此条，跳过升级")
        except Exception as e:  # noqa: BLE001
            print(f"  [queue] 升级跳过：{e}")
    return _finish(result, a.json, EXIT_CODES)


def _finish(result, as_json, exit_codes):
    if as_json:
        print(json.dumps({k: result.get(k) for k in (
            "alpha_id", "alpha_status", "verdict", "exit_code", "reason_code", "next_step",
            "failed_ra", "failed_ppa", "submit_status", "is_ppa")}, ensure_ascii=False))
    sys.exit(exit_codes[result["verdict"]])


if __name__ == "__main__":
    asyncio.run(main())
