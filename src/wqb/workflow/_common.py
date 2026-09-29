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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
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
    # Claude Code / Codex 两个主流宿主位（2026-09-10 审计补：codex 曾不在链上，
    # 导致 `tools/sync_skills.py` 永远不会把仓库推到 ~/.codex/skills，长期分叉）
    roots.append(os.path.expanduser("~/.codex/skills"))

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


# ---------------------------------------------------------------------------
# 产物路径收口（2026-09-25 结构优化目标 E）
# ---------------------------------------------------------------------------
# 背景：异步任务根目录 logs/_async_tasks 在 gem/batch_track/campaign/fe 四个节点
# 与 tasks.py、run_logged_subprocess 里各自重复同一表达式（WQB_TASK_ROOT or 默认位），
# 且 run_logged_subprocess 此前不支持 env 覆盖（不一致）。GEM 数据产物（final_expressions/
# 数据集 csv/whitelist）深嵌套在 skill 安装位内部（trailSomeAlphas/skills/.../data/），
# 随 _skill_roots() 解析结果漂移。统一收口到此处，写入点与读取点共用同一解析。


def resolve_async_tasks_root() -> str:
    """异步任务根目录：WQB_TASK_ROOT 优先（单测隔离），否则仓库 logs/_async_tasks。

    供 detached 节点（gem/batch_track/campaign/fe）、tasks.py 读取侧、
    run_logged_subprocess 同步运行器、以及 tools/cleanup_async_tasks.py 共用。
    """
    return os.environ.get("WQB_TASK_ROOT") or str(REPO_ROOT / "logs" / "_async_tasks")


def _safe_folder_name(name: str) -> str:
    """与 GEM pipeline_io.safe_dataset_id 同规则：仅保留字母数字与 -_。"""
    return "".join(c for c in str(name) if c.isalnum() or c in ("-", "_"))


def resolve_gem_data_dir(dataset_id: str, region: str, delay: int) -> Path:
    """GEM 数据产物目录（仓库稳定路径，与 skill 安装位解耦）。

    优先级：WQB_GEM_DATA_ROOT env > 仓库 data/gem_runs。返回
    <root>/{dataset_id}_{region}_delay{delay}（folder 名做 safe 清洗）。
    纯解析不 mkdir（写侧自建）。
    """
    root = os.environ.get("WQB_GEM_DATA_ROOT") or str(REPO_ROOT / "data" / "gem_runs")
    folder = f"{_safe_folder_name(dataset_id)}_{region}_delay{delay}"
    return Path(root) / folder


