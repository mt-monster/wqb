# -*- coding: utf-8 -*-
"""INDEX.md / docs/env_and_switches.md 里「可由代码导出的表」与 INDEX 的「只做路由」定位（skills 审查 IX-01 / 05 / 10 / 13 / 24）。

通则（报告 X-7）：能由代码生成的表，由代码生成并嵌入文档，测试比对生成物与已提交文档。
本文件守：区域表 / 闸门阶梯 / 环境变量目录三块嵌入块；环境变量登记与代码双向一致；INDEX 不再夹带变更日志、迁移记录与契约；
场景路由表覆盖了最容易触发歧义的意图，且每个目标都真实存在。
"""
import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "Claude" / "skills"
INDEX = SKILLS / "INDEX.md"
ENV_DOC = ROOT / "docs" / "env_and_switches.md"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import index_tables as T  # noqa: E402


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ----------------------------------------------------------------------------- 三块生成表

def test_embedded_blocks_match_the_generators():
    bad = T.drifted()
    assert not bad, f"嵌入块与生成结果不一致：{bad}。修复：python tools/index_tables.py --apply"


def test_region_table_reflects_profile_and_directory_facts():
    from wqb.config import REGIONS
    rows = {r["region"]: r for r in T.region_rows()}
    assert set(rows) == set(REGIONS)                                    # 每个 config.REGIONS 都有一行
    assert rows["AMR"]["profile"] is True and rows["AMR"]["tracking"] is True     # AMR profile 已于 2026-09-28 补建，tracking 目录一直在
    assert rows["TWN"]["profile"] is True and rows["TWN"]["tracking"] is False
    # 不再把 DEU / IND / EUR 的 verdict 字面量写死：profile 会随实证升降档（DEU 2026-10-02 升 active，
    # IND / EUR 2026-10-04 降 probe-only），写死就会在每次升降档时把本测试变红——这正是 2026-10-04 修掉的失败。
    # 守的是「表 == profile」（下面的逐区循环），不是某一区当前取什么值。
    assert rows["MEA"]["entry_verdict"] == "frozen"                              # MEA 冻结是稳定事实
    table = T.render_regions()
    assert "| AMR | ✓ | ✓ | `active` | — |" in table
    assert "| MEA | ✓ | ✓ | `frozen` |" in table
    for r, row in rows.items():                                         # 表里的 entry_verdict 逐个等于 profile front-matter
        prof = T.PROFILES / f"{r}.md"
        if prof.is_file():
            assert T._front_matter_value(prof, "entry_verdict") == row["entry_verdict"]
    idx = _read(INDEX)
    assert "不要手改" in idx and "index_tables.py regions" in idx


def test_gate_ladder_numbers_come_from_config_and_the_old_single_hard_line_is_gone():
    from wqb import config as C
    table = T.render_ladder()
    assert f"> {C.PLATFORM_CHECK_LINES['low_2y_sharpe_min']:g}" in table
    assert f"Delay-1 > {C.PLATFORM_CHECK_LINES['low_sharpe_min']['delay1']:g}" in table
    assert f"< {C.GATES_PLATFORM['self_corr_max']:g}" in table and f"< {C.GATES_INTERNAL['self_corr_max']:g}" in table
    for const in ("PLATFORM_CHECK_LINES", "GATES_INTERNAL", "GATES_PLATFORM", "PRODCORR_CEILING"):
        assert const in table, const
    idx = _read(INDEX)
    assert "Sharpe>1.58" not in idx and "**平台硬线**" not in idx            # 「平台 Sharpe 硬线」曾对应 1.25 / 1.3 / 1.58 三个数
    assert "不是一个数" in idx and "LOW_SHARPE" in idx and "LOW_2Y_SHARPE" in idx


# ----------------------------------------------------------------------------- 环境变量目录

def test_env_registry_covers_every_env_var_read_by_code_and_nothing_is_stale():
    scanned = set(T.scan_env())
    registered = set(T.load_registry()["vars"])
    assert not (scanned - registered), f"代码读取了未登记的环境变量：{sorted(scanned - registered)}（写进 docs/env_registry.json 再 --apply）"
    assert not (registered - scanned), f"登记了但代码已不再读取的环境变量：{sorted(registered - scanned)}"


def test_env_registry_entries_are_well_formed_and_credentials_only_carry_names():
    reg = T.load_registry()
    cats = reg["categories"]
    for name, meta in reg["vars"].items():
        assert meta["cat"] in cats, name
        assert len(meta["what"]) >= 8, name
        assert not re.search(r"(?i)sk-[a-z0-9]{10,}|password\s*=\s*\S+|api[_-]?key\s*=\s*\S+", meta["what"]), f"{name} 的说明里疑似带了凭据值"
    for name in ("CREDENTIALS_EMAIL", "CREDENTIALS_PASSWORD"):
        assert reg["vars"][name]["cat"] == "cred" and "标准名" in reg["vars"][name]["what"]
    for name, meta in reg["vars"].items():
        if name.startswith("WQB_DISABLE_"):
            assert "仅测试" in meta["what"], f"{name} 是测试隔离开关，说明里必须写明「仅测试」"


