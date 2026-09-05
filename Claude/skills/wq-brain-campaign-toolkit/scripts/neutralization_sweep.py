# -*- coding: utf-8 -*-
"""neutralization_sweep.py - 中性化/设置对照批生成（增强流水线 v2 设置层⑪⑫，零配额）。

诊断背景：GBR TOP700 截面下 SUBINDUSTRY 可能过度中性化（每行业仅数只股票），
该假说从未验证。本脚本把 top-N 赢家表达式渲染成多档中性化/decay 的对照批，
输出标准 alpha_list.json（per-item settings），交给 batch_simulator 七槽提交。

用法:
  # 中性化四档对照（默认）
  python neutralization_sweep.py --campaign-dir tracking/GBR --exprs winners.json
  # 自定义变体（笛卡尔积）
  python neutralization_sweep.py --campaign-dir tracking/GBR --exprs winners.json \
      --neutralizations SECTOR MARKET \
      --vary "decay:4,8" "truncation:0.05,0.08"
输出:
  candidates/settings_sweep_alpha_list.json   标准 alpha_list.json（直接交 batch_simulator）
  candidates/settings_sweep_plan.json         每批变体说明（回测后按 batch 对齐结果）
"""
import argparse
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, add_campaign_arg, atomic_write, load_json, read_exprs_any

DEFAULT_NEUTRALIZATIONS = ["SUBINDUSTRY", "SECTOR", "MARKET", "STATISTICAL"]
TOP_N = 4  # 每变体取 top-N 表达式（4 档 × 4 条 = 16 条 = 2 批）

EXPR_FIELD = "regular"


def main():
    ap = argparse.ArgumentParser(description="中性化/设置对照批生成（零配额，产出交 batch_simulator）")
    add_campaign_arg(ap)
    ap.add_argument("--exprs", required=True, help="top 赢家表达式文件（列表或 wave 风格 dict）")
    ap.add_argument("--neutralizations", nargs="*", default=DEFAULT_NEUTRALIZATIONS,
                    help="中性化档位（默认 SUBINDUSTRY/SECTOR/MARKET/STATISTICAL）")
    ap.add_argument("--vary", nargs="*", default=[], help='额外设置变体 "key:v1,v2"（笛卡尔积）')
    ap.add_argument("--top-n", type=int, default=TOP_N, help="每变体表达式条数（默认 4）")
    ap.add_argument("--wave", default="sweep", help="expressions 入库波号（默认 sweep）")
    ap.add_argument("--out", default=None, help="兼容：仅显式指定 alpha_list 导出文件名（交 batch_simulator）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    exprs = read_exprs_any(a.exprs)
    exprs = [e for e in exprs if isinstance(e, str)][:a.top_n]
    if not exprs:
        ap.error("--exprs 无有效表达式")

    # 变体轴：neutralization + 额外 vary
    vary_axes = {}
    for v in a.vary:
        if ":" not in v:
            ap.error(f"--vary 项格式应为 key:v1,v2，得到 {v}")
        k, vals = v.split(":", 1)
        vary_axes[k] = [x.strip() for x in vals.split(",") if x.strip()]
    axes = {"neutralization": list(a.neutralizations), **vary_axes}
    combos = [{}]
    for k, vals in axes.items():
        combos = [{**c, k: v} for c in combos for v in vals]

    base = dict(ctx.settings)
    alpha_list, plan = [], []
    for combo in combos:
        settings = copy.deepcopy(base)
        settings.update({k: v for k, v in combo.items() if k != "_exclude"})
        # 数值化：decay/truncation 等容忍字符串数字
        for k in list(settings):
            if isinstance(settings[k], str) and settings[k].lstrip("-").replace(".", "").isdigit():
                settings[k] = float(settings[k]) if "." in settings[k] else int(settings[k])
        for e in exprs:
            alpha_list.append({"type": "REGULAR", "settings": settings, EXPR_FIELD: e})
        plan.append({"vars": combo, "exprs": exprs, "note": "回测后按 settings 对齐结果 CSV"})

    # 主轨入库：变体批入 expressions 表（status=sweep）+ 计划入 ledger，零文件写
    from _lib.wqb_store import get_store
    st = get_store(ctx)
    try:
        r = st.upsert_expressions(
            ctx.region, a.wave,
            [{"expression": it[EXPR_FIELD], "settings": it["settings"], "status": "sweep"}
             for it in alpha_list],
            status="sweep",
        )
        st.upsert_ledger(ctx.region, "settings_sweep_plan",
                         {"axes": axes, "n_combos": len(combos), "n_total": len(alpha_list),
                          "plan": plan, "wave": a.wave})
        print(f"[db] 变体批入库成功: {r.get('n')} 条 wave={a.wave}（计划已入 ledger settings_sweep_plan）")
    except Exception as e:
        print(f"[db] 入库异常（仍打印候选）: {e}", file=sys.stderr)
    finally:
        st.close()

    if a.out:
        out_list = ctx.path("candidates", a.out)
        atomic_write(out_list, alpha_list)
        print(f"-> {out_list}")
    print(f"变体轴: {axes}")
    print(f"{len(combos)} 种设置 × {len(exprs)} 条 = {len(alpha_list)} 条 REGULAR（约 {len(alpha_list) // ctx.batch_size() + 1} 批）")
    print("下一步: batch_simulator.py 七槽提交；"
          "回测后对比各 neutralization 档位 sharpe 分布，验证过度中性化假说")


if __name__ == "__main__":
    main()
