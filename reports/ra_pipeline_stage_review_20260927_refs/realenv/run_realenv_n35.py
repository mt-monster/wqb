# -*- coding: utf-8 -*-
"""N35 · 真实环境探针：同一 alpha 再次入库时 alphas / backtest_results 按合并写，修复前后对照（2026-09-28 第八轮）。

N35（报告 §14.12.3 / §14.13）：`CampaignStore.upsert_backtest_rows` 同步 alphas 时每一列都取行里的值，行里没带就写
NULL 或缺省值——一次 toolkit 重评审就把已提交的 alpha 改回 UNSUBMITTED、清空提交时间与相关性，提交队列随后把它
放回 READY。`upsert_alpha_from_platform`（tools/sync_platform_alphas 的写入口）同样整行覆盖；backtest_results 的
ON CONFLICT 也把行里没带的指标清成 NULL。

方法（同 run_realenv.py）：wqb-db server 按仓库 .mcp.json 经 stdio 真实启动，收批走 MCP 协议层；平台同步、相关性落库、
toolkit 重评审、提交队列都在各自代码树的子进程里跑真实代码。修复前的代码树（BASE_DIR，默认 main 的 023bdb9）与本工作
树各用一个空库跑同一条 alpha 生命周期：
  ① 收批入库：harvest_multisim_results（精简形态 = mcp_core._slim_alpha + alpha_id / expression），点名数据集 probe_ds
  ② 相关性检查落库：CampaignStore.persist_correlation（source=platform_sync）
  ③ 提交后平台同步：tools/sync_platform_alphas 的真实转换 to_store_payload → upsert_alpha_from_platform
     → upsert_alpha_os_metrics（与该工具一样只补"本地还没记提交"的 alpha）
  ④ toolkit 重评审：metrics_cache.row_from_alpha → _lib.wqb_store.get_store → save_backtest_results（没点名数据集）
  ⑤ 事后补收：再调一次 harvest_multisim_results（没点名数据集）
  ⑥ 读取方：提交队列 enqueue_from_alphas；区域 ACTIVE 计数（tools/region_status 的查询）；sync 的"本地已提交台账"
     （date_submitted IS NOT NULL）；get_mining_yield 的 prod_clean / prod_blocked
载荷：tracking/mining/result_submit_* 的 11 条真实平台 checks 与指标（USA；记录里没有表达式，用占位式 rank(n35_<id>)）
与真实载荷裁剪件 tests/fixtures/alpha_detail_cluster_sample.json（IND，平台上已 DECOMMISSIONED）。其中 4 条走③成为
已提交（3 条 USA 记 ACTIVE、裁剪件记 DECOMMISSIONED）；提交时间、OS 段与相关性数值是构造值。

副作用：wqb-db server 写死 <tree>/data/wqb.db（N26），两棵树的该文件在演练期间换成空库，结束（含异常）后移到
$REALENV_SCRATCH/n35/，原有文件移回。本容器无 BRAIN 凭据，脚本不读 .env。用法见同目录 reproduce_realenv_n35.sh。
"""
from __future__ import annotations

import asyncio
import copy
import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_realenv as H  # noqa: E402  复用：stdio 起服（.mcp.json 原样）、副作用探针、脱敏

ROOT, BASE = H.ROOT, H.BASE_DIR
WORK = H.SCRATCH / "n35"
HOME = str(Path.home())
_rel0 = H.rel


def rel(p):
    return _rel0(p).replace(HOME + os.sep, "~" + os.sep)


H.rel = rel

if str(ROOT / "world-quant-brain-mcp") not in sys.path:
    sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))

FIXTURE = ROOT / "tests" / "fixtures" / "alpha_detail_cluster_sample.json"
WAVE = "n35_w1"
DATASET = "probe_ds"
SUBMITTED_USA = 3                                   # 前 3 条（按 alpha_id 排序）USA 记为 ACTIVE
DATE = "2026-09-21T10:15:00-04:00"
CORR = (0.62, 0.41)                                 # ② 相关性检查的构造值（prod, self）
COLS = ("status", "platform_status", "date_submitted", "stage", "two_year_sharpe", "prod_correlation",
        "prod_corr_source", "dataset", "returns", "long_count", "sharpe")

