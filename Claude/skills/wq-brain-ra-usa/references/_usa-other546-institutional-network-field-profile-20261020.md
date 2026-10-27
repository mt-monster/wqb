# other546「机构网络关系」字段画像（USA / D1 / TOP3000）

> as_of 2026-10-20。数据集 = `other546`（Institutional Network Analysis）。
> 塔位：`USA/D1/OTHER`（×1.4，**未点亮**）。1 批 8 条探针，预注册「全 \|S\| < 1.0 ⇒ 判弱封存」命中。
> 回测批次：`4wfvBJ2U759r8z71cILgyPHX`（multisim，8/8 COMPLETE，0 error）。

## 1. 字段画像

13 个字段**全部 VECTOR**，语义是「主公司 × 每一个 peer 公司」的**对级**属性；`vec_avg` = 该公司所有 peer 对的均值。

| 字段 | cov | userCount | alphaCount | 描述 | 边类型 |
|---|---:|---:|---:|---|---|
| `oth546_analystnet_common` | 0.6846 | 12 | 16 | 同时覆盖主公司与 peer 的**分析师数（共同覆盖）** | 分析师 |
| `oth546_busnet_common` | 0.7206 | 6 | 14 | 共享的业务/地理段数 | 业务 |
| `oth546_busnet_strength` | 0.7206 | 5 | 7 | 业务段报告相似度（相关） | 业务 |
| `oth546_executivenet_common` | 0.7467 | 0 | **0** | 共享的高管/董事数（现任或曾任） | 高管 |
| `oth546_from_analyst` | 0.6846 | 4 | 4 | 覆盖**主公司**的分析师数 | 分析师（节点度） |
| `oth546_to_analyst` | 0.6846 | 1 | 1 | 覆盖 **peer** 的分析师数 | 分析师（邻居度） |
| `oth546_from_freq` | 0.7467 | 2 | 2 | 主公司关联的高管/董事数 | 高管（节点度） |
| `oth546_qerf_ot` | 0.7467 | 1 | 1 | peer 关联的高管/董事数 | 高管（邻居度） |
| `oth546_geonet_common` | **0.3948** | 0 | 0 | 共享地理段数 | 地理 |
| `oth546_geonet_strength` | **0.3948** | 3 | 4 | 地理段存在向量的相关 | 地理 |
| `oth546_mdanet_strength` | 0.7002 | 0 | 0 | MD&A 文本相似度 | 文本 |
| `oth546_nlpbusnet_strength` | 0.7066 | 0 | 0 | 业务段文本相似度 | 文本 |
| `oth546_risknet_strength` | 0.6876 | 2 | 2 | 风险因素段文本相似度 | 文本 |

读数要点：

- **覆盖率分成三档**：节点/分析师德 0.6846、业务/高管/文本 0.70–0.75、地理仅 **0.3948**（`geonet_*` 直接排除）。
- **aC=0 的四个字段**（executivenet_common / geonet_common / mdana_strength / nlpbusnet_strength）
  是「零拥挤」区；本批测了 `executivenet_common` 作对照。
- 字段是**对级**而非公司级 ⇒ 任何 `vec_*` 聚合都会把「有几个 peer、每个多强」压成一个数，
  这是本集的结构性信息损失。

### 经济机制

社会网络 / 信息扩散假说：董事会互锁、共同分析师覆盖、业务相似度都构成信息传导渠道
（Cohen-Frazzini 的经济关联、Hong-Kubik-Solomon 的行业lead-lag、董事会互锁的信息优势）。
方向先验：**关系越强 ⇒ 信息扩散越快 ⇒ 动量/修正被更快定价** —— 方向不确定（可能是正向跟随，也可能已被套利）。

## 2. 适用模板（本批设计）

8 条 = 分析师边 × 3（含镜像/Δ）、业务边 × 2、高管边 × 1、风险文本边 × 1、分析师节点度 × 1。
同壳 `quantile(group_rank(winsorize(vec_avg(<F>), std=4), industry))`。

| # | 机制 | 表达式核心 |
|---|---|---|
| G1 | M01 水平（分析师共同覆盖） | `vec_avg(oth546_analystnet_common)` |
| G2 | M02 镜像 | 同 G1 取负 |
| G3 | M01 水平（业务共享段） | `vec_avg(oth546_busnet_common)` |
| G4 | M01 水平（业务相似度） | `vec_avg(oth546_busnet_strength)` |
| G5 | M01 水平（主公司分析师数） | `vec_avg(oth546_from_analyst)` |
| G6 | M03 变化量 | `ts_av_diff(vec_avg(oth546_analystnet_common), 22)` |
| G7 | M01 水平（风险文本相似） | `vec_avg(oth546_risknet_strength)` |
| G8 | M01 水平（高管共享，aC=0 对照） | `vec_avg(oth546_executivenet_common)` |

设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / 2014-01-01 → 2023-12-31。

## 3. 回测结果及指标

| # | alpha | 构造 | S | F | 2Y | SUB | TO | risk-neut | 结论 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| G1 | `gJW99Agg` | **analystnet_common** | 0.54 | 0.17 | **1.70 PASS** | 0.52 PASS | 15.80% | 0.59 | fail 2 |
| G2 | `bl8ddkzp` | −analystnet | −0.54 | −0.17 | −1.70 | −0.52 | 15.80% | −0.59 | 严格镜像 |
| G3 | `O0JxxYz7` | busnet_common | 0.72 | 0.32 | 0.93 | 0.27 fail(0.31) | 12.90% | 0.36 | fail 4 |
| G4 | `6XAee80J` | busnet_strength | 0.64 | 0.23 | 1.07 | 0.18 fail(0.28) | 14.28% | 0.44 | fail 4 |
| G5 | `pwvKKXZX` | **from_analyst** | 0.69 | 0.25 | **1.41** | 0.56 PASS | 14.21% | **0.64** | fail 3 |
| G6 | `zqrRRM0o` | Δ22 analystnet | 0.44 | 0.12 | 1.63 | 0.02 fail(0.19) | 14.94% | 0.13 | fail 3 |
| G7 | `d5KRRXox` | risknet_strength | 0.45 | 0.14 | 0.76 | 0.18 fail(0.19) | 14.46% | −0.16 | fail 4 |
| G8 | `omoggprE` | executivenet_common（aC=0） | 0.66 | 0.27 | 0.56 | 0.70 PASS | 13.01% | −0.07 | fail 3 |

