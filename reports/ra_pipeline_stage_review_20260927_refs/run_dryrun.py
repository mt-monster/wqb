# -*- coding: utf-8 -*-
"""RA 九步流水线 · 沙箱 dry-run 演练（2026-09-27）

运行环境：临时工作目录内 `git archive HEAD` 副本（见 reproduce.sh） + 合成种子库（region=KOR，dataset=syn_analyst）。
网络被封锁、子进程默认被拦截（仅在标注“沙箱内实跑本地脚本”的步骤临时放开），
每个探针都记录文件系统 / DB / 网络 / 子进程副作用。真实仓库与真实 DB 不受任何影响。
"""
import ast
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import contextlib

SBX = os.environ["SBX"]
STUBS = os.environ["STUBS"]
for p in (STUBS, os.path.join(SBX, "src"), os.path.join(SBX, "world-quant-brain-mcp"), SBX):
    if p not in sys.path:
        sys.path.insert(0, p)
os.chdir(SBX)  # WorkflowExecutor 的 store 用相对路径 data/wqb.db（见 §结论），故 cwd 固定在沙箱根

import sbx_guard as G  # noqa: E402  —— 导入即封网 + 拦截子进程
import logging  # noqa: E402
logging.basicConfig(level=logging.ERROR)

R, DS = "KOR", "syn_analyst"
CAMP = os.path.join(SBX, "tracking", R)
TOOLKIT = os.path.join(SBX, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")
VALIDATOR = os.path.join(SBX, "Claude", "skills", "alpha-expression-verifier", "scripts")
DB = os.path.join(SBX, "data", "wqb.db")
PY = sys.executable


def H1(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


def H2(t):
    print(f"\n--- {t}")


def q(sql, *p):
    c = sqlite3.connect(DB)
    try:
        return c.execute(sql, p).fetchall()
    finally:
        c.close()


def run_node(node, params, dry_run=True, label=None):
    from wqb.workflow import execute
    with G.Probe() as pr:
        res = execute(node, params, dry_run=dry_run)
    out = res.output if isinstance(res.output, dict) else {}
    cmd = out.get("command") or out.get("plan") or (" ".join(out["cmd"]) if isinstance(out.get("cmd"), list) else None)
    steps = [(s.get("step"), s.get("success")) for s in out.get("steps", []) if isinstance(s, dict)]
    print(f"[node] {label or node}  dry_run={dry_run}  success={res.success}  error={res.error!r}"[:600])
    if steps:
        print(f"       steps={steps}"[:600])
    if cmd:
        print(f"       cmd/plan= {str(cmd)[:420]}")
    print(f"       {pr.summary()}")
    if pr.fs["added"] or pr.fs["changed"]:
        print(f"       FS added={pr.fs['added'][:6]} changed={pr.fs['changed'][:6]}")
    if pr.subproc:
        print(f"       SUBPROC attempted: {[s[:160] for s in pr.subproc[:3]]}")
    if pr.net:
        print(f"       NET attempted: {pr.net[:3]}")
    return res, out, pr


def sh(argv, env_extra=None, cwd=None, allow=True, tail=60):
    """沙箱内实跑本地脚本（零平台调用；网络仍被子进程外的系统代理约束，脚本本身不应触网）。"""
    env = dict(os.environ)
    env.update(env_extra or {})
    G.block_subprocess(False)
    try:
        with G.Probe() as pr:
            p = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               env=env, cwd=cwd or SBX, timeout=600)
    finally:
        G.block_subprocess(True)
    lines = (p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr.strip() else "")).rstrip().splitlines()
    print(f"$ {' '.join(os.path.relpath(a, SBX) if a.startswith(SBX) else a for a in argv)}")
    for ln in lines[-tail:]:
        print("  | " + ln[:230])
    print(f"  => exit={p.returncode}  {pr.summary()}")
    if pr.fs["added"] or pr.fs["changed"]:
        print(f"     FS added={pr.fs['added'][:6]} changed={pr.fs['changed'][:6]}")
    return p, pr


def exec_funcs_from(path, names):
    """从源码里只摘出指定的赋值/函数定义并执行（避免导入整个模块的重依赖）。"""
    tree = ast.parse(open(path, encoding="utf-8").read())
    keep = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            keep.append(node)
        elif isinstance(node, ast.Assign) and any(getattr(t, "id", None) in names for t in node.targets):
            keep.append(node)
    ns = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), path, "exec"), ns)
    return ns


