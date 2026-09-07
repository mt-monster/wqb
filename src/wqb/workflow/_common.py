# -*- coding: utf-8 -*-
"""workflow 共享工具：路径解析、数据集类别推断、Python 解释器定位。

单一事实源，替代各节点里重复的 skill 目录探测、硬编码绝对路径、
以及 gem/feature_engineering 各自复制的 `_infer_category`。

约定（与 tools/wave_gate.py 的 WQ_TOOLKIT_DIR/WQ_VALIDATOR_DIR 模式对齐）：
  - env 优先（WQ_SKILLS_DIR / WQ_TOOLKIT_DIR），其余基于 os.path.expanduser("~")
  - 候选顺序见 _skill_roots()：Claude 安装位 > 历史 Agent 安装位（qoder-cn /
    cursor / workbuddy）> 仓库自带 Claude/skills（兜底，保证 clone 即可用）
"""
from __future__ import annotations

import logging
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

# src/wqb/workflow/_common.py -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]

def _skill_roots() -> tuple:
    """技能根目录候选表（按优先级）。

    2026-09-05 修复：此前只认 ~/.qoder-cn / ~/.cursor / ~/.workbuddy 三处，
    而仓库自带 Claude/skills/ 且 install_claude_skills.ps1 / install_now.py
    装到 %APPDATA%\\Claude\\skills 或 ~/.claude/skills —— 三组位置互不相交，
    导致 campaign / gem 节点在 Claude 侧安装时一律 "not found"。

    优先级：WQ_SKILLS_DIR 环境变量 > Claude 安装位 > 历史 Agent 安装位 >
    仓库自带 Claude/skills（最后兜底，保证 clone 即可用）。
    """
    roots = []

    env = os.environ.get("WQ_SKILLS_DIR")
    if env:
        roots.extend(part for part in env.split(os.pathsep) if part)

    # Claude 安装位（install_claude_skills.ps1 / install_now.py 的目标集合）
    for var, *parts in (
        ("APPDATA", "Claude", "skills"),
        ("APPDATA", "Anthropic", "Claude", "skills"),
        ("LOCALAPPDATA", "Claude", "skills"),
        ("LOCALAPPDATA", "Anthropic", "Claude", "skills"),
    ):
        base = os.environ.get(var)
        if base:
            roots.append(os.path.join(base, *parts))
    roots.append(os.path.expanduser("~/.claude/skills"))

    # 历史 Agent 安装位
    roots.append(os.path.expanduser("~/.qoder-cn/skills"))
    roots.append(os.path.expanduser("~/.cursor/skills"))
    roots.append(os.path.expanduser("~/.workbuddy/skills"))

    # 仓库自带副本（最后兜底）
    roots.append(str(REPO_ROOT / "Claude" / "skills"))

    seen = set()
    ordered = []
    for r in roots:
        if r and r not in seen:
            seen.add(r)
            ordered.append(r)
    return tuple(ordered)


#: 兼容旧引用；求值时刻的快照，动态解析一律走 _skill_roots()
_SKILL_ROOTS = _skill_roots()

# 平台 dataset category 前缀兜底表（与 src/wqb/config.py PLATFORM_CATEGORIES 同口径；
# 仅当 data/wqb.db 快照无记录时使用。短 key 放长 key 之后，避免子串误截断）。
_PREFIX_CATEGORY = [
    ("analyst", "analyst"),
    ("model", "model"),
    ("news", "news"),
    ("fundamental", "fundamental"),
    ("pv", "pv"),
    ("option", "option"),
    ("risk", "risk"),
    ("shortinterest", "shortinterest"),
    ("institutions", "institutions"),
    ("imbalance", "imbalance"),
    ("macro", "macro"),
    ("earnings", "earnings"),
    ("equity", "equity"),
    ("sentiment", "sentiment"),
    ("insiders", "insiders"),
    ("insider", "insiders"),
]

#: data/wqb.db（datasets 表为平台 get_datasets 快照，见 tools/ingest_dataset_assets.py）
_DB_PATH = REPO_ROOT / "data" / "wqb.db"