SYNC_SCRIPT = r'''
# tools/sync_platform_alphas.py 的回填段：to_store_payload → upsert_alpha_from_platform（只补本地没记提交的）
# → upsert_alpha_os_metrics
import json, os, sys
for p in ("src", "tools"):
    sys.path.insert(0, os.path.join(os.getcwd(), p))
from sync_platform_alphas import to_store_payload
from wqb.store import CampaignStore
db, spec = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
st = CampaignStore(db)
stats = {"backfilled_alpha": 0, "os": 0}
try:
    local = {r[0] for r in st.connection.execute("SELECT alpha_id FROM alphas WHERE date_submitted IS NOT NULL")}
    for a in spec["objects"]:
        payload = to_store_payload(a)
        os_data = payload.pop("os_data")
        if payload["alpha_id"] not in local:
            st.upsert_alpha_from_platform(payload)
            stats["backfilled_alpha"] += 1
        st.upsert_alpha_os_metrics(payload["alpha_id"], os_data, region=payload.get("region"),
                                   submitted_info={k: payload.get(k) for k in
                                                   ("platform_status", "stage", "alpha_type", "date_submitted",
                                                    "expression")})
        stats["os"] += 1
finally:
    st.close()
print(json.dumps(stats))
'''

CORR_SCRIPT = r'''
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
from wqb.store import CampaignStore
db, spec = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
st = CampaignStore(db)
try:
    out = [st.persist_correlation(aid, prod=p, self_=s, source="platform_sync") for aid, p, s in spec["corr"]]
finally:
    st.close()
print(json.dumps({"persisted": sum(1 for r in out if "skipped" not in r)}))
'''

TOOLKIT_SCRIPT = r'''
# pipeline stage_review 的写法：先取指标行（metrics_cache.fetch_rows → row_from_alpha），再 get_store → save_backtest_results
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "Claude", "skills", "wq-brain-campaign-toolkit", "scripts"))
import metrics_cache
spec = json.load(open(sys.argv[1], encoding="utf-8"))
rows_by_region = {region: [metrics_cache.row_from_alpha(aid, payload) for aid, payload in items]
                  for region, items in sorted(spec["by_region"].items())}
from _lib.wqb_store import get_store
st = get_store(None)
n = 0
try:
    for region, rows in rows_by_region.items():
        n += st.save_backtest_results(region, spec["wave"], rows)
finally:
    st.close()
print(json.dumps({"rows": sum(map(len, rows_by_region.values())), "written": n}))
'''

ENQUEUE_SCRIPT = r'''
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
from wqb.store.submit_queue import enqueue_from_alphas
print(json.dumps({"enqueued": enqueue_from_alphas(db_path=sys.argv[1], note="n35 probe", dedup=False)}))
'''


# ----------------------------------------------------------------------------- 输入
def payloads():
    """{alpha_id: GET /alphas/{id} 形态}：11 条真实平台 checks（USA）+ 真实载荷裁剪件（IND）。"""
    out = {}
    for f in sorted(glob.glob(str(ROOT / "tracking" / "mining" / "result_submit_*.json"))):
        aid = Path(f).name.split("_")[2]
        if aid in out:
            continue
        for ln in open(f, encoding="utf-8-sig").read().splitlines():
            if not ln.startswith("data:"):
                continue
            try:
                res = ((json.loads(ln[5:]).get("result") or {}).get("structuredContent") or {}).get("result")
            except (ValueError, AttributeError):
                continue
            cr = res.get("check_result") if isinstance(res, dict) else None
            if isinstance(cr, dict) and isinstance(cr.get("is_checks_summary"), list):
                m = cr.get("metrics") or {}
                out[aid] = {"id": aid, "type": "REGULAR", "status": "UNSUBMITTED",
                            "settings": {"region": m.get("region"), "universe": "TOP3000", "delay": 1,
                                         "neutralization": "SUBINDUSTRY"},
                            "regular": {"code": f"rank(n35_{aid})"},
                            "is": {**{k: m[k] for k in ("sharpe", "fitness", "turnover", "margin", "returns",
                                                        "drawdown") if m.get(k) is not None},
                                   "checks": cr["is_checks_summary"]}}
                break
    fx = json.loads(FIXTURE.read_text(encoding="utf-8"))
    fx.update(status="UNSUBMITTED", regular={"code": "rank(n35_fixture_cluster)"})
    out[fx["id"]] = fx
    return out


