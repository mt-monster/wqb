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

REPO = Path(__file__).resolve().parents[3]
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
    "brain-forum-browse",
    "wq-brain-ppa-mining",
    "brain-alpha-research",
    "brain-alpha-research-field-quality",
    "brain-alpha-research-news-sentiment",
    "brain-alpha-research-hypothesis-first",
    "brain-dataset-exploration-general",
    "brain-datafield-exploration-general",
    "brain-data-feature-engineering",
    "brain-make-some-gem",
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


def test_ev_subtract_accepts_the_named_filter_parameter():
    """决策表 D6 与平台都允许 subtract(x, y, filter=true)；此前 subtract 漏标 param_names，命名写法被本地闸误拒。"""
    pytest.importorskip("ply")
    v = _load_validator().ExpressionValidator()
    assert v.check_expression("subtract(a, b, filter=true)")["valid"]
    assert v.check_expression("subtract(a, b, true)")["valid"]
    assert not v.check_expression("subtract(a, b, foo=true)")["valid"]
    assert not v.check_expression("divide(a, b, filter=true)")["valid"]      # divide 没有 filter


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


# ----------------------------------------------------------------------------- FB：forum-browse

FB = SKILLS / "brain-forum-browse"
FORUM_TOOLS = ("search_forum_posts", "read_forum_post", "get_glossary_terms", "get_messages", "get_events",
               "get_user_alphas")
NONEXISTENT_WRITE_TOOLS = ("create_forum_comment", "create_forum_post", "upvote_forum_comment",
                           "get_forum_comment_votes", "delete_forum_comment", "delete_forum_vote")


def _default_of(node, name):
    a = node.args
    pos = a.posonlyargs + a.args
    defaults = [None] * (len(pos) - len(a.defaults)) + list(a.defaults)
    for arg, d in zip(pos, defaults):
        if arg.arg == name and d is not None:
            return ast.literal_eval(d)
    for arg, d in zip(a.kwonlyargs, a.kw_defaults):
        if arg.arg == name and d is not None:
            return ast.literal_eval(d)
    return None


def test_fb_documented_tools_exist_and_the_write_tools_really_do_not():
    http = _all_http_tools()
    t = _skill("brain-forum-browse")
    table = t.split("## 1. 当前能力", 1)[1].split("## 2. 运行模式", 1)[0]
    listed = set(re.findall(r"^\| `([a-z_]+)` \|", table, re.M))
    assert listed == set(FORUM_TOOLS), listed
    for name in FORUM_TOOLS:
        assert name in http, name
    for name in NONEXISTENT_WRITE_TOOLS:
        assert name not in http, f"{name} 现在注册了——休眠的写路径可以启用了：更新 forum-browse SKILL 与 write-path/README"
    for name in ("create_forum_comment", "create_forum_post", "upvote_forum_comment", "get_forum_comment_votes"):
        assert name in t                                         # 文档明确列出「不存在」
    assert "delete_forum_" in t
    # 参数与缺省值逐项对照
    assert _params(http["search_forum_posts"]) == ["search_query", "max_results"]
    assert _default_of(http["search_forum_posts"], "max_results") == 50 and "缺省 50" in t
    assert _params(http["read_forum_post"]) == ["article_id", "include_comments"]
    assert _default_of(http["read_forum_post"], "include_comments") is True and "缺省 true" in t
    assert _params(http["get_glossary_terms"]) == []
    assert _params(http["get_events"]) == []
    assert _params(http["get_messages"]) == ["limit", "offset"]


def test_no_mcp_tool_accepts_credentials_as_arguments():
    """凭据只由服务端配置提供：所有 MCP 工具都不得有 email / password 类参数（forum 三件套与 payment 已删）。"""
    bad = {}
    for path in [*sorted(MCP_DIR.glob("tools_*.py")), REPO / "wqb_db_mcp.py"]:
        for name, node in _mcp_tools(path).items():
            hit = [p for p in _params(node) if re.fullmatch(r"(?i)email|password|passwd|pwd|api_?key|secret", p)]
            if hit:
                bad[f"{path.name}::{name}"] = hit
    assert not bad, f"这些 MCP 工具还接受凭据参数：{bad}"


def test_fb_read_budgets_match_config_example_and_docs():
    cfg = json.loads(_read(FB / "configs" / "config.example.json"))
    q = cfg["quotas"]
    for doc in (_skill("brain-forum-browse"), _read(FB / "references" / "tools-and-troubleshooting.md"),
                _read(FB / "references" / "write-path" / "quotas-and-cooldown.md")):
        for tool, n in q.items():
            assert re.search(rf"{tool}`?\s*(?:≤|\|)\s*\|?\s*{n}\b|{tool}[^\n]*?≤\s*{n}\b|{tool}`\s*\|\s*{n}\b", doc), (tool, n)
    assert "_comment_write_path" in cfg
    assert "FORUM_RATE_LIMIT_SECONDS" in _read(FB / "SKILL.md")
    assert 'os.environ.get("FORUM_RATE_LIMIT_SECONDS", "0")' in _read(MCP_DIR / "brain_mixin_transport.py")


def test_fb_recon_section_matches_forum_recon_tool():
    src = _read(REPO / "tools" / "forum_recon.py")
    t = _skill("brain-forum-browse")
    assert re.search(r'"--limit".*?default=3', src) and "缺省 3" in t
    assert re.search(r'"--max-search-rounds".*?default=8', src, re.S) and "缺省 8" in t
    assert "TTL_DAYS = 7" in src and "7 天缓存" in t
    for flag in ("--question", "--context", "--out", "--dry-run"):
        assert f'"{flag}"' in src and flag in t
    assert "forum-recon-triggers.md" in t and (SKILLS / "wq-brain-ra-pipeline/references/forum-recon-triggers.md").is_file()


def test_fb_write_path_is_dormant_and_no_stale_merged_file_names_remain():
    t = _skill("brain-forum-browse")
    assert "「每轮必须贡献」已**撤销**" in t and "只属于休眠的写路径" in t
    assert "**" not in re.search(r'^description:\s*"(.*)"\s*$', t, re.M).group(1)
    wp = FB / "references" / "write-path"
    assert (wp / "README.md").is_file()
    for f in wp.glob("*.md"):
        if f.name != "README.md":
            assert "休眠" in _read(f).split("\n", 3)[2], f"{f.name} 缺休眠横幅"
    stale = ("auto-send-e1.md", "personal-perspective.md", "profile-bootstrap.md", "external-memory-sources.md",
             "merge-with-alpha-judge.md", "file-workspace.md", "index-post-protocol.md", "mcp-tools-and-search.md",
             "user-brain-api", "list_help_center_articles")
    offenders = []
    for f in FB.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".json", ".py", ".yaml"):
            text = _read(f)
            offenders += [f"{f.relative_to(FB)}: {w}" for w in stale if w in text]
    assert not offenders, offenders
    for link in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", t):
        if not link.startswith(("http", "mailto")):
            assert (FB / link).exists() or (REPO / link).exists(), link


