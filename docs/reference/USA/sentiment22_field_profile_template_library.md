# sentiment22 — 字段画像与模板库（USA / TOP3000 / D1 / MATRIX）

> 生成时间：2026-10-29
> 数据来源：`tools/scan_fields.py` 平台实拉，`tracking/USA/reference/usa_sentiment22_fields.json`
> 拉取完整性：`field_count=210 / platform_count=210 / complete=True`（all-or-error 校验通过）

---

## 1. 数据集画像

| 项 | 值 |
|---|---|
| 平台 id | 559（本地 `datasets.id`） |
| category | **SENTIMENT** |
| 塔位乘数 | **1.4×**（与 OTHER 并列最高） |
| 本季度 USA 已点亮 | **0 颗** |
| 字段数 | 210，全部 MATRIX |
| 平均覆盖率 | **0.9996**（min 0.9992 / 中位 1.0000） |
| 覆盖档 | 210/210 字段 cov ≥ 0.95，**无覆盖墙** |
| alphaCount 合计 | **692**，字段级 max 20，中位 ~2 |
| virgin 字段（alphaCount=0） | **59 / 210** |
| userCount max | 17 |
| 拥挤度判读 | 极低。对比 `sentiment1` 14878 / `sentiment27` 6680 / `sentiment23` 1571 → 本集是 SENTIMENT 塔内最干净的可用样本 |

**为什么选它而不是 sentiment23**：两者字段结构完全相同（210 字段同构），但
`sentiment23` alphaCount 1571（仅 12 个 virgin）、`sentiment22` 692（59 个 virgin）。
同样的信息量，拥挤度差 2.3×。`news_transformer_scores`（VS 5.0）覆盖率只有 0.6923–0.8810
且按 pre/main/post 时段切分，覆盖墙明显，降为第二优先级。

---

## 2. 字段结构（决定性：正好是「极性配对」的教科书形状）

210 字段 = **5 个模型变体 × 3 个极性 × 7 个统计量（105）+ 15 个时间序列聚合**，
再加一套 base 变体的镜像命名。

### 2.1 三根正交轴

| 轴 | 取值 | 含义 |
|---|---|---|
| **变体（variant）** | base（无前缀）/ `2` / `3` / `4` / `5` | 5 个独立情绪模型（AMR model 2–5）。**跨变体分歧是同数据集里唯一真正的第二个自由度** |
| **极性（polarity）** | `pos` / `neut` / `neg` | 正面 / 中性 / 负面情绪 |
| **统计量（statistic）** | `mean` / `median` / `min` / `max` / `std` / `conf_low` / `conf_up` | 中心趋势、稳健中心、尾部、二阶矩、置信区间端点 |

### 2.2 命名规则（写错就白烧一次仿真）

```
# base 变体：无下划线分隔 + 数字后缀（后缀不可省）
snt22pos_mean_270    snt22neg_mean_253    snt22neut_mean_267
snt22pos_max_257     snt22neg_max_255
snt22pos_conf_up_273 snt22neg_conf_low_260
snt22pos_median_258  snt22neg_median_256
snt22pos_min_266     snt22neg_min_268
snt22neut_conf_low_269  snt22neut_conf_up_261  snt22neut_max_254  snt22neut_min_264

# variant 2/3/4/5：下划线分隔，无后缀
snt22_2pos_mean   snt22_2neg_mean   snt22_2neut_mean
snt22_2neg_std    snt22_2pos_std
snt22_2pos_conf_up  snt22_2neg_conf_low
snt22_2pos_max    snt22_2neg_min
```

⚠ **base 变体没有 `std` 字段**（`std` 只存在于 variant 2/3/4/5）。
跨模型分歧必须用 `snt22_2*` 与 `snt22*` 两组配对。

### 2.3 派生恒等式（决定哪些模板是「伪多样性」）

```
conf_up = mean + 1.96 × std
conf_low = mean − 1.96 × std
⇒ conf_up − conf_low = 3.92 × std          ← 区间宽度是纯分歧度，与 std 共线
⇒ (conf_up + conf_low) / 2 = mean          ← 端点均值只是 mean 的仿射变换
```

**判据**：`ts_zscore(conf_up − conf_low)` 与 `ts_zscore(std)` 是同一个信号，同批跑属浪费。
真正不同的用法是**跨极性跨度** `pos_conf_up − neg_conf_low`（乐观上界减悲观下界，
同时吃到两端的分布宽度与中心位移，是 std 无法表达的）。

### 2.4 时间序列聚合族（`dts`）

| id 形状 | 语义 | 注意 |
|---|---|---|
| `snt22_2dts_gen` / `snt22_3dts_gen` … | N 日（2/3/4/5）时间序列 **general sentiment（水平）** | 变体族是**水平** |
| `snt22_2dts_sop` / `snt22_4dts_sop` … | N 日时间序列 **sum of positive sentiment** | |
| `snt22_2dts_tuen` / `snt22_5dts_tuen` … | N 日时间序列 **total of neutral sentiment** | |
| `snt22dts_gen_265` / `snt22dts_sop_263` / `snt22dts_tuen_271` | **standard deviation**（base 族是 std，不是水平！） | ⚠ 同名字根、不同语义，混用会静默出错 |

