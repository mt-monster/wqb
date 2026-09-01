# -*- coding: utf-8 -*-
"""统计 KOR 战役表达式中算子探索率"""
import json, re, glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

exprs = []
for f in glob.glob(r'D:\coding\traeCN_project\wqb\tracking\KOR\candidates\kor_wave*.json'):
    try:
        data = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        print('skip', f, e); continue
    if isinstance(data, list):
        exprs.extend(x for x in data if isinstance(x, str))
    elif isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                exprs.extend(x for x in v if isinstance(x, str))

ops = set()
for e in exprs:
    ops.update(re.findall(r'\b([a-z_]+)\s*\(', e))

all_ops = {'add','multiply','sign','subtract','pasteurize','log','max','abs','divide','min',
'signed_power','inverse','sqrt','reverse','power','densify','or','and','not','is_nan','if_else',
'ts_corr','ts_zscore','ts_returns','ts_product','ts_std_dev','ts_backfill','days_from_last_change',
'last_diff_value','ts_scale','ts_step','ts_sum','ts_av_diff','ts_kurtosis','ts_mean','ts_arg_max',
'ts_rank','ts_ir','ts_delay','ts_quantile','ts_count_nans','ts_covariance','ts_decay_linear',
'ts_arg_min','ts_regression','ts_max_diff','kth_element','hump','ts_delta','ts_target_tvr_decay',
'ts_target_tvr_hump','winsorize','rank','zscore','scale','normalize','quantile','vec_min',
'vec_count','vec_sum','vec_max','vec_avg','vec_stddev','vec_range','bucket','tail','trade_when',
'group_mean','group_rank','group_backfill','group_scale','group_count','group_zscore',
'group_std_dev','group_sum','group_neutralize','group_cartesian_product'}

used = ops & all_ops
print('total_exprs', len(exprs))
print('used_ops', len(used), sorted(used))
print('exploration_rate %.1f%%' % (100*len(used)/len(all_ops)))
unused = sorted(all_ops - used)
print('unused_ops', len(unused), unused)