EXPRS = {
    "e01_ok_group_rank": "group_rank(ts_delta(syn_eps_rev_up, 22), subindustry)",
    "e02_ok_backfill_rank": "rank(ts_backfill(syn_tgt_px_gap, 66))",
    "e03_inspect_violation": "ts_zscore(syn_tgt_px_gap, 66)",
    "e04_ok_event_trade_when": "trade_when(syn_surprise_evt > 0, rank(syn_eps_rev_dn), -1)",
    "e05_ghost_ts_entropy": "rank(ts_entropy(syn_rec_mean, 22))",
    "e06_vector_unwrapped": "rank(ts_mean(syn_est_vec, 22))",
    "e07_inaccessible_ts_min": "rank(ts_min(syn_eps_rev_up, 5))",
    "e08_weighted_mix": "add(multiply(0.4, rank(syn_eps_rev_up)), multiply(0.6, rank(syn_rec_mean)))",
    "e09_unknown_field": "rank(syn_fake_field)",
    "e10_hump_positional": "hump(rank(syn_rec_mean), 0.01)",
}

# =====================================================================================
H1("步 1 · S-PRE 查表（区域先验 / 库存 / 产出率）")
# =====================================================================================
H2("输入：区域 profile（references/regions/KOR.md front-matter）")
prof = open(os.path.join(SBX, "Claude/skills/wq-brain-ra-pipeline/references/regions/KOR.md"), encoding="utf-8").read()
fm = prof.split("---")[1]
for key in ("entry_verdict", "universe_default", "neutralization_default", "fast_kill"):
    for ln in fm.splitlines():
        if ln.strip().startswith(key + ":"):
            print(f"  {ln.strip()[:150]}")
H2("处理：get_campaign_summary / get_dead_ends / get_mining_yield(strict)（wqb-db MCP 函数，直调沙箱库）")
import wqb_db_mcp as dbm  # noqa: E402  (stub FastMCP；DB_PATH=沙箱根/data/wqb.db)
print("  DB_PATH used by wqb_db_mcp:", os.path.relpath(str(dbm.DB_PATH), SBX))
with G.Probe() as pr:
    summ = dbm.get_campaign_summary(R)
    dead = dbm.get_dead_ends(R)
    y = dbm.get_mining_yield(region=R)
    yd = dbm.get_mining_yield(region=R, by_dataset=True)
print("  campaign_summary:", G.dump(summ, 500))
print("  dead_ends:", len(dead))
print("  mining_yield(strict):", G.dump(y, 900))
print("  mining_yield(by_dataset):", G.dump(yd, 600))
print("  ", pr.summary())
H2("处理：库存盘点节点 inventory_scan（dry-run）")
run_node("inventory_scan", {"region": R, "target": 20})
H2("处理：s0-select 三方交叉 / build_gate_prior_from_inventory / select_ra_basket")
print("  以上三者都要打平台端点（recommend_datasets / GET /users/self/alphas / GET /alphas/{id}），"
      "沙箱断网 → 不执行，仅在报告中做静态推演。")

# =====================================================================================
H1("步 2 · S0 数据集体检 + 白名单（campaign 节点 S0 / region gates / 缓存）")
# =====================================================================================
H2("处理：campaign(stage=S0, calibrate=true) 与 campaign(stage=S0) 干跑")
run_node("campaign", {"region": R, "stage": "S0", "calibrate": True}, label="campaign S0 calibrate")
run_node("campaign", {"region": R, "stage": "S0"}, label="campaign S0 score")
H2("核查：campaign 节点 S0-calibrate / assemble-priors 的 ledger 缓存命中条件")
sys.path.insert(0, os.path.join(SBX, "src"))
from wqb.store import CampaignStore  # noqa: E402
st = CampaignStore(DB)
st.upsert_ledger(R, f"s0_calibrate_{R}", {"calibrated_at": "2026-09-27T00:00:00", "region": R, "stdout_tail": "..."})
cached = st.get_ledger(R, f"s0_calibrate_{R}")
print(f"  节点自己写入的缓存值 keys={sorted(cached)}；命中条件 cached.get('value') -> {cached.get('value')!r}")
print("  => 命中分支永远不成立（get_ledger 返回的是 payload 本体，不含 'value' 键）：缓存是死代码。")
st.connection.execute("DELETE FROM ledger_kv WHERE region=? AND key=?", (R, f"s0_calibrate_{R}"))
st.connection.commit()
H2("核查：_ensure_campaign_config 在 dry-run 下是否写盘（临时移走 AMR 的 settings.json）")
amr_cfg = os.path.join(SBX, "tracking", "AMR", "config", "settings.json")
shutil.move(amr_cfg, amr_cfg + ".bak")
res, out, pr = run_node("campaign", {"region": "AMR", "stage": "S0"}, label="campaign S0 (AMR, 缺 settings.json)")
print(f"  settings.json 在 dry-run 后存在? {os.path.exists(amr_cfg)}")
if os.path.exists(amr_cfg):
    print("  自动生成内容:", open(amr_cfg, encoding="utf-8").read()[:260].replace("\n", " "))
    os.remove(amr_cfg)
