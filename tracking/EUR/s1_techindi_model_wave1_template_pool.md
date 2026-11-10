# techindi_model 模板池（EUR / OTHER 塔 2→3 待点亮）· 2026-11-09

> 数据集 `techindi_model`：798 字段 MATRIX，cov 0.9997–1.00（近全市场稠密）
> 白地判据：**295 个 `probability_*` 字段 alphaCount = 0–6**（5 分位 × 3 horizon × 5 label 桶），
> 而拥挤侧 `predicted_*` 族 aC 达 202。已占位锚点 `LL5VwgO1`（S2.64 / prod **0.6926 过线**，
> `F=predicted_fifth_quantile_ten_day_return_15` + 双窗秩乘积 (2,252)，self 0.998 ⇒ 该几何锁死）。
> ⚠ 本集 prod 唯一已知的**可过线**证据：0.6926 < 0.7 ⇒ 本族是 EUR 少见的「prod 干净」信息源。
> ⚠ tm_N 族 + group_scale 幂次 4 次 prod 实测 0.7454/0.7794/0.7819/0.8163 ⇒ 该子路径判死。

## 一、模板清单（W1 已发 10 条，结构互异）

| # | 结构 | 表达式骨架 | 矩/几何 | 来源 | 设计理由 |
|---|---|---|---|---|---|
| T1 | 长期标准化（对照组） | `group_rank(ts_zscore(F10,252),industry)` | 水平 / zscore | 本集 TOP700 批次实证（S 3.36–3.84） | 首次搬**合法宇宙**复测；判 TOP700 强读能否存活 |
| T2 | 秩替换 | `group_rank(ts_rank(F10,252),industry)` | 水平 / 秩 | 自建 | 秩对重尾稳健，与 T1 只差变换 → 同时测「变换族」与「宇宙」两轴 |
| T3 | 分位利差 | `group_rank(subtract(F10, Q1_10),industry)` | 横截面离散度 | 自建（Q1 族 aC 9–88 全未开采） | 模型多空预测差 = 置信度强度，非方向 |
| T4 | 概率多空信念 | `group_rank(subtract(P4,P0),industry)` | 一阶方向矩 | 自建（概率白地首测） | softmax 概率差，bounded ∈[-1,1]，抗回归量纲 |
| T5 | 平滑信念 | `group_rank(ts_mean(subtract(P4,P0),22),industry)` | 一阶矩 + 平滑 | 自建 | 压 TO（TOP700 批 TO 0.54–0.65 贴线） |
| T6 | 长期标准化信念 | `group_rank(ts_zscore(subtract(P4,P0),252),industry)` | 一阶矩 / zscore | 自建 | 输入换概率 ⇒ 与 T1 天然低相关，主攻「新席位」 |
| T7 | 信念迁移 | `group_rank(ts_delta(subtract(P4,P0),22),industry)` | 一阶差分 | 自建 | 模型判断的变化率（迁移速度），与水平读数正交 |
| T8 | 极化度（非方向） | `group_rank(add(P0,P4),industry)` | 二阶/形状 | 自建 | 两极概率质量 = 模型置信度；方向中性 ⇒ 与 T4 逻辑正交 |
| T9 | 信念 × 强度复合 | `group_rank(multiply(subtract(P4,P0),F10),industry)` | 复合 | 自建 | 高信念 × 高预测值双条件；主信号仍是 F10 |
| T10 | 跨 horizon 分歧 | `group_rank(subtract(F10,F5),industry)` | 期限差 | 自建 | 10 日 vs 5 日预测背离 = 模型内部不一致 |

## 二、W2 预留模板（未发，等 W1 判定后按缺口补）

| # | 结构 | 骨架 | 备注 |
|---|---|---|---|
| T11 | 期望桶一阶矩 | `Σ k·Pk`（k=1..4，P0 权重 0） | 用概率向量重构期望分位，自归一化 |
| T12 | 概率熵/分歧 | 中间桶 mass − 两极 mass | 形状矩，与 T8 反向 |
| T13 | 中位数分位 Q3 | `predicted_third_quantile_ten_day_return_15`（aC 10 极冷） | 非端点分位，零占位 |
| T14 | tm 冷字段族 | `tm_1x_r1_r5_r10_rh_*`（aC=0 大批） | ⚠ 与 group_scale 组合已判死，须换几何 |
| T15 | 概率桶指派变化 | `ts_delta(P2,22)` | 中间桶迁移，非端点 |

## 三、判定纪律（本波）

1. **F 天花板前置**：techindi 已证 ret 8.54%（e76kv2xE）⇒ F 友好，可先看 S/TO。
2. **TO 是首要风险**：TOP700 批 0.54–0.65 > 30% 上限 ⇒ 本波 decay=8 + T5 平滑版作对照；若全批 TO 超线，W2 转 decay 16 + 内层 ts_mean。
3. **self 闸前置**：任何全 IS 闸件先与 `LL5VwgO1` 跑 self（TOP700 批实测 0.503–0.509 可过，但那是 TOP700 口径，须在合法宇宙重测）。
4. **prod 早测**：本族锚点 0.6926 仅剩 0.0074 余量 ⇒ 全闸件出现即测 prod，不做 S4 打磨。
5. **族容量**：概率读数与 predicted 读数是不同信息类型，**理论上可各占 1 席**；但须实测互相关 <0.5（组篮线）/ <0.7（提交线）。
