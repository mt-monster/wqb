# -*- coding: utf-8 -*-
"""
GLB 一二三阶流水线(参考顾问代码,断点续跑)
流程:
  一阶: get_first_order(GLB fields, ops_set, "glb") -> 模拟 -> 每10轮出总结
  二阶: top N -> group_ops(field) -> 模拟 -> 每10轮出总结
  三阶: top N -> trade_when(open_event, field, exit_event) -> 模拟 -> 每10轮出总结

用法:
  python glb_pipeline.py            # 顺序执行全部阶段
  python glb_pipeline.py field_scan # 仅扫描 GLB 字段
  python glb_pipeline.py stage1     # 生成+模拟一阶
  python glb_pipeline.py stage2     # 生成+模拟二阶
  python glb_pipeline.py stage3     # 生成+模拟三阶
  python glb_pipeline.py stage4     # 检查可提交 alpha
"""
import os
import sys
import time
import json
import pickle
import datetime
import random
import subprocess
from collections import defaultdict

# 导入 glb_machine_lib (自包含,修复 twin_field_factory 全局变量问题)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_machine_lib import (
    login, get_datafields, get_datasets, process_datafields,
    get_first_order, get_group_second_order_factory,
    trade_when_factory, load_task_pool, generate_sim_data, multi_simulate,
    get_alphas, get_check_submission, check_submission, locate_alpha, view_alphas,
    prune,
    ts_ops, basic_ops, arsenal, twin_field_ops, group_ops_list, SECOND_GROUP_OPS, ops_set,
    ts_comp_factory, vector_factory, group_factory,
)

# 别名兼容
group_ops = group_ops_list

# ==================== 配置 ====================
REGION = "GLB"
UNIVERSE = "TOP3000"
NEUT = "SUBINDUSTRY"
DELAY = 1

# ==================== 参考 WebData 的 GLB 数据集 ====================
# 当前仅运行 analyst15 (用户指定)
REF_DATASETS = {
    'analyst15': {'universe': 'TOP3000', 'total_fields': 307, 'avg_cov': 0.94},
}

# 方案D: top 150 fields (按coverage降序), 砍掉冷门字段
FIELD_PER_DATASET = 150
DATASET_MIN_ALPHA = 5000

# 单数据集(307 fields)可跑全量,放宽上限
FIRST_ORDER_MAX = 50000

# 阶间挑选
PICK_FIRST = 2000             # 一阶后挑选数(用于二阶)
PICK_SECOND_IN = 20           # 二阶输入(从 stage1 top 20 选)
SECOND_GROUP_OPS = ["group_neutralize", "group_rank", "group_zscore"]
PICK_SECOND = 100             # 二阶后挑选数(用于三阶)
PICK_THIRD_IN = 20            # 三阶输入(从 stage2 top 20 选, 避免 1300 候选爆炸)
SECOND_GROUP_FILTER = ["market", "sector", "industry"]

# 三阶:GLB 专用 open events
GLB_OPEN_EVENTS = [
    "ts_arg_max(volume, 5) == 0",
    "ts_corr(close, volume, 20) < 0",
    "ts_corr(close, volume, 5) < 0",
    "ts_mean(volume,10)>ts_mean(volume,60)",
    "group_rank(ts_std_dev(returns,60), sector) > 0.7",
    "ts_zscore(returns,60) > 2",
    "ts_arg_min(volume, 5) > 3",
    "ts_std_dev(returns, 5) > ts_std_dev(returns, 20)",
    "ts_arg_max(close, 5) == 0",
    "ts_arg_max(close, 20) == 0",
    "ts_corr(close, volume, 5) > 0.3",
    "ts_corr(close, volume, 20) > 0.3",
]
GLB_EXIT_EVENTS = ["abs(returns) > 0.1", "-1"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE_DIR, "cache")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")
os.makedirs(CACHE, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)
# 归因分析间隔: 每 N 个批次跑一次
# Stage2 (45 tasks): 间隔 5 → ~9 份报告
# Stage3 (130 tasks): 间隔 5 → ~26 份报告
ANALYSIS_INTERVAL = 5

