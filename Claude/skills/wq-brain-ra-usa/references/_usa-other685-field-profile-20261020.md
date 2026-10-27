# USA · other685「Enhanced Financial Indicators」字段画像与机制台账（2026-10-20）

> 数据集归属：**USA / D1 / OTHER 塔（未点亮）**。启用原因：用户指令「已点亮塔的数据集先不回测」，
> USA/D1 的 analyst=5 / model=4 / earnings=1 均已点亮；`other` 塔为 0 ⇒ 符合未点亮塔约束。
> 平台元数据（`get_datasets(category="other")`，2026-10-20）：
> `other685` · Enhanced Financial Indicators · coverage **0.7225** · fieldCount **72** ·
> userCount **136** · alphaCount **218** · valueScore 4 · pyramidMultiplier 1.4。
> 全部字段均为 **MATRIX**（无 VECTOR，无需 `vec_*` 聚合）。
> 平台描述：combines StarMine Earnings Quality (EQ) and Analyst Revisions Model (ARM).

## 1. 数据集级结论

| 维度 | 读数 | 判读 |
|---|---|---|
| 塔位 | USA/D1/OTHER = 0 | **未点亮**，符合用户 2026-10-20 约束 |
| 拥挤度 | 218 α / 136 用户（72 字段） | 低拥挤；字段级 alphaCount 中位数 1 |
| 覆盖 | 0.7225（数据集级） | 中高；但字段间跨度 0.36–0.996，**<0.5 的字段裸用会 CW** |
| 字段类型 | 72/72 MATRIX | 日频面板，可直接进 ts_/group_ 算子 |
| 更新频率 | 日频（MATRIX；估值/增长类随价格与分析预期更新，财务口径按季刷新） | 财报口径字段有 63–252 日粘滞，短窗差分会被摊平 |
| 话语体系 | StarMine EQ（质量）+ ARM（修正/增长百分位）+ 原始财务比率 | 质量/估值/增长三类，**不能简单相加**（禁混信号） |
| 已开采度 | 0-alphaCount 字段 14 个（见 §2 ★） | 这些是首选未开采面 |

**字段覆盖分层（裸用阈值）**：

- **cov ≥ 0.90（可直接裸用）**：StarMine 估值/收益率/百分位族，共 21 个字段。
- **0.55 ≤ cov < 0.90（本批主力，需通用壳 `ts_backfill(...,252)`）**：原始财务比率与 igaigr/cfroi 族。
- **cov < 0.55（不建议做主信号）**：`eps_forecast_current/next_fiscal_year`（0.471）、
  `oth685_02v`（0.4625）、`oth685_12v`（0.424）、`oth685_63v`（0.4687）、`oth685_82v`（0.3836）、
  `oth685_mktinv`（0.4395）、`oth685_lvtkmvni`（0.4802）、`oth685_epsgrow5`（0.3608）。
  其中 `eps_forecast_*` 虽 0-alphaCount，但覆盖率过低，**首批不使用**。

## 2. 全部 72 字段清单（按家族）

> 列：字段 id · 覆盖率 · alphaCount · 含义（平台 description 摘要）。★ = alphaCount 0（未开采）。

### 2.1 StarMine 估值倍数与历史分位（估值族，21）

