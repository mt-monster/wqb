# -*- coding: utf-8 -*-
"""tools_ops — 运维/审计类 MCP 工具（operator_audit/batch_status/submit_verdict/sa_probe/submit_batch）.

将 tools/ 下的 CLI 工具包装为 MCP 工具，消除 PowerShell 手写命令。
"""
import logging
import os
import sys
from typing import Any, Dict, List, Optional

from mcp_core import mcp, brain_client

logger = logging.getLogger("tools_ops")

# ── 路径引导 ──
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
_SRC_PATH = os.path.join(_REPO_ROOT, "src")
if _SRC_PATH not in sys.path:
    sys.path.insert(0, _SRC_PATH)


# ── operator_audit ──

@mcp.tool()
async def operator_audit(
    expressions: Optional[List[str]] = None,
    region: str = "USA",
    delay: int = 1,
    universe: str = "TOP3000",
) -> Dict[str, Any]:
    """审计算子安全性：catalog vs 平台实测算子差异 + 表达式幽灵算子检测.

    两种模式：
    1. 无 expressions：拉取平台实时算子列表，与 catalog 对比（ghost/missing/verified）
    2. 有 expressions：检测表达式中是否使用了幽灵算子（dispatch 前硬闸）

    Args:
        expressions: 待检测的 alpha 表达式列表（可选）
        region: 区域代码
        delay: 延迟
        universe: 宇宙

    Returns:
        模式1: {verified, ghost, missing, summary}
        模式2: {safe: bool, violations: [{expression, ghost_ops}]}
    """
    try:
        from wqb.expression.operator_audit import operator_audit as _audit, get_ghost_operators

        if expressions:
            # 模式 2：表达式幽灵算子检测
            ghosts = get_ghost_operators()
            from wqb.expression.grammar import extract_identifiers
            violations = []
            for expr in expressions:
                used = extract_identifiers(expr)
                bad = sorted(used & ghosts)
                if bad:
                    violations.append({"expression": expr, "ghost_ops": bad})
            return {
                "safe": len(violations) == 0,
                "total_expressions": len(expressions),
                "violations": violations,
                "ghost_operators": sorted(ghosts),
            }
        else:
            # 模式 1：平台算子审计
            await brain_client.ensure_authenticated()
            resp = await brain_client.get_operators()
            live_ops = set()
            if isinstance(resp, list):
                for item in resp:
                    if isinstance(item, dict) and item.get("name"):
                        live_ops.add(item["name"])
                    elif isinstance(item, str):
                        live_ops.add(item)
            elif isinstance(resp, dict):
                for item in resp.get("results", resp.get("operators", [])):
                    if isinstance(item, dict) and item.get("name"):
                        live_ops.add(item["name"])
                    elif isinstance(item, str):
                        live_ops.add(item)

            result = _audit(live_ops)
            result["success"] = True
            return result

    except Exception as e:
        return {"error": f"operator_audit failed: {str(e)}"}


# ── batch_status ──

