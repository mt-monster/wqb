# -*- coding: utf-8 -*-
"""ledger 键目录守护（skills 审查 X-1 / IX-20 / TR-17 / RA-129）。

目录 = docs/ledger_keys.json（人写）；扫描器 = tools/ledger_keys.py（从代码与文档抽取实际出现的键）。
守：代码里出现的键必须登记；文档里教的键必须登记；被读取的键必须有写入方（已知缺口显式登记 orphan 且必须仍为真）；
登记的代码引用必须真实存在；已废止的键只能出现在带「废止 / 历史」字样的行（现存违例进棘轮基线，只减不增）。
"""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import ledger_keys as LK  # noqa: E402

STATUSES = ("active", "legacy", "deprecated", "external")
ORPHAN_KINDS = ("read-without-writer", "promised-reader-missing")
WRITE_VERB = re.compile(r"写|追加|登记|留痕|upsert|ledger set|write|落", re.I)
MARK = re.compile(r"废止|已废|历史|deprecated|不再|旧键|legacy|勿用|已作废", re.I)

#: 文档里仍未带废止标记就教旧键的（文件, 键）——审查里点名要改的位置；改完必须从这里删（棘轮：只减不增）。
DEPRECATED_TEACHING_BASELINE = {
    ("Claude/skills/brain-dataset-mining-experience/SKILL.md", "s6_verdict_<wave>"),
}


@pytest.fixture(scope="module")
def entries():
    return LK.load_catalog()


@pytest.fixture(scope="module")
def recon():
    return LK.reconcile()


@pytest.fixture(scope="module")
def code_scan():
    return LK.scan_code()


# ----------------------------------------------------------------------------- 目录自身
def test_catalog_schema(entries):
    keys = [e["key"] for e in entries]
    assert len(keys) == len(set(keys)), "键重复"
    for e in entries:
        for f in ("key", "status", "purpose", "writers", "readers", "missing", "refresh"):
            assert f in e, f"{e.get('key')} 缺 {f}"
        assert e["status"] in STATUSES, e["key"]
        assert re.sub(r"<[^<>]*>", "", e["key"]).strip("_:") or LK.is_generic(e["key"]), e["key"]
        for side in ("writers", "readers"):
            for it in e[side]:
                assert it["kind"] in ("code", "agent"), (e["key"], it)
                assert it.get("ref"), (e["key"], it)
                if side == "readers":
                    assert it["kind"] == "code", f"{e['key']}：读取方只登记代码"
                if it["kind"] == "agent":
                    assert it.get("doc"), f"{e['key']}：agent 写入方必须指出教它写的文档"
        if "orphan" in e:
            o = e["orphan"]
            assert o["kind"] in ORPHAN_KINDS and o.get("tracked_by") and o.get("reason"), e["key"]


def test_generic_entries_cannot_swallow_coverage():
    assert LK.is_generic("<prefix>_<alpha_id>") and not LK.is_generic("s1_<ds>_d<delay>")
    assert LK.matches("<prefix>_<alpha_id>", "{prefix}_{alpha_id}")           # 只覆盖自己
    assert not LK.matches("<prefix>_<alpha_id>", "totally_unknown_key")       # 不覆盖别人
    assert LK.matches("s1_<ds>_d<delay>", "s1_{dataset_id}_d{delay}")
    assert LK.matches("<dataset>_dead", "{ds}_dead") and LK.matches("<dataset>_dead", "%_dead")
    assert not LK.matches("s0_whitelist", "s0_ranking")
    assert LK.norm_key("xr_probe_%s") == "xr_probe_<x>" and LK.norm_key("ckpt_w<W-1>") == "ckpt_w<x>"


def test_scanner_reads_the_real_call_shapes(code_scan):
    """扫描器必须抓得到几种典型写法，否则「代码键必须登记」这条守护就是空的。"""
    keys = code_scan["keys"]
    assert "s0_ranking" in keys and "wqb_db_mcp.py" in keys["region_rotation"]["write"]   # 字面量 + upsert_ledger_key(cur, key, …)
    assert "xr_probe_<x>" in keys                                                         # "xr_probe_%s" % tag
    assert "s2_compliance_w<x>" not in keys                                               # 变量键（f-string 先赋给变量）不在这里
    assert any(f.endswith("region_gates.py") for f in keys["s0_whitelist"]["read"])       # SQL key='…'
    assert "tools/update_operator_stats.py" in keys["region_kb"]["write"]                 # VALUES (?, 'region_kb', …)
    assert "tools/forum_recon.py" in keys["community_tpl_kb"]["write"]                    # VALUES ('KB','community_tpl_kb', …)
    assert "KB" not in keys, "VALUES 的第一个值是 region，不是键"


