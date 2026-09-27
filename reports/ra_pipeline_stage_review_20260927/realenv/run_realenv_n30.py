# -*- coding: utf-8 -*-
"""N30 · 真实环境探针：wave_results 两个自动写入方修复前后对照（2026-09-27 第五轮）。

N30：收批级联（wqb-db `harvest_multisim_results` → `_cascade_wave_result`）与 toolkit 评审写入
（`review_wave.py` / pipeline → `_lib/wave_results.WaveResultsStore`）都绕过 P0-1 写入契约、
把字符串波号截成数字；停止闸与写入契约各有一个 verdict 归一器。本脚本在同一份真实历史上把
"修复前代码树"（BASE_DIR）与本工作树各跑一遍同一调用序列，逐步打印 wave_results 的变化，
末尾给验证清单（✅ 修复后符合预期 / ❌ 不符合；每行并列修复前的实测）。

真实的部分（方法同 run_realenv.py）：
  * wqb-db server 按仓库 .mcp.json 的 command/args/env 经 stdio 真实启动，收批走 MCP 协议层；
  * 库 = tracking/KOR 真实历史经 MCP 写工具导入（复用 run_realenv.import_history，与第四轮同一导入）；
  * 评审 = 各自代码树里的 toolkit review_wave.py 真跑（CLI 子进程）；只补 focus = 各自的 campaign.py wave upsert；
    停止规则 = 各自代码树的 `_run_stop_rules_gate`；阈值 = tracking/KOR/config 原件。
替代的部分（本容器无 BRAIN 凭据；本脚本从不读取 world-quant-brain-mcp/.env）：
  * "新一批"平台结果 = KOR 真实 wave94（最近一波 ml_factor_proj，9 条带表达式与指标的真实行）：指标原样，
    只给 alpha_id 加前缀 n30_（与已导入的同一批行区分），按 GEM 标签波号 s2_ml_factor_proj_d1 收批；
  * review_wave.py 的指标读穿缓存（cache/metrics/<id>.json）预置为这 9 行，只含历史文件里有的字段
    （sharpe / fitness / 2Y / turnover / sub-universe；没有 margin / RN / checks）。评审判据要求 margin，
    所以这批在评审里 0 条达标——这是真实评审代码对这份输入的结论，不代表当时平台上的评审结果。
    每个 id 都有缓存，评审不会去登录平台。

副作用：wqb-db server 写死 <tree>/data/wqb.db（N26），演练期间两棵树的该文件被替换为导入快照的副本，
结束（含异常）后移到 $REALENV_SCRATCH/n30/，原有文件移回；战役目录用
$REALENV_SCRATCH/n30/<tree>/tracking/KOR（config 拷自原件）。仓库工作树不留任何文件。

用法：见同目录 reproduce_realenv_n30.sh。
"""
from __future__ import annotations

import asyncio
import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_realenv as H  # noqa: E402  复用：stdio 起服（.mcp.json 原样）、真实历史导入、副作用探针、脱敏

ROOT, BASE, R = H.ROOT, H.BASE_DIR, H.R
WORK = H.SCRATCH / "n30"
S2 = "s2_ml_factor_proj_d1"          # GEM 标签波号（KOR 主数据集 ml_factor_proj、delay 1）
PREFIX = "n30_"
TOOLKIT = Path("Claude") / "skills" / "wq-brain-campaign-toolkit" / "scripts"
ENUM = ("PASS", "FAIL", "PARTIAL")
HOME = str(Path.home())
_rel0 = H.rel


def rel(p):
    return _rel0(p).replace(HOME + os.sep, "~" + os.sep)


H.rel = rel   # run_realenv.sh() 打印命令与输出时同样脱敏家目录


# ----------------------------------------------------------------------------- 输入：真实历史行
def batch_from(wave_key, prefix=""):
    """tracking/KOR/candidates/wave<key>_results.json 的真实行 → 收批入参（平台 alpha 详情的扁平形态）。"""
    f = ROOT / "tracking" / R / "candidates" / f"wave{wave_key}_results.json"
    raw = json.load(open(f, encoding="utf-8"))
    prod = {str(r.get("alpha") or r.get("alpha_id")): r.get("prod_corr")
            for r in (raw.get("results") or raw.get("candidates") or []) if isinstance(r, dict)}
    out = []
    for r in H._rows_of(raw):
        if not (r.get("alpha_id") and r.get("expression") and isinstance(r.get("sharpe"), (int, float))):
            continue
        a = {k: r.get(k) for k in ("expression", "sharpe", "fitness", "turnover", "two_year_sharpe",
                                   "sub_universe_sharpe")}
        a["alpha_id"] = prefix + r["alpha_id"]
        a["prod_correlation"] = prod.get(r["alpha_id"])
        out.append({k: v for k, v in a.items() if v is not None})
    return out


