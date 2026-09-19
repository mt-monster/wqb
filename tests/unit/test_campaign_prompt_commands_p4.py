# -*- coding: utf-8 -*-
"""回归测试：战役提示词里的 CLI 命令必须真的能被 argparse 接受（2026-09-17）。

## 为什么
`AGENTS.md` 记录过一次事故：`batch_track` 给 `pipeline.py run` 拼了个不存在的
`--concurrency 7`，argparse exit=2，而 detached 分支不看退出码 → S3 每次"启动成功"
却从未真跑过，证据在 stderr 里躺了 13 天。为此建了 `_common.validate_argv()`。

同一类错误在**提示词/文档**里同样致命：v1 版 USA 战役提示词有 **9 处**命令
照抄即失败（已实测复现 2 处）：
  - `score --region USA`            → `error: unrecognized arguments: --region USA`
  - `pipeline --dataset pv63 ...`   → `error: argument cmd: invalid choice: 'pv63'`
  - `assemble-priors --snapshot`    → 实际是 `--snapshot-ledger`
  - `multi_create_simulate`         → 实际是 `create_multi_simulation`
  - `wave upsert ... --extra`       → wave upsert 无 `--extra`
  - `registry add-dead-end --extra` → 缺必填 `--id/--family/--reason/--rule`
  - `ledger set-verdict --wave W`   → 实际签名 `set-verdict [--json JSON] <wave>`

## 两层护栏
1. **`validate_argv`**（仓库既有工具）：逮"脚本压根没声明过的 `--flag` / 子命令"。
   对 `campaign.py` 这类**纯派发器**（自身零 `add_argument`）它按设计放行。
2. **本文件的 `_declared_options()`**：补上第 1 层的盲区 —— 把
   `campaign.py wave|registry|ledger <sub>` 的**子命令级** `add_argument` 抽出来，
   校验提示词里用到的 `--flag` 确实在该子命令声明过（逮住 `--extra` 这类错误）。

覆盖范围：`PROMPTS` 列出的提示词文件。新增战役提示词时加进去即可复用。
"""

import os
import re
import shlex
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.workflow._common import script_arg_contract, validate_argv  # noqa: E402

TOOLKIT = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")

PROMPTS = [
    os.path.join(REPO, "tracking", "USA", "campaign_prompt_usa_regular_20.md"),
]

#: 提示词里的 shell 变量 → 真实值。
#: ⚠ 必须用 **正斜杠**（`as_posix()`）：后文用 `shlex.split(posix=True)` 切词，
#: 反斜杠会被当成转义符吃掉，把 `Claude\skills\...` 变成 `Claudeskills...`。
_VARS = {
    "$WQ_TOOLKIT_DIR": TOOLKIT.replace("\\", "/"),
    "$TK": TOOLKIT.replace("\\", "/"),
    "$CD": "tracking/USA",
    "$DS": "__dataset__",
    "$W": "__wave__",
}

#: 派发式子命令 → 其 argparse 声明所在模块（补 validate_argv 的盲区）
#: ⚠ 只列"自身带子解析器"的：`campaign.py score` / `assemble-priors` 等是**扁平** parser
#: （无 add_parser），由 validate_argv 覆盖，不应放进本表。
_DISPATCH = {
    ("campaign.py", "wave"): os.path.join(TOOLKIT, "_lib", "wave_results.py"),
    ("campaign.py", "registry"): os.path.join(TOOLKIT, "_lib", "registry.py"),
    ("campaign.py", "ledger"): os.path.join(TOOLKIT, "_lib", "ledger.py"),
    ("campaign.py", "pipeline"): os.path.join(TOOLKIT, "pipeline.py"),
}

#: 这些 flag 由 campaign.py 在派发前统一摘除，任何子命令都不会看到
_GLOBAL_FLAGS = {"--campaign-dir"}


# ---------------------------------------------------------------------------
# 抽取与归一
# ---------------------------------------------------------------------------

def _extract_commands(path):
    """抽出 markdown 里以 `python ` 开头的命令（支持行尾 `\\` 续行）。"""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read().splitlines()

    cmds, buf = [], None
    for line in raw:
        if buf is not None:
            buf += " " + line.strip()
            if buf.endswith("\\"):
                buf = buf[:-1].strip()
                continue
            cmds.append(buf)
            buf = None
            continue
        s = line.strip()
        if s.startswith("python ") and s.endswith("\\"):
            buf = s[:-1].strip()
            continue
        if s.startswith("python "):
            cmds.append(s)
    if buf:
        cmds.append(buf)
    return cmds


def _normalize(cmd_line):
    """把提示词命令转成 argv（替换变量、剥行内注释与重定向）。"""
    for k, v in _VARS.items():
        cmd_line = cmd_line.replace(k, v)
    # 剥行内注释：`cmd  # 说明`（保守处理，避免误伤引号内的 #）
    cmd_line = re.sub(r"\s+#\s+", " # ", cmd_line).split(" # ")[0]
    # 剥重定向 / 管道
    cmd_line = re.split(r"\s*(?:2>&1|1>&2|>|<|\|)\s*", cmd_line)[0]
    tokens = shlex.split(cmd_line, posix=True)
    assert tokens and tokens[0] == "python", cmd_line
    return tokens[1:]


