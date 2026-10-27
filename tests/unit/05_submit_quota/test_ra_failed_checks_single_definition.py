# -*- coding: utf-8 -*-
"""backtest_results.ra_failed_checks 按 RA 唯一定义写（wqb.config，R3）。

这一列唯一的写入方是 CampaignStore.upsert_backtest_rows，此前存 `failed_checks or ra_failed_checks`：
toolkit 评审（metrics_cache.row_from_alpha）、wqb-db 收批（_flatten_platform_alpha）、campaign_intel
xr-probe 三条路径存的实际都是"所有 check 里 result=FAIL 的名字"。读取方（get_mining_yield /
campaign_intel 的严格产出率、prod-first 选探针、toolkit region_kb 的本地闸门先验、triage_prodcorr_batch、
提交队列）都把这一列为空当作"平台 RA 硬闸全过"。两种定义在两种情形下分叉：非 RA 项 FAIL（相关性
检查跑完后再取数）被记成 RA 不干净；RA 项 WARNING / ERROR 被记成干净。

**2026-10-23（P0-3，USA 复盘 §9.1）两处口径调整**：

  ① **优先级倒过来**：完整未分桶的 `checks`（每项带 result）成为**权威档**——按定义现算。
     此前「行里给了 ra_failed_checks 就用它」排在这条前面，于是调用方预算好的空名单（RA 全过）
     盖住了行里 checks 里的 RA-WARNING ⇒ 那一列非空不了。
     分桶（平台精简结构）形态的 checks 走 `checks_bucketed` 标记，**不重算**（桶摊平会把 ERROR
     并进 pass 桶），改信调用方预算好的 `ra` 名单。
  ② **NULL 二义消除**：写库时「RA 全过」落 `'[]'`（已知），NULL 只剩一个含义「这一行的 RA 状态
     未知」。此前空列表也落 NULL ⇒ 「全过」与「无信息」在列上不可区分，该列不可统计。

夹具是真实载荷裁剪件 tests/fixtures/alpha_detail_cluster_sample.json（13 项 checks，RA 全过），
在它上面各造一种情形。本文件断言：每条写入路径最终落进这一列的，都等于 wqb.config 从完整 checks
算出的 RA 失败项；failed_checks（全部 FAIL）照旧留在行里 / payload_json 里；平台原始 checks 的
name/result/value/limit 也留在 payload_json.checks（此前全丢 ⇒ 「差多少」不可重建）。
"""
import asyncio
import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
for _p in (REPO_ROOT, REPO_ROOT / "src", REPO_ROOT / "tools", TOOLKIT_SCRIPTS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.config import compute_webdata_failed_counts  # noqa: E402
from wqb.store import CampaignStore  # noqa: E402
from wqb.store._backtest import ra_failed_names  # noqa: E402

FIXTURE = REPO_ROOT / "tests" / "fixtures" / "alpha_detail_cluster_sample.json"
WAVE = "s2_item4_d1"

#: 情形 → (RA 失败项 = 这一列该存的, 全部 FAIL 项 = 此前这一列存的)
CASES = {
    "clean": ([], []),
    "corr_fail": ([], ["SELF_CORRELATION"]),                               # 非 RA 项 FAIL
    "ra_warning": (["LOW_SUB_UNIVERSE_SHARPE"], []),                       # RA 项 WARNING
    "ra_fail": (["LOW_2Y_SHARPE"], ["LOW_2Y_SHARPE"]),
}


def _raw(case):
    """GET /alphas/{id} 的原始形态（指标与 checks 在 is 块里）。"""
    d = json.loads(FIXTURE.read_text(encoding="utf-8"))
    checks = d["is"]["checks"]
    if case == "corr_fail":
        checks.append({"name": "SELF_CORRELATION", "result": "FAIL", "value": 0.83, "limit": 0.7})
    elif case == "ra_warning":
        next(c for c in checks if c["name"] == "LOW_SUB_UNIVERSE_SHARPE")["result"] = "WARNING"
    elif case == "ra_fail":
        next(c for c in checks if c["name"] == "LOW_2Y_SHARPE")["result"] = "FAIL"
    d["id"] = f"t4_{case}"
    d["regular"] = {"code": f"rank(ts_delta(x_{case}, 5))"}
    return d


def _mcp_core():
    """wq-brain-http 的精简实现（harvest_multisim_alphas 的返回形态由它产出）；缺 MCP 依赖时跳过。"""
    mcp_dir = str(REPO_ROOT / "world-quant-brain-mcp")
    if mcp_dir not in sys.path:
        sys.path.insert(0, mcp_dir)
    return pytest.importorskip("mcp_core")


def _slim(case):
    """harvest_multisim_alphas 返回的一条 alpha：mcp_core._slim_alpha + alpha_id / expression。"""
    s = _mcp_core()._slim_alpha(_raw(case))
    return {**s, "alpha_id": s["id"], "expression": s["code"]}


@pytest.fixture
def db_mcp(tmp_path, monkeypatch):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(path))
    cdir = tmp_path / "tracking" / "IND"
    (cdir / "config").mkdir(parents=True)
    monkeypatch.setenv("WQB_CAMPAIGN_DIR", str(cdir))
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    # 隔离临时库走 set_db_path（唯一正用）：`mod.DB_PATH = …` 已被 _GuardedModule 拦下
    # ——属性式 patch 在 DB 访问被拆到别的模块后静默失效，测试会写生产库（2026-10-04 事故）。
    mod.set_db_path(path)
    return mod, path


