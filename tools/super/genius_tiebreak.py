"""genius_tiebreak.py — Genius tie-breaker「六维」基线计算 + 候选边际估算。

官方口径（`brain-genius` 文档 §Criteria → "What happens if more consultants
qualify for a level than there are available spots?"，2026-09-18 版），六个
tie-breaker 指标（**同档超额时用「六项排名之和」排序，不是单看某一项**）：

===== ================================ ============== ==========================
序号   指标                              方向            本工具字段
===== ================================ ============== ==========================
 T1    Avg distinct Operators / Alpha    越低越好        avg_ops_per_alpha
 T2    Avg distinct Fields / Alpha       越低越好        avg_fields_per_alpha
 T3    Total distinct Operators          越高越好        total_distinct_ops
 T4    Total distinct Fields             越高越好        total_distinct_fields
 T5    Maximum Simulation Streak         越高越好        （平台未暴露，需人工看面板）
 T6    Community leader                  越高越好        （论坛赞+推荐，平台未暴露）
===== ================================ ============== ==========================

⚠ 官方脚注：`ts_backfill` / `group_backfill` **不计入** T1/T3 的算子计数。

⚠ 口径注意：T5/T6 与「提交哪颗 alpha」无关（streak 靠每天仿真、community 靠
论坛/推荐），所以候选评估只需管 T1–T4；本工具对 T5/T6 显式标注 `n/a`，
不静默省略。

为什么这决定「收益最大化」
--------------------------
六维不是加分项，是**同档超额时的排序键**。Genius 等级决定数据/算子权限与
季度付款档位（Grand Master 可达 80x、$8000+/季），而等级由「三项 eligibility
达标者之间的六维排名和」决定 ⇒ 六维是"能不能拿到更高付款档"的临门一脚。
又因官方明说 "Formulating a higher number of pyramids can potentially improve
both the Value Factor and Combined Alpha Performance through diversification"
（`brain-genius`），六维（T3/T4 要高）与塔（要多样）方向一致：
**少而新的算子/字段 + 多塔**＝同时讨好六维与 CAP。

用法：
    py tools/genius_tiebreak.py --compute                  # 账户六维基线
    py tools/genius_tiebreak.py --alphas 88N6OOP7,omEdka3v # 候选六维边际
    py tools/genius_tiebreak.py --compute --alphas ... --json
    py tools/genius_tiebreak.py --probe                    # 探测平台是否开放端点

设计说明：本文件是**仓库正式入口**，不是一次性临时脚本 —— MCP 目前没有暴露
Genius tie-breaker 端点（`get_leaderboard` 只给 valueFactor/dataFieldsUsed/
submissionsCount/meanProd/meanSelf），故按用户 2026-11-15 工具偏好「确实没有
对应 MCP 能力时才写脚本，并说明原因」落在这里，后续复用。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path


def _find_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / "world-quant-brain-mcp").is_dir():
            return parent
    raise RuntimeError("仓库根未找到（向上未见 world-quant-brain-mcp 目录）")


_ROOT = _find_root()
_MCP_DIR = _ROOT / "world-quant-brain-mcp"
for _p in (str(_MCP_DIR), str(_ROOT / "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# 官方脚注：这两个算子不计入 T1/T3
_EXCLUDED_OPS = frozenset({"ts_backfill", "group_backfill"})

_CACHE = _ROOT / "output_report" / ".cache_genius_os_alphas.json"


# --------------------------------------------------------------------------
# 表达式 → (distinct ops, distinct fields)
# --------------------------------------------------------------------------
def parse_expr(code: str) -> tuple[set[str], set[str]]:
    """返回 (distinct 算子集, distinct 字段集)。

    算子集已按官方脚注剔除 ts_backfill/group_backfill。

    口径说明：FASTEXPR 里 `name(` 形式必然是算子（语言无用户自定义函数），
    故不必依赖 `VERIFIED_SAFE_OPERATORS` —— 该常量在运行时从 config 状态加载，
    实测常为空（`len()==0`），依赖它会静默把算子全算成 0。
    与平台 `regular.operatorCount` 的差别：后者是**调用次数**（含重复），
    官方 tiebreak 要的是 **distinct**，故此处自行去重。
    """
    from wqb.expression.atom import extract_fields  # noqa: WPS433

    import re

    calls = set(re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code or ""))
    ops = calls - _EXCLUDED_OPS

    # 字段：复用仓库分词（已剔除算子调用、赋值左值、字符串、保留字）。
    # ★ 口径对齐平台：`dataFieldsUsed` 只数**数据集字段**，不含 base market
    #   fields（close/open/returns/cap…）与 grouping keys（sector/industry…）。
    #   实测不剔除时 T4=495，剔除后与平台 422 对齐（见 tools/genius_tiebreak.py 输出）。
    raw = {f for f in extract_fields(code or "")}
    fields = {f for f in raw if _is_dataset_field(f)}
    return ops, fields


def _is_dataset_field(name: str) -> bool:
    """是否平台口径下的「数据集字段」（剔除 base 行情字段与分组键）。"""
    try:
        from wqb.expression.atom import BASE_MARKET_FIELDS, GROUPING_KEYS  # noqa: WPS433
    except Exception:  # noqa: BLE001 - 导入失败就全算（宁可多算也不漏）
        return True
    if name in BASE_MARKET_FIELDS:
        return False
    if name.lower() in GROUPING_KEYS:
        return False
    return True


# --------------------------------------------------------------------------
# 平台取数
# --------------------------------------------------------------------------
async def _client():
    from brain_api import brain_client  # noqa: WPS433

    await brain_client.ensure_authenticated()
    return brain_client


async def fetch_os_alphas(refresh: bool = False, limit: int = 100) -> list[dict]:
    """拉全量已提交 alpha（OS），带本地缓存。"""
    if not refresh and _CACHE.exists():
        try:
            return json.loads(_CACHE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass

    client = await _client()
    rows: list[dict] = []
    offset = 0
    while True:
        resp = await client._request(
            "GET",
            f"{client.base_url}/users/self/alphas",
            params={"stage": "OS", "limit": limit, "offset": offset},
        )
        if resp.status_code != 200:
            print(f"[WARN] OS 列表 offset={offset} status={resp.status_code}", file=sys.stderr)
            break
        data = resp.json()
        batch = data.get("results") or []
        rows.extend(batch)
        if not data.get("next") or not batch:
            break
        offset += limit

    _CACHE.parent.mkdir(parents=True, exist_ok=True)
    _CACHE.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return rows


# --------------------------------------------------------------------------
# 六维基线
# --------------------------------------------------------------------------
def _code_of(row: dict) -> str:
    """原始 REST 把 code 放在 regular 子对象里（MCP 才拍平到顶层）。"""
    return ((row.get("regular") or {}).get("code")) or row.get("code") or ""


def _platform_opcount(row: dict) -> int | None:
    """平台自己的 operatorCount（=调用次数，含重复；用于与 distinct 口径对照）。"""
    v = (row.get("regular") or {}).get("operatorCount")
    return v if isinstance(v, int) else None


def compute_baseline(os_rows: list[dict]) -> dict:
    """计算 T1–T4。默认只统计 REGULAR（SUPER 由组件拼装，官方 tiebreak 主体是
    自身 alpha；同时给出含 SUPER 的对照，便于识别口径差异）。"""
    out: dict = {"n_total_os": len(os_rows)}

    for label, keep_super in (("regular", False), ("with_super", True)):
        rows = [
            r for r in os_rows
            if _code_of(r) and (keep_super or (r.get("type") or "REGULAR") == "REGULAR")
        ]
        if not rows:
            continue
        n = len(rows)
        sum_ops = sum_fields = 0
        sum_platform_oc = 0
        n_platform_oc = 0
        union_ops: set[str] = set()
        union_fields: set[str] = set()
        per_alpha: list[dict] = []
        for r in rows:
            code = _code_of(r)
            ops, fields = parse_expr(code)
            sum_ops += len(ops)
            sum_fields += len(fields)
            union_ops |= ops
            union_fields |= fields
            oc = _platform_opcount(r)
            if oc is not None:
                sum_platform_oc += oc
                n_platform_oc += 1
            per_alpha.append({"id": r.get("id"), "ops": len(ops), "fields": len(fields)})
        out[label] = {
            "n": n,
            "T1_avg_ops_per_alpha": round(sum_ops / n, 4),
            "T2_avg_fields_per_alpha": round(sum_fields / n, 4),
            "T3_total_distinct_ops": len(union_ops),
            "T4_total_distinct_fields": len(union_fields),
            "_avg_platform_opcount": (
                round(sum_platform_oc / n_platform_oc, 4) if n_platform_oc else None
            ),
            "_sum_ops": sum_ops,
            "_sum_fields": sum_fields,
            "_union_ops": sorted(union_ops),
            "_union_fields": sorted(union_fields),
            "_per_alpha": per_alpha,
        }
    return out


def candidate_marginal(base: dict, code: str) -> dict:
    """单颗候选对 T1–T4 的边际（以 regular 口径为基准）。"""
    b = base.get("regular") or {}
    if not b:
        return {"error": "no baseline"}
    n, sum_ops, sum_fields = b["n"], b["_sum_ops"], b["_sum_fields"]
    union_ops = set(b["_union_ops"])
    union_fields = set(b.get("_union_fields") or ())

    ops, fields = parse_expr(code)
    new_n = n + 1
    t1_old, t1_new = sum_ops / n, (sum_ops + len(ops)) / new_n
    t2_old, t2_new = sum_fields / n, (sum_fields + len(fields)) / new_n

    return {
        "ops": len(ops),
        "fields": len(fields),
        "ops_list": sorted(ops),
        "fields_list": sorted(fields),
        "T1": {"old": round(t1_old, 4), "new": round(t1_new, 4),
               "delta": round(t1_new - t1_old, 4),
               "verdict": "better" if t1_new < t1_old else ("worse" if t1_new > t1_old else "flat")},
        "T2": {"old": round(t2_old, 4), "new": round(t2_new, 4),
               "delta": round(t2_new - t2_old, 4),
               "verdict": "better" if t2_new < t2_old else ("worse" if t2_new > t2_old else "flat")},
        "T3": {"new_ops_introduced": sorted(ops - union_ops),
               "verdict": "better" if (ops - union_ops) else "flat"},
        "T4": {"new_fields_introduced": sorted(fields - union_fields),
               "verdict": "better" if (fields - union_fields) else "flat"},
        "T5": "n/a（streak，靠每日仿真，与选件无关）",
        "T6": "n/a（community，靠论坛/推荐，与选件无关）",
    }


# --------------------------------------------------------------------------
# 端点探测（平台是否已开放 tiebreak 明细）
# --------------------------------------------------------------------------
_CANDIDATE_ENDPOINTS = (
    "/users/self/competition/genius",
    "/users/self/competition/leaderboard",
    "/users/self/genius",
    "/users/self/activities/genius",
    "/consultant/genius",
)


async def probe() -> dict:
    client = await _client()
    out: dict = {}
    for path in _CANDIDATE_ENDPOINTS:
        try:
            resp = await client._request("GET", f"{client.base_url}{path}")
            try:
                body = resp.json()
            except Exception:  # noqa: BLE001
                body = None
            out[path] = {"status": resp.status_code, "body": body}
        except Exception as exc:  # noqa: BLE001
            out[path] = {"status": None, "error": str(exc)}
    return out


async def _alpha_code(alpha_id: str) -> str | None:
    """候选表达式。原始 REST 用 `/users/self/alphas/{id}`（`/alphas/{id}` 会 404）。"""
    client = await _client()
    for path in (f"/users/self/alphas/{alpha_id}", f"/alphas/{alpha_id}"):
        resp = await client._request("GET", f"{client.base_url}{path}")
        if resp.status_code == 200:
            body = resp.json() or {}
            return _code_of(body)
    return None


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Genius tie-breaker 六维基线/边际")
    ap.add_argument("--compute", action="store_true", help="计算账户六维基线")
    ap.add_argument("--alphas", default="", help="候选 id，逗号分隔")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    ap.add_argument("--refresh", action="store_true", help="强制重新拉取 OS alpha 列表")
    ap.add_argument("--probe", action="store_true", help="探测平台 tiebreak 端点")
    args = ap.parse_args()

    if args.probe:
        print(json.dumps(asyncio.run(probe()), ensure_ascii=False, indent=2))
        return 0

    if not (args.compute or args.alphas):
        ap.print_help()
        return 2

    result: dict = {}

    async def _run():
        rows = await fetch_os_alphas(refresh=args.refresh) if args.compute or args.alphas else []
        if args.compute:
            result["baseline"] = compute_baseline(rows)
        if args.alphas:
            base = result.get("baseline") or compute_baseline(rows)
            result["baseline"] = base
            cands = {}
            for aid in [x.strip() for x in args.alphas.split(",") if x.strip()]:
                code = await _alpha_code(aid)
                if not code:
                    cands[aid] = {"error": "code not found"}
                    continue
                cands[aid] = candidate_marginal(base, code)
            result["candidates"] = cands

    asyncio.run(_run())

    # 精简输出：去掉大数组，避免刷屏
    slim = {
        "baseline": {
            k: ({kk: vv for kk, vv in v.items() if not kk.startswith("_")}
                if isinstance(v, dict) else v)
            for k, v in result.get("baseline", {}).items()
        },
        "candidates": result.get("candidates", {}),
    }
    print(json.dumps(slim, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