def test_env_doc_has_the_generated_table_the_credential_register_and_the_switch_list():
    doc = _read(ENV_DOC)
    assert "index_tables.py env" in doc and "env_registry.json" in doc
    assert "## 1. 凭据来源与外发通道登记" in doc and "## 2. 变量目录（生成）" in doc and "## 3. CLI 开关" in doc
    assert "CREDENTIALS_EMAIL" in doc and "agent 不读 `.env` / `config.json`" in doc
    assert "WQB_GLOBAL_SLOTS" in T.embedded("env-table") and "WQB_GEM_MAX_PER_SKELETON" in T.embedded("env-table")
    for flag in re.findall(r"^\| `(--[a-z0-9-]+)", doc.split("## 3. CLI 开关", 1)[1], re.M):
        hit = any(flag in f.read_text(encoding="utf-8", errors="ignore")
                  for root in ("Claude/skills", "tools", "src") for f in (ROOT / root).rglob("*.py")
                  if "attic" not in f.parts and ".venv" not in f.parts)
        assert hit, f"§3 开关表里的 {flag} 在代码里找不到"


# ----------------------------------------------------------------------------- INDEX 只做路由

def test_index_is_a_routing_file_and_history_and_contract_moved_out():
    idx = _read(INDEX)
    assert len(idx.splitlines()) <= 300, "INDEX 又长回去了：契约进 CONTRACT.md、历史进 CHANGELOG.md、可导出的表由代码生成"
    for link in ("CONTRACT.md", "CHANGELOG.md", "GLOSSARY.md", "docs/env_and_switches.md", "submit-chain.md"):
        assert link in idx, f"INDEX 应指向 {link}"
    assert not re.search(r"⚠ ?20\d\d-\d\d-\d\d", idx), "INDEX 里又出现了带日期的 ⚠ 变更史条目——写进 CHANGELOG.md"
    assert not re.search(r"^## 20\d\d-\d\d-\d\d", idx, re.M)
    for legacy in ("旧名（禁用）", "外部扩展区迁入记录", "## 命名规范", "## frontmatter 规范", "### 共享产物归属表"):
        assert legacy not in idx, f"{legacy!r} 已迁出 INDEX"
    for moved_to in ("CONTRACT.md", "CHANGELOG.md"):
        assert (SKILLS / moved_to).is_file()
    assert "更早的历史（2026-09-29 从 INDEX 拆出" in _read(SKILLS / "CHANGELOG.md")


def test_index_states_which_copy_is_authoritative_and_that_sync_is_required():
    idx = _read(INDEX)
    sec = idx.split("## 权威副本与生效方式", 1)[1].split("\n## ", 1)[0]
    assert "编辑权威" in sec and "运行时优先" in sec and "改完必须" in sec and "sync_skills.py" in sec
    assert "AGENTS.md" in sec and "skill 多目标单向同步" in sec
    assert "skill 多目标单向同步" in _read(ROOT / "AGENTS.md")


