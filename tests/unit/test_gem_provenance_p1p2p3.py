# -*- coding: utf-8 -*-
"""回归测试：GEM 生成链路修复（2026-09-17 #1/#2/#3/#4/#6）。

## 背景（评估报告 `output_report/gem_evaluation_20260917.md`）
- **#1**：`expressions.source` **没有任何代码路径在写**（3 个 `INSERT INTO expressions`
  写入点全未设置它）→ 全库 89.8% 为 NULL、`source='gem'` 全部停在 2026-08-25/26/28、
  9 月 14,511 条全 NULL → GEM 产出不可辨识、无法做 phased/skeleton 的 A/B。
- **#2**：`gem_wave.py:172` 的写回 INSERT 引用 `bucket`/`skeleton`/`selected` 三个
  **当时并不存在的列** → 每次运行都在写回处 `OperationalError`，
  `_auto_dedup`/`_auto_bucket`/`_auto_skeleton` 三项能力算完即丢弃。
- **#3**：`gate.py::_load_exposure_map` 在闸6 里算出了 expression→expected_exposure
  映射然后**用完即丢** → SKILL.md 规则 7（语义多样性）/规则 8（Exposure 验证）无法度量。
- **#4**：SOP 窗口白名单只写在散文里，且 `_DEFAULT_WINDOWS=[20,60,120,5,10,252]`
  与白名单冲突（6 里 4 违规）→ 全库 23% 非白名单窗口，Top 恰为 20/10/120/60。
- **#6**：headless_runner 的 `--require-operators`/`--require-count`（多样性强制）
  **未从 gem.py 透传**。
"""

import json
import os
import sqlite3
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))

TK_SCRIPTS = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")
TK_CONFIG = os.path.join(
    REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "config", "platform_constraints.json"
)

from wqb.store import CampaignStore  # noqa: E402
from wqb.expression.skeleton import structural_signature  # noqa: E402


# ---------------------------------------------------------------------------
# fixture：真实 schema 的临时库
# ---------------------------------------------------------------------------

@pytest.fixture()
def store(tmp_path):
    st = CampaignStore(str(tmp_path / "t.db"))
    return st


# ---------------------------------------------------------------------------
# #1 + #3：规范写入器落 provenance
# ---------------------------------------------------------------------------

def test_upsert_persists_provenance(store):
    """source / skeleton / bucket / selected / expected_exposure 必须真的落库。"""
    store.upsert_expressions(
        "TEST", "w1",
        [{"expression": "rank(ts_backfill(close, 66))", "status": "gem",
          "source": "gem_phased", "skeleton": structural_signature("rank(ts_backfill(close, 66))"),
          "expected_exposure": "value"},
         {"expression": "ts_corr(rank(a), rank(b), 20)", "status": "gem",
          "source": "gem_phased", "bucket": "corr", "expected_exposure": "momentum"}],
    )
    conn = store.connection
    rows = {r["expression"]: r for r in conn.execute(
        "SELECT * FROM expressions").fetchall()}
    a = rows["rank(ts_backfill(close, 66))"]
    assert a["source"] == "gem_phased"
    assert a["expected_exposure"] == "value"
    assert a["skeleton"] == structural_signature("rank(ts_backfill(close, 66))")
    assert a["selected"] == 0
    b = rows["ts_corr(rank(a), rank(b), 20)"]
    assert b["bucket"] == "corr" and b["expected_exposure"] == "momentum"


def test_upsert_source_param_is_fallback(store):
    """条目没带 source 时用函数参数兜底（条目优先）。"""
    store.upsert_expressions("TEST", "w2", [{"expression": "rank(f)"}], source="probe")
    r = store.connection.execute(
        "SELECT source FROM expressions WHERE wave='w2'").fetchone()
    assert r[0] == "probe"


def test_expected_exposure_column_exists_in_schema_source():
    """schema 源文件必须含 expected_exposure（新库也能建出来）。"""
    src = open(os.path.join(REPO, "src", "wqb", "store", "_schema.py"),
               encoding="utf-8").read()
    assert '"expected_exposure", "TEXT"' in src
    assert '("bucket", "TEXT")' in src
    assert '("skeleton", "TEXT")' in src


# ---------------------------------------------------------------------------
# #2：gem_wave 写回列必须与真实 schema 一致（防止同源 bug 复发）
# ---------------------------------------------------------------------------