# ----------------------------------------------------------------------------- 对账
def test_every_key_used_in_code_is_cataloged(recon):
    assert not recon["uncovered_code"], (
        "代码里出现了目录没有的 ledger 键：\n  " + "\n  ".join(recon["uncovered_code"])
        + "\n→ 在 docs/ledger_keys.json 登记（用途 / 写入方 / 读取方 / 缺失行为 / 刷新责任）")


def test_every_key_taught_in_docs_is_cataloged(recon):
    assert not recon["uncovered_docs"], (
        "文档里教了目录没有的 ledger 键：\n  " + "\n  ".join(recon["uncovered_docs"]))


def test_read_keys_have_writers(recon):
    assert not recon["reads_no_writer"], (
        "有读取方却没有写入方（也没登记 orphan）：\n  " + "\n  ".join(recon["reads_no_writer"])
        + "\n→ 补写入方，或登记 orphan 并指向审查条目")


def test_orphans_are_still_true(entries, code_scan):
    for e in entries:
        o = e.get("orphan")
        if not o or o["kind"] != "read-without-writer":
            continue
        assert not e["writers"], f"{e['key']}：登记了 orphan 就不该再有写入方——缺口已补上？删掉 orphan 登记"
        found = [k for k, v in code_scan["keys"].items() if v["write"] and LK.matches(e["key"], k)]
        assert not found, f"{e['key']}：扫描发现了代码写入方 {found}——缺口已补上，请登记写入方并删除 orphan"


# ----------------------------------------------------------------------------- 引用真实
def _longest_literal(key):
    parts = [p for p in re.split(r"<[^<>]*>", key) if p.strip("_:")]
    return max(parts, key=len) if parts else ""


def test_code_refs_exist_and_mention_the_key(entries):
    bad = []
    for e in entries:
        lit = _longest_literal(e["key"])
        for side in ("writers", "readers"):
            for it in e[side]:
                f = ROOT / it["ref"] if it["kind"] == "code" else ROOT / it["doc"]
                if not f.is_file():
                    bad.append(f"{e['key']} {side}: 文件不存在 {f.relative_to(ROOT) if f.is_relative_to(ROOT) else f}")
                    continue
                text = f.read_text(encoding="utf-8", errors="ignore")
                if lit and lit not in text:
                    bad.append(f"{e['key']} {side}: {f.relative_to(ROOT).as_posix()} 里找不到 {lit!r}")
                if it["kind"] == "agent" and lit and not any(
                        lit in ln and WRITE_VERB.search(ln) for ln in text.splitlines()):
                    bad.append(f"{e['key']} {side}: {it['doc']} 没有一行同时提到该键和「写入」类动词——文档并没有教 agent 写它")
    assert not bad, "目录里的引用失真（文件改名 / 键改名 / 文档删了写法）：\n  " + "\n  ".join(bad)


# ----------------------------------------------------------------------------- 已废止的键
def _deprecated_regexes(entries):
    out = {}
    for e in entries:
        if e["status"] != "deprecated":
            continue
        parts = re.split(r"<[^<>]*>", e["key"])
        out[e["key"]] = re.compile(r"[A-Za-z0-9<>{}]{0,8}".join(re.escape(p) for p in parts))
    return out


def test_deprecated_keys_are_not_taught_without_a_mark(entries):
    regs = _deprecated_regexes(entries)
    offenders = set()
    for f in LK._doc_files():
        rel = f.relative_to(ROOT).as_posix()
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            for key, rx in regs.items():
                if rx.search(line) and not MARK.search(line):
                    offenders.add((rel, key))
    new = offenders - DEPRECATED_TEACHING_BASELINE
    fixed = DEPRECATED_TEACHING_BASELINE - offenders
    assert not new, f"文档在教已废止的 ledger 键（补「已废止」字样或改用替代）：{sorted(new)}"
    assert not fixed, f"已修复，请从 DEPRECATED_TEACHING_BASELINE 移除：{sorted(fixed)}"


# ----------------------------------------------------------------------------- 文档生成
def test_render_table_lists_every_key_and_orphans(entries):
    t = LK.render_table(entries)
    for e in entries:
        assert f"`{e['key']}`" in t
    assert "read-without-writer" in t and "**deprecated**" in t
