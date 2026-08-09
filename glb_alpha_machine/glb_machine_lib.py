# -*- coding: utf-8 -*-
"""
GLB 一二三阶 Alpha Machine 库(参考顾问 machine_lib.py)
适配 GLB 区域,修复 twin_field_factory 全局变量问题
"""
import requests
from os import environ
from time import sleep
import time
import json
import pandas as pd
import random
import pickle
from itertools import product
from collections import defaultdict

# ==================== 登录 ====================
def login():
    username = environ.get("BRAIN_EMAIL", "mthyzx@126.com")
    password = environ.get("BRAIN_PASSWORD", "asdqwe123!")
    last_err = None
    for attempt in range(20):
        try:
            s = requests.Session()
            s.auth = (username, password)
            response = s.post('https://api.worldquantbrain.com/authentication', timeout=30)
            if response.status_code != 201:
                raise RuntimeError(f"auth status {response.status_code}: {response.content[:200]}")
            return s
        except Exception as e:
            last_err = e
            err_type = type(e).__name__
            err_msg = str(e)[:120]
            print(f"  [login] attempt {attempt+1}/20 failed: {err_type}: {err_msg}", flush=True)
            if "ProxyError" in err_type or "MaxRetryError" in err_type or "ConnectionError" in err_type:
                time.sleep(30)  # Proxy errors are transient
            else:
                time.sleep(min(30 * (attempt + 1), 180))
    raise last_err

# ==================== 算子集 ====================
# 以下算子均经 /operators API 验证可用(2026-08-08)
# 不可用的已移除: log_diff, s_log_1p, fraction, scale_down (basic)
#                ts_skewness, ts_entropy, inst_tvr, sigmoid, ts_decay_exp_window,
#                ts_percentage, vector_neut, vector_proj, ts_moment, ts_min_max_cps,
#                ts_min_diff, ts_max (ts_ops)
basic_ops = ["log", "sqrt", "reverse", "inverse", "rank", "zscore",
             'quantile', "normalize"]

ts_ops = ["ts_rank", "ts_zscore", "ts_delta", "ts_sum", "ts_product",
          "ts_ir", "ts_std_dev", "ts_mean", "ts_arg_min", "ts_arg_max",
          "ts_max_diff", "ts_returns", "ts_scale", "ts_kurtosis",
          "ts_quantile"]

arsenal = ["signed_power"]

# 二阶 group 算子(API 验证: group_normalize 不可用)
SECOND_GROUP_OPS = ["group_neutralize", "group_rank", "group_scale", "group_zscore"]

twin_field_ops = ["ts_corr", "ts_covariance"]
group_ops_list = ["group_rank"]
group_ac_ops = ["group_sum", "group_mean", "group_std_dev"]
ops_set = basic_ops + ts_ops + arsenal + group_ops_list

# ==================== 数据拉取 ====================
def get_datafields(s, instrument_type='EQUITY', region='USA', delay=1,
                   universe='TOP3000', dataset_id='', search=''):
    base = ("https://api.worldquantbrain.com/data-fields?"
            f"instrumentType={instrument_type}"
            f"&region={region}&delay={str(delay)}&universe={universe}")
    if len(search) == 0:
        url_prefix = base + f"&dataset.id={dataset_id}&limit=50"
        url_template = url_prefix + "&offset={_off}"
        while True:
            resp = s.get(url_template.format(_off=0))
            if "retry-after" in resp.headers:
                time.sleep(float(resp.headers["Retry-After"]))
                continue
            try:
                count = resp.json()['count']
                break
            except Exception:
                time.sleep(30)
                continue
    else:
        url_template = base + f"&limit=50&search={search}" + "&offset={_off}"
        count = 100
    datafields_list = []
    for x in range(0, count, 50):
        while True:
            resp = s.get(url_template.format(_off=x))
            if "retry-after" in resp.headers:
                time.sleep(float(resp.headers["Retry-After"]))
                continue
            try:
                datafields_list.append(resp.json()['results'])
                break
            except Exception:
                time.sleep(30)
                continue
    flat = [item for sublist in datafields_list for item in sublist]
    return pd.DataFrame(flat)

def get_datasets(s, instrument_type='EQUITY', region='USA', delay=1, universe='TOP3000'):
    url = ("https://api.worldquantbrain.com/data-sets?"
           f"instrumentType={instrument_type}&region={region}"
           f"&delay={str(delay)}&universe={universe}")
    result = s.get(url)
    return pd.DataFrame(result.json()['results'])