shutil.move(amr_cfg + ".bak", amr_cfg)
H2("处理：开波前区域四闸（toolkit _lib/region_gates.run_region_gates，warn 模式）")
sys.path.insert(0, TOOLKIT)
from _lib import region_gates as rg  # noqa: E402
with G.Probe() as pr:
    rep = rg.run_region_gates(CAMP, R, mode="warn")
print("  ok:", rep["ok"], " hits:", rep.get("hits"), " ", pr.summary())

# =====================================================================================
H1("步 3 · S1 字段扫描 + 理解")
# =====================================================================================
run_node("campaign", {"region": R, "stage": "S1"}, label="campaign S1（缺 dataset）")
run_node("campaign", {"region": R, "stage": "S1", "dataset": DS}, label="campaign S1")
run_node("feature_engineering", {"region": R, "dataset_id": DS, "delay": 1, "universe": "TOP600"})
run_node("field_understanding", {"region": R, "dataset": DS})
H2("SOP 规则演示：字段 users 分级（SKILL.md 步 3；无对应工具，按规则对种子 catalog 手算）")
for fid, users in q("SELECT f.field_name, f.user_count FROM fields f JOIN datasets d ON d.id=f.dataset_id WHERE d.name=?", DS):
    tier = "≥50 仅方向验证" if (users or 0) >= 50 else ("10-49 进池·提交前实测 prod" if (users or 0) >= 10 else "0-9 优先池")
    print(f"  {fid:18s} users={users!s:>3}  → {tier}")

# =====================================================================================
H1("步 4 · S2 概念优先生成（priors → GEM → 预闸 → 选波）")
# =====================================================================================
run_node("campaign", {"region": R, "stage": "S2", "subcommand": "assemble-priors"}, label="campaign assemble-priors")
H2("沙箱内实跑 assemble_priors.py（纯本地 DB→文件，展示 S6 知识如何流入 S2）")
print("  (a) 仅设 WQB_DB_PATH/WQB_ROOT —— toolkit _lib/ledger 的 RegistryStore 不认这两个变量：")
sh([PY, os.path.join(TOOLKIT, "campaign.py"), "--campaign-dir", CAMP, "assemble-priors"],
   env_extra={"WQB_DB_PATH": DB, "WQB_ROOT": SBX}, tail=3)
pri = os.path.join(CAMP, "priors", "kor_priors.json")
pri_before = open(pri, encoding="utf-8").read() if os.path.exists(pri) else None
ws_env = {"WQB_DB_PATH": DB, "WQB_ROOT": SBX, "WQB_WORKSPACE": SBX}
print("  (b) 补 WQB_WORKSPACE（该模块专用的根目录变量），按 campaign 节点拼出的原样命令跑（不带 --snapshot-ledger）：")
sh([PY, os.path.join(TOOLKIT, "campaign.py"), "--campaign-dir", CAMP, "assemble-priors"], env_extra=ws_env, tail=8)
print("  priors 文件是否被本次重写:", (open(pri, encoding="utf-8").read() != pri_before) if os.path.exists(pri) else "文件不存在")
print("  DB 快照 priors_snapshot_kor 存在?（GEM 默认只读它）:",
      bool(q("SELECT 1 FROM ledger_kv WHERE region=? AND key='priors_snapshot_kor'", R)))
print("  (c) 同命令追加 --snapshot-ledger：")
sh([PY, os.path.join(TOOLKIT, "campaign.py"), "--campaign-dir", CAMP, "assemble-priors", "--snapshot-ledger"],
   env_extra=ws_env, tail=4)
