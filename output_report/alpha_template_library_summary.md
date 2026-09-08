# 社区 Alpha 模板库总结

> **数据来源**：`data/wqb.db` → `ledger_kv` → `region='KB'`
> **生成时间**：2026-09-08　**候选层 updated_at**：2026-08-31

## 1. ★ 已验证层 `template_kb` —— 跨区实证配方（10 个）

> 跨区域已验证配方模板化。骨架字段 SLOW/FAST/F 为占位；validated/failed 记录区域实证。明细证据在 registry_empirical win 层与 docs/experience/2026-08-22-full-campaign-history-retro.md。

> 库内 updated_at：2026-08-25　骨架中 `SLOW`/`FAST`/`F` 为占位符

| # | 名称 | 骨架 | 已验证（区域 / 实证） | 失败（区域 / 原因） |
|---|---|---|---|---|
| 1 | 慢×快跨周期混合 | `rank(add(multiply(w_s, rank(SLOW_FIELD)), multiply(w_f, rank(FAST_FIELD))))` | **KOR**：评级修正×SH，sh 1.77-1.83/2y 2.34-2.52<br>**EUR**：慢 MODEL×快 PV，Wj71Q12o ACTIVE<br>**IND**：mdl177 长窗负权重混合<br>**MEA**：EPS+Net 修正动量组合<br>**GBR**：other455×model264 | **KOR**：同周期慢信号互混全灭（LT） |
| 2 | 镜像反转翻案 | `subtract(0, rank(x)) 或 scale(-rank(x))` | **EUR**：fcf_to_price sh -1.9 → 镜像 1.91<br>**KOR**：pv106 wave34A 变化族镜像<br>**IND**：anl39 robust 破墙 | — |
| 3 | 修正广度去相关（破 PROD 墙） | `rank(raised_count_four_weeks / total_count) 双轴组合，去掉 revision 腿` | **MEA**：9qXoJge2 prod 0.716→0.6525 | **MEA**：保留 revision 腿的版本 prod 0.74+ |
| 4 | 镜像稀释破 PROD 墙 | `强腿 + 独立稀释腿（腿间相关≈0）` | **EUR**：FCF 镜像+gap 稀释 prod 0.90→0.68，IS 不降反升 | — |
| 5 | 长窗结构强 2Y | `rank(ts_rank(ts_backfill(F, 66), 250))` | **IND**：mdl177 三颗 ACTIVE sh 1.84-3.67 / 2y 2.2-3.6 | — |
| 6 | 多期限共识加权 | `add(multiply(rank(F_40d),0.33), add(multiply(rank(F_60d),0.34), multiply(rank(F_100d),0.33)))` | — | **KOR**：MSM 5d 组合族 fitness 0.99 / 2y 1.24 天花板（短周期单数据集边界） |
| 7 | 四向价值结构 | `ep_yield fy2 av_diff + fwdPE 反转 + fy1 水平 + delta66/22 双差分` | **GBR**：4 ACTIVE，sh 1.8 / margin 10.1bp | **KOR**：移植全灭 0.32-0.60（PREDSTARMINE-VALUE-DEAD） |
| 8 | 量价背离（101 最强主题） | `reverse(ts_corr(rank(price), rank(volume), 5~10))` | **GLB**：9qpQ0VQ2 相关主题 | — |
| 9 | 【负模板】单字段裸探针 | `rank(F) / ts_delta(F,n) 裸探针` | — | **KOR**：10+ 数据集首探 max|sh| 0.2-0.52 |
| 10 | 【负模板】稀疏事件流 | `——（须先 ts_backfill + trade_when 门控再进表达式）` | — | **KOR**：论坛/行为/AI equity 三族 CW 0.85-1.0<br>**IND**：news29 / fundamental1 governance |

> **负模板（反模式）是重要资产**：记录已被本工作区证伪的方向。
> 取用前先比对，避免在已知死路上重复消耗回测槽位。

## 2. 候选层 `community_tpl_kb` —— 社区论坛馈赠（141 个 / 19 大类）

### 2.1 来源与可信度

| 项 | 值 |
|---|---|
| 原始出处 | 论坛社区帖《【Community Leader -因子构造】Alpha 模板库——来自社区的馈赠》 |
| 增量来源 | 《Alpha模板手册·社区模板库篇（续集）》（`alpha模板.docx`，2026-08-31 合并 +10 个模板与幽灵算子警示表） |
| 人读全文 | `docs/reference/community_tpl_library_sequel.md` |
| 验证状态 | **全部 `candidate_unverified`** —— 未经本工作区战役实证 |
| 晋升协议 | 回测后回写 `validated`/`failed`；跨区双验证（或 1 区强证据）后晋升入 `template_kb` |

```
论坛社区帖《【Community Leader -因子构造】Alpha 模板库——来自社区的馈赠》（用户上传 docx 提炼）；2026-08-31 合并《Alpha模板手册·社区模板库篇（续集）》（用户上传 alpha模板.docx）增量：新增 10 个模板（含 2 个附加模板）+ ghost_operator_advisory 幽灵算子警示表；人读全文见 docs/reference/community_tpl_library_sequel.md
```

### 2.2 分类分布