@mcp.tool()
async def batch_status(
    simulation_ids: List[str],
) -> Dict[str, Any]:
    """查询回测批次/子任务状态（单次查询，非轮询）.

    输入一个或多个 simulation/multisim ID，输出每个批次的子任务状态汇总。
    等价于 tools/batch_status.py 的单次查询模式（无 --watch）。

    Args:
        simulation_ids: simulation 或 multisim ID 列表

    Returns:
        {batches: [{batch_id, kind, child_count, terminal, errors, all_terminal, children}], all_ok: bool}
    """
    try:
        await brain_client.ensure_authenticated()
        # 2026-09-21 根治：子任务成功终态为 COMPLETE（与 toolkit poller 一致）；此前集合漏 COMPLETE，
        # 已完成批永远 terminal=0 / all_ok=False，且 "COMPLETE" 字面量被计成 errors。
        TERMINAL = {"COMPLETE", "DONE", "WARNING", "ERROR", "CANCELLED", "FAILED", "FAIL"}  # WARNING=已完成但带告警（单位不兼容等），亦为终态；FAIL=平台子模拟裸状态字面量（2026-09-21 ASI psd 批实证：父 ERROR、子全 FAIL，旧集合永远 0/8 terminal）
        OK_STATUSES = {"COMPLETE", "DONE"}

        def _shape_url(loc):
            if loc.startswith("http"):
                return loc
            if loc.startswith("/"):
                return f"{brain_client.base_url}{loc}"
            return f"{brain_client.base_url}/simulations/{loc}"

        async def _fetch_one(loc_full):
            resp = await brain_client._request("GET", loc_full)
            if resp.status_code != 200:
                return {"error": f"HTTP {resp.status_code}", "status_code": resp.status_code}
            data = resp.json() if resp.text else {}
            err = brain_client._simulation_error_message(data)
            if not data.get("alpha") and err == "Unknown error":
                err = ""
            if (data.get("status") or "").upper() in OK_STATUSES and (err or "").strip().upper() in OK_STATUSES:
                err = ""
            is_ = data.get("is") or {}
            m = is_.get("metrics") or {}
            return {
                "status": data.get("status"),
                "alpha": data.get("alpha"),
                "error": err,
                "sharpe": is_.get("sharpe") or m.get("sharpe"),
                "fitness": is_.get("fitness") or m.get("fitness"),
                "turnover": is_.get("turnover") or m.get("turnover"),
            }

        async def _fetch_batch(batch_id):
            loc = _shape_url(batch_id)
            resp = await brain_client._request("GET", loc)
            if resp.status_code != 200:
                return {"batch_id": batch_id, "error": f"HTTP {resp.status_code}"}
            data = resp.json() if resp.text else {}
            children = data.get("children") or []
            if not children:
                parent = await _fetch_one(loc)
                st = (parent.get("status") or "").upper()
                done = st in TERMINAL
                return {
                    "batch_id": batch_id,
                    "kind": "multisim",
                    "child_count": 0,
                    "terminal": 0,
                    "errors": 1 if (parent.get("error") or done) else 0,
                    "all_terminal": done,
                    "children": [],
                    "parent_status": parent.get("status"),
                    "error": parent.get("error") or (f"parent {st} but children empty" if done else ""),
                }
            out_children = []
            for c in children:
                cloc = _shape_url(c if isinstance(c, str) else c.get("location", ""))
                child = await _fetch_one(cloc)
                child["location"] = cloc.rsplit("/", 1)[-1]
                out_children.append(child)
            term = [c for c in out_children if (c.get("status") or "").upper() in TERMINAL]
            errs = [c for c in out_children if c.get("error") and c["error"] != "HTTP 404"]
            return {
                "batch_id": batch_id,
                "kind": "multisim",
                "child_count": len(out_children),
                "terminal": len(term),
                "errors": len(errs),
                "all_terminal": len(term) == len(out_children) if out_children else False,
                "children": out_children,
            }

        # 清理 ID（去掉 URL 前缀）
        clean_ids = []
        for sid in simulation_ids:
            clean_ids.append(sid.replace(f"{brain_client.base_url}/simulations/", "").strip("/"))

        batches = []
        for bid in clean_ids:
            batches.append(await _fetch_batch(bid))

        bad = [b for b in batches if b.get("error") or (b.get("kind") == "multisim" and not b.get("all_terminal"))]
        return {"batches": batches, "all_ok": len(bad) == 0, "total": len(batches)}

    except Exception as e:
        return {"error": f"batch_status failed: {str(e)}"}


# ── submit_verdict ──


def _count_failed(checks, kind):
    """WebDataScope Failed RA/PPA 计数（规则唯一权威 = src/wqb/config.py 的 CHECK 名单 +
    wq-brain-ra-pipeline/references/webdatascope-failed-gates.md 的计数伪码）.

    返回 (count, items)；items 逐条 name/result/value/limit（报告要求逐条列名）。
    PPA 附加规则：LOW_SHARPE 的 value<1 无论 result 显示什么都计入。
    """
    from wqb.config import (RA_CHECK_NAMES as _RA_NAMES,  # noqa: WPS433（延迟导入：MCP 包不强依赖 src）
                            PPA_CHECK_NAMES as _PPA_NAMES,
                            check_counts_as_failed as _counts_bad)
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
            items.append({"name": nm, "result": res,
                          "value": c.get("value"), "limit": c.get("limit")})
    return len(items), items

