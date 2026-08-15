# 101 Formulaic Alphas 知识库（WorldQuant 官方论文总结）

来源：Zura Kakushadze, "101 Formulaic Alphas" (Dec 2015)，WorldQuant 生产级真实 alpha 公式。
PDF 原始文本：`reference/101_formulaic_alphas_raw.txt`

## 一、论文核心实证结论

1. **101 个 alpha 平均持仓期 0.6-6.4 天**（日频交易，turnover 0.16-1.60）
2. **平均两两相关性仅 15.9%**（中位 14.3%）——多样性的量化标杆
3. **收益与波动强相关**：ln(return) ≈ 0.76 × ln(volatility)（R²=0.73），即高波动 alpha 收益更高
4. **收益与 turnover 无显著相关**（t=-0.57）——**换手率不是 alpha 质量的代理指标**
5. **turnover 对 alpha 相关性无解释力**（R²=0.012）——低相关 alpha 组合不靠 turnover 区分
6. Sharpe 分布：中位 2.22，均值 2.27，Q1=1.93，最大 4.16（不含交易成本）

## 二、Alpha 构成要素（操作符字典）

| 操作符 | 含义 | 我的 BRAIN 等价 |
|---|---|---|
| rank(x) | 横截面排名 | rank(x) ✓ |
| delay(x,d) | d 天前的值 | ts_delay(x,d) |
| correlation(x,y,d) | 时序相关 | ts_corr(x,y,d) ✓ |
| covariance(x,y,d) | 时序协方差 | ts_covariance（无，用 ts_corr 替代） |
| scale(x,a) | 缩放使 sum(abs)=a | scale(x,a) ✓ |
| delta(x,d) | 今日-前d日 | ts_delta(x,d) ✓ |
| signedpower(x,a) | x^a 保号 | signed_power(x,a) ✓ |
| decay_linear(x,d) | 线性衰减加权均值 | ts_decay_linear（无；用 ts_mean 近似或 tail 加权） |
| indneutralize(x,g) | 组内去均值 | group_neutralize(x,g) ✓ |
| ts_min/ts_max(x,d) | 时序最值 | ts_min/ts_max ✓（可用 ts_min/max 或 ts_arg_min/max） |
| ts_argmax/argmin(x,d) | 最值出现天数 | ts_arg_max/ts_arg_min ✓ |
| ts_rank(x,d) | 时序排名 | ts_rank ✓ |
| sum/product(x,d) | 时序和/积 | ts_sum/ts_product ✓ |
| stddev(x,d) | 时序标准差 | ts_std_dev ✓ |
| min/max(x,d) | 时序最值 | ts_min/ts_max ✓ |
| adv{d} | 过去 d 天平均日成交额 | adv20/adv60/adv180（BRAIN 内置字段） |
| IndClass | 行业分类（GICS/BICS/NAICS/SIC） | industry/sector/subindustry ✓ |

## 三、101 个 alpha 按信号类型分类（可直接迁移的模板）

### A. 均值回归类（contrarian）
- **Alpha#4**: `-1 * Ts_Rank(rank(low), 9)` — 低价股时序排名反向（简单有效）
- **Alpha#12**: `sign(delta(volume,1)) * -1 * delta(close,1)` — 放量日价格反向
- **Alpha#33**: `rank(-1 * ((1 - (open/close))^1))` — 开盘-收盘反转
- **Alpha#42**: `rank(vwap - close) / rank(vwap + close)` — **delay-0 收盘反转**（经典）
- **Alpha#54**: `-1 * ((low-close)*(open^5)) / ((low-high)*(close^5))` — 收盘位置反转
- **Alpha#101**: `(close - open) / ((high - low) + 0.001)` — **日内走势延续**（收盘于高点则做多）

### B. 动量类（momentum）
- **Alpha#19**: `sign(close-delay(close,7) + delta(close,7)) * (1 + rank(1 + sum(returns,250)))` — 7日动量和250日动量
- **Alpha#46**: 20日动量斜率（delay20-close 对比）条件交易
- **Alpha#49/51**: 动量斜率阈值触发（0.1/0.05）

