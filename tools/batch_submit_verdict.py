# -*- coding: utf-8 -*-
"""batch_submit_verdict.py - 对 submit_ready 表中 IS_ONLY 的候选批量跑提交层相关性校验。

复用 tools/submit_verdict.py 的单条判定逻辑（模拟层 checks + GET /alphas/{id}/submit
零成本双视图），但：
  1) 单进程单次认证（避免 65 次子进程重复认证）；
  2) 带 checkpoint 断点续跑（results/batch_submit_verdict_checkpoint.json）；
  3) 429 用 Retry-After 退避（transport 的 _request 本身不重试 429）；
  4) 出 SUBMITTABLE 时调用 mark_verified 升级为 SUBMIT_LAYER_VERIFIED；
  5) 产出结果 CSV 与汇总。

判定逻辑与 submit_verdict.py 完全一致：
  - 模拟层无 FAIL 且无提交层硬闸 WARNING（LOW_FITNESS/LOW_SHARPE/LOW_2Y_SHARPE）
  - 且提交层 GET /submit == 200（可提交）或 == 404 且 status==UNSUBMITTED（处女提交，UNVERIFIABLE）
  -> SUBMITTABLE / UNVERIFIABLE / BLOCKED

用法:
  # 跑全部 IS_ONLY（默认）
  python tools/batch_submit_verdict.py
  # 限区域 / 限量
  python tools/batch_submit_verdict.py --region IND --limit 10
  # 忽略 checkpoint 全新跑
  python tools/batch_submit_verdict.py --fresh
  # 只对上一轮 UNVERIFIABLE（处女提交）补跑 prod/self 终验（check_correlation 平台异步队列，重）
  python tools/batch_submit_verdict.py --phase2-prod

运行环境: MCP venv（world-quant-brain-mcp/.venv），依赖 brain_api + requests。
"""
import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCP_DIR = ROOT / "world-quant-brain-mcp"
RESULTS = ROOT / "results"
CKPT = RESULTS / "batch_submit_verdict_checkpoint.json"
REPORT = RESULTS / "batch_submit_verdict_report.json"

# 提交层硬闸项：模拟层 WARNING 但提交层 FAIL 的检查名（与 submit_verdict.py 一致）
_SUBMIT_HARD_GATE_WARNINGS = {"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE"}


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, str(MCP_DIR / ".venv" / "Scripts" / "python.exe")]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _bootstrap_path():
    sys.path.insert(0, str(MCP_DIR))
    sys.path.insert(0, str(ROOT / "src"))


def _render_checks(checks):
    if not checks:
        return ""
    return "; ".join(
        f"[{c.get('name')}]{c.get('result')}(v={c.get('value')},lim={c.get('limit')})"
        for c in checks)


