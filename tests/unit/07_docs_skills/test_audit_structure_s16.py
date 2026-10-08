# -*- coding: utf-8 -*-
"""test_audit_structure_s16.py — S16「报告/产物命名规范」的守护测试。

为什么要有 S16
--------------
AGENTS.md §8.13 的命名规范（日期 `YYYYMMDD` **作后缀**、不带杠、纯 ASCII 无空格）
此前只写在文档里。2026-10-08 第二轮输出目录复核发现两个后果：

  ① 第一轮治理把 `output_report/`+`reports/` 的日期带杠件全部改名，却**漏扫了
     `tracking/` 顶层** —— 4 个 `tracking/2026-10-0X_robustness.md` 一直躺着；
  ② 之后仍有会话把分析报告写进 `cache/`（不入库，`git clean -fd` 即永久丢失）。

文字纪律守不住持续的写入。S16 把它变成读数：**存量入基线 → WARN，新增违规 → FAIL**。

本文件只测两件事：① S16 挂进了 `CHECKS`（否则写了函数也没人跑）；
② 命名判据本身判得对（纯函数 `_naming_violations`，无需沙箱、只读）。
"""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s16", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s16"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_s16_is_registered_in_checks(az):
    """S16 必须挂进 CHECKS，否则写了检查函数也没人跑（S13 的同款守）。"""
    assert "s16" in az.CHECKS, "S16 未注册到 CHECKS"
    assert az.CHECKS["s16"][1] is az.check_s16_output_naming


@pytest.mark.parametrize("name", [
    "skills_review_20261003.md",          # §8.13 的正例
    "output_report_20261008.md",
    "DEU_field_profile_complete_20261008.md",
    "ra_pipeline_stage_audit_20260916.md",
    "d9_status_backfill_rollback_20260928.json",
    "robustness_20261007.md",
])
def test_compliant_names_pass(az, name):
    assert az._naming_violations(name) == [], f"{name} 应合规却被判违规"


@pytest.mark.parametrize("name,kw", [
    ("2026-10-08_robustness.md", "带杠"),        # 上一轮漏网的实际形态
    ("db_schema_audit_2026-08-26.md", "带杠"),
    ("eur_d1_20260924_financing_mode_b1.md", "不在末尾"),  # 日期夹在中间
    ("ra_pipeline_stage_audit_20260916_v3.md", "不在末尾"),
    ("glb_campaign_20261008_breakthrough.md", "不在末尾"),
    ("字段报告 20261008.md", "ASCII"),           # 非 ASCII + 空格
])
def test_violating_names_are_caught(az, name, kw):
    bad = az._naming_violations(name)
    assert bad, f"{name} 违反规范却没被判出来"
    assert any(kw in b for b in bad), f"{name} 判出来了但理由不含「{kw}」：{bad}"


def test_scan_exempts_readme_and_non_report_suffixes(az):
    """目录说明与非报告类扩展名不进扫描面（否则会把 README / 图片等误判成产物）。"""
    assert "README.md" in az.S16_EXEMPT_NAMES
    assert ".md" in az.S16_SUFFIXES
    assert ".png" not in az.S16_SUFFIXES and ".bin" not in az.S16_SUFFIXES


def test_scan_covers_the_layer_that_was_missed(az):
    """扫描面必须含 `tracking/` 顶层 —— 第一轮治理漏的正是这一层。"""
    src = TOOL.read_text(encoding="utf-8")
    assert '"tracking/*.md"' in src or "'tracking/*.md'" in src, (
        "S16 的 git ls-files 路径表缺 `tracking/*.md`："
        "第一轮治理漏掉的就是 tracking/ 顶层，扫描面不能再退回只看 output_report/reports")
