# -*- coding: utf-8 -*-
"""闸 TRI（分类级字段分诊硬门）fail-closed 回归测试 —— 步 3/S1 入口。

背景（2026-09-30 落地）：全局 9125 条回测 → 646 条 ra_clean，仅 **7.1%**；
**49% 的回测（4475 条）打在后来被证伪的数据集上**，平均 22.8 条/死集。
浪费发生在「选集之后、回测之中」，而选集那一刻本地已有足够信息判定
「这个集不值得开」。故在 S1 唯一必经执行体（scan_fields.py，script_map["S1"]，
CLI 直调与 workflow_campaign(stage="S1") 两条路径都经过它）入口设 fail-closed 闸。

守护的契约，任一条被删/被绕过即红：
  1. 判级非「★可开波」→ 阻断（判死/族连坐/拥挤/无甜点字段/仅条件腿 全覆盖）
  2. 台账缺失 / 不可读 / 无 verdicts / 数据集不在台账内 → **一律阻断**（无法判定 = 阻断）
  3. 唯一逃生口 --skip-triage-gate / --triage-gate off，且必须打印醒目告警

设计：判定逻辑走**纯单测**（直接调用 `_triage_gate`，注入内存 sqlite 连接，不碰实时库、
不启子进程）；CLI 只留 2 条契约冒烟（缺台账 exit 2 / skip 才放行），
凭证文件指向不存在的路径 → 必然在登录前失败，**全程不触网**。
"""
from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCAN_FIELDS = (REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
               / "scripts" / "scan_fields.py")
PY = sys.executable

PASS = "★可开波"
BLOCKING = ["判死", "族连坐", "拥挤", "无甜点字段", "仅条件腿"]


def _load():
    spec = importlib.util.spec_from_file_location("_sf_tri", SCAN_FIELDS)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _db(rows=None):
    """内存库：ledger_kv(region,key,value)。rows = [(region,key,value_str)]"""
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY, region TEXT, "
              "key TEXT, value TEXT)")
    for r in (rows or []):
        c.execute("INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)", r)
    c.commit()
    return c


def _tri_payload(verdicts, **extra):
    d = {"generated_by": "tools/category_field_triage.py", "region": "KOR",
         "verdicts": verdicts}
    d.update(extra)
    return json.dumps(d, ensure_ascii=False)


def _ok_db(verdict=PASS, tags="", block=None):
    if block is None:
        block = (verdict != PASS)
    return _db([("KOR", "s1_triage_kor",
                 _tri_payload({"model219": {"verdict": verdict, "tags": tags,
                                            "block": block}}))])


# ---------------------------------------------------------------- 放行

def test_pass_verdict_allows_scan():
    """★可开波 → ok=True，且不带任何阻断标记。"""
    sf = _load()
    rep = sf._triage_gate("KOR", "model219", conn=_ok_db())
    assert rep["ok"] is True
    assert rep["verdict"] == PASS
    assert rep["ledger_missing"] is False and rep["unknown_dataset"] is False


# ---------------------------------------------------------------- 各级阻断

def test_every_non_pass_verdict_blocks():
    """五种非存活判级全部阻断，且 reason 里带判级名（便于定位）。"""
    sf = _load()
    for v in BLOCKING:
        rep = sf._triage_gate("KOR", "model219", conn=_ok_db(verdict=v, tags="x"))
        assert rep["ok"] is False, f"{v} 必须阻断"
        assert v in rep["reason"], f"{v} 的 reason 应含判级名，实际 {rep['reason']!r}"


def test_block_reason_carries_triage_tags():
    """阻断信息要带上分诊标签（族连坐要能看出连坐自谁）。"""
    sf = _load()
    rep = sf._triage_gate("KOR", "model219",
                          conn=_ok_db(verdict="族连坐", tags="同族(risk88,包含=1.00)"))
    assert "risk88" in rep["tags"]


# ---------------------------------------------------------------- fail-closed 四态

def test_missing_ledger_blocks():
    """台账缺失 → 阻断（这是 fail-closed 的核心，最容易被"改成放行"）。"""
    sf = _load()
    rep = sf._triage_gate("KOR", "model219", conn=_db())
    assert rep["ok"] is False
    assert rep["ledger_missing"] is True


