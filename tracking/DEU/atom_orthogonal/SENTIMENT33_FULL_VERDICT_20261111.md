# sentiment33 完整判定：小样本幻觉信号（四波 32 臂 + 文献 + 算子全集验证）

## 一、覆盖了哪些维度（回应「算子都试了吗」）

**四波共 32 臂**，算子覆盖：

| 类别 | 已用算子 |
|---|---|
| Vector | **vec_avg / vec_stddev / vec_range / vec_count** |
| Transformational | **bucket / trade_when / tail / hump** |
| Logical | **if_else / and / less / greater** |
| Time Series | ts_delta / ts_zscore / ts_rank / ts_mean / ts_backfill / ts_corr / ts_arg_min / ts_regression |
| Group | group_rank / group_zscore / group_backfill |
| Cross Sectional | rank / zscore / **winsorize** |
| Arithmetic | add / subtract / multiply / divide / inverse / abs |

**矩覆盖**：变化面（Δ22/66/132）× 水平面（zscore252/504）× 位置面（ts_rank252/504）× 向量内部（stddev/range/count）。
**结构覆盖**：单腿 / 双腿加性 / 双腿乘性 / 门控 / 分段 / 回归残差 / 分桶条件化 / 信噪比 / 覆盖面回填。
**字段覆盖**：fkw1 / fkw2 / fkw3 / fkw4 / score / 多字段平均（model6/7/8/9 交叉）。

## 二、文献依据（已查到）

| 文献 | 结论 | 如何影响我的设计 |
|---|---|---|
| **Agree to Disagree: Forecasting Implied Volatility Using Financial Report Tone Disagreement**（MDPI） | tone disagreement **预测隐含波动率**，不是收益率 | ⇒ 改做 BE35 的门控/风险用法 |
| **Analyst Forecast Dispersion, Investor Sentiment, and the Cross-Section of Stock Returns** | 分歧度效应**受投资者情绪调节** | ⇒ 解释为何直接使用方向不稳 |
| **Investors' opinion divergence, uncertainty resolution** | 分歧度机制是「不确定性解析」 | ⇒ 支持门控用法 |
| Tetlock 2007 / Loughran-McDonald 2011 | 媒体悲观词推价后反弹；LM 词典优于 Harvard IV | 情感水平的理论基础 |

## 三、★核心证据：R 与 longCount 的交叉验证

**判别标准**：达到 S=1.58 且 F=1.0 所需最小收益率 `needR = 0.125 / 1.58² ≈ 0.0501`。

| 阶段 | 代表 alpha | S | **R** | **lc** | 判定 |
|---|---|---:|---:|---:|---|
| 小样本高收益 | pwaww6eb（分歧×均值） | 0.57 | **+0.1125** | **12** | R 是 needR 的 2.2 倍，但只 12 只股 |
| 提覆盖后 | 58J88dP6（fkw1） | **-0.48** | **-0.0559** | 60 | **R 翻负** |
| 提覆盖后 | d5a55J2w（group_backfill） | **-0.65** | **-0.0768** | 59 | **R 翻负更深** |
| 提覆盖后 | ZYaYYVRj（三字段平均） | -0.11 | -0.0155 | 66 | 衰减 |
| **门控后（最高覆盖）** | 3q0qQn5O（trade_when 低分歧） | **0.28** | **+0.0214** | **139** | **R 仅 needR 的 43%** |
| 门控后 | leaepRYl（if_else 分段） | 0.05 | +0.0077 | 97 | 衰减 |
| 门控后 | RReRjkvg（分歧独立） | -0.00 | -0.0002 | 95 | **零收益** |

## 四、判定：sentiment33 是「小样本幻觉信号」

**决定性事实**：

```
lc = 12  →  R = +0.1125  (S 0.57，看似 R 够)
lc = 60  →  R = -0.0559  (S -0.48，翻负)
lc = 139 →  R = +0.0214  (S 0.28，仅 needR 的 43%)
```

**覆盖扩大 ⇒ 收益单调衰减并翻负/趋零。**
这证明那个 +0.1125 的高收益**只存在于 12 只股票的小样本里**——
那些股票恰好受益于某个未被建模的共同因素（行业/规模/时点），不是可持续的横截面预测能力。

**若它是真 alpha**，扩大覆盖应该保持或提升 S（因为分散化降低 idiosyncratic 波动），
而不是让 R 从 +0.11 掉到 +0.02。**方向相反 ⇒ 是拟合，不是信号。**

## 五、sentiment33 的结构性约束（复述）

| 项 | 值 | 影响 |
|---|---|---|
| platform coverage | **0.322** | 决定 lc 上限约 95-139 |
| 字段类型 | VECTOR（真，非伪装） | vec_stddev 有效（与 vec_avg 差 15% >> 2% 阈值） |
| 金字塔拥挤度 | 34 用户 / 51 alphas（低） | 拥挤度不是问题 |
| 满覆盖对照 | lc 149-188 | sentiment33 最多到 139 |

**结论**：数据量本身够（lc 139 已接近满覆盖），但**方向性信息不足**（R 0.0214 < needR 0.0501）。
这与 sentiment27 的「有覆盖无信号」是同一类死法，只是 sentiment33 的表现形式是「小样本假信号」。

## 六、由此得到的两条新方法论

### M-1：小样本高收益的识别法

**症状**：`R >> needR` 但 `longCount` 极小（< 30）。
**检验**：提高覆盖（换字段版本 / 改高层分组 / group_backfill / 降平滑）再看 R。
**判据**：若提高覆盖后 R 衰减 >50% 或翻负 ⇒ **小样本幻觉，判死**；若 R 保持 ⇒ 真信号，继续优化。

### M-2：分歧度类信号的正确用法（文献支持）

分歧度预测的是**波动率/不确定性**（MDPI tone disagreement 论文），不是收益率。
⇒ 正确用法是 **门控/权重/风险调整**（`trade_when`、`if_else`、信噪比除法），
错误的用法是直接当收益预测信号做多空。
实测佐证：直接用法（BE32/33）最高 S 0.57 且是小样本；门控用法（BE35）覆盖到 139 但 R 仅 0.0214。
**两者都不成，说明 sentiment33 的 tone disagreement 信息量本身不足**，不是用法问题。