| 字段 | cov | αC | 含义 |
|---|---:|---:|---|
| `diff_current_vs_hist_pe_ratio` | 0.9961 | 89 | 当前 P/E − 历史中位 P/E（正 = 高于自身历史） |
| `diff_current_vs_hist_price_ratio_earnings` | 0.9961 | 30 | 当前 P/E − 历史前瞻 12M P/E 中位 |
| `forward_pe_ratio_mean_fy1` | 0.9961 | 9 | FY1 均值预期前瞻 P/E |
| `forward_pe_ratio_smartest_fy1` | 0.9961 | 6 | FY1 SmartEstimate 前瞻 P/E |
| `mean_estimate_price_ratio_fy1` | 0.9951 | 12 | FY1 均值预期 P/E |
| `pe_ratio_last_fiscal_year` | 0.9182 | 2 | 上一财年 P/E（StarMine） |
| `pe_ratio_trailing_4q` | 0.9952 | 3 | 过去 4 个报告季度 P/E |
| `price_to_smartest_ratio_fy1_earnings` | 0.9903 | 1 | FY1 SmartEstimate P/E |
| `median_forward_12m_pe_ratio_hist` | 0.8898 | 1 | 自身历史前瞻 12M P/E 中位（基准） |
| `median_forward_12m_price_ratio_earnings_hist` | 0.8974 | 0 ★ | 同上（另一命名） |
| `peg_ratio_mean_fy1` | 0.8454 | 0 ★ | FY1 均值预期 PEG |
| `peg_ratio_smartest_fy1` | 0.8452 | 2 | FY1 SmartEstimate PEG |
| `peg_ratio_industry_percentile_smartest_f12m` | 0.8453 | 1 | PEG 行业内百分位（SmartEstimate F12M） |
| `peg_ratio_sector_percentile_smartest_f12m` | 0.9068 | 1 | PEG 行业内百分位（sector） |
| `earnings_yield_smartest_fy1` | 0.9964 | 15 | FY1 SmartEstimate E/P（%） |
| `earnings_yield_industry_percentile_fy1` | 0.9947 | 2 | FY1 E/P 行业内百分位 |
| `earnings_yield_sector_percentile_fy1` | 0.9947 | 3 | FY1 E/P sector 百分位 |
| `yield_smartest_fy1_earnings` | 0.9963 | 3 | FY1 SmartEstimate 收益率（E/P 口径） |
| `yield_industry_percentile_fy1_earnings` | 0.9948 | 3 | FY1 收益率行业内百分位 |
| `yield_sector_percentile_fy1_earnings` | 0.9947 | 1 | FY1 收益率 sector 百分位 |
| `eps_forecast_current_fiscal_year` | 0.471 | 0 ★ | 当前财年 EPS 预期（低覆盖，首批不用） |
| `eps_forecast_next_fiscal_year` | 0.471 | 0 ★ | 下一财年 EPS 预期（低覆盖，首批不用） |

### 2.2 StarMine 增长与 ARM 百分位（增长族，12）

| 字段 | cov | αC | 含义 |
|---|---:|---:|---|
| `blended_growth_rate_smartest` | 0.9207 | 2 | 去年→今年、今年→明年、长期增速的 SmartEstimate 均值 |
| `blended_growth_rate_industry_percentile` | 0.9208 | 0 ★ | 混合增速行业百分位 |
| `blended_growth_rate_sector_percentile` | 0.9208 | 2 | 混合增速 sector 百分位 |
| `growth_next_year_industry_percentile_earnings` | 0.9901 | 4 | 今年→明年盈利增速行业百分位 |
| `growth_next_year_sector_percentile_earnings` | 0.9677 | 0 ★ | 同上（sector） |
| `growth_this_year_industry_percentile_earnings` | 0.8925 | 1 | 去年→今年盈利增速行业百分位 |
| `growth_this_year_sector_percentile_earnings` | 0.9677 | 4 | 同上（sector） |
| `smartest_growth_next_vs_this_year_earnings` | 0.9677 | 0 ★ | 今年→明年 SmartEstimate 增速 |
| `smartest_growth_this_vs_last_year_earnings` | 0.8868 | 0 ★ | 去年→今年 SmartEstimate 增速 |
| `smartest_growth_f12m_vs_t12m_earnings` | 0.8324 | 1 | F12M vs T12M 盈利增速 |
| `oth685_92v` | 0.6757 | 3 | 过去 5 年 EPS 平均增速 |
| `oth685_epsgrow5` | 0.3608 | 0 ★ | 5 年 EPS 年均增速（低覆盖，不用） |

### 2.3 现金流收益率与现金回报（质量/现金族，10）

| 字段 | cov | αC | 含义 |
|---|---:|---:|---|
| `oth685_11v` | 0.6868 | 3 | P/CFO（价格/经营现金流） |
| `oth685_21v` | 0.6888 | 1 | P/FCF |
| `oth685_81v` | 0.6923 | 5 | FCF/EV（%） |
| `oth685_91v` | 0.6815 | 3 | CFO/EV（%） |
| `oth685_cfroi_3` | 0.5939 | 0 ★ | 现金口径 ROIC（3 期） |
| `oth685_cfroi_4` | 0.5654 | 1 | 现金口径 ROIC（4 期） |
| `oth685_cfroi_5` | 0.5354 | 1 | 现金口径 ROIC（5 期） |
| `oth685_cfroitrn` | 0.5695 | 1 | 现金 ROI 的变化/趋势 |
| `oth685_cfsurq0` | 0.6322 | 1 | 最近季度现金流 |
| `oth685_1yf_5145h` | 0.6348 | 1 | 未来财年财务指标（口径未明） |

