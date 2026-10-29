# earnings6 字段画像（USA / D1 / TOP3000）

> 抓取日 2026-10-29 · `get_datafields(dataset_id="earnings6", filter_sharpe=false)` 返回 `complete=true`, `platform_count=52`
> 数据集级：coverage **0.9853** / 52 字段 **全 VECTOR** / pyramidMultiplier 1.2（EARNINGS 塔）
> 定位：earnings 塔第 3 颗的备选来源（第 1 源 earnings_chart_dl 已封盘 S 1.34；第 2 源 earnings4 在飞）

---

## 1. 核心结论先说

**这个数据集的 52 个字段里，只有约 10 个是数值信号，其余 42 个是元数据（URL / 公司名 / 电话 / 密码 / 时区 / 状态枚举）。**

但正因如此，少数信号字段的拥挤度低到罕见：

| 字段 | alphaCount | userCount | 判读 |
|---|---|---|---|
| **`eps_change_percentage_value`** | **3** | 2 | 全数据集最不拥挤的数值信号，几乎无人挖 |
| **`eps_change_absolute_value`** | **5** | 5 | 同上族 |
| `preliminary_eps_range_lower_bound` | 34 | 27 | 初步 EPS 区间下沿 |
| `preliminary_eps_range_upper_bound` | 36 | 28 | 初步 EPS 区间上沿 |
| `ern6_1q` / `ern6_4q` | 87 / 70 | 66 / 60 | 历史财报日（日期型，适合做事件门控） |
| `ern6_actual_eps` | 157 | 99 | 报告 non-GAAP 摊薄 EPS |
| `ern6_estimated_eps` | 198 | 120 | **Estimize 加权 EPS 预期**（人群预测，非分析师） |
| `ern6_etype` | 573 | 191 | 财报日状态枚举（T/V/I），最拥挤但纯元数据 |
| `ern6_goto_broadcast` | 447 | 187 | 电话会录音链接，纯元数据 |

**⇒ 该数据集的拥挤集中在元数据字段（`ern6_etype` 573、`ern6_goto_broadcast` 447），而真正能构造信号的 EPS 族拥挤度只有个位数到百位。这是 earnings 六集中罕见的「信号字段比元数据字段更冷」结构。**

---

## 2. 字段分类

### 2.A 数值信号族（可用，10 个）

| 字段 | cov | 含义 | 机制角色 |
|---|---|---|---|
| `ern6_actual_eps` | 0.9278 | 报告 non-GAAP 摊薄（无摊薄则基本）EPS | 实际值 —— SUE 的分子 |
| `ern6_estimated_eps` | 0.9278 | **Estimize 加权 EPS 预期**（对上一完整期） | 预期值 —— SUE 的减项 |
| `preliminary_eps_range_lower_bound` | 0.9278 | 初步 EPS 或区间下沿 | 区间定位 |
| `preliminary_eps_range_upper_bound` | 0.9278 | 区间上沿（单值则等于下沿） | 区间定位 |
| `eps_change_absolute_value` | 0.9278 | EPS 相对上期的**绝对**变化 | 盈余动量 |
| `eps_change_percentage_value` | 0.9278 | EPS 相对上期的**百分比**变化 | 盈余动量（标准化版） |
| `ern6_stock_split_ratio` | 1.0 | 拆股参数 #:# | 事件型 |
| `ern6_x_dividend` | 0.9843 | 股息美元金额 | 事件型 |
| `ern6_x_dividend_oc` | 0.9843 | 股息（原币种金额） | 事件型 |
| `ern6_1q`…`ern6_4q` / `ern6_next_ed` | 0.9843 | 历史/下次财报日 | 事件门控轴 |

### 2.B 日期与状态族（做门控/轴，不做信号）

`ern6_1q`~`ern6_4q`、`ern6_next_ed`、`ern6_next_ed_fiscal_year`、`ern6_next_ed_quarter`、`ern6_estimated_fiscal_year`、`ern6_actual_fiscal_year`、`ern6_transcript_fiscal_year`、`ern6_board_of_directors_meeting`、`ern6_wqreceivetimestamp`、`ern6_time_zone`

- `ern6_actual_fiscal_year` / `ern6_estimated_fiscal_year` 是 **YYYY 整数**，可做「财报滞后度」= 当前年 − 财年。
- `ern6_wqreceivetimestamp` 是摄取时间戳 ⇒ 可做**数据延迟/新鲜度**信号（信息传播速度）。