def _load_ckpt():
    if CKPT.exists():
        try:
            return json.loads(CKPT.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_ckpt(ckpt):
    RESULTS.mkdir(exist_ok=True)
    tmp = CKPT.with_suffix(".tmp")
    tmp.write_text(json.dumps(ckpt, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, CKPT)


async def _get_submit_view(brain, alpha_id, max_tries=8):
    """GET /alphas/{id}/submit，带 429/Retry-After 退避。返回 (status_code, body)。"""
    url = f"{brain.base_url}/alphas/{alpha_id}/submit"
    last_exc = None
    for attempt in range(max_tries):
        try:
            resp = await brain._request("GET", url)
        except Exception as e:  # noqa: BLE001
            last_exc = e
            await asyncio.sleep(2.0 + attempt)
            continue
        if resp.status_code == 429:
            ra = resp.headers.get("Retry-After")
            wait = 5.0
            if ra:
                try:
                    wait = min(max(float(ra), 1.0), 120.0)
                except (TypeError, ValueError):
                    pass
            print(f"    [429] {alpha_id} 退避 {wait:.0f}s (attempt {attempt+1}/{max_tries})")
            await asyncio.sleep(wait)
            continue
        try:
            body = resp.json() if resp.text else {}
        except Exception:
            body = {}
        return resp.status_code, body
    return None, {"error": f"request failed after {max_tries} tries: {last_exc}"}


def _verdict(status, sim_checks, submit_status, layer_checks):
    fails = [c for c in sim_checks if c.get("result") == "FAIL"]
    warns = [c for c in sim_checks if c.get("result") == "WARNING"]
    hard = [c for c in warns if c.get("name") in _SUBMIT_HARD_GATE_WARNINGS]
    # 已上线（ACTIVE/SUBMITTED/PENDING 等）：本地队列行是过时副本，不可再提交
    if submit_status == 404 and status != "UNSUBMITTED":
        return "ALREADY_LIVE", f"platform_status={status}"
    prepost = submit_status == 404 and status == "UNSUBMITTED"
    ok = (not fails) and (not hard) and (submit_status == 200 or prepost)
    if ok and prepost:
        return "UNVERIFIABLE", ""
    if ok:
        return "SUBMITTABLE", ""
    # BLOCKED —— 失败原因
    if fails:
        return "BLOCKED", "SIM_FAIL:" + ",".join(c.get("name") for c in fails)
    if hard:
        return "BLOCKED", "SUBMIT_HARD_WARN:" + ",".join(c.get("name") for c in hard)
    if submit_status == 403:
        lc = layer_checks if isinstance(layer_checks, list) else []
        names = [(c.get("name") if isinstance(c, dict) else str(c)) for c in lc]
        return "BLOCKED", "SUBMIT_403:" + ",".join(names)
    return "BLOCKED", f"UNKNOWN(http={submit_status})"


async def run_phase1(brain, rows, ckpt, throttle=1.5, align_live=False):
    from wqb.store.submit_queue import mark_verified
    summary = {"SUBMITTABLE": 0, "BLOCKED": 0, "UNVERIFIABLE": 0, "ERROR": 0}
    print(f"=== Phase1: GET /submit 双视图判定，共 {len(rows)} 颗 ===")
    for i, row in enumerate(rows, 1):
        aid = row["alpha_id"]
        region = row["region"]
        if aid in ckpt and ckpt[aid].get("phase1_done"):
            v = ckpt[aid].get("verdict")
            summary[v] = summary.get(v, 0) + 1
            print(f"  [{i}/{len(rows)}] {region}/{aid} 跳过(ckpt={v})")
            continue
        print(f"  [{i}/{len(rows)}] {region}/{aid} ...", end="", flush=True)
        try:
            detail = await brain.get_alpha_details(aid)
        except Exception as e:  # noqa: BLE001
            print(f" get_details ERR: {e}")
            ckpt[aid] = {"phase1_done": True, "verdict": "ERROR", "error": str(e),
                         "region": region, "ts": _now()}
            summary["ERROR"] += 1
            _save_ckpt(ckpt)
            await asyncio.sleep(throttle)
            continue
        status = detail.get("status")
        is_ = detail.get("is") or {}
        # P8（2026-09-25）：塔位经济——pyramids.effective = 本提交能新点亮的塔数；
        # effective=0（塔已点亮）的候选提交边际价值低，需评估是否放弃（用户 2026-09-25 令）。
        tower_eff = (detail.get("pyramids") or {}).get("effective")
        sim_checks = is_.get("checks") or []
        submit_status, body = await _get_submit_view(brain, aid)
        if submit_status is None:
            print(f" submit_view ERR")
            ckpt[aid] = {"phase1_done": True, "verdict": "ERROR",
                         "error": str(body.get("error", "noop")), "region": region,
                         "ts": _now()}
            summary["ERROR"] += 1
            _save_ckpt(ckpt)
            await asyncio.sleep(throttle)
            continue
        if submit_status == 200:
            layer_checks = (body.get("is") or {}).get("checks") or []
        elif submit_status == 403:
            layer_checks = body.get("checks") or body.get("detail") or []
            if isinstance(layer_checks, list) and layer_checks and isinstance(layer_checks[0], str):
                layer_checks = [{"name": c, "result": "FAIL"} for c in layer_checks]
        else:
            layer_checks = []
        verdict, reason = _verdict(status, sim_checks, submit_status, layer_checks)
        rec = {
            "sharpe": is_.get("sharpe"), "fitness": is_.get("fitness"),
            "turnover": is_.get("turnover"), "region": region,
            "platform_status": status, "submit_http": submit_status,
            "tower_eff": tower_eff,
            "reason": reason, "ts": _now(),
        }
        if verdict == "SUBMITTABLE":
            try:
                n = mark_verified(aid, region=region, rec={
                    "sharpe": is_.get("sharpe"), "fitness": is_.get("fitness"),
                    "turnover": is_.get("turnover")})
                rec["mark_verified_n"] = n
            except Exception as e:  # noqa: BLE001
                rec["mark_err"] = str(e)
        elif verdict == "ALREADY_LIVE":
            # 本地队列行是过时副本：平台已上线。--align-live 时把本地状态对齐为 SUBMITTED
            if align_live:
                try:
                    from wqb.store.submit_queue import retire, STATUS_SUBMITTED
                    n = retire(aid, status=STATUS_SUBMITTED, region=region)
                    rec["aligned_n"] = n
                except Exception as e:  # noqa: BLE001
                    rec["align_err"] = str(e)
        rec["phase1_done"] = True
        rec["verdict"] = verdict
        ckpt[aid] = rec
        summary[verdict] = summary.get(verdict, 0) + 1
        print(f" {verdict} (http={submit_status}, status={status}, tower_eff={tower_eff}) {reason}")
        _save_ckpt(ckpt)
        await asyncio.sleep(throttle)
    # ---- P8：塔位贡献排序（提交优先级：effective>0 优先；=0 评估放弃）----
    ranked = sorted(
        ((a, r) for a, r in ckpt.items() if r.get("phase1_done")),
        key=lambda kv: (-(kv[1].get("tower_eff") or 0), kv[1].get("verdict") != "SUBMITTABLE"))
    print("--- 提交优先级（塔位贡献排序，P8）---")
    for a, r in ranked:
        eff = r.get("tower_eff")
        note = "可点亮" if (eff or 0) > 0 else "塔已点亮→评估是否放弃"
        print(f"  {r.get('region')}/{a} tower_eff={eff} {r.get('verdict')} [{note}]")
    # ---- P2：验证-提交同日闭环 ----
    print("[P2] 同日闭环纪律：上表为当日验证结果——终验通过的候选必须当日走用户确认并提交；"
          "拖延过夜即漂移（实证 A1Nn2vPQ 0.606→0.7079 / 0mXA6jYG 0.672→0.8168，4 天越线报废）。")
    return summary


def _now():
    from datetime import datetime
    return datetime.now().isoformat(timespec="seconds")


def _load_rows(region=None, limit=None, gate="IS_ONLY", status="READY"):
    import sqlite3
    from wqb.store.submit_queue import default_db_path, connect, ensure_table
    con = connect()
    ensure_table(con)
    q = "SELECT region, alpha_id FROM submit_ready WHERE status=? AND gate=?"
    ps = [status, gate]
    if region:
        q += " AND region=?"
        ps.append(region)
    q += " ORDER BY region, alpha_id"
    cur = con.execute(q, ps)
    rows = [{"region": r[0], "alpha_id": r[1]} for r in cur.fetchall()]
    con.close()
    if limit:
        rows = rows[:limit]
    return rows


async def main():
    ap = argparse.ArgumentParser(description="批量提交层相关性校验（IS_ONLY）")
    ap.add_argument("--region")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--fresh", action="store_true", help="忽略 checkpoint 全新跑")
    ap.add_argument("--throttle", type=float, default=1.5)
    ap.add_argument("--align-live", action="store_true",
                    help="对平台上已上线（ALREADY_LIVE）的本地过时行，对齐状态为 SUBMITTED")
    ap.add_argument("--phase2-prod", action="store_true",
                    help="只对上一轮 UNVERIFIABLE（处女提交）补跑 check_correlation 平台终验（重）")
    a = ap.parse_args()

    _bootstrap_path()
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    ckpt = {} if a.fresh else _load_ckpt()

    if a.phase2_prod:
        # Phase2：对 UNVERIFIABLE（处女提交）子集补跑相关性终验。
        #   prod: check_correlation(platform, 异步队列, 重) —— 提交层 PROD_CORRELATION 真值
        #   self: check_self_correlation(本地, 免费) —— 提交层 SELF_CORRELATION
        # 两者均 <0.7 才 mark_verified 升级为 SUBMIT_LAYER_VERIFIED。
        targets = [k for k, v in ckpt.items()
                   if v.get("verdict") == "UNVERIFIABLE" and not v.get("phase2_done")]
        print(f"=== Phase2: prod+self 相关性终验，对 {len(targets)} 颗 UNVERIFIABLE ===")
        from wqb.store.submit_queue import mark_verified
        promoted = 0
        for i, aid in enumerate(targets, 1):
            region = ckpt[aid].get("region")
            print(f"  [{i}/{len(targets)}] {region}/{aid} ...", end="", flush=True)
            try:
                res_prod = await brain.check_correlation(aid, "production", 0.7, refresh=False)
                res_self = await brain.check_self_correlation(
                    aid, threshold=0.7, correlation_type="self")
                # 2026-09-24 修复：字段语义见 _phase2_outcome docstring（三处假阴性）
                oc = _phase2_outcome(res_prod, res_self, threshold=0.7)
                prod_max, prod_pass = oc["prod_max"], oc["prod_pass"]
                self_max, self_pass = oc["self_max"], oc["self_pass"]
                ckpt[aid]["phase2_done"] = True
                ckpt[aid]["phase2"] = {
                    "prod_max": prod_max, "self_max": self_max,
                    "prod_pass": prod_pass, "self_pass": self_pass,
                }
                if oc["verdict"] == "PROMOTE":
                    n = mark_verified(aid, region=region, rec={
                        "prod": prod_max, "self": self_max})
                    ckpt[aid]["verdict"] = "SUBMIT_LAYER_VERIFIED"
                    ckpt[aid]["phase2_promoted"] = n
                    promoted += 1
                    print(f" PASS prod={prod_max} self={self_max} -> VERIFIED n={n}")
                elif oc["verdict"] == "PENDING":
                    # prod 未决（pending/busy/unavailable）：不判死也不放行，留待下轮重验
                    ckpt[aid]["verdict"] = "UNVERIFIABLE"
                    ckpt[aid]["phase2_pending"] = True
                    print(f" PENDING prod={prod_max}(pass={prod_pass}) "
                          f"self={self_max}(pass={self_pass}) -> 留待下轮")
                else:
                    ckpt[aid]["verdict"] = "BLOCKED_CORR"
                    print(f" FAIL {oc['verdict']} prod={prod_max}(pass={prod_pass}) "
                          f"self={self_max}(pass={self_pass})")
            except Exception as e:  # noqa: BLE001
                ckpt[aid]["phase2_err"] = str(e)
                print(f" ERR {e}")
            _save_ckpt(ckpt)
            await asyncio.sleep(2.0)
        _save_ckpt(ckpt)
        print(f"\n=== Phase2 汇总: 升级 VERIFIED={promoted} / 共 {len(targets)} ===")
        return

    rows = _load_rows(region=a.region, limit=a.limit)
    summary = await run_phase1(brain, rows, ckpt, throttle=a.throttle,
                               align_live=a.align_live)

    # 报告
    RESULTS.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(ckpt, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n=== 汇总 ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print(f"  checkpoint: {CKPT}")
    print(f"  report: {REPORT}")


def _phase2_outcome(res_prod, res_self, threshold=0.7):
    """Phase2 prod+self 终验的字段语义判定（2026-09-24 修复三处假阴性）。

    实证 bug（2026-09-23 P0-1 GLB/ASI 收割，19/19 全部假阴性）：
      1. check_self_correlation 顶层返回 passes_check（没有 all_passed）——旧代码读
         all_passed 使 self 恒为 FAIL；
      2. check_correlation(correlation_type="production") 的 max/passes 在
         checks["production"] 里，顶层 max_correlation 不存在——旧代码 prod_max 恒 None；
      3. prod 未决（pending / correlation_busy / data_unavailable）时 all_passed=None，
         bool(None)=False 被误判 FAIL——未决≠撞墙，必须等平台队列出真值再判。

    Returns: dict(prod_max, prod_pass, self_max, self_pass, verdict)
      verdict: PROMOTE（双过）/ BLOCKED_SELF / BLOCKED_PROD / PENDING（未决）
    """
    # --- self：本地计算，顶层 max_correlation + passes_check ---
    if isinstance(res_self, dict):
        self_max = res_self.get("max_correlation")
        self_pass = res_self.get("passes_check")
    else:
        self_max, self_pass = None, None

    # --- prod：真值在 checks["production"]；顶层只有 all_passed（None=未决）---
    prod_max = None
    prod_pass = None
    if isinstance(res_prod, dict):
        p = (res_prod.get("checks") or {}).get("production") or {}
        prod_max = p.get("max_correlation")
        prod_pass = p.get("passes_check")
        if prod_pass is None and prod_max is None:
            # 缓存命中/旧结构兜底：顶层 max_correlation
            prod_max = res_prod.get("max_correlation")
        if prod_pass is None:
            ap = res_prod.get("all_passed")
            # all_passed=None 是未决信号，不能 bool() 成 FAIL
            if ap is True and prod_max is not None:
                prod_pass = prod_max < threshold
            elif ap is False:
                prod_pass = False
    if prod_pass is None and prod_max is not None:
        prod_pass = prod_max < threshold
    if self_pass is None and self_max is not None:
        self_pass = self_max < threshold

    if self_pass is False:
        verdict = "BLOCKED_SELF"
    elif prod_pass is False:
        verdict = "BLOCKED_PROD"
    elif self_pass is True and prod_pass is True:
        verdict = "PROMOTE"
    else:
        verdict = "PENDING"
    return {
        "prod_max": prod_max, "prod_pass": prod_pass,
        "self_max": self_max, "self_pass": self_pass,
        "verdict": verdict,
    }


def _slim(res):
    if not isinstance(res, dict):
        return res
    return {
        "all_passed": res.get("all_passed"),
        "max_correlation": res.get("max_correlation"),
        "correlation_count": res.get("correlation_count"),
        "error": res.get("error"),
    }


if __name__ == "__main__":
    asyncio.run(main())
