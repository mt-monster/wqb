# -*- coding: utf-8 -*-
"""守护 7 份 `methodology_rules.json` 的跨文件一致性（2026-10-05 建立）。

背景
----
AGENTS.md §3.5 定了「双轨同源」纪律：方法论知识**双轨存放**——
`Claude/skills/wq-brain-campaign-toolkit/config/methodology_rules.json`（全局，跨区共享）
+ `tracking/<REGION>/reference/methodology_rules.json`（区域专属）。

实测 7 份：全局 24 条规则，EUR/GBR/IND/KOR/MEA/USA 合计 20 条。
**这不是冗余副本，而是 1 全局 + 6 区域覆盖的有意分层**（全局那份的 `_note` 明写了这一点），
所以「收敛成一份」是错的——那会毁掉区域专属知识。

真正缺的是**机器约束**：目前没有任何测试保证这 7 份文件自身合法。手工维护 JSON 的现实是
——打错 id、写坏 JSON、区域规则与全局规则静默「打架」都不会有人发现，而 `RuleStore.load()`
会在运行期才炸（`rules.py:127-130` 按 `rule_id` 合并，区域覆盖全局）。

本测试守三条不变量（全部只读，用 tmp_path 沙箱，不动真库）：

1. **可解析 + 结构合法**：7 份都能解析、都有 `rules` 列表、每条有 `rule_id`。
2. **`rule_id` 全局唯一**：同一 `rule_id` 不得同时出现在**两个区域**。
   区域**覆盖**全局是设计内的合法用法（合并语义），故只检测区域之间的重叠。
3. **合并语义真如文档所述**：用真实 `RuleStore.load()` 验证区域确实覆盖全局，
   且未被覆盖的全局规则仍然保留。

⚠ 与既有 `test_methodology_rules_connectivity.py` 不重叠：那个守的是
「规则 → 代码注入点」的连通性（曾发现 23 条里只有 4 条真正生效）；
本文件守的是「文件之间」的结构与合并一致性。
"""
import importlib
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
GLOBAL_RULES = TOOLKIT_SCRIPTS.parent / "config" / "methodology_rules.json"
REGION_RULE_FILES = sorted((REPO_ROOT / "tracking").glob("*/reference/methodology_rules.json"))


def _read(p: Path) -> dict:
    # BOM: 实测部分文件带 UTF-8 BOM，用 utf-8 会抛 JSONDecodeError
    return json.loads(p.read_text(encoding="utf-8-sig"))


def _rule_ids(p: Path) -> list:
    return [r.get("rule_id") for r in _read(p).get("rules", []) if isinstance(r, dict)]


def _load_rules_mod():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    return importlib.import_module("_lib.rules")


# ---------------------------------------------------------------- 1. 结构合法

def test_every_rules_file_parses_and_has_rules_list():
    """7 份都能解析，且都有非空 rules 列表（防空文件 / 语法错误 / 结构漂移）。"""
    files = [GLOBAL_RULES, *REGION_RULE_FILES]
    assert len(REGION_RULE_FILES) >= 1, "没有任何区域规则文件，路径约定可能已变"

    bad = []
    for p in files:
        try:
            d = _read(p)
        except Exception as e:  # noqa: BLE001
            bad.append(f"{p.relative_to(REPO_ROOT)}: 解析失败 {e}")
            continue
        if not isinstance(d.get("rules"), list):
            bad.append(f"{p.relative_to(REPO_ROOT)}: 缺 rules 列表")
        elif not d["rules"]:
            bad.append(f"{p.relative_to(REPO_ROOT)}: rules 为空")
    assert not bad, "规则文件结构不合法:\n  " + "\n  ".join(bad)


