# EUR ATOM 战役交付清单（2026-11-08 终版）

> SOP：/wq-brain-ra-eur · EUR/TOPCS1600/D1 · 全程未换 region
> 存档索引：字段画像 18 份 `tracking/EUR/reference/datasets/*.md`；战役日志 `tracking/EUR/reports/campaign_atom_2026-11.md`（23 节）

## A. 全闸通过 4 颗（Mode B + self + prod 三闸全过，互相关 <0.9，同批提交合法）

### 1. `leA5JeP7` — insider_agg_matrix · INSIDERS ×1.1
```
rank(group_scale(tail(winsorize(group_zscore(ts_sum(top_significant_value_2, 88), industry), std=2), lower=0.25, upper=0.75, newval=0.5), industry))
```
设置：SLOW_AND_FAST / decay 4 / trunc 0.08
指标：S 1.76｜F 0.94｜2Y 2.32｜sub 1.07｜robust 1.07｜TO 0.070｜self 0.33｜prod 0.6498
逻辑：高管前二大协同显著交易金额，88d（季度披露期+申报滞后）累积，行业内 zscore 相对位
机制：CMP(2012) conviction——高管用自有资金的大额买入是低估信号；字段梯度 _1/_2 正、_3/_4 反（字段级证据）

### 2. `mLo7pMwx` — news18 (RavenPack) · NEWS ×1.3
```
rank(group_scale(ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws18_multiple_comp_sse), vec_avg(nws18_multiple_comp_relevance)), 66), 504), densify(market)), target_tvr=0.05), sector))
```
设置：SLOW_AND_FAST / decay 15 / TOP2500
指标：S 1.69｜F 0.77｜2Y 1.81｜sub 0.90｜robust 0.92｜TO 0.064｜self 0.09｜prod 0.6366
逻辑：多实体新闻事件密度（vec_count）× 相关性加权，自身 504 日分位的异常高 → 反转（Da et al. 2011 注意力反转）；66d 密度窗为 EUR 峰
来源：论坛帖 43541109631895 模板迁移 + 本战役三杠杆改良（分位窗 504 破 prod 墙 / S&F 修 2Y / sector 栈）

### 3. `akKzvXww` — news18 · NEWS ×1.3
```
rank(group_scale(ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws18_sse), vec_avg(nws18_multiple_comp_relevance)), 66), 252), densify(market)), target_tvr=0.055), sector))
```
指标：S 1.68｜F 0.77｜2Y 1.31｜self 0.07｜prod 0.6183
与席位 2 差异：单实体事件流（sse）vs 多实体故事流（multiple_comp_sse），互相关 0.81——不同信息源

### 4. `0mYgWNOq` — news18 · NEWS ×1.3
```
rank(group_scale(ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws18_multiple_comp_bee), vec_avg(nws18_multiple_comp_relevance)), 66), 252), densify(market)), target_tvr=0.055), sector))
```
指标：S 1.63｜F 0.72｜2Y 1.22｜self 0.08｜prod 0.6475
与席位 2/3 差异：财报事件子类计数（bee）vs 全新闻流，互相关 0.70-0.74——事件类型正交
注：bee/bam/acb/qmb/ghc_lna 等子类字段 vec_count 逐位相同（同一事件集），bee 为代表

## B. 半全绿 2 颗（结构优秀，卡结构性约束，条件解锁后立即可用）

| alpha | 数据集 | S/F/2Y | 卡点 | 解锁条件 |
|---|---|---|---|---|
| `WjOzwnlO` | insider_feats (OTHER ×1.5) | 1.80/0.96/2.17 | prod 0.84（机制墙：insider 买卖比类 OS alpha 占位） | prod 池钉子衰减后重测 |
| `wpQGoApQ` | model238 (MODEL ×1.3) | 2.16/1.61/2.35 | sub 0.59/robust 0.59（信号在 TOPCS1600 中尾部，sub/robust 宇宙不含） | 无（结构性） |

## C. 数据集终局地图（22 集实测 + 5 跳过）

**出活**：insider_agg_matrix（席位 1，16 节全穷尽）｜news18（席位 2/3/4，三正交源）｜model238（半全绿）
**结构优秀但卡**：insider_feats（prod 墙）、insider_trx_matrix（prod 墙）、insiders1（S 1.14 差 0.11）
**归档**：institutions6/fund_holdings_panel（弱+枯竭）、news_sentiment_dl/nlp/36/54、news20、behavioral_signals、search_interest、stock_search_trends、other545、model68、price_signal_dl（平台 FAIL）、acquisition_model、other571、event_relation（平台故障）、卖方全族（2Y 枯竭）
**跳过**：insiders12（cov 0.19）、news54（无数值字段）、model307（销售分布无横截面信息）、sentiment/socialmedia/earnings/macro（拥挤或 vS≤2）

## D. 战役级可复用结论

1. `group_zscore` > `group_rank`（+0.10-0.13 S，信息保真），但必须外套 `rank(group_scale)` 整形
2. `vec_count` 只吃 RavenPack 式多事件字段；日更面板/标题 NLP 字段退化为 0/1
3. MATRIX 预聚合吃宽宇宙（TOP2500 +0.16S）；稀疏 VECTOR 事件被宽宇宙稀释
4. 稀疏流量唯一累加器 = `ts_sum`（ts_decay_linear 会把 0 值加权 → TO 爆炸）
5. 存量态字段直读（免 ts_sum）> 二次平滑（insider_feats 1.76 vs 1.43）
6. 中性化是（数据集×机制）级事实：S&F 救 insider/news 密度、杀 insiders1 比例与 model238 慢轴
7. F 闭式：`F=S×sqrt(returns/0.125)`（TO<0.125 时）——低 returns 族 F=1.0 需 S≈1.9+
8. sub 比率闸（0.52×S）下「先修结构、后加强度」
9. `group_backfill(x, group, d, std)` 第 3 参数 d 必填；解 CW（NaN 集中持仓）但只解 CW 不解 sub/robust
10. 窗口粒度由数据粒度决定：厂商预聚合 88d、逐笔明细 44d、日度事件 66d
11. prod 机制墙：同机制不同读数（股数/USD/比例）撞同一颗 prod 钉子（0.74-0.84），中性化/分组不可绕

## E. 提交建议

4 颗全闸（A 节）同批提交合法且互相关已验证。提交后 prod/self 池变化，B 节 2 颗与 vR1poWNz（S 1.14 差 0.11）建议 2 周后重测。**提交动作待用户显式确认。**