FIELD_CACHE = os.path.join(CACHE, "glb_fields.pkl")
FO_PKL = os.path.join(CACHE, "stage1_first_order.pkl")
SO_PKL = os.path.join(CACHE, "stage2_second_order.pkl")
TH_PKL = os.path.join(CACHE, "stage3_third_order.pkl")
SUMMARY_LOG = os.path.join(BASE_DIR, "glb_summary.log")
# 已知必死的字段(平台稳定报 'too much resource'),从所有阶段剔除
BLOCKED_FIELDS_FILE = os.path.join(CACHE, "blocked_fields.txt")

# ==================== 字段扫描 ====================
def scan_glb_datasets(s):
    """获取 GLB 全部数据集(参考+补充展示)"""
    ds_df = get_datasets(s, region=REGION, universe='TOP3000', delay=DELAY)
    print(f"{'数据集':15s} | {'alphaCount':>10s} | {'fields':>6s} | {'coverage':>8s} | 参考")
    print("-" * 70)
    for _, row in ds_df.sort_values('alphaCount', ascending=False).iterrows():
        ref_tag = "★" if row['id'] in REF_DATASETS else "  "
        cov = row.get('coverage', 0)
        print(f"{row['id']:15s} | {row['alphaCount']:>10} | {row['fieldCount']:>6} | {cov:>8.2f} | {ref_tag}")
    print(f"\n参考数据集(WebData): {list(REF_DATASETS.keys())}")
    return ds_df

def load_glb_fields(s):
    """按参考数据集拉取字段,缓存"""
    if os.path.exists(FIELD_CACHE):
        with open(FIELD_CACHE, "rb") as f:
            return pickle.load(f)
    all_fields = {}
    print(f"\n拉取 {len(REF_DATASETS)} 个参考数据集字段...")
    for dd, info in REF_DATASETS.items():
        uni = info['universe']
        df = get_datafields(s, dataset_id=dd, region=REGION, universe=uni, delay=DELAY)
        if FIELD_PER_DATASET and len(df) > FIELD_PER_DATASET:
            df = df.sort_values("coverage", ascending=False).head(FIELD_PER_DATASET)
        all_fields[dd] = df
        n_m = len(df[df['type'] == 'MATRIX']) if len(df) > 0 else 0
        n_v = len(df[df['type'] == 'VECTOR']) if len(df) > 0 else 0
        print(f"  {dd:12s} ({uni}): {len(df)} fields (M={n_m}, V={n_v})")
    with open(FIELD_CACHE, "wb") as f:
        pickle.dump(all_fields, f)
    return all_fields

def build_pc_fields(fields_map):
    """MATRIX 直接包 winsorize/backfill;VECTOR 展开 vec_avg/vec_sum/vec_ir
       注意: other432 是 MINVOL1M 数据集,在 TOP3000 模拟中覆盖会偏低"""
    pc = []
    warnings = []
    for dd, df in fields_map.items():
        ref_info = REF_DATASETS.get(dd, {})
        if ref_info.get('universe') != UNIVERSE:
            warnings.append(f"  ⚠ {dd} universe={ref_info.get('universe')} != sim {UNIVERSE}, 覆盖可能偏低")
        temp = process_datafields(df, "matrix") + process_datafields(df, "vector")
        pc.extend(temp)
    print(f"总 PC fields: {len(pc)}")
    for w in warnings:
        print(w)
    return pc

# ==================== 一阶 ====================
def gen_first_order(fields_map):
    """方案A: 仅输出 raw 字段(150 个),零算子,最快验证"""
    pc_fields = build_pc_fields(fields_map)
    # 方案A: 直接返回原始 PC 字段,不加任何算子
    fo = pc_fields
    random.seed(42)
    random.shuffle(fo)
    if len(fo) > FIRST_ORDER_MAX:
        fo = fo[:FIRST_ORDER_MAX]
    fo_list = [(a, 4) for a in fo]
    with open(FO_PKL, "wb") as f:
        pickle.dump(fo_list, f)
    print(f"一阶候选(写入文件): {len(fo_list)}")
    return fo_list

