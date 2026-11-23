# fund_holdings_panel · EUR / TOP2500 / D1 字段画像（2026-11-22 全字段普查）

> 类型 VECTOR · 30/30 字段全量拉取（complete=true）· category = **institutions**（×1.1，塔位 0/3）
> 采集：2026-11-22 · 数据 = 日频账户级机构持仓/交易面板

## 0. 可用性分层（全字段，全部为数值 VECTOR）

| 层 | 字段 | αC | cov | 语义 |
|---|---|---:|---:|---|
| **持仓存量** | `security_holding_usd_value`(105)、`holder_account_total`(126)、`mean_security_weight`(6)、`top_weighted_account_number`(11) | ≤126 | 0.86–0.92 | 持有金额/家数/平均权重/conviction 家数 |
| **交易流量** | `security_transaction_usd_value`(45)、`transaction_account_total`(24)、`boundary_transaction_total`(77)、`boundary_transaction_usd_value`(18)、`large_trade_count_50bps`(8)、`top_weighted_transaction_number`(7) | ≤77 | 0.84–0.91 | 交易金额/交易家数/开平仓事件 |
| **集中度（HHI 族）** | `herfindahl_index_holdings`(105)、`herfindahl_index_transactions`(11)、`holding_value_distribution_score`(80)、`transaction_value_distribution_score`(16) | ≤105 | 0.86–0.92 | 拥挤度/分散度 |
| **稳定事件** | `stable_boundary_trade_count_21d`(100) | 100 | 0.908 | 21 日内无同标的 boundary 交易账户的开平仓（**持久开仓**，d5WNR8oG 已用作腿） |
| `_active` 镜像 | 全字段 ×`_active` 变体（排除已清仓账户） | ≤99 | 0.843–0.857 | 同语义窄口径 |

**画像结论**：30 字段全数值、双口径（全量 vs active）。核心机制面 = ①机构开平仓事件流（boundary）②持仓集中度（HHI/conviction）③净买卖。**日频**（相对 institutions6 季频是巨大优势）。

## 1. 已验证线索

- `stable_boundary_trade_count_21d` 已作为混合腿出现在 IS_ONLY 候选 `d5WNR8oG`（CROWDING/S2 3.56）——说明该字段与 techindi 概率腿相容。
- KOR 侧同名数据集历史：`fund_holdings_panel` 曾触发「六维未穷尽但字段落地性收敛」判 PROVISIONAL（未引新信息源）；EUR 侧独立评估。

## 2. 机制假设（ATOM 优先，单集内组合）

- M1 持久开仓密度：`ts_rank(stable_boundary_trade_count_21d, 66)`（新开仓潮 → 正向）
- M2 净流量：`divide(security_transaction_usd_value, security_holding_usd_value)`（换手强度）
- M3 拥挤度反转：`-ts_zscore(herfindahl_index_holdings, 252)`（集中度上升→拥挤→反转）
- M4 conviction 扩张：`ts_delta(top_weighted_account_number, 66)`（conviction 家数增加）
- M5 大单跟随：`ts_sum(large_trade_count_50bps, 22)`（>0.5% AUM 大单累积）

## 3. 风险先验

- `holder_account_total` KOR 实测「零值≈0 排除 trade_when」——EUR 同构字段先用 preflight 验证零值分布
- cov 0.84–0.92 健康，sub 闸风险低于 socialmedia15
- HHI 族 aC 105 偏拥挤，prod 先验中等；transaction 分布分 aC≤16 冷

## 4. ★ Institutions ATOM 攻坚（2026-11-22，用户指令「在 Institutions 挖掘 ATOM」）

> 全字段重拉确认：institutions6 = 11/11 MATRIX（季频），fund_holdings_panel = 30/30 VECTOR（日频）。
> 本轮聚焦 fund_holdings_panel（日频），此前 10 臂全灭用的是「拥挤度/换手」族；本次改用**未测字段**设计 5 个结构互异模板族。
> 统一配置：TOP2500 / CROWDING / decay4 / trunc0.0 / nan ON / maxTrade OFF。

