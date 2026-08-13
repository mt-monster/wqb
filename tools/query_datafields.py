#!/usr/bin/env python3
"""Query get_datafields for key datasets and output analysis-ready format."""
import sys, os, json, asyncio
from pathlib import Path

MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))
os.chdir(str(MCP_DIR))

env_path = MCP_DIR / ".env"
for line in env_path.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line: continue
    k, v = line.split('=', 1)
    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TRACKING_DIR = Path(__file__).parent.parent / "tracking"
from brain_api import BrainApiClient

DATASETS = [
    ("model110", "MDL110 ML composite"),
    ("model243", "Combined Alpha Model (alpha#3 candidate)"),
    ("other36", "Japanese Short Positions (alpha#3 candidate)"),
]

SETTINGS = {"region": "ASI", "universe": "MINVOL1M", "delay": 1}

async def query_datafields(bc, dataset_id, label):
    """Call get_datafields API and return processed results."""
    try:
        resp = await bc._request(
            'GET',
            f"{bc.base_url}/data-fields"
            f"?dataset.id={dataset_id}"
            f"&region={SETTINGS['region']}"
            f"&universe={SETTINGS['universe']}"
            f"&delay={SETTINGS['delay']}"
        )
        data = resp.json() if hasattr(resp, 'json') else resp

        # Process: extract key fields
        results = data.get("results", data.get("data", data)) if isinstance(data, dict) else data

        if isinstance(results, list):
            fields = results
        elif isinstance(results, dict):
            fields = results.get("datafields", results.get("results", []))
        else:
            fields = []

        return {
            "dataset_id": dataset_id,
            "label": label,
            "total_count": len(fields),
            "filtered": False,
            "fields": fields,
        }
    except Exception as e:
        return {"dataset_id": dataset_id, "label": label, "error": str(e)}

async def main():
    bc = BrainApiClient()
    await bc.ensure_authenticated()
    print("[AUTH] OK\n")

    for ds_id, label in DATASETS:
        print(f"\n--- {ds_id}: {label} ---")
        result = await query_datafields(bc, ds_id, label)

        if "error" in result:
            print(f"  ERROR: {result['error']}")
            continue

        fields = result.get("fields", [])
        print(f"  Total fields: {len(fields)}")

        # Show top fields by alphaCount (sorted)
        if fields:
            sorted_fields = sorted(fields, key=lambda f: f.get("alphaCount", f.get("alpha_count", 0)) or 0, reverse=True)
            print(f"\n  Top 10 fields by alphaCount:")
            print(f"  {'field_id':<40} {'type':<10} {'count':>6} {'cov':>6} {'id_sh':>6} {'os_sh':>6}")
            print(f"  {'-'*40} {'-'*10} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")

            for f in sorted_fields[:15]:
                fid = f.get("id", "?")[:38]
                ftype = f.get("type", "?")[:8]
                cnt = f.get("alphaCount", f.get("alpha_count", 0)) or 0
                cov = f.get("coverage", f.get("coverageRatio", 0)) or 0
                id_sh = f.get("isSharpe", f.get("is_sharpe", 0)) or 0
                os_sh = f.get("osSharpe", f.get("os_sharpe", 0)) or 0

                # Filter out non-positive sharpe fields for cleaner output
                actual_sh = id_sh or os_sh
                if actual_sh <= 0:
                    continue

                print(f"  {fid:<40} {ftype:<10} {cnt:>6} {cov:>5.2f} {id_sh:>5.2f} {os_sh:>5.2f}")

        # Save to tracking
        out_file = TRACKING_DIR / f"datafields_{ds_id}_asi.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n  Saved: {out_file}")

    print("\n[DONE]")

if __name__ == "__main__":
    asyncio.run(main())
