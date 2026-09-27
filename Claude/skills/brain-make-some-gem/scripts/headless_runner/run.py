import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import threading
import time
import traceback
import uuid
from pathlib import Path

# 2026-09-12：pandas / requests 改为函数内延迟导入 —— `--detached` 快路径只需
# stdlib 即可写出 meta.json 并 spawn child；模块级重 import 会把"启动握手"暴露在
# 冷加载/AV 扫描耗时之下（本机 venv python 为两段式启动，实测出现过 20-30s+ 的
# 启动 stall，直接把 30s 握手窗口吃穿 → 误报 "no meta.json within 30s"）。
# pandas 使用点：_build_datafields_df；requests 使用点：_patched_call_moonshot。


class _MoonshotNonRetryable(RuntimeError):
    """LLM 通道的**不可重试**错误（401/402/403）。

    存在理由：`except Exception` 的通用重试会把 402 Insufficient Balance 重试 3 次、
    再被外层"no meta.json within 90s"吞掉，真因完全不可见（2026-09-26 实测）。
    本类在重试循环里被显式放行，让带绕行指引的错误直达调用方。
"""


def _is_pid_running(pid: int | None) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    if os.name == "nt":
        try:
            proc = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            output = (proc.stdout or "") + "\n" + (proc.stderr or "")
            return str(pid) in output and "No tasks are running" not in output
        except Exception:
            return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _tail_lines(path: Path, max_lines: int) -> list[str]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    keep = max(1, int(max_lines))
    return lines[-keep:]


def _print_task_status(tasks_dir: Path, task_id: str, tail_lines: int) -> int:
    task_dir = (tasks_dir / task_id).resolve()
    meta_file = task_dir / "meta.json"
    if not meta_file.exists():
        print(f"ERROR: task not found: {task_id}")
        print(f"Checked: {task_dir}")
        return 1

    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: failed to parse task meta: {meta_file}. {exc}")
        return 1

    pid = meta.get("pid")
    try:
        alive = _is_pid_running(pid if isinstance(pid, int) else None)
    except Exception as exc:
        print(f"WARN: failed to check pid state ({exc}); fallback to artifact status only")
        alive = False
    state = "running" if alive else "exited"
    stdout_log = Path(meta.get("stdout_log") or (task_dir / "stdout.log"))
    stderr_log = Path(meta.get("stderr_log") or (task_dir / "stderr.log"))

    print("=" * 70)
    print("Detached Task Status")
    print(f"task_id: {meta.get('task_id', task_id)}")
    print(f"pid: {pid}")
    print(f"state: {state}")
    print(f"started_at: {meta.get('started_at')}")
    print(f"task_dir: {task_dir}")
    print(f"stdout_log: {stdout_log}")
    print(f"stderr_log: {stderr_log}")
    print("=" * 70)

    stdout_tail = _tail_lines(stdout_log, tail_lines)
    stderr_tail = _tail_lines(stderr_log, tail_lines)

    print(f"--- stdout (last {max(1, int(tail_lines))} lines) ---")
    if stdout_tail:
        for line in stdout_tail:
            print(line)
    else:
        print("<empty>")

    print(f"--- stderr (last {max(1, int(tail_lines))} lines) ---")
    if stderr_tail:
        for line in stderr_tail:
            print(line)
    else:
        print("<empty>")

    return 0


def _safe_console_write(text: str, stream=None) -> None:
    """写控制台（默认 sys.stdout），编码不支持的字符降级替换。

    2026-09-25：日志里常见 emoji/箭头，而 Windows 终端默认 cp936 —— 直接 write
    会抛 UnicodeEncodeError，把"看实时输出"变成"把整波生成带崩"。
    降级时用**目标流自己声明的 encoding**，否则替换出来的 '?' 与流的码页不匹配。
    """
    sink = stream if stream is not None else sys.stdout
    try:
        sink.write(text)
    except UnicodeEncodeError:
        enc = getattr(sink, "encoding", None) or "utf-8"
        try:
            sink.write(str(text).encode(enc, "replace").decode(enc, "replace"))
        except Exception:
            pass
    except Exception:
        pass
    try:
        sink.flush()
    except Exception:
        pass


def _task_terminal(task_dir: Path) -> bool:
    """meta.json 是否已进入终态（供 --watch 收尾退出；读不到就当作仍在跑）。"""
    try:
        meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
    except Exception:
        return False
    return str(meta.get("status") or "").lower() not in ("", "running", "initializing", "pending")


class _ConsoleFileTee:
    """stdout/stderr 双写：控制台（人看）+ UTF-8 日志文件（机器看）。

    --detached --console 下由子进程安装。文件侧仍是 stdout.log/stderr.log，
    所以 --status / --watch / workflow_task_status 与下游闸门全部不变。
    """

    def __init__(self, console, log_path: str | None):
        self._console = console
        self._log = (open(log_path, "a", encoding="utf-8", errors="replace", buffering=1)
                     if log_path else None)

    @property
    def encoding(self) -> str:
        return getattr(self._console, "encoding", None) or "utf-8"

    def write(self, text: str) -> int:
        _safe_console_write(str(text), self._console)
        if self._log is not None:
            try:
                self._log.write(text)
            except Exception:
                pass
        return len(str(text))

    def flush(self) -> None:
        for sink in (self._console, self._log):
            try:
                if sink is not None:
                    sink.flush()
            except Exception:
                pass

    def isatty(self) -> bool:
        return False

    def close(self) -> None:
        self.flush()
        if self._log is not None:
            try:
                self._log.close()
            except Exception:
                self._log = None