def make_campaign(tag, batch):
    """临时战役目录（config 拷自原件）+ 预置指标读穿缓存；返回路径。"""
    camp = WORK / tag / "tracking" / R
    if camp.exists():
        shutil.rmtree(camp)
    (camp / "cache" / "metrics").mkdir(parents=True)
    shutil.copytree(ROOT / "tracking" / R / "config", camp / "config")
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    for a in batch:
        tvr = a.get("turnover")
        row = {"id": a["alpha_id"], "code": a["expression"], "neut": None,
               "sharpe": a.get("sharpe"), "fitness": a.get("fitness"), "two_year_sharpe": a.get("two_year_sharpe"),
               "margin_bp": None,
               "turnover_pct": (round(tvr * 100, 2) if tvr <= 1 else tvr) if isinstance(tvr, (int, float)) else None,
               "rn_sharpe": None, "rn_fitness": None, "robust_sharpe": None, "robust_limit": None,
               "sub_universe_sharpe": a.get("sub_universe_sharpe"), "sub_universe_limit": None,
               "failed_checks": [], "cached_at": now}
        (camp / "cache" / "metrics" / f"{a['alpha_id']}.json").write_text(
            json.dumps(row, ensure_ascii=False), encoding="utf-8")
    missing = [a["alpha_id"] for a in batch if not (camp / "cache" / "metrics" / f"{a['alpha_id']}.json").is_file()]
    if missing:
        sys.exit(f"指标缓存缺 {missing}：评审会去登录平台，拒跑")
    return camp


# ----------------------------------------------------------------------------- 库：wave_results 的逐行对照
def wr_rows(db):
    c = sqlite3.connect(str(db))
    c.row_factory = sqlite3.Row
    try:
        return {str(r["wave_number"]): dict(r) for r in c.execute("SELECT * FROM wave_results WHERE region=?", (R,))}
    finally:
        c.close()


def _j(s, default):
    try:
        v = json.loads(s) if isinstance(s, str) else s
    except ValueError:
        return default
    return default if v is None else v


def fmt(d):
    if d is None:
        return "（无此行）"
    kf = _j(d.get("key_findings"), [])
    kf = kf if isinstance(kf, list) else [kf]
    fp = _j(d.get("full_payload"), {})
    return (f"status={d.get('status')} verdict={d.get('verdict')!r} source={rel(str(d.get('source_file')))!r} "
            f"focus={H.dump(str(d.get('focus')), 24)!r} "
            f"created_at={d.get('created_at')} candidates={len(_j(d.get('candidates'), []))} "
            f"payload.wave={(fp.get('wave') if isinstance(fp, dict) else None)!r} "
            f"findings[0]={H.dump(kf[0], 72) if kf else None}")


def show_changes(db, before, label):
    after = wr_rows(db)
    changed = [w for w in sorted(set(after) | set(before)) if before.get(w) != after.get(w)]
    print(f"    wave_results 变化（{label}）：{len(changed)} 行" + ("" if changed else "（无）"))
    for w in changed:
        kind = "新增" if w not in before else ("删除" if w not in after else "修改")
        print(f"      [{kind}] wave_number={w!r}: {fmt(after.get(w, before.get(w)))}")
        if kind == "修改":
            print(f"             修改前: {fmt(before[w])}")
    return after, changed


def row_for(rows, wave):
    """该波的结论行：以原字符串为键，或旧版按数字入库、full_payload.wave 记着原字符串的行。"""
    if wave in rows:
        return wave, rows[wave]
    for k, d in rows.items():
        fp = _j(d.get("full_payload"), {})
        if isinstance(fp, dict) and fp.get("wave") == wave:
            return k, d
    return None, None


def py_probe(name, code, args, tree, db, marker):
    """在指定代码树里跑一段探针（env 只补 WQB_DB_PATH）；返回解析出的 JSON。"""
    path = WORK / f"{name}.py"
    path.write_text(code, encoding="utf-8")
    p, _ = H.sh([H.PY, str(path)] + [str(a) for a in args], env_extra={"WQB_DB_PATH": str(db)},
                cwd=tree, tail=3, root=tree, db=db)
    line = H.line_of(p.stdout, "^" + marker + " ")
    return json.loads(line[len(marker) + 1:]) if line else None


GATE_CODE = r'''
import json, sys
tree, camp = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree + "/src")
from wqb.workflow.nodes import campaign as C
out = C._run_stop_rules_gate("KOR", None, camp)
ev = out.get("evidence") or {}
print("N30_GATE " + json.dumps({"success": out.get("success"), "hits": out.get("hits"), "warning": out.get("warning"),
      "waves": ev.get("recent_closed_waves"), "verdicts": ev.get("recent_closed_verdicts"),
      "raw": ev.get("recent_closed_verdicts_raw")}, ensure_ascii=False, default=str))
'''

