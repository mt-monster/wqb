"""定向开发：对一个基础构造做「设置轴 + 表达式轴」扫描，找能把 S 顶过闸的变体。

用法：
    python tools/targeted_dev.py --tag s26_wp99 --alpha wp99v7qv
    python tools/targeted_dev.py --tag s26_wp99 --alpha wp99v7qv --stage ABCDE

设计要点（对齐项目约定）：
- 断点续跑：results/targeted_dev_<tag>.json 记录每个 variant 的 sim_id 与指标，
  重跑时按 label 跳过已完成（拿到 alpha 或明确 FAIL 的）。
- 单条批注意：n=1 的派发走**单仿真**端点，结果在 sim 对象的 `regular/alpha` 上，
  不在 `children` 里 —— 这里两种结构都兼容。
- 每次都写全量指标（S/F/TO/returns/margin/2Y/sub + 各闸 limit/result），便于归因。
"""
import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
WQB_TOOLS = os.path.join(os.environ.get("WQB_SCRIPTS") or os.path.join(os.path.expanduser("~"), "wqb-scripts"),
                         "wqb_tools.py")
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, os.path.dirname(WQB_TOOLS))

BASE_SETTINGS = dict(region="EUR", universe="TOPCS1600", decay=4,
                     neutralization="FAST", truncation=0.08,
                     nan_handling="ON", max_trade="ON",
                     # 2026-10-22 撤回 QUICK：失真不可预测（-0.18~+0.87）且会扭曲排序 ⇒ 回 FULL
                     simulation_mode="FULL")

ALT_FIELD = [None]   # stage I 用的第二字段（同数据集）

GATES = ("LOW_SHARPE", "LOW_FITNESS", "LOW_2Y_SHARPE", "LOW_SUB_UNIVERSE_SHARPE",
         "IS_LADDER_SHARPE", "CONCENTRATED_WEIGHT", "LOW_TURNOVER", "HIGH_TURNOVER")


