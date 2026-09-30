# -*- coding: utf-8 -*-
"""S-F：契约拆分（CONTRACT.md）、description 规范、凭据来源登记与 ace_lib 明文落盘（skills 审查 IX-18 / IX-19 / IX-20 / IX-21 / T0-15 / X-9）。

- `Claude/skills/CONTRACT.md` 承接从 INDEX 拆出的契约，AGENTS.md 只留摘要与指针；
- 每个 SKILL.md 的 `description` 是触发条件而非功能清单：≤ 300 字（此前最长 702 字）；
- 凭据来源登记（`docs/env_and_switches.md` §1）必须与代码一致：每个消费者都认标准名 `CREDENTIALS_*`；
- vendored `ace_lib.get_credentials()` 会把口令明文写进 `~/secrets/platform-brain.json`：调用 `ace_lib.start_session()` 的脚本必须先覆盖它。
"""
import ast
import json
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "Claude" / "skills"
CONTRACT = SKILLS / "CONTRACT.md"
ENV_DOC = ROOT / "docs" / "env_and_switches.md"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def _description(skill_md: Path) -> str:
    """不引入 PyYAML（MCP venv 没装）：只取 frontmatter 里的 `description:` 一行，兼容双引号 / 单引号 / 无引号。"""
    fm = re.match(r"^---\n(.*?)\n---\n", _read(skill_md), re.S).group(1)
    m = re.search(r"^description:\s*(.+)$", fm, re.M)
    assert m, f"{skill_md}: 缺 description"
    val = m.group(1).strip()
    if val[:1] in "\"'" and val[-1:] == val[:1]:
        val = val[1:-1]
    return val


# ----------------------------------------------------------------------------- CONTRACT

def test_contract_carries_frontmatter_boundary_naming_shared_artifacts_and_gates():
    t = _read(CONTRACT)
    for h in ("## 1. frontmatter 规范", "## 2. 正文必备段：`## 职责边界`", "## 3. 命名规范", "## 4. 共享产物归属", "## 5. 质量门禁"):
        assert h in t, h
    for field in ("`name`", "`layer`", "`description`", "`last_verified`", "`allowed-tools`", "`user-invocable`", "`version`", "`hooks`"):
        assert field in t, field
    assert "≤ 300 字" in t and "缺省 = 继承宿主默认权限" in t and "skill_capabilities_baseline.json" in t
    assert "白名单内的 skill 可声明" in t and "上游版本号" in t
    assert "本 skill 负责" in t and "本 skill 不做" in t and "上游 / 下游" in t
    assert "PLATFORM_CHECK_LINES" in t and "WAIT_THRESHOLDS" in t                       # 硬裁定①的权威常量清单跟上了 config
    for name in ("wave_results", "registry_empirical", "ledger_kv", "expressions", "field_catalog", "priors_snapshot_<region>", "submit_ready"):
        assert f"`{name}`" in t, name
    assert "docs/ledger_keys.json" in t and "test_ledger_key_catalog.py" in t
    assert (ROOT / "tests" / "unit" / "01_store_db" / "test_ledger_key_catalog.py").is_file() and (ROOT / "docs" / "ledger_keys.json").is_file()
    assert "失败于环境 vs 失败于内容" in t and "WQ_SKILLS_DIR" in t
    # 兼容 tests/unit/<主题子目录>/ 的新布局（`(?:[0-9]{2}_[a-z_]+/)?` 匹配可选子目录）
    for rel in re.findall(r"tests/unit/((?:[0-9]{2}_[a-z_]+/)?test_[a-z_]+\.py)", t):
        assert (ROOT / "tests" / "unit" / rel).is_file(), f"CONTRACT 提到的 {rel} 不存在"


def test_contract_shared_artifact_table_matches_the_code_owners():
    t = _read(CONTRACT)
    assert "wqb.wave_results_contract.upsert_wave_result" in t and (ROOT / "src" / "wqb" / "wave_results_contract.py").is_file()
    assert "wqb.registry_contract" in t and (ROOT / "src" / "wqb" / "registry_contract.py").is_file()
    assert "wqb.store.submit_queue" in t and "CREATE TABLE IF NOT EXISTS submit_ready" in _read(ROOT / "src" / "wqb" / "store" / "submit_queue.py")
    assert 'subcommand=assemble-priors' in t


