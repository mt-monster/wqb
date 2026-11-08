# other699（TipRanks 散户交易流）波 1 模板池 — 两读取证 + 机制映射

> 状态：设计稿（2026-11-03）。数据集 other699 Retail trading activities（TipRanks），7 字段全 event 型 VECTOR，cov 0.506。
> 待 inst25/option1 两波收批腾槽后派探针（方向先验两向并测）。

## 一、论坛两读（2026-11-03）
- **YQ11169《net_buy 类字段 117% 换手的驯服记录》**：换手三类归因（数据源高频翻转→治数据 ts_mean22；构造放大噪声→改占比结构；权重集中→truncation），decay 是最后一级不是第一反应。开放问题：**VECTOR division 版（新手/老手分群）净买方向相反时互相抵消——把抵消本身做成信号**（FR19939 评论）。
- **JX84394《KOR 卖/买比一周峰值反转》43 赞金帖**（同 option1 Delta-Skew 帖作者）：**四段式模板 ratio(无量纲) → ts_zscore(·,504) 自身基线 → ts_max(·,5) 事件峰值保留 → group_rank(sector)**，S 2.43/2Y 2.05。核心消融：**比值 vs 差值差 1.10 Sharpe（量纲！）**；ts_max(5) 峰值>均值（+0.12 S/+0.45 2Y/−2.7pp TO）；decay 阶梯提交前必须跑完（decay30 全面好于60，提交后才发现，翻车）。反号 −2.66 对称 = 机理证明。
- CHN 散户调仓权重反转帖（id 截断 404 未读成）——仅留标题线索：FASTEXPR→Python Robust Universe 修复。

## 二、文献链（金帖自带 + 方向先验）
- Kaniel-Saar-Titman 2008 JF：散户净买入短期正向预测（流动性提供者拿溢价）。
- Campbell-Grossman-Wang 1993 QJE：大成交量价格变动易反转（流动性需求溢价）。
- Nagel 2012 RFS：短期反转=流动性提供报酬。Barber-Odean-Zhu 2009：散户交易推动市场。
- **合成方向先验**：散户净买流正向（KST）与异常卖压反转（CGW）同源——都是流动性提供视角。

## 三、字段机制映射（7 字段，event 型 VECTOR，先聚合后算！）
- 核心信号：oth699_sharestraded（本笔股数，**正买负卖**）→ vec_sum=净买流、vec_count=活跃笔数。
- 结构腿：oth699_newnumofshares / prevnumofshares（持仓前后）→ 聚合后 subtract 得净持仓变化流（同机制净额合成 ✓）。
- 经验腿：oth699_priortransactionnumber / priordistincttradingdays（用户经验）→ **辅助信号**，只做条件/分组（新手 vs 老手分歧）。
- 元数据禁信号：oth699_executiontimestamp（时间戳）、oth699_aggsplitfactor（拆股因子）。

## 四、算子硬闸备忘
- **event 型 VECTOR 禁元素级 power/multiply**（option1 实测）——abs/sign 元素级同样高危，设计一律先 vec_sum/vec_avg/vec_count 聚合再进算子。
- **ts_max 不在册**：峰值保留恒等式 max(x,5) = subtract(x, ts_max_diff(x,5))；ts_zscore 若不在册用 divide(subtract(x, ts_mean(x,504)), ts_std_dev(x,504)) 自建。
- sharestraded 正负分解**不做元素级**：净额 vec_sum(x) 直接可用；强度用聚合后 abs/拆解在标量 TS 层做。

