# DEU 补货轮：字段画像与实测台账（2026-11-07 夜·二轮）

> region 固定 **DEU**，基线设置 TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 /
> nanHandling OFF / pasteurization ON / unitHandling VERIFY / maxTrade OFF。
> 并发严格 ≤2。prod / self 相关性只走 MCP。

---

## 一、★ 纠错：交付件从「6 颗」更正为「5 颗」

`xArYWKgg` 的 **self 相关实测 = 0.9976**（对标 ACTIVE 件 `LLM93nGa`，机制完全重叠）⇒ **废件，剔除**。

由此确立判读顺序（本轮正式采用）：

> **pyramids 判禁混 → self → prod → 互相关**

理由：本地库 141 颗 `prod=null` 且从未提交的存量件，死因基本都是 self 已死。
先测 prod 要等平台 1–5 分钟（常 240s 超时），而 self 走本地增量缓存**秒回**。

---

## 二、★★★ 工具坑：`batch_status` 的 `child_count` 恒为 0（本轮最大陷阱）

现象：NW18-A（`3lT7qy9Px4Rf9hA1dyFf7PdX`）连续多轮轮询 `batch_status` 全部返回
`child_count: 0, terminal: 0, parent_status: null`，据此我误判批次僵死并弃置。

**实际该批次早已 COMPLETE，8 个子 alpha 全部就绪。**

**正确轮询方式**：

```text
lookINTO_SimError_message({ locations: [
  "https://api.worldquantbrain.com/simulations/<multisim_id>",
  "https://api.worldquantbrain.com/simulations/<child_sim_id>", ...
]})
```

- 打在 **multisim id** 上 → 返回 `raw.children` = **子模拟 id 列表**（不是 alpha id）与 `raw.status`。
- 打在 **child sim id** 上 → 返回 `alpha` = 真正的 alpha id。
- 在跑中的返回 `raw.progress`（0.0–1.0）。

⚠️ 直接把 `raw.children` 当 alpha id 传给 `batch_get_alpha_metrics` 会 **8/8 全 404**。
必须先用 child sim id 解析出 alpha id 再收割。

---

## 三、news18 数据集判定：封盘

- 平台画像：70 字段，全 VECTOR / SYMBOL；单公司事件组 cov 0.6925–0.6965，多公司事件组 cov **0.9788**。
- 批次 NW18-A（8 条，`vector_neut` 无需，preflight `valid=true / unknown_fields=[]`），全 SUBINDUSTRY / decay 4 / trunc 0.08。

| # | alpha | 表达式核心 | 经济含义 | S | F | 2Y | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | pwdZb2Rb | `group_rank(ts_mean(vec_avg(nws18_multiple_comp_ssc),22),sector)` | 综合情绪水平 | −0.12 | −0.03 | −0.22 | 0.114 | 3 |
| 2 | xArW7Lbm | `group_rank(ts_delta(vec_avg(nws18_multiple_comp_ssc),22),sector)` | 情绪变化 | 0.08 | 0.01 | −0.67 | **0.972** | 4 |
| 3 | 6XdJ6WKK | `group_rank(ts_mean(vec_avg(nws18_multiple_comp_nip),22),sector)` | 叙事冲击 | 0.05 | 0.01 | −0.09 | 0.119 | 4 |
| 4 | **j2Yxkpe5** | `-group_rank(ts_mean(vec_avg(nws18_mltpl_cmp_event_simildays),66),sector)` | 事件新颖度 | **0.65** | 0.33 | **1.67** | 0.069 | 2 |
| 5 | omErjbo2 | `group_rank(ts_mean(vec_avg(multi_entity_story_event_count),22),sector)` | 关注度 | 0.36 | 0.14 | 0.71 | 0.095 | 3 |
| 6 | omErjbol | `-group_rank(ts_std_dev(vec_avg(nws18_multiple_comp_ssc),66),sector)` | 情绪分歧 | 0.34 | 0.14 | 0.87 | 0.054 | 4 |
| 7 | QPvgRxYW | `group_rank(ts_mean(vec_avg(nws18_multiple_comp_ghc_lna),22),sector)` | 分析师推荐变化 | −0.27 | −0.09 | −1.12 | 0.128 | 3 |
| 8 | 58EeKmjX | `-group_rank(ts_mean(vec_avg(nws18_multiple_comp_qmb),66),sector)` | 社论情绪 | 0.10 | 0.02 | 0.47 | 0.056 | 4 |