HARVEST_CODE = r'''
import json, sys
tree, region, wave, alphas_path = sys.argv[1:5]
sys.path.insert(0, tree)
import wqb_db_mcp as M          # 该树的 wqb-db 模块；库 = <tree>/data/wqb.db（写死，N26）
out = M.harvest_multisim_results(region, wave, json.load(open(alphas_path, encoding="utf-8")))
print("N30_HARVEST " + json.dumps(out, ensure_ascii=False, default=str))
'''

#: 点塔查询要登录平台（campaign_intel.py pyramid → BrainApiClient.ensure_authenticated）。本容器无凭据，
#: 探针只把这一个子进程换成固定输出（格式同 campaign_intel.py 的 [key_findings] 单行，内容标明是替身），
#: 节点代码与库都是真的。
PYRAMID_CODE = r'''
import json, sys, types
tree, wave = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree + "/src")
from wqb.workflow.nodes import auto_pyramid as P
OUT = "category  alpha_count need status\n\n[key_findings] KOR/D1 点塔 ?/? 已点亮(探针替身) 未点亮(探针替身)\n"
P.subprocess.run = lambda *a, **k: types.SimpleNamespace(returncode=0, stdout=OUT, stderr="")
res = []
for _ in range(2):
    o = P.run("KOR", wave)
    emb = next((s for s in o.get("steps", []) if s.get("step") == "auto_embed"), {})
    res.append({"success": o.get("success"), "error": o.get("error"), "embedded": emb.get("embedded"),
                "note": emb.get("note") or emb.get("error")})
print("N30_PYR " + json.dumps(res, ensure_ascii=False, default=str))
'''

NORM_CODE = r'''
import json, sys
tree, texts_path = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree + "/src")
from wqb.workflow.nodes import campaign as C
from wqb.wave_results_contract import normalize_verdict
texts = json.load(open(texts_path, encoding="utf-8"))
diff = []
for t in texts:
    g, c = C._normalize_verdict(t), (normalize_verdict(t)[0] or "UNKNOWN")
    if g != c:
        diff.append([t, g, c])
print("N30_NORM " + json.dumps({"n": len(texts), "diff": diff}, ensure_ascii=False))
'''


# ----------------------------------------------------------------------------- 默认库移开 / 移回
def _db_files(tree):
    return [Path(tree) / "data" / f"wqb.db{s}" for s in ("", "-wal", "-shm")]


def stash_default_db(tree, tag):
    db = Path(tree) / "data" / "wqb.db"
    if db.exists() and db.stat().st_size > 5_000_000 and os.environ.get("REALENV_ALLOW_DB_SWAP") != "1":
        sys.exit(f"{rel(db)} 像是生产库（{db.stat().st_size} bytes）。演练会把它临时移走、结束后移回；"
                 "确认后设 REALENV_ALLOW_DB_SWAP=1 再跑。")
    saved = []
    for p in _db_files(tree):
        if p.exists():
            dst = WORK / f"{tag}.{p.name}.before_n30"
            shutil.move(str(p), str(dst))
            saved.append((dst, p))
    return saved, (Path(tree) / "data").is_dir()


def restore_default_db(tree, tag, stash):
    saved, had_dir = stash
    for p in _db_files(tree):
        if p.exists():
            shutil.move(str(p), str(WORK / f"{tag}.{p.name}.after_n30"))
    for dst, p in saved:
        shutil.move(str(dst), str(p))
    data = Path(tree) / "data"
    if not had_dir and data.is_dir() and not any(data.iterdir()):
        data.rmdir()


def fresh_db(tree, snap):
    for p in _db_files(tree):
        p.unlink(missing_ok=True)
    (Path(tree) / "data").mkdir(exist_ok=True)
    shutil.copy2(snap, Path(tree) / "data" / "wqb.db")
    return Path(tree) / "data" / "wqb.db"


def checkpoint(db):
    c = sqlite3.connect(str(db))
    try:
        c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        c.close()


# ----------------------------------------------------------------------------- 同一调用序列
WATCH = ("2", "91", "91c", "94", S2)


def _wr(x):
    return x.get("wave_result") if isinstance(x, dict) else x


def run_gate(tag, tree, camp, db, label):
    gate = py_probe(f"n30_gate_{tag}", GATE_CODE, [tree, camp], tree, db, "N30_GATE") or {}
    print(f"    [{label}] 窗口 {gate.get('waves')} → 归一后 {gate.get('verdicts')}（原文 {H.dump(gate.get('raw'), 150)}）")
    print(f"    [{label}] success={gate.get('success')} hits={gate.get('hits')}")
    return gate