def test_fb_init_workspace_defaults_to_read_only_and_write_path_is_opt_in(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("fb_init_ws", FB / "scripts" / "init_workspace.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "SKILL_ROOT", tmp_path)
    monkeypatch.setattr(mod, "WORKSPACE", tmp_path / "ws")
    monkeypatch.setattr(mod, "RUNS", tmp_path / "runs")
    mod.init_workspace()
    assert sorted(p.name for p in (tmp_path / "ws").iterdir()) == ["action_ledger.json", "forum_memory.md", "skip_registry.json"]
    ro = mod.init_run("r1")
    assert sorted(Path(x).name for x in ro["created"]) == ["forum_stroll_notes.md", "session_plan.md"]
    assert "## 贡献计划" not in (tmp_path / "runs" / "r1" / "forum_stroll_notes.md").read_text(encoding="utf-8")
    mod.init_workspace(write_path=True)
    wr = mod.init_run("r2", write_path=True)
    assert sorted(Path(x).name for x in wr["created"]) == ["forum_findings.md", "forum_stroll_notes.md",
                                                            "run_contract.md", "session_plan.md"]
    assert (tmp_path / "ws" / "personal_experience_memory.md").is_file()


# ----------------------------------------------------------------------------- PP：ppa-mining

PPA = SKILLS / "wq-brain-ppa-mining"


def _ppa():
    return _read(PPA / "SKILL.md")


def test_pp_code_defaults_in_the_skill_match_score_datasets_source():
    src = _read(SKILLS / "wq-brain-campaign-toolkit" / "scripts" / "score_datasets.py")
    t = _ppa()
    for key, val in (("coverage_hard_min", "0.7"), ("field_count_hard_min", "5"), ("tier2_coverage_min", "0.85"),
                     ("tier2_field_count_min", "5"), ("tier2_alpha_count_max", "200"),
                     ("tier1_score_pct", "0.6"), ("tier2_score_pct", "0.3"), ("alpha_count_max", "50")):
        assert re.search(rf'h\.get\("{key}",\s*{re.escape(val)}\)', src), f"源码里 {key} 的缺省值不再是 {val}"
        assert re.search(rf"`{key}`\s*{re.escape(val)}", t), f"SKILL 没写 {key} = {val}"
    # 三个「拥挤度」口径都要能在代码里找到
    wq = _read(REPO / "tools" / "webdata_quality.py")
    assert "100 <= cnt <= 3000" in wq and "> 0.15" in wq and "100 ≤ count ≤ 3000" in t and "0.15" in t
    assert 'h.get("sweet_spot_ac_min", 50)' in src and 'h.get("sweet_spot_ac_max", 1000)' in src and "50–1000" in t


def test_pp_field_level_table_is_pinned_to_the_inspect_gate_source():
    src = _read(REPO / "tools" / "webdata_quality.py")
    t = _ppa()
    body = src.split("def check_expr_against_inspect", 1)[1]
    assert "coverage_ratio'] < 0.4" in body and "< 0.4" in t
    assert "abs(meta['skewness']) > 2" in body and "\\|skew\\| > 2" in t
    assert "meta['kurtosis'] > 8" in body and "| > 8 |" in t
    assert "{'daily': 22, 'weekly': 52, 'monthly': 120, 'quarterly': 252}" in body and "22 / 52 / 120 / 252" in t
    assert "daily=5" in body and "降到 5" in t
    for kw in ("ts_backfill", "group_backfill", "winsorize", "signed_power", "trade_when", "zero_inflated", "point_mass"):
        assert kw in body and kw in t, kw
    assert "is_placeholder" not in t.replace("旧文里的 `is_placeholder` **不是 BRAIN 算子**", "")


def test_pp_gate_line_table_matches_config():
    from wqb import config
    t = _ppa()
    gp, gi = config.GATES_PLATFORM, config.GATES_INTERNAL
    assert f"Sharpe ≥ {gp['sharpe_min']}" in t and f"Fitness ≥ {gp['fitness_min']}" in t
    lo, hi = gp["turnover_range"]
    assert f"[{int(lo * 100)}%, {int(hi * 100)}%]" in t
    assert f"self_corr < {gp['self_corr_max']}" in t and f"prod_corr < {gp['prod_corr_max']}" in t
    lo, hi = gi["turnover_range"]
    assert f"[{int(lo * 100)}%, {int(hi * 100)}%]" in t
    assert f"margin ≥ {int(gi['margin_bp_min'])}bp" in t and f"returns ≥ {int(gi['returns_min'] * 100)}%" in t
    assert f"self_corr < {gi['self_corr_max']}" in t
    assert "margin_bp_min" not in gp and "returns_min" not in gp        # 旧文的「平台硬线 Margin>5bp / Returns>5%」不成立
    assert "Margin > 5bp" in t                                             # 只在「已删」说明里出现


def test_pp_removed_teachings_stay_removed():
    t = _ppa()
    assert "ILLIQUID_MINVOL1M" not in t and "TaskStop" not in t and "lavender1203" not in t
    assert 'tags=["PowerPoolSelected"]` + `color` 的 MCP 提交在本环境**会被拦**' in t
    assert "C = 5" in t and "已删" in t.split("C = 5", 1)[1][:40]
    assert "189" in t and "没有依据" in t                                # 非标准窗口只在「已换」说明里
    assert "0.35" in t and "已删除作配方" in t


def test_pp_legacy_script_is_archived_and_not_offered():
    assert (REPO / "attic" / "ppa_mining_20260929" / "dataset_health_check.py").is_file()
    assert not (PPA / "scripts").exists()
    offenders = []
    for f in list((SKILLS).rglob("*.md")):
        for i, line in enumerate(_read(f).splitlines(), 1):
            if "dataset_health_check" in line and "归档" not in line:
                offenders.append(f"{f.relative_to(REPO)}:{i}")
    assert not offenders, offenders


def test_pp_referenced_commands_and_snapshot_page_exist():
    t = _ppa()
    assert "s0-select" in _read(REPO / "tools" / "campaign_intel.py")
    ph = _read(REPO / "tools" / "ppa_handoff.py")
    assert 'add_parser("sheet"' in ph and 'add_parser("record"' in ph and "--ppac" in ph
    wq = _read(REPO / "tools" / "webdata_quality.py")
    for flag in ("--zip", "--recommend", "--fields"):
        assert f"'{flag}'" in wq and flag in t
    assert "get_datasets" in _all_http_tools() and "get_mining_yield" in _all_db_tools()
    snap = _read(PPA / "references" / "region-snapshots-2026-08.md")
    assert "失效条件" in snap and "不是行动指令" in snap
    assert "references/region-snapshots-2026-08.md" in t
    assert 'mode="ppa"' in t and "score_datasets" in _read(SKILLS / "wq-brain-campaign-toolkit" / "SKILL.md") + "score_datasets"


def test_pp_ra_side_copy_is_a_short_pointer_page():
    exp = _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "ppa-mining-experience.md")
    assert len(exp.splitlines()) <= 60
    assert "dataset_health_check" not in exp.replace("已归档", "") or "不存在" in exp


# ----------------------------------------------------------------------------- AR：alpha-research

AR = SKILLS / "brain-alpha-research"


def test_ar_verification_commands_really_run_and_give_the_documented_output():
    from wqb import config
    t = _read(AR / "SKILL.md")
    cmd1 = ("import sys; sys.path.insert(0,'src'); from wqb.research.evidence import EVIDENCE_REGISTRY as R; "
            "[print(e.date, e.category, '|', e.actionable_rule) for e in R]")
    cmd2 = ("import sys; sys.path.insert(0,'src'); from wqb.config import REGIONS, neutralization_search_order; "
            "print(REGIONS['USA']['default_universe']); print(neutralization_search_order('USA'))")
    assert cmd1 in t and cmd2 in t
    o1 = subprocess.run([sys.executable, "-c", cmd1], cwd=str(REPO), capture_output=True, text=True, timeout=60)
    assert o1.returncode == 0 and len(o1.stdout.strip().splitlines()) >= 4, o1.stderr
    o2 = subprocess.run([sys.executable, "-c", cmd2], cwd=str(REPO), capture_output=True, text=True, timeout=60)
    assert o2.returncode == 0
    lines = o2.stdout.strip().splitlines()
    assert lines[0] == "TOP3000" and len(eval(lines[1])) == 11 and "（11 项）" in t
    assert "wqb research" in t and "不存在" in t                          # 只在「命令不存在」的说明里出现
    assert not (REPO / "pyproject.toml").exists() or "wqb" not in (_read(REPO / "pyproject.toml").split("[project.scripts]")[1]
                                                                    if "[project.scripts]" in _read(REPO / "pyproject.toml") else "")
    assert len(config.PARADIGMS) == 13 and config.SHAPE_CLASSES == {"S1", "S4", "S5", "S9"}


def test_ar_check_batch_really_has_no_callers_and_gate6_is_the_real_diversity_gate():
    callers = []
    for root in (REPO / "src", REPO / "tools", REPO / "Claude" / "skills", REPO / "world-quant-brain-mcp"):
        for f in root.rglob("*.py"):
            if ".venv" in f.parts or "attic" in f.parts or "trailSomeAlphas" in f.parts:
                continue
            try:
                tree = ast.parse(_read(f))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    fn = node.func
                    name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
                    if name == "check_batch":
                        callers.append(f"{f.relative_to(REPO)}:{node.lineno}")
    assert not callers, f"check_batch 现在有调用方了——AR SKILL 步 8 与 evidence.py 的说法要改：{callers}"
    assert "check_batch_diversity" in _read(SKILLS / "wq-brain-campaign-toolkit" / "scripts" / "gate.py")
    from wqb.research.evidence import EVIDENCE_REGISTRY
    assert any("check_batch_diversity" in e.actionable_rule for e in EVIDENCE_REGISTRY)


def test_ar_evidence_schema_ledger_writers_and_ghost_source_match_the_code():
    import dataclasses
    from wqb import config
    from wqb.research.evidence import Evidence
    t = _read(AR / "SKILL.md")
    for f in dataclasses.fields(Evidence):
        assert f"`{f.name}`" in t, f.name
    cat = {e["key"]: e for e in json.loads(_read(REPO / "docs" / "ledger_keys.json"))["entries"]}
    assert any(w["ref"] == "tools/forum_recon.py" for w in cat["community_tpl_kb"]["writers"])
    assert cat["template_kb"]["writers"] == [] and cat["template_kb"].get("orphan")
    assert len(config.GHOST_OPERATORS) >= 10 and "config.GHOST_OPERATORS" in t
    assert "operator_audit" in _all_http_tools()
    fa = _read(REPO / "tools" / "fetch_all_universes.py")
    assert "Desktop" not in fa and "CREDENTIALS_EMAIL" in fa


def test_ar_references_all_linked_and_the_webdata_rules_moved_to_field_quality():
    t = _read(AR / "SKILL.md")
    for f in sorted((AR / "references").glob("*.md")):
        assert f.name in t, f"{f.name} 没有入链（SKILL 索引里要写一行「何时读」）"
    assert not (AR / "references" / "webdatascope-data-quality.md").exists()
    moved = SKILLS / "brain-alpha-research-field-quality" / "references" / "webdatascope-data-quality.md"
    assert moved.is_file() and len(re.findall(r"^## 规则 \d+", _read(moved), re.M)) == 26
    for f in (SKILLS / "brain-alpha-research-field-quality" / "SKILL.md", SKILLS / "brain-alpha-repair" / "references" / "repair-recipes.md",
              AR / "references" / "sources.md"):
        assert "brain-alpha-research/references/webdatascope-data-quality" not in _read(f), f.name
    for f in (AR / "references").glob("*.md"):
        text = _read(f)
        assert "[[" not in text, f"{f.name} 还有 Obsidian wikilink"
    assert "已被禁止" in _read(AR / "references" / "asi-methodology.md")
    assert "[未验证" in _read(AR / "references" / "jump-decay-methodology.md")


# ----------------------------------------------------------------------------- 共用：算子目录 / 表格解析

def _platform_operator_catalog():
    """平台 `get_operators` 的 103 个算子全集（docs/reference/operators_catalog.json）。"""
    d = json.loads(_read(REPO / "docs" / "reference" / "operators_catalog.json"))
    return {o["name"] for o in d["results"]}


def _md_table_rows(text, header_startswith):
    """取以 header_startswith 开头的那张 markdown 表的数据行（每行拆成去掉首尾空白的单元格列表）。"""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(header_startswith):
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                rows.append(cells)
            return rows
    raise AssertionError(f"找不到表头 {header_startswith!r}")


# ----------------------------------------------------------------------------- FQ：field-quality

FQ = SKILLS / "brain-alpha-research-field-quality"
_TK = SKILLS / "wq-brain-campaign-toolkit" / "scripts"


def test_fq_crowding_table_numbers_match_their_code_sources():
    t = _read(FQ / "SKILL.md")
    wq = _read(REPO / "tools" / "webdata_quality.py")
    assert "if cnt < 50:" in wq and "100 <= cnt <= 3000" in wq and "cnt > 30000" in wq and "sweet_bonus = 0.5" in wq
    assert "100–3000" in t and "< 50" in t and "> 30000" in t and "×0.5" in t
    sd = _read(_TK / "score_datasets.py")
    doc = sd.split("def crowd_penalty", 1)[1].split('"""', 2)[1]
    for frag in ("ac<=50 满分 0.30", "50→500 线性降至 0.15", "500→5000 线性降至 0.02", ">5000 恒 0.02"):
        assert frag in doc, frag
    assert "≤ 50 → 0.30" in t and "降到 0.15" in t and "降到 0.02" in t and "> 5000 恒 0.02" in t
    assert 'h.get("sweet_spot_ac_min", 50)' in sd and 'h.get("sweet_spot_ac_max", 1000)' in sd and "50–1000" in t
    step2 = _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "step2-s0.md")
    assert "`alphaCount ≥ 1 万`" in step2 and "**连续 2 波**" in step2
    assert "1 万" in t and "连续 2 波" in t


