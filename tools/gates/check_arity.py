"""批量校验 alpha 表达式的算子元数 / 参数区间（零仿真成本）。

用法：
    python tools/check_arity.py --file exprs.txt      # 每行一条表达式
    python tools/check_arity.py "rank(close)" "ts_zscore(close, 252)"
    python tools/check_arity.py --file exprs.txt --json

退出码：0 = 全部通过；1 = 有失败项。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from wqb.expression.op_arity import check_expression  # noqa: E402


def load_expressions(args: argparse.Namespace) -> list[str]:
    exprs: list[str] = []
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
        exprs.extend(ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#"))
    exprs.extend(a.strip() for a in args.expressions if a.strip())
    return exprs


def main() -> int:
    ap = argparse.ArgumentParser(description="批量算子元数校验")
    ap.add_argument("expressions", nargs="*", help="表达式（可多条）")
    ap.add_argument("--file", help="表达式文件，每行一条")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    exprs = load_expressions(args)
    if not exprs:
        print("no expressions given", file=sys.stderr)
        return 2

    results = []
    for e in exprs:
        errs = check_expression(e)
        results.append({"expression": e, "ok": not errs, "errors": errs})

    failed = [r for r in results if not r["ok"]]
    if args.json:
        print(json.dumps({"total": len(results), "failed": len(failed), "results": results},
                         ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(("PASS :: " if r["ok"] else "FAIL :: ") + r["expression"])
            for x in r["errors"]:
                print("        " + str(x))
        print(f"--- total={len(results)} failed={len(failed)} " + ("all ok" if not failed else ""))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
