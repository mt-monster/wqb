# analyst46 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst46_profile.json`（6 字段）
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
| 字段总数 | 6 |
| 类型分布 | MATRIX 6 |
| coverage ≥ 0.5 | 0 / 6 |
| 白空间（alphaCount ≤ 2） | 1 / 6 |
| 平均 coverage | 0.4206 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 4 | 0 | MATRIX4 | 1 |
| **年龄/时间戳** | 新鲜度 | 1 | 0 | MATRIX1 | 0 |
| **排名/分位** | 相对位置 | 1 | 0 | MATRIX1 | 0 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 5 |
| `profit_` | 1 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

## 四、类别 → 经济学骨架映射

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：1｜代表：`anl46_alphadecay`

### 排名/分位 → 骨架：**横截面相对位置**

- **收益来源**：同业内相对位置，剥离行业共性
- **合规/工程注意**：⚠ 可能与本数据集已有的 rank 字段重复
- **字段数**：1｜代表：`anl46_performancepercentile`

### ⚠ 未分类 4 条（须逐条人工判读）

- `anl46_experts` ｜ A component showing the contribution from the historical performance of analysts who submitted ideas for the s
- `anl46_indicator` ｜ Cross-sectional ranking score from 1 to 10 for the stock within the region on a given day, with 10 being most 
- `anl46_sentiment` ｜ A composite score representing aggregated sell-side idea sentiment for the stock, combining decay, contributor
- `profit_report_component` ｜ A component reflecting how close the stock is to an earnings event, adjusting the signal according to proximit

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 10 | 8 | 0.419 | `anl46_alphadecay` | A component value measuring the impact of idea age (i.e., how recent o |
| 10 | 8 | 0.419 | `anl46_sentiment` | A composite score representing aggregated sell-side idea sentiment for |
| 9 | 7 | 0.427 | `anl46_performancepercentile` | A percentile rank (1–100) showing how well the Indicator signal has hi |
| 8 | 8 | 0.419 | `anl46_indicator` | Cross-sectional ranking score from 1 to 10 for the stock within the re |
| 7 | 7 | 0.419 | `anl46_experts` | A component showing the contribution from the historical performance o |
| 1 | 1 | 0.419 | `profit_report_component` | A component reflecting how close the stock is to an earnings event, ad |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl46_alphadecay`(αC 10)；`anl46_sentiment`(αC 10)；`anl46_performancepercentile`(αC 9)；`anl46_indicator`(αC 8)；`anl46_experts`(αC 7)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 年龄/时间戳 | — | — | — | — | cov≥0.5 0/1；类型 MATRIX |
| 排名/分位 | — | — | — | — | cov≥0.5 0/1；类型 MATRIX |

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
