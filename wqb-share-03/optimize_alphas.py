#!/usr/bin/env python3
"""
Optimized alpha simulation script for ASI/MINVOL1M.
Batch 1: model30 star_eps_surprise_prediction_fy1 (Alpha #1)
Batch 2: model110 mdl110_score optimization with low decay (Alpha #2)
"""
import sys
import os
import json
import time
import asyncio
import requests
from pathlib import Path
from datetime import datetime

# Setup paths
SCRIPT_DIR = Path(__file__).parent
MCP_DIR = SCRIPT_DIR.parent / "world-quant-brain-mcp"
TRACKING_DIR = SCRIPT_DIR.parent / "wqb-share-03" / "tracking"

# Add MCP dir to path for imports
sys.path.insert(0, str(MCP_DIR))

# Load credentials from .env
env_path = MCP_DIR / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)

BASE_URL = "https://api.worldquantbrain.com"
EMAIL = os.environ.get("CREDENTIALS_EMAIL", "")
PASSWORD = os.environ.get("CREDENTIALS_PASSWORD", "")

# ─── Common sim settings ───
COMMON_SETTINGS = {
    "instrumentType": "EQUITY",
    "region": "ASI",
    "universe": "MINVOL1M",
    "delay": 1,
    "neutralization": "INDUSTRY",
    "truncation": 0.15,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "visualization": False,
    "testPeriod": "P0Y0M",
    "maxTrade": "ON",
}

# ─── Batch 1: model30 star_eps_surprise (Alpha #1) ───
# Forum template sh=3.28, adapted to remove forbidden multiply
BATCH1_EXPRESSIONS = [
    # 1. Forum core (no liquidity filter, 7 ops)
    "group_rank(ts_rank(ts_decay_linear(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 5), 30), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    # 2. Forum core without ts_decay_linear (6 ops)
    "group_rank(ts_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 30), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    # 3. Proven template (ts_zscore + group_rank + ts_mean)
    "ts_zscore(group_rank(ts_mean(star_eps_surprise_prediction_fy1, 20), country), 40)",
    # 4. Proven template with cap-decile
    "ts_zscore(group_rank(ts_mean(star_eps_surprise_prediction_fy1, 20), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1'))), 40)",
    # 5. Forum core with w=60 (longer ts_rank)
    "group_rank(ts_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 60), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    # 6. Raw with cap-decile (no ts_rank, like QP9wEor5 for model110)
    "group_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), group_cartesian_product(country, bucket(rank(cap), range='0, 1, 0.1')))",
    # 7. Proven template with subindustry
    "ts_zscore(group_rank(ts_mean(star_eps_surprise_prediction_fy1, 20), subindustry), 40)",
    # 8. Forum core + ts_zscore outer (combine forum grouping with proven normalization)
    "ts_zscore(group_rank(ts_rank(ts_backfill(winsorize(star_eps_surprise_prediction_fy1, std=5), 60), 30), country), 40)",
]

# ─── Batch 2: model110 mdl110_score optimization (Alpha #2, decay=4) ───
# Skill insight: decay=4/5 boosts IS_LADDER_SHARPE to 2.0+
BATCH2_EXPRESSIONS = [
    # 1. bldevK7m (w=40) with decay=4 — original best asi_jpn 0.91
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),40),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    # 2. w=30 with decay=4
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),30),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    # 3. w=50 with decay=4
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),50),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    # 4. Raw (no ts_rank) with decay=4 — original 2Y=2.65, test if low decay fixes prod_corr
    "group_rank(ts_backfill(winsorize(mdl110_score,std=5),60),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    # 5. w=40 + ts_decay_linear(5) inside, decay=4
    "group_rank(ts_rank(ts_decay_linear(ts_backfill(winsorize(mdl110_score,std=5),60),5),40),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    # 6. w=60 with decay=4 (original rn_sh=1.79, 2Y=1.33)
    "group_rank(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),60),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    # 7. Raw + ts_decay_linear(5) inside, decay=4
    "group_rank(ts_decay_linear(ts_backfill(winsorize(mdl110_score,std=5),60),5),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
    # 8. w=40 + signed_power convexity, decay=4
    "group_rank(signed_power(subtract(ts_rank(ts_backfill(winsorize(mdl110_score,std=5),60),40),0.5),5),group_cartesian_product(country,bucket(rank(cap),range='0,1,0.1')))",
]


class WQClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self._authed = False

    def authenticate(self):
        """Authenticate with WQ Brain API using Basic Auth header."""
        import base64
        print(f"[AUTH] Authenticating as {EMAIL}...")
        credentials = f"{EMAIL}:{PASSWORD}"
        encoded = base64.b64encode(credentials.encode()).decode()
        resp = self.session.post(
            f"{self.base_url}/authentication",
            headers={"Authorization": f"Basic {encoded}"},
            timeout=30
        )
        if resp.status_code == 201:
            self._authed = True
            print("[AUTH] Success!")
            return True
        else:
            print(f"[AUTH] FAILED: {resp.status_code} {resp.text[:200]}")
            return False

    def create_multisim(self, expressions, decay=20, batch_label=""):
        """Submit a multi-simulation and return the location URL."""
        settings = dict(COMMON_SETTINGS)
        settings["decay"] = decay

        sim_data_list = []
        for expr in expressions:
            entry = {
                "type": "REGULAR",
                "settings": settings,
                "regular": expr,
            }
            sim_data_list.append(entry)

        payload = json.dumps(sim_data_list)
        print(f"[SIM] Submitting {len(expressions)} expressions (decay={decay}) {batch_label}...")

        resp = self.session.post(
            f"{self.base_url}/simulations",
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        if resp.status_code == 201:
            location = resp.headers.get("Location", "")
            print(f"[SIM] Submitted! Location: {location}")
            return location
        else:
            print(f"[SIM] FAILED: {resp.status_code} {resp.text[:300]}")
            return None

    def wait_for_completion(self, location, expected_children, timeout=900):
        """Wait for multisim completion, return results."""
        print(f"[WAIT] Polling {location} (expecting {expected_children} children, timeout={timeout}s)...")
        start = time.time()
        poll_interval = 10

        while time.time() - start < timeout:
            try:
                resp = self.session.get(location)
                if resp.status_code == 200:
                    data = resp.json()
                    status = data.get("status", "")
                    if status == "COMPLETE":
                        children = data.get("children", {}).get("simulations", [])
                        print(f"[WAIT] COMPLETE! {len(children)} children.")
                        return data
                    elif status == "FAILED":
                        print(f"[WAIT] FAILED: {data}")
                        return data
                    else:
                        elapsed = int(time.time() - start)
                        print(f"[WAIT] Status: {status} ({elapsed}s elapsed)...")
                else:
                    print(f"[WAIT] HTTP {resp.status_code}, retrying...")
            except Exception as e:
                print(f"[WAIT] Error: {e}, retrying...")

            time.sleep(poll_interval)

        print(f"[WAIT] TIMEOUT after {timeout}s")
        return None

    def get_alpha_details(self, alpha_id):
        """Get detailed alpha information including checks."""
        resp = self.session.get(f"{self.base_url}/alphas/{alpha_id}")
        if resp.status_code == 200:
            return resp.json()
        return None

    def extract_alpha_metrics(self, alpha_details):
        """Extract key metrics from alpha details."""
        if not alpha_details:
            return None

        is_data = alpha_details.get("is", {})
        os_data = alpha_details.get("os", {})
        checks = alpha_details.get("checks", [])

        # Extract check failures
        failed_checks = [c.get("name", "") for c in checks if c.get("result") == "FAIL"]
        warn_checks = [c.get("name", "") for c in checks if c.get("result") == "WARNING"]

        # Extract PnL-based metrics
        sharpe = is_data.get("sharpe", 0)
        fitness = is_data.get("fitness", 0)
        turnover = is_data.get("turnover", 0)
        margin = is_data.get("margin", 0)
        returns = is_data.get("returns", 0)
        longCount = is_data.get("longCount", 0)
        shortCount = is_data.get("shortCount", 0)

        # 2Y sharpe from checks
        two_year = None
        for c in checks:
            if "2Y" in c.get("name", "") or "IS_LADDER" in c.get("name", ""):
                two_year = c.get("value", 0)

        # Try to get 2Y from yearlyStats or pnl
        if two_year is None:
            # Try to compute from IS data
            two_year = is_data.get("sharpe", 0)  # fallback

        # Get OS sharpe (rn_sh)
        os_sharpe = os_data.get("sharpe", 0)

        return {
            "sharpe": round(sharpe, 2) if sharpe else 0,
            "fitness": round(fitness, 2) if fitness else 0,
            "turnover": round(turnover, 4) if turnover else 0,
            "margin_bp": round(margin * 10000, 2) if margin else 0,
            "returns": round(returns, 4) if returns else 0,
            "longCount": longCount,
            "os_sharpe": round(os_sharpe, 2) if os_sharpe else 0,
            "failed_checks": failed_checks,
            "warn_checks": warn_checks,
            "alpha_id": alpha_details.get("id", ""),
            "expr": alpha_details.get("regular", {}).get("code", ""),
            "decay": alpha_details.get("regular", {}).get("decay", 0),
        }


async def run_batch(client, expressions, decay, batch_name, batch_num):
    """Run a single batch and save results."""
    print(f"\n{'='*60}")
    print(f"  BATCH {batch_num}: {batch_name} (decay={decay})")
    print(f"{'='*60}\n")

    # Submit
    location = client.create_multisim(expressions, decay=decay, batch_label=f"({batch_name})")
    if not location:
        print(f"[ERROR] Failed to submit batch {batch_num}")
        return None

    # Wait for completion
    result = client.wait_for_completion(location, len(expressions), timeout=900)
    if not result:
        print(f"[ERROR] Timeout for batch {batch_num}")
        return None

    # Extract alpha IDs
    children = result.get("children", {}).get("simulations", [])
    alpha_ids = []
    for child in children:
        # Try to get alpha ID from child
        child_id = child.get("id", "")
        if child_id:
            alpha_ids.append(child_id)

    print(f"\n[RESULT] Got {len(alpha_ids)} alpha IDs from batch {batch_num}")

    # Get detailed metrics for each alpha
    alpha_results = []
    for i, aid in enumerate(alpha_ids):
        print(f"[DETAIL] Fetching alpha {i+1}/{len(alpha_ids)}: {aid}")
        details = client.get_alpha_details(aid)
        metrics = client.extract_alpha_metrics(details)
        if metrics:
            metrics["expr_idx"] = i + 1
            metrics["batch"] = batch_name
            alpha_results.append(metrics)
            print(f"  -> sh={metrics['sharpe']}, fit={metrics['fitness']}, tvr={metrics['turnover']}, margin={metrics['margin_bp']}bp, failed={metrics['failed_checks']}")
        time.sleep(1)  # Rate limit

    # Save results
    output = {
        "batch": f"opt_b{batch_num}",
        "name": batch_name,
        "decay": decay,
        "timestamp": datetime.now().isoformat(),
        "settings": COMMON_SETTINGS,
        "expressions": expressions,
        "alphas": alpha_results,
    }

    output_file = TRACKING_DIR / f"result_opt_b{batch_num}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] Results saved to {output_file}")

    return alpha_results


