# -*- coding: utf-8 -*-
"""submit_verdict.py - 提交层判定（替代手动 GET/POST /alphas/{id}/submit 探针）。

头部教训（KOR PPA 2026-08-22 实锤）：模拟详情里 LOW_FITNESS/LOW_2Y_SHARPE 显示
WARNING（不挡模拟、不进 fail 列表），但 POST submit 时平台重新评估为 FAIL——只看
get_alpha_details 的 checks.fail=[] 会误判"可提交"。判定必须走提交层：
GET /alphas/{id}/submit 的 403 检查列表（零成本，不消耗提交配额）。

2026-09-03 修正：处女提交（404）时提交层视图不可用，判定完全依赖模拟层。
模拟层 WARNING 中的 LOW_FITNESS/LOW_SHARPE/LOW_2Y_SHARPE 在提交层是硬闸 FAIL，
必须本地拦截，不再放行。

本工具输出双视图（2026-09-28 R8 修正）：
  1) 模拟层：get_alpha_details 的 checks fail/warning + WebDataScope Failed RA/PPA 计数
  2) 提交层：GET /alphas/{id}/submit —— **平台恒返 404**（2026-09-26 实测，ACTIVE 者也 404），
     该视图已定性为死端点，403 分支是历史遗留；**真闸只有用户确认后的 POST submit**
     （三态响应 + 异步补发，见 worldquant-submit-alpha）。

判定口径：**本工具是否决权威**（BLOCKED 即不提交）；报可放行时仍需
「平台 prod<0.7（另跑 check_correlation(refresh=True)）+ 用户确认」。
已提交/ACTIVE 的 alpha 报 ALREADY_SUBMITTED，不做可提交判定。

用法:
  python tools/submit_verdict.py --alpha-id 2rlRAZaZ

退出码: 0=可放行（SUBMITTABLE / UNVERIFIABLE / ALREADY_SUBMITTED）, 1=BLOCKED
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


# 提交层硬闸项：模拟层 WARNING 但提交层 FAIL 的检查名
_SUBMIT_HARD_GATE_WARNINGS = {"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE"}


def _count_failed(checks, kind):
    """WebDataScope Failed RA/PPA 计数（唯一口径源 = src/wqb.config）；返回 (count, items)。"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
        from wqb.config import (RA_CHECK_NAMES as _RA_NAMES, PPA_CHECK_NAMES as _PPA_NAMES,
                                check_counts_as_failed as _counts_bad)
    except Exception:
        return 0, []          # 拿不到口径时不误报：计数置 0 并在报告里注明
    names = _RA_NAMES if kind == "RA" else _PPA_NAMES
    items = []
    for c in checks or []:
        nm = str(c.get("name") or "")
        res = str(c.get("result") or "")
        hit = nm in names and _counts_bad(res)
        if kind == "PPA" and nm == "LOW_SHARPE":
            try:
                hit = hit or float(c.get("value") or 0) < 1
            except (TypeError, ValueError):
                pass
        if hit:
            items.append({"name": nm, "result": res, "value": c.get("value"),
                          "limit": c.get("limit")})
    return len(items), items


def _render_checks(checks):
    if not checks:
        return "  (无检查项)"
    return "\n".join(
        f"  [{c.get('name')}] {c.get('result')} value={c.get('value')} limit={c.get('limit')}"
        for c in checks)


async def _get_alpha_detail_resilient(brain, alpha_id, pages=60):
    """取 alpha 详情。优先 /alphas/{id}；429 时回退 /users/self/alphas 列表端点。

    背景（2026-09-29 实测）：探针波后 `/alphas/{id}` 单条端点被平台限流
    （"API rate limit exceeded"，全局限流，非本地并发），但
    `/users/self/alphas` 列表端点 200 且返回同结构的 is/settings/status 字段。
    列表端点不返回 `checks` 之外的部分字段，但对提交判定所需字段足够。
    在返回体里注入 `_source` 供打印溯源。
    """
    try:
        d = await brain.get_alpha_details(alpha_id)
        d["_source"] = "detail"
        return d
    except Exception as e:  # noqa: BLE001
        msg = str(e)[:120]
        print(f"[warn] /alphas/{alpha_id} 不可用（{msg}）→ 回退列表端点", file=sys.stderr)

    url = f"{brain.base_url}/users/self/alphas?limit=100&order=-dateCreated"
    for _ in range(pages):
        r = await brain._request("GET", url)
        if r.status_code != 200:
            raise RuntimeError(f"list endpoint {r.status_code}: {str(r.text)[:200]}")
        body = r.json()
        for a in body.get("results", []):
            if a.get("id") == alpha_id:
                a["_source"] = "list"
                return a
        nxt = body.get("next")
        if not nxt:
            break
        url = nxt
        await asyncio.sleep(0.5)
    raise RuntimeError(f"alpha {alpha_id} not found via list endpoint")