print("  DB 快照 priors_snapshot_kor 存在?:",
      bool(q("SELECT 1 FROM ledger_kv WHERE region=? AND key='priors_snapshot_kor'", R)))
if os.path.exists(pri):
    d = json.load(open(pri, encoding="utf-8"))
    print("  重写后的 priors wins:", G.dump(d.get("wins"), 500))
    print("  重写后的 priors dead_ends:", G.dump(d.get("dead_ends"), 300))
run_node("gem", {"region": R, "dataset_id": DS, "delay": 1, "universe": "TOP600", "data_type": "MATRIX"})
run_node("gem_wave", {"region": R, "dataset_id": DS, "delay": 1, "universe": "TOP600"})
H2("生成侧预闸 pipeline_pregate.pregate（GEM 落盘前；纯函数实跑）")
sys.path.insert(0, os.path.join(SBX, "Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas"))
import pipeline_pregate as pg  # noqa: E402
raw = [
    'quantile(syn_eps_rev_up, driver="gaussian", sigma=1.0)',
    "hump(rank(syn_rec_mean), 0.01)",
    "bucket(rank(syn_num_est))",
    "ts_mean(syn_eps_rev_up, 20)",
    "ts_mean(syn_eps_rev_up, 37)",
    "add(multiply(0.4, rank(syn_eps_rev_up)), multiply(0.6, rank(syn_rec_mean)))",
]
logs = []
with G.Probe() as pr:
    kept = pg.pregate(list(raw), log=lambda *a: logs.append(" ".join(map(str, a))), region=R)
print("  输入 6 条 →", (len(kept) if isinstance(kept, list) else kept))
for k in (kept if isinstance(kept, list) else []):
    print("   kept:", k)
for ln in logs[:12]:
    print("   log:", ln[:200])
print("  ", pr.summary())
run_node("campaign", {"region": R, "stage": "S2", "dataset": DS, "wave": "w4"}, label="campaign S2 选波（build_wave）")

# =====================================================================================
H1("步 5 · S2→S3 门禁（ghost-audit → wave_gate：语法/8 闸/体检硬门/多样性）")
# =====================================================================================
ef = os.path.join(SBX, "..", "out", "w5_candidates.txt")
os.makedirs(os.path.dirname(ef), exist_ok=True)
with open(ef, "w", encoding="utf-8") as f:
    f.write("\n".join(EXPRS.values()) + "\n")
print("  候选（10 条，每条故意覆盖一类闸）:")
for k, v in EXPRS.items():
    print(f"   {k:26s} {v}")
H2("① 幽灵算子硬闸（沙箱内实跑 campaign_intel.py ghost-audit）")
sh([PY, os.path.join(SBX, "tools", "campaign_intel.py"), "ghost-audit", "--region", R, "--exprs-file", ef], tail=12)
H2("② wave_gate 节点干跑（argv 契约）")
run_node("wave_gate", {"region": R, "dataset": DS, "wave": "w5", "exprs_file": ef, "from_db": False})
run_node("unified_gate", {"region": R, "dataset": DS, "wave": "w5", "exprs_file": ef, "from_db": False})
H2("③ tools/wave_gate.py 实跑 —— 不设 WQ_TOOLKIT_DIR（fresh clone / 仅 ~/.claude 安装位的情形）")
sh([PY, os.path.join(SBX, "tools", "wave_gate.py"), "--campaign-dir", CAMP, "--dataset", DS, "--wave", "w5",
    "--exprs-file", ef], env_extra={"WQB_DB_PATH": DB, "WQB_ROOT": SBX}, tail=8)
H2("④a tools/wave_gate.py 实跑 —— 设 WQ_TOOLKIT_DIR / WQ_VALIDATOR_DIR，但环境未装 PLY（requirements 未声明）")
gate_env_noply = {"WQB_DB_PATH": DB, "WQB_ROOT": SBX, "WQB_WORKSPACE": SBX, "WQ_TOOLKIT_DIR": TOOLKIT,
                  "WQ_VALIDATOR_DIR": VALIDATOR, "PYTHONPATH": os.environ.get("PYTHONPATH_NOPLY", "")}
sh([PY, os.path.join(SBX, "tools", "wave_gate.py"), "--campaign-dir", CAMP, "--dataset", DS, "--wave", "w5",
    "--exprs-file", ef], env_extra=gate_env_noply, tail=3)