def test_every_rule_has_an_id():
    """每条规则必须有 rule_id —— 它是合并的唯一键，缺了该规则永远不生效。"""
    orphans = []
    for p in [GLOBAL_RULES, *REGION_RULE_FILES]:
        for i, r in enumerate(_read(p).get("rules", [])):
            if not isinstance(r, dict) or not r.get("rule_id"):
                orphans.append(f"{p.relative_to(REPO_ROOT)}[index={i}]: {str(r)[:70]}")
    assert not orphans, "存在无 rule_id 的规则（永不生效）:\n  " + "\n  ".join(orphans)


# ---------------------------------------------------------------- 2. 跨文件唯一

def test_rule_ids_do_not_collide_across_regions():
    """同一 rule_id 不得出现在两个区域文件里。

    区域**覆盖**全局是设计内合法用法，但区域之间的重名会让「谁生效」取决于调用
    顺序 —— 无法排查，故禁止。
    """
    seen: dict = {}
    clashes = []
    for p in REGION_RULE_FILES:
        region = p.parents[1].name
        for rid in _rule_ids(p):
            if rid in seen and seen[rid] != region:
                clashes.append(f"{rid}: 同时在 {seen[rid]} 与 {region}")
            seen[rid] = region
    assert not clashes, "区域之间 rule_id 冲突:\n  " + "\n  ".join(clashes)


def test_global_rules_have_no_duplicate_ids():
    """全局文件内部也不得重复 id —— 重复会让 `load()` 的 dict 推导静默丢一条。"""
    ids = _rule_ids(GLOBAL_RULES)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    assert not dupes, f"全局规则文件内部 rule_id 重复（合并时会静默丢失）: {dupes}"
# ---------------------------------------------------------------- 3. 合并语义

def test_region_rules_override_global_for_same_id(tmp_path):
    """区域覆盖全局：同 rule_id 时区域版本胜出（`RuleStore.load()` 的文档语义）。

    同时断言未被覆盖的全局规则仍然保留——防「合并」退化成「只读区域」。
    """
    mod = _load_rules_mod()
    camp = tmp_path / "KOR"
    (camp / "reference").mkdir(parents=True)
    shared = "shared_rule_id_for_test"
    (camp / "reference" / "methodology_rules.json").write_text(
        json.dumps({"version": "test", "rules": [
            {"rule_id": shared, "type": "strategy", "action": {"op": "region_wins"}},
        ]}), encoding="utf-8")
    g = tmp_path / "global.json"
    g.write_text(json.dumps({"version": "test", "rules": [
        {"rule_id": shared, "type": "strategy", "action": {"op": "global_loses"}},
        {"rule_id": "global_only_id", "type": "strategy", "action": {"op": "keep"}},
    ]}), encoding="utf-8")

    store = mod.RuleStore(str(camp), global_path=str(g))
    assert not store._use_db(), "测试态不应走 DB 路径（会污染生产库）"
    by_id = {r["rule_id"]: r for r in store.load()["rules"]}

    assert by_id[shared]["action"]["op"] == "region_wins", "同 id 时区域未覆盖全局"
    assert "global_only_id" in by_id, "未被覆盖的全局规则丢失（合并退化成只读区域）"
    assert by_id["global_only_id"]["action"]["op"] == "keep"


def test_merge_keeps_both_sides(tmp_path):
    """反向负例：实现退化成「只返回区域规则」或「只返回全局规则」时都必须变红。"""
    mod = _load_rules_mod()
    camp = tmp_path / "EUR"
    (camp / "reference").mkdir(parents=True)
    (camp / "reference" / "methodology_rules.json").write_text(
        json.dumps({"version": "test", "rules": [
            {"rule_id": "r1", "type": "strategy", "action": {"op": "x"}},
        ]}), encoding="utf-8")
    g = tmp_path / "global.json"
    g.write_text(json.dumps({"version": "test", "rules": [
        {"rule_id": "g1", "type": "strategy", "action": {"op": "y"}},
    ]}), encoding="utf-8")

    ids = {r["rule_id"] for r in mod.RuleStore(str(camp), global_path=str(g)).load()["rules"]}
    assert {"r1", "g1"} <= ids, f"合并丢了规则，实际={ids}"