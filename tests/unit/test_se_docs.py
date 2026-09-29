# -*- coding: utf-8 -*-
"""skills 审查 S-E（L0 / L1 / L2 技能，2026-09-29）：文档 ↔ 代码一致性。

这批 skill 的共同病根：文档写了工具名 / 参数 / 数字 / 命令，代码早已改了（或从来没有）——
`get_ny_time.py` 从未存在、`authenticate` 早已没有参数却仍教「传邮箱和口令」、`imb5_mktcap` 被引擎的合规约束排除却
被示例当上下文、三份 `validator.py` 各自演化……本测试把每一处「文档写了名字 / 数字 / 名单」的地方绑到代码上。
"""
import ast
import filecmp
import importlib.util
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "Claude" / "skills"
MCP_DIR = REPO / "world-quant-brain-mcp"
for _p in (REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

SE_SKILLS = (
    "brain-next-move-analysis",
    "alpha-template-labs-data-analysis",
    "alpha-expression-verifier",
    "brain-feature-implementation",
    "brain-dataset-mining-experience",
)


def _read(p):
    return Path(p).read_text(encoding="utf-8")


def _skill(name):
    return _read(SKILLS / name / "SKILL.md")


def _mcp_tools(path):
    """path 里被 `@mcp.tool()` 装饰的函数 → {名字: ast 节点}。"""
    tree = ast.parse(_read(path))
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for d in node.decorator_list:
                target = d.func if isinstance(d, ast.Call) else d
                if isinstance(target, ast.Attribute) and target.attr == "tool":
                    out[node.name] = node
    return out


def _all_http_tools():
    out = {}
    for p in sorted(MCP_DIR.glob("tools_*.py")):
        out.update(_mcp_tools(p))
    return out


def _all_db_tools():
    return _mcp_tools(REPO / "wqb_db_mcp.py")


def _params(node):
    """函数的参数名列表（不含 self）。"""
    a = node.args
    return [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs if x.arg != "self"]


def _required_params(node):
    a = node.args
    pos = a.posonlyargs + a.args
    n_def = len(a.defaults)
    req = [x.arg for x in pos[: len(pos) - n_def] if x.arg != "self"]
    req += [x.arg for x, d in zip(a.kwonlyargs, a.kw_defaults) if d is None]
    return req


def _cited_tools(text, prefix):
    """文本里 `mcp__<server>__<tool>` 形式引用的工具名（去掉 `*` 通配）。"""
    return sorted({m for m in re.findall(prefix + r"__([A-Za-z0-9_]+)", text) if m})


# ----------------------------------------------------------------------------- 全体：结构

@pytest.mark.parametrize("name", SE_SKILLS)
def test_description_is_a_short_trigger_statement(name):
    m = re.search(r'^description:\s*"?(.*?)"?\s*$', _skill(name), re.M)
    assert m, name
    assert 60 <= len(m.group(1)) <= 260, f"{name}: description {len(m.group(1))} 字（应是触发场景，不是功能清单）"


@pytest.mark.parametrize("name", SE_SKILLS)
def test_boundary_section_directly_follows_h1(name):
    body = _skill(name).split("---", 2)[2]
    assert re.match(r"\s*# [^\n]+\n\n## 职责边界\n", body), f"{name}: 「## 职责边界」必须紧跟 H1"


@pytest.mark.parametrize("name", SE_SKILLS)
def test_no_host_specific_tool_or_author_environment_in_body(name):
    body = _skill(name).split("---", 2)[2]
    for bad in ("TaskCreate", "todo_write", "rtk python", "get_ny_time.py'"):
        assert bad not in body, f"{name}: 正文出现宿主 / 作者环境专有说法 {bad!r}"


# ----------------------------------------------------------------------------- NM：next-move

def _region_status_module():
    import region_status
    return region_status


def _mk_region_db(bt_sharpes=(), campaigns=()):
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE regions(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE backtest_results(region TEXT, sharpe REAL);
        CREATE TABLE alphas(region_id INTEGER, platform_status TEXT);
        CREATE TABLE waves(region_id INTEGER);
        CREATE TABLE registry_empirical(region TEXT, layer TEXT, payload TEXT);
        INSERT INTO regions VALUES (1, 'KOR');
    """)
    conn.executemany("INSERT INTO backtest_results VALUES ('KOR', ?)", [(s,) for s in bt_sharpes])
    conn.executemany("INSERT INTO registry_empirical VALUES ('KOR','campaign', ?)",
                     [(json.dumps({"status": s}),) for s in campaigns])
    return conn


def test_nm_region_status_thresholds_are_module_constants_and_drive_the_action():
    rs = _region_status_module()
    assert (rs.PASS_SHARPE_MIN, rs.PROD_SATURATION_MIN_PASS, rs.EXHAUSTED_FREEZE_PCT,
            rs.EXHAUSTED_MIN_CAMPAIGNS, rs.OPEN_CAMPAIGN_MAX_BACKTESTED) == (1.58, 10, 80.0, 5, 20)
    # 空库：以上皆不满足 → 继续观察
    assert rs.region_status(_mk_region_db(), "KOR")["suggested_action"] == rs.ACTION_WATCH
    # 达标数 = 阈值 → 继续（PROD 同质风险）；阈值 -1 不触发
    hit = [rs.PASS_SHARPE_MIN] * rs.PROD_SATURATION_MIN_PASS
    assert rs.region_status(_mk_region_db(hit), "KOR")["suggested_action"] == rs.ACTION_CONTINUE
    assert rs.region_status(_mk_region_db(hit[:-1]), "KOR")["suggested_action"] == rs.ACTION_WATCH
    # sharpe 略低于线不算达标
    assert rs.region_status(_mk_region_db([rs.PASS_SHARPE_MIN - 0.01] * 20), "KOR")["pass_ge_158"] == 0
    # 战役全穷尽且 >= 5 个 → 冻结/转区；4 个不够
    assert rs.region_status(_mk_region_db(campaigns=["exhausted"] * 5), "KOR")["suggested_action"] == rs.ACTION_FREEZE
    assert rs.region_status(_mk_region_db(campaigns=["exhausted"] * 4), "KOR")["suggested_action"] == rs.ACTION_WATCH
    # 有 untried 且回测 < 20 → 开战役候选；回测 >= 20 不算
    assert rs.region_status(_mk_region_db([0.1] * 3, ["untried"]), "KOR")["suggested_action"] == rs.ACTION_OPEN
    assert rs.region_status(_mk_region_db([0.1] * 20, ["untried"]), "KOR")["suggested_action"] == rs.ACTION_WATCH
    # 优先级：prod 同质 > 战役穷尽
    both = rs.region_status(_mk_region_db(hit, ["exhausted"] * 5), "KOR")
    assert both["suggested_action"] == rs.ACTION_CONTINUE


def test_nm_skill_action_table_matches_the_constants():
    rs = _region_status_module()
    t = _skill("brain-next-move-analysis")
    table = t.split("建议动作的判据", 1)[1].split("- **`entry_verdict`**", 1)[0]
    for label in (rs.ACTION_CONTINUE, rs.ACTION_FREEZE, rs.ACTION_OPEN, rs.ACTION_WATCH):
        assert label in table, label
    assert f"≥ {rs.PROD_SATURATION_MIN_PASS}" in table
    assert f"≥ {int(rs.EXHAUSTED_FREEZE_PCT)}%" in table
    assert f"≥ {rs.EXHAUSTED_MIN_CAMPAIGNS}" in table
    assert f"< {rs.OPEN_CAMPAIGN_MAX_BACKTESTED}" in table
    for const in ("PROD_SATURATION_MIN_PASS", "EXHAUSTED_FREEZE_PCT", "EXHAUSTED_MIN_CAMPAIGNS",
                  "OPEN_CAMPAIGN_MAX_BACKTESTED"):
        assert const in table and hasattr(rs, const), const


def test_nm_matrix_prod_saturation_shares_the_same_constant():
    rs = _region_status_module()
    m = _skill("wq-brain-campaign-matrix")
    assert f"≥ {rs.PROD_SATURATION_MIN_PASS}" in m and "pass_ge_158" in m


def test_nm_every_cited_mcp_tool_exists_and_arity_claims_hold():
    http, db = _all_http_tools(), _all_db_tools()
    text = _skill("brain-next-move-analysis") + _read(SKILLS / "brain-next-move-analysis" / "reference.md")
    # `mcp__wq-brain-http__<tool>` 与裸写的 `get_xxx(` 都要真实存在
    for name in _cited_tools(text, r"mcp__wq-brain-http"):
        assert name in http, f"wq-brain-http 没有工具 {name}"
    for name in _cited_tools(text, r"mcp__wqb-db"):
        assert name in db, f"wqb-db 没有工具 {name}"
    bare = set(re.findall(r"`(get_[a-z_]+|value_factor_trendScore|check_correlation|recommend_datasets|region_rotation)\(", text))
    for name in bare:
        assert name in http or name in db, f"文档引用的 {name}() 在两个 MCP 服务里都不存在"
    # 文档声称「authenticate 没有参数」「get_events 无参数」「趋势分数两个日期必填」——逐条绑到签名上
    assert _params(http["authenticate"]) == []
    assert _params(http["get_events"]) == []
    assert set(_required_params(http["value_factor_trendScore"])) == {"start_date", "end_date"}
    assert "random_string" not in text


def test_nm_reference_has_no_credential_passing_or_ghost_script_instruction():
    ref = _read(SKILLS / "brain-next-move-analysis" / "reference.md")
    sk = _skill("brain-next-move-analysis")
    assert "提供用户的电子邮件和密码" not in ref
    assert "不得读取**凭据文件" in ref and "不得向用户索要口令" in ref and "不得把口令传给任何工具" in ref
    assert not (REPO / "Claude" / "skills" / "brain-next-move-analysis" / "get_ny_time.py").exists()
    assert "没有 `get_ny_time.py`" in sk       # 只允许以「不存在」的方式出现
    assert "et_now" in sk                       # 取时唯一方式 = wqb.timeutil


def test_nm_time_snippet_actually_runs():
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0,'src'); from wqb.timeutil import et_now; print(et_now().isoformat())"],
        cwd=str(REPO), capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    assert re.match(r"\d{4}-\d\d-\d\dT\d\d:\d\d", out.stdout.strip())


def test_nm_region_list_is_not_hardcoded_and_config_regions_is_the_source():
    from wqb import config
    t = _skill("brain-next-move-analysis")
    assert "config.REGIONS" in t
    assert len(config.REGIONS) >= 14 and "DEU" in config.REGIONS and "JPN" in config.REGIONS
    assert not re.search(r"USA/EUR/KOR/IND/ASI/GBR", t), "不要在文档里写死区域名单"


# ----------------------------------------------------------------------------- LB：labs

def test_lb_labs_tools_and_agent_subcommands_exist():
    http = _all_http_tools()
    t = _skill("alpha-template-labs-data-analysis")
    for name in _cited_tools(t, r"mcp__wq-brain-http"):
        assert name in http, name
    agent = _read(MCP_DIR / "labs_data_analysis_agent.py")
    subs = set(re.findall(r'sub\.add_parser\(\s*"([a-z-]+)"', agent))
    for cmd in re.findall(r"^\| `([a-z-]+)(?: [^`]*)?` \|", t.split("### CLI 专用步骤", 1)[1].split("## 硬规则", 1)[0], re.M):
        if cmd in ("run-csv", "demo"):
            continue
        assert cmd in subs, f"文档列了不存在的子命令 {cmd}"
    assert {"run-csv", "demo"} <= subs


def test_lb_spec_classes_match_the_engine_classifier_and_spec_moved_into_the_skill():
    spec = _read(SKILLS / "alpha-template-labs-data-analysis" / "references" / "agent-spec.md")
    assert not (REPO / "docs" / "reference" / "brain-labs-data-analysis-agent.md").exists()
    tree = ast.parse(_read(MCP_DIR / "labs_data_analysis_agent.py"))
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "classify_field")
    classes = {r.value.value for r in ast.walk(fn)
               if isinstance(r, ast.Return) and isinstance(r.value, ast.Constant) and isinstance(r.value.value, str)}
    assert classes, "classify_field 没有字符串返回值？"
    for c in classes:
        assert f"`{c}`" in spec, f"引擎的形态类 {c} 没写进规范"
    listed = set(re.findall(r"^\| `([a-z_]+)` \|", spec.split("## 4.", 1)[1].split("## 5.", 1)[0], re.M))
    listed.discard("field_classification")          # 表头
    assert listed == classes


def test_lb_default_example_respects_the_engine_market_data_constraint():
    pytest.importorskip("pandas")
    pytest.importorskip("numpy")
    # 引擎依赖同目录的 `scripts` 包——在子进程里以 MCP 目录为 cwd 加载，避免与 inspect-raw 的同名 scripts 包互相污染
    code = ("import json, labs_data_analysis_agent as m; print(json.dumps(["
            "m.is_direct_market_data_field('imb5_mktcap', 'Market capitalization of security in regional currency units'),"
            "m.is_direct_market_data_field('imb5_score', 'SHIELD-OIL composite score (0-1)')]))")
    out = subprocess.run([sys.executable, "-c", code], cwd=str(MCP_DIR), capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr[-600:]
    assert json.loads(out.stdout.strip().splitlines()[-1]) == [True, False]
    t = _skill("alpha-template-labs-data-analysis")
    ex = t.split("## 默认示例", 1)[1]
    assert "imb5_mktcap" in ex and "只用它做相关性诊断" in ex and "不做" in ex


def test_lb_human_pause_and_labs_paths_are_explicit():
    t = _skill("alpha-template-labs-data-analysis")
    assert "【人工 · 在此暂停】" in t and "在收到 JSON 之前不得继续" in t
    assert "【需用户同意】" in t
    assert "Labs 里（Linux JupyterLab）" in t     # /tmp/... 是 Labs 内路径
    assert "tracking/_scratch/" in t
    src = _read(MCP_DIR / "tools_labs.py")
    assert "/tmp/labs_data_analysis_result.json" in src       # MCP 缺省值也是 Labs 内路径
    # ingest_labs_result 只解析返回，不落盘（文档这么说）
    lf = _read(MCP_DIR / "labs_functions.py")
    body = lf.split("async def ingest_labs_result", 1)[1].split("# Singleton", 1)[0]
    assert "write_text" not in body and "open(" not in body


# ----------------------------------------------------------------------------- EV：verifier

VERIFIER = SKILLS / "alpha-expression-verifier" / "scripts"


def _load_validator():
    # ply.lex 要从 sys.modules 里按 __module__ 找 __file__，所以必须先注册再执行
    name = "ev_validator_under_test"
    spec = importlib.util.spec_from_file_location(name, VERIFIER / "validator.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_ev_documented_examples_match_real_validator_output():
    pytest.importorskip("ply")
    v = _load_validator().ExpressionValidator()
    t = _skill("alpha-expression-verifier")
    table = t.split("## 示例（真实输出", 1)[1].split("## 常见错误", 1)[0]
    rows = re.findall(r"^\| `([^`]+)` \| `(true|false)` \| (.+?) \|$", table, re.M)
    assert len(rows) >= 6
    for expr, valid, errs in rows:
        res = v.check_expression(expr)
        assert str(res["valid"]).lower() == valid, expr
        for e in re.findall(r'"([^"]+)"', errs):
            assert e in res["errors"], f"{expr}: 文档的错误文本 {e!r} 不在真实输出 {res['errors']}"
        if valid == "true":
            assert res["errors"] == []


def test_ev_invalid_expression_exits_zero_and_errors_exit_one():
    pytest.importorskip("ply")
    script = str(VERIFIER / "verify_expr.py")
    bad = subprocess.run([sys.executable, script, "rank(close"], capture_output=True, text=True, timeout=60)
    assert bad.returncode == 0 and json.loads(bad.stdout)["valid"] is False     # 文档：非法表达式也以 0 退出
    none = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=60)
    assert none.returncode == 1 and "No expression provided" in json.loads(none.stdout)["errors"][0]
    t = _skill("alpha-expression-verifier")
    assert "退出码不表示合法与否" in t and "No expression provided" in t


def test_validator_copies_are_byte_identical_to_the_verifier_authority():
    """三份副本曾各自演化（hump / bucket / densify 的修复只落在权威版）；现在逐字节镜像，改一处必须四处一起改。"""
    canon = VERIFIER / "validator.py"
    copies = [
        SKILLS / "brain-feature-implementation" / "scripts" / "validator.py",
        SKILLS / "brain-make-some-gem" / "scripts" / "trailSomeAlphas" / "skills"
        / "brain-feature-implementation" / "scripts" / "validator.py",
        SKILLS / "brain-inspect-raw-template-create-setting" / "scripts" / "validator.py",
    ]
    for c in copies:
        assert c.is_file(), c
        assert filecmp.cmp(canon, c, shallow=False), (
            f"{c.relative_to(REPO)} 与权威版不同——按 validator.py 文件头「单一来源」一节四处一起覆盖")
    assert "单一来源" in _read(canon).split('"""', 2)[1]


def test_ev_stale_copies_would_have_let_the_2026_incidents_through():
    """回归：hump 位置参数 / bucket 缺 range 是两起真实事故（整批 CANCEL），权威版必须拦住。"""
    pytest.importorskip("ply")
    v = _load_validator().ExpressionValidator()
    assert not v.check_expression("hump(rank(close), 0.005)")["valid"]
    assert not v.check_expression("bucket(rank(cap))")["valid"]


def test_ev_docs_reference_paths_that_exist():
    t = _skill("alpha-expression-verifier")
    for rel in ("Claude/skills/alpha-expression-verifier/scripts/verify_expr.py",
                "wq-brain-campaign-toolkit/scripts/_lib/skill_roots.py"):
        assert rel in t, rel
    assert (REPO / "Claude/skills/alpha-expression-verifier/scripts/verify_expr.py").is_file()
    assert (SKILLS / "wq-brain-campaign-toolkit/scripts/_lib/skill_roots.py").is_file()
    assert "get_operators" in _all_http_tools()


# ----------------------------------------------------------------------------- FI：feature-implementation

FI = SKILLS / "brain-feature-implementation"
FI_EMBEDDED = SKILLS / "brain-make-some-gem" / "scripts" / "trailSomeAlphas" / "skills" / "brain-feature-implementation"


def test_fi_embedded_copy_is_identical_to_the_top_level_skill():
    cmp = filecmp.dircmp(FI, FI_EMBEDDED, ignore=["__pycache__"])

    def walk(c):
        assert not c.left_only and not c.right_only and not c.diff_files, (c.left_only, c.right_only, c.diff_files)
        for sub in c.subdirs.values():
            walk(sub)
    walk(cmp)


def test_fi_skill_text_is_not_spliced_into_the_gem_prompt():
    """FI SKILL.md 文档声称「GEM prompt 不拼入本文件」：build_prompt 只接收、不使用该参数。"""
    src = _read(SKILLS / "brain-make-some-gem" / "scripts" / "trailSomeAlphas" / "pipeline_prompts.py")
    fn = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "build_prompt")
    used = [n for n in ast.walk(fn) if isinstance(n, ast.Name) and n.id == "feature_implementation_skill_md"
            and isinstance(n.ctx, ast.Load)]
    assert not used, "build_prompt 现在使用了 FI 文本——同步改 brain-feature-implementation/SKILL.md「与 GEM 引擎的关系」一节"


def test_fi_documented_cli_flags_and_universe_source_exist():
    from wqb import config
    imp = _read(FI / "scripts" / "implement_idea.py")
    t = _skill("brain-feature-implementation")
    for flag in ("--template", "--dataset", "--idea", "--max-expressions", "--no-lint", "--field-whitelist",
                 "--field-profile", "--family-match"):
        assert f'"{flag}"' in imp and flag in t, flag
    assert 'default=24' in imp and "缺省 24" in t
    fetch = _read(FI / "scripts" / "fetch_dataset.py")
    for flag in ("--datasetid", "--region", "--delay", "--universe", "--data-type"):
        assert f'"{flag}"' in fetch and flag in t, flag
    assert all("default_universe" in cfg for cfg in config.REGIONS.values())
    assert config.REGIONS["KOR"]["default_universe"] == "TOP600"


def test_fi_fetch_dataset_takes_standard_env_credentials_without_config_json(tmp_path, monkeypatch, capsys):
    """凭据来源：CREDENTIALS_* 优先，config.json 只在环境变量不全时才需要；登录时不回显邮箱。"""
    stub = type(sys)("ace_lib")

    def _boom():
        raise RuntimeError("STOP_AT_LOGIN")
    stub.start_session = _boom
    stub.get_credentials = None
    monkeypatch.setitem(sys.modules, "ace_lib", stub)
    for k in ("BRAIN_USERNAME", "BRAIN_EMAIL", "BRAIN_PASSWORD"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("CREDENTIALS_EMAIL", "someone@example.invalid")
    monkeypatch.setenv("CREDENTIALS_PASSWORD", "not-a-real-password")
    monkeypatch.setenv("WQB_GEM_DATA_ROOT", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["fetch_dataset.py", "--datasetid", "x1", "--region", "USA"])
    spec = importlib.util.spec_from_file_location("fi_fetch_under_test", FI / "scripts" / "fetch_dataset.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert not (FI / "config.json").exists()
    with pytest.raises(SystemExit) as ei:
        mod.main()
    out = capsys.readouterr().out
    assert ei.value.code == 1 and "STOP_AT_LOGIN" in out          # 走到了登录，说明凭据阶段已通过
    assert "someone@example.invalid" not in out and "not-a-real-password" not in out
    assert "credentials missing" not in out


def test_fi_fetch_dataset_without_any_credentials_says_how_to_fix(tmp_path, monkeypatch, capsys):
    stub = type(sys)("ace_lib")
    stub.start_session = lambda: None
    monkeypatch.setitem(sys.modules, "ace_lib", stub)
    for k in ("CREDENTIALS_EMAIL", "CREDENTIALS_PASSWORD", "BRAIN_USERNAME", "BRAIN_EMAIL", "BRAIN_PASSWORD"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("WQB_GEM_DATA_ROOT", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["fetch_dataset.py", "--datasetid", "x1"])
    spec = importlib.util.spec_from_file_location("fi_fetch_under_test2", FI / "scripts" / "fetch_dataset.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if (FI / "config.json").exists():
        pytest.skip("本机 skill 目录里有 config.json")
    with pytest.raises(SystemExit) as ei:
        mod.main()
    assert ei.value.code == 1 and "CREDENTIALS_EMAIL" in capsys.readouterr().out


# ----------------------------------------------------------------------------- ME：mining-experience

def test_me_documented_flags_markers_and_status_words_exist():
    from wqb.research import dataset_experience as de
    t = _skill("brain-dataset-mining-experience")
    assert de.BEGIN.strip("<!-> ") in t and de.END.strip("<!-> ") in t
    src = _read(REPO / "src" / "wqb" / "research" / "dataset_experience.py")
    for word in ("UPDATED", "UNCHANGED", "DRY-RUN", "rows=", "--dry-run", "--waves", "choices=[0, 1]"):
        assert word in src, word
    for word in ("UPDATED", "UNCHANGED", "DRY-RUN", "--dry-run", "--waves"):
        assert word in t, word
    assert "s6_verdict_<wave>` 已废止" in t
    assert "upsert_wave_result" in t and "seal_dead_end" in t


def test_me_grep_tokens_in_the_verification_step_are_in_the_generated_block():
    from wqb.research import dataset_experience as de
    ev = {"region": "KOR", "waves_filter": ["245"], "delay_filter": 1, "catalogs": {}, "warnings": [],
          "rows": [{"dataset": "news46", "wave": "245", "alpha_id": "A1", "fields": ["f1"], "sharpe": 0.4,
                    "fitness": 0.1, "turnover": 0.3, "two_year_sharpe": 0.2, "sub_universe_sharpe": 0.1,
                    "robust": None, "prod_correlation": None, "self_correlation": None, "code": "rank(f1)",
                    "failed_checks": [], "delay": 1, "universe": "TOP600", "neutralization": "SECTOR",
                    "settings": {"decay": 4, "truncation": 0.08, "startDate": "2014-01-01", "endDate": "2023-12-31"}}]}
    block = de.render_dataset(ev, "news46")
    assert "范围：KOR / news46" in block and "筛选：delay=1；waves=245" in block and "去重后 1 条已完成回测" in block
    t = _skill("brain-dataset-mining-experience")
    assert "范围：|筛选：" in t


def test_me_manual_review_skeleton_matches_what_the_tool_writes_for_a_new_file(tmp_path):
    from wqb.research import dataset_experience as de
    p = tmp_path / "kor_x_campain.md"
    de.write_report(p, de.BEGIN + "\nx\n" + de.END + "\n", "KOR · x 因子挖掘经验")
    text = p.read_text(encoding="utf-8")
    assert text.startswith("# KOR · x 因子挖掘经验") and "## 人工机制复盘" in text
    t = _skill("brain-dataset-mining-experience")
    assert "## 人工机制复盘" in t and "待结合原式、字段语义与平台核查补充" in t