| # | 分类 | 模板数 | 占比 |
|---|---|---:|---:|
| 1 | 实战表达式模板 | 29 | 20.6% |
| 2 | 量价类模板 | 13 | 9.2% |
| 3 | 基础结构模板 | 10 | 7.1% |
| 4 | 信号处理模板 | 9 | 6.4% |
| 5 | 情绪/新闻类模板 | 8 | 5.7% |
| 6 | 高级统计模板 | 8 | 5.7% |
| 7 | 条件交易模板 | 7 | 5.0% |
| 8 | 复合多因子模板 | 7 | 5.0% |
| 9 | 数据预处理模板 | 7 | 5.0% |
| 10 | 期权类模板 | 6 | 4.3% |
| 11 | 分析师类模板 | 6 | 4.3% |
| 12 | 中性化技术模板 | 5 | 3.5% |
| 13 | 回填与覆盖模板 | 5 | 3.5% |
| 14 | 百分位与分位数模板 | 5 | 3.5% |
| 15 | 组合提取模板 | 4 | 2.8% |
| 16 | 社区验证过的算子级模板 | 4 | 2.8% |
| 17 | 事件驱动模板 | 3 | 2.1% |
| 18 | Turnover 控制模板 | 3 | 2.1% |
| 19 | 附加模板 | 2 | 1.4% |

### 2.3 经济角色分布

| 角色 | 模板数 | 占比 | 含义 |
|---|---:|---:|---|
| `transform` | 80 | 56.7% | 仅改变分布，不改变信息内容 |
| `residual` | 27 | 19.1% | 剥离市值分位 + 行业 |
| `gating` | 17 | 12.1% | 财报事件发生日才交易 |
| `combination` | 17 | 12.1% | 利润 / 规模比率 |

<details><summary>经济角色分类法（库内定义，点开）</summary>