@mcp.tool()
async def submit_verdict(alpha_id: str) -> Dict[str, Any]:
    """提交层判定（否决权威）：模拟层 checks + Failed-count 资格门 + GET /submit 双视图.

    等价于 tools/submit_verdict.py。判定口径（2026-09-28 R8 修正）：
    - **否决权威**：本工具说 BLOCKED 即不提交；说可放行时仍需满足「平台 prod<0.7 + 用户确认」
      —— prod/自相关不在本工具内查，需另跑 check_correlation(refresh=True)。
    - 模拟层：get_alpha_details 的 checks fail/warning + WebDataScope Failed RA/PPA 计数
      （规则见 wq-brain-ra-pipeline/references/webdatascope-failed-gates.md；唯一实现在 wqb.config）。
    - 提交层：GET /alphas/{id}/submit **平台恒返 404**（2026-09-26 实测，ACTIVE 者也 404）
      ——403 分支是死代码，该视图仅供历史兼容；**真闸只有用户确认后的 POST submit**
      （三态响应 + 异步补发，见 worldquant-submit-alpha / submit_alpha 节点）。

    Args:
        alpha_id: Alpha ID

    Returns:
        {verdict: "SUBMITTABLE"|"UNVERIFIABLE"|"BLOCKED"|"ALREADY_SUBMITTED",
         failed_ra, failed_ppa, sim_fails, submit_status, submit_checks, ...}
    """
    try:
        await brain_client.ensure_authenticated()

        # 模拟层
        detail = await brain_client.get_alpha_details(alpha_id)
        status = detail.get("status")
        is_ = detail.get("is") or {}
        sim_checks = is_.get("checks") or []
        fails = [c for c in sim_checks if c.get("result") == "FAIL"]
        warns = [c for c in sim_checks if c.get("result") == "WARNING"]

        # 已提交/已落地：不再做可提交判定（此前对 ACTIVE 也报 BLOCKED，假阴性）
        if status in ("ACTIVE", "SUBMITTED") or detail.get("dateSubmitted"):
            return {
                "verdict": "ALREADY_SUBMITTED",
                "verdict_note": (f"alpha 已提交/已落地（status={status}），不构成可提交判定对象；"
                                 "请勿重复 POST submit（幂等但浪费配额/产生混乱）。"),
                "alpha_id": alpha_id, "alpha_status": status,
                "sim_fails": fails, "sim_warnings": warns,
                "hard_gate_warnings": [], "submit_status": None, "submit_checks": [],
                "prepost_unverifiable": False,
                "failed_ra": 0, "failed_ppa": 0,
                "failed_ra_items": [], "failed_ppa_items": [],
            }

        # WebDataScope Failed-count 资格门（唯一实现 = wqb.config；REGULAR 看 RA、PPA 看 PPA）
        is_ppa = str(detail.get("type") or "").upper() == "PPA" or any(
            "PowerPoolSelected" in str(t) for t in (detail.get("tags") or []))
        failed_ra, failed_ra_items = _count_failed(sim_checks, "RA")
        failed_ppa, failed_ppa_items = _count_failed(sim_checks, "PPA")

        # 提交层
        submit_url = f"{brain_client.base_url}/alphas/{alpha_id}/submit"
        resp = await brain_client._request("GET", submit_url)
        submit_status = resp.status_code
        submit_checks = []
        if resp.status_code == 200:
            body = resp.json() if resp.text else {}
            submit_checks = (body.get("is") or {}).get("checks") or []
        elif resp.status_code == 403:
            body = resp.json() if resp.text else {}
            submit_checks = body.get("checks") or body.get("detail") or []
            if isinstance(submit_checks, list) and submit_checks and isinstance(submit_checks[0], str):
                submit_checks = [{"name": c, "result": "FAIL"} for c in submit_checks]

        # 判定：模拟层无 FAIL + 无提交层硬闸 WARNING + Failed-count 资格门为零，
        # 且提交层为 200 或处女提交 404
        _SUBMIT_HARD_GATE_WARNINGS = {"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE"}
        prepost_unverifiable = submit_status == 404 and status == "UNSUBMITTED"
        hard_gate_warns = [c for c in warns if c.get("name") in _SUBMIT_HARD_GATE_WARNINGS]
        failed_gate_ok = (failed_ppa == 0) if is_ppa else (failed_ra == 0)
        ok = (not fails and not hard_gate_warns and failed_gate_ok
              and (submit_status == 200 or prepost_unverifiable))

        # 2026-09-08：处女提交（404）时提交层没有任何信息，此前一律报 SUBMITTABLE，
        # 造成假阳性（IND qMja95Q2 判 SUBMITTABLE 实测 prod 0.7354；MEA Jj7ee6nO/omqEE1pn 同）。
        # 这种情况只能说明「模拟层无阻塞」，不能说明可提交 —— 单列 UNVERIFIABLE，
        # 迫使调用方另跑 check_correlation(refresh=True) 看 all_passed 才作准。
        if ok and prepost_unverifiable:
            verdict = "UNVERIFIABLE"
        elif ok:
            verdict = "SUBMITTABLE"
        else:
            verdict = "BLOCKED"

        return {
            "verdict": verdict,
            "verdict_note": (
                "提交层返回 404（GET /alphas/{id}/submit 平台恒 404，该视图已定性为死端点），"
                "无法验证。模拟层无 FAIL/硬闸 WARNING/Failed-count，但 PROD_CORRELATION / "
                "SELF_CORRELATION 未经平台确认——放行条件 = 平台 prod<0.7 + 用户确认；"
                "提交前必须另跑 check_correlation(alpha_id, refresh=True) 并确认 all_passed。"
            ) if verdict == "UNVERIFIABLE" else (
                "Failed-count 资格门非零" if not failed_gate_ok else None),
            "alpha_id": alpha_id,
            "alpha_status": status,
            "is_ppa": is_ppa,
            "sim_fails": fails,
            "sim_warnings": warns,
            "hard_gate_warnings": hard_gate_warns,
            "failed_ra": failed_ra, "failed_ppa": failed_ppa,
            "failed_ra_items": failed_ra_items, "failed_ppa_items": failed_ppa_items,
            "submit_status": submit_status,
            "submit_checks": submit_checks,
            "submit_layer_view": "dead_endpoint_404" if submit_status == 404 else "live",
            "prepost_unverifiable": prepost_unverifiable,
        }

    except Exception as e:
        return {"error": f"submit_verdict failed: {str(e)}"}