def platform_objects(pl, submitted):
    """③ 平台 OS 池列表里的对象（提交之后的样子）：status / stage / dateSubmitted / os 段为构造值。"""
    objs = []
    for aid in submitted:
        a = copy.deepcopy(pl[aid])
        a.update(status="DECOMMISSIONED" if (a.get("settings") or {}).get("region") == "IND" else "ACTIVE",
                 stage="OS", dateSubmitted=DATE,
                 os={"startDate": "2023-01-21", "sharpe": 0.61, "fitness": 0.4, "osISSharpeRatio": 0.31})
        objs.append(a)
    return objs


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
            dst = WORK / f"{tag}.{p.name}.before_n35"
            shutil.move(str(p), str(dst))
            saved.append((dst, p))
    return saved, (Path(tree) / "data").is_dir()


def restore(tree, tag, st):
    saved, had_dir = st
    for p in _db_files(tree):
        if p.exists():
            shutil.move(str(p), str(WORK / f"{tag}.{p.name}.after_n35"))
    for dst, p in saved:
        shutil.move(str(dst), str(p))
    data = Path(tree) / "data"
    if not had_dir and data.is_dir() and not any(data.iterdir()):
        data.rmdir()


def fresh_db(tree):
    for p in _db_files(tree):
        p.unlink(missing_ok=True)
    (Path(tree) / "data").mkdir(exist_ok=True)
    return Path(tree) / "data" / "wqb.db"


def _last_json(text):
    for ln in reversed((text or "").strip().splitlines()):
        try:
            return json.loads(ln)
        except ValueError:
            continue
    return None


def snapshot(db, ids):
    rows = H.q(db, "SELECT a.alpha_id, a.status, a.platform_status, a.date_submitted, a.stage, a.two_year_sharpe, "
                   "a.prod_correlation, a.prod_corr_source, d.name, a.returns, a.long_count, a.sharpe FROM alphas a "
                   "LEFT JOIN datasets d ON d.id = a.dataset_id")
    return {r[0]: dict(zip(COLS, r[1:])) for r in rows if r[0] in ids}


def _slim(pl, aids, status=None):
    import mcp_core  # noqa: PLC0415  wq-brain-http 的精简实现（两棵树里同一份）

    out = []
    for aid in aids:
        p = copy.deepcopy(pl[aid])
        if status:
            p["status"] = status.get(aid, p.get("status"))
        s = mcp_core._slim_alpha(p)
        s["alpha_id"], s["expression"] = aid, p["regular"]["code"]
        out.append(s)
    return out