def test_agents_md_points_at_the_contract_and_no_longer_says_repair_recipes_moved():
    a = _read(ROOT / "AGENTS.md")
    assert "Claude/skills/CONTRACT.md" in a and "### 8.10 INDEX 拆分" in a
    assert "配方已上移" not in a and "配方在本 skill 内" in a          # RE-01 / P0-6：optimization-v1 里并没有这些配方
    assert "$WQ_PY tools/sync_skills.py" in a and "改完必须" in a


# ----------------------------------------------------------------------------- description 规范

def test_every_skill_description_is_a_trigger_statement_under_300_chars():
    too_long, too_short = [], []
    for d in _skill_dirs():
        n = len(_description(d / "SKILL.md"))
        if n > 300:
            too_long.append(f"{d.name}: {n}")
        if n < 30:
            too_short.append(f"{d.name}: {n}")
    assert not too_long, f"description 超过 300 字（只写「何时触发 + 范围 + 不做」，细节进正文）：{too_long}"
    assert not too_short, f"description 过短，写不出触发条件：{too_short}"


def test_no_skill_description_is_an_english_duplicate_of_the_chinese_one():
    """此前 judge 的 description 把同一句话中英各写一遍（303 字）；触发条件只需一份。"""
    for d in _skill_dirs():
        desc = _description(d / "SKILL.md")
        latin_run = re.findall(r"[A-Za-z][A-Za-z ,'\-]{80,}", desc)
        assert not latin_run, f"{d.name} 的 description 里有整句英文重复：{latin_run[0][:40]}…"


# ----------------------------------------------------------------------------- 凭据来源登记 ↔ 代码

CONSUMERS = (
    ("world-quant-brain-mcp/brain_config.py", "MCP 服务"),
    ("Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/common.py", "toolkit"),
    ("Claude/skills/brain-make-some-gem/scripts/headless_runner/run.py", "GEM runner"),
    ("Claude/skills/brain-sim-alphas-in-batch-and-track/scripts/batch_simulator.py", "sim-alphas"),
    ("Claude/skills/brain-feature-implementation/scripts/fetch_dataset.py", "feature-implementation"),
    ("Claude/skills/brain-alpha-judge/scripts/vendor/load_credentials.py", "judge"),
    ("Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/skill.py", "selfcorr-quick"),
    ("Claude/skills/brain-inspect-raw-template-create-setting/scripts/load_credentials.py", "inspect-raw"),
    ("tools/fetch_all_universes.py", "fetch_all_universes"),
    ("tools/forum_recon.py", "forum_recon"),
)


def test_credential_register_lists_every_consumer_and_each_one_reads_the_standard_names():
    doc = _read(ENV_DOC).split("## 2. 变量目录", 1)[0]
    for rel, label in CONSUMERS:
        src = _read(ROOT / rel)
        assert "CREDENTIALS_EMAIL" in src and "CREDENTIALS_PASSWORD" in src, f"{label}（{rel}）没有认标准名 CREDENTIALS_*"
    for label in ("MCP 服务 `wq-brain-http`", "toolkit", "GEM runner", "sim-alphas", "feature-implementation", "judge", "selfcorr-quick",
                  "inspect-raw", "fetch_all_universes", "forum_recon"):
        assert label in doc, f"凭据登记表缺消费者：{label}"
    assert "标准名 = `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`" in doc
    assert "外发通道" in doc and "BRAIN_JUDGE_LLM_API_KEY" in doc and "OPENAI_API_KEY" in doc and "MOONSHOT_API_KEY" in doc


def test_register_states_the_documented_priority_orders_for_the_two_that_changed():
    doc = _read(ENV_DOC)
    gem = next(ln for ln in doc.splitlines() if ln.startswith("| GEM runner"))
    assert gem.index("环境") < gem.index("config.json")                                   # 环境变量 > config.json（DEC-56）
    sim = next(ln for ln in doc.splitlines() if ln.startswith("| sim-alphas"))
    assert sim.index("环境") < sim.index("configs/config.json") < sim.index("MCP `.env`")
    assert "**否**（已覆盖 `ace_lib.get_credentials`）" in sim


