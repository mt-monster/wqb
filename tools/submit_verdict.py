# -*- coding: utf-8 -*-
"""submit_verdict.py - 提交层判定（替代手动 GET/POST /alphas/{id}/submit 探针）。

头部教训（KOR PPA 2026-08-22 实锤）：模拟详情里 LOW_FITNESS/LOW_2Y_SHARPE 显示
WARNING（不挡模拟、不进 fail 列表），但 POST submit 时平台重新评估为 FAIL——只看
get_alpha_details 的 checks.fail=[] 会误判"可提交"。判定必须走提交层：
GET /alphas/{id}/submit 的 403 检查列表（零成本，不消耗提交配额）。

本工具输出双视图：
  1) 模拟层：get_alpha_details 的 checks fail/warning 逐条
  2) 提交层：GET /alphas/{id}/submit —— 200 无检查=可提交；403 带检查列表=BLOCKED 及原因

用法:
  python tools/submit_verdict.py --alpha-id 2rlRAZaZ
  python tools/submit_verdict.py --alpha-id 2rlRAZaZ

退出码: 0=可直接提交（模拟无 FAIL 且提交层 200）, 1=BLOCKED/未就绪
运行环境: 使用 MCP venv（`$WQ_PY` 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import argparse
import asyncio
import os
import sys


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _bootstrap():
    py = _mcp_venv_python()
    if py and os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)
    mcp = os.environ.get("WQ_MCP_DIR", r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp")
    sys.path.insert(0, mcp)


def _render_checks(checks):
    if not checks:
        return "  (无检查项)"
    return "\n".join(
        f"  [{c.get('name')}] {c.get('result')} value={c.get('value')} limit={c.get('limit')}"
        for c in checks)


async def main():
    ap = argparse.ArgumentParser(description="提交层判定：模拟层 + GET /alphas/{id}/submit 双视图")
    ap.add_argument("--alpha-id", required=True)
    ap.add_argument("--with-quota", action="store_true", help="（已废弃：配额检查已于 2026-08-25 移除，此参数无效果）")
    a = ap.parse_args()

    _bootstrap()
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    detail = await brain.get_alpha_details(a.alpha_id)
    status = detail.get("status")
    is_ = detail.get("is") or {}
    sim_checks = is_.get("checks") or []
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

    # 提交层判定：GET /alphas/{id}/submit（零成本）
    submit_url = f"{brain.base_url}/alphas/{a.alpha_id}/submit"
    resp = await brain._request("GET", submit_url)
    layer_checks = []
    submit_status = resp.status_code
    if resp.status_code == 200:
        body = resp.json() if resp.text else {}
        layer_checks = (body.get("is") or {}).get("checks") or []
    elif resp.status_code == 403:
        body = resp.json() if resp.text else {}
        layer_checks = body.get("checks") or body.get("detail") or []
        if isinstance(layer_checks, list) and layer_checks and isinstance(layer_checks[0], str):
            layer_checks = [{"name": c, "result": "FAIL"} for c in layer_checks]

    print(f"\n--- 提交层 GET /alphas/{a.alpha_id}/submit: HTTP {submit_status} ---")
    if submit_status == 200:
        print("  OK：无 403 拦截，可直接走 POST submit")
    elif submit_status == 403:
        print("  BLOCKED：提交层重新评估为 FAIL（模拟 WARNING 升级实锤）")
        print(_render_checks(layer_checks) if isinstance(layer_checks, list) else f"  {layer_checks}")
    elif submit_status == 404 and status == "UNSUBMITTED":
        # 2026-09-01 实证（RR7OWQKd）：处女提交（从未 POST 过）的 alpha，GET /submit
        # 无提交记录 → 404。这不是候选缺陷，是提交层视图本身不可用——
        # 403 升级检查只有 POST 之后才存在。此时以模拟层 + 双闸预检
        # （check_self_correlation 本地 + check_correlation("production") 平台新鲜值）为准；
        # POST 201 异步受理后会翻 OS（~40s），再次 POST 得到的 403 是"已提交"拒绝而非硬闸失败。
        print("  PREPOST：处女提交无提交记录（404），提交层视图不可用。")
        print("  → 以模拟层（上方 checks）+ 双闸预检为准；POST 201 后 ~40s 内翻 OS 为成功实证。")
    else:
        print(f"  非预期响应 {submit_status}：{str(resp.text)[:300]}")

    # 配额检查已移除（2026-08-25 用户要求）
    # if a.with_quota:
    #     q = await brain.get_submission_quota()
    #     print(f"\n--- 提交配额 ---")
    #     print(f"  rolling  剩余: {q.get('rolling', {}).get('remaining', '?')}")
    #     print(f"  daily    剩余: {q.get('daily', {}).get('remaining', '?')}")

    # 判定：模拟层无 FAIL，且提交层为 200，或处女提交 404（视图不可用，降级为模拟层判定）
    prepost_unverifiable = submit_status == 404 and status == "UNSUBMITTED"
    ok = not fails and (submit_status == 200 or prepost_unverifiable)
    print(f"\nVERDICT: {'SUBMITTABLE' if ok else 'BLOCKED'}")
    if not fails and prepost_unverifiable:
        print("  判定依据: 模拟层无 FAIL + 处女提交 404（提交层降级为模拟层+双闸预检）")
    elif fails:
        print("  原因: 模拟层 checks 存在 FAIL，先优化再试")
    elif submit_status == 403:
        print("  原因: 提交层 403，见上检查列表（模拟层 WARNING 已升级）")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    asyncio.run(main())