**结论：news18 封盘。** 最强 S 0.65，距 1.58 线差 0.93。
唯一亮点：`j2Yxkpe5`（事件新颖度）**2Y = 1.67 已过 2Y 硬闸**且 RA 只有 2，说明「事件新颖度」方向在 DEU 有真实的长周期效力，
但**水平强度不足**。若后续要救，只能靠加腿（但禁止混信号调参）或换几何，不在本轮预算内。

---

## 四、analyst93 数据集：本轮最重要新发现

**平台画像**：100 字段，**全部 VECTOR**，cov **0.6328–0.6459**，alphaCount 0–52。
category = **ANALYST**（在禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL} **之外**）⇒ 单数据集 ATOM 合法且**不占禁混配额**。

### 4.1 字段族结构（4 个族 × 两套口径）

命名规律 `anl93_<族>_<主体>_<指标>`：

| 族 | 含义 | 字段数 |
|---|---|---:|
| `accuracy` | 预测命中概率 | 21 |
| `consistency` | 预测误差负标准差（越大越稳定） | 4 |
| `correv` | 修正方向的命中率 | 4 |
| `profitabilityprev` | 跟随该分析师预测的历史日均收益 | 29 |
| `recprofitabilityprev` | 跟随该分析师**推荐**的历史日均收益 | 29 |

`主体` 有两种：`analyst` = 单分析师级，`estimator` = 在该股票上的汇总口径。

### 4.2 零拥挤字段（alphaCount = 0，从未被人用过）

`anl93_estimator_accuracy2`、`anl93_estimator_consistency`、`anl93_estimator_correct_forecast_times1/2`、
`anl93_estimator_relative_accuracy3/4`、`anl93_estimator_relative_ratio2`、`anl93_estimator_relative_consistency2`、
`anl93_estimator_profitability1_120d`、`anl93_estimator_profitability2_60d`、
`anl93_recprofitabilityprev_estimator_profitability1_20d`、`..._relative_profitability3/4`

### 4.3 ★ 字段名陷阱（已踩）

`anl93_estimator_profitability2` / `anl93_estimator_profitability1_120d` **不存在**。
真实名字带族前缀：`anl93_profitabilityprev_estimator_profitability2`、`anl93_profitabilityprev_estimator_profitability1_120d`。
`preflight` 会以 `unknown_soft`（reason: "dataset-prefixed field not found"）报出来，**必须读 unknown_soft，不能只看 valid=true**。

### 4.4 ANALYST93-A 波次（`3oK5rp3XH4De9Nx158zPDRar`，8 条，在飞）

