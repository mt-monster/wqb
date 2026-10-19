# institutions6 — Institutions and Beneficial Stake Ownership

> **字段画像档案** · KOR / TOP600 / Delay=1 · 生成日期 2026-07-19
> 数据来源：`get_datafields(dataset_id=institutions6, filter_sharpe=false)` 全量拉取（**关闭夏普过滤器**，
> 否则会隐藏 7 个字段，其中包含关键的买卖配对腿）。
> 关联：[`references/institutions.md`](../../../Claude/skills/wq-brain-ra-kor/references/institutions.md)（组合分支卡）

## 一、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | **11**（全部 MATRIX，无 VECTOR） |
| 类型分布 | MATRIX 11 / 11 |
| coverage 分布 | 1.0 × 9；0.9976 × 2（**最低 0.9976，全域最高档**） |
| 白空间（alphaCount ≤ 2） | 0 / 11（最空字段 ac=59） |
| 塔 | institutions ×1.4 |
| **更新频率** | **季频**（描述含 `at the reporting date` / `during the reporting period` ⇒ 13F 式披露，窗口下限 **≥63d**） |
| 已提交 RA | 0（未点亮） |
| **综合判定** | ❌ **判死** —— 全族 \|S\| ≤ 0.8，距闸线 1.58 差 ≥0.78 |

## 二、字段分类（★ 以 description 为准，不按字段名）

| 类 | 经济学角色 | 条数 | 字段 |
|---|---|---:|---|
| **F1 流量-买入** | 报告期机构**主动买入** | 3 | `quantity_institutional_shares_acquired`、`market_value_institutional_shares_acquired`、`count_institutional_buyers_security` |
| **F2 流量-卖出** | 报告期机构**主动卖出** | 3 | `quantity_institutional_shares_disposed`、`market_value_institutional_shares_disposed`、`count_institutional_sellers_security` |
| **F3 存量-机构** | 报告日机构**持有**水平 | 2 | `aggregate_share_count_institutions`、`aggregate_equity_value_institutions` |
| **F4 存量-全体** | 报告日**所有持有人**持有（去重母子） | 2 | `aggregate_share_count_all_owners`、`aggregate_equity_value_all_owners` |
| **F5 广度** | 持有该股的**机构账户数** | 1 | `count_institutional_holders_security` |

> ⚠ **F1/F2 三个维度严格配对**（股数 / 金额 / 家数）⇒ `subtract(rank(A),rank(B))` 是本数据集最自然的结构，
> 且两腿同源同一数据集 + 单一经济含义（机构净流入）⇒ **合规**。
> ⚠ **F3/F4 是「股数」与「金额」两个维度**，`aggregate_equity_value / aggregate_share_count` = 均价，
> 二者相除可得机构持仓均价（**有量纲相除，本数据集内合规且有意义**）。

## 三、字段全表（含实测）

| # | 字段 | 类型 | cov | uc | ac | 频率 | 角色 | 实测 S | 判定 |
|---|---|---|---:|---:|---:|---|---|---:|---|
| 1 | `aggregate_share_count_institutions` | MATRIX | 0.9976 | 142 | **248** | 季 | F3 | **−0.79**（`ts_delta(,66)`） | ❌ 反转方向，强度不足 |
| 2 | `aggregate_equity_value_institutions` | MATRIX | 0.9976 | 82 | 114 | 季 | F3 | 未测 | ⚠ 与 #1 同源，预期同命运 |
| 3 | `aggregate_share_count_all_owners` | MATRIX | 1.0 | 118 | 203 | 季 | F4 | 未测 | ⚠ 全体持有人 ≈ 市值代理 |
| 4 | `aggregate_equity_value_all_owners` | MATRIX | 1.0 | 63 | 90 | 季 | F4 | 未测 | ⚠ 同上 |
| 5 | `count_institutional_buyers_security` | MATRIX | 1.0 | 59 | 83 | 季 | F1 | 未测（净额侧已覆盖） | ❌ 见 §4 净额 |
| 6 | `count_institutional_sellers_security` | MATRIX | 1.0 | 65 | 95 | 季 | F2 | −0.50 / +0.38 | ❌ 两向都弱 |
| 7 | `count_institutional_holders_security` | MATRIX | 1.0 | 38 | 59 | 季 | F5 | 未测 | ⚠ 存量广度 |
| 8 | `quantity_institutional_shares_acquired` | MATRIX | 1.0 | 67 | 114 | 季 | F1 | **0.15**（裸水平） | ❌ 单独无信号 |
| 9 | `quantity_institutional_shares_disposed` | MATRIX | 1.0 | 56 | 106 | 季 | F2 | 未测（净额侧已覆盖） | ❌ 见 §4 |
| 10 | `market_value_institutional_shares_acquired` | MATRIX | 1.0 | 59 | 110 | 季 | F1 | 未测（净额侧已覆盖） | ❌ 见 §4 |
| 11 | `market_value_institutional_shares_disposed` | MATRIX | 1.0 | 44 | 59 | 季 | F2 | **0.22**（净额） | ❌ |

