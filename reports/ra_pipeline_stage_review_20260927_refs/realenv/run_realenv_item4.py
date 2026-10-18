# -*- coding: utf-8 -*-
"""第 4 项 · 真实环境探针：backtest_results.ra_failed_checks 按 RA 唯一定义写，修复前后对照（2026-09-28 第七轮）。

第 4 项（报告 §14.11.3 / §14.12）：这一列唯一的写入方 CampaignStore.upsert_backtest_rows 此前存
`failed_checks or ra_failed_checks`，三条生产路径存进去的实际是"所有 check 里 FAIL 的名字"；读取方（严格产出率、
prod-first 选探针、本地闸门先验、提交队列……）都把空当作"平台 RA 硬闸全过"。修复后这一列按 wqb.config 的
RA 唯一定义（R3）写：18 项 RA check 里 result 既不是 PASS 也不是 PENDING 的。

方法（同 run_realenv.py）：wqb-db server 按仓库 .mcp.json 经 stdio 真实启动，写入走 MCP 协议层；toolkit 评审
写入按 pipeline stage_review 的写法（先 metrics_cache.row_from_alpha，再 _lib.wqb_store.get_store →
save_backtest_results）在各自代码树的子进程里跑。修复前的代码树（BASE_DIR，默认 main 的 baf6f19）与本工作树
各用一个空库跑同一序列：
  ① 真实评审行：tracking/*/reviews/*.json 里带 failed_checks 的行（row_from_alpha 的产出，旧缓存行形态，
     没有 ra_failed_checks 键）→ upsert_backtest_rows
  ② 平台载荷，每条走三条写入路径——toolkit 评审（row_from_alpha → save_backtest_results）；收批·原始形态
     （get_alpha_details 形态 → harvest_multisim_results，campaign_intel xr-probe 是同一拍平）；收批·精简形态
     （mcp_core._slim_alpha + alpha_id / expression = harvest_multisim_alphas 的返回形态 → harvest_multisim_results，
     SOP 步 6）。载荷两组：
       真实：tracking/mining/result_submit_*（提交前检查的 SSE 记录，含完整 is.checks 与指标；记录里没有表达式，
             用占位式 rank(i4_<id>) 作关联键）
       分叉情形：真实载荷裁剪件 tests/fixtures/alpha_detail_cluster_sample.json 上各造一种——原样 /
             非 RA 项 SELF_CORRELATION FAIL / RA 项 LOW_SUB_UNIVERSE_SHARPE WARNING / RA 项 LOW_2Y_SHARPE FAIL
  ③ 读取方：get_mining_yield（严格产出率）；提交队列 enqueue_from_alphas（各自树的代码，按骨架去重关掉）
期望值 = 本工作树 wqb.config.compute_webdata_failed_counts 从完整 checks 算出的 RA 失败项（评审行：failed_checks ∩ RA）。

副作用：wqb-db server 写死 <tree>/data/wqb.db（N26），两棵树的该文件在演练期间换成空库，结束（含异常）后移到
$REALENV_SCRATCH/item4/，原有文件移回。本容器无 BRAIN 凭据，脚本不读 .env。用法见同目录 reproduce_realenv_item4.sh。
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
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_realenv as H  # noqa: E402  复用：stdio 起服（.mcp.json 原样）、副作用探针、脱敏

ROOT, BASE = H.ROOT, H.BASE_DIR
WORK = H.SCRATCH / "item4"
HOME = str(Path.home())
_rel0 = H.rel


def rel(p):
    return _rel0(p).replace(HOME + os.sep, "~" + os.sep)


H.rel = rel

for _p in (ROOT / "src", ROOT / "world-quant-brain-mcp"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
from wqb.config import RA_CHECK_NAMES, compute_webdata_failed_counts  # noqa: E402  期望值 = 唯一定义

FIXTURE = ROOT / "tests" / "fixtures" / "alpha_detail_cluster_sample.json"
CASES = ("clean", "corr_fail", "ra_warning", "ra_fail")
#: 写入路径 → (alpha_id 前缀, 波号)；backtest_results 按 alpha_id 唯一，同一载荷三条路径各用一个前缀
PATHS = {"toolkit": ("tk_", "i4_toolkit"), "raw": ("raw_", "i4_raw"), "slim": ("slim_", "i4_slim")}
PATH_LABEL = {"toolkit": "toolkit 评审", "raw": "收批·原始形态", "slim": "收批·精简形态"}
REVIEW_WAVE = "i4_review"

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
keys = {k for rows in rows_by_region.values() for r in rows for k in r}
print(json.dumps({"rows": sum(map(len, rows_by_region.values())), "written": n,
                  "row_has_ra_failed_checks": "ra_failed_checks" in keys}))
'''

ENQUEUE_SCRIPT = r'''
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
from wqb.store.submit_queue import enqueue_from_alphas
print(json.dumps({"enqueued": enqueue_from_alphas(db_path=sys.argv[1], note="item4 probe", dedup=False)}))
'''


# ----------------------------------------------------------------------------- 输入
def review_rows():
    """tracking/*/reviews/*.json 里带 failed_checks 的评审行，按 alpha 去重 → {region: [row, …]}。"""
    seen, out = set(), defaultdict(list)

    def walk(o, region):
        if isinstance(o, dict):
            aid = o.get("id") or o.get("alpha_id")
            if "failed_checks" in o and aid and o.get("code") and aid not in seen:
                seen.add(aid)
                out[region].append(dict(o))
            for v in o.values():
                walk(v, region)
        elif isinstance(o, list):
            for x in o:
                walk(x, region)

    for f in sorted(glob.glob(str(ROOT / "tracking" / "*" / "reviews" / "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8-sig"))
        except ValueError:
            continue
        walk(d, Path(f).parent.parent.name)
    return dict(out)


def submit_payloads():
    """tracking/mining/result_submit_*：含完整 is.checks 与指标的平台记录 → {alpha_id: GET /alphas/{id} 形态}。"""
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
                out[aid] = {"id": aid, "type": "REGULAR", "settings": {"region": m.get("region")},
                            "regular": {"code": f"rank(i4_{aid})"},          # 记录里没有表达式：占位，只作关联键
                            "is": {**{k: m[k] for k in ("sharpe", "fitness", "turnover", "margin", "returns",
                                                        "drawdown") if m.get(k) is not None},
                                   "checks": cr["is_checks_summary"]}}
                break
    return out


def variants():
    """真实载荷裁剪件上的四种情形（与 tests/unit/test_ra_failed_checks_single_definition.py 同一构造）。"""
    out = {}
    for case in CASES:
        d = json.loads(FIXTURE.read_text(encoding="utf-8"))
        checks = d["is"]["checks"]
        if case == "corr_fail":           # 非 RA 项 FAIL：相关性检查跑完之后再取数
            checks.append({"name": "SELF_CORRELATION", "result": "FAIL", "value": 0.83, "limit": 0.7})
        elif case == "ra_warning":        # RA 项 WARNING
            next(c for c in checks if c["name"] == "LOW_SUB_UNIVERSE_SHARPE")["result"] = "WARNING"
        elif case == "ra_fail":
            next(c for c in checks if c["name"] == "LOW_2Y_SHARPE")["result"] = "FAIL"
        d.pop("status", None)
        d["id"] = f"v_{case}"
        d["regular"] = {"code": f"rank(ts_delta(i4_{case}, 5))"}
        out[d["id"]] = d
    return out


def definitions(checks):
    """(RA 唯一定义的失败项, 全部 FAIL 项 = 修复前这一列的写法)。"""
    return (compute_webdata_failed_counts(checks)["ra_failed_names"],
            [c.get("name") for c in checks if isinstance(c, dict) and c.get("result") == "FAIL"])


def stored(names):
    return json.dumps(names, ensure_ascii=False) if names else None


def build_inputs():
    import mcp_core  # noqa: PLC0415  wq-brain-http 的精简实现（两棵树里同一份，未改动）

    review = review_rows()
    real, var = submit_payloads(), variants()
    inp = {"review": review, "toolkit": defaultdict(list), "raw": defaultdict(list), "slim": defaultdict(list),
           "expected": {}, "group": {}, "real": real, "var": var}
    for region, rows in review.items():
        for r in rows:
            fails = list(r.get("failed_checks") or [])
            inp["expected"][r["id"]] = ([n for n in fails if n in RA_CHECK_NAMES], fails)
            inp["group"][r["id"]] = ("review", "review", region)
    for group, payloads in (("real", real), ("variant", var)):
        for aid, payload in payloads.items():
            region = payload["settings"]["region"]
            exp = definitions(payload["is"]["checks"])
            for path, (prefix, _wave) in PATHS.items():
                p = copy.deepcopy(payload)
                p["id"] = prefix + aid
                inp["expected"][p["id"]] = exp
                inp["group"][p["id"]] = (group, path, region)
                if path == "toolkit":
                    inp["toolkit"][region].append((p["id"], p))
                elif path == "raw":
                    inp["raw"][region].append(p)
                else:
                    s = mcp_core._slim_alpha(p)
                    s["alpha_id"], s["expression"] = p["id"], p["regular"]["code"]
                    inp["slim"][region].append(s)
    return inp


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
            dst = WORK / f"{tag}.{p.name}.before_item4"
            shutil.move(str(p), str(dst))
            saved.append((dst, p))
    return saved, (Path(tree) / "data").is_dir()


def restore(tree, tag, st):
    saved, had_dir = st
    for p in _db_files(tree):
        if p.exists():
            shutil.move(str(p), str(WORK / f"{tag}.{p.name}.after_item4"))
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


# ----------------------------------------------------------------------------- 同一序列
async def sequence(tag, tree, inp):
    H.H1({"base": "修复前（BASE_DIR）", "fixed": "修复后（本工作树）"}[tag] + " · 同一序列（空库起步）")
    db = fresh_db(tree)
    rec = {}
    spec = WORK / f"{tag}.toolkit_input.json"
    spec.write_text(json.dumps({"wave": PATHS["toolkit"][1], "by_region": inp["toolkit"]}, ensure_ascii=False),
                    encoding="utf-8")
    script = WORK / "toolkit_write.py"
    script.write_text(TOOLKIT_SCRIPT, encoding="utf-8")
    H.H2("② toolkit 评审写入（pipeline stage_review 的写法；本树 toolkit，子进程，WQB_DB_PATH 指向演练库）")
    p, _ = H.sh([H.PY, str(script), str(spec)], env_extra={"WQB_DB_PATH": str(db)}, cwd=tree, root=tree, db=db, tail=4)
    rec["toolkit"] = _last_json(p.stdout) or {}

    async with H.open_server(f"wqb-db·{tag}", tree, "wqb-db", db) as srv:
        H.H2("① 真实评审行 → upsert_backtest_rows（按区域）")
        for region, rows in sorted(inp["review"].items()):
            res, err, _pr = await srv.call("upsert_backtest_rows", quiet=True, region=region, wave=REVIEW_WAVE,
                                           rows=rows)
            print(f"    {region}: {len(rows)} 行 → n={(res or {}).get('n') if isinstance(res, dict) else res}"
                  f"  isError={err}")
        for path in ("raw", "slim"):
            H.H2(f"② {PATH_LABEL[path]} → harvest_multisim_results（按区域）")
            for region, alphas in sorted(inp[path].items()):
                res, err, _pr = await srv.call("harvest_multisim_results", quiet=True, region=region,
                                               wave=PATHS[path][1], alphas=alphas)
                got = res.get("upserted") if isinstance(res, dict) else res
                print(f"    {region}: {len(alphas)} 条 → upserted={got}  isError={err}")
        H.H2("③ 读取方：get_mining_yield（默认严格口径）")
        y, _err, _pr = await srv.call("get_mining_yield", n=700)
        rec["yield"] = y if isinstance(y, dict) else {}

    H.H2("③ 读取方：提交队列 enqueue_from_alphas（本树 src，dedup 关）")
    missing = [c for c in ("soft_deleted", "disposition")
               if c not in {r[1] for r in H.q(db, "PRAGMA table_info(alphas)")}]
    if missing:
        conn = sqlite3.connect(str(db))
        try:
            for c in missing:
                conn.execute(f"ALTER TABLE alphas ADD COLUMN {c} {'INTEGER DEFAULT 0' if c == 'soft_deleted' else 'TEXT'}")
            conn.commit()
        finally:
            conn.close()
        print(f"    注：CampaignStore 建的 alphas 表没有 {missing}，提交队列的入队查询要用（生产库与 "
              f"test_submit_queue_gates 夹具里有），空库上直接 no such column——两棵树相同的既有缺口，与本项无关；"
              f"演练库补上这两列再入队")
    script = WORK / "enqueue.py"
    script.write_text(ENQUEUE_SCRIPT, encoding="utf-8")
    H.sh([H.PY, str(script), str(db)], cwd=tree, root=tree, db=db, tail=3)

    rec["col"] = dict(H.q(db, "SELECT alpha_id, ra_failed_checks FROM backtest_results"))
    rec["payload_failed"] = {a: json.loads(v) if v else v for a, v in H.q(
        db, "SELECT alpha_id, json_extract(payload_json, '$.failed_checks') FROM backtest_results")}
    over = "ABS(COALESCE(sharpe,0))>=1.58 AND COALESCE(fitness,0)>=1.0"     # 与 get_mining_yield 同一谓词
    rec["over"] = {a for (a,) in H.q(db, f"SELECT alpha_id FROM backtest_results WHERE {over}")}
    rec["clean"] = {a for (a,) in H.q(
        db, f"SELECT alpha_id FROM backtest_results WHERE {over} AND COALESCE(TRIM(ra_failed_checks),'') IN ('', '[]')")}
    rec["gate"] = {a: (g, s) for a, g, s in H.q(db, "SELECT alpha_id, gate, status FROM submit_ready")}
    print(f"    backtest_results {len(rec['col'])} 行；submit_ready {len(rec['gate'])} 行")
    return rec


# ----------------------------------------------------------------------------- 主流程
def _ids(inp, group, path=None):
    return sorted(a for a, (g, p, _r) in inp["group"].items() if g == group and (path is None or p == path))


def _mismatch(rec, inp, ids):
    return [a for a in ids if rec["col"].get(a, "<缺行>") != stored(inp["expected"][a][0])]


async def body():
    H.H1("第 4 项真实环境探针 · 步 0 · 环境与输入")
    for tag, tree in (("本工作树", ROOT), ("BASE_DIR", BASE)):
        head = subprocess.run(["git", "-C", str(tree), "log", "--oneline", "-1"], capture_output=True,
                              text=True).stdout.strip()
        print(f"  {tag}: {rel(tree)}  HEAD={head or '（git archive 副本，无 .git）'}")
    print("  本工作树未提交改动（= 第 4 项修复）:", sorted(H.git_dirty(ROOT)))
    print("  world-quant-brain-mcp/.env 存在?", (ROOT / "world-quant-brain-mcp" / ".env").exists(), "（只判存在，不读取）")
    inp = build_inputs()
    n_review = sum(map(len, inp["review"].values()))
    names = Counter(n for a in _ids(inp, "review") for n in inp["expected"][a][1])
    print(f"  ① 真实评审行 {n_review} 条（{', '.join(f'{r} {len(v)}' for r, v in sorted(inp['review'].items()))}）；"
          f"failed_checks 里出现的名字：{dict(names)}；非 RA 名字："
          f"{sorted(n for n in names if n not in RA_CHECK_NAMES) or '无'}")
    print(f"  ② 真实平台载荷 {len(inp['real'])} 条（{sorted(inp['real'])}）：")
    diverge = []
    for aid, pl in sorted(inp["real"].items()):
        ra, fails = definitions(pl["is"]["checks"])
        nonpass = sorted({(c.get('name'), c.get('result')) for c in pl["is"]["checks"]
                          if c.get("result") not in ("PASS", None)})
        print(f"     {aid} {pl['settings']['region']} S={pl['is'].get('sharpe')} F={pl['is'].get('fitness')} "
              f"RA 失败={ra} 全部 FAIL={fails} 非 PASS 项={nonpass}")
        if ra != fails:
            diverge.append(aid)
    print(f"     两种定义在真实载荷上分叉的条数：{len(diverge)} {diverge}")
    for aid, pl in inp["var"].items():
        ra, fails = definitions(pl["is"]["checks"])
        print(f"  ② 分叉情形 {aid}: RA 失败={ra}  全部 FAIL（修复前这一列）={fails}")

    out = {tag: await sequence(tag, tree, inp) for tag, tree in (("base", BASE), ("fixed", ROOT))}
    b, f = out["base"], out["fixed"]

    H.H1("逐行对照：分叉情形 × 三条写入路径（这一列：修复前 → 修复后 ｜ 期望 = RA 唯一定义）")
    for aid in _ids(inp, "variant"):
        _g, path, _r = inp["group"][aid]
        exp = stored(inp["expected"][aid][0])
        print(f"  {aid:<20} {PATH_LABEL[path]:<10} {str(b['col'].get(aid)):<30} → {str(f['col'].get(aid)):<30} "
              f"｜ 期望 {exp}  {'✓' if f['col'].get(aid) == exp else '✗'}")

    H.H1("读取方")
    for tag, rec in (("修复前", b), ("修复后", f)):
        t = (rec["yield"] or {}).get("totals") or {}
        rows = {r.get("region"): (r.get("backtested"), r.get("passed"), r.get("ra_clean"))
                for r in (rec["yield"] or {}).get("rows") or []}
        print(f"  get_mining_yield {tag}：totals backtested={t.get('backtested')} passed={t.get('passed')} "
              f"ra_clean={t.get('ra_clean')}；按区 (backtested, passed, ra_clean)={rows}")
    only_b, only_f = sorted(b["clean"] - f["clean"]), sorted(f["clean"] - b["clean"])
    print(f"  严格口径计为 RA 干净的集合差：只在修复前={only_b}；只在修复后={only_f}")
    for aid in _ids(inp, "variant"):
        print(f"  提交队列 {aid:<20} 修复前 {b['gate'].get(aid)}  →  修复后 {f['gate'].get(aid)}")

    H.H1("第 4 项验证清单（✅/❌ 判修复后，括号里是修复前的实测）")
    both = set(b["col"]) & set(f["col"])
    skipped = sorted(a for a in inp["expected"] if a not in b["col"] and a not in f["col"])
    one_sided = sorted(a for a in inp["expected"] if (a in b["col"]) != (a in f["col"]))
    rv_all, real, var = _ids(inp, "review"), _ids(inp, "real"), _ids(inp, "variant")
    rv = [a for a in rv_all if a in both]
    if skipped:
        print(f"  两棵树都没入库 {len(skipped)} 条：{skipped}——代码末尾带空白（截断的旧评审行）：upsert_expressions 存 "
              f"strip 后的式子，回测行按原串查不到 expression_id 就跳过。与本项无关的既有问题；下面只比两棵树都入库的行")
    exp_clean = {a for a in f["over"] if not inp["expected"][a][0]}
    gate = lambda rec, a: (rec["gate"].get(a) or ("<未入队>", ""))  # noqa: E731
    # 提交队列的期望：RA 项 WARNING → RA 闸拦下；非 RA 的相关性 FAIL 不再冒充 RA，改由 alphas 的相关性数值拦
    # （收批两条路径从 checks 带上了 SELF_CORRELATION 数值）；toolkit 评审行不带相关性数值 → IS_ONLY 待 verify
    q_ok = (all(gate(f, p + "v_ra_warning")[0].startswith("FAIL:RA:LOW_SUB_UNIVERSE_SHARPE") for p in ("tk_", "raw_", "slim_"))
            and all(gate(f, p + "v_corr_fail")[0] == "FAIL:SELF" for p in ("raw_", "slim_"))
            and gate(f, "tk_v_corr_fail") == ("IS_ONLY", "READY")
            and all(gate(f, p + "v_ra_fail")[0].startswith("FAIL:RA:LOW_2Y_SHARPE") for p in ("tk_", "raw_", "slim_")))
    items = [
        ("两棵树入库的行集合相同（本项不改变哪些行能入库）",
         not one_sided and all(a in both for a in real + var),
         f"只在一棵树里有的行：{one_sided or '无'}；两棵树都没入库 {len(skipped)} 条（见上）", "—"),
        (f"真实评审行（{len(rv)}/{len(rv_all)} 条入库，只有 failed_checks 的旧缓存行形态）：这一列 = failed_checks ∩ RA，"
         f"两棵树逐条相同",
         not _mismatch(f, inp, rv) and all(b["col"].get(a) == f["col"].get(a) for a in rv),
         f"修复后与期望不符 {len(_mismatch(f, inp, rv))} 条；两树不同 {sum(b['col'].get(a) != f['col'].get(a) for a in rv)} 条",
         f"修复前与期望不符 {len(_mismatch(b, inp, rv))} 条"),
        (f"真实平台载荷（{len(inp['real'])} 条 × 3 条写入路径 = {len(real)} 行）：这一列 = RA 唯一定义，两棵树逐条相同",
         not _mismatch(f, inp, real) and all(b["col"].get(a) == f["col"].get(a) for a in real),
         f"修复后与期望不符 {_mismatch(f, inp, real) or 0}；两树不同 {[a for a in real if b['col'].get(a) != f['col'].get(a)] or 0}",
         f"修复前与期望不符 {_mismatch(b, inp, real) or 0}"),
        (f"分叉情形（4 种 × 3 条写入路径 = {len(var)} 行）：这一列 = RA 唯一定义",
         not _mismatch(f, inp, var),
         f"修复后与期望不符 {_mismatch(f, inp, var) or 0}",
         f"修复前与期望不符 {len(_mismatch(b, inp, var))} 行：{_mismatch(b, inp, var)}"),
        ("toolkit 评审行带上 ra_failed_checks（按唯一定义现算；拿不到 wqb 时才不带、由存储层回落）",
         f["toolkit"].get("row_has_ra_failed_checks") is True and f["toolkit"].get("written") == f["toolkit"].get("rows"),
         f"修复后：{f['toolkit']}", f"修复前：{b['toolkit']}"),
        ("全部 FAIL 项照旧留在 payload_json.failed_checks（评审 / 诊断用），四条路径逐条一致",
         all((f["payload_failed"].get(a) or []) == inp["expected"][a][1] for a in rv + real + var),
         f"修复后不一致：{[a for a in rv + real + var if (f['payload_failed'].get(a) or []) != inp['expected'][a][1]] or '无'}",
         f"修复前不一致：{[a for a in rv + real + var if (b['payload_failed'].get(a) or []) != inp['expected'][a][1]] or '无'}"),
        ("严格产出率的 RA 干净集合 = 按定义（sharpe/fitness 过线且 RA 失败项为空）",
         f["clean"] == exp_clean,
         f"修复后：ra_clean {len(f['clean'])} 条；只在修复后计为干净 {only_f}",
         f"修复前：ra_clean {len(b['clean'])} 条；只在修复前计为干净 {only_b}"),
        ("提交队列：RA 项 WARNING 被 RA 闸拦下；相关性 FAIL 不再冒充 RA（收批路径由 SELF 数值拦，toolkit 行 IS_ONLY 待 verify）",
         q_ok,
         "修复后：" + "；".join(f"{a} {gate(f, a)}" for a in var if "clean" not in a),
         "修复前：" + "；".join(f"{a} {gate(b, a)}" for a in var if "clean" not in a)),
        (f"真实数据（评审行 {len(rv)} + 平台载荷 {len(real)}）的提交队列判定两棵树相同",
         all(gate(b, a) == gate(f, a) for a in rv + real),
         f"两树不同：{[a for a in rv + real if gate(b, a) != gate(f, a)] or '无'}",
         f"修复前入队 {len(b['gate'])} 条"),
    ]
    for title, ok, after, before in items:
        print(f"  {'✅' if ok else '❌'} {title}")
        print(f"       {after}")
        print(f"       （{before}）")
    print(f"\n  结果：{sum(1 for _t, ok, _a, _b in items if ok)}/{len(items)} ✅")


async def main():
    if BASE is None or not (BASE / "wqb_db_mcp.py").is_file():
        sys.exit("需要 BASE_DIR=<第 4 项修复前的代码树>（见 reproduce_realenv_item4.sh）")
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