def _platform_category(dataset_id: str) -> Optional[str]:
    """以平台 category 为准：优先查 datasets 快照（category 非空的最新一条）。

    快照缺记录（如 model50 在 IND 仅存 category=NULL 行）时返回 None，
    由调用方回退前缀推断。
    """
    try:
        conn = sqlite3.connect(_DB_PATH)
        try:
            row = conn.execute(
                "SELECT category FROM datasets WHERE name=? "
                "AND category IS NOT NULL AND category != '' "
                "ORDER BY id DESC LIMIT 1",
                (dataset_id,),
            ).fetchone()
            return str(row[0]) if row else None
        finally:
            conn.close()
    except Exception:
        return None


def infer_data_category(dataset_id: str) -> str:
    """推断数据集类别：平台 category 优先（data/wqb.db 快照），无记录时前缀兜底。

    分类口径一律以平台 category 为准（2026-09-01 统一）——如 model50 内容为
    下行风险评估打分（International Scorings Data），但平台分类为 model，
    不按内容语义归入 risk。
    """
    platform = _platform_category(dataset_id)
    if platform:
        return platform
    lower = dataset_id.lower()
    for key, value in _PREFIX_CATEGORY:
        if key in lower:
            return value
    return "other"


#: 历史 Agent 安装位：能用，但都是各自独立的物理拷贝，随时可能落后。
#: `~/.workbuddy/skills` 实测是一份含已废止 brain-enhance-template 的完整旧拷贝
#: （2026-09-06 审计）。落到这些位置说明主安装位没解析到 —— 必须让人看见，
#: 否则就是"跑着两周前的引擎还以为是最新的"。
_LEGACY_ROOTS = (
    os.path.expanduser("~/.qoder-cn/skills"),
    os.path.expanduser("~/.cursor/skills"),
    os.path.expanduser("~/.workbuddy/skills"),
)


def _warn_if_legacy(root: str, what: str) -> None:
    if os.path.normcase(os.path.abspath(root)) in {
        os.path.normcase(os.path.abspath(p)) for p in _LEGACY_ROOTS
    }:
        logging.getLogger(__name__).warning(
            "%s 解析到历史 Agent 安装位 %s —— 该目录是独立物理拷贝，可能已落后于"
            "仓库 Claude/skills。跑 `python tools/sync_skills.py --check` 核对，"
            "或设 WQ_SKILLS_DIR 指定权威位置。",
            what, root,
        )


#: skill 完整性探针：某些 skill 存在多份物理拷贝，旧版缺关键文件却仍能"跑起来"，
#: 只是静默降级（如无 priors 生成）。命中缺失即告警——降级不报错比直接崩溃危险。
_SKILL_INTEGRITY_PROBES = {
    # 2026-09-08：venv 内 cnhkmcp/untracked/skills 下有一份 1443 行的旧 GEM 引擎，
    # 无 economic_priors.py，且 run_pipeline.py 用 strict parse_args() 不认 --priors-file。
    # 若解析命中那份，整条概念优先链路会静默退化成"无经济学先验"生成。
    "brain-makeSomeGem": [
        ("scripts/trailSomeAlphas/economic_priors.py",
         "缺 economic_priors.py —— 这是旧版 GEM 引擎拷贝，概念优先先验(wins/dead_ends/"
         "gate_priors)不会进入 prompt，生成质量会静默劣化"),
        ("scripts/trailSomeAlphas/run_pipeline.py",
         "缺 run_pipeline.py —— GEM 引擎不完整，headless_runner 无法委派"),
    ],
}


def _warn_if_incomplete(skill_dir: str, skill_name: str) -> None:
    probes = _SKILL_INTEGRITY_PROBES.get(skill_name)
    if not probes:
        return
    log = logging.getLogger(__name__)
    for rel, why in probes:
        if not os.path.isfile(os.path.join(skill_dir, *rel.split("/"))):
            log.warning(
                "skill %s 解析到 %s，但 %s —— 跑 `python tools/sync_skills.py` 同步仓库副本，"
                "或设 WQ_SKILLS_DIR 指向完整安装位。",
                skill_name, skill_dir, why,
            )


def resolve_skill_dir(skill_name: str) -> Optional[str]:
    """定位 skill 根目录（如 brain-makeSomeGem）。返回绝对路径或 None。"""
    for root in _skill_roots():
        candidate = os.path.join(root, skill_name)
        if os.path.isdir(candidate):
            _warn_if_legacy(root, f"skill {skill_name}")
            _warn_if_incomplete(candidate, skill_name)
            return candidate
    return None