## 五、模板清单草案（12 互异 · 家族 6）
- T1 净买流水平（ts_mean22 后 group_rank，KST 正向）｜T2 净买流自身异常（zscore504 自建，KOR 段2）｜T3 事件峰值保留（ts_max_diff 恒等式，KOR 段3·照抄臂唯一）。
- T4 活跃笔数突变（ts_delta(ts_mean(vec_count,22),22)，突变面）｜T5 平均每笔净买强度（divide(vec_sum, vec_count) 无量纲比值结构）。
- T6 净持仓变化流（聚合后 subtract(new,prev)，同机制净额 ✓）。
- T7 trade_when(经验高, 净买流正向, -1) 老手条件化｜T8 trade_when(经验低, 净买流, -1) 新手条件化（FR19939 分歧信号拆两臂）。
- T9 净买流反向对照（散户情绪反向假说对测）｜T10 卖压异常反转（zscore 峰值取反，CGW 回补）。
- T11 参与者经验水平（vec_avg(priortransactionnumber) ts_mean22，慢变量画像）｜T12 country 分组轴（si3 心得①迁移对照）。
- 窗口 22/504 白名单（504=2 交易年自身基线，KOR 实测 252/504/1008=2.21/2.43/2.37 有据）。

## 六、覆盖闸
- cov 0.506 不作判据；探针收批后逐颗 get_alpha_yearly_stats 按「连续多年双零」口径验。

## 七·五、探针归因（oth699p_20261103 6/6 收满，2026-11-03 10:2x）
| 臂 | 机制 | S | 判 |
|---|---|---:|---|
| P1 净买流正向 w22 | KST 流动性提供 | 0.24 | 方向正（P2 反向 −0.24 严格对称=机理），弱 |
| P3 活跃笔数 w22 | 参与广度 | **0.47** | 全批最佳，正向 |
| P5 经验腿 w22 | 用户经验水平 | 0.36 | 微弱正 |
| P4 比值（净买/笔数） | 无量纲化 | 0.18 | **弱——KOR「卖/买比」在此不可复制**（sharestraded 正买负卖混合，无买卖分侧，event 禁元素级 sign 分解）|
| P6 净持仓变化流 | 同机制净额 | 0.24 | 弱 |

**方向定案**：散户活跃度/参与广度正向 > 净买流正向（KST 成立但弱）> 经验。水平面天花板 0.47 低——**波 1 主攻 = KOR 金帖段2/段3（ts_zscore 自身基线 504 + ts_max 峰值保留）迁移到活跃度最强腿**，探针未测结构面。

## 七、待补
- 探针批（方向两向）+ 派发实录 + 收批归因。
## 九、波 1 收批归因（12/12 全收 · 2026-11-04）

| 臂 | 面 | S | 读数结论 |
|---|---|---|---|
| T1 | 活跃度慢窗(66) | 0.34 | 基线弱 |
| **T2** | **活跃度 zscore 自身基线(22/504)** | **0.84** | **全场最佳——KOR 段2 迁移生效** |
| T3 | T2+峰值 ts_max(5) | 0.68 | 峰值保留对水平面反噬（事件型边界再证） |
| T4 | 净买流 zscore(vec_sum) | -0.08 | 流向面死 |
| T5 | 净买流+峰值 | 0.59 | 同 T3 教训 |
| T6 | 持仓变化(ts_delta) | 0.17 | 死 |
| T7 | 经验条件化(trade_when 高经验) | 0.38 | 无增益 |
| T8 | 净买流>0 条件化 | 0.41 | 无增益 |
| T9 | (派发序 9) | 0.20 | 弱 |
| T10 | (派发序 10) | 0.48 | 弱 |
| T11 | 活跃度 country 轴 | 0.72 | 好于 T1/T2 之外但低于 T2(subindustry)——country 杠杆×机制面专属性又一例 |
| T12 | 经验<分位 trade_when | 0.0 | 条件死臂（TO=0，条件未触发） |

**判弱封组合**：max S 0.84 << DEU 门槛 1.58，缺口近一倍，无追投价值。
**机制归因**：活跃度/参与广度面（T2 0.84 / T11 0.72 / T3 0.68）> 流向面（|S|≤0.59）> 动态突变面全灭——与 inst25 同构。
**族归因**：oth699 并入「注意力/情绪/做空行为族 DEU 系统性弱」证据链（第 7 集：snt7/sn12/snt27/sm12/si3/inst25/oth699），封盘不再追投。
