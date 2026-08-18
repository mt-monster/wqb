# USA 战役第 20 次多样性评估（波8-11, 批次 PP→AO, ~44 轮 × 8 并发 ≈ 352 条回测）

日期: 2026-08-16 | 范围: USA/TOP3000 D1 | 累计: 波1-11 共 568 条回测, PASS=0

## 1. 探索率盘点（波8-11 增量）

| 维度 | 波8-11 新增 | 池规模 | 累计探索率 | 结论 |
|---|---|---|---|---|
| 数据集 | +5 (opt40/analyst44/inst6/obim/si3 成分/analyst44 成分) | 237 候选 | 11/237 = 4.6% | 波11 双数据集混合是探索维度突破, 但单数据集仍缺技术面/宏观/事件驱动 |
| 字段 | ~100 (opt40 ~30 / analyst44 8 / inst6 ~20 / obim ~35 / si3 5) | 628 白名单 | ~16% | 高度集中: dark/lit/impact/spread/loan_util/EPS/inst6 占比 7 族占 80%+; obim 198 字段仅探 ~35 |
| 操作符 | +multiply/ts_av_diff/vec_avg/vec_sum/days_from_last_change | 102 白名单 | ~19% | 波11 乘法族定式落地; winsorize/ts_entropy/ts_backfill/sigmoid/ts_corr/ts_regression/ts_arg_max 仍未试 |
| 骨架 | +乘法复合/组标准化(industry)/变化率×差值 | — | 8 类 | 波11 新定式: rank(ts_av_diff(慢变))×rank(subtract(差值)) 乘法, 混合族专用 |
| 风格 | +借贷×微结构混合 (新增风格) | — | 7 类 | 仍缺: 动量/技术面/宏观/盈余漂移/事件驱动 |

## 2. 收益来源归因（波8-11 实证）

| 路线 | 天花板 | 撞墙类型 | 归因 |
|---|---|---|---|
| opt40 IV 族 | sharpe 1.06 | **PROD 墙** 0.83-0.91 | 与全平台波动率因子高度重叠, 大众低波异象挖尽 |
| analyst44 consensus | 0.45 | **信息含量墙** | 21d 修正稀疏多数为 0; EPS/EBITDA/nxt 三连冗余 |
| inst6 13F | 1.03 | **信息含量墙** (d2 margin 7.2bp 达标注但 sharpe 不足) | 13F 低频持股信息, 骨架穷尽后天花板由信息含量决定 |
| obim 微结构单数据集 | 0.71 | **信号弱墙** | 亮点: dark/lit 0.51 + impact−spread 0.60; 单信号均不足 |
| si3×obim 混合 (波11) | **1.13/2y 1.08** | **margin 结构性墙** 0.0-0.6bp | 做空需求×冲击净效应乘法, sharpe/fit/2y 同步改善但多头空头日收益差被稀释至 ~0; decay2/4 全档验证 |

**核心结论**: 每条路线都撞不同类型的墙——红海族撞 PROD 墙、低频弱信号族撞信息含量墙、混合族撞 margin 墙。**波11 最重要的发现是 margin 墙与数据集特性绑定**（inst6 decay2 解锁 7.2bp vs si3×obim 全档 0.6bp），选数据集时必须预检 margin 维度。

## 3. 风格多样性评估

- 现有 7 风格: 期权 IV / 情绪反转 / 借贷水平 / 分析师共识 / 机构持股 / 微结构订单流 / 借贷×微结构混合
- **已判死风格族**: 情绪(3 数据集) / 期权(2 数据集) / 借贷(si3 水平) / 分析师共识 / 机构持股 / si3×obim 混合骨架族
- **缺口**: 动量/技术面(macro38)、宏观、盈余漂移(earnings4)、事件驱动(news52)
- 目标要求 3 个不同数据集完全不同风格相关性<0.4 → 当前 0 达标, 风格缺口是主要瓶颈

## 4. 预处理分布

- quantile 外层 100% / rank 归一 ~68% / group_zscore ~87% / ts_decay_linear ~18% / vec_* VECTOR 聚合 ~77%
- **未用工具箱** (Round10 遗留): winsorize+ts_backfill+group_rank 稳健三件套、ts_entropy 差异化、days_from_last_change(仅 1 次)
- 波11 验证: signed_power 单调变换被 quantile 抵消 (TUNE 批 5 档指数同指标); group_zscore(industry) 组标准化是唯一有效预处理改进 (+0.03)

## 5. 失效风险清单（波8-11 新增）

1. **margin 结构性天花板**: 低频信号族(借贷/13F/混合) margin 0.0-0.6bp 与 decay 无关; 只有数据集特性(inst6 13F 披露节奏)能解锁 → **选数据集前必须查该族 margin 表现**
2. **混合族 2y 转正但 PROD 未知**: si3×obim 乘法族 2y 1.05-1.08 大幅转正, 但未提交无 PROD 数据; 若 sharpe 达标需先测 PROD
3. **RN-IS 脱节**: obim executed 占比 RN 1.03 vs IS 0.15; fill_prob RN 1.17 vs IS 负 → RN 高不等于 IS 强
4. **2y 检查改名**: IS_LADDER_SHARPE 槽位替代 LOW_2Y_SHARPE, _wait_sims.py 已兼容 (调查闭环)

## 6. Skills 优化动作（本轮落地/建议）

1. ✅ **双数据集混合流程已融合** (用户 2026-08-16 授权): expr_lint.py 门控(>2 拦截/==2 标 MIX) + 批命名规范 + 台账 mix_strategy 节
2. ✅ **2y 检查双名称兼容**: _wait_sims.py IS_LADDER_SHARPE/LOW_2Y_SHARPE 双解析
3. ✅ **乘法定式沉淀**: 混合族用 rank(ts_av_diff(慢变 10-20d))×rank(subtract(差值)) 乘法, 加法已被证伪
4. ✅ **判死粒度升级**: 骨架族级判死(混合族) vs 数据集级判死, 混合流程保留可复用
5. 建议落地: **margin 预检规则**——新数据集首发探针批必须混入 2-3 条 margin 敏感骨架(水平信号 vs 变化信号对照), 一轮即可定 margin 维度
6. 建议落地: ts_entropy/winsorize/ts_backfill 在下一数据集补测

## 7. 下 10 轮方向（波12+）

- **主攻 macro38** (Technical Ratings Model): os_is_sharpe 0.5392(候选最高) / 1371 用户蓝海 / 宏观金字塔未点亮(need 3) / 技术面风格与全部已判死族独立; Round10 备选延续
- **备选**: earnings4 (盈余公告效应=PEAD 经典异象, 事件风格) / news52 (Conference call, 344 用户极蓝海)
- **禁用**: 已判死 8 数据集全系 + 情绪类任何数据集 + si3×obim 混合骨架族
- **混合复用**: macro38 技术面 × 基本面成分 (若单数据集摸到 1.2+ 且 margin 达标可考虑, 需先验证 macro38 margin 维度)