def resolve_toolkit_dir() -> Optional[str]:
    """定位 wq-brain-campaign-toolkit/scripts（含 WQ_TOOLKIT_DIR 覆盖）。"""
    env = os.environ.get("WQ_TOOLKIT_DIR")
    if env and os.path.isdir(env):
        return env
    for root in _skill_roots():
        candidate = os.path.join(root, "wq-brain-campaign-toolkit", "scripts")
        if os.path.isdir(candidate):
            _warn_if_legacy(root, "campaign toolkit")
            return candidate
    return None


def resolve_tools_dir() -> str:
    """定位仓库 tools/ 目录（基于 REPO_ROOT 推导，不依赖 cwd、不硬编码盘符）。"""
    return str(REPO_ROOT / "tools")


def resolve_campaign_dir(region: str) -> Optional[str]:
    """解析区域战役目录 tracking/<region>。

    优先级：WQB_CAMPAIGN_DIR 环境变量 > WQB_WORKSPACE_ROOT > 仓库 tracking/<region>。
    """
    env = os.environ.get("WQB_CAMPAIGN_DIR")
    if env and os.path.exists(env):
        return os.path.abspath(env)

    workspace_root = os.environ.get("WQB_WORKSPACE_ROOT")
    if workspace_root:
        candidate = os.path.join(workspace_root, "tracking", region)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

    candidate = REPO_ROOT / "tracking" / region
    if candidate.is_dir():
        return str(candidate)
    return None


def wq_py() -> str:
    """返回 MCP venv 的 python 解释器路径。

    优先 WQ_PY 环境变量；回退到 world-quant-brain-mcp/.venv/Scripts/python.exe；
    最后回退 "python"。
    """
    env = os.environ.get("WQ_PY")
    if env and os.path.isfile(env):
        return env
    for rel in (
        os.path.join("world-quant-brain-mcp", ".venv", "Scripts", "python.exe"),
        os.path.join("world-quant-brain-mcp", ".venv", "bin", "python"),
    ):
        candidate = REPO_ROOT / rel
        if candidate.is_file():
            return str(candidate)
    return "python"


# ---------------------------------------------------------------------------
# 平台客户端与台账基元（2026-09-05 从 judge/submit_alpha/superalpha 上提）
# ---------------------------------------------------------------------------

def get_brain_client():
    """延迟导入 brain_client 单例（避免循环依赖与启动开销）。

    三节点（judge / submit_alpha / superalpha）此前逐字重复本函数，
    现统一在此：把 world-quant-brain-mcp/ 临时插入 sys.path 后导入。
    """
    import sys

    mcp_dir = str(REPO_ROOT / "world-quant-brain-mcp")
    if mcp_dir not in sys.path:
        sys.path.insert(0, mcp_dir)
    from brain_api import brain_client  # noqa

    return brain_client


def run_async(coro):
    """在同步节点里执行异步 brain_client 方法。

    无运行中事件循环时新建 loop；已在运行中（如 MCP async 工具上下文）
    则切到独立线程跑，避免 `asyncio.run()` 嵌套报错。

    注意：superalpha 原为简化版（缺"运行中循环"分支），统一到此处后
    在 async 上下文里的行为由"抛错"变为"线程执行"，属修复而非回归。
    """
    import asyncio
    import concurrent.futures

    logger = logging.getLogger(__name__)
    try:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()
        # 已在运行中的事件循环：用独立线程跑
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(lambda: asyncio.run(coro)).result()
    except Exception as e:
        logger.warning(f"async brain call failed: {e}")
        return {"__error__": str(e)}


def persist_workflow_record(
    store,
    prefix: str,
    alpha_id: str,
    payload: Dict[str, Any],
) -> None:
    """把节点结果写入 WORKFLOW 台账（失败只告警，不抛给调用方）。

    judge / submit_alpha 的 `_finalize` 结构相同（if store → try upsert
    → except 告警），仅台账 key 前缀与字段不同；差异由 prefix + payload
    参数化，公共的容错与日志收在此处。
    """
    if not store:
        return
    try:
        store.upsert_ledger("WORKFLOW", f"{prefix}_{alpha_id}", payload)
    except Exception as e:
        logging.getLogger(__name__).warning(
            f"Failed to save {prefix} record for {alpha_id}: {e}"
        )