### 2.4 资产增长 / 投资 / 资本开支（增长投资族，8）

| 字段 | cov | αC | 含义 |
|---|---:|---:|---|
| `oth685_2_igaigr` | 0.5950 | 6 | 近期资产基数变化（资产增长） |
| `oth685_3_igaigr` | 0.5679 | 1 | 资产增长率（区间口径） |
| `oth685_4_igaigr` | 0.5373 | 2 | 资产增长百分比 |
| `oth685_5_igaigr` | 0.5108 | 1 | 资产增长率（另一区间） |
| `oth685_invgrow5` | 0.5608 | 0 ★ | 5 年投资年均增速 |
| `oth685_mktinv` | 0.4395 | 1 | 市场投资（低覆盖） |
| `oth685_lvtkmvni` | 0.4802 | 1 | 投资/资产总市值（低覆盖） |
| `oth685_econaccumdep` | 0.6295 | 0 ★ | 经济累计折旧 |

### 2.5 盈利能力 / ROI 变化（ROI 族，8）

| 字段 | cov | αC | 含义 |
|---|---:|---:|---|
| `oth685_roitran1` | 0.6238 | 0 ★ | ROI 变化（区间 1） |
| `oth685_roitran2` | 0.6257 | 1 | ROI 变化（区间 2） |
| `oth685_roitrn_1` | 0.5253 | 4 | ROI 变化（特定窗口 1） |
| `oth685_roitrn_2` | 0.5024 | 2 | ROI 变化（特定窗口 2） |
| `oth685_rgdani_s` | 0.5474 | 3 | 回归调整净利润 |
| `oth685_03v` | 0.6772 | 4 | 财务/运营指标（口径未明） |
| `oth685_15v` | 0.5281 | 2 | 财务/运营指标（口径未明） |
| `oth685_epsgrow5` | 0.3608 | 0 ★ | 5 年 EPS 增速（低覆盖） |

### 2.6 杠杆 / 营运资本 / 销售效率（杠杆族，6）

| 字段 | cov | αC | 含义 |
|---|---:|---:|---|
| `oth685_leveragemkt` | 0.5863 | 1 | 市场杠杆 |
| `oth685_wd_ratio` | 0.5863 | 0 ★ | 营运资本比率 |
| `oth685_entwdrat` | 0.5863 | 0 ★ | EV / 营运资本 |
| `oth685_prc_sale` | 0.5993 | 1 | P/S |
| `oth685_s_fcf_p` | 0.5641 | 0 ★ | 销售 / 每股 FCF |
| `oth685_vol_his_30d_call` | 0.6196 | 3 | 30 日历史波动（call 口径） |

### 2.7 EPS 惊喜 / 摊薄 / 股息 / 其他（7）

| 字段 | cov | αC | 含义 |
|---|---:|---:|---|
| `oth685_epssurpq` | 0.6321 | 0 ★ | **季度 EPS 惊喜**（PEAD 候选） |
| `oth685_63v` | 0.4687 | 0 ★ | 终止经营/非常项目摊薄 EPS 环比变化 |
| `oth685_02v` | 0.4625 | 1 | 上季终止经营金额 |
| `oth685_12v` | 0.4240 | 1 | 终止经营环比变化 |
| `oth685_72v` | 0.5814 | 0 ★ | 每股股息环比变化（绝对） |
| `oth685_82v` | 0.3836 | 1 | 每股股息环比变化（%） |
| `oth685_coverage` | 0.5604 | 0 ★ | 数据覆盖率（非信号，排除） |

## 3. 适用模板（由字段体征决定，不按数据集名套）

| 体征 | 适用模板 | 字段 |
|---|---|---|
| 比率水平（有经济方向） | 水平秩：通用壳直接 `group_rank` | `oth685_cfroi_3/4/5`、`oth685_91v`、`oth685_81v`、`oth685_wd_ratio`、`oth685_leveragemkt` |
| 已含“变化”的字段 | **水平**使用，不要再差分（差分会变成二阶变化，噪声翻倍） | `oth685_*_igaigr`、`oth685_cfroitrn`、`oth685_roitran1/2` |
| 事件型惊喜（季度） | `ts_zscore(...,252)` 做测量口径归一，再 rank | `oth685_epssurpq` |
| 自身历史相对（P/E vs 历史） | 直接反号 + 横向秩 | `diff_current_vs_hist_pe_ratio` |
| 0–100 百分位 | 直接秩变换（已是同行相对位次），**不要再套 group 归一** | `*_industry_percentile*`、`*_sector_percentile*` |
| 低覆盖（<0.55） | 主信号排除；只可作门控/对照 | §1 列出 8 个 |