async def sequence(tag, tree, snap, batch, b94, b91c):
    name = {"base": "修复前（BASE_DIR，N30 修复前的提交）", "fixed": "修复后（本工作树）"}[tag]
    H.H1(f"{name} · 同一调用序列")
    db = fresh_db(tree, snap)
    camp = make_campaign(tag, batch)
    ids = [a["alpha_id"] for a in batch]
    rec = {}
    before = wr_rows(db)
    H.H2("⓪ SOP 的手动补收入口（ra-pipeline SKILL.md:405 `mcp__wqb-db__harvest_multisim_results`）在 MCP 层是否存在")
    async with H.open_server(f"wqb-db·{tag}", tree, "wqb-db", db) as srv:
        names = sorted(t.name for t in (await srv.s.list_tools()).tools)
        rec["mcp_tools"] = {n: n in names for n in ("harvest_multisim_results", "workflow_auto_harvest",
                                                    "upsert_wave_result", "workflow_auto_pyramid")}
        print(f"    wqb-db 注册工具 {len(names)} 个；其中 {rec['mcp_tools']}")
        res, err, _ = await srv.call("harvest_multisim_results", label="harvest_multisim_results（按 SOP 原样调用）",
                                     n=200, region=R, wave=S2, alphas=batch[:1])
        rec["mcp_harvest"] = {"isError": err, "out": res}
    print("    → 726a350（2026-09-19）把它降级为内部函数、未改 SOP；以下三次收批在本树里直接调用该函数（原 MCP 工具同一函数体）")

    def harvest(label, wave, alphas):
        ap = WORK / f"{tag}_alphas_{wave}.json"
        ap.write_text(json.dumps(alphas, ensure_ascii=False), encoding="utf-8")
        out = py_probe(f"n30_harvest_{tag}", HARVEST_CODE, [tree, R, wave, ap], tree, db, "N30_HARVEST")
        print(f"    harvest_multisim_results({R}, {wave!r}, {len(alphas)} 条) → {H.dump(out, 360)}")
        return out

    H.H2(f"① 收批 GEM 标签波 {S2}（{len(batch)} 条真实指标）")
    rec["A1_out"] = harvest("A1", S2, batch)
    before, rec["A1_changed"] = show_changes(db, before, f"收批 {S2}")
    rec["bt_waves"] = sorted({w for (w,) in H.q(db, "SELECT DISTINCT wave FROM backtest_results WHERE alpha_id LIKE ?",
                                               PREFIX + "%")})
    pool = H.q(db, "SELECT value FROM ledger_kv WHERE region=? AND key='salvage_pool'", R)
    pool = _j(pool[0][0], {}) if pool else {}
    rec["pool_waves"] = sorted({str(e.get("wave")) for e in (pool.get("entries") or [])
                                if str(e.get("alpha_id", "")).startswith(PREFIX)})
    print(f"    这批在 backtest_results 的波号: {rec['bt_waves']}；salvage_pool 条目的波号: {rec['pool_waves']}")

    H.H2("② 补收已结案的真实波 94（人按 PROD 相关写的 RED → 导入为 FAIL）")
    rec["A2_out"] = harvest("A2", "94", b94)
    before, rec["A2_changed"] = show_changes(db, before, "补收 94")

    H.H2("③ 补收真实波 91c（原 verdict 无法归一，导入为 open）")
    rec["A3_out"] = harvest("A3", "91c", b91c)
    before, rec["A3_changed"] = show_changes(db, before, "补收 91c")
    rec["after_harvest"] = before

    H.H2(f"④ 评审（本树 toolkit review_wave.py 真跑：--alphas 这 {len(ids)} 条 --tag {S2}）")
    review = [H.PY, str(Path(tree) / TOOLKIT / "review_wave.py"), "--campaign-dir", str(camp),
              "--alphas", *ids, "--tag", S2, "--coverage-writeback", "never"]
    p, _ = H.sh(review, env_extra={"WQB_DB_PATH": str(db)}, cwd=tree, tail=6, root=tree, db=db)
    rec["review_exit"] = p.returncode
    before, rec["B1_changed"] = show_changes(db, before, "评审")
    rec["review_key"], r1 = row_for(before, S2)
    rec["review_row"] = r1

    H.H2("⑤ 隔两秒重评同一波（重跑评审）")
    time.sleep(2.1)
    H.sh(review, env_extra={"WQB_DB_PATH": str(db)}, cwd=tree, tail=2, root=tree, db=db)
    before, rec["B2_changed"] = show_changes(db, before, "重评")
    _, r2 = row_for(before, S2)
    rec["created"] = ((r1 or {}).get("created_at"), (r2 or {}).get("created_at"))
    print(f"    结论行 created_at：评审 {rec['created'][0]} → 重评 {rec['created'][1]}")

    H.H2("⑥ 停止规则 B（本树 _run_stop_rules_gate 读这个库；窗口 = 按波的开始时刻取最近 3 个 closed 波）")
    rec["gate"] = run_gate(tag, tree, camp, db, "评审后")
    checkpoint(db)
    shutil.copy2(db, WORK / f"{tag}_after_review.db")   # 升级路径（步 9）从修复前这一刻的库起步

    H.H2("⑦ 只补写 focus（本树 toolkit：campaign.py wave upsert，不带 --status / --verdict）")
    cli = [H.PY, str(Path(tree) / TOOLKIT / "campaign.py"), "--campaign-dir", str(camp), "wave", "upsert",
           "--focus", "N30 探针：只补 focus"]
    p, _ = H.sh(cli + ["--wave", S2], env_extra={"WQB_DB_PATH": str(db)}, cwd=tree, tail=3, root=tree, db=db)
    rec["cli_exit"] = p.returncode
    key = rec["review_key"]
    if p.returncode != 0 and key and key != S2:
        print(f"    （该版本认不出字符串波号；改用它自己写的数字键 {key!r} 再补一次）")
        H.sh(cli + ["--wave", key], env_extra={"WQB_DB_PATH": str(db)}, cwd=tree, tail=3, root=tree, db=db)
    before, rec["C_changed"] = show_changes(db, before, "只补 focus")
    rec["after_cli"] = row_for(before, S2)[1] or (before.get(key) if key else None)

    H.H2(f"⑧ 点塔进度回写（本树 auto_pyramid 节点，对 {S2} 连跑两次；只把平台点塔查询换成替身输出）")
    pyr = py_probe(f"n30_pyramid_{tag}", PYRAMID_CODE, [tree, S2], tree, db, "N30_PYR") or []
    for i, o in enumerate(pyr, 1):
        print(f"    第 {i} 次: success={o.get('success')} embedded={o.get('embedded')} "
              f"error={H.dump(o.get('error'), 90) if o.get('error') else None} note={H.dump(o.get('note'), 90) if o.get('note') else None}")
    before, rec["P_changed"] = show_changes(db, before, "点塔回写 ×2")
    rec["pyramid"] = pyr
    k_now, r_now = row_for(before, S2)
    kf = _j((r_now or {}).get("key_findings"), [])
    rec["pyramid_lines"] = [str(x) for x in (kf if isinstance(kf, list) else [kf]) if str(x).startswith("[pyramid]")]
    print(f"    {S2} 的结论行: {k_now!r}" + ("（库里找不到这一波的结论行）" if k_now is None else "")
          + f"；其中 [pyramid] 行 {len(rec['pyramid_lines'])} 条 {[H.dump(x, 80) for x in rec['pyramid_lines']]}")

    H.H2("⑨ 停止规则 B（补 focus、点塔回写之后再判一次）")
    rec["gate2"] = run_gate(tag, tree, camp, db, "最后")
    rec["rows"] = before
    print("    本序列涉及各行的最终状态：")
    for w in WATCH + ((key,) if key and key not in WATCH else ()):
        print(f"      {w!r}: {fmt(before.get(w))}")
    return rec


