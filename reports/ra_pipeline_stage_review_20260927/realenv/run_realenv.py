# -*- coding: utf-8 -*-
"""RA 九步流水线 · 真实环境 dry-run（2026-09-27，两个 P0 修复之后）

与第一轮沙箱演练（../run_dryrun.py）的区别：
  * 真实仓库工作树（非 git archive 副本），真实默认库路径 <repo>/data/wqb.db（演练期间把原库临时移到
    REALENV_SCRATCH、从空库开始，结束后移回；>5MB 的库需 REALENV_ALLOW_DB_SWAP=1 才动）；
  * 两个 MCP server 按仓库 .mcp.json 的 command/args/env 翻译成本机路径后**经 stdio 真实启动**，
    所有调用都走 MCP 协议层（FastMCP 参数校验、工具注册、stderr 启动告警全部是真的）；
  * 数据 = tracking/KOR 下已入库的真实历史：candidates/wave*_result*.json（逐 alpha 指标 + 波级 verdict 原文）、
    priors/kor_priors.json（反推 DB 侧 KB）、reference/kor_<ds>_fields.json（字段目录）、config/thresholds.json；
    全部经 wqb-db 的 MCP 写工具导入（导入即在演练契约本身）；
  * 平台：本容器无 BRAIN 凭据（world-quant-brain-mcp/.env 不存在；本脚本从不读取它），
    平台类工具只记录其真实失败形态——不会也无法产生任何平台写入；
  * 需要"修复前"对照的两个 P0，用 scratchpad 里的 git archive 原始副本（BASE_DIR）起同样两个 server 重放。

用法：见同目录 reproduce_realenv.sh。输出为纯文本演练记录（realenv_transcript.txt）。
"""
from __future__ import annotations

import asyncio
import contextlib
import glob
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(os.environ.get("WQB_REPO") or Path(__file__).resolve().parents[3]).resolve()
BASE_DIR = Path(os.environ["BASE_DIR"]).resolve() if os.environ.get("BASE_DIR") else None
SCRATCH = Path(os.environ.get("REALENV_SCRATCH") or Path(tempfile.gettempdir()) / "wqb_realenv").resolve()
_VENV = ROOT / "world-quant-brain-mcp" / ".venv"
PY = str(_VENV / "bin" / "python") if (_VENV / "bin" / "python").exists() else str(_VENV / "Scripts" / "python.exe")
R = "KOR"
DS = "ml_factor_proj"            # KOR 唯一产生过 ACTIVE 的数据集（wave91c 2 RA）；有字段目录与多波真实回测
DS2 = "multi_source_model"       # wave91c 跨数据集 mix 的另一腿（short_horizon_hedge3_* 等字段所在）
WIN_PREFIX = "D:/coding/traeCN_project/wqb"
SCRATCH.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------------- 输出工具
def H1(t):
    print("\n" + "=" * 110 + f"\n{t}\n" + "=" * 110, flush=True)


def H2(t):
    print(f"\n--- {t}", flush=True)


def dump(obj, n=600):
    s = json.dumps(obj, ensure_ascii=False, default=str) if not isinstance(obj, str) else obj
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[:n] + f" …(+{len(s) - n} chars)"


def rel(p):
    p = str(p)
    for base, tag in ((str(ROOT), "<repo>"), (str(BASE_DIR or "/nonexistent"), "<base>"), (str(SCRATCH), "<scratch>")):
        p = p.replace(base, tag)
    return p


# ----------------------------------------------------------------------------- 副作用探针（真实环境版）
def db_counts(db):
    if not Path(db).exists():
        return {}
    c = sqlite3.connect(str(db))
    try:
        tabs = [t for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        return {t: c.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tabs}
    finally:
        c.close()


def git_dirty(root):
    try:
        out = subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True).stdout
    except Exception:
        return set()
    return {ln[3:] for ln in out.splitlines() if ln.strip()}


def watched_files(root):
    found = {}
    for sub in ("logs/_async_tasks", "data"):
        d = Path(root) / sub
        if d.is_dir():
            for f in d.iterdir():
                if f.is_file():
                    found[str(f)] = f.stat().st_mtime
    return found


class Probe:
    """记录一次调用前后：DB 各表行数变化 / git 工作树新增脏文件 / logs/_async_tasks 与 data/ 下新文件。"""

    def __init__(self, root, db):
        self.root, self.db = Path(root), Path(db)

    def __enter__(self):
        self.c0, self.g0, self.f0 = db_counts(self.db), git_dirty(self.root), watched_files(self.root)
        return self

    def __exit__(self, *exc):
        c1, g1, f1 = db_counts(self.db), git_dirty(self.root), watched_files(self.root)
        self.db_delta = {t: c1.get(t, 0) - self.c0.get(t, 0) for t in set(c1) | set(self.c0)
                         if c1.get(t, 0) != self.c0.get(t, 0)}
        self.git_new = sorted(g1 - self.g0)
        self.files_new = sorted(rel(f) for f in f1 if f not in self.f0 or f1[f] != self.f0.get(f))
        return False

    def summary(self):
        parts = []
        parts.append("DB Δ=" + (dump(self.db_delta, 300) if self.db_delta else "无"))
        parts.append("git 新脏文件=" + (dump(self.git_new, 200) if self.git_new else "无"))
        if self.files_new:
            parts.append("新/改文件=" + dump(self.files_new, 300))
        return " | ".join(parts)


# ----------------------------------------------------------------------------- MCP 客户端
class Srv:
    def __init__(self, name, session, root, db):
        self.name, self.s, self.root, self.db = name, session, Path(root), Path(db)
        self.calls = 0

    async def call(self, tool, quiet=False, label=None, n=700, **args):
        self.calls += 1
        t0 = time.time()
        with Probe(self.root, self.db) as pr:
            try:
                res = await self.s.call_tool(tool, args)
                is_err = bool(res.isError)
                if res.structuredContent is not None:
                    sc = res.structuredContent
                    data = sc["result"] if isinstance(sc, dict) and set(sc) == {"result"} else sc
                else:
                    txt = "\n".join(getattr(c, "text", "") for c in res.content)
                    try:
                        data = json.loads(txt)
                    except Exception:
                        data = txt
            except Exception as e:  # 传输层异常
                is_err, data = True, f"<transport exception> {type(e).__name__}: {e}"
        dt = time.time() - t0
        if not quiet:
            argstr = ", ".join(f"{k}={dump(v, 80)}" for k, v in args.items())
            print(f"[{self.name}] {label or tool}({argstr[:300]})  → isError={is_err}  {dt:.2f}s", flush=True)
            print(f"    out: {dump(data, n)}", flush=True)
            print(f"    side-effects: {pr.summary()}", flush=True)
        return data, is_err, pr


def server_params(root, which, extra_env=None):
    """把 .mcp.json 里的 Windows 路径翻译成本机路径（command 换成本机 venv 解释器）。"""
    cfg = json.load(open(ROOT / ".mcp.json", encoding="utf-8"))["mcpServers"][which]
    tr = lambda s: s.replace(WIN_PREFIX, str(root))  # noqa: E731
    env = {k: tr(v) for k, v in (cfg.get("env") or {}).items()}
    env.update(extra_env or {})
    args = [tr(a) for a in cfg.get("args", [])]
    return StdioServerParameters(command=PY, args=args, cwd=str(root), env=env), cfg


