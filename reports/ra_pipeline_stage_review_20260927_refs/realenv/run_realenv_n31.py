# -*- coding: utf-8 -*-
"""N31 · 真实环境探针：SOP 步 6 手动补收入口修复前后对照（2026-09-27 第六轮）。

N31：SOP（ra-pipeline SKILL.md 步 6）写的收批入库工具 `mcp__wqb-db__harvest_multisim_results` 自 726a350
（2026-09-19）起不在 MCP 工具表里——那次提交把 `_flatten_platform_alpha` 插进了它与 `@mcp.tool()` 之间，
装饰器改挂到私有函数上。声称承接它的 `workflow_auto_harvest` 按不存在的列读写，调用即报错。

方法（同 run_realenv.py）：wqb-db server 按仓库 .mcp.json 经 stdio 真实启动，所有调用走 MCP 协议层；
库 = tracking/KOR 真实历史经 MCP 写工具导入（run_realenv.import_history）。修复前的代码树（BASE_DIR，
默认 main 的 9ca1cc8）与本工作树各跑一遍：
  ⓪ 工具表；① **照各自代码树里 SOP 的原文**调收批入库；② workflow_auto_harvest 只读报告（真实波 94）；
  ③ workflow_auto_harvest 带 alphas（入库 + 报告）。
输入 = `harvest_multisim_alphas` 的返回形态（mcp_core._slim_alpha：指标嵌在 metrics、checks 分桶），由 KOR
真实 wave94 的 9 条指标与 tracking/KOR/config/settings.json 组装；alpha_id 加前缀 n31_（与已导入的同批行区分），
multisimulation_id 标为 n31probe。历史文件没有逐项 checks，checks 置空。本容器无 BRAIN 凭据，脚本不读 .env。

副作用：wqb-db server 写死 <tree>/data/wqb.db（N26），两棵树的该文件在演练期间换成导入快照的副本，
结束（含异常）后移到 $REALENV_SCRATCH/n31/，原有文件移回。用法见同目录 reproduce_realenv_n31.sh。
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_realenv as H  # noqa: E402  复用：stdio 起服（.mcp.json 原样）、真实历史导入、副作用探针、脱敏

ROOT, BASE, R = H.ROOT, H.BASE_DIR, H.R
WORK = H.SCRATCH / "n31"
S2 = "s2_ml_factor_proj_d1"
PREFIX, MSID = "n31_", "n31probe"
SOP_REL = Path("Claude") / "skills" / "wq-brain-ra-pipeline" / "SKILL.md"
HOME = str(Path.home())
_rel0 = H.rel


def rel(p):
    return _rel0(p).replace(HOME + os.sep, "~" + os.sep)


H.rel = rel


# ----------------------------------------------------------------------------- 输入：平台返回形态
def platform_response():
    """KOR 真实 wave94 的 9 条指标 → harvest_multisim_alphas 的返回值形态。"""
    raw = json.load(open(ROOT / "tracking" / R / "candidates" / "wave94_results.json", encoding="utf-8"))
    settings = json.load(open(ROOT / "tracking" / R / "config" / "settings.json", encoding="utf-8"))
    stg = {k: settings.get(k) for k in ("region", "universe", "delay", "neutralization", "decay", "truncation")
           if settings.get(k) is not None}
    alphas = []
    for r in raw.get("results") or raw.get("candidates") or []:
        if not (r.get("alpha") and r.get("expr") and isinstance(r.get("sharpe"), (int, float))):
            continue
        m = {"sharpe": r["sharpe"], "fitness": r.get("fitness"), "turnover": r.get("tvr"),
             "two_year_sharpe": r.get("two_year"), "sub_universe_sharpe": r.get("sub"),
             "prodCorrelation": r.get("prod_corr")}
        aid = PREFIX + r["alpha"]
        alphas.append({"alpha_id": aid, "id": aid, "expression": r["expr"], "code": r["expr"],
                       "status": "UNSUBMITTED", "settings": stg,
                       "metrics": {k: v for k, v in m.items() if v is not None},
                       "checks": {"fail": [], "warning": [], "pass": [], "pending": []}})
    return {"success": True, "multisimulation_id": MSID, "total": len(alphas), "complete": len(alphas),
            "error_count": 0, "alphas": alphas, "errors": None}


def sop_harvest_call(tree):
    """该树 SOP 手动补收块：harvest_multisim_alphas 之后那一行 wqb-db 调用 → (工具名, 是否传整个返回值, 原文)。"""
    lines = (Path(tree) / SOP_REL).read_text(encoding="utf-8").splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith("mcp__wq-brain-http__harvest_multisim_alphas"))
    line = next(ln for ln in lines[i + 1:] if ln.startswith("mcp__wqb-db__"))
    return re.match(r"mcp__wqb-db__(\w+)", line).group(1), "整个返回值" in line, line.strip()


# ----------------------------------------------------------------------------- 库
def _db_files(tree):
    return [Path(tree) / "data" / f"wqb.db{s}" for s in ("", "-wal", "-shm")]


def stash(tree, tag):
    db = Path(tree) / "data" / "wqb.db"
    if db.exists() and db.stat().st_size > 5_000_000 and os.environ.get("REALENV_ALLOW_DB_SWAP") != "1":
        sys.exit(f"{rel(db)} 像是生产库（{db.stat().st_size} bytes）；确认后设 REALENV_ALLOW_DB_SWAP=1 再跑")
    saved = []
    for p in _db_files(tree):
        if p.exists():
            dst = WORK / f"{tag}.{p.name}.before_n31"
            shutil.move(str(p), str(dst))
            saved.append((dst, p))
    return saved, (Path(tree) / "data").is_dir()


def restore(tree, tag, st):
    saved, had_dir = st
    for p in _db_files(tree):
        if p.exists():
            shutil.move(str(p), str(WORK / f"{tag}.{p.name}.after_n31"))
    for dst, p in saved:
        shutil.move(str(dst), str(p))
    data = Path(tree) / "data"
    if not had_dir and data.is_dir() and not any(data.iterdir()):
        data.rmdir()


def fresh_db(tree, snap):
    for p in _db_files(tree):
        p.unlink(missing_ok=True)
    (Path(tree) / "data").mkdir(exist_ok=True)
    if snap is not None:
        shutil.copy2(snap, Path(tree) / "data" / "wqb.db")
    return Path(tree) / "data" / "wqb.db"


def checkpoint(db):
    c = sqlite3.connect(str(db))
    try:
        c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        c.close()


def _out(res):
    return res if isinstance(res, dict) else {"raw": res}


# ----------------------------------------------------------------------------- 同一调用序列
async def sequence(tag, tree, snap, resp):
    H.H1({"base": "修复前（BASE_DIR）", "fixed": "修复后（本工作树）"}[tag] + " · 同一调用序列")
    db = fresh_db(tree, snap)
    rec = {}
    async with H.open_server(f"wqb-db·{tag}", tree, "wqb-db", db) as srv:
        H.H2("⓪ 工具表")
        tools = {t.name: t for t in (await srv.s.list_tools()).tools}
        rec["n_tools"] = len(tools)
        rec["has_harvest"] = "harvest_multisim_results" in tools
        rec["private"] = sorted(n for n in tools if n.startswith("_"))
        rec["wah_params"] = sorted((tools.get("workflow_auto_harvest").inputSchema or {}).get("properties", {}))
        print(f"    {len(tools)} 个工具；harvest_multisim_results 在表里: {rec['has_harvest']}；"
              f"私有函数工具: {rec['private']}；workflow_auto_harvest 参数: {rec['wah_params']}")

        tool, whole, line = sop_harvest_call(tree)
        H.H2(f"① 照本树 SOP 原文调收批入库：{line}")
        args = {"region": R, "wave": S2, "alphas": resp if whole else resp["alphas"]}
        print(f"    alphas 传的是：{'整个返回值' if whole else 'alphas 列表'}（{len(resp['alphas'])} 条）")
        res, err, pr = await srv.call(tool, label=f"{tool}（SOP 原文）", n=420, **args)
        rec["sop"] = {"tool": tool, "isError": err, "out": _out(res), "db_delta": pr.db_delta}

        H.H2("② workflow_auto_harvest 只读报告（真实波 94，导入时已有 9 条回测行）")
        res, err, pr = await srv.call("workflow_auto_harvest", n=420, region=R, wave="94")
        rec["report94"] = {"isError": err, "out": _out(res), "db_delta": pr.db_delta}

        H.H2(f"③ workflow_auto_harvest 带 alphas（整个返回值）：{S2}")
        res, err, pr = await srv.call("workflow_auto_harvest", n=420, region=R, wave=S2, alphas=resp)
        rec["wah"] = {"isError": err, "out": _out(res), "db_delta": pr.db_delta}

    H.H2("库里这批的结果")
    rec["rows"] = H.q(db, "SELECT alpha_id, sharpe, fitness, turnover, two_year_sharpe, sub_universe_sharpe, "
                          "json_extract(payload_json, '$.multisim_id'), json_extract(payload_json, '$.neut') "
                          "FROM backtest_results WHERE alpha_id LIKE ? ORDER BY alpha_id", PREFIX + "%")
    rec["wr"] = H.q(db, "SELECT wave_number, status, verdict, source_file FROM wave_results WHERE wave_number=?", S2)
    rec["pool"] = H.q(db, "SELECT COUNT(*) FROM json_each((SELECT value FROM ledger_kv WHERE region=? "
                          "AND key='salvage_pool'), '$.entries') e WHERE json_extract(e.value, '$.alpha_id') LIKE ?",
                      R, PREFIX + "%")[0][0] if H.q(db, "SELECT 1 FROM ledger_kv WHERE region=? AND key='salvage_pool'", R) else 0
    print(f"    backtest_results（n31_*）{len(rec['rows'])} 行：{H.dump(rec['rows'][:3], 300)}")
    print(f"    wave_results[{S2}]: {rec['wr']}；salvage_pool 里 n31_* 条目: {rec['pool']}")
    return rec


# ----------------------------------------------------------------------------- 主流程
def _ok_report(x):
    out = x.get("out") or {}
    return (not x.get("isError")) and out.get("success") is True


async def body():
    H.H1("N31 真实环境探针 · 步 0 · 环境")
    for tag, tree in (("本工作树", ROOT), ("BASE_DIR", BASE)):
        head = subprocess.run(["git", "-C", str(tree), "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip()
        print(f"  {tag}: {rel(tree)}  HEAD={head or '（git archive 副本，无 .git）'}")
    print("  本工作树未提交改动（= N31 修复）:", sorted(H.git_dirty(ROOT)))
    print("  world-quant-brain-mcp/.env 存在?", (ROOT / "world-quant-brain-mcp" / ".env").exists(), "（只判存在，不读取）")
    resp = platform_response()
    print(f"  输入：harvest_multisim_alphas 返回形态，{resp['total']} 条（KOR 真实 wave94 指标 + 真实 settings），"
          f"multisimulation_id={MSID}；第一条：{H.dump(resp['alphas'][0], 420)}")

    H.H1("步 1 · 导入 tracking/KOR 真实历史（本工作树的 wqb-db server，经 MCP 写工具）")
    db = fresh_db(ROOT, None)
    async with H.open_server("wqb-db·import", ROOT, "wqb-db", db) as srv:
        stats, _t, _s = await H.import_history(srv, ROOT)
    checkpoint(db)
    snap = WORK / "imported.db"
    shutil.copy2(db, snap)
    print(f"  导入：{H.dump(stats, 300)}")
    print(f"  wave 94 回测行: {H.q(snap, 'SELECT COUNT(*) FROM backtest_results WHERE wave=?', '94')[0][0]}")

    out = {tag: await sequence(tag, tree, snap, resp) for tag, tree in (("base", BASE), ("fixed", ROOT))}
    b, f = out["base"], out["fixed"]

    H.H1("N31 验证清单（✅/❌ 判修复后，括号里是修复前的实测）")
    exp = {PREFIX + r["alpha_id"][len(PREFIX):]: r for r in resp["alphas"]}
    rows_ok = len(f["rows"]) == len(exp) and all(
        (sh, fit, tvr, ty, sub) == tuple(exp[aid]["metrics"].get(k) for k in
                                         ("sharpe", "fitness", "turnover", "two_year_sharpe", "sub_universe_sharpe"))
        and ms == MSID and neut == exp[aid]["settings"].get("neutralization")
        for aid, sh, fit, tvr, ty, sub, ms, neut in f["rows"])
    fs, bs = f["sop"], b["sop"]
    items = [
        ("工具表：SOP 的收批入库工具在表里，没有私有函数工具",
         f["has_harvest"] and not f["private"] and f["n_tools"] == b["n_tools"],
         f"修复后：harvest_multisim_results 在表里，私有函数工具 {f['private']}，共 {f['n_tools']} 个",
         f"修复前：harvest_multisim_results 在表里={b['has_harvest']}，私有函数工具 {b['private']}，共 {b['n_tools']} 个"),
        ("照 SOP 原文调收批入库可用",
         not fs["isError"] and fs["out"].get("upserted") == len(exp),
         f"修复后：{fs['tool']} → upserted={fs['out'].get('upserted')}，multisim_id={fs['out'].get('multisim_id')}，"
         f"wave_result={H.dump(fs['out'].get('wave_result'), 90)}；DB Δ={fs['db_delta']}",
         f"修复前：{bs['tool']} → isError={bs['isError']} {H.dump(bs['out'], 90)}"),
        ("平台嵌套输出逐项拍平入库（sharpe/fitness/turnover/2Y/sub/中性化/批次标记）+ 级联结论 + salvage",
         rows_ok and bool(f["wr"]) and f["wr"][0][3] == "harvest:auto" and f["pool"] > 0,
         f"修复后：{len(f['rows'])} 行逐项与输入一致={rows_ok}；wave_results {f['wr']}；salvage 条目 {f['pool']}",
         f"修复前：{len(b['rows'])} 行；wave_results {b['wr']}"),
        ("workflow_auto_harvest 只读报告可用（真实波 94），不写库",
         _ok_report(f["report94"]) and not f["report94"]["db_delta"],
         f"修复后：success={(f['report94']['out'] or {}).get('success')}，"
         f"报告 {H.dump(next((s.get('report') for s in ((f['report94']['out'] or {}).get('output') or {}).get('steps', []) if s.get('report')), None), 160)}；"
         f"DB Δ={f['report94']['db_delta'] or '无'}",
         f"修复前：success={(b['report94']['out'] or {}).get('success')}，error={H.dump((b['report94']['out'] or {}).get('error'), 100)}"),
        ("workflow_auto_harvest 带 alphas：入库 + 报告",
         _ok_report(f["wah"]) and ((f["wah"]["out"] or {}).get("ingest") or {}).get("upserted") == len(exp),
         f"修复后：success={(f['wah']['out'] or {}).get('success')}，ingest={H.dump((f['wah']['out'] or {}).get('ingest'), 160)}",
         f"修复前：success={(b['wah']['out'] or {}).get('success')}，error={H.dump((b['wah']['out'] or {}).get('error'), 100)}"),
    ]
    for title, ok, after, before in items:
        print(f"  {'✅' if ok else '❌'} {title}")
        print(f"       {after}")
        print(f"       （{before}）")
    print(f"\n  结果：{sum(1 for _t, ok, _a, _b in items if ok)}/{len(items)} ✅")


async def main():
    if BASE is None or not (BASE / "wqb_db_mcp.py").is_file():
        sys.exit("需要 BASE_DIR=<N31 修复前的代码树>（见 reproduce_realenv_n31.sh）")
    WORK.mkdir(parents=True, exist_ok=True)
    st = {"fixed": stash(ROOT, "fixed"), "base": stash(BASE, "base")}
    try:
        await body()
    finally:
        restore(ROOT, "fixed", st["fixed"])
        restore(BASE, "base", st["base"])
        print(f"\n[收尾] 两棵树的 data/wqb.db 已复原；演练库留在 {rel(WORK)}/", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