# ----------------------------------------------------------------------------- batch_simulator：优先级与不落盘

def _batch_simulator_ns(tmp_path, fake_ace):
    import logging
    path = SKILLS / "brain-sim-alphas-in-batch-and-track" / "scripts" / "batch_simulator.py"
    tree = ast.parse(_read(path))
    names = {"_set_brain_env", "_pin_ace_credentials", "load_credentials_from_env", "load_credentials_from_config",
             "load_credentials_from_dotenv", "load_credentials_fallback", "_parse_dotenv"}
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in body} == names
    ns = {"os": os, "json": json, "Path": Path, "Dict": dict, "logger": logging.getLogger("bs-test"),
          "SKILL_ROOT": tmp_path, "ace_lib": fake_ace, "__file__": str(tmp_path / "scripts" / "batch_simulator.py")}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), ns)
    return ns


class _FakeAce:
    def get_credentials(self):                                          # 模拟 vendored ace_lib 的危险默认行为
        raise AssertionError("ace_lib.get_credentials 不应被调用——它会明文落盘 / input() 提问")


def _clear(monkeypatch):
    for k in ("CREDENTIALS_EMAIL", "CREDENTIALS_PASSWORD", "BRAIN_USERNAME", "BRAIN_EMAIL", "BRAIN_PASSWORD",
              "BRAIN_CREDENTIAL_EMAIL", "BRAIN_CREDENTIAL_PASSWORD"):
        monkeypatch.setenv(k, "x")
        monkeypatch.delenv(k)


def test_batch_simulator_reads_env_before_config_json_before_dotenv(tmp_path, monkeypatch):
    _clear(monkeypatch)
    ns = _batch_simulator_ns(tmp_path, _FakeAce())
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"email": "cfg@example.invalid", "password": "cfg-pass"}), encoding="utf-8")
    monkeypatch.setenv("CREDENTIALS_EMAIL", "std@example.invalid")
    monkeypatch.setenv("CREDENTIALS_PASSWORD", "std-pass")
    monkeypatch.setenv("BRAIN_EMAIL", "legacy@example.invalid")
    monkeypatch.setenv("BRAIN_PASSWORD", "legacy-pass")
    assert ns["load_credentials_from_env"]() is True
    assert os.environ["BRAIN_CREDENTIAL_EMAIL"] == "std@example.invalid"           # 标准名优先于旧别名
    _clear(monkeypatch)
    assert ns["load_credentials_from_env"]() is False                               # 环境里什么都没有：不误报成功
    assert ns["load_credentials_from_config"](str(cfg)) is True                     # 然后才轮到 config.json
    assert os.environ["BRAIN_CREDENTIAL_EMAIL"] == "cfg@example.invalid"
    _clear(monkeypatch)
    monkeypatch.setenv("BRAIN_USERNAME", "legacy-only@example.invalid")
    monkeypatch.setenv("BRAIN_PASSWORD", "legacy-pass")
    assert ns["load_credentials_from_env"]() is True and os.environ["BRAIN_CREDENTIAL_EMAIL"] == "legacy-only@example.invalid"
    src = (SKILLS / "brain-sim-alphas-in-batch-and-track" / "scripts" / "batch_simulator.py").read_text(encoding="utf-8")
    main = src.split("def main()", 1)[1]
    assert main.index("load_credentials_from_env()") < main.index("load_credentials_from_config(") < main.index("load_credentials_from_dotenv()")
    assert "_pin_ace_credentials()" in main and main.index("_pin_ace_credentials()") < main.index("ace_lib.start_session()")
    _clear(monkeypatch)