# ----------------------------------------------------------------------------- 同一条生命周期
async def lifecycle(tag, tree, pl, submitted):
    H.H1({"base": "修复前（BASE_DIR）", "fixed": "修复后（本工作树）"}[tag] + " · 同一条 alpha 生命周期（空库起步）")
    db = fresh_db(tree)
    ids = sorted(pl)
    by_region = {}
    for aid in ids:
        by_region.setdefault(pl[aid]["settings"]["region"], []).append(aid)
    steps = {}

    async with H.open_server(f"wqb-db·{tag}·1", tree, "wqb-db", db) as srv:
        H.H2(f"① 收批入库 harvest_multisim_results（精简形态，点名数据集 {DATASET}）")
        for region, aids in sorted(by_region.items()):
            res, err, _pr = await srv.call("harvest_multisim_results", quiet=True, region=region, wave=WAVE,
                                           alphas=_slim(pl, aids), dataset=DATASET)
            print(f"    {region}: {len(aids)} 条 → upserted={(res or {}).get('upserted')}  isError={err}")
    steps["①收批"] = snapshot(db, ids)

    H.H2(f"② 相关性检查落库 persist_correlation（{len(submitted)} 条，prod={CORR[0]} self={CORR[1]}，构造值）")
    spec = WORK / f"{tag}.corr.json"
    spec.write_text(json.dumps({"corr": [[a, *CORR] for a in submitted]}), encoding="utf-8")
    script = WORK / "corr.py"
    script.write_text(CORR_SCRIPT, encoding="utf-8")
    H.sh([H.PY, str(script), str(db), str(spec)], cwd=tree, root=tree, db=db, tail=2)
    steps["②相关性"] = snapshot(db, ids)

    H.H2("③ 提交后平台同步：sync_platform_alphas.to_store_payload → upsert_alpha_from_platform → upsert_alpha_os_metrics")
    spec = WORK / f"{tag}.sync.json"
    spec.write_text(json.dumps({"objects": platform_objects(pl, submitted)}, ensure_ascii=False), encoding="utf-8")
    script = WORK / "sync.py"
    script.write_text(SYNC_SCRIPT, encoding="utf-8")
    H.sh([H.PY, str(script), str(db), str(spec)], cwd=tree, root=tree, db=db, tail=2)
    steps["③平台同步"] = snapshot(db, ids)

    H.H2("④ toolkit 重评审（pipeline stage_review 的写法，没点名数据集）")
    spec = WORK / f"{tag}.toolkit.json"
    spec.write_text(json.dumps({"wave": WAVE, "by_region": {r: [[a, pl[a]] for a in aids]
                                                            for r, aids in by_region.items()}},
                               ensure_ascii=False), encoding="utf-8")
    script = WORK / "toolkit_write.py"
    script.write_text(TOOLKIT_SCRIPT, encoding="utf-8")
    H.sh([H.PY, str(script), str(spec)], env_extra={"WQB_DB_PATH": str(db)}, cwd=tree, root=tree, db=db, tail=2)
    steps["④重评审"] = snapshot(db, ids)
    rec = {"bt4": {r[0]: r[1:] for r in H.q(db, "SELECT alpha_id, returns, drawdown, long_count, short_count, "
                                                "dataset FROM backtest_results")}}

    async with H.open_server(f"wqb-db·{tag}·2", tree, "wqb-db", db) as srv:
        H.H2("⑤ 事后补收：再调一次 harvest_multisim_results（没点名数据集；平台 status 按提交后的样子）")
        status = {o["id"]: o["status"] for o in platform_objects(pl, submitted)}
        for region, aids in sorted(by_region.items()):
            res, err, _pr = await srv.call("harvest_multisim_results", quiet=True, region=region, wave=WAVE,
                                           alphas=_slim(pl, aids, status))
            print(f"    {region}: {len(aids)} 条 → upserted={(res or {}).get('upserted')}  isError={err}")
        steps["⑤补收"] = snapshot(db, ids)
        H.H2("⑥ 读取方：get_mining_yield（严格口径）")
        y, _err, _pr = await srv.call("get_mining_yield", n=500)
        rec["yield"] = (y or {}).get("totals") if isinstance(y, dict) else {}

    H.H2("⑥ 读取方：提交队列 enqueue_from_alphas（本树 src，dedup 关）")
    have = {r[1] for r in H.q(db, "PRAGMA table_info(alphas)")}
    miss = [c for c in ("soft_deleted", "disposition") if c not in have]
    if miss:
        conn = sqlite3.connect(str(db))
        try:
            for c in miss:
                conn.execute(f"ALTER TABLE alphas ADD COLUMN {c} {'INTEGER DEFAULT 0' if c == 'soft_deleted' else 'TEXT'}")
            conn.commit()
        finally:
            conn.close()
        print(f"    注：CampaignStore 建的 alphas 表没有 {miss}（N33，两棵树相同），演练库补上后再入队")
    script = WORK / "enqueue.py"
    script.write_text(ENQUEUE_SCRIPT, encoding="utf-8")
    H.sh([H.PY, str(script), str(db)], cwd=tree, root=tree, db=db, tail=2)
    rec["queue"] = {a: (g, s) for a, g, s in H.q(db, "SELECT alpha_id, gate, status FROM submit_ready")}
    rec["active"] = dict(H.q(db, "SELECT r.name, COUNT(*) FROM alphas a JOIN regions r ON a.region_id=r.id "
                                 "WHERE UPPER(COALESCE(a.platform_status,''))='ACTIVE' GROUP BY r.name"))
    rec["ledger"] = sorted(a for (a,) in H.q(db, "SELECT alpha_id FROM alphas WHERE date_submitted IS NOT NULL"))
    rec["steps"] = steps
    return rec


