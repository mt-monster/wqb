# -*- coding: utf-8 -*-
"""RA 九步流水线 · 真实环境 dry-run（2026-09-27；第四轮 = P0 + P1 两批（R18–R21 / R22·R5·R12·R4·R3）修复之后）

每一步末尾打印【阶段小结】：输入 / 处理 / 输出变化 / 价值判定。其中的数字全部取自本次运行的
实际输出；判定栏的星级沿用报告 §1 的评判口径，并随本次数据给出结论（与预期不符时如实打印）。

对照关系：
  * P0 修复前后 → 附 B（BASE_DIR = 修复前原始副本，默认 d1c7d78）；
  * P1 第一批（R18–R21）修复前后 → 与同目录 realenv_transcript_p0.txt（P0 修复后、P1 修复前的第二轮实录）
    同名步骤逐行对照；本脚本对 P1 相关探针的步骤编号与第二轮保持一致（4.1 / 4.6 / 5 ①②③ / 导入表）；
  * P1 第二批（R22 / R5 / R12 / R4 / R3）修复前后 → 与同目录 realenv_transcript_r18_r21.txt（第三轮实录）
    的步 5–9 / 附 A 对照；新增探针：5 ④⑤⑥（R12）、6（R5）、7 R4、8 R3、9 窗口（R22）。
  * 两个 MCP server 与所有子进程的 env = .mcp.json 原样（第二轮主 server 需补 WQB_WORKSPACE 才能跑通
    assemble-priors，即 N19(b)；R19 后不再补——这本身就是 R19 的验证）。

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


def STAGE(title, inputs, process, outputs, verdict):
    """阶段小结：输入 / 处理 / 输出变化 / 价值判定（数字取自本次运行）。"""
    print(f"\n  ┌─ 【阶段小结 · {title}】", flush=True)
    for tag, text in (("输入", inputs), ("处理", process), ("输出变化", outputs)):
        print(f"  │ {tag}：{text}")
    print(f"  └ 价值判定：{verdict}", flush=True)


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


#: 工作区根 / 库路径类变量。演练 shell 自身若带着它们会掩盖 R19 的路径解析——子进程一律剔除，
#: 需要时再由 env_extra 显式给出（本轮不给：子进程 env = .mcp.json 原样）。
_ROOT_VARS = ("WQB_ROOT", "WQ_PROJECT_ROOT", "WQB_WORKSPACE", "WQB_DB_PATH")


def mcp_env(which):
    """.mcp.json 里该 server 的 env 原样（Windows 路径翻译成本机）。"""
    cfg = json.load(open(ROOT / ".mcp.json", encoding="utf-8"))["mcpServers"][which]
    return {k: v.replace(WIN_PREFIX, str(ROOT)) for k, v in (cfg.get("env") or {}).items()}


def sh(argv, env_extra=None, cwd=None, tail=30, root=ROOT, db=None, env_drop=_ROOT_VARS):
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


def snap_state(gem):
    """GEM 干跑 priors_snapshot_check 的三态：缺失 / 过期(源) / 新鲜。"""
    sc = step_of(gem, "priors_snapshot_check") or {}
    if not sc:
        return "无检查步"
    if sc.get("stale_sources"):
        return "过期(" + "+".join(s.split("@")[0].split("/", 1)[-1] for s in sc["stale_sources"]) + ")"
    return "缺失" if sc.get("warning") else "新鲜"


def line_of(text, pat):
    return next((ln for ln in (text or "").splitlines() if re.search(pat, ln)), "")


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
    stats = {"files": len(files), "rows_in": 0, "rows_written": 0, "rows_no_expr": 0, "verdict": {}, "suggestion": {}}
    table, suggestions = [], {}
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
        sug = None
        if raw_v is None:
            outcome_key = outcome = "无 verdict → 不写 wave_results"
        else:
            findings = [str(x) for x in (d.get("key_insight"), d.get("conclusion")) if x][:2]
            got, err, _ = await db_srv.call(
                "upsert_wave_result", quiet=True, region=R, wave_number=wave, verdict=str(raw_v),
                focus=str(d.get("focus") or d.get("tag") or ds)[:200], key_findings=findings,
                source_file=rel(f))
            if isinstance(got, dict) and got.get("action"):
                outcome_key, outcome = "closed", f"closed/{got.get('verdict')}"
            else:
                # 契约拒绝（无法归一）→ 按导入策略以 open 状态落库（open 波不参与停止规则 B），原文进 key_findings。
                # R20：拒绝信息附判定表建议（只展示、不自动采用——与契约一致）
                sug = got.get("suggestion") if isinstance(got, dict) else None
                got2, _, _ = await db_srv.call(
                    "upsert_wave_result", quiet=True, region=R, wave_number=wave, status="open",
                    focus=str(d.get("focus") or d.get("tag") or ds)[:200],
                    key_findings=[f"原 verdict（未能归一，导入为 open）: {raw_v}"] + findings, source_file=rel(f))
                ok2 = isinstance(got2, dict) and got2.get("action")
                outcome_key = "REJECTED→open" if ok2 else "REJECTED"
                outcome = outcome_key if ok2 else f"REJECTED ({dump(got2, 80)})"
                if sug:
                    outcome += f"（建议 {sug['verdict']}/{sug['confidence']}）"
                    suggestions[wave] = sug
                    k = f"{sug['verdict']}/{sug['confidence']}"
                    stats["suggestion"][k] = stats["suggestion"].get(k, 0) + 1
                else:
                    stats["suggestion"]["无建议"] = stats["suggestion"].get("无建议", 0) + 1
            # 让 updated_at 严格递增（停止规则 B 按 datetime(updated_at) 秒级排序取"最近 3 个"）
            await asyncio.sleep(1.05)
        stats["verdict"][outcome_key.split(" ")[0]] = stats["verdict"].get(outcome_key.split(" ")[0], 0) + 1
        table.append((os.path.basename(f), wave, ds, len(rows), len(with_expr), str(raw_v)[:46], outcome))
    return stats, table, suggestions


def verdict_coverage(root):
    """真实历史 verdict 原文：写入契约（MCP 实际用的）vs 迁移工具 classify（带人工复核的一次性工具）。"""
    for sub in ("src", "tools"):
        if str(root / sub) not in sys.path:
            sys.path.insert(0, str(root / sub))
    from wqb.wave_results_contract import normalize_verdict, suggest_verdict
    from migrate_wave_verdict_enum import classify
    rows = []
    for f in sorted(glob.glob(str(root / "tracking" / R / "candidates" / "wave*_result*.json")), key=_wave_sort):
        v = json.load(open(f, encoding="utf-8")).get("verdict")
        if v is None:
            continue
        c_enum, c_rule = classify(str(v))
        n_enum = normalize_verdict(v)[0]
        sug = suggest_verdict(v) if n_enum is None else None   # 契约只在拒绝时给建议（R20）
        rows.append((_wave_key(f), str(v), n_enum, c_enum, c_rule, sug))
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
    await db_srv.call("upsert_ledger_key", quiet=True, region=R, key="region_kb", value=kb)
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


# ----------------------------------------------------------------------------- P1 第二批探针（子进程脚本）
#: R4：仓库里全部带 rn_sharpe 的真实评审行（review_wave 自己的行格式；KOR 历史没有 rn 字段），按各区
#: thresholds 判 near / 组合候选（二者合起来就是 salvage 池的来源）。"修复前" = 同一行去掉 rn_sharpe：
#: R4 之前 rn_exposure 只进 passes()/walls()，near 池与 combo_candidate 看不到它。
R4_PROBE = r'''
import glob, json, os, sys
sys.path.insert(0, os.getcwd())          # cwd = toolkit scripts/（脚本本身在 SCRATCH）
import review_wave as rw

root = sys.argv[1]


def rows_of(o):
    if isinstance(o, dict):
        if "rn_sharpe" in o and o.get("sharpe") is not None:
            yield o
        for v in o.values():
            yield from rows_of(v)
    elif isinstance(o, list):
        for v in o:
            yield from rows_of(v)


out, seen = {}, {}
for f in sorted(glob.glob(os.path.join(root, "tracking", "*", "reviews", "*.json"))):
    reg = f.replace("\\", "/").split("/")[-3]
    tf = os.path.join(root, "tracking", reg, "config", "thresholds.json")
    if not os.path.isfile(tf):
        continue
    th = json.load(open(tf, encoding="utf-8"))
    t, tn = th["review"], th["near"]
    try:
        data = json.load(open(f, encoding="utf-8"))
    except ValueError:
        continue
    s = out.setdefault(reg, {"rows": 0, "rn_exposure": 0, "rn_max_sharpe": None, "near_min": tn["sharpe_min"],
                             "combo_min": t.get("combo_sharpe_min", 1.0), "near_old": 0, "near_new": 0,
                             "combo_old": 0, "combo_new": 0, "excluded": 0, "leak": 0, "examples": []})
    for r in rows_of(data):
        key = str(r.get("id") or r.get("alpha_id") or json.dumps(r, sort_keys=True))
        if key in seen.setdefault(reg, set()):
            continue
        seen[reg].add(key)
        s["rows"] += 1
        rn = rw.rn_exposure(r, t)
        s["rn_exposure"] += rn
        if rn:
            s["rn_max_sharpe"] = max(r["sharpe"], s["rn_max_sharpe"] if s["rn_max_sharpe"] is not None else r["sharpe"])
        if rw.passes(r, t):
            continue
        old = dict(r, rn_sharpe=None)
        near_old = rw.is_near(old, tn)
        near_new = rw.is_near(r, tn) and rw.near_block_wall(r, t, tn) is None     # = review_wave.main 的 near 循环
        combo_old, combo_new = rw.combo_candidate(old, t), rw.combo_candidate(r, t)
        s["near_old"] += near_old
        s["near_new"] += near_new
        s["combo_old"] += combo_old
        s["combo_new"] += combo_new
        if (near_old or combo_old) and not (near_new or combo_new):
            s["excluded"] += 1
            if len(s["examples"]) < 3:
                s["examples"].append([key, r.get("sharpe"), r.get("rn_sharpe")])
        if (near_new or combo_new) and rn:
            s["leak"] += 1
print("R4JSON " + json.dumps(out, ensure_ascii=False))
'''

#: R3：mcp_core 的失败计数到底用哪份实现。repo = 仓库布局；docker = 屏蔽整个 wqb 包（镜像只打包
#: world-quant-brain-mcp/、没有 src/），走冻结副本。同一组 N3 checks 两种布局必须同数，且等于 wqb.config。
R3_PROBE = r'''
import json, os, sys
sys.path.insert(0, os.getcwd())          # cwd = world-quant-brain-mcp/（脚本本身在 SCRATCH）
mode = sys.argv[1]
if mode == "docker":
    sys.modules["wqb"] = None
import mcp_core as m
N3 = [{"name": "LOW_2Y_SHARPE", "result": "WARNING", "value": 0.9, "limit": 1.0},
      {"name": "IS_LADDER_SHARPE", "result": "WARNING", "value": 1.1, "limit": 1.2},
      {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "FAIL", "value": 0.4, "limit": 0.6}]
_, _, _, ra = m._slim_checks(N3)
res = {"mode": mode, "source": getattr(m, "FAILED_COUNT_SOURCE", "（无此属性：修复前）"),
       "failed_ra": ra["failed_ra_count"], "failed_ppa": ra["failed_ppa_count"], "ra_failed": ra.get("ra_failed_checks")}
if mode == "repo":
    from wqb.config import compute_webdata_failed_counts
    c = compute_webdata_failed_counts(N3)
    res["wqb_config"] = {"failed_ra": c["failed_ra"], "failed_ppa": c["failed_ppa"]}
print("R3JSON " + json.dumps(res, ensure_ascii=False))
'''


def run_probe(name, code, args, cwd, marker, env_extra=None):
    """把探针脚本写到 SCRATCH 再执行（打印同 sh()）；返回 (进程, 解析出的 JSON 或 None)。"""
    path = SCRATCH / f"{name}.py"
    path.write_text(code, encoding="utf-8")
    p, _ = sh([PY, str(path)] + [str(a) for a in args], env_extra=env_extra, cwd=cwd, tail=4)
    line = line_of(p.stdout, "^" + marker + " ")
    return p, (json.loads(line[len(marker) + 1:]) if line else None)


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


def _rule_b(x):
    sr = step_of(x, "stop_rules_gate") or {}
    ev = sr.get("evidence") or {}
    return {"S2_success": node_out(x).get("success"), "rule_B_blocks": sr.get("success") is False,
            "window": ev.get("recent_closed_verdicts"),
            "waves": ev.get("recent_closed_waves")}   # R22 起闸自己报窗口里是哪几个波（修复前的代码无此字段）


async def p0_replay(tag, db_srv, http, root, db, wave_fail):
    """返回关键结论（供阶段小结 / 附 B 对照），打印逐条实录。"""
    res = {}
    H2(f"[{tag}] P0-1 ① 字符串波号 s2_{DS}_d1 经 MCP 写 verdict（SKILL 步 4/9 的波号形态）")
    w1, e1, _ = await db_srv.call("upsert_wave_result", region=R, wave_number=f"s2_{DS}_d1", verdict="FAIL",
                                  key_findings=["probe"], n=300)
    await db_srv.call("get_wave_result", region=R, wave_number=f"s2_{DS}_d1", n=300)
    res["str_wave"] = "参数校验拒绝" if e1 else (w1.get("action") if isinstance(w1, dict) else str(w1)[:40])
    H2(f"[{tag}] P0-1 ② 停止规则 B：真实历史下最近 3 个 closed 波 → 下一波 S2（build_wave）干跑")
    g, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage="S2", dataset=DS, wave="p0_next", dry_run=True)
    print("    " + _gate_line(g))
    res["before_update"] = _rule_b(g)
    H2(f"[{tag}] P0-1 ③ 按步 9 只补写点塔进度到 key_findings（不带 verdict）—— wave {wave_fail}")
    await db_srv.call("upsert_wave_result", region=R, wave_number=wave_fail,
                      key_findings=["[pyramid] ANALYST 2/3 · MODEL 1/3（步 9 点塔进度）"], n=300)
    row = q(db, "SELECT wave_number, verdict, status, substr(key_findings,1,60) FROM wave_results "
                "WHERE region=? AND wave_number=?", R, str(wave_fail))
    print("    行现状:", row)
    res["verdict_after_kf_only"] = row[0][1] if row else None
    g2, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage="S2", dataset=DS, wave="p0_next", dry_run=True)
    print("    同一下一波 S2 干跑: " + _gate_line(g2))
    res["after_update"] = _rule_b(g2)
    H2(f"[{tag}] P0-1 ④ 新波只写 key_findings（缺 verdict、默认 closed）")
    hw, he, _ = await db_srv.call("upsert_wave_result", region=R, wave_number="p0_hollow", key_findings=["探针全灭"], n=300)
    hollow = q(db, "SELECT wave_number, verdict, status FROM wave_results WHERE region=? AND wave_number='p0_hollow'", R)
    print("    p0_hollow 行:", hollow)
    res["hollow"] = ("参数校验拒绝" if he else "契约拒绝" if isinstance(hw, dict) and hw.get("error") else "写入") + \
                    f"，行={hollow}"

    # P0-2：两次回放都从"无快照"起步（演练脚本直接删键，对称对照）
    c = sqlite3.connect(str(db))
    c.execute("DELETE FROM ledger_kv WHERE region=? AND key IN ('priors_snapshot_kor', 'assemble_priors_cache_KOR')", (R,))
    c.commit()
    c.close()
    H2(f"[{tag}] P0-2 ① assemble-priors 干跑命令：SKILL ra-pipeline 步 4 写法 stage=S2 / gem SKILL 写法 stage=S6（均带 dataset/wave）")
    tails = {}
    for stage in ("S2", "S6"):
        x, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage=stage, subcommand="assemble-priors",
                                  dataset=DS, wave="p0", dry_run=True)
        bc, va = step_of(x, "build_command"), step_of(x, "validate_argv")
        tails[stage] = ' '.join((bc or {}).get('command', '').split()[-2:]) if bc else None
        print(f"    stage={stage}: success={node_out(x).get('success')}  "
              f"cmd尾={' '.join((bc or {}).get('command', '').split()[-4:]) if bc else None}  "
              f"argv错误={dump((va or {}).get('error'), 120) if va else None}  "
              f"拦截={dump(node_out(x).get('error'), 110) if not bc and not va else None}")
    res["assemble_cmd_tail"] = tails
    H2(f"[{tag}] P0-2 ② 真跑 assemble-priors（先 SOP 的 S2 写法；被拦则退 S6 写法）")
    o, st = await run_assemble(http, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
    if not o.get("task_id"):
        print(f"    S2 写法未启动：{dump(o.get('error'), 160)}")
        o, st = await run_assemble(http, "S6", "workflow_campaign(S6, assemble-priors, 真跑)")
    sv, ts = snapshot(db)
    print("    DB 快照 priors_snapshot_kor:", f"存在 updated_at={ts} wins={len(sv['wins'])}" if sv else "不存在")
    res["assemble_rc"], res["snapshot"] = st.get("returncode"), bool(sv)
    subprocess.run(["git", "-C", str(root), "checkout", "--", f"tracking/{R}/priors/"], capture_output=True)
    H2(f"[{tag}] P0-2 ③ GEM 干跑（默认 --priors-from-db）：快照状态是否可见")
    gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
    print("    steps:", [s.get("step") for s in node_out(gem).get("steps", [])])
    print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check") or "（无此步）", 400))
    print("    干跑结论:", dump({"success": node_out(gem).get("success"), "error": node_out(gem).get("error")}, 260))
    res["gem_snapshot_check"] = step_of(gem, "priors_snapshot_check") is not None
    return res


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
    print("  工作树未提交改动（= 本轮 P1 第二批修复 R22 / R5 / R12 / R4 / R3）:", sorted(git_dirty(ROOT)))
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
    HTTP_ENV = mcp_env("wq-brain-http")   # .mcp.json 原样：MCP_TRANSPORT / WQB_ASI_UNIVERSE_FIX / WQ_TOOLKIT_DIR / WQ_VALIDATOR_DIR
    TOOLKIT = ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
    CAMPAIGN = ROOT / "tracking" / R
    V = {}                                 # 本次运行的关键结论：阶段小结 + 末尾 P1 验证清单
    async with contextlib.AsyncExitStack() as stack:
        # 两个 server 的 env 都是 .mcp.json 原样（第二轮主 server 另补了 WQB_WORKSPACE，本轮不补）
        db_srv = await stack.enter_async_context(open_server("wqb-db", ROOT, "wqb-db", DB))
        http = await stack.enter_async_context(open_server("wq-brain-http", ROOT, "wq-brain-http", DB))
        n_tools, n_warn = {}, {}
        for s in (db_srv, http):
            tools = (await s.s.list_tools()).tools
            names = [t.name for t in tools]
            n_tools[s.name] = len(tools)
            print(f"  [{s.name}] tools={len(tools)}  私有名工具={[n for n in names if n.startswith('_')]}  "
                  f"无 dry_run 参数的 workflow_*={[t.name for t in tools if t.name.startswith('workflow_') and 'dry_run' not in (t.inputSchema or {}).get('properties', {})]}")
        await asyncio.sleep(0.5)
        for name in ("wqb-db", "wq-brain-http"):
            txt = (SCRATCH / f"{name}.stderr").read_text(encoding="utf-8", errors="replace")
            warn = [ln for ln in txt.splitlines() if re.search(r"WARN|不可用|not found|No BRAIN|Error", ln)]
            n_warn[name] = len(warn)
            print(f"  [{name}] 启动 stderr 告警: {dump([rel(w)[:150] for w in warn], 900)}")

        H2("空库首调：先调只读工具（_conn 直连，不建 schema）")
        first, first_err, _ = await db_srv.call("get_campaign_summary", region=R, n=300)
        n_tab0 = len(db_counts(DB))
        print("    data/wqb.db 此刻存在?", DB.exists(), " 表数:", n_tab0)
        STAGE("步 0 · 真实环境基线（演练前提，不是 SOP 步骤）",
              ".mcp.json 的两个 server（command 是 Windows 绝对路径）；仓库工作树；默认库路径 data/wqb.db 为空",
              "路径翻译成本机后经 stdio 启动两个 server（env = .mcp.json 原样，不补任何根目录变量）；列工具；读启动 stderr；空库上先调只读工具",
              f"wqb-db {n_tools.get('wqb-db')} 个工具 / wq-brain-http {n_tools.get('wq-brain-http')} 个；启动告警 {sum(n_warn.values())} 条；"
              f"空库首调 isError={first_err}（{dump(first, 70)}），默认路径留下 {n_tab0} 表的空库文件",
              "环境事实，不评星。N23（.mcp.json 不可移植）/ N24（工具面）/ N26（空库首调即建空库）仍在，属 P2，不在本轮范围")

        # ------------------------------------------------------------------ 导入
        H1("导入 · tracking/KOR 真实历史 → 经 wqb-db MCP 写工具落库（导入本身即契约实测）")
        stats, table, SUGG = await import_history(db_srv, ROOT)
        print(f"  {'file':28s} {'wave':8s} {'dataset':16s} rows expr  verdict 原文 → 契约结果（R20：被拒时附判定表建议，不自动采用）")
        for fn, wave, ds, nr, ne, rv, oc in table:
            print(f"  {fn:28s} {wave:8s} {ds[:16]:16s} {nr:>4} {ne:>4}  {rv!r:50s} → {oc}")
        print("  汇总:", dump(stats, 700))
        H2("verdict 原文覆盖率：写入契约 normalize_verdict + 被拒时的判定表建议 suggest_verdict（R20） vs 迁移工具 classify")
        cov = verdict_coverage(ROOT)
        for wave, raw, n_enum, c_enum, c_rule, sug in cov:
            s = f"{sug['verdict']}/{sug['confidence']}" if sug else "-"
            print(f"  {wave:6s} 契约={str(n_enum):7s} 建议={s:14s} classify={str(c_enum):7s} ({c_rule[:16]:16s})  {raw[:56]!r}")
        n_norm = sum(1 for r in cov if r[2])
        n_rej = len(cov) - n_norm
        n_sug = sum(1 for r in cov if r[5])
        by_conf = {}
        for r in cov:
            if r[5]:
                by_conf[r[5]["confidence"]] = by_conf.get(r[5]["confidence"], 0) + 1
        disagree = [(r[0], r[5]["verdict"], r[3]) for r in cov if r[5] and r[3] and r[5]["verdict"] != r[3]]
        print(f"  可归一：契约 {n_norm}/{len(cov)}；被拒 {n_rej} 条中附建议 {n_sug} 条 {by_conf}；"
              f"classify {sum(1 for r in cov if r[3])}/{len(cov)}")
        print(f"  建议与 classify 都给出结论但不一致（wave, 建议, classify）：{disagree}")
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
        V["R20"] = {"rejected": n_rej, "with_suggestion": n_sug, "by_conf": by_conf, "91c": SUGG.get("91c")}
        STAGE("导入（演练前提；同时是 P0-1 写入契约 + R20 在真实写法上的实测）",
              f"{stats['files']} 个 wave*_result*.json（{stats['rows_in']} 行逐 alpha 指标、{len(cov)} 条波级 verdict 原文）；"
              f"priors/kor_priors.json；字段目录 {DS} / {DS2}",
              "upsert_backtest_rows 逐行入库；verdict 走 upsert_wave_result（契约）——被拒则按导入策略以 open 落库（open 不进规则 B）；"
              "KB 反推 region_kb + registry",
              f"入库 {stats['rows_written']}/{stats['rows_in']} 行（{stats['rows_no_expr']} 行在历史文件里本就没有表达式）；"
              f"verdict {dump(stats['verdict'], 120)}；被拒时的建议 {dump(stats['suggestion'], 160)}",
              f"契约仍保守：{n_norm}/{len(cov)} 条可直接归一，其余拒绝、不写 closed。R20 后被拒的 {n_rej} 条中 {n_sug} 条附判定表建议"
              f" {by_conf}，与 classify 分歧 {len(disagree)} 条。★★★ 保留：拒绝 + 建议 = 不替人猜结论，也不让人卡在'该写什么'")

        # ------------------------------------------------------------------ 步 1
        H1("步 1 · S-PRE 查表（区域先验 / 库存 / 产出率）")
        summ, _, _ = await db_srv.call("get_campaign_summary", region=R, n=700)
        await db_srv.call("get_dead_ends", region=R, n=500)
        y_all, _, _ = await db_srv.call("get_mining_yield", region=R, strict=True, n=700)
        y_ds, _, _ = await db_srv.call("get_mining_yield", region=R, by_dataset=True, n=900)
        await db_srv.call("get_dead_datasets", region=R, n=400)
        await db_srv.call("list_wave_results", region=R, status="closed", limit=5, n=700)
        await http.call("workflow_execute", label="workflow_execute(inventory_scan, dry_run)", node="inventory_scan",
                        params={"region": R, "target": 20}, dry_run=True, n=600)
        inv, _, _ = await db_srv.call("workflow_inventory_scan", label="wqb-db workflow_inventory_scan（无 dry_run 参数 → 真跑）",
                                      region=R, target=20, n=600)
        rec, _, _ = await http.call("recommend_datasets", region=R, delay=1, universe="TOP600", top_n=5, n=400)
        tot = y_all.get("totals", {}) if isinstance(y_all, dict) else {}
        producing = [(r.get("dataset"), f"{r.get('ra_clean')}/{r.get('backtested')}") for r in
                     (y_ds.get("rows", []) if isinstance(y_ds, dict) else []) if r.get("ra_clean")]
        zero_ds = sum(1 for r in (y_ds.get("rows", []) if isinstance(y_ds, dict) else []) if not r.get("ra_clean"))
        sw = summ.get("waves", {}) if isinstance(summ, dict) else {}
        STAGE("步 1 · S-PRE 查表",
              "导入后的 KOR 库（wave_results / backtest_results / registry）；references/regions/KOR.md（profile，本演练不读）",
              "get_campaign_summary / get_dead_ends / get_mining_yield(strict, by_dataset) / get_dead_datasets / list_wave_results；"
              "inventory_scan（干跑 + wqb-db 真跑）；recommend_datasets（平台）",
              f"严格 yield {tot.get('ra_clean')}/{tot.get('backtested')} = {tot.get('yield_rate')}；按数据集有产出的只有 {producing}，"
              f"其余 {zero_ds} 个为 0；summary 波 {sw.get('total')} / closed {sw.get('closed')} / dead_ends {summ.get('dead_ends') if isinstance(summ, dict) else None}；"
              f"inventory_scan 真跑 success={node_out(inv).get('success')}；recommend_datasets → {dump(rec, 60)}",
              "★★★ 保留深化：按数据集的 yield 一步指出唯一产出集（与 wave91c 的 2 条 ACTIVE 吻合），S0 选集应直接引用它；"
              "inventory_scan 节点未入 SOP（N13）、wqb-db 同名工具没有 dry_run（N24）；平台类查询无凭据时 fail-closed")

        # ------------------------------------------------------------------ 步 2
        H1("步 2 · S0 数据集体检 + 白名单")
        s0c, _, _ = await http.call("workflow_campaign", region=R, stage="S0", calibrate=True, dry_run=True, n=800)
        s0s, _, _ = await http.call("workflow_campaign", region=R, stage="S0", dry_run=True, n=800)
        H2("开波前区域四闸（toolkit _lib/region_gates，warn 模式；真实 tracking/KOR；env 不带任何根目录变量）")
        prg, _ = sh([PY, "-c", "import sys,json; sys.path.insert(0,'.'); from _lib import region_gates as rg; "
                              f"r=rg.run_region_gates(r'{CAMPAIGN}', '{R}', mode='warn', dataset='{DS}'); "
                              "print('RESULT', json.dumps({'ok': r.get('ok'), 'gates': {n: (x or {}).get('success') "
                              "for n, x in (r.get('results') or {}).items()}, 'hits': {n: (x or {}).get('hits') "
                              "for n, x in (r.get('results') or {}).items() if (x or {}).get('hits')}, "
                              "'cli_default': list(rg.resolve_mode(None)) if hasattr(rg, 'resolve_mode') else None}, "
                              "ensure_ascii=False))"],
                    cwd=TOOLKIT, tail=8)
        try:
            rg_res = json.loads(line_of(prg.stdout, r"^RESULT ").split(" ", 1)[1])
        except Exception:
            rg_res = {}
        cli_default = rg_res.get("cli_default") or ["?", "toolkit 缺 resolve_mode"]
        print(f"  CLI 入口（build_wave / wave_gate）不带 --gate-mode 时：{cli_default[0]}（{cli_default[1]}）")
        STAGE("步 2 · S0 数据集体检 + 白名单",
              "战役目录 tracking/KOR（settings / thresholds）；库（s0_whitelist 等 ledger、wave_results、expressions）",
              "S0 calibrate / score 命令构建（干跑；真跑要调平台）；toolkit region_gates 四闸（catalog / signal_floor / stop_rules / backlog，warn 模式）",
              f"命令构建 success={node_out(s0c).get('success')}/{node_out(s0s).get('success')}；四闸 {rg_res.get('gates')}，命中 {rg_res.get('hits')}；"
              f"warn 模式下 ok={rg_res.get('ok')}；CLI 缺省 gate-mode={cli_default[0]}",
              "★★★ 保留深化：停止规则 B 在真实历史上命中 95/96/97 连续判死，与团队事后结论一致；"
              f"toolkit CLI 侧缺省 {cli_default[0]}（{cli_default[1]}；R5 收尾）；SOP 的 workflow 入口"
              "（campaign S2/S3、batch_track）一律 enforce（R5，见步 6）；S0 的平台打分部分本环境不可演练")

        # ------------------------------------------------------------------ 步 3
        H1(f"步 3 · S1 字段扫描 + 理解（dataset={DS}，真实字段目录）")
        s1, _, _ = await http.call("workflow_campaign", region=R, stage="S1", dataset=DS, dry_run=True, n=700)
        await http.call("workflow_feature_engineering", region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True, n=700)
        cat3, _, _ = await db_srv.call("get_field_catalog", region=R, dataset=DS, n=400)
        clu, _, _ = await db_srv.call("build_field_prefix_clusters", region=R, dataset=DS, n=700)
        await http.call("workflow_execute", label="workflow_execute(field_understanding, dry_run)", node="field_understanding",
                        params={"region": R, "dataset": DS}, dry_run=True, n=500)
        fu, _, _ = await db_srv.call("workflow_field_understanding", label="wqb-db workflow_field_understanding（真跑）",
                                     region=R, dataset=DS, n=700)
        cat3 = cat3 if isinstance(cat3, dict) else {}
        clu = clu if isinstance(clu, dict) else {}
        STAGE("步 3 · S1 字段扫描 + 理解",
              f"字段目录 {DS}（{cat3.get('field_count')} 字段，经导入入库）",
              "S1 scan_fields 命令构建（干跑）；FE 干跑；typed catalog 读取；前缀聚类；field_understanding（干跑 + wqb-db 真跑）",
              f"S1 success={node_out(s1).get('success')}；类型分布 {cat3.get('type_distribution')}；前缀簇 {clu.get('total_clusters')} 个 "
              f"{[(c.get('prefix'), c.get('count')) for c in (clu.get('top_clusters') or [])[:3]]}；"
              f"field_understanding 真跑 → {dump(node_out(fu).get('error'), 80)}",
              "★★ 保留 typed catalog（闸 2/3/8 与 catalog 前置闸的数据源）；field_understanding 读写不存在的表（N24）→ ✂ 下线候选；"
              "FE 移出主链（§13.4）")

        # ------------------------------------------------------------------ 步 4
        H1("步 4 · S2 概念优先生成（priors 快照闭环 → GEM → 预闸）")
        H2("4.0 修复前节点在带 dataset/wave 调用时拼出的 argv —— 静态 validate_argv 放行，实跑呢？（--print 不写文件）")
        sh([PY, str(TOOLKIT / "campaign.py"), "--campaign-dir", str(CAMPAIGN), "assemble-priors", "--dataset", DS,
            "--wave", "w_next", "--print"], cwd=TOOLKIT, tail=3)
        H2("4.1 assemble-priors 真跑（server 与子进程 env = .mcp.json 原样，不含 WQB_WORKSPACE）—— 第二轮在此崩溃 rc=1（N19b）")
        _, st41 = await run_assemble(http, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
        sv, ts = snapshot(DB)
        print("    DB 快照:", f"存在 updated_at={ts} wins={len(sv['wins'])} dead_ends={len(sv['dead_ends'])}" if sv else "不存在")
        V["4.1"] = {"rc": st41.get("returncode"), "status": st41.get("status"), "snapshot": bool(sv)}
        subprocess.run(["git", "-C", str(ROOT), "checkout", "--", f"tracking/{R}/priors/"], capture_output=True)
        c = sqlite3.connect(str(DB))
        c.execute("DELETE FROM ledger_kv WHERE region=? AND key IN ('priors_snapshot_kor', 'assemble_priors_cache_KOR')", (R,))
        c.commit()
        c.close()
        H2("4.2 GEM 干跑 —— 快照缺失时（演练脚本先删掉 4.1 写的快照）")
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    steps:", [s.get("step") for s in node_out(gem).get("steps", [])])
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 400))
        print("    干跑结论:", dump({"success": node_out(gem).get("success"), "error": node_out(gem).get("error")}, 300))
        states = [snap_state(gem)]
        H2("4.3 assemble-priors 真跑（KOR 此刻命中停止规则 B；assemble-priors 零配额、不开波，按 N16 豁免开波闸）")
        _, st43 = await run_assemble(http, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
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
        states.append(snap_state(gem))
        H2("4.5 模拟 S6 回写：region_kb 追加一条新 win（经 MCP upsert_ledger_key）→ GEM 干跑应提示过期")
        await asyncio.sleep(1.1)
        kb_now, _, _ = await db_srv.call("get_ledger_key", quiet=True, region=R, key="region_kb")
        kb_val = dict(kb_now) if isinstance(kb_now, dict) and "error" not in kb_now else {}
        kb_val.setdefault("win_recipes", []).append({"name": "realenv-demo 新 win（S6 回写）", "key": "rank(ts_delta(x, 22))",
                                                     "evidence": "dry-run 演示条目"})
        await db_srv.call("upsert_ledger_key", region=R, key="region_kb", value=kb_val, n=200)
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 500))
        states.append(snap_state(gem))
        H2("4.5b 模拟 S6 判死封存（registry dead_end，S6 最常见的回写）：wave97 真实结论 model219 判死")
        await asyncio.sleep(1.1)
        await db_srv.call("seal_dead_end", region=R, entry_id="KOR-MODEL219-DEAD", family="model219 盈余质量/前瞻估值族",
                          reason="wave97 0/6：model219 盈余质量/前瞻估值族不入 book（真实 verdict 原文）", wave_numbers=[97], n=300)
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 600))
        states.append(snap_state(gem))
        H2("4.6 按告警重组快照 → GEM 干跑恢复安静；新 win / 新 dead_end 是否进快照（R18：新登记优先 + 截断可见）")
        _, st46 = await run_assemble(http, "S2", "workflow_campaign(S2, assemble-priors, 真跑)")
        gem, _, _ = await http.call("workflow_gem", quiet=True, region=R, dataset_id=DS, delay=1, universe="TOP600", dry_run=True)
        print("    priors_snapshot_check:", dump(step_of(gem, "priors_snapshot_check"), 300))
        states.append(snap_state(gem))
        sv, ts = snapshot(DB)
        new_win = bool(sv) and any("realenv-demo" in str(w.get("id", "")) for w in sv["wins"])
        print("    快照含新 win?", new_win)
        n_dead = q(DB, "SELECT COUNT(*) FROM registry_empirical WHERE region=? AND layer='dead_end'", R)[0][0]
        snap_dead = [d.get("_entry_id") for d in (sv or {}).get("dead_ends", [])]
        trunc = (sv or {}).get("truncated") or {}
        in_snap = "KOR-MODEL219-DEAD" in snap_dead
        print(f"    registry dead_end {n_dead} 条 → 快照 dead_ends {len(snap_dead)} 条（MAX_DEADENDS=12；R18：按登记先后倒序取，"
              f"名额外的记入快照 truncated）")
        pos = snap_dead.index("KOR-MODEL219-DEAD") + 1 if in_snap else None
        print(f"    新封存的 KOR-MODEL219-DEAD 进快照? {in_snap}{f'（第 {pos} 位）' if pos else ''}；快照 truncated = {trunc}")
        print(f"    assemble-priors stdout 的截断提示: {rel(line_of(st46.get('stdout_tail'), r'truncated')) or '（无）'}")
        V["R18"] = {"in_snapshot": in_snap, "registry_dead": n_dead, "snap_dead": len(snap_dead), "truncated": trunc,
                    "new_win": new_win}
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
        ppg, _ = sh([PY, "-c", "import sys; sys.path.insert(0,'.'); import pipeline_pregate as pg; "
                              f"ex=[l.strip() for l in open(r'{ef_all}',encoding='utf-8') if l.strip()]; logs=[]; "
                              f"kept, rep = pg.pregate(list(ex), log=lambda *a: logs.append(' '.join(map(str,a))), region='{R}'); "
                              "print('PREGATE in', len(ex), 'kept', len(kept)); [print('log', l[:180]) for l in logs[:14]]"],
                    cwd=pregate_dir, tail=18)
        mpg = re.search(r"PREGATE in (\d+) kept (\d+)", ppg.stdout)
        pg_io = f"{mpg.group(1)}→{mpg.group(2)}" if mpg else "?"
        n_kb_wins = len((kb_val or {}).get("win_recipes", []))
        n_reg = dict(q(DB, "SELECT layer, COUNT(*) FROM registry_empirical WHERE region=? GROUP BY layer", R))
        STAGE("步 4 · S2 概念优先生成",
              f"DB 侧 KB：region_kb（{n_kb_wins} 条 win_recipes，含 4.5 追加 1 条）+ registry_empirical {n_reg}（含 4.5b 新封存 1 条）"
              f" + KB/template_kb；GEM 默认 --priors-from-db（只读 DB 快照）",
              "assemble-priors 经 campaign 节点真跑 3 次（写 priors 文件 + DB 快照）；GEM 干跑 5 次看快照检查；模拟 S6 回写 region_kb / seal_dead_end；"
              f"pregate 预闸 {len(real_exprs)} 条真实式",
              f"4.1（.mcp.json 原样 env）rc={V['4.1']['rc']}；GEM 快照检查依次 {states}；4.6 快照 wins {len((sv or {}).get('wins', []))} / "
              f"dead_ends {len(snap_dead)}：新 win 进快照={new_win}，KOR-MODEL219-DEAD 进快照={in_snap}，truncated={trunc}；pregate {pg_io}",
              ("★★★ 保留深化：S6→S2 知识回流在真实链路上闭环（P0-2 + N16/N17）" +
               ("；R18 后新判死结论能进 GEM、被截条目可见" if in_snap and trunc else "；⚠ R18 预期未达成（见上）") +
               "；GEM 真跑仍需 headless_runner/config.json（N27：干跑止步 check_config）；pregate 零配额 ★★★"))

        # ------------------------------------------------------------------ 步 5
        H1("步 5 · S2→S3 门禁（ghost-audit → wave_gate：语法/8 闸/体检硬门/多样性）")
        print(f"  候选 = 库内 {DS} 真实历史表达式 {len(real_exprs)} 条（{rel(ef_all)}）")
        pga, _ = sh([PY, str(ROOT / "tools" / "campaign_intel.py"), "ghost-audit", "--region", R, "--exprs-file", str(ef_all)], tail=10)
        await http.call("workflow_execute", label="workflow_execute(wave_gate, dry_run)", node="wave_gate",
                        params={"region": R, "dataset": DS, "wave": "g1", "exprs_file": str(ef_all), "from_db": False}, dry_run=True, n=600)
        await db_srv.call("workflow_unified_gate", label="wqb-db workflow_unified_gate（真跑；wqb-db 的 env 无 WQ_TOOLKIT_DIR）",
                          region=R, dataset=DS, wave="g1", exprs_file=str(ef_all), from_db=False, n=900)

        def gate_json(wv, db=DB):
            rj = q(db, "SELECT report_json FROM gate_results WHERE region=? AND wave=?", R, wv)
            return json.loads(rj[0][0]) if rj else {}

        # 步 5 各次 wave_gate 显式 --gate-mode warn：这里看的是表达式门禁本身；开波闸的拦截在步 2 / 6 / 9 单独演示。
        # 不写的话 2026-10-12（toolkit region_gates.WARN_SUNSET 次日）起缺省 enforce，KOR 命中规则 B，
        # ①–⑤ 会全部停在开波闸，演练不可复现。
        H2("① wave_gate.py 真跑：env = .mcp.json 的 wq-brain-http 原样（无 WQB_ROOT / WQB_WORKSPACE / WQB_DB_PATH）；"
           "只声明 --dataset（漏声明跨集 mix 的第二腿 multi_source_model）")
        print("  （第二轮同一调用：候选被写进仓库根下名为 D:\\coding\\traeCN_project\\wqb 的杂散库，gate.py 读真库找不到候选 → exit 2（N19a））")
        p1, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--gate-mode", "warn", "--campaign-dir", str(CAMPAIGN), "--dataset", DS,
                    "--wave", "g2", "--exprs-file", str(ef_all)], env_extra=HTTP_ENV, tail=0)
        for pat in (r"^\[done \]", r"静态闸 1-5 拦截|^\[gate \] (FAIL|PASS|ERROR)", r"^\[state\]"):
            print("  | " + rel(line_of(p1.stdout, pat) or f"（无匹配 {pat} 的行）")[:230])
        # 只认"仓库根下名字字面就是 D:\\coding\\...\\wqb 的子目录"（仅 POSIX 可能出现）。
        # 切勿写成 `ROOT / "D:\\…"`：Windows 上右侧是绝对路径，拼出来就是仓库本身。
        stray_name = WIN_PREFIX.replace("/", "\\")
        stray = ROOT / stray_name
        stray_found = os.name != "nt" and stray_name in os.listdir(ROOT) and stray.resolve().parent == ROOT
        if stray_found:
            sdb = stray / "data" / "wqb.db"
            rows = q(sdb, "SELECT wave, status, COUNT(*) FROM expressions GROUP BY wave, status") if sdb.exists() else []
            print(f"  ★ 仓库根下出现杂散目录 {rel(stray)!r}（git 视其为 ignored：`git status` 看不见）；其中库 expressions={rows}")
            shutil.rmtree(stray)
            print("    已删除（演练自身造成的污染）")
        else:
            print("  仓库根下无杂散目录（R19：wave_gate 与 toolkit 同一套库路径解析）")
        g2_real = q(DB, "SELECT status, COUNT(*) FROM expressions WHERE region=? AND wave='g2' GROUP BY status", R)
        print(f"  真库 g2 逐条状态: {g2_real}")
        V["R19"] = {"assemble_rc": V["4.1"]["rc"], "gate1_exit": p1.returncode, "stray": stray_found,
                    "g2_in_real_db": sum(n for _, n in g2_real)}

        H2("② 补声明 --datasets 重跑（agent 看到 FIELD 失败后的自然动作；走默认缓存）")
        print("  （第二轮同一调用：gate.cached=39/39，结论不变、仍拦 19 条（N21））")
        p2, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--gate-mode", "warn", "--campaign-dir", str(CAMPAIGN), "--dataset", DS,
                    "--datasets", DS2, "--wave", "g3b", "--exprs-file", str(ef_all)], env_extra=HTTP_ENV, tail=0)
        for pat in (r"^\[done \]", r"^\[state\]"):
            print("  | " + rel(line_of(p2.stdout, pat) or f"（无匹配 {pat} 的行）")[:230])
        gb = gate_json("g3b").get("gate") or {}
        print(f"  | gate.cached={gb.get('cached')} / total={gb.get('total')}（R21：缓存键含闸门签名 = 数据集集合 / 合并白名单 / "
              f"字段类型 / banned / poison / 平台约束）")

        H2("③ --datasets + --no-cache —— 两腿白名单的真实判定（对照组）；以下为完整门禁输出")
        p3, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--gate-mode", "warn", "--campaign-dir", str(CAMPAIGN), "--dataset", DS,
                    "--datasets", DS2, "--no-cache", "--wave", "g3", "--exprs-file", str(ef_all)], env_extra=HTTP_ENV, tail=0)
        glines = p3.stdout.splitlines()
        keep = [ln for ln in glines if not re.match(r"\[syntax\] \d+: PASS|\[qp +\] \w+ \d+:", ln) and ln.strip()]
        print("  （省略逐条 [syntax] PASS 与逐条 [qp] 行，见下方汇总表）")
        for ln in keep[-46:]:
            print("  | " + rel(ln)[:230])
        print("  ③ 逐条回写行: " + (line_of(p3.stdout, r"^\[state\]") or "（无）"))
        dist = q(DB, "SELECT wave, status, COUNT(*) FROM expressions WHERE region=? AND wave IN ('g2','g3b','g3') "
                     "GROUP BY wave, status ORDER BY wave, status", R)
        print("  门禁三波逐条状态（R7/R21 回写）:", dist)
        print("  真库 expressions 状态分布:", dict(q(DB, "SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status", R)))
        # 三次门禁之后的区级积压（积压闸口径：pending+gated / 全部表达式；阈值 30%）
        n_pg, n_all = q(DB, "SELECT SUM(status IN ('pending','gated')), COUNT(*) FROM expressions WHERE region=?", R)[0]
        backlog = f"{n_pg}/{n_all} = {n_pg / n_all:.0%}（阈值 30%）" if n_all else "?"
        print(f"  三次门禁后区级积压（pending+gated）: {backlog}")
        H2("门禁逐条结论 × 真实回测（同一批 39 条的历史实测：闸拦下的是不是好信号？）")
        per_wave = {}
        for wv in ("g2", "g3b", "g3"):
            items = (gate_json(wv).get("gate") or {}).get("report") or []
            if not items:
                print(f"  {wv}: 无 gate_results")
                continue
            exprs_g = [ln.strip() for ln in ef_all.read_text(encoding="utf-8").splitlines() if ln.strip()]
            blk, ok = [], []
            tags = {}
            for it in items:
                e = it.get("expr") or exprs_g[it["index"] - 1]
                s = q(DB, "SELECT MAX(sharpe) FROM backtest_results WHERE region=? AND code=?", R, e)[0][0]
                (ok if it.get("pass") else blk).append(s)
                for iss in it.get("issues") or []:
                    m = re.match(r"\[([\w-]+)\]", iss)
                    tags[m.group(1) if m else iss[:20]] = tags.get(m.group(1) if m else iss[:20], 0) + 1
            mean = lambda xs: round(sum(x for x in xs if x is not None) / max(1, len([x for x in xs if x is not None])), 2)  # noqa: E731
            top = lambda xs: max([x for x in xs if x is not None] or [None])  # noqa: E731
            per_wave[wv] = {"pass": len(ok), "blocked": len(blk), "blk_mean": mean(blk), "blk_max": top(blk), "tags": tags}
            print(f"  {wv}: 放行 {len(ok)} 条（实测 sharpe 均值 {mean(ok)}，最高 {top(ok)}）；"
                  f"拦截 {len(blk)} 条（均值 {mean(blk)}，最高 {top(blk)}）；拦截理由 {tags}")
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
        n_block = sum(1 for v in pred.values() if v[0] == "BLOCK")
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
        w1 = per_wave.get("g2", {})
        wb = per_wave.get("g3b", {})
        w3 = per_wave.get("g3", {})
        g2_state = dict((s, n) for w, s, n in dist if w == "g2")
        # 闸门环境缺失（verifier / op_arity 不可达）的逐条标记数——本轮首跑曾 39/39 全是 [ARITY_UNKNOWN]
        n_env_unknown = sum(v["tags"].get(t, 0) for v in per_wave.values() for t in ("ARITY_UNKNOWN", "SYNTAX_UNKNOWN"))
        V["R19"]["env_unknown"] = n_env_unknown
        all_pass_g3 = w3.get("pass") == len(real_exprs)
        V["R21"] = {"cached": gb.get("cached"), "total": gb.get("total"), "pass_g3b": wb.get("pass"), "pass_g3": w3.get("pass"),
                    "g2_state": g2_state, "backlog": backlog}
        cache_ok = gb.get("cached") == 0 and wb.get("pass") == w3.get("pass") and (w3.get("pass") or 0) > 0

        # R12：tools/ 下 CLI 自己找 skill 脚本（skill_paths）+ 门禁环境缺失 exit 2。三次调用的写入都指到演练库的
        # 副本（WQB_DB_PATH），不改变步 6–9 的区域状态（否则多出的 gated 行会把积压推过 30%）。
        probe_db = SCRATCH / "wqb.db.r12probe"
        for suffix in ("", "-wal", "-shm"):
            if Path(str(probe_db) + suffix).exists():
                Path(str(probe_db) + suffix).unlink()
        src_c, dst_c = sqlite3.connect(str(DB)), sqlite3.connect(str(probe_db))
        src_c.backup(dst_c)
        src_c.close()
        dst_c.close()
        no_dirs = ("WQ_TOOLKIT_DIR", "WQ_VALIDATOR_DIR")
        env_r12 = {k: v for k, v in HTTP_ENV.items() if k not in no_dirs}
        env_r12["WQB_DB_PATH"] = str(probe_db)
        H2("④ R12：env 去掉 WQ_TOOLKIT_DIR / WQ_VALIDATOR_DIR（= wqb-db server 的 env 形态），同 ③ 的参数重跑 wave_gate")
        print("  （第三轮及以前：tools/ 下 CLI 只搜 ~/.qoder-cn / ~/.cursor / ~/.workbuddy，不含 ~/.claude、~/.codex 与仓库兜底（N12））")
        p4, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--gate-mode", "warn", "--campaign-dir", str(CAMPAIGN), "--dataset", DS,
                    "--datasets", DS2, "--no-cache", "--wave", "g4", "--exprs-file", str(ef_all)],
                   env_extra=env_r12, env_drop=_ROOT_VARS + no_dirs, tail=0)
        for pat in (r"^\[done \]", r"^\[state\]"):
            print("  | " + rel(line_of(p4.stdout, pat) or f"（无匹配 {pat} 的行）")[:230])
        items4 =(gate_json("g4", probe_db).get("gate") or {}).get("report") or []
        pass4 = sum(1 for it in items4 if it.get("pass"))
        n4_unknown = len(re.findall(r"\[(?:ARITY|SYNTAX)_UNKNOWN\]", p4.stdout))
        print(f"  放行 {pass4}/{len(items4)}（③ 对照组 {w3.get('pass')}）；闸门环境缺失标记 {n4_unknown} 条")
        H2("⑤ R12：verifier 缺 ply（假 verifier：import 即打印提示并 exit 1，与真实缺 ply 的行为一致）")
        print("  （修复前：wave_gate 随之 exit 1——与'表达式不合格'同一个退出码，调用方分不清）")
        fake = SCRATCH / "fake_verifier"
        fake.mkdir(exist_ok=True)
        (fake / "validator.py").write_text('import sys\nprint("错误: 需要安装PLY库。")\nsys.exit(1)\n', encoding="utf-8")
        p5, _ = sh([PY, str(ROOT / "tools" / "wave_gate.py"), "--gate-mode", "warn", "--campaign-dir", str(CAMPAIGN), "--dataset", DS,
                    "--datasets", DS2, "--no-cache", "--wave", "g5", "--exprs-file", str(ef_all)],
                   env_extra={**env_r12, "WQ_VALIDATOR_DIR": str(fake)}, env_drop=_ROOT_VARS + no_dirs, tail=0)
        print("  | " + rel(line_of(p5.stdout, r"门禁环境缺失|^\[done \]") or "（无 [done ] 行）")[:230])
        H2("⑥ R12：probe_batch_mode.py --dry-run（同 ④ 的 env：无 WQ_TOOLKIT_DIR；库指到副本）")
        cand = SCRATCH / "realenv_probe_candidates.json"
        cand.write_text(json.dumps([{"id": i, "expression": e} for i, e in enumerate(real_exprs[:8], 1)], ensure_ascii=False),
                        encoding="utf-8")
        cache_dir_existed = (CAMPAIGN / "cache").is_dir()
        p6, _ = sh([PY, str(ROOT / "tools" / "probe_batch_mode.py"), "--campaign-dir", str(CAMPAIGN), "--dataset", DS,
                    "--wave", "999", "--candidates", str(cand), "--dry-run"],
                   env_extra=env_r12, env_drop=_ROOT_VARS + no_dirs, tail=8)
        # --dry-run 仍把结果写进战役 cache/（gitignored，Probe 看不到）——演练自己造的，删掉
        probe_cache = CAMPAIGN / "cache" / f"probe_wave999_{DS}.json"
        if probe_cache.exists():
            probe_cache.unlink()
            if not cache_dir_existed and not any(probe_cache.parent.iterdir()):
                probe_cache.parent.rmdir()
            print(f"  （干跑仍写了 {rel(probe_cache)}（tracking/.gitignore 忽略 cache/）；演练自身产物，已删除）")
        V["R12"] = {"gate_exit": p4.returncode, "gate_pass": f"{pass4}/{len(items4)}", "gate_pass_n": pass4,
                    "ref_pass": w3.get("pass"), "gate_unknown": n4_unknown,
                    "fake_exit": p5.returncode, "fake_msg": "门禁环境缺失" in p5.stdout,
                    "probe_exit": p6.returncode, "probe_dry": "DRY_RUN" in p6.stdout}
        r12_ok = (p4.returncode in (0, 1) and n4_unknown == 0 and pass4 == w3.get("pass") and p5.returncode == 2
                  and V["R12"]["fake_msg"] and p6.returncode == 0 and V["R12"]["probe_dry"])
        STAGE("步 5 · S2→S3 门禁",
              f"{len(real_exprs)} 条 {DS} 真实历史表达式（含 {len(real_pass)} 条实测过廉价闸者，其中 88lr21xo / A1lb2KpR 是 ACTIVE 原式）；"
              f"两份字段目录；子进程 env = .mcp.json 原样",
              "ghost-audit → wave_gate.py（语法 → gate.py 静态闸 1-5 逐条 → 批级多样性 / 体检硬门 / prod-sat / opcat / 质量预估），"
              "三种调用：① 只声明主集  ② 补声明第二腿、走缓存  ③ 补声明 + --no-cache（对照组）；"
              "R12 探针（写入指到库副本）：④ env 去掉 WQ_TOOLKIT_DIR / WQ_VALIDATOR_DIR  ⑤ 假 verifier 缺 ply  ⑥ probe_batch_mode 干跑",
              f"① exit={p1.returncode}：放行 {w1.get('pass')}/{len(real_exprs)}，拦 {w1.get('blocked')}（{w1.get('tags')}，被拦者实测均值 "
              f"{w1.get('blk_mean')}、最高 {w1.get('blk_max')}），逐条回写 {g2_state}，杂散目录={stray_found}；"
              f"② cached={gb.get('cached')}/{gb.get('total')}，放行 {wb.get('pass')}；③ 放行 {w3.get('pass')}；"
              f"门禁后积压（pending+gated）{backlog}；闸门环境缺失标记 {n_env_unknown} 条；质量预估 BLOCK {n_block}/{len(pred)}；"
              f"④ exit={p4.returncode}、放行 {pass4}/{len(items4)}、环境缺失标记 {n4_unknown}；⑤ exit={p5.returncode}；"
              f"⑥ exit={p6.returncode}（DRY_RUN={V['R12']['probe_dry']}）",
              (("静态闸 ★★★：两腿都声明时 39/39 放行、含全部实测赢家" if all_pass_g3
                else f"⚠ 两腿都声明时仍只放行 {w3.get('pass')}/{len(real_exprs)}（见上方拦截理由）") +
               ("，补声明后缓存不再掩盖结论（R21）" if cache_ok else "，⚠ 补声明后缓存结论与对照组不一致") +
               ("；不带 WQ_* 目录变量也找得到 toolkit / verifier、缺 ply 报 ERROR(2) 而非 FAIL(1)（R12）" if r12_ok
                else "；⚠ R12 预期未达成（见 ④⑤⑥）") +
               "；逐条回写让 gated 只表示'过了闸'，FAIL 候选记 fail、不再计入积压（R7）"
               "；漏声明第二腿仍会拦下赢家——FIELD 报错应点名字段所属的已知数据集（建议）"
               f"；质量预估 ✗（{n_block}/{len(pred)} BLOCK 含全部实测赢家，R27 未做）；[opcat] 只打印不判定 ✂（R6 未做）；体检硬门缺包未生效"))

        # ------------------------------------------------------------------ 步 6
        H1("步 6 · S3 七槽回测（前置三闸 on 真实历史）")
        bt, _, _ = await http.call("workflow_batch_track", region=R, wave="g2", dataset=DS, dry_run=True, n=600)
        s3, _, _ = await http.call("workflow_campaign", region=R, stage="S3", dataset=DS, wave="g2", dry_run=True, n=1400)
        bt_o = node_out(bt)
        bt_cmd = str(bt_o.get("command") or "")
        bt_gates = {s.get("step"): s.get("success") for s in bt_o.get("steps", []) if str(s.get("step", "")).endswith("_gate")}
        s3_gates = {s.get("step"): s.get("success") for s in node_out(s3).get("steps", []) if str(s.get("step", "")).endswith("_gate")}
        V["R5"] = {"bt_success": bt_o.get("success"), "bt_gates": bt_gates, "bt_error": bt_o.get("error"),
                   "bt_has_cmd": "--submit" in bt_cmd, "same_as_s3": bt_gates == s3_gates}
        r5_ok = bt_o.get("success") is False and bt_gates.get("stop_rules_gate") is False and "--submit" in bt_cmd
        STAGE("步 6 · S3 七槽回测",
              f"门禁后的 g2（逐条状态 {g2_state}）；区域状态（停止规则 B 命中）",
              "SOP 指定入口 workflow_batch_track 干跑 vs workflow_campaign(S3) 干跑（R5 后两者共用 run_open_wave_gates："
              "signal_floor / stop_rules / backlog，首个拦截即停）",
              f"batch_track success={bt_o.get('success')}、闸 {bt_gates}、error={dump(bt_o.get('error'), 70)}、"
              f"仍带回将要执行的命令（含 --submit={'--submit' in bt_cmd}）；campaign S3 success={node_out(s3).get('success')}，闸 {s3_gates}",
              "★★ 保留（七槽 / 设置先验 / 连坐隔离 / argv 握手都有实证）；" +
              ("N5 已修（R5）：SOP 指定入口与 S3 同过三闸，规则 B 命中的区域干跑即拦截、不再照样发批" if r5_ok
               else "⚠ R5 预期未达成：batch_track 未被区域闸拦截"))

        # ------------------------------------------------------------------ 步 7
        H1("步 7 · S4 诊断改进（真实回测行上的墙诊断 / salvage）")
        s4, _, _ = await http.call("workflow_campaign", region=R, stage="S4", dataset=DS, wave="94", dry_run=True, n=700)
        await db_srv.call("list_alphas_by_wave", region=R, wave_number="94", n=500)
        await db_srv.call("search_alphas_by_sharpe", region=R, min_sharpe=1.2, limit=8, n=900)
        sb, _, _ = await db_srv.call("backfill_salvage_pool_batch", region=R, candidates_dir=str(CAMPAIGN / "candidates"), n=700)
        sp, _, _ = await db_srv.call("get_salvage_pool", region=R, n=500)
        await http.call("workflow_execute", label="workflow_execute(auto_review, dry_run)", node="auto_review",
                        params={"region": R, "wave": "94", "dataset": DS}, dry_run=True, n=500)
        H2("review_wave 判定（真实 thresholds.json × 真实回测行，wave 91/91b/91c/94 sharpe 前 6）")
        prw, _ = sh([PY, "-c", "import sys,json,sqlite3; sys.path.insert(0,'.'); import review_wave as rw; "
                              f"t=json.load(open(r'{CAMPAIGN / 'config' / 'thresholds.json'}',encoding='utf-8')); "
                              "tr=t['review']; tn=dict(t.get('near') or {}); "
                              f"c=sqlite3.connect(r'{DB}'); "
                              "rows=c.execute(\"SELECT alpha_id,wave,sharpe,fitness,two_year_sharpe,sub_universe_sharpe,turnover FROM backtest_results "
                              f"WHERE region='{R}' AND wave IN ('91','91b','91c','94') ORDER BY sharpe DESC LIMIT 6\").fetchall(); "
                              "[print(a,w,'S=%s F=%s 2Y=%s sub=%s'%(s,f,y,sb),'passes=',rw.passes({'sharpe':s,'fitness':f,'two_year_sharpe':y,"
                              "'sub_universe_sharpe':sb,'turnover_pct':(tv or 0)*100,'margin_bp':None,'failed_checks':[]},tr),"
                              "'walls=',rw.walls({'sharpe':s,'fitness':f,'two_year_sharpe':y,'sub_universe_sharpe':sb,'turnover_pct':(tv or 0)*100,"
                              "'margin_bp':None,'failed_checks':[]},tr)) for a,w,s,f,y,sb,tv in rows]"],
                    cwd=TOOLKIT, tail=10)
        H2("R4：near / 组合候选（= salvage 池来源）排除 RN_EXPOSURE —— 仓库内全部带 rn_sharpe 的真实评审行（KOR 历史无 rn 字段）")
        print("  （修复前 = 同一行去掉 rn_sharpe：R4 之前 rn_exposure 只进 passes()/walls()，near 池与 combo_candidate 看不到它）")
        _, r4 = run_probe("r4_near_probe", R4_PROBE, [ROOT], TOOLKIT, "R4JSON")
        r4 = r4 or {}
        r4 = {reg: s for reg, s in r4.items() if s["rows"]}
        for reg, s in sorted(r4.items()):
            print(f"  {reg}: 评审行 {s['rows']}（RN_EXPOSURE {s['rn_exposure']}，其 raw sharpe 最高 {s['rn_max_sharpe']}；"
                  f"near 线 {s['near_min']} / 组合线 {s['combo_min']}）；near {s['near_old']} → {s['near_new']}，"
                  f"组合候选 {s['combo_old']} → {s['combo_new']}；被挡出 near/salvage {s['excluded']} 条 例 {s['examples']}；"
                  f"新池内仍有 RN_EXPOSURE {s['leak']} 条")
        r4_tot = {k: sum(s[k] for s in r4.values()) for k in ("rows", "rn_exposure", "excluded", "leak")}
        rn_max = max((s["rn_max_sharpe"] for s in r4.values() if s["rn_max_sharpe"] is not None), default=None)
        V["R4"] = dict(r4_tot, regions=sorted(r4), rn_max_sharpe=rn_max)
        # 三态：True = 真实数据上看到被挡出的行；False = 新池里还有 RN_EXPOSURE；None = 真实数据无触发样本（只能靠单测）
        r4_ok = False if r4_tot["leak"] else (True if r4_tot["excluded"] else None)
        V["R4"]["ok"] = r4_ok
        if r4_ok is None:
            print(f"  → 仓库真实数据里没有 R4 的触发样本：{r4_tot['rn_exposure']} 条 RN_EXPOSURE 行 raw sharpe 最高 {rn_max}，"
                  f"全部在 near / 组合线之下，修复前后池子一致；R4 的效果只能由单测（构造行）验证")
        rs4 = step_of(s4, "resolve_s4_alphas") or {}
        entries = sp.get("entries", []) if isinstance(sp, dict) else []
        n_noexpr = sum(1 for e in entries if not e.get("expression"))
        rw_lines = [ln for ln in prw.stdout.splitlines() if "passes=" in ln]
        n_mu = sum(1 for ln in rw_lines if "passes= False" in ln and "walls= ['MARGIN_UNKNOWN']" in ln)
        sb = sb if isinstance(sb, dict) else {}
        STAGE("步 7 · S4 诊断改进",
              "wave 94 的回测行；91/91b/91c/94 sharpe 前 6；tracking/KOR/config/thresholds.json；candidates 目录；"
              f"R4 探针：{'/'.join(sorted(r4))} 评审文件里带 rn_sharpe 的 {r4_tot['rows']} 条真实行",
              "S4 review_wave 命令构建（干跑）；按波列 alpha / 按 sharpe 检索；salvage 批量回填；auto_review 干跑；"
              "review_wave.passes() / walls() 判定函数直调；R4：review_wave 的 near / combo 判据新旧对照",
              f"S4 解析 alpha {rs4.get('alpha_count')} 条；salvage 回填 processed={sb.get('processed')} success={sb.get('success')} "
              f"skipped={sb.get('skipped')}，池内 {len(entries)} 条中无表达式 {n_noexpr} 条；"
              f"review_wave：{n_mu}/{len(rw_lines)} 条 walls 只有 MARGIN_UNKNOWN 却 passes=False；"
              f"R4：RN_EXPOSURE {r4_tot['rn_exposure']} 条（raw sharpe 最高 {rn_max}）中 {r4_tot['excluded']} 条此前会进 near/salvage、"
              f"现被挡出；新池内残留 {r4_tot['leak']} 条",
              "★★★ 保留墙诊断（RN_EXPOSURE / ROBUST_STRUCTURAL 有实证）；salvage 收无表达式条目（N26）、passes/walls 缺失值口径不一（N27）"
              "——P2/P3 待办；" + {True: "N4 已修（R4）：真实行里 RN_EXPOSURE 不再进 near / salvage / 组合候选",
                                  False: "⚠ R4 预期未达成：新池里仍有 RN_EXPOSURE 行",
                                  None: "R4 为防御性修复：真实数据无触发样本（RN_EXPOSURE 行都在 near / 组合线之下），"
                                        "新池无残留、效果由单测守"}[r4_ok])

        # ------------------------------------------------------------------ 步 8
        H1("步 8 · S4→S5 稳健闸与提交判定")
        srd, _, _ = await db_srv.call("get_submit_ready", region=R, n=600)
        sv8, _, _ = await http.call("submit_verdict", alpha_id="88lr21xo", n=500)
        await http.call("workflow_judge", alpha_id="88lr21xo", dry_run=True, n=500)
        sa1, _, _ = await http.call("workflow_submit_alpha", label="workflow_submit_alpha（未确认，干跑）", alpha_id="78jQ29rL",
                                    dry_run=True, n=500)
        sa2, _, _ = await http.call("workflow_submit_alpha", label="workflow_submit_alpha（confirm_submit=True，干跑）",
                                    alpha_id="78jQ29rL", confirm_submit=True, dry_run=True, n=500)
        H2("R3：RA / PPA 资格门失败计数（submit 判定的输入）只剩 wqb.config 一份——同一组 N3 checks，仓库布局 vs 镜像布局")
        print("  （N3 checks = LOW_2Y_SHARPE WARNING / IS_LADDER_SHARPE WARNING / LOW_SUB_UNIVERSE_SHARPE FAIL；生产口径 failed_ra=3）")
        mcp_dir = ROOT / "world-quant-brain-mcp"
        _, r3_repo = run_probe("r3_failed_count", R3_PROBE, ["repo"], mcp_dir, "R3JSON")
        print("  仓库布局 →", dump(r3_repo, 400))
        _, r3_docker = run_probe("r3_failed_count", R3_PROBE, ["docker"], mcp_dir, "R3JSON")
        print("  镜像布局 →", dump(r3_docker, 400))
        r3_repo, r3_docker = r3_repo or {}, r3_docker or {}
        r3_before = None
        if BASE_DIR:
            print("  修复前（BASE_DIR 原始副本：mcp_core 内联一份、wqb.config 另一份）:")
            _, r3_before = run_probe("r3_failed_count", R3_PROBE, ["repo"], BASE_DIR / "world-quant-brain-mcp", "R3JSON",
                                     env_extra={"PYTHONPATH": str(BASE_DIR / "src")})
            print("  修复前 →", dump(r3_before, 400))
        V["R3"] = {"repo": r3_repo, "docker": r3_docker, "before": r3_before}
        counts = {(d.get("failed_ra"), d.get("failed_ppa")) for d in (r3_repo, r3_docker, r3_repo.get("wqb_config") or {})}
        r3_ok = (r3_repo.get("source") == "wqb.config" and r3_docker.get("source") == "mcp_core frozen copy"
                 and counts == {(3, 1)})
        STAGE("步 8 · S4→S5 稳健闸与提交判定",
              "88lr21xo（ACTIVE 原式）/ 78jQ29rL（同族实测 1.91）；平台凭据：无；R3 探针：N3 那组 checks",
              "get_submit_ready；submit_verdict（平台侧否决权威）；judge / submit_alpha 干跑（未确认 / confirm_submit=True）；"
              "R3：mcp_core._slim_checks 在仓库布局 / 镜像布局（屏蔽 wqb 包）各算一次，并与 wqb.config 对照",
              f"submit_ready={srd}；submit_verdict → {dump(sv8, 80)}；submit_alpha 干跑 submitted="
              f"{node_out(sa1).get('submitted')}/{node_out(sa2).get('submitted')}（只给请求计划、不触平台）；"
              f"R3：仓库布局 source={r3_repo.get('source')} failed_ra/ppa={r3_repo.get('failed_ra')}/{r3_repo.get('failed_ppa')}，"
              f"镜像布局 source={r3_docker.get('source')} {r3_docker.get('failed_ra')}/{r3_docker.get('failed_ppa')}，"
              f"wqb.config {(r3_repo.get('wqb_config') or {}).get('failed_ra')}/{(r3_repo.get('wqb_config') or {}).get('failed_ppa')}"
              + (f"；修复前 mcp_core {r3_before.get('failed_ra')}/{r3_before.get('failed_ppa')} vs wqb.config "
                 f"{(r3_before.get('wqb_config') or {}).get('failed_ra')}/{(r3_before.get('wqb_config') or {}).get('failed_ppa')}"
                 if r3_before else ""),
              "★★★ 保留：否决链在无凭据时 fail-closed、不会误放行；用户确认门在干跑下同样不触平台；" +
              ("N3 已修（R3）：失败计数只剩 wqb.config 一份，镜像里的冻结副本与它同数（单测逐项守一致）" if r3_ok
               else "⚠ R3 预期未达成（见上方两种布局的输出）") +
              "；submit_verdict 定位（N8）仍是 P1 待办")

        # ------------------------------------------------------------------ 步 9
        H1("步 9 · S6 复盘回写（P0-1 契约 on 真实历史 + 停止闸闭环）")
        closed = q(DB, "SELECT wave_number, verdict FROM wave_results WHERE region=? AND status='closed' "
                       "ORDER BY datetime(COALESCE(updated_at, created_at)) DESC LIMIT 3", R)
        n_closed, n_open = (q(DB, "SELECT SUM(status='closed'), SUM(status='open') FROM wave_results WHERE region=?", R)[0])
        print("  最近 3 个 closed 波（按 updated_at = 第三轮及以前停止规则 B 的取法）:", closed)
        wave_fail = closed[0][0] if closed else "97"
        after = await p0_replay("修复后", db_srv, http, ROOT, DB, wave_fail)
        s91c = SUGG.get("91c")
        H2("残留（N22）：按导入时拒绝信息里的判定表建议补记 91c —— "
           + (f"R20 给 91c 的建议 = {s91c['verdict']}/{s91c['confidence']}（{s91c['rule']}）" if s91c else "91c 导入时无建议，按原文补记 PASS"))
        await db_srv.call("upsert_wave_result", region=R, wave_number="91c", verdict=(s91c or {}).get("verdict", "PASS"),
                          key_findings=["补记：2 RA 提交成功（88lr21xo + A1lb2KpR ACTIVE）"], n=260)
        win = q(DB, "SELECT wave_number, verdict FROM wave_results WHERE region=? AND status='closed' "
                    "ORDER BY datetime(COALESCE(updated_at, created_at)) DESC LIMIT 3", R)
        print("  旧取法（按 updated_at）的最近 3 个 closed 波:", win)
        g9, _, _ = await http.call("workflow_campaign", quiet=True, region=R, stage="S2", dataset=DS, wave="p0_next", dry_run=True)
        rb9 = _rule_b(g9)
        print(f"  停止规则 B 实际窗口（R22：按波的开始时刻 = waves.created_at，无表达式的波用结论行 created_at）: "
              f"{rb9['waves']} → {rb9['window']}")
        print("  下一波 S2 干跑: " + _gate_line(g9))
        bl = step_of(g9, "backlog_gate") or {}
        if bl:
            print("  同一干跑的积压闸:", dump({"success": bl.get("success"), "error": bl.get("error"),
                                              "pending_gated": (bl.get("evidence") or {}).get("pending_gated"),
                                              "total": (bl.get("evidence") or {}).get("total"),
                                              "pending_gated_ratio": (bl.get("evidence") or {}).get("pending_gated_ratio")}, 400))
        else:
            print("  同一干跑的积压闸：未执行（三道开波闸首个拦截即停，停止规则已拦）")
        bl_txt = (f"积压闸 success={bl.get('success')}，pending+gated 占比 {(bl.get('evidence') or {}).get('pending_gated_ratio')}"
                  if bl else "积压闸未执行：停止规则先拦")
        H2("S6 其余动作")
        pf, _ = sh([PY, str(ROOT / "tools" / "step_funnel.py"), "--region", R], tail=25)
        await http.call("workflow_execute", label="workflow_execute(auto_pyramid, dry_run)", node="auto_pyramid",
                        params={"region": R, "wave": wave_fail}, dry_run=True, n=400)
        r22_ok = bool(rb9["rule_B_blocks"]) and "91c" not in (rb9["waves"] or []) and bool(win) and win[0][0] == "91c"
        V["R22"] = {"old_order": [w for w, _ in win], "gate_window": rb9["waves"], "blocks": rb9["rule_B_blocks"],
                    "S2_success": rb9["S2_success"]}
        funnel_v = line_of(pf.stdout, r"\(空\)=|FAIL=").strip()
        STAGE("步 9 · S6 复盘回写",
              f"wave_results（closed {n_closed} / open {n_open}）；按 updated_at 的最近 3 个 closed 波 {closed}；导入时 R20 给 91c 的建议 "
              f"{(s91c or {}).get('verdict')}/{(s91c or {}).get('confidence')}",
              "P0-1 回放（字符串波号 / 只补 key_findings / 空壳结案）→ assemble-priors + GEM 快照检查 → 按建议补记 91c → step_funnel → auto_pyramid 干跑",
              f"字符串波号 {after['str_wave']}；只补 key_findings 后 verdict={after['verdict_after_kf_only']}、规则 B 仍拦截="
              f"{after['after_update']['rule_B_blocks']}；空壳结案 {after['hollow']}；补记 91c 后：旧取法（按 updated_at）"
              f"{[w for w, _ in win]}，规则 B 实际窗口（R22）{rb9['waves']} → 拦截={rb9['rule_B_blocks']}，"
              f"下一波 S2 success={rb9['S2_success']}（{bl_txt}）；"
              f"step_funnel verdict 分布 {funnel_v}",
              ("★★★ 保留：P0-1 契约在真实链路上守住规则 B 的输入" +
               ("；N22 已修（R22）：窗口按波的开始时刻取，补记旧波 91c 不再挤进'最近 3 个'，区域停波维持" if r22_ok
                else "；⚠ R22 预期未达成（见上方两种窗口）")))

        H1("附 A · 19 个 workflow 节点经 MCP workflow_execute(dry_run=True) 全量扫描（仓库 _DRY_RUN_CASES 参数）")
        import ast
        src_t = (ROOT / "tests" / "unit" / "test_skill_integrity.py").read_text(encoding="utf-8")
        cases = {}
        for node in ast.parse(src_t).body:
            if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "_DRY_RUN_CASES" for t in node.targets):
                cases = eval(compile(ast.Expression(node.value), "cases", "eval"), {})
        print(f"  {'node':24s} {'ok':6s} side-effects / error")
        n_ok, fails, silent, dirty_nodes, errs = 0, [], [], [], {}
        for node, params in sorted(cases.items()):
            out, err, pr = await http.call("workflow_execute", quiet=True, node=node, params=params, dry_run=True)
            ok = out.get("success") if isinstance(out, dict) else None
            e = (out.get("error") if isinstance(out, dict) else str(out)) or ""
            n_ok += bool(ok)
            if not ok:
                fails.append(node)
                errs[node] = e
                if not e:
                    silent.append(node)
            if pr.db_delta or pr.git_new:
                dirty_nodes.append(node)
            print(f"  {node:24s} {str(ok):6s} {pr.summary()[:150]}  {dump(rel(str(e)), 110) if e else ''}")
        print("  wq-brain-http workflow_list_nodes:", dump((await http.call("workflow_list_nodes", quiet=True))[0], 200))
        V["A"] = {"n_ok": n_ok, "n": len(cases), "fails": fails, "silent": silent, "dirty": dirty_nodes,
                  "batch_track_error": errs.get("batch_track")}
        print(f"  小结：{n_ok}/{len(cases)} 成功；失败 {fails}（其中无 error 的静默失败 {silent or '无'}）；"
              f"有 DB / git 副作用的节点 {dirty_nodes or '无'}")

    # ---------------------------------------------------------------------- 修复前对照
    before = None
    if BASE_DIR:
        H1("附 B · P0 修复前对照：导入后快照（同一份真实历史）复制到 git archive 原始副本，起修复前的两个 server 重放 P0 序列")
        bdb = BASE_DIR / "data" / "wqb.db"
        bdb.parent.mkdir(exist_ok=True)
        for suffix in ("", "-wal", "-shm"):
            if Path(str(bdb) + suffix).exists():
                Path(str(bdb) + suffix).unlink()
        # 用"导入后快照"起步：同一份真实历史，不带步 1–9 的演练写入（门禁重跑留下的逐条状态、91c 补记等）
        src_c = sqlite3.connect(str(SCRATCH / "wqb.db.imported"))
        dst = sqlite3.connect(str(bdb))
        src_c.backup(dst)
        src_c.close()
        dst.close()
        print("  base 库:", rel(bdb), dump(db_counts(bdb), 300))
        async with contextlib.AsyncExitStack() as stack:
            bdb_srv = await stack.enter_async_context(open_server("base:wqb-db", BASE_DIR, "wqb-db", bdb,
                                                                  errlog_name="base.wqb-db.stderr"))
            # 修复前代码的 assemble-priors 离开 WQB_WORKSPACE 会崩（N19b）——为了让 P0 对照只反映 P0，这里给它补上
            bhttp = await stack.enter_async_context(open_server("base:wq-brain-http", BASE_DIR, "wq-brain-http", bdb,
                                                                extra_env={"WQB_WORKSPACE": str(BASE_DIR)},
                                                                errlog_name="base.wq-brain-http.stderr"))
            closed_b = q(bdb, "SELECT wave_number, verdict FROM wave_results WHERE region=? AND status='closed' "
                              "ORDER BY datetime(COALESCE(updated_at, created_at)) DESC LIMIT 3", R)
            print("  base 最近 3 个 closed 波:", closed_b)
            before = await p0_replay("修复前", bdb_srv, bhttp, BASE_DIR, bdb, closed_b[0][0] if closed_b else "97")
        H2("P0 修复前 / 修复后（同一份导入后真实库、同一 MCP 调用序列）")
        for k, label in (("str_wave", "写字符串波号 s2_<ds>_d1"),
                         ("before_update", "补写前：下一波 S2 干跑"),
                         ("verdict_after_kf_only", "只补 key_findings 后该波 verdict"),
                         ("after_update", "补写后：同一下一波 S2 干跑"),
                         ("hollow", "新波只写 key_findings（缺 verdict）"),
                         ("assemble_cmd_tail", "assemble-priors 干跑命令尾（S2 / S6）"),
                         ("snapshot", "assemble-priors 真跑后 DB 快照存在"),
                         ("gem_snapshot_check", "GEM 干跑有快照检查步")):
            print(f"  {label:30s} 修复前 {dump(before.get(k), 110):60s} │ 修复后 {dump(after.get(k), 110)}")

    H1("P1 验证清单 —— 第一批（R18–R21）对照第二轮实录 realenv_transcript_p0.txt；"
       "第二批（R22 / R5 / R12 / R4 / R3）对照第三轮实录 realenv_transcript_r18_r21.txt")
    r18, r19, r20, r21 = V.get("R18", {}), V.get("R19", {}), V.get("R20", {}), V.get("R21", {})
    r22, r5, r12, r4, r3, va = (V.get(k) or {} for k in ("R22", "R5", "R12", "R4", "R3", "A"))
    r3r, r3d, r3b = r3.get("repo") or {}, r3.get("docker") or {}, r3.get("before") or {}
    checks = [
        ("R18 priors 截断：新登记优先 + 截断可见",
         "4.6：registry dead_end 13 → 快照 12，KOR-MODEL219-DEAD 进快照 False，截断无记录",
         f"4.6：registry dead_end {r18.get('registry_dead')} → 快照 {r18.get('snap_dead')}，KOR-MODEL219-DEAD 进快照 "
         f"{r18.get('in_snapshot')}，truncated={r18.get('truncated')}",
         bool(r18.get("in_snapshot")) and bool(r18.get("truncated"))),
        ("R19 库路径收敛（.mcp.json 原样 env）",
         "4.1 assemble-priors rc=1；① 候选写进杂散库、gate.py exit 2",
         f"4.1 rc={r19.get('assemble_rc')}；① exit={r19.get('gate1_exit')}，真库 g2 {r19.get('g2_in_real_db')} 条，杂散目录={r19.get('stray')}，"
         f"闸门环境缺失标记 {r19.get('env_unknown')} 条（本轮首跑修 gate.py 前为 117 条 [ARITY_UNKNOWN]）",
         r19.get("assemble_rc") == 0 and not r19.get("stray") and r19.get("g2_in_real_db", 0) > 0
         and r19.get("gate1_exit") in (0, 1) and r19.get("env_unknown") == 0),
        ("R20 verdict 判定表 + 拒绝时给建议",
         "导入时 24 条被拒，均无任何建议",
         f"被拒 {r20.get('rejected')} 条中 {r20.get('with_suggestion')} 条附建议 {r20.get('by_conf')}；91c → {r20.get('91c')}",
         r20.get("with_suggestion") == r20.get("rejected") and (r20.get("91c") or {}).get("verdict") == "PASS"),
        ("R21 gate 缓存键 + 逐条状态回写（含 R7）",
         "② cached=39/39、放行 20/39；三次门禁 117 条全记 gated（含 38 条 FIELD 失败），积压 117/364 = 32% 越过 30% 上限",
         f"② cached={r21.get('cached')}/{r21.get('total')}、放行 {r21.get('pass_g3b')}（对照组 {r21.get('pass_g3')}）；"
         f"g2 回写 {r21.get('g2_state')}；三次门禁后积压 {r21.get('backlog')}",
         r21.get("cached") == 0 and r21.get("pass_g3b") == r21.get("pass_g3") and (r21.get("pass_g3") or 0) > 0
         and {"gated", "fail"} <= set(r21.get("g2_state") or {})),
        ("R22 停止规则 B 窗口按波的开始时刻",
         "步 9：补记 91c 后按 updated_at 取窗口 [91c PASS, 97 FAIL, s2_ml_factor_proj_d1 FAIL] → 规则 B 解除、下一波 S2 success=True（N22）",
         f"步 9：补记 91c 后旧取法 {r22.get('old_order')}；实际窗口 {r22.get('gate_window')} → 规则 B 拦截={r22.get('blocks')}，"
         f"下一波 S2 success={r22.get('S2_success')}",
         r22.get("blocks") is True and "91c" not in (r22.get("gate_window") or [])
         and (r22.get("old_order") or [None])[0] == "91c"),
        ("R5 batch_track 过三道开波闸",
         "步 6：batch_track 干跑 success=True、区域闸步 []——规则 B 命中的区域照样发批（N5）；附 A batch_track True",
         f"步 6：batch_track success={r5.get('bt_success')}、闸 {r5.get('bt_gates')}（与 S3 同一结果={r5.get('same_as_s3')}）、"
         f"仍带回命令={r5.get('bt_has_cmd')}；附 A 失败 {va.get('fails')}，静默失败 {va.get('silent') or '无'}",
         r5.get("bt_success") is False and (r5.get("bt_gates") or {}).get("stop_rules_gate") is False
         and bool(r5.get("bt_has_cmd")) and "batch_track" in (va.get("fails") or []) and not va.get("silent")),
        ("R12 tools/ 下 CLI 的 skill 解析 + 门禁环境缺失 exit 2",
         "tools/ 下 CLI 只搜 ~/.qoder-cn / ~/.cursor / ~/.workbuddy（本机单测 3 个 N12 用例红）；verifier 缺 ply → exit 1（与'表达式不合格'同码）",
         f"④ 无 WQ_* 目录变量：exit={r12.get('gate_exit')}、放行 {r12.get('gate_pass')}（对照组 {r12.get('ref_pass')}）、"
         f"环境缺失标记 {r12.get('gate_unknown')}；⑤ 假 verifier exit={r12.get('fake_exit')}（门禁环境缺失={r12.get('fake_msg')}）；"
         f"⑥ probe_batch_mode exit={r12.get('probe_exit')}（DRY_RUN={r12.get('probe_dry')}）",
         r12.get("gate_exit") in (0, 1) and r12.get("gate_unknown") == 0 and r12.get("gate_pass_n") == r12.get("ref_pass")
         and r12.get("fake_exit") == 2 and bool(r12.get("fake_msg")) and r12.get("probe_exit") == 0 and bool(r12.get("probe_dry"))),
        ("R4 near / salvage 池排除 RN_EXPOSURE",
         "near 池只排除 ROBUST_STRUCTURAL；RN_EXPOSURE 行照样进 near / salvage / 组合候选（N4；第三轮未实测条数）",
         f"{'/'.join(r4.get('regions') or [])} 真实评审行 {r4.get('rows')} 条（RN_EXPOSURE {r4.get('rn_exposure')}，"
         f"raw sharpe 最高 {r4.get('rn_max_sharpe')}）：此前会进 near/salvage、现被挡出 {r4.get('excluded')} 条；"
         f"新池内残留 {r4.get('leak')} 条" + ("——真实数据无触发样本，效果由单测守" if r4.get("ok") is None else ""),
         r4.get("ok")),
        ("R3 Failed-count 单一实现",
         "三份实现（mcp_core / wqb.config / build_gate_prior）；同一组 N3 checks：mcp_core failed_ra=3、wqb.config 0（N3）",
         f"仓库布局 {r3r.get('source')} {r3r.get('failed_ra')}/{r3r.get('failed_ppa')}；镜像布局 {r3d.get('source')} "
         f"{r3d.get('failed_ra')}/{r3d.get('failed_ppa')}；wqb.config {(r3r.get('wqb_config') or {}).get('failed_ra')}/"
         f"{(r3r.get('wqb_config') or {}).get('failed_ppa')}" +
         (f"（修复前副本实测：mcp_core {r3b.get('failed_ra')} vs wqb.config {(r3b.get('wqb_config') or {}).get('failed_ra')}）" if r3b else ""),
         r3r.get("source") == "wqb.config" and r3d.get("source") == "mcp_core frozen copy"
         and {(r3r.get("failed_ra"), r3r.get("failed_ppa")), (r3d.get("failed_ra"), r3d.get("failed_ppa")),
              ((r3r.get("wqb_config") or {}).get("failed_ra"), (r3r.get("wqb_config") or {}).get("failed_ppa"))} == {(3, 1)}),
    ]
    print("  （✅ 真实环境验证通过 / ❌ 与预期不符 / ➖ 真实数据无触发样本、无从验证，靠单测）")
    for name, prev, now, ok in checks:
        mark = "➖" if ok is None else ("✅" if ok else "❌")
        print(f"  {mark} {name}\n      修复前：{prev}\n      本轮：  {now}")

    print("\n[REAL-ENV DRY-RUN END]")
    print("  仓库已入库文件是否被改动（应只剩本轮修复 + 报告）:", sorted(git_dirty(ROOT)))


if __name__ == "__main__":
    asyncio.run(main())