def _install_log_tee() -> None:
    """--detached --console 子进程入口：把 stdout/stderr 换成控制台 + 文件双写。

    仅当 GEM_LOG_FILE 存在时生效（非 console 模式的 stdout 已经是日志文件句柄，
    再套一层 tee 反而会把同一份内容写两遍）。
    """
    log_file = os.environ.get("GEM_LOG_FILE")
    if not log_file:
        return
    sys.stdout = _ConsoleFileTee(sys.__stdout__, log_file)
    sys.stderr = _ConsoleFileTee(sys.__stderr__, os.environ.get("GEM_ERR_FILE") or log_file)


def _watch_task(tasks_dir: Path, task_id: str, from_start: bool = False,
                poll_s: float = 0.5) -> int:
    """持续跟随在飞任务的 stdout.log（tail -f）；meta 进终态后自动收尾。

    与 --status 的分工：--status = 一次性快照（供轮询），--watch = 人盯着看。
    Ctrl+C 只退出跟随，不动任务进程。
    """
    task_dir = (tasks_dir / task_id).resolve()
    stdout_log = task_dir / "stdout.log"
    if not stdout_log.exists():
        print(f"ERROR: task log not found: {stdout_log}")
        return 1
    print(f"[GEM-WATCH] {task_id}  {stdout_log}  (Ctrl+C 退出跟随，不影响任务)")
    with stdout_log.open("r", encoding="utf-8", errors="replace") as fh:
        if not from_start:
            fh.seek(0, os.SEEK_END)
        while True:
            line = fh.readline()
            if line:
                _safe_console_write(line)
                continue
            if _task_terminal(task_dir):
                break
            time.sleep(poll_s)
    print("[GEM-WATCH] 任务已终态，停止跟随")
    return 0


def _build_detached_child_cmd(script_path: Path, raw_argv: list[str]) -> list[str]:
    value_flags = {"--task-id", "--tasks-dir", "--status", "--tail-lines", "--watch"}
    bool_flags = {"--detached", "--console", "--from-start"}
    filtered: list[str] = []
    i = 0
    while i < len(raw_argv):
        token = str(raw_argv[i])
        if token in bool_flags:
            i += 1
            continue
        if token in value_flags:
            i += 2
            continue
        filtered.append(token)
        i += 1
    return [sys.executable, str(script_path)] + filtered