def get_vec_fields(fields):
    vec_ops = ["vec_avg", "vec_sum", "vec_ir", "vec_max", "vec_count", "vec_skewness", "vec_stddev", "vec_choose"]
    vec_fields = []
    for field in fields:
        for vec_op in vec_ops:
            if vec_op == "vec_choose":
                vec_fields.append(f"{vec_op}({field}, nth=-1)")
                vec_fields.append(f"{vec_op}({field}, nth=0)")
            else:
                vec_fields.append(f"{vec_op}({field})")
    return vec_fields

def process_datafields(df, data_type):
    if data_type == "matrix":
        datafields = df[df['type'] == "MATRIX"]["id"].tolist()
    elif data_type == "vector":
        datafields = get_vec_fields(df[df['type'] == "VECTOR"]["id"].tolist())
    return [f"winsorize(ts_backfill({f}, 120), std=4)" for f in datafields]

# ==================== 表达式工厂(顾问 get_first_order 复刻) ====================
def ts_factory(op, field):
    days = [5, 22, 66]  # 方案D: 去掉 120/240 天, 保留短中长期三个时间尺度
    return [f"{op}({field}, {d})" for d in days]

def ts_comp_factory(op, field, factor, paras):
    l1 = [5, 22, 66, 240]
    output = []
    for day, para in product(l1, paras):
        if isinstance(para, float):
            output.append(f"{op}({field}, {day}, {factor}={para:.1f})")
        else:
            output.append(f"{op}({field}, {day}, {factor}={para})")
    return output

def vector_factory(op, field):
    return [f"{op}({field}, cap)"]

def group_factory(op, field, region):
    """GLB 分组工厂:仅使用 API 验证可用的标准分组 + 公式分组
       其他字段(pv13_*, sta1/2/3_*, oth171_*, oth455_*)在 GLB 上不存在
    """
    output = []
    cap_group = "bucket(rank(cap), range='0.1, 1, 0.1')"
    sector_cap_group = "bucket(group_rank(cap,sector),range='0,1,0.1')"
    vol_group = "bucket(rank(ts_std_dev(ts_returns(close,1),20)),range='0.1,1,0.1')"

    if region == "glb":
        groups = ["market", "sector", "industry", "subindustry",
                  cap_group, sector_cap_group, vol_group]
    else:
        groups = ["market", "sector", "industry", "subindustry", cap_group]

    for group in groups:
        alpha = f"{op}({field}, densify({group}))"
        output.append(alpha)
    return output

def get_first_order(vec_fields, ops_set, region="usa", raw_fields=None):
    """顾问 get_first_order 复刻(修复 twin_field_factory 全局变量)"""
    alpha_set = []
    for field in vec_fields:
        alpha_set.append(field)
        for op in ops_set:
            if op == "ts_percentage":
                alpha_set += ts_comp_factory(op, field, "percentage", [0.5])
            elif op == "ts_decay_exp_window":
                alpha_set += ts_comp_factory(op, field, "factor", [0.5])
            elif op == "ts_moment":
                alpha_set += ts_comp_factory(op, field, "k", [2, 3, 4])
            elif op == "ts_entropy":
                alpha_set += ts_comp_factory(op, field, "buckets", [10])
            elif op in twin_field_ops:
                # twin_field_ops 需要另一字段,这里跳过(避免爆炸组合)
                # 顾问原版引用了全局 fields 变量,此处不展开
                pass
            elif op.startswith("ts_") or op == "inst_tvr":
                alpha_set += ts_factory(op, field)
            elif op.startswith("group_"):
                alpha_set += group_factory(op, field, region)
            elif op.startswith("vector"):
                alpha_set += vector_factory(op, field)
            elif op == "signed_power":
                alpha_set.append(f"{op}({field}, 2)")
            else:
                alpha_set.append(f"{op}({field})")
    return alpha_set

def get_group_second_order_factory(first_order, group_ops, region):
    second_order = []
    for fo in first_order:
        for group_op in group_ops:
            second_order += group_factory(group_op, fo, region)
    return second_order