def build_variants(base_expr, stage="ABCDE"):
    """构造变体清单：[(label, expr, settings)]"""
    V = []
    if "A" in stage:      # decay 轴
        for d in (2, 6, 8, 10, 15):
            V.append((f"A_decay{d}", base_expr, {**BASE_SETTINGS, "decay": d}))
    if "B" in stage:      # truncation 轴
        for t in (0.04, 0.06, 0.10, 0.12, 0.16):
            V.append((f"B_trunc{int(t*100):02d}", base_expr, {**BASE_SETTINGS, "truncation": t}))
    if "C" in stage:      # 中性化轴
        for n in ("SLOW", "INDUSTRY", "SUBINDUSTRY", "MARKET"):
            V.append((f"C_neut_{n}", base_expr, {**BASE_SETTINGS, "neutralization": n}))
    if "D" in stage:      # universe 轴
        for u in ("TOP2500", "TOP1200", "TOP600"):
            V.append((f"D_univ_{u}", base_expr, {**BASE_SETTINGS, "universe": u}))
    if "E" in stage:      # 稀疏化阈值轴（改表达式）
        for q in (0.75, 0.80, 0.88, 0.90, 0.92):
            V.append((f"E_q{int(q*100)}", base_expr.replace("0.85)", f"{q})", 1), BASE_SETTINGS))
    if "L" in stage:      # 关键组合：先保住稀疏门（保 S），再套 tail/分组（压 prod）
        # K_tail_ind 已证 tail+group_zscore 能把 prod 0.755→0.651，但它作用在未门控的乘积上毁了 S。
        # 改为作用于**带稀疏门的完整 base_expr**，让门保 S、分组+尾截压 prod。
        B = base_expr
        cands = {
            "L_tail_ind":  f"tail(group_zscore({B}, industry), lower=-1.1, upper=1.1, newval=0)",
            "L_tail_sub":  f"tail(group_zscore({B}, subindustry), lower=-1.1, upper=1.1, newval=0)",
            "L_groupz":    f"group_zscore({B}, industry)",
            "L_groupz_mkt":f"group_zscore({B}, market)",
            "L_tail_raw":  f"tail({B}, lower=-1.1, upper=1.1, newval=0)",
        }
        for k, v in cands.items():
            V.append((k, v, BASE_SETTINGS))
    if "K" in stage:      # 门控 × genius × 降prod 扩展电池（论坛验证过的结构）
        mF = re.search(r"ts_backfill\(vec_(?:sum|avg)\([^)]*\), \d+\)", base_expr)
        if mF:
            F = mF.group(0)
            X = f"multiply(rank(ts_mean({F}, 5)), rank(ts_mean({F}, 66)))"
            cands = {
                # —— 降 prod 组（论坛实测有效）——
                "K_tail_ind": f"tail(group_zscore({X}, industry), lower=-1.1, upper=1.1, newval=0)",  # 0.77→0.68 先例
                "K_mm":       f"subtract(ts_mean({X}, 5), ts_mean({X}, 22))",                      # mm 结构 0.86→0.67
                # —— genius 门控组 ——
                "K_tail_z":   f"tail(ts_zscore({X}, 252), lower=-1.5, upper=1.5, newval=0)",         # 时序zscore尾部截断
                "K_hump01":   f"hump(ts_backfill({X}, 3), hump=0.001)",                              # 小变动抑制
                "K_hump10":   f"hump(ts_backfill({X}, 3), hump=0.01)",                               # 中强度
                # —— 稀疏门控的「别的形式」——
                "K_tsq_gate": f"if_else(greater(ts_quantile({X}, 252), 0.85), {X}, 0)",              # 时序分位门（非截面）
                "K_gr_sub":   f"if_else(greater(group_rank({X}, subindustry), 0.85), {X}, 0)",       # 组内门
                "K_pow3":     f"power(rank({X}), 3)",                                                # 幂强调极端（非硬门）
                # —— 归一化/分组轴 ——
                "K_groupz":   f"group_zscore({X}, industry)",
                "K_gsd":      f"divide({X}, add(group_std_dev({X}, industry), 0.1))",                # 组内分歧度分母
            }
            for k, v in cands.items():
                V.append((k, v, BASE_SETTINGS))
    if "J" in stage:      # 幂压缩：signed_power 降 prod（项目铁律：幂 2.5 最优）
        mF = re.search(r"ts_backfill\(vec_(?:sum|avg)\([^)]*\), \d+\)", base_expr)
        if mF:
            F = mF.group(0)
            X = f"multiply(rank(ts_mean({F}, 5)), rank(ts_mean({F}, 66)))"
            for pw in (2.5, 3.0):
                v = f"signed_power({X}, {pw})"
                V.append((f"J_pow{str(pw).replace('.','p')}",
                          f"if_else(greater(rank({v}), 0.85), {v}, 0)", BASE_SETTINGS))
    if "I" in stage:      # 价差腿：同数据集两字段各自的信号相减（合规多腿三路之一）
        mF = re.search(r"ts_backfill\(vec_(?:sum|avg)\(([^)]*)\), (\d+)\)", base_expr)
        alt = ALT_FIELD[0] if ALT_FIELD else None
        if mF and alt:
            F1 = f"ts_backfill(vec_sum({mF.group(1)}), {mF.group(2)})"
            F2 = f"ts_backfill(vec_sum({alt}), {mF.group(2)})"
            def prod(F):
                return f"multiply(rank(ts_mean({F}, 5)), rank(ts_mean({F}, 66)))"
            for q in (0.80, 0.85):
                X = f"subtract(rank({prod(F1)}), rank({prod(F2)}))"
                V.append((f"I_spread_{alt.split('_')[-1]}_q{int(q*100)}",
                          f"if_else(greater(rank({X}), {q}), {X}, 0)", BASE_SETTINGS))
    if "H" in stage:      # 结构轴：换归一化层 / 三窗 / 残差化 / 分组
        mF = re.search(r"ts_backfill\(vec_(?:sum|avg)\([^)]*\), \d+\)", base_expr)
        if mF:
            F = mF.group(0)
            X = f"multiply(rank(ts_mean({F}, 5)), rank(ts_mean({F}, 66)))"
            cands = {
                "H_zs":    f"multiply(ts_zscore(ts_mean({F}, 5), 252), ts_zscore(ts_mean({F}, 66), 252))",
                "H_tsr":   f"multiply(ts_rank(ts_mean({F}, 5), 252), ts_rank(ts_mean({F}, 66), 252))",
                "H_tri":   f"add(add(rank(ts_mean({F}, 5)), rank(ts_mean({F}, 22))), rank(ts_mean({F}, 66)))",
                "H_resid": f"subtract(rank({X}), ts_mean(rank({X}), 252))",
                "H_gr":    f"group_rank({X}, subindustry)",
            }
            for k, v in cands.items():
                V.append((k, f"if_else(greater(rank({v}), 0.85), {v}, 0)", BASE_SETTINGS))
    if "G" in stage:      # 极值档：decay 0/1 + 极窄/极宽 truncation
        for d in (0, 1):
            V.append((f"G_decay{d}", base_expr, {**BASE_SETTINGS, "decay": d}))
        for t in (0.02, 0.20):
            V.append((f"G_trunc{int(t*100):02d}", base_expr, {**BASE_SETTINGS, "truncation": t}))
    if "F" in stage:      # 双窗轴（改表达式）：直接替换窗口字面量，避免正则嵌套括号
        for ws, wl in ((3, 66), (5, 126), (10, 66), (5, 252)):
            e = base_expr.replace(", 5))", f", {ws}))").replace(", 66))", f", {wl}))")
            V.append((f"F_win{ws}_{wl}", e, BASE_SETTINGS))
    return V