def _call(mod, name, args):
    out = asyncio.run(mod.mcp.call_tool(name, args))
    if isinstance(out, tuple):
        out = out[1]
    if isinstance(out, dict):
        return out.get("result", out)
    return json.loads(out[0].text)


def _column(path, wave=WAVE):
    conn = sqlite3.connect(str(path))
    try:
        return dict(conn.execute("SELECT alpha_id, ra_failed_checks FROM backtest_results WHERE wave=?",
                                 (wave,)).fetchall())
    finally:
        conn.close()


def _stored(names):
    """写库后的列值：**空列表 = 已知全过 → '[]'**（2026-10-23 P0-3：不再是 NULL）；
    None = 未知 → NULL。"""
    return json.dumps(names, ensure_ascii=False) if names is not None else None


# ---------------------------------------------------------------- 定义本身

@pytest.mark.parametrize("case", sorted(CASES))
def test_cases_are_what_they_claim(case):
    """夹具自检：RA 失败项与全部 FAIL 项在 corr_fail / ra_warning 上确实分叉。"""
    checks = _raw(case)["is"]["checks"]
    ra, fails = CASES[case]
    assert compute_webdata_failed_counts(checks)["ra_failed_names"] == ra
    assert [c["name"] for c in checks if c["result"] == "FAIL"] == fails


# ---------------------------------------------------------------- 存储层（唯一写入方）

