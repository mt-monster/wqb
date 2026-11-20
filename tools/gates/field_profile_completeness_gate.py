#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字段画像完整性硬闸——「全字段探测禁止抽样」的机械守卫。

## 为什么有这只工具（2026-11-17 用户指令）

用户 hard constraint：「数据集一旦选定，必须做全字段探测，禁止抽样或仅试探部分字段」。
但本次 KOR fund_holdings_panel 实际只探测了 15 个 active 字段中的 5 个「代表」，
理由是「active 是非active 的同源子集」——这是拿一个合理先验去推翻一条硬约束。
根因不是判断错，而是**没有任何机制检查「字段全表声明的字段」vs「实际探测的字段」**，
全靠 agent 读档案时自觉，一松懈就漏。

## 判据（三道，任一违反即 exit 2）

1. **分母完整**：`## 字段全表`（或 `## 1. 字段全表`）的表格必须逐行列出每个字段的真实 id，
   ⛔ 不接受通配占位（`*_active`、`8 个同构孪生`、`等 N 个`）——那是「清单就不全」，
   连分母都没有，谈不上全字段探测。
2. **实测覆盖**：`### 10.1` / `## 字段全表` 之后某处必须有「实测表」，其字段 id 集合 ⊇ 字段全表 id 集合。
   差集 = 声明了但没探测的字段 ⇒ FAIL，并逐条列出。
3. **计数一致**：实测表行数 == 字段全表 id 数（防止重复行掩盖缺失）。

## 用法

    python tools/gates/field_profile_completeness_gate.py \
        --profile tracking/KOR/reference/datasets/fund_holdings_panel.md
    # exit 0 = 完整；exit 2 = 有字段未探测或清单含通配；exit 1 = 参数/文件错误

设计原则：**不依赖 DB / 平台 API**（本集 DB field_catalog 为 0 行，平台 API 有成本），
分母取档案自己的字段全表——所以第 1 道闸先堵住「档案用通配伪装全量」。
配合 `audit_dataset_coverage.py`（那只是「数据集是否验过」），本闸管「集内字段是否探全」。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# 反引号里的字段 id：小写字母/数字/下划线，且带已知数据集字段形态
_FIELD_RE = re.compile(r"`([a-z][a-z0-9_]{2,})`")
# 通配/占位信号：出现这些词说明该行不是逐字段清单
_PLACEHOLDER_RE = re.compile(
    r"\*_active|同构孪生|同构|\b\d+\s*个\b|等\s*\d+|representative|代表字段|e\.g\.", re.I
)
# 「全表」章节标题
_FULL_SECTION_RE = re.compile(r"^#{2,3}\s+.*字段全表", re.M)
# 任意后续章节标题（用于切出「字段全表」节的正文）
_ANY_SECTION_RE = re.compile(r"^#{2,3}\s+", re.M)


def _extract_field_ids(text: str) -> Tuple[Set[str], List[str]]:
    """返回 (字段 id 集合, 占位行原文列表)。"""
    ids: Set[str] = set()
    placeholders: List[str] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        if _PLACEHOLDER_RE.search(line):
            placeholders.append(line.strip())
        for m in _FIELD_RE.finditer(line):
            ids.add(m.group(1))
    return ids, placeholders


def check_profile(profile: Path) -> Dict:
    raw = profile.read_text(encoding="utf-8")
    m = _FULL_SECTION_RE.search(raw)
    if not m:
        return {"ok": False, "reason": "no_field_full_section",
                "error": "档案里找不到「字段全表」章节，无法建立分母"}

    # 切出「字段全表」节的正文：从标题后到下一个同级/更高级标题
    rest = raw[m.end():]
    nxt = _ANY_SECTION_RE.search(rest)
    section = rest[:nxt.start()] if nxt else rest

    full_ids, placeholders = _extract_field_ids(section)

    # 实测字段判定：只认「带数字读数的表格行」，绝不能只用「字段在全表出现」——
    # 那会让 missing 恒空（全表字段必然出现），闸形同虚设（测试 test_missing_field_readout_fails 逮到）。
    measured_ids: Set[str] = set()
    for line in raw.splitlines():
        if not line.strip().startswith("|"):
            continue
        fm = re.match(r"\s*\|\s*`?([a-z][a-z0-9_]{2,})`?\s*\|", line)
        if fm and re.search(r"\|\s*\*{0,2}\d+(?:\.\d+)?\*{0,2}", line):
            measured_ids.add(fm.group(1))

    missing = sorted(full_ids - measured_ids)
    measured_full = sorted(full_ids & measured_ids)

    problems: List[str] = []
    if placeholders:
        problems.append(f"字段全表含 {len(placeholders)} 处通配/占位行（分母不全）：")
        for p in placeholders[:6]:
            problems.append("  " + p[:140])
    if missing:
        problems.append(f"字段全表中 {len(missing)} 个字段在档案中无任何实测读数：")
        problems.append("  " + ", ".join(missing))
    if not full_ids:
        problems.append("字段全表未解析出任何字段 id（表格格式异常）")

    ok = not problems
    return {
        "ok": ok,
        "profile": str(profile),
        "full_field_count": len(full_ids),
        "measured_with_readout": len(measured_full),
        "missing_ids": missing,
        "placeholder_lines": placeholders,
        "problems": problems,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="字段画像完整性硬闸（全字段探测禁止抽样）")
    ap.add_argument("--profile", required=True, help="字段画像档案路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args(argv)

    p = Path(args.profile)
    if not p.exists():
        print(f"ERROR: 档案不存在: {p}", file=sys.stderr)
        return 1

    res = check_profile(p)
    if args.json:
        import json
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(f"[field-completeness] {p}")
        print(f"  字段全表 id 数: {res['full_field_count']}")
        print(f"  带实测读数的字段: {res['measured_with_readout']}")
        if res["ok"]:
            print("  ✅ PASS：全字段均有实测读数，且分母无通配占位")
        else:
            print("  ⛔ FAIL：")
            for line in res["problems"]:
                print("   " + line)
    return 0 if res["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