async def main():
    print(f"\n{'#'*60}")
    print(f"#  WQ PPA Alpha Optimization — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"#  Target: Push near-miss candidates to full pass")
    print(f"{'#'*60}\n")

    client = WQClient()

    # Authenticate
    if not client.authenticate():
        print("[FATAL] Authentication failed. Exiting.")
        return

    # ─── Batch 1: model30 star_eps (Alpha #1) ───
    b1_results = await run_batch(
        client, BATCH1_EXPRESSIONS, decay=20,
        batch_name="model30_star_eps_asi", batch_num=1
    )

    # ─── Batch 2: model110 optimization (Alpha #2, decay=4) ───
    b2_results = await run_batch(
        client, BATCH2_EXPRESSIONS, decay=4,
        batch_name="model110_mdl110_score_opt_decay4", batch_num=2
    )

    # ─── Summary ───
    print(f"\n{'='*60}")
    print("  OPTIMIZATION SUMMARY")
    print(f"{'='*60}\n")

    for batch_name, results in [("Batch 1 (model30)", b1_results), ("Batch 2 (model110 d=4)", b2_results)]:
        if not results:
            print(f"{batch_name}: NO RESULTS")
            continue

        print(f"\n{batch_name}:")
        best_sh = 0
        passing = []
        for r in results:
            sh = r.get("sharpe", 0)
            fit = r.get("fitness", 0)
            failed = r.get("failed_checks", [])
            if sh > best_sh:
                best_sh = sh
            # Check if all thresholds pass
            if (sh > 1.58 and fit > 1.0 and
                r.get("turnover", 0) >= 0.05 and r.get("turnover", 0) <= 0.30 and
                r.get("margin_bp", 0) > 5 and
                len(failed) == 0):
                passing.append(r)
                print(f"  ✅ PASS: {r['alpha_id']} sh={sh} fit={fit} tvr={r['turnover']} margin={r['margin_bp']}bp")

        if not passing:
            print(f"  Best sharpe: {best_sh} (no full pass)")
            for r in results:
                sh = r.get("sharpe", 0)
                if sh > 0.5:
                    print(f"  🟡 {r['alpha_id']}: sh={sh} fit={r.get('fitness',0)} failed={r.get('failed_checks',[])}")


if __name__ == "__main__":
    asyncio.run(main())