H2("④b 同上 + 沙箱本地装好 PLY（与生产 MCP venv 等价的依赖面）")
gate_env = {"WQB_DB_PATH": DB, "WQB_ROOT": SBX, "WQB_WORKSPACE": SBX, "WQ_TOOLKIT_DIR": TOOLKIT,
            "WQ_VALIDATOR_DIR": VALIDATOR}
before = dict(q("SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status", R))
sh([PY, os.path.join(SBX, "tools", "wave_gate.py"), "--campaign-dir", CAMP, "--dataset", DS, "--wave", "w5",
    "--exprs-file", ef], env_extra=gate_env, tail=70)
after = dict(q("SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status", R))
print(f"  expressions 状态分布 前={before} 后={after}")
print("  gate_results 行:", q("SELECT region, wave, dataset, all_pass FROM gate_results"))
H2("⑤ 干净子集（e01/e02/e04）再跑一次，看 PASS 路径与 [opcat] 行为")
ef2 = os.path.join(SBX, "..", "out", "w6_clean.txt")
with open(ef2, "w", encoding="utf-8") as f:
    f.write("\n".join([EXPRS["e02_ok_backfill_rank"], EXPRS["e04_ok_event_trade_when"],
                       "rank(ts_delta(syn_eps_rev_dn, 22))"]) + "\n")
sh([PY, os.path.join(SBX, "tools", "wave_gate.py"), "--campaign-dir", CAMP, "--dataset", DS, "--wave", "w6",
    "--exprs-file", ef2], env_extra=gate_env, tail=40)
H2("⑥ 体检硬门单独验证：e02(合规) + e03(低覆盖/厚尾未处理) + 普通式，跳过闸6 以隔离变量")
ef3 = os.path.join(SBX, "..", "out", "w7_inspect.txt")
with open(ef3, "w", encoding="utf-8") as f:
    f.write("\n".join([EXPRS["e02_ok_backfill_rank"], EXPRS["e03_inspect_violation"],
                       "rank(ts_delta(syn_eps_rev_dn, 22))"]) + "\n")
sh([PY, os.path.join(SBX, "tools", "wave_gate.py"), "--campaign-dir", CAMP, "--dataset", DS, "--wave", "w7",
    "--exprs-file", ef3, "--skip-diversity-gate", "--skip-quality"], env_extra=gate_env, tail=30)
H2("⑦ [opcat] 语义验证：全合规、无 group_* 算子的批（跳过闸6，保留质量/多样性展示段）")
ef4 = os.path.join(SBX, "..", "out", "w8_opcat.txt")
with open(ef4, "w", encoding="utf-8") as f:
    f.write("\n".join([EXPRS["e02_ok_backfill_rank"], "rank(ts_mean(syn_eps_rev_up, 66))",
                       "rank(ts_delta(syn_eps_rev_dn, 22))"]) + "\n")
sh([PY, os.path.join(SBX, "tools", "wave_gate.py"), "--campaign-dir", CAMP, "--dataset", DS, "--wave", "w8",
    "--exprs-file", ef4, "--skip-diversity-gate"], env_extra=gate_env, tail=30)
print("  w5..w8 候选在 expressions 中的状态:",
      q("SELECT wave, status, COUNT(*) FROM expressions WHERE region=? AND wave IN ('w5','w6','w7','w8') GROUP BY wave, status", R))

# =====================================================================================
H1("步 6 · S3 七槽回测（batch_track / campaign S3 前置闸）")
# =====================================================================================
run_node("batch_track", {"region": R, "wave": "w4", "dataset": DS})
run_node("campaign", {"region": R, "stage": "S3", "dataset": DS, "wave": "w4"}, label="campaign S3（前置三闸 enforce）")
print("  积压证据（backlog gate evidence）:")
sys.path.insert(0, os.path.join(SBX, "src"))
from wqb.workflow.nodes import campaign as C  # noqa: E402
print("  ", G.dump(C._run_backlog_gate(R, DS, CAMP), 700))