# ---------------------------------------------------------------------------
# argv 契约校验（2026-09-06 新增）
# ---------------------------------------------------------------------------
#
# 背景（本次审计 P0）：batch_track 往 toolkit pipeline.py 拼了一个该脚本
# 根本不接受的 `--concurrency 7`，argparse 以 exit=2 立即拒绝；而 detached
# 分支只 Popen + 写 meta.json、从不看退出码，于是节点返回 success=True、
# Agent 以为 S3 已启动。真相在 stderr.log 里躺了 13 天才被翻出来
# （src/logs/_async_tasks/batch_track_GLB_1_20260904_125754/stderr.log）。
#
# 根治手段不是"这次把参数删掉"，而是让 dry-run 校验它自己构建出来的命令：
# 静态解析目标脚本的 add_argument / add_parser，比对 argv 里的每个 --flag
# 与子命令。纯文本扫描，不 import、不 subprocess，因此在 dry-run 里零副作用。

#: `add_argument("--foo", "-f", ...)` —— 逐个捕获引号里的选项串
_ADD_ARGUMENT_RE = re.compile(r"add_argument\(\s*([^)]*)", re.S)
_OPTION_STRING_RE = re.compile(r"""(["'])(-{1,2}[A-Za-z0-9][\w-]*)\1""")
#: `sub.add_parser("run")` / `subparsers.add_parser('quota', ...)`
_ADD_PARSER_RE = re.compile(r"""add_parser\(\s*(["'])([A-Za-z0-9][\w-]*)\1""")
#: 本地 import（`from _lib.common import ...` / `import metrics_cache`），
#: 用于把共享的 add_argument 辅助函数也纳入扫描
_LOCAL_IMPORT_RE = re.compile(
    r"^\s*(?:from\s+([A-Za-z_][\w.]*)\s+import|import\s+([A-Za-z_][\w.]*))",
    re.M,
)


