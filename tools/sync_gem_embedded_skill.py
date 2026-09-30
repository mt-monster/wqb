# -*- coding: utf-8 -*-
"""同步 GEM 引擎内嵌的两份 skill 副本到顶层权威版。

## 同步什么（约定：**顶层是源，内嵌是派生物**）

| 权威（`Claude/skills/…`） | 内嵌副本（`brain-make-some-gem/scripts/trailSomeAlphas/skills/…`） |
|---|---|
| `brain-feature-implementation/SKILL.md` | 同名 |
| `brain-data-feature-engineering/reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md` | 同名（2026-09-29 起纳入；此前 `reference.md` 已悄悄漂移到 399 行旧稿，Jaccard 0.82） |

`brain-data-feature-engineering` 的内嵌目录**故意不放 `SKILL.md`**——解析探针（`pipeline_paths._resolve_skill_dir`）
用它把内嵌目录排除掉；本工具不会、也不许创建它。

## 这些副本会不会被喂进 LLM prompt？

**不会**（2026-09-29 更正，旧文写反了）。`pipeline_prompts.build_prompt` 只用 dfe `SKILL.md`「是否非空」决定附不附一句
固定的 8 问提示，FI 那份完全不用（`tests/unit/07_docs_skills/test_se_docs.py` 钉死）。同步它们是为了**不让同名文件互相矛盾**——
2026-09-26 前内嵌 FI `SKILL.md` 是 2026-08-22 的 49 行旧英文稿（还引用不存在的 `manage_todo_list`），
一旦有人在兜底位读到它就会照旧稿操作。`scripts/` 里的 `ace_lib` / `validator` 才是运行时硬依赖，见下。

由 `tests/unit/03_gem/test_gem_skill_paths.py`（FI `SKILL.md` 与 dfe 三个文件逐字节一致）机械守护；本工具是失败时的修复入口。

## 用法

    python tools/sync_gem_embedded_skill.py --check   # 只校验（等价于测试的守卫，退出码 1 = 有漂移）
    python tools/sync_gem_embedded_skill.py --apply   # 从权威版覆盖内嵌副本

本工具只同步上表的文件，不动内嵌的 `scripts/`。2026-09-29（skills 审查 FI-03 / EV）：两份 `scripts/` 目前逐字节相同，
其中 `validator.py` 与 `alpha-expression-verifier` 的权威版一致——之前三份 validator 各自演化，GEM 与外部 idea 入库通道
用的是缺 hump / bucket / densify 修复的旧副本。此后由 `tests/unit/07_docs_skills/test_se_docs.py` 守护；
改 validator 时按其文件头「单一来源」一节四处一起覆盖。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "Claude" / "skills"
EMBEDDED_ROOT = (SKILLS_DIR / "brain-make-some-gem" / "scripts" / "trailSomeAlphas" / "skills")

#: 保持向后兼容：旧调用方 / 测试引用的两个常量
AUTHORITATIVE = SKILLS_DIR / "brain-feature-implementation" / "SKILL.md"
EMBEDDED = EMBEDDED_ROOT / "brain-feature-implementation" / "SKILL.md"

#: (skill 名, 文件名)——权威与内嵌同名同相对位置
SYNCED = (
    ("brain-feature-implementation", "SKILL.md"),
    ("brain-data-feature-engineering", "reference.md"),
    ("brain-data-feature-engineering", "examples.md"),
    ("brain-data-feature-engineering", "OUTPUT_TEMPLATE.md"),
)


def pairs() -> list[tuple[Path, Path]]:
    return [(SKILLS_DIR / skill / name, EMBEDDED_ROOT / skill / name) for skill, name in SYNCED]


def _read_normalized(path: Path) -> bytes:
    """读字节并归一换行（仓库 LF / 安装位 CRLF 的历史差异不算漂移）。"""
    return path.read_bytes().replace(b"\r\n", b"\n")


def drifted() -> list[tuple[Path, Path]]:
    """内容与权威不一致（或内嵌缺失）的 (权威, 内嵌) 对。"""
    out = []
    for auth, emb in pairs():
        if not emb.is_file() or _read_normalized(auth) != _read_normalized(emb):
            out.append((auth, emb))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="同步 GEM 内嵌的 FI SKILL.md 与 dfe 三个文件")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="只校验，不写入（退出码 1 = 有漂移）")
    g.add_argument("--apply", action="store_true", help="从权威版覆盖内嵌副本")
    a = ap.parse_args(argv)

    for auth, _ in pairs():
        if not auth.is_file():
            print(f"[ERROR] 权威版不存在：{auth}", file=sys.stderr)
            return 2

    bad = drifted()
    for auth, emb in pairs():
        state = "DRIFT" if (auth, emb) in bad else "ok"
        n_src = len(_read_normalized(auth).splitlines())
        n_dst = len(_read_normalized(emb).splitlines()) if emb.is_file() else 0
        print(f"[{state:5s}] {auth.relative_to(REPO_ROOT)} ({n_src} 行)  ↔  "
              f"{emb.relative_to(REPO_ROOT)} ({n_dst if emb.is_file() else '缺失'} 行)")

    if a.check:
        if not bad:
            print("[OK] 全部一致（归一换行后逐字节相同）")
            return 0
        print(f"[DRIFT] {len(bad)} 个内嵌副本与权威版不一致。\n"
              "        修复：python tools/sync_gem_embedded_skill.py --apply", file=sys.stderr)
        return 1

    if not bad:
        print("[OK] 已一致，无需写入")
        return 0
    for auth, emb in bad:
        emb.parent.mkdir(parents=True, exist_ok=True)
        data = _read_normalized(auth)
        emb.write_bytes(data)
        print(f"[APPLIED] {emb.relative_to(REPO_ROOT)}（写入 {len(data)} B，LF 换行）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
