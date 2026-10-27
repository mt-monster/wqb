# -*- coding: utf-8 -*-
"""`build_wave --max-size-auto` 的 s0-select 调用必须给 `--json` 一个路径（2026-10-24）。

事故形态：命令写成 `[..., "s0-select", "--region", R, "--json"]`，而 campaign_intel 的
`--json` 是带值参数 ⇒ 子进程 argparse exit 2；下游是 `if returncode == 0:` 静默跳过，
于是 `--max-size-auto` **从未生效**过、也没人报错。

本用例只做静态契约（AST）：抓到「`--json` 后没有值」这一种形态即可，运行端到端会真打平台。
另核 `campaign_intel` 的 `--json` 产物带顶层 `est_seats`（消费方读的就是它）。
"""
import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BUILD_WAVE = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts" / "build_wave.py"
CAMPAIGN_INTEL = REPO / "tools" / "campaign_intel.py"


def _s0_select_commands(tree):
    """找出所有含 "campaign_intel.py" 字面量的 list 实参（subprocess 的命令）。"""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "run"):
            continue
        if not node.args:
            continue
        argv = node.args[0]
        if not isinstance(argv, ast.List):
            continue
        # campaign_intel.py 常包在 os.path.join(...) 里，按子树找常量
        if not any(isinstance(n, ast.Constant) and n.value == "campaign_intel.py"
                   for e in argv.elts for n in ast.walk(e)):
            continue
        out.append(argv)
    return out


def test_max_size_auto_json_flag_is_given_a_value():
    tree = ast.parse(BUILD_WAVE.read_text(encoding="utf-8"))
    cmds = _s0_select_commands(tree)
    assert cmds, "build_wave 里找不到 campaign_intel s0-select 的派发命令（测试需同步）"
    for argv in cmds:
        pos = next((i for i, e in enumerate(argv.elts)
                    if isinstance(e, ast.Constant) and e.value == "--json"), None)
        if pos is None:
            continue
        assert pos + 1 < len(argv.elts), (
            "`--json` 必须带一个路径实参：裸 `--json` 会被 argparse 判 exit 2，"
            "而调用方 `if returncode == 0` 会静默吞掉（--max-size-auto 永不生效）")
        nxt = argv.elts[pos + 1]
        assert not (isinstance(nxt, ast.Constant) and str(nxt.value).startswith("--")), (
            "`--json` 后面紧跟了另一个开关，等于没给值")


def test_campaign_intel_json_payload_has_top_level_est_seats():
    """消费方读 `_sel.get("est_seats")`，产物必须真的写顶层 est_seats。"""
    src = CAMPAIGN_INTEL.read_text(encoding="utf-8")
    assert '"est_seats": [' in src, (
        "campaign_intel s0-select --json 产物需带顶层 est_seats 列表"
        "（build_wave --max-size-auto 的唯一输入）")
