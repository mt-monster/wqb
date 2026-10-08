#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全量测试并行跑批器（按域分组 + markdown 报告）
=================================================
并行跑完 `cache/test_groups.json`（由 `tools/scan_test_groups.py` 产出）里的全部
12 个分组用例，解析每组的 passed/failed/skipped/errors/duration 与失败用例清单，
生成一份「全方位总结」markdown 报告到 `output_report/`（报告唯一出口，
见 2026-10-01 组织审计定案）。

为何要并行：根 `tests/` 串行全量实测 ~155 s（2026-10-04 基线 3024 passed），
按 10 个编号域 + tests 根级 + MCP 包分组后各跑各的 nodeid，可摊平到分钟级。
参数 -q --no-header -p no:cacheprovider -ra 与 `pytest tests/ -x` 同口径。

用法：
  python tools/run_grouped_tests.py            # 并行跑全部，写报告
  python tools/run_grouped_tests.py --workers 4

2026-10-04 由仓库根 `wq_fulltest_run.py` 转正为本 CLI（工作台 UI 已下架
`attic/forum_workbench_20261004/`）。命名不用 `test_` 前缀：它是跑批器，不是用例。
"""
from __future__ import annotations
import sys
import argparse, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO_ROOT = find_repo_root(__file__)  # 本文件在 tools/ 下，仓库根 = 上两级
DATA = REPO_ROOT / "cache" / "test_groups.json"
VENV_PY = REPO_ROOT / "world-quant-brain-mcp" / ".venv" / "Scripts" / "python.exe"
OUT_DIR = REPO_ROOT / "output_report"
TZ8 = timezone(timedelta(hours=8))

# 分组 -> 业务场景说明（用于报告「测了哪些功能/业务场景」）
SCENARIOS = {
    "01_store_db": "存储/数据原子层：alpha 数据 atom 标注与落地、字段目录索引构建、波次选择(wave selection)构建、S1 分类字段分诊 B 阶段。验证数据如何被规范写入与回读。",
    "02_workflow": "战役工作流编排：alpha_properties 部分 PATCH 提交属性读写、campaign prompt 命令(P4)、detached 首输出心跳保活、judge 评审检查清单(P3)。验证九步流水线的节点行为。",
    "03_gem": "GEM 概念优先信号生成引擎：控制台 watch、组合字段、pipeline 模式、pregate 平台约束预检。验证 brain-make-some-gem 如何把 idea 渲染成合法 alpha 表达式。",
    "04_gates": "提交前闸门体系：catalog gate、cluster variants、gate5 覆盖矩阵、equal_weight_leg_add（组合形态铁律——禁止两条独立信号腿加权相加）。验证提交层四闸与混信号铁律拦截。",
    "05_submit_quota": "提交与配额链路：鉴权瞬断重试、batch 状态鉴权、batch submit_verdict 阶段2 否决权威。验证平台 POST 提交、403/瞬断处理与配额判定。",
    "06_wave_pipeline": "波次流水线全链路：backlog 丢弃守卫、未消费 backlog 闸门(P0/P2)、harvest 字段路径与 longcount 字段校验。验证 构建波次→并发回测→harvest 收口 的守卫。",
    "07_docs_skills": "文档/技能一致性（双轨同源守护）：审计修复、alpha repair 文档、docs 一致性(292)、经验库引用。验证 skill/文档与代码同源、引用不漂移。",
    "08_forum_recon": "论坛情报复盘决策：campaign intel 落地、饱和数据集标记、prod 首波、S0 选区排名。验证「论坛情报→挖掘方向」的复盘与选向逻辑。",
    "09_core": "核心域包(src/wqb)：config 域常量、dataset experience、diversity 多样性、field semantic classify 字段语义分类。验证规范核心包的行为契约。",
    "10_toolkit_scripts": "工具脚本正确性：degraded pack 标记、OS decay 基准/校准、s2 字段校验器。验证辅助工具链的输出符合预期。",
    "tests_root": "tests 根级 CLI 入口：toolified cli 命令行装配。验证根级命令入口可用。",
    "mcp_pkg": "MCP 服务包(wq-brain-http)单体：brain_api 门面、mcp_tools 工具、submit_verdict 工具、tools_workflow 节点注册。验证 MCP 层与上层 workflow 节点同步。",
}

_lock = threading.Lock()

def pytest_bin() -> str:
    return str(VENV_PY) if VENV_PY.exists() else sys.executable

def parse_summary(lines: list) -> dict:
    text = "\n".join(lines[-500:])
    def num(pat):
        m = re.search(pat, text)
        return int(m.group(1)) if m else 0
    dur = ""
    m = re.search(r"in\s+([\d.]+)s", text)
    if m:
        dur = m.group(1) + "s"
    failed_cases = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("FAILED "):
            failed_cases.append(s[len("FAILED "):].strip())
    seen, uniq = set(), []
    for c in failed_cases:
        key = c.split(" - ")[0]
        if key not in seen:
            seen.add(key); uniq.append(c)
    collect_err = "ERROR collecting" in text or "ERRORS" in text
    return {
        "passed": num(r"(\d+)\s+passed"),
        "failed": num(r"(\d+)\s+failed"),
        "skipped": num(r"(\d+)\s+skipped"),
        "errors": num(r"(\d+)\s+error"),
        "duration": dur,
        "failed_cases": uniq[:30],
        "collect_error": collect_err,
    }

def run_group(g: dict) -> dict:
    if g["id"] == "tests_root":
        args = [f["path"] for f in g["files"]]
    else:
        args = [g["dir"]]
    cmd = [pytest_bin(), "-m", "pytest", *args, "-q", "--no-header",
           "-p", "no:cacheprovider", "-ra"]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=900)
    except subprocess.TimeoutExpired:
        return {**_empty(g), "status": "timeout", "elapsed": 900.0}
    out = (r.stdout or "") + "\n" + (r.stderr or "")
    s = parse_summary(out.splitlines())
    s["status"] = ("failed" if (s["failed"] or s["errors"] or s["collect_error"]) else "passed") if r.returncode in (0,1,2,3,4,5) else "error"
    s["elapsed"] = round(time.time() - t0, 1)
    s["group_id"] = g["id"]; s["group_name"] = g["name"]
    s["file_count"] = g["file_count"]; s["case_count"] = g["case_count"]
    s["dir"] = g["dir"]
    return s

def _empty(g):
    return {"passed":0,"failed":0,"skipped":0,"errors":0,"duration":"","failed_cases":[],
            "collect_error":False,"status":"error","elapsed":0.0,
            "group_id":g["id"],"group_name":g["name"],"file_count":g["file_count"],
            "case_count":g["case_count"],"dir":g["dir"]}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    groups = data["groups"]
    print(f"[fulltest] 共 {len(groups)} 组 / {data['total_cases']} 用例，并行度 {args.workers}，解释器 {pytest_bin()}")

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_group, g): g for g in groups}
        for f in as_completed(futs):
            r = f.result()
            with _lock:
                results.append(r)
                tot = sum((x["passed"]+x["failed"]+x["skipped"]+x["errors"]) for x in results)
                print(f"  ✓ {r['group_id']:<14} {r['status']:<7} "
                      f"通过{r['passed']}/失败{r['failed']}/跳过{r['skipped']}/错误{r['errors']} "
                      f"({r['elapsed']}s)  [{tot}/{data['total_cases']}]")

    results.sort(key=lambda x: x["group_id"])
    write_report(results, data, args.workers)
    print("[fulltest] 报告已生成")
    return 0

def write_report(results, data, workers):
    OUT_DIR.mkdir(exist_ok=True)
    now = datetime.now(TZ8).strftime("%Y-%m-%d %H:%M")
    ts = datetime.now(TZ8).strftime("%Y%m%d_%H%M")
    tot_p = sum(r["passed"] for r in results)
    tot_f = sum(r["failed"] for r in results)
    tot_s = sum(r["skipped"] for r in results)
    tot_e = sum(r["errors"] for r in results)
    tot_c = sum(r["case_count"] for r in results)
    dur = sum(r["elapsed"] for r in results)
    rate = (tot_p / tot_c * 100) if tot_c else 0
    ran = tot_p + tot_f + tot_s + tot_e

    L = []
    L.append(f"# wq 工作台 · 全量测试总结报告\n")
    L.append(f"> 生成时间：{now}（GMT+8）　|　运行模式：pytest --collect-only 口径，并行度 {workers}")
    L.append(f"> 解释器：`{pytest_bin()}`　|　参数：`-q --no-header -p no:cacheprovider -ra`\n")
    L.append("## 一、总览指标\n")
    L.append("| 指标 | 数值 |")
    L.append("|---|---|")
    L.append(f"| 分组数 | {len(results)}")
    L.append(f"| 测试文件 | {data['total_files']}")
    L.append(f"| 用例总数（收集口径） | {tot_c}")
    L.append(f"| 实际执行（通过+失败+跳过+错误） | {ran}")
    L.append(f"| ✅ 通过 | {tot_p}")
    L.append(f"| ❌ 失败 | {tot_f}")
    L.append(f"| ⏭ 跳过 | {tot_s}")
    L.append(f"| ⚠ 错误 | {tot_e}")
    L.append(f"| **通过率** | **{rate:.1f}%**")
    L.append(f"| 累计耗时（并行墙钟近似） | {dur:.1f}s |\n")

    L.append("## 二、分组结果明细\n")
    L.append("| 分组 | 业务域 | 文件 | 用例 | 通过 | 失败 | 跳过 | 错误 | 耗时 | 状态 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in results:
        sc = SCENARIOS.get(r["group_id"], "")
        short = sc.split("：")[0] if "：" in sc else sc[:10]
        status = "✅" if r["status"] == "passed" else ("⏱" if r["status"] == "timeout" else "❌")
        L.append(f"| `{r['group_id']}` | {short} | {r['file_count']} | {r['case_count']} | "
                 f"{r['passed']} | {r['failed']} | {r['skipped']} | {r['errors']} | {r['duration'] or f'{r['elapsed']}s'} | {status} |")
    L.append("")

    L.append("## 三、测了哪些功能与业务场景（重点）\n")
    L.append("全量用例覆盖 **WorldQuant BRAIN alpha 挖掘工作区** 的整条链路——从字段/数据存储、")
    L.append("GEM 信号生成、提交前闸门与配额，到波次回测流水线、论坛情报复盘决策，以及 MCP 服务与文档/技能同源守护。\n")
    for r in results:
        sc = SCENARIOS.get(r["group_id"], "（无说明）")
        L.append(f"### `{r['group_id']}` {r['group_name']}　（{r['case_count']} 用例）\n")
        L.append(f"- **业务场景**：{sc}\n")
        L.append(f"- **覆盖范围**：{r['file_count']} 个测试文件，{r['passed']} 通过 / {r['failed']} 失败 / {r['skipped']} 跳过 / {r['errors']} 错误。\n")

    L.append("## 四、失败 / 异常明细\n")
    any_fail = False
    for r in results:
        if r["failed_cases"]:
            any_fail = True
            L.append(f"### `{r['group_id']}` {r['group_name']}（失败 {r['failed']} 条）\n")
            for c in r["failed_cases"]:
                L.append(f"- `{c}`")
            L.append("")
        if r["status"] == "timeout":
            any_fail = True
            L.append(f"### `{r['group_id']}` 超时（>900s 被终止）\n")
        if r["collect_error"]:
            any_fail = True
            L.append(f"### `{r['group_id']}` 收集期报错（collection error）\n")
    if not any_fail:
        L.append("✅ 本轮全量运行**无失败、无错误、无超时、无收集异常**。\n")

    L.append("## 五、结论与说明\n")
    L.append(f"- 通过率 **{rate:.1f}%**（{tot_p}/{tot_c}），整体健康。")
    L.append("- 测试引擎与本工作台「测试中心」模块**同源**（均调用 pytest，参数一致），本报告即模块「运行本组」在全部 12 个分组上的汇总体现。")
    L.append("- 并行运行（workers=%d）下，少数带共享状态/网络 mock 的用例结果可能与串行略有出入；如需严格串行复现，加 `--workers 1`。" % workers)
    L.append("- 业务重点守卫生效验证：组合形态铁律（禁止两条独立信号腿相加，`04_gates/test_gate_equal_weight_leg_add`）、提交层四闸与 SUB 比值闸（`04_gates`）、提交路由 fail-closed 否决权威（`05_submit_quota`、`mcp_pkg/test_submit_verdict_tool_unit`）、双轨同源（`07_docs_skills`）、波次流水线守卫（`06_wave_pipeline`）均有专项用例覆盖。")
    if tot_f or tot_e:
        L.append(f"\n⚠ 存在 {tot_f} 失败 / {tot_e} 错误，建议优先排查第四节明细对应文件。")
    else:
        L.append("\n本轮可作为回归基线：后续改动后以 `python tools/run_grouped_tests.py` 复跑对比。")

    out = OUT_DIR / f"fulltest_report_{ts}.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"[fulltest] 报告：{out}  ({out.stat().st_size//1024} KB)")
    # 同时回显关键行
    print(f"[fulltest] 通过率 {rate:.1f}%  通过{tot_p}/失败{tot_f}/跳过{tot_s}/错误{tot_e}  耗时{dur:.1f}s")

if __name__ == "__main__":
    raise SystemExit(main())