# =====================================================================================
H1("步 7 · S4 诊断改进（review_wave 墙诊断 / auto_review / booster）")
# =====================================================================================
run_node("campaign", {"region": R, "stage": "S4", "dataset": DS, "wave": "w1"}, label="campaign S4 (wave=w1)")
run_node("campaign", {"region": R, "stage": "S4", "dataset": DS, "wave": "w9"}, label="campaign S4 (wave=w9 不存在)")
H2("review_wave 判定函数实跑（种子 w1 最强 5 条）")
os.environ.setdefault("CAMPAIGN_SKIP_DIR_CHECK", "0")
import importlib  # noqa: E402
rw = importlib.import_module("review_wave")
t = json.load(open(os.path.join(CAMP, "config", "thresholds.json"), encoding="utf-8"))
t_rev, t_near = t["review"], dict(t.get("near") or {})
t_rev.setdefault("rn_sharpe_min", 0.0)
for aid, s, f, y2, rn, fc in q("SELECT alpha_id, sharpe, fitness, two_year_sharpe, risk_neutralized_sharpe, ra_failed_checks "
                               "FROM backtest_results WHERE region=? AND wave='w1' ORDER BY sharpe DESC LIMIT 5", R):
    # metrics_cache.py:73 把平台 risk_neutralized 映射为 rn_sharpe，review_wave 读的是这个键
    r = {"sharpe": s, "fitness": f, "two_year_sharpe": y2, "margin_bp": 8.0, "turnover_pct": 12.0,
         "rn_sharpe": rn, "failed_checks": json.loads(fc) if fc else []}
    print(f"  {aid} S={s} F={f} 2Y={y2} RN={rn} failed={r['failed_checks']} → passes={rw.passes(r, t_rev)} "
          f"walls={rw.walls(r, t_rev)} near={rw.is_near(r, t_near)}")
run_node("auto_review", {"region": R, "wave": "w1", "dataset": DS})
run_node("alpha_booster", {"region": R, "wave": "w1", "dataset": DS})
run_node("modeb_improve", {"region": R, "dataset": DS, "base_field": "syn_eps_rev_up"})
print("  s4-prescreen / prod-first / check_correlation 需平台 → 沙箱不执行。")

# =====================================================================================
H1("步 8 · S4→S5 稳健闸与提交判定（Failed-count 资格门 / submit_verdict / 用户确认）")
# =====================================================================================
checks = [
    {"name": "LOW_SHARPE", "result": "PASS", "value": 1.81, "limit": 1.58},
    {"name": "LOW_FITNESS", "result": "PASS", "value": 1.09, "limit": 1.0},
    {"name": "LOW_2Y_SHARPE", "result": "WARNING", "value": 1.41, "limit": 1.58},
    {"name": "IS_LADDER_SHARPE", "result": "WARNING", "value": 1.44, "limit": 1.58},
    {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "FAIL", "value": 0.52, "limit": 0.89},
    {"name": "CONCENTRATED_WEIGHT", "result": "PASS"},
]
print("  合成 is.checks:", [(c["name"], c["result"]) for c in checks])
core = exec_funcs_from(os.path.join(SBX, "world-quant-brain-mcp", "mcp_core.py"),
                       {"_RA_2Y_NAMES", "_RA_CHECK_NAMES", "_PPA_CHECK_NAMES", "_ra_bad", "_slim_checks"})
_, _, _, ra = core["_slim_checks"](checks)
print("  生产口径 mcp_core._slim_checks →", G.dump(ra, 400))
from wqb.config import compute_webdata_failed_counts  # noqa: E402
print("  src/wqb/config.compute_webdata_failed_counts →", G.dump(compute_webdata_failed_counts(checks), 400))
H2("submit_verdict 判定表（网络依赖 → 按 tools_ops.py:236-251 源码静态推演）")
for sim_fail, hard_warn, submit_status, status in ((False, False, 404, "UNSUBMITTED"), (False, False, 200, "UNSUBMITTED"),
                                                   (False, True, 404, "UNSUBMITTED"), (False, False, 403, "UNSUBMITTED")):
    prepost = submit_status == 404 and status == "UNSUBMITTED"
    ok = (not sim_fail) and (not hard_warn) and (submit_status == 200 or prepost)
    verdict = "UNVERIFIABLE" if (ok and prepost) else ("SUBMITTABLE" if ok else "BLOCKED")
    print(f"  sim_fail={sim_fail!s:5} hard_warn={hard_warn!s:5} submit={submit_status} → {verdict}")
run_node("judge", {"alpha_id": "SYNw1039"})
run_node("submit_alpha", {"alpha_id": "SYNw1039"}, label="submit_alpha（未确认）")
run_node("submit_alpha", {"alpha_id": "SYNw1039", "confirm_submit": True}, label="submit_alpha（confirm_submit=True，干跑）")

