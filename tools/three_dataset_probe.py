# -*- coding: utf-8 -*-
"""three_dataset_probe.py - 3 数据集组合边界探索计划生成（P2-3，2026-08-31）。

背景：平台硬上限是混合 >3 个数据集（即 4 个及以上）不点亮金字塔，3 个是允许的。
但目前所有成功案例都是 ≤2 数据集（MEA 战役纪律 ≤2），3 数据集组合是否真的能点亮
且有增量从未验证。本工具在数据资产丰富的区域（USA/KOR）生成 1-2 批 3 数据集组合
探针，验证平台上限的真实增量。

设计原则：
  1. 三类别正交：analyst × fundamental × pv（跨金字塔层，周期+逻辑双正交）
  2. 主信号强度分层：强信号数据集作主腿（权重 0.5），中信号作辅助腿（各 0.25）
  3. 正交性预检：每两腿字段集 Jaccard < 0.3（复用 validator.check_combo_orthogonality）
  4. 早停：1 批 8 条，0 达标即停（不烧配额）

用法:
  # 生成 3 数据集组合探针批次（dry-run 只打印不写库）
  python tools/three_dataset_probe.py --campaign-dir tracking/USA \
      --datasets analyst9,fundamental94,pv1 --dry-run

  # 正式生成（入 expressions 表 status=probe3）
  python tools/three_dataset_probe.py --campaign-dir tracking/USA \
      --datasets analyst9,fundamental94,pv1 --wave probe3
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 三类别正交组合模板（主腿 0.5 + 辅助腿各 0.25）
_TEMPLATES = [
    {
        "name": "三类别加权混合",
        "expr": "add(add(multiply(0.5, rank({a})), multiply(0.25, rank({b}))), multiply(0.25, rank({c})))",
        "note": "主腿 0.5 + 辅助腿各 0.25（强信号主导）",
    },
    {
        "name": "三类别等权混合",
        "expr": "add(add(multiply(0.34, rank({a})), multiply(0.33, rank({b}))), multiply(0.33, rank({c})))",
        "note": "三等权（无主导腿，多样性探索）",
    },
    {
        "name": "主腿 × 双辅助门控",
        "expr": "trade_when(greater(rank({b}), 0.5), add(multiply(0.6, rank({a})), multiply(0.4, rank({c}))), 0)",
        "note": "辅助腿 b 作门控，主腿 a + 辅助 c（事件驱动）",
    },
    {
        "name": "三类别共振",
        "expr": "multiply(multiply(rank({a}), rank({b})), rank({c}))",
        "note": "三信号共振（同向才放大，反向抵消）",
    },
]

# 字段角色占位符（实际使用时从各数据集 typed catalog 选代表字段）
_FIELD_PLACEHOLDERS = {
    "analyst": "anl_field",
    "fundamental": "fnd_field",
    "pv": "close",
}


def _category_of(dataset: str) -> str:
    """按数据集 id 前缀归类金字塔类别。"""
    d = dataset.lower()
    for cat in ("analyst", "fundamental", "pv", "news", "sentiment", "model",
                "risk", "earnings", "insiders", "institutions", "shortinterest"):
        if d.startswith(cat):
            return cat
    return "other"


def generate_probe_exprs(datasets, field_map=None):
    """生成 3 数据集组合探针表达式。

    datasets: 3 个数据集 id 列表
    field_map: {dataset: field} 代表字段映射（缺省用占位符）
    返回 [(template_name, expr, note), ...]
    """
    if len(datasets) != 3:
        raise ValueError(f"需要恰好 3 个数据集，得到 {len(datasets)}")
    field_map = field_map or {}
    # 按类别排序：analyst -> fundamental -> pv（主腿优先 analyst）
    cats = [_category_of(d) for d in datasets]
    fields = [field_map.get(d, _FIELD_PLACEHOLDERS.get(c, f"{d}_field"))
              for d, c in zip(datasets, cats)]
    out = []
    for t in _TEMPLATES:
        expr = t["expr"].format(a=fields[0], b=fields[1], c=fields[2])
        out.append({
            "template": t["name"],
            "expr": expr,
            "note": t["note"],
            "datasets": datasets,
            "categories": cats,
            "fields": fields,
        })
    return out


def main():
    ap = argparse.ArgumentParser(description="3 数据集组合边界探索计划生成（P2-3）")
    ap.add_argument("--campaign-dir", required=True, help="战役目录")
    ap.add_argument("--datasets", required=True,
                    help="3 个数据集 id，逗号分隔（如 analyst9,fundamental94,pv1）")
    ap.add_argument("--fields", default=None,
                    help="代表字段映射，逗号分隔（如 anl9_rev:fnd94_margin:close），缺省用占位符")
    ap.add_argument("--wave", default="probe3", help="expressions 入库波号（默认 probe3）")
    ap.add_argument("--dry-run", action="store_true", help="只打印不写库")
    a = ap.parse_args()

    datasets = [d.strip() for d in a.datasets.split(",") if d.strip()]
    if len(datasets) != 3:
        ap.error(f"需要恰好 3 个数据集，得到 {len(datasets)}: {datasets}")

    field_map = {}
    if a.fields:
        parts = [f.strip() for f in a.fields.split(":") if f.strip()]
        if len(parts) == 3:
            field_map = dict(zip(datasets, parts))

    probes = generate_probe_exprs(datasets, field_map)

    print(f"[P2-3] 3 数据集组合探针：{datasets}")
    print(f"  类别: {[ _category_of(d) for d in datasets ]}")
    print(f"  字段: {[p['fields'] for p in probes[:1]][0]}")
    print(f"  模板数: {len(probes)}（每模板 1 条，共 {len(probes)} 条）")
    for i, p in enumerate(probes, 1):
        print(f"\n  {i}. [{p['template']}] {p['note']}")
        print(f"     {p['expr']}")

    # 正交性预检提示
    print("\n[P2-3] 正交性预检提示：发批前用 validator.check_combo_orthogonality")
    print("       逐对校验 3 腿字段集 Jaccard < 0.3，同族叠加直接拦截")

    if a.dry_run:
        print("\n[P2-3][dry-run] 仅打印，未入库")
        return

    # 正式入库（走 toolkit wqb_store）
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", ".qoder-cn", "skills",
                                    "wq-brain-campaign-toolkit", "scripts"))
    try:
        from _lib.common import CampaignContext
        from _lib.wqb_store import get_store
        ctx = CampaignContext(a.campaign_dir)
        st = get_store(ctx)
        try:
            r = st.upsert_expressions(
                ctx.region, a.wave,
                [{"expression": p["expr"], "status": "probe3",
                  "note": f"P2-3 3数据集探针: {p['template']}"} for p in probes],
                status="probe3",
            )
            print(f"\n[P2-3] 入库成功: {r.get('n')} 条 wave={a.wave} status=probe3")
            print("  下一步: batch_simulator.py 七槽提交；0 达标即停（早停，不烧配额）")
        finally:
            st.close()
    except Exception as e:
        print(f"\n[P2-3] 入库异常（已打印候选，可手动入库）: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