### 2.C 纯元数据（禁用，42 个中的绝大多数）

`ern6_actual_url`、`ern6_estimated_url`、`ern6_prelim_earnings_link`、`ern6_goto_broadcast`、`ern6_company_name(s)`、`ern6_confnumber`、`ern6_confpasscode`、`ern6_actual_currenty`、`ern6_actual_source`、`ern6_actual_period`、`ern6_quarter`、`ern6_transcript_quarter`、`ern6_isin`、`ern6stock_symbol`、`ern6_eps6stock_symbol`、`ern6_stock_exchange`、`ern6_eps6ww_status`、`ern6ww_status`、`ern6_time_of_day`、`ern6_estimated_tod`、`ern6_conferencecalltime`、`ern6_meeting_status`、`ern6_mtg_type`、`ern6_div_freq`、`ern6_dividend_status`、`ern6_split_status`、`ern6_estimated_etype`、`ern6_etype`

> ⚠ `ern6_etype`（573 alpha）与 `ern6_goto_broadcast`（447 alpha）虽最拥挤，但语义是「日期可信度枚举」和「录音链接」，**不是信号**。它们的高 alphaCount 是「被当成占位字段顺手用」的伪拥挤，不构成机制竞争。

---

## 3. 机制设计（5 条，按机制正交性排序）

### M1 · SUE 标准化盈余惊喜（PEAD 核心，最优先）

**经济含义**：实际 EPS 超预期幅度越大，股价对好消息的反应不足（post-earnings announcement drift）⇒ 后续继续跑赢。这是学术界最稳健的异象之一（Bernard & Thomas 1989/1990；论坛「Earnings Datasets」帖同款模板：UnexpectedEarnings 高 + EarningsAnnouncementReturn 正 → 做多）。

**与其它源的正交性**：earnings_chart_dl 是图像 CNN 预测未来收益分位（纯统计），earnings4 是期权隐含波动率（纯市场定价），本条是**会计基本面惊喜** ⇒ 三者机制互不重叠，self-corr 风险最低。

**实现（单位安全，禁止加 ε）**：
```
divide(subtract(vec_avg(ern6_actual_eps), vec_avg(ern6_estimated_eps)), abs(vec_avg(ern6_estimated_eps)))
```
分子分母同为「每股金额 / 每股金额」⇒ 无量纲。分母可能为 0（预期 EPS=0）⇒ 交给平台产生 Inf，由外层 `group_rank` / `winsorize` 吸收。

**可证伪判据**：若该式 S < 0.5 且 `eps_change_percentage_value` 单独式 S > 该值，则「惊喜 vs 预期」结构不如「同比变化」结构，PEAD 线改走 M2。

### M2 · EPS 同比变化率（零竞争字段）

**经济含义**：盈余动量（earnings momentum）—— EPS 同比增长最快的公司后续跑赢（Chordia & Shivakumar 2006）。

**实现**：`eps_change_percentage_value` 直接作信号（已是标准化百分比，无量纲）。
```
group_rank(ts_backfill(vec_avg(eps_change_percentage_value), 66), subindustry)
```
`ts_backfill` 必需：财报是季度事件，不 backfill 会让序列在「有值/NaN」间跳变（fundamental91 波 131 的 155% 换手病理同源）。

**可证伪判据**：alphaCount=3 意味着几乎无人验证过。若 S > 1.0，该字段是全新活矿，值得为其单独开一波。

### M3 · 实际 EPS 在初步区间的百分位（区间定位，独有结构）

**经济含义**：初步公告给出 EPS 区间，实际落在区间上沿 = 内部预期向上修正 = 好消息；落在下沿反之。这个「落在区间的哪里」是 earnings6 独有的结构，其它 earnings 数据集都没有。

**实现**：
```
divide(subtract(vec_avg(ern6_actual_eps), vec_avg(preliminary_eps_range_lower_bound)),
       subtract(vec_avg(preliminary_eps_range_upper_bound), vec_avg(preliminary_eps_range_lower_bound)))
```
单位：EPS / EPS ⇒ 无量纲。单值公告时上下沿相等 ⇒ 分母 0 ⇒ Inf，同理交外层吸收。

**可证伪判据**：若该式与 M1 的互相关 > 0.7，说明两者都在测同一份「超预期」，M3 不独立成塔；若 < 0.4，M3 是独立机制。

