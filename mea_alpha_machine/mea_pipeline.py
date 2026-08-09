# -*- coding: utf-8 -*-
"""
MEA 一二三阶流水线(自驱动,断点续跑)
规模设计:
  一阶: 精选 ~2800 候选(数据质量优先) -> 模拟 -> 按 |sharpe| 挑 top 2000
  二阶: top 400 x 5 group ops = 2000 -> 模拟 -> 挑 top 300
  三阶: top 100 x 16 trade_when combos = 1600 -> 模拟 -> 检查可提交
用法:
  python mea_pipeline.py           # 顺序执行全部阶段
  python mea_pipeline.py stage1    # 只跑生成一阶候选(不模拟)
  python mea_pipeline.py stage2    # 只跑一阶模拟
  python mea_pipeline.py stage3    # 只跑二阶模拟
  python mea_pipeline.py stage4    # 只跑三阶模拟
  python mea_pipeline.py stage5    # 三阶后挑选+check_submission
"""
import os
import sys
import time
import pickle
import datetime
import random
from collections import defaultdict

from mea_machine_lib import *

# ---------------- 配置 ----------------
REGION = "MEA"
UNIVERSE = "TOP400"
NEUT = "SUBINDUSTRY"

FIRST_ORDER_TARGET = 2800   # 一阶候选目标数(精选)
PICK_FIRST = 2000           # 一阶模拟后挑选数(用户指定)
PICK_SECOND_IN = 400        # 二阶输入:一阶挑选后取 top 400
SECOND_PER_EXPR = 5         # 二阶 group 算子数
PICK_SECOND = 300           # 二阶模拟后挑选数
PICK_THIRD_IN = 100         # 三阶输入
THIRD_PER_EXPR = 16         # 三阶每表达式 trade_when 组合数(精选)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE_DIR, "cache")
os.makedirs(CACHE, exist_ok=True)

FIELD_CACHE = os.path.join(CACHE, "mea_fields.pkl")
FO_PKL = os.path.join(CACHE, "stage1_first_order.pkl")
SO_PKL = os.path.join(CACHE, "stage2_second_order.pkl")
TH_PKL = os.path.join(CACHE, "stage3_third_order.pkl")
RESULT_PKL = os.path.join(CACHE, "final_result.pkl")

# ---------------- 字段精选 ----------------
# 数据集:alphaCount>1000 (MEA 全部有意义的),每数据集按 coverage 取 top N
DATASET_TOPN = {
    "pv1": 23,              # 基础行情全覆盖
    "analyst7": 40,         # 券商预期
    "fundamental6": 40,     # 基本面
    "fundamental72": 40,    # 综合基本面
    "model25": 40,          # 盈利质量
    "pv96": 30,             # 公司行为
    "model31": 30,          # 盈利质量模型
    "behavioral_signals": 7,
    "earnings3": 4,         # 财报日期(事件类)
    "analyst_base_ref": 4,
}
DATASETS = list(DATASET_TOPN.keys())
VEC_OPTS = ["vec_avg"]      # VECTOR 精简:只用 vec_avg(最稳最常用)

# 一阶算子模板:每字段 ~10-11 个表达式(含 raw)
def first_order_templates(field):
    t = []
    t.append(field)                                        # raw(已 winsorize/backfill)
    t.append(f"rank({field})")
    t.append(f"zscore({field})")
    t.append(f"ts_rank({field}, 22)")
    t.append(f"ts_zscore({field}, 22)")
    t.append(f"ts_delta({field}, 5)")
    t.append(f"ts_std_dev({field}, 22)")
    t.append(f"ts_mean({field}, 22)")
    t.append(f"ts_returns({field}, 5)")
    t.append(f"ts_scale({field}, 22)")
    t.append(f"group_rank({field}, densify(sector))")
    return t

# ---------------- 数据拉取(带缓存) ----------------
def load_mea_fields(s):
    if os.path.exists(FIELD_CACHE):
        with open(FIELD_CACHE, "rb") as f:
            return pickle.load(f)
    fields_map = {}
    for dd in DATASETS:
        df = get_datafields(s, dataset_id=dd, region=REGION, universe=UNIVERSE, delay=1)
        # 按 coverage 降序取 top N
        df = df.sort_values("coverage", ascending=False)
        fields_map[dd] = df.head(DATASET_TOPN[dd])
        print(f"{dd}: {len(df)} fields -> keep {len(fields_map[dd])}")
    with open(FIELD_CACHE, "wb") as f:
        pickle.dump(fields_map, f)
    return fields_map

