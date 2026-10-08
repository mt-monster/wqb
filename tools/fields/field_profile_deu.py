#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兼容转发壳（deprecated）—— 实际实现已迁移到 tools/field_profile.py。

迁移原因（2026-10-08）："DEU 专用"版把表名硬编码为 `field_profile_deu`，
且 build 首行 `DROP TABLE IF EXISTS` ⇒ 跑第二个区域会**清掉已建区域的画像数据**。

新实现（`tools/field_profile.py`）：
  · 主表 `field_profile_perf`（复合主键 region+dataset+field）—— 多区共存不串号
  · 每区一个只读视图 `field_profile_<region小写>`（如 field_profile_eur）
  · 兼容视图 `field_profile_deu` 指向 perf 表 WHERE region='DEU'（旧查询/文档不破）
  · 新增 `--all-regions` / `--list` / `--migrate-legacy`

本文件仅保留以兼容既有引用（skill 文档 / 历史命令），行为完全转发到新实现。

用法（与旧版一致，另支持任意区域）:
    python tools/field_profile_deu.py --build --region DEU
    python tools/field_profile_deu.py --query --region EUR --verdict WEAK
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from field_profile import main  # noqa: E402

if __name__ == "__main__":
    print(
        "[deprecated] tools/field_profile_deu.py 已迁移 → tools/field_profile.py"
        "（多区域通用版，支持任意 --region）",
        file=sys.stderr,
    )
    sys.exit(main())
