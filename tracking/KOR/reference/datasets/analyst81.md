# analyst81 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst81_profile.json`（5 字段）
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
| 字段总数 | 5 |
| 类型分布 | MATRIX 5 |
| coverage ≥ 0.5 | 0 / 5 |
| 白空间（alphaCount ≤ 2） | 1 / 5 |
| 平均 coverage | 0.2651 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 5 | 0 | MATRIX5 | 1 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 3 |
| `default_` | 1 |
| `financial_` | 1 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

## 四、类别 → 经济学骨架映射

### ⚠ 未分类 5 条（须逐条人工判读）

- `anl81_class` ｜ Creditwrothiness class indices in integers: 9(AAA), 5(AA), 4(A), 1(BBB), 2(BB), 3(B), 7(CCC), 8(CC), 6(C), 10(
- `anl81_confidence_level_percent` ｜ Confidence level of the assessment, measuring data completeness and reliability as a percentage from 0 to 100
- `anl81_probability_of_default_percent` ｜ Estimated probability of default over the rating horizon, expressed as a percentage from 0 to 100
- `default_likelihood_percent` ｜ Previous-period probability of default estimated by mode_finance, expressed as a percentage from 0 to 100
- `financial_data_completeness_percent` ｜ Confidence level for the lagged assessment, 0–100%, indicating completeness/reliability of available data

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 6 | 6 | 0.258 | `anl81_class` | Creditwrothiness class indices in integers: 9(AAA), 5(AA), 4(A), 1(BBB |
| 5 | 5 | 0.258 | `anl81_confidence_level_percent` | Confidence level of the assessment, measuring data completeness and re |
| 5 | 5 | 0.258 | `anl81_probability_of_default_percent` | Estimated probability of default over the rating horizon, expressed as |
| 5 | 5 | 0.276 | `financial_data_completeness_percent` | Confidence level for the lagged assessment, 0–100%, indicating complet |
| 1 | 1 | 0.276 | `default_likelihood_percent` | Previous-period probability of default estimated by mode_finance, expr |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl81_class`(αC 6)；`anl81_confidence_level_percent`(αC 5)；`anl81_probability_of_default_percent`(αC 5)；`financial_data_completeness_percent`(αC 5)；`default_likelihood_percent`(αC 1)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|

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
