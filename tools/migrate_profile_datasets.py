#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一次性迁移：14 个 region profile 的 datasets 块 → 精确化结构形态（2026-10-01）。

规则（证据驱动，忠实保留原文）：
  * red.datasets   = 旧 red 里的合法数据集 id ∪ ledger `*_dead` 键（数据集级判死的唯一无歧义来源）
  * green.datasets = 旧 green 里的合法数据集 id ∪ registry win 层 payload.dataset 绑定
  * 其余旧文本项   = `scope: family` 族级条目，原文原样保留（family 本来就该跨数据集）
  * 冲突裁决       = 同一数据集同时命中 green 证据与 ledger 判死 → 判死胜出（green 移除并留注记）
  * red_reason / green_note / 行尾注释 → 折叠进对应条目的 reason/note，信息不丢

用法：
  python tools/migrate_profile_datasets.py            # 只打印提案（dry-run）
  python tools/migrate_profile_datasets.py --apply    # 改写 14 个 profile（仓库权威目录）
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO = find_repo_root(__file__)
sys.path.insert(0, str(REPO / "src"))
PROFILE_DIR = REPO / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "regions"
DB = REPO / "data" / "wqb.db"


def _old_block(text: str) -> dict:
    """抓旧形态 datasets 块（inline 列表 + red_reason/green_note + green 行尾注释）。"""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    fm = m.group(1)
    out = {"red": [], "green": [], "yellow": [], "red_reason": "", "green_note": "", "green_comment": ""}
    dm = re.search(r"^datasets:\n((?:^[ \t].*(?:\n|$))*)", fm, re.M)
    if not dm:
        return out
    block = dm.group(1)

    def _lst(key):
        mm = re.search(rf"^[ \t]+{key}:\s*\[(.*?)\]\s*(#.*)?$", block, re.M)
        if not mm:
            return []
        items = [x.strip().strip("\"'") for x in mm.group(1).split(",") if x.strip()]
        return items

    out["red"], out["green"], out["yellow"] = _lst("red"), _lst("green"), _lst("yellow")
    gm = re.search(r"^[ \t]+green:\s*\[.*?\]\s*#(.*)$", block, re.M)
    if gm:
        out["green_comment"] = gm.group(1).strip()
    for key in ("red_reason", "green_note"):
        mm = re.search(rf"^[ \t]+{key}:\s*\"(.*?)\"", block, re.M)
        if mm:
            out[key] = mm.group(1).strip()
    return out


def _db_evidence():
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    win, dead, valid = {}, {}, {}
    for r in conn.execute("SELECT region, payload FROM registry_empirical WHERE layer='win'"):
        import json
        try:
            p = json.loads(r["payload"])
        except Exception:
            p = {}
        ds = p.get("dataset") or p.get("datasets")
        if isinstance(ds, str):
            ds = [ds]
        if isinstance(ds, list):
            win.setdefault(r["region"], set()).update(x for x in ds if isinstance(x, str))
    for r in conn.execute("SELECT region, key FROM ledger_kv WHERE key LIKE '%_dead'"):
        dead.setdefault(r["region"], set()).add(r["key"][:-5])
    for r in conn.execute("SELECT d.name AS ds, r.name AS reg FROM datasets d JOIN regions r ON d.region_id=r.id"):
        valid.setdefault(r["reg"], set()).add(r["ds"])
    conn.close()
    return win, dead, valid


def _is_id(item: str, valid: set) -> bool:
    return item.strip().lower() in valid