**禁用**：`oth685_coverage`（元数据，不是信号）。

## 4. 机制台账（首批 M01–M08）

设置（`wqb.profiles explain --region USA --dataset other685`）：**SUBINDUSTRY / decay 5 / trunc 0.08**；
与 analyst 战役的 RAM/decay20 不同，跨档不可比。
壳：`quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`。

| # | 机制 | 字段 | 经济方向 | SIG | 假说与文献 |
|---:|---|---|---|---|---|
| 1 | 资产增长异象 | `oth685_2_igaigr` | **负** | `-1 * oth685_2_igaigr` | Cooper/Gulen/Schill (2008)：资产扩张 = 过度投资/稀释，未来收益低 |
| 2 | 现金 ROIC 水平 | `oth685_cfroi_3` | 正 | `oth685_cfroi_3` | 现金回报率高的公司质量溢价；Novy-Marx 质量因子 |
| 3 | CFO/EV 收益率 | `oth685_91v` | 正 | `oth685_91v` | 现金创造相对企业价值便宜 ⇒ 价值+质量混合 |
| 4 | FCF/EV 收益率 | `oth685_81v` | 正 | `oth685_81v` | 自由现金流收益率是稳健的价值/质量锚 |
| 5 | 季度 EPS 惊喜 | `oth685_epssurpq` | 正 | `ts_zscore(oth685_epssurpq, 252)` | PEAD：惊喜后漂移；zscore 解决量纲 |
| 6 | 现金 ROI 趋势 | `oth685_cfroitrn` | 正 | `oth685_cfroitrn` | 资本回报改善 = 质量改善，慢信号 |
| 7 | 估值相对自身历史 | `diff_current_vs_hist_pe_ratio` | **负** | `-1 * diff_current_vs_hist_pe_ratio` | 相对自身历史贵 ⇒ 均值回归（不是绝对低估值） |
| 8 | 混合增长百分位 | `blended_growth_rate_industry_percentile` | 正 | `blended_growth_rate_industry_percentile` | 增长百分位形态（论坛实证：百分位形态 2Y 更干净） |

**正交性检查**：8 条分别对应 资产扩张 / 现金回报水平 / CFO 收益 / FCF 收益 / 事件惊喜 / ROI 趋势 / 相对估值 / 增长，
无两条共用同一字段；#2/#3/#4 同属“现金/质量”，但分别测回报率、现金流收益率两种定价口径，属同族对照而非重复。

**完整表达式（可直接发批）**：

| # | 完整表达式 |
|---:|---|
| 1 | `quantile(group_rank(hump(ts_backfill(winsorize(-1 * oth685_2_igaigr, std=4), 252), hump=0.01), industry))` |
| 2 | `quantile(group_rank(hump(ts_backfill(winsorize(oth685_cfroi_3, std=4), 252), hump=0.01), industry))` |
| 3 | `quantile(group_rank(hump(ts_backfill(winsorize(oth685_91v, std=4), 252), hump=0.01), industry))` |
| 4 | `quantile(group_rank(hump(ts_backfill(winsorize(oth685_81v, std=4), 252), hump=0.01), industry))` |
| 5 | `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(oth685_epssurpq, 252), std=4), 252), hump=0.01), industry))` |
| 6 | `quantile(group_rank(hump(ts_backfill(winsorize(oth685_cfroitrn, std=4), 252), hump=0.01), industry))` |
| 7 | `quantile(group_rank(hump(ts_backfill(winsorize(-1 * diff_current_vs_hist_pe_ratio, std=4), 252), hump=0.01), industry))` |
| 8 | `quantile(group_rank(hump(ts_backfill(winsorize(blended_growth_rate_industry_percentile, std=4), 252), hump=0.01), industry))` |

**判据（写死）**：任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 / TO≥1% 且 fail 数 = 0 ⇒ 立即 `check_correlation(refresh=True)`
做 prod/self 双端点（<0.7）；只过 1–2 闸的先按 §5 归因，不直接扩批。 <!-- from config.prod_corr_max -->