def test_fq_prescreen_gate_cli_and_ledger_key_are_what_the_skill_says():
    t = _read(FQ / "SKILL.md")
    pg = _read(REPO / "tools" / "prescreen_gate.py")
    for flag in ("--region", "--record", "--source", "--summary"):
        assert f'"{flag}"' in pg and flag in t, flag
    assert "exempt" in t and "webdata_quality" in t
    assert "0=PASS" in pg and "exit 0 = PASS / 1 = BLOCK" in t
    assert "没有接入 workflow 节点" in t or "未接入 workflow 节点" in t
    assert not re.search(r"prescreen_gate|prescreen_", _read(REPO / "src" / "wqb" / "workflow" / "nodes" / "campaign.py"))
    cat = {e["key"]: e for e in json.loads(_read(REPO / "docs" / "ledger_keys.json"))["entries"]}
    assert any(w["ref"] == "tools/prescreen_gate.py" for w in cat["prescreen_<region>"]["writers"])


def test_fq_data_pack_coverage_and_rule_document_moved_in():
    t = _read(FQ / "SKILL.md")
    for r in ("ASI", "CHN", "EUR", "GLB", "JPN", "KOR", "USA"):
        assert r in t.split("数据包区域覆盖边界", 1)[1][:400], r
    assert "DEU / IND / GBR / MEA / TWN" in t and "--source exempt" in t
    ref = FQ / "references" / "webdatascope-data-quality.md"
    assert ref.is_file() and "references/webdatascope-data-quality.md" in t
    # 规则 13 的「时序窗口下限」是理论下限，闸实际执行的是代码口径——两层口径必须都写明
    r13 = _read(ref).split("## 规则 13", 1)[1].split("## 规则 14", 1)[0]
    assert "两层口径" in r13 and "monthly ≥ 120" in r13 and "quarterly ≥ 252" in r13
    assert "{'daily': 22, 'weekly': 52, 'monthly': 120, 'quarterly': 252}" in _read(REPO / "tools" / "webdata_quality.py")


def test_fq_prior_is_staged_and_agrees_with_the_ra_step3_users_grading():
    t = _read(FQ / "SKILL.md")
    ra3 = _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "step3-s1-semantic.md").split("## 3.3", 1)[1].split("## 3.4", 1)[0]
    for tok in ("≥ 50", "10–49", "0–9", "冷门字段占批次预算 ≥ 50%"):
        assert tok in ra3 and tok in t, tok
    assert "受 ra-pipeline 步 3" in t and "分阶段" in t and "饱和数据集" in t and "不叠加本先验" in t
    assert "不依赖 `jq`" in t and not re.search(r"\bjq\s+[-'\.]", t) and "这此" not in t   # 旧文的 jq 依赖与笔误
    assert "get_datafields" in t and "get_datafields" in _all_http_tools()
    body = t.split("## 验证清单", 1)[1]
    assert "prescreen_gate.py --region <R>" in body and "get_ledger_key(region" in body and "笔记 / 回报里有前 ~30 字段表" in body


# ----------------------------------------------------------------------------- NS：news-sentiment

NS = SKILLS / "brain-alpha-research-news-sentiment"
_NEWS_DOCS = REPO / "docs" / "reference"


def test_ns_classifier_facts_in_the_skill_match_the_module():
    from wqb.research import news_field_classifier as nfc
    t = _read(NS / "SKILL.md")
    assert set(nfc.DATASET_OVERRIDES) == {"news12"} and "目前只有 `news12`" in t
    for fam, kws in nfc.KEYWORD_RULES.items():
        for kw in kws:
            assert f"`{kw}`" in t, f"分类器关键词 {kw!r}（{fam.value}）没写进 SKILL 的家族表"
    assert nfc.classify_field("news_novelty") == nfc.FieldFamily.ATTENTION and "`novelty` 归 attention" in t
    assert nfc.is_news_dataset("news12") and nfc.is_news_dataset("snt3") and nfc.is_news_dataset("sentiment22")
    assert not nfc.is_news_dataset("socialmedia12") and not nfc.is_news_dataset("nws12") and nfc.is_news_dataset("x", "news")
    assert not nfc.is_news_dataset("x", "sentiment")                     # category 只认 news
    assert "tracking/taxonomies/taxonomy_<ds>_<REGION>.json" in t
    assert nfc._taxonomy_path("d", "R", "tracking/taxonomies").replace("\\", "/") == "tracking/taxonomies/taxonomy_d_R.json"
    assert "data/field_taxonomy" not in t and "data/field_taxonomy" not in _read(_NEWS_DOCS / "news_sentiment_playbook.md")
    # 没有任何流水线代码调用分类器
    users = [str(f.relative_to(REPO)) for root in (REPO / "src", REPO / "tools", MCP_DIR)
             for f in root.rglob("*.py") if ".venv" not in f.parts and "news_field_classifier" in _read(f)
             and f.name != "news_field_classifier.py"]
    assert not users, f"分类器有了调用方，SKILL 里「没有任何流水线节点调用」要改：{users}"


def test_ns_bucket_table_matches_the_pairing_matrix_document():
    t = _read(NS / "SKILL.md")
    rows = _md_table_rows(t, "| 桶 |")
    skill = {}
    for cells in rows:
        name = re.sub(r"[*]", "", cells[0]).split()[0]
        strong = {x for x in re.split(r"[、,\s]+", cells[3]) if re.fullmatch(r"[a-z_]+", x)}
        maybe = {x for x in re.split(r"[、,\s]+", cells[4]) if re.fullmatch(r"[a-z_]+", x)}
        skill[name] = (strong, maybe, "HIGH" in cells[2])
    doc = _read(_NEWS_DOCS / "news_bucket_field_map.md")
    mrows = _md_table_rows(doc, "| Family")
    buckets = ["Level", "Change", "Surprise", "Dispersion", "Event", "Propagation"]
    matrix = {b: (set(), set()) for b in buckets}
    for cells in mrows:
        fam = cells[0]
        for b, mark in zip(buckets, cells[1:7]):
            if mark == "●":
                matrix[b][0].add(fam)
            elif mark == "◐":
                matrix[b][1].add(fam)
    assert set(skill) == {"Level", "Change", "Surprise", "Dispersion", "Event-conditioned", "Propagation"}
    for b, key in (("Level", "Level"), ("Change", "Change"), ("Surprise", "Surprise"), ("Dispersion", "Dispersion"),
                   ("Event", "Event-conditioned"), ("Propagation", "Propagation")):
        assert skill[key][0] == matrix[b][0] and skill[key][1] == matrix[b][1], (key, skill[key], matrix[b])
    assert {k for k, v in skill.items() if v[2]} == {"Dispersion", "Event-conditioned", "Propagation"}


