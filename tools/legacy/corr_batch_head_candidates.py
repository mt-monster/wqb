# -*- coding: utf-8 -*-
"""头部候选 prod/self 相关性批量测试（2026-09-14）。

目标：IND qMja95Q2 / 2rlVPwdw + USA N1QMJ10q + DEU 异族 5 颗。
流程：金字塔塔状态快照 → get_alpha_details 核验平台状态（ACTIVE/OS 即已点亮，跳过）
      → check_self_correlation(0.7) → check_correlation('production', 0.7)。
prod 走平台单并发队列（1-5 分钟/颗），串行执行；结果逐颗写 checkpoint，可断点续跑。
"""
import asyncio
import json
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
OUT = r"D:\coding\traeCN_project\wqb\logs\_corr_batch_results.json"
PYRAMID_OUT = r"D:\coding\traeCN_project\wqb\logs\_pyramid_snapshot.json"

TARGETS = [
    ("qMja95Q2", "IND", "mdl135 icc 族最强（sh 4.26 / ladder 2.97）"),
    ("2rlVPwdw", "IND", "mdl135 icc 族（sh 2.73 / ladder 2.36）"),
    ("N1QMJ10q", "USA", "2Y=4.25（sharpe 2.42 / fitness 1.47）"),
    ("le81Lq2e", "DEU", "other455_formula_r85（fit 2.05）"),
    ("6XrJ5OvE", "DEU", "model28_drift66_r82（fit 1.93）"),
    ("78ZMplOb", "DEU", "model25_squeeze2_r81（fit 1.91）"),
    ("N1Q3d6le", "DEU", "boundary_push_r76 M216（fit 1.89）"),
    ("6XrJLG8J", "DEU", "si3_subfam_r74（fit 1.83 / 2Y 2.60）"),
]


def load_state():
    try:
        return json.load(open(OUT, encoding="utf-8"))
    except Exception:
        return {}


def save_state(state):
    json.dump(state, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


async def main():
    from brain_api import brain_client

    await brain_client.ensure_authenticated()

    # 1) 金字塔塔状态快照（幂等，每次刷新）
    try:
        mult = await brain_client.get_pyramid_multipliers()
        palphas = await brain_client.get_pyramid_alphas()
        json.dump({"captured_at": datetime.now().isoformat(timespec="seconds"),
                   "multipliers": mult, "pyramid_alphas": palphas},
                  open(PYRAMID_OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"[pyramid] 快照已存 {PYRAMID_OUT}")
    except Exception as e:
        print(f"[pyramid] 快照失败（不阻塞）: {str(e)[:120]}")

    state = load_state()
    for aid, region, note in TARGETS:
        if aid in state and "error" not in state[aid] and state[aid].get("prod_corr", {}).get("max_correlation") is not None:
            print(f"[skip] {aid} 已有完整结果")
            continue
        print(f"\n===== {aid} ({region}) {note} =====")
        rec = {"region": region, "note": note}
        try:
            d = await brain_client.get_alpha_details(aid)
            st, stage = d.get("status"), d.get("stage")
            rec["platform_status"], rec["platform_stage"] = st, stage
            s = d.get("settings") or {}
            rec["settings"] = {k: s.get(k) for k in ("region", "universe", "delay", "neutralization")}
            print(f"  平台状态: {st}/{stage} | {rec['settings']}")
            if st == "ACTIVE" or stage == "OS":
                rec["skip_reason"] = "已在平台点亮（ACTIVE/OS），不重复提交"
                state[aid] = rec
                save_state(state)
                continue

            sc = await brain_client.check_self_correlation(aid, threshold=0.7)
            rec["self_corr"] = {"max": sc.get("max_correlation"), "pass": sc.get("passes_check"),
                                "status": sc.get("status")}
            print(f"  self_corr: max={sc.get('max_correlation')} pass={sc.get('passes_check')} ({sc.get('status')})")
            save_state(state)

            pc = await brain_client.check_correlation(aid, correlation_type="production", threshold=0.7)
            checks = pc.get("checks") or {}
            prod = checks.get("production") or {}
            rec["prod_corr"] = {"max": prod.get("max_correlation"), "pass": prod.get("passes_check"),
                                "status": prod.get("status", pc.get("status"))}
            print(f"  prod_corr: max={prod.get('max_correlation')} pass={prod.get('passes_check')}")
        except Exception as e:
            rec["error"] = str(e)[:200]
            print(f"  ERROR: {str(e)[:150]}")
        state[aid] = rec
        save_state(state)

    print("\n全部完成，checkpoint 已保存")


asyncio.run(main())
