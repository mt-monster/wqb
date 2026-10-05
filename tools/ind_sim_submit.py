"""IND 战役专用：按精确 settings 直连 POST /simulations（multi-sim），绕开 CLI 固定档。

用法:
    python tools/ind_sim_submit.py --path tracking/IND/candidates/xxx_exprs.txt \
        --decay 8 --neutralization STATISTICAL [--preflight-catalog data/field_catalog.json]

与 tools/submit_batch.py 的差别：本脚本显式带 nanHandling / maxTrade
（CLI 固定 OFF/ON，实测会把行为族信号 S 2.19 -> 0.46 打掉）。

字段名预检（--preflight-catalog）：本项目最高频白跑原因=坏字段导致整批 children 连坐 CANCELLED
（已踩 3 次：台账近似名、数据集内前缀不统一、手写 id 臆测）。提交前用本地 catalog 兜底校验。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))

# FASTEXPR 里的算子/参数名（不是字段）
_FUNC_NAMES = {
    "group_rank", "group_zscore", "group_neutralize", "group_backfill", "ts_mean", "ts_delta",
    "ts_rank", "ts_quantile", "ts_zscore", "ts_std_dev", "ts_scale", "ts_backfill", "ts_sum",
    "ts_product", "ts_min", "ts_minmax", "ts_max", "ts_decay_linear", "ts_decay_exp_window",
    "ts_av_diff", "ts_corr", "ts_clip", "ts_argmin", "ts_argmax", "ts_target_tvr_decay",
    "ts_target_tvr_hump", "ts_regression", "vec_avg", "vec_sum", "vec_max", "vec_min",
    "vec_count", "vec_stddev", "vec_ir", "vec_kurtosis", "vec_skewness", "vec_range",
    "rank", "zscore", "scale", "normalize", "winsorize", "tail", "truncate", "quantile",
    "clip", "abs", "sign", "log", "sqrt", "exp", "power", "inverse", "s_log", "reverse",
    "multiply", "divide", "add", "subtract", "negate", "bucket", "kth_element",
    "last_diff_value", "hump", "hump_decay", "days_from_last_change", "trade_when",
    "if_else", "and", "or", "not", "greater", "less", "equal", "std", "driver", "newval",
    "lower", "upper", "buckets", "range", "stddev", "target_tvr", "dense", "constant",
}
_PARAM_NAMES = {"x", "y", "z", "a", "b", "c", "d", "n", "w", "f", "k", "i", "j", "p", "q", "m"}


def extract_fields(expr: str) -> set[str]:
    """从 FASTEXPR 提取候选字段标识符（粗筛：排除已知算子名与参数名）。"""
    out = set()
    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr):
        if tok in _FUNC_NAMES or tok in _PARAM_NAMES or tok.startswith("lambda"):
            continue
        out.add(tok)
    return out


def load_catalog(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("fields", data.get("data", []))
    ids = []
    for row in data or []:
        if isinstance(row, dict):
            fid = row.get("id") or row.get("field_id") or row.get("name")
            if fid:
                ids.append(fid)
        elif isinstance(row, str):
            ids.append(row)
    return ids



# 常见算子名（用于从表达式中剥离函数、只剩字段名）
_KNOWN_OPS = {
    "vec_avg", "vec_sum", "vec_max", "vec_min", "vec_count", "vec_stddev", "vec_range",
    "ts_rank", "ts_mean", "ts_sum", "ts_delta", "ts_zscore", "ts_std_dev", "ts_backfill",
    "ts_decay_linear", "ts_quantile", "ts_scale", "ts_corr", "ts_arg_max", "ts_arg_min",
    "ts_av_diff", "ts_max_diff", "ts_regression", "ts_count_nans", "ts_ir", "ts_step",
    "quantile", "rank", "zscore", "scale", "normalize", "winsorize", "vector_neut",
    "group_rank", "group_zscore", "group_neutralize", "group_mean", "group_scale",
    "group_backfill", "bucket", "densify", "hump", "trade_when", "if_else", "tail", "kth_element",
    "add", "subtract", "multiply", "divide", "abs", "sign", "log", "sqrt", "exp", "power",
    "signed_power", "inverse", "reverse", "negate", "less", "greater", "equal", "and", "or",
    "not", "max", "min", "pasteurize", "last_diff_value", "days_from_last_change",
}


def _extract_field_like(expr: str) -> List[str]:
    """粗提表达式里的字段标识符（排除算子名与内置字段）。"""
    import re as _re

    builtins = {"open", "high", "low", "close", "vwap", "returns", "adv20", "adv60",
                "cap", "sharesout", "volume", "sector", "industry", "subindustry",
                "market", "country", "exchange", "date"}
    out = []
    for tok in _re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr):
        if tok in _KNOWN_OPS or tok in builtins or tok.isdigit():
            continue
        out.append(tok)
    return out


def _check_field_types_by_region(exprs: List[str], region: str) -> List[str]:
    """校验「MATRIX 字段不该套 vec_avg」「VECTOR 字段应套聚合」。

    返回问题描述列表（空=通过）。库不可用时静默通过（不阻断工具）。
    """
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    try:
        from wqb.region_catalog import RegionCatalog

        rc = RegionCatalog()
        ftype: Dict[str, str] = {}
        for ds in rc.dataset_names(region):
            for r in rc.fields(ds, region=region):
                ftype.setdefault(str(r["field_name"]), str(r["field_type"] or ""))
        rc.close()
    except Exception as e:  # 库不可用：不阻断
        print(f"[ind-sim] 跳过字段类型检查（本地 catalog 不可用: {type(e).__name__}）")
        return []

    import re as _re

    problems: List[str] = []
    for i, e in enumerate(exprs, 1):
        vec = set(_re.findall(r"vec_\w+\(([a-zA-Z_][a-zA-Z0-9_]*)\)", e))
        for f in _extract_field_like(e):
            t = ftype.get(f)
            if not t:
                continue
            if t.upper() == "MATRIX" and f in vec:
                problems.append(
                    f"第 {i} 条：MATRIX 字段 `{f}` 被套了 vec_*()（平台只会回 status=FAIL 无报错）")
            if t.upper() == "VECTOR" and f not in vec:
                problems.append(
                    f"第 {i} 条：VECTOR 字段 `{f}` 未套 vec_*() 聚合")
    return problems


def build_settings(a: argparse.Namespace) -> dict:
    return {
        "instrumentType": "EQUITY",
        "region": a.region,
        "universe": a.universe,
        "delay": a.delay,
        "decay": a.decay,
        "neutralization": a.neutralization,
        "truncation": a.truncation,
        "pasteurization": "ON",
        "unitHandling": "VERIFY",
        "nanHandling": a.nan_handling,
        "maxTrade": a.max_trade,
        "maxPosition": "OFF",
        "language": "FASTEXPR",
        "visualization": False,
        "startDate": "2014-01-01",
        "endDate": "2023-12-31",
    }


async def main_async(a: argparse.Namespace) -> int:
    from brain_api import brain_client as brain  # noqa: E402

    # 表达式行判定：FASTEXPR 只可能由 ASCII 标识符/数字/括号/逗号/引号/空格组成。
    # 裸中文注释行会被当表达式送进平台并让整批 children 连坐 CANCELLED，
    # 故按"含 CJK 字符即跳过"过滤，而不只认# 前缀。
    lines = Path(a.path).read_text(encoding="utf-8").splitlines()
    exprs, skipped = [], []
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if any("一" <= ch <= "鿿" for ch in s):
            skipped.append(s)
            continue
        exprs.append(s)
    if skipped:
        print(f"[ind-sim] skip {len(skipped)} non-FASTEXPR line(s) (CJK/annotation)")
        for s in skipped[:3]:
            print(f"[ind-sim]   e.g. {s[:60]}")
    # ---- 括号平衡硬闸（2026-10-04 补）----
    # check_expression 只查括号"是否配对"于它自己解析的粒度，对 f-string 少写一个右括号
    # 这类整体失衡会漏放行（实测 7/8 条 balance=1 全部发到平台报 "Unexpected end of input"
    # 并连坐整批 CANCELLED）。这里做最朴素的全量计数，零成本。
    unbalanced = []
    for e in exprs:
        bal = 0
        for ch in e:
            bal += (ch == "(") - (ch == ")")
        if bal:
            unbalanced.append((e[:60], bal))
    if unbalanced:
        print(f"[ind-sim] ABORT: {len(unbalanced)} 条括号不平衡（会整批连坐 CANCELLED）:")
        for frag, bal in unbalanced:
            print(f"          balance={bal:+d}  {frag}...")
        return 3
    print(f"[ind-sim] 括号平衡自检 OK（{len(exprs)} 条）")

    # ---- 字段类型闸（2026-10-05 补）----
    # 平台对「MATRIX 字段套 vec_avg()」这类类型不匹配**只回 status=FAIL 且无任何 message**
    # （实测 d92：8/8 FAIL 零报错，白扔 8 槽位）。本地 fields 表带 field_type 且实测与平台一致，
    # 故在此按区读 `field_type` 做静态校验。
    type_bad = _check_field_types_by_region(exprs, a.region)
    if type_bad:
        print(f"[ind-sim] ABORT: {len(type_bad)} 条字段类型用法有误:")
        for line in type_bad:
            print(f"          {line}")
        return 3
    print(f"[ind-sim] 字段类型自检 OK（region={a.region}）")

    st = build_settings(a)
    print(f"[ind-sim] n={len(exprs)} settings={json.dumps(st, ensure_ascii=False)}")
    if a.dry_run:
        print("[ind-sim] DRY-RUN sample:", json.dumps(
            {"type": "REGULAR", "settings": st, "regular": exprs[0]}, ensure_ascii=False)[:400])
        return 0

    # 字段名预检（零成本，防整批连坐 CANCELLED）
    if a.preflight_catalog:
        known = set(load_catalog(a.preflight_catalog))
        if known:
            unknown = sorted({f for e in exprs for f in extract_fields(e) if f not in known})
            if unknown:
                print(f"[ind-sim] ABORT: 字段不在本地 catalog {a.preflight_catalog}:")
                for u in unknown:
                    print(f"          - {u}")
                print("[ind-sim] 请用 get_datafields(dataset_id=...) 核对真实字段 id 后再提交。")
                return 3
            print(f"[ind-sim] preflight OK: {len(exprs)} 条表达式的字段全部存在于 catalog")
        else:
            print(f"[ind-sim] WARN: catalog {a.preflight_catalog} 为空，跳过预检")

    await brain.ensure_authenticated()

    chunks = [exprs[i:i + 10] for i in range(0, len(exprs), 10)]
    for ch in chunks:
        payload = [{"type": "REGULAR", "settings": st, "regular": e} for e in ch]
        body = payload[0] if len(payload) == 1 else payload
        r = await brain._request("POST", brain.base_url + "/simulations", json=body)
        if r.status_code >= 400:
            print(f"[ind-sim] POST {r.status_code}: {str(brain._response_payload(r))[:400]}")
            return 2
        loc = r.headers.get("Location", "")
        print(f"[ind-sim] submitted {len(ch)} -> {loc}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--region", default="IND")
    ap.add_argument("--universe", default="TOP500")
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--decay", type=int, default=8)
    ap.add_argument("--neutralization", default="STATISTICAL")
    ap.add_argument("--truncation", type=float, default=0.08)
    ap.add_argument("--nan-handling", default="ON")
    ap.add_argument("--max-trade", default="OFF")
    ap.add_argument("--preflight-catalog", default="",
                    help="本地字段 catalog JSON；提供则提交前校验字段存在性")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    return asyncio.run(main_async(a))


if __name__ == "__main__":
    sys.exit(main())