### C. 量价相关性类（volume-price）
- **Alpha#2**: `-1 * correlation(rank(delta(log(volume),2)), rank((close-open)/open), 6)` — 量价背离
- **Alpha#3**: `-1 * correlation(rank(open), rank(volume), 10)` — 开盘量价反向
- **Alpha#6**: `-1 * correlation(open, volume, 10)`
- **Alpha#13**: `-1 * rank(covariance(rank(close), rank(volume), 5))` — 价量协方差反向
- **Alpha#44**: `-1 * correlation(high, rank(volume), 5)` — 高点量价反向
- **Alpha#55**: `-1 * correlation(rank(stochastic位置), rank(volume), 6)` — 随机位置量价反向

### D. 波动类（volatility）
- **Alpha#18**: `-1 * rank(stddev(abs(close-open),5) + (close-open) + correlation(close,open,10))`
- **Alpha#22**: `-1 * (delta(correlation(high,volume,5),5) * rank(stddev(close,20)))` — 高波动+量价
- **Alpha#40**: `-1 * rank(stddev(high,10)) * correlation(high,volume,10)` — 高波动反向

### E. 开盘跳空类（gap）
- **Alpha#20**: `rank(open-delay(high,1)) * rank(open-delay(close,1)) * rank(open-delay(low,1))` — 开盘跳空三连
- **Alpha#28**: `scale(correlation(adv20,low,5) + (high+low)/2 - close)` — 低点量价+位置
- **Alpha#57**: `(close - vwap) / decay_linear(rank(ts_argmax(close,30)), 2)` — 收盘-vwap 位置

### F. 行业中性化类（indneutralize，最接近 BRAIN group_neutralize）
- **Alpha#48**: `indneutralize(corr(delta(close,1),delta(delay(close,1),1),250) * delta(close,1)/close, subindustry) / sum((delta(close,1)/delay(close,1))^2, 250)` — **行业中性化的日内动量**（高难度，含 250 日窗口）
- **Alpha#58/59/63/67/69/70/76/79/80/82/87/89/91/93/97**: 均以 `indneutralize(vwap/close/low/volume/adv, sector/industry)` 为内核
- **Alpha#100**: 双重行业中性化 + 量价位置组合

### G. 混合复杂类（多因子叠加）
- **Alpha#36**: `2.21*rank(corr(close-open, delay(volume,1), 15)) + 0.7*rank(open-close) + 0.73*rank(Ts_Rank(delay(-returns,6),5)) + rank(abs(corr(vwap,adv20,6))) + 0.6*rank((sum(close,200)/200-open)*(close-open))` — **多因子加权组合范式**（权重×rank 因子相加）
- **Alpha#71/73/76/77/82/87/88/92/96**: max/min 包裹两个 decay_linear 因子
- **Alpha#61-99**: 大量 `rank(A) < rank(B)` 布尔比较 × -1 的模式（条件信号）

## 四、关键操作符使用规律（迁移到 BRAIN 的要点）

### 1. 乘数常数在 rank 外的经典模式
```
Alpha#36: 2.21*rank(corr(...)) + 0.7*rank(...) + 0.73*rank(...) + rank(...) + 0.6*rank(...)
```
→ BRAIN 等价：`add(multiply(rank(ts_corr(ts_delta(close,1), ts_delay(volume,1), 15)), 2.21), ...)`
（注意 BRAIN 用户之前对 add/负号敏感，用 add/subtract 而非 `-x`）

### 2. 布尔条件模式
```
Alpha#46: (0.25 < slope) ? -1 : (slope < 0 ? 1 : -1*(close-delay(close,1)))
```
→ BRAIN 无三目运算符，用 `if_else(greater(slope, 0.25), -1, ...)` 或 trade_when 组合替代

### 3. 量价背离（vol-price divergence）是最强主题
- 10 个 alpha（#2,#3,#6,#13,#15,#16,#44,#55,#40,#22）以量价相关性/协方差为核心
- 方向几乎全是 **-1 × correlation(price, volume)**：价量同向=拥挤=反向
- BRAIN 直接用 `reverse(ts_corr(rank(close), rank(volume), 5))` 即可复刻