def build_pc_fields(fields_map):
    """MATRIX 直接用;VECTOR 用 vec_avg 精简展开"""
    pc = []
    for dd, df in fields_map.items():
        for _, row in df.iterrows():
            fid = row["id"]
            ftype = row["type"]
            base = f"winsorize(ts_backfill({fid}, 120), std=4)"
            if ftype == "VECTOR":
                for vop in VEC_OPTS:
                    pc.append(f"winsorize(ts_backfill({vop}({fid}), 120), std=4)")
            else:
                pc.append(base)
    return pc

# ---------------- 一阶候选 ----------------
def gen_first_order(s):
    fields_map = load_mea_fields(s)
    pc_fields = build_pc_fields(fields_map)
    print(f"pc_fields: {len(pc_fields)}")
    cands = []
    for field in pc_fields:
        for expr in first_order_templates(field):
            cands.append(expr)
    # 去重
    cands = list(dict.fromkeys(cands))
    random.seed(42)
    random.shuffle(cands)
    if len(cands) > FIRST_ORDER_TARGET:
        cands = cands[:FIRST_ORDER_TARGET]
    fo_list = [(a, 4) for a in cands]   # (expr, decay=4)
    with open(FO_PKL, "wb") as f:
        pickle.dump(fo_list, f)
    print(f"first order candidates: {len(fo_list)}")
    return fo_list