| 族 | 机制 | 核心字段 | 表达式骨架 | alpha |
|---|---|---|---|---|
| **A1 B 换手强度** | 交易额÷持仓额 = 机构换手率，z 相对自身一年 | security_transaction_usd_value / security_holding_usd_value | `group_rank(ts_zscore(ts_backfill(divide(vec_sum(T),vec_sum(H)),66),252),industry)` | 待收割 |
| **A2 H conviction 扩张** | 重仓账户家数 22d 变化（信念增强） | top_weighted_account_number | `group_rank(ts_delta(ts_backfill(vec_sum(X),66),22),industry)` | 待收割 |
| **A3 H 平均权重** | 组合平均权重（基金 conviction 程度）的异常 | mean_security_weight | `group_rank(ts_zscore(ts_backfill(vec_avg(W),66),252),industry)` | 待收割 |
| **A4 E 大单事件** | >0.5% AUM 大单笔数（信息含量高的交易） | large_trade_count_50bps | `group_rank(ts_zscore(ts_backfill(vec_sum(L),66),252),industry)` | 待收割 |
| **A5 E 持久开仓** | 21d 无重复 boundary 交易的持久开仓潮 | stable_boundary_trade_count_21d | `group_rank(ts_zscore(ts_backfill(vec_sum(S),66),252),industry)` | 待收割 |

**探针批** `3pLZND4S54nXcylEOWOJCv`（5 臂）：preflight 全过（字段存在 + VECTOR 降维 + 无 UNITS 隐患）。
收割后：有效族（|S|≥1.0）做完整梯度（同类别算子全替换 + 参数档 + 多配置档）；全灭则换 institutions6 季频集。

**Wave 1 结果（TOP2500/CROWDING，`3pLZND4S54nXcylEOWOJCv`）——5 族全灭**：

| 族 | alpha | S | F | 2Y | sub | TO | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| A1 换手 zscore | kqaYp508 | 0.09 | 0.01 | 1.66 | 0.14 | 38.3% | 2 |
| A2 conviction delta | Jj82aLvx | −0.27 | −0.06 | 0.15 | −0.42 | 16.8% | 4 |
| A3 平均权重 | d5aPJwZX | −0.40 | −0.12 | −0.53 | −0.11 | 8.2% | 3 |
| A4 大单 zscore | QP0oRdGG | 0.23 | 0.05 | 1.16 | 0.89 | 19.3% | 3 |
| A5 持久开仓 zscore | XgaOZEo0 | 0.29 | 0.05 | −0.02 | 0.31 | 27.2% | 3 |

⇒ zscore（相对自身历史）形态全灭；A1 换手 2Y1.66 值得换抽取形态再试。

**Wave 2（形态对照 + SLOW_AND_FAST，`E9Zguc9x4E3aXgOmBBRwVC`，在飞）**：
A1 三形态（group_backfill 保留水平 / ts_rank 分位 / ts_delta 变化）+ A4 保留水平 + A5 分位。
⚠ 派批时静态闸逮到 `group_backfill` 只给 2 参（签名需 3 参 `(x,group,d)`）——修正为 3 参后重派成功，静态闸有效。

**Wave 2 结果（SLOW_AND_FAST，`E9Zguc9x4E3aXgOmBBRwVC`）**：4 臂 UNITS 错
（换手比 `divide(USD,USD)` 带量纲，`add(...,1)` 加裸常数冲突 = 记忆登记的裸常数 UNITS 坑）；
唯一成功的持久开仓分位形态 `RRevg0p0` S0.30/2Y0.26 ⇒ 全灭。
⇒ **fund_holdings_panel 旧轮 ATOM 判定：信号层弱**（两轮 12 臂 + 换形态 + 换配置，|S|≤0.40）。

