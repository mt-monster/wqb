# EUR 字段属性补全与「属性 → 模板」规则

> 日期：2026-10-20 ｜ 回答：属性补全能落地吗？落地后规则是什么？

## 一、结论：分两层，一层已完成，一层需一步手工

| 层 | 属性 | 覆盖 | 状态 | 数据源 |
|---|---|---:|---|---|
| **语义属性** | `sem_type`（count / ratio / level_amount / score / probability / revision_change / estimate_level / percentile / dispersion / sentiment / cluster_label / identifier …） | **38,609 / 38,609 = 100%** | ✅ **已完成** | `tools/fields/field_semantic_type.py --build --region EUR`（解析 description） |
| **物理分布属性** | `skew` / `kurt` / `pos_ratio` / `neg_ratio` / `near_zero_ratio` / `integer` / `freq` / `shape` | **1,501 / 38,609 = 3.9%** | ⚠️ **需手工一步** | WebDataScope 浏览器扩展导出的 `WebData_*.zip` |

### 物理属性为什么不能自动补

平台 `get_datafields` 只返回 `name / type / coverage / description`，**不含分布统计**。
分布统计来自 WebDataScope 扩展的导出包（msgpack+zlib 私有格式，内含 `data/{dataset}.bin`）。

**补全步骤（一次，约几分钟）**：
1. 在浏览器打开 WebDataScope 扩展，选择 region=EUR、delay=1
2. 导出数据质量包 → 得到 `WebData_<date>_V<x>.zip`
3. 执行：
```bash
python tools/webdata_quality.py --zip <路径>/WebData_2026xxxx_V0.10.9.zip \
    --region EUR --delay 1 --fields <数据集逗号分隔> --json-out tracking/quality_eur1.json
# 全量（不带 --fields）：会把所有数据集写回 field_profile
python tools/webdata_quality.py --zip <路径>/WebData_2026xxxx_V0.10.9.zip --region EUR --delay 1
```

## 二、语义属性（sem_type）的精度验证

拿 1,501 个有真实分布统计的字段做交叉验证：

| sem_type | 交叉验证结论 | 精度 |
|---|---|---|
| `count` | 对应 `integer=1` 的占 42/61 | **69%** |
| `percentile` | 对应 `integer=0` 的占 58/79 | **73%** |
| `level_amount` | integer 1:0 ≈ 21:18 | 无判别力 |

⇒ **sem_type 可作先验，不能当事实**。物理属性（尤其 integer/sparse）仍需真实统计。

## 三、sem_type 与历史表现的相关性（EUR 已测字段实证）

| sem_type | n | avg best_S | max best_S | ALIVE 数 |
|---|---:|---:|---:|---:|
| **ratio** | 33 | **0.51** | **2.09** | **4** |
| unknown | 79 | 0.22 | 1.87 | 1 |
| level_amount | 30 | 0.13 | 1.51 | 0 |
| estimate_level | 12 | 0.48 | 1.40 | 0 |
| probability | 20 | 0.01 | 1.22 | 0 |
| percentile | 26 | 0.03 | 1.06 | 0 |
| count | 23 | 0.17 | 1.04 | 0 |
| sentiment | 24 | 0.12 | 0.68 | 0 |
| **score** | 39 | **−0.02** | 0.55 | 0 |
| **revision_change** | 13 | **−0.05** | 0.46 | 0 |

**两条硬结论**：
1. **`ratio` 型字段胜率最高**（5 个 ALIVE 里占 4 个）——因为比率**天然已归一化**，不含规模污染，本身就是横截面可比的
2. **`score` / `revision_change` 最差（avg ≈ 0）**——`score` 是有界噪声；`revision_change` **已经是变化量**，再套 `ts_delta` 等于对导数求导，信息全毁

## 四、属性 → 模板规则表（可执行）

| 属性 | 判据 | 强制规则 | 依据 |
|---|---|---|---|
| `freq` = quarterly / semi-annual | — | **backfill ≥252、平滑 ≥63、禁 3–22 短窗** | 季频字段在短窗内是常数 |
| `near_zero_ratio` > 0.3（42%） | 稀疏 | 必须 backfill + 事件式 decay | 零膨胀=事件型，否则大面积 NaN |
| `shape` = ceiling | — | 先 `rank`，禁裸 zscore | 上限截断使 zscore 失真 |
| `integer=1`（48%） | — | 用 spread / ratio（计数差），禁 level | 计数水平≈规模代理 |
| `pos_ratio` ≈ 1（49%） | 全正 | 禁裸 zscore，先 `rank` | 右偏，zscore 被极端值主导 |
| 有符号（36%） | 0.1–0.9 | 可直接用，**符号即方向** | 最宝贵类型 |
| `coverage` < 0.6 | — | 只作条件/分组，不作主腿 | sub/robust 会崩 |
| **`sem_type` = ratio** | — | 直接上模板（冠军栈/差分均可） | 实测 avg_S 0.51 最高 |
| **`sem_type` = revision_change** | — | **禁再用 `ts_delta`**，用 level 或累积和 | 已是变化量，二次差分毁信号 |
| **`sem_type` = score** | — | 先 `rank`/`quantile`，或只作门控条件 | 有界噪声，avg_S ≈ 0 |
| **`sem_type` = count** | — | 用 spread/ratio，稀疏时 backfill+decay | 与 integer 规则一致 |
| **`sem_type` = level_amount** | — | **必须先做 `vector_neut(F, size)` 体检** | 归零即 size 代理（institutions 实证） |
| **`sem_type` = identifier / cluster_label / temporal_meta** | — | **不可作信号**（仅分组轴或用 `vec_count` 计数） | 结构决定 |

