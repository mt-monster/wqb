import os
"""Submit EUR RA candidate qMNEG2Z2 with tri-state verification.

Flow: POST /submit (201 accepted) -> GET /submit (200 final) -> wait async
-> re-GET -> OS pool ACTIVE confirmation.
qMNEG2Z2: rev252*0.5 + rev252*vol_rank*0.5, EUR/TOP2500/D1/STATISTICAL
IS: S 2.30 / F 1.27 / subU 1.51 / 2Y 2.36 (全部 PASS)
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(os.environ.get("WQ_JUDGE_SKILL", os.path.join(os.path.expanduser("~"), ".zcode", "skills", "brain-alpha-judge"))) / "scripts" / "vendor"))
from load_credentials import load_credentials
from ace_client import AceClient

ALPHA = "qMNEG2Z2"


def main():
    creds = load_credentials(skill_dir=Path(os.environ.get("WQ_JUDGE_SKILL", os.path.join(os.path.expanduser("~"), ".zcode", "skills", "brain-alpha-judge"))))
    client = AceClient(username=creds.username, password=creds.password)

    print(f"\n=== {ALPHA} ===")
    v1 = client.get_submit_verdict(ALPHA)
    print(f"round1: post={v1['post_status']} verdict={v1['verdict_status']} "
          f"success={v1['final_success']} failed={v1['failed_checks']}")

    if not v1["final_success"]:
        print(f"  REJECTED at round1, skipped async wait")
        return

    # wait for async checks (SELF_CORRELATION / PROD_CORRELATION / DATA_DIVERSITY)
    print("  waiting 60s for async checks...")
    time.sleep(60)
    v2 = client.get_submit_verdict(ALPHA)
    print(f"round2: post={v2['post_status']} verdict={v2['verdict_status']} "
          f"success={v2['final_success']} failed={v2['failed_checks']}")

    if v2["final_success"]:
        print("  FINAL SUCCESS (async checks passed)")
    elif v2["verdict_status"] == 404:
        print("  SUBMISSION RECORD CLEARED - rejected by async checks")
    else:
        print("  status:", v2["verdict_status"], "failed:", v2["failed_checks"])


if __name__ == "__main__":
    main()