def _all_commands():
    out = []
    for p in PROMPTS:
        if not os.path.isfile(p):
            pytest.skip(f"提示词不存在：{p}")
        for c in _extract_commands(p):
            out.append((os.path.basename(p), c))
    return out


def _declared_options(module_path, subcommand):
    """抽 `sub.add_parser("<subcommand>")` 到下一个 add_parser 之间的 `--flag`。

    兼容两种写法：`p = sub.add_parser("set"); p.add_argument("--json")`（同行）
    与后续多行 `p.add_argument("--x")`。
    """
    if not os.path.isfile(module_path):
        return set()
    opts: set = set()
    collecting = False
    for line in open(module_path, encoding="utf-8").read().splitlines():
        if "add_parser(" in line:
            collecting = (f'"{subcommand}"' in line) or (f"'{subcommand}'" in line)
            if collecting:
                opts |= set(re.findall(r'add_argument\(\s*"(--[^"]+)"', line))
            continue
        if collecting:
            opts |= set(re.findall(r'add_argument\(\s*"(--[^"]+)"', line))
    return opts


def _strip_global_flags(args):
    """摘除 `--campaign-dir <值>` / `--campaign-dir=<值>`（campaign.py 在派发前统一取走）。"""
    out, i = [], 0
    while i < len(args):
        a = args[i]
        if a == "--campaign-dir":
            i += 2
            continue
        if a.startswith("--campaign-dir="):
            i += 1
            continue
        out.append(a)
        i += 1
    return out


def _dispatch_target(args):
    """若命令是 `campaign.py <dispatch> <sub> ...`，返回 (模块路径, 子命令名)。

    ⚠ 必须先剥掉全局 `--campaign-dir`，否则 args[1] 会是它而不是派发名。
    """
    args = _strip_global_flags(args)
    if len(args) < 3:
        return None
    script = os.path.basename(args[0])
    if script != "campaign.py":
        return None
    mod = _DISPATCH.get((script, args[1]))
    return (mod, args[2]) if mod else None


# ---------------------------------------------------------------------------
# 护栏 1：脚本存在 + validate_argv
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("prompt,cmd_line", _all_commands())
def test_prompt_command_script_exists(prompt, cmd_line):
    args = _normalize(cmd_line)
    script = args[0]
    if not os.path.isabs(script):
        script = os.path.join(REPO, script)
    assert os.path.isfile(script), f"[{prompt}] 脚本不存在：{script}\n    命令：{cmd_line}"


@pytest.mark.parametrize("prompt,cmd_line", _all_commands())
def test_prompt_command_passes_validate_argv(prompt, cmd_line):
    """未知 --flag / 未知子命令 / 游离位置参数一律拒绝。"""
    args = _normalize(cmd_line)
    script = args[0]
    if not os.path.isabs(script):
        script = os.path.join(REPO, script)
    if not os.path.isfile(script):
        pytest.skip("脚本不存在（由上一条用例报错）")
    ok, err = validate_argv([sys.executable, script] + args[1:])
    assert ok, f"[{prompt}] argparse 会拒绝：{cmd_line}\n    → {err}"


# ---------------------------------------------------------------------------
# 护栏 2：派发式子命令的 flag 必须在对应子命令里声明过
#    （补 validate_argv 对"纯派发器"放行的盲区）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("prompt,cmd_line", _all_commands())
def test_dispatch_subcommand_flags_are_declared(prompt, cmd_line):
    args = _normalize(cmd_line)
    target = _dispatch_target(args)
    if not target:
        pytest.skip("非派发式子命令")
    module, sub = target
    declared = _declared_options(module, sub)
    assert declared, (
        f"抽不到 {os.path.basename(module)} 的 `{sub}` 子命令声明 —— 抽取逻辑需更新"
    )
    # 剥掉全局 flag 后：args[0]=脚本, args[1]=派发名, args[2]=子命令, 其余才是其参数
    local = _strip_global_flags(args)
    used = {t.split("=", 1)[0] for t in local[3:] if t.startswith("--")}
    unknown = sorted(used - declared - _GLOBAL_FLAGS)
    assert not unknown, (
        f"[{prompt}] `campaign.py {local[1]} {sub}` 不接受 {unknown}；"
        f"该子命令已声明：{sorted(declared)}\n    命令：{cmd_line}"
    )


def test_guard_is_not_vacuous():
    """护栏必须真的在跑命令且真的能校验，否则上游改动会让它静默失效。"""
    cmds = _all_commands()
    assert len(cmds) >= 10, f"只抽到 {len(cmds)} 条命令，抽取逻辑可能失效"

    statically_checkable = 0
    dispatch_checkable = 0
    for _p, cmd_line in cmds:
        args = _normalize(cmd_line)
        if _dispatch_target(args):
            dispatch_checkable += 1
        script = args[0]
        if not os.path.isabs(script):
            script = os.path.join(REPO, script)
        if os.path.isfile(script) and script_arg_contract(script) is not None:
            statically_checkable += 1

    assert statically_checkable >= 5, f"仅 {statically_checkable} 条可静态校验"
    assert dispatch_checkable >= 3, f"仅 {dispatch_checkable} 条走派发校验"


