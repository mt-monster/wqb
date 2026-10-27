#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IND 全数据集 · 全模板族流水线（带断点续跑）— 薄入口。

2026-10-25：从 EUR 侧的区域参数化版本复制到 IND skill 自带一份，**region 硬钉为 IND**。
此前 IND 借用 EUR skill 的 eur_main.py / eur_runner.py（靠 WQB_CAMPAIGN_REGION=IND），
代码归属与运行区域不一致，容易串；现在 IND 自带一份，断点仍用 _IND 后缀，可无缝续跑。
模块分工见 `wqb_campaign/`（与 EUR 副本逐字相同；S6 只放行完全相同的副本，分叉即 FAIL）。

模块分工
--------
    config      路径常量（含补 LIT_CACHE）
    persist     checkpoint / results / heartbeat 原子读写
    bad_tokens  平台拒绝名单
    transport   sims_terminal / wait_slot / dispatch / harvest（所有可能挂起处）
    fields      字段选择（语义分类 / 幽灵过滤 / full+probe）
    generate    模板族 + build_exprs + 后处理电池
    audit       check_prod / year_profile / fetch_codes
    lit         compute_lit（点塔计数）
    sweep       设置轴补扫
    report      digest / progress
    pipeline    run()（原 main）

用法：
  python ind_main.py                                   # 从断点继续
  python ind_main.py --datasets insiders1 option1
  python ind_main.py --only-cats EARNINGS,INSIDERS
  python ind_main.py --min-cov 0.35 --require-ten-years
  WQB_CAMPAIGN_FRESH=1 python ind_main.py
"""
import os
import sys

# ★ 必须在 import wqb_campaign 之前钉住区域：config.py 的缺省是 EUR，且会把
#   REGION 写回环境变量；漏设就会去读写 EUR 的断点/数据集（KOR 副本踩过此坑）。
os.environ["WQB_CAMPAIGN_REGION"] = "IND"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wqb_campaign.pipeline_ind import run  # noqa: E402
from wqb_campaign.lock import InstanceLock, AlreadyRunning  # noqa: E402

if __name__ == "__main__":
    # 单实例：同一 (region, lane) 只允许一个 campaign，防止同一断点上双写
    try:
        with InstanceLock("campaign"):
            run()
    except AlreadyRunning as e:
        print(f"[lock] {e}")
        raise SystemExit(3)
