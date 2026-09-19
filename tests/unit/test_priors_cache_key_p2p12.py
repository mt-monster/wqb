# -*- coding: utf-8 -*-
"""回归测试：priors 快照键不得与 cache marker 撞名（2026-09-17 P2-12）。

背景（实测）：`priors_snapshot_*` 曾在 6 个区域（CHN/DEU/EUR/GBR/IND/USA）同时存在
大小写两版，payload 不同：

- `priors_snapshot_<REGION>`（大写）= campaign 节点的 **cache marker**（`assembled_at`+`stdout_tail`，~2033 B）
- `priors_snapshot_<region>`（小写）= toolkit `assemble_priors.py` 的**真实 payload**（wins/dead_ends，2.5–7 KB）

消费侧（GEM 的 `run.py` / `economic_priors.py`）读小写，故生成流程数据无误；
危害是**键空间歧义**：按大写查会拿到不含 `wins` 的缓存标记。

修法：cache marker 独立命名为 `assemble_priors_cache_<REGION>`，存量 6 键已改名。
本测试锁定"不再撞名"这一契约，防止回归。
"""

import os
import re
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))

CAMPAIGN = os.path.join(REPO, "src", "wqb", "workflow", "nodes", "campaign.py")
GEM_RUN = os.path.join(
    REPO, "Claude", "skills", "brain-make-some-gem", "scripts",
    "headless_runner", "run.py",
)
GEM_PRIORS = os.path.join(
    REPO, "Claude", "skills", "brain-make-some-gem", "scripts",
    "trailSomeAlphas", "economic_priors.py",
)
ASSEMBLE = os.path.join(
    REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts", "assemble_priors.py",
)


def _read(p):
    assert os.path.isfile(p), f"缺少文件：{p}"
    return open(p, encoding="utf-8").read()


def test_campaign_cache_key_is_not_priors_snapshot():
    """campaign 节点的 cache marker 不得再用 `priors_snapshot_{region}` 命名。"""
    src = _read(CAMPAIGN)
    assert 'f"assemble_priors_cache_{region}"' in src
    # 不得再有「大写 region 拼出的 priors_snapshot 键」
    assert 'f"priors_snapshot_{region}"' not in src


def test_campaign_cache_key_used_both_on_read_and_write():
    """读写两侧必须同名 —— 只改一侧会让缓存永远 miss（或永远 hit 旧键）。"""
    src = _read(CAMPAIGN)
    assert src.count('f"assemble_priors_cache_{region}"') == 2


def test_gem_consumers_read_lowercase_payload():
    """GEM 两个消费点必须读小写 payload 键（与 assemble_priors 的写入一致）。"""
    assert 'priors_snapshot_{region.strip().lower()}' in _read(GEM_RUN)
    assert 'priors_snapshot_{region.lower()}' in _read(GEM_PRIORS)


def test_assemble_priors_writes_lowercase_prefix():
    """生产者用 ctx.prefix 落小写键；ctx.prefix 必须 == region.lower()。"""
    assert "priors_snapshot_{ctx.prefix}" in _read(ASSEMBLE)
    common = _read(os.path.join(
        REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts", "_lib", "common.py",
    ))
    assert "self.prefix = self.region.lower()" in common.replace("  ", " ").replace("\n", " ")\
        or "self.prefix = self.region.lower()" in common


def test_producer_and_consumer_prefix_agree():
    """契约一致性：生产者(region.lower) == 消费者(region.lower)。"""
    g1 = re.search(r"priors_snapshot_\{([^}]+)\}", _read(GEM_RUN)).group(1)
    g2 = re.search(r"priors_snapshot_\{([^}]+)\}", _read(GEM_PRIORS)).group(1)
    assert "lower()" in g1 and "lower()" in g2


def test_live_ledger_has_no_case_collision():
    """生产库实况：`priors_snapshot_*` 不得再出现大写后缀（撞键已清理）。"""
    sys.path.insert(0, os.path.join(REPO, "src"))
    try:
        from wqb.workflow._common import resolve_db_path
    except Exception:  # pragma: no cover
        pytest.skip("resolve_db_path 不可用")
    db = resolve_db_path()
    if not os.path.isfile(db):
        pytest.skip("无生产库（CI 环境）")
    import sqlite3
    conn = sqlite3.connect(db)
    try:
        keys = [k for (k,) in conn.execute(
            "SELECT key FROM ledger_kv WHERE key LIKE 'priors_snapshot_%'"
        )]
    finally:
        conn.close()
    uppercased = [k for k in keys if k[len("priors_snapshot_"):] != k[len("priors_snapshot_"):].lower()]
    assert not uppercased, f"仍存在大写撞键：{uppercased}"