def propose(region: str, old: dict, win: set, dead: set, valid: set) -> str:
    """生成新 datasets 块文本。"""
    red_ids = sorted({x.strip() for x in old["red"] if _is_id(x, valid)})
    red_fams = [x for x in old["red"] if not _is_id(x, valid)]
    green_ids = sorted({x.strip() for x in old["green"] if _is_id(x, valid)})
    green_fams = [x for x in old["green"] if not _is_id(x, valid)]
    dead_new = sorted(set(dead) - set(red_ids))                    # 判死但旧 red 未收录
    win_new = sorted(set(win) - set(green_ids))                    # 胜绩但旧 green 未收录
    conflicts = sorted((set(green_ids) | set(win)) & set(dead))    # green 证据 ∩ 判死
    # 旧 red 文本 id 与 win 绑定撞车：保守留 red（人写的 red_reason 是显式判断），告警人工裁
    red_win_tension = sorted(set(red_ids) & set(win))
    red_all = sorted(set(red_ids) | set(dead))
    green_final = sorted((set(green_ids) | set(win)) - set(conflicts) - set(red_ids))

    L = ["datasets:", "  red:"]
    if red_all:
        reason = old["red_reason"] or "DB 实证判死"
        L.append(f"    - datasets: [{', '.join(red_all)}]")
        L.append(f'      reason: "{reason}（键 = ledger *_dead ∪ 旧 red 文本 id；明细查 get_dead_datasets）"')
    if red_fams:
        fams = ", ".join(red_fams)
        L.append("    - scope: family")
        L.append(f"      families: [{fams}]")
        if old["red_reason"]:
            L.append(f'      reason: "{old["red_reason"]}"')
    if not red_all and not red_fams:
        L[-1] = "  red: []"
    L.append("  green:")
    if green_final:
        L.append(f"    - datasets: [{', '.join(green_final)}]")
        L.append('      note: "旧 green 文本 id ∪ registry win 层实证绑定"')
    if green_fams:
        fams = ", ".join(green_fams)
        L.append("    - scope: family")
        L.append(f"      families: [{fams}]")
        L.append('      note: "族级方向（2026-10-01 迁移自旧文本形态；逐数据集绑定待实证补齐）"')
    if old["green_comment"]:
        L.append("    - scope: family")
        L.append(f'      families: ["{old["green_comment"]}"]')
        L.append('      note: "迁移自旧 green 行尾注释"')
    if old["green_note"]:
        L.append("    - scope: family")
        L.append(f'      families: ["{old["green_note"]}"]')
        L.append('      note: "迁移自旧 green_note"')
    if not green_final and not green_fams and not old["green_comment"] and not old["green_note"]:
        L[-1] = "  green: []"
    yl = ", ".join(old["yellow"])
    L.append(f"  yellow: [{yl}]")
    return "\n".join(L), {"red_ids": red_ids, "dead_new": dead_new, "win_new": win_new,
                          "conflicts": conflicts, "red_fams": red_fams, "green_fams": green_fams,
                          "red_win_tension": red_win_tension}


def _splice(text: str, new_block: str) -> str:
    """用新块替换旧 datasets 块（保持其余 front-matter 原样）。"""
    m = re.match(r"(---\n)(.*?)(\n---)", text, re.S)
    head, fm, tail = m.group(1), m.group(2), m.group(3)
    dm = re.search(r"^datasets:\n(?:^[ \t].*(?:\n|$))*", fm, re.M)
    assert dm, "datasets 块定位失败"
    fm2 = fm[: dm.start()] + new_block + "\n" + fm[dm.end():]
    return head + fm2 + tail + text[m.end():]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    win, dead, valid = _db_evidence()
    rc = 0
    for path in sorted(PROFILE_DIR.glob("*.md")):
        region = path.stem
        old = _old_block(path.read_text(encoding="utf-8"))
        block, info = propose(region, old, win.get(region, set()), dead.get(region, set()),
                              valid.get(region, set()))
        print(f"===== {region} =====")
        if info["conflicts"]:
            print(f"  ⚠ 冲突（判死胜出，从 green 移除）: {info['conflicts']}")
        if info["red_win_tension"]:
            print(f"  ⚠ red∩win 张力（保守留 red，请人工裁定）: {info['red_win_tension']}")
        if info["dead_new"]:
            print(f"  + red 补录判死: {info['dead_new']}")
        if info["win_new"]:
            print(f"  + green 补录胜绩: {info['win_new']}")
        print(block)
        if args.apply:
            path.write_text(_splice(path.read_text(encoding="utf-8"), block), encoding="utf-8")
            print("  → 已改写")
    return rc


if __name__ == "__main__":
    sys.exit(main())
