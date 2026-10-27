# -*- coding: utf-8 -*-
"""对「S 弱 / 2Y 强」的集，按其 **max-2Y 那颗** 算年度画像，判断 2Y 是否为样本假象。

要点：这类集的 max-S 颗 2Y 往往很低，用 max-S 算年度画像会完全看错对象。
（2026-10-26 other315 的教训：S 2.91 但首年 2022、仅 2 年，任何闸位调参都无意义。）

用法：python tools/_yp_for_2y_leaders.py
"""
import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
os.environ.setdefault("WQB_REPO_ROOT", ROOT)
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))

from wqb_campaign.audit import year_profile  # noqa: E402

TARGETS = ["pv13", "insider_feats", "pattern_scores", "pv30", "continuation_score", "pv37"]


def main():
    res = json.load(open(os.path.join(ROOT, "results", "full_template_campaign_results.json"),
                         encoding="utf-8")).get("results") or {}
    for ds in TARGETS:
        v = res.get(ds) or {}
        al = [a for a in (v.get("alphas") or []) if a.get("y2") is not None]
        if not al:
            print("%-20s 无 2Y 数据" % ds)
            continue
        top = max(al, key=lambda a: a["y2"])
        yp = year_profile(top["alpha"])
        if not isinstance(yp, dict):
            print("%-20s yp 取不到（alpha=%s）" % (ds, top["alpha"]))
            continue
        print("=" * 88)
        print("%-20s max-2Y 颗 %s  S=%s 2Y=%s sub=%s"
              % (ds, top["alpha"], top.get("s"), top.get("y2"), top.get("sub")))
        print("    首年=%s  年数=%s  fragile=%s  top_year=%s top_share=%s"
              % (yp.get("first_year"), yp.get("n_years"), yp.get("fragile"),
                 yp.get("top_year"), yp.get("top_share")))
        yrs = yp.get("years") or {}
        if isinstance(yrs, dict):
            print("    年度 Sharpe: " + "  ".join("%s=%.2f" % (y, (d or {}).get("sharpe") or 0)
                                                 for y, d in sorted(yrs.items())))


if __name__ == "__main__":
    main()
