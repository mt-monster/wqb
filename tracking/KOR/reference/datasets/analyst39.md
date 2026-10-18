# analyst39 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst39_profile.json`（43 字段）
> 区域 KOR（不换）｜universe TOP600（本区唯一合法）｜delay 1

---

## 一、分析思路

1. **先用 description 做零假设重分类**，不看字段名 —— 字段名会骗人（description 是唯一语义依据）。
2. 与「按字段名分类」对照，**记录差异**（差异往往就是被漏掉的资产）。
3. 每类映射到经济学机制：说清「收益从哪来」，说不出的不进骨架。
4. 机制 → 骨架 → 候选；**骨架形态由体检体征决定，壳层由经济机制决定**。
5. 双通道取证（论坛 + 论文）后本区实测，结论回写本文档。

## 二、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | 43 |
| 类型分布 | MATRIX 43 |
| coverage ≥ 0.5 | 43 / 43 |
| 白空间（alphaCount ≤ 2） | 0 / 43 |
| 平均 coverage | 0.8952 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 32 | 32 | MATRIX32 | 0 |
| **年龄/时间戳** | 新鲜度 | 8 | 8 | MATRIX8 | 0 |
| **共识均值** | 预期水平 | 2 | 2 | MATRIX2 | 0 |
| **家数/估计者数量** | 关注广度 | 1 | 1 | MATRIX1 | 0 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 43 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 1 | — | `anl39_tp_all_delay_1_numofests` (cov 0.565, αC 27) |

## 四、类别 → 经济学骨架映射

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：8｜代表：`anl39_analyststart`, `anl39_2_curfperiodend`, `anl39_2_curfyearend`

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：2｜代表：`anl39_grosmgn5yr`, `anl39_tp_all_delay_1_mean`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：1｜代表：`anl39_tp_all_delay_1_numofests`

### ⚠ 未分类 32 条（须逐条人工判读）