**实际发批（2026-10-20，multisim `2RlVsXegr4lR9s712HQjBXPJ`，8 条）**：
设置按 profile = EQUITY / USA / TOP3000 / D1 / **SUBINDUSTRY / decay 5 / trunc 0.08**（与 analyst 战役不同档，结果不可跨档比较）。
`preflight_expressions` 的 8 个真实字段全部 `fields_checked` 通过，仅报 `unknown_fields=["std"]`（`winsorize(std=)` 已知误报）；
`vector_fields=[]`、`any_changed=false`（全 MATRIX，无 VECTOR 需要聚合）。

### 4.1 批 1 收批（8/8 COMPLETE；0 颗过闸；水平/质量族判弱）

| # | 字段 | alpha | S | F | 2Y | SUB | risk-neut S | TO | fail |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `-igaigr` 资产增长 | `ZYmKlmr8` | 0.71 | 0.36 | 1.20 | 0.10 | 0.16 | 1.00% | S/F/2Y/SUB |
| 2 | `cfroi_3` 现金 ROIC | `0mjMQj8v` | 0.79 | 0.41 | 1.20 | 0.19 | 0.41 | 0.92% | S/F/2Y/SUB/TO |
| 3 | `91v` CFO/EV | `pwvKzv7V` | 0.42 | 0.15 | 0.49 | 0.13 | 0.41 | 1.14% | S/F/2Y/SUB |
| 4 | `81v` FCF/EV | `mLYVzYX6` | 0.31 | 0.10 | 0.25 | 0.13 | 0.48 | 1.09% | S/F/2Y |
| 5 | `epssurpq` 惊喜 | `1YjzmjgR` | 0.61 | 0.27 | 0.58 | 0.20 | 0.29 | 1.12% | S/F/2Y/SUB |
| 6 | `cfroitrn` ROI 趋势 | `O0JxmJpY` | 0.55 | 0.23 | 0.78 | 0.03 | 0.02 | 0.96% | S/F/2Y/SUB/TO |
| 7 | `-diff_pe_hist` 自身历史估值 | `P0MOlMpw` | 0.74 | 0.33 | **1.31** | 0.67 | 0.39 | 1.05% | S/F/2Y |
| 8 | `blended_growth_industry_pct` 增长百分位 | `kqJZmJ3g` | **0.88** | 0.41 | **1.72** | 0.44 | 0.26 | 1.01% | S/F |

**归因（写死，作为批 2 的设计依据）**：

1. **水平族（估值/质量）在 USA 没有全期 alpha**：6 条水平型 S 0.31–0.79，整体与「USA value/quality 饱和」一致。
   即使 #2 现金 ROIC 的 risk-neutralized S 0.41、#4 FCF/EV 0.48，也只是风格 beta 的整理效果，总收益不足
   ⇒ **不再用纯水平形态扩批**。
2. **相对形态确实抬 2Y，但抬不动全期 S**：仅两条 2Y>1.2（#8 1.72、#7 1.31），二者分别是行业百分位与「当前 vs 自身历史」；
   但 #8 的 risk-neutralized S 只有 0.26 ⇒ 近两年强度大半来自增长/价值风格，不是独立 alpha。
   这与论坛「百分位形态改善 2Y」方向一致，但**2Y 好 ≠ 全期可交付**。
3. **SUB 与覆盖率同向**：#7/#8 覆盖 0.996/0.921 ⇒ SUB 0.67/0.44；低覆盖的 #1/#6（0.595/0.570）SUB 0.10/0.03。
   ⇒ 后续优先 cov ≥0.83 的字段；低覆盖字段除非机制独立，不再占槽。
4. **TO 贴地板**：#2/#6 跌破 1%（0.92%/0.96%）。这类季频字段 + `hump 0.01` 会把换手压到闸线下；
   但 TO<12.5% 时 F 与 TO 无关，**先不当作机制已死**；若后续候选 S/F 已过而只差 TO，优先去掉 `hump` 而不是加 decay。
5. **批次结论**：other685 未见底，但「原始水平 / 现金收益率」路径已用尽（8 条里 6 条）。批 2 转向
   **百分位 × 加速度 × 修正形态**，并对最强字段 #8 做一次测量口径复测。

### 4.2 批 2 预注册（M09–M16；已发批 `3yQipVdHb5isbwC1eOPCHrwx`）

设置与批 1 完全一致（SUBINDUSTRY / decay 5 / trunc 0.08），保证跨批可比。
壳不变；8 条真实字段 `preflight_expressions` 全过（`unknown_fields=["std"]` 仍为已知误报，`vector_fields=[]`）。