@contextlib.asynccontextmanager
async def open_server(stack_name, root, which, db, extra_env=None, errlog_name=None):
    params, _ = server_params(root, which, extra_env)
    errlog = open(SCRATCH / (errlog_name or f"{stack_name}.stderr"), "w", encoding="utf-8")
    async with stdio_client(params, errlog=errlog) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            yield Srv(stack_name, s, root, db)
    errlog.close()


async def wait_task(http, task_id, timeout=180):
    """轮询异步任务（campaign 节点 detached 执行）直到终态。"""
    t0 = time.time()
    while time.time() - t0 < timeout:
        st, _, _ = await http.call("workflow_task_status", quiet=True, task_id=task_id, tail_lines=12)
        # 返回形态 {found, task: {task_id, status ∈ running/succeeded/failed/unknown, stdout_tail, ...}}
        task = st.get("task") if isinstance(st, dict) and isinstance(st.get("task"), dict) else {}
        if task.get("status") not in (None, "running"):
            return task
        await asyncio.sleep(1.0)
    return {"status": "timeout"}


def sh(argv, env_extra=None, cwd=None, tail=30, root=ROOT, db=None, env_drop=()):
    env = {k: v for k, v in os.environ.items() if k not in env_drop}
    env.update(env_extra or {})
    with Probe(root, db or (Path(root) / "data" / "wqb.db")) as pr:
        p = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=env, cwd=str(cwd or root), timeout=900)
    lines = (p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr.strip() else "")).rstrip().splitlines()
    print("$ " + " ".join(rel(a) for a in argv), flush=True)
    for ln in (lines[-tail:] if tail else []):
        print("  | " + rel(ln)[:240])
    print(f"  => exit={p.returncode} | {pr.summary()}", flush=True)
    return p, pr


def q(db, sql, *p):
    c = sqlite3.connect(str(db))
    try:
        return c.execute(sql, p).fetchall()
    finally:
        c.close()


def node_out(x):
    """workflow_* 工具返回 {success, node, params, output:{...节点结果...}, error}；取节点结果本体。"""
    if isinstance(x, dict) and isinstance(x.get("output"), dict):
        return x["output"]
    return x if isinstance(x, dict) else {}


def step_of(x, name):
    return next((s for s in node_out(x).get("steps", []) if isinstance(s, dict) and s.get("step") == name), None)


def snapshot(db):
    rows = q(db, "SELECT value, updated_at FROM ledger_kv WHERE region=? AND key='priors_snapshot_kor'", R)
    return (json.loads(rows[0][0]), rows[0][1]) if rows else (None, None)


# ----------------------------------------------------------------------------- 真实历史 → MCP 导入
_ALPHA_ID = re.compile(r"^[A-Za-z0-9]{7,8}$")


def _dataset_of(d):
    ds = d.get("dataset") if d.get("dataset") is not None else d.get("datasets")
    if isinstance(ds, list):
        ds = ds[0] if ds else None
    if isinstance(ds, dict):
        return "_mixed"
    m = re.match(r"\s*([a-z][a-z0-9_]*)", str(ds or ""))
    return m.group(1) if m else "_unknown"


def _rows_of(d):
    rows = d.get("results") or d.get("candidates") or (d.get("verdicts") if isinstance(d.get("verdicts"), list) else None) or []
    if isinstance(rows, dict):
        rows = list(rows.values())
    out = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        aid = r.get("alpha_id") or r.get("alpha") or (r.get("id") if _ALPHA_ID.match(str(r.get("id") or "")) else None)
        row = {
            "alpha_id": aid,
            "expression": r.get("expr") or r.get("expression") or r.get("code"),
            "sharpe": r.get("sharpe"),
            "fitness": r.get("fitness"),
            "turnover": r.get("turnover") if r.get("turnover") is not None else r.get("tvr"),
            "two_year_sharpe": r.get("two_year_sharpe") if r.get("two_year_sharpe") is not None else r.get("two_year"),
            "sub_universe_sharpe": r.get("sub_universe_sharpe") if r.get("sub_universe_sharpe") is not None else r.get("sub"),
            "row_verdict": r.get("verdict"),
            "note": r.get("note") or r.get("reason"),
        }
        out.append({k: v for k, v in row.items() if v is not None})
    return out


def _wave_key(path):
    m = re.search(r"wave(\w+?)_(?:results|batch_result)", os.path.basename(path))
    return m.group(1) if m else os.path.basename(path)


def _wave_sort(path):
    m = re.search(r"wave(\d+)", os.path.basename(path))
    return (int(m.group(1)) if m else 0, os.path.basename(path))


async def import_history(db_srv, root):
    files = sorted(glob.glob(str(root / "tracking" / R / "candidates" / "wave*_result*.json")), key=_wave_sort)
    stats = {"files": len(files), "rows_in": 0, "rows_written": 0, "rows_no_expr": 0, "verdict": {}}
    table = []
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        wave, ds = _wave_key(f), _dataset_of(d)
        rows = _rows_of(d)
        with_expr = [r for r in rows if r.get("expression")]
        stats["rows_in"] += len(rows)
        stats["rows_no_expr"] += len(rows) - len(with_expr)
        if with_expr:
            got, err, _ = await db_srv.call("upsert_backtest_rows", quiet=True, region=R, wave=wave, rows=with_expr, dataset=ds)
            stats["rows_written"] += (got or {}).get("n", 0) if isinstance(got, dict) else 0
        raw_v = d.get("verdict")
        if raw_v is None:
            outcome = "无 verdict → 不写 wave_results"
        else:
            findings = [str(x) for x in (d.get("key_insight"), d.get("conclusion")) if x][:2]
            got, err, _ = await db_srv.call(
                "upsert_wave_result", quiet=True, region=R, wave_number=wave, verdict=str(raw_v),
                focus=str(d.get("focus") or d.get("tag") or ds)[:200], key_findings=findings,
                source_file=rel(f))
            if isinstance(got, dict) and got.get("action"):
                outcome = f"closed/{got.get('verdict')}"
            else:
                # 契约拒绝（无法归一）→ 按导入策略以 open 状态落库（open 波不参与停止规则 B），原文进 key_findings
                got2, _, _ = await db_srv.call(
                    "upsert_wave_result", quiet=True, region=R, wave_number=wave, status="open",
                    focus=str(d.get("focus") or d.get("tag") or ds)[:200],
                    key_findings=[f"原 verdict（未能归一，导入为 open）: {raw_v}"] + findings, source_file=rel(f))
                outcome = "REJECTED→open" if isinstance(got2, dict) and got2.get("action") else f"REJECTED ({dump(got2, 80)})"
            # 让 updated_at 严格递增（停止规则 B 按 datetime(updated_at) 秒级排序取"最近 3 个"）
            await asyncio.sleep(1.05)
        stats["verdict"][outcome.split(" ")[0].split("/")[0]] = stats["verdict"].get(outcome.split(" ")[0].split("/")[0], 0) + 1
        table.append((os.path.basename(f), wave, ds, len(rows), len(with_expr), str(raw_v)[:46], outcome))
    return stats, table


