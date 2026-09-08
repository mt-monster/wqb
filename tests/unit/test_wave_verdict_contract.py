# -*- coding: utf-8 -*-
"""wave_results.verdict 契约回归（2026-09-08 新增）。

背景：`_lib/wave_results.py` 同一个文件里两套契约打架——

  - `upsert()` 硬约束 verdict ∈ {PASS, FAIL, PARTIAL}，违约 `raise SystemExit`
  - `auto_upsert_from_review()` 自动生成 "GREEN: 5 候选达标" 式描述性文字

而 `SystemExit` 不继承 `Exception`，`pipeline.py:stage_review` 那句
`except Exception as e: print("...（不阻断）")` 根本抓不到。实测后果：CHN
chn_w2_other545_ppa 波回测 5/5 成功落库后，pipeline 当场退出，
`[review]`/`[ledger]`/`[done]` 一行不打，review checkpoint 也不落。

本文件把三件事做成回归：
  1. 三个分支生成的 verdict 都是枚举值，描述性文字降到 key_findings 首条
  2. 两个调用方（pipeline.py / review_wave.py）的 except 真能挡住 SystemExit
  3. 仓库副本与 ~/.claude 安装副本不漂移（改一份忘另一份 = 运行时仍是旧行为）
"""
from __future__ import annotations

import ast
import importlib
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLKIT_REL = Path("wq-brain-campaign-toolkit") / "scripts"
CALLERS = ("pipeline.py", "review_wave.py")
#: 本次契约涉及的文件；两份副本必须逐字一致（行尾除外）
SYNCED_FILES = ("_lib/wave_results.py",) + CALLERS


def _toolkit_scripts_dirs():
    """运行时那份 toolkit scripts + 仓库副本（两者可能重合，去重）。

    运行时那份走 `wqb.workflow._common.resolve_toolkit_dir()` —— 与 campaign /
    gem 节点定位 toolkit 是同一个入口，返回的就是首个命中根（本机 = ~/.claude），
    也就是 Agent 真正加载的那份。历史 Agent 安装位（~/.workbuddy 等）排在它后面，
    只要 ~/.claude 在场就永远轮不到，故不纳入同步范围。
    """
    cands = []
    try:
        from wqb.workflow._common import resolve_toolkit_dir
        runtime = resolve_toolkit_dir()
        if runtime:
            cands.append(Path(runtime))
    except Exception:  # pragma: no cover - 解析失败回落仓库副本
        pass
    cands.append(REPO_ROOT / "Claude" / "skills" / TOOLKIT_REL)

    seen, out = set(), []
    for c in cands:
        if not (c / "_lib" / "wave_results.py").is_file():
            continue
        key = c.resolve()
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


SCRIPTS_DIRS = _toolkit_scripts_dirs()


@pytest.fixture(scope="module")
def wave_results_mod():
    """加载运行时那一份 `_lib.wave_results`（相对 import 要求按包加载）。"""
    if not SCRIPTS_DIRS:
        pytest.skip("wq-brain-campaign-toolkit 未安装且仓库副本缺失")
    d = str(SCRIPTS_DIRS[0])
    if d not in sys.path:
        sys.path.insert(0, d)
    for m in ("_lib.wave_results", "_lib.ledger", "_lib.common", "_lib"):
        sys.modules.pop(m, None)
    return importlib.import_module("_lib.wave_results")


def _fake_rows(n):
    return [{"id": f"a{i}", "sharpe": 1.4 + i * 0.01, "fitness": 1.1,
             "two_year_sharpe": 1.2} for i in range(n)]


# ---------------- 1. verdict 三态 ----------------

@pytest.mark.parametrize("n_cand,n_near,verdict,note_prefix", [
    (2, 0, "PASS", "GREEN:"),
    (0, 3, "PARTIAL", "YELLOW:"),
    (0, 0, "FAIL", "RED:"),
])
def test_auto_upsert_writes_enum_verdict(wave_results_mod, tmp_path,
                                         n_cand, n_near, verdict, note_prefix):
    """三个分支都写枚举值，原描述性文字进 key_findings 首条（一个字不丢）。"""
    store = wave_results_mod.WaveResultsStore("TST", db_path=str(tmp_path / "t.db"))
    rows = _fake_rows(5)
    near = [{"id": f"n{i}", "sharpe": 1.0, "walls": ["SHARPE"]} for i in range(n_near)]

    out = store.auto_upsert_from_review(
        "chn_w2_other545_ppa", rows, rows[:n_cand], near,
        settings={"dataset": "other545", "universe": "TOP2000U",
                  "neutralization": "SUBINDUSTRY", "delay": 1, "decay": 4},
        multisim_ids=["ms_x"],
    )
    assert not out.get("skipped"), out

    got = store.get(out["wave_number"])
    assert got["verdict"] == verdict
    findings = json.loads(got["key_findings"])
    assert findings and findings[0].startswith(note_prefix), findings


