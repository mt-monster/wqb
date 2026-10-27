# other545「NEMO 2.0 网络动量」字段画像（USA / D1 / TOP3000）

> as_of 2026-10-20。数据集 = `other545`（NEMO 2.0，网络动量合成）。
> 塔位：`USA/D1/OTHER`（×1.4，**未点亮**）。1 批 8 条探针，预注册判据「全 \|S\| < 1.0 ⇒ 判弱封存」命中。
> 回测批次：`1DVZjI30h4EEcvY13K3f6dBh`（multisim，8/8 COMPLETE，0 error）。

## 1. 字段画像

| 字段 | 类型 | cov | userCount | alphaCount | 描述 | 信号角色 |
|---|---|---:|---:|---:|---|---|
| `oth545_score` | VECTOR | 0.8051 | 4 | 5 | **七条网络动量信号合成的最终 NEMO 2.0 评分** | 合成主信号 |
| `oth545_pln_omen` | VECTOR | 0.8051 | 5 | 12 | NLP 文本挖掘关联得到的**网络动量评分** | 单成分（文本） |
| `oth545_mpd` | VECTOR | 0.8051 | 5 | 6 | 动态价格动量评分（ML 价格动量） | 单成分（价格） |
| `oth545_mktcap` | VECTOR | 0.8051 | 9 | 10 | 公司市值（美元） | **非信号**：规模控制变量 |

- 4 个字段全是 VECTOR、覆盖率一律 0.8051 ⇒ 覆盖不是区分因素，**必须先用 `vec_avg` 聚合再进标量算子**。
- 拥挤度整体极低（aC 5–12、userCount 4–9），是典型的「低拥挤 ≠ 有 alpha」样本。
- `mktcap` 无截面信息（市值本身是 size），本批不投。

### 经济机制

Cohen & Frazzini (2008) *Economic Links and Predictable Returns*：经济关联公司之间存在动量溢出（lead-lag）。
NEMO 2.0 把七条网络动量信号（价格、文本、供应链等）合成为一个评分。方向先验：**正**（关联公司上涨 ⇒ 本公司未来上涨）。

## 2. 适用模板（本批设计）

8 条 = 水平 × 2（含严格镜像）/ 单成分 × 3 / Δ 轴 × 1 / 时序秩 × 1 / 时序 z 分 × 1。
通用壳 `quantile(group_rank(winsorize(<SIG>, std=4), industry))` —— 与 board_gov / pv63 / other699 同壳，保证跨数据集可比。

| # | 机制 | 表达式核心 |
|---|---|---|
| A1 | M01 水平（合成） | `vec_avg(oth545_score)` |
| A2 | M02 镜像 | 同 A1 取负 |
| A3 | M01 水平（文本成分） | `vec_avg(oth545_pln_omen)` |
| A4 | M02 镜像 | 同 A3 取负 |
| A5 | M01 水平（价格成分） | `vec_avg(oth545_mpd)` |
| A6 | M03 变化量 | `ts_av_diff(vec_avg(oth545_score), 22)` |
| A7 | M04 时序秩 | `ts_rank(vec_avg(oth545_score), 252)` |
| A8 | M05 时序 z 分 | `ts_zscore(vec_avg(oth545_score), 66)` |

设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / 2014-01-01 → 2023-12-31。

## 3. 回测结果及指标

| # | alpha | 构造 | S | F | 2Y | SUB | TO | risk-neut | 结论 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| A1 | `akVEEYnx` | score 水平 | 0.86 | 0.53 | 0.75 | 0.62 | 11.23% | 0.04 | fail 3 |
| A2 | `vROvvqlG` | −score | −0.86 | −0.53 | −0.75 | −0.62 | 11.23% | −0.04 | 严格镜像 |
| A3 | `QPY99JVw` | **pln_omen 水平** | **0.86** | **0.56** | **0.98** | 0.59 | **6.04%** | **0.46** | fail 3（全批最优） |
| A4 | `1Yjzz9z6` | −pln_omen | −0.86 | −0.56 | −0.98 | −0.59 | 6.04% | −0.46 | 严格镜像 |
| A5 | `6XAee8eE` | mpd 水平 | 0.81 | 0.49 | 0.66 | 0.76 | 13.36% | −0.18 | fail 3 |
| A6 | `leM33q3A` | Δ22 score | 0.80 | 0.37 | 0.61 | 0.86 | 20.08% | 0.13 | fail 3 |
| A7 | `78onnAn5` | ts_rank 252 | 0.69 | 0.35 | 0.54 | 0.65 | 14.01% | −0.19 | fail 3 |
| A8 | `xA1dd6Ng` | ts_zscore 66 | 0.79 | 0.40 | 0.51 | 0.74 | 16.34% | 0.00 | fail 3 |