#: 报告 §14.10 给出的生产库审计查询（只读），这里原样按区域过滤后使用：
#: ① 旧版评审的数字键行（full_payload.wave 与键不一致）；② verdict 不是枚举的行（旧收批级联的自由文本），
#: 附带其候选 alpha 实际属于哪一波（按 backtest_results）。
AUDIT_SQL = (
    "SELECT 'legacy_key', wave_number, verdict, status, json_extract(full_payload, '$.wave') FROM wave_results "
    "WHERE region=? AND json_extract(full_payload, '$.wave') IS NOT NULL "
    "AND CAST(json_extract(full_payload, '$.wave') AS TEXT) != CAST(wave_number AS TEXT) "
    "UNION ALL "
    "SELECT 'free_text', wr.wave_number, wr.verdict, wr.status, "
    "(SELECT GROUP_CONCAT(DISTINCT br.wave) FROM json_each(COALESCE(wr.candidates, '[]')) c "
    " JOIN backtest_results br ON br.alpha_id = json_extract(c.value, '$.alpha_id')) "
    "FROM wave_results wr WHERE wr.region=? AND wr.verdict IS NOT NULL "
    "AND wr.verdict NOT IN ('PASS', 'FAIL', 'PARTIAL')")


async def upgrade(batch):
    """修复后的代码接手修复前留下的库：从修复前评审后的快照起步，用本工作树重评同一波。"""
    H.H1(f"步 7 · 升级路径：修复后的代码接手修复前留下的库（修复前序列 ⑥ 之后的快照），重评 {S2}")
    db = fresh_db(ROOT, WORK / "base_after_review.db")
    camp = make_campaign("upgrade", batch)
    before = wr_rows(db)
    print("  接手前的可疑行（§14.10 审计查询：旧评审的数字键行 / verdict 不是枚举的行及其候选实际所属的波）:")
    for r in H.q(db, AUDIT_SQL, R, R):
        print(f"    {r}")
    review = [H.PY, str(ROOT / TOOLKIT / "review_wave.py"), "--campaign-dir", str(camp),
              "--alphas", *[a["alpha_id"] for a in batch], "--tag", S2, "--coverage-writeback", "never"]
    p, _ = H.sh(review, env_extra={"WQB_DB_PATH": str(db)}, cwd=ROOT, tail=3, root=ROOT, db=db)
    after, changed = show_changes(db, before, "修复后重评")
    gate = run_gate("upgrade", ROOT, camp, db, "接手后")
    left = H.q(db, AUDIT_SQL, R, R)
    print(f"  接手后仍可疑的行（需人工处理）: {left}")
    return {"exit": p.returncode, "changed": changed, "before": before, "after": after, "gate": gate, "left": left}