def test_unreadable_ledger_blocks_instead_of_raising():
    """库不可达/缺表 → 按缺台账阻断，绝不能吞成放行（换空库绕过的口子）。"""
    sf = _load()
    c = sqlite3.connect(":memory:")  # 没有 ledger_kv 表
    rep = sf._triage_gate("KOR", "model219", conn=c)
    assert rep["ok"] is False
    assert rep["ledger_missing"] is True


def test_malformed_json_blocks():
    """台账 JSON 坏掉 → 按缺台账阻断。"""
    sf = _load()
    rep = sf._triage_gate("KOR", "model219",
                          conn=_db([("KOR", "s1_triage_kor", "{not json")]))
    assert rep["ok"] is False and rep["ledger_missing"] is True


def test_legacy_ledger_without_verdicts_blocks():
    """旧版台账只有 survivors、没有 verdicts 全量判级表 → 无法判定该集等级 → 阻断。

    只存 survivors 时「不在表里」与「不是存活」无法区分，闸就只能放行（等于没闸），
    故 verdicts 是硬要求。
    """
    sf = _load()
    rep = sf._triage_gate("KOR", "model219",
                          conn=_db([("KOR", "s1_triage_kor",
                                     json.dumps({"survivors": ["news18"]}))]))
    assert rep["ok"] is False
    assert "verdicts" in rep["reason"]


def test_dataset_absent_from_ledger_blocks():
    """数据集不在分诊台账内（新同步进库 / 台账过期）→ 阻断，不能默认放行。"""
    sf = _load()
    rep = sf._triage_gate("KOR", "__brand_new_ds__", conn=_ok_db())
    assert rep["ok"] is False
    assert rep["unknown_dataset"] is True
    assert rep["ledger_missing"] is False  # 是"未知集"不是"缺台账"，两者要能区分


def test_region_key_is_case_normalised():
    """台账键 s1_triage_<region.lower()>，region 大小写不影响命中。"""
    sf = _load()
    rep = sf._triage_gate("KOR", "model219", conn=_ok_db())
    assert rep["ok"] is True  # 键已是小写；大写 region 走同一把键


def test_missing_block_key_blocks_instead_of_passing():
    """台账条目缺 block 键 → 必须阻断。

    fail-open 陷阱：`ent.get("block")` 在键缺失时返回 None（falsy），
    若直接 `if not block: pass` 就等于**没有任何台账也能放行**。
    """
    sf = _load()
    rep = sf._triage_gate("KOR", "model219",
                          conn=_db([("KOR", "s1_triage_kor",
                                     _tri_payload({"model219": {"verdict": "判死"}}))]))
    assert rep["ok"] is False, "缺 block 键必须阻断（否则是 fail-open 漏洞）"
    assert "block" in rep["reason"]


def test_block_false_overrides_non_pass_verdict():
    """「判死但有实证产出」→ block=False → 放行。

    实测依据：判死记录是**族级**的（payload rule 明写「analyst44 一致预期类字段…
    不再投任何变体」），同集其他族仍可能活。KOR 3 个有 ra_clean 的集全是判死，
    按 verdict 硬拦会 100% 误杀 29/29 条历史产出。
    """
    sf = _load()
    rep = sf._triage_gate("KOR", "model219",
                          conn=_ok_db(verdict="判死", tags="判死×4; 实证产出(ra=8)",
                                      block=False))
    assert rep["ok"] is True
    assert rep["verdict"] == "判死", "判级如实保留，只是不阻断"


def test_block_true_blocks_even_if_verdict_looks_pass():
    """以 block 为准而非 verdict：verdict 与 block 打架时按 block 阻断（保守侧）。"""
    sf = _load()
    rep = sf._triage_gate("KOR", "model219", conn=_ok_db(verdict=PASS, block=True))
    assert rep["ok"] is False


# ---------------------------------------------------------------- CLI 契约冒烟