| # | 机制 | 字段 | 方向 | SIG | 设计依据 |
|---:|---|---|---|---|---|
| M09 | 增长百分位自归一 | `blended_growth_rate_industry_percentile` | 正 | `ts_zscore(..., 252)` | 批 1 #8 的测量口径复测（2Y 已过、只缺 S/F；先归一再判） |
| M10 | 增长加速度（SmartEstimate） | `smartest_growth_next_vs_this_year_earnings` | 正 | 原字段 | 预期增速的二阶变化；0 αC，cov 0.9677 |
| M11 | 增长百分位加速度 | `growth_next_year_industry_percentile_earnings - growth_this_year_industry_percentile_earnings` | 正 | 两字段差 | 同口径（0–100）相减，跨行业可比；避免量纲 |
| M12 | GARP（PEG 行业百分位） | `peg_ratio_industry_percentile_smartest_f12m` | 正（低 PEG 好） | `-1 *` | 增长/估值合成，单字段自带配比；cov 0.8453 |
| M13 | SmartEstimate vs 共识分歧 | `forward_pe_ratio_mean_fy1 / forward_pe_ratio_smartest_fy1` | 正 | `trade_when(smart PE>0, 比值−1, -1)` | 聪明分析师 EPS 高于共识 ⇒ 比值>1；同集两字段 |
| M14 | 盈利收益率行业百分位 | `earnings_yield_industry_percentile_fy1` | 正 | 原字段 | 批 1 水平族未测「百分位形态」；检验百分位能否救价值 |
| M15 | ROI 趋势（区间 1） | `oth685_roitran1` | 正 | 原字段 | 0 αC 未开采；字段本身已是变化量，不再差分 |
| M16 | 增长百分位修正 | `blended_growth_rate_industry_percentile` | 正 | `ts_av_diff(..., 63)` | 批 1 #8 是水平，修正量是另一机制（预期上调） |

⚠ M13 的分母用 `+ 0.01` 防零，`trade_when` 第三参 `-1` 保证只在正 PE 样本内持仓；
若 VERIFY 报单位告警或出现极值失真，M13 先判测量问题、不判机制死。

### 4.3 批 2 收批（8/8 COMPLETE；0 颗过闸；最强 S1.01）

| # | 机制 | alpha | S | F | 2Y | SUB | risk-neut S | TO | fail |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| M09 | 增长百分位自归一 | `npA8Oxjx` | **1.01** | 0.55 | 1.39 | **0.77** | 0.48 | 0.97% | S/F/TO/2Y |
| M10 | 增长加速度（SmartEstimate） | `A1Q7OjpY` | 0.09 | 0.02 | −0.20 | 0.16 | 0.10 | 1.04% | S/F/2Y |
| M11 | 增长百分位加速度 | `d5KRlkMK` | 0.83 | 0.41 | **1.51** | 0.72 | 0.34 | 1.01% | S/F/2Y |
| M12 | GARP（PEG 百分位，负号） | `3qjenQKO` | 0.45 | 0.18 | 0.98 | −0.04 | −0.12 | 0.98% | S/F/2Y/SUB/TO |
| M13 | SmartEstimate vs 共识分歧 | `wp9EJKr1` | 0.96 | 0.44 | 0.17 | 0.61 | **0.63** | 1.44% | S/F/2Y（+UNITS 警告） |
| M14 | 盈利收益率行业百分位 | `1YjznkMK` | 0.71 | 0.42 | 1.15 | 0.25 | **0.72** | 1.05% | S/F/SUB/2Y |
| M15 | ROI 趋势 tran1 | `pwvK1Y9o` | 0.62 | 0.27 | 0.71 | −0.03 | 0.29 | 0.94% | S/F/2Y/SUB/TO |
| M16 | 增长百分位修正 Δ63 | `vROvJwWr` | 0.99 | 0.52 | **1.57** | **0.75** | 0.43 | 1.03% | S/F/2Y（差 0.01） |

**归因（写死）**：

1. **同一字段的三种形态**：Δ63 修正（0.99/2Y1.57/SUB0.75）≈ 自身 z 分（1.01/1.39/0.77）
   > 原始水平（0.88/2Y1.72/SUB0.44）在 S/SUB 上；水平形态 2Y 最高但 S 最低。
   ⇒ 修正量给全期强度、水平给近期强度，**两者都停在 S≈1.0**，说明瓶颈不在形态。