设置口径：全部 `quantile(group_rank(winsorize(<SIG>, std=4), industry))`，USA/TOP3000/D1/SUBINDUSTRY/decay5/trunc0.08。

## 4. 归因

1. **两组严格镜像，无方向两段**：score 0.86 / −0.86、pln_omen 0.86 / −0.86，差 0；2Y 也逐位对称。
   ⇒ 每个字段只有一个方向成分，不存在「关联公司涨 → 做多」与「关联公司跌 → 做空」的非对称。
2. **全批 max S 0.86，离闸线 1.58 差 0.72** ⇒ **构造层失败，不是设置层**。8 条 TO 6–20%、无一踩 LOW_TURNOVER，
   所以不是「太慢」；同时没有一条接近 1.0，说明信号本身没有截面信息。
3. **合成反而稀释了唯一有效的成分**：`score`（七信号合成）risk-neut **0.04**，而被合成的单一文本成分 `pln_omen`
   risk-neut **0.46**、TO 仅 6.04%、2Y 0.98。⇒ **合成把正交成分平均掉了，取合成字段等于主动丢掉独立性。**
   可复用判据：遇到 `*_score` / `*_composite` 合成字段，**必须同时测其成分字段**，不能只测合成。
4. **价格动量成分是纯风格**：`mpd` risk-neut −0.18，且 2Y 0.66 低于全期 0.81 ⇒ 动态价格动量在 USA 已被套利。
5. **时序归一三连败（第 N 次复证）**：Δ22 0.80 但 TO 翻倍至 20.08%、ts_rank252 0.69、ts_zscore66 0.79 且
   risk-neut 归零。⇒ 与 `USA-PV63-*`、`USA-MFRP-*` 同一结论：**在 USA 把水平换成「自身历史偏离」会摧毁信号**。
6. **网络动量在 USA 全期无 alpha**：Cohen-Frazzini 的原始样本（1965–2004 月度）之后已被套利；
   近端 2Y 仅 0.98，也不存在「近年变强」的补救空间。

## 5. 决策（判弱封存 `USA-OTHER545-NEMO-WEAK`）

- 预注册「全 \|S\| < 1.0 ⇒ 判弱」成立（max 0.86）。
- **salvage**：`QPY99JVw`（`pln_omen` 水平，S 0.86 / F 0.56 / 2Y 0.98 / risk-neut 0.46 / TO 6.04%）
  登记为「NLP 经济关联动量」的弱方向笔记 —— 本批唯一 risk-neut > 0.4 的构造，若将来做 regime/组合腿可回捞，
  **单腿 REGULAR 不可交付**。
- **不发第 2 批**：8 条已覆盖水平/镜像/单成分/Δ/秩/z 分六个面，且「合成 vs 成分」的分层已给出机制解释。
  再发 = 盲扫。
- 本集**不更新 dead_end 键**（`other545` 原不在判死名单；判弱与判死在取出规则上等价，但按本区惯例
  「论坛取证闸未过」时不强行 `seal_dead_end`，与 pv63 / pv115 / other580 处理一致）。

## 6. 可复用方法论（新增 2 条）

1. **合成字段必须与成分字段同批测**：合成评分可能把正交成分平均掉（本集 score rns 0.04 vs 单成分 0.46）。
   判据：若 `*_score` 的 risk-neut 明显低于其任一成分，说明信息被稀释，应以成分为主信号。
2. **网络动量类数据集在 USA/D1 的边界**：全期 S 上限 ~0.86、2Y < 1.0 ⇒ 该族在 USA 已无可交付空间。
   后续遇到「网络/关联溢出」类数据集（NEMO、供应链动量、peer momentum），**先按本集结论降权**，
   只在有「非价格、非文本合成」的新边类型时才投入。

## 7. 索引

- 本篇：`references/_usa-other545-nemo-field-profile-20261020.md`
- 交付台账：`references/_usa-atom-delivery-log-20261020.md`（other545 行）
- 同型「严格镜像 + 时序归一失效」对照：`references/_usa-pv63-order-flow-field-profile-20261020.md`、
  `references/_usa-other699-individual-investor-field-profile-20261020.md`
- 合成 vs 成分的对照先例：`references/_usa-other685-field-profile-20261020.md`（24 条 × 6 字段株）