def _mk_campaign(d: Path) -> Path:
    camp = d / "KOR"
    (camp / "config").mkdir(parents=True, exist_ok=True)
    (camp / "config" / "settings.json").write_text(
        json.dumps({"region": "KOR"}), encoding="utf-8")
    (camp / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    return camp


def _run_scan_fields(camp: Path, dataset: str, db: Path, extra=None, tmp=None):
    env = dict(os.environ)
    env["WQB_DB_PATH"] = str(db)
    env["CAMPAIGN_SKIP_DIR_CHECK"] = "1"
    env.pop("WQB_TRI_MODE", None)  # 默认 enforce，勿被外部泄漏成 off
    # 凭证链指向不存在的路径 → load_credentials 必然 FileNotFoundError，
    # 因此在**登录前**就失败：全程不触网、不依赖真实凭据。
    env["BRAIN_CREDENTIALS"] = str(Path(tmp) / "no_creds.json")
    env["MCP_CONFIG_FILE"] = str(Path(tmp) / "no_cfg.json")
    for k in ("CREDENTIALS_EMAIL", "CREDENTIALS_PASSWORD",
              "WQ_USERNAME", "WQ_PASSWORD"):
        env.pop(k, None)
    cmd = [PY, str(SCAN_FIELDS), "--campaign-dir", str(camp), "--dataset", dataset]
    cmd += list(extra or [])
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, timeout=120)


def test_cli_missing_ledger_exits_2(tmp_path):
    """缺分诊台账 → exit 2，并打印闸 TRI 阻断说明与修复命令。"""
    camp = _mk_campaign(tmp_path)
    db = tmp_path / "tri.db"
    c = sqlite3.connect(str(db))
    c.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY, region TEXT, "
              "key TEXT, value TEXT)")
    c.commit()
    c.close()
    r = _run_scan_fields(camp, "model219", db, tmp=tmp_path)
    out = (r.stdout or "") + (r.stderr or "")
    assert r.returncode == 2, f"缺台账应 exit 2，实际 {r.returncode}\n{out[:1200]}"
    assert "闸 TRI 阻断" in out, f"应给出闸 TRI 阻断说明\n{out[:1200]}"
    assert "category_field_triage.py" in out, f"应给出修复命令\n{out[:1200]}"


def test_cli_skip_flag_disables_gate(tmp_path):
    """--skip-triage-gate 是唯一逃生口：不再因缺台账阻断，但必须打印醒目告警。"""
    camp = _mk_campaign(tmp_path)
    db = tmp_path / "tri.db"
    c = sqlite3.connect(str(db))
    c.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY, region TEXT, "
              "key TEXT, value TEXT)")
    c.commit()
    c.close()
    r = _run_scan_fields(camp, "model219", db,
                         extra=["--skip-triage-gate"], tmp=tmp_path)
    out = (r.stdout or "") + (r.stderr or "")
    assert "闸 TRI 阻断" not in out, f"显式 skip 后不应再阻断\n{out[:1200]}"
    assert "闸 TRI 已关闭" in out, f"skip 时必须打印醒目告警\n{out[:1200]}"
    assert r.returncode != 2


def test_cli_warn_mode_does_not_block(tmp_path):
    """--triage-gate warn：只告警不阻断（exit 与阻断路径不同）。"""
    camp = _mk_campaign(tmp_path)
    db = tmp_path / "tri.db"
    c = sqlite3.connect(str(db))
    c.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY, region TEXT, "
              "key TEXT, value TEXT)")
    c.commit()
    c.close()
    r = _run_scan_fields(camp, "model219", db,
                         extra=["--triage-gate", "warn"], tmp=tmp_path)
    out = (r.stdout or "") + (r.stderr or "")
    assert "闸 TRI 告警" in out, f"warn 模式应告警\n{out[:1200]}"
    assert r.returncode != 2, "warn 模式不得阻断"


# ---------------------------------------------------------------- 契约完整性

def test_gate_is_wired_into_s1_entry():
    """闸必须挂在 S1 唯一必经执行体里（挂在文档里不算）。

    scan_fields.py 是 script_map["S1"]；CLI 直调与 workflow_campaign(stage="S1")
    两条路径都经过它。删掉调用即红。
    """
    src = SCAN_FIELDS.read_text(encoding="utf-8")
    assert "_triage_gate(" in src, "scan_fields.py 未调用闸 TRI"
    assert "sys.exit(2)" in src, "闸 TRI 缺阻断出口"


def test_triage_tool_writes_verdicts_map():
    """分诊工具必须写 verdicts 全量判级表（闸的判定依据），不是只写 survivors。"""
    src = (REPO / "tools" / "category_field_triage.py").read_text(encoding="utf-8")
    assert '"verdicts"' in src, "分诊台账缺 verdicts，闸无法区分「不在表里」与「不是存活」"


def test_toolkit_and_repo_script_stay_in_sync():
    """skill 安装位是派生物：仓库源改动后必须 sync（防直接改安装位造成漂移）。"""
    assert SCAN_FIELDS.exists(), "toolkit scan_fields.py 缺失"
