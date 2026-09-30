# -*- coding: utf-8 -*-
"""audit_skill_drift.py - skills 脚本副本漂移检测（2026-09-30 结构审计 P1-5）

为什么单独一个工具
------------------
`sync_skills.py` 管的是**仓库 → Agent 安装位**的单向同步；本工具管的是
**仓库内部 skill 之间**的内容漂移。两者职责不同，不混在一起。

现状（2026-09-30 审计）
-----------------------
`Claude/skills/` 下有 7 组内容逐字节相同的脚本副本。它们分两类，性质完全不同：

**A. GEM 内嵌快照（设计内，不算漂移）**
`brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-feature-implementation/`
是整棵 skill 的 vendored 快照，由 `tools/sync_gem_embedded_skill.py` 同步、
由 `tests/unit/03_gem/test_gem_skill_paths.py` 与 `test_se_docs.py` 守护。
`validator.py` 文件头「单一来源」一节明确要求改一处四处一起覆盖。
→ 这类**故意保留**，本工具不报。

**B. 跨 skill 复制（真漂移风险）**
同一份脚本被多个**平级** skill 各自 vendoring。改一处漏三处，历史已发生
（`validator.py` 曾三份各自演化，缺 hump / bucket / densify 修复）。
→ 这类要报。

本工具只做检测，不改文件布局。提取到 `_shared/` 属结构性变更，收益明确但
回归面大（要动 import 方式 + sync 工具 + 测试 + SKILL.md 契约），留待有
实际维护痛点时再做。

用法
----
    python tools/audit_skill_drift.py            # 人读的报告
    python tools/audit_skill_drift.py --json     # 机器读
    python tools/audit_skill_drift.py --check    # 只判退出码（有 B 类副本即 1）

退出码：0=无跨 skill 复制，1=存在（--check 用），2=工具故障
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "Claude" / "skills"

#: GEM 内嵌快照的路径标记——其下一层才是真正的 skill 名
EMBEDDED_ROOT = "trailSomeAlphas"

#: 不参与漂移检测的文件（包标记 / 缓存）
SKIP_NAMES = {"__init__.py"}


def _is_embedded(p: Path) -> bool:
    return EMBEDDED_ROOT in p.parts


def _skill_of(p: Path) -> str:
    """取该脚本所属的 skill 名（skills/<name>/...）。

    注意内嵌快照路径：
        skills/brain-make-some-gem/scripts/trailSomeAlphas/skills/<inner>/...
    这里 `<inner>` 才是真正的 owner（GEM 是宿主，内嵌的是被嵌进去的 skill）。
    直接取 rel.parts[0] 会错归给 brain-make-some-gem。
    """
    parts = p.relative_to(SKILLS).parts
    if EMBEDDED_ROOT in parts:
        i = parts.index(EMBEDDED_ROOT)
        # 形如 …/trailSomeAlphas/skills/<inner>/...，owner 在 EMBEDDED_ROOT 后第 2 段
        if i + 2 < len(parts):
            return parts[i + 2]
    return parts[0] if parts else "?"


def _md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def collect() -> dict[str, list[Path]]:
    """按内容哈希分组所有 skill 脚本（排除 __pycache__ / __init__.py）。"""
    by_hash: dict[str, list[Path]] = defaultdict(list)
    if not SKILLS.is_dir():
        return by_hash
    for p in sorted(SKILLS.rglob("*.py")):
        if "__pycache__" in p.parts or p.name in SKIP_NAMES:
            continue
        by_hash[_md5(p)].append(p)
    return {h: v for h, v in by_hash.items() if len(v) > 1}


def classify(groups: dict[str, list[Path]]) -> tuple[list[dict], list[dict]]:
    """把副本组分成 A（内嵌快照，设计内）与 B（跨 skill 复制，真风险）。

    判据：设该组涉及的所有 skill（含内嵌快照背后的 owner skill）。若这些
    skill 名字去重后**只剩一个**，说明是「同一 skill 的顶层版 + 其 GEM 内嵌
    快照」——设计内的单一来源复制，不报。否则涉及 ≥2 个平级 skill，属真漂移。
    """
    embedded: list[dict] = []
    cross: list[dict] = []
    for h, paths in groups.items():
        owners = sorted({_skill_of(p) for p in paths})
        entry = {
            "hash": h[:12],
            "name": paths[0].name,
            "bytes": paths[0].stat().st_size,
            "skills": owners,
            "paths": [p.relative_to(REPO_ROOT).as_posix() for p in paths],
        }
        if len(owners) <= 1:
            # 全部副本都在内嵌里 → A 类
            entry["kind"] = "A:内嵌快照(设计内)"
            embedded.append(entry)
        else:
            entry["kind"] = "B:跨skill复制"
            cross.append(entry)
    return embedded, cross


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="skills 脚本副本漂移检测（只读，不改布局）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--check", action="store_true",
                    help="静默：只判退出码（存在 B 类跨 skill 复制返回 1）")
    args = ap.parse_args(argv)

    if not SKILLS.is_dir():
        print(f"[audit_skill_drift] {SKILLS} 不存在", file=sys.stderr)
        return 2

    if args.check:
        # 静默模式：只返回退出码，供 audit_structure S6 转调（不刷屏）
        groups = collect()
        _embedded, cross = classify(groups)
        return 1 if cross else 0

    groups = collect()
    embedded, cross = classify(groups)

    if args.json:
        print(json.dumps(
            {"embedded": embedded, "cross_skill": cross}, ensure_ascii=False, indent=2))
        return 1 if cross else 0

    if not groups:
        print("[audit_skill_drift] 无重复副本。")
        return 0

    print(f"[audit_skill_drift] 共 {len(groups)} 组内容相同的脚本副本。\n")

    if cross:
        print("B 类 · 跨 skill 复制（改一处漏多处，历史已发生）：")
        for e in cross:
            print(f"  - {e['name']}  ({e['bytes']} bytes, {len(e['paths'])} 份)")
            print(f"    skills: {', '.join(e['skills'])}")
            for p in e["paths"]:
                print(f"      · {p}")
        print()

    if embedded:
        print("A 类 · GEM 内嵌快照（设计内保留，由 sync_gem_embedded_skill 同步）：")
        for e in embedded:
            print(f"  - {e['name']}  ({e['bytes']} bytes, {len(e['paths'])} 份)")
        print()

    print(f"[audit_skill_drift] B={len(cross)}  A={len(embedded)}"
          f"  → B 类是待治理项，A 类不报。")
    return 1 if cross else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
