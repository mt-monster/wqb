# -*- coding: utf-8 -*-
"""论坛来源骨架库（forum-derived skeletons）。

来源：WorldQuant BRAIN 中文论坛「Alpha 灵感」类文章（2026-10-02 调研，见
reports/forum_alpha_inspiration_taxonomy_20261002.md）。

## 为什么是「降维成骨架」而不是「塞表达式」

论坛里的模板是**自由字符串**（如 `group_rank({field}/cap, industry)`、
`-ts_zscore(ts_std_dev(a - b, 200), 1000)`）。若直接塞进 prompt，会绕过
skeleton mode 的「代码组装 → 语法强保证」这条命脉，退化成模板展开器时代
的老病（约束只在语法层）。故本模块只吸收**算子拓扑 + 经济学机制**，
字段选择仍交给 LLM 填槽，表达式仍由 render_skeleton 组装。

## 与现有 144 骨架的缺口对照（新增前已核实）

| 新增骨架 | 现有最接近 | 缺口 |
|---|---|---|
| ratio_eff.group_flow_stock | ratio_eff.flow_stock = rank(divide(x,y+eps)) | 缺 group 版；项目实证「内嵌 group_rank 是独立增益维度」 |
| spread_residual.ts_instability | spread_residual.cross_horizon = subtract(rank(x),rank(y)) | 只有**静态价差**，缺「价差的时序不稳定性」 |
| spread_residual.group_regression_residual | spread_residual.ts_regression_residual = rank(ts_regression(...)) | 缺 group 版残差 |
| trend_cons.sign_persistence | trend_cons.ma_ratio（快慢均线比） | 缺「方向持续性 vs 幅度」这一维 |

## 溯源纪律

每条骨架带 `mechanism`（参与 assign_slots 的机制级去重）与 `forum_ref`
（论坛出处，供复盘时对比「论坛来源骨架 vs 原生骨架」的过闸率）。
**论坛表达式默认未实证**，本模块只取其拓扑，不承诺收益。

算子全部取自 platform_constraints.json::known_ops（103 个已验证算子）。
"""
from __future__ import annotations

# 论坛来源骨架（origin=forum 供反馈闭环分层统计）
SKELETONS = [
    {
        "id": "ratio_eff.group_flow_stock",
        "family": "ratio_eff",
        "n_fields": 2,
        "needs_window": False,
        "sign_allowed": True,
        "template": "group_rank(divide({x}, {y} + 0.0001), subindustry)",
        "description": "单位规模效率的行业内部排序（x=流量/存量信号，y=规模分母）",
        "mechanism": "group_rank 单位规模效率：组内相对效率排序，剥离规模与行业 beta",
        "origin": "forum",
        "forum_ref": "新手营模板 group_rank({field}/cap, industry)（ZH20577）",
    },
    {
        "id": "spread_residual.ts_instability",
        "family": "spread_residual",
        "n_fields": 2,
        "needs_window": True,
        "sign_allowed": True,
        "template": "ts_zscore(ts_std_dev(subtract({x}, {y}), {W}), {W2})",
        "description": "两字段价差的时序不稳定性（不看价差水平，看价差波动）",
        "mechanism": "ts_std_dev 价差不稳定性：分歧/价差的波动率而非水平，与静态价差解耦",
        "origin": "forum",
        "forum_ref": "双字段 Sentiment 四地区实现 -ts_zscore(ts_std_dev(a-b,200),1000)（LX57490, 94票）"
                     "；「从变化的稳定性而不是变化的大小入手」（XZ77557, 30票）",
    },
    {
        "id": "spread_residual.group_regression_residual",
        "family": "spread_residual",
        "n_fields": 2,
        "needs_window": True,
        "sign_allowed": True,
        "template": "group_zscore(ts_regression({y}, {x}, {W}), subindustry)",
        "description": "剥离自变量后再做行业内标准化的残差信号",
        "mechanism": "ts_regression 组内残差：先剥离控制变量再做行业内标准化",
        "origin": "forum",
        "forum_ref": "「用残差表达新信息，比简单堆字段更容易解释」（XZ77557, 29票）",
    },
    {
        "id": "trend_cons.sign_persistence",
        "family": "trend_cons",
        "n_fields": 1,
        "needs_window": True,
        "sign_allowed": True,
        "template": "rank(ts_mean(sign(ts_delta({x}, 1)), {W}))",
        "description": "方向一致性：窗口内同向变化的占比，与变化幅度解耦",
        "mechanism": "sign+ts_mean 方向持续性：符号一致性而非幅度，与 ts_mean 水平解耦",
        "origin": "forum",
        "forum_ref": "「先构造字段的变化，再观察符号持续性、连续同号长度或滚动一致性」（XZ77557）",
    },
]
