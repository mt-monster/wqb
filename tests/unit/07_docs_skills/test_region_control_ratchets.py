# -*- coding: utf-8 -*-
"""区域 × 类别控制层的两条棘轮（2026-10-04）：

1. 代码里按区域代码字面量做分支 / 查表——区域差异应放在数据层（tracking/<R>/config、config.py、
   platform_constraints.json、cells.json），新增即红；
2. thresholds.json 里没有读取方的键——写了却不生效的配置会让人以为「已经按区域控制住了」（KOR 闸 7 / CW 的教训），
   新增即红。
两条都是「只许减不许增」：修掉的条目必须从基线删掉（否则基线会掩护以后的回归）。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIX = ROOT / "tests" / "fixtures"

from wqb.profiles.audit import region_literal_branches, unread_threshold_keys  # noqa: E402


def _by_file_name(entries):
    """按「文件名:种类:区域」比对——脚本挪进主题目录（tools/<主题>/）不算新增。"""
    out = set()
    for e in entries:
        path, kind, regions = e.rsplit(":", 2)
        out.add(f"{Path(path).name}:{kind}:{regions}")
    return out


def test_no_new_region_literal_branches():
    base = _by_file_name(json.loads((FIX / "region_literal_baseline.json").read_text(encoding="utf-8"))["entries"])
    now = _by_file_name(region_literal_branches())
    new, fixed = sorted(now - base), sorted(base - now)
    assert not new, ("新增了按区域代码字面量的分支 / 查表（区域差异写进数据层：tracking/<R>/config、config.py、"
                     "platform_constraints.json 或 cells.json）：\n  " + "\n  ".join(new))
    assert not fixed, "这些条目已修掉，请从 tests/fixtures/region_literal_baseline.json 删除：\n  " + "\n  ".join(fixed)


def test_no_new_unread_threshold_keys():
    base = set(json.loads((FIX / "threshold_unread_keys_baseline.json").read_text(encoding="utf-8"))["entries"])
    now = set(unread_threshold_keys())
    new, fixed = sorted(now - base), sorted(base - now)
    assert not new, ("thresholds.json 新增了代码里没有读取方的键（先接线再写配置，或写进 cells.json）：\n  "
                     + "\n  ".join(new))
    assert not fixed, ("这些阈值键已删掉或接上了读取方，请从 tests/fixtures/threshold_unread_keys_baseline.json 删除：\n  "
                       + "\n  ".join(fixed))