# ----------------------------------------------------------------------------- 主流程
def verdict_texts(base_rows):
    texts = set()
    for f in glob.glob(str(ROOT / "tracking" / "*" / "candidates" / "wave*_result*.json")):
        try:
            v = json.load(open(f, encoding="utf-8")).get("verdict")
        except Exception:
            continue
        if v is not None and not isinstance(v, (dict, list)):
            texts.add(str(v))
    texts |= {str(r["verdict"]) for r in base_rows.values() if r.get("verdict") and "过硬闸" in str(r["verdict"])}
    return sorted(texts)


def _changed_rows(rec, key):
    return set(rec.get(key) or [])


async def body():
    H.H1("N30 真实环境探针 · 步 0 · 环境")
    for tag, tree in (("本工作树", ROOT), ("BASE_DIR", BASE)):
        head = subprocess.run(["git", "-C", str(tree), "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip()
        print(f"  {tag}: {rel(tree)}  HEAD={head or '（git archive 副本，无 .git）'}")
    print("  本工作树未提交改动（= N30 修复）:", sorted(H.git_dirty(ROOT)))
    print("  world-quant-brain-mcp/.env 存在?", (ROOT / "world-quant-brain-mcp" / ".env").exists(), "（只判存在，不读取）")
    batch = batch_from("94", PREFIX)
    b94, b91c = batch_from("94"), batch_from("91c")
    print(f"  输入：wave94 真实行 {len(batch)} 条（id 加前缀 {PREFIX}）→ 收批 {S2}；补收 94 用原 id {len(b94)} 条；"
          f"补收 91c {len(b91c)} 条")
    for a in batch:
        print(f"    {a['alpha_id']:<14} sharpe={a.get('sharpe')} fitness={a.get('fitness')} "
              f"2Y={a.get('two_year_sharpe')} tvr={a.get('turnover')} prod_corr={a.get('prod_correlation')}")

    H.H1("步 1 · 导入 tracking/KOR 真实历史（本工作树的 wqb-db server，经 MCP 写工具；同第四轮 import_history）")
    for p in _db_files(ROOT):          # 导入从空库开始（原库已在 main() 里移开）
        p.unlink(missing_ok=True)
    db = ROOT / "data" / "wqb.db"
    async with H.open_server("wqb-db·import", ROOT, "wqb-db", db) as srv:
        stats, _table, _sug = await H.import_history(srv, ROOT)
    checkpoint(db)
    snap = WORK / "imported.db"
    shutil.copy2(db, snap)
    rows = wr_rows(snap)
    closed = {w: d.get("verdict") for w, d in rows.items() if d.get("status") == "closed"}
    print(f"  导入：{H.dump(stats, 400)}")
    print(f"  wave_results：{len(rows)} 行（closed {len(closed)} / open {len(rows) - len(closed)}）；closed 行 verdict: {closed}")
    print("  本探针要动到的几行（导入后）：")
    for w in WATCH:
        print(f"    {w!r}: {fmt(rows.get(w))}")

    out = {}
    for tag, tree in (("base", BASE), ("fixed", ROOT)):
        out[tag] = await sequence(tag, tree, snap, batch, b94, b91c)
    b, f = out["base"], out["fixed"]
    real = sorted(glob.glob(str(ROOT / "tracking" / R / "candidates" / f"wave{b['review_key']}_*.json")))
    if b["review_key"] not in (None, S2) and real:
        print(f"\n  注：修复前评审顺延出的 {b['review_key']!r} 是另一个真实存在的 KOR 波"
              f"（{', '.join(os.path.basename(p) for p in real)}；导入后库里没有它的结论行，所以被当成空号）")

    up = await upgrade(batch)

    H.H1("步 8 · 两个 verdict 归一器（停止闸 _normalize_verdict vs 写入契约 normalize_verdict）")
    texts = verdict_texts(b["rows"])
    tp = WORK / "verdict_texts.json"
    tp.write_text(json.dumps(texts, ensure_ascii=False), encoding="utf-8")
    print(f"  样本：全部区域 tracking/*/candidates/wave*_result*.json 的 verdict 原文 + 修复前收批写进库的原文，去重 {len(texts)} 条")
    norm = {}
    for tag, tree in (("base", BASE), ("fixed", ROOT)):
        norm[tag] = py_probe(f"n30_norm_{tag}", NORM_CODE, [tree, tp], tree, snap, "N30_NORM") or {}
        d = norm[tag].get("diff") or []
        print(f"  {tag}: {len(d)}/{norm[tag].get('n')} 条两边结论不同" + ("" if not d else "，如:"))
        for t, g, c in d[:6]:
            print(f"      {H.dump(t, 60)!s:<64} 停止闸={g:<8} 契约={c}")

    # ------------------------------------------------------------------------- 清单
    H.H1("N30 验证清单（同一份真实历史、同一调用序列；✅/❌ 判修复后，括号里是修复前的实测）")
    fs2 = f["after_harvest"].get(S2) or {}
    fs2_payload = _j(fs2.get("full_payload"), {})
    base_harvest_rows = [w for w in b["A1_changed"] if w != S2]
    items = []

    ok = (S2 in f["A1_changed"] and "2" not in f["A1_changed"] and fs2.get("verdict") in ENUM
          and fs2.get("source_file") == "harvest:auto" and f["bt_waves"] == [S2] and set(f["pool_waves"]) <= {S2})
    items.append(("N30a 收批按原波号写、与 backtest_results 同键", ok,
                  f"修复后：{S2}（暂定 {fs2.get('verdict')}，{(fs2_payload.get('harvest') or {}).get('n_pass')} 条过硬闸，"
                  f"source harvest:auto）；backtest 在 {f['bt_waves']}、salvage 记 {f['pool_waves']}",
                  f"修复前：写进 {base_harvest_rows}（verdict "
                  f"{[(b['after_harvest'].get(w) or {}).get('verdict') for w in base_harvest_rows]}）；"
                  f"backtest 在 {b['bt_waves']}、salvage 记 {b['pool_waves']}"))
    ok = not (_changed_rows(f, "A2_changed") | _changed_rows(f, "A3_changed")) and \
        all(str(_wr(f[k]) or "").startswith("kept") for k in ("A2_out", "A3_out"))
    items.append(("N30a 不覆盖人写 / 导入的结论、不动显式 open 的行", ok,
                  f"修复后：94 / 91 / 91c 都不变（{H.dump(_wr(f['A2_out']), 70)}；{H.dump(_wr(f['A3_out']), 60)}）",
                  f"修复前：补收 94 改了 {sorted(_changed_rows(b, 'A2_changed'))}、补收 91c 改了 {sorted(_changed_rows(b, 'A3_changed'))}"))
    frr = f["review_row"] or {}
    fkf = _j(frr.get("key_findings"), [])
    ok = (f["review_key"] == S2 and frr.get("source_file") == "pipeline:auto" and frr.get("verdict") in ENUM
          and not any(str(x).startswith("[harvest]") for x in fkf) and f["review_exit"] == 0)
    items.append(("N30b 评审按原波号写、覆盖收批的暂定结论", ok,
                  f"修复后：{f['review_key']}：{fs2.get('verdict')}（收批暂定）→ {frr.get('verdict')}（评审），"
                  f"source pipeline:auto，[harvest] 摘要已替换",
                  f"修复前：写进 {b['review_key']!r}（full_payload.wave={S2}），{S2} 本身无结论行"))
    ok = f["created"][0] is not None and f["created"][0] == f["created"][1]
    items.append(("N30b 重评保留 created_at（R22 兜底时钟不被重置）", ok,
                  f"修复后：{f['created'][0]} → {f['created'][1]}",
                  f"修复前：{b['created'][0]} → {b['created'][1]}"))
    fac, bac = f["after_cli"] or {}, b["after_cli"] or {}
    ok = f["cli_exit"] == 0 and fac.get("status") == "closed" and fac.get("verdict") == frr.get("verdict")
    items.append(("CLI 只补 focus 不改结论、不改回 open", ok,
                  f"修复后：exit {f['cli_exit']}，{fac.get('status')}/{fac.get('verdict')}",
                  f"修复前：--wave {S2} exit {b['cli_exit']}（波号只收整数）；改用 {b['review_key']!r} 后 "
                  f"{bac.get('status')}/{bac.get('verdict')!r}"))
    fw, bw = f["gate"].get("waves") or [], b["gate"].get("waves") or []
    fw2, bw2 = f["gate2"].get("waves") or [], b["gate2"].get("waves") or []
    ghosts = set(base_harvest_rows) | ({b["review_key"]} if b["review_key"] not in (None, S2) else set())
    ok = fw.count(S2) == 1 and fw2 == fw and not ghosts & (set(fw) | set(fw2))
    items.append(("停止规则 B 窗口：一波只占一格、没有幽灵波号，补 focus / 点塔回写不改变窗口", ok,
                  f"修复后：评审后 {fw} → {f['gate'].get('verdicts')}；最后 {fw2}；"
                  f"拦截={f['gate2'].get('success') is False}",
                  f"修复前：评审后 {bw} → {b['gate'].get('verdicts')}（{sorted(ghosts & set(bw))} 都是 {S2} 这一波）；"
                  f"最后 {bw2} → {b['gate2'].get('verdicts')}；拦截={b['gate2'].get('success') is False}"))
    fp, bp = f.get("pyramid") or [], b.get("pyramid") or []
    fr_final = row_for(f["rows"], S2)[1] or {}
    ok = (len(fp) == 2 and all(o.get("success") and o.get("embedded") for o in fp) and len(f["pyramid_lines"]) == 1
          and fr_final.get("verdict") == frr.get("verdict") and fr_final.get("status") == "closed")
    items.append(("N30d 点塔回写走契约：写进这一波、重跑不重复、结论不动", ok,
                  f"修复后：两次 success/embedded={[(o.get('success'), o.get('embedded')) for o in fp]}，"
                  f"[pyramid] 行 {len(f['pyramid_lines'])} 条，{fr_final.get('status')}/{fr_final.get('verdict')}",
                  f"修复前：两次 success/embedded={[(o.get('success'), o.get('embedded')) for o in bp]}，"
                  f"但 {S2} 没有以原字符串为键的行，实际写入 {len(b['pyramid_lines'])} 条"))
    nd_f, nd_b = norm["fixed"].get("diff") or [], norm["base"].get("diff") or []
    items.append(("N30c 停止闸与写入契约同一张归一表", not nd_f and bool(norm["fixed"].get("n")),
                  f"修复后：{len(nd_f)}/{norm['fixed'].get('n')} 条不同",
                  f"修复前：{len(nd_b)}/{norm['base'].get('n')} 条不同"))
    bk = b["review_key"]
    ub, ua = up["before"].get(bk) or {}, up["after"].get(S2) or {}
    ok = (up["exit"] == 0 and bk not in (None, S2) and bk not in up["after"] and ua.get("verdict") in ENUM
          and ua.get("created_at") == ub.get("created_at") and ua.get("source_file") == "pipeline:auto")
    items.append(("升级：修复后的代码认领修复前评审写下的数字键行", ok,
                  f"接手后：{bk!r} → {S2!r}（created_at {ua.get('created_at')} 原样保留，{ua.get('status')}/"
                  f"{ua.get('verdict')}）；规则 B 窗口 {up['gate'].get('waves')}",
                  f"仍需人工处理：{[(r[1], r[0], r[4]) for r in up['left']]}——旧收批级联新写或改写的行（最后一项 = 候选实际所属的波）：没有 full_payload.wave，自动认领认不出，按 §14.10 人工处理"))
    for title, ok, after, before in items:
        print(f"  {'✅' if ok else '❌'} {title}")
        print(f"       {after}")
        print(f"       （{before}）")
    print(f"\n  结果：{sum(1 for _t, ok, _a, _b in items if ok)}/{len(items)} ✅")

    H.H1("本轮新发现（不在 N30 修复范围内，另行决定）")
    mt, mh = f.get("mcp_tools") or {}, f.get("mcp_harvest") or {}
    print(f"  · SOP 的手动补收入口不存在：wqb-db 注册表 {mt}；按 SOP 调用 → isError={mh.get('isError')} "
          f"{H.dump(mh.get('out'), 120)}。两棵树相同（726a350 起）。`workflow_auto_harvest` 只按 multisim_id 读库里已有的"
          f"回测行，不接收平台 alpha 列表，也不写 wave_results——SOP 那一步（平台结果入库 + 级联结论）目前没有 MCP 入口。")


async def main():
    if BASE is None or not (BASE / "wqb_db_mcp.py").is_file():
        sys.exit("需要 BASE_DIR=<N30 修复前的代码树>（见 reproduce_realenv_n30.sh）")
    WORK.mkdir(parents=True, exist_ok=True)
    stash = {"fixed": stash_default_db(ROOT, "fixed"), "base": stash_default_db(BASE, "base")}
    try:
        await body()
    finally:
        restore_default_db(ROOT, "fixed", stash["fixed"])
        restore_default_db(BASE, "base", stash["base"])
        print(f"\n[收尾] 两棵树的 data/wqb.db 已复原；演练库留在 {rel(WORK)}/", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
