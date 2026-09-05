# -*- coding: utf-8 -*-
"""增强流水线 v2 全量本地测试（零配额，假战役目录隔离，临时目录自动清理）。

覆盖 9 新脚本 + diversity_slots/diversity_audit 模板扩充 + gate 闸6 回归。
全部不触网。运行：python tests/test_enhance_v2.py
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.join(tempfile.gettempdir(), "wqb_enhance_v2_tst")
TOOLKIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLKIT_SCRIPTS = os.path.join(TOOLKIT, "scripts")
PY = r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"
CAM = os.path.join(ROOT, "GBR")
PASS, FAIL = [], []


def w(rel, obj, sig=False):
    p = os.path.join(CAM, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8-sig" if sig else "utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return p


def run(script, *args, expect_exit=0):
    cmd = [PY, os.path.join(TOOLKIT_SCRIPTS, script), "--campaign-dir", CAM] + list(args)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    ok = r.returncode == expect_exit
    (PASS if ok else FAIL).append(f"{script} {' '.join(args)}")
    if not ok:
        print(f"\n[FAIL] {script} {' '.join(args)} exit={r.returncode} expect={expect_exit}")
        print("stdout:", r.stdout[-1500:])
        print("stderr:", r.stderr[-1500:])
    return r


def check(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    if not cond:
        print(f"[FAIL] {name} {extra}")


def build_fixtures():
    if os.path.isdir(CAM):
        shutil.rmtree(CAM)  # 只清假战役目录（本文件在 skill tests/，不会被删）
    os.makedirs(CAM, exist_ok=True)
    # 1. settings（dir 名 GBR == region）
    w("config/settings.json", {
        "_doc": "test", "instrumentType": "EQUITY", "region": "GBR", "universe": "TOP700",
        "delay": 1, "neutralization": "SUBINDUSTRY", "decay": 4, "truncation": 0.08,
        "maxTrade": "ON", "pasteurization": "ON", "unitHandling": "VERIFY",
        "nanHandling": "ON", "language": "FASTEXPR", "visualization": False,
        "startDate": "2014-01-01", "endDate": "2023-12-31", "_multi_sim_batch_size": 8})
    # 2. thresholds（含 probe_scoring_v2 权重段）
    w("config/thresholds.json", {
        "probe_scoring_v2": {"w_sharpe": 1.2, "w_fitness": 0.8, "w_mirror": 0.5, "w_margin": 0.3,
                              "w_tvr": 0.2, "w_rn": 0.4, "w_breadth": 0.4, "cw_penalty": 0.4,
                              "green_min": 2.0, "yellow_min": 1.0, "breadth_bar": 0.4,
                              "tvr_low": 5, "tvr_high": 30, "rn_bar": 0.5,
                              "early_red_sh": 0.3, "red_2y_sh_abs_min": 0.8, "red_2y_max": 0.7},
        "probe_scoring": {"green_min": 2.0, "yellow_min": 1.0}})
    # 3. typed catalog（目标数据集 analyst9）
    w("reference/gbr_analyst9_fields.json", {
        "data_type": "MATRIX", "dataset": "analyst9",
        "fields": [{"id": f"anl9_f{i:02d}", "type": "MATRIX", "cov": 0.9} for i in range(12)]})
    # 4. 历史 results CSV
    def csv_rows(ds, exprs, sharpes, ms):
        return [{"id": f"{ds}{i}", "dataset": ds, "code": e, "sharpe": s, "fitness": 0.3,
                 "two_year_sharpe": 0.5, "margin_bp": 4.0, "turnover_pct": 15.0,
                 "rn_sharpe": 0.4, "rn_fitness": 0.2, "failed_checks": "['LOW_MARGIN']",
                 "multisim": ms, "batch_idx": i % 8}
                for i, (e, s) in enumerate(zip(exprs, sharpes))]
    rows = []
    rows += csv_rows("news20", [f"rank(vec_avg(nw20_f{i:02d}))" for i in range(6)],
                     [0.7] * 6, "MS1a")
    rows += csv_rows("news20", [f"rank(vec_avg(nw20_f{i:02d}))" for i in range(6, 12)],
                     [0.7] * 6, "MS1b")
    rows += csv_rows("model53", [f"rank(mdl53_f{i:02d})" for i in range(6)],
                     [0.2] * 6, "MS2a")
    rows += csv_rows("model53", [f"rank(mdl53_f{i:02d})" for i in range(6, 12)],
                     [0.2] * 6, "MS2b")
    anl = [f"rank(vec_avg(anl9_f{i:02d}))" for i in range(12)]
    anl_sh = [-0.55] + [0.15] * 11
    rows += csv_rows("analyst9", anl, anl_sh, "MS3")
    rows += csv_rows("analyst9", [f"rank(ts_backfill(vec_avg(anl9_f{i:02d}), 66))" for i in range(4)],
                     [0.2] * 4, "MS4")
    rows += csv_rows("analyst9", ["trade_when(greater(ts_rank(vec_avg(anl9_f00), 10), 0.5), vec_avg(anl9_f00), 0)"],
                     [0.1], "MS5")
    rows += csv_rows("ds_a", [f"rank(dsa_f{i:02d})" for i in range(4)], [0.85] * 4, "MSa1")
    rows += csv_rows("ds_a", [f"ts_rank(dsa_f{i:02d}, 120)" for i in range(4)], [0.8] * 4, "MSa2")
    rows += csv_rows("ds_b", [f"rank(dsb_f{i:02d})" for i in range(4)], [0.1] * 4, "MSb1")
    rows += csv_rows("ds_b", [f"ts_rank(dsb_f{i:02d}, 120)" for i in range(4)], [0.15] * 4, "MSb2")
    rows += csv_rows("ds_c", [f"rank(dsc_f{i:02d})" for i in range(4)], [0.82] * 4, "MSc1")
    rows += csv_rows("ds_c", [f"ts_rank(dsc_f{i:02d}, 120)" for i in range(4)], [0.81] * 4, "MSc2")
    os.makedirs(os.path.join(CAM, "results"), exist_ok=True)
    with open(os.path.join(CAM, "results", "fake_probe.csv"), "w", encoding="utf-8-sig", newline="") as f:
        wcsv = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wcsv.writeheader()
        wcsv.writerows(rows)
    # 5. candidates
    w("candidates/gbr_wave20_exprs.json", {
        "wave20": ["rank(vec_avg(anl9_f00))", "rank(vec_avg(anl9_f01))",
                   "rank(vec_avg(anl9_f02))", "ts_rank(vec_avg(anl9_f03), 120)",
                   "signed_power(vec_avg(anl9_f04), 2)", "log(vec_avg(anl9_f05) + 1)",
                   "trade_when(greater(ts_rank(vec_avg(anl9_f06), 10), 0.5), vec_avg(anl9_f06), 0)"]})
    # gate 闸6 合规批：含 group/ratio 骨架 + required_operators，无 vec_*（MATRIX 数据集）
    w("candidates/gbr_wave20_gate_ok.json", {
        "expressions": ["rank(anl9_f00)", "ts_rank(anl9_f01, 120)",
                        "signed_power(anl9_f02, 2)", "group_rank(anl9_f03, industry)",
                        "divide(anl9_f04, anl9_f05)",
                        "trade_when(greater(ts_rank(anl9_f06, 10), 0.5), anl9_f06, 0)"]})
    w("candidates/signal_a.json", {"exprs": [
        {"expr": "rank(vec_avg(anl9_f00))", "sharpe": 0.6},
        {"expr": "ts_rank(vec_avg(anl9_f01), 120)", "sharpe": 0.5}]})
    w("candidates/signal_b.json", {"exprs": [
        {"expr": "rank(mdl53_f00)", "sharpe": -0.5},
        {"expr": "rank(mdl53_f01)", "sharpe": 0.3}]})
    w("candidates/migrated_kor_analyst9.json", {"count": 0, "migrated": []})
    w("candidates/mix_sig.json", {"count": 0, "mixes": []})
    # 6. 台账（含 diversity_audit_latest 契约 + news20_dead 判死）
    w("gbr_d1_campaign_state.json", {
        "diversity_audit_latest": {
            "next_round_injections": {
                "issued_at": "2026-08-18", "expires_after_batches": 10,
                "per_batch_min_operators": 2,
                "required_operators": ["signed_power", "ts_rank"],
                "skeleton_quota": {"group": 1, "ratio": 1},
                "exempt": ["repair"], "consumed_batches": []}},
        "news20_dead": {"dataset": "news20", "reason": "test dead", "dead_at": "2026-08-18"},
        "model53_dead": {"dataset": "model53", "reason": "test dead", "dead_at": "2026-08-18"},
        "ds_b_dead": {"dataset": "ds_b", "reason": "test dead", "dead_at": "2026-08-18"}},
        sig=True)
    # 7. 迁移源目录（KOR candidates）
    os.makedirs(os.path.join(ROOT, "KORcand"), exist_ok=True)
    w("../KORcand/kor_win.json", {"w": ["rank(kor_f00)", "ts_rank(kor_f01, 120)"]})
    # 8. params/history for param_opt
    w("params.json", {"backfill_window": {"values": [33, 66, 120]}, "decay": {"values": [4, 6, 8]}})
    w("history.json", [
        {"params": {"backfill_window": 66, "decay": 4}, "score": 0.7},
        {"params": {"backfill_window": 66, "decay": 6}, "score": 0.5},
        {"params": {"backfill_window": 120, "decay": 4}, "score": 0.3},
        {"params": {"backfill_window": 33, "decay": 8}, "score": 0.1}])


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    build_fixtures()
    # ---- 0. py_compile 全部 ----
    for s in ["ortho_prescreen.py", "migrate_templates.py", "proxy_prescreen.py",
              "calibrate_probe.py", "param_opt.py", "fit_mix_weights.py", "build_mix.py",
              "neutralization_sweep.py", "rescue_checklist.py", "diversity_slots.py",
              "diversity_audit.py", "gate.py"]:
        r = subprocess.run([PY, "-m", "py_compile", os.path.join(TOOLKIT_SCRIPTS, s)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        check(f"py_compile {s}", r.returncode == 0, r.stderr[-500:])

    # ---- 1. ortho_prescreen ----
    run("ortho_prescreen.py", "--exprs", os.path.join(CAM, "candidates/gbr_wave20_exprs.json"))
    rep = json.load(open(os.path.join(CAM, "reference", "ortho_prescreen_report.json"), encoding="utf-8"))
    check("ortho: report 存在", "items" in rep and rep["strong_history"] > 0)
    check("ortho: 同质候选被剔除", rep["dropped"] >= 1, str(rep["dropped"]))

    # ---- 2. migrate_templates ----
    run("migrate_templates.py", "--src-dir", os.path.join(ROOT, "KORcand"),
        "--target-dataset", "analyst9", "--map", json.dumps({"kor_f00": "anl9_f07", "kor_f01": "anl9_f08"}))
    mig = json.load(open(os.path.join(CAM, "candidates", "migrated_KORcand_analyst9.json"), encoding="utf-8"))
    check("migrate: 迁移 2 条", mig["count"] == 2, str(mig["count"]))
    check("migrate: 字段替换生效", all("kor_f" not in m["expr"] for m in mig["migrated"]))

    # ---- 3. proxy_prescreen 训练 + 打分（先补 fhp 强候选行制造双类标签） ----
    with open(os.path.join(CAM, "results", "fake_probe.csv"), "a", encoding="utf-8-sig", newline="") as f:
        wcsv = csv.writer(f)
        for i in range(8):
            wcsv.writerow([f"fhp{i}", "fhp", f"rank(fhp_f{i:02d})", 0.9, 1.0, 0.8, 6.0, 20.0,
                           0.9, 0.8, "[]", "MS9", i])
    run("proxy_prescreen.py", "--train")
    check("proxy: 模型训练成功", os.path.exists(os.path.join(CAM, "reference", "proxy_model.joblib")))
    stats = json.load(open(os.path.join(CAM, "reference", "proxy_model_features.json"), encoding="utf-8"))
    check("proxy: 训练样本 >= 30", stats["stats"]["n_samples"] >= 30, str(stats["stats"]))
    run("proxy_prescreen.py", "--score", os.path.join(CAM, "candidates/gbr_wave20_exprs.json"), "--filter")
    check("proxy: 打分报告", os.path.exists(os.path.join(CAM, "reference", "proxy_score_report.json")))

    # ---- 4. calibrate_probe（fhp 已入 CSV，双类标签） ----
    run("calibrate_probe.py")
    cal = json.load(open(os.path.join(CAM, "reference", "probe_weights_calibrated.json"), encoding="utf-8"))
    check("calib: 校准输出存在", "weights" in cal and cal["stats"]["n"] >= 10)
    check("calib: 双类样本", cal["stats"]["n_pos"] >= 1, str(cal["stats"]))

    # ---- 5. param_opt TPE ----
    run("param_opt.py", "--params", os.path.join(CAM, "params.json"),
        "--history", os.path.join(CAM, "history.json"), "--top", "4")
    po = json.load(open(os.path.join(CAM, "reference", "param_opt_next.json"), encoding="utf-8"))
    check("paramopt: TPE 提议 4 组", len(po["suggestions"]) == 4)
    first = po["suggestions"][0]["params"]
    check("paramopt: 好档位优先（33 不占首位）", first["backfill_window"] != 33, str(first))
    check("paramopt: 建议含 good 窗口 66",
          any(s["params"]["backfill_window"] == 66 for s in po["suggestions"]))

    # ---- 6. build_mix ----
    run("build_mix.py", "--signal-a", os.path.join(CAM, "candidates/signal_a.json"),
        "--signal-b", os.path.join(CAM, "candidates/signal_b.json"), "--top-k", "2",
        "--weights", "0.5,0.5", "0.7,0.3")
    bm = json.load(open(os.path.join(CAM, "candidates", "mix_signal_a_signal_b.json"), encoding="utf-8"))
    check("build_mix: 方向修正", bm["direction_fixed"] is True)
    check("build_mix: mix 数量 = 2*2*2", bm["count"] == 8, str(bm["count"]))

    # ---- 7. neutralization_sweep ----
    run("neutralization_sweep.py", "--exprs", os.path.join(CAM, "candidates/gbr_wave20_exprs.json"),
        "--top-n", "2", "--neutralizations", "SUBINDUSTRY", "SECTOR")
    ns = json.load(open(os.path.join(CAM, "candidates", "settings_sweep_alpha_list.json"), encoding="utf-8"))
    check("neut: 2 档 × 2 条 = 4", len(ns) == 4, str(len(ns)))
    check("neut: per-item settings", all("settings" in a and "regular" in a for a in ns))
    check("neut: neutralization 覆盖", {a["settings"]["neutralization"] for a in ns} == {"SUBINDUSTRY", "SECTOR"})

    # ---- 8. rescue_checklist ----
    run("rescue_checklist.py", "--dataset", "model53", "--fail", expect_exit=1)
    rc = json.load(open(os.path.join(CAM, "reference", "rescue_checklist_model53.json"), encoding="utf-8"))
    check("rescue: 未全绿禁止判死", rc["all_pass"] is False)
    run("rescue_checklist.py", "--dataset", "analyst9", "--fail", expect_exit=1)
    # ---- 9. diversity_slots 新模板 ----
    r = run("diversity_slots.py")
    check("slots: 契约渲染含 signed_power 模板", "signed_power" in r.stdout, r.stdout[-300:])
    check("slots: 契约渲染含 ts_rank 模板", "ts_rank" in r.stdout)
    # ---- 10. gate 闸6 回归 ----
    # 同质批（single 骨架 + vec_* 违闸2）→ 拒绝且输出含 diversity 诊断
    r = run("gate.py", "--file", os.path.join(CAM, "candidates/gbr_wave20_exprs.json"),
            "--dataset", "analyst9", expect_exit=1)
    check("gate: 闸6 批级多样性字段出现", "diversity" in (r.stdout + r.stderr).lower())
    # 合规批（group/ratio 骨架 + required_operators）→ 全闸放行
    r = run("gate.py", "--file", os.path.join(CAM, "candidates/gbr_wave20_gate_ok.json"),
            "--dataset", "analyst9", expect_exit=0)
    check("gate: 合规批放行且闸6 达标", "diversity" in (r.stdout + r.stderr).lower())

    print(f"\n===== 测试完成: PASS={len(PASS)} FAIL={len(FAIL)} =====")
    if FAIL:
        print("FAILED ITEMS:")
        for x in FAIL:
            print(" -", x)
        sys.exit(1)
    print("ALL PASS")


if __name__ == "__main__":
    main()
