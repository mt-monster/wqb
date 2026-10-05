# -*- coding: utf-8 -*-
"""s2_compliance_mark.py - S2 合规标记工具：写入特征工程文档记录到 ledger_kv。

用法:
  python s2_compliance_mark.py --campaign-dir <DIR> --wave <WAVE> \\
      --doc-path <PATH> [--candidate-pool-source skill|manual] [--notes "备注"]

示例:
  python s2_compliance_mark.py --campaign-dir tracking/KOR --wave 36 \\
      --doc-path tracking/KOR/feature_engineering_kor_streetaccount1_20260826.md \\
      --candidate-pool-source skill --notes "brain-data-feature-engineering skill 生成"
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, add_campaign_arg
from _lib.wqb_store import get_store


def main():
    ap = argparse.ArgumentParser(description="S2 合规标记工具")
    add_campaign_arg(ap)
    ap.add_argument("--wave", required=True, help="波次编号")
    ap.add_argument("--doc-path", required=True, help="特征工程文档路径")
    ap.add_argument("--candidate-pool-source", default="skill",
                    choices=["skill", "manual"],
                    help="候选池来源: skill=brain-data-feature-engineering skill 生成, manual=手动构建")
    ap.add_argument("--notes", default="", help="备注说明")
    ap.add_argument("--force", action="store_true", help="强制覆盖已有记录")
    a = ap.parse_args()

    ctx = CampaignContext(a.campaign_dir)

    # 校验文档存在
    if not os.path.exists(a.doc_path):
        print(f"[error] 文档不存在: {a.doc_path}")
        sys.exit(1)

    # 校验文档内容包含必要章节
    with open(a.doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    required_sections = ["字段", "特征", "建议"]
    missing = [s for s in required_sections if s not in content]
    if missing:
        print(f"[warning] 文档缺少推荐章节: {missing}（仍允许标记，但建议补充）")

    # 构建记录
    record = {
        "feature_engineering_doc": os.path.abspath(a.doc_path),
        "candidate_pool_source": a.candidate_pool_source,
        "wave": a.wave,
        "region": ctx.region,
        "marked_at": __import__('datetime').datetime.now().isoformat(timespec="seconds"),
        "notes": a.notes,
        "checklist_version": "1.0"
    }

    # 写入 ledger_kv
    st = get_store(ctx)
    try:
        key = f"s2_compliance_w{a.wave}"
        existing = st.get_ledger(ctx.region, key)
        if existing and not a.force:
            print(f"[error] 记录已存在（wave={a.wave}），使用 --force 覆盖")
            print(f"  现有记录: doc={existing.get('feature_engineering_doc')}")
            sys.exit(1)

        result = st.upsert_ledger(ctx.region, key, record)
        print(f"[ok] S2 合规标记已写入: {result}")
        print(f"  wave={a.wave}, doc={os.path.basename(a.doc_path)}, source={a.candidate_pool_source}")
        if a.notes:
            print(f"  notes={a.notes}")
    finally:
        st.close()


if __name__ == "__main__":
    main()