```json
{
  "added_at": "2026-09-08",
  "why": "原 category 是**结构**分类（基础结构/量价/情绪/期权…），GEM 按 category 检索骨架时拿到的是「模板长什么样」而不是「模板在经济上做了什么」，因此产出高度偏向 transform 类。2026-09-08 实证：CHN news_sentiment_enriched 8 条、market_news_sent 8 条、ASI oth36 7 条，几乎全是同一字段的不同包裹 —— 方向一致、强度相当、互相关极高，因为它们本来就是同一条信息。",
  "roles": {
    "residual": "**减法**：原始信号 − 已被市场定价/已被其他变量解释的成分 = 残差。残差才是新信息。这是唯一能凭空创造正交性的一类。",
    "gating": "**条件**：不改变信号本身，改变「何时持有」。是换手控制与事件条件性的唯一正解。",
    "combination": "**组合**：两个及以上不同信息源的交互（乘/差/相关）。有增量但受 D2『禁止同信号加权调参』约束。",
    "transform": "**包裹**：rank/zscore/winsorize/backfill 等。只改变分布，**不增加信息**。一个字段包 100 种壳，还是那一个 alpha。"
  },
  "counts": {
    "transform": 80,
    "residual": 27,
    "gating": 17,
    "combination": 17
  },
  "key_templates_by_role": {
    "residual 最有代表性": [
      "TPL-202 情绪剥离成交量残差",
      "TPL-402 分析师剥离双动量",
      "TPL-1658 盈利剥离预期",
      "TPL-104 价格剥离趋势",
      "TPL-109 剥离市场共同成分"
    ],
    "gating 最有代表性": [
      "TPL-1001 days_from_last_change 事件门控/动态衰减",
      "TPL-1201 ts_target_tvr_hump 目标换手（已验证算子）",
      "TPL-601/602/603 trade_when 三件套"
    ]
  },
  "EMPIRICAL_CORRECTION_20260908": {
    "status": "上条 generation_rule『residual≥2』**已被历史数据否定，勿采用**",
    "what_i_claimed": "读模板库后推断『减法(residual)才产生新信息，应优先』",
    "what_data_says": "1496 条历史回测中 margin 有效的 844 条，按经济作用分桶的**双达标率**（|sharpe|>=1.58 且 |margin|>5bp，即 Sharpe 与单位换手收益同时过线）：combination 14.2%（n=332）> transform 9.5%（n=284）> residual_ts 6.8%（n=59）> residual_xs 6.7%（n=15）> residual_xf 4.2%（n=144）> gating 0%（n=10）。**实际排序与推断相反：combination 最优，residual_xf 最差。**",
    "why_i_was_wrong": "① 数据污染：1496 条里 652 条（43.6%）margin 为 NULL，初版把 NULL 当 0 计入中位数；② 极端值：residual_ts 的均值 margin 119.53bp 而中位数 0.00bp，均值被少数极端值带偏；③ 方法论错误：把『读文档读出的机制解释』当成了『测出来的证据』。与同日上午的成本假象是同型错误——都是先有解释后有验证。",
    "robust_finding": "唯一稳健的结论是骨架层而非角色层：**divide 比率型 `divide(rank(A), add(1, rank(B)))` 双达标率 31.4%（n=35），是 add 加权和型 `add(w1*A, w2*B)` 13.9%（n=201）的 2.3 倍**，而使用量只有后者 1/6，严重欠用。注意 divide 的 |S| 中位数反而更低（0.80 vs 1.21）——它是『要么很好要么不行』的分布，对提交更有用（提交只看能否过线，不看中位数）。",
    "caveat": "分类器是正则代理不是语义解析：residual_xf 桶靠 `subtract(` 匹配，会把 `subtract(1, rank(x))` 这种纯取反也算进去，该桶结论污染严重。所有角色层结论都应视为弱证据。"
  }
}
```
</details>

### 2.4 占位符约定

原帖尖括号 `<field/>` 风格 ≡ 本库 `{field}` 花括号风格，两者等价。

| 占位符 | 含义 | 取值 |
|---|---|---|
| `{field} / {data}` | 数据字段 | 基本面、量价、情绪等字段 |
| `{alpha}` | 已有因子信号 | 任意有效表达式 |
| `{ts_op}` | 时序算子 | ts_rank, ts_zscore, ts_delta, ts_ir, ts_mean, ts_std_dev |
| `{group_op}` | 分组算子 | group_rank, group_zscore, group_neutralize, group_mean |
| `{vec_op}` | 向量聚合算子 | vec_avg, vec_sum, vec_max, vec_min, vec_stddev, vec_count |
| `{d} / {d1} / {d2}` | 时间窗口（天） | 5, 10, 22, 66, 126, 252, 504 |
| `{group}` | 分组字段 | industry, sector, subindustry, market, sta1_top3000c20 |
| `{range}` | bucket 分组区间 | “0.1,1,0.1”, “0,1,0.1” |
| `{threshold}` | 阈值 | 视具体模板而定 |

### 2.5 ⚠ 幽灵算子警示（取骨架前必查）

> **规则**：凡骨架含下列算子的模板，入批前必须替换为等价算子或先经 validate_expressions 实测，否则整批 ERROR/CANCELLED

| 幽灵算子 | 状态 | 等价替换 | 受影响模板 |
|---|---|---|---|
| `sigmoid` | ghost | multiply(x, inverse(add(1, abs(x)))) 即 x/(1+\|x\|)，或省去压缩层用 zscore/rank | `TPL-203`, `TPL-204`, `TPL-205`, `TPL-208`, `TPL-303`, `TPL-802`, `TPL-1635` |
| `ts_entropy` | ghost | 无精确等价；代理 ts_std_dev/ts_kurtosis 度量不确定性（需实测） | `TPL-1608`, `TPL-1641`, `TPL-1642`, `TPL-1643` |
| `ts_skewness` | ghost | 候选 ts_moment(x, d, k=3)（ts_moment 亦未入目录，需实测） | `TPL-1607` |
| `ts_percentage` | ghost | ts_quantile(x, d, p)（已验证） | `TPL-1501`, `TPL-1637`, `TPL-1653` |
| `ts_median` | ghost | ts_quantile(x, d, 0.5)（已验证） | `TPL-1504` |
| `ts_min` | ghost | TPL-1601 替代公式；见 docs/reference/community_tpl_library_sequel.md §十八 | `TPL-108`, `TPL-910` |
| `ts_max` | ghost | ts_delay(x, ts_arg_max(x, d))（=TPL-1625）或 TPL-1601 公式 | `TPL-108`, `TPL-910`, `TPL-1625` |
| `ts_decay_exp_window` | ghost | ts_decay_linear(x, d)（语义近似，已验证） | `TPL-107`, `TPL-206`, `TPL-1638` |
| `ts_min_max_cps` | ghost | 无等价（展开依赖 ts_min/ts_max，慎用） | `TPL-910` |
| `group_normalize` | ghost | alpha / group_sum(abs(alpha), group)（=TPL-1603，已验证） | `TPL-1110` |

### 2.6 分类详解（141 个全清单）

#### 实战表达式模板（29 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-1601` | ts_max/ts_min 替代公式 | `` |  | `transform` |
| `TPL-1602` | 线性衰减权重公式（新增） | `weight = {d} + ts_step(0); ts_sum({data} * weight, {d}) / ts_sum(weight, {d})` | 等效于 ts_decay_linear 的手写实现 | `transform` |
| `TPL-1603` | 组归一化公式（新增） | `{data} / group_sum(abs({data}), {group})` | 等效于 group_normalize | `transform` |
| `TPL-1607` | 偏度因子 | `-group_rank(ts_skewness(returns, {d}), {group})` | 负偏度股票往往表现更好 | `transform` |
| `TPL-1608` | 熵信号 | `ts_zscore({field}, {d1}) * ts_entropy({field}, {d2})` | 标准化与不确定性度量组合 | `transform` |
| `TPL-1609` | 分析师动量短长差 | `log(ts_mean(anl4_{data}_{stats}, {d_short})) - log(ts_mean(anl4_{data}_{stats}, {d_long}))` |  | `residual` |
| `TPL-1623` | 老虎哥回归 | `group_rank(ts_regression(ts_zscore({field1}, {d}), ts_zscore(vec_sum({field2}), {d}), {d}), densify(sector))` |  | `residual` |
| `TPL-1625` | 延迟最大值位置（ts_max 等效） | `ts_max({field}, {d}) ≡ ts_delay({field}, ts_arg_max({field}, {d}))` | ts_max 幽灵时的等效写法 | `transform` |
| `TPL-1634` | ts_moment 高阶矩 k 值 | `ts_moment({field}, {d}, k={k})` |  | `transform` |
| `TPL-1635` | 龙头股因子增强 | `sigmoid(rank(star_pm_global_rank))` |  | `transform` |
| `TPL-1636` | purify 数据清洗嵌套 | `group_rank(ts_rank(purify({field}), {d}), {group})` |  | `transform` |
| `TPL-1637` | 理想振幅因子（新增） | `amplitude = (high - low)/close; ideal_amp = ts_percentage(amplitude, {d}, percentage=0.5); group_rank(amplitude - ideal_amp, {group})` | 实际振幅相对理想中位振幅的偏离 | `transform` |
| `TPL-1638` | MACD 风格乖离率（新增） | `ema_short = ts_decay_exp_window({field}, {d_short}, 0.9); ema_long = ts_decay_exp_window({field}, {d_long}, 0.9); dif = ema_short - ema_long; ts_zscore(dif, {d_…` | 快慢指数衰减均线差值的标准化信号 | `transform` |
| `TPL-1639` | 收益率条件筛选反转（新增） | `high_ret = ts_rank(returns, {d1}) > 0.8; low_ret = ts_rank(returns, {d1}) < 0.2; if_else(high_ret, -returns, if_else(low_ret, returns, 0))` | 极端上涨做空、极端下跌做多、中间不持仓的反转策略 | `transform` |
| `TPL-1640` | 三阶嵌套优化版（新增） | `{group_op}({ts_op1}({ts_op2}({field}, {d1}), {d2}), {group})` |  | `transform` |
| `TPL-1641` | ts_entropy 信号检测 | `ts_entropy({field}, {d})` | 衡量时序数据不确定性，高熵值表示更多随机性 | `transform` |
| `TPL-1642` | 熵+ZScore 组合 | `ts_zscore({field}, {d}) * ts_entropy({field}, {d})` |  | `combination` |
| `TPL-1643` | ts_ir+ts_entropy 信号组合（本轮已补全） | `signal = ts_ir({field}, {d}) + ts_entropy({field}, {d}); group_rank(signal, {group})` |  | `combination` |
| `TPL-1644` | trade_when 市值过滤（新增） | `trade_when(rank(cap) > {threshold}, {alpha}, -1)` | 仅交易大市值股票，降低 prod corr | `gating` |
| `TPL-1645` | trade_when 盈利过滤（新增） | `trade_when(eps > {threshold} * est_eps, group_rank((eps - est_eps)/est_eps, industry), -1)` | 只交易盈利超预期股票 | `gating` |
| `TPL-1648` | bucket 市值分组中性化 | `my_group2 = bucket(rank(cap), range='{range}'); group_neutralize({alpha}, my_group2)` |  | `residual` |
| `TPL-1649` | group_zscore 时序组合 | `group_zscore(ts_ir({field}, {d}), {group})` |  | `transform` |
| `TPL-1650` | scale+rank+ts 组合 | `scale(rank(ts_zscore({field}, {d})))` |  | `transform` |
| `TPL-1653` | 量小换手率（新增） | `turnover = volume/sharesout; low_turnover = ts_percentage(turnover, {d}, percentage=0.2); group_rank(turnover < low_turnover, {group})` | 换手率低于历史 20 分位时的选股信号 | `transform` |
| `TPL-1654` | 隔夜收益因子（新增） | `overnight_ret = open/ts_delay(close, 1) - 1; group_rank(ts_mean(overnight_ret, {d}), {group})` | 隔夜收益均值分组排名 | `transform` |
| `TPL-1655` | sta1 分组三因子（新增） | `a = rank(group_rank(ts_rank(ts_backfill({field1}, {d1}), {d2}), sta1_top3000c20)); trade_when(rank(a) > {threshold}, -zscore(ts_zscore({field2}, {d3})) * a, {ex…` | sta1 分组下的三因子复合条件交易 | `gating` |
| `TPL-1656` | macro 泛化 | `group_rank(ts_delta(ts_zscore({macro_field}, {d1}), {d2}), country)` | 基于 Labs 分析 macro 数据的泛化模板 | `residual` |
| `TPL-1657` | ASI broker | `signal = group_rank(ts_rank({broker_field}, {d}), market); trade_when(volume > adv20, signal, -1)` | ASI 区域 broker 因子 | `combination` |
| `TPL-1658` | Earnings 超预期 | `surprise = (actual_eps - est_eps) / abs(est_eps); group_rank(ts_zscore(surprise, {d}), industry)` | 盈利超预期因子 | `residual` |

#### 量价类模板（13 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-101` | 换手率反转 | `-{ts_op}(volume/sharesout, {d})` | 高换手率股票未来收益倾向走低 | `transform` |
| `TPL-102` | 量稳换手率 (STR) | `-ts_std_dev(volume/sharesout, {d1})/ts_mean(volume/sharesout, {d2}) 优化版：外层再加 -group_neutralize(..., bucket(rank(cap), range="0.1,1,0.1"))` | 换手率波动/均值，衡量换手率稳定性 | `combination` |
| `TPL-103` | 价格反转 | `-{ts_op}({price_field}, {d})` | 短期价格/收益反转因子（含日内、隔夜变体） | `transform` |
| `TPL-104` | 价格乖离率 | `-(close - ts_mean(close, {d}))/ts_mean(close, {d})` | 价格偏离均线的幅度，偏离越大越倾向回归 | `residual` |
| `TPL-105` | 量价相关性 | `-ts_corr({price_field}, {volume_field}, {d})` | 量价相关性高时未来收益走低 | `combination` |
| `TPL-106` | 跳跃因子 | `-group_neutralize(ts_mean((close/open-1) - log(close/open), {d}), bucket(rank(cap), range="0.1,1,0.1")) 带成交量增强版：信号再乘以 ts_rank(volume, 5)` | 捕捉开盘跳空中的反转信号 | `combination` |
| `TPL-107` | 指数衰减动量 | `-ts_decay_exp_window({field}, {d}, factor={f})` | 指数衰减权重计算动量，越近数据权重越大 | `transform` |
| `TPL-108` | 成交量周期函数 (VOC) | `m_minus = ts_mean(volume, {d_long}) - ts_mean(volume, {d_short}); delta = (ts_max(m_minus, {d_short}) - m_minus)/(ts_max(m_minus, {d_short}) - ts_min(m_minus, {…` | 基于成交量均值差和周期位置构造的量价周期信号 | `combination` |
| `TPL-109` | 市场相关性因子 | `mkt_ret = group_mean(returns, 1, market); pt = ts_corr(returns, mkt_ret, {d}); rank(1/(2(1-pt)))` | 衡量个股与市场相关性，低相关性股票获得更高排名 | `residual` |
| `TPL-110` | 成交量趋势 | `ts_decay_linear(volume/ts_sum(volume, {d_long}), {d_short})` | 成交量占长期总量比例的线性衰减趋势 | `transform` |
| `TPL-111` | VWAP 收益相关 | `returns > -{threshold} ? ts_ir(ts_corr(ts_returns(vwap, 1), ts_delay(group_neutralize({field}, market), {d1}), {d2}), {d2}) : -1` | VWAP 收益与延迟中性化信号的相关性 | `combination` |
| `TPL-112` | 动量因子创建 | `ts_sum(winsorize(ts_backfill({data}, {day}), std=4.0), {n}*21) - ts_sum(winsorize(ts_backfill({data}, {day}), std=4.0), {m}*21)` | 长期动量减去短期动量，回填并去极值处理 | `transform` |
| `TPL-113` | 线性衰减排名 | `-ts_rank(ts_decay_linear({field}, {d1}), {d2})` | 对线性衰减后的信号做时序排名后取负 | `transform` |

#### 基础结构模板（10 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-001` | 基本面时序排名 | `{ts_op}({field}, {d})，外层做分组截面比较` | 将基本面数据的时序表现在行业内/行业间做截面比较 | `transform` |
| `TPL-002` | 利润/规模比率 | `{ts_op}({profit_field}/{size_field}, {d})` |  | `transform` |
| `TPL-003` | 向量数据处理（VECTOR 字段必用） | `{ts_op}({vec_op}({vector_field}), {d})` | 将 VECTOR 类型（如分析师一致预期）数据先聚合为标量再做时序处理 | `transform` |
| `TPL-004` | 双重中性化 | `a = ts_zscore({field}, 252); a1 = group_neutralize(a, bucket(rank(cap), range="0.1,1,0.1")); group_neutralize(a1, {group})` | 先市值分组中性化、再行业分组中性化，消除规模与行业暴露 | `residual` |
| `TPL-005` | 回归中性化 | `a = {ts_op}({field}, {d}); a1 = group_neutralize(a, bucket(rank(cap), range="{range}")); a2 = group_neutralize(a1, {group}); b = ts_zscore(cap, {d}); b1 = group…` | 通过回归方法剥离市值因子暴露，比单纯分组中性化更精细 | `residual` |
| `TPL-006` | 基本面动量 | `log(ts_mean({field}, {d_short})) - log(ts_mean({field}, {d_long}))` |  | `residual` |
| `TPL-007` | 财报事件驱动 | `event = ts_delta({fundamental_field}, -1); if_else(event != 0, {alpha}, nan) 扩展版：change = if_else(days_from_last_change() == {d}, ts_delta(close, {d}), nan)` | 在财报数据发生变化的时点触发 Alpha 信号 | `gating` |
| `TPL-008` | 标准化回填 | `{ts_op}(winsorize(ts_backfill({field}, {d_backfill}), std={std}), {d})` | 对低频数据做回填、去极值后再做时序标准化 | `transform` |
| `TPL-009` | 信号质量分组 | `signal = {ts_op}({field}, {d}); credit_quality = bucket(rank(ts_delay(signal, 1), rate=0), range="{range}"); group_neutralize({decay_op}(signal, k={k}), credit_…` | 根据信号质量分组后进行中性化处理 | `gating` |
| `TPL-010` | 复合分组中性化 | `group_neutralize({alpha}, densify({group1})*1000 + densify({group2}))` | 用复合分组（行业+国家/交易所）联合中性化 | `residual` |

#### 信号处理模板（9 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-1101` | 黄金比例幂变换 | `signed_power({alpha}, 0.618)；其他幂次：0.5（平方根）、2（平方增强）` |  | `transform` |
| `TPL-1102` | 尾部截断 | `right_tail({alpha}, minimum={min})；左尾版：left_tail({alpha}, maximum={max})` |  | `transform` |
| `TPL-1103` | Clamp 边界限制 | `clamp({alpha}, lower={low}, upper={high})` |  | `transform` |
| `TPL-1104` | 分数映射 | `fraction({alpha})，将连续变量映射到分布内的相对位置` |  | `transform` |
| `TPL-1105` | NaN 外推 | `nan_out({field}, lower={low}, upper={high})，将超范围值替换为 NaN` |  | `transform` |
| `TPL-1106` | Purify 数据清洗 | `purify({field})，自动化清洗异常值和噪声` |  | `transform` |
| `TPL-1107` | 条件保留 | `keep({field}, {condition}, period={d})` |  | `transform` |
| `TPL-1109` | Truncate 截断 | `truncate({alpha}, maxPercent={percent})；percent∈{0.01, 0.05}` |  | `transform` |
| `TPL-1110` | 组合 Normalize | `group_normalize({alpha}, {group}) alpha / group_sum(abs(alpha), group)` |  | `transform` |

#### 情绪/新闻类模板（8 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-201` | 情绪差值 | `{ts_op}(rank(ts_backfill({positive_sentiment}, {d})) - rank(ts_backfill({negative_sentiment}, {d})), {d2})` | 正面情绪排名减负面情绪排名，得到净情绪信号 | `combination` |
| `TPL-202` | 新闻情绪回归残差 | `sentiment = ts_backfill(ts_delay({vec_op}({sentiment_field}), 1), {d1}); vhat = ts_regression(volume, sentiment, {d2}); ehat = -ts_regression(returns, vhat, {d3…` | 先回归成交量对情绪的依赖，再用残差构造因子 | `residual` |
| `TPL-203` | 社交媒体情绪 | `rank({vec_op}(scl12_alltype_buzzvec) * scl12_sentiment) 条件版：sent_vol = vec_sum(scl12_alltype_buzzvec); trade_when(rank(sent_vol) > 0.95, -zscore(scl12_buzz)*sen…` |  | `combination` |
| `TPL-204` | 条件情绪过滤 | `group_rank(sigmoid(if_else(ts_zscore({sentiment_field}, {d}) > {threshold}, ts_zscore({sentiment_field}, {d}), 0)), {group})` | 只在情绪 Z-score 超阈值时保留信号，否则置 0 | `transform` |
| `TPL-205` | 情绪+波动率复合 | `log(1 + sigmoid(ts_zscore({sentiment_field}, {d1})) * sigmoid(ts_zscore({volatility_field}, {d2})))` | 情绪与波动率双 Z-score 经 sigmoid 压缩后复合相乘 | `combination` |
| `TPL-206` | 指数衰减情绪 | `ts_decay_exp_window(vec_avg({sentiment_field}), {d}, {factor}) 双来源组合示例：ts_decay_exp_window(vec_avg(mws85_sentiment), 10, 0.9) + ts_decay_exp_window(vec_avg(nws1…` |  | `combination` |
| `TPL-207` | 新闻结果排名 | `percent = ts_rank(vec_stddev({news_field}), {d1}); -ts_rank(ts_decay_linear(percent, {d2}), {d2})` | 对新闻结果离散度做排名，再线性衰减后取负 | `transform` |
| `TPL-208` | 分组行业提取情绪 | `scale(group_extra(ts_sum(sigmoid(ts_backfill({data}, {d1})), {d2}) - ts_sum(sigmoid(ts_backfill({data}, {d1})), {d2}), 0.5, densify(industry)))` | 从行业分组中提取情绪/基本面信号并标准化 | `transform` |

#### 高级统计模板（8 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-901` | 高阶矩（ts_moment） | `{ts_op}({group_op}(ts_moment({field}, {d}, k={k}), {group}))` |  | `transform` |
| `TPL-904` | 三元相关（新增） | `group_rank(ts_triple_corr({field1}, {field2}, {field3}, {d}), {group})` |  | `transform` |
| `TPL-905` | Theil-Sen 回归（新增） | `group_rank(ts_theilsen({field1}, {field2}, {d}), {group})` | 比普通回归更鲁棒；X 可用 ts_step(1) | `transform` |
| `TPL-906` | 多项式回归残差（新增） | `ts_poly_regression({field1}, {field2}, {d}, k={k})` |  | `transform` |
| `TPL-907` | 向量中性化（新增） | `ts_vector_neut({alpha}, {risk_factor}, {d})（窗口不宜过长，计算慢） 分组版：group_vector_neut({alpha}, {risk_factor}, {group})` |  | `residual` |
| `TPL-908` | 加权衰减（新增） | `group_neutralize(ts_weighted_decay({alpha}, k={k}), {group})` |  | `residual` |
| `TPL-909` | 回归斜率 | `ts_regression(ts_zscore({field}, {d}), ts_step(1), {d}, rettype=2)` | rettype=2 返回斜率，用于检测趋势 | `residual` |
| `TPL-910` | 最小最大压缩 | `ts_min_max_cps({field}, {d}, f={f}) x - f * (ts_min(x, d) + ts_max(x, d))` |  | `transform` |

#### 条件交易模板（7 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-601` | 流动性过滤 | `trade_when(volume > adv20 * {threshold}, {alpha}, -1)` |  | `gating` |
| `TPL-602` | 波动率过滤 | `trade_when(ts_rank(ts_std_dev(returns, {d1}), {d2}) < {threshold}, {alpha}, -1)` |  | `gating` |
| `TPL-603` | 极端收益过滤 | `trade_when(abs(returns) < {entry}, {alpha}, abs(returns) > {exit})` |  | `gating` |
| `TPL-604` | 市值过滤 | `trade_when(rank(cap) > {threshold}, {alpha}, -1)` |  | `gating` |
| `TPL-605` | 触发条件交易 | `triggerTradeexp = (ts_arg_max(volume, {d}) < 1) && (volume > ts_sum(volume, {d})/{n}); triggerExitexp = -1; trade_when(triggerTradeexp, {alpha}, triggerExitexp)…` |  | `gating` |
| `TPL-606` | 组合条件交易 | `my_group2 = bucket(rank(cap), range="0,1,0.1"); trade_when(volume > adv20, group_neutralize({alpha}, my_group2), -1)` |  | `residual` |
| `TPL-607` | 条件排名交易 | `a = {ts_op}({field}, {d}); trade_when(rank(a) > {threshold}, -zscore({field2})*a, -rank(a))` |  | `gating` |

#### 复合多因子模板（7 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-701` | 三因子乘积（本轮已补全） | `my_group = market; rank(group_rank(ts_decay_linear(volume/ts_sum(volume, 252), 10), my_group) * group_rank(ts_rank(vec_avg({fundamental}), {d}), my_group) * gro…` |  | `combination` |
| `TPL-702` | 波动率条件反转（新增） | `vol = ts_std_dev({ret_field}, {d}); vol_mean = group_mean(vol, 1, market); flip_ret = if_else(vol < vol_mean, -{ret_field}, {ret_field}); -ts_mean(flip_ret, {d}…` | 低波动做反转、高波动做动量的自适应切换 | `transform` |
| `TPL-703` | 恐惧指标组合（新增） | `fear = ts_mean(abs(returns - group_mean(returns, 1, market)) / (abs(returns) + abs(group_mean(returns, 1, market)) + 0.1), {d}); -group_neutralize(fear * {signa…` |  | `residual` |
| `TPL-704` | 债务杠杆相关性（新增） | `group_neutralize(ts_zscore({leverage_field}, {d1}) * ts_corr({leverage_field}, returns, {d2}), sector)` |  | `residual` |
| `TPL-705` | 模型数据信号（新增） | `简单版：-{model_field}（如 mdl175_01dtsv、mdl175_01icc） 排名版：rank(group_rank(ts_rank(ts_backfill({model_field}, 5), 5), sta1_top3000c20))` |  | `transform` |
| `TPL-706` | 回归 zscore 模板（新增） | `ts_regression(ts_zscore({field1}, {d}), ts_zscore({field2}, {d}), {d})` |  | `transform` |
| `TPL-707` | 分组 Delta | `group_neutralize(ts_delta({field}, {d}), sector)` |  | `residual` |

#### 数据预处理模板（7 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-801` | Winsorize 截断 | `winsorize({field}, std={std})；std∈{3, 4, 5}` |  | `transform` |
| `TPL-802` | Sigmoid 归一化 | `sigmoid({ts_op}({field}, {d}))；d∈{22, 66, 252}` |  | `transform` |
| `TPL-803` | 数据回填 | `ts_backfill({field}, {d})；d∈{115, 120, 180, 252}` |  | `transform` |
| `TPL-804` | 条件替换 | `if_else(is_not_nan({field}), {field}, {alternative})` |  | `transform` |
| `TPL-805` | 极端值替换 | `tail(tail({field}, lower={low}, upper={high}, newval={low}), lower=-{high}, upper=-{low}, newval=-{low})` |  | `transform` |
| `TPL-806` | 组合预处理 | `{ts_op}(winsorize(ts_backfill({field}, {d_backfill}), std={std}), {d})` |  | `transform` |
| `TPL-807` | ts_min/ts_max 替代 | `ts_backfill(if_else(ts_arg_min({field}, {d}) == 0, {field}, nan), 120)` | 当 ts_min/ts_max 不可用时的替代方案 | `transform` |

#### 期权类模板（6 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-301` | 期权希腊字母差值 | `{group_op}(({put_greek} - {call_greek}), {group})` | 反映期权市场多空力量对比 | `combination` |
| `TPL-302` | 期权价格信号 | `group_rank({ts_op}({vec_op}({option_price_field})/close, {d}), {group})` | 期权价格相对正股价格的比率信号，分组排名 | `combination` |
| `TPL-303` | 期权波动率信号 | `sigmoid({ts_op}({opt_high} - {opt_low}, {d}))` | 期权高低价差的波动性信号，经 sigmoid 压缩 | `combination` |
| `TPL-304` | 隐含波动率比率 | `{ts_op}(implied_volatilitycall{tenor}/parkinsonvolatility, {d})` |  | `transform` |
| `TPL-305` | Put-Call 成交量比 | `{ts_op}(pcrvol{tenor}, {d})` |  | `transform` |
| `TPL-306` | 期权盈亏平衡点 | `group_rank(ts_zscore({breakeven_field}/close, {d}), {group})` |  | `transform` |

#### 分析师类模板（6 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-401` | 分析师预期变化 | `{vec_op}(tail(tail({analyst_change_field}, lower={low}, upper={high}, newval={low}), lower=-{high}, upper=-{low}, newval=-{low}))` |  | `transform` |
| `TPL-402` | 剥离动量的分析师因子 | `afr = {vec_op}({analyst_field}); short_mom = ts_mean(returns - group_mean(returns, 1, market), {d_short}); long_mom = ts_delay(ts_mean(returns - group_mean(retu…` | 对短期/长期超额动量双重回归中性化后的分析师因子 | `residual` |
| `TPL-403` | 分析师覆盖度过滤（新增） | `coverage_filter = ts_sum(vec_count({analyst_field}), {d}) > {min_count}; if_else(coverage_filter, {alpha}, nan)` | 只有分析师覆盖达到一定数量才启用信号，过滤覆盖不足的股票 | `transform` |
| `TPL-404` | 老虎哥回归模板（新增） | `group_rank(ts_regression(ts_zscore({field1}, {d1}), ts_zscore(vec_sum({field2}), {d2}), {d3}), densify(sector))` | 两个字段做时序回归后按行业密度分组排名 | `transform` |
| `TPL-406` | 三因子组合模板（新增，即 TPL-701 完整原文） | `my_group = market; rank(group_rank(ts_decay_linear(volume/ts_sum(volume, 252), 10), my_group) * group_rank(ts_rank(vec_avg({fundamental}), {d}), my_group) * gro…` | 成交量趋势、基本面时序排名与短期反转三因子乘积组合 | `transform` |
| `TPL-407` | 分析师 FCF 比率（新增） | `ts_rank(vec_avg({fcf_field}) / vec_avg({profit_field}), {d})` | 自由现金流与盈利预期的比率信号 | `transform` |

#### 中性化技术模板（5 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-501` | 市值分组中性化 | `group_neutralize({alpha}, bucket(rank(cap), range="{range}"))` |  | `residual` |
| `TPL-502` | 双重中性化（行业+市值） | `a1 = group_neutralize({alpha}, bucket(rank(cap), range="{range}")); group_neutralize(a1, {group})` |  | `residual` |
| `TPL-503` | 回归中性化（新增） | `regression_neut({alpha}, {factor}) 多层版：regression_neut(regression_neut({alpha}, {factor1}), {factor2})` |  | `residual` |
| `TPL-504` | 中性化顺序优化（新增） | `a = ts_zscore({field}, 252); a1 = group_neutralize(a, {group}); a2 = group_neutralize(a1, bucket(rank(cap), range="0.1,1,0.1"))` | 先行业再市值的中性化顺序，与反向顺序效果可能不同 | `residual` |
| `TPL-505` | sta1 分组中性化（新增） | `group_neutralize({alpha}, sta1_top3000c20)` | 使用预定义 sta1 分组做中性化 | `residual` |

#### 回填与覆盖模板（5 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-1301` | 分组回填 | `group_backfill({field}, {group})，使用组内最近值填充 NaN` |  | `transform` |
| `TPL-1302` | 嵌套回填排名 | `rank(group_backfill({field}, {group}))` |  | `transform` |
| `TPL-1303` | 覆盖度过滤 | `group_count(is_nan({field}), market) > {threshold} ? {alpha} : nan；threshold∈{40, 50}` |  | `gating` |
| `TPL-1304` | NaN 替换 | `if_else(is_not_nan({field}), {field}, {default})；default∈{0, 0.5, nan}` |  | `transform` |
| `TPL-1305` | 综合数据清洗 | `{ts_op}(winsorize(group_backfill(ts_backfill({field}, {d1}), {group}), std={std}), {d2})` |  | `transform` |

#### 百分位与分位数模板（5 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-1501` | 时序百分位 | `ts_percentage({field}, {d}, percentage={p})；p∈{0.5, 0.25, 0.75}` |  | `transform` |
| `TPL-1502` | 分位数 | `{ts_op}(ts_quantile({field}, {d}, {q}), {d2})；q∈{0.25, 0.5, 0.75}` |  | `transform` |
| `TPL-1503` | Max-Min 比率 | `ts_max_diff({field}, {d}) / ts_av_diff({field}, {d})` |  | `residual` |
| `TPL-1504` | 中位数 | `{field} - ts_median({field}, {d})` |  | `transform` |
| `TPL-1505` | 累积乘积 | `ts_product(1 + {ret_field}, {d})，计算累积收益` |  | `transform` |

#### 组合提取模板（4 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-1401` | group_extra 填补 | `group_extra({field}, {weight}, {group})` |  | `transform` |
| `TPL-1403` | PnL 反馈 | `if_else(inst_pnl() > {threshold}, {alpha}, nan)；threshold∈{0, -0.05}` | 基于单标的 PnL 进行条件交易 | `gating` |
| `TPL-1404` | 流动性加权 | `{alpha} * log(volume)，将仓位偏向高流动性股票` |  | `combination` |
| `TPL-1405` | 市值回归中性化 | `regression_neut({alpha}, log(cap))` |  | `residual` |

#### 社区验证过的算子级模板（4 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-OP-01` | ts_decay_linear 唤醒低频死信号 | `ts_decay_linear(vec_max(x) - vec_min(x), d)` | 低频/稀疏向量信号用 vec 极差 + 线性衰减激活 | `transform` |
| `TPL-OP-02` | ts_zscore 事件触发 | `event = abs(ts_zscore(x, n)) > 3; trade_when(event, signal, -1)` | zscore 极端偏离时触发交易 | `gating` |
| `TPL-OP-03` | ts_zscore 离群过滤 | `ts_zscore(x, n) > 5 ? nan : x` | zscore 超阈值视为离群点剔除（置 NaN） | `transform` |
| `TPL-OP-04` | ts_regression 提取 beta/残差/截距/R2 | `ts_regression(close, vwap, 4, lag=0, rettype=2)` | 通过 rettype 提取回归的不同统计量 | `transform` |

#### 事件驱动模板（3 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-1001` | 数据变化天数 | `if_else(days_from_last_change({field}) == {days}, {alpha}, nan) 动态衰减版：{alpha} / (1 + days_from_last_change({field}))` |  | `gating` |
| `TPL-1002` | 最近差值（新增） | `{ts_op}(last_diff_value({field}, {d}), {d2})` | 返回过去 d 天内最近一次不同于当前值的历史值 | `transform` |
| `TPL-1003` | 缺失值计数（新增） | `-ts_count_nans(ts_backfill({field}, {d1}), {d2})` | 分析师覆盖度信号，缺失越少覆盖越好 | `transform` |

#### Turnover 控制模板（3 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-1201` | 目标换手率 Hump | `ts_target_tvr_hump({alpha}, lambda_min=0, lambda_max=1, target_tvr={target})` |  | `gating` |
| `TPL-1202` | Delta 限制换手率（新增） | `ts_target_tvr_delta_limit({alpha}, {factor}, lambda_min=0, lambda_max=1, target_tvr={target})` |  | `gating` |
| `TPL-1203` | Hump 衰减组合（新增） | `hump_decay({alpha}, hump={h})；h∈{0.001, 0.01} 嵌套版：hump(hump_decay({alpha}, hump=0.001))` |  | `transform` |

#### 附加模板（2 个）

| ID | 名称 | 骨架 | 用途 | 角色 |
|---|---|---|---|---|
| `TPL-ATT-IND-SENTIMENT` | IND 情感数据模板（附加模板一） | `S1 = ts_mean(ts_backfill({sentiment}, 250), 22); R1 = ts_product(1+returns, 22); alpha = ts_quantile(S1-R1, 5, driver='cauchy')` | 情感分数减去市场已 price-in 收益，做多情感相对收益高的股票 | `transform` |
| `TPL-ATT-VELOCITY` | 速度/加速度差分预处理（附加模板二） | `速度: ts_delta(field, day)；加速度: ts_delta(ts_delta(field, day), day)；days=[5,22,66,240]` | 多周期一阶/二阶差分生成基础字段后套其他算子回测 | `transform` |

## 3. 取用纪律（小结）

1. **先查幽灵算子表**（§2.5）：含 `sigmoid` / `ts_entropy` / `ts_skewness` 等算子的
   骨架，入批前必须替换等价算子或先 `validate_expressions` 实测，否则整批 ERROR/CANCELLED。
2. **候选层不等于可用**：141 个全部 `candidate_unverified`，仅作骨架灵感，
   不可直接当已验证配方。
3. **优先复用已验证层**（§1）：10 个跨区实证配方含具体 Sharpe 与区域证据。
4. **负模板先比对**：§1 末尾两个负模板标记了证伪方向（单字段裸探针、稀疏事件流）。
5. **回写闭环**：取用后务必回写 `validated`/`failed`，否则知识库无法晋升。
