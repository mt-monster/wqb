# S1 台账 · OTHER 塔攻坚（other532 / other455）· 2026-11-04

> 目标：补齐 **DEU/D1/OTHER 塔**的第 3 颗（`get_pyramid_alphas` 显示 other = 2/3，差 1 颗点亮，乘数 1.8）。
> 本文件合并原 `s1_other532_wave1_template_pool.md`，含正式波 12 模板 + 探针批 10 条全部结果。

---

## 一、为什么盯 OTHER 塔（平台事实，本轮首次读到）

`get_pyramid_alphas` / `get_pyramid_multipliers` 给出 DEU/D1 的真实塔进度：

| 塔 | 已提交数 | 差几颗点亮 | 乘数 |
|---|---:|---:|---:|
| **other** | **2** | **1** | 1.8 |
| model | 1 | 2 | 1.8 |
| analyst | 1 | 2 | 1.8 |
| fundamental | 1 | 2 | 1.8 |
| institutions | 1 | 2 | 1.6 |
| shortinterest | 1 | 2 | 1.3 |
| pv / earnings / sentiment / news / insiders / risk / option / macro / socialmedia / imbalance | 0 | 3 | 1.2–1.8 |

合计仅 7 颗。⇒ **other 是离点亮最近的一塔**，本波据此选靶。

### 1.1 提交篮三颗的塔归属（`get_alpha_details().pyramids`）

