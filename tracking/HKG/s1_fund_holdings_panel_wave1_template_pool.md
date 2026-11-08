# HKG · fund_holdings_panel · wave1 模板池（15 模板，四维互异）

> 生成 2026-11-06 05:45 · HKG / TOP800 / D1
> 选它理由：**institutions category 在 HKG 为 0/3（未点亮塔）**、cov 0.892/0.785、aC 3–17 极低；且按新判据（TO>40% + |S|<0.3 ⇒ 高频刷新噪声）应避开日频聚合面，本集是**季频机构持仓 + 事件型交易流**，天然慢变。

## 1. 字段画像（30 字段 = 12 MATRIX 主 + 6 MATRIX `_active` + 12 VECTOR 主 + 6 VECTOR `_active`）

### 1.1 MATRIX 结构面（cov 0.892；`_active` 版 cov 0.785）

| 字段 | aC | 经济含义 | 模板角色 |
|---|---:|---|---|
| `holder_account_total` | 8 | 持有该 ISIN 的基金/账户家数 | **机构广度**（主信号） |
| `herfindahl_index_holdings` | 12 | 按账户权重算的 HHI 持仓集中度 | **拥挤度** |
| `holding_value_distribution_score` | 8 | 持仓价值在账户间的集中度（自定义拥挤度量） | 拥挤度（与 HHI 不同构造） |
| `mean_security_weight` | 13 | 仅对持有它的账户求平均组合权重 | 信念强度 |
| `security_holding_usd_value` | 17 | 全体账户合计持仓 USD 市值 | 规模/天数分母 |
| `top_weighted_account_number` | 3 | 该 ISIN 属于「信念持仓」（组合前 30%）的账户数 | **信念广度** |

### 1.2 VECTOR 交易流面（cov 0.855；`_active` 版 cov 0.739，**必须 `vec_avg()`**）

| 字段 | aC | 经济含义 | 模板角色 |
|---|---:|---|---|
| `security_transaction_usd_value` | 11 | 当日交易 USD 金额 | **数据集内 DaysADV 分母** |
| `boundary_transaction_total` | 6 | 边界交易笔数（新建仓 / 完全清仓） | **事件型进/出** |
| `boundary_transaction_usd_value` | 1 | 边界交易 USD 金额 | 事件强度 |
| `large_trade_count_50bps` | 1 | 单笔 > 基金 AUM 0.5% 的笔数 | 大单信念 |
| `herfindahl_index_transactions` | 3 | 交易金额在交易账户间的 HHI | 交易集中度 |
| `transaction_account_total` | 3 | 当日交易账户数 | 参与广度 |
| `transaction_value_distribution_score` | 2 | 交易金额分布集中度（0–1） | 交易拥挤 |
| `stable_boundary_trade_count_21d` | 2 | 「此前无边界交易」账户的边界交易笔数 | **耐心资本** |
| `top_weighted_transaction_number` | 3 | 信念持仓账户的交易笔数 | 信念交易 |

**硬陷阱**：18 个 VECTOR 字段裸用必报 `does not support event inputs`，必须 `vec_avg()`。12 个 MATRIX 可直接用。

## 2. 模板库（四维坐标：骨架 / 矩 / 分组轴 / 非线性）

| # | 名称 | 骨架 | 矩 | 分组轴 | 非线性 | 来源 |
|---|---|---|---|---|---|---|
| T1 | 持仓集中度（拥挤） | 单腿 | 水平 | subindustry | — | 论坛《机构持仓变化与拥挤反转》+ Brown-Howard-Lundblad 拥挤尾部风险 |
| T2 | 机构广度 | 单腿 | 水平 | subindustry | — | 论坛《机构广度：institutions6 印度市场》 |
| T3 | 广度增量（建仓期） | 单腿 | 一阶差分 | subindustry | — | 论坛《机构参与「新鲜度门」》 |
| T4 | **数据集内 DaysADV** = 持仓额 / 交易额 | 两腿比 | 水平比 | subindustry | — | 论坛《从近期论文挖出的 18 个 Alpha 创意》：DaysADV↑1σ ⇒ NCSKEW +14.8% / DUVOL +23.5%，**亚洲与对冲基金最强** |
| T5 | 信念持仓占比 | 两腿比 | 水平比 | subindustry | — | 自建（`top_weighted_account_number / holder_account_total`） |
| T6 | 信号 ×(1−拥挤度) | 三腿 | 复合 | subindustry | 乘法门控 | 论坛《好信号也要挑时机：信号×(1-拥挤度) 的非对称加权》 |
| T7 | 边界交易冲击（新进/清仓事件） | 单腿 | 事件水平 | subindustry | — | 论坛《机构持仓结构：IVA/MFM/CNI 三分法》 |
| T8 | 大单信念交易 | 单腿 | 水平 | subindustry | — | 自建（`large_trade_count_50bps`） |
| T9 | 交易 vs 持仓集中度背离 | 两腿差 | 形状差 | subindustry | — | 自建（交易拥挤 ≠ 持有拥挤） |
| T10 | 主动 vs 全量账户背离 | 两腿差 | `_active − 全量` | subindustry | — | 自建（主动管理人 vs 被动托管） |
| T11 | 耐心资本 | 两腿比 | 水平比 | subindustry | — | 论坛 IVA/MFM/CNI「稳定性因子」 |
| T12 | 缺口回填 + 慢速标准化 | 单腿 | 水平 | subindustry | `group_backfill(...,252)` + `ts_zscore` | 论坛《覆盖率低的数据字段怎么用》 |
| T13 | 事件门控（有交易才持仓） | 门控 | 事件触发 | subindustry | `trade_when` | 论坛《状态门控与换手约束》 |
| T14 | 拥挤度中性化档 | 单腿 | 水平 | —（改中性化档为 CROWDING） | — | 论坛《CROWDING 均值回归模板》 |
| T15 | 广度 bucket 自定义分组 | 单腿 | 水平 | `bucket(rank(holder_account_total), range="0,1,0.2")` | 组内标准化 | CLAUDE.md「部分字段适合做 bucket 自定义分组」 |

