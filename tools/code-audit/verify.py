# -*- coding: utf-8 -*-
"""verify.py — 主干健康的一键校验入口（2026-10-07 治理第二轮 P2-8）。

为什么存在
----------
治理第二轮复核时发现两件事：

1. 上一轮建议「补一条最小 CI：pytest + 三道闸」，但同时也记录着
   **本机 `make` 不存在**（Git Bash 环境无 make，Good）。若真按原建议写 `make verify`，
   得到的就是一个「写下来很漂亮、实跑越不过去」的目标——把纪律变成装饰。
   ⇒ 所以入口选 Python 脚本：`.venv` 里有解释器就能跑，Windows / Linux 同一条命令。

2. CI 缺位的真正代价不是"偶尔忘了跑"，而是**没有人能证明主干是绿的**。
   3112 个测试在第一次被跑之前，一直是未知态。本脚本把「证明」压缩成一条命令。

跑什么（顺序即严重度排序，先便宜后贵）
--------------------------------------
  1. tools/audit_structure.py                     结构契约 S1–S15（FAIL 阻断）
  2. code-audit/repo_governance_check.py --warn   未跟踪源码（**告警位，不阻断**）
  3. code-audit/doc_path_refs.py                  活文档死指针（棘轮）
  4. code-audit/audit_destructive_default.py      默认即破坏（棘轮）
  5. pytest tests/ -q                             验证路由

用法
----
    .venv/Scripts/python.exe tools/code-audit/verify.py          # 全跑
    .venv/Scripts/python.exe tools/code-audit/verify.py --fast   # 跳过 pytest
    .venv/Scripts/python.exe tools/code-audit/verify.py --json out.json

退出码：0 = 全绿（WARN 不算失败）；1 = 有一步 FAIL。
只读：本脚本不改仓库任何文件（--json 会把汇总写到给定路径，那是唯一的写）。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
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
REPO_ROOT = find_repo_root(__file__)
PY = sys.executable


def _run(name: str, argv: list[str], *, fatal: bool, root: Path) -> dict:
    t0 = time.time()
    proc = subprocess.run([PY, *argv], cwd=str(root),
                          capture_output=True, text=True, errors="replace")
    dur = time.time() - t0
    return {
        "step": name,
        "argv": argv,
        "rc": proc.returncode,
        "fatal": fatal,
        "seconds": round(dur, 2),
        "tail": (proc.stdout.strip().splitlines() or [""])[-1:],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="主干健康一键校验（闸 + 测试）")
    ap.add_argument("--fast", action="store_true", help="跳过 pytest（只要闸）")
    ap.add_argument("--json", metavar="PATH", help="把机器可读汇总写到该路径")
    args = ap.parse_args(argv)

    steps: list[dict] = []
    failures = 0

    def emit(name: str, argv: list[str], *, fatal: bool) -> None:
        nonlocal failures
        r = _run(name, argv, fatal=fatal, root=REPO_ROOT)
        steps.append(r)
        mark = "PASS" if r["rc"] == 0 else ("FAIL" if fatal else "NOTE")
        if r["rc"] != 0 and fatal:
            failures += 1
        line = r["tail"][0] if r["tail"] else ""
        print(f"  [{mark}] {name}  ({r['seconds']}s) {line}")

    print("[verify] 仓库 := %s" % REPO_ROOT)
    print("[verify] 解释器 := %s\n" % PY)
    print("[verify] === 守护闸 ===")

    emit("structure S1-S15", ["tools/audit_structure.py"], fatal=True)
    emit("gov untracked(warn)", ["tools/code-audit/repo_governance_check.py", "--warn"],
         fatal=False)
    emit("doc path refs", ["tools/code-audit/doc_path_refs.py"], fatal=True)
    emit("destructive default", ["tools/code-audit/audit_destructive_default.py"],
         fatal=True)

    if not args.fast:
        print("\n[verify] === 验证路由 ===")
        emit("pytest tests/", ["-m", "pytest", "tests/", "-q", "--no-header",
                               "-p", "no:cacheprovider"], fatal=True)

    print()
    if failures:
        print(f"[verify] ❌ FAIL：{failures} 步未通过。")
    else:
        print("[verify] ✅ 全部通过（NOTE 位是设计内的告警，不算失败）。")

    if args.json:
        Path(args.json).write_text(
            json.dumps({"repo": str(REPO_ROOT), "py": PY,
                        "steps": steps, "failures": failures},
                       ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        print(f"[verify] 汇总已写 {args.json}")

    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
