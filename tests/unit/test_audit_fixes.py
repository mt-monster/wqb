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
    """仓库 Claude/skills 与**全部** Agent 安装位必须一致。

    2026-09-06 实测：安装位的 brain-make-some-gem 停在 2026-08-22、仓库已是
    09-05；ra-pipeline 的体检包路径仓库已修正而安装位仍是旧文。Agent 读旧
    SOP、测试读新文，两边各自"自洽"，只有运行时才炸。

    2026-09-10 审计：此前只校验首个安装位（`resolve_install_root()`），
    导致 ~/.codex、~/.workbuddy 等宿主分叉无人察觉。现改为校验全部安装位。
    """
    sync = REPO_ROOT / "tools" / "sync_skills.py"
    if not sync.is_file():
        pytest.skip("sync_skills.py 不存在")

    sys.path.insert(0, str(REPO_ROOT / "tools"))
    import sync_skills

    if not sync_skills.SOURCE.is_dir():
        pytest.skip("仓库 Claude/skills 不在场")
    targets = sync_skills.resolve_install_roots()
    if not targets:
        pytest.skip("本机未找到 skill 安装位")

    drifted = []
    for target in targets:
        only_source, changed, _only_target = sync_skills.diff_tree(
            sync_skills.SOURCE, target
        )
        if only_source or changed:
            drifted.append((target, only_source[:3], changed[:3]))
    assert not drifted, (
        "以下 skill 安装位与仓库漂移："
        + "；".join(
            f"{t}（缺 {[str(p) for p in src]}，陈旧 {[str(p) for p in chg]}）"
            for t, src, chg in drifted
        )
        + " 跑 `python tools/sync_skills.py` 同步。"
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


# ---------------------------------------------------------------------------
# 9. batch_track 漏 --submit（2026-09-08 P0：节点"启动成功"但一条回测都没发）
# ---------------------------------------------------------------------------
#
# 实测 CHN/chn_w1_other_ppa：节点拼的命令没有 `--submit`，pipeline.py 走
# `if not a.submit` 分支打一行 `[plan] gate 过 8 式；加 --submit 提交` 就
# rc=0 退出。stderr 干净、进程正常退出、任务被判 succeeded，而
# backtest_results 0 行、ckpt batches 为空。另因子进程没用 `-u`，stdout 被
# 块缓冲，观察时两个日志都是 0 字节 —— 外部完全看不出发生过什么。


def _batch_track_dry_run_command(**overrides):
    from wqb.workflow import execute

    params = {"region": "KOR", "wave": "_t", "dataset": "_t"}
    params.update(overrides)
    result = execute("batch_track", params, dry_run=True)
    return (result.output or {}).get("command", "")


def test_batch_track_command_has_submit_flag():
    """缺 --submit 时 pipeline 只出计划就退出，回测一条不发。"""
    command = _batch_track_dry_run_command()
    if not command:
        pytest.skip("toolkit 未安装，无命令可查")
    assert "--submit" in command, (
        "batch_track 必须传 --submit —— 这是提交**回测**(simulation)，"
        "不是提交 alpha（提交 alpha 走 submit_alpha 且需用户确认）"
    )


def test_batch_track_command_is_unbuffered():
    """detached 的 stdout 重定向到文件；不加 -u 就是块缓冲，退出即丢日志。"""
    command = _batch_track_dry_run_command()
    if not command:
        pytest.skip("toolkit 未安装，无命令可查")
    assert " -u " in f" {command} ", f"解释器缺 -u：{command}"


def test_batch_track_submit_false_omits_flag():
    """submit=False 是"只出计划"的合法用法，必须能显式关掉。"""
    command = _batch_track_dry_run_command(submit=False)
    if not command:
        pytest.skip("toolkit 未安装，无命令可查")
    assert "--submit" not in command


def test_validate_argv_still_enforces_behind_interpreter_flags(tmp_path):
    """加 -u 之后 argv 校验不能被静默关掉。

    旧实现把 cmd[1] 当脚本；命令变成 `python -u script.py …` 后它会去读
    "-u"，读不到就 fail-open —— 等于 2026-09-06 补的那道闸自己哑了。
    """
    from wqb.workflow._common import validate_argv

    script = tmp_path / "fake.py"
    script.write_text(
        "import argparse\n"
        "ap = argparse.ArgumentParser()\n"
        "ap.add_argument('--dataset')\n",
        encoding="utf-8",
    )
    ok, _ = validate_argv(["python", "-u", str(script), "--dataset", "d"])
    assert ok, "合法命令不应被 -u 影响"

    ok, err = validate_argv(["python", "-u", str(script), "--concurrency", "7"])
    assert not ok and "--concurrency" in err, "-u 之后校验必须照样生效"


def test_no_submit_error_catches_plan_only_stdout():
    """铁证级判据：pipeline 自己打印的计划行。"""
    from wqb.workflow._common import batch_track_no_submit_error

    err = batch_track_no_submit_error(
        "[gate] total=8 passed=8\n[plan] gate 过 8 式；加 --submit 提交（七槽填槽 + 配额闸）\n",
        0, 0,
    )
    assert err and "--submit" in err


def test_no_submit_error_catches_empty_stdout():
    """块缓冲丢日志的那种"什么都没发生"。"""
    from wqb.workflow._common import batch_track_no_submit_error

    assert batch_track_no_submit_error("", 0, 0)
    assert batch_track_no_submit_error("   \n", None, None)


def test_no_submit_error_catches_zero_rows_wave():
    from wqb.workflow._common import batch_track_no_submit_error

    err = batch_track_no_submit_error("[slot] 七槽填槽\n[done] checkpoint: x\n", 0, 0)
    assert err and "0 行" in err


def test_no_submit_error_allows_checkpoint_resume():
    """同波重跑：review 阶段 checkpoint 跳过，零新增但已有回测行 —— 合法。

    断言特意不写成"行数没涨就判失败"，否则每次续跑都会被误判成失败。
    """
    from wqb.workflow._common import batch_track_no_submit_error

    stdout = "[review] 已完成（checkpoint），跳过\n[done] checkpoint: x\n"
    assert batch_track_no_submit_error(stdout, 8, 8) is None
    assert batch_track_no_submit_error(stdout, 0, 8) is None      # 本次新增
    assert batch_track_no_submit_error(stdout, None, None) is None  # 读不到库→放行


def _seed_backtest_db(path: Path, rows: int, region: str, wave: str) -> None:
    import sqlite3

    conn = sqlite3.connect(str(path))
    conn.execute(
        "CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, region TEXT, wave TEXT)"
    )
    conn.executemany(
        "INSERT INTO backtest_results (region, wave) VALUES (?, ?)",
        [(region, wave)] * rows,
    )
    conn.commit()
    conn.close()


def _write_batch_track_task(root: Path, task_id: str, meta: dict, stdout: str) -> None:
    d = root / task_id
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    (d / "stdout.log").write_text(stdout, encoding="utf-8")
    (d / "stderr.log").write_text("", encoding="utf-8")


def test_task_status_marks_plan_only_batch_track_failed(tmp_path, monkeypatch):
    """终态断言：rc=0 + stderr 干净 ≠ 成功。此前它就被判成 succeeded。"""
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path / "tasks"))
    db = tmp_path / "wqb.db"
    _seed_backtest_db(db, 0, "CHN", "chn_w1_other_ppa")
    monkeypatch.setenv("WQB_DB_PATH", str(db))

    from wqb.workflow import tasks

    monkeypatch.setattr(tasks, "_pid_alive", lambda pid: False)
    _write_batch_track_task(
        tmp_path / "tasks", "batch_track_CHN_x",
        {"task_id": "batch_track_CHN_x", "pid": 4242, "region": "CHN",
         "wave": "chn_w1_other_ppa", "submit": True, "backtest_rows_before": 0},
        "[gate] total=8 passed=8\n[plan] gate 过 8 式；加 --submit 提交\n",
    )

    task = tasks.get_task("batch_track_CHN_x")
    assert task["status"] == "failed", task
    assert "--submit" in (task["error"] or "")


