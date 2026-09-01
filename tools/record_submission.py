# -*- coding: utf-8 -*-
"""提交落账工具 —— 把一次真实提交写入 submission_ledger（审计 P0-3）。

历史问题：submission_ledger 长期只有 DRYRUN 测试数据，真实提交从未入账。
提交脚本在拿到 verdict 后调用本 CLI 落账。

用法：
  # 提交成功
  python tools/record_submission.py --alpha-id 78jYpn0Z --region MEA --type SUPER --status ACTIVE

  # 提交被拒（带 verdict 明细）
  python tools/record_submission.py --alpha-id 88lGnVVX --region IND --status FAILED \
      --verdict-json '{"LOW_SHARPE": "1.37<1.58", "LOW_FITNESS": "0.81<1.0"}'

  # 批量从 verdict 文件（submit 脚本产出的 JSON）落账
  python tools/record_submission.py --from-json research-data/ind_submit_3_2026-08-29.json --region IND
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# src/wqb 包内部用绝对导入（from wqb.store.campaign ...），需把 src 也放进 path
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def main():
    ap = argparse.ArgumentParser(description="记录 alpha 提交到 submission_ledger")
    ap.add_argument("--alpha-id", help="alpha id")
    ap.add_argument("--region", help="区域，如 MEA / IND")
    ap.add_argument("--type", dest="submission_type", default="REGULAR",
                    choices=["REGULAR", "SUPER"], help="提交类型")
    ap.add_argument("--status", default="ACTIVE",
                    choices=["ACTIVE", "FAILED", "PENDING", "DRYRUN"], help="提交结果")
    ap.add_argument("--verdict-json", help="verdict JSON 字符串")
    ap.add_argument("--from-json", help="从 submit 脚本产出的 JSON 批量落账")
    ap.add_argument("--db", default=str(ROOT / "data" / "wqb.db"), help="数据库路径")
    args = ap.parse_args()

    from src.wqb.store.campaign import CampaignStore

    store = CampaignStore(args.db)

    def do(aid, region, typ, status, verdict):
        r = store.record_submission(aid, region=region, submission_type=typ,
                                    status=status, verdict=verdict)
        print(f"  {aid:<12}[{region or '?':<5}/{typ:<8}] {status}")

    if args.from_json:
        data = json.loads(Path(args.from_json).read_text(encoding="utf-8"))
        alphas = data.get("alphas") or {}
        print(f"[batch] from {args.from_json}: {len(alphas)} 条")
        for aid, info in alphas.items():
            st = "ACTIVE"
            verdict = {}
            if info.get("submit2"):
                s2 = info["submit2"]
                st = "ACTIVE" if s2.get("success") else "FAILED"
                verdict = {c.get("name"): f"{c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}"
                           for c in (s2.get("checks") or []) if c.get("result") == "FAIL"}
            elif info.get("submit1"):
                s1 = info["submit1"]
                st = "ACTIVE" if s1.get("success") else "FAILED"
                verdict = {c.get("name"): f"{c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}"
                           for c in (s1.get("checks") or []) if c.get("result") == "FAIL"}
            elif info.get("pre_error"):
                st = "FAILED"
                verdict = {"error": info["pre_error"][:200]}
            typ = "SUPER" if info.get("pre_status") == "SUPER" else args.submission_type
            do(aid, args.region or info.get("region"), typ, st, verdict or None)
    elif args.alpha_id:
        verdict = json.loads(args.verdict_json) if args.verdict_json else None
        do(args.alpha_id, args.region, args.submission_type, args.status, verdict)
    else:
        ap.error("需指定 --alpha-id 或 --from-json")


if __name__ == "__main__":
    main()