def test_gem_wave_writeback_columns_match_real_schema():
    """`gem_wave._WRITEBACK_COLUMNS` ⊆ expressions 实际列。

    这是本次修复的**核心守卫**：此前该节点 INSERT 引用了三个不存在的列，
    每次运行都 OperationalError、三项能力算完即丢弃 —— 列名对不上必须立即变红。
    """
    sys.path.insert(0, os.path.join(REPO, "src"))
    from wqb.workflow.nodes import gem_wave

    schema_path = os.path.join(str(REPO), "src", "wqb", "store", "_schema.py")
    assert os.path.isfile(schema_path)

    # 用真实 schema（CampaignStore.ensure_schema）建库后取实际列
    import tempfile
    db = os.path.join(tempfile.mkdtemp(), "s.db")
    CampaignStore(db)
    real_cols = {r[1] for r in sqlite3.connect(db).execute(
        "PRAGMA table_info(expressions)")}

    unknown = [c for c in gem_wave._WRITEBACK_COLUMNS if c not in real_cols]
    assert not unknown, (
        f"gem_wave 写回列引用了不存在的列：{unknown}\n"
        f"（2026-09-17 事故同源：引用了当时不存在的 bucket/skeleton/selected）"
    )


def test_gem_wave_writeback_updates_by_id(tmp_path):
    """端到端：真实 schema 建库 → SELECT → 骨架标注 → 按 id UPDATE，不得报错。

    注：**必须按 id UPDATE**（行来自 `SELECT * FROM expressions`，语义是"给已有行补属性"）。
    修复前用 `INSERT OR REPLACE` 有两重 bug：① 引用不存在的列；
    ② REPLACE 整行重写且不提供 wave_id（NOT NULL）→ 即便列存在也失败。
    """
    from wqb.workflow.nodes import gem_wave

    db = str(tmp_path / "s.db")
    store = CampaignStore(db)
    store.upsert_expressions("TEST", "w9",
                             [{"expression": "rank(x)", "status": "gem",
                               "source": "gem_phased"}])

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM expressions WHERE region=? AND status='gem'", ("TEST",))
    expressions = [dict(r) for r in cur.fetchall()]
    expressions = gem_wave._auto_skeleton(expressions)

    set_cols = [c for c in gem_wave._WRITEBACK_COLUMNS if c != "id"]
    set_sql = ", ".join(f"{c}=?" for c in set_cols)
    for expr in expressions:
        cur.execute(
            f"UPDATE expressions SET {set_sql} WHERE id=?",
            tuple(expr.get(c) for c in set_cols) + (expr["id"],),
        )
    conn.commit()

    skel = cur.execute(
        "SELECT skeleton FROM expressions WHERE region='TEST'").fetchone()[0]
    assert skel and "F" in skel, "写回后 skeleton 必须真的落库（此前列不存在）"


def test_gem_wave_auto_skeleton_uses_structural_signature():
    """`_auto_skeleton` 必须产出**结构签名**（可判同族），不再是 3 桶子串匹配。"""
    from wqb.workflow.nodes import gem_wave

    items = [{"expression": "rank(ts_backfill(close, 66))"},
             {"expression": "rank(ts_backfill(open, 66))"}]
    gem_wave._auto_skeleton(items)
    # 两条同骨架（仅字段不同）必须得到同一签名 —— 这样才能被去重识别为兄弟变体
    assert items[0]["skeleton"] == items[1]["skeleton"]
    assert "rank_ts" not in items[0]["skeleton"]  # 旧 3 桶值已废弃
    assert "F" in items[0]["skeleton"]


def test_gem_wave_dedup_suppresses_siblings():
    """`gem_wave` 的去重链必须能抑制"同骨架换字段"。"""
    from wqb.workflow.nodes import gem_wave

    items = [{"expression": f"rank(ts_backfill(f{i}, 66))"} for i in range(9)]
    items += [{"expression": "ts_corr(a,b,20)"}]
    gem_wave._auto_skeleton(items)
    from wqb.expression.skeleton import dedup_by_skeleton  # noqa: E402
    # max_share=None 单独考察 max_per_skeleton（默认 0.25 的占比上限会更严）
    kept, dropped = dedup_by_skeleton(items, max_per_skeleton=3, max_share=None)
    assert len(kept) == 4 and len(dropped) == 6
    # 默认参数（含 max_share=0.25）会更严：10 条 → 上限 int(10*0.25)=2，再加 1 条异骨架
    kept2, _ = dedup_by_skeleton(items, max_per_skeleton=3)
    assert len(kept2) == 3


