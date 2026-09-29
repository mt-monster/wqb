# -*- coding: utf-8 -*-
"""tools/skill_lint.py 的自测 + 「内容为真」棘轮（skills 审查 X-17 #1/#2/#5/#14，2026-09-29）。

两层：
  1. 自测：argparse AST 提取（子命令 / 必填 / helper / 多 parser）、campaign.py 分发、占位符与反例豁免、
     MCP 参数校验、表达式过闸——保证检查器本身不误报/漏报；
  2. 棘轮：仓库现存违规登记在 tests/fixtures/skill_lint_baseline.json。**新增违规必红**；已修复者必须从基线删除
     （否则红），这样基线只会缩小，进度可见。有意接受时用 `python tools/skill_lint.py --update-baseline`
     重写并人审 diff。
"""
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import skill_lint as L  # noqa: E402


def _script(tmp_path, name, body):
    p = tmp_path / name
    p.write_text(textwrap.dedent(body), encoding="utf-8")
    L.parse_argparse.cache_clear()
    return p


# ── argparse AST ──────────────────────────────────────────────────────────────
def test_argparse_extraction_subcommands_required_and_flags(tmp_path):
    p = _script(tmp_path, "tool.py", """
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("--region", required=True)
        sub = ap.add_subparsers(dest="cmd")
        up = sub.add_parser("upsert")
        up.add_argument("--wave", required=True)
        up.add_argument("--dry-run", action="store_true")
        sub.add_parser("get").add_argument("--wave")
    """)
    spec = L.parse_argparse(str(p))
    assert set(spec.subs) == {"upsert", "get"} and not spec.dynamic and not spec.multi
    assert spec.top["--region"]["required"] is True
    assert spec.subs["upsert"]["--wave"]["required"] and not spec.subs["upsert"]["--dry-run"]["takes_value"]


def test_unknown_helper_marks_parser_dynamic_and_multi_parser_is_flagged(tmp_path):
    p = _script(tmp_path, "h.py", """
        import argparse
        def add_common(p): p.add_argument("--x")
        ap = argparse.ArgumentParser()
        add_common(ap)
    """)
    assert L.parse_argparse(str(p)).dynamic is True
    q = _script(tmp_path, "m.py", """
        import argparse
        pre = argparse.ArgumentParser(add_help=False); pre.add_argument("--status")
        ap = argparse.ArgumentParser(); ap.add_argument("--must", required=True)
    """)
    assert L.parse_argparse(str(q)).multi is True


def test_known_helper_add_campaign_arg_is_understood(tmp_path):
    p = _script(tmp_path, "c.py", """
        import argparse
        ap = argparse.ArgumentParser()
        add_campaign_arg(ap)
        ap.add_argument("--dataset", required=True)
    """)
    spec = L.parse_argparse(str(p))
    assert "--campaign-dir" in spec.top and not spec.dynamic


# ── 命令抽取 / 分词 ───────────────────────────────────────────────────────────
def test_tokenizer_keeps_placeholders_but_stops_at_redirects():
    assert L.tokenize("x.py --dir <DIR> --n 3 > out.txt") == ["x.py", "--dir", "<DIR>", "--n", "3"]
    assert L.tokenize("x.py --a 1 [--opt] | tee log") == ["x.py", "--a", "1"]
    assert L.tokenize("x.py --a 1 # 注释") == ["x.py", "--a", "1"]


def test_campaign_dispatch_covers_the_real_table():
    table = L.campaign_dispatch()
    assert table["wave"].name == "wave_results.py" and table["gate"].name == "gate.py"
    assert L._split_campaign(["--campaign-dir", "X", "wave", "upsert", "--wave", "1"]) == ("wave", ["upsert", "--wave", "1"], True)


def _lint_doc(tmp_path, monkeypatch, md, fn):
    doc = tmp_path / "Claude" / "skills" / "demo" / "SKILL.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(md, encoding="utf-8")
    monkeypatch.setattr(L, "iter_docs", lambda: [doc])
    monkeypatch.setattr(L, "rel", lambda p: "demo/SKILL.md")
    return fn()