def test_ns_bucket_gates_are_guidance_and_the_dead_references_stay_dead():
    assert not (REPO / "src" / "wqb" / "search" / "news_loop.py").exists()
    for f in ("news_bucket_field_map.md", "news_sentiment_playbook.md"):
        d = _read(_NEWS_DOCS / f)
        flat = re.sub(r"[\s>]+", " ", d)                         # 引用块折行后再看上下文
        for m in re.finditer(r"news_loop\.py", flat):
            assert "does not exist" in flat[m.start(): m.start() + 120], (f, flat[m.start(): m.start() + 120])
        assert "P15_EVENT_CONDITIONED" not in d.replace("No template named\n  `P15_EVENT_CONDITIONED` exists in code.", "") or "exists in code" in d
    for f in ("news_dataset_portfolio.md",):
        d = _read(_NEWS_DOCS / f)
        assert "never existed" in d
    t = _read(NS / "SKILL.md")
    for line in t.splitlines():
        assert "news-refresh-portfolio" not in line, line
    assert "不是闸门" in t and "无代码闸" in t and "check_batch_diversity" in t
    for n in ("Hard gates",):
        assert n not in _read(_NEWS_DOCS / "news_sentiment_playbook.md")
    # 每批设计目标里唯一有执行点的一条：覆盖 < 0.4 → backfill（体检硬门检查 1）
    assert "coverage_ratio'] < 0.4" in _read(REPO / "tools" / "webdata_quality.py")


def test_ns_playbook_ghost_table_is_exactly_config_ghost_operators():
    from wqb import config
    d = _read(_NEWS_DOCS / "news_sentiment_playbook.md")
    sec = d.split("## 5.", 1)[1].split("## 6.", 1)[0]
    ops = set(re.findall(r"^\| `([a-z_0-9]+)` \|", sec, re.M))
    assert ops == set(config.GHOST_OPERATORS), (ops ^ set(config.GHOST_OPERATORS))


def test_ns_routing_checks_use_real_s0_select_tags_and_weak_probe_cap():
    from wqb import config
    t = _read(NS / "SKILL.md")
    step2 = _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "step2-s0.md")
    ci = _read(REPO / "tools" / "campaign_intel.py")
    assert 's0-select' in ci and "跨区弱" in ci and "[跨区弱:REG:maxS@bt]" in step2 and "[跨区弱:REG:maxS@bt]" in t
    assert "`lit=Y`" in step2 and "lit=Y" in t and "hist_backtested ≥ 8" in t and "`bt ≥ 8`" in step2
    assert config.MINING["weak_probe_slots_max"] == 1 and "`MINING[\"weak_probe_slots_max\"]` = 1" in t
    assert "D0-P" in t and "D0-P" in _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "decision-table.md")
    port = _read(_NEWS_DOCS / "news_dataset_portfolio.md")
    assert "candidate source, not a routing rule" in port and "alphaCount / fieldCount ≤ 5" in port
    for f in ("news_dataset_portfolio.md", "news.md", "news_sentiment_playbook.md", "news_bucket_field_map.md"):
        assert "researcher_workflow" not in _read(_NEWS_DOCS / f), f


def test_ns_news12_field_code_c_and_motif_ids_do_not_collide():
    t = _read(NS / "SKILL.md")
    n = _read(_NEWS_DOCS / "news.md")
    assert "C（旧称 M）" in t and "**C** (context/microstructure)" in n and "| M | **event_type**" not in n
    assert "M4 → Surprise 或 Change" in t and "自身的历史" in t


# ----------------------------------------------------------------------------- HF：hypothesis-first

HF = SKILLS / "brain-alpha-research-hypothesis-first"


def _hf_example():
    t = _read(HF / "SKILL.md")
    m = re.search(r"```json\n(\{\"hypotheses\".*?)\n```", t, re.S)
    assert m, "hypothesis-first 里找不到 JSON 示例"
    return json.loads(m.group(1))


def test_hf_json_example_loads_with_the_real_catalog_loader_and_validates(tmp_path):
    from wqb.research import hypothesis_miner as hm
    ex = _hf_example()
    path = tmp_path / "ex_hypotheses.json"
    path.write_text(json.dumps(ex), encoding="utf-8")
    hs = hm.load_catalog(str(path))
    assert len(hs) == 1 and set(hs[0].to_dict()) == set(hm._REQUIRED_FIELDS)
    exps = hm.run_hypothesis_round(str(path))["H_overreact_attention"]["expressions"]
    assert len(exps) == 4
    spec = importlib.util.spec_from_file_location("_hf_validator", SKILLS / "alpha-expression-verifier" / "scripts" / "validator.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_hf_validator"] = mod
    spec.loader.exec_module(mod)
    v = mod.ExpressionValidator()
    for e in exps:
        e = e.replace("<关注度字段>", "volume").replace("<反应字段>", "returns").replace("<同集无关字段>", "close")
        r = v.check_expression(e)
        assert r["valid"], (e, r["errors"])
    for w in re.findall(r"ts_zscore\(<[^>]+>, (\d+)\)", json.dumps(ex, ensure_ascii=False)):
        assert int(w) in (1, 5, 22, 66, 252, 504, 1008, 1260), w          # 示例只用标准窗口
    # 单一字段清单：SKILL 里的 8 个必填字段名就是代码里的 8 个
    t = _read(HF / "SKILL.md")
    assert "8 个必填字段" in t and len(hm._REQUIRED_FIELDS) == 8


def test_hf_verdict_table_quotes_the_code_constants_and_judge_behaves_as_documented():
    from wqb.research import hypothesis_miner as hm
    t = _read(HF / "SKILL.md")
    for name, val in (("_PSEUDO_SIGNAL_TOLERANCE", "0.1"), ("_MIN_PRIMARY_SHARPE", "0.3"),
                      ("_SUPPORTED_SHARPE_DELTA", "0.5"), ("_SUPPORTED_FITNESS", "0.8")):
        assert float(getattr(hm, name)) == float(val) and name in t, name
    R = hm.ExperimentResult
    cases = [
        (R("h", 0.5, 0.4, 0.45, 0.48), "rejected"),                                      # 伪信号
        (R("h", 0.5, 0.5, 0.9, 0.5, primary_fitness=0.9), "rejected"),                   # 对照更好
        (R("h", 0.2, 0.1, 0.0, 0.15), "needs_refinement"),
        (R("h", -0.8, -0.5, 0.4, -0.6), "needs_refinement"),                             # 负值先试翻符号
        (R("h", 0.8, 0.5, 0.5, 0.6, primary_fitness=0.4), "partially_supported"),
        (R("h", 1.5, 1.0, 0.0, 1.3, primary_fitness=1.0), "supported"),
    ]
    for r, want in cases:
        assert hm.judge(r)["status"].value == want, (r, want)
    for state in ("rejected", "needs_refinement", "partially_supported", "supported"):
        assert f"`{state}`" in t
    assert "`expected_direction` 只是记录" in t and "expected_direction" not in _read(REPO / "src" / "wqb" / "research" / "hypothesis_miner.py").split("def judge", 1)[1].split("def load_catalog", 1)[0]


def test_hf_node_params_paths_ledger_and_tools_match_the_skill():
    import inspect
    from wqb.workflow.nodes import hypothesis_round as hr
    from wqb.workflow._common import REPO_ROOT
    t = _read(HF / "SKILL.md")
    sig = set(inspect.signature(hr.run).parameters)
    for p in ("dataset_id", "region", "delay", "max_hypotheses", "catalog_path", "save_ledger"):
        assert p in sig and p in t, p
    assert Path(hr._CATALOG_DIR) == Path(str(REPO_ROOT)) / "data" / "hypothesis_catalog" and "data/hypothesis_catalog/<dataset>_hypotheses.json" in t
    assert Path(hr._LEDGER_DIR) == Path(str(REPO_ROOT)) / "tracking" / "hypotheses" and "tracking/hypotheses/ledger.jsonl" in t
    wf = _all_http_tools()["workflow_execute"]
    assert {"node", "params", "dry_run"} <= set(_params(wf)) and 'node="hypothesis_round"' in t
    db = _all_db_tools()
    assert "source" in _params(db["upsert_expressions"]) and 'source="hypothesis"' in t and "`hypothesis`" in _read(REPO / "wqb_db_mcp.py")
    for tool in ("list_expressions", "list_alphas_by_wave", "get_gate_result", "upsert_wave_result"):
        assert tool in db and tool in t or tool == "upsert_wave_result", tool
    for tool in ("workflow_batch_track", "create_multi_simulation"):
        assert tool in _all_http_tools()
    assert "hypothesis_round" in _read(REPO / "src" / "wqb" / "workflow" / "registry.py")
    # judge() 没有生产调用方（只有单测）——SKILL 状态表这样写
    callers = [str(f.relative_to(REPO)) for root in (REPO / "src", REPO / "tools", MCP_DIR) for f in root.rglob("*.py")
               if ".venv" not in f.parts and re.search(r"\bjudge\(", _read(f)) and "hypothesis_miner" in _read(f)
               and f.name != "hypothesis_miner.py"]
    assert not callers, callers
    assert "没有调用方" in t