# ==================== trade_when(顾问 trade_when_factory 适配 GLB) ====================
def trade_when_factory(op, field, region):
    output = []
    open_events = ["ts_arg_max(volume, 5) == 0", "ts_corr(close, volume, 20) < 0",
                   "ts_corr(close, volume, 5) < 0", "ts_mean(volume,10)>ts_mean(volume,60)",
                   "group_rank(ts_std_dev(returns,60), sector) > 0.7", "ts_zscore(returns,60) > 2",
                   "ts_skewness(returns,120)> 0.7", "ts_arg_min(volume, 5) > 3",
                   "ts_std_dev(returns, 5) > ts_std_dev(returns, 20)",
                   "ts_arg_max(close, 5) == 0", "ts_arg_max(close, 20) == 0",
                   "ts_corr(close, volume, 5) > 0", "ts_corr(close, volume, 5) > 0.3",
                   "ts_corr(close, volume, 5) > 0.5", "ts_corr(close, volume, 20) > 0",
                   "ts_corr(close, volume, 20) > 0.3", "ts_corr(close, volume, 20) > 0.5"]

    exit_events = ["abs(returns) > 0.1", "-1"]

    glb_events = ["rank(vec_avg(mdl109_news_sent_1m)) > 0.8",
                  "ts_rank(vec_avg(mdl109_news_sent_1m),22) > 0.8",
                  "rank(vec_avg(nws20_ssc)) > 0.8",
                  "ts_rank(vec_avg(nws20_ssc),22) > 0.8",
                  "vec_avg(nws20_ssc) > 0",
                  "rank(vec_avg(nws20_bee)) > 0.8",
                  "ts_rank(vec_avg(nws20_bee),22) > 0.8",
                  "rank(vec_avg(nws20_qmb)) > 0.8",
                  "ts_rank(vec_avg(nws20_qmb),22) > 0.8"]

    all_open = open_events + glb_events
    for oe in all_open:
        for ee in exit_events:
            output.append(f"{op}({oe}, {field}, {ee})")
    return output

# ==================== 模拟 ====================
def generate_sim_data(alpha_list, region, uni, neut):
    sim_data = []
    for alpha, decay in alpha_list:
        sim_data.append({
            'type': 'REGULAR',
            'settings': {
                'instrumentType': 'EQUITY', 'region': region, 'universe': uni,
                'delay': 1, 'decay': decay, 'neutralization': neut,
                'truncation': 0.08, 'pasteurization': 'ON',
                'unitHandling': 'VERIFY', 'nanHandling': 'ON',
                'language': 'FASTEXPR', 'visualization': False,
            },
            'regular': alpha
        })
    return sim_data

def load_task_pool(alpha_list, limit_multi=10, limit_concurrent=9):
    tasks = [alpha_list[i:i + limit_multi] for i in range(0, len(alpha_list), limit_multi)]
    pools = [tasks[i:i + limit_concurrent] for i in range(0, len(tasks), limit_concurrent)]
    return pools

def multi_simulate(alpha_pools, neut, region, universe, start):
    s = login()
    for x, pool in enumerate(alpha_pools):
        if x < start:
            continue
        progress_urls = []
        for y, task in enumerate(pool):
            sim_data_list = generate_sim_data(task, region, universe, neut)
            try:
                resp = s.post('https://api.worldquantbrain.com/simulations', json=sim_data_list)
                progress_urls.append(resp.headers['Location'])
            except Exception:
                print("  loc key error")
                sleep(600)
                s = login()
        print(f"pool {x} task {y} post done")
        for j, progress in enumerate(progress_urls):
            try:
                while True:
                    sim = s.get(progress)
                    if sim.headers.get("Retry-After", 0) == 0:
                        break
                    time.sleep(float(sim.headers["Retry-After"]))
            except Exception:
                print(f"other: {progress}")
        print(f"pool {x} task {j} simulate done")
    print("Simulate done")