### 4.1 ★★ 论坛+论文驱动 10 新模板（2026-11-22，用户第三轮指令）——天花板抬到 S1.36

按用户指令查论坛（MCP）+ 论文（paper_search --diverse，25篇/20作者）后，组 **10 个与已测互异的模板**（每字段一行 TemplatePlan），
批 `3RH10K3w04TJaVA1cqp7pR32`（10 臂）。**T10 `holding_value_distribution_score` 出 S1.31/2Y2.48/fRA2 纯 ATOM（INSTITUTIONS eff=1）**，
五轴梯度（内层算子/参数/分组/中性化/decay/外层）**全量穷尽后（内层16算子全测）**天花板 = **`kqaMXAv6` S1.52/F0.78/2Y2.77/sub1.44**（`ts_scale(backfill(hvds,22),252)` + group_rank + CROWDING），距 S 闸 1.58 仅 **0.06** / F 闸 0.22。
⇒ **该集 ATOM 天花板由 0.86 抬升到 1.52（+0.66），仍未过闸**；breadth/smart money/HHI 背离族全灭。
⇒ 完整 TemplatePlan（evidence+excluded+全轴 Δ 表）见 `fund_holdings_panel_EUR_templateplan_20261122.md` §7（权威结论）。

---

## 附：institutions6 ATOM 攻坚（2026-11-22，同批用户指令）

> 全字段 11/11 MATRIX 重拉确认（季频）。用买卖不对称机制（JMZ 2003），此前测的是 density zscore，
> 本次用**未测的比值形态**，配置 TOP2500/SLOW_AND_FAST/decay4。

| 族 | 机制 | 字段 | alpha | S | F | 2Y | sub |
|---|---|---|---|---:|---:|---:|---:|
| R1 买卖家数比 | 买家/卖家比（相对自身历史） | buyers/sellers | leaNo6n5 | **0.86** | 0.28 | 1.40 | 0.85 |
| R2 买家占比 | 买家/持有人数 | buyers/holders | 78Y2eqp8 | 0.84 | 0.27 | 1.08 | 0.59 |
| R3 净买入金额占比 | (买入−卖出)/持仓市值 | market_value acquired/disposed | 9ql2NPnK | 0.52 | 0.13 | 0.42 | 0.31 |
| R4 买入股数占比 | 买入股数/机构总持股 | quantity acquired/shares | O0W2lw37 | 0.59 | 0.15 | 1.66 | 0.34 |
| R5 持有人数变化 | 持有人数 delta | holders | KPg2WY1z | −0.32 | −0.07 | −0.88 | 0.18 |

**梯度 Δ 表（`2X0yiZc0l5iSbJksXhh0PGC`，R1 买卖家数比 ts_zscore 层同类算子全替换）**：

| 算子 | alpha | S | 2Y | ΔS |
|---|---|---:|---:|---:|
| **ts_zscore（基线）** | leaNo6n5 | **0.86** | 1.40 | — |
| ts_rank | 0mPLbKwq | 0.77 | 1.12 | −0.09 |
| ts_quantile | rK7w1rj8 | 0.79 | 1.09 | −0.07 |
| ts_decay_linear | pwakq1Po | −0.18 | −0.46 | −1.04 |
| ts_ir | d5a62lOK | 0.07 | −0.11 | −0.79 |

⇒ 基线 ts_zscore 最优，替换全降 ⇒ **R1 族梯度穷尽，天花板 S0.86**。

**institutions6 ATOM 最终判定**：信号层弱（比值形态 5 族 + 梯度，天花板 S0.86；此前 density 形态天花板 S0.95）⇒
两形态族一致远低于 S1.58 闸。**作强腿不可行，但作弱腿贡献过 S3.90（d5aPlXjX）** —— 再次印证"作强腿弱、作弱腿强"的结构属性。