def test_task_status_keeps_real_run_succeeded(tmp_path, monkeypatch):
    """真跑过（有回测行 + 正常尾声）不能被断言误伤。"""
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path / "tasks"))
    db = tmp_path / "wqb.db"
    _seed_backtest_db(db, 8, "CHN", "chn_w1_other_ppa")
    monkeypatch.setenv("WQB_DB_PATH", str(db))

    from wqb.workflow import tasks

    monkeypatch.setattr(tasks, "_pid_alive", lambda pid: False)
    _write_batch_track_task(
        tmp_path / "tasks", "batch_track_CHN_ok",
        {"task_id": "batch_track_CHN_ok", "pid": 4242, "region": "CHN",
         "wave": "chn_w1_other_ppa", "submit": True, "backtest_rows_before": 0},
        "[slot] 七槽填槽：总 1 批\n[db] backtest_results +8/8\n[done] checkpoint: x\n",
    )

    assert tasks.get_task("batch_track_CHN_ok")["status"] == "succeeded"


def test_task_status_ignores_tasks_without_submit_marker(tmp_path, monkeypatch):
    """老任务目录（无 submit 键）行为不变，不被新断言追溯判失败。"""
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path / "tasks"))
    from wqb.workflow import tasks

    monkeypatch.setattr(tasks, "_pid_alive", lambda pid: False)
    _write_batch_track_task(
        tmp_path / "tasks", "batch_track_KOR_old",
        {"task_id": "batch_track_KOR_old", "pid": 1, "region": "KOR", "wave": "36A"},
        "",
    )
    assert tasks.get_task("batch_track_KOR_old")["status"] == "succeeded"