# ==================== Alpha 查询 ====================
def get_alphas(start_date, end_date, sharpe_th, fitness_th, region, alpha_num, usage, year=2026):
    s = login()
    next_alphas = []
    decay_alphas = []
    count = 0
    for i in range(0, alpha_num, 100):
        print(i)
        url_e = ("https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d" % i
                 + "&status=UNSUBMITTED%1FIS_FAIL"
                 + f"&dateCreated%3E={year}-{start_date}T00:00:00-04:00"
                 + f"&dateCreated%3C{year}-{end_date}T00:00:00-04:00"
                 + f"&is.fitness%3E{fitness_th}&is.sharpe%3E{sharpe_th}"
                 + f"&settings.region={region}&order=-is.sharpe&hidden=false&type!=SUPER")
        url_c = ("https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d" % i
                 + "&status=UNSUBMITTED%1FIS_FAIL"
                 + f"&dateCreated%3E={year}-{start_date}T00:00:00-04:00"
                 + f"&dateCreated%3C{year}-{end_date}T00:00:00-04:00"
                 + f"&is.fitness%3C-{fitness_th}&is.sharpe%3C-{sharpe_th}"
                 + f"&settings.region={region}&order=is.sharpe&hidden=false&type!=SUPER")
        urls = [url_e]
        if usage != "submit":
            urls.append(url_c)
        for url in urls:
            response = s.get(url)
            try:
                alpha_list = response.json()["results"]
                for j in range(len(alpha_list)):
                    a = alpha_list[j]
                    sharpe = a["is"]["sharpe"]
                    decay = a["settings"]["decay"]
                    exp = a['regular']['code']
                    count += 1
                    if sharpe < -1.2:
                        exp = "-%s" % exp
                    rec = [a["id"], exp, sharpe, a["is"]["turnover"], a["is"]["fitness"],
                           a["is"]["margin"], a["dateCreated"], decay]
                    print(rec)
                    if a["is"]["turnover"] > 0.7:
                        rec.append(decay * 4); decay_alphas.append(rec)
                    elif a["is"]["turnover"] > 0.5:
                        rec.append(decay * 3); decay_alphas.append(rec)
                    elif a["is"]["turnover"] > 0.4:
                        rec.append(decay * 2); decay_alphas.append(rec)
                    elif a["is"]["turnover"] > 0.35:
                        rec.append(decay + 4); decay_alphas.append(rec)
                    elif a["is"]["turnover"] > 0.3:
                        rec.append(decay + 2); decay_alphas.append(rec)
                    else:
                        next_alphas.append(rec)
            except Exception:
                print(f"{i} finished re-login")
                s = login()
    print(f"count: {count}")
    return {"next": next_alphas, "decay": decay_alphas}

def locate_alpha(s, alpha_id):
    while True:
        alpha = s.get("https://api.worldquantbrain.com/alphas/" + alpha_id)
        if "retry-after" in alpha.headers:
            time.sleep(float(alpha.headers["Retry-After"]))
        else:
            break
    metrics = json.loads(alpha.content.decode('utf-8'))
    return [alpha_id, metrics['regular']['code'], metrics["is"]["sharpe"],
            metrics["is"]["turnover"], metrics["is"]["fitness"], metrics["is"]["margin"],
            metrics["dateCreated"], metrics["settings"]["decay"]]

def get_check_submission(s, alpha_id):
    while True:
        result = s.get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/check")
        if "retry-after" in result.headers:
            time.sleep(float(result.headers["Retry-After"]))
        else:
            break
    try:
        if result.json().get("is", 0) == 0:
            return "sleep"
        checks_df = pd.DataFrame(result.json()["is"]["checks"])
        pc = checks_df[checks_df.name == "PROD_CORRELATION"]["value"].values[0]
        if not any(checks_df["result"] == "FAIL"):
            return pc
        return "fail"
    except Exception:
        return "error"

def check_submission(alpha_bag, gold_bag, start):
    depot = []
    s = login()
    for idx, g in enumerate(alpha_bag):
        if idx < start:
            continue
        if idx % 5 == 0:
            print(idx)
        if idx % 200 == 0:
            s = login()
        pc = get_check_submission(s, g)
        if pc == "sleep":
            sleep(100); s = login(); alpha_bag.append(g)
        elif pc != pc:
            print("check self-correlation error")
            sleep(100); alpha_bag.append(g)
        elif pc == "fail":
            continue
        elif pc == "error":
            depot.append(g)
        else:
            print(g)
            gold_bag.append((g, pc))
    print(depot)
    return gold_bag

def view_alphas(gold_bag):
    s = login()
    sharp_list = []
    for gold, pc in gold_bag:
        triple = locate_alpha(s, gold)
        info = [triple[2], triple[3], triple[4], triple[5], triple[6], triple[1]]
        info.append(pc)
        sharp_list.append(info)
    sharp_list.sort(reverse=True, key=lambda x: x[3])
    for i in sharp_list:
        print(i)

def prune(next_alpha_recs, region, prefix, keep_num):
    output = []
    num_dict = defaultdict(int)
    for rec in next_alpha_recs:
        exp = rec[1]
        field = exp.split(prefix)[-1].split(",")[0]
        sharpe = rec[2]
        if sharpe < 0:
            field = "-%s" % field
        if num_dict[field] < keep_num:
            num_dict[field] += 1
            output.append([exp, rec[-1]])
    return {region: output}