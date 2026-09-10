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

import ace_lib


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _wqb_store():
    roots = [
        os.environ.get("WQB_ROOT"),
        os.environ.get("WQ_PROJECT_ROOT"),
        r"D:\coding\traeCN_project\wqb",
    ]
    for root in roots:
        if not root:
            continue
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            from wqb.store import CampaignStore
            db = os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")
            return CampaignStore(db)
    raise ImportError("wqb.store not found; set WQB_ROOT")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--idea", default=None, help="idea_context.json（兼容；优先 --from-db）")
    ap.add_argument("--from-db", action="store_true", help="从 ledger idea / expressions 读")
    ap.add_argument("--region", default=None, help="区域（--from-db 或写库必填）")
    ap.add_argument("--dataset", default=None, help="数据集 id")
    ap.add_argument("--delay", type=int, default=None, help="delay")
    ap.add_argument("--wave", default=None, help="expressions 波号（默认 s2_<ds>_d<delay>）")
    ap.add_argument("--settings_json", required=True, help="JSON string of settings config")
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
            decay=int(resolved.get("decay", 0)),
            neutralization=resolved["neutralization"],
            truncation=float(resolved.get("truncation", 0.08)),
            pasteurization=resolved.get("pasteurization", "ON"),
            test_period=resolved.get("testperiod", "P0Y0M0D"),
            unit_handling=resolved.get("unithandling", "VERIFY"),
            nan_handling=resolved.get("nanhandling", "OFF"),
            max_trade=resolved.get("maxtrade", "OFF"),
            visualization=bool(resolved.get("visualization", False)),
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
