# -*- coding: utf-8 -*-
"""同步 GEM 引擎内嵌的 `brain-feature-implementation/SKILL.md` 到顶层权威版。

## 为什么需要它（2026-09-26 审计）

`brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-feature-implementation/SKILL.md`
会被 `run_pipeline.py` 读入并**拼进 LLM prompt**。它曾是 2026-08-22 的一份 49 行旧英文稿
（还引用不存在的 `manage_todo_list` 工具），而顶层权威版已演进到 111 行——
"同名不同文"在这里是有害的：一旦 skill 解析兜底到内嵌副本，就会把过时规范喂给模型。

该文件现已由 `tests/unit/test_gem_skill_paths.py::test_embedded_fi_copy_matches_authoritative`
机械守护。本工具是失败时的修复入口，也是**批量同步**入口。

## 用法

    python tools/sync_gem_embedded_skill.py --check   # 只校验（等价于测试的守卫，退出码 1 = 有漂移）
    python tools/sync_gem_embedded_skill.py --apply   # 从权威版覆盖内嵌副本

约定：**顶层是源，内嵌是派生物**；本工具只同步 SKILL.md，不动内嵌的 `scripts/`。
2026-09-29（skills 审查 FI-03 / EV）：两份 `scripts/` 目前逐字节相同，其中 `validator.py` 与
`alpha-expression-verifier` 的权威版一致——之前三份 validator 各自演化，GEM 与外部 idea 入库通道
用的是缺 hump / bucket / densify 修复的旧副本。此后由 `tests/unit/test_se_docs.py` 守护；
改 validator 时按其文件头「单一来源」一节四处一起覆盖。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "Claude" / "skills"
AUTHORITATIVE = SKILLS_DIR / "brain-feature-implementation" / "SKILL.md"
EMBEDDED = (SKILLS_DIR / "brain-make-some-gem" / "scripts" / "trailSomeAlphas"
            / "skills" / "brain-feature-implementation" / "SKILL.md")


def _read_normalized(path: Path) -> bytes:
    """读字节并归一换行（仓库 LF / 安装位 CRLF 的历史差异不算漂移）。"""
    return path.read_bytes().replace(b"\r\n", b"\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="同步 GEM 内嵌 FI SKILL.md")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="只校验，不写入（退出码 1 = 有漂移）")
    g.add_argument("--apply", action="store_true", help="从权威版覆盖内嵌副本")
    a = ap.parse_args(argv)

    if not AUTHORITATIVE.is_file():
        print(f"[ERROR] 权威版不存在：{AUTHORITATIVE}", file=sys.stderr)
        return 2
    if not EMBEDDED.is_file():
        print(f"[ERROR] 内嵌副本不存在：{EMBEDDED}", file=sys.stderr)
        return 2

    src = _read_normalized(AUTHORITATIVE)
    dst = _read_normalized(EMBEDDED)
    in_sync = src == dst

    print(f"权威版 : {AUTHORITATIVE.relative_to(REPO_ROOT)}  ({len(src.splitlines())} 行)")
    print(f"内嵌版 : {EMBEDDED.relative_to(REPO_ROOT)}  ({len(dst.splitlines())} 行)")

    if a.check:
        if in_sync:
            print("[OK] 内容一致（归一换行后逐字节相同）")
            return 0
        print("[DRIFT] 内嵌副本与权威版不一致——它会被喂进 LLM prompt，必须修。\n"
              "        修复：python tools/sync_gem_embedded_skill.py --apply", file=sys.stderr)
        return 1

    if in_sync:
        print("[OK] 已一致，无需写入")
        return 0
    EMBEDDED.write_bytes(src)
    print(f"[APPLIED] 已用权威版覆盖内嵌副本（写入 {len(src)} B，LF 换行）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
