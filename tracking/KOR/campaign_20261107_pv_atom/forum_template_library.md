# 论坛可移植模板库（KOR 本轮在用）· 2026-11-07

## F1 · 机构参与「新鲜度门」（来源：论坛，24 赞，IND/TOP500 已提交 OS）
- 原帖：《【Alpha Idea】机构参与"新鲜度门"：IND 机构持股广度在机构撤退期的逆势吸筹尝试》author LC97552
- 战绩：Sharpe **1.62** / Fitness 1.37 / 2Y **2.47** / Margin 36.3bps / 18 项硬检查全 PASS（含 PC/SC）
- 数据集：**institutions6**（KOR 同名数据集存在，字段已验证可用）

### 骨架
```
trade_when(
  ts_arg_max(<PARTICIPATION_MEASURE>, G) < T,
  signed_power(ts_quantile(divide(<BUYER_FLOW>, ts_mean(<HOLDER_BASE>, M)), W, driver="gaussian"), p),
  -1)
```
KOR 实例（冠军参数）：PARTICIPATION=count_institutional_holders_security, BUYER_FLOW=count_institutional_buyers_security,
G=90, T=33, M=72, W=840, p=1.6

### 各件作用（原帖实证）
| 件 | 取值 | 为什么 |
|---|---|---|
| 比值核 | divide(buyers, ts_mean(holders, 72)) | 分母 72 日平滑剥 13F 季度披露阶梯跳变，是 **FT>1.0 首破点** |
| 自锚定分位 | ts_quantile(_, 840, driver=gaussian) | 比值尺度随全市场机构参与周期漂移，需对自身 3 年+ 历史取分位；gaussian 比经验分位平滑 |
| 保号凸化 | signed_power(_, 1.6) | 凸放大极端分位、保留符号 |
| **新鲜度门** | ts_arg_max(holders, 90) < 33 | 持有人峰值距今 <33 日才持仓；否则 trade_when 第三参 -1 平仓 |
| 设置 | SUBINDUSTRY / decay 9 / trunc 0.03 | decay 每 +2 → TO −0.2pp，dec9 是 TO 地板 |

### ★ 最重要的一条方法论（原帖明确结论）
**`ts_arg_max` 作信号时是「信号摧毁器」（假信号多、时序噪声大，原帖经验 864/958/1097 反复验证）；
作门控条件（新鲜度阈值）时是冠军机制。用法边界比算子本身更决定成败。**

### G/T 网格甜点（原帖实测）
- 甜点：**66/33 与 90/33**（G∈[66,180] × T∈[22,45] 内）
- 66/22 崩到 SH 1.02；G≥120 单调衰减
- 分母窗 m↑ → 曲线平滑度 np 单调降（0.691→0.557）、SH 单调升（1.45→1.62）
- 不可同时达到：{SH≥1.58 ∧ np≥0.6 ∧ 2021>0 ∧ wTO≥5%}

### 原帖已证伪的 5 代前身（**KOR 不要重试**）
同步比值 divide(buyers,holders) 裸信号 = 结构不可行；ts_corr(buyers,holders,66) = 0.38；
美元净流 = 0.44；渗透率 = 0.20；sellers 反向 = 0.71。

### 论文支撑（可复用）
- Gabaix & Koijen (2023) Inelastic Markets：$1 机构流入 → $5 市值，流量停滞后价格影响仍持续
- Feng/He/Wang/Xiao (2026) Active Fund Co-Holdings：机构持仓网络变化 → 下一月焦点股超额收益，形成后**持续而非反转**
- Da/Larrain/Sialm/Tessada (2016) Coordinated Noise Trading：养老金再配置造成价格短暂偏离
- Gabaix et al. (2005)：大机构交易在流动性不足市场制造无基本面 price spike

## F2 · KOR fundamental（来源：论坛，20 赞）—— **经评论区证伪，不采纳**
- 主张：rank(ts_backfill(fnd17_yield,126)) − rank(ts_backfill(fnd10_pe_ttm,63))，STATISTICAL 中性化 → S 1.76，Python 版 2.08
- 证伪点（评论区 YR99599 + 作者自评）：
  1. **KOR 的 STATISTICAL 中性化不可用（报 400）** ⇒ 1.76 无法复现
  2. Python 版 (2.08) 与 FastExpr 版 (1.76) **不是同一个信号**：前者是「对自身移动均值的偏离」（时序去均值），后者是「水平值横截面排名」；2.08 vs 1.76 的差来自这个改动，不是 rank 实现
  3. 「MARKET 中性化下信号消失 ⇒ 纯 Alpha」推论方向反了：净敞口被抹掉才掉分，通常说明 PnL 相当部分来自净市场暴露
  4. TOP600 只有 600 只票，估统计风险因子自由度紧，残差留噪声 ⇒ IS 虚高
  5. 「年报季提高权重」= 拟合披露日历（韩股年报集中 3-4 月披露，4-5 月信号最强 = 新数据刚到），不是季节性 alpha
- **可复用陷阱**：小截面（TOP600）上 STATISTICAL / 高自由度中性化的 IS 高分不可信；季节性强弱多是数据到达日历。
- 附带确认：**KOR D1 唯一可用 universe 是 TOP600**（TOP3000/2000/1000 全报错），与本战役 MCP 实测一致。

## 工具坑：preflight 对 driver 参数值报假阳性
`ts_quantile(x, 840, driver="gaussian")` 会让 `preflight_expressions` 返回
`valid=false, unknown_fields=["gaussian"]`。但 `get_operators` 确认定义就是 `ts_quantile(x,d, driver="gaussian")`，
且返回体 `platform_field_count: 2` 证明其余标识符全部解析成功 ⇒ **纯假阳性，可派发**。
判读口诀：unknown_fields 只含 driver 值（gaussian/uniform/cauchy）时忽略；含真实字段名才拦截。