# =====================================================================================
H1("步 9 · S6 复盘回写（step_funnel / upsert_wave_result / 停止闸闭环）")
# =====================================================================================
H2("step_funnel.py 实跑（只读推导）")
sh([PY, os.path.join(SBX, "tools", "step_funnel.py"), "--region", R], env_extra={"WQB_DB_PATH": DB}, tail=40)
H2("回写 w4 verdict=FAIL → 停止规则 B 是否对下一波生效")
print("  upsert_wave_result:", dbm.upsert_wave_result(R, "w4", verdict="FAIL", key_findings=["fixture: 0 达标"]))
g = C._run_stop_rules_gate(R, DS, CAMP)
print("  stop_rules_gate →", G.dump({k: g.get(k) for k in ("success", "hits", "warning", "evidence")}, 600))
run_node("campaign", {"region": R, "stage": "S2", "dataset": DS, "wave": "w7"}, label="下一波 campaign S2（应被规则 B 拦截）")
H2("只补写 key_findings（例如按步 9 把点塔进度追加进 key_findings），不带 verdict")
print("  upsert_wave_result:", dbm.upsert_wave_result(R, "w4", key_findings=["[pyramid] ANALYST 2/3 (fixture)"]))
print("  w4 行现状:", q("SELECT wave_number, verdict, status, key_findings FROM wave_results WHERE region=? AND wave_number='w4'", R))
g = C._run_stop_rules_gate(R, DS, CAMP)
print("  stop_rules_gate →", G.dump({k: g.get(k) for k in ("success", "hits", "warning", "evidence")}, 700))
run_node("campaign", {"region": R, "stage": "S2", "dataset": DS, "wave": "w7"}, label="下一波 campaign S2（规则 B 是否仍拦截）")
run_node("auto_pyramid", {"region": R, "wave": "w4"})
H2("wave_number 类型契约（MCP 签名 vs 表结构，静态核对）")
import inspect  # noqa: E402
print("  upsert_wave_result 签名:", inspect.signature(dbm.upsert_wave_result).parameters["wave_number"])
print("  get_wave_result 签名:", inspect.signature(dbm.get_wave_result).parameters["wave_number"])
print("  表结构:", [r for r in q("PRAGMA table_info(wave_results)") if r[1] == "wave_number"])

# =====================================================================================
H1("附：19 个 workflow 节点 dry-run 契约全量扫描（仓库自带 _DRY_RUN_CASES 参数）")
# =====================================================================================
cases = {}
src_t = open(os.path.join(SBX, "tests", "unit", "test_skill_integrity.py"), encoding="utf-8").read()
tree = ast.parse(src_t)
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "_DRY_RUN_CASES" for t in node.targets):
        cases = eval(compile(ast.Expression(node.value), "cases", "eval"), {})  # 含 ["_a_"]*10
rows_out = []
for node, params in sorted(cases.items()):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res, out, pr = run_node(node, params)
    rows_out.append((node, res.success, (res.error or "")[:90], pr.summary(), pr.fs["added"][:3] + pr.fs["changed"][:3]))
print(f"  {'node':24s} {'ok':5s} {'side-effects':40s} error / fs")
for node, ok, err, summ, fs in rows_out:
    print(f"  {node:24s} {str(ok):5s} {summ[:40]:40s} {err} {fs if fs else ''}")

H2("WorkflowExecutor.store 相对路径核查：换一个 cwd 调同一节点")
other = os.path.join(SBX, "..", "elsewhere")
os.makedirs(other, exist_ok=True)
os.chdir(other)
import wqb.workflow.executor as ex  # noqa: E402
ex._default_executor = None
from wqb.workflow import execute  # noqa: E402
execute("judge", {"alpha_id": "X"}, dry_run=True)
print("  cwd=", os.path.relpath(other, SBX), " 生成的库文件:", [os.path.relpath(os.path.join(dp, f), other)
      for dp, _, fs in os.walk(other) for f in fs])
os.chdir(SBX)
print("\n[DRY-RUN END] 全程：真实仓库未改动；网络尝试次数 =", len(G.NET_ATTEMPTS),
      "；被拦截的子进程尝试 =", len(G.SUBPROC_ATTEMPTS))