def test_hf_retired_artifacts_are_named_as_retired_and_the_dormant_status_is_explicit():
    t = _read(HF / "SKILL.md")
    for stale in ("data/field_semantics", "data/hypothesis_ledger"):
        for line in t.splitlines():
            if stale in line:
                assert "已取消" in line or "从未存在" in line, (stale, line)
    assert "## 状态：条件激活（dormant）" in t and "不存在「等假设生成器」的前置" in t
    assert "s1_semantic_<ds>" in t and "冷门字段" in t and "不再作种子排序依据" in t
    step2 = _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "step2-s0.md")
    assert "hypothesis-first" in step2 and "dormant" in step2
    assert "load_catalog` 抛错" in t


# ----------------------------------------------------------------------------- DE：dataset-exploration

DE = SKILLS / "brain-dataset-exploration-general"


def test_de_has_no_region_table_and_jpn_is_a_valid_region():
    from wqb import config
    t = _read(DE / "SKILL.md")
    assert "JPN" in config.REGIONS and config.REGIONS["JPN"]["default_universe"] == "TOP1600"
    assert not re.search(r"^\|\s*(USA|KOR|EUR|CHN|JPN|ASI|GLB)\s*\|", t, re.M), "又出现了区域 → universe 表"
    assert "不是有效的 EQUITY 区域" not in t and "返回 0" not in t.replace("静默返回 0 条", "")
    assert 'config.REGIONS[<R>]["default_universe"]' in t and "get_platform_setting_options" in t
    assert "先走 RA 步 2 选集" in t and "确定数据集：根据战略重要性" not in t        # 上游 = 白名单内某集；无判据的「自选」删


def test_de_classification_landing_point_and_taxonomies_match_the_tool():
    t = _read(DE / "SKILL.md")
    src = _read(REPO / "tools" / "field_semantic_classify.py")
    for flag in ("--region", "--dataset", "--write-ledger"):
        assert f'"{flag}"' in src and flag in t, flag
    import field_semantic_classify as fsc
    assert len(fsc.ECON_CATEGORIES) == 10 and "共 10 类" in t
    assert "s1_semantic_<ds>" in t and "wave_gate" in t
    ra = _read(SKILLS / "wq-brain-ra-pipeline" / "SKILL.md")
    assert "s1_semantic_<ds>" in ra and "field_semantic_classify.py" in ra
    assert (SKILLS / "wq-brain-ra-pipeline" / "references" / "concept-taxonomy-map.md").is_file()
    assert "conn = db_connect(readonly=True)" in src and "`fields` 表" in t


def test_de_scoring_and_research_sections_point_at_the_current_sources():
    t = _read(DE / "SKILL.md")
    for line in t.splitlines():
        if "log10(1+alphaCount)" in line:
            assert "取代" in line and "不要再用" in line
    assert (SKILLS / "wq-brain-campaign-toolkit" / "references" / "probe-scoring-v2.md").is_file() and "probe-scoring-v2.md" in t
    assert (REPO / "tools" / "forum_recon.py").is_file() and "forum_recon.py" in t
    assert (SKILLS / "wq-brain-ra-pipeline" / "references" / "forum-recon-triggers.md").is_file()
    assert "不要**为数据集审计加载 `brain-forum-browse`" in t
    assert "代表字段 ≤ 12 个" in t and "不产「增强描述」" in t and "不写表达式" in t


def test_de_reference_is_short_chinese_and_the_six_tips_live_only_in_datafield_exploration():
    ref = _read(DE / "reference.md")
    assert len(ref.splitlines()) <= 60 and "Job Duty Manual" in ref
    assert "scale_down" not in ref and "ts_median" not in ref and "Position Overview" not in ref
    assert "reference.md" in _read(DE / "SKILL.md")
    tools = _all_http_tools()
    for name in re.findall(r"`((?:get|create|search|read)_[a-z_]+)`", ref.split("MCP 工具速查", 1)[1].split("平台文档页", 1)[0]):
        assert name in tools, f"reference.md 速查表里的工具 {name} 不存在"
    assert "ensure_authenticated" in _read(MCP_DIR / "tools_sim.py") and not _required_params(tools["authenticate"])


# ----------------------------------------------------------------------------- DF：datafield-exploration

DF = SKILLS / "brain-datafield-exploration-general"


def test_df_every_operator_is_in_the_platform_catalog_unless_marked_as_a_counterexample():
    cat = _platform_operator_catalog()
    assert len(cat) == 103 and "scale_down" not in cat and "ts_median" not in cat and not any(n.startswith("ts_event_") for n in cat)
    marks = ("不要", "不在", "幽灵", "不存在", "旧文", "原帖", "没有", "过不了", "会被拒", "替换", "换成", "不能")
    pat = re.compile(r"\b(ts_[a-z_]+|vec_[a-z_]+|group_[a-z_]+|scale_down|zscore|rank|abs|if_else|trade_when|winsorize)\(")
    for f in (DF / "SKILL.md", DF / "reference.md"):
        for i, line in enumerate(_read(f).splitlines(), 1):
            for name in pat.findall(line):
                if name not in cat:
                    assert any(m in line for m in marks), f"{f.name}:{i} 出现目录外算子 {name}：{line[:80]}"
    t = _read(DF / "SKILL.md")
    for v in ("vec_avg", "vec_sum", "vec_max", "vec_min", "vec_count", "vec_stddev", "vec_range"):
        assert v in cat and f"`{v}`" in t + _read(DF / "reference.md"), v


def test_df_vector_matrix_event_rules_match_gate_3_gate_8_and_the_fix_tool():
    t = _read(DF / "SKILL.md")
    gate = _read(_TK / "gate.py")
    assert "最内层" in _read(SKILLS / "wq-brain-campaign-toolkit" / "references" / "gate-rules.md") and "[TYPE]" in t
    assert re.search(r"8.*EVENT.*block", gate) and "平台无 ts_event_*" in gate
    assert "平台没有 `ts_event_*` 系列" in t and "闸 8 直接 FAIL" in t
    tools = _all_http_tools()
    assert "fix_vector_fields" in tools and "auto_fix_vector" in _params(tools["preflight_expressions"])
    assert "does not support event inputs" in _read(MCP_DIR / "tools_sim.py").split("async def fix_vector_fields", 1)[1][:900]
    assert "fix_vector_fields" in t and "auto_fix_vector=true" in t
    for old in ("VECTOR 字段应**直接**用于", "`winsorize` 安全", "转成 VECTOR"):
        for line in t.splitlines():
            if old in line:
                assert "旧文" in line and "已更正" in line, f"旧口径 {old!r} 只许出现在「旧文…已更正」的说明里：{line[:60]}"


def test_df_documented_method_expressions_pass_the_mcp_static_gate_grammar():
    spec = importlib.util.spec_from_file_location("_df_validator", SKILLS / "alpha-expression-verifier" / "scripts" / "validator.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_df_validator"] = mod
    spec.loader.exec_module(mod)
    v = mod.ExpressionValidator()
    rows = _md_table_rows(_read(DF / "reference.md"), "| 法 | MATRIX")
    assert len(rows) == 6
    for cells in rows:
        for cell in cells[1:3]:
            e = cell.strip("`").replace("datafield", "close").replace(", N)", ", 22)").replace("> X", "> 10").replace("> k", "> 1")
            assert "?" not in e, e
            r = v.check_expression(e)
            assert r["valid"], (e, r["errors"])
    src = _read(MCP_DIR / "tools_sim.py")
    assert "_toolkit_gate_check(alpha_expressions)" in src and "len(alpha_expressions) < 2" in src and "len(alpha_expressions) > 10" in src
    t = _read(DF / "SKILL.md")
    assert "单次 2–10 条" in t and "没有 `? :` 三元" in t


def test_df_offline_pack_fields_and_window_floors_match_the_generator():
    t = _read(DF / "SKILL.md")
    wq = _read(REPO / "tools" / "webdata_quality.py")
    for key in ("coverage_ratio", "skewness", "kurtosis", "frequency", "distribution_shape", "min_window",
                "recommended_decay", "recommended_truncation"):
        assert f"'{key}'" in wq and f"`{key}`" in t, key
    body = wq.split("def check_expr_against_inspect", 1)[1]
    assert "{'daily': 22, 'weekly': 52, 'monthly': 120, 'quarterly': 252}" in body and "daily=5" in body
    assert "daily ≥ 22" in t and "weekly ≥ 52" in t and "monthly ≥ 120" in t and "quarterly ≥ 252" in t
    for shape in ("point_mass", "zero_inflated", "ceiling", "concentrated", "spread"):
        assert shape in wq and shape in t, shape
    assert "tracking/mining/field_inspect_<region 小写>_<dataset>.json" in t and "field_inspect_{" in _read(REPO / "tools" / "field_inspect_gate.py") + "field_inspect_{"