- `anl39_2_curperiodnum` ｜ Number of the current fiscal period within the fiscal year (e.g., quarter 1–4)
- `anl39_2curfyearend` ｜ Fiscal year-end for the entity as of the current point in time (e.g., month of fiscal year end)
- `anl39_2curperiodtype` ｜ Type of Current Period
- `anl39_2cursharesoutstanding` ｜ Shares outstanding for the security as of the current point in time
- `anl39_aepsinclxo` ｜ EPS including extraordinary items - most recent fiscal year
- `anl39_agrosmgn` ｜ Gross Margin - 1st historical fiscal year
- `anl39_agrosmgn2` ｜ Gross Margin - 2nd historical fiscal year
- `anl39_atanbvps` ｜ Book value (tangible) per share - most recent fiscal year
- `anl39_curperiodtype` ｜ Type of current period
- `anl39_epschngin` ｜ EPS Change % - prior quarter
- `anl39_ghcspea` ｜ EPS Change % - year over year
- `anl39_ghcspemtt` ｜ Percent change in EPS, trailing 12 months versus the prior trailing 12 months
- `anl39_ptmepsincx` ｜ Earnings per share including extraordinary items for the prior trailing 12-month period
- `anl39_qepsinclxo` ｜ EPS including extraordinary items - most recent quarter
- `anl39_qgrosmgn` ｜ Gross Margin - most recent quarter
- `anl39_qtanbvps` ｜ Book value (tangible) per share - most recent quarter
- `anl39_qtotd2eq` ｜ Total debt to total equity ratio for the most recent quarter
- `anl39_qtotd2eq2` ｜ Total debt/total equity - most recent quarter, 1 year ago
- `anl39_rasv2_atotd2eq` ｜ Total debt to total equity ratio for the most recent fiscal year
- `anl39_roxlcxspea` ｜ EPS excluding extraordinary items - most recent fiscal year
- `anl39_roxlcxspeq` ｜ EPS excluding extraordinary items - most recent quarter
- `anl39_rygnhcspe` ｜ EPS Change % - most recent quarter 1 year ago
- `anl39_spvba` ｜ Book value (Common Equity) per share - most recent fiscal year
- `anl39_spvbq` ｜ Book value (Common Equity) per share - most recent quarter
- `anl39_tp_all_delay_1_high` ｜ High estimate
- `anl39_tp_all_delay_1_low` ｜ Low estimate
- `anl39_tp_all_delay_1_median` ｜ Median estimate
- `anl39_tp_all_delay_1_stddev` ｜ Standart deviation of estimates
- `anl39_ttmepsincx` ｜ EPS including extraordinary items - trailing 12 month
- `anl39_ttmgrosmgn` ｜ Gross Margin - trailing 12 month
- … 另有 2 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 388 | 210 | 0.998 | `anl39_qepsinclxo` | EPS including extraordinary items - most recent quarter |
| 335 | 202 | 0.998 | `anl39_spvbq` | Book value (Common Equity) per share - most recent quarter |
| 247 | 106 | 0.909 | `anl39_2curfyearend` | Fiscal year-end for the entity as of the current point in time (e.g.,  |
| 205 | 70 | 0.909 | `anl39_2curfperiodend` | End date of the current fiscal period as of the PIT date |
| 204 | 90 | 0.928 | `anl39_2_curfperiodend` | End date of the current fiscal period as of the point in time |
| 187 | 85 | 0.928 | `anl39_2_curfyearend` | Current fiscal year-end month as of the point-in-time date |
| 182 | 118 | 0.998 | `anl39_roxlcxspeq` | EPS excluding extraordinary items - most recent quarter |
| 177 | 104 | 0.990 | `anl39_ttmepsincx` | EPS including extraordinary items - trailing 12 month |
| 173 | 74 | 0.928 | `anl39_curfperiodend` | Calendar date of the current fiscal period end as of the point-in-time |
| 165 | 78 | 0.928 | `anl39_curfyearend` | Fiscal year-end month for the entity as of the point-in-time date |
| 158 | 118 | 0.998 | `anl39_qtanbvps` | Book value (tangible) per share - most recent quarter |
| 124 | 95 | 0.990 | `anl39_xlcxspemtt` | EPS excluding extraordinary items - trailing 12 month |
| 124 | 73 | 0.988 | `anl39_aepsinclxo` | EPS including extraordinary items - most recent fiscal year |
| 105 | 74 | 0.996 | `anl39_spvba` | Book value (Common Equity) per share - most recent fiscal year |
| 97 | 66 | 0.994 | `anl39_epschngin` | EPS Change % - prior quarter |
| 83 | 46 | 0.817 | `anl39_2curperiodtype` | Type of Current Period |
| 81 | 65 | 0.988 | `anl39_rygnhcspe` | EPS Change % - most recent quarter 1 year ago |
| 78 | 60 | 0.988 | `anl39_roxlcxspea` | EPS excluding extraordinary items - most recent fiscal year |
| 77 | 58 | 0.996 | `anl39_atanbvps` | Book value (tangible) per share - most recent fiscal year |
| 72 | 58 | 0.926 | `anl39_ttmgrosmgn` | Gross Margin - trailing 12 month |
| 69 | 54 | 0.932 | `anl39_qgrosmgn` | Gross Margin - most recent quarter |
| 62 | 43 | 0.829 | `anl39_curperiodtype` | Type of current period |
| 56 | 40 | 0.565 | `anl39_tp_all_delay_1_stddev` | Standart deviation of estimates |
| 43 | 35 | 0.997 | `anl39_qtotd2eq` | Total debt to total equity ratio for the most recent quarter |
| 35 | 31 | 0.973 | `anl39_ghcspea` | EPS Change % - year over year |
| 33 | 25 | 0.565 | `anl39_tp_all_delay_1_high` | High estimate |
| 31 | 29 | 0.928 | `anl39_2_curperiodnum` | Number of the current fiscal period within the fiscal year (e.g., quar |
| 28 | 24 | 0.909 | `anl39_2cursharesoutstanding` | Shares outstanding for the security as of the current point in time |
| 27 | 22 | 0.969 | `anl39_ghcspemtt` | Percent change in EPS, trailing 12 months versus the prior trailing 12 |
| 27 | 20 | 0.565 | `anl39_tp_all_delay_1_numofests` | Number of estimates |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl39_qepsinclxo`(αC 388)；`anl39_spvbq`(αC 335)；`anl39_2curfyearend`(αC 247)；`anl39_2curfperiodend`(αC 205)；`anl39_2_curfperiodend`(αC 204)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 年龄/时间戳 | — | — | — | — | cov≥0.5 8/8；类型 MATRIX |
| 共识均值 | — | — | — | — | cov≥0.5 2/2；类型 MATRIX |
| 家数/估计者数量 | — | — | — | — | cov≥0.5 1/1；类型 MATRIX |

**预处理决策（由画像推导，不由拍脑袋）**：

| 画像读数 | 预处理决策 | 依据 |
|---|---|---|
| VECTOR 占比高 | **必须 `vec_avg`/`vec_sum` 降维** | 裸用 `rank`/`ts_*` 秒拒；一条错整批 CANCELLED |
| cov < 0.4 的字段 | 先 `ts_backfill`/`group_backfill` | 体检硬门检查 1 |
| 季频更新（报告日） | 窗口下限 ≥ 63d | 窗口低于更新周期 = 噪声 |
| 单边恒正 | 改变化率 | 体检读数映射 |
| 离散评分型 | 禁 `winsorize`/`signed_power` | 无连续尾部，零效果 |

## 五、本区实测与死因

> **待回填**：本数据集在 KOR/TOP600/D1 的实测读数（S / TO / RN_S / 2Y）与死因归因。
> 死因判据三条：① TO 是否 <0.10（近静态）；② 有效持仓占比；③ risk_neutralized_S vs raw_S。
> ⚠ 预筛更严版：**TO < 0.03 的候选连差分都不要做**（差分只会更低）。

## 六、双通道取证

- **通道 A（论坛）**：`search_forum_posts` 长中文 query 会炸，砍短关键词；`read_forum_post` 必传 `include_comments=false`（true 会 30s 超时）。
- **通道 B（论文）**：`domain_search`。
- **待回填**：本数据集相关的论坛模板与文献机制。

## 七、下一步

> **待回填**：本数据集尚未证伪的假设、下一波设计（须满足铁律 G：候选数 ≤ 上波 1/3，且写明继承/准入/收窄）。
