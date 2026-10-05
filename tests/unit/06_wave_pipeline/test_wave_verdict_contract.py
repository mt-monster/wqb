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

REPO_ROOT = Path(__file__).resolve().parents[3]
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
    """加载运行时那一份 `_lib.wave_results`（相对 import 要求按包加载）。

    模块级：本文件多个用例共用同一份模块。但"把安装副本插到 sys.path[0] + 换掉
    `_lib*`"是全局副作用，模块跑完必须还原——否则安装副本会滞留在 sys.path[0]，
    后续文件里 `import gate`（如 test_p1_fixes_20260927::test_gate_resolves_workspace_without_env）
    会解析到安装副本、走不回仓库 src/。用 MonkeyPatch.context()（可在模块级 fixture 内
    使用）快照并在 teardown 还原 sys.path 及 sys.modules 里的 `_lib`/`_lib.*`/`gate`。
    """
    if not SCRIPTS_DIRS:
        pytest.skip("wq-brain-campaign-toolkit 未安装且仓库副本缺失")
    with pytest.MonkeyPatch.context() as mp:
        # delitem：清掉当前副本并记录原值，teardown 逐一还原（不存在则 no-op）
        for m in ("_lib.wave_results", "_lib.ledger", "_lib.common", "_lib", "gate"):
            mp.delitem(sys.modules, m, raising=False)
        # syspath_prepend：先快照整条 sys.path，再插首位；undo 时整条还原
        mp.syspath_prepend(str(SCRIPTS_DIRS[0]))
        yield importlib.import_module("_lib.wave_results")
        # 导入安装副本会新塞进 `_lib*`（及其自插的子路径经上面 syspath 还原），
        # delitem 的 undo 不会移除"导入新建"的键，故显式弹出；随后 undo 补回原值
        for m in [k for k in list(sys.modules)
                  if k == "_lib" or k.startswith("_lib.") or k == "gate"]:
            sys.modules.pop(m, None)


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


# ---------------- 3b. 写入方转发的参数，契约必须接得住 ----------------

def test_mcp_wrapper_params_are_accepted_by_contract(tmp_path):
    """`wqb_db_mcp.upsert_wave_result` 声明的每个参数，契约都得吃下（不许报未知列）。

    战例（2026-10-06 实测）：包装层自 2026-10-02 起无条件转发 `n_pass` / `n_near`，
    而契约把它们当未知列拒绝 ⇒ **这个写库工具每一次调用都 TypeError**，在 HEAD 上
    全程哑巴。它藏了 9 天不被发现的原因很值得记：同文件的守护用例先因
    `DB_PATH` 属性式 patch 被硬闸拦下而 ERROR，**报错盖住了真 bug**——所以修完
    fixture 必须回头看那些“从 ERROR 变 FAILED”的用例，别当噪声。

    表与契约都只有 9 个可写列（`wave_results` 实测 16 列，无 n_pass/n_near）：
    计数是“证据”，不是列。本用例不绑实现细节（不猜哪些是证据参数），
    只钉住一条：按写入方签名原样传进来不得抛 TypeError。
    """
    import inspect
    import sqlite3

    from wqb import wave_results_contract as contract
    from wqb.store import CampaignStore
    import wqb_db_mcp

    tool = getattr(wqb_db_mcp.upsert_wave_result, "fn", wqb_db_mcp.upsert_wave_result)
    params = [p.name for p in inspect.signature(tool).parameters.values()
              if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
    assert "n_pass" in params and "n_near" in params, \
        "写入方签名变了——本用例的意义就在于盯住它与契约的一致性"

    db = tmp_path / "contract.db"
    CampaignStore(str(db)).close()                      # 建表
    conn = sqlite3.connect(str(db))
    try:
        forwarded = {name: None for name in params if name not in ("region", "wave_number")}
        forwarded["verdict"] = "PASS"                   # 给个合法结论，让它真能落库
        try:
            res = contract.upsert_wave_result(conn, "KOR", "999", "2026-10-06T00:00:00",
                                              **forwarded)
        except TypeError as e:
            pytest.fail(f"契约不接受写入方转发的参数：{e}")
        conn.commit()
        row = conn.execute("SELECT verdict, status FROM wave_results"
                           " WHERE region='KOR' AND wave_number='999'").fetchone()
    finally:
        conn.close()
    assert "不认识的列" not in json.dumps(res, ensure_ascii=False), res
    assert res.get("action") == "inserted", res          # 参数全被吃下且真的写了库
    assert row == ("PASS", "closed"), row                # 计数没被当成列弄坏行


# ---------------- 4. 历史行归一迁移 ----------------

@pytest.mark.parametrize("verdict,expect", [
    ("0/8 过硬闸, 新高 0.02", "FAIL"),      # DB 实存（EUR/wave104）
    ("GATE_FAIL", "FAIL"),                  # DB 实存（EUR/wave124）
    ("3/8 过硬闸", "PARTIAL"),   # 2026-09-26 对齐 campaign（N>0 → PARTIAL）
    ("GREEN: 2 候选达标", "PASS"),
    ("YELLOW: 0 候选, 3 near", "PARTIAL"),
    ("RED: 5 全灭", "FAIL"),
    ("PASS", None),                          # 已是枚举，跳过
    ("", None),                              # 空 verdict 由 status=closed 闸管
    ("一句无法判定的结论", None),            # 宁可漏改不可错改
])
def test_migration_classify(verdict, expect, monkeypatch):
    # 同样别把 tools/ 永久插进 sys.path：monkeypatch 用例结束即还原（含被删的模块）
    monkeypatch.syspath_prepend(str(REPO_ROOT / "tools"))
    monkeypatch.delitem(sys.modules, "migrate_wave_verdict_enum", raising=False)
    import migrate_wave_verdict_enum as M
    assert M.classify(verdict)[0] == expect
