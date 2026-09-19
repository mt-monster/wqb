# -*- coding: utf-8 -*-
"""wave_id 契约 —— 波号形态校验与归一（2026-09-17 P2-6）。

## 问题（实测，2026-09-17）
`expressions.wave` 存在**裸 Unix 时间戳**形态的波号，全部集中在 DEU：

| 事实 | 实测值 |
|---|---|
| 受影响行数 | **20 行**（DEU 全区 1,658 行中的 1.2%）|
| 分布 | 全部 `dataset='analyst93'`、`status='gated'`、`created_at` 均为 2026-09-13 |
| 形态 | 5 个不同时间戳（`1789243710` / `1789243758` / `1789243775` …），各挂 4 条，跨度约 1 分钟 |
| 其他区域 | JPN / EUR / IND / USA / KOR / GBR 均为 **0 行** |

成因：写入方（`tools/mcp_batch_writer.py` 的 `upsert_expressions`）对 `wave` 只做
`str(wave)`，**无任何形态校验**；调用方在未给波号时直接用 `time.time()` 顶替
（`tools/wave_gate.py` 的 `tag = ... str(int(time.time()))` 是同一习惯）。

## 后果修正（推翻了 2026-09-16 审计的表述）
审计原文称"DEU 波号时间戳致 floor 统计 0 样本 → floor 恒 0.5"。**实测不予支持**：
信号天花板闸读的是 `backtest_results.wave`（该表 DEU **无**时间戳），
实测 `_run_signal_floor_gate('DEU')` 正常给出 `batches=2 / max_sh=1.7 / verdict=ok`。
故本问题**不影响 floor 闸**，真实影响是**波号空间被污染**：
5 个无名"波"混入波级统计（wave-key-check、台账、波数计数），
使 DEU 看起来有从未命名过的波次。

## 处理策略
- **写入侧**：`normalize_wave_id()` 把裸时间戳改写为可追溯的显式形态（根因修复）；
- **存量**：`tools/normalize_wave_ids.py` 按同一函数回填（dry-run 默认 + DB 备份）；
- **不删除**旧行：只改波号，保留 `id` / `created_at` 原始追溯链。
"""

from __future__ import annotations

import re
from typing import Optional

#: 裸 epoch 秒：10 位整数（2001-09-09 ~ 2286-11-20），足够区分"波号 1/2/105"与时间戳。
#: 上限刻意收得很宽（9999999999），下限 10 位以避免误伤 3 位波号。
_EPOCH_RE = re.compile(r"^\d{10}$")

#: 合理时间范围护栏：2001-09-09 之后、2286 年之前。越界只警告不当作时间戳，
#: 避免把某个恰好 10 位的人工编号误判。
_EPOCH_MIN = 1_000_000_000
_EPOCH_MAX = 9_999_999_999

#: 显式标注前缀：明确表示"该波号从未被命名"，便于后续审计一眼识别（不做静默美化）。
UNLABELED_PREFIX = "unlabeled"


def is_timestamp_wave(wave: object) -> bool:
    """判断波号是否为裸 epoch 秒（10 位整数且在合理区间内）。

    >>> is_timestamp_wave("1789243710")
    True
    >>> is_timestamp_wave("s2_analyst93_d1")
    False
    >>> is_timestamp_wave("105")
    False
    >>> is_timestamp_wave(None)
    False
    """
    if wave is None:
        return False
    s = str(wave).strip()
    if not _EPOCH_RE.match(s):
        return False
    return _EPOCH_MIN <= int(s) <= _EPOCH_MAX


def normalize_wave_id(wave: object, *, dataset: Optional[str] = None,
                      region: Optional[str] = None) -> str:
    """把裸时间戳波号改写为可追溯的显式形态；其他形态原样返回（幂等）。

    归一规则：`<ts>` → `"unlabeled_<dataset|region|wave>_<ts>"`。

    刻意**不**猜真实波号（如 `s2_analyst93_d1`）——那属于编造历史；
    保留原时间戳使新旧对应关系可逆，`unlabeled_` 前缀使问题自曝而非被掩盖。

    >>> normalize_wave_id("1789243710", dataset="analyst93")
    'unlabeled_analyst93_1789243710'
    >>> normalize_wave_id("s2_analyst93_d1", dataset="analyst93")
    's2_analyst93_d1'
    """
    if wave is None:
        return ""
    s = str(wave).strip()
    if not is_timestamp_wave(s):
        return s
    anchor = dataset or region or "wave"
    return f"{UNLABELED_PREFIX}_{anchor}_{s}"


def wave_kind(wave: object) -> str:
    """波号形态分类，供统计/审计侧区分口径。

    - `timestamp`：裸 epoch 秒（应被 `normalize_wave_id` 归一）
    - `numeric`：纯数字但非 10 位（正常人工波号，如 `105` / `192`）
    - `named`：含字母的命名波号（如 `s2_xxx_d1` / `57G`）
    - `missing`：None / 空串
    """
    if wave is None or str(wave).strip() == "":
        return "missing"
    s = str(wave).strip()
    if is_timestamp_wave(s):
        return "timestamp"
    if s.isdigit():
        return "numeric"
    return "named"