# ---------------------------------------------------------------------------
# #1：gem.py 的 source 标注
# ---------------------------------------------------------------------------

def test_label_source_writes_and_does_not_overwrite(tmp_path, monkeypatch):
    """_label_source 只标 NULL/空，不得覆盖已有来源；异常时返回 0。"""
    from wqb.workflow.nodes import gem as gem_node

    store = CampaignStore(str(tmp_path / "s.db"))
    store.upsert_expressions("TEST", "w1", [
        {"expression": "rank(a)", "status": "gem"},            # NULL → 会被标
        {"expression": "rank(b)", "status": "gem", "source": "manual"},  # 已有 → 不动
    ])
    monkeypatch.setattr(gem_node, "resolve_db_path", lambda: str(tmp_path / "s.db"))

    n = gem_node._label_source(["rank(a)", "rank(b)"], "TEST", "phased")
    assert n == 1
    conn = store.connection
    got = {r[0]: r[1] for r in conn.execute(
        "SELECT expression, source FROM expressions")}
    assert got["rank(a)"] == "gem_phased"
    assert got["rank(b)"] == "manual"          # 不得覆盖


def test_label_source_returns_zero_on_error(monkeypatch):
    from wqb.workflow.nodes import gem as gem_node
    # DB 不存在 → 异常 → 返回 0（可观测性增强不得影响主流程）
    monkeypatch.setattr(gem_node, "resolve_db_path",
                        lambda: os.path.join(str(tmp_path_none()), "missing.db"))
    assert gem_node._label_source(["rank(a)"], "TEST", None) == 0


def tmp_path_none():
    import tempfile
    return tempfile.mkdtemp()


def test_label_source_builds_mode_label():
    """mode 未知 → `gem`；已知 → `gem_<mode>`。"""
    src = open(os.path.join(REPO, "src", "wqb", "workflow", "nodes", "gem.py"),
               encoding="utf-8").read()
    assert 'f"gem_{str(pipeline_mode).strip().lower()}"' in src
    assert 'label = "gem"' in src


# ---------------------------------------------------------------------------
# #6：gem.py 透传多样性强制参数
# ---------------------------------------------------------------------------

def test_gem_forwards_require_operators():
    src = open(os.path.join(REPO, "src", "wqb", "workflow", "nodes", "gem.py"),
               encoding="utf-8").read()
    assert '"--require-operators"' in src
    assert '"--require-count"' in src
    # 必须真的出现在 run() 的参数里（而不是只在别处）
    assert "require_operators: Optional[str] = None" in src
    assert "require_count: int = 2" in src


def test_gem_registry_has_new_params():
    sys.path.insert(0, os.path.join(REPO, "src"))
    from wqb.workflow.registry import get_registry
    reg = get_registry()
    meta = reg.get_meta("gem") if hasattr(reg, "get_meta") else reg._meta["gem"]
    for p in ("require_operators", "require_count"):
        assert p in (meta.optional_params or []), f"gem 节点缺参数 {p}"
    # gem_wave 的新参数也要登记
    meta2 = reg.get_meta("gem_wave") if hasattr(reg, "get_meta") else reg._meta["gem_wave"]
    for p in ("max_per_skeleton", "source"):
        assert p in (meta2.optional_params or []), f"gem_wave 节点缺参数 {p}"


# ---------------------------------------------------------------------------
# #3：gate 把 exposure 映射落库
# ---------------------------------------------------------------------------

def test_gate_has_exposure_persistence():
    """gate.py 必须存在 exposure 落库函数，且是尽力而为（异常返回 0）。"""
    src = open(os.path.join(TK_SCRIPTS, "gate.py"), encoding="utf-8").read()
    assert "_persist_exposure_map" in src
    assert "UPDATE expressions SET expected_exposure=" in src
    assert "except Exception" in src.split("def _persist_exposure_map")[1].split("def ")[0]