2. **二阶差分抹平信号**：M10（SmartEstimate 增速，本身已是加速度口径再直接排序）S0.09/2Y−0.20，
   与 analyst surprise 族「二阶差分把方向稀释」的教训一致 ⇒ 增长加速度不做二阶处理。
3. **PEG 口径在 USA 不成立**：M12 S0.45 / SUB−0.04 / risk-neut −0.12，且 TO 跌破 1% ⇒ 判弱。
4. **M13 是唯一「非风格」候选**：risk-neut 0.63（全数据集最高），但 2Y 0.17 ⇒ 近两年失效；
   UNITS 警告来自 `−1` 常数（`subtract` 期望 CSPrice 单位），已改为无常数比值 `mean_PE/smart_PE`（单调等价）。
5. **M14 的大中盘有效、但 SUB 结构性失败**：risk-neut 0.72 最高，SUB 0.25 < 0.43×S ⇒ 小盘反向，
   SUBINDUSTRY 中性化下不可救，判弱。
6. **批次结论**：16 条表达式（两批）内最高 S1.01/F0.55；字段形态、加速度、PEG、ROI 全部试过且均弱。
   ⇒ 下一个判断点不是继续换字段，而是**设置档**：other 类别缺省 SUBINDUSTRY 可能过度剥离了增长预期成分。

### 4.4 批 3：设置对照（同表达式、只换中性化；已发批 `4rMJln2eM4YS9P9moQfTea7`）

