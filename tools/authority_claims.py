# -*- coding: utf-8 -*-
"""authority_claims.py — SKILL.md / INDEX.md 里「唯一权威 / 唯一事实源 / 唯一入口…」宣称的计数（棘轮基线维护）。

背景（skills 审查 X-2）：仅 SKILL.md + INDEX 里这类宣称就有 47 次，关于提交判定至少 10 处互相矛盾。
规则：「唯一…」宣称只在 `Claude/skills/GLOSSARY.md` 的登记表里登记（宣称 / 唯一实现 / 守护测试）；别处写「见 X」。
`tests/unit/07_docs_skills/test_glossary_docs.py` 用 `tests/fixtures/authority_claims_baseline.json` 做**只减不增**的棘轮：
新增一处宣称必红；删掉一处后必须 `--update-baseline` 把基线降下来。

  python tools/authority_claims.py                 # 列出各文件的宣称次数与相对基线的差异
  python tools/authority_claims.py --update-baseline
"""
import json
import re
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
SK = REPO / "Claude" / "skills"
BASELINE = REPO / "tests" / "fixtures" / "authority_claims_baseline.json"
CLAIM = re.compile(r"唯一(?:权威|事实源|基准|入口|正式写入方|真相源|标准依据|生产提交原语|实现)")
#: 登记处本身不计
EXEMPT = {"GLOSSARY.md"}


def _files():
    yield SK / "INDEX.md"
    for p in sorted(SK.glob("*/SKILL.md")):
        yield p


def count_claims():
    out = {}
    for p in _files():
        n = len(CLAIM.findall(p.read_text(encoding="utf-8", errors="ignore")))
        if n:
            out[p.relative_to(SK).as_posix()] = n
    return out


def load_baseline():
    return json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    cur, base = count_claims(), load_baseline()
    if "--update-baseline" in argv:
        BASELINE.write_text(json.dumps(cur, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"baseline written: {sum(cur.values())} claims / {len(cur)} files")
        return 0
    bad = 0
    for f in sorted(set(cur) | set(base)):
        c, b = cur.get(f, 0), base.get(f, 0)
        flag = "" if c == b else ("  ← 新增（登记到 GLOSSARY 或改成「见 X」）" if c > b else "  ← 已减少，请 --update-baseline")
        bad += c != b
        print(f"{c:3d} / 基线 {b:3d}  {f}{flag}")
    print(f"合计 {sum(cur.values())}（基线 {sum(base.values())}）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