# ---------------------------------------------------------------------------
# 10. 四个异步节点的 detached 输出必须无缓冲（2026-09-08，batch_track 修复推广）
# ---------------------------------------------------------------------------
#
# detached 把 stdout 重定向到文件时 Python 默认块缓冲：进程退出时未满的缓冲直接
# 丢，任务日志是 0 字节，外部完全看不出发生过什么（CHN/chn_w1_other_ppa 实测）。
# `-u` 管住直接启动的解释器，PYTHONUNBUFFERED 连它再 spawn 的进程一起管住 ——
# gem 的 run.py 与 campaign 的 pipeline.py 都会再起后台 child，缺一不可。


def _node_dry_run_commands(node, params):
    """干跑取节点构建出的命令（顶层 command 或 steps 里的）。"""
    from wqb.workflow import execute

    result = execute(node, params, dry_run=True)
    out = result.output or {}
    commands = [out["command"]] if out.get("command") else []
    for step in out.get("steps") or []:
        if isinstance(step, dict) and step.get("command"):
            commands.append(step["command"])
    return commands


@pytest.mark.parametrize("node,params", [
    ("batch_track", {"region": "KOR", "wave": "_t", "dataset": "_t"}),
    ("campaign", {"region": "KOR", "stage": "S0"}),
    ("feature_engineering", {"region": "KOR", "dataset_id": "fundamental78",
                             "delay": 1, "universe": "TOP3000"}),
    ("gem", {"region": "KOR", "dataset_id": "fundamental78", "delay": 1,
             "universe": "TOP3000", "data_category": "fundamental"}),
])
def test_async_node_commands_are_unbuffered(node, params):
    commands = _node_dry_run_commands(node, params)
    if not commands:
        pytest.skip(f"{node}: skill/toolkit 未安装或战役目录缺失，无命令可查")
    for command in commands:
        assert " -u " in f" {command} ", f"{node} 解释器缺 -u：{command}"


def test_unbuffered_env_sets_pythonunbuffered():
    from wqb.workflow._common import unbuffered_env

    env = unbuffered_env()
    assert env["PYTHONUNBUFFERED"] == "1"
    # extra 覆盖不能把 PYTHONUNBUFFERED 顶掉（campaign 传 PYTHONIOENCODING）
    env2 = unbuffered_env({"PYTHONIOENCODING": "utf-8"})
    assert env2["PYTHONUNBUFFERED"] == "1"
    assert env2["PYTHONIOENCODING"] == "utf-8"


def test_unbuffered_env_does_not_mutate_parent_environ(monkeypatch):
    """凭证桥只能活在子进程环境里，绝不能污染 MCP 进程自身。"""
    import os

    from wqb.workflow._common import unbuffered_env

    monkeypatch.delenv("WQ_USERNAME", raising=False)
    monkeypatch.delenv("PYTHONUNBUFFERED", raising=False)
    unbuffered_env()
    assert "PYTHONUNBUFFERED" not in os.environ
    assert "WQ_USERNAME" not in os.environ


def test_credential_bridge_renames_without_overriding(monkeypatch):
    """CREDENTIALS_* → WQ_*；已显式设过的 WQ_* 不被覆盖。"""
    from wqb.workflow._common import with_brain_credentials

    env = {"CREDENTIALS_EMAIL": "a@b.c", "CREDENTIALS_PASSWORD": "pw"}
    assert with_brain_credentials(env)["WQ_USERNAME"] == "a@b.c"
    assert env["WQ_PASSWORD"] == "pw"

    explicit = {"WQ_USERNAME": "keep", "WQ_PASSWORD": "keep-pw",
                "CREDENTIALS_EMAIL": "other@b.c", "CREDENTIALS_PASSWORD": "other"}
    out = with_brain_credentials(explicit)
    assert out["WQ_USERNAME"] == "keep" and out["WQ_PASSWORD"] == "keep-pw"
