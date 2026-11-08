# 晚批数据集判死与 starmine 突破（2026-11-07，P30/P31/P34 及 P21/P28）

## 判死（数据集级，附证据）

| 数据集 | 塔 | 最强件 | S | 2Y | TO | 判定 |
|---|---|---|---:|---:|---:|---|
| **ai_factor_transfer** | model | 88RYzrrv BB位置×RSI 双腿 | **1.08** | 1.09 | 0.462 | ⛔ 技术指标族 KOR 无效 |
| **pv103** | pv | QPvgVMJp 收盘/VWAP×异常量 双腿 | **1.03** | 0.58 | 0.607 | ⛔ 盘中结构无效且换手过高 |
| **model170** | model | mLo1X8JK 估值差×盈利动量 双腿 | **1.27** | 0.53 | 0.093 | ⛔ 估值差机制弱、2Y 缺失 |
| **price_signal_dl** | model | —（10/10 仿真 FAIL） | — | — | — | ⛔ **有字段目录无实际数据** |

### ai_factor_transfer 的方向发现（重要）
10 条模板里 6 条水平反转全为负：
`-group_rank(typical_price_bollinger_band_position)` **−0.91**、`-group_rank(cumulative_money_flow_volume_adjusted)` **−0.93**、
`-group_rank(momentum_williams_r_adjusted)` **−0.48**、`-group_rank(liquidity_weighted_returns_ma_2)` +0.30。
⇒ 取负即正 ⇒ **KOR 上 RSI/CMF/威廉指标是弱正向动量**，不是超买超卖反转。
与 P19（5 日收益取负 = −1.29 ⇒ 正向动量）**同向印证**：
**KOR/D1/TOP600 的技术面整体是动量市，反转几何系统性失效。**
这解释了三颗交付件为何都不是技术反转 —— 它们走的是持仓分歧 / 预测修正 / 内部人波动。

### price_signal_dl 的诊断路径（可复用）
1. `preflight_expressions` → valid=true、unknown_fields=[]
2. `validate_expressions` → valid=true、platform_field_count=2
3. 单条 `create_multi_simulation` 探针 → 子仿真 status=**FAIL**（progress 0.35 → ERROR）
4. `harvest_multisim_alphas` → 全部 "No alpha_id in sim response"
⇒ **判据：字段名校验全绿但子仿真 FAIL = 目录里有、KOR 实际无数据**（与 macro63 同型）。
**教训**：preflight/validate 只验字段名存在性，不验区域数据可用性；新数据集首波必须 ≤2 条探针先验数据可用性，再铺 10 模板。

## ⭐ predictive_starmine —— 第二个「2Y 引擎」

**数据集画像**：cov 0.9434，**645 MATRIX 字段**，字段级 aC **0–4（几乎零拥挤）**，cov=1.0 的字段 313 个。
字段族：`analyst_{up,down}grade_count_{7,14,30,60,90}d`、
`analyst_{upward,downward}_revision_count_{fq1,fq2,fy1,fy2}_{earnings,ebitda,revenue}_{7,14,30}d`、
`mean_estimate_change_pct_{f12m,fy1}_{earnings,ebitda,revenue}`、`recommendation_mean_change`、`arm_score_change`。
**27 组 up/down 匹配对全部 cov≥0.99**（已脚本配对，见 `cache/_star_pairs.py`）。

### P34 首波读数（SUBINDUSTRY / decay4 / trunc0.08）
| 件 | 模板 | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| **A1VmPWbd** | fy1 盈利**向上修正数 − 向下修正数** (14d) | **1.25** | 0.82 | **1.72** | 1.25 | 0.186 |
| Xg9enrPb | arm_score_change_1d | 1.32 | 0.54 | 1.31 | 1.26 | 0.539 |
| N1N3rwW7 | mean_estimate_change_pct_fy1_earnings | 1.18 | 0.70 | 1.15 | 0.97 | 0.199 |
| A1VmPWJX | mean_estimate_change_pct_f12m_earnings | 1.17 | 0.70 | 1.08 | 1.06 | 0.198 |
| zq30mMQE | 升级数差 × 预期变化率 双腿 | 1.17 | 0.63 | 0.90 | 0.92 | 0.219 |
| gJedMA7J | upgrade − downgrade (14d) | 0.92 | 0.74 | 1.15 | 0.81 | 0.127 |

**结论**：starmine 的**修正广度差**（upward − downward revision count）是 KOR 第二个能顶到 2Y 1.72 的引擎，
S 1.25 差 0.33。机制：Chan–Jegadeesh–Lakonishok (1996) 分析师修正动量 + Womack (1996) 修正漂移。
**P35 已派**（10 模板）：66/132 日长窗偏离 × 4 个口径（fy1/fq1/fq2 earnings、fy1 ebitda）× 三口径复合广度 × 幅度×广度双腿 × 归一化广度比 × 22 日平滑。

## 波次吞吐修正（已生效）
`--batch-size 10` ⇒ 一个 multisim 覆盖整波，单波 6–12 分钟（原 batch-size 2 需 5 个串行批次、必超时）。
已连发 6 波（P21/P27/P28/P30/P31/P32/P34/P35）无 CONCURRENT_SIMULATION_LIMIT 报错 ⇒ 2 个并发 multisim×10 条 = 平台可承受。