# ---------------------------------------------------------------------------
# 反向自检：v1 的错误写法必须被逮住
# ---------------------------------------------------------------------------

def test_validate_argv_rejects_unknown_flag_and_typo():
    """validate_argv 应逮住"脚本没声明的 flag"与"少打了 -ledger"。"""
    cases = [
        (os.path.join(TOOLKIT, "score_datasets.py"),
         ["--campaign-dir", "tracking/USA", "--region", "USA"], "score 没有 --region"),
        (os.path.join(TOOLKIT, "assemble_priors.py"),
         ["--campaign-dir", "tracking/USA", "--snapshot"], "少打了 -ledger"),
    ]
    for script, args, why in cases:
        ok, _ = validate_argv([sys.executable, script] + args)
        assert not ok, f"漏放：{why}"


def test_dispatch_extractor_rejects_v1_forms():
    """派发层提取器应逮住 validate_argv 看不到的两处 v1 错误。"""
    wave_mod = os.path.join(TOOLKIT, "_lib", "wave_results.py")
    ledger_mod = os.path.join(TOOLKIT, "_lib", "ledger.py")

    wave_opts = _declared_options(wave_mod, "upsert")
    assert wave_opts, "抽不到 wave upsert 声明"
    assert "--extra" not in wave_opts, (
        "wave upsert 突然支持 --extra 了？请复核提示词与 skill 文档口径"
    )
    assert "--finding" in wave_opts, "wave upsert 应支持 --finding"

    sv_opts = _declared_options(ledger_mod, "set-verdict")
    assert sv_opts, "抽不到 ledger set-verdict 声明"
    assert "--wave" not in sv_opts and "--verdict" not in sv_opts, (
        "set-verdict 的参数已变，请复核 `set-verdict [--json JSON] <wave>` 口径"
    )
    assert "--json" in sv_opts


def test_registry_required_flags_still_required():
    """registry 写实证的必填参数必须仍在（v1 只给 --extra 会失败）。"""
    reg_mod = os.path.join(TOOLKIT, "_lib", "registry.py")
    src = open(reg_mod, encoding="utf-8").read()
    for sub, need in (("add-dead-end", ["--id", "--family", "--reason", "--rule"]),
                      ("add-win", ["--id", "--what", "--key"])):
        block_ok = False
        # 注意：声明形如 `sub.add_parser("add-dead-end", help=...)` —— 名字后面还有参数，
        # 因此正则不能要求紧跟 `)`
        for m in re.finditer(rf'add_parser\("{sub}"', src):
            seg = src[m.start(): m.start() + 1500]
            nxt = seg.find("add_parser(", 10)
            if nxt > 0:
                seg = seg[:nxt]
            block_ok = all(f'add_argument("{f}", required=True)' in seg for f in need)
            if block_ok:
                break
        assert block_ok, f"{sub} 的必填参数 {need} 未全部声明（提示词依赖它们）"


# ---------------------------------------------------------------------------
# 口径覆盖：提示词必须包含本轮接入的闸与契约
# ---------------------------------------------------------------------------

def test_prompt_declares_the_new_gates_and_contracts():
    text = open(PROMPTS[0], encoding="utf-8").read()
    required = [
        "signal_floor",             # 三道开波闸之一
        "backlog_gate",
        "stop_rules",
        "gate-mode",                # 灰度三档
        "inspect-mode",             # 体检缺包策略
        "unconsumed",               # 新积压口径（含 gem/selected）
        "check_batch_diversity",    # 唯一执行口径
        "create_multi_simulation",  # 正确的 MCP 工具名
        "submit_verdict",           # 提交唯一权威
        "degraded_gates",           # judge 参考层可用性
        "wave_id",                  # 波号契约
        "priors_snapshot_",         # priors 键口径
        "sync_skills",              # skill 同步
        "step_funnel",              # 步级漏斗（S6 复盘入口）
    ]
    missing = [k for k in required if k not in text]
    assert not missing, f"提示词缺以下口径/契约：{missing}"


def test_prompt_does_not_reintroduce_v1_errors():
    """提示词正文不得再出现 v1 的错误写法（对照表内的"错误示例"除外）。"""
    text = open(PROMPTS[0], encoding="utf-8").read()
    # 只看命令行：抽出来的命令里不得有这些模式
    for _p, cmd_line in _all_commands():
        for bad, why in [
            ("pipeline --dataset", "pipeline 缺 run 位置子命令"),
            ("score --region", "score 没有 --region"),
            ("multi_create_simulate", "工具名写反了"),
            ("--snapshot ", "--snapshot 应为 --snapshot-ledger"),
        ]:
            assert bad not in cmd_line, f"提示词命令重现 v1 错误（{why}）：{cmd_line}"
