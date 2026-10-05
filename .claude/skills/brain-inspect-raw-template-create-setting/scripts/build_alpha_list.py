from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _wqb_store():
    """CampaignStore（WQB_DB_PATH 优先隔离）；找不到工作区直接报错并说明怎么设。"""
    from scripts._workspace import open_store
    st = open_store()
    if st is None:
        raise ImportError("找不到 wqb 工作区（含 src/wqb）：设 WQB_WORKSPACE 指向工作区根")
    return st


#: 可选设置字段（键为小写）。--settings_json 里没给的，优先取战役 config/settings.json，再用下面的脚本缺省。
#: 战役 settings.json 与脚本缺省**并不总是一致**（nanHandling / maxTrade 各区 ON、OFF 都有），
#: 所以漏传时静默用脚本缺省会悄悄改变回测口径——这里把每个缺省的来源打印出来（skills 审查 IR-07）。
OPTIONAL_DEFAULTS = {
    "decay": 0,
    "truncation": 0.08,
    "pasteurization": "ON",
    "testperiod": "P0Y0M0D",      # 「无测试期」统一写 P0Y0M0D；P6Y 是真实的 6 年测试期，不是无测试期
    "unithandling": "VERIFY",
    "nanhandling": "OFF",
    "maxtrade": "OFF",
    "visualization": False,
}


def fill_optional(resolved: dict, campaign_settings: dict | None = None) -> tuple[dict, dict]:
    """补齐可选字段。返回 (补齐后的 dict, {字段: 来源})。--settings_json 里给出的键永远优先；
    其次战役 settings.json（键大小写不敏感）；最后脚本缺省。"""
    camp = {str(k).lower(): v for k, v in (campaign_settings or {}).items() if not str(k).startswith("_")}
    out = dict(resolved)
    sources: dict = {}
    for key, default in OPTIONAL_DEFAULTS.items():
        if key in out:
            sources[key] = "settings_json"
        elif key in camp:
            out[key] = camp[key]
            sources[key] = "campaign settings.json"
        else:
            out[key] = default
            sources[key] = "脚本缺省"
    return out, sources


def main() -> None:
    import ace_lib      # 延迟导入：ace_lib 依赖 tqdm 等，只有真正构建 alpha 时才需要（fill_optional 等纯函数可单测）

    ap = argparse.ArgumentParser()
    ap.add_argument("--idea", default=None, help="idea_context.json（兼容；优先 --from-db）")
    ap.add_argument("--from-db", action="store_true", help="从 ledger idea / expressions 读")
    ap.add_argument("--region", default=None, help="区域（--from-db 或写库必填）")
    ap.add_argument("--dataset", default=None, help="数据集 id")
    ap.add_argument("--delay", type=int, default=None, help="delay")
    ap.add_argument("--wave", default=None, help="expressions 波号（默认 s2_<ds>_d<delay>）")
    ap.add_argument("--settings_json", required=True, help="JSON string of settings config")
    ap.add_argument("--campaign-dir", default=None,
                    help="战役目录：--settings_json 没给的可选字段（decay / truncation / nanHandling / maxTrade / "
                         "testPeriod / unitHandling / pasteurization / visualization）取该目录 config/settings.json；"
                         "不传则用脚本缺省（每个字段的来源都会打印）")
    ap.add_argument("--out", default=None, help="兼容：仅当显式指定时写 alpha_list.json（测试）")
    args = ap.parse_args()

    try:
        settings_doc = json.loads(args.settings_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string provided for --settings_json: {e}")

    resolved_raw = settings_doc.get("resolved", settings_doc)
    if not isinstance(resolved_raw, dict):
        raise ValueError("Settings file must contain settings dict or 'resolved' key")

    resolved = {k.lower(): v for k, v in resolved_raw.items()}
    camp_settings = None
    if args.campaign_dir:
        camp_path = Path(args.campaign_dir) / "config" / "settings.json"
        if not camp_path.is_file():
            raise SystemExit(f"--campaign-dir 下没有 config/settings.json: {camp_path}")
        camp_settings = _load_json(camp_path)
    resolved, opt_sources = fill_optional(resolved, camp_settings)
    print("[settings] 可选字段来源: " + ", ".join(f"{k}={resolved[k]!r}({v})" for k, v in opt_sources.items()))
    region = (args.region or resolved.get("region") or "").upper()
    dataset = args.dataset or resolved.get("dataset") or resolved.get("datasetid")
    delay = args.delay if args.delay is not None else int(resolved.get("delay", 1))
    wave = args.wave or (f"s2_{dataset}_d{delay}" if dataset else None)
    if not region:
        raise ValueError("region required (--region or settings.region)")
    if not wave:
        raise ValueError("--wave or --dataset required")

    expressions: list[str] = []
    if args.from_db or not args.idea:
        st = _wqb_store()
        try:
            idea = None
            if dataset is not None:
                idea = st.get_idea(region, str(dataset), int(delay))
            if idea and isinstance(idea.get("expression_list"), list):
                expressions = [str(x) for x in idea["expression_list"] if x]
            if not expressions:
                rows = st.list_expressions(region, str(wave), dataset=dataset)
                expressions = [r["expression"] for r in rows if r.get("expression")]
        finally:
            st.close()
        if not expressions:
            raise SystemExit(f"DB 无表达式: {region}/{wave}（可先 GEM 入库或传 --idea）")
    else:
        idea_ctx = _load_json(Path(args.idea).resolve())
        expressions = idea_ctx.get("expression_list") or []
        if not isinstance(expressions, list) or not all(isinstance(x, str) for x in expressions):
            raise ValueError("idea_context.json must contain expression_list: list[str]")

    new_alphas = [
        ace_lib.generate_alpha(
            regular=expr,
            alpha_type="REGULAR",
            region=resolved["region"],
            universe=resolved["universe"],
            delay=int(resolved["delay"]),
            decay=int(resolved["decay"]),
            neutralization=resolved["neutralization"],
            truncation=float(resolved["truncation"]),
            pasteurization=resolved["pasteurization"],
            test_period=resolved["testperiod"],
            unit_handling=resolved["unithandling"],
            nan_handling=resolved["nanhandling"],
            max_trade=resolved["maxtrade"],
            visualization=bool(resolved["visualization"]),
        )
        for expr in expressions
    ]

    expressions_data = []
    for alpha in new_alphas:
        if not isinstance(alpha, dict) or "regular" not in alpha:
            continue
        expressions_data.append({
            "expression": alpha["regular"],
            "status": "pending",
            "settings": alpha.get("settings") or {
                k: resolved[k] for k in (
                    "region", "universe", "delay", "decay", "neutralization", "truncation"
                ) if k in resolved
            },
            "dataset": dataset,
        })

    st = _wqb_store()
    try:
        st.save_wave_expressions(region, str(wave), expressions_data, dataset=dataset, status="pending")
    finally:
        st.close()
    print(f"Saved {len(expressions_data)} expressions to database: {region}/{wave}")

    if args.out:
        out_path = Path(args.out).resolve()
        existing_alphas = []
        if out_path.exists():
            try:
                existing_alphas = _load_json(out_path)
                if not isinstance(existing_alphas, list):
                    existing_alphas = []
            except Exception:
                existing_alphas = []
        final_list = existing_alphas + new_alphas
        out_path.write_text(json.dumps(final_list, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"(compat) Wrote {len(new_alphas)} alphas to {out_path}")


if __name__ == "__main__":
    main()