# ── sa_probe ──

@mcp.tool()
async def sa_probe(
    region: str,
    min_eligible: int = 10,
    limit_hint: int = 950,
) -> Dict[str, Any]:
    """SuperAlpha 组件池探针（≥10 ACTIVE REGULAR 硬前置）.

    等价于 tools/sa_probe.py。拉取指定区域全部 REGULAR alpha，
    统计 ACTIVE 组件数，输出 GO/BLOCKED verdict。

    Args:
        region: 区域代码（如 KOR/USA/MEA）
        min_eligible: GO 阈值（默认 10）
        limit_hint: 单阶段最大翻页量

    Returns:
        {verdict: "GO"|"BLOCKED", eligible: int, total: int, need: int, pool_summary: {...}}
    """
    try:
        await brain_client.ensure_authenticated()

        pool = []
        eligible_count = 0
        # 2026-09-03 根治：提前退出 — 找到足够 ACTIVE alpha 即停，不扫描全量。
        # 原实现串行翻页最多 2*19=38 次 API 调用，导致 MCP 超时。
        early_exit_threshold = min_eligible + 5  # 多找 5 个缓冲
        for stage in ("OS", "IS"):
            off = 0
            while off < limit_hint:
                d = await brain_client.get_user_alphas(
                    stage=stage, limit=50, alpha_type="REGULAR",
                    order="-dateSubmitted", offset=off)
                res = d.get("results") or []
                if not res:
                    break
                for r in res:
                    s = r.get("settings") or {}
                    if (s.get("region") or r.get("region")) != region:
                        continue
                    entry = {
                        "id": r["id"], "stage": stage, "name": r.get("name"),
                        "status": r.get("status"), "type": r.get("type"),
                        "sharpe": (r.get("is") or {}).get("sharpe"),
                        "fitness": (r.get("is") or {}).get("fitness"),
                        "dateSubmitted": r.get("dateSubmitted"),
                    }
                    pool.append(entry)
                    if entry["status"] == "ACTIVE":
                        eligible_count += 1
                if len(res) < 50:
                    break
                off += 50
                # 提前退出：已找到足够 ACTIVE alpha
                if eligible_count >= early_exit_threshold:
                    break
            if eligible_count >= early_exit_threshold:
                break

        # 去重
        seen, dedup = set(), []
        for a in pool:
            if a["id"] not in seen:
                seen.add(a["id"])
                dedup.append(a)

        eligible = [p for p in dedup if p["status"] == "ACTIVE"]
        verdict = "GO" if len(eligible) >= min_eligible else "BLOCKED"

        return {
            "verdict": verdict,
            "region": region,
            "total": len(dedup),
            "eligible": len(eligible),
            "need": max(0, min_eligible - len(eligible)),
            "os_count": sum(1 for p in dedup if p["stage"] == "OS"),
            "is_count": sum(1 for p in dedup if p["stage"] == "IS"),
            "eligible_ids": [p["id"] for p in eligible],
        }

    except Exception as e:
        return {"error": f"sa_probe failed: {str(e)}"}