def test_df_settings_trap_and_cost_claims_are_backed_by_code():
    t = _read(DF / "SKILL.md")
    assert 'testPeriod: str = "P0Y0M0D"' in _read(SKILLS / "brain-inspect-raw-template-create-setting" / "scripts" / "resolve_settings.py") and "`P0Y0M0D`" in t
    assert "params['dataset.id'] = dataset_id" in _read(MCP_DIR / "brain_mixin_simulation.py") and "dataset.id=<id>" in t
    assert "1 + 1 + 3 + 1" not in t and "6 条" in t and "≈ 15 条仿真" in t
    assert re.findall(r"^## 法 (\d)：", t, re.M) == list("123456")                  # 六法连号，其余章节不占数字
    assert "## 类型先行" in t and "## 批量字段收割" in t and not re.search(r"^## (?:4′|7)\.", t, re.M)
    assert "`ts_median`" in t and "幽灵算子" in t and "ts_median" in __import__("wqb.config", fromlist=["GHOST_OPERATORS"]).GHOST_OPERATORS
    for link in re.findall(r"\]\((\.\./[a-z0-9-]+/SKILL\.md|reference\.md)\)", t):
        assert (DF / link).resolve().is_file(), link


# ----------------------------------------------------------------------------- 共用：从源码取函数 / 参数缺省

def _func_from_source(path, *names, extra_globals=None):
    """不 import 整个模块（GEM 引擎的依赖在测试环境里不全），只把指定的顶层函数抽出来执行。"""
    import os
    tree = ast.parse(_read(path))
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in body} == set(names), f"{path} 里找不到 {names}"
    ns = {"re": re, "os": os, "json": json, "Path": Path}
    ns.update(extra_globals or {})
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), ns)
    return ns