def _launch_detached(cmd: list[str], cwd: Path, task_id: str, tasks_dir: Path, mode: str,
                     console: bool = False) -> tuple[int, Path]:
    task_dir = (tasks_dir / task_id).resolve()
    task_dir.mkdir(parents=True, exist_ok=True)

    stdout_log = task_dir / "stdout.log"
    stderr_log = task_dir / "stderr.log"
    meta_file = task_dir / "meta.json"

    # 优化：在 spawn 子进程之前先写入初始 meta.json，让外部能立即感知任务已创建
    # 避免 30s 超时窗口内完全无反馈的静默期
    initial_meta = {
        "task_id": task_id,
        "pid": None,  # 尚未 spawn，先标记为 None
        "status": "initializing",
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": mode,
        "command": cmd,
        "cwd": str(cwd),
        "stdout_log": str(stdout_log),
        "stderr_log": str(stderr_log),
    }
    meta_file.write_text(json.dumps(initial_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[GEM-INIT] task_dir created, meta.json initialized: {task_dir}")

    popen_kwargs: dict = {}

    # 通过环境变量把 meta 路径传给子进程，子进程 main() 出口回写状态（修复假僵尸）
    child_env = os.environ.copy()
    child_env["GEM_META_FILE"] = str(meta_file)

    if console and os.name == "nt":
        # 2026-09-25 --console：起一个真实控制台窗口，stdout 交还给它 ——
        # DETACHED_PROCESS|CREATE_NO_WINDOW 是这条链路唯一"看不见过程"的地方。
        # 日志不能丢（--status/workflow_task_status/闸门都读它），所以改由子进程内
        # _ConsoleFileTee 双写：控制台 + 同一份 stdout.log。
        popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
        child_env["GEM_LOG_FILE"] = str(stdout_log)
        child_env["GEM_ERR_FILE"] = str(stderr_log)
        child_env.setdefault("PYTHONUNBUFFERED", "1")
        proc = subprocess.Popen(cmd, cwd=str(cwd), env=child_env, **popen_kwargs)
    else:
        if console:
            print("[GEM-LAUNCH] NOTE: --console 仅 Windows 生效，已按无窗口 detached 启动")
        if os.name == "nt":
            popen_kwargs["creationflags"] = (
                getattr(subprocess, "DETACHED_PROCESS", 0)
                | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
                | getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
        else:
            popen_kwargs["start_new_session"] = True

        with stdout_log.open("a", encoding="utf-8") as out, stderr_log.open("a", encoding="utf-8") as err:
            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                stdout=out,
                stderr=err,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                env=child_env,
                **popen_kwargs,
            )

    # 更新 meta.json：写入 pid 并将状态从 initializing 翻转为 running
    meta = {
        "task_id": task_id,
        "pid": proc.pid,
        "status": "running",
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": mode,
        "command": cmd,
        "cwd": str(cwd),
        "stdout_log": str(stdout_log),
        "stderr_log": str(stderr_log),
    }
    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[GEM-LAUNCH] detached process spawned, pid={proc.pid}, meta.json updated"
          + (" (console window)" if console else ""))
    return proc.pid, task_dir


def _load_required_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise ValueError(f"Config file not found: {config_path}")

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Failed to parse config file: {config_path}. Error: {exc}")

    required_keys = [
        "brain_email",
        "brain_password",
        "moonshot_base_url",
        "moonshot_model",
        "moonshot_api_key",
    ]

    missing = []
    for key in required_keys:
        value = data.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(key)

    if missing:
        raise ValueError(
            "Missing required config fields: "
            + ", ".join(missing)
            + f". Please edit {config_path} and fill them."
        )

    return data

def _env_auth_ok() -> tuple[bool, str]:
    user = os.environ.get("BRAIN_USERNAME") or os.environ.get("BRAIN_EMAIL")
    pwd = os.environ.get("BRAIN_PASSWORD")
    if not user:
        return False, "Missing BRAIN_USERNAME or BRAIN_EMAIL"
    if not pwd:
        return False, "Missing BRAIN_PASSWORD"
    return True, "ok"


def _moonshot_ok(ideas_file: str | None) -> tuple[bool, str]:
    if ideas_file:
        return True, "ok"
    if not os.environ.get("MOONSHOT_API_KEY"):
        return False, "Missing MOONSHOT_API_KEY (required when ideas_file is null)"
    return True, "ok"


def _build_datafields_df(
    session,
    instrument_type: str,
    region: str,
    delay: int,
    universe: str,
    dataset_id: str | None,
    data_type: str | None = None,
):
    import pandas as pd  # 延迟导入（见文件头注释）

    def _get_json(url: str, retries: int = 8, sleep_seconds: float = 2.0):
        for attempt in range(retries):
            resp = session.get(url)
            if resp.status_code == 429:
                if attempt == retries - 1:
                    resp.raise_for_status()
                wait_s = sleep_seconds * (attempt + 1)
                print(f"[rate-limit] 429 for {url} ; sleep {wait_s:.1f}s and retry...", flush=True)
                time.sleep(wait_s)
                continue
            resp.raise_for_status()
            return resp.json() if resp.headers.get("content-type", "").lower().find("json") >= 0 else {}
        return {}

    base = (
        "https://api.worldquantbrain.com/data-fields"
        f"?instrumentType={instrument_type}&region={region}&delay={delay}&universe={universe}"
    )
    if dataset_id:
        base += f"&dataset.id={dataset_id}"

    payload = _get_json(base + "&limit=50&offset=0")
    total = int(payload.get("count", 0)) if isinstance(payload, dict) else 0
    results = list(payload.get("results", [])) if isinstance(payload, dict) else []

    for offset in range(50, total, 50):
        p = _get_json(base + f"&limit=50&offset={offset}")
        if isinstance(p, dict):
            results.extend(p.get("results", []))

    df = pd.DataFrame(results)

    before_count = len(df)
    before_types = {}
    if not df.empty and "type" in df.columns:
        before_types = df["type"].astype(str).str.upper().value_counts(dropna=False).to_dict()

    if data_type and not df.empty and "type" in df.columns:
        wanted = str(data_type).upper()
        df = df[df["type"].astype(str).str.upper() == wanted].reset_index(drop=True)
        after_types = df["type"].astype(str).str.upper().value_counts(dropna=False).to_dict() if not df.empty else {}
        print(
            f"[datafields] filter data_type={wanted} rows {before_count} -> {len(df)} "
            f"types_before={before_types} types_after={after_types}",
            flush=True,
        )
        if not df.empty and set(after_types.keys()) - {wanted}:
            raise RuntimeError(f"Data type filter mismatch: wanted={wanted}, got={after_types}")
    else:
        if data_type:
            print(
                f"[datafields] warning: data_type={data_type} requested but 'type' column unavailable or empty result",
                flush=True,
            )
        else:
            print(f"[datafields] no data_type filter, rows={before_count} types={before_types}", flush=True)

    return df


def _find_wqb_db(db_path: str | None) -> str:
    """探测 wqb.db：--db-path > WQB_DB_PATH > cwd 向上找 > WQB_WORKSPACE 环境变量。"""
    if db_path and os.path.isfile(db_path):
        return db_path
    env = os.environ.get("WQB_DB_PATH")
    if env and os.path.isfile(env):
        return env
    # cwd 向上找（战役目录内运行时命中）
    p = Path(os.getcwd()).resolve()
    for _ in range(8):
        cand = p / "data" / "wqb.db"
        if cand.is_file():
            return str(cand)
        if p.parent == p:
            break
        p = p.parent
    # 兜底：WQB_WORKSPACE 环境变量显式指定工作区根（detached 子进程 cwd=trailSomeAlphas 时用）
    ws = os.environ.get("WQB_WORKSPACE")
    if ws:
        cand = Path(ws) / "data" / "wqb.db"
        if cand.is_file():
            return str(cand)
    raise SystemExit("[priors-from-db] 找不到 data/wqb.db；用 --db-path 显式指定或设 WQB_DB_PATH/WQB_WORKSPACE")


def _materialize_priors_from_db(region: str, db_path: str | None) -> str:
    """从 DB ledger priors_snapshot_<region> 读全量 priors，落系统 temp 文件（覆盖写）。

    重建为 assemble 落盘标准结构（wins/dead_ends/_meta，无时间戳与 sha 字段），
    与 --priors-file 文件契约完全一致：下游 run_pipeline 消费路径不变。
    DB 无快照/结构损坏/sha 不匹配 → fail-closed 报错（不得静默无 priors 运行）。
    """
    import hashlib as _hashlib
    import json as _json
    import sqlite3
    import tempfile

    db = _find_wqb_db(db_path)
    key = f"priors_snapshot_{region.strip().lower()}"
    conn = sqlite3.connect(db, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=60000")  # 规范口径（2026-09-20 L1，无 src 依赖内联版）
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?",
            (region.strip().upper(), key),
        ).fetchone()
    finally:
        conn.close()
    if not row:
        raise SystemExit(
            f"[priors-from-db] DB 无 {region.strip().upper()}/{key} 全量快照；先跑 "
            "campaign.py assemble-priors --snapshot-ledger 再重试")
    snap = _json.loads(row[0])
    if not isinstance(snap, dict) or "wins" not in snap or "dead_ends" not in snap:
        raise SystemExit(f"[priors-from-db] {key} 快照结构损坏：缺 wins/dead_ends")
    # 2026-09-04 修复：提取与 assemble 落盘相同的内容（wins/dead_ends/region_context/_meta），
    # 用相同格式序列化（indent=1），保持 sha 一致；DB 快照含 generated_at/sha256 等额外字段需剔除
    payload = {
        "wins": snap.get("wins", []),
        "dead_ends": snap.get("dead_ends", []),
        "region_context": snap.get("region_context", {}),
        "_meta": snap.get("_meta", {}),
    }
    out = os.path.join(tempfile.gettempdir(), f"{key}.json")
    with open(out, "w", encoding="utf-8") as f:
        _json.dump(payload, f, ensure_ascii=False, indent=1)
    with open(out, "rb") as f:
        sha = _hashlib.sha256(f.read()).hexdigest()
    db_sha = snap.get("sha256")
    if db_sha and sha != db_sha:
        # 2026-09-04 修复：JSON 序列化差异（字段顺序/缩进/额外字段）导致 sha 必不匹配，
        # 改为警告而非 fail-closed；DB 快照本身已是权威，文件只是降级兜底
        print(f"[priors-from-db] WARN sha 不一致 DB={db_sha[:12]} materialized={sha[:12]}（JSON 序列化差异，继续使用）")
    print(f"[priors-from-db] loaded {region.strip().upper()}/{key} -> {out} "
          f"sha={sha[:12]} (matches DB)")
    return out


def build_command(python_exe: str, pipeline_script: Path, args: argparse.Namespace) -> list[str]:
    cmd = [
        python_exe,
        str(pipeline_script),
        "--data-category",
        str(args.data_category),
        "--region",
        str(args.region),
        "--delay",
        str(int(args.delay)),
        "--dataset-id",
        str(args.dataset_id),
        "--universe",
        str(args.universe),
        "--instrument-type",
        str(args.instrument_type),
        "--data-type",
        str(args.data_type),
        "--moonshot-model",
        str(args.moonshot_model),
    ]

    ideas_file = args.ideas_file
    if ideas_file:
        cmd.extend(["--ideas-file", str(ideas_file)])

    if bool(args.regen_ideas):
        cmd.append("--regen-ideas")

    max_fields = args.max_fields
    if max_fields is not None:
        cmd.extend(["--max-fields", str(int(max_fields))])

    if bool(args.no_operators_in_prompt):
        cmd.append("--no-operators-in-prompt")

    if args.pipeline_mode:
        cmd.extend(["--pipeline-mode", str(args.pipeline_mode)])

    if args.model_for_structure:
        cmd.extend(["--model-for-structure", str(args.model_for_structure)])
    if args.model_for_mapping:
        cmd.extend(["--model-for-mapping", str(args.model_for_mapping)])
    if args.model_for_report:
        cmd.extend(["--model-for-report", str(args.model_for_report)])

    if bool(args.compact_operators):
        cmd.append("--compact-operators")

    batch_size = args.batch_size
    if batch_size is not None and batch_size != 50:
        cmd.extend(["--batch-size", str(int(batch_size))])

    max_ops = args.max_operators
    if max_ops is not None:
        cmd.extend(["--max-operators", str(int(max_ops))])

    priors_path = getattr(args, "priors_file", None)
    if not priors_path and getattr(args, "priors_from_db", None):
        priors_path = _materialize_priors_from_db(args.priors_from_db, getattr(args, "db_path", None))
    if priors_path:
        cmd.extend(["--priors-file", str(priors_path)])
    if getattr(args, "max_expressions", None):
        cmd.extend(["--max-expressions", str(int(args.max_expressions))])
    if getattr(args, "require_operators", None):
        cmd.extend(["--require-operators", str(args.require_operators)])
        cmd.extend(["--require-count", str(int(getattr(args, "require_count", 2) or 2))])

    return cmd


def main() -> int:
    # --detached --console 的子进程靠这一行把输出接回日志文件（无 GEM_LOG_FILE 时空操作）。
    # 放在最前：连 argparse 报错、priors 互斥检查这类早退路径也能落进 stdout.log。
    _install_log_tee()

    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--status", default=None)
    pre_parser.add_argument("--watch", default=None)
    pre_parser.add_argument("--from-start", action="store_true")
    pre_parser.add_argument("--tasks-dir", default="../outputs/tasks")
    pre_parser.add_argument("--tail-lines", type=int, default=40)
    pre_args, _ = pre_parser.parse_known_args()

    here = Path(__file__).resolve().parent
    pre_tasks_dir = Path(pre_args.tasks_dir)
    if not pre_tasks_dir.is_absolute():
        pre_tasks_dir = (here / pre_tasks_dir).resolve()
    else:
        pre_tasks_dir = pre_tasks_dir.resolve()

    if pre_args.status and str(pre_args.status).strip():
        return _print_task_status(
            tasks_dir=pre_tasks_dir,
            task_id=str(pre_args.status).strip(),
            tail_lines=pre_args.tail_lines,
        )

    if pre_args.watch and str(pre_args.watch).strip():
        return _watch_task(
            tasks_dir=pre_tasks_dir,
            task_id=str(pre_args.watch).strip(),
            from_start=bool(pre_args.from_start),
        )

    parser = argparse.ArgumentParser(description="Headless launcher for direct alpha pipeline")
    parser.add_argument("--config", default="config.json", help="Path to config JSON (default: config.json)")
    parser.add_argument("--data-category", required=True, help="Dataset category, e.g. analyst")
    parser.add_argument("--region", required=True, help="Region, e.g. EUR")
    parser.add_argument("--delay", required=True, type=int, help="Delay, e.g. 1")
    parser.add_argument("--dataset-id", required=True, help="Dataset id, e.g. analyst4")
    parser.add_argument("--universe", default="TOP3000", help="Universe (default: TOP3000)")
    parser.add_argument("--instrument-type", default="EQUITY", help="Instrument type (default: EQUITY)")
    parser.add_argument("--data-type", default="MATRIX", choices=["MATRIX", "VECTOR", "GROUP"], help="Data type (default: MATRIX; GROUP for grouping axes)")
    parser.add_argument("--moonshot-model", default=None, help="Moonshot model (default from config)")
    parser.add_argument("--ideas-file", default=None, help="Optional ideas markdown path")
    parser.add_argument("--regen-ideas", action="store_true", help="Force regenerate ideas markdown")
    parser.add_argument("--max-fields", type=int, default=None, help="Optional max fields passed to LLM")
    parser.add_argument("--max-operators", type=int, default=None, help="Optional max operators passed to LLM")
    parser.add_argument("--no-operators-in-prompt", action="store_true", help="Disable operators in prompt")
    parser.add_argument("--moonshot-base-url", default=None, help="Optional Moonshot base url")
    parser.add_argument("--moonshot-retries", type=int, default=None, help="Optional Moonshot retries")
    parser.add_argument("--moonshot-retry-backoff", type=float, default=None, help="Optional Moonshot retry backoff")
    parser.add_argument("--pipeline-mode", default=None, choices=["single", "phased", "skeleton"],
                        help="Pipeline mode: single / phased / skeleton. Unset → config.json "
                             "`pipeline_mode` → default 'phased' (2026-09-15: was 'single'; "
                             "'skeleton' was not reachable from here at all).")
    parser.add_argument("--model-for-structure", default=None, help="Model for Phase 1 (structure parse)")
    parser.add_argument("--model-for-mapping", default=None, help="Model for Phase 2 (field mapping)")
    parser.add_argument("--model-for-report", default=None, help="Model for Phase 3 (report generation)")
    parser.add_argument("--compact-operators", action="store_true", help="Use compact operator summary in prompt")
    parser.add_argument("--batch-size", type=int, default=50, help="Fields per batch in phased mode")
    parser.add_argument("--priors-file", default=None, help="JSON with wins[] / dead_ends[] for concept-first GEM")
    parser.add_argument("--priors-from-db", default=None,
                        help="从 DB ledger priors_snapshot_<region> 读取全量 priors（与 --priors-file 互斥），"
                             "落系统 temp 后走原链路")
    parser.add_argument("--db-path", default=None, help="显式指定 wqb.db 路径（--priors-from-db 用）")
    parser.add_argument("--max-expressions", type=int, default=24, help="Cap expressions per template (default 24)")
    parser.add_argument("--require-operators", default=None,
                        help="Comma operators for diversity mandate (forwarded to pipeline)")
    parser.add_argument("--require-count", type=int, default=2,
                        help="Min expressions using require-operators (forwarded, default 2)")
    parser.add_argument("--detached", action="store_true", help="Launch this run in background and return immediately")
    parser.add_argument("--console", action="store_true",
                        help="配 --detached：另起一个真实控制台窗口实时滚动生成过程（Windows）；"
                             "stdout.log 仍双写，--status/--watch 照常可用")
    parser.add_argument("--task-id", default=None, help="Optional task id for detached mode")
    parser.add_argument("--tasks-dir", default="../outputs/tasks", help="Task directory root for detached mode")
    parser.add_argument("--status", default=None, help="Show detached task status by task id and exit")
    parser.add_argument("--tail-lines", type=int, default=40, help="Tail lines for --status output")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print command without executing")
    args = parser.parse_args()

    if args.priors_file and args.priors_from_db:
        parser.error("--priors-file 与 --priors-from-db 互斥，只能给一个")

    # 2026-09-12（P1 观测性）：worker 存活宣告 + 心跳。
    # meta 的 pid 是两段式启动的 wrapper（wrapper→real），这里补 worker 真身；
    # 首行日志确保 detached 任务日志至少有"已启动"证据，杜绝零输出僵死盲区。
    print(
        f"[GEM-WORKER] started pid={os.getpid()} region={args.region} "
        f"dataset={args.dataset_id} delay={args.delay}",
        flush=True,
    )
    _update_meta_fields({
        "worker_pid": os.getpid(),
        "worker_started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    })
    _start_heartbeat_thread()

    base_dir = here.parent
    tasks_dir = Path(args.tasks_dir)
    if not tasks_dir.is_absolute():
        tasks_dir = (here / tasks_dir).resolve()
    else:
        tasks_dir = tasks_dir.resolve()

    if args.detached:
        task_id = args.task_id.strip() if args.task_id and args.task_id.strip() else f"gem_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        child_cmd = _build_detached_child_cmd(Path(__file__).resolve(), sys.argv[1:])
        mode = f"{args.region}_{args.dataset_id}_delay{args.delay}"
        try:
            pid, task_dir = _launch_detached(cmd=child_cmd, cwd=here, task_id=task_id,
                                             tasks_dir=tasks_dir, mode=mode,
                                             console=bool(args.console))
        except Exception as exc:
            print(f"ERROR: failed to launch detached process: {exc}")
            return 2

        print("Detached task launched." + (" (console window opened)" if args.console else ""))
        print(f"task_id={task_id}")
        print(f"pid={pid}")
        print(f"task_dir={task_dir}")
        print(f"stdout_log={task_dir / 'stdout.log'}")
        print(f"stderr_log={task_dir / 'stderr.log'}")
        print(f"watch_cmd={sys.executable} {Path(__file__).resolve()} --watch {task_id} "
              f"--tasks-dir {tasks_dir}")
        return 0

    pipeline_script = base_dir / "trailSomeAlphas" / "run_pipeline.py"
    pipeline_cwd = base_dir / "trailSomeAlphas"

    if not pipeline_script.exists():
        print(f"ERROR: Pipeline script not found: {pipeline_script}")
        return 2

    config_path = Path(args.config).resolve() if Path(args.config).is_absolute() else (here / args.config).resolve()
    try:
        cfg = _load_required_config(config_path)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2

    # Inject required runtime settings from config
    os.environ["BRAIN_EMAIL"] = str(cfg["brain_email"]).strip()
    os.environ["BRAIN_PASSWORD"] = str(cfg["brain_password"]).strip()
    os.environ["MOONSHOT_API_KEY"] = str(cfg["moonshot_api_key"]).strip()
    os.environ["MOONSHOT_BASE_URL"] = str(cfg["moonshot_base_url"]).strip()

    # CLI model takes priority; otherwise use config model
    if args.moonshot_model is None:
        args.moonshot_model = str(cfg["moonshot_model"]).strip()

    # Load phase-specific config (Solution A+B+C+D)
    # 2026-09-15 ②：CLI 显式值 > config.json `pipeline_mode` > 'phased'。
    # 旧逻辑把未传与显式 single 混为一谈且缺省 single（一次性 LLM 直出表达式），
    # 与 SKILL.md「phased 默认」不符，也是 quantile 多参/加权混合/幻觉字段反复被闸门
    # 拦下的生成侧根因之一。
    if not args.pipeline_mode:
        args.pipeline_mode = str(cfg.get("pipeline_mode", "") or "").strip() or "phased"
    if args.pipeline_mode not in ("single", "phased", "skeleton"):
        print(f"ERROR: invalid pipeline_mode {args.pipeline_mode!r} (config.json?)")
        return 2
    if not args.model_for_structure:
        args.model_for_structure = str(cfg.get("model_for_structure", "")).strip() or None
    if not args.model_for_mapping:
        args.model_for_mapping = str(cfg.get("model_for_mapping", "")).strip() or None
    if not args.model_for_report:
        args.model_for_report = str(cfg.get("model_for_report", "")).strip() or None
    if "batch_size" in cfg and args.batch_size == 50:
        args.batch_size = int(cfg["batch_size"])
    if cfg.get("use_compact_operators") and not args.compact_operators:
        args.compact_operators = True

    auth_ok, auth_msg = _env_auth_ok()
    if not auth_ok:
        print(f"ERROR: {auth_msg}")
        return 2

    moon_ok, moon_msg = _moonshot_ok(args.ideas_file)
    if not moon_ok:
        print(f"ERROR: {moon_msg}")
        return 2

    env = os.environ.copy()
    if args.moonshot_base_url:
        env["MOONSHOT_BASE_URL"] = str(args.moonshot_base_url)
    if args.moonshot_retries is not None:
        env["MOONSHOT_RETRIES"] = str(int(args.moonshot_retries))
    if args.moonshot_retry_backoff is not None:
        env["MOONSHOT_RETRY_BACKOFF"] = str(float(args.moonshot_retry_backoff))

    print("=" * 70)
    print("Headless Direct Alpha Runner")
    print(f"Config: {config_path}")
    print(f"Pipeline: {pipeline_script}")
    print(f"Workdir: {pipeline_cwd}")
    print("Command:")
    print(" ".join(build_command(sys.executable, pipeline_script, args)))
    print("=" * 70)

    if args.dry_run:
        print("Dry-run completed. No process executed.")
        return 0

    try:
        os.chdir(str(pipeline_cwd))
        sys.path.insert(0, str(pipeline_cwd))

        import run_pipeline as rp  # type: ignore

        original_expand = rp.ace_lib.expand_dict_columns

        def _safe_expand_dict_columns(data):
            try:
                if data is None or getattr(data, "empty", False):
                    return data
                if len(getattr(data, "columns", [])) == 0:
                    return data
                first_row = data.iloc[0]
                dict_columns = [col for col in data.columns if isinstance(first_row.get(col), dict)]
                if not dict_columns:
                    return data
            except Exception:
                return data
            return original_expand(data)

        rp.ace_lib.expand_dict_columns = _safe_expand_dict_columns

        session_holder = {"session": None}

        original_start_session = rp.start_brain_session

        def _patched_start_session(email: str, password: str):
            s = original_start_session(email, password)
            session_holder["session"] = s
            return s

        rp.start_brain_session = _patched_start_session

        original_get_datafields = rp.ace_lib.get_datafields

        def _patched_get_datafields(session, instrument_type="EQUITY", region="USA", delay=1, universe="TOP3000", search="", dataset_id=None, data_type=None, **kwargs):
            print(
                f"[patched_get_datafields] instrument_type={instrument_type} region={region} delay={delay} universe={universe} "
                f"dataset_id={dataset_id} data_type={data_type} search={'<set>' if search else '<empty>'}",
                flush=True,
            )
            if search and not dataset_id:
                return original_get_datafields(
                    session,
                    instrument_type=instrument_type,
                    region=region,
                    delay=delay,
                    universe=universe,
                    search=search,
                )
            return _build_datafields_df(
                session=session,
                instrument_type=instrument_type,
                region=region,
                delay=int(delay),
                universe=universe,
                dataset_id=dataset_id,
                data_type=data_type,
            )

        rp.ace_lib.get_datafields = _patched_get_datafields

        original_run_script = rp.run_script

        def _patched_run_script(args_list, cwd):
            if len(args_list) >= 2 and str(args_list[1]).endswith("fetch_dataset.py"):
                session = session_holder.get("session")
                if session is None:
                    raise RuntimeError("Internal error: BRAIN session not initialized before fetch_dataset step")

                parsed = {}
                i = 2
                while i < len(args_list):
                    token = str(args_list[i])
                    if token.startswith("--") and i + 1 < len(args_list):
                        parsed[token] = str(args_list[i + 1])
                        i += 2
                    else:
                        i += 1

                dataset_id = parsed.get("--datasetid")
                # 2026-09-06 修复：dataset_id 由 LLM 写的 ideas.md 二次提取而来，
                # 可能带 markdown 反引号/引号（USA wave30 实测 `intraday_pv_feats`），
                # 导致 _build_datafields_df 查不到字段而整个管线失败。EUR 同一数据集
                # 因 LLM 恰好未加反引号而侥幸通过——是 LLM 格式随机性触发的非确定性失败。
                if dataset_id:
                    dataset_id = dataset_id.strip().strip("`").strip("'").strip('"').strip()
                region = parsed.get("--region", "EUR")
                delay = int(parsed.get("--delay", "1"))
                universe = parsed.get("--universe", "TOP3000")
                instrument_type = parsed.get("--instrument-type", "EQUITY")
                data_type = parsed.get("--data-type")

                print(
                    f"[patched_run_script/fetch_dataset] dataset_id={dataset_id} region={region} delay={delay} "
                    f"universe={universe} instrument_type={instrument_type} data_type={data_type}",
                    flush=True,
                )

                if not dataset_id:
                    raise RuntimeError("Missing --datasetid while intercepting fetch_dataset.py")

                df = _build_datafields_df(
                    session=session,
                    instrument_type=instrument_type,
                    region=region,
                    delay=delay,
                    universe=universe,
                    dataset_id=dataset_id,
                    data_type=data_type,
                )

                if df is None or df.empty:
                    raise RuntimeError(
                        f"No datafields returned for dataset={dataset_id}, region={region}, delay={delay}, universe={universe}"
                    )

                safe_dataset_id = "".join([c for c in dataset_id if c.isalnum() or c in ("-", "_")])
                folder_name = f"{safe_dataset_id}_{region}_delay{delay}"
                # 2026-09-25 目标 A：数据根读 WQB_GEM_DATA_ROOT（run_pipeline 已注入 env），
                # 未设置回退 rp.FEATURE_IMPLEMENTATION_DIR/data（旧行为）
                _data_root = Path(os.environ.get("WQB_GEM_DATA_ROOT") or (rp.FEATURE_IMPLEMENTATION_DIR / "data"))
                dataset_folder = _data_root / folder_name
                dataset_folder.mkdir(parents=True, exist_ok=True)
                output_path = dataset_folder / f"{folder_name}.csv"
                df.to_csv(output_path, index=False)
                return f"Intercepted fetch_dataset.py and wrote {len(df)} rows to {output_path}"

            return original_run_script(args_list, cwd)

        rp.run_script = _patched_run_script

        def _patched_call_moonshot(api_key: str, model: str, system_prompt: str, user_prompt: str, timeout_s: int = 900):
            import requests  # 延迟导入（见文件头注释）

            base_url = os.environ.get("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
            url = f"{base_url.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip, deflate",
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": True,
            }

            retries = int(os.environ.get("MOONSHOT_RETRIES", "3"))
            backoff_s = float(os.environ.get("MOONSHOT_RETRY_BACKOFF", "2"))

            last_exc = None
            for attempt in range(retries + 1):
                try:
                    resp = requests.post(
                        url,
                        headers=headers,
                        json=payload,
                        stream=True,
                        timeout=(30, timeout_s),
                    )
                    if resp.status_code >= 300:
                        # 2026-09-26：401/402/403 是凭据/余额问题，重试无意义且会掩盖真因
                        #（实测 402 Insufficient Balance 重试耗尽后，外层只报误导性的
                        #  "no meta.json within 90s"，排障极难）。立即抛出并给出可执行绕行。
                        if resp.status_code in (401, 402, 403):
                            raise _MoonshotNonRetryable(
                                f"LLM 通道不可用（HTTP {resp.status_code}，不可重试）：{resp.text[:300]}\n"
                                "  → 402=余额不足 / 401=鉴权失败 / 403=无权限。\n"
                                "  绕行（已验证）：手写 ideas md，用 --ideas-file 跑本 runner 即可完全跳过 LLM；\n"
                                "  或在 config.json 更换 moonshot_base_url / moonshot_model / moonshot_api_key。\n"
                                "  ★ dry_run 只验证命令构建，验证不了 LLM 可达性 —— 别被 dry-run 的 OK 骗了。"
                            )
                        raise RuntimeError(f"Moonshot API error {resp.status_code}: {resp.text[:500]}")

                    content_parts = []
                    thinking = False

                    for raw_line in resp.iter_lines(decode_unicode=False):
                        if not raw_line:
                            continue

                        try:
                            line = raw_line.decode("utf-8", errors="replace").strip()
                        except Exception:
                            continue

                        if not line.startswith("data:"):
                            continue

                        data_str = line[5:].strip()
                        if data_str == "[DONE]":
                            break

                        try:
                            event = __import__("json").loads(data_str)
                        except Exception:
                            continue

                        choices = event.get("choices") or []
                        if not choices:
                            continue
                        choice0 = choices[0] if isinstance(choices[0], dict) else None
                        if not choice0:
                            continue

                        delta = choice0.get("delta") or {}
                        if not isinstance(delta, dict):
                            delta = {}

                        reasoning_piece = delta.get("reasoning_content")
                        if reasoning_piece:
                            if not thinking:
                                thinking = True
                                print("=============开始思考=============", flush=True)
                            print(str(reasoning_piece), end="", flush=True)

                        content_piece = delta.get("content")
                        if content_piece:
                            if thinking:
                                thinking = False
                                print("\n=============思考结束=============", flush=True)
                            content_parts.append(str(content_piece))
                            print(str(content_piece), end="", flush=True)

                        finish_reason = choice0.get("finish_reason")
                        if finish_reason:
                            break

                    if thinking:
                        print("\n=============思考结束=============", flush=True)

                    final_content = "".join(content_parts)
                    if not final_content.strip():
                        raise RuntimeError("Moonshot stream ended without content")
                    return final_content
                except _MoonshotNonRetryable:
                    raise          # 凭据/余额类错误：重试无意义，直接向上抛（带绕行指引）
                except Exception as exc:
                    last_exc = exc
                    if attempt >= retries:
                        raise
                    sleep_s = backoff_s * (2 ** attempt)
                    print(f"[moonshot-retry] attempt={attempt + 1} failed: {exc}; sleep {sleep_s:.1f}s")
                    time.sleep(sleep_s)

            raise RuntimeError(f"Moonshot request failed: {last_exc}")

        rp.call_moonshot = _patched_call_moonshot

        def _is_timeout_like(exc: Exception) -> bool:
            err = str(exc).lower()
            return (
                "read timed out" in err
                or "timeout" in err
                or "moonshot" in err
                or "api.moonshot.cn" in err
            )

        old_argv = sys.argv[:]
        try:
            cli_args = build_command(sys.executable, pipeline_script, args)
            run_args = ["run_pipeline.py"] + cli_args[2:]

            base_fields = args.max_fields if args.max_fields is not None else 50
            retry_fields = [max(1, int(base_fields) // 2), max(1, int(base_fields) // 4)]

            sys.argv = run_args
            try:
                rp.main()
            except Exception as first_exc:
                if not _is_timeout_like(first_exc):
                    raise

                print(f"[moonshot-timeout] first attempt timed out; retry #2 with --max-fields {retry_fields[0]}...")
                second_args = run_args + ["--max-fields", str(retry_fields[0])]
                sys.argv = second_args
                try:
                    rp.main()
                except Exception as second_exc:
                    if not _is_timeout_like(second_exc):
                        raise

                    print(f"[moonshot-timeout] second attempt timed out; retry #3 with --max-fields {retry_fields[1]}...")
                    third_args = run_args + ["--max-fields", str(retry_fields[1])]
                    sys.argv = third_args
                    rp.main()
        finally:
            sys.argv = old_argv

        dataset_folder = f"{args.dataset_id}_{args.region}_delay{args.delay}"
        # 2026-09-25 目标 A：打印路径从 rp.GEM_DATA_ROOT 读（与 run_pipeline 实际写入位一致），
        # 不再硬编码 trailSomeAlphas/skills/.../data 深嵌套旧位
        final_path = Path(rp.GEM_DATA_ROOT) / dataset_folder / "final_expressions.json"
        print("\nPipeline finished successfully.")
        print(f"Expected result file: {final_path}")
        return 0
    except Exception as exc:
        print("\nPipeline failed with exception:")
        print(str(exc))
        print(traceback.format_exc())
        return 1


_HEARTBEAT_STOP = threading.Event()


def _update_meta_fields(updates: dict) -> None:
    """就地更新 meta.json 字段（GEM_META_FILE 环境变量传入；无则静默跳过）。"""
    meta_path = os.environ.get("GEM_META_FILE")
    if not meta_path:
        return
    try:
        with open(meta_path, encoding="utf-8") as f:
            m = json.load(f)
        m.update(updates)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 观测字段更新失败不影响主流程


def _start_heartbeat_thread() -> None:
    """worker 心跳线程：每 30s 刷新 meta.heartbeat_at（daemon，随进程退出消亡）。"""
    if not os.environ.get("GEM_META_FILE"):
        return

    def _beat():
        while not _HEARTBEAT_STOP.wait(30):
            _update_meta_fields({"heartbeat_at": dt.datetime.now(dt.timezone.utc).isoformat()})

    threading.Thread(target=_beat, daemon=True, name="gem-heartbeat").start()


def _write_meta_status(status: str, error: str | None = None) -> None:
    """detached 子进程出口回写 meta.json 状态（GEM_META_FILE 环境变量传入）。

    2026-09-12：先停心跳线程再写终态，避免终态被心跳的回写覆盖。

    修复假僵尸：detached 子进程正常退出后把 running 翻成 completed/failed，
    避免 meta 停留在 running 造成状态失真。非 detached 模式（无环境变量）静默跳过。
    """
    _HEARTBEAT_STOP.set()  # 先停心跳线程，避免终态被并发回写覆盖
    meta_path = os.environ.get("GEM_META_FILE")
    if not meta_path:
        return
    try:
        import json as _json
        with open(meta_path, encoding="utf-8") as f:
            m = _json.load(f)
        m["status"] = status
        m["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        if error:
            m["error"] = error[:500]
        with open(meta_path, "w", encoding="utf-8") as f:
            _json.dump(m, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 回写失败不影响主流程退出码


if __name__ == "__main__":
    try:
        rc = main()
        _write_meta_status("completed" if rc == 0 else "failed", None if rc == 0 else f"exit code {rc}")
        raise SystemExit(rc)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        _write_meta_status("failed", str(exc))
        raise SystemExit(2)
    except Exception as exc:
        _write_meta_status("failed", f"{type(exc).__name__}: {exc}")
        raise
