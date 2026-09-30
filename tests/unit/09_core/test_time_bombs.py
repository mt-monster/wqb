# -*- coding: utf-8 -*-
"""时间炸弹登记表（docs/time_bombs.json）守护（skills 审查 X-19 / RA-124）。

三条：
1. 登记项自身有效：字段齐、证据文件 / 需要字样真实存在、code/auto 项引用的测试真实存在；
2. 人工项（manual）过期未办完 = 红（给一天宽限）；
3. 文档里出现的**严格未来日期**必须在登记表里（date 或 mentions）——新写「到某日会怎样」的文案，
   必须先登记，否则这条红。今天及以前的日期是变更记录，不受限。
"""
import ast
import datetime as dt
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
REG = ROOT / "docs" / "time_bombs.json"
SK = ROOT / "Claude" / "skills"

#: 语料 / 嵌套技能库：不是本仓库自己的规则文本
SKIP_PREFIX = ("brain-alpha-judge/data/forum_corpus/", "brain-make-some-gem/scripts/trailSomeAlphas/skills/")

_FULL = re.compile(r"(?<![\d-])(20\d{2})-(\d{2})-(\d{2})(?![\d-])")
#: 「至/到/截止/直到 MM-DD」这种省略年份的到期写法（按今年算）
_SHORT = re.compile(r"(?:至|到|截止|直到)\s*(\d{2})-(\d{2})(?![\d-])")

KINDS = ("code", "auto", "manual")


def _load():
    return json.loads(REG.read_text(encoding="utf-8"))["entries"]


def _today():
    return dt.date.today()


def _d(s):
    return dt.date.fromisoformat(s)


def _test_exists(nodeid):
    path, _, name = nodeid.partition("::")
    f = ROOT / path
    if not f.is_file() or not name:
        return False
    tree = ast.parse(f.read_text(encoding="utf-8"))
    return any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name
               for n in ast.walk(tree))


def test_registry_entries_are_well_formed_and_evidence_exists():
    entries = _load()
    assert entries, "登记表为空"
    ids = [e["id"] for e in entries]
    assert len(ids) == len(set(ids)), "id 重复"
    for e in entries:
        for k in ("id", "date", "what", "where", "resolution"):
            assert e.get(k), f"{e.get('id')} 缺 {k}"
        _d(e["date"])
        for m in e.get("mentions", []):
            _d(m)
        res = e["resolution"]
        assert res["kind"] in KINDS, (e["id"], res["kind"])
        if res["kind"] in ("code", "auto"):
            assert res.get("mechanism"), f"{e['id']} 缺 mechanism"
            assert _test_exists(res.get("test", "")), f"{e['id']} 引用的测试不存在：{res.get('test')}"
        else:
            assert res.get("owner"), f"{e['id']} manual 项必须有 owner"
            assert res.get("status") in ("pending", "done"), e["id"]
        for w in e["where"]:
            if w.startswith("ledger:"):
                continue
            path, _, needle = w.partition("::")
            f = ROOT / path
            assert f.is_file(), f"{e['id']} where 指向不存在的文件：{path}"
            if needle:
                assert needle in f.read_text(encoding="utf-8"), f"{e['id']}：{path} 里找不到 {needle!r}"


def test_manual_entries_are_not_overdue():
    today = _today()
    overdue = [e["id"] for e in _load()
               if e["resolution"]["kind"] == "manual" and e["resolution"].get("status") != "done"
               and _d(e["date"]) < today]
    assert not overdue, f"人工项已过期未办完：{overdue}（办完把 resolution.status 改 done，或改期并说明）"


def _doc_files():
    files = [ROOT / "AGENTS.md", ROOT / "CLAUDE.md", ROOT / "README.md", SK / "INDEX.md"]
    for p in sorted(SK.rglob("*.md")):
        rel = p.relative_to(SK).as_posix()
        if any(rel.startswith(x) for x in SKIP_PREFIX):
            continue
        files.append(p)
    return [f for f in dict.fromkeys(files) if f.is_file()]


def _future_dates(text, today):
    """文本里的严格未来日期 → [(date, snippet)]。"""
    found = []
    for m in _FULL.finditer(text):
        try:
            d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            continue
        if d > today:
            found.append((d, text[max(0, m.start() - 12): m.end() + 12].replace("\n", " ")))
    for m in _SHORT.finditer(text):
        try:
            d = dt.date(today.year, int(m.group(1)), int(m.group(2)))
        except ValueError:
            continue
        if d > today:
            found.append((d, text[max(0, m.start() - 12): m.end() + 12].replace("\n", " ")))
    return found


def test_future_dated_doc_text_is_registered():
    today = _today()
    registered = set()
    for e in _load():
        registered.add(_d(e["date"]))
        registered.update(_d(x) for x in e.get("mentions", []))
    bad = []
    for f in _doc_files():
        for d, snip in _future_dates(f.read_text(encoding="utf-8", errors="ignore"), today):
            if d not in registered:
                bad.append(f"{f.relative_to(ROOT).as_posix()}: {d} …{snip}…")
    assert not bad, ("文档里出现了未登记的未来日期（先在 docs/time_bombs.json 登记，再写文案）：\n  "
                     + "\n  ".join(bad[:20]))


def test_scanner_finds_full_and_short_forms_and_ignores_past():
    today = dt.date(2026, 9, 29)
    assert [d for d, _ in _future_dates("2026-10-12 起 enforce", today)] == [dt.date(2026, 10, 12)]
    assert [d for d, _ in _future_dates("停止规则放行至 10-05", today)] == [dt.date(2026, 10, 5)]
    assert _future_dates("2026-09-29 整改；灰度自 2026-09-17 起；range 10-49、11-16", today) == []
    assert _future_dates("12 版本 2026-13-45", today) == []          # 非法日期不炸


def test_every_time_dependent_constant_in_code_is_registered():
    """代码里的日期常量（date(2026, …)）若晚于今天，必须在登记表 —— 抓「改了常量忘了登记」。"""
    today = _today()
    registered = set()
    for e in _load():
        registered.add(_d(e["date"]))
        registered.update(_d(x) for x in e.get("mentions", []))
    pat = re.compile(r"(?:datetime\.)?date\((20\d{2}),\s*(\d{1,2}),\s*(\d{1,2})\)")
    roots = [ROOT / "src", ROOT / "tools", SK]
    bad = []
    for base in roots:
        for p in base.rglob("*.py"):
            rel = p.relative_to(ROOT).as_posix()
            if "/tests/" in rel or ".venv" in rel or any(x in rel for x in SKIP_PREFIX):
                continue
            for m in pat.finditer(p.read_text(encoding="utf-8", errors="ignore")):
                d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                if d > today and d not in registered:
                    bad.append(f"{rel}: {d}")
    assert not bad, "代码里有未登记的未来日期常量：\n  " + "\n  ".join(bad)