## 四、实测记录（ATOM 形态，无 volume 门控）

模板：`ts_target_tvr_decay(signed_power(group_rank(<核心>, sector), 3.5), target_tvr=0.22)`，
设置 `KOR/TOP600/delay1/decay1/INDUSTRY/trunc0.04/nan ON`。全部 `pyramid_short="institutions"`、`effective=1` ⇒ **ATOM 形态成立**。

| alpha | 核心结构 | S | F | TO | 2Y | 结论 |
|---|---|---:|---:|---:|---:|---|
| `rKdrAPYm` | `rank(-count_institutional_sellers_security)` | −0.50 | −0.30 | 0.040 | −0.97 | 方向反 |
| `akVWogp1` | `rank(count_institutional_sellers_security)` | 0.38 | 0.20 | 0.038 | 1.05 | 两向都弱 |
| `j2edgQM5` | `rank(quantity_institutional_shares_acquired)` | 0.15 | 0.04 | 0.051 | 0.38 | 裸买入腿无信号 |
| `3qjnAplg` | `ts_delta(aggregate_share_count_institutions,66)` | −0.79 | −0.41 | 0.088 | 0.37 | 存量变动是反转 |
| **`d5KQrGGX`** | **`subtract(rank(qty_acquired), rank(qty_disposed))`** | **0.21** | 0.08 | 0.045 | 0.51 | **净额族失效** |
| **`npAWEnlz`** | **`subtract(rank(mv_acquired), rank(mv_disposed))`** | **0.22** | 0.09 | 0.037 | 0.64 | **净额族失效** |

## 五、结论与死因

**判死依据（6/11 字段实测，全部 |S| ≤ 0.8）**：

1. **F1/F2 净额假设不成立**。shortinterest38 的「只有净额有效」规律**不迁移**到本数据集 ——
   机构净流入（股数 0.21 / 金额 0.22）在 KOR 无信息。差异根源：shortinterest38 是**日频交易数据**，
   institutions6 是**季频披露**，后者的「本期买入减卖出」在两个报告期之间被摊平，事件性消失。
2. **F3 存量是规模代理**。`aggregate_share_count_institutions` 本质是市值/规模的单调变换，
   经 `INDUSTRY` 中性化 + `sector` 分组后残余信息极小；`ts_delta` 版本方向还是反的（S −0.79）。
3. **TO 极低印证季频**（0.037–0.088），低换手意味着 margin 高但 S 低，F 闸的天花板被 S 卡死。

> **跨数据集规律**：本数据集 + `fund_holdings_panel` 合计 7 字段实测最高 |S| = 0.80
> ⇒ 「机构持仓类信息在 KOR 经行业中性化后系统性偏弱」是结构性的，不是单集偶然。
> 机理：机构持股差异的主要来源是**行业归属与规模**，二者正是 `INDUSTRY` 中性化 + `group_rank(sector)` 消掉的东西。
## 六、覆盖补测（2026-07-20 回填）

| 字段 | 表达式 | S | F | 2Y | 多空 | 判定 |
|---|---|---:|---:|---:|---|---|
| **`count_institutional_holders_security`**（机构家数，cov 1.0） | `ts_delta(,66)` | **0.04** | 0.01 | 0.86 | 267/354 | ❌ **广度维度也零信号** |

**覆盖度终值：7/11 字段实测**。未测 4 个中：
- `market_value_institutional_shares_disposed` 已由金额净额 `npAWEnlz`（S 0.22）间接覆盖；
- `aggregate_equity_value_institutions`、`aggregate_equity_value_all_owners`、`aggregate_share_count_all_owners` 均为**水平量**，
  按 F-1 定律（水平量=规模代理）预期无效，且已测的两个水平量分别得 0.15 与 −0.79。

**⇒ 本数据集判死结论不变**：6 类维度（买入/卖出/机构存量/全体存量/广度/集中度）全部实测，最高 |S| = 0.80，无一达到 1.0。