## 五、平台物理约束（血的教训）

| 约束 | 报错原文 | 后果与解法 |
|---|---|---|
| VECTOR 事件型**禁止事件层算术** | `Operator multiply does not support event inputs` | `multiply(F1,F2)` 直接失败 ⇒ 先 `vec_*` 聚合 |
| VECTOR 事件型**禁止 `ts_backfill`** | `Operator ts_backfill does not support event inputs` | `ts_backfill(F, 252)` 直接失败 ⇒ 必须 `ts_backfill(vec_avg(F), 252)` |

⇒ **铁律：VECTOR 字段一律先 `vec_*(F)`，再做任何时序或算术运算。**
（2026-10-20 标定实验第一轮 64 条因忽略此条全部报错，修正后重跑）

## 六、落地清单

- [x] `sem_type` 全量补全（38,609 字段）
- [x] `sem_type` 接入 `field_profile_full`（可 `--sem-type` 查询）
- [x] 属性→模板规则表（本文）
- [ ] 物理分布属性补全（需 WebDataScope 导出，**待用户手工一步**）
- [ ] 标定矩阵结果（8 字段 × 8 模板，进行中）

---

## 七、标定矩阵结果（8 字段 × 8 模板，wave calib2）

**面板**：8 个属性正交字段（4 VECTOR + 4 MATRIX；5 个来自 news*，多为季/半年频）

| 模板 | 8 个字段的 S | 中位 | 最高 |
|---|---|---:|---:|
| **T3 一阶差分** `ts_delta(bf(F),W1)` | −0.09 / 0.08 / 0.18 / 0.19 / 0.22 / 0.23 / 0.34 / **0.51** | **+0.19** | **0.51** |
| **T4 二阶差分** `ts_delta(ts_delta(...))` | −0.01 / 0.03 / 0.09 / 0.14 / 0.19 / 0.20 / 0.24 / **0.46** | **+0.17** | 0.46 |
| T7 事件衰减 `ts_decay_linear(bf,252),63)` | −0.56 / −0.30 / −0.17 / −0.09 / −0.06 / −0.00 / 0.24 / 0.42 | −0.06 | 0.42 |
| T2 横截面秩 `rank(bf(F))` | −0.37 / −0.10 / −0.07 / −0.05 / 0.03 / 0.21 / 0.23 / 0.24 | −0.01 | 0.24 |
| T6 时序秩 `ts_rank(bf(F),ZW)` | −0.37 / −0.18 / −0.08 / −0.02 / 0.04 / 0.07 / 0.24 | −0.08 | 0.24 |
| T1 冠军栈 | −0.19 / −0.16 / −0.16 / −0.11 / −0.07 / 0.03 / 0.20 / 0.32 | −0.09 | 0.32 |
| T5 双窗秩乘积 | −0.54 / −0.35 / −0.33 / −0.14 / −0.03 / 0.03 / 0.23 / 0.25 | **−0.09** | 0.25 |

### 三条结论
1. **差分族（T3/T4）压倒性领先**：中位 +0.17~+0.19，其余模板中位全为负 ⇒ 对**季/半年频的新闻情感类字段**，信息在「变化」不在「水平」
2. **双窗秩乘积（T5）在这个面板上最差**（中位 −0.09）—— 与跨区经验（KOR/IND 四赢）相反，说明它**不适合慢频文本字段**，需要在高频价量类字段上验证
3. **面板绝对值全部 ≤0.51**：这批 news 字段本身弱（文本统计量），标定只能给出**相对排序**，不能给出可用 alpha

### ⚠️ 面板偏差（必须承认）
5/8 字段来自 news*，属性集中在「慢频 + 全正 + 大量 unknown 语义」⇒ 结论对「快频/价量」字段不可外推。
下一轮标定应换面板：从有 ALIVE 证据的 `predictive_starmine`（S 2.06）或高频 PV 字段里抽。
