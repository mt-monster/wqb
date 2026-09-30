# -*- coding: utf-8 -*-
"""GLOSSARY.md（术语 / 状态词表 / 「唯一」宣称登记表）与提交链文档的守护（skills 审查 X-2 / X-4 / X-5 / X-7）。

守：登记表里的路径 / 符号 / 测试真实存在；代码里的枚举（verdict、退出码、检查名）都出现在词表里；
「唯一…」宣称只减不增；GLOSSARY 与提交链文档里的相对链接可达。
"""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SK = ROOT / "Claude" / "skills"
GLOSSARY = SK / "GLOSSARY.md"
CHAIN_DOCS = [SK / "worldquant-submit-alpha" / "references" / n
              for n in ("submit-chain.md", "quota-and-tower.md", "ppa-handoff.md", "scenarios.md", "fallback-rest.md")]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))


def _text(p):
    return p.read_text(encoding="utf-8")


def test_registry_rows_point_at_real_files_symbols_and_tests():
    text = _text(GLOSSARY)
    section = text.split("## 3. 「唯一」宣称登记表", 1)[1]
    rows = [ln for ln in section.splitlines() if ln.startswith("| ") and not ln.startswith("| ---") and "宣称" not in ln.split("|")[1]]
    assert len(rows) >= 15, "登记表行数异常"
    bad = []
    for ln in rows:
        for tok in re.findall(r"`([^`]+)`", ln):
            path, _, sym = tok.partition("::")
            if "/" not in path and not path.endswith((".py", ".json", ".md")):
                continue                                    # 符号名（GATE_REGISTRY 等）不当路径
            f = ROOT / path
            if not f.exists():
                bad.append(f"{tok}：文件不存在")
            elif sym and sym not in f.read_text(encoding="utf-8", errors="ignore"):
                bad.append(f"{tok}：文件里找不到符号")
    assert not bad, "登记表引用失真：\n  " + "\n  ".join(bad)


def test_every_qualified_symbol_in_glossary_exists():
    text = _text(GLOSSARY)
    bad = []
    for path, sym in re.findall(r"`([\w./-]+\.py)::(\w+)`", text):
        f = ROOT / path
        if not f.exists() or sym not in f.read_text(encoding="utf-8", errors="ignore"):
            bad.append(f"{path}::{sym}")
    assert not bad, bad


def test_code_enums_appear_in_the_glossary_vocabulary():
    from wqb.submit_verdict_core import EXIT_CODES, SUBMIT_HARD_GATE_WARNINGS, VERDICTS
    from wqb.wave_results_contract import VERDICT_OK
    from wqb.alpha_properties import COLORS
    t = _text(GLOSSARY)
    for v in VERDICTS:
        assert v in t, f"词表缺 submit_verdict 取值 {v}"
    for code in set(EXIT_CODES.values()) - {0}:
        assert f"{code}" in t
    for v in VERDICT_OK:
        assert v in t, f"词表缺波级 verdict {v}"
    for name in SUBMIT_HARD_GATE_WARNINGS:
        assert name in t, f"词表缺硬闸类 WARNING {name}"
    for c in COLORS:
        assert c in t, f"词表缺颜色 {c}"


def test_submit_chain_states_the_same_exit_codes_as_code():
    from wqb.submit_verdict_core import EXIT_CODES
    t = _text(SK / "worldquant-submit-alpha" / "references" / "submit-chain.md")
    for verdict, code in EXIT_CODES.items():
        row = next((ln for ln in t.splitlines() if ln.startswith(f"| `{verdict}`")), None)
        assert row is not None, f"提交链缺 {verdict} 一行"
        assert f"**{code}**" in row or f"| {code} |" in row, f"{verdict} 的退出码应为 {code}：{row}"


def test_wait_windows_in_docs_reference_config_keys_not_copies():
    from wqb.config import WAIT_THRESHOLDS
    docs = "\n".join(_text(p) for p in CHAIN_DOCS + [SK / "worldquant-submit-alpha" / "SKILL.md"])
    for key in ("submit_flip_wait_s", "submit_flip_poll_s", "submit_repost_max"):
        assert key in docs, f"提交链文档没有引用 WAIT_THRESHOLDS.{key}"
    # 文档里出现的窗口秒数必须和 config 一致（240 / 5）
    assert f"{WAIT_THRESHOLDS['submit_flip_wait_s']} s" in docs and "60 s" not in docs.replace("每 60 s", "")


def test_relative_links_in_new_docs_resolve():
    bad = []
    for f in [GLOSSARY, SK / "worldquant-submit-alpha" / "SKILL.md"] + CHAIN_DOCS:
        for m in re.finditer(r"\]\((?!https?://|#)([^)#\s]+)", _text(f)):
            target = (f.parent / m.group(1)).resolve()
            if not target.exists():
                bad.append(f"{f.relative_to(ROOT).as_posix()} → {m.group(1)}")
    assert not bad, "断链：\n  " + "\n  ".join(bad)


def test_authority_claims_only_decrease():
    import authority_claims as A
    cur, base = A.count_claims(), A.load_baseline()
    grew = {f: (base.get(f, 0), n) for f, n in cur.items() if n > base.get(f, 0)}
    shrank = {f: (n, base[f]) for f, n in ((f, cur.get(f, 0)) for f in base) if n < base[f]}
    assert not grew, f"新增了「唯一…」宣称（登记到 GLOSSARY 或改成「见 X」）：{grew}"
    assert not shrank, f"宣称已减少，请 python tools/authority_claims.py --update-baseline：{shrank}"


def test_glossary_is_linked_from_index():
    idx = _text(SK / "INDEX.md")
    assert "GLOSSARY.md" in idx, "INDEX.md 应指向 GLOSSARY.md"