def test_command_checks_catch_the_bm14_class_and_respect_counterexample_markers(tmp_path, monkeypatch):
    md = textwrap.dedent("""
        ```bash
        python $TK/campaign.py --campaign-dir $CD wave upsert --wave 3 --verdict PARTIAL --extra @notes.json
        python $TK/campaign.py --campaign-dir $CD ledger keys
        python $TK/campaign.py --campaign-dir $CD nosuch
        ```

        反例（不要这样写）：

        ```bash
        python $TK/campaign.py --campaign-dir $CD wave upsert --extra @x.json
        ```
    """)
    vs = _lint_doc(tmp_path, monkeypatch, md, L.check_commands)
    kinds = sorted((v["check"], v["msg"].split(":")[0]) for v in vs)
    assert ("cmd-flag", "wave_results.py upsert") in kinds          # --extra 不存在
    assert any(v["check"] == "cmd-subcommand" and "keys" in v["msg"] for v in vs)
    assert any(v["check"] == "cmd-subcommand" and "nosuch" in v["msg"] for v in vs)
    assert len(vs) == 3                                             # 反例块被豁免


def test_valid_commands_pass(tmp_path, monkeypatch):
    md = "```bash\npython tools/mcp_ping.py --service wqb-db --timeout 30\n```\n"
    assert _lint_doc(tmp_path, monkeypatch, md, L.check_commands) == []


# ── MCP ───────────────────────────────────────────────────────────────────────
def test_mcp_registry_reads_real_signatures():
    reg = L.mcp_registry()
    assert "confirm_submit" in reg["wq-brain-http"]["workflow_submit_alpha"]
    assert "region" in reg["wqb-db"]["get_region_config"]
    assert "dataset" not in reg["wq-brain-http"]["workflow_submit_alpha"]


def test_mcp_check_flags_unknown_tool_and_param(tmp_path, monkeypatch):
    md = textwrap.dedent("""
        调用 mcp__wq-brain-http__workflow_submit_alpha(alpha_id="X", dataset="d", confirm_submit=False)。
        再调 mcp__wq-brain-http__submit_alpha(alpha_id="X")。
        合规：mcp__wq-brain-http__workflow_submit_alpha(alpha_id="X", confirm_submit=False)。
    """)
    vs = _lint_doc(tmp_path, monkeypatch, md, L.check_mcp)
    assert [(v["check"]) for v in vs] == ["mcp-param", "mcp-tool"]


# ── 表达式 / 凭据 / 裸 python ──────────────────────────────────────────────────
def test_expression_check_reports_policy_violations_only(tmp_path, monkeypatch):
    md = textwrap.dedent("""
        推荐写法：`add(rank(ts_mean(aaa1, 22)), rank(ts_mean(bbb1, 22)))`

        伪代码模板（不报）：`winsorize(x, std=N)` 与 `ts_rank(ts_zscore(...))`。

        <!-- lint:counterexample -->
        `add(rank(ts_mean(aaa1, 5)), rank(ts_mean(ccc1, 5)))`
    """)
    vs = _lint_doc(tmp_path, monkeypatch, md, L.check_exprs)
    assert len(vs) == 1 and "equal_weight_leg_add" in vs[0]["msg"]


def test_secret_check_flags_instructions_not_prohibitions(tmp_path, monkeypatch):
    md = textwrap.dedent("""
        凭据：load_dotenv("world-quant-brain-mcp/.env") 读取。
        **禁止**读取 world-quant-brain-mcp/.env。

        运行：python run.py --password hunter2

        反例：
        python run.py --password hunter2
    """)
    vs = _lint_doc(tmp_path, monkeypatch, md, L.check_secrets)
    assert sorted(v["check"] for v in vs) == ["cli-password", "env-read"]


def test_bare_python_exempts_scripts_that_reexec_into_the_venv(tmp_path, monkeypatch):
    md = "```bash\npython tools/mcp_ping.py\npython Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py --expr x\n```\n"
    vs = _lint_doc(tmp_path, monkeypatch, md, L.check_bare_python)
    # mcp_ping 不含 import _pyenv 之外的 re-exec？—— 以脚本源码为准：含 import _pyenv 即豁免
    assert all("gate.py" in v["snippet"] for v in vs)


# ── 棘轮 ──────────────────────────────────────────────────────────────────────
def test_no_new_skill_lint_violations_and_baseline_never_goes_stale():
    vs = L.run()
    new, fixed = L.diff_against_baseline(vs)
    assert not new, ("新增了 skill 文档违规（命令不可执行 / MCP 参数不在签名 / 表达式违反闸 / 凭据指示 / 裸 python）：\n  "
                     + "\n  ".join(new[:15]) + "\n修文档；确属有意的反例用 `<!-- lint:counterexample -->` 标记。")
    assert not fixed, ("这些违规已修复，请从 tests/fixtures/skill_lint_baseline.json 删除（或重跑 "
                       "`python tools/skill_lint.py --update-baseline`）：\n  " + "\n  ".join(fixed[:15]))