def test_store_resolver_precedence_and_shapes():
    ra_warn = [{"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "WARNING"},
               {"name": "SELF_CORRELATION", "result": "FAIL"}, {"name": "LOW_FITNESS", "result": "PENDING"}]
    # 1. 完整未分桶的 checks 是权威档：按定义现算（RA 项 WARNING 算，非 RA 项 FAIL 不算，PENDING 不算）。
    #    调用方给的名单**盖不住**它 —— 此前正是这个顺序让 RA-WARNING 被空名单盖成"全过"。
    assert ra_failed_names({"ra_failed_checks": [], "failed_checks": ["LOW_SHARPE"], "checks": ra_warn}) == \
        ["LOW_SUB_UNIVERSE_SHARPE"]
    assert ra_failed_names({"ra_failed_checks": ["LOW_SHARPE"], "checks": ra_warn}) == \
        ["LOW_SUB_UNIVERSE_SHARPE"]
    assert ra_failed_names({"checks": ra_warn, "failed_checks": ["SELF_CORRELATION"]}) == \
        ["LOW_SUB_UNIVERSE_SHARPE"]
    # 2. 分桶（平台精简结构）形态的 checks 不重算 —— 桶摊平会把 ERROR 并进 pass 桶；
    #    改信调用方预算好的 ra 名单（打 checks_bucketed 标记）。
    bucketed = {"checks": [{"name": "LOW_FITNESS", "result": "PASS"},
                           {"name": "LOW_2Y_SHARPE", "result": "PASS"}],
                "checks_bucketed": True, "ra_failed_checks": ["LOW_2Y_SHARPE"]}
    assert ra_failed_names(bucketed) == ["LOW_2Y_SHARPE"]
    # 3. 没有 checks → 用调用方预算好的 ra_failed_checks（只留 RA 项名；空列表 = RA 全过）
    assert ra_failed_names({"ra_failed_checks": ["SELF_CORRELATION", "LOW_2Y_SHARPE", "LOW_2Y_SHARPE"]}) == \
        ["LOW_2Y_SHARPE"]
    assert ra_failed_names({"ra_failed_checks": [{"name": "LOW_SHARPE", "value": 1.2}]}) == ["LOW_SHARPE"]
    # 旧路径写过 JSON 字符串，还有双重编码的
    assert ra_failed_names({"ra_failed_checks": '["LOW_SHARPE", "PROD_CORRELATION"]'}) == ["LOW_SHARPE"]
    assert ra_failed_names({"ra_failed_checks": json.dumps(json.dumps(["LOW_FITNESS"]))}) == ["LOW_FITNESS"]
    assert ra_failed_names({"ra_failed_checks": "LOW_SHARPE, SELF_CORRELATION"}) == ["LOW_SHARPE"]  # 逗号分隔
    assert ra_failed_names({"ra_failed_checks": "", "failed_checks": ["LOW_SHARPE"]}) == []
    # 4. 只有 failed_checks（旧指标缓存行）→ 只留 RA 项名；**空 ⇒ 未知**（不能认证「全过」）
    assert ra_failed_names({"failed_checks": ["SELF_CORRELATION", "LOW_ROBUST_UNIVERSE_SHARPE"]}) == \
        ["LOW_ROBUST_UNIVERSE_SHARPE"]
    assert ra_failed_names({"failed_checks": ["SELF_CORRELATION"]}) is None
    assert ra_failed_names({"failed_checks": []}) is None
    # 什么都没有 → None（未知，入库 NULL）
    assert ra_failed_names({"sharpe": 1.7}) is None
    assert ra_failed_names({"ra_failed_checks": None, "checks": [], "failed_checks": None}) is None


def test_store_writes_the_column_by_definition_and_keeps_failed_checks_in_payload(tmp_path):
    path = tmp_path / "wqb.db"
    st = CampaignStore(str(path))
    try:
        n = st.upsert_backtest_rows("IND", WAVE, [
            # 旧指标缓存行：只有 failed_checks；非 RA 项 FAIL 此前被记成"RA 不干净"
            {"id": "s_corr", "code": "rank(a)", "sharpe": 2.0, "fitness": 1.4, "failed_checks": ["SELF_CORRELATION"]},
            {"id": "s_legacy", "code": "rank(b)", "sharpe": 2.0, "fitness": 1.4, "failed_checks": ["LOW_2Y_SHARPE"]},
            # 完整 checks：RA 项 WARNING 此前被记成干净
            {"alpha_id": "s_warn", "code": "rank(c)", "sharpe": 2.0, "fitness": 1.4,
             "checks": _raw("ra_warning")["is"]["checks"], "failed_checks": []},
            # 两个键都给：checks 是权威档（此前优先 ra_failed_checks）
            {"alpha_id": "s_both", "code": "rank(d)", "sharpe": 2.0, "fitness": 1.4,
             "failed_checks": ["SELF_CORRELATION"], "ra_failed_checks": []},
            # 只有 ra_failed_checks（无 checks）：按它来
            {"alpha_id": "s_ra_only", "code": "rank(e)", "sharpe": 2.0, "fitness": 1.4,
             "ra_failed_checks": ["LOW_2Y_SHARPE"]},
            # 什么 RA 信息都没有：未知 ⇒ NULL（与"全过"区分开）
            {"alpha_id": "s_unknown", "code": "rank(f)", "sharpe": 2.0, "fitness": 1.4},
        ])
        assert n == 6
    finally:
        st.close()
    assert _column(path) == {"s_corr": None,                    # 只知"没有 RA 项 FAIL"⇒ 未知（不是全过）
                             "s_legacy": '["LOW_2Y_SHARPE"]',
                             "s_warn": '["LOW_SUB_UNIVERSE_SHARPE"]',
                             "s_both": "[]",                     # 调用方给的名单 = 已知全过
                             "s_ra_only": '["LOW_2Y_SHARPE"]',
                             "s_unknown": None}                  # 未知 ⇒ NULL
    conn = sqlite3.connect(str(path))
    try:
        payload = conn.execute("SELECT json_extract(payload_json, '$.failed_checks') FROM backtest_results "
                               "WHERE alpha_id='s_corr'").fetchone()[0]
        # 2026-10-23（P0-2）：平台原始 checks 落 payload_json.checks —— name/result/value/limit 齐
        # （此前整段丢失 ⇒ "差多少"不可重建、RA 项的 WARNING/ERROR 不可见）
        checks_json = conn.execute("SELECT json_extract(payload_json, '$.checks') FROM backtest_results "
                                   "WHERE alpha_id='s_warn'").fetchone()[0]
    finally:
        conn.close()
    assert json.loads(payload) == ["SELF_CORRELATION"]                      # 全部 FAIL 照旧在 payload 里
    kept = json.loads(checks_json)
    assert [c["name"] for c in kept] == [c["name"] for c in _raw("ra_warning")["is"]["checks"]]
    warn = next(c for c in kept if c["name"] == "LOW_SUB_UNIVERSE_SHARPE")
    assert warn["result"] == "WARNING"
    assert "value" in warn and "limit" in warn                              # 差多少留得住


def test_ra_warning_row_must_never_land_as_all_pass(tmp_path):
    """报告 P0-3 的验收口径：故意构造含 RA-WARNING 的行，写库后该列**非空**。

    此前该行要么被记成"RA 全过"（空名单盖住 WARNING），要么落 NULL（空列表当 falsy）——
    两种都让"这一列可统计"落空。
    """
    path = tmp_path / "wqb.db"
    st = CampaignStore(str(path))
    try:
        st.upsert_backtest_rows("IND", WAVE, [
            {"alpha_id": "w1", "code": "rank(x)", "sharpe": 2.0, "fitness": 1.4,
             "checks": _raw("ra_warning")["is"]["checks"]},
        ])
    finally:
        st.close()
    assert _column(path)["w1"] == '["LOW_SUB_UNIVERSE_SHARPE"]'


def test_all_pass_row_is_known_empty_not_null(tmp_path):
    """「RA 全过」写 '[]'（已知），不写 NULL（未知）—— 该列要能统计就得分得开这两种。"""
    path = tmp_path / "wqb.db"
    st = CampaignStore(str(path))
    try:
        st.upsert_backtest_rows("IND", WAVE, [
            {"alpha_id": "p1", "code": "rank(x)", "sharpe": 2.0, "fitness": 1.4,
             "checks": _raw("clean")["is"]["checks"]},
        ])
    finally:
        st.close()
    col = _column(path)["p1"]
    assert col == "[]"
    assert col is not None


# ---------------------------------------------------------------- 每条写入路径

@pytest.mark.parametrize("case", sorted(CASES))
def test_every_writer_path_lands_the_same_ra_list(case, db_mcp):
    mod, _ = db_mcp
    ra, fails = CASES[case]
    rows = {}
    # wqb-db 收批 / campaign_intel xr-probe：原始 is 块经拍平
    flat = mod._flatten_platform_alpha(_raw(case))
    assert flat["failed_checks"] == fails
    rows["flatten(raw)"] = flat
    # toolkit 评审：GET /alphas/{id} → row_from_alpha
    sys.modules.pop("metrics_cache", None)
    mc = importlib.import_module("metrics_cache")
    row = mc.row_from_alpha(f"t4_{case}", _raw(case))
    assert row["failed_checks"] == fails                                      # 评审用的全部 FAIL 不变
    rows["row_from_alpha"] = row
    # tools/harvest_multisim.py 收批 CLI
    hm = importlib.import_module("harvest_multisim")

    class _Resp:
        status_code = 200

        def __init__(self, data):
            self._data, self.text = data, json.dumps(data)

        def json(self):
            return self._data

    class _Brain:
        async def _request(self, method, path):
            return _Resp(_raw(case))

    det = asyncio.run(hm.fetch_alpha_details(_Brain(), f"t4_{case}"))
    assert det["failed_checks"] == fails
    rows["harvest_multisim"] = hm._to_backtest_rows([det])[0]
    for path, r in rows.items():
        assert r["ra_failed_checks"] == ra, path
        assert ra_failed_names(r) == ra, path                                 # 存储层落这一列的值


@pytest.mark.parametrize("case", sorted(CASES))
def test_slim_harvest_shape_uses_the_precomputed_ra_block(case, db_mcp):
    """harvest_multisim_alphas 的精简结构：ra 块按同一定义预算，RA 全过时不带名单键 → 空列表。

    此前 ra 块没有名单就回落到分桶 checks 的 FAIL（corr_fail 被记成不干净）。
    """
    mod, _ = db_mcp
    ra, fails = CASES[case]
    flat = mod._flatten_platform_alpha(_slim(case))
    assert flat["ra_failed_checks"] == ra
    assert flat["failed_checks"] == fails
    assert mod._flatten_platform_alpha(flat) == flat                         # 幂等


def test_row_from_alpha_without_wqb_falls_back_through_the_store(monkeypatch):
    """toolkit 装在仓库外、找不到 wqb 包：行里不带 ra_failed_checks（调用方没预算）。

    但 P0-2 之后这一行**带完整 checks**（name/result/value/limit）⇒ 存储层走权威档现算 ⇒
    仍能判出 RA 状态；这是「载荷保真」带来的直接收益。
    """
    sys.modules.pop("metrics_cache", None)
    mc = importlib.import_module("metrics_cache")
    monkeypatch.setitem(sys.modules, "wqb.config", None)                     # import wqb.config → ImportError
    row = mc.row_from_alpha("t4_corr_fail", _raw("corr_fail"))
    assert "ra_failed_checks" not in row and row["failed_checks"] == ["SELF_CORRELATION"]
    assert row["checks"], "P0-2：平台原始 checks 必须随行透传"
    assert ra_failed_names(row) == []                                        # 非 RA 项 FAIL 不算 RA 失败
    # 只剩 failed_checks 一档（无 checks、无调用方名单）⇒ 未知，不能认证「全过」
    assert ra_failed_names({"failed_checks": ["SELF_CORRELATION"]}) is None


def test_row_from_alpha_reads_two_year_from_either_platform_carrier():
    """2Y 按 alpha 代际只发 LOW_2Y_SHARPE 或 IS_LADDER_SHARPE 之一（`wqb.config.RA_2Y_NAMES`）。

    toolkit 评审此前只认前者 ⇒ 只发 ladder 的颗 `two_year_sharpe=None`，
    `review_wave.walls` 标 2Y_UNKNOWN 并跳过 2Y 墙（2026-10-23 IND/wave232 实测 10/29 颗）。
    """
    sys.modules.pop("metrics_cache", None)
    mc = importlib.import_module("metrics_cache")

    raw = _raw("clean")
    low = next(c for c in raw["is"]["checks"] if c["name"] == "LOW_2Y_SHARPE")
    low["name"] = "IS_LADDER_SHARPE"
    assert mc.row_from_alpha("t4_ladder", raw)["two_year_sharpe"] == low["value"]

    # 两个载体同时存在：LOW_2Y_SHARPE 优先（更直接的 2Y 读数）
    both = _raw("clean")
    low2 = next(c for c in both["is"]["checks"] if c["name"] == "LOW_2Y_SHARPE")
    both["is"]["checks"].append({"name": "IS_LADDER_SHARPE", "result": "PASS",
                                 "value": low2["value"] + 1.0})
    assert mc.row_from_alpha("t4_both", both)["two_year_sharpe"] == low2["value"]


# ---------------------------------------------------------------- 端到端：收批入库 → 严格产出率

@pytest.mark.parametrize("shape", ["raw", "slim"])
def test_harvest_then_strict_yield_counts_by_ra_definition(shape, db_mcp):
    mod, path = db_mcp
    make = _raw if shape == "raw" else _slim
    alphas = [make(case) for case in sorted(CASES)]
    out = _call(mod, "harvest_multisim_results", {"region": "IND", "wave": WAVE, "alphas": alphas})
    assert out["upserted"] == 4, out
    assert _column(path) == {f"t4_{case}": _stored(ra) for case, (ra, _) in CASES.items()}
    y = _call(mod, "get_mining_yield", {"region": "IND"})["totals"]
    # 四条 sharpe 3.67 / fitness 2.96 全过线；RA 干净的是 clean 与 corr_fail（此前是 clean 与 ra_warning）
    assert (y["backtested"], y["passed"], y["ra_clean"]) == (4, 4, 2)
