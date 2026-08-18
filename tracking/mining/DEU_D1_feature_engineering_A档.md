# DEU D1 特征工程报告 — fund_holdings_panel + insider_agg_matrix
# 生成时间: 2026-08-10
# 工具: brain-data-feature-engineering 工作流（8 类问题驱动）
# 目标: 将原始字段 → 有预测含义的可用特征 → 可直接模拟的表达式

---

## 1. 数据集理解

### 1.1 fund_holdings_panel（institutions ×1.9，18 VECTOR 字段，字段级 0 用户 0 alpha）

**核心故事**：DEU 股票上机构基金的**日度交易行为**。全部字段是"总额/计数/集中度"，按 `_active`（活跃账户）与全账户两个版本给出。

**关键结构性观察** ⚠️：
- **所有字段无方向**（boundary = 新建仓+清仓之和，未拆分 buy/sell）
- 信号本质 = 机构**活动强度、规模、集中度、持久性**，而非方向
- 因此 alpha 逻辑必须建立在："机构在动 → 信息揭示/价格压力/后续跟随"，而不是"机构在买"

### 1.2 insider_agg_matrix（insiders ×1.9，34 MATRIX 字段）

**核心故事**：DEU 公司内部人（高管/董事）交易。
- `directional_indicator` / `directional_indicator_2`：**cov=1.00 且 alphaCount=0**（全平台最干净的点塔素材）
- **有方向**（buy/sell 拆分、方向指标），可直接构造净买信号
- 高管（top_）vs 董事（secondary_）拆分，significance 值排序可用

---

## 2. 字段解构（关键字段语义）

### fund_holdings_panel
| 字段 | 真正衡量什么 | 特征价值 |
|------|-------------|---------|
| `stable_boundary_trade_count_21d` | 21 天无前序边界交易的建仓/清仓数 = **持久性决策**（剔除了频繁倒仓的噪声账户） | ⭐⭐⭐⭐⭐ 最高质量 |
| `boundary_transaction_usd_value` | 边界交易美元总额 = **资金行动规模** | ⭐⭐⭐⭐⭐ |
| `top_weighted_transaction_number` | 重仓股（conviction）交易数 = **基金核心信念的变动** | ⭐⭐⭐⭐ |
| `large_trade_count_50bps` | 交易额 > 0.5% AUM 的大额交易 = **单笔冲击强度** | ⭐⭐⭐⭐ |
| `herfindahl_index_transactions` | 交易价值跨账户集中度（0-1）= **少数账户垄断程度** | ⭐⭐⭐ |
| `transaction_value_distribution_score` | 交易价值分布集中度（0-1） | ⭐⭐⭐ |
| `security_transaction_usd_value` | 该证券当日总交易额 = **流量水平**（不含方向） | ⭐⭐⭐ |
| `transaction_account_total` | 交易账户数 = **分歧度/广度** | ⭐⭐ |

### insider_agg_matrix
| 字段 | 真正衡量什么 | 特征价值 |
|------|-------------|---------|
| `directional_indicator` | 内部人净方向（100% 覆盖） | ⭐⭐⭐⭐⭐ |
| `directional_indicator_2` | 增强净方向（100% 覆盖，0 alpha） | ⭐⭐⭐⭐⭐ |
| `total_top_buy/sell_shares` | 高管买入/卖出股数 | ⭐⭐⭐⭐ |
| `total_buy/sell_shares` | 全体董事买入/卖出股数 | ⭐⭐⭐ |
| `top_significant_value_1` | 最大显著交易金额 | ⭐⭐⭐ |
| `top_directional_significant_value_1` | 最大方向性显著交易金额 | ⭐⭐⭐⭐ |

---

## 3. 特征工程建议（按 8 类问题）

### 3.1 Stability — "什么稳定？"
- **F1 "机构关注度稳定性"**：低波动 = 机构行为模式稳定可预期
  - `-ts_std_dev(vec_sum(herfindahl_index_transactions), 63)`
  - 逻辑：HHI 波动低 → 交易模式稳定 → 信息结构清晰
- **F2 "内部人情绪一致性"**：`ts_std_dev(directional_indicator, 63)`（低 = 内部人意见一致）

### 3.2 Change — "什么在变？"
- **F3 "边界资金流加速度"**：`ts_delta(vec_sum(boundary_transaction_usd_value), 5)`
  - 机构建仓/清仓活动 5 日变化 = 资金流加速
- **F4 "大额交易激增"**：`ts_delta(vec_sum(large_trade_count_50bps), 22)`
- **F5 "内部人方向反转"**：`ts_delta(directional_indicator, 5)`（内部人转向）

### 3.3 Anomaly — "什么异常？"
- **F6 "交易集中度异常"**：`ts_zscore(vec_sum(herfindahl_index_transactions), 126)`
  - 少数账户突然垄断交易 = 信息性事件（如大宗建仓）