**动机（归因驱动，不是扫参）**：analyst 战役同族慢信号（目标价/修正）在 **STATISTICAL** 中性化下
拿到 S2.07/1.94，在 REVERSION_AND_MOMENTUM 下只有 1.6–1.7；本集批 1/2 全部在 SUBINDUSTRY 下 S≤1.01。
⇒ 用**相同 8 条表达式**换 STATISTICAL，做单变量对照：能直接回答「S 低是信号弱还是中性化过度」。
设置：EQUITY/USA/TOP3000/D1/**STATISTICAL / decay 5 / trunc 0.08**（其余与批 1/2 完全一致）。

| # | 沿用 | 表达式来源 |
|---:|---|---|
| 1 | M09 增长百分位 z 分 | 批 2 `npA8Oxjx` |
| 2 | M16 增长百分位 Δ63 | 批 2 `vROvJwWr` |
| 3 | M13 SmartEstimate 分歧（去掉 ±1 常数，修 UNITS） | 批 2 `wp9EJKr1` |
| 4 | M08 增长百分位水平 | 批 1 `kqJZmJ3g` |
| 5 | M11 增长百分位加速度 | 批 2 `d5KRlkMK` |
| 6 | M07 自身历史 P/E（负号） | 批 1 `P0MOlMpw` |
| 7 | M02 现金 ROIC 水平 | 批 1 `0mjMQj8v` |
| 8 | M14 盈利收益率百分位 | 批 2 `1YjznkMK` |

**判据（写死）**：任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥0.75 且 fail=0 ⇒ 立即相关性实测；
若全部 S < 1.2 ⇒ **other685 判弱并转下一个未点亮塔数据集**（写明理由：16 条 × 个字段形态 + 设置对照均达不到强度）；
若落在 1.2–1.58，只对该机制做一次结构性改进，不扩同族。

### 4.5 批 3 收批与数据集裁决（8/8 COMPLETE；全部 S<1.2 ⇒ **other685 判弱**）

| # | 机制 | alpha | S | F | 2Y | SUB | TO | 对照（SUBINDUSTRY） |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | M09 增长百分位 z 分 | `npA8O2pq` | 0.79 | 0.29 | 1.30 | 0.38 | 3.51% | S1.01/SUB0.77/TO0.97% **更差** |
| 2 | M16 增长百分位 Δ63 | `0mjMKEOp` | 0.71 | 0.24 | 1.35 | 0.34 | 3.43% | S0.99/SUB0.75/TO1.03% **更差** |
| 3 | M13 SmartEstimate 分歧 | `78onK175` | 0.85 | 0.31 | 0.33 | **0.96** | 3.63% | S0.96/SUB0.61；S 降、SUB 升 |
| 4 | M08 增长百分位水平 | `E5VerE1r` | 0.59 | 0.19 | 0.83 | 0.31 | 3.91% | S0.88/2Y1.72 **更差** |
| 5 | M11 增长百分位加速度 | `Vkd3YPV0` | 0.26 | 0.05 | 1.24 | 0.24 | 3.74% | S0.83 **更差** |
| 6 | M07 自身历史 P/E | `YPxgW06o` | 0.75 | 0.26 | 1.74 | 0.64 | 3.67% | S0.74/2Y1.31；2Y 抬、S 平 |
| 7 | M02 现金 ROIC | `bl8dWqkZ` | 0.51 | 0.15 | 0.36 | −0.18 | 4.11% | S0.79/SUB0.19 **更差** |
| 8 | M14 盈利收益率百分位 | `d5KRl0XE` | **1.02** | 0.45 | **1.83** | 0.36 | 4.25% | S0.71/2Y1.15/SUB0.25；S、2Y 升 |

**归因与裁决**：

1. **STATISTICAL 不适用于本集**：同表达式换中性化后 7/8 条 S 下降（幅度 0.2–0.57），
   TO 从 ~1% 抬到 3.4–4.3%、returns 反而下降（margin 0.0007–0.0012 vs 0.004–0.008）
   ⇒ SUBINDUSTRY 的持仓集中度本身就是本集收益来源，analyst 战役的 STATISTICAL 先验**不能跨数据集迁移**。
2. **唯一改善是 M14（EY 百分位）**：S0.71→1.02、2Y1.15→1.83，但 SUB 0.36 仍破（limit 0.44），
   且其 SUBINDUSTRY 版 SUB 只有 0.25 ⇒ 小盘反向是结构性的，换中性化只放大了大中盘腿，不能交付。
3. **M13 仍是「非风格」候选**（SUB 0.96），但 2Y 0.33 说明近几年失效，且 S0.85 离 1.58 太远。
4. **裁决**：按 §4.4 预注册判据（全部 S<1.2）⇒ **other685 判弱，停止扩批**。
   证据链：24 条表达式（3 批）= 6 个字段株 × 水平/修正/z 分/加速度/复合形态 + 2 种中性化；
   最高 S1.02（还伴 SUB 破闸），无一条同时满足 S/F/2Y/SUB。字段族本身不提供 ≥1.58 的截面强度。
   **该集只保留为「组合腿/条件门控」的备选字段池，不再单独作为主数据集开挖。**
5. 转下一个**未点亮塔**数据集；选择依据与画像另行建档。`other` 塔仍为 0，但不等于必须继续在本集消耗配额。

## 5. 论坛/文献证据（可复用）

1. **ARM 百分位形态决定 2Y**（论坛帖 `43579597796247`，31 票，IND 实证）：同一修正信号用原始修正量做窗口扫描 2Y 只到 1.3–1.4，
   换成 StarMine ARM 百分位形态后 2Y 2.50 ⇒ 「修近年衰减先换字段呈现形态，比调窗口优先」。
   本数据集 §2.2 的 `*_percentile*` 字段正对应此形态，M08 采用。
2. **快慢错配模板**（同帖）：`正交化(ts_rank(快修正 / 慢基线, 504), 对手语义腿)`；快窗 3–7、慢窗 66。
   本数据集无情绪腿，暂不套用；若 M08 增长百分位信号过强但 2Y 不足，可把“增长快 / 估值慢”做成同类错配（见后续批）。
3. **质量的两种定价口径要分开测**（Novy-Marx 2013；Asness/Frazzini/Israel/Moskowitz 2015）：
   ROIC 水平与现金流收益率不是同一因子，故 M02/M03/M04 并列而非取一。

## 6. 风险与预判

- **估值族拥挤**：`diff_current_vs_hist_pe_ratio` 已有 89 颗 alpha，prod 相关性可能高；#7 是首次试，若 prod > 0.7 直接放弃该字段。
- **SUB 墙**：低覆盖财务比率天然偏小盘；若 SUB < 0.43×S，先按已验证的测量口径（`ts_zscore` 自波动归一）复测，不要先换字段。
- **CW 风险**：`oth685_cfroi_3`（0.5939）、`oth685_cfroitrn`（0.5695）、`oth685_2_igaigr`（0.595）覆盖偏低，
  若出现 `CONCENTRATED_WEIGHT`，先补内层 `ts_backfill(...,252)` 或加 `group_backfill`，不判机制死。
- **换手**：financial ratio 字段更新频率低，TO 可能 <1% ⇒ 触发 LOW_TURNOVER；若是，按「去壳诊断批」先确认字段是否静态。