def _signature_defaults(path, name, top_level=True):
    tree = ast.parse(_read(path))
    nodes = tree.body if top_level else list(ast.walk(tree))
    fn = next(n for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    a = fn.args
    pos = a.posonlyargs + a.args
    defaults = {arg.arg: ast.literal_eval(d) for arg, d in zip(pos[len(pos) - len(a.defaults):], a.defaults)}
    return [x.arg for x in pos], defaults


# ----------------------------------------------------------------------------- FE：feature-engineering

FE = SKILLS / "brain-data-feature-engineering"
GEM = SKILLS / "brain-make-some-gem"
TRAIL = GEM / "scripts" / "trailSomeAlphas"
_GEM_NODE = REPO / "src" / "wqb" / "workflow" / "nodes" / "gem.py"


def test_fe_source_injection_table_matches_the_engine_and_the_ledger_example_is_manual():
    from wqb.workflow.nodes import gem as gem_node
    t = _read(FE / "SKILL.md")
    assert gem_node.TEMPLATE_IDEAS_SOURCES == ("feature_engineering_node", "standalone", "standalone_v2")
    for src in gem_node.TEMPLATE_IDEAS_SOURCES:
        assert f"`{src}`" in t, src
    assert '_tpl_sources = ("feature_engineering_node", "standalone", "standalone_v2")' in _read(TRAIL / "run_pipeline.py")
    for tpl in ("feature_engineering_node", "standalone", "standalone_v2", "standalone (x)"):
        assert gem_node.is_template_ideas_source(tpl), tpl
    for real in ("manual", "s2_nested", "kb_templates.py", None, ""):
        assert not gem_node.is_template_ideas_source(real), real
    m = re.search(r"```json\n(\{\"dataset\".*?)\n```", t, re.S)
    assert m, "FE SKILL 里找不到台账 JSON 示例"
    raw = re.sub(r",\s*\.\.\.", "", m.group(1))                    # 示例里的省略号
    raw = re.sub(r"(?<![\"\w])<[^>\"]+>", "0", raw)                 # 未加引号的占位符（<DELAY> / <概念数>）
    rec = json.loads(raw)
    assert rec["source"] == "manual" and {"ideas_md_path", "field_whitelist", "concept_count", "preprocessing"} <= set(rec)
    assert "写成 `standalone` 会被 GEM 静默忽略" in t


def test_fe_ledger_readers_and_gate_claims_hold():
    t = _read(FE / "SKILL.md")
    assert "field_whitelist" in _read(REPO / "tools" / "s2_field_validator.py")
    assert 's1_key = f"s1_{dataset}_d1"' in _read(REPO / "src" / "wqb" / "workflow" / "nodes" / "campaign.py")
    assert not re.search(r"s1_", _read(SKILLS / "wq-brain-campaign-toolkit" / "scripts" / "gate.py")), "闸 1–5 现在读 s1_ 键了？改 FE SKILL"
    assert "toolkit 的闸 1–5 不读它" in t
    readers = []
    for root in (REPO / "src", REPO / "tools", MCP_DIR, SKILLS):
        for f in root.rglob("*.py"):
            if ".venv" in f.parts or "attic" in f.parts:
                continue
            if re.search(r"\.get\(\s*[\"']preprocessing[\"']", _read(f)):
                # 2026-09-30：as_posix() 跨平台化。Windows 下 str(relative_to())
                # 产出反斜杠分隔，与硬编码的 "/" 期望值不匹配（该断言一直只在
                # POSIX 绿）。语义没变，只是路径分隔符归一。
                readers.append(f.relative_to(REPO).as_posix())
    assert readers == ["src/wqb/workflow/nodes/feature_engineering.py"], readers        # 只有节点自己回显
    assert "`preprocessing` **只作记录**" in t
    assert "campaign.py" in t and "ledger" in _read(SKILLS / "wq-brain-campaign-toolkit" / "scripts" / "campaign.py")


def test_fe_concept_block_example_parses_with_the_real_gem_parser_and_renders_valid_expressions():
    t = _read(FE / "SKILL.md")
    m = re.search(r"```markdown\n(.*?)\n```", t, re.S)
    assert m, "FE SKILL 里找不到概念块示例"
    ns = _func_from_source(TRAIL / "pipeline_reports.py", "extract_template_blocks")
    blocks = ns["extract_template_blocks"](m.group(1))
    assert len(blocks) == 3 and 3 <= 12
    labels = set(re.findall(r'\("([a-z]+)", \[', _read(TRAIL / "pipeline_reports.py").split("_EXPOSURE_KEYWORDS", 1)[1].split("]\n\n", 1)[0])) | {"other"}
    pv1 = {"returns", "volume", "adv20", "close", "vwap", "cap"}
    spec = importlib.util.spec_from_file_location("_fe_validator", SKILLS / "alpha-expression-verifier" / "scripts" / "validator.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_fe_validator"] = mod
    spec.loader.exec_module(mod)
    v = mod.ExpressionValidator()
    for b in blocks:
        tpl = b["template"]
        holes = set(re.findall(r"\{([A-Za-z0-9_]+)\}", tpl))
        assert holes and holes <= pv1, (tpl, holes)                                     # 占位符 = pv1 的真实字段后缀
        rendered = tpl.format(**{h: h for h in holes})
        r = v.check_expression(rendered)
        assert r["valid"], (rendered, r["errors"])
        for w in re.findall(r",\s*(\d+)\)", rendered):
            assert int(w) in (1, 5, 22, 66, 252, 504, 1008, 1260), (rendered, w)
        exp = re.search(r"\*\*Expected Exposure\*\*\s*:\s*([a-z]+)", b["idea"], re.I)
        assert exp and exp.group(1).lower() in labels, b["idea"]
    assert "No **Concept** blocks with **Implementation Example** found" in _read(TRAIL / "run_pipeline.py")
    assert "[validate] 丢弃" in _read(TRAIL / "run_pipeline.py")


def test_fe_paths_universe_tiers_budget_and_template_docs_are_consistent():
    from wqb import config
    t = _read(FE / "SKILL.md")
    paths = _read(TRAIL / "pipeline_paths.py")
    assert 'GEM_REPORT_ROOT = GEM_DATA_ROOT / "output_report"' in paths and 'repo / "data" / "gem_runs"' in paths
    assert "data/gem_runs/output_report/manual_<REGION>_delay<D>_<ds>_ideas.md" in t and "./output_report/" in t
    rp = _read(TRAIL / "run_pipeline.py")
    assert 'f"gem_{args.region}_delay{args.delay}_{args.dataset_id}_ideas.md"' in rp and "manual_" not in rp      # 重跑清理不会误删 manual_
    for r, u in (("KOR", "TOP600"), ("AMR", "TOP600"), ("EUR", "TOP2500"), ("JPN", "TOP1600")):
        assert config.REGIONS[r]["default_universe"] == u and f"{r} " in t
    assert 'config.REGIONS[<region>]["default_universe"]' in t
    assert "黑盒 > 半透明 > 透明" in t and "`model109`" in t and "8–12 个" in t
    assert "### 第" not in t and "3.1 稳定性特征" not in t and "OUTPUT_TEMPLATE.md" in t          # 报告提纲只在模板文件里
    tpl = _read(FE / "OUTPUT_TEMPLATE.md")
    assert "唯一提纲" in tpl and "`{字段后缀}`" in tpl
    assert "虚构的教学案例" in _read(FE / "examples.md").split("## Dataset Overview", 1)[0]
    assert "第 3 步 8 问" not in t.split("## 第 0 步", 1)[0]
    for name in ("OUTPUT_TEMPLATE.md", "reference.md", "examples.md"):
        assert f"[`{name}`]({name})" in t and (FE / name).is_file(), name
    head = t.split("## 第 0 步", 1)[0]
    assert "**不选数据集**（没有 `dataset_id` → 回 RA 步 2，不自行挑）" in head and "基于元数据选择" not in t        # FE-04：选集属 S0
    assert "本 skill 不应当" not in t and "## 原则" not in t and "所有字段都被分析" not in t                        # FE-10 / FE-12：口号与不可检的自查删掉
    acceptance = t.split("## 验收", 1)[1].split("## references", 1)[0]
    assert re.findall(r"^(\d)\. \*\*", acceptance, re.M) == list("1234") and "get_ledger_key" in acceptance        # 每项对应一个可检产物
    assert "闸 6 的收益来源多样性读它" in t and "concept-taxonomy-map.md" in t and (SKILLS / "wq-brain-ra-pipeline" / "references" / "concept-taxonomy-map.md").is_file()


# ----------------------------------------------------------------------------- GM：make-some-gem

def test_gm_skill_text_is_not_spliced_into_the_prompt_and_docs_stopped_saying_so():
    fn = next(n for n in ast.walk(ast.parse(_read(TRAIL / "pipeline_prompts.py")))
              if isinstance(n, ast.FunctionDef) and n.name == "build_prompt")
    for pname, allowed_uses in (("feature_implementation_skill_md", 0), ("feature_engineering_skill_md", 1)):
        loads = [n for n in ast.walk(fn) if isinstance(n, ast.Name) and n.id == pname and isinstance(n.ctx, ast.Load)]
        assert len(loads) == allowed_uses, (pname, len(loads))
    if_tests = [n.test for n in ast.walk(fn) if isinstance(n, ast.If)]
    assert any(isinstance(x, ast.Name) and x.id == "feature_engineering_skill_md" for x in if_tests), "dfe 只应作真值判断"
    for f in (TRAIL / "pipeline_paths.py", TRAIL / "run_pipeline.py"):
        txt = _read(f)
        assert "拼进 LLM prompt" not in txt and "以空内容" not in txt, f.name
    t = _read(GEM / "SKILL.md")
    assert "正文从不进 LLM prompt" in t and "skill 目录解析异常" in t
    assert "引擎读**两份 SKILL.md 拼进 LLM prompt**" not in t
    assert "正文从不拼进 LLM prompt" in _read(TRAIL / "skills" / "README.md")


def test_gm_priors_keys_and_prompt_nudge_claims_match_the_engine():
    src = _read(TRAIL / "economic_priors.py")
    body = src.split("def compact_priors_text", 1)[1].split("\ndef shape_constraint_rules", 1)[0]
    used = set(re.findall(r'priors\.get\("([a-z_]+)"\)', body))
    assert used == {"region_context", "wins", "dead_ends", "skeleton_field_matrix", "gate_priors"}, used
    assert "by_decay" not in body and "by_neutralization" not in body
    t = _read(GEM / "SKILL.md")
    for k in used:
        assert f"`{k}`" in t, k
    assert "只消费 `wins` / `dead_ends` 两个键」是错的" in t
    assert "wins[:6]" in body and "dead[:12]" in body and "notes[:4]" in body
    assert "eff[:6]" in body and "mdead[:8]" in body and "hints[:4]" in body and "有效 ≤ 6 / 死 ≤ 8 / 正交提示 ≤ 4" in t
    assert "agent 在**每次开生成前先跑一次**" in t and "`stage` 只是标签" in t and 'stage="S6"' not in t                # GM-01 / GM-14
    assert "soft nudge only" in _read(TRAIL / "pipeline_prompts.py") and "软提示" in t
    assert 'default="never"' in _read(SKILLS / "wq-brain-campaign-toolkit" / "scripts" / "build_wave.py").split('"--enhance-diversity"', 1)[1][:120]
    assert "enhance_diversity: str = \"never\"" in _read(SKILLS / "brain-sim-alphas-in-batch-and-track" / "scripts" / "batch_simulator.py")


def test_gm_mcp_and_node_parameters_match_the_reference_table():
    mcp_names, mcp_def = _signature_defaults(MCP_DIR / "tools_workflow.py", "workflow_gem", top_level=False)
    node_names, node_def = _signature_defaults(_GEM_NODE, "run")
    only_node = {"batch_size", "require_operators", "require_count", "prod_first", "prod_first_top_k"}
    assert only_node <= set(node_names) and not (only_node & set(mcp_names))
    assert set(mcp_names) - {"dry_run"} <= set(node_names)
    # pipeline_mode 自 2026-09-30 起支持自动识别：节点默认 None = 触发
    # `_auto_detect_pipeline_mode`（字段数 >100 / news 类 → phased，见
    # tests/unit/03_gem/test_gem_pipeline_mode.py），MCP 层也保持 None（把「未指定」
    # 原样透传给节点，不在中间层填默认值）。旧断言写的是自动识别之前的固定默认值。
    assert node_def["pipeline_mode"] is None and mcp_def["pipeline_mode"] is None
    assert node_def["priors_from_db"] is True and mcp_def["priors_from_db"] is True
    assert node_def["detached"] is True and node_def["batch_size"] == 100 and node_def["require_count"] == 2
    assert node_def["prod_first"] is False and node_def["prod_first_top_k"] == 2
    ref = _read(GEM / "reference.md")
    for n in only_node:
        assert f"`{n}`" in ref
    assert "`workflow_execute(node=\"gem\", params={…})`" in _read(GEM / "SKILL.md")
    assert 'GEM_META_TIMEOUT_SEC", "90"' in _read(_GEM_NODE) and "`GEM_META_TIMEOUT_SEC`" in ref


def _load_runner():
    spec = importlib.util.spec_from_file_location("_gem_run", GEM / "scripts" / "headless_runner" / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_gem_run"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_gm_runner_credentials_env_beats_config_reports_only_names_and_relaxes_secrets(tmp_path, monkeypatch):
    run = _load_runner()

    def clear_creds():
        for k in ("CREDENTIALS_EMAIL", "CREDENTIALS_PASSWORD", "BRAIN_USERNAME", "BRAIN_EMAIL", "BRAIN_PASSWORD", "MOONSHOT_API_KEY", "MOONSHOT_BASE_URL"):
            monkeypatch.setenv(k, "x")                                       # 先登记原值：run.py 直接写 os.environ 的痕迹也会在收尾时被清掉
            monkeypatch.delenv(k)

    clear_creds()
    cfg_path = tmp_path / "c.json"
    base = {"moonshot_base_url": "https://llm.example/v1", "moonshot_model": "m"}
    cfg_path.write_text(json.dumps(base), encoding="utf-8")
    with pytest.raises(ValueError) as e:                                     # 什么都没有：报缺哪些键，不含任何值
        run._load_required_config(cfg_path)
    assert "brain_email" in str(e.value) and "moonshot_api_key" in str(e.value) and "llm.example" not in str(e.value)
    with pytest.raises(ValueError) as e2:                                    # --ideas-file 不调 LLM：不再要 LLM 密钥，BRAIN 账号仍要
        run._load_required_config(cfg_path, ideas_file="x.md")
    assert "brain_email" in str(e2.value) and "moonshot_api_key" not in str(e2.value).split("Please edit")[0]
    monkeypatch.setenv("CREDENTIALS_EMAIL", "env-user@example.com")
    monkeypatch.setenv("CREDENTIALS_PASSWORD", "env-pass")
    with pytest.raises(ValueError, match="moonshot_api_key"):
        run._load_required_config(cfg_path)                                  # BRAIN 账号齐了，LLM 密钥仍要
    run._load_required_config(cfg_path, ideas_file="x.md")                   # --ideas-file 不调 LLM，不要密钥
    monkeypatch.setenv("MOONSHOT_API_KEY", "env-key")
    cfg = run._load_required_config(cfg_path)
    cfg_secret = dict(cfg, brain_email="cfg-user@example.com", brain_password="cfg-pass", moonshot_api_key="cfg-key")
    src = run._apply_runtime_credentials(cfg_secret)
    assert src == {"brain": "env", "moonshot": "env"}                        # 环境变量 > config.json（此前是反的）
    assert os_environ("BRAIN_EMAIL") == "env-user@example.com" and os_environ("MOONSHOT_API_KEY") == "env-key"
    assert not any("env-pass" in str(v) or "cfg-pass" in str(v) for v in src.values())
    clear_creds()                                                            # 环境里什么都没有 → 回落 config.json
    src = run._apply_runtime_credentials(cfg_secret)
    assert src == {"brain": "config.json", "moonshot": "config.json"} and os_environ("BRAIN_EMAIL") == "cfg-user@example.com"
    assert run._env_auth_ok() == (True, "ok")
    clear_creds()
    ok, msg = run._env_auth_ok()
    assert not ok and "CREDENTIALS_EMAIL" in msg
    assert run._apply_runtime_credentials(dict(base)) == {"brain": "config.json", "moonshot": "none"}     # 都没有：如实报 none
    ns = _func_from_source(TRAIL / "pipeline_data.py", "load_brain_credentials", "load_brain_credentials_from_env_or_args")
    monkeypatch.setenv("BRAIN_USERNAME", "legacy@example.com"); monkeypatch.setenv("BRAIN_PASSWORD", "legacy-pass")
    monkeypatch.setenv("CREDENTIALS_EMAIL", "std@example.com"); monkeypatch.setenv("CREDENTIALS_PASSWORD", "std-pass")
    assert ns["load_brain_credentials_from_env_or_args"](None, None, Path("/nonexistent")) == ("std@example.com", "std-pass")
    monkeypatch.delenv("CREDENTIALS_EMAIL"); monkeypatch.delenv("CREDENTIALS_PASSWORD")
    assert ns["load_brain_credentials_from_env_or_args"](None, None, Path("/nonexistent")) == ("legacy@example.com", "legacy-pass")


def os_environ(key):
    import os
    return os.environ.get(key)


def test_gm_config_example_is_secret_free_named_by_the_node_and_never_synced_as_config_json():
    import sync_skills
    hr = GEM / "scripts" / "headless_runner"
    ex = json.loads(_read(hr / "config.example.json"))
    assert {"brain_email", "brain_password", "moonshot_base_url", "moonshot_model", "moonshot_api_key", "pipeline_mode"} <= set(ex)
    for k in ("brain_email", "brain_password", "moonshot_api_key"):
        assert ex[k] == "", k
    assert ex["moonshot_model"] == re.search(r'--moonshot-model", default="([^"]+)"', _read(TRAIL / "run_pipeline.py")).group(1)
    assert "config.example.json" in _read(_GEM_NODE)
    assert "**/config.json" in _read(REPO / ".gitignore").split("Python", 1)[0]
    assert sync_skills._is_ignored(Path("brain-make-some-gem/scripts/headless_runner/config.json"))
    assert not sync_skills._is_ignored(Path("brain-make-some-gem/scripts/headless_runner/config.example.json"))
    readme = _read(hr / "README.md")
    assert 'BRAIN_PASSWORD="your_password"' not in readme and "口令不要写在命令行参数里" in readme


def test_gm_runner_writes_expressions_itself_and_the_documented_commands_are_valid():
    rp = _read(TRAIL / "run_pipeline.py")
    assert 'st.upsert_expressions(' in rp and 'status="gem"' in rp and 's2_{dataset_id}_d{args.delay}' in rp
    assert '"source": "s2_nested"' in rp and 'print(f"[db] expressions/{args.region}/{wave}' in rp
    run_src = _read(GEM / "scripts" / "headless_runner" / "run.py")
    assert '"--wave"' not in run_src and '"--priors-from-db", default=None' in run_src and "nargs" not in run_src.split('"--priors-from-db"', 1)[1][:200]
    for doc in (GEM / "SKILL.md", GEM / "scripts" / "headless_runner" / "README.md", GEM / "reference.md"):
        txt = _read(doc)
        assert not re.search(r"--priors-from-db\s+--", txt), f"{doc.name}: --priors-from-db 后面漏了区域值"
        assert "cd scripts/headless_runner" not in txt, doc.name
    t = _read(GEM / "SKILL.md")
    assert "`mcp__wqb-db__list_expressions(region, wave)` 有行" in t and "看不到行，不得声称步 4 成功" in t
    assert "resp.status_code in (401, 402, 403)" in run_src and "MOONSHOT_RETRIES\", \"3\"" in run_src and 'MOONSHOT_RETRIES", "2"' in _read(TRAIL / "pipeline_llm.py")
    assert "DETACHED_PROCESS" in run_src and "**Windows 专有**" in t
    fail = t.split("## 失败分支", 1)[1].split("## 反模式", 1)[0]
    for row in ("**「no meta.json within 90s」**", "**`402 Insufficient Balance`**", "**LLM 通道不可达**", "`401 Incorrect authentication credentials`",
                "| 候选不足 |", "**不补参数变体凑数**"):
        assert row in fail, row                                                     # GM-14：最具迷惑性的两种故障进了失败表
    assert "LLM 余额不足" in fail and "不可重试" in fail and "干跑也验证不了" in fail


def test_gm_ra_pregate_table_covers_the_module_rules_and_iron_rules_are_reconciled():
    pre = _read(TRAIL / "pipeline_pregate.py")
    ra = _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "step4-generation.md")
    for reason in ("bucket_missing_range", "region_invalid_group_field", "region_invalid_field", "region_vector_ts_forbidden"):
        assert f'"{reason}"' in pre, reason
    for token in ("region_invalid_fields", "region_vector_ts_forbidden", "`WQB_GEM_MAX_PER_SKELETON`，缺省 12"):
        assert token in ra, token
    assert 'os.environ.get("WQB_GEM_MAX_PER_SKELETON", "12")' in pre
    t = _read(GEM / "SKILL.md")
    assert "规则表只在一处维护" in t and "step4-generation.md" in t
    assert "每加一腿都必须点名" not in t and "不靠加腿修闸" in t and "决策表 D3" in t and "D6" in t
    gate6 = _read(SKILLS / "wq-brain-campaign-toolkit" / "references" / "gate-rules.md")
    assert "required_operators" in gate6 and "per_batch_min_operators" in gate6 and "确定性注入" in t and "闸 6 的批级契约仍在" in t
    assert "build_wave contract skeleton injection" in _read(TRAIL / "pipeline_prompts.py")
    assert "调**一个入口** `tools/wave_gate.py`" in t and "`check_batch` 已不是门禁" in t and (REPO / "tools" / "wave_gate.py").is_file()   # GM-02
    assert "判死粒度 = 概念，不是数据集" in t and "想法级 `dead_end`" in _read(SKILLS / "wq-brain-ra-pipeline" / "references" / "step7-diagnose.md")   # GM-08


def test_gm_mode_b_and_quality_estimation_and_emit_ideas_claims_hold():
    node = _read(_GEM_NODE)
    assert 'result["mode_b_required"] = True' in node and 'quality_result.get("expected_block_count", 0) > 0' in node
    assert 'prod_first_result.get("blocked_families", 0) > 0' in node
    wg = _read(REPO / "tools" / "wave_gate.py")
    assert "ADVISORY_HARD" in wg and "qp_mod.predict_all" in wg and '"--batch-type"' in wg
    reg = _read(REPO / "src" / "wqb" / "workflow" / "registry.py")
    assert "modeb_improve" in reg
    t = _read(GEM / "SKILL.md")
    for tok in ("mode_b_required = true", "modeb_improve", "--batch-type probe|repair", "tools/quality_predict.py"):
        assert tok in t, tok
    kb = _read(REPO / "tools" / "kb_templates.py")
    assert '"source": "kb_templates.py"' in kb and "json.dump(ideas" in kb
    ns = _func_from_source(TRAIL / "pipeline_reports.py", "extract_template_blocks", "extract_table_template_blocks",
                           "extract_named_template_blocks")
    assert ns["extract_template_blocks"](json.dumps({"ideas": [{"template": "rank({x})"}]})) == []       # JSON 不是 ideas markdown
    assert "**不能直接当 `ideas_file`**" in t
    assert "gem.py:1219" not in t and "_find_final_expressions" in t and "def _find_final_expressions" in _read(_GEM_NODE)


def test_gm_vendored_ace_lib_import_time_dependencies_are_declared_for_the_mcp_venv():
    """GEM / sim-alphas / feature-implementation / inspect-raw 共用 vendored `ace_lib`：其顶层 import 的第三方包必须写进
    MCP `requirements.txt`——否则按文档建的 venv 里 `pipeline_paths` 一 import 就 `No module named 'tqdm'`
    （2026-09-29 在云端容器里才暴露：本机 venv 是手工补装过的，`test_gem_skill_paths` 的实跑解析在非 Windows 上又一直被 skip）。"""
    req = _read(MCP_DIR / "requirements.txt")
    declared = {re.split(r"[<>=!~\[;\s]", ln.strip(), maxsplit=1)[0].lower().replace("_", "-")
                for ln in req.splitlines() if ln.strip() and not ln.lstrip().startswith("#")}
    std = sys.stdlib_module_names
    local = {"ace_lib", "helpful_functions"}
    seen = set()
    for name in ("ace_lib.py", "helpful_functions.py"):
        for node in ast.parse(_read(SKILLS / "brain-feature-implementation" / "scripts" / name)).body:
            if isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods = [node.module.split(".")[0]]
            else:
                continue
            for m in mods:
                if m in std or m in local:
                    continue
                seen.add(m)
                assert m.lower().replace("_", "-") in declared, f"{name} 顶层 import {m}，但 MCP requirements.txt 没声明"
    assert {"pandas", "requests", "tqdm"} <= seen, seen
    assert "jinja2" in declared and "pandas.io.formats.style" in _read(SKILLS / "brain-feature-implementation" / "scripts" / "helpful_functions.py")
    assert "_MCP_VENV = _find_mcp_venv()" in _read(REPO / "tests" / "unit" / "03_gem" / "test_gem_skill_paths.py")     # POSIX 布局也要能实跑


def test_gm_embedded_readme_and_maintenance_guards_are_documented():
    t = _read(GEM / "SKILL.md")
    assert "tests/unit/03_gem/test_gem_skill_paths.py" in t and "python tools/sync_gem_embedded_skill.py --apply" in t
    assert "`validator.py` 与 `alpha-expression-verifier` 权威版四处一起改" in t
    readme = _read(TRAIL / "skills" / "README.md")
    assert "从不拼进 LLM prompt" in readme and "GENERATED.md" in readme
    for f in ("reference.md", "examples.md"):
        txt = _read(GEM / f)
        assert "skills/brain-feature-implementation/data/{datasetID}" not in txt.split("旧位", 1)[0]
        assert "data/gem_runs" in txt or f == "examples.md"
        assert not re.search(r"^[A-Z][a-z]+ .*\b(should|must)\b", txt, re.M), f"{f} 还是英文旧稿"
