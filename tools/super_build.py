# -*- coding: utf-8 -*-
"""super_build.py - SuperAlpha 组套流水线（替代 track_mea_super.py / _resume / _submit 三件套）。

配方来源：wq-brain-superalpha skill（实测验证，2026-08-22/23）：
  - selection: (1 + 0 * (prod_correlation > 0)) * (0.7 - prod_correlation) *
               (self_correlation < gate) * (turnover > 0.01) * (turnover < 0.5)
    （USA 必备 no-op 门控；逻辑符只能用 * / || / ==）
  - combo:     1 - maxCorr（generate_stats/self_corr/reduce_max 构造，压 SELF）
  - 关键杠杆：neutralization 用 SUBINDUSTRY（MARKET 地板 ~0.717 压不进 0.7）
  - 提交：description 各需 ≥100 英文字；name 用 prodCorrelation 最大值约定

子命令:
  select  创建 SUPER simulation（参数全 CLI，不再硬编码区域）
          python tools/super_build.py select --region MEA --universe TOP400 \
              --delay 1 --decay 5 --selection-limit 10 --self-gate 0.55
  status  查 SUPER 模拟状态与指标
          python tools/super_build.py status --alpha-id KPGvRMg1
  probe   零成本双闸探针（SELF 本地计算 + PROD 平台）
          python tools/super_build.py probe --alpha-id KPGvRMg1
  submit  设置属性（内置 ≥100 英文描述）+ 两次 submit 判定
          python tools/super_build.py submit --alpha-id KPGvRMg1 --name 0.6944

退出码: 0=成功（select 已创建 / probe 双闸过 / submit 已受理）, 1=失败
运行环境: 使用 MCP venv（`$WQ_PY` 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import argparse
import asyncio
import json
import os
import sys

REGION_HINT = {"USA": "the US equity market", "KOR": "the Korean equity market",
               "MEA": "the Middle East and Africa equity markets",
               "EUR": "the European equity market", "GBR": "the UK equity market",
               "IND": "the Indian equity market", "GLB": "the global equity market",
               "DEU": "the German equity market"}

SELECTION_TEMPLATE = (
    "(1 + 0 * (prod_correlation > 0)) * "
    "(0.7 - prod_correlation) * "
    "(self_correlation < {self_gate}) * "
    "(turnover > 0.01) * (turnover < 0.5)"
)
COMBO_TEMPLATE = (
    "stats = generate_stats(alpha); "
    "innerCorr = self_corr(stats.returns, 500); "
    "ic = if_else(innerCorr == 1.0, nan, innerCorr); "
    "maxCorr = reduce_max(ic); "
    "1 - maxCorr"
)


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


def build_selection_description(region, limit, gate):
    """selection_description：≥100 英文（平台硬门槛，勿缩写）。"""
    market = REGION_HINT.get(region, f"the {region} equity market")
    return (
        f"This selection expression defines which active regular alphas from {market} "
        f"become components of this SuperAlpha, and assigns each component its weight. "
        f"Every candidate is scored by its production correlation so that novel, "
        f"low-correlation signals are strongly preferred, which helps the combined "
        f"alpha keep its overall production correlation below the submission threshold "
        f"of zero point seven. A non-gating term keeps novel alphas with near-zero "
        f"production correlation from being zeroed out, while a hard self-correlation "
        f"gate removes components that are too similar to existing alphas in the book. "
        f"A turnover band between one and fifty percent controls trading costs and "
        f"ensures the selected components are tradable in live execution. The final "
        f"score multiplies all factors, and the platform retains the top {limit} "
        f"scoring components. Subindustry neutralization is used to decorrelate the "
        f"component signals from the current production book, which is the decisive "
        f"lever for passing the production correlation test. This description "
        f"documents the design intent, the correlation penalty structure, and every "
        f"hard gate applied before a candidate may enter the final combination."
    )


def build_combo_description(region):
    """combo_description：≥100 英文（平台硬门槛，勿缩写）。"""
    market = REGION_HINT.get(region, f"the {region} equity market")
    return (
        f"This combination expression aggregates the daily returns of every component "
        f"selected for {market} into a single SuperAlpha signal. It first computes the "
        f"rolling self-correlation between each pair of component return streams over "
        f"a five hundred day lookback window, and replaces the perfect correlation of "
        f"each component with itself by a missing value so it does not distort the "
        f"aggregate statistic. The maximum pairwise correlation is then extracted "
        f"across all component pairs, and the final weight is one minus that maximum. "
        f"This construction actively penalizes redundant components that duplicate "
        f"each other, pushing the combined self-correlation of the SuperAlpha below "
        f"the submission threshold. The resulting single daily signal is the weighted "
        f"combination that maximizes diversity while preserving the alpha content of "
        f"the selected components. It is evaluated in the same simulation settings as "
        f"the selection stage, including decay, neutralization and truncation, so the "
        f"combined behavior remains consistent with the component pool."
    )


async def cmd_select(a):
    from brain_api import BrainApiClient, SimulationData, SimulationSettings  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    settings = SimulationSettings(
        instrumentType="EQUITY", region=a.region, universe=a.universe,
        delay=a.delay, decay=a.decay, neutralization=a.neutralization,
        truncation=a.truncation, testPeriod="P0Y0M", language="FASTEXPR",
        visualization=False, pasteurization="ON", maxTrade="OFF",
        selectionHandling="POSITIVE", selectionLimit=a.selection_limit,
        componentActivation="IS", unitHandling="VERIFY", nanHandling="ON",
    )
    selection = SELECTION_TEMPLATE.format(self_gate=a.self_gate)
    sim_data = SimulationData(type="SUPER", settings=settings, regular=None,
                              combo=COMBO_TEMPLATE, selection=selection)
    print(f"[select] SUPER {a.region}/{a.universe}/d{a.delay}/decay{a.decay}/"
          f"{a.neutralization} selectionLimit={a.selection_limit} self_gate={a.self_gate}")
    result = await brain.create_simulation(sim_data)
    if "error" in result:
        print(f"[error] {result.get('error')} / {result.get('message')}")
        sys.exit(1)
    aid = result.get("id")
    is_ = result.get("is") or {}
    print(f"[result] alpha id = {aid}")
    print(f"  sharpe={is_.get('sharpe')} fitness={is_.get('fitness')} "
          f"turnover={is_.get('turnover')}")
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump(result, open(a.json_out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, default=str)
        print(f"[out] {a.json_out}")
    return 0


async def cmd_status(a):
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    d = await brain.get_alpha_details(a.alpha_id)
    status = d.get("status")
    is_ = d.get("is") or {}
    checks = is_.get("checks") or []
    fails = [c for c in checks if c.get("result") == "FAIL"]
    print(f"=== {a.alpha_id} status={status} ===")
    print(f"  sharpe={is_.get('sharpe')} fitness={is_.get('fitness')} "
          f"turnover={is_.get('turnover')}")
    for c in checks:
        print(f"  [{c.get('name')}] {c.get('result')} value={c.get('value')} limit={c.get('limit')}")
    if status != "ACTIVE" and fails:
        print("NOTE: checks 存在 FAIL，SA 未就绪")
        return 1
    return 0


async def cmd_probe(a):
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    print(f"=== 双闸探针 {a.alpha_id} （零成本）===")
    selfr = await brain.check_self_correlation(a.alpha_id, correlation_type="self")
    print(f"  SELF max={selfr.get('max_correlation')} pass={selfr.get('passes_check')}")
    ok = bool(selfr.get("passes_check"))
    try:
        prodr = await brain.check_correlation(a.alpha_id, correlation_type="production")
        passed = []
        for name, c in (prodr.get("checks") or {}).items():
            print(f"  PROD[{name}] max={c.get('max_correlation')} pass={c.get('passes_check')}")
            if c.get("passes_check") is False:
                ok = False
    except Exception as e:
        print(f"  PROD error: {str(e)[:200]}")
        ok = False
    print(f"\nVERDICT: {'PASS' if ok else 'BLOCKED'}（需双双 < 0.7 才可提交）")
    return 0 if ok else 1


async def cmd_submit(a):
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # 1) 提交层前置判定（零成本 GET，模拟 WARNING 升级 FAIL 的盲区拦截）
    if not a.skip_precheck:
        d = await brain.get_alpha_details(a.alpha_id)
        details_is = d.get("is") or {}
        if any(c.get("result") == "FAIL" for c in (details_is.get("checks") or [])):
            print(f"[precheck] 模拟层 checks 存在 FAIL，拒绝提交（先优化）")
            return 1
        resp = await brain._request("GET", f"{brain.base_url}/alphas/{a.alpha_id}/submit")
        if resp.status_code == 403:
            print(f"[precheck] 提交层 403 BLOCKED：{str(resp.json())[:400]}")
            return 1
        print(f"[precheck] 提交层 OK（HTTP {resp.status_code}）")

    # 2) 设置属性：name + 两个 ≥100 英文 description
    sel_desc = build_selection_description(a.region, a.selection_limit or 10, a.self_gate or 0.55)
    combo_desc = build_combo_description(a.region)
    await brain.set_alpha_properties(a.alpha_id, name=a.name,
                                     selection_description=sel_desc,
                                     combo_description=combo_desc)
    print(f"[props] name={a.name} 描述已设置（selection {len(sel_desc.split())} 词 / "
          f"combo {len(combo_desc.split())} 词）")

    # 3) 两次 submit 判定（skill 实测：第一次 201 异步，第二次回带 PROD/SELF verdict）
    for i in (1, 2):
        print(f"\n[submit] 第 {i} 次 POST /alphas/{a.alpha_id}/submit ...")
        v = await brain.submit_alpha(a.alpha_id)
        print(f"  HTTP {v.get('status_code')} success={v.get('success')} reason={v.get('reason')}")
        for c in v.get("checks") or []:
            print(f"  [{c.get('name')}] {c.get('result')} value={c.get('value')} limit={c.get('limit')}")
        if v.get("success"):
            print("\nVERDICT: 提交已受理，等多线程 2-3 分钟翻转为 ACTIVE（用 status 子命令确认）")
            return 0
        if i == 1 and v.get("status_code") in (201, 202):
            # 异步受理但未出 verdict：等平台计算后再试一次
            print("  (异步受理，等 30s 后重试取 verdict)")
            await asyncio.sleep(30)
            continue
        break
    print("\nVERDICT: BLOCKED（见上检查列表，用 probe 子命令看 PROD/SELF 具体值）")
    return 1


def main():
    ap = argparse.ArgumentParser(description="SuperAlpha 组套流水线")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("select", help="创建 SUPER simulation")
    p.add_argument("--region", required=True)
    p.add_argument("--universe", default="TOP400")
    p.add_argument("--delay", type=int, default=1)
    p.add_argument("--decay", type=int, default=5)
    p.add_argument("--neutralization", default="SUBINDUSTRY", help="关键杠杆，勿改 MARKET")
    p.add_argument("--truncation", type=float, default=0.08)
    p.add_argument("--selection-limit", type=int, default=10)
    p.add_argument("--self-gate", type=float, default=0.55)
    p.add_argument("--json", dest="json_out", help="原始结果落盘")
    p.set_defaults(fn=cmd_select)

    p = sub.add_parser("status", help="查 SUPER 模拟状态与指标")
    p.add_argument("--alpha-id", required=True)
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("probe", help="零成本双闸探针（SELF+PROD）")
    p.add_argument("--alpha-id", required=True)
    p.set_defaults(fn=cmd_probe)

    p = sub.add_parser("submit", help="设置属性 + 两次 submit 判定")
    p.add_argument("--alpha-id", required=True)
    p.add_argument("--name", required=True, help="命名约定：PROD 最大值，如 0.6944")
    p.add_argument("--region", default="USA", help="用于生成描述模板的英文市场名")
    p.add_argument("--selection-limit", type=int, default=10)
    p.add_argument("--self-gate", type=float, default=0.55)
    p.add_argument("--skip-precheck", action="store_true", help="跳过提交层前置判定")
    p.set_defaults(fn=cmd_submit)

    a = ap.parse_args()
    return asyncio.run(a.fn(a))


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))