⇒ `dts` 族自带 2/3/4/5 日窗口，是**数据集内建的多尺度**，可省掉表达式里的窗口扫描。
但 base 族（`snt22dts_*`）是 std，与变体族不同义。

---

## 3. 经济机制（每条模板对应一个可证伪假设）

| # | 机制 | 文献锚点 | 可证伪预测 |
|---|---|---|---|
| M1 | **媒体语调水平** | Tetlock (2007) *Giving Content to Investor Sentiment* | 负语调 → 下期负收益；正负差为正 → 正收益 |
| M2 | **意见分歧 → 高估 → 低回报** | Miller (1977); Diether–Malloy–Scherbina (2002) | 情绪 std / 区间宽度越高 → 未来收益越低 |
| M3 | **新闻慢速融入** | Hong–Torous–Valkanov; 「Slowly Incorporated News」论坛帖 | 累积语调（ts_sum 长窗）比瞬时语调更预测收益 |
| M4 | **注意力/关注冲击 → 短期买压后反转** | Da–Engelberg–Gao (2011) | 中性情绪占比高 = 信息真空 = 低关注，与收益负相关 |
| M5 | **极性耦合（正负情绪同向波动）** | 论坛「相关性算子 + FAST 中性化」实践 | 正负情绪相关性异常 → 定价错配 |
| M6 | **模型分歧（跨建模方法不一致）** | 本数据集特有（AMR model 2 vs base） | 模型间分歧大的股票 → 不确定性溢价/折价 |

---

## 4. 波 203 模板库（10 个结构互异模板）

差异落在**骨架几何 / 矩（水平·一阶差分·二阶）/ 分组轴 / 非线性变换 / 字段轴**五个维度，
不是换窗口或换常数。

| # | 模板 | 表达式 | 机制 | 结构差异点 |
|---|---|---|---|---|
| **T1** | 极性差·水平·zscore | `ts_zscore(ts_mean(subtract(snt22pos_mean_270, snt22neg_mean_253), 22), 252)` | M1 | 基线：一阶矩 + 双极性差分 |
| **T2** | 极性比·有界 | `ts_zscore(ts_mean(divide(snt22pos_mean_270, add(snt22pos_mean_270, snt22neg_mean_253)), 22), 252)` | M1 | 商式而非差式；对情绪总量归一并消除量纲，横截面上与 T1 不同排序 |
| **T3** | 二阶矩·分歧度 | `ts_zscore(ts_mean(snt22_2neg_std, 22), 252)` | M2 | 换到 `std` 字段（二阶矩），非中心趋势 |
| **T4** | 跨极性跨度 | `ts_zscore(ts_mean(subtract(snt22_2pos_conf_up, snt22_2neg_conf_low), 22), 252)` | M2 | 双端点构造：同时吃分布宽度与中心位移，**不可由 std 线性表示** |
| **T5** | 尾部极值差·ts_rank | `ts_rank(subtract(snt22pos_max_257, snt22neg_max_255), 252)` | M1+M2 | 极值（max）而非均值；时间算子换成 `ts_rank`（秩几何） |
| **T6** | 极性耦合·相关性算子 | `reverse(ts_zscore(ts_corr(snt22pos_mean_270, snt22neg_mean_253, 66), 252))` | M5 | **双变量** `ts_corr`，论坛 94 赞帖明确的 sentiment 专用族；`reverse` 定向 |
| **T7** | 慢速累积融入 | `ts_zscore(ts_sum(subtract(snt22pos_mean_270, snt22neg_mean_253), 66), 252)` | M3 | `ts_sum` 累积而非 `ts_mean` 平滑 ⇒ 信息存量而非信息速率 |
| **T8** | 语调一阶差分 | `ts_zscore(ts_av_diff(ts_mean(subtract(snt22pos_mean_270, snt22neg_mean_253), 22), 66), 252)` | M3 | 差分几何：语调的**变化**而非水平 |
| **T9** | 跨模型分歧 | `ts_zscore(ts_mean(subtract(snt22_2pos_mean, snt22pos_mean_270), 22), 252)` | M6 | **字段轴切换**：同极性跨变体相减，与所有单变体模板正交 |
| **T10** | 中性真空度 | `reverse(ts_zscore(ts_mean(snt22_2neut_mean, 66), 252))` | M4 | 用 `neut` 轴（信息真空），与 pos/neg 语义独立；`reverse` 使其为「低中性 = 高关注」 |

### 4.1 ATOM 合规性
10 条全部**单数据集**（`sentiment22`），不含 `returns` / `close` / `adv20`，全部满足 ATOM 定义。
SENTIMENT 类别不在 {PV, MODEL, OTHER} 内 ⇒ **不触碰三塔禁混硬约束**，也不占 trio×非trio 的 ≤5 配额。