### 4. 行业中性化是复杂 alpha 的骨架
- 从 Alpha#48 到 #100，一半以上用到 indneutralize
- BRAIN 用 `group_neutralize(x, industry)` 完美等价
- 核心思想：**在行业内去均值后取 delta/相关**，捕捉行业内相对变化

### 5. decay_linear 是平滑利器（BRAIN 缺失，需替代）
- 线性衰减权重：d 天权重 d,d-1,...,1
- BRAIN 替代方案：
  - 近似：`ts_mean(x, d)`（等权，效果略差）
  - 或组合：`ts_delta` + 短窗 `ts_mean` 模拟衰减
  - 或用 `ts_decay_exp_window`（指数衰减，BRAIN 有该操作符）

### 6. adv 系列字段（BRAIN 内置）
- adv20/adv60/adv120/adv180 = 过去 d 天平均日成交额
- 论文大量使用 `volume/adv20`（成交量活跃度比）、`correlation(price, advN)`
- BRAIN 可直接用这些字段，无需自算

## 五、可直接迁移到 BRAIN 的高价值模板（按性价比排序）

### 性价比极高（简单、经典、已验证）
```python
# 1. 量价背离（Alpha#13 复刻）
reverse(rank(ts_covariance_approx(rank(close), rank(volume), 5)))  
# 用 ts_corr 替代：reverse(ts_corr(rank(close), rank(volume), 5))

# 2. 收盘反转（Alpha#42 复刻，delay-0 注意用 D0）
quantile(ts_backfill(vec_avg(vwap), 60)) 差异于 close → rank 差
# 等价：rank(vwap - close) / rank(vwap + close)

# 3. 低价时序反转（Alpha#4 复刻）
reverse(ts_rank(rank(low), 9))

# 4. 波动放量反向（Alpha#12 复刻）
multiply(sign(ts_delta(volume, 1)), reverse(ts_delta(close, 1)))

# 5. 日内位置反转（Alpha#101 复刻）
divide(ts_delta(close, 1), add(ts_delta(high,1) - ts_delta(low,1), 0.001))  # 近似
```

### 性价比高（行业中性化，BRAIN 完美支持）
```python
# 6. 行业中性化日内动量（Alpha#48 思想）
group_neutralize(multiply(ts_corr(ts_delta(close,1), ts_delta(ts_delay(close,1),1), 250), divide(ts_delta(close,1), close)), industry)

# 7. 行业中性化 vwap 量价（Alpha#58 思想）
reverse(ts_rank(ts_mean(ts_corr(group_neutralize(vwap, sector), volume, 4), 8), 6))

# 8. 多因子加权（Alpha#36 思想）
add(multiply(rank(ts_corr(ts_delta(close,1), ts_delay(volume,1), 15)), 2.21),
    multiply(rank(ts_delta(close,1)), -1))  # 权重×rank 范式
```

## 六、论文给我们的 3 个战略启示

1. **多样性是硬指标**：101 个 alpha 平均相关 15.9%。我们组 alpha 时目标相关性 <0.4 是合理的，但可以更激进——用不同信号族（量价/动量/情绪/机构/形态）天然低相关
2. **turnover 不是质量代理**：论文证实收益与换手无关。我们的 alpha 不应刻意控制 turnover 来"看起来好"，而应关注信号本身
3. **波动-收益正相关**：高波动 alpha 收益更高（slope 0.76）。IS_LADDER/2Y 检查失败可能部分因为波动不足——**适当引入高波动信号（如日反转、量价背离）可能同时提升收益**

## 七、与当前挖掘任务（GBR IS_LADDER 困境）的关联

当前 GBR 候选（mdl238 机构+质量-形态）sharpe 1.59 但 IS_LADDER(2Y) 0.68 不达标。
论文启示：
- **量价背离类信号**（reverse(ts_corr(rank(close), rank(volume), N))）在 GBR 未试过，且论文证明其低相关、高 Sharpe（中位 2.2）
- **行业中性化骨架**（group_neutralize + 行业内 delta）是论文复杂 alpha 的主流，可尝试组合进 GBR 候选提升 2Y
- **decay_linear 平滑**可替代 ts_mean 提升信号稳定性（2Y 可能受益）

---
*知识库生成时间：2026-08-07，来源 PDF 已归档 reference/101_formulaic_alphas_raw.txt*