def _fmt(s):
    return (f"{s['status']}/{s['platform_status']}/{'有' if s['date_submitted'] else '无'}提交时间/{s['stage']} "
            f"2Y={s['two_year_sharpe']} prod={s['prod_correlation']}({s['prod_corr_source']}) ds={s['dataset']} "
            f"ret={s['returns']} long={s['long_count']}")


# ----------------------------------------------------------------------------- 主流程
async def body():
    H.H1("N35 真实环境探针 · 步 0 · 环境与输入")
    for tag, tree in (("本工作树", ROOT), ("BASE_DIR", BASE)):
        head = subprocess.run(["git", "-C", str(tree), "log", "--oneline", "-1"], capture_output=True,
                              text=True).stdout.strip()
        print(f"  {tag}: {rel(tree)}  HEAD={head or '（git archive 副本，无 .git）'}")
    print("  本工作树未提交改动（= N35 修复）:", sorted(H.git_dirty(ROOT)))
    print("  world-quant-brain-mcp/.env 存在?", (ROOT / "world-quant-brain-mcp" / ".env").exists(), "（只判存在，不读取）")
    pl = payloads()
    usa = sorted(a for a in pl if pl[a]["settings"]["region"] == "USA")
    ind = sorted(a for a in pl if pl[a]["settings"]["region"] == "IND")
    submitted = usa[:SUBMITTED_USA] + ind
    print(f"  载荷 {len(pl)} 条：USA {len(usa)}（真实平台 checks）+ IND {len(ind)}（真实载荷裁剪件）")
    print(f"  走③成为已提交的 {len(submitted)} 条：{submitted}（USA 记 ACTIVE、IND 记 DECOMMISSIONED）")

    out = {tag: await lifecycle(tag, tree, pl, submitted) for tag, tree in (("base", BASE), ("fixed", ROOT))}
    b, f = out["base"], out["fixed"]

    H.H1("逐步对照：一条已提交的 alpha（修复前 → 修复后）")
    probe = submitted[0]
    for step in b["steps"]:
        print(f"  {step:<7} 修复前 {_fmt(b['steps'][step][probe])}")
        print(f"  {'':<7} 修复后 {_fmt(f['steps'][step][probe])}")
    other = usa[-1]
    H.H2(f"对照：一条没提交的 alpha {other}（⑤ 之后）")
    print(f"  修复前 {_fmt(b['steps']['⑤补收'][other])}")
    print(f"  修复后 {_fmt(f['steps']['⑤补收'][other])}")

    H.H1("读取方")
    for tag, rec in (("修复前", b), ("修复后", f)):
        print(f"  {tag}：提交队列里的已提交 alpha {sorted(a for a in rec['queue'] if a in submitted)}（入队共 {len(rec['queue'])} 条）；"
              f"区域 ACTIVE 计数 {rec['active']}；sync 的本地已提交台账 {len(rec['ledger'])} 条；"
              f"get_mining_yield prod_clean={rec['yield'].get('prod_clean')} prod_blocked={rec['yield'].get('prod_blocked')}")

    H.H1("N35 验证清单（✅/❌ 判修复后，括号里是修复前的实测）")
    sub_usa = submitted[:SUBMITTED_USA]
    f3, b3 = f["steps"]["③平台同步"], b["steps"]["③平台同步"]
    f1 = f["steps"]["①收批"]
    kept_sync = all(f3[a]["two_year_sharpe"] == f1[a]["two_year_sharpe"] and f3[a]["dataset"] == DATASET
                    for a in submitted)
    def lifecycle_ok(snap, a):
        want = "DECOMMISSIONED" if a in ind else "ACTIVE"
        return (snap[a]["platform_status"] == want and snap[a]["date_submitted"] == DATE and snap[a]["stage"] == "OS"
                and snap[a]["prod_correlation"] == CORR[0] and snap[a]["dataset"] == DATASET)
    f4, b4, f5, b5 = (f["steps"]["④重评审"], b["steps"]["④重评审"], f["steps"]["⑤补收"], b["steps"]["⑤补收"])
    # ④ 之后立刻取（⑤ 的补收会把收批指标重新写一遍，看不出 ④ 是否清过）；对照 ① 收批时 alphas 里的同名指标
    bt_keep = all((f["bt4"][a][0], f["bt4"][a][2]) == (f1[a]["returns"], f1[a]["long_count"]) for a in pl)
    ex = ind[0]
    upd = all(f4[a]["sharpe"] == pl[a]["is"]["sharpe"] for a in pl)
    items = [
        ("③ 平台同步后，本地回测写进来的 2Y 与数据集归属保留（sync 传 two_year_sharpe=None、字段投票推断不出数据集）",
         kept_sync,
         "修复后：" + "；".join(f"{a} 2Y={f3[a]['two_year_sharpe']} ds={f3[a]['dataset']}" for a in submitted),
         "修复前：" + "；".join(f"{a} 2Y={b3[a]['two_year_sharpe']} ds={b3[a]['dataset']}" for a in submitted)),
        ("④ toolkit 重评审后，已提交 alpha 的提交态 / 提交时间 / 相关性 / 数据集保留",
         all(lifecycle_ok(f4, a) for a in submitted),
         "修复后：" + _fmt(f4[probe]), "修复前：" + _fmt(b4[probe])),
        ("⑤ 事后补收后同上（收批行 status=COMPLETE 不把 ACTIVE 改回去）",
         all(lifecycle_ok(f5, a) for a in submitted),
         "修复后：" + _fmt(f5[probe]), "修复前：" + _fmt(b5[probe])),
        ("回测行：收批写进来的 returns / drawdown / 多空数，在 ④ 重评审后保留（重评审行不带这些）",
         bt_keep,
         f"修复后 ④ 之后 {ex}: returns/drawdown/long/short/dataset={f['bt4'][ex]}",
         f"修复前 ④ 之后 {ex}: returns/drawdown/long/short/dataset={b['bt4'][ex]}"),
        ("行里带了的指标照常更新（④ 的 sharpe = 平台载荷的 sharpe）",
         upd, "修复后逐条相符" if upd else "修复后有不符", "修复前：" + ("逐条相符" if all(
             b4[a]["sharpe"] == pl[a]["is"]["sharpe"] for a in pl) else "有不符")),
        (f"提交队列：已提交的 {len(submitted)} 条不再入队",
         not any(a in f["queue"] for a in submitted),
         f"修复后：已提交的入队 {sorted(a for a in f['queue'] if a in submitted) or '无'}",
         f"修复前：已提交的入队 {[(a, f['queue'].get(a) or b['queue'].get(a)) for a in submitted if a in b['queue']]}"),
        ("区域 ACTIVE 计数与 sync 的本地已提交台账保留",
         f["active"].get("USA") == len(sub_usa) and len(f["ledger"]) == len(submitted),
         f"修复后：ACTIVE {f['active']}，已提交台账 {len(f['ledger'])} 条",
         f"修复前：ACTIVE {b['active']}，已提交台账 {len(b['ledger'])} 条"),
        ("没提交的 alpha：提交相关的列两棵树相同（都没有提交态），本项不改变它们的去留",
         all((b5[a]["platform_status"], b5[a]["date_submitted"]) == (f5[a]["platform_status"], f5[a]["date_submitted"])
             for a in pl if a not in submitted)
         and {a for a in f["queue"] if a not in submitted} == {a for a in b["queue"] if a not in submitted},
         f"修复后入队（未提交）{sorted(a for a in f['queue'] if a not in submitted)}",
         f"修复前入队（未提交）{sorted(a for a in b['queue'] if a not in submitted)}"),
    ]
    for title, ok, after, before in items:
        print(f"  {'✅' if ok else '❌'} {title}")
        print(f"       {after}")
        print(f"       （{before}）")
    print(f"\n  结果：{sum(1 for _t, ok, _a, _b in items if ok)}/{len(items)} ✅")


async def main():
    if BASE is None or not (BASE / "wqb_db_mcp.py").is_file():
        sys.exit("需要 BASE_DIR=<N35 修复前的代码树>（见 reproduce_realenv_n35.sh）")
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
