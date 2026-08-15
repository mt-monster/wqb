#!/usr/bin/env python3
"""mine_core.py - 参数化 Alpha 挖掘模板（替代 mine_v6..v27 版本爆炸）。

设计目标
--------
- 所有"版本"差异都收敛为 **数据**（候选列表 + 设置），不再是 21 个复制粘贴的脚本。
- ace_lib 路径可配置：环境变量 WQ_ACE_LIB 优先，缺省回退到原 skill 路径（去硬编码，见优化建议⑧）。
- 内置 checkpoint / resume：每完成一个候选即增量落盘，中断重跑自动跳过已完成的，
  符合本项目回测脚本"断点续跑"纪律（见 .workbuddy/memory/ 回测研究纪律）。

用法
----
1. 在下方 `build_candidates()` 里以数据形式填写你的候选（name / code / settings）。
2. 运行：`python mining/scripts/mine_core.py`
3. 重跑会自动跳过已有结果的候选；输出在 `mining/runs/<TAG>_results.json`。

注意：本文件是模板，未硬编码任何真实策略；请按需填充 `build_candidates()`。
"""
import os, sys, json, time

# ---- ace_lib 可配置导入（优化建议⑧）----
SKILL_DIR = os.environ.get(
    "WQ_ACE_LIB",
    r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts",
)
sys.path.insert(0, SKILL_DIR)
import ace_lib  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNS_DIR = os.path.join(ROOT, "mining", "runs")
os.makedirs(RUNS_DIR, exist_ok=True)

TAG = "template"          # 改：每轮任务一个唯一 tag，避免结果互相覆盖
OUT_JSON = os.path.join(RUNS_DIR, f"{TAG}_results.json")
USE_MULTI = False         # True=批量 multi_alpha；False=逐个 single_alpha


def build_candidates():
    """返回候选列表：每项 (name, code, settings)。在此填充你的挖掘策略。"""
    # 示例（请替换为真实候选）：
    SET = {
        "instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000",
        "delay": 1, "decay": 6, "neutralization": "SUBINDUSTRY", "truncation": 0.08,
        "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
        "maxTrade": "ON", "language": "FASTEXPR", "visualization": False,
        "startDate": "2014-01-01", "endDate": "2023-12-31",
    }
    return [
        # ("C1_example", "rank(ts_zscore(close, 20))", dict(SET)),
    ]


def full_check(s, aid):
    """复刻 mine_v20 的硬闸门体检：返回是否全部硬闸通过。"""
    j = ace_lib.get_simulation_result_json(s, aid) if hasattr(ace_lib, "get_simulation_result_json") else {}
    sh = (j.get("is") or {}).get("sharpe")
    fit = (j.get("is") or {}).get("fitness")
    print(f"    -> {aid} sh={sh} fit={fit}")
    try:
        df = ace_lib.get_check_submission(s, aid)
        realfail = df[(df["result"] == "FAIL") & (df["name"] != "ALREADY_SUBMITTED")]
        if len(realfail):
            print(f"    HARD FAIL: {list(realfail['name'])}")
            return False
        print("    >>> ALL HARD GATES PASS")
        return True
    except Exception as e:
        print(f"    [check skipped] {e}")
        return None


def load_done():
    if os.path.exists(OUT_JSON):
        try:
            return {r["name"]: r for r in json.load(open(OUT_JSON)) if r.get("alpha_id")}
        except Exception:
            return {}
    return {}


def main():
    s = ace_lib.start_session()
    cands = build_candidates()
    if not cands:
        print("[mine_core] build_candidates() 为空——请先填写候选。退出。")
        return
    done = load_done()
    results = list(done.values())
    print(f"[mine_core] {len(cands)} 候选，已完成 {len(done)}，待跑 {len(cands) - len(done)}")

    pending = [c for c in cands if c[0] not in done]
    for name, code, settings in pending:
        sim = {"type": "REGULAR", "settings": settings, "regular": code}
        print(f"\n=== {name}\n  {code}", flush=True)
        try:
            if USE_MULTI:
                outs = ace_lib.simulate_multi_alpha(s, [sim])
                aid = outs[0].get("alpha_id")
            else:
                r = ace_lib.simulate_single_alpha(s, sim)
                aid = r.get("alpha_id")
            print(f"  -> alpha_id={aid}", flush=True)
            rec = {"name": name, "code": code, "alpha_id": aid}
            if aid:
                full_check(s, aid)
            results.append(rec)
        except Exception as e:
            print(f"  -> ERROR: {e}", flush=True)
            results.append({"name": name, "code": code, "alpha_id": None, "error": str(e)})
        # 增量落盘（checkpoint/resume）
        json.dump(results, open(OUT_JSON, "w"), indent=2)
        time.sleep(2)

    print(f"\n=== DONE === 结果已写入 {os.path.relpath(OUT_JSON, ROOT)}")
    for r in results:
        print(" ", r["name"], "->", r.get("alpha_id"))


if __name__ == "__main__":
    main()
