from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))


@dataclass(frozen=True)
class ResolvedSettings:
    instrumentType: str
    region: str
    delay: int
    universe: str
    neutralization: str
    decay: int = 0
    truncation: float = 0.08
    pasteurization: str = "ON"
    testPeriod: str = "P0Y0M0D"
    unitHandling: str = "VERIFY"
    nanHandling: str = "OFF"
    maxTrade: str = "OFF"
    language: str = "FASTEXPR"
    visualization: bool = False


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_candidates(idea_ctx: dict[str, Any], options_snapshot: dict[str, Any]) -> dict[str, Any]:
    region = str(idea_ctx["region"])
    delay = int(idea_ctx["delay"])

    rows = options_snapshot.get("rows") or []
    if not isinstance(rows, list):
        raise ValueError("options snapshot 'rows' must be a list")

    # Filter for matching Instrument/Region/Delay
    candidates = [
        r
        for r in rows
        if r.get("InstrumentType") == "EQUITY" and r.get("Region") == region and int(r.get("Delay")) == delay
    ]

    if not candidates:
        raise RuntimeError(
            f"No valid settings found for InstrumentType=EQUITY, Region={region}, Delay={delay}. "
            "Re-fetch options or adjust region/delay."
        )

    # In practice, usually there's only one 'row' per (Instrument, Region, Delay) combination 
    # that contains the lists of valid Universes and Neutralizations.
    # But we'll return all matches just in case.
    
    return {
        "context": {
            "dataset": idea_ctx.get("dataset_id"),
            "region": region,
            "delay": delay
        },
        "valid_options": candidates
    }


def _wqb_store():
    """定位 workspace src/wqb 的 CampaignStore（WQB_DB_PATH 优先隔离）。"""
    import os
    roots = [os.environ.get("WQB_ROOT"), os.environ.get("WQ_PROJECT_ROOT"),
             r"D:\coding\traeCN_project\wqb"]
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
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--idea", required=True, help="idea_context.json")
    ap.add_argument("--options", required=True, help="sim_options_snapshot.json")
    ap.add_argument("--out", default=None, help="兼容：settings_candidates.json 导出路径（下游 AI 消费契约）")
    args = ap.parse_args()

    idea_path = Path(args.idea).resolve()
    opt_path = Path(args.options).resolve()

    idea_ctx = _load_json(idea_path)
    options = _load_json(opt_path)

    payload = resolve_candidates(idea_ctx, options)

    # 主轨入库：设置候选入 ledger_kv（region + dataset/delay 维度），文件仅显式 --out 写
    region = (payload.get("context") or {}).get("region")
    ds = (payload.get("context") or {}).get("dataset")
    delay = (payload.get("context") or {}).get("delay")
    key = f"resolve_settings_{ds}_d{delay}" if ds else "resolve_settings"
    st = _wqb_store()
    if st is not None and region:
        try:
            st.upsert_ledger(region, key, payload)
            print(f"[db] 设置候选入 ledger {region}:{key}")
        except Exception as e:
            print(f"[db] 入库异常（仍写文件）: {e}", file=sys.stderr)
        finally:
            st.close()
    elif st is None:
        print("[db] wqb workspace 未定位，跳过入库", file=sys.stderr)

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote candidates: {out_path}")
    print("Next step: AI should inspect these candidates and the 'idea' text to choose specific settings.")


if __name__ == "__main__":
    main()
