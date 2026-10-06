# -*- coding: utf-8 -*-
"""candidate_health_card.py — 为推荐候选生成「三层体检卡」（闸 / 回报 / 加钱）。

三层口径（映射顾问 base payment 因子树，见 .workbuddy/memory/MEMORY.md §2）：
  ① 闸层  = 能不能提交 : ra 失败检查=0、prod<0.7、self<0.7、turnover<=0.30
  ② 回报层 = 值不值     : judge 六指标 sharpe/fitness/2Y/margin/turnover/returns
                          （+ drawdown 风险、longCount/shortCount 多空均衡）
  ③ 加钱层 = Value Factor 三项 : 单α表现 / 多样性(towers 倍率) / 独特性(prod·self 定族)

★ 为什么需要它（2026-10-06）
  盘点报告里的两张表只有 sharpe/fitness/2Y/turnover/prod/self，**缺两项关键数据**：
    - `margin`（官方「好 alpha」三线之一，>4bps）：`submit_ready` 表**根本没有这一列**；
    - **约束变体** `is.investabilityConstrained.*` / `is.riskNeutralized.*`：约束后表现
      普遍比原始低 31–34%，平台真正扣分扣的是它们（对应闸 LOW_INVESTABILITY_CONSTRAINED_SHARPE
      / LOW_ROBUST_UNIVERSE_SHARPE）。
  本工具一次性把这三层数据取齐并落盘，供报告逐颗解释。

★ 只读纪律
  本地 DB 只读 + 平台 `get_alpha_details` 只读 GET。**不写库、不提交、不占相关性队列**。
  （与 backfill_alpha_metrics_from_platform.py 的区别：那个是"补空写库"，这个是"取数出卡"。）

用法:
  python tools/candidate_health_card.py --status READY            # 默认：全部 READY 行（10 颗）
  python tools/candidate_health_card.py --status READY --region GBR
  python tools/candidate_health_card.py --ids j289xaxO WjegEmQO
  python tools/candidate_health_card.py --status READY --no-resume   # 忽略 checkpoint 重取
退出码: 0=正常  3=DB/平台失败
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_DIR = os.path.join(REPO_ROOT, "world-quant-brain-mcp")
DB = os.path.join(REPO_ROOT, "data", "wqb.db")
RESULTS = os.path.join(REPO_ROOT, "results")
CKPT = os.path.join(RESULTS, "candidate_health_card_ckpt.json")

MARGIN_BP_MIN = 4.0     # 官方「好 alpha」线：margin > 4 bps
TURNOVER_MAX = 0.30     # 官方「好 alpha」线：turnover < 30%
PROD_MAX = 0.7
SELF_MAX = 0.7
SAFE_MARGIN = 0.05      # 闸层安全余量：>=0.05 安全；<0.03 不提

_IS_KEEP = ("sharpe", "fitness", "turnover", "margin", "returns",
            "drawdown", "longCount", "shortCount", "pnl", "bookSize")
_CONS_NAMES = ("investabilityConstrained", "riskNeutralized")


def pick_targets(con: sqlite3.Connection, status: Optional[str], region: Optional[str],
                 ids: Optional[List[str]], limit: Optional[int]) -> List[Dict[str, Any]]:
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if ids:
        q = "SELECT * FROM submit_ready WHERE alpha_id IN (" + ",".join("?" * len(ids)) + ")"
        return [dict(r) for r in cur.execute(q, ids).fetchall()]
    q = "SELECT * FROM submit_ready WHERE 1=1"
    ps: List[Any] = []
    if status:
        q += " AND status=?"
        ps.append(status)
    if region:
        q += " AND region=?"
        ps.append(region)
    q += " ORDER BY sharpe DESC"
    if limit:
        q += f" LIMIT {int(limit)}"
    return [dict(r) for r in cur.execute(q, ps).fetchall()]


async def fetch_platform(alpha_id: str) -> Dict[str, Any]:
    """只读 GET `get_alpha_details`，抽三层所需字段（兼容 result 包装）。"""
    from brain_api import brain_client
    d = await brain_client.get_alpha_details(alpha_id)
    if isinstance(d, dict) and isinstance(d.get("result"), dict):
        d = d["result"]
    d = d or {}
    isd = d.get("is") or {}

    flat = {k: isd.get(k) for k in _IS_KEEP if isd.get(k) is not None}
    cons: Dict[str, Any] = {}
    for name in _CONS_NAMES:
        blk = isd.get(name)
        if isinstance(blk, dict):
            cons[name] = {k: blk.get(k) for k in _IS_KEEP if blk.get(k) is not None}

    checks: List[Dict[str, Any]] = []
    for c in (isd.get("checks") or []):
        if isinstance(c, dict):
            checks.append({k: v for k, v in c.items() if not isinstance(v, (dict, list))})

    return {"is": flat, "constraints": cons, "checks": checks,
            "is_keys": sorted(isd.keys()) if isinstance(isd, dict) else []}


def _verdict_of(c: Dict[str, Any]) -> str:
    for k in ("result", "status", "verdict"):
        v = c.get(k)
        if isinstance(v, str) and v:
            return v.upper()
    return ""


def derive(local: Dict[str, Any], plat: Dict[str, Any]) -> Dict[str, Any]:
    """派生三层判定（供报告直接引用，避免每次手算）。"""
    isd = plat.get("is") or {}
    cons = plat.get("constraints") or {}
    checks = plat.get("checks") or []

    # 实测（2026-10-06）：checps 的 result 只有 PASS / PENDING / WARNING，**从不出现 FAIL**
    #   —— 未 FAIL 即 RA 层通过；PENDING = 提交时才测（SELF/PROD 相关、DATA_DIVERSITY、
    #   REGULAR_SUBMISSION、POWER_POOL）；WARNING = 非致命提示（CLUSTER_TEST 偏低、
    #   MATCHES_COMPETITION / MATCHES_THEMES 未命中）。
    hard_fail = [c.get("name") for c in checks if _verdict_of(c) in ("FAIL", "FAILED", "FALSE")]
    warn = [c.get("name") for c in checks if _verdict_of(c) == "WARNING"]
    pending = [c.get("name") for c in checks if _verdict_of(c) == "PENDING"]

    def _find(name: str) -> Dict[str, Any]:
        for c in checks:
            if c.get("name") == name:
                return c
        return {}

    cluster = _find("CLUSTER_TEST")
    pyramid = _find("MATCHES_PYRAMID")
    themes = [c for c in checks if c.get("name") == "MATCHES_THEMES"]

    to = isd.get("turnover")
    if to is None:
        to = local.get("turnover")
    margin = isd.get("margin")
    margin_bp = round(margin * 1e4, 3) if isinstance(margin, (int, float)) else None

    prod = local.get("prod")
    self_ = local.get("self")
    rem = None
    if isinstance(prod, (int, float)) and isinstance(self_, (int, float)):
        rem = round(min(PROD_MAX - prod, SELF_MAX - self_), 4)

    base_s = isd.get("sharpe")
    cons_view: Dict[str, Any] = {}
    for name, blk in cons.items():
        s = blk.get("sharpe")
        cons_view[name] = {
            "sharpe": s,
            "delta_pct": round((s - base_s) / base_s * 100.0, 1) if (s is not None and base_s) else None,
        }

    return {
        "gate_layer": {
            "ra_hard_fail": hard_fail,
            "ra_warnings": warn,
            "ra_pending": pending,
            "prod": prod, "self": self_, "margin_remaining": rem,
            "turnover": to, "turnover_ok": (to is not None and to <= TURNOVER_MAX),
            "margin_bp": margin_bp, "margin_ok": (margin_bp is not None and margin_bp >= MARGIN_BP_MIN),
            "prod_ok": (prod is not None and prod < PROD_MAX),
            "self_ok": (self_ is not None and self_ < SELF_MAX),
            "safety": ("SAFE" if (rem is not None and rem >= SAFE_MARGIN) else
                       ("THIN" if (rem is not None and rem < 0.03) else "EDGE")),
            "all_pass": (not hard_fail
                         and (prod is not None and prod < PROD_MAX)
                         and (self_ is not None and self_ < SELF_MAX)),
        },
        "return_layer": {
            "sharpe": isd.get("sharpe", local.get("sharpe")),
            "fitness": isd.get("fitness", local.get("fitness")),
            "two_year": local.get("two_year"),
            "sub_universe": local.get("sub_universe"),
            "margin_bp": margin_bp,
            "turnover": to,
            "returns": isd.get("returns"),
            "drawdown": isd.get("drawdown"),
            "long_count": isd.get("longCount"),
            "short_count": isd.get("shortCount"),
        },
        "vf_layer": {
            "towers": local.get("towers"),
            "prod": prod, "self": self_,
            "constraint_sharpe": cons_view,
            "base_sharpe": base_s,
            "cluster_test": {"value": cluster.get("value"), "result": cluster.get("result")},
            "pyramid": {"result": pyramid.get("result"), "multiplier": pyramid.get("multiplier")},
            "themes": [c.get("result") for c in themes],
        },
    }


def load_ckpt() -> Dict[str, Any]:
    if os.path.exists(CKPT):
        try:
            return json.load(open(CKPT, encoding="utf-8"))
        except Exception:
            pass
    return {"done": {}}


def save_ckpt(ck: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CKPT), exist_ok=True)
    tmp = CKPT + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, CKPT)


def main() -> int:
    ap = argparse.ArgumentParser(description="候选三层体检卡（只读：本地 DB + 平台 GET）")
    ap.add_argument("--status", default="READY", help="submit_ready.status 过滤（默认 READY；传 '' 表示不限）")
    ap.add_argument("--region", default=None, help="限区（如 GBR）")
    ap.add_argument("--ids", nargs="*", default=None, help="指定 alpha_id 列表")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None, help="输出 JSON 路径")
    ap.add_argument("--no-resume", action="store_true", help="忽略 checkpoint 重新取数")
    a = ap.parse_args()

    try:
        # 走规范工厂（WAL + busy_timeout），勿用裸 sqlite3.connect —— 守住
        # tests/unit/01_store_db/test_db_write_guards.py::TestNoNakedSqliteConnect。
        from wqb.db_conn import connect as _db_connect
        con = _db_connect(DB)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] DB 打开失败: {e}", file=sys.stderr)
        return 3

    targets = pick_targets(con, a.status or None, a.region, a.ids, a.limit)
    con.close()
    print(f"[targets] {len(targets)} 颗（status={a.status or '*'} region={a.region or '*'}）")
    if not targets:
        return 0

    ck = {"done": {}} if a.no_resume else load_ckpt()
    done = ck.get("done", {})

    cards: List[Dict[str, Any]] = []
    for i, r in enumerate(targets, 1):
        aid = r["alpha_id"]
        cached = done.get(aid)
        if cached and not a.no_resume:
            plat = cached
            print(f"  [{i}/{len(targets)}] {aid} (cache)")
        else:
            try:
                plat = asyncio.run(fetch_platform(aid))
                done[aid] = plat
                save_ckpt({"done": done})
                nchk = len(plat.get("checks") or [])
                print(f"  [{i}/{len(targets)}] {aid} ok (checks={nchk}, cons={list((plat.get('constraints') or {}).keys())})")
            except Exception as e:  # noqa: BLE001
                plat = {"error": str(e)[:200], "is": {}, "constraints": {}, "checks": []}
                print(f"  [{i}/{len(targets)}] {aid} ERR: {str(e)[:120]}")

        towers: Any = None
        if r.get("towers"):
            try:
                towers = json.loads(r["towers"])
            except Exception:
                towers = r.get("towers")
        local = {
            "region": r.get("region"), "universe": r.get("universe"), "delay": r.get("delay"),
            "neutralization": r.get("neutralization"), "skeleton": r.get("skeleton"),
            "sharpe": r.get("sharpe"), "fitness": r.get("fitness"), "turnover": r.get("turnover"),
            "two_year": r.get("two_year"), "sub_universe": r.get("sub_universe"),
            "prod": r.get("prod"), "self": r.get("self"), "towers": towers,
            "gate": r.get("gate"), "status": r.get("status"), "note": r.get("note"),
            "expr": r.get("expr"),
        }
        card = {"alpha_id": aid, "local": local, "platform": plat}
        if not plat.get("error"):
            card["layers"] = derive(local, plat)
        cards.append(card)

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = a.out or os.path.join(RESULTS, f"candidate_health_card_{ts}.json")
    summary = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": "submit_ready", "status": a.status or "*", "region": a.region or "*",
        "count": len(cards),
        "all_pass": sum(1 for c in cards if (c.get("layers") or {}).get("gate_layer", {}).get("all_pass")),
        "margin_ok": sum(1 for c in cards if (c.get("layers") or {}).get("gate_layer", {}).get("margin_ok")),
        "with_constraint": sum(1 for c in cards if (c.get("layers") or {}).get("vf_layer", {}).get("constraint_sharpe")),
        "candidates": cards,
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tmp = out_path + ".tmp"
    json.dump(summary, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, out_path)
    print(f"\n[done] {out_path}")
    print(f"[summary] count={summary['count']} all_pass={summary['all_pass']} "
          f"margin_ok={summary['margin_ok']} with_constraint={summary['with_constraint']}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, MCP_DIR)
    try:
        import _pyenv  # type: ignore  # noqa: E402
        # bootstrap_paths() 把 <repo>/src 与 MCP 目录都注入 sys.path —— 之后才能 `import wqb.*`
        # （只 insert(MCP_DIR) 只够 brain_api，不够 wqb）。
        _pyenv.bootstrap_paths()
        _pyenv.reexec_under_venv()
    except Exception:
        pass
    sys.exit(main())