### 四维覆盖核对

| 维度 | 覆盖 | 说明 |
|---|---|---|
| 骨架结构 | 5/5 | 单腿(T1,T2,T3,T7,T8,T12,T14,T15) / 两腿比(T4,T5,T11) / 两腿差(T9,T10) / 三腿复合(T6) / 门控(T13) |
| 矩 | 4/4 | 水平(T1,T2,T4,T5,T7,T8,T11) / 一阶差分(T3) / 形状差(T9,T10) / 事件计数(T7,T13) |
| 分组轴 | 4/4 | subindustry / bucket 自定义 / CROWDING 中性化 / market（备选） |
| 非线性 | 3/3 | 无 / 乘法门控(T6) / trade_when(T13) + group_backfill 回填 |

## 3. 单位安全设计（VERIFY 档下最容易踩的坑）

| 模板 | 分子 / 分母 | 是否同单位 |
|---|---|---|
| T4 | `security_holding_usd_value` / `security_transaction_usd_value` | ✅ 同为 USD |
| T5 | `top_weighted_account_number` / `holder_account_total` | ✅ 同为账户数 |
| T11 | `stable_boundary_trade_count_21d` / `boundary_transaction_total` | ✅ 同为笔数 |
| T9 | HHI − HHI | ✅ 同为 0–1 指数 |
| T10 | `_active` − 全量 | ✅ 同字段同单位 |

⚠️ **禁止** `add(<USD 金额>, 0.0001)` 一类保护常数——VERIFY 档必报单位不兼容；改用同单位相除或 `ts_backfill` 兜底。

## 4. 方向先验

| 假设 | 方向 | 依据 |
|---|---|---|
| H1 拥挤 ⇒ 反转 | 做空高 HHI / 高 distribution score | Brown-Howard-Lundblad；论坛拥挤反转帖 |
| H2 广度 ⇒ 正 | 做多持有家数多的 | 论坛 institutions6 帖（治理认可 + 流动性溢价） |
| H3 广度增量 ⇒ 正 | 做多 Δholder 正的（建仓期） | 论坛「新鲜度门」帖 |
| H4 DaysADV ⇒ 负 | 做空高 DaysADV（崩盘风险） | 论文 abstract_id=6987094，亚洲最强 |
| H5 信念持仓 ⇒ 正 | 做多高 conviction 占比 | smart money 假说 |
| H6 边界交易（新进）⇒ 正 | 做多新建仓事件 | 事件驱动 |

## 5. wave1 已派（4 条探针 / 2 批）

| 批 | 表达式 | 覆盖维 | 算子 |
|---|---|---|---:|
| `rhtF1Qd4IdazzQhTEBY5O` | `group_rank(herfindahl_index_holdings, subindustry)` | 结构面拥挤（T1） | 1 |
| `rhtF1Qd4IdazzQhTEBY5O` | `group_rank(vec_avg(security_transaction_usd_value), subindustry)` | 交易流水平 | 2 |
| `3MKg1U54z4NYbzh1huQXUDhs` | `group_rank(holder_account_total, subindustry)` | 广度（T2） | 1 |
| `3MKg1U54z4NYbzh1huQXUDhs` | `group_rank(vec_avg(boundary_transaction_total), subindustry)` | 事件（T7） | 2 |

**批级设置**：HKG / TOP800 / D1 / decay 4 / SECTOR / trunc 0.08 / unit VERIFY / nan **ON** / pasteurization ON / maxTrade OFF。

**读法（不变）**：第一轮只看 **2Y**。2Y ≥ 1.58 才进第二代；同时看 **TO**——若 4 条 TO 全部 >40% 则说明又是字段级刷新率问题，直接封盘（`news_sentiment_transfer` / `other553` 已两次实证）。

## 6. 第二代预备（待 wave1 解锁）

- T4 / T5 / T11 三条比值腿不依赖 level 方向，只要任一分母有覆盖就能跑，**优先级最高**。
- T6 / T13 两条门控腿用于压 TO 与提升 robust 子宇宙一致性。
- T14 换中性化档为 CROWDING 是设置级实验，需单独一批（不能与 SUBINDUSTRY/SECTOR 同批混档）。