def test_pinning_ace_credentials_replaces_the_plaintext_persisting_default(tmp_path, monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    fake = _FakeAce()
    ns = _batch_simulator_ns(tmp_path, fake)
    monkeypatch.setenv("BRAIN_CREDENTIAL_EMAIL", "pin@example.invalid")
    monkeypatch.setenv("BRAIN_CREDENTIAL_PASSWORD", "pin-pass")
    ns["_pin_ace_credentials"]()
    assert fake.get_credentials() == ("pin@example.invalid", "pin-pass")          # 覆盖后直接返回环境里的凭据
    assert not (tmp_path / "secrets").exists()                                        # 没有任何落盘


def test_every_script_that_starts_an_ace_lib_session_overrides_get_credentials():
    """vendored `ace_lib.get_credentials()`：`~/secrets/platform-brain.json` 不存在时 `input()` 提问并把邮箱 / 口令**明文写盘**。"""
    ace = _read(SKILLS / "brain-feature-implementation" / "scripts" / "ace_lib.py")
    assert 'platform-brain.json' in ace and "json.dump(data, file)" in ace           # 危险默认行为仍在（这就是要覆盖它的原因）
    callers = []
    for root in (SKILLS, ROOT / "tools", ROOT / "src"):
        for f in root.rglob("*.py"):
            if any(x in f.parts for x in (".venv", "attic", "__pycache__", "tests")) or f.name == "ace_lib.py":
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"\bace_lib\.start_session\(", text):
                callers.append(f)
    assert callers, "找不到 ace_lib.start_session() 的调用方？扫描口径变了"
    for f in callers:
        assert re.search(r"ace_lib\.get_credentials\s*=", _read(f)), (
            f"{f.relative_to(ROOT)} 调用 ace_lib.start_session() 却没覆盖 ace_lib.get_credentials——"
            "口令会被明文写进 ~/secrets/platform-brain.json（skills 审查 T0-15）")


# ----------------------------------------------------------------------------- last_verified 必须随内容变化（X-17 #10 / X-19）

def _git(*args):
    import subprocess
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    return r.returncode, r.stdout.strip()


def test_last_verified_is_not_older_than_the_last_commit_that_changed_the_skills_docs():
    """此前 33 / 33 个 skill 是同一天的批量戳，掩盖了内容过期。规则：skill 目录下的 *.md（不含 scripts / data）最近一次提交的日期，
    不得晚于该 SKILL.md 的 `last_verified`——改了文档就得重新核对并更新这个日期。浅克隆里 git 把边界提交当作全量新增，日期不可信，跳过。"""
    code, out = _git("rev-parse", "--is-shallow-repository")
    if code != 0:
        pytest.skip("不在 git 仓库里")
    if out == "true":
        pytest.skip("浅克隆：边界提交会让所有文件的「最近提交日期」失真")
    stale = []
    for d in _skill_dirs():
        m = re.search(r"^last_verified:\s*(\d{4}-\d{2}-\d{2})", _read(d / "SKILL.md"), re.M)
        assert m, f"{d.name} 缺 last_verified"
        # 排除项按「相对 skill 目录」的路径段判断——绝对路径里一定有 `skills`（Claude/skills/…），按绝对路径判会把全部文档排除、
        # 让 `git log` 退化成「整个仓库最近一次提交」（浅克隆里跳过所以一直没暴露）
        docs = [str(p.relative_to(ROOT)) for p in d.rglob("*.md")
                if not any(x in p.relative_to(d).parts for x in ("scripts", "data", "outputs", "output_report", "skills"))]
        assert docs, f"{d.name} 没有可核对的文档（排除规则把它们全排掉了？）"
        code, last = _git("log", "-1", "--format=%cs", "--", *docs)
        if code == 0 and last and m.group(1) < last:
            stale.append(f"{d.name}: last_verified={m.group(1)} < 文档最近提交 {last}")
    assert not stale, "文档改了但 last_verified 没更新（重新核对后改成当天日期）：\n  " + "\n  ".join(stale)


def test_last_verified_dates_are_well_formed_and_not_in_the_future():
    import datetime as dt
    today = dt.date.today()
    for d in _skill_dirs():
        m = re.search(r"^last_verified:\s*(\S+)", _read(d / "SKILL.md"), re.M)
        assert m and re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(1)), f"{d.name}: last_verified 格式不对"
        assert dt.date.fromisoformat(m.group(1)) <= today, f"{d.name}: last_verified 在未来"