def verdict_coverage(root):
    """真实历史 verdict 原文：写入契约（MCP 实际用的）vs 迁移工具 classify（带人工复核的一次性工具）。"""
    for sub in ("src", "tools"):
        if str(root / sub) not in sys.path:
            sys.path.insert(0, str(root / sub))
    from wqb.wave_results_contract import normalize_verdict
    from migrate_wave_verdict_enum import classify
    rows = []
    for f in sorted(glob.glob(str(root / "tracking" / R / "candidates" / "wave*_result*.json")), key=_wave_sort):
        v = json.load(open(f, encoding="utf-8")).get("verdict")
        if v is None:
            continue
        c_enum, c_rule = classify(str(v))
        rows.append((_wave_key(f), str(v), normalize_verdict(v)[0], c_enum, c_rule))
    return rows


async def import_kb(db_srv, root):
    """用最近一次组装产物 tracking/KOR/priors/kor_priors.json 反推 DB 侧 KB（region_kb + registry_empirical）。"""
    pri = json.load(open(root / "tracking" / R / "priors" / "kor_priors.json", encoding="utf-8"))
    ctx = pri.get("region_context") or {}
    kb = {
        "win_recipes": [{"name": w["id"], "key": w.get("key", ""), "evidence": w.get("evidence", "")}
                        for w in pri["wins"] if w.get("source") == "region_kb"],
        "tier": ctx.get("tier"), "settings_proven": ctx.get("settings_proven"),
        "notes": ctx.get("key_notes") or ctx.get("notes") or [],
        "dead_patterns": [],
    }
    out = {"region_kb": await db_srv.call("upsert_ledger_key", quiet=True, region=R, key="region_kb", value=kb)}
    n_win = n_dead = 0
    for w in pri["wins"]:
        if w.get("source") == "registry_win":
            eid = re.sub(r"[^A-Z0-9]+", "-", (w.get("evidence", "").split("；")[0].split(" ")[-1] or w["id"]).upper())[:60] or f"KOR-WIN-{n_win}"
            await db_srv.call("upsert_registry_empirical", quiet=True, region=R, layer="win", entry_id=eid,
                              payload={"id": w["id"], "what": w.get("what"), "key": w.get("key"), "evidence": w.get("evidence")})
            n_win += 1
    for de in pri["dead_ends"]:
        if de.get("source") == "registry_dead_end":
            await db_srv.call("upsert_registry_empirical", quiet=True, region=R, layer="dead_end",
                              entry_id=de.get("_entry_id") or f"KOR-DEAD-{n_dead}", family=de.get("family"),
                              payload={"family": de.get("family"), "reason": de.get("reason"), "salvage": de.get("salvage")})
            n_dead += 1
    skipped = [w["id"] for w in pri["wins"] if w.get("source") not in ("region_kb", "registry_win")]
    return pri, {"region_kb_win_recipes": len(kb["win_recipes"]), "registry_win": n_win, "registry_dead_end": n_dead,
                 "未反推（源为 template_kb，结构不可逆）": skipped}


def load_catalog(ds):
    p = ROOT / "tracking" / R / "reference" / f"kor_{ds}_fields.json"
    d = json.load(open(p, encoding="utf-8"))
    return d, p


# ----------------------------------------------------------------------------- P0 回放（修复后 / 修复前各跑一遍）
def _gate_line(x):
    o = node_out(x)
    sr = step_of(x, "stop_rules_gate") or {}
    return (f"success={o.get('success')}  stop_rules: success={sr.get('success')} hits={sr.get('hits')} "
            f"verdicts={((sr.get('evidence') or {}).get('recent_closed_verdicts'))} warning={dump(sr.get('warning'), 90) if sr.get('warning') else None}")


async def run_assemble(http, stage, label):
    """真跑 assemble-priors（campaign 节点异步任务）并等终态；返回 (节点输出, 任务终态)。"""
    res, _, _ = await http.call("workflow_campaign", label=label, region=R, stage=stage, subcommand="assemble-priors",
                                dry_run=False, n=300)
    o = node_out(res)
    st = await wait_task(http, o["task_id"]) if o.get("task_id") else {}
    if st:
        print(f"    任务终态: {dump({k: st.get(k) for k in ('status', 'returncode', 'error')}, 200)}")
        print(f"    stdout_tail: {dump(rel(str(st.get('stdout_tail') or '')), 420)}")
        if st.get("returncode"):
            print(f"    stderr_tail: {dump(rel(str(st.get('stderr_tail') or '')), 420)}")
    return o, st