async def main():
    ap = argparse.ArgumentParser(description="提交层判定：模拟层 + GET /alphas/{id}/submit 双视图")
    ap.add_argument("--alpha-id", required=True)
    ap.add_argument("--with-quota", action="store_true", help="（已废弃：配额检查已于 2026-08-25 移除，此参数无效果）")
    a = ap.parse_args()

    _bootstrap()
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    detail = await _get_alpha_detail_resilient(brain, a.alpha_id)
    status = detail.get("status")
    is_ = detail.get("is") or {}
    sim_checks = is_.get("checks") or []
    fails = [c for c in sim_checks if c.get("result") == "FAIL"]
    warns = [c for c in sim_checks if c.get("result") == "WARNING"]
    print(f"=== alpha {a.alpha_id} status={status} "
          f"(detail source={detail.get('_source', '?')}) ===")
    if detail.get("_source") == "list":
        print("  [注意] 详情来自列表端点：其 `is.checks` 仅为平台摘要，"
              "**不等于模拟层全量 checks**。")
        print("         全量 checks（含 LOW_SHARPE/LOW_FITNESS/LOW_2Y_SHARPE/"
              "LOW_SUB_UNIVERSE_SHARPE/LOW_ROBUST_UNIVERSE_*）"
              "需 /alphas/{id}，该端点正被限流。")
        print("         下方 FAIL 抑制判定/Failed-count 门在 list 源下**不可信**，"
              "以硬指标(F/T/S/2Y)为准。")
    print(f"--- 模拟层 checks: {len(sim_checks)} 条 "
          f"(FAIL {len(fails)} / WARNING {len(warns)}) ---")
    if fails:
        print(_render_checks(fails))
    if warns:
        print("  [warning 条目不挡模拟，但提交层可能升级为 FAIL，见下]")
        print(_render_checks(warns))
    if not fails and not warns:
        print("  (无 FAIL/WARNING)")

    # 已提交/已落地：不做可提交判定（此前对 ACTIVE 也判 BLOCKED，假阴性）
    if status in ("ACTIVE", "SUBMITTED") or detail.get("dateSubmitted"):
        print(f"\nVERDICT: ALREADY_SUBMITTED（status={status}）")
        print("  alpha 已提交/已落地，不构成可提交判定对象；请勿重复 POST submit。")
        sys.exit(0)

    failed_ra, failed_ra_items = _count_failed(sim_checks, "RA")
    failed_ppa, failed_ppa_items = _count_failed(sim_checks, "PPA")
    is_ppa = str(detail.get("type") or "").upper() == "PPA"
    print(f"\n--- WebDataScope Failed-count 资格门（REGULAR 看 RA / PPA 看 PPA）---")
    print(f"  Failed RA = {failed_ra}；Failed PPA = {failed_ppa}"
          + ("（本候选按 PPA 判定）" if is_ppa else "（本候选按 REGULAR 判定）"))
    for it in (failed_ppa_items if is_ppa else failed_ra_items):
        print(f"    [{it['name']}] {it['result']} value={it['value']} limit={it['limit']}")

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

    # 判定：模拟层无 FAIL + 无提交层硬闸 WARNING + Failed-count 为零，
    # 且提交层为 200 或处女提交 404
    prepost_unverifiable = submit_status == 404 and status == "UNSUBMITTED"
    hard_gate_warns = [c for c in warns if c.get("name") in _SUBMIT_HARD_GATE_WARNINGS]
    failed_gate_ok = (failed_ppa == 0) if is_ppa else (failed_ra == 0)
    ok = (not fails and not hard_gate_warns and failed_gate_ok
          and (submit_status == 200 or prepost_unverifiable))
    verdict = "UNVERIFIABLE" if (ok and prepost_unverifiable) else ("SUBMITTABLE" if ok else "BLOCKED")
    print(f"\nVERDICT: {verdict}")
    if not failed_gate_ok:
        names = [c["name"] for c in (failed_ppa_items if is_ppa else failed_ra_items)]
        print(f"  原因: Failed-count 资格门非零（{'PPA' if is_ppa else 'RA'}）：{names}")
    elif hard_gate_warns:
        names = [c.get("name") for c in hard_gate_warns]
        print(f"  原因: 模拟层 WARNING 含提交层硬闸项 {names}（提交时平台判 FAIL）")
    elif not fails and prepost_unverifiable:
        print("  判定依据: 模拟层无 FAIL/硬闸 WARNING/Failed-count，但提交层 404"
              "（GET /submit 平台恒 404，死端点）无法验证。")
        print("  放行条件 = 平台 prod<0.7 + 用户确认；提交前必须另跑 "
              "check_correlation(alpha_id, refresh=True) 确认 all_passed。")
    elif fails:
        print("  原因: 模拟层 checks 存在 FAIL，先优化再试")
    elif submit_status == 403:
        print("  原因: 提交层 403，见上检查列表（模拟层 WARNING 已升级）")

    # --- 队列状态升级（2026-09-20）---
    # 本工具是提交判定的唯一权威；出 SUBMITTABLE 时把待提交队列里该条
    # 从 IS_ONLY 升级为 SUBMIT_LAYER_VERIFIED 并刷新 verified_at，
    # 使队列可信度与判定权威一致。容错：绝不影响判定结果与退出码。
    if verdict == "SUBMITTABLE":
        try:
            sys.path.insert(0, os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
            from wqb.store.submit_queue import mark_verified
            n = mark_verified(a.alpha_id, rec={
                "sharpe": is_.get("sharpe"), "fitness": is_.get("fitness"),
                "turnover": is_.get("turnover"),
            })
            print(f"  [queue] 已升级 SUBMIT_LAYER_VERIFIED（{n} 条）" if n
                  else "  [queue] 队列中无此条，跳过升级")
        except Exception as e:  # noqa: BLE001
            print(f"  [queue] 升级跳过：{e}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    asyncio.run(main())