def load_ck(path):
    if os.path.exists(path):
        try:
            return json.load(open(path, encoding="utf-8"))
        except Exception:
            pass
    return {"variants": {}}


def save_ck(path, ck):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(ck, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def dispatch_one(label, expr, st):
    fn = os.path.join(ROOT, "cache", f"_dev_{label}.txt")
    with open(fn, "w", encoding="utf-8") as fh:
        fh.write(expr.strip() + "\n")
    cmd = [VENV_PY, WQB_TOOLS, "dispatch", fn, "--label", f"dev_{label}",
           "--region", st["region"], "--universe", st["universe"],
           "--decay", str(st["decay"]), "--neutralization", st["neutralization"],
           "--truncation", str(st["truncation"]),
           "--nan-handling", st["nan_handling"], "--max-trade", st["max_trade"],
           "--simulation-mode", st.get("simulation_mode", "QUICK"),
           "--force", "--allow-probe-repeat"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
    m = re.search(r'"sim_id": "([^"]+)"', out)
    return (m.group(1) if m else None), out


async def resolve_alpha(client, get_json, sim_id, max_poll=60):
    """轮询一个 sim（单仿真或多仿真组）直到拿到 alpha。"""
    for i in range(max_poll):
        try:
            j = await get_json(client, f"/simulations/{sim_id}", tries=2, base_sleep=1.5)
        except Exception:
            await asyncio.sleep(15)
            continue
        st = j.get("status")
        if j.get("alpha"):
            return j["alpha"], "ok"
        ch = j.get("children") or []
        if ch:
            cj = await get_json(client, f"/simulations/{ch[0]}", tries=2, base_sleep=1.5)
            if cj.get("alpha"):
                return cj["alpha"], "ok"
            if cj.get("status") in ("FAIL", "ERROR"):
                return None, "fail"
        if st in ("ERROR", "FAIL"):
            return None, "fail"
        await asyncio.sleep(20)
    return None, "timeout"


async def fetch_metrics(client, get_json, aid):
    j = await get_json(client, f"/alphas/{aid}", tries=3, base_sleep=2.0)
    m = j.get("is") or {}
    checks = {x.get("name"): x for x in (m.get("checks") or []) if isinstance(x, dict)}
    two_year = m.get("twoYearSharpe")
    for nm in ("LOW_2Y_SHARPE", "IS_LADDER_SHARPE"):
        v = (checks.get(nm) or {}).get("value")
        if v is not None:
            two_year = v
            break
    sub = m.get("subUniverseSharpe")
    if (checks.get("LOW_SUB_UNIVERSE_SHARPE") or {}).get("value") is not None:
        sub = checks["LOW_SUB_UNIVERSE_SHARPE"]["value"]
    return {
        "alpha": aid, "s": m.get("sharpe"), "f": m.get("fitness"), "to": m.get("turnover"),
        "returns": m.get("returns"), "margin": m.get("margin"),
        "y2": two_year, "sub": sub,
        "gates": {g: {"value": (checks.get(g) or {}).get("value"),
                      "limit": (checks.get(g) or {}).get("limit"),
                      "result": (checks.get(g) or {}).get("result")}
                  for g in GATES if g in checks},
    }


def run_corr_batch(ck, ck_path, s_min=1.4):
    """对 S≥s_min 的变体批量查 prod/self（≤6 个/次，prod 端点是异步排队）。"""
    ids, seen = [], set()
    if ck.get("base_alpha"):
        ids.append(ck["base_alpha"]); seen.add(ck["base_alpha"])
    for k, v in ck["variants"].items():
        a = v.get("alpha")
        if a and a not in seen and (v.get("s") or 0) >= s_min and not v.get("prod"):
            ids.append(a); seen.add(a)
    if not ids:
        return
    # prod 端点是异步排队（单并发、一颗 1.5–7 分钟）：批别贪大，≤2 颗/批；
    # 一批超时也要能继续下一批，不能整批崩掉。
    for i in range(0, len(ids), 2):
        batch = ids[i:i + 2]
        try:
            out = subprocess.run([VENV_PY, WQB_TOOLS, "corr"] + batch,
                                 capture_output=True, text=True, timeout=900).stdout
        except subprocess.TimeoutExpired:
            print(f"  [corr] 批 {batch} 超时（900s），跳过本批")
            continue
        for line in out.splitlines():
            m = re.match(r"\s*(\w+)\s+prod=([-\d.]+)\s*\[\w+\]\s+self=([-\d.]+)", line)
            if not m:
                continue
            aid, prod, selfc = m.group(1), float(m.group(2)), float(m.group(3))
            for k, v in ck["variants"].items():
                if v.get("alpha") == aid:
                    v["prod"], v["self"] = prod, selfc
            if ck.get("base_alpha") == aid:
                ck.setdefault("base_corr", {})["prod"], ck["base_corr"]["self"] = prod, selfc
            print(f"  [corr] {aid} prod={prod} self={selfc}")
        save_ck(ck_path, ck)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--alpha", required=True, help="基础 alpha id")
    ap.add_argument("--stage", default="ABCDE")
    ap.add_argument("--poll", type=int, default=60)
    ap.add_argument("--alt-field", default=None, help="stage I 的第二字段")
    ap.add_argument("--corr", action="store_true", help="扫描后批量查 prod/self")
    ap.add_argument("--corr-smin", type=float, default=1.4)
    args = ap.parse_args()
    ALT_FIELD[0] = args.alt_field

    from brain_api import brain_client
    from wqb_tools import _get_json

    ck_path = os.path.join(ROOT, "results", f"targeted_dev_{args.tag}.json")
    ck = load_ck(ck_path)
    await brain_client.ensure_authenticated()

    base = await _get_json(brain_client, f"/alphas/{args.alpha}")
    base_expr = (base.get("regular") or {}).get("code")
    if not base_expr:
        print("[fatal] 取不到基础表达式")
        return
    print(f"[base] {args.alpha} 代码长度 {len(base_expr)}")
    ck["base_alpha"] = args.alpha
    ck["base_expr"] = base_expr
    save_ck(ck_path, ck)

    variants = build_variants(base_expr, args.stage)
    print(f"[plan] {len(variants)} 个变体")

    for label, expr, st in variants:
        rec = ck["variants"].get(label)
        if rec and (rec.get("alpha") or rec.get("state") in ("fail", "timeout")):
            print(f"[skip] {label} 已完成（{rec.get('alpha') or rec.get('state')}）")
            continue
        t0 = time.time()
        sim_id, out = dispatch_one(label, expr, st)
        if not sim_id:
            print(f"[fail] {label} 派发失败: {out[-160:]}")
            ck["variants"][label] = {"state": "dispatch_fail", "settings": st, "ts": datetime.now().isoformat()}
            save_ck(ck_path, ck)
            continue
        aid, state = await resolve_alpha(brain_client, _get_json, sim_id, args.poll)
        rec = {"sim_id": sim_id, "state": state, "settings": st,
               "ts": datetime.now().isoformat(), "elapsed": round(time.time() - t0, 1)}
        if aid:
            rec.update(await fetch_metrics(brain_client, _get_json, aid))
        ck["variants"][label] = rec
        save_ck(ck_path, ck)
        if aid:
            print(f"[ok] {label:20s} S={rec['s']} F={rec['f']} 2Y={rec['y2']} sub={rec['sub']} TO={rec['to']} ({rec['elapsed']}s)")
        else:
            print(f"[x ] {label:20s} state={state}")

    if args.corr:
        run_corr_batch(ck, ck_path, args.corr_smin)

    rows = [v for v in ck["variants"].values() if v.get("s") is not None]
    rows.sort(key=lambda v: -(v["s"] or -9))
    print("\n=== 按 S 排序 ===")
    print(f"{'label':22s} {'S':>6s} {'F':>6s} {'2Y':>6s} {'sub':>6s} {'TO':>7s} {'prod':>6s}  RA")
    for lab, v in sorted(ck["variants"].items(), key=lambda kv: -(kv[1].get("s") or -9)):
        if v.get("s") is None:
            continue
        ra = (v["s"] >= 1.58) and ((v["f"] or 0) >= 1.0) and ((v["y2"] or 0) >= 1.58) and ((v.get("prod") or 0) < 0.7)
        print(f"{lab:22s} {v['s']:6.2f} {v['f'] or 0:6.2f} {v['y2'] or 0:6.2f} {v['sub'] or 0:6.2f} "
              f"{v['to'] or 0:7.4f} {v.get('prod') if v.get('prod') is not None else -1:6.2f}  {'PASS' if ra else ''}")


if __name__ == "__main__":
    asyncio.run(main())