async def p0_replay(tag, db_srv, http, root, db, wave_fail):
    H2(f"[{tag}] P0-1 ① 字符串波号 s2_{DS}_d1 经 MCP 写 verdict（SKILL 步 4/9 的波号形态）")
    await db_srv.call("upsert_wave_result", region=R, wave_number=f"s2_{DS}_d1", verdict="FAIL", key_findings=["probe"], n=300)
    await db_srv.call("get_wave_result", region=R, wave_number=f"s2_{DS}_d1", n=300)
    H2(f"[{tag}] P0-1 ② 停止规则 B：真实历史下最近 3 个 closed 波 → 下一波 S2（build_wave）干跑")
    g, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage="S2", dataset=DS, wave="p0_next", dry_run=True)
    print("    " + _gate_line(g))
    H2(f"[{tag}] P0-1 ③ 按步 9 只补写点塔进度到 key_findings（不带 verdict）—— wave {wave_fail}")
    await db_srv.call("upsert_wave_result", region=R, wave_number=wave_fail,
                      key_findings=["[pyramid] ANALYST 2/3 · MODEL 1/3（步 9 点塔进度）"], n=300)
    print("    行现状:", q(db, "SELECT wave_number, verdict, status, substr(key_findings,1,60) FROM wave_results "
                         "WHERE region=? AND wave_number=?", R, str(wave_fail)))
    g2, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage="S2", dataset=DS, wave="p0_next", dry_run=True)
    print("    同一下一波 S2 干跑: " + _gate_line(g2))
    H2(f"[{tag}] P0-1 ④ 新波只写 key_findings（缺 verdict、默认 closed）")
    await db_srv.call("upsert_wave_result", region=R, wave_number="p0_hollow", key_findings=["探针全灭"], n=300)
    print("    p0_hollow 行:", q(db, "SELECT wave_number, verdict, status FROM wave_results WHERE region=? AND wave_number='p0_hollow'", R))

    # P0-2：两次回放都从"无快照"起步（演练脚本直接删键，对称对照）
    c = sqlite3.connect(str(db))
    c.execute("DELETE FROM ledger_kv WHERE region=? AND key IN ('priors_snapshot_kor', 'assemble_priors_cache_KOR')", (R,))
    c.commit()
    c.close()
    H2(f"[{tag}] P0-2 ① assemble-priors 干跑命令：SKILL ra-pipeline 步 4 写法 stage=S2 / gem SKILL 写法 stage=S6（均带 dataset/wave）")
    for stage in ("S2", "S6"):
        x, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage=stage, subcommand="assemble-priors",
                                  dataset=DS, wave="p0", dry_run=True)
        bc, va = step_of(x, "build_command"), step_of(x, "validate_argv")
        print(f"    stage={stage}: success={node_out(x).get('success')}  "
              f"cmd尾={' '.join((bc or {}).get('command', '').split()[-4:]) if bc else None}  "
              f"argv错误={dump((va or {}).get('error'), 120) if va else None}  "
              f"拦截={dump(node_out(x).get('error'), 110) if not bc and not va else None}")
    H2(f"[{tag}] P0-2 ② 真跑 assemble-priors（先 SOP 的 S2 写法；被拦则退 S6 写法）")
    o, st = await run_assemble(http, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
    if not o.get("task_id"):
        print(f"    S2 写法未启动：{dump(o.get('error'), 160)}")
        o, st = await run_assemble(http, "S6", "workflow_campaign(S6, assemble-priors, 真跑)")
    sv, ts = snapshot(db)
    print("    DB 快照 priors_snapshot_kor:", f"存在 updated_at={ts} wins={len(sv['wins'])}" if sv else "不存在")
    subprocess.run(["git", "-C", str(root), "checkout", "--", f"tracking/{R}/priors/"], capture_output=True)
    H2(f"[{tag}] P0-2 ③ GEM 干跑（默认 --priors-from-db）：快照状态是否可见")
    gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
    print("    steps:", [s.get("step") for s in node_out(gem).get("steps", [])])
    print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check") or "（无此步）", 400))
    print("    干跑结论:", dump({"success": node_out(gem).get("success"), "error": node_out(gem).get("error")}, 260))


# ============================================================================= 主流程
async def main():
    DB = ROOT / "data" / "wqb.db"
    H1("步 0 · 真实环境基线（服务启动 / 路径翻译 / 全新库）")
    cfg = json.load(open(ROOT / ".mcp.json", encoding="utf-8"))["mcpServers"]
    for name, c in cfg.items():
        print(f"  .mcp.json {name}: command={c['command']}  exists_on_this_host={Path(c['command']).exists()}")
    print(f"  → 本机翻译：command={rel(PY)}（{subprocess.run([PY, '-V'], capture_output=True, text=True).stdout.strip()}），"
          f"路径前缀 {WIN_PREFIX} → <repo>")
    print("  git HEAD:", subprocess.run(["git", "-C", str(ROOT), "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip())
    print("  工作树未提交改动（= 本轮 P0 修复）:", sorted(git_dirty(ROOT)))
    print("  world-quant-brain-mcp/.env 存在?", (ROOT / "world-quant-brain-mcp" / ".env").exists(), "（只判存在，不读取）")
    dirty_priors = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", f"tracking/{R}/priors/"],
                                  capture_output=True, text=True).stdout.strip()
    if dirty_priors:
        sys.exit(f"tracking/{R}/priors/ 有未提交改动（演练会 git checkout 复原该目录）——先提交或暂存：{dirty_priors}")
    if DB.exists() and DB.stat().st_size > 5_000_000 and os.environ.get("REALENV_ALLOW_DB_SWAP") != "1":
        sys.exit(f"{DB} 像是生产库（{DB.stat().st_size} bytes）。演练会把它临时移走、结束后移回；"
                 "确认后设 REALENV_ALLOW_DB_SWAP=1 再跑。")
    if (SCRATCH / "wqb.db.before_realenv").exists():
        sys.exit(f"{rel(SCRATCH)}/wqb.db.before_realenv 已存在（上次演练未正常收尾？）——先把它移回 data/wqb.db 再跑。")
    print("  data/wqb.db 本轮开始前存在?", DB.exists(), "→ 临时移到 scratch，演练结束后移回" if DB.exists() else "")
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB) + suffix)
        if p.exists():
            shutil.move(str(p), str(SCRATCH / (p.name + ".before_realenv")))
    try:
        await _main_body(DB)
    finally:
        for suffix in ("", "-wal", "-shm"):
            cur = Path(str(DB) + suffix)
            if cur.exists():
                shutil.move(str(cur), str(SCRATCH / (cur.name + ".realenv")))
            saved = SCRATCH / (cur.name + ".before_realenv")
            if saved.exists():
                shutil.move(str(saved), str(cur))
        subprocess.run(["git", "-C", str(ROOT), "checkout", "--", f"tracking/{R}/priors/"], capture_output=True)
        print(f"\n[清理] 演练库已移到 {rel(SCRATCH)}/wqb.db.realenv；原 data/wqb.db 已移回；tracking/{R}/priors/ 已复原")


async def _main_body(DB):
    http_env = {"WQB_WORKSPACE": str(ROOT)}
    async with contextlib.AsyncExitStack() as stack:
        db_srv = await stack.enter_async_context(open_server("wqb-db", ROOT, "wqb-db", DB))
        http = await stack.enter_async_context(open_server("wq-brain-http", ROOT, "wq-brain-http", DB, extra_env=http_env))
        for s in (db_srv, http):
            tools = (await s.s.list_tools()).tools
            names = [t.name for t in tools]
            print(f"  [{s.name}] tools={len(tools)}  私有名工具={[n for n in names if n.startswith('_')]}  "
                  f"无 dry_run 参数的 workflow_*={[t.name for t in tools if t.name.startswith('workflow_') and 'dry_run' not in (t.inputSchema or {}).get('properties', {})]}")
        await asyncio.sleep(0.5)
        for name in ("wqb-db", "wq-brain-http"):
            txt = (SCRATCH / f"{name}.stderr").read_text(encoding="utf-8", errors="replace")
            warn = [ln for ln in txt.splitlines() if re.search(r"WARN|不可用|not found|No BRAIN|Error", ln)]
            print(f"  [{name}] 启动 stderr 告警: {dump([rel(w)[:150] for w in warn], 900)}")

        H2("空库首调：先调只读工具（_conn 直连，不建 schema）")
        await db_srv.call("get_campaign_summary", region=R, n=300)
        print("    data/wqb.db 此刻存在?", DB.exists(), " 表数:", len(db_counts(DB)))

        # ------------------------------------------------------------------ 导入
        H1("导入 · tracking/KOR 真实历史 → 经 wqb-db MCP 写工具落库（导入本身即契约实测）")
        stats, table = await import_history(db_srv, ROOT)
        print(f"  {'file':28s} {'wave':8s} {'dataset':16s} rows expr  verdict 原文 → 契约结果")
        for fn, wave, ds, nr, ne, rv, oc in table:
            print(f"  {fn:28s} {wave:8s} {ds[:16]:16s} {nr:>4} {ne:>4}  {rv!r:50s} → {oc}")
        print("  汇总:", dump(stats, 600))
        H2("verdict 原文覆盖率：写入契约 normalize_verdict（MCP 实际使用）vs tools/migrate_wave_verdict_enum.classify")
        cov = verdict_coverage(ROOT)
        for wave, raw, n_enum, c_enum, c_rule in cov:
            print(f"  {wave:6s} 契约={str(n_enum):7s} classify={str(c_enum):7s} ({c_rule[:18]:18s})  {raw[:60]!r}")
        print(f"  可归一：契约 {sum(1 for r in cov if r[2])}/{len(cov)}，classify {sum(1 for r in cov if r[3])}/{len(cov)}")
        pri, kbstat = await import_kb(db_srv, ROOT)
        print("  KB 反推（来自 tracking/KOR/priors/kor_priors.json）:", dump(kbstat, 500))
        for ds_ in (DS, DS2):
            cat, cat_path = load_catalog(ds_)
            got, err, _ = await db_srv.call("upsert_field_catalog", quiet=True, region=R, catalog=cat)
            print(f"  字段目录 {rel(cat_path)} → upsert_field_catalog: isError={err} {dump(got, 300)}")
        print("  库内行数:", dump(db_counts(DB), 700))
        # 导入后快照：附 B 的修复前对照从这里起步（与修复后回放同一份真实历史，不带步 1–9 的演练写入）
        imported = SCRATCH / "wqb.db.imported"
        if imported.exists():
            imported.unlink()
        _s, _d = sqlite3.connect(str(DB)), sqlite3.connect(str(imported))
        _s.backup(_d)
        _d.close()
        _s.close()

        # ------------------------------------------------------------------ 步 1
        H1("步 1 · S-PRE 查表（区域先验 / 库存 / 产出率）")
        await db_srv.call("get_campaign_summary", region=R, n=700)
        await db_srv.call("get_dead_ends", region=R, n=500)
        await db_srv.call("get_mining_yield", region=R, strict=True, n=700)
        await db_srv.call("get_mining_yield", region=R, by_dataset=True, n=900)
        await db_srv.call("get_dead_datasets", region=R, n=400)
        await db_srv.call("list_wave_results", region=R, status="closed", limit=5, n=700)
        await http.call("workflow_execute", label="workflow_execute(inventory_scan, dry_run)", node="inventory_scan",
                        params={"region": R, "target": 20}, dry_run=True, n=600)
        await db_srv.call("workflow_inventory_scan", label="wqb-db workflow_inventory_scan（无 dry_run 参数 → 真跑）",
                          region=R, target=20, n=600)
        await http.call("recommend_datasets", region=R, delay=1, universe="TOP600", top_n=5, n=400)

        # ------------------------------------------------------------------ 步 2
        H1("步 2 · S0 数据集体检 + 白名单")
        await http.call("workflow_campaign", region=R, stage="S0", calibrate=True, dry_run=True, n=800)
        await http.call("workflow_campaign", region=R, stage="S0", dry_run=True, n=800)
        H2("开波前区域四闸（toolkit _lib/region_gates，warn 模式；真实 tracking/KOR）")
        sh([PY, "-c", "import sys,json; sys.path.insert(0,'.'); from _lib import region_gates as rg; "
                      f"r=rg.run_region_gates(r'{ROOT / 'tracking' / R}', '{R}', mode='warn', dataset='{DS}'); "
                      "print('RESULT', json.dumps({'ok': r.get('ok'), 'skipped_reason': r.get('skipped_reason'), "
                      "'results': {n: {k: v for k, v in (x or {}).items() if k in ('success','hits','error','warning')} "
                      "for n, x in (r.get('results') or {}).items()}}, ensure_ascii=False)[:1400])"],
           cwd=ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts", env_extra={"WQB_WORKSPACE": str(ROOT)}, tail=8)

        # ------------------------------------------------------------------ 步 3
        H1(f"步 3 · S1 字段扫描 + 理解（dataset={DS}，真实字段目录）")
        await http.call("workflow_campaign", region=R, stage="S1", dataset=DS, dry_run=True, n=700)
        await http.call("workflow_feature_engineering", region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True, n=700)
        await db_srv.call("get_field_catalog", region=R, dataset=DS, n=400)
        await db_srv.call("build_field_prefix_clusters", region=R, dataset=DS, n=700)
        await http.call("workflow_execute", label="workflow_execute(field_understanding, dry_run)", node="field_understanding",
                        params={"region": R, "dataset": DS}, dry_run=True, n=500)
        await db_srv.call("workflow_field_understanding", label="wqb-db workflow_field_understanding（真跑）",
                          region=R, dataset=DS, n=700)

        # ------------------------------------------------------------------ 步 4
        H1("步 4 · S2 概念优先生成（priors 快照闭环 → GEM → 预闸）")
        H2("4.0 修复前节点在带 dataset/wave 调用时拼出的 argv —— 静态 validate_argv 放行，实跑呢？（--print 不写文件）")
        sh([PY, str(ROOT / "Claude/skills/wq-brain-campaign-toolkit/scripts/campaign.py"), "--campaign-dir",
            str(ROOT / "tracking" / R), "assemble-priors", "--dataset", DS, "--wave", "w_next", "--print"],
           env_extra={"WQB_WORKSPACE": str(ROOT)}, cwd=ROOT / "Claude/skills/wq-brain-campaign-toolkit/scripts", tail=3)
        H2("4.1 assemble-priors 在 .mcp.json 原样 env（不含 WQB_WORKSPACE）下真跑 —— 本机路径可移植性")
        async with open_server("wq-brain-http(.mcp.json 原样 env)", ROOT, "wq-brain-http", DB,
                               errlog_name="wq-brain-http.nows.stderr") as http_plain:
            await run_assemble(http_plain, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
        sv, ts = snapshot(DB)
        print("    DB 快照:", f"存在 updated_at={ts}" if sv else "不存在")
        subprocess.run(["git", "-C", str(ROOT), "checkout", "--", f"tracking/{R}/priors/"], capture_output=True)
        c = sqlite3.connect(str(DB))
        c.execute("DELETE FROM ledger_kv WHERE region=? AND key IN ('priors_snapshot_kor', 'assemble_priors_cache_KOR')", (R,))
        c.commit()
        c.close()
        H2("4.2 GEM 干跑 —— 快照缺失时")
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    steps:", [s.get("step") for s in node_out(gem).get("steps", [])])
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 400))
        print("    干跑结论:", dump({"success": node_out(gem).get("success"), "error": node_out(gem).get("error")}, 300))
        H2("4.3 assemble-priors 真跑（WQB_WORKSPACE=<repo>，等价于用户本机 D:\\ 默认路径恰好正确的情形；KOR 此刻命中停止规则 B）")
        await run_assemble(http, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
        sv, ts = snapshot(DB)
        if sv:
            print(f"    快照 updated_at={ts} wins={len(sv['wins'])} dead_ends={len(sv['dead_ends'])} sha256={str(sv.get('sha256', ''))[:16]}…")
            tracked = {w["id"] for w in pri["wins"]}
            print(f"    与仓库已入库 priors 对照：wins 重合 {len(tracked & {w['id'] for w in sv['wins']})}/{len(tracked)}，"
                  f"dead_ends {len(sv['dead_ends'])}/{len(pri['dead_ends'])}")
        else:
            print("    DB 快照: 不存在")
        diff = subprocess.run(["git", "-C", str(ROOT), "diff", "--stat", "--", f"tracking/{R}/priors/"],
                              capture_output=True, text=True).stdout.strip()
        print("    被重写的已入库文件:", diff or "无")
        H2("4.4 GEM 干跑 —— 快照新鲜")
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 300))
        H2("4.5 模拟 S6 回写：region_kb 追加一条新 win（经 MCP upsert_ledger_key）→ GEM 干跑应提示过期")
        await asyncio.sleep(1.1)
        kb_now, _, _ = await db_srv.call("get_ledger_key", quiet=True, region=R, key="region_kb")
        kb_val = dict(kb_now) if isinstance(kb_now, dict) and "error" not in kb_now else {}
        kb_val.setdefault("win_recipes", []).append({"name": "realenv-demo 新 win（S6 回写）", "key": "rank(ts_delta(x, 22))",
                                                     "evidence": "dry-run 演示条目"})
        await db_srv.call("upsert_ledger_key", region=R, key="region_kb", value=kb_val, n=200)
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 500))
        H2("4.5b 模拟 S6 判死封存（registry dead_end，S6 最常见的回写）：wave97 真实结论 model219 判死")
        await asyncio.sleep(1.1)
        await db_srv.call("seal_dead_end", region=R, entry_id="KOR-MODEL219-DEAD", family="model219 盈余质量/前瞻估值族",
                          reason="wave97 0/6：model219 盈余质量/前瞻估值族不入 book（真实 verdict 原文）", wave_numbers=[97], n=300)
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 600))
        H2("4.6 按告警重组快照 → GEM 干跑恢复安静；新 win / 新 dead_end 是否进快照")
        await run_assemble(http, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 300))
        sv, ts = snapshot(DB)
        print("    快照含新 win?", bool(sv) and any("realenv-demo" in str(w.get("id", "")) for w in sv["wins"]))
        n_dead = q(DB, "SELECT COUNT(*) FROM registry_empirical WHERE region=? AND layer='dead_end'", R)[0][0]
        snap_dead = [d.get("_entry_id") for d in (sv or {}).get("dead_ends", [])]
        print(f"    registry dead_end {n_dead} 条 → 快照 dead_ends {len(snap_dead)} 条（MAX_DEADENDS=12，按 entry_id 字母序截断）；"
              f"新封存的 KOR-MODEL219-DEAD 进快照? {'KOR-MODEL219-DEAD' in snap_dead}；快照末条={snap_dead[-1:]}")
        subprocess.run(["git", "-C", str(ROOT), "checkout", "--", f"tracking/{R}/priors/"], capture_output=True)
        H2("4.7 GEM 干跑止步于 check_config / gem_wave 干跑")
        cc = step_of(gem, "check_config") or {}
        print("    check_config:", dump({k: cc.get(k) for k in ("success", "error")}, 300))
        await http.call("workflow_execute", label="workflow_execute(gem_wave, dry_run)", node="gem_wave",
                        params={"region": R, "dataset_id": DS, "delay": 1, "universe": "TOP600"}, dry_run=True, n=500)
        H2("4.8 生成侧预闸 pipeline_pregate（真实历史表达式：wave91 / 91b / 91c / 94 的 ml_factor_proj 候选）")
        real_exprs = [e for (e,) in q(DB, "SELECT DISTINCT expression FROM expressions WHERE region=? AND dataset=? LIMIT 40", R, DS)]
        ef_all = SCRATCH / "realenv_mlfp_exprs.txt"
        ef_all.write_text("\n".join(real_exprs) + "\n", encoding="utf-8")
        pregate_dir = ROOT / "Claude" / "skills" / "brain-make-some-gem" / "scripts" / "trailSomeAlphas"
        sh([PY, "-c", "import sys; sys.path.insert(0,'.'); import pipeline_pregate as pg; "
                      f"ex=[l.strip() for l in open(r'{ef_all}',encoding='utf-8') if l.strip()]; logs=[]; "
                      f"k=pg.pregate(list(ex), log=lambda *a: logs.append(' '.join(map(str,a))), region='{R}'); "
                      "print('in', len(ex), 'kept', len(k) if isinstance(k, list) else k); [print('log', l[:180]) for l in logs[:14]]"],
           cwd=pregate_dir, tail=18)

        # ------------------------------------------------------------------ 步 5
        H1("步 5 · S2→S3 门禁（ghost-audit → wave_gate：语法/8 闸/体检硬门/多样性）")
        print(f"  候选 = 库内 {DS} 真实历史表达式 {len(real_exprs)} 条（{rel(ef_all)}）")
        sh([PY, str(ROOT / "tools" / "campaign_intel.py"), "ghost-audit", "--region", R, "--exprs-file", str(ef_all)], tail=10)
        await http.call("workflow_execute", label="workflow_execute(wave_gate, dry_run)", node="wave_gate",
                        params={"region": R, "dataset": DS, "wave": "g1", "exprs_file": str(ef_all), "from_db": False}, dry_run=True, n=600)
        await db_srv.call("workflow_unified_gate", label="wqb-db workflow_unified_gate（真跑；wqb-db 的 env 无 WQ_TOOLKIT_DIR）",
                          region=R, dataset=DS, wave="g1", exprs_file=str(ef_all), from_db=False, n=900)
        gate_env = {k: v for k, v in (http_env | {"WQ_TOOLKIT_DIR": str(ROOT / "Claude/skills/wq-brain-campaign-toolkit/scripts"),
                                                  "WQ_VALIDATOR_DIR": str(ROOT / "Claude/skills/alpha-expression-verifier/scripts")}).items()}
        H2("tools/wave_gate.py 真跑 ①：env = .mcp.json 的 wq-brain-http（有 WQ_TOOLKIT_DIR/WQ_VALIDATOR_DIR，无 WQB_ROOT）")
        before = dict(q(DB, "SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status", R))
        sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--campaign-dir", str(ROOT / "tracking" / R), "--dataset", DS,
            "--wave", "g2", "--exprs-file", str(ef_all)], env_extra=gate_env, tail=8,
           env_drop=("WQB_ROOT", "WQ_PROJECT_ROOT"))
        after = dict(q(DB, "SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status", R))
        print(f"  真库 expressions 状态分布 前={before} 后={after}")
        # 只认"仓库根下名字字面就是 D:\\coding\\...\\wqb 的子目录"（仅 POSIX 可能出现）。
        # 切勿写成 `ROOT / "D:\\…"`：Windows 上右侧是绝对路径，拼出来就是仓库本身。
        stray_name = WIN_PREFIX.replace("/", "\\")
        stray = ROOT / stray_name
        if os.name != "nt" and stray_name in os.listdir(ROOT) and stray.resolve().parent == ROOT:
            sdb = stray / "data" / "wqb.db"
            rows = q(sdb, "SELECT wave, status, COUNT(*) FROM expressions GROUP BY wave, status") if sdb.exists() else []
            print(f"  ★ 仓库根下出现杂散目录 {rel(stray)!r}（git 视其为 ignored：`git status` 看不见）；其中库 expressions={rows}")
            shutil.rmtree(stray)
            print("    已删除（演练自身造成的污染）")
        H2("tools/wave_gate.py 真跑 ②：补 WQB_ROOT=<repo>（等价用户本机 D:\\ 默认恰好正确）")
        H2("  ②a 只声明 --dataset（漏声明跨数据集 mix 的第二腿 multi_source_model）")
        gpa, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--campaign-dir", str(ROOT / "tracking" / R), "--dataset", DS,
                     "--wave", "g3a", "--exprs-file", str(ef_all)], env_extra=gate_env | {"WQB_ROOT": str(ROOT)}, tail=0)
        print("  | " + next((ln for ln in gpa.stdout.splitlines() if ln.startswith("[done ]")), "?")[:230])
        print("  | " + next((ln for ln in gpa.stdout.splitlines() if "静态闸 1-5 拦截" in ln), "（无静态闸拦截行）")[:230])
        H2("  ②b 补声明 --datasets 重跑（agent 看到 FIELD 失败后的自然动作；走默认缓存）")
        gpb, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--campaign-dir", str(ROOT / "tracking" / R), "--dataset", DS,
                     "--datasets", DS2, "--wave", "g3b", "--exprs-file", str(ef_all)],
                    env_extra=gate_env | {"WQB_ROOT": str(ROOT)}, tail=0)
        print("  | " + next((ln for ln in gpb.stdout.splitlines() if ln.startswith("[done ]")), "?")[:230])
        rb = q(DB, "SELECT report_json FROM gate_results WHERE region=? AND wave='g3b'", R)
        if rb:
            gb = json.loads(rb[0][0]).get("gate") or {}
            print(f"  | gate.cached={gb.get('cached')} / total={gb.get('total')}（缓存键 = sha1(主 dataset + 表达式)，不含 --datasets）")
        H2("  ②c 声明 --datasets 且 --no-cache —— 两腿白名单的真实判定；以下为完整门禁输出")
        gp, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--campaign-dir", str(ROOT / "tracking" / R), "--dataset", DS,
                    "--datasets", DS2, "--no-cache", "--wave", "g3", "--exprs-file", str(ef_all)],
                   env_extra=gate_env | {"WQB_ROOT": str(ROOT)}, tail=0)
        glines = gp.stdout.splitlines()
        keep = [ln for ln in glines if not re.match(r"\[syntax\] \d+: PASS|\[qp +\] \w+ \d+:", ln) and ln.strip()]
        print("  （省略逐条 [syntax] PASS 与逐条 [qp] 行，见下方汇总表）")
        for ln in keep[-45:]:
            print("  | " + rel(ln)[:230])
        print("  真库 expressions 状态分布:", dict(q(DB, "SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status", R)))
        H2("门禁逐条结论 × 真实回测（同一批 39 条的历史实测：闸拦下的是不是好信号？）")
        for wv in ("g3a", "g3b", "g3"):
            rj = q(DB, "SELECT report_json FROM gate_results WHERE region=? AND wave=?", R, wv)
            if not rj:
                print(f"  {wv}: 无 gate_results")
                continue
            items = (json.loads(rj[0][0]).get("gate") or {}).get("report") or []
            exprs_g = [ln.strip() for ln in ef_all.read_text(encoding="utf-8").splitlines() if ln.strip()]
            blk, ok = [], []
            tags = {}
            for it in items:
                e = exprs_g[it["index"] - 1]
                s = q(DB, "SELECT MAX(sharpe) FROM backtest_results WHERE region=? AND code=?", R, e)[0][0]
                (ok if it.get("pass") else blk).append(s)
                for iss in it.get("issues") or []:
                    m = re.match(r"\[([\w-]+)\]", iss)
                    tags[m.group(1) if m else iss[:20]] = tags.get(m.group(1) if m else iss[:20], 0) + 1
            mean = lambda xs: round(sum(x for x in xs if x is not None) / max(1, len([x for x in xs if x is not None])), 2)  # noqa: E731
            print(f"  {wv}: 放行 {len(ok)} 条（实测 sharpe 均值 {mean(ok)}，最高 {max([x for x in ok if x is not None] or [None])}）；"
                  f"拦截 {len(blk)} 条（均值 {mean(blk)}，最高 {max([x for x in blk if x is not None] or [None])}）；拦截理由 {tags}")
        H2("质量预估 vs 真实回测（同一批 39 条的历史实测；判断预估闸的校准度）")
        exprs_in = [ln.strip() for ln in ef_all.read_text(encoding="utf-8").splitlines() if ln.strip()]
        pred = {}
        for ln in glines:
            m = re.match(r"\[qp +\] (\w+) (\d+): 预估Sharpe ([\d.]+).*?预估Fitness ([\d.]+)", ln)
            if m:
                pred[int(m.group(2))] = (m.group(1), float(m.group(3)), float(m.group(4)))
        rows_cmp = []
        for i, e in enumerate(exprs_in, 1):
            act = q(DB, "SELECT MAX(sharpe), MAX(fitness), GROUP_CONCAT(DISTINCT alpha_id) FROM backtest_results "
                        "WHERE region=? AND code=?", R, e)[0]
            if i in pred and act[0] is not None:
                rows_cmp.append((i, pred[i], act))
        real_pass = [r for r in rows_cmp if r[2][0] > 1.58 and (r[2][1] or 0) >= 1.0]
        print(f"  可对照 {len(rows_cmp)} 条；实测过廉价闸（S>1.58 & F>=1.0）{len(real_pass)} 条，其预估标签："
              f"{[(r[0], r[1][0], r[1][1], r[2][0], r[2][2]) for r in real_pass]}")
        if rows_cmp:
            import statistics
            ps = [r[1][1] for r in rows_cmp]
            acts = [r[2][0] for r in rows_cmp]
            try:
                corr = statistics.correlation(ps, acts)
            except Exception:
                corr = None
            print(f"  预估 sharpe 区间 [{min(ps):.2f}, {max(ps):.2f}]，实测 sharpe 区间 [{min(acts):.2f}, {max(acts):.2f}]，"
                  f"预估↔实测 Pearson = {corr if corr is None else round(corr, 3)}")
        print("  gate_results:", q(DB, "SELECT region, wave, dataset, all_pass FROM gate_results"))
        await http.call("operator_audit", expressions=real_exprs[:6], region=R, delay=1, universe="TOP600", n=600)
        await http.call("validate_expressions", alpha_expressions=real_exprs[:3], region=R, universe="TOP600", delay=1, n=400)

        # ------------------------------------------------------------------ 步 6
        H1("步 6 · S3 七槽回测（前置三闸 on 真实历史）")
        await http.call("workflow_batch_track", region=R, wave="g2", dataset=DS, dry_run=True, n=600)
        await http.call("workflow_campaign", region=R, stage="S3", dataset=DS, wave="g2", dry_run=True, n=1400)

        # ------------------------------------------------------------------ 步 7
        H1("步 7 · S4 诊断改进（真实回测行上的墙诊断 / salvage）")
        await http.call("workflow_campaign", region=R, stage="S4", dataset=DS, wave="94", dry_run=True, n=700)
        await db_srv.call("list_alphas_by_wave", region=R, wave_number="94", n=500)
        await db_srv.call("search_alphas_by_sharpe", region=R, min_sharpe=1.2, limit=8, n=900)
        await db_srv.call("backfill_salvage_pool_batch", region=R, candidates_dir=str(ROOT / "tracking" / R / "candidates"), n=700)
        await db_srv.call("get_salvage_pool", region=R, n=500)
        await http.call("workflow_execute", label="workflow_execute(auto_review, dry_run)", node="auto_review",
                        params={"region": R, "wave": "94", "dataset": DS}, dry_run=True, n=500)
        H2("review_wave 判定（真实 thresholds.json × 真实回测行，wave 91/91b/91c/94 sharpe 前 6）")
        sh([PY, "-c", "import sys,json,sqlite3; sys.path.insert(0,'.'); import review_wave as rw; "
                      f"t=json.load(open(r'{ROOT / 'tracking' / R / 'config' / 'thresholds.json'}',encoding='utf-8')); "
                      "tr=t['review']; tn=dict(t.get('near') or {}); "
                      f"c=sqlite3.connect(r'{DB}'); "
                      "rows=c.execute(\"SELECT alpha_id,wave,sharpe,fitness,two_year_sharpe,sub_universe_sharpe,turnover FROM backtest_results "
                      f"WHERE region='{R}' AND wave IN ('91','91b','91c','94') ORDER BY sharpe DESC LIMIT 6\").fetchall(); "
                      "[print(a,w,'S=%s F=%s 2Y=%s sub=%s'%(s,f,y,sb),'passes=',rw.passes({'sharpe':s,'fitness':f,'two_year_sharpe':y,"
                      "'sub_universe_sharpe':sb,'turnover_pct':(tv or 0)*100,'margin_bp':None,'failed_checks':[]},tr),"
                      "'walls=',rw.walls({'sharpe':s,'fitness':f,'two_year_sharpe':y,'sub_universe_sharpe':sb,'turnover_pct':(tv or 0)*100,"
                      "'margin_bp':None,'failed_checks':[]},tr)) for a,w,s,f,y,sb,tv in rows]"],
           cwd=ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts", tail=10)

        # ------------------------------------------------------------------ 步 8
        H1("步 8 · S4→S5 稳健闸与提交判定")
        await db_srv.call("get_submit_ready", region=R, n=600)
        await http.call("submit_verdict", alpha_id="88lr21xo", n=500)
        await http.call("workflow_judge", alpha_id="88lr21xo", dry_run=True, n=500)
        await http.call("workflow_submit_alpha", label="workflow_submit_alpha（未确认，干跑）", alpha_id="78jQ29rL", dry_run=True, n=500)
        await http.call("workflow_submit_alpha", label="workflow_submit_alpha（confirm_submit=True，干跑）", alpha_id="78jQ29rL",
                        confirm_submit=True, dry_run=True, n=500)

        # ------------------------------------------------------------------ 步 9
        H1("步 9 · S6 复盘回写（P0-1 契约 on 真实历史 + 停止闸闭环）")
        closed = q(DB, "SELECT wave_number, verdict FROM wave_results WHERE region=? AND status='closed' "
                       "ORDER BY datetime(COALESCE(updated_at, created_at)) DESC LIMIT 3", R)
        print("  最近 3 个 closed 波（停止规则 B 的输入）:", closed)
        wave_fail = closed[0][0] if closed else "97"
        await p0_replay("修复后", db_srv, http, ROOT, DB, wave_fail)
        H2("残留：规则 B 的窗口按 updated_at 取 —— 按拒绝提示把 91c（'✅ 2 RA 提交成功'，导入时被拒→open）补记为 PASS")
        await db_srv.call("upsert_wave_result", region=R, wave_number="91c", verdict="PASS",
                          key_findings=["补记：2 RA 提交成功（88lr21xo + A1lb2KpR ACTIVE）"], n=260)
        print("  最近 3 个 closed 波（按 updated_at）:", q(DB, "SELECT wave_number, verdict FROM wave_results WHERE region=? AND "
                                                "status='closed' ORDER BY datetime(COALESCE(updated_at, created_at)) DESC LIMIT 3", R))
        g3, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage="S2", dataset=DS, wave="p0_next", dry_run=True)
        print("  下一波 S2 干跑: " + _gate_line(g3))
        H2("S6 其余动作")
        sh([PY, str(ROOT / "tools" / "step_funnel.py"), "--region", R], env_extra={"WQB_DB_PATH": str(DB)}, tail=25)
        await http.call("workflow_execute", label="workflow_execute(auto_pyramid, dry_run)", node="auto_pyramid",
                        params={"region": R, "wave": wave_fail}, dry_run=True, n=400)

        H1("附 A · 19 个 workflow 节点经 MCP workflow_execute(dry_run=True) 全量扫描（仓库 _DRY_RUN_CASES 参数）")
        import ast
        src_t = (ROOT / "tests" / "unit" / "test_skill_integrity.py").read_text(encoding="utf-8")
        cases = {}
        for node in ast.parse(src_t).body:
            if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "_DRY_RUN_CASES" for t in node.targets):
                cases = eval(compile(ast.Expression(node.value), "cases", "eval"), {})
        print(f"  {'node':24s} {'ok':6s} side-effects / error")
        for node, params in sorted(cases.items()):
            out, err, pr = await http.call("workflow_execute", quiet=True, node=node, params=params, dry_run=True)
            ok = out.get("success") if isinstance(out, dict) else None
            e = (out.get("error") if isinstance(out, dict) else str(out)) or ""
            print(f"  {node:24s} {str(ok):6s} {pr.summary()[:150]}  {dump(rel(str(e)), 110) if e else ''}")
        print("  wq-brain-http workflow_list_nodes:", dump((await http.call("workflow_list_nodes", quiet=True))[0], 200))

    # ---------------------------------------------------------------------- 修复前对照
    if BASE_DIR:
        H1("附 B · 修复前对照：导入后快照（同一份真实历史）复制到 git archive 原始副本，起修复前的两个 server 重放 P0 序列")
        bdb = BASE_DIR / "data" / "wqb.db"
        bdb.parent.mkdir(exist_ok=True)
        for suffix in ("", "-wal", "-shm"):
            if Path(str(bdb) + suffix).exists():
                Path(str(bdb) + suffix).unlink()
        # 用"导入后快照"起步：同一份真实历史，不带步 1–9 的演练写入（门禁重跑留下的 gated、91c 补记等）
        src_c = sqlite3.connect(str(SCRATCH / "wqb.db.imported"))
        dst = sqlite3.connect(str(bdb))
        src_c.backup(dst)
        src_c.close()
        dst.close()
        print("  base 库:", rel(bdb), dump(db_counts(bdb), 300))
        async with contextlib.AsyncExitStack() as stack:
            bdb_srv = await stack.enter_async_context(open_server("base:wqb-db", BASE_DIR, "wqb-db", bdb,
                                                                  errlog_name="base.wqb-db.stderr"))
            bhttp = await stack.enter_async_context(open_server("base:wq-brain-http", BASE_DIR, "wq-brain-http", bdb,
                                                                extra_env={"WQB_WORKSPACE": str(BASE_DIR)},
                                                                errlog_name="base.wq-brain-http.stderr"))
            closed = q(bdb, "SELECT wave_number, verdict FROM wave_results WHERE region=? AND status='closed' "
                            "ORDER BY datetime(COALESCE(updated_at, created_at)) DESC LIMIT 3", R)
            print("  base 最近 3 个 closed 波:", closed)
            await p0_replay("修复前", bdb_srv, bhttp, BASE_DIR, bdb, closed[0][0] if closed else "97")

    print("\n[REAL-ENV DRY-RUN END]")
    print("  仓库已入库文件是否被改动（应只剩本轮 P0 修复 + 报告）:", sorted(git_dirty(ROOT)))


if __name__ == "__main__":
    asyncio.run(main())