| # | 模板 | 表达式 | 经济机制 |
|---|---|---|---|
| 1 | 技能水平 | `group_rank(ts_backfill(vec_avg(anl93_profitabilityprev_estimator_profitability2),66),sector)` | 被强分析师覆盖 ⇒ 未来超额收益 |
| 2 | 技能改善 | `group_rank(ts_delta(ts_backfill(vec_avg(anl93_profitabilityprev_estimator_profitability2),66),22),sector)` | 覆盖结构改善的边际信息 |
| 3 | 准确度分歧 | `-group_rank(ts_std_dev(ts_backfill(vec_avg(anl93_analyst_accuracy1),66),66),sector)` | 分歧度低 ⇒ 定价共识（低分歧溢价） |
| 4 | 修正命中率 | `group_rank(ts_backfill(vec_avg(anl93_estimator_correct_revision_ratio),66),sector)` | 修正方向可信度 |
| 5 | 预测一致性 | `group_rank(ts_backfill(vec_avg(anl93_estimator_consistency),66),sector)` | 误差波动低 ⇒ 信息质量高（**零拥挤**） |
| 6 | 覆盖强度 | `group_rank(ts_sum(ts_backfill(vec_avg(anl93_estimator_total_forecast_times1),66),252),sector)` | 分析师注意力/覆盖度 |
| 7 | 命中效率 | `group_rank(divide(ts_backfill(vec_avg(anl93_estimator_accuracy1),66),add(ts_backfill(vec_avg(anl93_estimator_total_forecast_times1),66),1)),sector)` | 每单位预测量的命中数 |
| 8 | 技能稳定性 | `group_rank(ts_ir(ts_backfill(vec_avg(anl93_profitabilityprev_estimator_profitability1_120d),66),252),sector)` | 技能的信噪比而非水平 |

算子数 4–6，全部 ≤12 上限。preflight `valid=true / unknown_soft=[] / platform_field_count=7`。

---

## 五、institutions1 数据集：由 ACTIVE 件反向定位

**平台画像**：7 字段，全 VECTOR，cov **0.2289**（低，但用户口径允许动态调整，只要求近十年有数据），
alphaCount 1–19（极低拥挤）。category = **INSTITUTIONS**（禁混集合之外）。

### 5.1 情报来源：ACTIVE 件 `2rmGAPqN`（2026-10-09 提交）

- 指标：S **1.81** / F 1.48 / 2Y **2.55** / sub 1.3 / self 0.0327 / prod 0.6292 / `checks.fail=[]` / `ra.failed_ra_count=0`
- pyramids = `["DEU/D1/INSTITUTIONS", "DEU/D1/OTHER"]`（INSTITUTIONS 集合外 × OTHER 集合内 ⇒ 合法，但计入 ≤5 配额）
- 设置：DEU/TOP500/D1/decay 4/**FAST 中性化**/trunc 0.08/nanHandling **ON**
- 核心：`inst1_valueeur / inst1_holdings`（单位持仓价值）+ `inst1_tradesignificance > 2.0` 门控 + `oth455` 的 GROUP 字段当分组轴

⇒ **推翻「institutions 塔全封」**：`fund_holdings_panel` 弱 ≠ institutions 塔弱。
塔级判死不得由单数据集结果外推（与 insiders 塔同理）。

### 5.2 INST1-A 波次（`2AfnVoboZ4lucEHporI75Z5`，8 条，在飞）

| # | 模板 | 表达式 | 经济机制 |
|---|---|---|---|
| 1 | 流量动量 | `group_rank(ts_delta(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),22),sector)` | 建仓速度的二阶变化 |
| 2 | 显著性加权流 | `group_rank(ts_sum(multiply(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),vec_avg(inst1_tradesignificance)),66),sector)` | 重要交易权重更高 |
| 3 | 股份流占持仓 | `group_rank(ts_sum(divide(vec_sum(inst1_shares),add(vec_sum(inst1_holdings),0.0001)),66),sector)` | 换手强度（不含价格） |
| 4 | 买入持续性 | `group_rank(ts_mean(divide(vec_sum(inst1_valueeur),add(abs(vec_sum(inst1_valueeur)),0.0001)),66),sector)` | 净买入期数占比（符号持续性） |
| 5 | 流量分歧 | `-group_rank(ts_std_dev(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),66),sector)` | 建仓稳定性（低波动优） |
| 6 | 成交价相对历史 | `group_rank(divide(vec_avg(inst1_price),ts_mean(vec_avg(inst1_price),252)),sector)` | 机构在自身历史高价区买入 ⇒ 估值自信 |
| 7 | 事件广度 | `group_rank(ts_mean(vec_count(inst1_valueeur),66),sector)` | 参与机构家数（拥挤/共识） |
| 8 | 流量标准分 | `group_rank(ts_zscore(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),252),sector)` | 相对自身 5 年常态的异常建仓 |