# ==================== 带总结的模拟 ====================
def multi_simulate_with_summary(alpha_list, tag, start=0, summary_every=10):
    """串行提交,适配 Token-Bucket 并发模型
       策略: 每组 8 个 multi-sim / 提交间隔 25s / 子任务错误容忍
    """
    SIMS_PER_BATCH = 4  # 减小批次避免平台资源耗尽(task11+ 全部 ERROR)
    SUBMIT_INTERVAL = 120  # 2分钟间隔,加速 stage3 (stage2 已验证可用)
    # 幂等续跑: 跳过被封禁字段 + 已模拟过的表达式, 避免重复提交/重踩死路
    blocked = _load_blocked_fields()
    if blocked:
        n0 = len(alpha_list)
        alpha_list = [a for a in alpha_list if a[0] not in blocked]
        skipped = n0 - len(alpha_list)
        if skipped:
            print(f"  [{tag}] skipped {skipped} blocked field(s)", flush=True)
    done_exprs = _load_done_expressions(tag)
    if done_exprs:
        n0 = len(alpha_list)
        alpha_list = [a for a in alpha_list if a[0] not in done_exprs]
        skipped = n0 - len(alpha_list)
        if skipped:
            print(f"  [{tag}] skipped {skipped} already-simulated expr(s)", flush=True)
    tasks = [alpha_list[i:i + SIMS_PER_BATCH] for i in range(0, len(alpha_list), SIMS_PER_BATCH)]
    total_tasks = len(tasks)
    log_file = os.path.join(BASE_DIR, f"log_{tag}.txt")

    # 断点续跑
    progress_file = os.path.join(CACHE, f"progress_{tag}.pkl")
    done = 0
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "rb") as f:
                done = pickle.load(f).get("done", 0)
        except Exception:
            pass

    stats = {"total_posted": 0, "total_success": 0, "total_errored": 0,
             "total_alphas": len(alpha_list), "start_time": time.time(),
             "done_at_resume": done}

    s = login()
    for x in range(done, total_tasks):
        task_no = x + 1
        task = tasks[x]
        if not task:
            continue
        sim_data_list = generate_sim_data(task, REGION, UNIVERSE, NEUT)

        # 提交(最多 15 次,429 退避 + proxy 容错)
        progress_url = None
        for attempt in range(15):
            try:
                resp = s.post("https://api.worldquantbrain.com/simulations", json=sim_data_list, timeout=60)
                if resp.status_code == 201:
                    progress_url = resp.headers.get("Location")
                    stats["total_posted"] += 1
                    break
                elif resp.status_code == 429:
                    wait = min(40 * (attempt + 1), 300)
                    print(f"  task {task_no}/{total_tasks} 429, wait {wait}s", flush=True)
                    time.sleep(wait)
                    s = login()
                else:
                    print(f"  task {task_no} attempt {attempt+1}: HTTP {resp.status_code}", flush=True)
                    time.sleep(30)
                    s = login()
            except Exception as e:
                err_type = type(e).__name__
                print(f"  task {task_no} attempt {attempt+1}: {err_type}", flush=True)
                if "ProxyError" in err_type or "MaxRetryError" in err_type:
                    time.sleep(60)  # Proxy errors need longer wait
                else:
                    time.sleep(min(30 * (attempt + 1), 120))
                s = login()
        if not progress_url:
            stats["total_errored"] += SIMS_PER_BATCH
            print(f"  task {task_no}/{total_tasks} GIVE UP", flush=True)
            time.sleep(SUBMIT_INTERVAL)
            continue

        # 轮询状态
        child_results = {}
        max_wait = 600  # 10 分钟超时(sims 通常 8-12 分钟完成)
        waited = 0
        last_progress = -1
        while waited < max_wait:
            try:
                sim = s.get(progress_url, timeout=30)
                ra = sim.headers.get("Retry-After", 0)
                if ra == 0:
                    data = sim.json()
                    status = data.get("status", "UNKNOWN")
                    children = data.get("children", [])
                    progress = data.get("progress")
                    if status == "COMPLETE":
                        child_results = children
                        break
                    elif status in ("ERROR", "DONE"):
                        child_details = {}
                        for cid in children:
                            if isinstance(cid, dict):
                                child_details[cid.get("id", "")] = cid
                            elif isinstance(cid, str):
                                try:
                                    cr = s.get(f"https://api.worldquantbrain.com/simulations/{cid}", timeout=15)
                                    child_details[cid] = cr.json()
                                except Exception:
                                    child_details[cid] = {"status": "UNKNOWN"}
                        child_results = child_details
                        break
                    elif progress is not None and progress != last_progress:
                        # Print progress update every 10%
                        if int(progress * 10) > last_progress * 10:
                            print(f"  task {task_no}/{total_tasks} sim progress={progress:.0%}", flush=True)
                            last_progress = progress
                        time.sleep(5)
                    else:
                        time.sleep(5)
                else:
                    time.sleep(float(ra))
            except Exception as e:
                err_type = type(e).__name__
                print(f"  task {task_no}/{total_tasks} poll err: {err_type}", flush=True)
                time.sleep(30)
                s = login()
            waited += 5
        if waited >= max_wait:
            print(f"  task {task_no}/{total_tasks} poll TIMEOUT after {waited}s", flush=True)
            # Try one final attempt to get children
            try:
                final = s.get(progress_url, timeout=15)
                if final.status_code == 200:
                    fd = final.json()
                    children = fd.get("children", [])
                    if children:
                        child_results = children
            except Exception:
                pass

        # 统计子任务
        batch_success = 0
        batch_error = 0
        error_records = []
        if child_results:
            if isinstance(child_results, list):
                # COMPLETE: children = [id1, id2, ...] -> 全部成功
                batch_success = len(child_results)
            elif isinstance(child_results, dict):
                # ERROR/DONE: children = {id: {status, message}}
                for cid, val in child_results.items():
                    if isinstance(val, dict):
                        st = val.get("status", "UNKNOWN")
                        if st == "COMPLETE":
                            batch_success += 1
                        else:
                            batch_error += 1
                            msg = str(val.get("message", ""))[:200]
                            if msg:
                                print(f"  task {task_no} child {cid}: {st} - {msg}", flush=True)
                            error_records.append({
                                "task_no": task_no, "child_id": cid, "status": st,
                                "message": msg, "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
                            })
                    else:
                        batch_success += 1
        # No child_results means poll timeout - mark as error
        if not child_results:
            batch_error = SIMS_PER_BATCH
            print(f"  task {task_no}/{total_tasks} no results (poll timeout)", flush=True)
            error_records.append({
                "task_no": task_no, "child_id": None, "status": "POLL_TIMEOUT",
                "message": "no child_results after max_wait",
                "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            })
        stats["total_success"] += batch_success
        stats["total_errored"] += batch_error

        # (c) 落盘子任务错误, 弥补原脚本只 print 到 stdout 的缺陷
        if error_records:
            _append_errors_batch(tag, error_records)

        # 获取并存储每个子任务的 IS 指标
        if child_results:
            if isinstance(child_results, list):
                child_ids = child_results
            elif isinstance(child_results, dict):
                child_ids = list(child_results.keys())
            else:
                child_ids = []
            if child_ids:
                records = fetch_child_results(s, child_ids, tag, task_no, task)
                _append_results_batch(tag, records)

        line = f"[{tag}] task {task_no}/{total_tasks} done succ={batch_success} err={batch_error} ({time.strftime('%H:%M:%S')})"
        print(line, flush=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        with open(progress_file, "wb") as f:
            pickle.dump({"done": task_no}, f)

        if task_no % summary_every == 0:
            _print_summary(tag, stats, task_no, total_tasks)

        # 每 N 个批次完成后运行归因分析 (避免噪音,间隔足够大信号更清晰)
        if task_no % ANALYSIS_INTERVAL == 0:
            _run_batch_analysis(tag, task_no, total_tasks)

        time.sleep(SUBMIT_INTERVAL)

    _print_final_summary(tag, stats, total_tasks)


def _print_summary(tag, stats, current, total):
    elapsed = time.time() - stats["start_time"]
    rate = stats["total_posted"] / (elapsed / 60) if elapsed > 0 else 0
    summary = (
        f"\n{'='*60}\n"
        f"[{tag}] === 每{10}轮总结 ===\n"
        f"  已完成 task: {current}/{total}\n"
        f"  已提交模拟数: {stats['total_posted']}\n"
        f"  总候选数: {stats['total_alphas']}\n"
        f"  用时: {elapsed/60:.1f} 分钟\n"
        f"  速率: {rate:.1f} tasks/min\n"
        f"  错误 task: {stats['total_errored']}\n"
        f"{'='*60}\n"
    )
    print(summary, flush=True)
    with open(SUMMARY_LOG, "a", encoding="utf-8") as f:
        f.write(summary)


def _print_final_summary(tag, stats, total):
    elapsed = time.time() - stats["start_time"]
    final = (
        f"\n{'='*60}\n"
        f"[{tag}] === 最终总结 ===\n"
        f"  全部完成: {total}/{total} tasks\n"
        f"  总提交: {stats['total_posted']}\n"
        f"  总候选: {stats['total_alphas']}\n"
        f"  总用时: {elapsed/60:.1f} 分钟\n"
        f"  错误 task: {stats['total_errored']}\n"
        f"{'='*60}\n"
    )
    print(final, flush=True)
    with open(SUMMARY_LOG, "a", encoding="utf-8") as f:
        f.write(final)

    # 自动调用因子归因分析
    print(f"\n[{tag}] 运行因子归因分析...", flush=True)
    analyze_script = os.path.join(BASE_DIR, "analyze_results.py")
    if os.path.exists(analyze_script):
        import subprocess
        venv_python = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "world-quant-brain-mcp", ".venv", "Scripts", "python.exe"
        )
        result = subprocess.run(
            [venv_python, analyze_script, tag, "--save"],
            capture_output=True, text=True, encoding="utf-8",
            timeout=120
        )
        if result.stdout:
            print(result.stdout[-3000:], flush=True)
        if result.stderr:
            print(result.stderr[-500:], flush=True)

        # 自动生成最终 Markdown 报告
        md_script = os.path.join(BASE_DIR, "generate_md_report.py")
        if os.path.exists(md_script):
            md_result = subprocess.run(
                [venv_python, md_script, tag],
                capture_output=True, text=True, encoding="utf-8", timeout=60
            )
            md_out = md_result.stdout or md_result.stderr
            print(md_out, flush=True)
    else:
        print(f"  analyze_results.py not found, skip", flush=True)


# ==================== 批次归因分析 ====================
def _run_batch_analysis(tag, task_no, total_tasks):
    """每 ANALYSIS_INTERVAL 个批次完成后运行归因分析"""
    analyze_script = os.path.join(BASE_DIR, "analyze_results.py")
    if not os.path.exists(analyze_script):
        return
    venv_python = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "world-quant-brain-mcp", ".venv", "Scripts", "python.exe"
    )
    print(f"\n[{tag}] batch {task_no}/{total_tasks} -> 归因分析 (间隔{ANALYSIS_INTERVAL}批次)...", flush=True)
    log = analyze_log(tag)
    with open(log, "a", encoding="utf-8") as af:
        af.write(f"\n{'='*60}\n"
                 f"batch {task_no}/{total_tasks} @ {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                 f"{'='*60}\n")
    result = subprocess.run(
        [venv_python, analyze_script, tag, "--top", "10"],
        capture_output=True, text=True, encoding="utf-8", timeout=120
    )
    report = result.stdout or result.stderr
    print(report, flush=True)
    with open(log, "a", encoding="utf-8") as af:
        af.write(report + "\n")

    # 自动生成 Markdown 报告
    md_script = os.path.join(BASE_DIR, "generate_md_report.py")
    if os.path.exists(md_script):
        md_result = subprocess.run(
            [venv_python, md_script, tag],
            capture_output=True, text=True, encoding="utf-8", timeout=60
        )
        md_out = md_result.stdout or md_result.stderr
        print(md_out, flush=True)
        with open(log, "a", encoding="utf-8") as af:
            af.write(md_out + "\n")


def analyze_log(tag):
    return os.path.join(ANALYSIS_DIR, f"analysis_{tag}.txt")


def _append_results_batch(tag, records):
    """Append a batch of result records to the JSONL file"""
    results_file = os.path.join(CACHE, f"results_{tag}.jsonl")
    with open(results_file, "a", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _load_blocked_fields():
    """读取被永久封禁的字段表达式集合(精确匹配)"""
    if not os.path.exists(BLOCKED_FIELDS_FILE):
        return set()
    blocked = set()
    with open(BLOCKED_FIELDS_FILE, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                blocked.add(s)
    return blocked


def _load_done_expressions(tag):
    """已写入 results_{tag}.jsonl 的 expression 集合, 用于断点续跑幂等跳过"""
    results_file = os.path.join(CACHE, f"results_{tag}.jsonl")
    done = set()
    if os.path.exists(results_file):
        with open(results_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    e = r.get("expression")
                    if e:
                        done.add(e)
                except Exception:
                    pass
    return done


def _append_errors_batch(tag, errors):
    """将子任务错误(含平台 message)持久化到 disk, 弥补原脚本只 print 的缺陷"""
    err_file = os.path.join(CACHE, f"errors_{tag}.jsonl")
    with open(err_file, "a", encoding="utf-8") as f:
        for e in errors:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def fetch_child_results(s, child_ids, tag, task_no, task):
    """Fetch IS metrics for each child simulation in a completed batch.
       Sim response has no is; must follow alpha ID -> /alphas/{id} to get metrics.
    """
    records = []
    for i, child_id in enumerate(child_ids):
        if i >= len(task):
            break
        alpha_expr = task[i][0]
        decay = task[i][1]
        record = {
            "alpha_id": child_id,
            "expression": alpha_expr,
            "decay": decay,
            "task_no": task_no,
            "child_index": i,
            "status": "UNKNOWN",
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        try:
            resp = s.get(f"https://api.worldquantbrain.com/simulations/{child_id}", timeout=30)
            if resp.status_code == 200:
                sim_data = resp.json()
                record["status"] = sim_data.get("status", "UNKNOWN")
                alpha_id = sim_data.get("alpha")
                if alpha_id:
                    aresp = s.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}", timeout=30)
                    if aresp.status_code == 200:
                        adata = aresp.json()
                        is_data = adata.get("is", {}) or {}
                        record["alpha_platform_id"] = alpha_id
                        record["is"] = {
                            "sharpe": is_data.get("sharpe"),
                            "turnover": is_data.get("turnover"),
                            "fitness": is_data.get("fitness"),
                            "margin": is_data.get("margin"),
                            "return": is_data.get("returns"),
                            "drawdown": is_data.get("drawdown"),
                            "pnl": is_data.get("pnl"),
                        }
                        # Extract sub-region sharpe for robustness
                        for sub in ["glbAmer", "glbApac", "glbEmea"]:
                            sub_data = is_data.get(sub, {}) or {}
                            record["is"][f"sharpe_{sub}"] = sub_data.get("sharpe")
                            record["is"][f"turnover_{sub}"] = sub_data.get("turnover")
                            record["is"][f"fitness_{sub}"] = sub_data.get("fitness")
                    else:
                        record["is"] = {}
                else:
                    record["is"] = {}
            else:
                record["status"] = f"HTTP_{resp.status_code}"
        except Exception as e:
            record["status"] = "FETCH_ERROR"
            record["error"] = str(e)[:80]
        records.append(record)
    return records


def build_stage1_summary(tag):
    """Read results from JSONL and return sorted list of completed alphas.
       This is the bridge between stage1 and stage2 — no API calls needed.
    """
    results_file = os.path.join(CACHE, f"results_{tag}.jsonl")
    if not os.path.exists(results_file):
        print(f"No results file: {results_file}")
        return []

    results = []
    with open(results_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    results.append(json.loads(line))
                except Exception:
                    pass

    # Filter by sharpe availability
    complete = [r for r in results if r.get("is", {}).get("sharpe") is not None]
    complete.sort(key=lambda r: abs(r["is"]["sharpe"]), reverse=True)

    total = len(results)
    n_complete = len(complete)
    print(f"Results: {total} total, {n_complete} with metrics")

    if n_complete > 0:
        print(f"\nTop 10 by |sharpe|:")
        for r in complete[:10]:
            ism = r["is"]
            print(f"  sharpe={ism['sharpe']:6.2f}  turnover={ism['turnover']:.2f}  "
                  f"fitness={ism['fitness']:.2f}  margin={ism['margin']:.4f}  "
                  f"return={ism['return']:.2f}  alpha={r['alpha_id']}")
            print(f"    expr={r['expression'][:100]}")
        print()

    return complete

# ==================== 挑选函数 ====================
def fetch_top_glb(s, top_n, date_start, date_end):
    """拉取 GLB 全部 IS alpha,按 |sharpe| 排序取 top_n"""
    recs = []
    offset = 0
    while True:
        url = ("https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d" % offset
               + "&status=UNSUBMITTED%1FIS_FAIL"
               + f"&dateCreated%3E={date_start}T00:00:00-04:00"
               + f"&dateCreated%3C{date_end}T00:00:00-04:00"
               + f"&settings.region={REGION}&order=-is.sharpe&hidden=false&type!=SUPER")
        resp = None
        for attempt in range(6):
            try:
                resp = s.get(url)
                break
            except Exception:
                time.sleep(min(30 * (attempt + 1), 120))
                s = login()
        if resp is None:
            break
        if "retry-after" in resp.headers:
            time.sleep(float(resp.headers["Retry-After"]))
            continue
        try:
            results = resp.json().get("results", [])
        except Exception:
            time.sleep(30)
            continue
        if not results:
            break
        for a in results:
            recs.append([a["id"], a["regular"]["code"], a["is"]["sharpe"],
                         a["is"]["turnover"], a["is"]["fitness"], a["is"]["margin"],
                         a["dateCreated"], a["settings"]["decay"]])
        if len(results) < 100:
            break
        offset += 100
    for r in recs:
        if r[2] < 0:
            r[1] = "-" + r[1]
            r[2] = -r[2]
    recs.sort(key=lambda r: r[2], reverse=True)
    print(f"fetched {len(recs)} GLB alphas, top sharpe={recs[0][2]:.2f}" if recs else "no alphas")
    return recs[:top_n]

def apply_decay_recs(recs):
    out = []
    for rec in recs:
        decay = rec[-1]
        turnover = rec[3]
        if turnover > 0.7:
            decay = decay * 4
        elif turnover > 0.5:
            decay = decay * 3
        elif turnover > 0.4:
            decay = decay * 2
        elif turnover > 0.35:
            decay = decay + 4
        elif turnover > 0.3:
            decay = decay + 2
        out.append([rec[1], decay])
    return out

def gen_second_order(recs):
    """top N -> 4 个已验证 group 算子(neutralize/rank/scale/zscore)"""
    top = recs[:PICK_SECOND_IN]
    so = []
    for expr, decay in apply_decay_recs(top):
        for alpha in get_group_second_order_factory([expr], SECOND_GROUP_OPS, "glb"):
            so.append((alpha, decay))
    with open(SO_PKL, "wb") as f:
        pickle.dump(so, f)
    print(f"二阶候选: {len(so)}")
    return so

def gen_third_order(recs):
    """top N -> trade_when"""
    top = recs[:PICK_THIRD_IN]
    th = []
    for expr, decay in apply_decay_recs(top):
        for oe in GLB_OPEN_EVENTS:
            for ee in GLB_EXIT_EVENTS:
                th.append(("trade_when(%s, %s, %s)" % (oe, expr, ee), decay))
    with open(TH_PKL, "wb") as f:
        pickle.dump(th, f)
    print(f"三阶候选: {len(th)}")
    return th

# ==================== 阶段调度 ====================
def date_window():
    today = datetime.date.today()
    start = (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    end = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return start, end

def stage0_field_scan():
    """仅扫描 GLB 字段,不模拟"""
    s = login()
    fields_map = load_glb_fields(s)
    pc_fields = build_pc_fields(fields_map)
    print(f"\n总可用 PC 字段: {len(pc_fields)}")
    print("字段样例:")
    for f in pc_fields[:5]:
        print(f"  {f}")

def stage1():
    """生成并模拟一阶"""
    s = login()
    fields_map = load_glb_fields(s)
    fo = gen_first_order(fields_map)
    print(f"\n开始模拟一阶: {len(fo)} 候选")
    multi_simulate_with_summary(fo, "glb_first", summary_every=10)

def stage2():
    """生成并模拟二阶 - 使用本地 stage1 结果,零 API 调用"""
    results = build_stage1_summary("glb_first")
    top = results[:PICK_SECOND_IN]
    # (b) 从 stage2 候选池剔除已知必死的 anl15_* 字段(精确匹配)
    blocked = _load_blocked_fields()
    if blocked:
        n0 = len(top)
        top = [r for r in top if r.get("expression") not in blocked]
        if n0 != len(top):
            print(f"stage2: excluded {n0 - len(top)} blocked field(s) from candidate pool")
    so = []
    for r in top:
        # 使用精简分组列表(仅4个核心分组),避免7分组膨胀
        for op in SECOND_GROUP_OPS:
            field = r["expression"]
            for grp in SECOND_GROUP_FILTER:
                alpha = f"{op}({field}, densify({grp}))"
                so.append((alpha, r["decay"]))
    with open(SO_PKL, "wb") as f:
        pickle.dump(so, f)
    print(f"开始模拟二阶: {len(so)} 候选 ({PICK_SECOND_IN} fields × {len(SECOND_GROUP_OPS)} ops × {len(SECOND_GROUP_FILTER)} groups)")
    multi_simulate_with_summary(so, "glb_second", summary_every=10)
    # ---- Stage2 完成后自动进入 Stage3 ----
    print(f"\n{'='*60}")
    print(f"[glb_second] Stage2 完成，自动进入 Stage3...")
    print(f"{'='*60}")
    stage3()

def stage3():
    """生成并模拟三阶 - 使用本地 stage2 结果,零 API 调用"""
    results = build_stage1_summary("glb_second")
    top = results[:PICK_THIRD_IN]
    th = []
    for r in top:
        for oe in GLB_OPEN_EVENTS:
            for ee in GLB_EXIT_EVENTS:
                th.append(("trade_when(%s, %s, %s)" % (oe, r["expression"], ee),
                           r["decay"]))
    with open(TH_PKL, "wb") as f:
        pickle.dump(th, f)
    print("开始模拟三阶:", len(th), "候选")
    multi_simulate_with_summary(th, "glb_third", summary_every=10)


def stage4():
    """检查可提交 alpha"""
    s = login()
    ds, de = date_window()
    recs = fetch_top_glb(s, 200, ds, de)
    stone_bag = [r[0] for r in recs]
    print(f"检查可提交: {len(stone_bag)} 个 alpha")
    gold_bag = []
    check_submission(stone_bag, gold_bag, 0)
    print(f"\n可提交 GOLD: {len(gold_bag)}")
    for g in gold_bag:
        print(g)
    if gold_bag:
        view_alphas(gold_bag)

STAGES = {"field_scan": stage0_field_scan, "stage1": stage1,
          "stage2": stage2, "stage3": stage3, "stage4": stage4}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "all":
        stage1(); stage2(); stage3(); stage4()
    elif which == "field_scan":
        stage0_field_scan()
    else:
        STAGES[which]()
    print("\n=== GLB pipeline finished ===")