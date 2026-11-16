# -*- coding: utf-8 -*-
"""知识版本指纹：让“这条经验是在什么知识状态下产生的”可回溯（2026-11-15）。

三个来源：
- `priors_sha`：本波 S2 实际消费的先验文件指纹。优先读 `wave_meta_<wave>.priors_sha`
  （`build_wave.py` 写入）；老波没有 meta 时退化为 `priors_snapshot_<region>` 的 canonical hash。
- `rules_sha`：区域规则（ledger `methodology_rules`）+ 全局规则文件的 canonical hash。
- `knowledge_version` = `priors_sha[:8]-rules_sha[:8]`，写进每条 `attempt_knowledge`。

P2/P4 可以据此按版本对比产出率（同一知识版本下的回测才有可比性）。
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Dict, Optional

from wqb.paths import find_repo_root


def canonical_hash(obj: Any) -> str:
    """稳定 JSON hash（sort_keys=True，UTF-8）。"""
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _ledger(store: Any, region: str, key: str) -> Any:
    try:
        return store.get_ledger(region, key)
    except Exception:
        return None


def priors_fingerprint(store: Any, region: str, wave: str) -> Optional[str]:
    """本波先验指纹；取不到返回 None（不猜、不伪造版本）。"""
    meta = _ledger(store, region, f"wave_meta_{wave}")
    if isinstance(meta, dict) and meta.get("priors_sha"):
        return str(meta["priors_sha"])
    for key in (f"priors_snapshot_{region}", f"priors_snapshot_{region.lower()}"):
        snap = _ledger(store, region, key)
        if isinstance(snap, dict) and snap:
            return canonical_hash(snap)
    return None


def _global_rules_path() -> str:
    return os.path.join(str(find_repo_root(__file__)), "Claude", "skills",
                        "wq-brain-campaign-toolkit", "config", "methodology_rules.json")


def rules_fingerprint(store: Any, region: str) -> Optional[str]:
    """区域规则 + 全局规则的 canonical hash；两者都取不到返回 None。"""
    region_rules: Any = None
    try:
        region_rules = store.get_methodology_rules(region)
    except Exception:
        region_rules = None
    global_rules: Any = None
    path = _global_rules_path()
    try:
        with open(path, encoding="utf-8-sig") as f:
            global_rules = json.load(f)
    except Exception:
        global_rules = None
    if region_rules is None and global_rules is None:
        return None
    return canonical_hash({
        "region": region_rules or {},
        "global": global_rules or {},
    })


def knowledge_version(priors_sha: Optional[str], rules_sha: Optional[str]) -> str:
    p = (priors_sha or "na")[:8]
    r = (rules_sha or "na")[:8]
    return f"{p}-{r}"
