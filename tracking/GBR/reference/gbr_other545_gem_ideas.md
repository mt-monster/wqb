# GBR delay1 other545 GEM Ideas（TOP700 / SUBINDUSTRY / decay4）

**Dataset**: other545
**Region**: GBR
**Delay**: 1

数据集：other545（NEMO 2.0 网络动量模型，4 字段）。六法在线评测 2026-11-14（批 `1LWN9m40a4WqbPRy9LbNPew` @NONE/dec0/nanOFF）：
- 法1 覆盖：`oth545_score` **329/700（47%）**、`mpd` 329、`pln_omen` **276/700（39%）**、`mktcap` 329
- 法2 非零：`divide(score, score)` 329 = 覆盖同数 ⇒ 零值可忽略
- 法3 频率：`ts_std_dev(score,22)` 变化 330/329 ≈ 100% ⇒ **日更**
- 法6 形态：`ts_zscore(score,252) > 0` 占 **165/329 = 50.2%**（对 50% 参考）⇒ **分布对称**（罕见的好性质：无需强偏态修正）
- 读数一致性：score 0.65 / mpd 0.60 / pln_omen 0.63 / mktcap 0.48 ⇒ **三个子分数与综合分高度同源**（综合分信息≈子分数），mktcap 是规模基座（0.48）

死路规避：
- 不用 mktcap（规模基座，非信号）
- 不做 sign/sqrt/tail/hump 压缩（矩阵 C 实证：压缩即毁信号）
- 不用 group_sum/group_std_dev/group_count（矩阵 F 实证：TO 0.77-0.82 爆闸）

文献锚：
- **论坛帖（29 赞）《藤蔓相连的生态：other515 供应链上下游联动》**：供应链网络把大客户股价表现映射到供应商，是多资产动量经典灵感；**采购占比（Revenue Exposure）越高传导越强**；需防网络图谱循环死锁。
- **Zhang-Gonzalez-Tu《Ownership Links and Return Predictability》**：**子公司组合收益显著预测母公司未来收益**（FF6 异常 107bp/月）；外国/跨行业/少数股权子公司的预测力更强 ⇒ 支持「网络联动 + 慢信息扩散」机制。
- Cohen-Frazzini (2008) 经济关联动量：客户-供应商链条上的信息扩散存在时滞。

**Concept**: 网络动量综合分（network momentum composite）
- **Mechanism**: NEMO 2.0 综合分由 7 个网络动量信号聚合，捕捉「通过经济关联（供应链/持股/文本联动）传导的动量」；慢信息扩散 ⇒ 正向漂移
- **Fields**: `oth545_score`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({oth545_score}), 22), sector)`
- **Direction**: 正
- **expected_exposure**: network momentum drift

**Concept**: 文本挖掘网络联动（text-mined linkage momentum）
- **Mechanism**: pln_omen 由文本挖掘的关联关系构造（比供应链图谱更宽），预测关联公司间的联动传导
- **Fields**: `oth545_pln_omen`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({oth545_pln_omen}), 66), industry)`
- **Direction**: 正
- **expected_exposure**: text-based economic linkage momentum

**Concept**: 动态价格动量（dynamic price momentum）
- **Mechanism**: mpd 为机器学习加权的动态价格动量（区别于静态 12-1 动量，按市场状态调节）
- **Fields**: `oth545_mpd`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({oth545_mpd}), 66), sector)`
- **Direction**: 正
- **expected_exposure**: state-dependent price momentum

**Concept**: 网络动量变化率（momentum acceleration）
- **Mechanism**: 综合分的**变化**而非水平——网络信息扩散的加速阶段（避免水平效应被套利）
- **Fields**: `oth545_score`
- **Implementation Example**: `group_rank(ts_delta(vec_avg({oth545_score}), 22), sector)`
- **Direction**: 正
- **expected_exposure**: network momentum acceleration

**Concept**: 子分数共振（sub-score agreement）
- **Mechanism**: mpd 与 pln_omen 同向时信号最可靠（价格动量与文本联动共振 = 多条独立证据指向同方向）；用 rank 差构造对偶，不用加权相加
- **Fields**: `oth545_mpd`, `oth545_pln_omen`
- **Implementation Example**: `group_rank(subtract(ts_mean(vec_avg({oth545_mpd}), 22), ts_mean(vec_avg({oth545_pln_omen}), 22)), sector)`
- **Direction**: 正（价量动量相对文本联动超配时买）
- **expected_exposure**: price-vs-text linkage divergence

**Concept**: 综合分相对自身历史（timing，非选股）
- **Mechanism**: score 相对自身 252 日均值的偏离 = 网络动量的时序异常（用于择时叠加而非纯选股）
- **Fields**: `oth545_score`
- **Implementation Example**: `group_rank(ts_zscore(vec_avg({oth545_score}), 252), sector)`
- **Direction**: 正
- **expected_exposure**: network momentum timing

**Concept**: 综合分长窗水平（slow decay）
- **Mechanism**: 网络动量的超慢成分（66 日均值）——信息沿供应链传导需要数周，慢窗更贴合机制
- **Fields**: `oth545_score`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({oth545_score}), 66), industry)`
- **Direction**: 正
- **expected_exposure**: slow network diffusion

多样性自检：Expected Exposure 6 种 ✓；字段族 3（综合分、pln_omen、mpd）✓；分组轴 sector/industry ✓；时间尺度 22/66/252 ✓；算子数 3-6 全部 ≤8 ✓。
⚠ 强制检查：lc/sc 必须 ≥150（本集真实覆盖 329，若显著低于此值即判异常）。