def _read_text(path: str) -> Optional[str]:
    """尽力读文件；任何异常都返回 None。

    本模块的静态探测属"能查就查"的加固层，绝不允许自己变成新的故障点 ——
    调用方（节点）在拿到 None 时一律放行。except 写宽而非只捕 OSError：
    单测会 monkeypatch `open`，路径可能被 stub 成非文件对象。
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def _local_module_files(text: str, base_dir: str) -> List[str]:
    """把脚本里的本地 import 解析成同目录下的实际 .py 路径。

    只认能在脚本自身目录里落到实处的模块（`_lib.common` → `_lib/common.py`），
    标准库与第三方包自然解析不到，直接忽略。
    """
    files: List[str] = []
    for m in _LOCAL_IMPORT_RE.finditer(text):
        mod = m.group(1) or m.group(2)
        if not mod or mod.startswith("."):
            continue
        rel = mod.replace(".", os.sep)
        for candidate in (
            os.path.join(base_dir, rel + ".py"),
            os.path.join(base_dir, rel, "__init__.py"),
        ):
            if os.path.isfile(candidate):
                files.append(candidate)
    return files


def script_arg_contract(script_path: str) -> Optional[Tuple[Set[str], Set[str]]]:
    """静态解析脚本的 argparse 契约，返回 (选项串集合, 子命令集合)。

    读不到文件或文件里根本没有 add_argument 时返回 None —— 表示"无法校验"，
    调用方应放行（fail-open），避免把非 argparse 脚本误判成非法。

    2026-09-06：扫描范围含脚本的本地 import。toolkit 把 `--campaign-dir` 这类
    公共参数收在 `_lib/common.py:add_campaign_arg(ap)` 里注册，只扫单文件会把
    合法命令误判为非法（首版实现即在 score_datasets.py 上误报）。宁可漏报不可
    误报——本校验只负责逮"脚本从没声明过"的确定性错误。
    """
    text = _read_text(script_path)
    if text is None:
        return None

    def _options_in(chunk: str) -> Set[str]:
        found: Set[str] = set()
        for m in _ADD_ARGUMENT_RE.finditer(chunk):
            for om in _OPTION_STRING_RE.finditer(m.group(1)):
                found.add(om.group(2))
        return found

    # 脚本自身必须声明过参数才做校验。campaign.py 这类纯派发器（零 add_argument，
    # 只把子命令转交给 assemble_priors.py 等）无从校验，返回 None 放行；
    # 否则它会拿被 import 进来的辅助模块参数当自己的契约，产生误报。
    own = _options_in(text)
    if not own:
        return None

    base_dir = os.path.dirname(os.path.abspath(script_path))
    options = set(own)
    for path in _local_module_files(text, base_dir):
        extra = _read_text(path)
        if extra:
            options |= _options_in(extra)

    # 子命令只认脚本自身声明的，避免被辅助模块里的同名 parser 污染
    subcommands = {m.group(2) for m in _ADD_PARSER_RE.finditer(text)}
    return options, subcommands


def validate_argv(cmd: Sequence[str]) -> Tuple[bool, Optional[str]]:
    """校验已构建的命令行能否被目标脚本的 argparse 接受。

    cmd 形如 [python, script.py, ...args]。返回 (ok, error)；无法静态校验
    时返回 (True, None)。只检查"脚本压根没有声明过的 --flag / 子命令"这类
    确定性错误，不做类型或必填校验（那是脚本自己的事）。
    """
    if len(cmd) < 2:
        return True, None

    contract = script_arg_contract(cmd[1])
    if contract is None:
        return True, None
    options, subcommands = contract

    unknown_flags: List[str] = []
    unknown_subcommands: List[str] = []
    seen_subcommand = not subcommands  # 无子命令的脚本不做子命令校验
    expect_value = False

    for token in cmd[2:]:
        if token.startswith("-") and len(token) > 1:
            expect_value = False
            flag = token.split("=", 1)[0]
            if flag not in options and flag not in unknown_flags:
                unknown_flags.append(flag)
            expect_value = "=" not in token
            continue
        # 位置参数：第一个非选项 token 视为子命令（仅当脚本声明了子命令）
        if expect_value:
            expect_value = False
            continue
        if not seen_subcommand:
            seen_subcommand = True
            if token not in subcommands:
                unknown_subcommands.append(token)

    if unknown_flags or unknown_subcommands:
        parts = []
        if unknown_flags:
            parts.append(f"未声明的参数 {unknown_flags}")
        if unknown_subcommands:
            parts.append(f"未声明的子命令 {unknown_subcommands}")
        return False, (
            f"{os.path.basename(cmd[1])} 的 argparse 不接受该命令："
            + "；".join(parts)
            + f"（脚本已声明 {len(options)} 个选项"
            + (f"、子命令 {sorted(subcommands)}" if subcommands else "")
            + "）"
        )
    return True, None


def detached_launch_failed(
    proc,
    stderr_log: str,
    grace_sec: float = 1.5,
) -> Optional[str]:
    """detached 启动后的存活握手：进程秒退或 stderr 有内容即判失败。

    2026-09-06 新增。detached 的价值是不阻塞 MCP 调用方，代价是退出码没人
    看 —— argparse 拒绝、ImportError、路径不存在这类"启动即死"全被吞成
    success=True。这里只等一个很短的宽限期：跑得起来的任务此刻仍在运行，
    跑不起来的已经把原因写进 stderr 了。

    返回失败原因字符串；一切正常返回 None。无法判定存活（如测试替身没有
    `poll`）时返回 None 放行 —— 本握手是加固层，不该自己成为故障点。
    """
    import time

    poll = getattr(proc, "poll", None)
    if not callable(poll):
        return None

    try:
        deadline = time.time() + grace_sec
        while time.time() < deadline:
            if poll() is not None:
                break
            time.sleep(0.1)
        rc = poll()
    except Exception:
        return None

    tail = ""
    try:
        with open(stderr_log, "r", encoding="utf-8", errors="replace") as f:
            tail = f.read()[-800:].strip()
    except Exception:
        pass

    if rc is not None and rc != 0:
        return f"子进程启动后立即退出 rc={rc}" + (f"；stderr: {tail}" if tail else "")
    if rc == 0 and not tail:
        # 正常任务不会在 1.5s 内干净退出；但也可能是极小批次，放行并交给调用方轮询
        return None
    if tail:
        return f"子进程 stderr 非空（疑似启动失败）：{tail}"
    return None
