# socialmedia12 · EUR / TOP2500 / D1 字段画像 + 模板族设计

> 采集：2026-11-22（MCP `get_datafields(dataset_id=socialmedia12, filter_sharpe=false)`，平台声明 6 字段 = 实取 6 字段，`complete=true`）
> 塔位：SOCIALMEDIA **0/3 未点亮**（EUR 唯一余量 ≥2 席的塔）
> 倍率：1.2（低于 techindi 的 OTHER 1.5，但塔位余量最大）
> 来源披露：`scl12_buzz` 曾被用作 rK7nJ5nE 的**弱腿**（techindi 强腿 × buzz 250d backfill）⇒ S 2.58 / 2Y 2.57 / sub 1.55，说明该字段族在 EUR 有定价力，**但从未作为强腿做过纯 ATOM**。

## 0. 字段全表（6/6，无抽样）

| # | 字段 | 类型 | 覆盖率 | aC | userCount | onboard | 语义 | 可用性判据 |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | `scl12_sentiment` | MATRIX | 0.8495 | 942 | 469 | 2021-12-01 | 情绪分 | ✅ **核心信号**（连续、有符号） |
| 2 | `scl12_buzz` | MATRIX | 0.8495 | 907 | 457 | 2021-12-01 | 相对情绪成交量（关注度） | ✅ **核心信号**（半正定强度量） |
| 3 | `entity_employee_count` | VECTOR | 0.7507 | 244 | 175 | 2025-11-01 | 员工数（快照） | ⚠ 静态快照 ⇒ 只能作**规模分母/分组键**，不可作时序信号 |
| 4 | `entity_total_revenue` | VECTOR | 0.7507 | 318 | 187 | 2025-11-01 | 营收（快照） | ⚠ 同上，规模分母 |
| 5 | `entity_sector_name` | VECTOR | 0.7507 | 155 | 102 | 2025-11-01 | 行业名（分类） | ⛔ 分类变量，不可作信号 |
| 6 | `entity_profile_summary` | VECTOR | 0.7507 | 230 | 101 | 2025-11-01 | 公司简介文本 | ⛔ 文本，不可作信号 |

**画像结论**：可用信号字段只有 **2 个 MATRIX**（sentiment / buzz），4 个 VECTOR 中 2 个静态规模量可作分母、2 个是分类/文本（排除）。
⚠ 静态字段是**快照**（无历史序列）⇒ 任何 `ts_*` 包裹在它们上面都是常数序列，禁止使用。

**覆盖率口径**：0.8495 是名义值（平台按 TOP2500 分母算），需按 §7.6 六维体检确认近十年逐年非零。

## 1. 逐字段实测读数（全表 6/6，一字段一行，2026-11-22 平台实跑）

> 探针统一设置：EUR / TOP2500 / D1 / CROWDING / decay 4 / trunc 0.0 / nanHandling ON / maxTrade OFF

| 字段 | 主探针形态 | alpha | S | F | 2Y | sub | TO | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|
| `scl12_sentiment` | 三族最好（D 差分 ts_delta22） | Jj82v2dx | 0.38 | 0.10 | 1.64 | 0.25 | 26.1% | ⛔ 作强腿无定价力 |
| `scl12_buzz` | B 比值（div 一年均值）0.39；作 techindi 弱腿 2.58 | Grm7e7kx | 0.39 | 0.09 | 1.57 | 0.16 | 29.2% | ⛔ 强腿弱 / ✅ 弱腿强 |
| `entity_employee_count` | 静态快照直读 `vec_avg` | 58J2ga3k | 0.68 | 0.28 | 1.44 | 0.54 | 18.2% | ⛔ 静态快照，无时序语义 |
| `entity_total_revenue` | 静态快照直读 `vec_avg` | A1x2vgbR | 0.59 | 0.28 | 1.12 | 0.28 | 13.6% | ⛔ 静态快照 |
| `entity_sector_name` | 分类量直读 `vec_avg` | 88N2Para | 0.39 | 0.14 | 0.73 | −0.17 | 17.7% | ⛔ 分类变量 |
| `entity_profile_summary` | 文本量直读 `vec_avg` | npaXPZoq | 0.39 | 0.14 | 0.73 | −0.17 | 17.7% | ⛔ 文本量 |

**★ 关键观察**：`entity_sector_name` 与 `entity_profile_summary` 读数**逐位相同**（S0.39/F0.14/2Y0.73/sub−0.17/TO17.7%）
⇒ 两者在数值化后落到同一个退化常量，证实文本/分类字段不承载可交易信息。

### 1.1 五族明细（Wave B，`o2HYt79o4wL9fq1dF7HqZah`）