# ---------------- 模拟(带登录刷新) ----------------
def mea_multi_simulate(alpha_list, tag, start=0):
    """与 multi_simulate 等价,但每 pool 后刷新登录,写进度日志"""
    alpha_pools = load_task_pool(alpha_list, 10, 9)
    total_pools = len(alpha_pools)
    log = os.path.join(BASE_DIR, f"log_{tag}.txt")
    # 断点续跑:若日志已有完成记录,自动跳过
    done_pools = set()
    if os.path.exists(log):
        with open(log, encoding="utf-8") as f:
            for line in f:
                if f"[{tag}] pool" in line:
                    try:
                        n = int(line.split("pool ")[1].split("/")[0])
                        done_pools.add(n)
                    except Exception:
                        pass
    for x, pool in enumerate(alpha_pools):
        pool_no = x + 1
        if pool_no in done_pools:
            print(f"[{tag}] pool {pool_no}/{total_pools} already done, skip", flush=True)
            continue
        if x < start:
            continue
        s = login()
        progress_urls = []
        for y, task in enumerate(pool):
            sim_data_list = generate_sim_data(task, REGION, UNIVERSE, NEUT)
            # POST 失败重试(最多 5 次,间隔递增),避免漏提交
            for attempt in range(5):
                try:
                    resp = s.post("https://api.worldquantbrain.com/simulations", json=sim_data_list)
                    progress_urls.append(resp.headers["Location"])
                    break
                except Exception as e:
                    print(f"pool {x} task {y} post attempt {attempt+1} error: {e}", flush=True)
                    time.sleep(min(30 * (attempt + 1), 120))
                    s = login()
            else:
                print(f"pool {x} task {y} give up after 5 attempts", flush=True)
        for j, progress in enumerate(progress_urls):
            while True:
                try:
                    sim = s.get(progress)
                    ra = sim.headers.get("Retry-After", 0)
                    if ra == 0:
                        break
                    time.sleep(float(ra))
                except Exception:
                    time.sleep(30)
                    s = login()
        line = f"[{tag}] pool {pool_no}/{total_pools} done ({time.strftime('%H:%M:%S')})"
        print(line, flush=True)
        with open(log, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        # 每个 pool 完成后都保存断点
        with open(os.path.join(CACHE, f"progress_{tag}.pkl"), "wb") as f:
            pickle.dump({"done": pool_no}, f)
    print(f"[{tag}] ALL DONE", flush=True)

# ---------------- 效果挑选 ----------------
def fetch_top_is_alphas(s, top_n, date_start, date_end):
    """拉取窗口内 MEA 全部 IS alpha,按 |sharpe| 排序取 top_n;
    负 sharpe 的表达式取反(与顾问原逻辑一致)"""
    recs = []
    offset = 0
    while True:
        url = ("https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d" % offset
               + "&status=UNSUBMITTED%1FIS_FAIL"
               + "&dateCreated%3E=" + date_start + "T00:00:00-04:00"
               + "&dateCreated%3C" + date_end + "T00:00:00-04:00"
               + "&settings.region=" + REGION + "&order=-is.sharpe&hidden=false&type!=SUPER")
        resp = None
        for attempt in range(6):
            try:
                resp = s.get(url)
                break
            except Exception as e:
                print(f"fetch offset {offset} attempt {attempt+1} error: {type(e).__name__}", flush=True)
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
    # 按 |sharpe| 排序;负 sharpe 取反
    for r in recs:
        if r[2] < 0:
            r[1] = "-" + r[1]
            r[2] = -r[2]
    recs.sort(key=lambda r: r[2], reverse=True)
    print(f"fetched {len(recs)} alphas, top sharpe={recs[0][2]:.2f}" if recs else "no alphas fetched")
    return recs[:top_n]

def apply_decay_recs(recs):
    """依据 turnover 决定加大 decay(沿用顾问 get_alphas 逻辑)"""
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
    """top 400 x 5 group ops"""
    top = recs[:PICK_SECOND_IN]
    group_ops = ["group_neutralize", "group_rank", "group_normalize", "group_scale", "group_zscore"]
    so = []
    for expr, decay in apply_decay_recs(top):
        for alpha in get_group_second_order_factory([expr], group_ops, "mea"):
            so.append((alpha, decay))
    with open(SO_PKL, "wb") as f:
        pickle.dump(so, f)
    print(f"second order candidates: {len(so)}")
    return so

def gen_third_order(recs):
    """top 100 x 精选 trade_when 组合(16 个/expr)"""
    top = recs[:PICK_THIRD_IN]
    # 精选 open 事件(通用性强,MEA 字段均存在)与 exit 事件
    open_ev = [
        "ts_arg_max(volume, 5) == 0",
        "ts_corr(close, volume, 20) < 0",
        "ts_corr(close, volume, 5) > 0.3",
        "ts_mean(volume,10)>ts_mean(volume,60)",
        "group_rank(ts_std_dev(returns,60), sector) > 0.7",
        "ts_zscore(returns,60) > 2",
        "ts_skewness(returns,120)> 0.7",
        "ts_std_dev(returns, 5) > ts_std_dev(returns, 20)",
    ]
    exit_ev = ["abs(returns) > 0.1", "-1"]
    th = []
    for expr, decay in apply_decay_recs(top):
        for oe in open_ev:
            for ee in exit_ev:
                th.append(("trade_when(%s, %s, %s)" % (oe, expr, ee), decay))
    with open(TH_PKL, "wb") as f:
        pickle.dump(th, f)
    print(f"third order candidates: {len(th)}")
    return th

# ---------------- 阶段调度 ----------------
def date_window():
    today = datetime.date.today()
    start = (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    end = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return start, end

def stage1():
    s = login()
    gen_first_order(s)

def stage2():
    with open(FO_PKL, "rb") as f:
        fo = pickle.load(f)
    print(f"simulating first order: {len(fo)}")
    mea_multi_simulate(fo, "first")

def stage3():
    s = login()
    ds, de = date_window()
    recs = fetch_top_is_alphas(s, PICK_FIRST, ds, de)
    with open(os.path.join(CACHE, "pick_first.pkl"), "wb") as f:
        pickle.dump(recs, f)
    print(f"picked {len(recs)} for second order")
    gen_second_order(recs)
    with open(SO_PKL, "rb") as f:
        so = pickle.load(f)
    mea_multi_simulate(so, "second")

def stage4():
    s = login()
    ds, de = date_window()
    recs = fetch_top_is_alphas(s, PICK_SECOND, ds, de)
    with open(os.path.join(CACHE, "pick_second.pkl"), "wb") as f:
        pickle.dump(recs, f)
    print(f"picked {len(recs)} for third order")
    gen_third_order(recs)
    with open(TH_PKL, "rb") as f:
        th = pickle.load(f)
    mea_multi_simulate(th, "third")

def stage5():
    s = login()
    ds, de = date_window()
    recs = fetch_top_is_alphas(s, 200, ds, de)
    stone_bag = [r[0] for r in recs]
    print(f"checking submission for {len(stone_bag)} alphas")
    gold_bag = []
    check_submission(stone_bag, gold_bag, 0)
    with open(RESULT_PKL, "wb") as f:
        pickle.dump({"gold": gold_bag}, f)
    print(f"GOLD: {len(gold_bag)}")
    for g in gold_bag:
        print(g)

STAGES = {"stage1": stage1, "stage2": stage2, "stage3": stage3,
          "stage4": stage4, "stage5": stage5}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "all":
        stage1(); stage2(); stage3(); stage4(); stage5()
    else:
        STAGES[which]()
    print("=== pipeline finished ===")