def test_persist_exposure_map_never_raises(tmp_path, monkeypatch):
    """store 缺失/异常时必须返回 0，绝不能影响门禁判定。"""
    sys.path.insert(0, TK_SCRIPTS)
    import gate

    class _BadCtx:
        region = "TEST"

        def __getattr__(self, k):
            raise RuntimeError("boom")

    assert gate._persist_exposure_map(_BadCtx(), {"rank(a)": "value"}) == 0
    assert gate._persist_exposure_map(None, {}) == 0


# ---------------------------------------------------------------------------
# #4：窗口白名单
# ---------------------------------------------------------------------------

def _pc():
    return json.load(open(TK_CONFIG, encoding="utf-8"))


def test_window_whitelist_in_platform_config():
    wl = _pc().get("window_whitelist")
    assert wl == [1, 5, 22, 66, 252, 504, 1008, 1260]


def test_config_standard_windows_agrees_with_platform_config():
    """两处同源常量必须一致（src/wqb/config.py 与 toolkit config）。"""
    from wqb import config
    assert list(config.STANDARD_WINDOWS) == _pc().get("window_whitelist")


def test_operator_coverage_default_windows_are_in_whitelist():
    """污染源必须已对齐：`_DEFAULT_WINDOWS` 的每个值都要在白名单内。"""
    sys.path.insert(0, TK_SCRIPTS)
    from _lib.operator_coverage import _DEFAULT_WINDOWS  # noqa: E402
    wl = set(_pc().get("window_whitelist"))
    bad = [w for w in _DEFAULT_WINDOWS if w not in wl]
    assert not bad, (
        f"_DEFAULT_WINDOWS 仍有白名单外的值 {bad} —— 这正是全库 23% "
        f"非白名单窗口的产生源（20/10/120/60）"
    )


def test_expression_windows_extracts_windows_only():
    sys.path.insert(0, TK_SCRIPTS)
    import gate
    assert gate.expression_windows("ts_decay_linear(ts_backfill(f, 66), 22)") == [66, 22]
    assert gate.expression_windows("ts_corr(a, b, 20)") == [20]
    assert gate.expression_windows("winsorize(x, std=4)") == []          # 命名参数
    assert gate.expression_windows('bucket(rank(x), range="0,1,0.1")') == []  # 引号串
    assert gate.expression_windows("quantile(x)") == []                  # 小数
    assert gate.expression_windows("") == []


def test_window_warning_does_not_block(tmp_path):
    """非白名单窗口是 **warning**（SOP 允许"给解释后用"），不得判 FAIL。"""
    sys.path.insert(0, TK_SCRIPTS)
    import gate
    pc = _pc()
    poison = [p for p in pc.get("poison_patterns", [])
              if p.get("severity", "block") == "block"]
    # 一个窗口违规、其余干净的简单表达式
    expr = "rank(ts_mean(f, 10))"     # 10 不在白名单
    out = gate.check_one(expr, ({"f", "ts_mean"}, "MATRIX", {}, []), None, poison, pc)
    win = [w for w in out["warnings"] if "WINDOW" in w]
    assert win, "未产生窗口告警"
    assert out["pass"] is True, "warning 不得影响 pass"
    assert out["issues"] == []


# ---------------------------------------------------------------------------
# 兜底：防回归的静态检查
# ---------------------------------------------------------------------------

def test_gem_wave_no_longer_writes_sourceless():
    """gem_wave 写回必须包含 source 与 expected_exposure（修复前只有 11 列）。"""
    from wqb.workflow.nodes import gem_wave
    assert "source" in gem_wave._WRITEBACK_COLUMNS
    assert "expected_exposure" in gem_wave._WRITEBACK_COLUMNS
    assert "skeleton" in gem_wave._WRITEBACK_COLUMNS


# ---------------------------------------------------------------------------
# 2026-09-17 追补：写入器自动骨架 + MCP 工具 source 形参（真实链路接线）
# 背景：实际生成链路 = GEM runner → AI 调 MCP upsert_expressions 落库，
# 该链路既不传 source 也不写 skeleton → 两列全库近乎全空（skeleton 0 行）。
# ---------------------------------------------------------------------------

