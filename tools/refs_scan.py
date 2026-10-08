# -*- coding: utf-8 -*-
"""refs_scan.py - 文件级引用核验（只读，判「能不能归档」用）

为什么需要它
------------
归档/删除一个脚本前必须证明它 refs=0。AGENTS.md §8.5 记录了这个判断**连续踩过三个坑**：

1. **子串 grep 高估引用** —— `tools/pipeline_integration.py` 被 grep 命中，实际命中处是
   ledger key 字符串 `pipeline_integration_{dataset}`，不是 import；
2. **dotted token 漏判** —— `from wqb.research.selection_contract import …` 若不按 `.`/`/`
   切分索引，会把真实引用判成零引用（首跑就这样误判过 `selection_contract.py`）；
3. **路径快照假命中** —— `output_report/py_complexity_scan.json`、`tracking/MANIFEST.json`
   这类文件把**全仓路径列表**写进正文，任何文件都能在里面"被引用"。

本工具把这三条教训固化成默认行为：token 级匹配（同时索引点号、正斜杠、反斜杠
切分后的各段）、默认排除路径快照类文件、报告命中处所在文件（供人工判别 import 还是 CLI 字符串），
并在 `refs=0` 后标注该文件有没有 `__main__`（区分「库模块」与「未登记 CLI」）。

用法
----
    python tools/refs_scan.py --dir tracking/reference              # 目录内每个 .py 的引用数
    python tools/refs_scan.py --names gate,wave_gate --show-hits    # 指定名字并打命中文件
    python tools/refs_scan.py --dir tools --only-zero --out cache/refs.json

退出码：0 = 正常出报告（**不代表零引用**）；2 = 工具故障。
只读：不删不改任何文件。判归档仍需人工看命中形态（见 §8.5 与 tools/legacy/README.md）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict


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
REPO_ROOT = find_repo_root(__file__)

#: 扫语料时跳过的目录（attic/cache/logs 属归档与运行产物，不参与"活引用"判定）
SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", "attic", "cache",
    "logs", "research-data", "extensions", ".pytest_cache", ".claude", ".workbuddy",
    ".qoder-cn", ".cursor", ".codex", ".cline", ".agents", ".trae-cn", ".box-agent",
    ".box-agent-scratch", ".kimi-code", "site-packages", "downloads",
}

#: 参与投票的文本类型（只扫代码/文档/配置，不扫二进制与产物）
TEXT_EXT = {".py", ".md", ".json", ".sh", ".toml", ".ini", ".ps1", ".bat",
            ".txt", ".yml", ".yaml"}

#: 教训 3：把全仓路径写进正文的快照类文件，命中即假阳性，默认排除
PATH_DUMP_FILES = {
    "py_complexity_scan.json", "MANIFEST.json", "audit_structure_baseline.json",
    "test_groups.json", "time_bombs.json", "env_registry.json", "ledger_keys.json",
}

MAX_FILE_BYTES = 3_000_000
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
SPLIT_RE = re.compile(r"[./\\]")


def iter_text_files(extra_skip: set, exclude_dirs: set):
    """extra_skip = 按单段目录名排除；exclude_dirs = 按绝对目录排除（候选自身所在层，
    否则同目录互引与自引用会假投票）。"""
    skip = SKIP_DIRS | extra_skip
    for p in REPO_ROOT.rglob("*"):
        if not p.is_file() or any(part in skip for part in p.parts):
            continue
        if p.parent in exclude_dirs:
            continue
        if p.suffix.lower() not in TEXT_EXT or p.name in PATH_DUMP_FILES:
            continue
        try:
            if p.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        yield p


def tokenize(text: str) -> set:
    """整词 + 按点号 / 正斜杠 / 反斜杠切分后的各段（教训 2）。"""
    out = set(WORD_RE.findall(text))
    for seg in SPLIT_RE.split(text):
        seg = seg.strip("\"\u0060' ,:;()[]{}")
        if seg and len(seg) > 1:
            out.add(seg)
    return out


def build_index(corpus: list, quiet: bool) -> dict:
    index: dict[str, list[str]] = defaultdict(list)
    unreadable = 0
    for p in corpus:
        try:
            toks = tokenize(p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            unreadable += 1
            continue
        rel = p.relative_to(REPO_ROOT).as_posix()
        for t in toks:
            index[t].append(rel)
    if unreadable and not quiet:
        print(f"[warn] {unreadable} 个语料文件读不了，已跳过", file=sys.stderr)
    return index


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="文件级引用核验（只读）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dir", help="扫描该目录下的每个 .py（相对仓库根或绝对路径）")
    g.add_argument("--names", help="逗号分隔的 basename/文件名清单，如 gate.py,wave_gate")
    ap.add_argument("--ext", default=".py", help="候选扩展名过滤（默认 .py；传 all 不过滤）")
    ap.add_argument("--show-hits", action="store_true", help="打印命中所在文件（人工判别用）")
    ap.add_argument("--only-zero", action="store_true", help="只输出 refs=0 的候选")
    ap.add_argument("--extra-skip", default="", help="额外跳过的顶层目录名，逗号分隔")
    ap.add_argument("--out", help="把结果写成 JSON（相对仓库根）")
    ap.add_argument("-q", "--quiet", action="store_true")
    a = ap.parse_args(argv)

    extra_skip = {s.strip() for s in a.extra_skip.split(",") if s.strip()}
    exclude_dirs: set = set()

    if a.dir:
        target = (REPO_ROOT / a.dir) if not Path(a.dir).is_absolute() else Path(a.dir)
        if not target.is_dir():
            print(f"[error] 目录不存在：{target}", file=sys.stderr)
            return 2
        cands = sorted(p for p in target.iterdir() if p.is_file())
        if a.ext != "all":
            cands = [p for p in cands if p.suffix.lower() == a.ext.lower()]
        exclude_dirs.add(target.resolve())      # 候选层不投票（包含同目录互引）
    else:
        cands = []
        for raw in a.names.split(","):
            raw = raw.strip()
            if not raw:
                continue
            name = raw if "." in raw else f"{raw}.py"
            found = list(REPO_ROOT.rglob(name))
            if not found:
                print(f"[warn] 找不到候选：{name}", file=sys.stderr)
            cands.extend(found)
        cands = sorted(set(cands))
        # --names 模式只排除候选自身（下面 `h != rel` 负责），不能排整个同层 ——
        # 同层工具互调是**真引用**，排掉会把它们误判成 refs=0。

    corpus = list(iter_text_files(extra_skip, exclude_dirs))
    if not a.quiet:
        print(f"[refs_scan] 语料 {len(corpus)} 文件｜候选 {len(cands)} 个"
              f"（已排除路径快照 {len(PATH_DUMP_FILES)} 类文件名）")
    index = build_index(corpus, a.quiet)

    rows = []
    for c in cands:
        try:
            has_main = "if __name__" in c.read_text(encoding="utf-8", errors="replace")
        except OSError:
            has_main = None
        rel = c.relative_to(REPO_ROOT).as_posix()
        hits = sorted({h for h in index.get(c.stem, []) + index.get(c.name, [])
                       if h != rel})
        rows.append({"candidate": rel, "refs": len(hits), "has_main": has_main,
                     "hits": hits if a.show_hits else hits[:5]})

    zero = [r for r in rows if r["refs"] == 0]
    out_rows = zero if a.only_zero else rows
    for r in out_rows:
        flag = "REFS=0 " if r["refs"] == 0 else f"refs={r['refs']:<3}"
        print(f"  {flag} __main__={r['has_main']}  {r['candidate']}")
        if a.show_hits and r["hits"]:
            for h in r["hits"]:
                print(f"            ← {h}")

    print(f"\n[refs_scan] 候选 {len(rows)}｜refs=0 {len(zero)}｜"
          f"有引用 {len(rows) - len(zero)}")
    print("  ⚠ refs=0 只是**必要条件**：删除前仍需人工看命中形态 + "
          "确认无动态调用/注册式引用（AGENTS.md §8.5、tools/legacy/README.md）")
    if a.out:
        dest = REPO_ROOT / a.out if not Path(a.out).is_absolute() else Path(a.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[refs_scan] JSON → {dest.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