- **F7 "持久性交易爆发"**：`ts_zscore(vec_sum(stable_boundary_trade_count_21d), 126)`

### 3.4 Interaction — "什么组合？"
- **F8 "持久 × 规模"（最强候选）**：`vec_sum(stable_boundary_trade_count_21d) * vec_sum(boundary_transaction_usd_value)`
  - 持久决策 × 大资金 = 最可信的机构行为信号
- **F9 "conviction × 集中度"**：`vec_sum(top_weighted_transaction_number) * vec_sum(herfindahl_index_transactions)`

### 3.5 Structure — "什么结构？"
- **F10 "持久交易占比"（信号质量比）**：`vec_sum(stable_boundary_trade_count_21d) / (1 + vec_sum(boundary_transaction_total))`
  - 越高 = 机构决策越"想清楚才动"
- **F11 "内部人净买卖强度"**：`(total_top_buy_shares - total_top_sell_shares) / (1 + total_top_buy_shares + total_top_sell_shares)`
  - 高管净方向 × 强度（-1 ~ +1 归一）

### 3.6 Cumulative — "什么累积？"
- **F12 "3 个月持久性机构活动"**：`ts_sum(vec_sum(stable_boundary_trade_count_21d), 63)`
- **F13 "内部人 3 个月净方向动量"**：`ts_sum(directional_indicator, 63)`
  - 内部人持续净买/净卖 = 最强传统 alpha 族
- **F14 "conviction 累积"**：`ts_sum(vec_sum(top_weighted_transaction_number), 126)`

### 3.7 Relative — "什么相对？"
- **F15 "截面机构活跃度"**：`rank(vec_sum(boundary_transaction_usd_value))`
- **F16 "截面内部人强度"**：`rank(ts_sum(directional_indicator, 63))`
- **F17 "相对自身历史分位"**：`ts_rank` ⚠️ 平台仅支持 1 参数（已验证报错）→ 用 `ts_zscore(x, 126)` 替代

### 3.8 Essential — "什么本质？"
- **F18 "交易强度（按市值归一）"**：`vec_sum(boundary_transaction_usd_value) / market_cap`
  - 本质：机构活动相对公司规模的紧迫度
- **F19 "内部人本质信号"**：`directional_indicator * (total_top_buy_shares + total_top_sell_shares)`
  - 方向 × 交易量 = 内部人信念的确定性

---

## 4. 优先模拟清单（第一批 8 模拟）

| # | 表达式草案（FASTEXPR） | 信号逻辑 | 预期 |
|---|------------------------|---------|------|
| 1 | `rank(ts_sum(vec_sum(stable_boundary_trade_count_21d), 63))` | 持久性机构活动累积 | 强 |
| 2 | `rank(ts_delta(vec_sum(boundary_transaction_usd_value), 5))` | 资金流加速度 | 中 |
| 3 | `rank(vec_sum(stable_boundary_trade_count_21d) * vec_sum(boundary_transaction_usd_value))` | 持久×规模 | 强 |
| 4 | `rank(ts_sum(directional_indicator, 63))` | 内部人净方向动量 | 强 |
| 5 | `rank((total_top_buy_shares - total_top_sell_shares) / (1 + total_top_buy_shares + total_top_sell_shares))` | 高管净买卖强度 | 强 |
| 6 | `rank(ts_delta(directional_indicator, 5))` | 内部人转向 | 中 |
| 7 | `rank(ts_zscore(vec_sum(herfindahl_index_transactions), 126))` | 交易集中度异常 | 中 |
| 8 | `rank(vec_sum(top_weighted_transaction_number))` | conviction 交易活跃度 | 中 |

**模拟配置**：NONE 中性化 / decay 0 / 快速筛选（skill 标准），命中后套 × vol 范式 + INDUSTRY。

---

## 5. 实现注意事项

1. **VECTOR 归约**：fund_holdings_panel 字段必须 `vec_sum` 或 `vec_mean` 包裹后再运算
2. **ts_rank 不可用**：平台 ts_rank 仅 1 参数（实测报错），相对分位一律用 `ts_zscore` / `rank` 替代
3. **无方向限制**（fund_holdings_panel）：特征都是"活动强度"型，可能对动量/反转敏感度低；若 8 模拟无命中，考虑与有方向信号（如 `directional_indicator`、returns）混合
4. **稀疏性**：内部人字段 ts 窗口建议 ≥63 天；DEU 披露节奏稀疏，`ts_sum` 比 `ts_delta` 稳健
5. **64 算子预算**：上面所有表达式 <20 ops，给 ×vol 增强留足空间
6. **边界条件**：`/` 除零 → 统一 `/(1+x)` 防护