def test_index_wq_py_definition_is_cross_platform_and_matches_the_pyenv_probe():
    idx = _read(INDEX)
    sec = idx.split("## 运行环境", 1)[1].split("\n## ", 1)[0]
    assert "Scripts/python.exe" in sec and ".venv/bin/python" in sec and "tools/_pyenv.py" in sec
    assert "不写裸 `python`" in sec
    spec = importlib.util.spec_from_file_location("_pyenv_t", ROOT / "tools" / "_pyenv.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    src = _read(ROOT / "tools" / "_pyenv.py")
    # 探测顺序：$WQ_PY → Scripts/python.exe → bin/python → 当前解释器（INDEX 表里的「自动探测」行）
    assert src.index("WQ_PY") < src.index('"Scripts"') < src.index('"bin"')
    assert mod.venv_python()


def test_index_lists_the_five_allowed_file_classes():
    idx = _read(INDEX)
    sec = idx.split("**允许写的文件只有五类**", 1)[1].split("\n## ", 1)[0]
    for cls in ("| A 真相源 |", "| B 运行态缓存 |", "| C 静态配置与凭证 |", "| D CLI 临时 `@file.json` |", "| E 人读产物 |"):
        assert cls in sec, cls
    assert "planning-with-files" in sec and "task_plan.md" in sec


ROUTING_INTENTS = (
    ("提交 alpha", ("worldquant-submit-alpha", "wq-brain-superalpha", "brain-alpha-judge")),
    ("相关性怎么办", ("check_self_correlation", "brain-calculate-alpha-selfcorr-quick", "brain-alpha-robustness")),
    ("批量回测 / 盯回测进度", ("workflow_batch_track", "wq-backtest-monitor", "brain-sim-alphas-in-batch-and-track")),
    ("这个 alpha 为什么没过 / 怎么改进", ("brain-how-to-pass-alpha-test", "wq-brain-alpha-optimization-v1", "brain-alpha-repair")),
)


def test_intent_routing_table_covers_the_ambiguous_intents_and_every_target_exists():
    idx = _read(INDEX)
    sec = idx.split("## 任务 → skill 场景路由表", 1)[1].split("\n## ", 1)[0]
    rows = [ln for ln in sec.splitlines() if ln.startswith("| ") and not ln.startswith("| 用户说") and not ln.startswith("|---")]
    assert len(rows) >= 12, "场景路由表少于 12 行"
    for intent, targets in ROUTING_INTENTS:
        row = next((r for r in rows if intent in r), None)
        assert row, f"路由表缺意图「{intent}」"
        for t in targets:
            assert t in row, f"「{intent}」一行应点名 {t}"
    skill_dirs = {p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()}
    named = set()
    for r in rows:
        named.update(re.findall(r"`(brain-[a-z0-9-]+|wq-brain-[a-z0-9-]+|wqb-[a-z0-9-]+|worldquant-[a-z0-9-]+|alpha-[a-z0-9-]+|pull-brain-skills|planning-with-files)`", r))
    assert named and named <= skill_dirs, f"路由表点名了不存在的 skill：{sorted(named - skill_dirs)}"
    assert len(named) >= 20, "路由表覆盖的 skill 太少"
    for path in re.findall(r"`((?:worldquant-submit-alpha|tools)/[A-Za-z0-9_./-]+\.(?:md|py))`", sec):
        base = SKILLS if path.startswith("worldquant") else ROOT
        assert (base / path).is_file(), path


def test_index_layers_stages_gates_and_counts_state_the_single_versions():
    idx = _read(INDEX)
    # IX-06 / IX-07：Ln ≡ Sn，L-INT 与迁移史、删除线行不再占位
    assert "Ln ≡ Sn" in idx and "L-INT" not in idx and "~~" not in idx and "共用运行环境约定" not in idx
    # IX-08：S5 = 否决 / 放行两种权力（只引用 submit-chain）；S3 产物 = DB；S6 日常回写归 RA 步 9；健康线三层不复写数字
    stages = idx.split("## 挖掘流水线阶段", 1)[1].split("\n## ", 1)[0]
    s5 = next(ln for ln in stages.splitlines() if ln.startswith("| S5 "))
    assert "否决" in s5 and "放行" in s5 and "submit-chain.md" in s5 and "提交层唯一权威" not in idx
    s3 = next(ln for ln in stages.splitlines() if ln.startswith("| S3 "))
    assert "backtest_results" in s3 and "不是真相源" in s3
    s6 = next(ln for ln in stages.splitlines() if ln.startswith("| S6 "))
    assert "日常回写由 RA 步 9 编排" in s6
    layers = stages.split("健康检查判据分层", 1)[1].split("\n\n", 1)[0]
    assert "回填带" in layers and not re.search(r"\d\.\d\d", layers), "三层健康线的数字只在 config / decision-table，本文不复写"
    # IX-09：索引只写「阶段 → 子命令」，实现细节留 toolkit / wqb-concurrency
    for detail in ("ThreadPoolExecutor", "N=min(", "--max-rounds>1", "linear_mix", "单批在飞串行"):
        assert detail not in idx, f"{detail!r} 是实现细节，不属于索引"
    # IX-11：闸表来自注册表，含子闸与附加闸
    for gate in ("| 闸2b |", "| 闸2b-2 |", "| 闸9 |"):
        assert gate in idx, gate
    # IX-12 / IX-14 / IX-16：计数只留现值；分工声明不再写 70/30；并发口径不再自成一节
    assert "`tools_submit` 0 是有意的" in idx and "submit_alpha` 工具已于" in idx
    assert "并发口径" not in idx and "旧模型" not in idx
    div = idx.split("## 分工声明", 1)[1].split("\n## ", 1)[0]
    assert "mode-b-qualification.md" in div and "无法度量的口号" in div and "（默认入口，70%）" not in div
    assert "MCP 直发批也过闸" in _read(SKILLS / "wq-brain-campaign-toolkit" / "references" / "gate-rules.md")
    # IX-15：嵌套副本四条纪律各有守护；KOR 历史脚本不再冒充「权威版本」
    nested = idx.split("## 嵌套副本", 1)[1].split("\n## ", 1)[0]
    assert nested.count("test_gem_skill_paths") >= 4 and "待清理（非「权威版本」）" in nested and "待用户裁定" in nested
    assert "tracking/KOR/scripts\\" not in idx
    # IX-22 / IX-23：配额只留指针（时区库计算，不写死 12:00）；带日期的区域硬事实不在 INDEX
    quota = idx.split("## 提交配额口径", 1)[1]
    assert "quota-and-tower.md" in quota and "America/New_York" in quota and "不要写死" in quota
    assert "平台区域硬事实" not in idx and "prod 竞速" not in idx and "pwRJmvP3" not in idx