## 4. 归因

1. **G1/G2 严格镜像**（S ±0.54、2Y ±1.70，差 0）⇒ 分析师共同覆盖只有单一方向成分，无「关系强的公司与关系弱的公司」两段结构。
2. **2Y 按边类型分层，切得非常干净**：
   - **分析师边**：analystnet 2Y **1.70**、from_analyst **1.41**、Δ22 **1.63** —— 三条全部 ≥1.41；
   - **业务/高管/风险边**：busnet 0.93、busnet_strength 1.07、executivenet 0.56、risknet 0.76 —— 全部 ≤1.07。

   ⇒ 「共同分析师覆盖」这条边在 **2022 年后**才被定价，而业务相似度、高管互锁、风险语言相似度**从来没有 alpha**。
   这与信息扩散假说的推论一致但方向相反：不是「关系强 ⇒ 信息传导 ⇒ 收益」，而是「分析师网络是一种后知后觉的修正渠道」。
3. **risk-neut 同样按边分层**：from_analyst **0.64**、analystnet 0.59 最高；executivenet −0.07、risknet −0.16 为负。
   ⇒ 只有分析师边包含独立于 size/流动性/动量的信息，其余边是纯风格暴露。
4. **全期 S 全部 < 0.73**：2Y 的强不能补全期缺口（平台同时要全期 1.58 与 2Y 1.58）⇒
   这是 **regime 依赖**，不是可交付信号。
5. **Δ22 最差**（0.44 / SUB 0.02）⇒ 网络结构是慢变量，对其做变化量只增加噪音。
   （与 other699「快构造没信号」、pv63「偏离化摧毁信号」三次同向。）
6. **零拥挤 ≠ 有 alpha**：`executivenet_common` 的 alphaCount = 0，但 S 0.66 / 2Y 0.56 / risk-neut −0.07。
   与 `acquisition_model` 的 text 字段（aC 3、\|S\| 0.14）构成第二个反例。
7. **对级字段聚合损失**：8 条构造本质是「把 peer 对分布压成均值」，`vec_avg` 之后只剩下「平均关系强度」，
   而真正可能有用的是「关系的截面离散度 / 最强度 / 边数量」——本批未测 `vec_count` / `vec_stddev` / `vec_max`，
   但 G3/G4（共享段数与相似度）与 G8（高管共享数）已经覆盖了「关系数量」这一面且全弱，
   ⇒ 再发聚合轮只是在同一信息上换测度，按归因纪律不补批。

## 5. 决策（判弱封存 `USA-OTHER546-INSTITUTIONAL-NETWORK-WEAK`）

- 预注册「全 \|S\| < 1.0 ⇒ 判弱」成立（max 0.72）。
- **salvage**：`gJW99Agg`（analystnet_common，S 0.54 / 2Y **1.70** / SUB 0.52 PASS / risk-neut 0.59）
  与 `pwvKKXZX`（from_analyst，S 0.69 / 2Y 1.41 / risk-neut **0.64**）
  登记为「分析师共同覆盖的 2022 后定价」方向笔记。若将来做 **regime-aware 组合**（仅在分析师网络扩散活跃期开启）
  可回捞，全期 REGULAR 单腿不可交付。
- **不发第 2 批**：三条边（分析师/业务/高管）+ 文本边已各自给出读数，2Y 分层与 risk-neut 分层互证；
  再换 `vec_count`/`vec_max` 只是同信息换测度。
- **不更新 dead_end 键**（与 pv63 / pv115 / other580 / other545 同处理：论坛取证闸未过时不强行 `seal_dead_end`）。

## 6. 可复用方法论（新增 3 条）

1. **网络类字段要按「边类型」分层读，不能整集平均**：本集的 2Y 分层（分析师 1.4–1.7 vs 业务/高管/风险 ≤1.07）
   与 risk-neut 分层（0.59–0.64 vs −0.16–0.44）完全一致。整集报告「max S 0.72」会掩盖「有一条边在近端有效」。
2. **「2Y 强 + 全期弱」= regime 依赖，不是可交付**：全期 0.54–0.69、2Y 1.4–1.7 的组合必须当作
   「近端现象」，只能进 regime/组合腿，不能当全期单腿。
3. **alphaCount = 0 不是质量证明**：`executivenet_common`、`geonet_common`、`mdana_strength`、`nlpbusnet_strength`
   四个 aC=0 字段，实际测下来 S 0.66 / rns −0.07 / cov 0.39–0.75。零拥挤只说明没人用，不说明有用。

## 7. 索引

- 本篇：`references/_usa-other546-institutional-network-field-profile-20261020.md`
- 交付台账：`references/_usa-atom-delivery-log-20261020.md`（other546 行）
- 同型「2Y 强 + 全期弱」对照：`references/_usa-acquisition-model-field-profile-20261020.md`（Δ22 2Y −0.68 翻向）
- 同型「零拥挤 ≠ 有 alpha」对照：`references/_usa-acquisition-model-field-profile-20261020.md` §5.2 第 5 条
- 网络动量主线：`references/_usa-other545-nemo-field-profile-20261020.md`