| 族 | 表达式骨架 | alpha | S | F | 2Y | sub | TO | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| B1 H 水平 | `group_rank(ts_mean(scl12_sentiment,22),industry)` | 9ql272Jo | 0.04 | 0.00 | 0.75 | −0.05 | 7.6% | 4 |
| B2 R 相对历史 | `group_rank(ts_zscore(ts_backfill(scl12_sentiment,66),250),industry)` | WjlxVx9G | 0.07 | 0.01 | 1.01 | 0.06 | 17.3% | 3 |
| B3 B 关注度比值 | `group_rank(divide(scl12_buzz,ts_mean(scl12_buzz,250)),industry)` | Grm7e7kx | 0.39 | 0.09 | 1.57 | 0.16 | 29.2% | 4 |
| B4 X 情绪×关注 | `group_rank(multiply(scl12_sentiment,scl12_buzz),industry)` | xAvEdEng | 0.40 | 0.10 | 1.57 | 0.18 | 28.9% | 4 |
| B5 D 差分 | `group_rank(ts_delta(scl12_sentiment,22),industry)` | Jj82v2dx | 0.38 | 0.10 | 1.64 | 0.25 | 26.1% | 2 |

## 2. 分布与更新频率（实测回填）

| 字段 | 预期形态 | 预期更新 | 风险 |
|---|---|---|---|
| `scl12_sentiment` | 有符号、近似标准化（−1..1 或 z 值） | 日频 | 可能大量 0 值（无社媒讨论日）⇒ 零值≠中性，须先测 `!=0` 比例 |
| `scl12_buzz` | 右偏非负（成交量倍数） | 日频 | 长尾极值 ⇒ 需 winsorize / ts_rank |
| `entity_*` | 静态快照 | 年报/变更 | 迟滞；仅在 `divide` 分母位置使用 |

## 2. 5 个结构互异模板族（族级定义见 `template_family_exhaustion_20261122.md`）

### B1 · H 水平（存量情绪）
```
group_rank(ts_mean(scl12_sentiment, 22), industry)
```
- 机制：过去一月平均情绪水平 ⇒ 情绪定价漂移
- 与其它族的区别：**不对比自身历史**，只读绝对水平
- 风险：若 sentiment 是长期稳定的公司属性 ⇒ 近似静态暴露，TO 会极低（<0.05 触发 LOW_TURNOVER 视下游假设）

### B2 · R 相对自身历史（情绪异常）
```
group_rank(ts_zscore(ts_backfill(scl12_sentiment, 66), 250), industry)
```
- 机制：情绪相对自身一年基线的标准分 ⇒ 情绪**突变**而非水平
- 与 B1 的区别：消掉公司固定效应（B1 买"一直是好情绪"，B2 买"情绪变好了"）

### B3 · B 比值（关注度相对基线）
```
group_rank(divide(scl12_buzz, ts_mean(scl12_buzz, 250)), industry)
```
- 机制：当前关注度 ÷ 一年均值 ⇒ 异常放量（注意力冲击）
- 与 B2 的区别：buzz 是强度量，比值保序且非负，不会因零值爆负

### B4 · X 交叉（情绪 × 关注度）
```
group_rank(multiply(scl12_sentiment, scl12_buzz), industry)
```
- 机制：**有讨论的正面情绪才有效**（低关注的正面情绪没人交易）⇒ 交互项
- 与 B1/B3 的区别：两字段相乘，纯二维交互，不是单字段形态

### B5 · D 差分（情绪变化）
```
group_rank(ts_delta(scl12_sentiment, 22), industry)
```
- 机制：情绪一月动量 ⇒ 情绪改善方向
- 与 B2 的区别：B2 是相对基线的 z（含波动率归一），B5 是裸变化量（量纲保留）

### B6（备） · E 事件新鲜度
```
group_rank(ts_arg_max(scl12_buzz, 66), industry)
```
- 机制：关注度峰值距今多久 ⇒ 新鲜度门控（旧结论：`ts_arg_max` 作门控是冠军、作信号是摧毁器）
- 只在 B1–B5 出现 ≥1 条 |S|≥1.0 后才投入（作 boost/门控腿）

## 3. 派批纪律

- 首波 5 臂 = B1–B5，统一设置 **TOP2500 / CROWDING / decay 4 / trunc 0.0 / nanHandling ON / maxTrade OFF**（与已确认的族 M 配置同档，读数可直接与 techindi 族对比）
- 有效族（|S| ≥ 1.0 且 RA-clean）→ 做完整梯度：**同类别算子全替换（ts_rank/ts_zscore/ts_mean/ts_sum/ts_decay_*/ts_scale/ts_quantile/ts_av_diff…）+ 参数档（窗口 22/44/66/250、decay 0/4/8/16）+ 外层轴（industry/subindustry/sector/market）**
- 反向读数（S 为负且 |S| 大）⇒ 取负号重派，不判死
- 塔位：SOCIALMEDIA 0/3，本集最多交 3 颗；**但与 rK7nJ5nE 的互相关必须实测**（共享 buzz 字段）

## 4. 已知风险

1. `scl12_buzz` 与 rK7nJ5nE 的弱腿同源 ⇒ 纯 buzz 族与 rK7nJ5nE 互相关可能 >0.7，届时只能择一进篮
2. 静态 `entity_*` 字段做分母时须 `vec_avg` 降维，且**禁止 ts_ 包裹**
3. 2014 起是否有数据未验证（onboard 2021-12-01 指平台实现时间，不等于数据起点）⇒ 十年要求待 `get_alpha_yearly_stats` 核
