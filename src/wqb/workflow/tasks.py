# -*- coding: utf-8 -*-
"""异步任务状态查询：把两套后台任务布局统一成一个可查接口。

背景（2026-09-06 审计）：workflow 的四个重活节点都改成了异步启动，但**没有任何
配套的状态原语** ——

  - `campaign` / `feature_engineering` 写 `<root>/<task_id>.json`（线程收尾，
    完成后整体覆盖写结果），另有 `.out` / `.err` 旁路文件；
  - `gem` / `batch_track` 写 `<root>/<task_id>/meta.json` + `stdout.log` /
    `stderr.log`（detached Popen）。

两套格式互不兼容，且 MCP 侧一个查询工具都没有。后果有两个：
  ① `execute_chain` 无法在异步节点之后 join —— 文档里那条
     `campaign → feature_engineering → gem` 的链一旦实跑，下游节点会读到
     上游还没落库的空结果；
  ② Agent 想知道后台任务死活只能 shell 出去翻文件，与 AGENTS.md §5
     「结构化数据读写优先走 MCP」直接冲突。

本模块提供统一读取（两种布局都认），供 `workflow_task_status` MCP 工具与
`execute_chain` 的 join 使用。只读，不改任何任务文件。
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from ._common import REPO_ROOT

#: 任务根目录。与四个节点一致：WQB_TASK_ROOT 优先（单测隔离），否则仓库 logs/_async_tasks
def task_root() -> str:
    return os.environ.get("WQB_TASK_ROOT") or os.path.join(
        REPO_ROOT, "logs", "_async_tasks"
    )


def _read_json(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _tail(path: str, limit: int = 2000) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()[-limit:]
    except Exception:
        return ""


def _pid_alive(pid: Optional[int]) -> Optional[bool]:
    """进程是否还活着；无法判定返回 None。"""
    if not pid:
        return None
    try:
        if os.name == "nt":
            import subprocess
            # errors="replace"：中文 Windows 的 tasklist 走 GBK，用 utf-8 硬解会
            # 在 subprocess 的读取线程里抛 UnicodeDecodeError（实测），
            # 而那是后台线程的异常，调用方只会看到 pid_alive=None 这种哑失败。
            out = subprocess.run(
                ["tasklist", "/FI", f"PID eq {int(pid)}", "/NH"],
                capture_output=True, text=True, timeout=10,
                encoding="utf-8", errors="replace",
            ).stdout or ""
            return str(pid) in out
        os.kill(int(pid), 0)
        return True
    except ProcessLookupError:
        return False
    except Exception:
        return None


def _from_flat(path: str, task_id: str, tail_lines: int) -> Dict[str, Any]:
    """campaign / feature_engineering 布局：<task_id>.json"""
    data = _read_json(path) or {}
    root = os.path.dirname(path)
    finished = "finished_at" in data or "returncode" in data or "success" in data
    status = "running"
    if data.get("status") == "running":
        status = "running"
    elif finished:
        status = "succeeded" if data.get("success") else "failed"

    out = {
        "task_id": task_id,
        "layout": "flat",
        "status": status,
        "task_file": path,
        "started_at": data.get("started_at"),
        "finished_at": data.get("finished_at"),
        "returncode": data.get("returncode"),
        "error": data.get("error") or data.get("ledger_error"),
    }
    stdout_path = os.path.join(root, f"{task_id}.out")
    stderr_path = os.path.join(root, f"{task_id}.err")
    out["stdout_tail"] = data.get("stdout_tail") or _tail(stdout_path, tail_lines)
    out["stderr_tail"] = data.get("stderr_tail") or _tail(stderr_path, tail_lines)
    # 保留节点自己写的结论字段（ideas_md_path / field_whitelist / summary 等）
    out["payload"] = {
        k: v for k, v in data.items()
        if k not in ("stdout_tail", "stderr_tail")
    }
    return out


def _assert_batch_track_submitted(
    meta: Dict[str, Any], stdout_log: str
) -> Optional[str]:
    """batch_track 终态后置断言：跑完了 ≠ 提交过回测。返回失败原因或 None。

    2026-09-08 新增。实测 CHN/chn_w1_other_ppa：节点漏拼 `--submit`，
    pipeline.py 打一行 `[plan] …加 --submit 提交` 就 rc=0 退出，stderr 干净，
    于是这里把它判成 succeeded —— 而 backtest_results 一行没落、ckpt batches
    为空。退出码与 stderr 在"计划模式"下都是无信息的，唯一能证伪的是
    stdout 的计划行与库里的回测行数。

    只对 batch_track 且 submit=True 的任务生效：meta 里 `submit` 键的存在
    即标记（老任务目录没有它，行为保持不变）。
    """
    if "submit" not in meta:
        return None
    if not meta.get("submit"):
        return None  # 只出计划的合法用法：必然有计划行、必然零新增
    region, wave = meta.get("region"), meta.get("wave")
    if not region or not wave:
        return None

    from ._common import backtest_row_count, batch_track_no_submit_error

    # 独立读一段 stdout：list_tasks 会传 tail_lines=0，不能拿调用方的尾巴当依据
    text = _tail(stdout_log, 4000)
    return batch_track_no_submit_error(
        text, meta.get("backtest_rows_before"), backtest_row_count(region, wave),
    )


def _from_dir(task_dir: str, task_id: str, tail_lines: int) -> Dict[str, Any]:
    """gem / batch_track 布局：<task_id>/meta.json + stdout.log / stderr.log"""
    meta = _read_json(os.path.join(task_dir, "meta.json")) or {}
    stdout_log = meta.get("stdout_log") or os.path.join(task_dir, "stdout.log")
    stderr_log = meta.get("stderr_log") or os.path.join(task_dir, "stderr.log")
    stderr_tail = _tail(stderr_log, tail_lines)

    alive = _pid_alive(meta.get("pid"))
    error = meta.get("failed_at_launch")
    if meta.get("failed_at_launch"):
        status = "failed"
    elif alive is True:
        status = "running"
    elif alive is False:
        # 进程已退出：stderr 有内容视作失败，否则按完成处理
        status = "failed" if stderr_tail.strip() else "succeeded"
    else:
        status = "unknown"

    if status == "succeeded":
        assert_error = _assert_batch_track_submitted(meta, stdout_log)
        if assert_error:
            status = "failed"
            error = assert_error

    return {
        "task_id": task_id,
        "layout": "dir",
        "status": status,
        "task_dir": task_dir,
        "pid": meta.get("pid"),
        "pid_alive": alive,
        "started_at": meta.get("started_at"),
        "error": error,
        "cmd": " ".join(meta.get("cmd", [])) if isinstance(meta.get("cmd"), list) else meta.get("cmd"),
        "stdout_tail": _tail(stdout_log, tail_lines),
        "stderr_tail": stderr_tail,
        "payload": meta,
    }


def get_task(task_id: str, tail_lines: int = 2000) -> Optional[Dict[str, Any]]:
    """按 task_id 查单个任务（两种布局都认）。找不到返回 None。"""
    root = task_root()
    flat = os.path.join(root, f"{task_id}.json")
    if os.path.isfile(flat):
        return _from_flat(flat, task_id, tail_lines)
    task_dir = os.path.join(root, task_id)
    if os.path.isdir(task_dir):
        return _from_dir(task_dir, task_id, tail_lines)
    return None


def list_tasks(
    prefix: Optional[str] = None,
    limit: int = 20,
    tail_lines: int = 0,
) -> List[Dict[str, Any]]:
    """列出最近的任务（按修改时间倒序）。

    Args:
        prefix: 只列 task_id 以此开头的（如 "batch_track" / "campaign_KOR"）
        limit: 最多返回多少条
        tail_lines: 每条附带的日志尾字符数；0 表示不带日志（列表场景默认省流）
    """
    root = task_root()
    if not os.path.isdir(root):
        return []

    entries: List[tuple] = []
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isdir(path):
            task_id = name
        elif name.endswith(".json"):
            task_id = name[:-5]
        else:
            continue
        if prefix and not task_id.startswith(prefix):
            continue
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            mtime = 0
        entries.append((mtime, task_id))

    entries.sort(reverse=True)
    out: List[Dict[str, Any]] = []
    for _mtime, task_id in entries[:limit]:
        task = get_task(task_id, tail_lines=tail_lines)
        if task:
            if not tail_lines:
                task.pop("stdout_tail", None)
                task.pop("stderr_tail", None)
                task.pop("payload", None)
            out.append(task)
    return out


def wait_for_task(
    task_id: str,
    timeout_sec: float = 600.0,
    poll_sec: float = 5.0,
) -> Dict[str, Any]:
    """阻塞等待任务终态（供 execute_chain 在异步节点后 join）。

    返回最后一次读到的任务状态；超时则带 `timed_out: True` 返回，
    调用方自行决定是继续等还是判失败。
    """
    import time

    deadline = time.time() + timeout_sec
    last: Dict[str, Any] = {"task_id": task_id, "status": "missing"}
    while time.time() < deadline:
        task = get_task(task_id)
        if task:
            last = task
            if task.get("status") in ("succeeded", "failed"):
                return task
        time.sleep(poll_sec)
    last["timed_out"] = True
    return last
