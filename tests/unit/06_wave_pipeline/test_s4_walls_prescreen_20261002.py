# -*- coding: utf-8 -*-
"""2026-10-02 步 7（S4）P0–P2 落地回归护栏。

对应审查报告 §14 的 F1/F1b/F2/F3/F4：

P0-a  `s4_walls_<region>_<wave>` 结构化写者（toolkit pipeline.stage_review）
      - 旧状：SOP 主路径（pipeline --review）**从不写**该键，唯一写者是
        campaign.py 走 workflow_campaign(S4) 时的 stdout 关键词扫描；step_eval 的
        `walls_coverage` 实测恒为 0，近 25 个波次 0 有键。
      - 现：`build_s4_walls_payload`（纯函数）+ `_write_s4_walls`（normal + 全灭通道都调）。
P0-b  campaign.py `_extract_walls_summary` 结构化优先
      - 旧状：只扫子进程 stdout 关键词 → 漏报（全 PASS → None）+ 误报（"structural" 告警 → 假墙）。
      - 现：先读 ledger 结构化键（_source='ledger'），扫不到才 fallback（_source='stdout_scan'）。
P1    预筛唯一口径（_lib/prescreen）
      - 旧状：campaign_intel s4-prescreen / auto_review._prescreen / review_wave.walls()
        **三套口径互不一致**；前两套 `x or 0` 把 NULL 当 0（静默判死）。
      - 现：三处共用一个 prescreen；NULL → `*_UNKNOWN`（不判败）。
P1-b  s4-prescreen 进 S4 编排（campaign.py run 的 S4 分支）
      - 旧状：SKILL.md 把它写成固定动作却从未被编排调用。
      - 现：resolve_s4_alphas 后离线预筛；全灭 → 跳过 review_wave 直接判死。
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src", REPO_ROOT / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TOOLKIT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(TOOLKIT_SCRIPTS))


# ============================================================ P1 预筛唯一口径

def test_prescreen_file_shipped_in_repo():
    """`_lib/prescreen.py` 必须在**仓库副本**（安装位滞后会静默 fallback）。"""
    assert (TOOLKIT_SCRIPTS / "_lib" / "prescreen.py").is_file()


def test_prescreen_three_callers_share_one_source():
    """三处调用方都能解析到同一个 prescreen（防再次口径分裂）。"""
    from _lib.prescreen import prescreen as ps_mod, prescreen_row  # noqa

    # ① auto_review
    from wqb.workflow.nodes import auto_review
    r = auto_review._prescreen([
        {"alpha_id": "A", "sharpe": 2.0, "fitness": 1.5,
         "two_year_sharpe": None, "turnover": 0.1, "status": "COMPLETE"},
    ])
    assert "A" in r["READY"], "auto_review 应走新口径（NULL 2Y 不判败）"

    # ② campaign_intel
    import importlib
    ci = importlib.import_module("campaign_intel")
    pr = ci._load_prescreen_row()
    assert pr is not None, "campaign_intel 必须解析到 _lib/prescreen 而非内联兜底"
    assert pr is prescreen_row

    # ③ campaign 节点离线预筛
    from wqb.workflow.nodes import campaign
    assert campaign.resolve_toolkit_file("_lib/prescreen.py"), "campaign 侧解析器应命中仓库副本"


def test_prescreen_null_not_treated_as_zero():
    """F4 核心：2Y/fitness/turnover 为 NULL → 记 *_UNKNOWN（留观），不得判死。"""
    from _lib.prescreen import prescreen_row, READY, REVIEW, REJECT
    tier, reasons = prescreen_row({
        "alpha_id": "X", "sharpe": 2.0, "fitness": None,
        "two_year_sharpe": None, "turnover": None, "status": "COMPLETE"})
    assert tier == READY, "只有 sharpe 在、其余 NULL 应留观/达标，不得 REJECT"
    assert "FITNESS_UNKNOWN" in reasons and "2Y_UNKNOWN" in reasons

    # sharpe 缺失是唯一"缺失即死"闸
    tier2, reasons2 = prescreen_row({"alpha_id": "Y", "sharpe": None})
    assert tier2 == REJECT and "NO_SHARPE" in reasons2


def test_prescreen_legacy_zero_coercion_is_gone():
    """旧口径（or 0）会把 2Y NULL → 0 < 1.58 判死；新口径不得复现。"""
    from _lib.prescreen import prescreen_row
    tier, _ = prescreen_row({
        "alpha_id": "Z", "sharpe": 1.7, "fitness": 1.1,
        "two_year_sharpe": None, "turnover": 0.1})
    assert tier != "REJECT"


# ======================================================== P0-a 结构化 s4_walls

def _load_pipeline():
    import importlib
    sys.modules.pop("pipeline", None)
    return importlib.import_module("pipeline")


def test_build_s4_walls_payload_shape():
    """纯函数：把 r['walls'] 聚合成结构化 payload（计数而非 bool）。"""
    pl = _load_pipeline()
    rows = [
        {"id": "a1", "walls": ["structural", "robust"]},
        {"id": "a2", "walls": ["structural"]},
        {"id": "a3", "walls": []},          # 无墙 = 达标候选
    ]
    p = pl.build_s4_walls_payload("USA", "s2_demo_d1", rows, reviewed_at="2026-10-02T01:00:00")
    assert p["walls"]["structural"] == 2      # 计数
    assert p["walls"]["robust"] == 1
    assert p["n_rows"] == 3
    assert p["n_candidates"] == 1
    assert p["per_alpha"]["a1"] == ["structural", "robust"]
    assert p["region"] == "USA" and p["wave"] == "s2_demo_d1"
    assert p["reviewed_at"] == "2026-10-02T01:00:00"


def test_build_s4_walls_payload_empty_rows():
    pl = _load_pipeline()
    p = pl.build_s4_walls_payload("KOR", "s2_x_d1", [])
    assert p["walls"] == {} and p["n_rows"] == 0


def test_write_s4_walls_lands_ledger_key(tmp_path, monkeypatch):
    """`_write_s4_walls` 必须把键写进 ledger（step_eval walls_coverage 的唯一来源）。

    注：`make_ledger_store` → SqliteLedgerStore → `_lib/wqb_store.resolve_db_path(ctx)`
    优先取 `WQB_DB_PATH` 环境变量。**必须**让它指向临时库，否则会写进真实
    `data/wqb.db`（本测试首版曾污染真库，已修）。
    """
    from wqb.store import CampaignStore
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))

    pl = _load_pipeline()

    class _Ctx:
        region = "USA"
        dir = None

    ck = {"wave": "s2_demo_d1"}
    rows = [{"id": "a1", "walls": ["structural"]}, {"id": "a2", "walls": []}]
    out = pl._write_s4_walls(_Ctx(), ck, rows)
    assert out is not None, "写入不应失败"

    conn = sqlite3.connect(str(db))
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?",
            ("USA", "s4_walls_USA_s2_demo_d1")).fetchone()
    finally:
        conn.close()
    assert row is not None, "结构化键未落库"
    payload = json.loads(row[0]) if isinstance(row[0], (str, bytes)) else row[0]
    assert payload["walls"]["structural"] == 1



def test_stage_review_declares_both_write_calls():
    """normal + 全灭快速通道都必须调 `_write_s4_walls`（防未来回归只留一处）。"""
    src = (TOOLKIT_SCRIPTS / "pipeline.py").read_text(encoding="utf-8")
    assert src.count("_write_s4_walls(ctx, ck, rows)") == 2, \
        "应恰好 2 处（normal 通道 + 全灭快速通道）"


# ============================================== P0-b _extract_walls_summary

def test_extract_walls_prefers_structured_ledger(tmp_path, monkeypatch):
    """结构化键存在时，_extract_walls_summary 必须读 ledger 并标 _source='ledger'。"""
    from wqb.store import CampaignStore
    db = tmp_path / "wqb.db"
    st = CampaignStore(str(db))
    payload = {"walls": {"structural": 3}, "n_rows": 5, "n_candidates": 2}
    st.upsert_ledger("USA", "s4_walls_USA_s2_demo_d1", payload)  # upsert 接受对象，内部序列化
    st.close()

    from wqb.workflow.nodes import campaign
    st2 = CampaignStore(str(db))
    out = campaign._extract_walls_summary(
        stdout="irrelevant stdout", region="USA", wave="s2_demo_d1", store=st2)
    st2.close()
    assert out is not None
    assert out["walls"] == {"structural": 3}
    assert out.pop("_source") == "ledger"


def test_extract_walls_fallback_marks_stdout_scan(tmp_path, monkeypatch):
    """无结构化键（空库）时 fallback 到 stdout 扫描，且 _source 明确标注。"""
    from wqb.store import CampaignStore
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    from wqb.workflow.nodes import campaign
    out = campaign._extract_walls_summary(
        stdout="structural wall detected x5", region="ZZZ", wave="s9_none_d1", store=None)
    assert out is not None and out.pop("_source") == "stdout_scan"


def test_extract_walls_all_pass_returns_none_on_fallback(tmp_path, monkeypatch):
    """全 PASS（无任何墙关键词）→ fallback 结果为空/None（不得造假墙）。"""
    from wqb.store import CampaignStore
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    from wqb.workflow.nodes import campaign
    out = campaign._extract_walls_summary(
        stdout="all checks passed, everything is great", region="ZZZ",
        wave="s9_none_d1", store=None)
    # fallback 至少不能凭空造出 structural=True
    if out is not None:
        assert not out.get("structural"), f"全 PASS 不应产生假墙: {out}"


# ==================================== P1-b S4 编排前置预筛（campaign 节点）

def test_s4_prescreen_local_returns_tiers_or_none(tmp_path, monkeypatch):
    """离线预筛：可解析 prescreen 时必须返回三档，不可用才 None（fail-open）。"""
    from wqb.store import CampaignStore
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()   # 空库 → 无行 → None
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    from wqb.workflow.nodes import campaign
    out = campaign._s4_prescreen_local("ZZZ", "s9_definitely_absent_d1", ["nope1", "nope2"])
    assert out is None or set(out) == {"READY", "REVIEW", "REJECT"}


def test_s4_branch_wires_prescreen_and_all_reject_early_return():
    """S4 分支源码必须包含预筛调用 + 全灭早退（防未来重构删掉）。"""
    src = (REPO_ROOT / "src" / "wqb" / "workflow" / "nodes" / "campaign.py").read_text(
        encoding="utf-8")
    assert "_s4_prescreen_local(region, resolved_wave, alpha_ids)" in src
    assert "s4_prescreen_all_reject" in src
    assert "跳过 review_wave" in src


def test_resolve_thresholds_for_region_reads_review_node():
    """区域阈值从 tracking/<REGION>/config/thresholds.json 的 review 节读。"""
    from wqb.workflow.nodes import campaign
    t = campaign._resolve_thresholds_for_region("USA")
    # USA 有 thresholds.json 则应含 sharpe_min；无则 None（两者都可接受，只要求不抛）
    if t is not None:
        assert "sharpe_min" in t


# ================================================== resolve_toolkit_file 契约

def test_resolve_toolkit_file_prefers_repo_copy():
    """新 helper 必须命中仓库副本（本次 off-by-one 踩坑的回归护栏）。"""
    from wqb.workflow._common import resolve_toolkit_file
    f = resolve_toolkit_file("_lib/prescreen.py")
    assert f is not None
    assert "prescreen.py" in f
    norm = f.replace("\\", "/")
    assert "Claude/skills/wq-brain-campaign-toolkit/scripts" in norm


def test_resolve_toolkit_file_missing_returns_none():
    from wqb.workflow._common import resolve_toolkit_file
    assert resolve_toolkit_file("_lib/__definitely_absent__.py") is None


# ============================================ P2 salvage dataset 提取（F5）

def test_salvage_dataset_regex_covers_widened_prefixes():
    """旧正则漏 insd1_ / count_institutional_* / mean_flash_* → dataset=None（79%）。"""
    import importlib
    sys.modules.pop("review_wave", None)
    rw = importlib.import_module("review_wave")
    cases = {
        "rank(insd1_count_institutional_buyer)": "insd1",
        "mean_flash_return_5": "flash",
        "count_institutional_holders_change": "institutional",
        "group_rank(ts_zscore(anl10_eps,252),industry)": "anl10",
        "sentiment_score_avg": "sentiment",
        "model16_signal": "model16",
    }
    for expr, expect in cases.items():
        m = rw._SALVAGE_DS_RE.search(expr)
        assert m and m.group(1) == expect, f"{expr} -> {m.group(1) if m else None}"


def test_salvage_entry_default_dataset_fallback():
    """表达式无任何可识别前缀时，退回 default_dataset（本波数据集）。"""
    import importlib
    sys.modules.pop("review_wave", None)
    rw = importlib.import_module("review_wave")
    e = rw._salvage_entry({"id": "x", "code": "rank(close)", "sharpe": 1.2, "fitness": 1.0},
                          "w1", default_dataset="pv1")
    assert e["dataset"] == "pv1"
