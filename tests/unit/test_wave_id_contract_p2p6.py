# -*- coding: utf-8 -*-
"""回归测试：波号形态契约与裸时间戳归一（2026-09-17 P2-6）。

背景（实测）：`expressions.wave` 混入 20 行裸 Unix 时间戳（全部 DEU / analyst93），
成因是写入方在缺波号时用 `time.time()` 顶替，且写入路径无形态校验。

同时**锁定一条被推翻的审计结论**：审计称"DEU 波号时间戳致 floor 统计 0 样本 →
floor 恒 0.5"。实测不成立 —— 信号天花板闸读 `backtest_results.wave`（无时间戳污染），
`_run_signal_floor_gate('DEU')` 正常返回 `batches=2 / max_sh=1.7 / ok`。
故本模块的职责是**口径卫生**（波号空间不被污染），不是修 floor 闸。
"""

import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.wave_id import (  # noqa: E402
    UNLABELED_PREFIX,
    is_timestamp_wave,
    normalize_wave_id,
    wave_kind,
)


# ---- is_timestamp_wave ----------------------------------------------------

def test_detects_ten_digit_epoch():
    assert is_timestamp_wave("1789243710") is True
    assert is_timestamp_wave(1789243710) is True
    assert is_timestamp_wave(" 1789243710 ") is True


def test_rejects_normal_wave_numbers():
    """普通人工波号（105 / 192）绝不能被误判成时间戳。"""
    for w in ("105", "192", "1", "999999999"):  # 最后一项 9 位
        assert is_timestamp_wave(w) is False, w


def test_rejects_named_and_missing_waves():
    for w in ("s2_analyst93_d1", "57G", "wave104", "unlabeled_analyst93_1789243710", None, ""):
        assert is_timestamp_wave(w) is False, w


def test_rejects_out_of_range_ten_digit():
    """10 位但越界（如 0000000001）不当作时间戳，避免误伤人工编号。"""
    assert is_timestamp_wave("0000000001") is False
    assert is_timestamp_wave("99999999999") is False  # 11 位


# ---- normalize_wave_id ----------------------------------------------------

def test_normalize_rewrites_timestamp_and_keeps_traceability():
    """归一必须保留原时间戳（可逆），并带 unlabeled_ 前缀（问题自曝）。"""
    got = normalize_wave_id("1789243710", dataset="analyst93")
    assert got == "unlabeled_analyst93_1789243710"
    assert got.startswith(UNLABELED_PREFIX)
    assert "1789243710" in got  # 可回溯


def test_normalize_is_idempotent():
    once = normalize_wave_id("1789243710", dataset="analyst93")
    assert normalize_wave_id(once, dataset="analyst93") == once


def test_normalize_passes_through_named_wave_unchanged():
    """正常波号一个字节都不改（本护栏只治漂移，不做美化）。"""
    for w in ("s2_analyst93_d1", "105", "57G", "s2_reopen_r105_d1"):
        assert normalize_wave_id(w, dataset="analyst93") == w


def test_normalize_falls_back_to_region_then_generic():
    """缺 dataset 时退到 region，再退到通用锚点 —— 绝不产生空标签。"""
    assert normalize_wave_id("1789243710", region="DEU") == "unlabeled_DEU_1789243710"
    assert normalize_wave_id("1789243710") == "unlabeled_wave_1789243710"


def test_normalize_handles_none():
    assert normalize_wave_id(None) == ""


# ---- wave_kind ------------------------------------------------------------

@pytest.mark.parametrize("wave,expected", [
    ("1789243710", "timestamp"),
    ("105", "numeric"),
    ("192", "numeric"),
    ("s2_analyst93_d1", "named"),
    ("57G", "named"),
    (None, "missing"),
    ("", "missing"),
    ("   ", "missing"),
])
def test_wave_kind_classification(wave, expected):
    assert wave_kind(wave) == expected


# ---- 写入侧护栏接线 -------------------------------------------------------

def test_batch_writer_applies_normalization():
    """写入器必须真的调用归一函数（否则根因残留，存量修完还会再长）。"""
    src = open(os.path.join(REPO, "tools", "mcp_batch_writer.py"), encoding="utf-8").read()
    assert "_normalize_wave" in src
    assert "normalize_wave_id" in src
    # 两个写入分支都要过护栏
    assert src.count("wave = _normalize_wave(") == 2


def test_migration_tool_exists_and_defaults_to_dry_run():
    """迁移工具必须默认 dry-run（防误写）。"""
    src = open(os.path.join(REPO, "tools", "normalize_wave_ids.py"), encoding="utf-8").read()
    assert '"--apply"' in src
    assert "db-backup" in src
    assert "DRY-RUN" in src
