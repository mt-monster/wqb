# blaoMOAq 双目标优化 + repair 报告（2026-11-16 17:2x ~ 17:3x）

> **【17:37 结论翻转】CW 已修复成功。** 上一步判「结构性不可修」是错的——根因不是 `group_rank` 本身，而是**时间平滑加错了位置**：14 条全把平滑加在 rank **输入侧**（`group_rank(ts_mean(...))`），正确做法是加在 **输出侧**（`ts_mean(group_rank(...), w)`）。输出侧平滑让 `CONCENTRATED_WEIGHT` 从 WARNING 转 PASS，且窗口越短 S 越高。
> **修复件 `blaoQ6Kq`（输出侧 `ts_mean w=5`）：S 1.65 / F 1.15 / 2Y 2.67 / sub 1.34 / TO 3.32% / margin 36.47bp，`checks.fail=[]`、`CONCENTRATED_WEIGHT=PASS`、`ra_failed=false`、self .1548 —— 全闸通过。** 备选 `gJaR8e0J`（w=10）亦 Ra=0、2Y 2.75 略高。
> 目标 B：压缩仍到物理下限（5 算子 → 修复件 6 调用，多 1 个 ts_mean 是修复必需）。**本轮零提交，提交权归用户。**
> 全程 MCP `create_multi_simulation` + `lookINTO_SimError_message` + `batch_get_alpha_metrics` + `preflight_expressions`，零临时脚本。

## 【17:37 新增】repair 成功：输出侧时间平滑治 CW

对照 brain-alpha-repair 证据页（`concentrated-weight-evidence.md`：「**时间平滑治 CW**」，唯一可继承结论）——上一轮 14 条把平滑加在 `group_rank` **输入侧**故全败；本轮改加**输出侧**即成功。

| 变体 | 骨架 | S | F | 2Y | sub | TO | CW | Ra failed |
|---|---|---:|---:|---:|---:|---:|---|---:|
| 原件 | `group_rank(decay60)` | 1.63 | 1.12 | 2.66 | 1.33 | 4.68% | WARNING | 1 |
| group_neutralize 替 rank | `group_neutralize(decay60)` | 1.08 | 0.67 | 2.22 | 1.09 | 4.41% | — | 3 |
| group_neutralize + 输入侧 ts_mean22 | — | 1.05 | 0.63 | 2.02 | 1.18 | 3.61% | — | 2 |
| 输入侧 ts_mean22 再 rank | `group_rank(ts_mean(decay60,22))` | 1.46 | 0.95 | 2.67 | 1.22 | 3.05% | — | 2 |
| 输出侧 ts_mean22（`d5aEZAxw`） | `ts_mean(group_rank(decay60),22)` | 1.54 | 1.04 | 2.76 | 1.28 | 2.67% | **PASS** | 1（S 差 .04） |
| 输出侧 ts_mean15（`9qlapxk2`） | 同上 w=15 | 1.57 | 1.06 | 2.75 | 1.30 | 2.88% | PASS | 1（S 差 .01） |
| **输出侧 ts_mean10（`gJaR8e0J`）** | 同上 w=10 | 1.63 | 1.13 | **2.75** | 1.33 | 3.08% | **PASS** | **0** ✅ |
| **输出侧 ts_mean5（`blaoQ6Kq`）** | 同上 w=5 | **1.65** | **1.15** | 2.67 | **1.34** | 3.32% | **PASS** | **0** ✅ |

**规律**：输出侧 `ts_mean` 窗口 w∈[5,10] ⇒ Ra=0；w≥15 ⇒ S 掉到 1.57 以下触 LOW_SHARPE 破线；w=5 是最优（S/F/sub 最高，2Y 略低于 w=10 但仍 2.67 宽裕）。**w=5/10 是修复甜点区。**

**修复件 `blaoQ6Kq` 全维度**
- 指标：S **1.65** / F **1.15** / 2Y **2.67** / sub **1.34** / investability 1.62 / TO **3.32%** / margin **36.47bp** / long 344 / short 306（对比原件 long?/short?，持仓更均衡）。
- 闸：`checks.fail=[]`、warning 仅 MATCHES_COMPETITION/THEMES（无 CW）、`CONCENTRATED_WEIGHT=PASS`、`ra_failed=false`。
- 相关：self **.1548**（top `bl6KwjwK` .1548，非当日提交件；pool 29/34）。**prod 未测——平台相关性槽熔断剩 439s，提交链前置待补**。
- 塔六元组：`GBR/D1/SENTIMENT`｜倍率 **×1.7**｜当季 **0**｜交后 **1**｜**否（门槛 3，差 2 颗）**｜塔边际 **0**。
- 六维：ops 4 / fields 2｜T1 −0.0016｜T2 +0.0004｜T3 flat｜**T4 +2 新字段**（`snl27_top75pctranking`/`snl27_top75pctrankingavg`）｜T5/T6 n/a。