## 6. 关键待验证问题
- fund_holdings_panel 无方向活动信号在 DEU TOP500 是否有预测力？（学术上"机构关注度"有短期动量效应，待实测）
- insider `directional_indicator` 100% 覆盖但信号可能稀疏（多数日为 0）→ 截面 rank 是否会退化？
- 两个数据集的信号族（行为/资金流）能否绕过 model264 等撞过的 sub_universe 墙？

---

## 7. brain-datafield-exploration-general 6法探测实测结果（2026-08-10，14 模拟）

**探测配置**：NONE / decay 0 / P0Y0M / FASTEXPR / DEU D1 TOP500（universe=500）
**方法应用**：方法1 基础覆盖（raw 字段）→ longCount；方法2 非零覆盖（`!=0 ? 1:0`）→ longCount；方法3 更新频率（`ts_std_dev(x,22)!=0 ? 1:0`）→ longCount

### 7.1 fund_holdings_panel（批1，8 模拟）

| 字段 | 覆盖(方法1) | 非零(方法2) | Sharpe(非零版) | Fitness | sub_univ | 22d更新(方法3) |
|------|------------|------------|----------------|---------|----------|----------------|
| **boundary_transaction_usd_value** | 106/500=21.2% | 106/500=21.2% | **0.95** | 0.49 | **0.61 ✅ 通过(lim 0.43)** | **306/500=61.2%** |
| herfindahl_index_transactions | 302/500=60.4% | 302/500=60.4% | 0.78 | **0.98** | 0.53 ✅ | — |
| top_weighted_transaction_number | 153/500=30.6% | 153/500=30.6% | 0.80 | 0.65 | 0.06 | — |
| stable_boundary_trade_count_21d | 82/500=16.4% | 82/500=16.4% | 0.91 | 0.43 | 0.40(lim 0.43) | — |

### 7.2 insider_agg_matrix（批2，6 模拟）

| 字段 | 覆盖(方法1) | 非零(方法2) | Sharpe | Fitness | sub_univ | 22d更新(方法3) |
|------|------------|------------|--------|---------|----------|----------------|
| directional_indicator | 12/500=2.4% | 12/500=2.4% | 0.91 | 0.43 | 0.34(lim 0.43) | **60/500=12%** |
| total_top_buy - sell | 8/500=1.6% | 9/500=1.8% | 0.21 | 0.07 | 0.23 | — |
| (top buy-sell)!=0 | 9/500=1.8% | 9/500=1.8% | 0.76 | 0.35 | -0.21 | — |

### 7.3 关键结论（元数据 vs 实测的差异）

1. **boundary_transaction_usd_value = 唯一 sub_universe 通过的字段（0.61 vs limit 0.43）** 🎯
   - 当日覆盖仅 21.2%，但 **22 天窗口更新频率 61.2%** → 字段是"低频事件型"，必须用 `ts_sum/ts_decay` 窗口累积才能把覆盖拉到 60%+
   - 非零版 fitness 0.49 待提升；sharpe 0.95 是 DEU 探测中最高
2. **herfindahl_index_transactions**：覆盖 60.4% 最佳 + fitness 0.98 逼近门槛 + sub 0.53 通过；但 sharpe 0.78、2y≈0 → 需 × vol / 混合增强
3. **⚠️ directional_indicator 陷阱揭穿**：字段级 cov=1.0（平台元数据）≠ 非零覆盖 2.4%！DEU 内部人披露极稀疏（22 天窗口仅 12% 股票有变动）→ 截面 rank 退化风险极高，**降级为 C 档**
4. **stable_boundary 覆盖仅 16.4%**：21d 稳定边界交易在 DEU 太稀有，降级
5. **更新频率确认**：两数据集均为低频事件数据 → 所有特征必须包裹 `ts_sum(x, N≥22)` 平滑

### 7.4 修正后的优先模拟清单（第二批）

| # | 表达式 | 依据 |
|---|--------|------|
| 1 | `rank(ts_sum(vec_sum(boundary_transaction_usd_value), 22))` | sub 0.61 基础 + 窗口拉覆盖 |
| 2 | `rank(ts_sum(vec_sum(boundary_transaction_usd_value), 63))` | 更长窗口对比 |
| 3 | `rank(ts_sum(vec_sum(herfindahl_index_transactions), 22) / (1 + ts_sum(vec_sum(boundary_transaction_usd_value), 22)))` | 集中度/规模 比率 |
| 4 | `rank(ts_decay_linear(vec_sum(boundary_transaction_usd_value), 22, dense=true))` | 时间加权 |
| 5 | `rank(ts_sum(vec_sum(boundary_transaction_usd_value), 22) * vec_sum(herfindahl_index_transactions))` | 交互 |
| 6 | `rank(ts_sum(vec_sum(top_weighted_transaction_number), 63))` | 30.6% 覆盖 + fitness 0.92 |
