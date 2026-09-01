# -*- coding: utf-8 -*-
"""提交闭环后的 DB 收尾（备份先行）：

1) d5jJebLv: status UNSUBMITTED -> COMPLETE（与其余 8 颗 ACTIVE 对齐），并补 submission_ledger
2) Jj7aRNKm / 2rlVPwdw: 写入平台 submit#1 给出的权威 PROD/SELF 值
"""
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "src"))

DB = WQ_ROOT / "data" / "wqb.db"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BAK = WQ_ROOT / "data" / f"wqb.db.bak_submit3_{STAMP}"

# 平台 submit#1 权威值（本地预检值略有差异，见报告）
PLATFORM_VALUES = {
    "Jj7aRNKm": {"prod": 0.9445, "self": 0.9445},  # 本地: prod 0.9445 / self 0.9449
    "2rlVPwdw": {"prod": 0.9128, "self": 0.9128},  # 本地: prod 0.9128 / self 0.9133
}


def backup():
    """用 sqlite3 backup API 做 WAL 一致性备份（直接 cp 会漏未 checkpoint 的 WAL）。"""
    src = sqlite3.connect(str(DB))
    dst = sqlite3.connect(str(BAK))
    with dst:
        src.backup(dst)
    src.close()
    dst.close()
    print(f"[backup] {BAK.name}")


def main():
    backup()
    from wqb.store.campaign import CampaignStore

    con = sqlite3.connect(str(DB))
    cur = con.cursor()

    # 1) d5jJebLv status 对齐
    cur.execute(
        "UPDATE alphas SET status='COMPLETE' WHERE alpha_id='d5jJebLv' AND status<>'COMPLETE'"
    )
    print(f"[alphas] d5jJebLv status -> COMPLETE (rows={cur.rowcount})")

    # 2) 两颗写入平台权威双闸值（只填 NULL，不覆盖已有）
    for aid, v in PLATFORM_VALUES.items():
        cur.execute(
            "UPDATE alphas SET prod_correlation=?, self_correlation=? "
            "WHERE alpha_id=? AND (prod_correlation IS NULL OR self_correlation IS NULL)",
            (v["prod"], v["self"], aid),
        )
        print(f"[alphas] {aid} prod={v['prod']} self={v['self']} (rows={cur.rowcount})")

    con.commit()

    # 3) d5jJebLv 补落账（平台已于 2026-08-31 08:34 ET 提交成功）
    store = CampaignStore(str(DB))
    try:
        store.record_submission(
            alpha_id="d5jJebLv",
            region="IND",
            submission_type="REGULAR",
            status="ACTIVE",
            verdict={
                "note": "submitted outside this script; backfilled from platform details",
                "platform_status": "ACTIVE",
                "stage": "OS",
                "date_submitted": "2026-08-31T08:34:25-04:00",
                "checks": [
                    {"name": "PROD_CORRELATION", "value": 0.5716, "limit": 0.7, "result": "PASS"},
                    {"name": "SELF_CORRELATION", "value": 0.3704, "limit": 0.7, "result": "PASS"},
                    {"name": "IS_LADDER_SHARPE", "value": 2.85, "limit": 2.02, "result": "PASS"},
                ],
            },
            quota_used=1,
        )
        print("[ledger] d5jJebLv recorded")
    except Exception as e:
        print(f"[ledger] FAILED {e}")
    store.close()

    # 验证
    cur.execute(
        """SELECT alpha_id, status, platform_status, stage, prod_correlation,
                  self_correlation, is_ladder_sharpe, date_submitted
           FROM alphas WHERE alpha_id IN ('d5jJebLv','Jj7aRNKm','2rlVPwdw')"""
    )
    print("\n[verify]")
    for r in cur.fetchall():
        print("  ", r)
    cur.execute(
        "SELECT alpha_id, status, quota_used, submitted_at FROM submission_ledger WHERE alpha_id='d5jJebLv'"
    )
    print("[ledger verify]", cur.fetchall())
    con.close()


if __name__ == "__main__":
    main()
