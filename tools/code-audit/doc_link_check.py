#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""活文档 markdown 链接死链闸（2026-11-19 新增）。

为什么需要它（`doc_path_refs.py` 的真空地带）：

`tools/code-audit/doc_path_refs.py` 只校验**反引号里的路径**与**带 `/` 且首段是仓库顶层目录**
的写法（见其 `collect()`：`if not t or "/" not in t: continue`）。于是两类东西它永远看不见：

  1. **markdown 链接** `](docs/experience/02_signal_patterns.md)` —— 渲染器按「链接所在文件」
     解析，skill 里这么写必然 404；
  2. **裸文件名** `](SKILL.md)` —— 同目录/跨目录都无从判断。

本闸按**两种解析口径**判定，任一成立即算活：
  (a) 相对**链接所在文件的目录**（渲染器语义）；
  (b) 相对**仓库根**（agent 语义）——仓库自己的约定，见
      `tests/unit/07_docs_skills/test_skill_integrity.py:186`
      「允许相对 skill 目录，或相对仓库根（skill 里常直接写 src/... docs/...）」。
两种口径都解析不到 ⇒ **死链**，登记进基线并 FAIL（棘轮：只拦新增）。

用法：
    python tools/code-audit/doc_link_check.py                 # 检查（新增死链 ⇒ exit 1）
    python tools/code-audit/doc_link_check.py --update-baseline  # 重写基线（确认合理时）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "code-audit"))
import doc_path_refs as _dpr  # noqa: E402

BASELINE = REPO / "tests" / "fixtures" / "doc_link_check_baseline.json"

MDLINK = re.compile(r"\]\(([^)\n]{1,300})\)")

#: 占位符形态：模板变量 / 通配 / 省略号 / 裸 `url` / 记忆片段 id（`memory/<hex>`）
PLACEHOLDER = re.compile(r"[\{\}<>*]|\.\.\.|^\$|\bTODO\b|^url$", re.I)
FRAGMENT_ID = re.compile(r"^[\w\-]+/[0-9a-f]{6,}$", re.I)


def _live_md_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=REPO, capture_output=True, text=True,
        encoding="utf-8").stdout
    files = [p.strip() for p in out.splitlines() if p.strip()]
    return sorted(f for f in files if _dpr.is_live(f))


def _targets(text: str) -> list[tuple[int, str]]:
    """返回 (行号, 链接目标) —— 跳过围栏代码块与有意提及的行。"""
    out = []
    for i, ln in enumerate(_dpr.strip_fences(text).split("\n"), start=1):
        if _dpr.NONEXIST.search(ln) or _dpr.EXEMPT_MARK in ln:
            continue
        for m in MDLINK.finditer(ln):
            raw = m.group(1).strip()
            if not raw:
                continue
            if "://" in raw or raw.startswith("#") or raw.startswith("mailto:"):
                continue
            tgt = raw.split("#", 1)[0].split("?", 1)[0].strip()
            if not tgt or PLACEHOLDER.search(tgt) or FRAGMENT_ID.match(tgt):
                continue
            out.append((i, tgt))
    return out


def resolves(fp: Path, target: str) -> bool:
    """两种口径任一成立即算活：

    (a) 相对**链接所在文件的目录**（渲染器语义）
    (b) 相对**仓库根**（agent 语义；仓库约定见
        `tests/unit/07_docs_skills/test_skill_integrity.py:186`
        「允许相对 skill 目录，或相对仓库根（skill 里常直接写 src/... docs/...）」）
    """
    return (fp.parent / target).exists() or (REPO / target).exists()


def scan() -> tuple[list[str], int, int]:
    broken: list[str] = []
    n_docs = n_links = 0
    for md in _live_md_files():
        fp = REPO / md
        if not fp.exists():
            continue
        n_docs += 1
        text = fp.read_text(encoding="utf-8", errors="replace")
        for line, tgt in _targets(text):
            n_links += 1
            if resolves(fp, tgt):
                continue
            broken.append(f"{md}:{line} → {tgt}")
    return sorted(broken), n_docs, n_links


def load_baseline() -> set[str]:
    if not BASELINE.exists():
        return set()
    return set(json.loads(BASELINE.read_text(encoding="utf-8")).get("violations", []))


def write_baseline(violations: list[str], n_docs: int, n_links: int) -> None:
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_doc": ("活文档 markdown 死链基线（棘轮）。只拦新增：修好一条请重跑 --update-baseline 收紧；"
                 "只在确认该死链合理时才手工放宽。"),
        "n_docs": n_docs,
        "n_links": n_links,
        "violations": violations,
    }
    tmp = BASELINE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, BASELINE)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="活文档 markdown 链接死链闸（棘轮）")
    ap.add_argument("--update-baseline", action="store_true", help="重写棘轮基线")
    args = ap.parse_args(argv)

    try:
        broken, n_docs, n_links = scan()
        baseline = load_baseline()
    except Exception as exc:  # pragma: no cover — 工具故障不得伪装成「无违规」
        print(f"[doc_link_check] 工具故障：{exc!r}（退出码 2 = 无法判定，不是「无死链」）",
              file=sys.stderr)
        return 2

    new_broken = sorted(set(broken) - baseline)
    stale = sorted(baseline - set(broken))

    print(f"[doc_link_check] 活文档 {n_docs} 篇 ｜ markdown 链接 {n_links} 条 ｜ "
          f"死链 {len(broken)}（基线 {len(baseline)}）")

    if args.update_baseline:
        write_baseline(broken, n_docs, n_links)
        print(f"[doc_link_check] 基线已写入 {BASELINE.relative_to(REPO)}（{len(broken)} 条）")
        return 0

    if new_broken:
        print(f"\n❌ 新增死链 {len(new_broken)} 条：")
        for b in new_broken:
            print(f"   [BROKEN ] {b}")
        print("修法：① 改成真实路径（相对所在目录，或仓库根相对——skill 里直写 docs/... 亦可）"
              " ② 恢复丢失文件 ③ 归档并写明「已归档」")
        return 1
    if stale:
        print(f"\nℹ 基线里已修复的 {len(stale)} 条（重跑 --update-baseline 可收紧）：")
        for s in stale:
            print(f"   [FIXED  ] {s}")
    print("\n✅ 无新增死链")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