算子数 6–8，全部 ≤12。preflight `valid=true / unknown_fields=[] / platform_field_count=5`。

---

## 六、insiders1 数据集：下一批候选（待派发）

**平台画像**：8 字段，全 VECTOR，cov **0.5343**（比 institutions1 高 1.3 倍），alphaCount 1–11（极低拥挤）。
category = **INSIDERS**（禁混集合之外）。字段几何与 institutions1 **完全同构**（holdings / price / shares /
tradesignificance / value / valueeur / 币种码），但数据实体不同（内部人 vs 机构）⇒ 天然对照实验。

**动机**：`insider_agg_matrix`（同塔）已全灭（最强 S 0.89），但按「塔级判死不得由单数据集外推」，
insiders1 必须独立验证。内部人买入是全金融文献中最稳固的异象之一
（Lakonishok & Lee 2001；Cohen–Malloy–Pomorski 2012「routine vs opportunistic insiders」：
**机会型内部人**的买入预测力远强于常规型，且强度随交易金额/职位显著性上升）。

**预备模板方向**（结构上刻意区别于 INST1-A，以通过对照实验获得独立信息）：
flow-to-position 比（`valueeur / (holdings × price)`）、集群笔数、显著性加权净额、
短期减长期加速度（`ts_mean22 − ts_mean252`）、符号持续性、`ts_ir` 信噪比、
成交价溢价、`trade_when(显著性≥2)` 门控。

---

## 七、本轮封盘清单（勿重试）

| 数据集 / 路线 | 结论 | 最强证据 |
|---|---|---|
| `event_ml_signals`（104 字段） | **DEU 全字段 coverage = 0**，无数据 | 平台画像 |
| `news18` | 封盘 | S 上限 0.65（8 条） |
| `model264` 的 `_l1`/`_l2` 连续变体 | 封盘，只有 `_class` 分档有效 | S 上限 0.64（8 条） |
| `fund_holdings_panel` | 封盘 | S 上限 0.57（8 条） |
| `insider_agg_matrix` | 封盘（但**不**代表 INSIDERS 塔封盘） | S 上限 0.89（8 条） |
| MODEL 族新增 | **容量硬顶 3 颗，已满** | `max_mutually_below_subset_size=3` |

---

## 八、交付状态

**合格 5 颗**（全闸通过、全部 UNSUBMITTED）：

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | self | prod |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | mLox6Mg2 | sentiment7 + sentiment27 | SENTIMENT | 2.05 | 1.71 | 2.53 | 0.147 | 0.030 | 0.6935 |
| 2 | E56pROb9 | model216 + starmine | MODEL | 1.79 | 1.70 | 2.03 | 0.067 | 0.600 | 0.6859 |
| 3 | QPvzNNGG | predictive_starmine | MODEL | 1.70 | 1.30 | 2.18 | 0.155 | 0.678 | 0.6777 |
| 4 | LLMzYrZe | predictive_starmine | MODEL | 1.61 | 1.16 | 1.69 | 0.153 | 0.670 | 0.6697 |
| 5 | MPY9VNY9 | shortinterest3 | SHORTINTEREST | 1.59 | 1.26 | 2.36 | 0.036 | 0.270 | 0.5986 |

严格单数据集 ATOM = **3 颗**（QPvzNNGG / LLMzYrZe / MPY9VNY9）。目标 10 颗 ⇒ **缺口 5 颗**。

⚠️ mLox6Mg2 的 prod 0.6935 已贴近 0.7 红线，提交前须 `refresh=True` 终验（工具自述 prod 2–3 天可漂 0.58→0.98）。