### 4.2 窗口依据
只用标准窗口 `22 / 66 / 252`：22 = 月、66 = 季度、252 = 年。无自定义极端窗口。

---

## 5. 论坛取证（用户要求「用机制前先查论坛」）

| 帖 id | 赞 | 结论 | 落地方式 |
|---|---|---|---|
| `39845230299927` | 73 | **极性配对**：`diff = pos − neg`、`log_diff`、`ratio = pos/(pos+neg)`，再套一/二阶单变量算子，可造差异化 ATOM 且 **PC 更低** | T1（diff）、T2（ratio）直接落此配方 |
| `40847481080087` | 94 | 点亮 sentiment/news 塔的实战结论：**相关性算子 + FAST 中性化** 组合最适合 sentiment 数据 | T6 用 `ts_corr`；波 203b 整批用 `FAST` 中性化做对照 |
| `43211291823511` | 96 | 「双字段 Sentiment：四个地区的组合方法」真身用了 `snt22_2neut_conf_low_379`、`snt22_3neg_conf_low_343` —— **conf 端点字段确实可用于出货 alpha** | T4 用 conf 端点（但用跨极性跨度而非单端点） |
| `35294898626711` | 51 | 情绪数据用 `ts_covariance` 建模板 | 备选（本波未用，留在 T6 的邻域） |
| `19514322953495` | 7 | 「Slowly Incorporated News」：`(s − ts_mean(s,21)) / ts_std_dev(s,21)` | T1/T7 的 zscore 几何来源 |
| `43622610097047` / `43622616931351` | 30 / 30 | 中文论坛已单独写过 sentiment22 负面情绪偏度 / sentiment23 消费者信心映射 —— 说明该集被同行关注，但**平台 alphaCount 仅 692**，实际出货很少 | 拥挤度判读的交叉验证 |

---

## 6. 派发记录（波 203，双中性化 2×10 因子设计）

| 批 | multisim id | 中性化 | decay | trunc | 表达式 |
|---|---|---|---|---|---|
| **203a** | `63eWWfGZ4gmb8T4tBBO3oM` | `SLOW_AND_FAST` | 5 | 0.08 | T1–T10 |
| **203b** | `28zKAFbrB5g5byix1Kiot8W` | `FAST` | 5 | 0.08 | T1–T10 |

共同设置：`USA / TOP3000 / D1 / EQUITY / FASTEXPR / nanHandling=ON / pasteurization=ON /
maxTrade=OFF / unitHandling=VERIFY / testPeriod=P0Y0M`。

**设计意图**：同 10 模板跑两种中性化 = 一次拿到「模板归因」+「中性化敏感性」两张表，
而不是把两批花在两次独立的模板扫描上。`FAST` 是对论坛 94 赞结论的直接检验。

**预检**：`preflight_expressions` → `valid=true / unknown_fields=[]`；
`operator_audit` → `safe=true / violations=[]`（幽灵算子 19 个均未使用）。

### 判读口径（收批前先定好，避免事后合理化）
1. **模板归因**：10 条里若某条 S ≥ 1.58 且 F ≥ 1.0，记为「模板族出货」；全灭则判 M1–M6 在 USA/D1 全部不成立。
2. **`SUB/S ≥ 0.434` 是硬线**（波 201 实测 limit 恒等于 0.434×S）。参数族全是 `ts_zscore` 裸外层、**无 group 外层** ⇒ 按波 201 的三层规律，SUB/S 应落在 0.45–0.63 的可用带。若实测 < 0.44，说明该规律在 sentiment 上不成立，需回写修正。
3. **换手**：`ts_sum`/`ts_mean` 是换手控制器，`ts_av_diff`（T8）是换手放大器 —— T8 若 TO > 70% 属预期行为，不算新发现。
4. **中性化对照**：若 203b(FAST) 系统性优于 203a(SLOW_AND_FAST)，则采纳论坛结论并为 SENTIMENT 塔锁定 `FAST` 设置。
5. **prod**：本集平台 alphaCount 仅 692（<30 的 20 倍，但远低于 sentiment1 的 14878）⇒ 按「prod 与 alphaCount 同向」先验，**预期 prod 墙风险中低**，但仍须逐颗实测，不得据先验放行。

---

## 7. 后续（本波未覆盖、留作下一波）

- `sentiment23` 同构 210 字段：结构复用本库模板，但拥挤度 2.3×，只在 203 出货后作为「第二颗塔位候选」使用。
- `news_transformer_scores`（315 字段 / VS 5.0）：**时段轴（pre / main / post-market）是同数据集内的真第三维**，与 sentiment22 的「模型变体轴」正交，可作为独立的第二机制来源。
- `ts_covariance` 模板族（论坛 51 赞）与 `dts` 内建 2/3/4/5 日多尺度尚未使用。
