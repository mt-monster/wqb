# -*- coding: utf-8 -*-
"""2026-09-27 四个 P1 的回归护栏（见 reports/ra_pipeline_stage_review_20260927.md §14.5 / §14.7）。

R18  priors 截断按"新登记优先"：新封存的死路不再因 entry_id 字母序排在后面而进不了 GEM
R19  战役库路径收敛：toolkit 各 store 与 get_store 同一解析；wave_gate 不再落硬编码盘符；
     只读路径不建库；节点子进程注入 WQB_WORKSPACE；WorkflowExecutor 不再用相对路径；
     补充（第三轮真实环境演练发现）：gate.py 找工作区 src/（op_arity / 家族天花板 / vector_wrap）
     与 toolkit 同一套解析，闸门环境缺失的结论不进逐条缓存
R20  verdict：写入契约拒绝时给出建议值（不自动采用）；判定表与历史写法对齐
R21  gate.py 逐条缓存键纳入数据集集合与白名单指纹；wave_gate 逐条回写 gated / fail
     （只因闸门环境缺失判 FAIL 的保持 pending）
"""
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
for _p in (REPO_ROOT / "src", REPO_ROOT / "tools", TOOLKIT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

KOR_CAMPAIGN = REPO_ROOT / "tracking" / "KOR"


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    return path


@pytest.fixture
def clean_env(monkeypatch):
    for k in ("WQB_DB_PATH", "WQB_WORKSPACE", "WQB_ROOT", "WQ_PROJECT_ROOT"):
        monkeypatch.delenv(k, raising=False)
    return monkeypatch


def _registry(db, rows):
    """按给定顺序登记 registry_empirical（id 自增 = 登记顺序）。rows: (layer, entry_id, payload)。"""
    conn = sqlite3.connect(str(db))
    for layer, eid, payload in rows:
        conn.execute(
            "INSERT INTO registry_empirical (region, layer, entry_id, family, payload, created_at, updated_at) "
            "VALUES ('KOR', ?, ?, ?, ?, '2026-09-27T00:00:00', '2026-09-27T00:00:00')",
            (layer, eid, payload.get("family") or payload.get("what"), json.dumps(payload, ensure_ascii=False)))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------- R18：新登记优先

def test_priors_keep_newest_dead_end_and_record_truncation(db_path, clean_env):
    import assemble_priors as ap
    from _lib.common import CampaignContext

    clean_env.setenv("WQB_DB_PATH", str(db_path))
    old = [f"KOR-A{i:02d}-DEAD" for i in range(12)]           # 字母序靠前、先登记
    _registry(db_path, [("dead_end", e, {"family": f"fam-{e}", "reason": "old"}) for e in old]
              + [("dead_end", "KOR-MODEL219-DEAD", {"family": "model219", "reason": "wave97 判死"})])

    payload = ap.assemble_priors_dict(CampaignContext(str(KOR_CAMPAIGN)))
    ids = [d.get("_entry_id") for d in payload["dead_ends"]]
    assert len(ids) == ap.MAX_DEADENDS == 12
    assert ids[0] == "KOR-MODEL219-DEAD"                      # 此前按字母序被截掉
    assert payload["_meta"]["truncated"]["dead_ends"] == ["KOR-A00-DEAD"]   # 最早登记的让位


def test_priors_wins_newest_first(db_path, clean_env):
    import assemble_priors as ap
    from _lib.common import CampaignContext

    clean_env.setenv("WQB_DB_PATH", str(db_path))
    _registry(db_path, [("win", f"KOR-W{i}", {"id": f"win-{i}", "what": f"win-{i}", "key": "k"})
                        for i in range(8)])
    payload = ap.assemble_priors_dict(CampaignContext(str(KOR_CAMPAIGN)))
    assert [w["id"] for w in payload["wins"]] == [f"win-{i}" for i in (7, 6, 5, 4, 3, 2)]
    assert payload["_meta"]["truncated"]["wins"] == ["win-1", "win-0"]


def test_registry_list_default_order_unchanged(db_path):
    from _lib.registry import RegistryStore

    _registry(db_path, [("dead_end", "KOR-A", {"family": "a"}), ("dead_end", "KOR-C", {"family": "c"}),
                        ("dead_end", "KOR-B", {"family": "b"})])
    rs = RegistryStore("KOR", db_path=str(db_path))
    assert [r["entry_id"] for r in rs.list("dead_end")] == ["KOR-A", "KOR-B", "KOR-C"]   # CLI 展示仍按字母序
    assert [r["entry_id"] for r in rs.list("dead_end", newest_first=True)] == ["KOR-B", "KOR-C", "KOR-A"]


# ---------------------------------------------------------------- R19：一次运行一个库

def _workspace(root, region="TST"):
    """最小工作区：<root>/src/wqb（标记）+ tracking/<region>/config/settings.json。"""
    (root / "src" / "wqb").mkdir(parents=True)
    camp = root / "tracking" / region
    (camp / "config").mkdir(parents=True)
    (camp / "config" / "settings.json").write_text(json.dumps({"region": region}), encoding="utf-8")
    (camp / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    return camp


def test_toolkit_stores_and_get_store_share_one_db(tmp_path, clean_env):
    from _lib.common import CampaignContext
    from _lib.ledger import SqliteLedgerStore
    from _lib.registry import RegistryStore
    from _lib.wave_results import WaveResultsStore
    from _lib.wqb_store import get_store, resolve_db_path

    camp = _workspace(tmp_path / "ws")
    clean_env.setenv("WQB_WORKSPACE", str(tmp_path / "elsewhere"))     # 战役目录上溯优先于它
    ctx = CampaignContext(str(camp))
    expected = str(tmp_path / "ws" / "data" / "wqb.db")
    assert resolve_db_path(ctx) == expected
    st = get_store(ctx)
    try:
        assert st.path == expected
    finally:
        st.close()
    assert SqliteLedgerStore("TST", ctx=ctx).db_path == expected
    assert RegistryStore("TST", ctx=ctx).db_path == expected
    assert WaveResultsStore("TST", ctx=ctx).db_path == expected


def test_toolkit_db_path_env_precedence(tmp_path, clean_env):
    from _lib import wqb_store

    clean_env.setenv("WQB_WORKSPACE", str(tmp_path / "ws_only"))        # 显式变量按原样采信
    assert wqb_store.resolve_db_path() == str(tmp_path / "ws_only" / "data" / "wqb.db")
    clean_env.setenv("WQB_DB_PATH", str(tmp_path / "x.db"))
    assert wqb_store.resolve_db_path(SimpleNamespace(dir=str(tmp_path))) == str(tmp_path / "x.db")


def test_legacy_root_is_gone(tmp_path, clean_env):
    """2026-09-29（X-14 / DEC-37）：作者本机盘符的「历史默认工作区」彻底移除——此前只在它存在时入选，
    仍是一条固定路径候选；现只认环境变量与「战役目录 / 本文件 / cwd 上溯」这些可验证的来源。

    2026-09-30 修正断言方式：原写法 `all("traeCN_project" not in r for r in
    _workspace_roots())` 在**仓库内**跑时必然失败——`_workspace_roots` 里的
    `_walk_up(__file__)` 从 toolkit 自身位置上溯，会合法地找到真仓库根（其路径
    本就含 traeCN_project）。那不是回归，是对「可验证来源」实现的误读。

    改用与本文件 test_wave_gate_db_path_never_hardcoded 一致的静态判据：
    直接检查源码里没有该盘符字面量。
    """
    from _lib import wqb_store

    assert not hasattr(wqb_store, "_LEGACY_ROOT")
    # 只扫**可执行代码**：模块的 docstring 里有「历史默认 `D:\...` 此前无条件兜底……
    # 彻底移除」这类变更记录，字面量出现在文档里是正确的，不能当成残留代码。
    # 用 ast 剔除所有字符串常量 / 注释后再查。
    import ast
    src = Path(wqb_store.__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    lines = src.splitlines()
    doc_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            doc_lines.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    offenders = [
        f"{wqb_store.__file__}:{i}"
        for i, line in enumerate(lines, 1)
        if "traeCN_project" in line and i not in doc_lines
    ]
    assert not offenders, f"可执行代码里仍有作者本机盘符: {offenders}"
    # 且解析结果必须来自可验证来源：每一条都应当真的含工作区标记
    for r in wqb_store._workspace_roots():
        assert (Path(r) / "src" / "wqb").is_dir() or (Path(r) / "data" / "wqb.db").exists(), (
            f"_workspace_roots 给出未验证的候选根: {r}")


def test_wave_gate_db_path_never_hardcoded(tmp_path, clean_env):
    import wave_gate

    assert wave_gate._wqb_db_path() == os.path.join(str(REPO_ROOT), "data", "wqb.db")
    camp = _workspace(tmp_path / "ws")
    assert wave_gate._wqb_db_path(str(camp)) == str(tmp_path / "ws" / "data" / "wqb.db")
    clean_env.setenv("WQB_DB_PATH", str(tmp_path / "x.db"))
    assert wave_gate._wqb_db_path(str(camp)) == str(tmp_path / "x.db")
    assert "traeCN_project" not in Path(wave_gate.__file__).read_text(encoding="utf-8")


def test_platform_category_is_read_only(tmp_path, clean_env):
    from wqb.workflow import _common

    missing = tmp_path / "missing.db"
    clean_env.setenv("WQB_DB_PATH", str(missing))
    assert _common._platform_category("analyst44") is None
    assert not missing.exists()                                          # 此前 sqlite3.connect 会建空库


def test_child_env_and_executor_default(clean_env):
    from wqb.workflow import _common
    from wqb.workflow.executor import WorkflowExecutor

    assert _common.unbuffered_env()["WQB_WORKSPACE"] == str(_common.REPO_ROOT)
    clean_env.setenv("WQB_WORKSPACE", "/custom")
    assert _common.unbuffered_env()["WQB_WORKSPACE"] == "/custom"       # 不覆盖已有值
    ex = WorkflowExecutor()
    assert os.path.isabs(ex.db_path) and ex.db_path == _common.resolve_db_path()


# ---------------------------------------------------------------- R21：缓存键 + 逐条回写

def test_gate_cache_key_depends_on_merged_whitelist():
    import gate

    one = gate.gate_signature(["ml_factor_proj"], ({"a"}, "MATRIX", {"a": "MATRIX"}, []), [], {"known_ops": ["rank"]})
    two = gate.gate_signature(["ml_factor_proj", "multi_source_model"],
                              ({"a", "b"}, "MATRIX", {"a": "MATRIX", "b": "MATRIX"}, []), [], {"known_ops": ["rank"]})
    assert one != two
    assert gate.cache_key("ml_factor_proj", "rank(b)", one) != gate.cache_key("ml_factor_proj", "rank(b)", two)
    again = gate.gate_signature(["ml_factor_proj"], ({"a"}, "MATRIX", {"a": "MATRIX"}, []), [],
                                {"known_ops": ["rank"]})
    assert one == again                                                 # 同输入同指纹：缓存仍然可命中


_STUB_GATE = "\n".join([
    "import json, sys",
    "args = sys.argv",
    "print(json.dumps({'all_pass': False, 'dataset': 'stubds', 'total': 3, 'passed': 1, 'cached': 0,",
    "    'diversity_gate': {'applied': False, 'pass': True, 'issues': []}, 'priors_gate': {'pass': True},",
    "    'report': [{'index': 1, 'expr': 'rank(close)', 'pass': True, 'issues': []},",
    "               {'index': 2, 'expr': 'rank(bogus_field)', 'pass': False,",
    "                'issues': ['[FIELD] 未验证字段: bogus_field']},",
    "               {'index': 3, 'expr': 'rank(open)', 'pass': False,",
    "                'issues': ['[ARITY_UNKNOWN] op_arity 不可达']}]}))",
    "sys.exit(1)",
])


def test_wave_gate_exprs_file_writes_back_gated_and_fail(tmp_path, clean_env):
    import importlib.util

    validator = REPO_ROOT / "Claude" / "skills" / "alpha-expression-verifier" / "scripts"
    if importlib.util.find_spec("ply") is None or not (validator / "validator.py").is_file():
        pytest.skip("wave_gate 语法闸依赖 alpha-expression-verifier + ply")
    toolkit = tmp_path / "toolkit"
    toolkit.mkdir()
    (toolkit / "gate.py").write_text(_STUB_GATE, encoding="utf-8")
    camp = tmp_path / "campaign"
    (camp / "config").mkdir(parents=True)
    (camp / "config" / "settings.json").write_text(json.dumps({"region": "TST"}), encoding="utf-8")
    ef = tmp_path / "exprs.txt"
    ef.write_text("rank(close)\nrank(bogus_field)\nrank(open)\n", encoding="utf-8")
    db = tmp_path / "data" / "wqb.db"
    CampaignStore(str(db)).close()
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    env = {k: v for k, v in os.environ.items() if k not in ("WQB_ROOT", "WQ_PROJECT_ROOT", "WQB_WORKSPACE")}
    env.update({"WQ_TOOLKIT_DIR": str(toolkit), "WQ_VALIDATOR_DIR": str(validator),
                "WQB_DB_PATH": str(db), "PYTHONIOENCODING": "utf-8"})
    r = subprocess.run([sys.executable, str(REPO_ROOT / "tools" / "wave_gate.py"), "--campaign-dir", str(camp),
                        "--dataset", "stubds", "--wave", "g1", "--exprs-file", str(ef), "--inspect-mode", "off",
                        "--skip-semantic-gate"],   # 隔离闸 SEM（本用例专测 R21 逐条状态回写）
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=str(cwd),
                       timeout=300)
    assert r.returncode == 1, r.stdout + r.stderr                        # FAIL 终态（不是 exit 2 的 ERROR）
    conn = sqlite3.connect(str(db))
    rows = dict(conn.execute("SELECT expression, status FROM expressions WHERE region='TST' AND wave='g1'"))
    conn.close()
    # 只因闸门环境缺失（[*_UNKNOWN]）判 FAIL 的保持 pending：那是"没校验"，不是"式子坏"
    assert rows == {"rank(close)": "gated", "rank(bogus_field)": "fail", "rank(open)": "pending"}
    assert "未判定 1" in r.stdout and "仅因闸门环境缺失" in r.stdout
    assert list(cwd.iterdir()) == []                                     # 不再在 cwd 造杂散目录


# ---------------------------------------------------------------- R19 补充：gate.py 的工作区解析（第三轮演练发现）

def test_gate_resolves_workspace_without_env(tmp_path, clean_env):
    import gate

    clean_env.delenv("WQB_WORKSPACE_ROOT", raising=False)
    clean_env.chdir(tmp_path)                                            # cwd 与仓库无关
    dirs = gate._workspace_src_dirs()
    # 仓库内 toolkit 自身上溯即得工作区（此前"上溯 5 级"落到仓库的上一级，.mcp.json env 又不含
    # WQB_ROOT：op_arity 不可达，KOR 真实环境 39/39 全记 [ARITY_UNKNOWN]）
    assert str(REPO_ROOT / "src") in dirs
    assert gate._load_arity_check() is not None
    assert gate._find_tools_lib() == str(REPO_ROOT / "tools" / "lib")
    camp = _workspace(tmp_path / "ws")
    assert gate._workspace_src_dirs(str(camp))[0] == str(tmp_path / "ws" / "src")    # 战役目录上溯优先


def test_gate_installed_copy_uses_workspace_env_and_never_caches_env_unknown(tmp_path, clean_env):
    import importlib.util
    import re
    import shutil

    validator = REPO_ROOT / "Claude" / "skills" / "alpha-expression-verifier" / "scripts"
    if importlib.util.find_spec("ply") is None or not (validator / "validator.py").is_file():
        pytest.skip("gate.py 语法闸依赖 alpha-expression-verifier + ply")
    # 安装位拷贝（~/.claude/skills/... 同构）：从自身位置上溯找不到工作区
    installed = tmp_path / "skills" / "wq-brain-campaign-toolkit"
    shutil.copytree(TOOLKIT.parent, installed, ignore=shutil.ignore_patterns("__pycache__"))
    camp = tmp_path / "KOR"
    (camp / "config").mkdir(parents=True)
    (camp / "config" / "settings.json").write_text(json.dumps({"region": "KOR"}), encoding="utf-8")
    (camp / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    (camp / "reference").mkdir()
    shutil.copy(KOR_CAMPAIGN / "reference" / "kor_ml_factor_proj_fields.json", camp / "reference")
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()
    cache = tmp_path / "gate_cache.json"
    env = {k: v for k, v in os.environ.items()
           if k not in ("WQB_ROOT", "WQ_PROJECT_ROOT", "WQB_WORKSPACE", "WQB_WORKSPACE_ROOT")}
    env.update({"WQB_DB_PATH": str(db), "WQ_VALIDATOR_DIR": str(validator), "PYTHONIOENCODING": "utf-8"})
    argv = [sys.executable, str(installed / "scripts" / "gate.py"), "--campaign-dir", str(camp),
            "--dataset", "ml_factor_proj", "--expr", "rank(change_6m_rating_revision)",
            "--cache-file", str(cache), "--skip-diversity-gate"]

    def run(extra):
        r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**env, **extra}, cwd=str(tmp_path), timeout=300)
        m = re.search(r"^\{.*", r.stdout, re.S | re.M)
        assert m, r.stdout + r.stderr
        return json.loads(m.group(0))

    if not os.path.isdir(r"D:\coding\traeCN_project\wqb\src\wqb"):     # 作者本机该盘符兜底仍在，那里跳过这半
        out = run({})
        assert out["report"][0]["issues"][0].startswith("[ARITY_UNKNOWN]")
        assert not cache.exists()                                        # 环境缺失的结论不入缓存
    out = run({"WQB_WORKSPACE": str(REPO_ROOT)})                         # 节点给子进程注入的变量（R19）
    assert out["passed"] == 1 and out["report"][0]["issues"] == []
    assert cache.exists()


# ---------------------------------------------------------------- R20：判定表 + 拒绝时给建议

def _kor_rejected_verdicts():
    from wqb.wave_results_contract import normalize_verdict

    out = {}
    for f in sorted((KOR_CAMPAIGN / "candidates").glob("wave*_result*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        if not isinstance(data, dict):        # wave_AL3_* 等批量列表工件不是单波结果 dict，跳过
            continue
        v = data.get("verdict")
        if v is not None and normalize_verdict(v)[0] is None:
            out[f.name.split("_result")[0].replace("wave", "")] = str(v)
    return out


def test_suggest_verdict_covers_real_rejected_history():
    from wqb.wave_results_contract import suggest_verdict

    rejected = _kor_rejected_verdicts()
    assert len(rejected) == 24                                          # 真实历史里被契约拒绝的写法
    sug = {w: suggest_verdict(v) for w, v in rejected.items()}
    assert all(sug.values()), [w for w, s in sug.items() if not s]     # 每条都有建议
    assert (sug["91c"]["verdict"], sug["91c"]["confidence"]) == ("PASS", "high")    # ✅ 2 RA 提交成功
    assert sug["104"]["verdict"] == "PASS"                              # 2 GREEN + 6 RED
    assert (sug["101"]["verdict"], sug["103"]["verdict"]) == ("FAIL", "FAIL")      # FULL_RED / 8/8 RED
    assert sug["87"]["verdict"] == sug["90"]["verdict"] == "PARTIAL"   # NEAR / 突破
    assert (sug["75b"]["verdict"], sug["75b"]["confidence"]) == ("FAIL", "low")    # no_submit


def test_verdict_from_counts_is_the_table():
    from wqb.wave_results_contract import verdict_from_counts

    assert verdict_from_counts(1, 0) == verdict_from_counts(2, 5) == "PASS"
    assert verdict_from_counts(0, 3) == "PARTIAL"
    assert verdict_from_counts(0, 0) == "FAIL"


def test_rejection_carries_suggestion_and_never_writes(db_path, monkeypatch):
    import importlib

    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    monkeypatch.setattr(mod, "DB_PATH", db_path)
    out = mod.upsert_wave_result("KOR", "91c", verdict="✅ 2 RA 提交成功 (88lr21xo + A1lb2KpR 均 ACTIVE)")
    assert "error" in out and out["suggestion"]["verdict"] == "PASS"
    assert "未自动采用" in out["error"] and "判定表" in out["error"]
    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT COUNT(*) FROM wave_results").fetchone()[0] == 0      # 建议不落库
    conn.close()
