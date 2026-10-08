# -*- coding: utf-8 -*-
"""治理闸的自证（2026-10-06 治理评审实施）。

覆盖三件「写了文档但流程不认」的老问题：

1. **未跟踪白名单 文档 ↔ 代码 对齐**：`docs/governance/untracked_allowlist.md` §1 自称
   「执行者 = `repo_governance_check.py`」，而那份前缀常量曾在 `= ()` 处声明后从未被使用
   （评审实锤）。本测试把两边的**集合相等**钉住，缺一边即红。
2. **抢救点裁决台账不过期**：台账正文是生成物，必须由 `snapshot_adjudicate.py --check`
   口径重算后逐字一致；否则「清单变了、文档还写着旧的」会伪装成「已裁决」。
   ⚠ 抢救点 ref（`preserve/*` tag、`wip/*` 分支）是本机产物、不入库，干净克隆里不存在
   —— 那种情况**跳过并写明原因**，不判失败（与根 conftest 的 `needs_*` 同口径）。
3. **两个死指针工具同口径**：`skill_lint` 与 `doc_path_refs` 自述「同口径」，但豁免词表
   与台账接线实测会飘（本轮就补齐了九个缺失词）。两边词表同集、台账读取都已接线。
4. **工具故障不得伪装成「无违规」**：裁决工具自身报错时必须把退出码抬到 2。
5. **活文档不得再宣称「从未存在」**：HEAD 曾把 `src/wqb/semantic_ledger.py` 判成
   「全仓从未落地」，而它在对象库里活得好好的（`git cat-file -s 4910e65:…` = 2407）。
   这类错句会把下一个 Agent 指挥成「放弃可取回的资产」，故机械钉住。
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]


def _load(rel: str, name: str):
    """按路径加载 tools/ 下的脚本为模块（它们不是包，只能这么引）。"""
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def rgc():
    sys.path.insert(0, str(REPO / "src"))
    return _load("tools/code-audit/repo_governance_check.py", "repo_governance_check")


@pytest.fixture(scope="module")
def sa():
    return _load("tools/code-audit/snapshot_adjudicate.py", "snapshot_adjudicate_mod")


# ---------------------------------------------------------------- 1. 白名单双轨对齐

ALLOWLIST_DOC = REPO / "docs" / "governance" / "untracked_allowlist.md"


def _doc_prefixes() -> set[str]:
    """§1 表首列反引号路径（`logs/`、`.claude/`、`.claude/`、`.codex/`、`.cline/` 等）。"""
    text = ALLOWLIST_DOC.read_text(encoding="utf-8")
    sec = text.split("## 1.", 1)[1].split("## 2.", 1)[0]
    out: set[str] = set()
    for line in sec.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("路径", "") or set(cells[0]) <= {"-"}:
            continue
        for tok in re.findall(r"`([^`]+)`", cells[0]):
            out.add(tok.strip("/ ") + "/")
    return out


def test_untracked_allowlist_doc_and_code_agree(rgc):
    """文档 §1 与代码常量必须**逐条同集**（谁也不许单飞）。"""
    assert ALLOWLIST_DOC.is_file(), "白名单文档消失，代码常量就成了无对账面的独裁表"
    doc = _doc_prefixes()
    code = {p.strip("/ ") + "/" for p in rgc.EXPECTED_UNTRACKED_PREFIXES}
    missing_in_code = sorted(doc - code)
    missing_in_doc = sorted(code - doc)
    assert not missing_in_code and not missing_in_doc, (
        "未跟踪白名单两边漂移（文档写了但流程不认 / 代码认了但文档没写）：\n"
        f"  代码缺：{missing_in_code}\n  文档缺：{missing_in_doc}\n"
        "修法：同一提交里改 `docs/governance/untracked_allowlist.md` §1 与 "
        "`repo_governance_check.py::EXPECTED_UNTRACKED_PREFIXES`。")


def test_allowlist_prefixes_are_actually_consumed(rgc):
    """常量必须**真被使用**（评审实锤：声明后从未接线，等于没写）。"""
    src = (REPO / "tools" / "code-audit" / "repo_governance_check.py").read_text(encoding="utf-8")
    body = src.split("EXPECTED_UNTRACKED_PREFIXES = (", 1)[-1]
    # 定义之外还要有引用点：`_in_allowlisted_prefix()` 里那一次
    uses = len(re.findall(r"EXPECTED_UNTRACKED_PREFIXES", src))
    assert uses >= 2, f"EXPECTED_UNTRACKED_PREFIXES 只有定义无消费（uses={uses}）"
    assert rgc._in_allowlisted_prefix("logs/a.py") is True
    assert rgc._in_allowlisted_prefix("src/wqb/x.py") is False
    assert body, "常量结构变了，本测试的取体逻辑需同步"


# ---------------------------------------------------------------- 2. 裁决台账不过期

SA = REPO / "tools" / "code-audit" / "snapshot_adjudicate.py"
ADJ_DOC = REPO / "docs" / "governance" / "snapshot_adjudication.md"


def _refs_present() -> bool:
    r = subprocess.run(["git", "tag", "-l", "preserve/*", "backup/*"],
                       cwd=str(REPO), capture_output=True, text=True)
    if r.returncode != 0 or r.stdout.strip():
        return True
    b = subprocess.run(["git", "branch", "--format=%(refname:short)"],
                       cwd=str(REPO), capture_output=True, text=True)
    return any(x.startswith("wip/") for x in b.stdout.splitlines())


@pytest.mark.skipif(not _refs_present(),
                    reason="抢救点 ref（preserve/* tag、wip/* 分支）是本机产物、不入库；"
                           "干净克隆下无对象可裁决 —— 跳过并写明原因，不是失败")
def test_snapshot_adjudication_doc_is_up_to_date():
    """台账正文 = 生成物，必须与当前对象库逐字一致（`--check` 的退出码口径）。"""
    assert SA.is_file(), "裁决生成器缺失：台账无法再校验，等于闸被拆了"
    r = subprocess.run([sys.executable, str(SA), "--check"],
                       cwd=str(REPO), capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, (
        "抢救点独有源码的裁决台账已过期（新增独有件无人裁决，或某件从快照消失）。\n"
        f"{r.stdout}\n{r.stderr}\n"
        "修法：在 tests/fixtures/snapshot_adjudication.json 里逐件写 verdict+basis，"
        "再跑 python tools/code-audit/snapshot_adjudicate.py --apply")


@pytest.mark.skipif(not _refs_present(),
                    reason="同上：无抢救点 ref 时无清单可核")
def test_dropped_verdicts_carry_evidence():
    """判「不回迁」必须带依据 —— 防止把「没人看过」固化成「已裁决」。"""
    import json

    fx = json.loads((REPO / "tests" / "fixtures" / "snapshot_adjudication.json")
                    .read_text(encoding="utf-8"))
    for path, v in (fx.get("verdicts") or {}).items():
        if v.get("verdict") in ("DROPPED", "RESTORED"):
            assert (v.get("basis") or "").strip(), f"{path} 判 {v.get('verdict')} 但没写依据"
            # 依据里必须含**可复核的记号**（命令 / 行号 / 日期），不接受「看起来没用」
            assert re.search(r"git |`|\d{4}-\d{2}-\d{2}|L\d+", v["basis"]), \
                f"{path} 的依据不可复核：{v['basis'][:60]}"


# ---------------------------------------------------------------- 3. 两个死指针工具同口径


def _alts(rx) -> set[str]:
    """把正则的备选支拆成集合（只取字面部，丢 `re.I` 这类尾巴）。"""
    return {a for a in rx.pattern.replace("(?i)", "").split("|") if a and "(" not in a and "?" not in a}


def test_dead_pointer_wordlists_agree():
    """`skill_lint` 与 `doc_path_refs` 自述「同口径」的豁免词表必须同集。

    2026-10-06 实测两边已飘：skill_lint 少「已下架/已废弃/已废止/未生成/丢失/已停用/旧稿」等，
    同一句文档在一个工具里豁免、在另一个里被判违规 —— 「两边各说一套」正是本仓反复出事的原因。
    """
    sl = _load("tools/skill_lint.py", "skill_lint_for_words")
    dpr = _load("tools/code-audit/doc_path_refs.py", "doc_path_refs_for_words")
    a, b = _alts(sl._NONEXIST), _alts(dpr.NONEXIST)
    assert a == b, (
        "死指针豁免词表漂移：\n"
        f"  只在 skill_lint：{sorted(a - b)}\n  只在 doc_path_refs：{sorted(b - a)}\n"
        "修法：两个正则同改（两边注释已写明必须同集）。")


def test_snapshot_ledger_exemption_is_wired():
    """台账豁免必须在**两个**工具里都真接上（只接一个就是下一轮假阳性的源头）。"""
    dpr = _load("tools/code-audit/doc_path_refs.py", "doc_path_refs_for_ledger")
    sl = _load("tools/skill_lint.py", "skill_lint_for_ledger")
    led = dpr.snapshot_only_paths()
    assert led, "台账里没有条目 —— 豁免面为空，本测试无法证明接线有效"
    assert led == sl._snapshot_only_paths(), "两个工具读到的台账集合不一致"
    dpr_src = (REPO / "tools" / "code-audit" / "doc_path_refs.py").read_text(encoding="utf-8")
    sl_src = (REPO / "tools" / "skill_lint.py").read_text(encoding="utf-8")
    assert "snapshot_only_paths()" in dpr_src, "doc_path_refs 的台账读取没被调用（只定义未接线）"
    assert "_snapshot_only_paths()" in sl_src, "skill_lint 的台账读取没被调用（只定义未接线）"


# ---------------------------------------------------------------- 4. 工具故障不得伪装成「无违规」


def test_adjudicate_tool_failure_is_loud():
    """`snapshot_adjudicate.py --check` 自身报错时必须退非 0，不能当成「台账没问题」。"""
    src = SA.read_text(encoding="utf-8")
    assert "sys.exit(2)" in src, "工具异常未映射到 rc=2（静默失败就是 fail-open）"
    assert "except Exception" in src, "没有兜底异常处理：脚本崩溃时退出码不可预期"


# ---------------------------------------------------------------- 6. 改名识别（止住幻影 PENDING）


def test_rename_is_adjudicated_as_not_lost(sa):
    """文件名按规范改过、内容没变的件不得再挂 PENDING。

    2026-10-08 实证：`tracking/2026-10-06_robustness.md` → `tracking/robustness_20261006.md`
    这类改名让快照里的旧名在 main「无同名件」⇒ 台账凭空多一条 PENDING。
    PENDING 的语义是「**没人看过**」，把「已改名入库」算进去就是台账自己制造的假象。
    """
    idx = {"robustness_20261006.md": [("tracking/robustness_20261006.md", "b1")]}
    v, basis = sa.rule_verdict("tracking/2026-10-06_robustness.md", "b1", idx)
    assert v == "DROPPED", f"改名被判 {v}（应为 DROPPED）：{basis}"
    assert "改名" in basis and "robustness_20261006.md" in basis


def test_rename_needs_identical_content(sa):
    """词干相同但**内容不同** = 真分叉，不许借「改名」之名判成件未丢失。"""
    idx = {"robustness_20261006.md": [("tracking/robustness_20261006.md", "other-blob")]}
    v, _basis = sa.rule_verdict("tracking/2026-10-06_robustness.md", "b1", idx)
    assert v == "PENDING", "内容不同却判了已处理 —— 分叉件会被静默丢掉"


def test_same_blob_with_unrelated_stem_is_not_a_rename(sa):
    """同 blob 但词干无关（空 `__init__.py` / 同模板头这类成片同内容件）不得冒充改名。

    不设这道闸，改名识别就会退化成「机器替人判不回迁」——那正是本台账明确不做的事。
    """
    idx = {"zzz.md": [("docs/zzz.md", "b1")]}
    v, _basis = sa.rule_verdict("tracking/2026-10-06_robustness.md", "b1", idx)
    assert v == "PENDING", "词干无关的同内容件被误认成改名"


# ---------------------------------------------------------------- 5. 活文档不许再说谎


def test_sop_does_not_claim_semantic_ledger_never_existed():
    """2026-10-06 实错的复发性守卫：`semantic_ledger` 被写成「从未落地 / 不存在」。

    它其实存在于抢救点 `4910e65`（2407 字节，含 `ledger_has_l35`）。裁决是「不回迁」，
    但**措辞必须是「只存在于抢救点」**——写「从未存在」会让下一个 Agent 放弃可取回的件。
    """
    f = REPO / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / \
        "signal-hypothesis-construction.md"
    text = f.read_text(encoding="utf-8")
    # 只拦**裸断言**：「从未存在」前面没有否定词就是错句；写成「并非从未存在」是对的。
    # （不这么区分就会退化成「禁止提这个事实」，而那正是本守卫要防的另一侧错误。）
    NEG = ("并", "不", "非", "未必要", "曾")
    for frag in ("从未落地", "从未存在", "也不存在"):
        for m in re.finditer(re.escape(frag), text):
            before = text[max(0, m.start() - 6):m.start()]
            assert any(n in before for n in NEG), (
                f"活文档又出现不可复核的裸断言「{frag}」（{f.name}，上下文：…{before}{frag}…）。\n"
                "正确措辞：「不在 main，但存在于抢救点 <ref>」 + 裁决台账链接。")
    # 反向要求：提到 semantic_ledger 就必须给出真实位置（抢救点），否则读者无从取件
    if "semantic_ledger" in text:
        assert "4910e65" in text or "snapshot_adjudication" in text, \
            "引用了 semantic_ledger 却没交代它在哪里 —— 读者只能白找"