def _platform_category(dataset_id: str) -> Optional[str]:
    """以平台 category 为准：优先查 datasets 快照（category 非空的最新一条）。

    快照缺记录（如 model50 在 IND 仅存 category=NULL 行）时返回 None，
    由调用方回退前缀推断。

    2026-09-27 R19：走 resolve_db_path()（此前用模块常量、不认 WQB_DB_PATH），并以只读
    URI 打开——`sqlite3.connect` 遇到不存在的文件会建空库，任一 GEM 干跑 / 单测都会在
    默认路径留下 0 字节 data/wqb.db。
    """
    db = resolve_db_path()
    if not os.path.isfile(db):
        return None
    try:
        conn = db_connect(db, readonly=True, timeout=5.0)
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
    "brain-make-some-gem": [
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
    """定位 skill 根目录（如 brain-make-some-gem）。返回绝对路径或 None。"""
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


#: add_argument 里的 store_true / store_false / count / help / version 这类不吃值的 action
_NOVALUE_ACTION_RE = re.compile(
    r"""action\s*=\s*(["'])(store_true|store_false|count|help|version)\1"""
)
#: `add_argument("name", ...)` 首个引号串不带 `-` 即位置参数
_POSITIONAL_STRING_RE = re.compile(r"""^\s*(["'])([A-Za-z_][\w-]*)\1""")


def script_positional_contract(script_path: str) -> Optional[Tuple[bool, Set[str]]]:
    """静态解析脚本能否接受"多余的位置参数"，返回 (拒绝任何位置参数?, 不吃值的选项集合)。

    2026-09-12 新增。`validate_argv` 原本只逮未声明的 --flag / 子命令，
    对 `build_wave.py --wave W build-wave --from-db` 这种多出来的位置参数
    （campaign 节点把分发器入口名 `build-wave` 拼给了 build_wave.py 本体）
    静默放行，干跑"通过"、实跑 argparse rc=2。

    判定原则仍是"宁可漏报不可误报"：脚本（含本地 import 的辅助模块）只要声明过
    任何位置参数、子命令或 `nargs`，就返回 (False, ...) 放弃位置参数校验；只有
    完全没有位置参数概念的脚本才返回 (True, ...)。第二项列出不吃值的选项，
    供调用方区分"跟在选项后面的值"与"孤立的位置参数"。读不到/无 add_argument
    返回 None（无法校验）。
    """
    text = _read_text(script_path)
    if text is None:
        return None
    own_chunks = [m.group(1) for m in _ADD_ARGUMENT_RE.finditer(text)]
    if not own_chunks:
        return None
    if _ADD_PARSER_RE.search(text):
        return False, set()
    # 位置参数/nargs 只看脚本自身：辅助模块（如 _lib/ledger.py）自带的 CLI 位置参数
    # 不属于导入方的契约，算进来会让 build_wave.py 这类脚本永远无法校验。
    strict = not any("nargs" in ch or _POSITIONAL_STRING_RE.match(ch) for ch in own_chunks)
    # 不吃值的选项则连同本地 import 的共享辅助函数一起收（与 script_arg_contract 同口径）
    base_dir = os.path.dirname(os.path.abspath(script_path))
    all_chunks = list(own_chunks)
    for path in _local_module_files(text, base_dir):
        extra = _read_text(path)
        if extra:
            all_chunks.extend(m.group(1) for m in _ADD_ARGUMENT_RE.finditer(extra))
    novalue: Set[str] = set()
    for chunk in all_chunks:
        if _NOVALUE_ACTION_RE.search(chunk):
            for om in _OPTION_STRING_RE.finditer(chunk):
                novalue.add(om.group(2))
    return strict, novalue


def _script_index(cmd: Sequence[str]) -> Optional[int]:
    """定位 cmd 里的目标脚本下标，跳过解释器自身的开关。

    2026-09-08：detached 子进程改用 `python -u script.py ...` 之后，
    `cmd[1]` 不再是脚本 —— 旧实现会把 `-u` 当成脚本路径去读，`_read_text`
    读不到就 fail-open，于是 argv 契约校验被静默关掉（正是它当初要根治的
    那类"加固层自己哑掉"的故障）。这里显式跳过前导解释器开关。
    """
    for i in range(1, len(cmd)):
        token = cmd[i]
        if token.startswith("-") and len(token) > 1:
            # `-m mod` / `-X opt` 带值；其余（-u/-B/-E/-s…）是纯开关
            continue
        return i
    return None


def validate_argv(cmd: Sequence[str]) -> Tuple[bool, Optional[str]]:
    """校验已构建的命令行能否被目标脚本的 argparse 接受。

    cmd 形如 [python, script.py, ...args]（解释器与脚本之间允许 `-u` 这类
    开关）。返回 (ok, error)；无法静态校验时返回 (True, None)。只检查"脚本
    压根没有声明过的 --flag / 子命令"这类确定性错误，不做类型或必填校验
    （那是脚本自己的事）。
    """
    if len(cmd) < 2:
        return True, None

    idx = _script_index(cmd)
    if idx is None:
        return True, None

    contract = script_arg_contract(cmd[idx])
    if contract is None:
        return True, None
    options, subcommands = contract
    # 多余位置参数校验（2026-09-12）：仅对"完全没有位置参数概念"的脚本启用
    positional_contract = script_positional_contract(cmd[idx])
    strict_positional, novalue_flags = positional_contract or (False, set())

    unknown_flags: List[str] = []
    unknown_subcommands: List[str] = []
    stray_positionals: List[str] = []
    seen_subcommand = not subcommands  # 无子命令的脚本不做子命令校验
    expect_value = False

    for token in cmd[idx + 1:]:
        if token.startswith("-") and len(token) > 1:
            expect_value = False
            flag = token.split("=", 1)[0]
            if flag not in options and flag not in unknown_flags:
                unknown_flags.append(flag)
            # store_true 这类不吃值的选项后面若跟了非选项 token，那就是孤立的位置参数
            expect_value = "=" not in token and flag not in novalue_flags
            continue
        # 位置参数：第一个非选项 token 视为子命令（仅当脚本声明了子命令）
        if expect_value:
            expect_value = False
            continue
        if not seen_subcommand:
            seen_subcommand = True
            if token not in subcommands:
                unknown_subcommands.append(token)
        elif strict_positional and not subcommands:
            stray_positionals.append(token)

    if unknown_flags or unknown_subcommands or stray_positionals:
        parts = []
        if unknown_flags:
            parts.append(f"未声明的参数 {unknown_flags}")
        if unknown_subcommands:
            parts.append(f"未声明的子命令 {unknown_subcommands}")
        if stray_positionals:
            parts.append(f"脚本不接受位置参数，却收到 {stray_positionals}")
        return False, (
            f"{os.path.basename(cmd[idx])} 的 argparse 不接受该命令："
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
    stdout_log: Optional[str] = None,
    first_output_sec: float = 0.0,
) -> Optional[str]:
    """detached 启动后的存活握手：进程秒退或 stderr 有内容即判失败。

    2026-09-06 新增。detached 的价值是不阻塞 MCP 调用方，代价是退出码没人
    看 —— argparse 拒绝、ImportError、路径不存在这类"启动即死"全被吞成
    success=True。这里只等一个很短的宽限期：跑得起来的任务此刻仍在运行，
    跑不起来的已经把原因写进 stderr 了。

    2026-09-21 新增「首字节心跳」（stdout_log + first_output_sec>0 时生效）：
    子进程存活但在 first_output_sec 内 stdout/stderr 仍是 0 字节 → 判「启动挂死」，
    杀掉整棵进程树并返回原因。实证：batch_track 以 DETACHED_PROCESS 启动的
    pipeline 在 venv 启动器下解释器只加载了 python313.dll 就永久阻塞（3 小时
    0 字节输出、CPU 15ms），旧握手（只看秒退/stderr）把它当成"启动成功"。
    `-u` + PYTHONUNBUFFERED 保证正常任务几秒内必有首行输出，静默即异常。

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

    if rc is None and stdout_log and first_output_sec > 0:
        try:
            hb_deadline = time.time() + first_output_sec
            got_output = False
            while time.time() < hb_deadline:
                try:
                    if os.path.getsize(stdout_log) > 0:
                        got_output = True
                        break
                except OSError:
                    pass
                if poll() is not None:
                    break
                time.sleep(0.25)
            if poll() is None and not got_output:
                try:
                    if os.path.getsize(stderr_log) > 0:
                        got_output = True
                except OSError:
                    pass
            if poll() is None and not got_output:
                _kill_process_tree(proc)
                return (f"子进程存活但 {first_output_sec:.0f}s 内 stdout/stderr 均为 0 字节"
                        f"（启动挂死，已杀进程树 pid={getattr(proc, 'pid', '?')}）")
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


# ---------------------------------------------------------------------------
# detached 子进程可观测性与"真跑过没有"断言（2026-09-08 新增）
# ---------------------------------------------------------------------------
#
# 背景（CHN/chn_w1_other_ppa 实测）：batch_track 拼命令时漏了 `--submit`，
# toolkit pipeline.py 只打一行 `[plan] gate 过 8 式；加 --submit 提交` 就
# rc=0 正常退出。三层保护同时失效：
#   ① argv 契约校验只逮"多了不认识的参数"，逮不到"少了必需的参数"；
#   ② 存活握手看的是 rc 与 stderr —— 计划模式两者都干净；
#   ③ 子进程没用 `-u`，stdout 被块缓冲，观察时两个日志都是 0 字节。
# 于是节点返回 success=True，而 backtest_results 一行没落。
#
# 根治分两半：启动侧强制无缓冲（下面的 unbuffered_env + 节点里的 `-u`），
# 终态侧补一条后置断言（batch_track_no_submit_error）。


def unbuffered_env(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """给 detached 子进程用的环境：无缓冲输出 + BRAIN 凭证改名桥。

    无缓冲与命令行 `-u` 双保险 —— `-u` 管直接启动的那个解释器，
    PYTHONUNBUFFERED 连它再 spawn 出来的子进程一起管住。日志实时落盘是
    detached 模式唯一的可观测手段；缓冲住就等于没有。

    凭证桥见 with_brain_credentials（只改名，不落盘、不打印）。

    2026-09-27 R19：缺省注入 WQB_WORKSPACE=REPO_ROOT（不覆盖已有值）——toolkit 若是
    安装位拷贝（~/.claude/skills/...），它从自身位置上溯找不到工作区；有了它，子进程
    与本节点读写的是同一个库（toolkit `_lib/wqb_store.resolve_db_path`）。
    """
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env.setdefault("WQB_WORKSPACE", str(REPO_ROOT))
    with_brain_credentials(env)
    if extra:
        env.update(extra)
    return env


#: MCP 侧凭证的环境变量名（brain_config._load_dotenv_into_environ 从
#: world-quant-brain-mcp/.env 装入）→ toolkit 侧 load_credentials() 认的名字。
_CREDENTIAL_BRIDGE = (("CREDENTIALS_EMAIL", "WQ_USERNAME"),
                      ("CREDENTIALS_PASSWORD", "WQ_PASSWORD"))


def _mcp_dotenv_values(keys: Sequence[str]) -> Dict[str, str]:
    """从 world-quant-brain-mcp/.env 取指定键（只读，不落盘、不记日志）。"""
    path = REPO_ROOT / "world-quant-brain-mcp" / ".env"
    found: Dict[str, str] = {}
    text = _read_text(str(path))
    if not text:
        return found
    wanted = set(keys)
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k in wanted:
            found[k] = v.strip().strip('"').strip("'")
    return found


def with_brain_credentials(env: Dict[str, str]) -> Dict[str, str]:
    """把 BRAIN 凭证按 toolkit 认的名字补进子进程环境（原地修改并返回）。

    2026-09-08：补上 `--submit` 后，pipeline.py 第一次真的走到
    `stage_submit_poll` → `load_credentials()`，当场 FileNotFoundError
    (`~/.brain_mcp_config.json`) —— 因为两边各叫各的名字：

      - MCP 侧：`world-quant-brain-mcp/.env` 的 CREDENTIALS_EMAIL / _PASSWORD
        （brain_config.load_config 装入 os.environ）；
      - toolkit 侧：`WQ_USERNAME` / `WQ_PASSWORD` → `BRAIN_CREDENTIALS` →
        `~/.brain_credentials` → `MCP_CONFIG_FILE`（_lib/common.py:load_credentials）。

    这里只做改名（外加 .env 兜底读取）：不写文件、不打印、不入库，凭证只活在
    子进程的环境里。已显式设过 WQ_USERNAME/WQ_PASSWORD 的一律不覆盖。
    """
    if env.get("WQ_USERNAME") and env.get("WQ_PASSWORD"):
        return env

    missing = [src for src, _ in _CREDENTIAL_BRIDGE if not env.get(src)]
    if missing:
        env_file = _mcp_dotenv_values(missing)
        for key, value in env_file.items():
            if value:
                env.setdefault(key, value)

    for src, dst in _CREDENTIAL_BRIDGE:
        value = env.get(src)
        if value and not env.get(dst):
            env[dst] = value
    return env


def resolve_db_path() -> str:
    """当前生效的战役库路径（WQB_DB_PATH 优先，与 store.default_db_path 同口径）。"""
    return os.environ.get("WQB_DB_PATH") or str(_DB_PATH)


def connect_db_readonly(path: Optional[str] = None, timeout: float = 5.0) -> sqlite3.Connection:
    """只读打开战役库（`mode=ro` URI）。

    库文件不存在时抛 `sqlite3.OperationalError`，而不是像 `sqlite3.connect` 那样悄悄建一个
    空库——开波闸等纯读路径（含 dry-run，契约"不写库"）用它（2026-09-27 R5）。
    """
    db = path or resolve_db_path()
    return db_connect(db, readonly=True, timeout=timeout)


def local_ts(value: Any) -> str:
    """库内时间戳统一成本地时间 `YYYY-MM-DD HH:MM:SS`，便于跨写入方比较先后。

    写入方两种口径并存：Python `datetime.now().isoformat()`（本地时间、`T` 分隔：CampaignStore /
    wqb-db MCP / _lib/region_kb）与 SQLite `datetime('now')` / `CURRENT_TIMESTAMP`（UTC、空格分隔：
    toolkit _lib/ledger、_lib/registry、_lib/wave_results）。空格分隔的按 UTC 换算成本地时间——
    否则东八区上刚写的行看起来早 8 小时。无法解析的截断原样返回，空值返回 ""。
    2026-09-27：由 gem 节点的快照新鲜度检查（N17）提升为公共函数，停止规则 B 的窗口（R22）复用。
    """
    s = str(value or "").strip()
    if not s or "T" in s:
        return s.replace("T", " ")[:19]
    try:
        utc = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return s[:19]
    return utc.astimezone().strftime("%Y-%m-%d %H:%M:%S")


def backtest_row_count(region: str, wave: str) -> Optional[int]:
    """某 region/wave 当前的 backtest_results 行数；无法判定时返回 None。

    只读：库文件不存在、表缺失、并发锁住等一律返回 None，由调用方按
    "无法判定"放行 —— 断言层不该自己变成新的故障点。
    """
    path = resolve_db_path()
    if not os.path.isfile(path):
        return None
    try:
        conn = db_connect(path, timeout=5)
        try:
            row = conn.execute(
                "SELECT COUNT(*) FROM backtest_results WHERE region=? AND wave=?",
                (region, str(wave)),
            ).fetchone()
            return int(row[0]) if row else None
        finally:
            conn.close()
    except Exception:
        return None


#: pipeline.py 在 `not a.submit` 分支打印的计划行（scripts/pipeline.py main 末尾）。
#: 命中即铁证：这次运行只做了计划，一条回测都没提交。
_PLAN_ONLY_MARKER = "加 --submit 提交"


def batch_track_no_submit_error(
    stdout_text: str,
    rows_before: Optional[int],
    rows_after: Optional[int],
) -> Optional[str]:
    """batch_track 终态断言：`任务跑完了` ≠ `提交过回测`。返回失败原因或 None。

    三级判据，按证据强度从强到弱：
      ① stdout 里有 pipeline 的计划行 —— 铁证，它自己说了没提交；
      ② stdout 全空 —— 什么都没发生（或缓冲丢了），无从证明跑过；
      ③ 回测行数没涨 **且** 该 wave 至今 0 行 —— 全链从未落过任何回测。

    ③ 特意不写成"行数没涨就判失败"：pipeline 的 review 阶段带 checkpoint，
    同一波重跑会打印 `[review] 已完成（checkpoint），跳过` 并合法地零新增。
    那种情况下 wave 已有行，说明回测确实跑过，不该误判成失败。
    """
    text = stdout_text or ""
    if _PLAN_ONLY_MARKER in text:
        return (
            "pipeline 未提交任何回测，检查 --submit："
            "stdout 出现计划行（pipeline 只跑了 gate 就退出，未进 submit 阶段）"
        )
    if not text.strip():
        return (
            "pipeline 未提交任何回测，检查 --submit："
            "任务已终止但 stdout 全空 —— 无从证明它跑过 submit 阶段"
            "（子进程未用 -u/PYTHONUNBUFFERED 时缓冲内容会随进程退出丢失）"
        )
    if rows_before is None or rows_after is None:
        return None  # 读不到库，无法判定 —— 放行
    if rows_after > rows_before:
        return None
    if rows_after > 0:
        return None  # 该波已有回测行（checkpoint 重跑合法跳过 review）
    return (
        "pipeline 未提交任何回测，检查 --submit："
        f"backtest_results 该波仍为 0 行（运行前 {rows_before}，运行后 {rows_after}）"
    )


# ---------------------------------------------------------------------------
# 同步子进程的"日志文件 + 进程树超时"运行器（2026-09-20）
# ---------------------------------------------------------------------------
# 事故：workflow_execute(node="wave_gate") 在 MCP 服务内以
# `subprocess.run(capture_output=True, timeout=1800)` 跑 tools/wave_gate.py，
# 结果卡满 1800s 才回 "wave_gate 超时"，而同一命令在终端 <1s 完成，且超时后
# 子进程的全部输出被丢弃、无法定位卡点。根因候选（管道句柄被孙进程继承致
# communicate() 不返回 / 子进程链在服务环境下阻塞）都指向同一类缺陷：
#   ① 用 PIPE 收集输出 —— 任何持有管道句柄的后代进程不退出，父进程就永远收不完；
#   ② 超时只杀直接子进程，不杀进程树，孤儿继续占句柄/占槽；
#   ③ 超时即丢弃已产生的输出，Agent 只能看到一句"超时"。
# 本运行器把三点一起治：输出直写日志文件（无管道）、超时杀整棵进程树、
# 无论成败都返回日志路径与尾部，且 stdin 一律 DEVNULL（服务内无终端，任何
# 意外的交互读都会永久阻塞）。同步节点（wave_gate / auto_review / auto_pyramid
# 之类"跑完就回"的短脚本）统一走它；detached 长任务仍走 tasks.py。


def _kill_process_tree(proc: "subprocess.Popen") -> None:
    """杀掉 proc 及其全部后代（Windows: taskkill /T；POSIX: killpg）。"""
    import subprocess as _sp
    try:
        if os.name == "nt":
            _sp.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                    capture_output=True, timeout=30)
        else:
            import signal
            try:
                pgid = os.getpgid(proc.pid)
                # 子进程与本进程同组（启动方漏了 start_new_session=True）时 killpg 会连调用方一起
                # SIGKILL——2026-09-29 在测试里实测整个 pytest 被杀（exit 137）。此时只杀子进程。
                if pgid == os.getpgrp():
                    proc.kill()
                else:
                    os.killpg(pgid, signal.SIGKILL)
            except Exception:
                proc.kill()
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
    try:
        proc.wait(timeout=15)
    except Exception:
        pass


def run_logged_subprocess(
    cmd: Sequence[str],
    *,
    log_name: str,
    timeout_sec: float,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    tail_chars: int = 4000,
) -> Dict[str, Any]:
    """同步跑一个短命脚本：stdout+stderr 直写 logs/_async_tasks/<log_name>.log。

    Returns:
        {returncode, timed_out, elapsed_sec, log_path, tail}
        timed_out=True 时 returncode=None，且已杀整棵进程树；tail 是超时前
        已落盘的输出尾部（定位卡点用）。
    """
    import subprocess as _sp
    import time as _time

    log_dir = Path(resolve_async_tasks_root())
    log_dir.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(log_name))[:120]
    log_path = log_dir / f"{safe}_{_time.strftime('%Y%m%d_%H%M%S')}.log"

    popen_kwargs: Dict[str, Any] = {
        "cwd": cwd or str(REPO_ROOT),
        "env": env,
        "stdin": _sp.DEVNULL,
        "close_fds": True,
    }
    if os.name == "nt":
        popen_kwargs["creationflags"] = getattr(_sp, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        popen_kwargs["start_new_session"] = True

    t0 = _time.time()
    timed_out = False
    returncode: Optional[int] = None
    with open(log_path, "w", encoding="utf-8", errors="replace") as fh:
        proc = _sp.Popen(list(cmd), stdout=fh, stderr=_sp.STDOUT, **popen_kwargs)
        try:
            returncode = proc.wait(timeout=timeout_sec)
        except _sp.TimeoutExpired:
            timed_out = True
            _kill_process_tree(proc)
    elapsed = round(_time.time() - t0, 2)

    tail = ""
    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - tail_chars * 4))
            tail = fh.read()[-tail_chars:]
    except Exception:
        pass
    return {
        "returncode": returncode,
        "timed_out": timed_out,
        "elapsed_sec": elapsed,
        "log_path": str(log_path),
        "tail": tail,
    }