def test_upsert_auto_computes_skeleton(tmp_path):
    """不给 skeleton 时写入器必须自动计算（任何路径落库的行都带骨架）。"""
    db = str(tmp_path / "s.db")
    store = CampaignStore(db)
    store.upsert_expressions("TEST", "w_auto",
                             [{"expression": "rank(ts_backfill(close, 66))"},
                              {"expression": "ts_corr(rank(a), rank(b), 20)"}])
    conn = sqlite3.connect(db)
    rows = conn.execute("SELECT expression, skeleton FROM expressions "
                        "WHERE region='TEST' ORDER BY id").fetchall()
    assert all(r[1] for r in rows), f"骨架未自动填充: {rows}"
    # 同骨架换字段 → 折叠为同一签名（去重的前提）
    assert rows[0][1] == "rank ( ts_backfill ( F , N ) )"
    assert rows[1][1] == "ts_corr ( rank ( F ) , rank ( F ) , N )"


def test_upsert_respects_explicit_skeleton(tmp_path):
    """条目已带 skeleton 时以条目为准（不覆盖上游给的分类）。"""
    db = str(tmp_path / "s.db")
    store = CampaignStore(db)
    store.upsert_expressions("TEST", "w_keep",
                             [{"expression": "rank(close)", "skeleton": "CUSTOM"}])
    conn = sqlite3.connect(db)
    got = conn.execute("SELECT skeleton FROM expressions WHERE region='TEST'").fetchone()[0]
    assert got == "CUSTOM"


def test_mcp_upsert_tool_exposes_source_param():
    """MCP 写库工具必须暴露 source 形参（否则真实链路永远写不进来源标签）。"""
    import inspect
    import importlib.util as _u
    p = os.path.join(REPO, "wqb_db_mcp.py")
    if not os.path.isfile(p):
        import pytest as _pytest
        _pytest.skip("wqb_db_mcp.py 不在仓库根")
    src = open(p, encoding="utf-8").read()
    sig = src.split("def upsert_expressions(", 1)[1].split(")", 1)[0]
    assert "source" in sig, "upsert_expressions 缺 source 形参"
    assert "source=source" in src, "source 未透传到 store"


# ---------------------------------------------------------------------------
# 2026-09-17 追补：写入器自动骨架 + MCP 工具 source 形参（真实链路接线）
# 背景：实际生成链路 = GEM runner → AI 调 MCP upsert_expressions 落库，
# 该链路既不传 source 也不写 skeleton → 两列全库近乎全空（skeleton 0 行）。
# ---------------------------------------------------------------------------

def test_upsert_auto_computes_skeleton(tmp_path):
    """不给 skeleton 时写入器必须自动计算（任何路径落库的行都带骨架）。"""
    db = str(tmp_path / "s.db")
    store = CampaignStore(db)
    store.upsert_expressions("TEST", "w_auto",
                             [{"expression": "rank(ts_backfill(close, 66))"},
                              {"expression": "ts_corr(rank(a), rank(b), 20)"}])
    conn = sqlite3.connect(db)
    rows = conn.execute("SELECT expression, skeleton FROM expressions "
                        "WHERE region='TEST' ORDER BY id").fetchall()
    assert all(r[1] for r in rows), f"骨架未自动填充: {rows}"
    # 同骨架换字段 → 折叠为同一签名（去重的前提）
    assert rows[0][1] == "rank ( ts_backfill ( F , N ) )"
    assert rows[1][1] == "ts_corr ( rank ( F ) , rank ( F ) , N )"


def test_upsert_respects_explicit_skeleton(tmp_path):
    """条目已带 skeleton 时以条目为准（不覆盖上游给的分类）。"""
    db = str(tmp_path / "s.db")
    store = CampaignStore(db)
    store.upsert_expressions("TEST", "w_keep",
                             [{"expression": "rank(close)", "skeleton": "CUSTOM"}])
    conn = sqlite3.connect(db)
    got = conn.execute("SELECT skeleton FROM expressions WHERE region='TEST'").fetchone()[0]
    assert got == "CUSTOM"


def test_mcp_upsert_tool_exposes_source_param():
    """MCP 写库工具必须暴露 source 形参（否则真实链路永远写不进来源标签）。"""
    import inspect
    import importlib.util as _u
    p = os.path.join(REPO, "wqb_db_mcp.py")
    if not os.path.isfile(p):
        import pytest as _pytest
        _pytest.skip("wqb_db_mcp.py 不在仓库根")
    src = open(p, encoding="utf-8").read()
    sig = src.split("def upsert_expressions(", 1)[1].split(")", 1)[0]
    assert "source" in sig, "upsert_expressions 缺 source 形参"
    assert "source=source" in src, "source 未透传到 store"