def test_auto_upsert_does_not_kill_process(wave_results_mod, tmp_path):
    """回归本体：auto_upsert_from_review 不得抛 SystemExit（会当场杀死 pipeline）。"""
    store = wave_results_mod.WaveResultsStore("TST", db_path=str(tmp_path / "t.db"))
    try:
        store.auto_upsert_from_review("chn_w2_other545_ppa", _fake_rows(5), [], [])
    except SystemExit as e:  # pragma: no cover - 修复前必现
        pytest.fail(f"auto_upsert_from_review 抛 SystemExit，会杀死整条 pipeline: {e}")


def test_upsert_still_rejects_descriptive_verdict(wave_results_mod, tmp_path):
    """upsert 的三态硬闸保持不变——修的是生成侧，不是把闸拆了。"""
    store = wave_results_mod.WaveResultsStore("TST", db_path=str(tmp_path / "t.db"))
    with pytest.raises(SystemExit):
        store.upsert(1, verdict="RED: 5 全灭", status="closed")


# ---------------- 2. 调用方真能"不阻断" ----------------

def _catches_systemexit(handler: ast.ExceptHandler) -> bool:
    t = handler.type
    if t is None:  # 裸 except
        return True
    elts = t.elts if isinstance(t, ast.Tuple) else [t]
    names = {e.id for e in elts if isinstance(e, ast.Name)}
    return bool(names & {"SystemExit", "BaseException"})


@pytest.mark.parametrize("script", CALLERS)
def test_callers_catch_systemexit(script):
    """包住 auto_upsert_from_review 的 try 必须挡得住 SystemExit。

    只写 `except Exception` 时注释里的"不阻断"是假的：_lib/wave_results 的
    契约校验（wave_number / status / verdict）用的全是 raise SystemExit。
    """
    if not SCRIPTS_DIRS:
        pytest.skip("wq-brain-campaign-toolkit 未安装且仓库副本缺失")
    for d in SCRIPTS_DIRS:
        path = d / script
        tree = ast.parse(path.read_text(encoding="utf-8"))
        tries = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.Try) and any(
                isinstance(c, ast.Call)
                and getattr(c.func, "attr", None) == "auto_upsert_from_review"
                for stmt in n.body for c in ast.walk(stmt)
            )
        ]
        assert tries, f"{path}: 找不到包住 auto_upsert_from_review 的 try"
        for t in tries:
            assert any(_catches_systemexit(h) for h in t.handlers), (
                f"{path}:{t.lineno} 的 except 抓不到 SystemExit，"
                f"wave_results 契约校验会静默杀掉整条流程"
            )


# ---------------- 3. 两份副本不漂移 ----------------

@pytest.mark.parametrize("rel", SYNCED_FILES)
def test_toolkit_copies_in_sync(rel):
    """仓库副本与安装副本逐字一致（忽略行尾）——只改一份 = 运行时仍是旧行为。"""
    if len(SCRIPTS_DIRS) < 2:
        pytest.skip("只有一份 toolkit 副本在场，无从对比")
    base = SCRIPTS_DIRS[0]
    ref = (base / rel).read_bytes().replace(b"\r\n", b"\n")
    for other in SCRIPTS_DIRS[1:]:
        got = (other / rel).read_bytes().replace(b"\r\n", b"\n")
        assert got == ref, f"{rel} 两份副本漂移：\n  {base / rel}\n  {other / rel}"


# ---------------- 4. 历史行归一迁移 ----------------

@pytest.mark.parametrize("verdict,expect", [
    ("0/8 过硬闸, 新高 0.02", "FAIL"),      # DB 实存（EUR/wave104）
    ("GATE_FAIL", "FAIL"),                  # DB 实存（EUR/wave124）
    ("3/8 过硬闸", "PASS"),
    ("GREEN: 2 候选达标", "PASS"),
    ("YELLOW: 0 候选, 3 near", "PARTIAL"),
    ("RED: 5 全灭", "FAIL"),
    ("PASS", None),                          # 已是枚举，跳过
    ("", None),                              # 空 verdict 由 status=closed 闸管
    ("一句无法判定的结论", None),            # 宁可漏改不可错改
])
def test_migration_classify(verdict, expect):
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    import migrate_wave_verdict_enum as M
    assert M.classify(verdict)[0] == expect