### M4 · 财报日临近度 / 财报后漂移窗（事件门控，非独立信号）

**经济含义**：PEAD 的收益集中在财报后 1-60 个交易日。用「距下次财报天数」做门控，只在漂移窗内持仓，可提高信号纯度、降低无效换手。

**实现**：`ern6_next_ed` 是日期 ⇒ 需转为「天数差」。若平台无日期减法算子，退化方案：用 `ern6_1q`~`ern6_4q` 中最近的历史财报日对齐。

**注意**：门控腿若引入非 earnings6 字段会破坏 ATOM。必须在 earnings6 内部完成，或接受两塔（但 earnings 是目标塔，另一塔只能是非 trio 的 category）。

### M5 · 拆股 / 股息事件（事件型，低优先）

`ern6_stock_split_ratio`（拆股比例）、`ern6_x_dividend`（股息金额）。学术上拆股公告有正漂移（signaling），股息 initiations/omissions 有强信号（dividend clientele）。但：
- 拆股在 USA 大盘股中极稀疏（TOP3000 每年几十家）⇒ coverage 会崩
- 股息金额与股价量级相关 ⇒ 必须除以价格，而 `close` 是 PV 字段 ⇒ **破坏 ATOM**

**⇒ M5 仅在 ATOM 约束可放宽时启用；单塔线不碰。**

---

## 4. 骨架与设置建议

沿用 earnings_chart_dl 三波（波 134-137）已验证的最优骨架：
```
ts_decay_linear(group_rank(<core>, subindustry), 22)
```
- 该骨架在 chart_dl 上稳定给出 TO 14-18%、eff 0.55-0.63；避免 sentiment21 的 `group_rank(<已衰减序列>, g)` 写法（TO 冲到 100%）。
- **VECTOR 字段必须 `vec_avg`**（52 字段全 VECTOR）。
- **事件稀疏字段必须 `ts_backfill`**（M2/M5），否则重演 fundamental91 的 NaN 填充伪影。
- 设置：TOP3000 / D1 / decay 0 / SUBINDUSTRY / trunc 0.08 / nanHandling ON / IS 2014-01-01~2023-12-31。

**时间跨度警告**：coverage 0.9853 是**股票覆盖率**不是时间跨度。`ern6_actual_eps` 依赖 Estimize 一致预期数据，很可能不像 chart_dl 那样回溯到 2014 —— **首波必须先跑 `get_alpha_yearly_stats` 看逐年 longCount，再决定是否投第二波**（GBR earnings6 的 PEAD 曾实测 S1.77/2Y2.06 却因数据自 2019-12 起而不满足十年覆盖，是该坑的既证案例）。

---

## 5. 与其它 earnings 数据集的定位对比

| 数据集 | cov | 字段 | 信号密度 | 机制 | 状态 |
|---|---|---|---|---|---|
| `earnings_chart_dl` | 0.991 | 100 | 高（分位桶族） | 图像 CNN 预测收益分位 | **已封盘**：三波 18 条，S 天花板 1.35，互相关 0.90-0.99 ⇒ 最多出 1 颗 |
| `earnings4` | 0.9692 | 375 | 中（期权族） | 隐含波动率 / 事件波动贡献 | 在飞（波 138） |
| **`earnings6`** | **0.9853** | **52** | **低但极冷（3-5 alpha）** | **盈余惊喜 / PEAD / 区间定位** | **本画像新建，未派发** |
| `earnings27` | 0.2734 | 14 | — | — | 排除（coverage 过低） |
| `earnings7` | 0.6479 | 40 | — | — | 排除（coverage 过低） |
| `earnings_sent_matrix` | 0.7 | 7 | — | — | 排除（coverage 低 + 字段少） |

---

## 6. 下一步

1. earnings4 首波（波 138）结果回来后决定 earnings 塔第 2 颗来源是否成立。
2. earnings6 首波（3-4 条探针）：M1 SUE / M2 EPS 同比 / M3 区间定位，三条机制各一条 + 一条 M1 的反向对照。
3. **首波前先解决时间跨度**：任一 earnings6 alpha 出结果后立刻跑 `get_alpha_yearly_stats` 验证 2014-2023 逐年 longCount；若数据起始晚于 2014，该数据集同样不满足「近十年都有数据」的硬约束，直接排除，不投第二波。