| alpha | 表达式要点 | pyramids.list | multiplier |
|---|---|---|---|
| `Vkx3MjW8` | mdl264_amihud_class + 盈利预期变化 + 预测惊喜 | DEU/D1/**MODEL** | 1.8 |
| `MPY9VNY9` | shrt3_bar 双窗口差分 | DEU/D1/**SHORTINTEREST** | 1.3 |
| `Vkxnb8QG` | mean_loan_rate_main 门控 eps_y1_estimate_change_3mo | DEU/D1/**SHORTINTEREST** + DEU/D1/**ANALYST** | 1.3 / 1.8 |

⇒ 提交 `MPY9VNY9` + `Vkxnb8QG` 后 shortinterest = 1+2 = **3/3 点亮**；model、analyst 各变 2/3。

---

## 二、候选数据集筛选（`get_datasets(category=other)` 41 个）

| 数据集 | 覆盖 | 字段 | alphas | users | 判定 |
|---|---:|---:|---:|---:|---|
| **other532 Specific Returns** | **0.8563** | 8 | 51 | 32 | **本波实测 → 判弱（见 §四）** |
| **other455 Relationship AI/ML** | **0.9535** | 1500（300 MATRIX + 1200 GROUP） | 239 | 107 | **本波探针 → 弱（见 §五）** |
| dl_riskfree_returns | 0.7147 | 133 | 964 | 404 | 无风险利率，非信号源 |
| other250 details data | 0.6126 | 12 | 4 | 3 | 电商价格/评分，与股票收益关系弱 |
| other47 Web Intelligence | 0.577 | 18 | 73 | 41 | 前波 R2 族已封盘 |
| other545 Linked Firms Momentum | 0.5269 | 4 | 8 | 8 | VECTOR + 覆盖偏低，备选 |
| insider_matrix / insider_trx_matrix | ~0.55 | 33 | 101 | 67 | 前轮判死封存 |
| other699 | 0.506 | 7 | 5 | 5 | 前波封盘 |
| techindi_model | 0 | 399 | 4298 | 853 | 前波 REGULAR 0 颗（prod 深钉） |

---

## 三、other532 正式波（12 模板，task `oth532_wave1_20261104`）

字段：`oth532_global_daily_specificreturn`（覆盖 0.9714，18 users / 25 alphas，Barra 风险模型残差收益）。

### 3.1 模板池（结构互异 12 个，算子数全部 10–11，符合 [10,15]）

| 模板 | 机制 | 文献来源 |
|---|---|---|
| T1 | 残差动量 ÷ 残差波动（252/126） | Blitz, Huij & Martens (2011) *Residual Momentum* |
| T2 | 短期特异反转（5d z − 22d z 期限结构） | Lehmann (1990) / Nagel (2012) |
| T3 | 特异波动率期限结构（22d vol ÷ 252d vol） | Ang, Hodrick, Xing & Zhang (2006) |
| T4 | 日频 vs 月频残差口径差 | 自建（信息加工差异） |
| T5 | 长期特异反转（252 vs 504 z 差） | De Bondt & Thaler (1985) |
| T6 | 新兴市场残差动量 ÷ 波动 | Blitz et al. 跨市场验证 |
| T7 | 欧洲（eue）残差短期反转 | Lehmann (1990) 欧洲样本 |
| T8 | 残差收益符号持续性（66 vs 252 sign 差） | 自建 |
| T9 | 残差动量 ÷ 504d 波动 | Blitz et al. 稳健性变体 |
| T10 | `ts_quantile` 水平 − `ts_zscore` | 自建（分布形状） |
| T11 | 残差回撤代理（`ts_max_diff` 恒等式） | 自建 |
| T12 | 欧洲（eult）vs 全球残差相对强弱 | 自建 |

### 3.2 回测结果（12/12 全收）

| 模板 | alpha | Sharpe | 换手 | Fitness |
|---|---|---:|---:|---:|
| T9 mom/vol 504 | `78LjpKvO` | **0.98** | 4.44% | 0.64 |
| T1 mom/vol 126 | `d5WjMLOJ` | 0.77 | 3.90% | 0.45 |
| 未标注（mom 类） | `gJej2dGM` | 0.71 | 3.92% | 0.38 |
| T6 emerging mom | `d5WjMaQY` | 0.63 | 4.04% | 0.34 |
| T8 sign persist | `3qolNbqN` | 0.57 | 5.50% | 0.26 |
| T5 long rev | `P0o7R51W` | 0.26 | 3.29% | 0.10 |
| T4 daily-monthly | `RRE7Oppn` | 0.22 | 7.68% | 0.06 |
| T2 rev term | `1YNw8EXm` | 0.20 | 4.58% | 0.06 |
| T12 EU(eult)-global | `LLM7Qrre` | 0.14 | 2.96% | 0.04 |
| T10 quantile | `A1VlAOrl` | −0.22 | 2.78% | −0.08 |
| T3 vol term | `O0A7Lp9d` | −0.38 | 8.54% | −0.15 |
| **T7 EU(eue) rev** | `LLM7QjLm` | **−1.10** | 7.76% | −0.78 |

**读数**：最高 0.98，远低于 LOW_SHARPE 1.58。**T7 = −1.10 ⇒ 该字段真方向与假设相反，翻正约 +1.10**，是唯一有点信息量的结构。

---

## 四、探针批（10 条，task `oth_other_probe1_20261104`）——真信号审判

探针批按既有规则「探针/定向破闸/对比实验/修复批不受算子数约束」，用**原始几何**（2–3 算子）排除平滑干扰。

### 4.1 other532 原始几何（4 条）

| 探针 | 表达式 | Sharpe | 换手 |
|---|---|---:|---:|
| P1 原始 1 日反转 | `-rank(ts_backfill(F,22))` | **−0.20** | **76.23%** |
| P2 5 日反转 | `-rank(ts_mean(ts_backfill(F,22),5))` | **0.03** | 38.21% |
| P3 66 日动量 | `rank(ts_mean(ts_backfill(F,22),66))` | **0.07** | 10.03% |
| P4 低波动 | `-rank(ts_std_dev(ts_backfill(F,22),22))` | **−0.32** | 10.29% |

### 4.2 other455 网络位置（6 条）

| 探针 | 字段族 | Sharpe | 换手 |
|---|---|---:|---:|
| Q1 relation w5 pca_fact1 水平 | relation | **0.50** | 1.42% |
| Q2 relation w5 pca_fact1 66d 变化 | relation | 0.11 | 2.85% |
| Q3 competitor w1 pca_fact1 | competitor | −0.28 | 1.07% |
| Q4 partner w1 pca_fact1 | partner | −0.22 | 1.21% |
| Q5 customer w1 pca_fact1 | customer | −0.27 | 1.08% |
| Q6 group_rank（cluster_20 自定义分组） | relation+GROUP | −0.36 | 2.43% |

---

## 五、结论

### 5.1 `other532` 判弱封盘（证据充分）

四种经典变换（1 日反转 / 5 日反转 / 66 日动量 / 低波动）在**原始几何**下全部落在 **−0.32 ~ +0.07**，即该残差收益字段在 DEU/TOP500 上**没有可交易的一阶边际**。
正式波的 0.77–0.98 全部来自「除以长期波动 + `ts_rank(504)` + `ts_decay_linear(22)`」这套平滑机器，换手被压到 3–4%（原版 10–76%）——**是平滑+中性化造出来的形状，不是信号**。
⇒ **other532 封盘，不再投入。**

### 5.2 ★★★★★ 方法论收获：算子数下限 [10,15] 会直接杀死快信号

本轮唯一一次「模板全灭但原因不在信号」的教训：

| 同一字段 | 算子数 | 换手 | Sharpe |
|---|---:|---:|---:|
| 原始反转 | 3 | 76% | −0.20 |
| 平滑后反转 | 10 | 4.6% | +0.20 |

为了把算子数从 3 堆到 10，被迫加 `ts_rank(504)`、`ts_decay_linear(22)`、`winsorize`、`group_neutralize`、`hump` 五层平滑，**换手从 76% 掉到 4.6%，信号被抹平**。
⇒ **快信号（高频翻转类）不适合硬凑 10 个算子**；凑算子应优先用信息保真的算子（`ts_av_diff` / `ts_delta` / `ts_scale` / `signed_power` / `group_zscore`），而不是平滑类。且 PPA 通道本就要求 ≤8 算子，两条约束在同一批 alpha 上互斥。

### 5.3 `other455` 判弱（暂不判死）

四个关系族（competitor / partner / customer）在 `rank(水平)` 下全是 **−0.22 ~ −0.28**（翻正后仅 +0.22~+0.28），relation w5 最好 **+0.50**，自定义 cluster 分组反而更差（−0.36）。
⇒ 一阶水平无信号；但**换手仅 1%** 说明它是极慢的横截面评分，尚未试过的方向（跨窗口一致、PCA 因子间比值、族间相对强度）留待后续，**不判死但降优先级**。

### 5.4 OTHER 塔的现实判断

**other532 + other455 两个最高覆盖候选都撑不到 1.58**。OTHER 塔第 3 颗若继续在这两个集里找，边际期望很低。
剩余未试的 other 候选：`other250`（cov 0.6126，电商价格/评分）、`other545`（cov 0.5269，VECTOR 网络动量）、`other47`（前波封盘）、`other699`（封盘）。
⇒ **建议把火力改投 model / analyst 塔**（两塔在提交篮落地后各为 2/3，同样只差 1 颗，乘数同为 1.8），而不是继续挤 OTHER。

---

## 六、附：踩坑记录

1. **`preflight_expressions` 必须显式带 `region/universe/delay`**。首次调用忘传，工具默认按 **USA/TOP3000** 校验，把 `idiosyncratic_return_eue_daily` / `eult_daily` 误报为 `unknown_fields`，差点误判字段不存在。
2. **多模拟父任务 spawn 慢**：账户仿真槽被兄弟会话占满时，`create_multi_simulation` 父任务 `child_count=0` 可持续 3.5 分钟，`batch_status` 会返回空；不是失败，等即可。单批从提交到出值约 2.5–4 分钟。
3. **`batch_status` 的参数名是 `simulation_ids`（数组）**，传 `multisimulation_id` 会抛 PTC_ARGUMENT_VALIDATION_FAILED。
