# -*- coding: utf-8 -*-
"""结构性解耦骨架（prod 墙破墙专用）。

从 skeletons.py 拆分而来，只包含骨架数据定义，无逻辑代码。
"""

# 2026-09-12 退役：interact.weighted_mix 骨架（w*rank(x)+(1-w)*rank(y)）与
# 「禁止混信号加权调参」纪律冲突（权重网格 = 被点名的过拟合模式），且产物被
# gate 闸5 weighted_signal_mix 正则100%拦截，属纯浪费产出。原 INTERACT_WEIGHTS
# 常量随骨架一并删除。合规替代表达：ts_corr / subtract / ratio 等单一信号结构。

# ---- 2026-09-17 结构性解耦骨架（prod 墙破墙专用）----
# 针对「单点拥挤」prod 分布（max>0.7 但仅 1-2 个 alpha 撞车）设计：
# 保留信号核心收益，改变其「形状」使其与撞车 alpha 不再相似。
# 四族：nonlinear（非线性/条件）、time_agg（时间聚合变体）、
#       group_decouple（分组/中性化）、spread_residual（价差/残差）。


SKELETONS = [
    # ---- nonlinear 族：非线性/条件结构 ----
    {
        "id": "nonlinear.ts_quantile_gaussian",
        "family": "nonlinear",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_quantile({x}, {W}, driver=\"gaussian\"))",
        "description": "{W} 日分位正态化后 rank（强制正态分布，改变截面特性，与线性 rank 解耦）",
        "mechanism": "ts_quantile 将信号转为正态分布分位数，改变收益分布形状，与简单 rank 产生本质差异",
    },
    {
        "id": "nonlinear.conditional_sign",
        "family": "nonlinear",
        "n_fields": 2,
        "needs_window": False,
        "sign_allowed": True,
        "template": "if_else(greater({x}, 0), rank({x}), rank({y}))",
        "description": "条件符号门控（{x} 正时 rank({x})，否则 rank({y})，正负不对称策略）",
        "mechanism": "信号正负时采取不同策略，与线性 rank 的单向暴露解耦",
    },
    {
        "id": "nonlinear.hump_smooth",
        "family": "nonlinear",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "hump(rank({x}), hump=0.01)",
        "description": "变动幅度压制 rank（截断极端值，改变收益来源分布）",
        "mechanism": "hump 截断极端 rank 值，抑制尾部收益，与未截断的线性 rank 解耦",
    },
    {
        "id": "nonlinear.tail_trim",
        "family": "nonlinear",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "tail(rank({x}), lower=0.1, upper=0.9, newval=0.5)",
        "description": "中段压平只留两端极端信念（10/90 分位外保留，改变收益分布形状）",
        "mechanism": "tail 将中段 rank 压平为 0.5，只保留极端值，与全分布 rank 解耦",
    },
    # ---- time_agg 族：时间聚合算子变体 ----
    {
        "id": "time_agg.av_diff",
        "family": "time_agg",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_av_diff({x}, {W}))",
        "description": "{W} 日均值绝对偏离 rank（捕捉短期偏离，与 ts_mean 平滑解耦）",
        "mechanism": "ts_av_diff 计算信号与其均值的差，放大短期波动，与 ts_mean 的长期平滑解耦",
    },
    {
        "id": "time_agg.ts_ir",
        "family": "time_agg",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_ir({x}, {W}))",
        "description": "{W} 日时序信息比 rank（均值/波动，信号质量而非信号水平）",
        "mechanism": "ts_ir 捕捉信号的稳定性和趋势强度，与 ts_mean 的绝对水平解耦",
    },
    {
        "id": "time_agg.arg_max_timing",
        "family": "time_agg",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_arg_max({x}, {W}))",
        "description": "{W} 日内峰值位置 rank（峰值越近尾部=趋势仍在强化，引入时序信息）",
        "mechanism": "ts_arg_max 捕捉极值出现的时间点，与 ts_mean 的幅度信息解耦",
    },
    {
        "id": "time_agg.arg_min_timing",
        "family": "time_agg",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_arg_min({x}, {W}))",
        "description": "{W} 日内谷值位置 rank（谷值越近尾部=趋势仍在弱化，引入时序信息）",
        "mechanism": "ts_arg_min 捕捉极值出现的时间点，与 ts_mean 的幅度信息解耦",
    },
    # ---- group_decouple 族：分组/中性化维度 ----
    {
        "id": "group_decouple.neutralize_industry",
        "family": "group_decouple",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "group_neutralize({x}, subindustry)",
        "description": "行业中性化（剔除行业均值，保留截面相对强弱，与全市场 rank 解耦）",
        "mechanism": "group_neutralize 将收益来源从全市场 beta 转为行业 alpha，与未中性化的 rank 解耦",
    },
    {
        "id": "group_decouple.rank_subindustry",
        "family": "group_decouple",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "group_rank({x}, subindustry)",
        "description": "子行业内部 rank（组内相对位置，与全市场 rank 解耦）",
        "mechanism": "group_rank 在子行业内部排序，与全市场排序的 rank 解耦",
    },
    {
        "id": "group_decouple.zscore_sector",
        "family": "group_decouple",
        "n_fields": 1,
        "needs_window": False,
        "sign_allowed": True,
        "template": "group_zscore({x}, sector)",
        "description": "行业内 z-score（剔除行业 beta，保留组内相对位置，与全市场 zscore 解耦）",
        "mechanism": "group_zscore 计算信号在行业内的标准分数，与全市场 zscore 解耦",
    },
    # ---- spread_residual 族：价差/残差信号 ----
    {
        "id": "spread_residual.cross_horizon",
        "family": "spread_residual",
        "n_fields": 2,
        "needs_window": False,
        "sign_allowed": True,
        "template": "subtract(rank({x}), rank({y}))",
        "description": "跨期价差（长期预期 - 短期预期，捕捉期限结构差异）",
        "mechanism": "subtract 构建两个相关字段的价差，与单一字段水平信号解耦",
    },
    {
        "id": "spread_residual.cross_source",
        "family": "spread_residual",
        "n_fields": 2,
        "needs_window": False,
        "sign_allowed": True,
        "template": "subtract(rank({x}), rank({y}))",
        "description": "跨源价差（不同信息源预期差，捕捉信息不一致）",
        "mechanism": "subtract 构建不同信息源的价差，与单一信息源信号解耦",
    },
    {
        "id": "spread_residual.ts_regression_residual",
        "family": "spread_residual",
        "n_fields": 2,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_regression({y}, {x}, {W}))",
        "description": "{y} 对 {x} 的 {W} 日回归残差 rank（剔除 {x} 影响后的纯 alpha）",
        "mechanism": "ts_regression 取残差，剔除自变量影响，与原始信号解耦",
    },
]

