# institutions 字段画像 + 论坛/论文模板匹配（2026-11-16）

## 一、数据集与字段画像（平台实拉，GBR/TOP700/D1）

### institutions6（11 字段，全 MATRIX，元数据 cov 1.0）

| 字段 | 语义 | ac | 画像要点 |
|---|---|---:|---|
| `count_institutional_buyers_security` | 本期增持机构家数 | 181 | **计数器、季度阶梯披露**、覆盖充足 |
| `count_institutional_sellers_security` | 本期减持机构家数 | 212 | 同族，GBR 已证唯一活族（0.95） |
| `count_institutional_holders_security` | 当前持有人总数 | 110 | **持有人基数**（天然分母） |
| `aggregate_equity_value_institutions` | 机构持仓总市值 | 128 | 连续值、美元量纲 |
| `aggregate_equity_value_all_owners` | 全部持有人总市值 | 99 | 分母候选 |
| `aggregate_share_count_institutions` | 机构持股数 | 119 | 股数量纲 |
| `aggregate_share_count_all_owners` | 全部持股数 | 135 | 分母候选 |
| `market_value_institutional_shares_acquired` | 买入金额 | 116 | 美元量纲 |
| `market_value_institutional_shares_disposed` | 卖出金额 | 83 | 美元量纲 |
| `quantity_institutional_shares_acquired` | 买入股数 | 151 | 股数量纲 |
| `quantity_institutional_shares_disposed` | 卖出股数 | 93 | 股数量纲 |

**关键画像结论（决定模板选择）**：
- 全部为 **13F 式季度披露** → 序列是**阶梯函数**，直接做水平/差分会被披露跳变主导
- **计数类（buyers/sellers/holders）** 是覆盖最稳的族，连续值族受币种/拆股口径影响
- 分母必须做**~72 日（一季度）平滑**才能剥掉阶梯跳变
- 量纲陷阱：美元/股数字段**禁止 `add(x, 常数)`**（本日实测 3 次整批拒收）

### fund_holdings_panel（18 字段，全 VECTOR，cov 0.89-0.93）

交易行为族：`boundary_transaction_total`（开/清仓笔数）、`stable_boundary_trade_count_21d`（21 日无重复的耐久变动）、`large_trade_count_50bps`（大单）、`security_transaction_usd_value`、`transaction_account_total`（账户广度）、`transaction_value_distribution_score`（集中度）、`herfindahl_index_transactions`。
⚠ **目录变更**：历史最优字段 `herfindahl_index_holdings` 已不在当前目录，历史 0.80/2Y1.50 不可复现。

---

## 二、论坛取证

### ★ 主命中：机构参与「新鲜度门」配方（LC97552，24 赞，2026-09-09）
帖子 ID `43358755666967`。**同一数据集 institutions6、同一组字段**，IND/TOP500/D1 实测 **S1.62 / F1.37 / 2Y2.47 / margin 36.3bps / 18 项硬检查全 PASS，已提交 OS**。

```text
trade_when(
  ts_arg_max(count_institutional_holders_security, 90) < 33,
  signed_power(
    ts_quantile(divide(count_institutional_buyers_security,
                        ts_mean(count_institutional_holders_security, 72)),
                840, driver="gaussian"),
    1.6),
  -1)
```
Settings：SUBINDUSTRY / decay 9 / truncation 0.03 / delay 1 / pasteurization ON。

**机制**：机构参与度的"新鲜度"携带信息——覆盖人数峰值距今 <33 日（仍在参与、且拥挤顶点已过）+ 买家/持有人比值异常抬升 = 逆势吸筹窗口。

**三条可复用结论（作者自述，50 批 414 次模拟）**：
1. **`ts_arg_max` 作门控是冠军、作信号是摧毁器**（本仓库 memory `freshness-gate-fhp` 已有同结论）
2. 分母 `ts_mean(holders, 72)` 是「Fitness 首破 1.0」的关键（剥季度阶梯）
3. G∈[66,180]×T∈[22,45]：**66/33 与 90/33 是甜点**，66/22 崩到 S1.02，G≥120 单调衰减

**作者留下的开放问题（原文）**：「门控窗口 G/T 在其他 Region 的慢变阶梯披露计数类（**如 GBR Institutions**）是否可平移？系数必重扫，机制可推断。」——本条即本轮回测的直接立项理由。

### 13F 披露时滞（WL27618，28 赞，2026-09-15）
帖子 ID `43497524382231`。要点：① 回测必须按**披露生效日**更新，不可用报告期截止日（防前视）；② **剔除高频换手机构**——13F 只对长线机构的持仓有跟踪价值；③ 滞后信息仍可交易，因为后续跟风资金会买单。

### 机构撤离后超额弹性（IND，2 赞）
引用 Dasgupta et al. (2011, "The Price Impact of Institutional Herding") — 机构羊群的价格冲击。

---

## 三、论文锚（论坛引用，未本次联网复核）

| 论文 | 机制 | 对应字段/模板 |
|---|---|---|
| **Gabaix & Koijen (2023)** Inelastic Markets Hypothesis | $1 机构流入 → $5 市值，且流量停滞后价格影响持续 | 支撑「参与度变化→定价滞后」；对应 buyers/holders 比值 |
| **Feng, He, Wang & Xiao (2026)** Active Fund Co-Holdings | 机构参与变化 → 下一月焦点股超额收益，**持续而非反转**，集中于高摩擦小盘 | 支撑持有网络/参与广度；指出「持续」意味着不应做反转 |
| **Da, Larrain, Sialm & Tessada (2016)** Coordinated Noise Trading | 养老金再配置造成价格短暂偏离；「突增→保持→回落」节奏 | 对应新鲜度门的时间结构 |
| **Gabaix et al. (2005)** Institutional Investors and Volatility | 大机构在流动性不足市场制造价格 spike | 对应「撤退期波动」regime |
| **Dasgupta et al. (2011)** Price Impact of Institutional Herding | 机构羊群的价格冲击与后续修正 | 对应 sellers 族（GBR 唯一活族） |

⚠ WebSearch 工具本轮 4 次超时不可用，以上论文源自论坛帖引用，**未做联网原文核对**。

---

## 四、模板匹配表（本轮回测依据）

| # | 模板 | 来源 | 字段映射 | 与 GBR 历史的关系 |
|---|---|---|---|---|
| **T1** | **新鲜度门 × 广度比值**（主） | 论坛 LC97552（已 OS） | holders→gate, buyers/holders→signal | **从未测过**；GBR 历史只测过 sellers 水平/ts_rank |
| T2 | 13F 滞后 + 长线机构过滤 | 论坛 WL27618 | 同上，但用长平滑替代门控 | 部分对应历史 ts_mean 平滑（弱） |
| T3 | 机构羊群冲击（sellers 族） | Dasgupta 2011 | sellers 计数 | **已测，GBR 唯一活族 0.95** |
| T4 | 参与广度持续溢价（非反转） | Feng 2026 | buyers/holders 水平 | 已测（水平/比值）→ 弱 |
| T5 | 协调噪声（养老金再配置） | Da 2016 | 账户广度/集中度（fund_holdings_panel） | 已测 → 0.28 |

**结论**：五个模板里 **T1 是唯一从未在 GBR 测过的**，且它在 IND 已出货；T3 已到顶（0.95），T4/T5 已证弱。**本轮全部火力对准 T1**。