**采纳建议**：原件 `blaoMOAq` 标 `SUPERSEDED`（同骨架互相关必 >0.99），改以 `blaoQ6Kq` 为候选；`gJaR8e0J` 为备选（2Y 更高）。**但塔边际为 0（当季 0→1 不点亮），且 prod 未测**——是否占用 ET 配额交用户定。提交前须补：prod 回源（槽恢复后）、稳健审计、方案 D、同席互相关。

---

## 以下为 17:2x 初版（结论已被上节推翻，保留作过程留痕）

## 0 关键纠错（用户 17:16 质疑）

初稿把 `GBR/D1/SENTIMENT` 误读为「当季 3 已点亮」——实为**把 `EUR/D1/sentiment=3` 串读到了 GBR**。
权威复核（`get_pyramid_alphas` 显式季度日期 + OS 列表 GBR 全部已提交件交叉验证）：

- **`GBR/D1/SENTIMENT` 当季 = 0**（OS 列表无任何 GBR alpha 带此塔）
- 倍率 ×1.7 正确（`get_alpha_details().pyramids` 确认）
- ⇒ blaoMOAq 若提交是 **0→1，仍不点亮（门槛 3），塔边际 0**——理由从「已亮」纠正为「离点亮差 2 颗」，但结论（边际 0）碰巧不变。
- 战略含义反而更重要：它是 GBR/SENTIMENT 从 0 往 3 走的**稀有高倍率载体**（×1.7），只可惜 CW 过不了闸。

## 1 原件快照

```
group_rank(ts_decay_linear(vec_avg(snl27_top75pctranking) - vec_avg(snl27_top75pctrankingavg), 60), subindustry)
GBR / TOP700 / delay1 / decay8 / MARKET / trunc0.08 / nan OFF
```
S **1.63** / F **1.12** / TO **4.68%** / 2Y **2.66** / sub **1.33** / margin **25.32bp** / investability 1.62
self **.1504**（pool 29，top `bl6KwjwK` 0.15，安全）
**`CONCENTRATED_WEIGHT` WARNING，`ra_failed_checks=[CONCENTRATED_WEIGHT]` ⇒ 按铁律 WARNING 视同 FAIL，提交必拦。**
塔 GBR/D1/SENTIMENT ×1.7，当季 0（纠错后）。

## 2 压缩：5 算子已到下限

`op_count` = 5（vec_avg×2 + group_rank + ts_decay_linear + subtract），`compress` 无候选、`scan --delete` = 0。
两字段各一次，无重复子式，变量合并 0 收益。六维：ops 3 distinct（T1 −0.0043）/ fields 2（**T4 +2 新字段**硬收益）/ T3 flat。

## 3 CW 修复三通道全试（14 条实测）

### 3a 削极值通道（4 条）

| 变体 | id | S | F | sub | 2Y | Ra failed | CW |
|---|---|---:|---:|---:|---:|---:|---|
| 原件 | blaoMOAq | 1.63 | 1.12 | 1.33 | 2.66 | 1 | 未修 |
| winsorize std2 | VkN2PYb0 | 1.63 | 1.12 | 1.33 | 2.66 | 1 | **逐位相同，no-op**（group_rank∈[0,1]，std2 已覆盖全域） |
| tail 0.05/0.95 | blaoqW0Z | **1.91** | **1.30** | **0.75** | 2.11 | 2 | 未修 + sub 崩 |
| vec_sum 替 vec_avg | 1YWadn3z | 1.58 | 1.08 | 1.33 | 2.57 | 1 | 未修 |
| rank 去分组 | xAvPkm7l | 0.92 | 0.55 | 0.63 | 1.99 | 3 | 全崩 |

### 3b 窗口精调通道（4 条，④d 邻域）

| 窗口 | id | S | F | sub | 2Y | Ra failed |
|---:|---|---:|---:|---:|---:|---:|
| 54 | xAvPkd3p | 1.53 | 1.03 | 1.28 | 2.45 | 2 |
| 57 | N1PgrRVg | **1.61** | **1.11** | 1.35 | 2.64 | 1（CW 仍在） |
| **60（原）** | blaoMOAq | **1.63** | **1.12** | **1.33** | **2.66** | 1 |
| 63 | blaoqdOR | 1.56 | 1.05 | 1.26 | 2.50 | 2 |
| 66 | LLKg1dZ2 | 1.59 | 1.08 | 1.32 | 2.61 | 1 |

