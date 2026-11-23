# earnings6 · EUR / TOP800 / D1 字段画像（2026-11-22 全字段普查）

> 类型 VECTOR · 66/66 字段全量拉取（complete=true）· category = **earnings**（×1.2，塔位 1/3 未满）
> 采集：2026-11-22 · 拉取宇宙 TOP2500（字段注册区相同；实测最佳回测宇宙 TOP800）

## 0. 可用性分层（全字段）

| 层 | 字段 | 数量 | αC | 说明 |
|---|---|---:|---|---|
| **核心数值（唯一可挖面）** | `ern6_actual_eps`（实际 non-GAAP EPS，cov 0.526）、`ern6_estimated_eps`（Estimize 加权预期，cov 0.526） | 2 | 142 / 65 | **全部历史出货都出自这对字段** |
| 辅助数值 | `eps_change_absolute_value`(17)、`eps_change_percentage_value`(10)、`preliminary_eps_range_lower_bound`(13)、`preliminary_eps_range_upper_bound`(12) | 4 | ≤17 | 同 cov 0.526，未测 |
| 股息金额 | `ern6_x_dividend`(97)、`ern6_x_dividend_oc`(81)、`_233`(8)、`_235`(13) | 4 | — | 现金股息 USD/原币 |
| 日期/日历 | `ern6_1q/2q/3q/4q`、`next_ed`、`conferencecalltime`、fiscal_year 系、`time_of_day` | ~20 | — | 事件日历（PEAD 门控可用，非信号） |
| 文本/标识 | company_name、isin、stock_symbol、url、confpasscode、timezone、wqreceivetimestamp | ~36 | — | ⛔ 无信号语义 |

**画像结论**：earnings6 = 双 EPS 字段（实际 vs Estimize 预期）的 earnings-surprise 单一信息源数据集；66 字段中 62 个是元数据。字段覆盖率 0.526 是 cov 结构性上限（⇒ 覆盖不足型 CW 风险集中在小宇宙）。

## 1. 已验证机制（历史出货 = mcp-20261120 批）

骨架：`group_rank(add(ts_mean(ts_delta(group_backfill(divide(group_backfill(vec_avg(actual), G, 20), add(abs(group_backfill(vec_avg(estimated), G, 20)),1)), market, 20), 610), W), ts_mean(ts_delta(divide(ts_backfill(vec_avg(actual),500), add(abs(ts_backfill(vec_avg(estimated),500)),1)), 252), W)), market)`

TOP800/SUBINDUSTRY/decay16–32 上 17 颗 S 2.13–2.48 / F 3.1–3.9 / 2Y 1.72–2.09 / TO 2.5–2.9%，**全部只挂 `CONCENTRATED_WEIGHT`（0.167 > 0.1）+ 个别 2Y 差 0.01（限 2.02@TOP800）**。

## 2. 实测记录（2026-11-22 本轮）

### 批1：TOP800→TOP2500 重跑 8 原式 + 2 变体（decay16/SUBINDUSTRY/trunc0.08）

| 变体 | S | F | 2Y | sub | CW |
|---|---:|---:|---:|---:|---|
| 8 颗原式（610/105 族） | 0.96–1.05 | 0.81–0.92 | 0.71–0.94 | 0.58–0.81 | ✅ PASS |
| ts_backfill 替代版（73 窗） | 0.84 | 0.68 | 0.55 | 0.58 | ✅ |
| 秩合成（group_rank 内层 add） | 0.74 | 0.48 | **1.87** | 0.50 | ❌ 0.368 |

**判读**：TOP2500 使 S 从 2.4 塌到 1.05（−56%）⇒ **EPS surprise 信号住小盘**（longCount 121/878 严重不对称，大盘段只贡献空头）。换宇宙修 CW 是死路。2Y 在 TOP2500 反而崩（1.87 秩合成除外）——TOP800 的 2Y 限 2.02 是真实约束。

### 批2：TOP800 + INDUSTRY（放宽中性化组稀疏度，治 CW 根因）+ decay32/trunc0.05

CW 根因假设：SUBINDUSTRY 在 TOP800（~1600 只×cov0.526≈850 有效）上组内只剩 1–2 只 ⇒ 权重集中。放宽到 INDUSTRY 组更大。

### 批3–7：decay / truncation / 宇宙 三轴梯度（58 臂总计）

| 批 | 设置 | 最佳 2Y | 判定 |
|---|---|---:|---|
| 批3 | TOP2500 / SUBINDUSTRY / d16 / trunc0.08 | 1.87 | S 塌到 1.05 ⇒ 信号住小盘 |
| 批4 | **TOP800 / INDUSTRY / d16 / trunc0.05** | **1.99**（LLK3EMa1, 115窗） | CW 全过，只差 2Y 0.03 |
| 批5 | TOP800 / INDUSTRY / **d8** / trunc0.05 | 1.99（Grm9K3v5, 115窗） | decay 下调无增益，峰同值 |
| 批6 | **TOPCS1600** / INDUSTRY / d16 / trunc0.08 | 0.76 | ⛔ longCount 83 vs short 895 ⇒ 大宇宙纯空头无信息 |
| 批7 | TOP800 / INDUSTRY / d16 / **trunc0.08** + 610/252 变体 | 1.93 | truncation 抬高伤 2Y（1.99→1.93） |

**★ 结论（3 条可迁移定律）**：
1. **CW 的根因是中性化组稀疏度，不是权重上限**：SUBINDUSTRY→INDUSTRY 令 CW 0.167→PASS（5/8 臂过），代价 S −0.05/2Y −0.1；truncation 0.05→0.08 反而伤 2Y。
2. **2Y 限值 2.02 是 TOP800 专属**：TOP2500/TOPCS1600 下限值为 1.58。TOP800 触发 IS_LADDER（三年阶梯），且限值与 S 无关（恒 2.02）⇒ 「降 S 降闸限」杠杆对 2Y 无效。
3. **decay 轴对 2Y 单调性已穷尽**：d32→1.90 / d16→1.99 / d8→1.99；2Y 峰值 1.99，限 2.02，差 0.03 不可破。

**判定：earnings6 纯 ATOM 在「双 EPS 字段 + 610/252 双慢腿 + market 组 + ts_mean 平滑」这一形态族的参数轴已封顶**（7 批 58 臂）。剩余可试面（非参数轴）：
- 外层/内层**算子族替换**（group_rank→group_neutralize / ts_mean→ts_zscore）
- 加 winsorize 扫 12 档（EUR 甜点 std 0.3）
- 引入 `preliminary_eps_range_lower/upper_bound`（未测的辅助数值字段，aC 12/13）

## 3. 待试面

- **rank 化预处理**：`rank()` 包住 divide 输出，消除 EPS 量纲离群
- **winsorize 档位扫**：std 0.3/0.5/1
- **辅助字段族**：`eps_change_absolute_value` / `eps_change_percentage_value` / `preliminary_eps_range_*`（4 个未测数值字段）

## 4. 禁区

- ⛔ TOP2500/TOPCS1600+（信号住小盘，58 臂实证）
- ⛔ 66 字段中 62 个元数据字段不可作信号
- ⛔ SUBINDUSTRY@TOP800 结构性 CW（批2 已证）
- ⛔ decay 轴（d8/d16/d32 全扫过，2Y 峰 1.99）
