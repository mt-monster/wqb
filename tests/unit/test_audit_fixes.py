# -*- coding: utf-8 -*-
"""2026-09-06 dry-run 审计所修缺陷的回归守护。

每个测试对应一条实测到的故障，注释写清"原来怎么坏的"，避免日后被当成
多余约束删掉。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "tools"))


# ---------------------------------------------------------------------------
# 1. argv 契约校验（P0：--concurrency 被 argparse 拒绝却报 success）
# ---------------------------------------------------------------------------

def test_validate_argv_rejects_undeclared_flag(tmp_path):
    from wqb.workflow._common import validate_argv

    script = tmp_path / "fake.py"
    script.write_text(
        "import argparse\n"
        "ap = argparse.ArgumentParser()\n"
        "ap.add_argument('--dataset')\n"
        "ap.add_argument('--wave')\n",
        encoding="utf-8",
    )
    ok, err = validate_argv(["python", str(script), "--dataset", "d", "--wave", "w"])
    assert ok, err

    ok, err = validate_argv(
        ["python", str(script), "--dataset", "d", "--concurrency", "7"]
    )
    assert not ok
    assert "--concurrency" in err


def test_validate_argv_sees_args_from_local_helper_modules(tmp_path):
    """辅助模块注册的参数也算数（首版实现在 score_datasets.py 上误报过）。"""
    from wqb.workflow._common import validate_argv

    (tmp_path / "_lib").mkdir()
    (tmp_path / "_lib" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "_lib" / "common.py").write_text(
        "def add_campaign_arg(ap):\n    ap.add_argument('--campaign-dir')\n",
        encoding="utf-8",
    )
    script = tmp_path / "tool.py"
    script.write_text(
        "from _lib.common import add_campaign_arg\n"
        "import argparse\n"
        "ap = argparse.ArgumentParser()\n"
        "ap.add_argument('--dataset')\n"
        "add_campaign_arg(ap)\n",
        encoding="utf-8",
    )
    ok, err = validate_argv(["python", str(script), "--campaign-dir", "X"])
    assert ok, err


def test_validate_argv_fails_open_for_dispatcher_scripts(tmp_path):
    """自身零 add_argument 的派发器（如 toolkit campaign.py）不做校验，放行。"""
    from wqb.workflow._common import validate_argv

    script = tmp_path / "dispatch.py"
    script.write_text("SUB = {'assemble-priors': 'assemble_priors'}\n", encoding="utf-8")
    ok, err = validate_argv(["python", str(script), "--whatever", "x"])
    assert ok, err


def test_batch_track_command_has_no_concurrency_flag():
    """pipeline.py run 从未声明 --concurrency；带上它 argparse 直接 exit=2。"""
    from wqb.workflow import execute

    result = execute(
        "batch_track",
        {"region": "KOR", "wave": "_t", "dataset": "_t"},
        dry_run=True,
    )
    command = (result.output or {}).get("command", "")
    if not command:
        pytest.skip("toolkit 未安装，无命令可查")
    assert "--concurrency" not in command


# ---------------------------------------------------------------------------
# 2. campaign 子命令重复 append（S6 + assemble-priors 生成两次子命令）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("subcommand", ["assemble-priors", "diversity-extract"])
def test_campaign_subcommand_appears_once(subcommand):
    from wqb.workflow import execute

    result = execute(
        "campaign",
        {"region": "KOR", "stage": "S6", "subcommand": subcommand},
        dry_run=True,
    )
    commands = [
        s["command"] for s in (result.output or {}).get("steps", []) if s.get("command")
    ]
    if not commands:
        pytest.skip("toolkit 未安装或战役目录缺失")
    assert commands[-1].count(subcommand) == 1, (
        f"{subcommand} 在命令里出现了 {commands[-1].count(subcommand)} 次：{commands[-1]}"
    )


# ---------------------------------------------------------------------------
# 3. 幽灵算子黑名单自擦除（2026-09-04 被一次审计清空到只剩 neutralize）
# ---------------------------------------------------------------------------

def test_ghost_blacklist_survives_a_verified_only_audit():
    """用"只探平台已有算子"的结果重跑审计，ghost 不能被清空。

    原实现 library = verified | ghost 两者同源于 operators_verified.json，
    ghost 一旦写空就再也回不来（自擦除棘轮）。
    """
    from wqb.config import VERIFIED_SAFE_OPERATORS
    from wqb.expression.operator_audit import operator_audit

    result = operator_audit(VERIFIED_SAFE_OPERATORS)
    assert result["summary"]["total_ghost"] >= 15, (
        "幽灵算子黑名单被审计清空了 —— KNOWN_GHOST_SEED 应保证它不可被擦除"
    )


def test_known_ghost_seed_is_not_derived_from_audit_output():
    """种子必须是代码常量，不能来自 operators_verified.json。"""
    from wqb.config import KNOWN_GHOST_SEED

    assert {"ts_entropy", "group_normalize", "sigmoid", "tanh"} <= KNOWN_GHOST_SEED


# ---------------------------------------------------------------------------
# 4. 体检硬门（此前整条可执行路径零调用方）
# ---------------------------------------------------------------------------

def test_field_inspect_gate_reports_unavailable_instead_of_passing(tmp_path, monkeypatch):
    """没有体检包时必须明说"未生效"，绝不能伪装成通过。"""
    import field_inspect_gate as fig

    monkeypatch.setattr(fig, "INSPECT_DIR", str(tmp_path))
    report = fig.check_expressions(["rank(x)"], "USA", "nosuchds")
    assert report["status"] == "unavailable"
    assert report["enforced"] is False
    assert "webdata_quality" in report["hint"]


def test_field_inspect_gate_blocks_low_coverage_without_backfill(tmp_path, monkeypatch):
    import field_inspect_gate as fig

    monkeypatch.setattr(fig, "INSPECT_DIR", str(tmp_path))
    pack = {
        "fields": {
            "ds": {
                "lowcov": {
                    "metadata": {
                        "coverage_ratio": 0.2,
                        "skewness": 0.0,
                        "kurtosis": 1.0,
                        "distribution_shape": "normal",
                    },
                    "advices": [],
                }
            }
        }
    }
    (tmp_path / "field_inspect_usa_ds.json").write_text(
        json.dumps(pack), encoding="utf-8"
    )

    report = fig.check_expressions(
        ["rank(lowcov)", "rank(ts_backfill(lowcov, 120))"], "USA", "ds"
    )
    assert report["enforced"] is True
    assert len(report["violations"]) == 1
    assert "rank(lowcov)" == report["violations"][0]["expression"]


def test_field_inspect_gate_ignores_kwargs_and_group_vars():
    import field_inspect_gate as fig

    assert fig.expression_fields("winsorize(fat_field, std=4)") == ["fat_field"]
    assert fig.expression_fields("group_rank(ts_delta(f_x, 22), subindustry)") == ["f_x"]


# ---------------------------------------------------------------------------
# 5. 指纹回填（30.8% 为 NULL，去重全靠它）
# ---------------------------------------------------------------------------

def test_expression_fingerprint_is_whitespace_and_case_insensitive():
    from wqb.store._expressions import expression_fingerprint

    a = expression_fingerprint("rank(ts_delta(close, 22))")
    b = expression_fingerprint("rank( ts_delta( Close , 22 ) )")
    assert a == b
    assert len(a) == 12
    assert a != expression_fingerprint("rank(ts_delta(open, 22))")


# ---------------------------------------------------------------------------
# 6. 混信号毒模式（CLAUDE.md 禁令，此前 gate 不拦）
# ---------------------------------------------------------------------------

def test_weighted_signal_mix_poison_pattern():
    import re

    cfg = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "config" / "platform_constraints.json"
    if not cfg.is_file():
        pytest.skip("toolkit config 不在仓库内")
    patterns = json.loads(cfg.read_text(encoding="utf-8"))["poison_patterns"]
    entry = next((p for p in patterns if p["name"] == "weighted_signal_mix"), None)
    assert entry is not None, "混信号毒模式规则缺失"
    rx = re.compile(entry["regex"])

    # ASI 实测形状：同骨架权重微调
    assert rx.search("add(add(0.4*rank(a), 0.3*rank(b)), 0.3*rank(c))")
    assert rx.search("0.5*rank(a) + 0.25*rank(b)")
    # 合法写法不得误伤：分母 eps 保护、单腿缩放
    assert not rx.search("divide(flow, add(stock, 0.0001))")
    assert not rx.search("multiply(rank(a), 0.5)")
    assert not rx.search("rank(ts_delta(divide(ts_backfill(fnd72_ebitda), 120), 22))")


# ---------------------------------------------------------------------------
# 7. 异步任务状态（此前 MCP 侧无任何查询工具，两套布局互不兼容）
# ---------------------------------------------------------------------------

def test_task_reader_handles_both_layouts(tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path))
    from wqb.workflow import tasks

    # flat 布局（campaign / feature_engineering）
    (tmp_path / "campaign_KOR_S0_1.json").write_text(
        json.dumps({"task_id": "campaign_KOR_S0_1", "success": True,
                    "finished_at": "2026-09-06T00:00:00"}),
        encoding="utf-8",
    )
    # dir 布局（gem / batch_track）
    d = tmp_path / "batch_track_KOR_1"
    d.mkdir()
    (d / "meta.json").write_text(
        json.dumps({"task_id": "batch_track_KOR_1", "pid": None,
                    "failed_at_launch": "argparse rejected"}),
        encoding="utf-8",
    )
    (d / "stderr.log").write_text("unrecognized arguments: --concurrency 7",
                                  encoding="utf-8")

    flat = tasks.get_task("campaign_KOR_S0_1")
    assert flat["layout"] == "flat" and flat["status"] == "succeeded"

    diry = tasks.get_task("batch_track_KOR_1")
    assert diry["layout"] == "dir" and diry["status"] == "failed"
    assert "--concurrency" in diry["stderr_tail"]

    listed = tasks.list_tasks()
    assert {t["task_id"] for t in listed} == {
        "campaign_KOR_S0_1", "batch_track_KOR_1",
    }


def test_chain_extracts_task_id_from_nested_steps():
    from wqb.workflow.executor import WorkflowExecutor

    assert WorkflowExecutor._extract_task_id({"task_id": "a"}) == "a"
    assert WorkflowExecutor._extract_task_id(
        {"steps": [{"step": "x"}, {"step": "y", "task_id": "b"}]}
    ) == "b"
    assert WorkflowExecutor._extract_task_id({"steps": []}) is None


# ---------------------------------------------------------------------------
# 8. skill 安装位与仓库同步（安装位曾落后仓库约两周）
# ---------------------------------------------------------------------------

def test_sync_skills_reports_no_drift():
    """仓库 Claude/skills 与 Agent 实际加载的安装位必须一致。

    2026-09-06 实测：安装位的 brain-makeSomeGem 停在 2026-08-22、仓库已是
    09-05；ra-pipeline 的体检包路径仓库已修正而安装位仍是旧文。Agent 读旧
    SOP、测试读新文，两边各自"自洽"，只有运行时才炸。
    """
    sync = REPO_ROOT / "tools" / "sync_skills.py"
    if not sync.is_file():
        pytest.skip("sync_skills.py 不存在")

    sys.path.insert(0, str(REPO_ROOT / "tools"))
    import sync_skills

    if not sync_skills.SOURCE.is_dir():
        pytest.skip("仓库 Claude/skills 不在场")
    target = sync_skills.resolve_install_root()
    if target is None:
        pytest.skip("本机未找到 skill 安装位")

    only_source, changed, _only_target = sync_skills.diff_tree(
        sync_skills.SOURCE, target
    )
    assert not (only_source or changed), (
        f"skill 安装位与仓库漂移：缺 {[str(p) for p in only_source[:5]]}，"
        f"陈旧 {[str(p) for p in changed[:5]]}。"
        f"跑 `python tools/sync_skills.py` 同步。"
    )


# ---------------------------------------------------------------------------
# 9. 去重历史不再按状态漏掉 gem/raw（1 681 行里 759 行是重复）
# ---------------------------------------------------------------------------

def test_history_expressions_includes_generated_by_default(tmp_path):
    from wqb.store import CampaignStore

    store = CampaignStore(str(tmp_path / "t.db"))
    store.upsert_expressions("KOR", "1", [{"expression": "rank(a)"}], dataset="ds",
                             status="gem")
    store.upsert_expressions("KOR", "2", [{"expression": "rank(b)"}], dataset="ds",
                             status="selected")

    default = set(store.history_expressions("KOR"))
    assert {"rank(a)", "rank(b)"} <= default, (
        "gem 状态的表达式必须进入去重历史，否则同一条可以一波一波重复生成"
    )

    legacy = set(store.history_expressions("KOR", include_generated=False))
    assert "rank(a)" not in legacy and "rank(b)" in legacy
    store.close()


def test_history_expressions_still_honours_exclude_waves(tmp_path):
    """本波自己的输入仍要排除掉 —— 这才是 exclude_waves 的职责。"""
    from wqb.store import CampaignStore

    store = CampaignStore(str(tmp_path / "t2.db"))
    store.upsert_expressions("KOR", "9", [{"expression": "rank(x)"}], dataset="ds",
                             status="gem")
    assert "rank(x)" not in set(store.history_expressions("KOR", exclude_waves=["9"]))
    store.close()


# ---------------------------------------------------------------------------
# 10. 实测产出率工具（选区最硬先验，此前库里躺着没人查）
# ---------------------------------------------------------------------------

def test_get_mining_yield_separates_conversion_from_yield():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_wqb_db_mcp", str(REPO_ROOT / "wqb_db_mcp.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    out = mod.get_mining_yield()
    assert "rows" in out and "totals" in out
    for row in out["rows"]:
        assert {"region", "expressions", "backtested", "conversion",
                "passed", "yield_rate"} <= set(row)
        # 两个比率是不同的量：conversion 看流水线，yield_rate 看标的
        if row["backtested"]:
            assert row["yield_rate"] == pytest.approx(
                row["passed"] / row["backtested"], abs=1e-4
            )
        else:
            assert row["yield_rate"] is None
    # 无回测记录的排最后，便于选区时直接读第一行
    seen_none = False
    for row in out["rows"]:
        if row["yield_rate"] is None:
            seen_none = True
        elif seen_none:
            pytest.fail("yield_rate 为 None 的行必须排在有值行之后")


# ---------------------------------------------------------------------------
# 11. 体检包导出（--export-expr 自诞生起恒产出 0 字段）
# ---------------------------------------------------------------------------

def test_export_expr_derives_dataset_id_without_region():
    """dataSetList.json 条目形如 `analyst11_USA_TOP3000_Delay1`（四段）。

    原实现 `rsplit('_', 2)[0]` 只切掉 universe/delay，留下 `analyst11_USA`，
    随后又拼一次 region → `startswith('analyst11_USA_USA_')` 永不匹配 →
    candidates 为空 → continue → 导出 0 字段。现存两份体检包 fields 为 {}
    就是这么来的，体检硬门因此一直无米下锅。
    """
    name = "analyst11_USA_TOP3000_Delay1"
    assert name.rsplit("_", 3)[0] == "analyst11"
    assert name.startswith(f"{name.rsplit('_', 3)[0]}_USA_")
    # 旧写法的反例，保留以说明为何不能退回去
    assert name.rsplit("_", 2)[0] == "analyst11_USA"
    assert not name.startswith("analyst11_USA_USA_")


def test_webdata_quality_export_uses_four_part_split():
    """守护源码本身，防止有人"顺手"改回 rsplit('_', 2)。"""
    src = (REPO_ROOT / "tools" / "webdata_quality.py").read_text(
        encoding="utf-8", errors="replace"
    )
    marker = "rsplit('_', 3)[0]"
    assert marker in src, (
        f"webdata_quality.py 的 --export-expr 数据集名推导应为 {marker}；"
        "改回 rsplit('_', 2) 会让导出恒为 0 字段"
    )


def test_generated_field_inspect_packs_are_loadable():
    """已生成的体检包必须能被闸读出非空字段（有包才测）。"""
    import field_inspect_gate as fig

    inspect_dir = Path(fig.INSPECT_DIR)
    if not inspect_dir.is_dir():
        pytest.skip("tracking/mining 不存在")
    packs = sorted(inspect_dir.glob("field_inspect_*.json"))
    non_empty = [p for p in packs if fig.load_pack(*_parse_pack_name(p))]
    if not packs:
        pytest.skip("尚未生成体检包（跑 tools/gen_field_inspect_packs.py）")
    assert non_empty, (
        f"{len(packs)} 份体检包全部为空 —— 说明 --export-expr 又回到 0 字段状态"
    )


def _parse_pack_name(path: Path):
    stem = path.stem[len("field_inspect_"):]
    region, _, dataset = stem.partition("_")
    return region, dataset
