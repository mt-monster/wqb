# -*- coding: utf-8 -*-
"""skills 审查 S-D（引擎与执行层，2026-09-29）：matrix / toolkit / wqb-concurrency / sim-alphas / inspect-raw 的文档 ↔ 代码一致性。

这些 skill 此前的共同病根是「文档是一份追加式日志，代码已经改了、文档没跟」：闸数与闸名、探针阈值、
并发数、配额闸缺省、已归档脚本仍被当作可用命令……本测试把每一处「文档写了数字 / 名单」的地方
绑到代码上——代码改了而文档没改，这里会红。
"""
import importlib
import json
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SKILLS = REPO / "Claude" / "skills"
TK = SKILLS / "wq-brain-campaign-toolkit"
TK_SCRIPTS = TK / "scripts"
for _p in (REPO / "src", REPO / "tools", TK_SCRIPTS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

SIX = ("wq-brain-campaign-matrix", "wq-brain-campaign-toolkit", "wqb-concurrency",
       "brain-sim-alphas-in-batch-and-track", "brain-inspect-raw-template-create-setting")


def _read(p):
    return Path(p).read_text(encoding="utf-8")


def _skill(name):
    return _read(SKILLS / name / "SKILL.md")


def _ref(name):
    return _read(TK / "references" / name)


# ----------------------------------------------------------------------------- 全体：结构

@pytest.mark.parametrize("name", SIX)
def test_description_is_a_short_trigger_statement(name):
    m = re.search(r'^description:\s*"(.*)"\s*$', _skill(name), re.M)
    assert m, name
    assert 60 <= len(m.group(1)) <= 220, f"{name}: description {len(m.group(1))} 字（应是触发场景，不是功能清单）"


@pytest.mark.parametrize("name", SIX)
def test_boundary_section_directly_follows_h1(name):
    body = _skill(name).split("---", 2)[2]
    assert re.match(r"\s*# [^\n]+\n\n## 职责边界\n", body), f"{name}: 「## 职责边界」必须紧跟 H1"


# ----------------------------------------------------------------------------- matrix

def test_matrix_allowed_tools_match_the_body():
    t = _skill("wq-brain-campaign-matrix")
    head = t.split("---", 2)[1]
    for tool in ("get_region_config", "get_dead_ends", "get_campaigns", "get_cross_region_lessons"):
        assert f"mcp__wqb-db__{tool}" in head and f"mcp__wqb-db__{tool}" in t.split("---", 2)[2]
    assert not re.search(r"mcp__wqb-db__(upsert|seal)_", head), "matrix 只读：写入调用序列归 RA 步 9"


def test_matrix_storage_map_and_registry_schema_follow_the_contract():
    from wqb import registry_contract as rc
    t = _skill("wq-brain-campaign-matrix")
    assert "cross_region_lessons" in t and "已废弃" in t          # 旧表只以「已废弃」出现
    for layer, fields in rc.REQUIRED.items():
        row = next((ln for ln in t.splitlines() if ln.startswith(f"| `{layer}` |") and "entry_id" not in ln
                    and ln.count("|") >= 5 and "必填" not in ln and "`" in ln.split("|")[2]), None)
        assert row, f"回写规范表缺 {layer} 行"
        for f in fields:
            assert f"`{f}`" in row, f"{layer} 行没写必填字段 {f}"
    assert "唯一一张" in t and "「层」一词只指" in t


def test_matrix_config_package_has_the_promised_fields_and_no_copied_dispatch_chain():
    t = _skill("wq-brain-campaign-matrix")
    for f in ("prod_risk", "prod_saturation", "excluded_families", "candidate_datasets", "entry_verdict"):
        assert f in t, f
    assert "超集" in t and "不是白名单" in t
    for chain_word in ("workflow_batch_track", "submit_verdict", "workflow_submit_alpha", "upsert_wave_result"):
        assert chain_word not in t, f"matrix 又复制了九步派发链（{chain_word}）——只该交还 ra-pipeline"
    assert "cross_region_lessons" not in re.findall(r"\| `cross_region_lessons` \|", t)


def test_matrix_prod_saturation_reads_the_single_region_status_implementation():
    import region_status
    from wqb.store import CampaignStore
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        db = Path(d) / "wqb.db"
        CampaignStore(str(db)).close()
        import sqlite3
        conn = sqlite3.connect(str(db))
        try:
            out = region_status.region_status(conn, "KOR")
        finally:
            conn.close()
    assert "pass_ge_158" in out and "suggested_action" in out
    t = _skill("wq-brain-campaign-matrix")
    assert "pass_ge_158" in t and "≥ 10" in t


def test_index_has_the_single_new_region_checklist_and_matrix_links_it():
    idx = _read(SKILLS / "INDEX.md")
    assert "### 开新区检查表" in idx
    for landing in ("config.py::REGIONS", "tracking/<R>/config/", "regions/<R>.md", "区域清单"):
        assert landing in idx.split("### 开新区检查表", 1)[1].split("\n## ", 1)[0]
    assert "INDEX §开新区检查表" in _skill("wq-brain-campaign-matrix")


# ----------------------------------------------------------------------------- toolkit：SKILL

def test_toolkit_subcommand_table_is_complete_and_archived_scripts_are_not_offered():
    import campaign
    t = _skill("wq-brain-campaign-toolkit")
    table = t.split("## 6. 子命令一览", 1)[1].split("## 7.", 1)[0]
    for sub in list(campaign.SUBCOMMANDS) + ["ledger", "registry", "wave"]:
        assert f"| `{sub}` |" in table, f"子命令表缺 {sub}"
    for script in sorted(TK_SCRIPTS.glob("*.py")):
        assert script.name in t, f"toolkit SKILL 没提到 scripts/{script.name}"
    # 2026-09-30：归档清单改为「git 记录 ∪ 磁盘」的并集。
    # 原来只 glob 磁盘，而 attic/ 在 .gitignore 中 —— 工作区里该目录可能已被清空
    # （本次实测：目录不存在，但 git 仍跟踪 7 个 .py，处于「已删未暂存」状态），
    # 于是 archived 只剩硬编码的 10 个，撞破 >=15 的断言。归档事实的权威是
    # git（移动而非删除，历史完整保留），故以 git 为准、磁盘为补充。
    import subprocess
    attic_dir = REPO / "attic" / "toolkit_zero_ref_20260928"
    archived = set()
    if attic_dir.is_dir():
        archived |= {p.stem for p in attic_dir.glob("*.py")}
    try:
        r = subprocess.run(["git", "ls-files", str(attic_dir.relative_to(REPO)).replace("\\", "/")],
                           cwd=str(REPO), capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            archived |= {Path(x).stem for x in r.stdout.splitlines()
                         if x.endswith(".py") and "zero_ref" in x}
    except (OSError, subprocess.SubprocessError):
        pass  # 非 git 环境（如打包副本）退回纯磁盘判断
    archived |= {"migrate_templates", "compose_signals", "param_opt", "ortho_prescreen", "proxy_prescreen",
                 "rescue_checklist", "calibrate_probe", "fit_mix_weights", "build_mix", "diversity_slots"}
    assert len(archived) >= 15
    for name in archived:
        assert not (TK_SCRIPTS / f"{name}.py").exists(), f"{name} 已归档，scripts/ 里不该还有"
        for ln in t.splitlines():
            if re.search(rf"\b{name}\b", ln):
                assert "归档" in ln or "attic" in ln, f"已归档脚本 {name} 出现在非「已归档」行：{ln[:80]}"


def test_toolkit_gate_facts_match_the_code():
    t = _skill("wq-brain-campaign-toolkit")
    assert "**8 闸 + 可选闸0**" in t                                   # 口径由 test_docs_consistency 同样守
    assert "闸 7（longCount）目前只有 WARN" in t and "没有任何代码读取区域 profile" in t
    src = (TK_SCRIPTS / "gate.py").read_text(encoding="utf-8")
    assert "longCount" in src and "< 80" in src
    for ln in t.splitlines():
        if "ts_event_" in ln:
            assert "没有" in ln or "作废" in ln, f"仍在教 ts_event_*：{ln[:80]}"
    assert "FAIL-CLOSED" in t and "自动续约" in t


def test_toolkit_quota_semantics_are_stated_as_the_code_behaves():
    t = _skill("wq-brain-campaign-toolkit")
    assert "缺省**不**因提交额度中止回测发起" in t
    assert "dispatch" in t and "submit" in t
    src = (TK_SCRIPTS / "pipeline.py").read_text(encoding="utf-8")
    assert "n_slots = min(2, n_total)" in src
    assert "pipeline.py` 没有任何提交 alpha 的动作" in t


def test_toolkit_write_matrix_names_the_single_implementations():
    t = _skill("wq-brain-campaign-toolkit")
    for impl in ("wqb.wave_results_contract.upsert_wave_result", "wqb.registry_contract",
                 "wqb.store.submit_queue", "docs/ledger_keys.json"):
        assert impl in t, impl
    assert "唯一正式写入方" not in t and "唯一权威实现" not in t
    for mod in ("wqb.wave_results_contract", "wqb.registry_contract", "wqb.store.submit_queue"):
        importlib.import_module(mod)


def test_toolkit_product_contract_keys_exist_in_the_ledger_catalog():
    cat = json.loads(_read(REPO / "docs" / "ledger_keys.json"))["entries"]
    norm = lambda k: re.sub(r"<[^<>]*>", "<>", k)               # noqa: E731
    known = {norm(e["key"]) for e in cat}
    section = _skill("wq-brain-campaign-toolkit").split("**产物契约", 1)[1].split("## 7.", 1)[0]
    tokens = set()
    for m in re.finditer(r"`([^`]+)`", section):
        tok = m.group(1)
        if re.fullmatch(r"[A-Za-z0-9_<>:]+", tok) and ("_" in tok) and "." not in tok and "--" not in tok:
            tokens.add(tok)
    # 只对「像 ledger 键的记号」较真：表名 / 工具名 / 概念名放行
    allow = {"wave_results", "backtest_results", "gate_results", "expressions", "fields", "region_kb",
             "methodology_rules", "ledger_kv", "dataset_health", "upsert_ledger_key", "workflow_campaign"}
    missing = sorted(t for t in tokens if norm(t) not in known and t not in allow)
    assert not missing, f"产物契约表里的键在 docs/ledger_keys.json 里没有登记：{missing}"


def test_fail_fast_link_resolves_from_the_repo_root():
    assert (REPO / "docs" / "experience" / "fail_fast_rules.md").is_file()
    assert "[`docs/experience/fail_fast_rules.md`](docs/experience/fail_fast_rules.md)" in _skill("wq-brain-campaign-toolkit")


# ----------------------------------------------------------------------------- toolkit：references

def test_gate_rules_lists_every_platform_poison_pattern_and_points_to_the_registry():
    pc = json.loads(_read(TK / "config" / "platform_constraints.json"))
    t = _ref("gate-rules.md")
    names = [p["name"] for p in pc["poison_patterns"]]
    for n in names:
        assert n in t, f"gate-rules 闸 5 没列 {n}"
    assert f"平台级 {len(names)} 条" in t
    assert "GATE_REGISTRY" in t and "唯一注册表" in t
    assert "diversity_slots.py --campaign-dir" not in t
    assert "FAIL-CLOSED" in t and "不是「过期就不再拦」" in t
    for wall in ("RN_EXPOSURE", "ROBUST_STRUCTURAL", "TVR_UNKNOWN", "2Y_UNKNOWN"):
        assert wall in t


def test_gate_rules_does_not_describe_the_file_era_build_wave():
    t = _ref("gate-rules.md")
    assert "<region>_wave*_exprs.json" not in t and "candidates/*.json" not in t
    assert "history_expressions" in t and "linear_mix" in t and "上限" in t
    assert "--enhance-diversity never" in t


def test_probe_scoring_numbers_are_the_code_defaults():
    import score_datasets
    import inspect
    src = inspect.getsource(score_datasets)
    assert 'h.get("tier1_score_pct", 0.6)' in src and 'h.get("tier2_score_pct", 0.3)' in src
    assert 'h.get("coverage_hard_min", 0.7)' in src
    t = _ref("probe-scoring-v2.md")
    assert "`tier1_score_pct` 缺省 0.6" in t and "`tier2_score_pct` 缺省 0.3" in t
    assert "`coverage_hard_min`）" not in t and "缺省 0.7" in t
    assert "P80" not in t.replace("旧版这里写的 P80 / P55", "")
    for banned in ("跨Category rank加法", "两两融合"):
        assert banned not in src, f"score_datasets 打印的 action 仍在推荐被禁的拼腿：{banned}"
    assert "不拼腿" in t
    pc = json.loads(_read(TK / "config" / "platform_constraints.json"))
    p6 = next(p for p in pc["probe_battery"] if p["probe"].startswith("P6"))
    assert "ts_zscore(F,66)" in p6["expr"] and "ts_zscore(F,66)" in t


def test_poll_and_quota_tables_equal_the_code_constants():
    import poller
    from wqb.config import CONCURRENCY, WAIT_THRESHOLDS
    t = _ref("poll-and-quota.md")
    for key, unit in (("init_interval", " s"), ("max_interval", " s")):
        assert f"| `{key}` | {poller.DEFAULT_POLL[key]}{unit} |" in t
    assert f"| `backoff_factor` | {poller.DEFAULT_POLL['backoff_factor']} |" in t
    assert poller.DEFAULT_POLL["stall_minutes"] == WAIT_THRESHOLDS["sim_stall_min"]
    assert "sim_stall_min" in t and "sim_timeout_min" in t
    assert CONCURRENCY["slots"] == 2 and "min(2" in t and "min(5" not in t
    assert "单批在飞" in t and "已废止" in t
    assert "不区分通道" in t and "POST /submit" in t


def test_ledger_schema_points_to_the_catalog_and_marks_legacy_keys():
    t = _ref("ledger-schema.md")
    assert "docs/ledger_keys.json" in t and "单事务" in t
    for ln in t.splitlines():
        if "set-verdict" in ln or "wave<N>_verdict" in ln:
            assert "废止" in ln or "已废止" in ln, ln[:80]
    assert "文件时代" in t and "step_funnel" in t


def test_campaign_dir_contract_marks_files_and_its_json_example_is_valid():
    t = _ref("campaign-dir-contract.md")
    m = re.search(r"```json\n(.*?)\n```", t, re.S)
    assert m and isinstance(json.loads(m.group(1)), dict), "settings 示例必须是合法 JSON（不能带 # 注释）"
    for tag in ("[必需]", "[可选]", "[历史]"):
        assert tag in t
    assert "config.py::GATES" in t and "signal_floor" in t and "stop_rules" in t
    assert "两版 schema 并存" in t


def test_selection_and_post_wave_pages_are_split_and_the_catalog_points_at_the_right_one():
    sel, post = _ref("selection-plan.md"), _ref("post-wave-reading.md")
    assert "research_leads" not in sel and "post-wave-reading.md" in sel
    assert "research_leads_w<W>" in post and "缺陷白名单" in post and "correction_plan" in post
    for term in ("资格线", "增强资格", "UNITS", "受保护状态"):
        assert term in sel + post
    cat = json.loads(_read(REPO / "docs" / "ledger_keys.json"))["entries"]
    e = next(x for x in cat if x["key"] == "research_leads_w<W>")
    assert e["writers"][0]["doc"].endswith("post-wave-reading.md")


def test_retired_docs_moved_to_attic_and_merged_page_is_short():
    attic = REPO / "attic" / "toolkit_docs_20260929"
    for name in ("enhancement-v2.md", "S2_COMPLIANCE_CHECKLIST.md", "S2_COMPLIANCE_GUIDE.md",
                 "DIVERSITY_EXTRACT_README.md", "DIVERSITY_EXTRACT_SUMMARY.md",
                 "DIVERSITY_EXTRACT_QUICKSTART.md", "README.md"):
        assert (attic / name).is_file(), name
    assert not list(TK.glob("DIVERSITY_EXTRACT_*")) and not (TK / "references" / "enhancement-v2.md").exists()
    assert len(_ref("diversity-extract.md").splitlines()) <= 60
    assert "diversity_extract.py" in _ref("diversity-extract.md")
    src = (TK_SCRIPTS / "_lib" / "diversity_extractor.py").read_text(encoding="utf-8")
    assert "_win = [5, 22, 66, 252]" in src and "[5, 10, 20, 60, 120, 250]" not in src


# ----------------------------------------------------------------------------- wqb-concurrency

def test_concurrency_numbers_are_pinned_to_one_source():
    import re as _re
    from wqb.config import CONCURRENCY
    import slots
    t = _skill("wqb-concurrency")
    assert CONCURRENCY["slots"] == 2 and CONCURRENCY["burst_capacity"] == 2
    monkey_env = __import__("os").environ.pop("WQB_GLOBAL_SLOTS", None)
    try:
        assert slots.global_cap() == CONCURRENCY["slots"]
    finally:
        if monkey_env is not None:
            __import__("os").environ["WQB_GLOBAL_SLOTS"] = monkey_env
    src = (TK_SCRIPTS / "pipeline.py").read_text(encoding="utf-8")
    assert _re.search(r"n_slots = min\(2, n_total\)", src)
    assert "`slots=2`" in t and "`WQB_GLOBAL_SLOTS`" in t
    assert "C=5" not in t.replace("旧的固定槽位 C=5", "").replace("「C=5、", "")


def test_conservative_envelope_constants_have_no_readers_yet_and_the_doc_says_so():
    hits = []
    for root in (REPO / "src", REPO / "tools", SKILLS):
        for p in root.rglob("*.py"):
            if "attic" in p.parts or "__pycache__" in p.parts:
                continue
            s = p.read_text(encoding="utf-8", errors="ignore")
            if "safe_instant_submits" in s or "min_batch_interval_sec" in s:
                hits.append(p.relative_to(REPO).as_posix())
    assert hits == ["src/wqb/config.py"], f"这两个常量有了读取方：{hits}——同步修 wqb-concurrency §1 的说法"
    assert "没有代码读取" in _skill("wqb-concurrency")


def test_concurrency_boundary_no_longer_swallows_the_ledger_loop():
    t = _skill("wqb-concurrency")
    assert "不管台账、复盘与选波" in t
    assert "每 10 波" not in t and "台账同步门（执行层硬门）" not in t
    assert "文件时代" in t and "step_funnel" in t
    for anchor in ("## 4. 🚨 孤儿模拟占槽", "## 8. 🌟 七槽填槽模式", "### 8.1 账户级槽位仲裁"):
        assert anchor in t, f"{anchor} 被其它文档引用（§4 / §8 / §8.1），编号不能变"
    assert "harvest_multisim_alphas" in t and "validate_fields" in t
    assert "agent 不读取 `.env`" in t


# ----------------------------------------------------------------------------- sim-alphas

def test_sim_alphas_entry_table_and_no_stale_claims():
    t = _skill("brain-sim-alphas-in-batch-and-track")
    table = t.split("## 入口选用表", 1)[1].split("**并发纪律", 1)[0]
    for entry in ("workflow_batch_track", "pipeline.py", "batch_simulator.py"):
        assert entry in table
    assert "唯一入口" not in t and "--batch-size 3" not in t and "--concurrency 2" not in t
    assert "不写 `settings.json`" in t
    assert "缺省 `never`" in t
    body_after_env = t.split("## 运行环境", 1)[1]
    assert not re.search(r"^python ", body_after_env, re.M)             # 不用裸 python
    for f in ("README.md", "reference.md", "examples.md"):
        s = _read(SKILLS / "brain-sim-alphas-in-batch-and-track" / f)
        assert "$env:BRAIN_PASSWORD" not in s and "--batch-size 3" not in s


def test_sim_alphas_credential_chain_matches_batch_simulator():
    src = _read(SKILLS / "brain-sim-alphas-in-batch-and-track" / "scripts" / "batch_simulator.py")
    assert 'os.environ.get("CREDENTIALS_EMAIL")' in src and 'os.environ.get("BRAIN_EMAIL")' in src
    t = _skill("brain-sim-alphas-in-batch-and-track")
    assert "CREDENTIALS_EMAIL" in t and "BRAIN_EMAIL" in t and "agent 不读取 `.env`" in t


# ----------------------------------------------------------------------------- inspect-raw

@pytest.fixture(scope="module")
def inspect_mod():
    skill = SKILLS / "brain-inspect-raw-template-create-setting"
    if str(skill) not in sys.path:
        sys.path.insert(0, str(skill))
    import importlib.util
    spec = importlib.util.spec_from_file_location("_bal_test", skill / "scripts" / "build_alpha_list.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_inspect_raw_optional_defaults_precedence(inspect_mod):
    out, src = inspect_mod.fill_optional({"region": "KOR", "nanhandling": "ON"},
                                         {"maxTrade": "ON", "decay": 4, "_multi_sim_batch_size": 8})
    assert out["nanhandling"] == "ON" and src["nanhandling"] == "settings_json"          # 显式给的优先
    assert out["maxtrade"] == "ON" and src["maxtrade"] == "campaign settings.json"       # 其次战役 settings
    assert out["decay"] == 4
    assert out["truncation"] == 0.08 and src["truncation"] == "脚本缺省"                  # 最后脚本缺省
    assert "_multi_sim_batch_size" not in out
    bare, srcs = inspect_mod.fill_optional({"region": "KOR"})
    assert bare["nanhandling"] == "OFF" and set(srcs.values()) == {"脚本缺省"}


def test_inspect_raw_doc_states_the_real_defaults_and_the_real_campaign_split(inspect_mod):
    t = _skill("brain-inspect-raw-template-create-setting")
    d = inspect_mod.OPTIONAL_DEFAULTS
    for key, shown in (("decay", "decay=0"), ("truncation", "truncation=0.08"), ("pasteurization", "pasteurization=ON"),
                       ("testperiod", "testPeriod=P0Y0M0D"), ("unithandling", "unitHandling=VERIFY"),
                       ("nanhandling", "nanHandling=OFF"), ("maxtrade", "maxTrade=OFF")):
        assert key in d and shown in t, shown
    import glob
    n_on = n_off = 0
    for p in glob.glob(str(REPO / "tracking" / "*" / "config" / "settings.json")):
        v = json.loads(_read(p)).get("nanHandling")
        n_on += v == "ON"
        n_off += v == "OFF"
    assert n_on and n_off, "战役 settings 不再是 ON/OFF 混用了？——同步修 inspect-raw 的「战役并不统一」一节"
    assert "--campaign-dir" in t and "不要假定脚本缺省 = 战役口径" in t


def test_inspect_raw_credentials_prefer_the_standard_names(tmp_path, monkeypatch):
    skill = SKILLS / "brain-inspect-raw-template-create-setting"
    if str(skill) not in sys.path:
        sys.path.insert(0, str(skill))
    from scripts.load_credentials import load_credentials
    monkeypatch.setenv("CREDENTIALS_EMAIL", "std@example.invalid")
    monkeypatch.setenv("CREDENTIALS_PASSWORD", "std-pass")
    monkeypatch.setenv("BRAIN_EMAIL", "legacy@example.invalid")
    monkeypatch.setenv("BRAIN_PASSWORD", "legacy-pass")
    assert load_credentials(skill_dir=tmp_path).username == "std@example.invalid"
    monkeypatch.delenv("CREDENTIALS_EMAIL")
    monkeypatch.delenv("CREDENTIALS_PASSWORD")
    assert load_credentials(skill_dir=tmp_path).username == "legacy@example.invalid"      # 旧别名仍认


def test_inspect_raw_boundary_no_longer_promises_a_settings_plan_or_ai_handoff():
    t = _skill("brain-inspect-raw-template-create-setting")
    assert "产出**设置计划**" not in t and "停止并交还" not in t and "交还控制权给 AI" not in t
    assert "GEM 节点已直接把表达式写进" in t and "互斥" in t
    src = _read(SKILLS / "brain-inspect-raw-template-create-setting" / "scripts" / "process_template.py")
    assert "ACTION REQUIRED FOR AI/AGENT" not in src and "--out-dir" in src