60 是最优窗口；精调无解 CW。

### 3c 换轴通道（4 条，L1 分组轴杠杆）

| 轴+窗口 | id | S | F | sub | 2Y | Ra failed |
|---|---|---:|---:|---:|---:|---:|
| industry 60 | mLarA6lW | 1.24 | 0.78 | 1.14 | 2.58 | 3 |
| sector 60 | npaZ2r1M | 1.07 | 0.70 | 0.76 | 2.22 | 3 |
| industry 57 | O0WbZg17 | 1.24 | 0.78 | 1.17 | 2.57 | 3 |
| sector 57 | ZYa2nNR8 | 1.08 | 0.71 | 0.81 | 2.21 | 3 |

subindustry 是信号承重轴——换粗轴丢失 peer-relative 精度，S 腰斩。**与 e7adKz7g 的「industry→subindustry 救 sub」正好相反：这里 subindustry 救 S，但代价是 CW。**

### 3d group_zscore 替换（1 条）

`1YWadzj6` S1.35/F0.89/2Y2.53/Ra failed 3 —— 全崩。

## 4 根因

`group_rank(·, subindustry)` 在 GBR/TOP700 下，部分 subindustry 组内样本极少（1–3 只），
组内 rank 输出趋近二值（0 或 1），经 scale 后少数票占极大权重 ⇒ `CONCENTRATED_WEIGHT`。
- 削极值无效：winsorize 对 rank 有界输出 no-op；tail 削rank两端反而破坏 sub 与 2Y。
- 换轴无效：subindustry 精度是信号来源，换粗轴 S 腰斩。
- 窗口无效：CW 来自横截面分组结构，与时序平滑窗长无关。

⇒ **CW 与信号骨架同源，不可在不换骨架的前提下修复**。达到 skill §6 止损（14 条变体 ≥3 轮结构性问题）。

## 5 universe 扫描

GBR/delay1 只有 TOP700 **单档**（`get_platform_setting_options` 权威）⇒ 按 ⑤ 规则直接跳过，无优化空间。

## 6 建议（交用户）

1. **不提交**——CW 是硬 WIRE（WARNING 视同 FAIL），提交节点必拦。
2. **若一定救**：转 `brain-alpha-repair` 换终算子骨架（如 `group_rank` → `group_neutralize` + 连续权重，或改用 `bucket(rank(·))` 做分组轴），保住 subindustry 的 precision 同时让组内输出连续——这是唯一未试方向。
3. 塔 GBR/SENTIMENT 当季 0，本件是 ×1.7 高倍率稀有载体，值得 repair 再试；但直接提交不可行。
4. 全部 14 个变体标 `SUPERSEDED` / `REJECT`，无采纳件。

## 附：全维度

塔六元组：`GBR/D1/SENTIMENT`｜×1.7｜**0**｜交后 1｜**否（差 2 颗）**｜边际 0（纠错后）。
六维：ops 3 / fields 2｜T1 −0.0043（微改善）｜T2 +0.0004（软成本）｜T3 flat｜**T4 +2 新字段（`snl27_top75pctranking`/`snl27_top75pctrankingavg`）硬收益**｜T5/T6 n/a。

---

## 【17:56 提交链更新】blaoQ6Kq prod 撞墙 ⇒ 未提交

用户 17:40 点名提交 `blaoQ6Kq`。前置全部补齐（稳健 PASS、方案 D pass_offset、verdict exit10、配额 ET11-16 2/4）后，**prod 当刻 refresh 实测 0.9405 ≥ 0.7 —— 硬闸否决、无豁免，未提交、未占配额**。

- prod 直方图：max **0.9405**（range[0.9,1.0] 有 1 个异常点），min −0.3722，其余 99.99% 落在 [−0.4,0.6] ⇒ **单点撞墙**（某颗已提交 ACTIVE 与本件相关 0.9405），非整体高相关。
- 平台 prod 槽不稳：先被另一检查（holder `0mPKr3bq`）占单并发槽，再触发账号级熔断（两轮共等 ~13 分钟冷却），最终 refresh 拿到权威值。
- 台账 `submit_blaoQ6Kq` = `REJECT_PROD`（prod .9405、submit_attempted=false、quota_consumed=false）。
- **结论**：CW 虽已修复（Ra=0 全闸过），但 prod 撞墙使本族不可交。备选 `gJaR8e0J`（输出侧 w=10，同骨架同字段同塔）prod 待实测确认——窗口不同 PnL 略异，相关值可能变化，但撞的是同一批生产池，预期仍高。若也 ≥0.7 ⇒ 整个 snl27 申报结构族判死。