# ── submit_batch ──

@mcp.tool()
async def submit_batch(
    expressions: List[str],
    region: str = "USA",
    universe: str = "TOP3000",
    delay: int = 1,
    decay: int = 4,
    neutralization: str = "SUBINDUSTRY",
    alpha_type: str = "REGULAR",
    truncation: float = 0.0,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """批量提交 alpha 表达式进行回测（REST 直连）.

    等价于 tools/submit_batch.py。将表达式列表组装为 payload 并 POST /simulations。

    Args:
        expressions: alpha 表达式列表
        region: 区域代码
        universe: 宇宙
        delay: 延迟
        decay: decay 值
        neutralization: 中性化方式
        alpha_type: alpha 类型（REGULAR/SUPER）
        truncation: 截断
        dry_run: 是否干跑（不实际提交）

    Returns:
        {success: bool, submitted: int, locations: [str], errors: [str]}
    """
    try:
        settings = {
            "instrumentType": "EQUITY",
            "region": region,
            "universe": universe,
            "delay": delay,
            "truncation": truncation,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "OFF",
            "maxTrade": "ON",
            "maxPosition": "OFF",
            "language": "FASTEXPR",
            "visualization": False,
            "startDate": "2014-01-01",
            "endDate": "2023-12-31",
            "decay": decay,
            "neutralization": neutralization,
        }

        payload = [{"type": alpha_type, "settings": settings, "regular": e} for e in expressions]

        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "would_submit": len(payload),
                "sample_payload": payload[0] if payload else None,
            }

        await brain_client.ensure_authenticated()
        resp = await brain_client._request(
            "POST", f"{brain_client.base_url}/simulations", json=payload)
        loc = resp.headers.get("Location", "")

        return {
            "success": resp.status_code == 201,
            "submitted": len(payload),
            "status_code": resp.status_code,
            "location": loc,
            "response_preview": resp.text[:500] if resp.status_code != 201 else None,
        }

    except Exception as e:
        return {"error": f"submit_batch failed: {str(e)}"}
