# KOR Short Interest 专项调研与挖掘方案

> 2026-09-28 · 双源调研（项目 skill `brain-forum-browse` recon 模式 + MCP 论坛检索 + 外部学术检索）

## 一、论坛调研（MCP 实时检索，4 篇高价值帖）

### 帖1《基于MCP提交的3个Short Interest因子》（LR93609，87赞/20评）
- **EUR shortinterest 仅 2 字段**：`shrt3_bar`（借券需求 1-10 评级）、`shrt3_utilizationpercent_units`（**利用率 = 借出股数/可借股数**）
- 跑出 3 个可提交因子：①**拥挤度择时**（模板原封）②**截面回归**（略调）③**幅度限制**（信号加强）
- **可复用经验（评论区）**：①`NAN HANDLING 开 ON`（"类似于 ts_backfill"，与不开差别很大）②评论者 JB53978 说"为 Short Interest 塔点亮花了两天设计模板"→ 该塔公认难点 ③作者经验："重点是对字段和模板的理解，不是工具"

### 帖2《峰值年龄波动率：卖空借贷压力的"不稳定信号"因子》（MY65447）
- **核心创新**：**不关心卖空多不多，而关心卖空者稳不稳**（决策一致性/不稳定性）
- 完整表达式：`group_normalize(ts_std_dev(-ts_arg_max(vec_avg(borrow_activity_score), 20), 20), densify(sector))`
- Setting：decay 10 / STATISTICAL / truncation 0.005
- **踩坑**：不做行业中性化 Sharpe 仅 0.89；加 group_normalize 后大幅提升（金融/科技板块借贷基线系统性偏移）
- 可抽象模板：输入信号 X + 回溯窗 T（短线 5-10 / 长线 40-60）+ vec_* 聚合 + group 轴

### 帖3《WorldQuant BRAIN Alpha研究实战》（XC83126，35赞）
- **单字段无信号 → 比值有信号**：`short_interest.sale_volume / short_interest.x` 比值结构显著提升（印证我方"比值/价差结构"方向）

### 帖4《KOR 投资者「卖/买比」一周峰值反转因子》（JX84394，20赞）★ 我方已提交 omLjG1M5 的作者原帖
- **韩国卖空受限市场特性**：样本内两次卖空禁令（2020-03-16 起约 14 个月、2023-11-06 起）→ 悲观者只能**现货抛售**（Miller 1977）→ 现货卖压比其它市场更"拥挤"→ **过度反应更大、反转更强**
- 这解释了为何 shrt38 净买入族 S 高达 2.2+（但我们已撞 prod 墙）

## 二、外部学术（韩国市场 short selling 专项，2 篇）

### 论文1：Net Arbitrage Trading（NAT）in Korean market
（Jeong/Eo/Kang, Pacific-Basin Finance Journal 2026, DOI 10.1016/j.pacfin.2026.103139）
- **NAT = 外国投资者异常持股（AHF）− 异常卖空利益（ASI）**，即**同时结合 long 侧与 short 侧的净额**
- **韩国市场关键结论**：**外国投资者是主要套利者**（有显著预测力）；**本土机构投资者的交易无预测力**
- NAT 显著正向预测横截面收益；危机期套利者撤资 → 错误定价加剧
- → **可落地机制**：用 `institutions6`（外国/机构持股）− `shrt38`（卖空利益）构造**跨数据集价差**（但注意我方禁止 add 两腿；单信号价差 `subtract(rank(A),rank(B))` 合规）

### 论文2：Return predictability of short-selling and financial distress（Korean market）
（Pacific-Basin Finance Journal, S0927538X2300269X）
- **与美国相反**：韩国卖空活动集中在**投资级（investment-grade）**公司
- 卖空活动对**投资级**股票有预测力，**投机级无**
- **按投资者类型**：机构/外国人的卖空有预测力；**散户卖空无预测力**（且高散户卖空 → 高未来收益，正向）
- Amihud 非流动性 / VIX 高低期无显著差异

## 三、机制 Map（→ KOR shortinterest38 字段映射）

| 论文/帖子机制 | KOR 字段 | 状态 |
|---|---|---|
| 利用率/拥挤度（帖1） | `shrt38_amt_wgt`、`shrt38_tot_amt_wgt`、`shrt38_tot_qty_wgt`（**短卖换手/量权重**） | **本轮 probe** |
| 峰值新近度+不稳定性（帖2） | `ts_arg_max`/`ts_std_dev` on `vec_avg(amt_wgt)` | **本轮 probe** |
| 投资者类别分解（论文2） | `shrt38_agg_invactdc_vni`（Institutions/Securities/Insurance/Pension 等投资者代码） | 待挖（需 vec 按类别筛） |
| 频率/窗口维度 | `shrt38_pyt_qrf`（日/周/月）、`shrt38_stk_agg_invactcalc_prd_typ`（5d/20d/月/年） | 待挖 |
| 净买入反转（帖4） | `shrt38_accum_net_buy_amt` 等 | ❌ prod 0.88 撞墙（已封存） |
| NAT 跨数据集价差（论文1） | `institutions6` × `shrt38` | 候选（单信号价差结构） |
| 数据集内生行业中性化（帖2必需） | `shrt38_sector` / `shrt38_industry`（MATRIX） | 可用于 group 轴 |

## 四、本轮 probe（SIW 波，12 条，decay 4 起）

1. `amt_wgt` 水平 / 2. `tot_amt_wgt` 水平 / 3. `tot_qty_wgt` 水平 / 4. `ytq` 总卖空股数
5. `amt_wgt` ts_delta（拥挤度动量）/ 6. `amt_wgt` ts_rank 252（长窗强度）
7. `amt_wgt` ts_std_dev 20（**不稳定性，帖2核心**）/ 8. `amt_wgt` ts_arg_max 20（**峰值新近度，帖2核心**）
9. 日度 `qty_wgt` / 10. `tot_amt_wgt / tot_qty_wgt`（单位卖空金额，帖3比值结构）
11. `amt_wgt` ts_mean5 平滑 / 12. `amt_wgt` + sector 轴（帖2行业中性化）

**关键前提**：`*_wgt` 在 shortinterest38 是 **VECTOR 类型**（非 event），可用 `vec_avg` 聚合——与 risk59 的 event 字段陷阱不同。
