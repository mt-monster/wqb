# 波 193/194：universe 杠杆证伪 + 中性化 11 档发现（USA / board_gov_stats + RISK）

- 日期：2026-10-29
- 区域：USA / D1 / TOP3000
- 出发点：`board_gov_stats` 数据集级 S 天花板 1.30（距 1.58 闸差 18%），RISK 塔 3/3 撞 prod 墙（0.8325–0.8971）

---

## 发现 1（决定性）：universe 收紧方向是错的

**受控实验**：同一表达式、同一平台中性化、同一 decay / truncation / nanHandling，唯一变量 = universe。

| 表达式 | universe | alpha | S | F | TO | 2Y | SUB | invest_S | ratio | DD | margin |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `group_rank(ts_backfill(ceo_tenure_days, 120), subindustry)` + MARKET 中性化 | **TOP3000** | `E563xJMP` | **1.30** | 0.78 | 1.11% | 1.66 | 0.40 | 1.34 | 1.0308 | **10.40%** | **8.07bp** |
| 同上 | **TOP1000** | `0mYoaWVv` | **0.52** | 0.20 | 1.52% | 1.05 | 0.45 | 0.54 | 1.0385 | **14.57%** | **2.33bp** |

**结论**：
- S 从 1.30 掉到 0.52，**跌幅 60%**；DD 恶化 40%（10.40% → 14.57%）；margin 崩 71%（8.07bp → 2.33bp）。
- ⇒ **`board_gov_stats` 的治理信号集中在小盘尾部**（TOP3000 覆盖但 TOP1000 不覆盖的那 2000 只）。经济学解释一致：小盘股信息不对称大、治理质量离散度大、定价效率低，因此治理差异被定价得更充分；大盘股被卖方充分覆盖，治理质量已被 price in。
- **落地动作**：`board_gov_stats` 的 universe 固定 TOP3000，**不再向上收紧**。TOP500 只会更差，已派出的 `netw_TOP500` 仅作单调性验证。

**与既有教训的关系**：此前在 RISK 残差信号上「universe 降档必死」的结论，现在在 `board_gov_stats` 上得到**同向但机制不同**的确认 —— RISK 的死因是残差信号在大盘股上被套利掉，`board_gov_stats` 的死因是治理信息在小盘股上才有 alpha。两者都指向「宽 universe 优先」，但**不能反推「宽 universe 万能」**：仍需逐数据集实测。

---

## 发现 2（★ 本轮最高价值）：USA 有 11 档中性化，此前只用了 5 档

`get_platform_setting_options()` 实测 USA/D1 合法 neutralization 共 **11 档**：

```
NONE, REVERSION_AND_MOMENTUM, STATISTICAL, CROWDING, FAST, SLOW,
MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW_AND_FAST
```

**此前波 191/192 的中性化消融只覆盖 5 档**（SUBINDUSTRY / INDUSTRY / MARKET / STATISTICAL / NONE）。

未测的 6 档中，有 4 档直接对症 USA 区的支配性瓶颈（prod 墙）：

| 档位 | 机制含义 | 为什么可能是 prod 墙的钥匙 |
|---|---|---|
| **`REVERSION_AND_MOMENTUM`** | 剥离反转 + 动量风格暴露 | RISK 塔三颗（`88RAN85m` / `ZYQZEawY` / `qMLbW8xP`）核心机制就是**残差反转**。若 prod 0.83–0.90 源于"信号只是既有反转风格的重包装"，这一档可剥离该成分，prod 应显著下降 |
| **`CROWDING`** | 剥离拥挤度暴露 | prod 相关的本质是"与生产池同向拥挤"。拥挤度中性化是最直接的对症杠杆，此前完全未用 |
| `FAST` / `SLOW` / `SLOW_AND_FAST` | 快变 / 慢变风格剥离 | `board_gov_stats` 是慢变量（TO 1.1%），`SLOW` 剥离可能改变 S 与 SUB 的分布 |
| `SECTOR` | 比 INDUSTRY 粗、比 MARKET 细的分组 | 补全 MARKET/INDUSTRY/SUBINDUSTRY 的粒度阶梯 |

**这是方法论层面的漏项**：中性化不是「选一个最优分组粗细」，而是**同时包含风格剥离维度**（反转/动量/拥挤/快慢）。此前的 5 档扫描全部落在"行业粒度"这一个轴上，**风格剥离轴完全空白**。

**新的标准动作（写入 SOP）**：
1. 任何候选卡 `LOW_SHARPE` / `LOW_SUB_UNIVERSE_SHARPE` → 先扫粒度轴 5 档
2. 任何候选卡 `PROD_CORRELATION` → **先扫风格剥离轴** `CROWDING` / `REVERSION_AND_MOMENTUM` / `SLOW`，再考虑改表达式
3 **风格剥离优先于降相关表达式改造** —— 前者是零改动的设置层杠杆，后者要重跑整个骨架设计

---

## 发现 3：同账号跨区 prod 对照 —— USA 拥挤度远高于 IND / GLB

`alpha_corr_cache` 只读盘点（同账号并行会话的 prod 实测结果）：

| region | alpha | S | F | TO | 2Y | SUB | prod | fRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| **IND** | `LLMAM0xv` | 1.65 | 1.17 | 17.64% | 2.09 | 1.11 | **0.2167** | **0** | ✅ 可提交 |
| IND | `9qxL8vx9` | 1.96 | 1.39 | 19.98% | 2.58 | 1.10 | **0.3488** | **0** | ✅ 可提交 |
| **GLB** | `QPvdz93w` | 3.03 | 1.80 | 38.93% | 2.72 | 1.77 | **0.5197** | **0** | ACTIVE（已提交）|
| GLB | `d5WAzegY` | 2.73 | 1.93 | 26.05% | 2.42 | 1.44 | **0.5699** | **0** | ✅ 可提交 |
| GLB | `d5WqeQbx` | 2.71 | 1.43 | 7.55% | 2.68 | 1.64 | **0.5846** | **0** | ✅ 可提交 |
| GLB | `RREnK5R1` | 2.82 | 2.04 | 26.27% | 2.23 | 2.00 | **0.5874** | **0** | ✅ 可提交 |
| GLB | `A1VMzqJg` | 2.76 | 1.99 | 26.45% | 2.23 | 1.76 | **0.6431** | **0** | ✅ 可提交 |
| **USA** | `kqNRbvJP` | 1.82 | 2.04 | 13.52% | 2.43 | 0.91 | **0.8463** | 0 | ❌ |
| **USA** | `ZYQZEawY` | 1.64 | 1.00 | 18.58% | 1.64 | 0.78 | **0.8817** | 0 | ❌ |
| **USA** | `88RAN85m` | 2.68 | 1.01 | 61.77% | 1.68 | 2.21 | **0.8971** | 0 | ❌ |
| **USA** | `qMLbW8xP` | 1.73 | 1.02 | 8.19% | 2.48 | 0.84 | **0.8325** | 0 | ❌ |

**结论**：
- 同一账号、同一时期、同样 IS 全闸（fRA=0）的候选：**IND 0.22–0.35 / GLB 0.52–0.64 / USA 0.83–0.90**。
- USA 的 prod 基线比 IND 高 **3–4 倍**。⇒ **USA 不是「难挖」，是「生产池已经塞满」**。
- **映射到策略**：USA 区的正确目标不是「堆 IS 指标」，而是「找生产池里没有的机制」。而判断"生产池有没有"，唯一手段是 prod 实测，IS 指标完全无法替代。

**顺带**：兄弟会话的两个写法值得借鉴，都是我没用过的算子几何：
- `ts_regression(y, x, 252, rettype=0)` → 取残差。**比 `vector_neut` 更强的剥离**（滚动回归残差 vs 单期正交化），且 `rettype=0` 直接给残差。
- `trade_when(rank(ts_mean(外集字段, 22)) > 0.7, signed_power(subtract(group_rank(...), 0.5), 0.5), 0)` → **另一数据集作门控 + 居中后压缩尾部 + exit=0（空仓退出）**。注意这是跨数据集两塔组合，在 GLB 合规，在 USA 需按三塔禁混规则核对。

---

## 波 193 设计（board_gov_stats 提 S 第 6–8 自由度，8 条，已落库待派）

跳过所有已测尽的轴（分组轴 / backfill / 算子矩 / 结构比 / 5 档粒度中性化 / universe / decay），只测三类新几何：

| # | 模板 | 表达式 | 设计意图 |
|---|---|---|---|
| T1 | 尾部放大 | `signed_power(group_zscore(ts_backfill(ceo_tenure_days, 120), subindustry), 3)` | 治理 alpha 若为尾部效应（极端治理才有 alpha、中间无差别），放大尾部应提 S |
| T2 | 尾部压缩（T1 对照） | 同上 `, 0.5` | 若 T1 有效而 T2 无效，证明是尾部驱动；两者同效则说明是单纯分布变换 |
| T3 | 正交化剥离 | `group_rank(vector_neut(ts_backfill(ceo_tenure_days,120), ts_backfill(board_member_count_2,120)), subindustry)` | 剥离董事会规模，提纯"任期"本身（任期与董事会规模可能混淆） |
| T4 | flag 门控 | `trade_when(less(ts_backfill(ceo_chairman_duality_flag,120), 0.5), group_rank(ts_backfill(ceo_tenure_days,120), subindustry), -1)` | 只在"非董事长兼任 CEO"子样本里做任期排序；exit=-1 保持持仓不长仓 |
| T5 | 新字段·chairman 任期 | `group_rank(ts_backfill(chairman_tenure_days, 120), industry)` | 任期族 4 个未测字段之一；董事长任期比 CEO 任期更贴近"权力稳定性" |
| T6 | 新字段·median 任期 | `group_rank(ts_backfill(median_chief_officer_tenure_days, 120), industry)` | 高管团队任期中位数，衡量治理团队稳定性而非单一 CEO |
| T7 | 双维度乘性交互 | `group_rank(multiply(rank(ts_backfill(ceo_tenure_days,120)), rank(ts_backfill(board_external_connection_count,120))), subindustry)` | "既有经验又有人脉"的领导层；**乘法交互不是 add 加权**，不违反混信号禁令 |
| T8 | 分布形状对照 | `group_zscore(ts_backfill(ceo_tenure_days, 120), subindustry)` | group_rank → group_zscore 的形状差异（保守变换，作为 T1/T2 的基线） |

**ATOM 合规**：全部仅用 `board_gov_stats` 单数据集字段 ⇒ 单塔 INSIDERS，符合 ATOM 与三塔禁混。
**预检状态**：`preflight_expressions` 8/8 字段有效、`operator_audit` safe（无幽灵算子）。

## 波 194 设计（中性化风格剥离轴，6 条，待派）

| # | 表达式 | decay | neutralization | tag |
|---|---|---|---|---|
| 1 | RISK 最优骨架（同 `88RAN85m`） | 8 | **REVERSION_AND_MOMENTUM** | risk_d8_REVMOM |
| 2 | 同上 | 8 | **CROWDING** | risk_d8_CROWDING |
| 3 | 同上 | 8 | SLOW | risk_d8_SLOW |
| 4 | 同上 | 8 | SLOW_AND_FAST | risk_d8_SLOWFAST |
| 5 | tenure 骨架（同 `E563xJMP`） | 0 | **CROWDING** | tenure_d0_CROWDING |
| 6 | 同上 | 0 | **REVERSION_AND_MOMENTUM** | tenure_d0_REVMOM |

RISK 骨架：`group_zscore(reverse(ts_av_diff(ts_backfill(rsk65_trsd_4mfte_mfm, 22), 252)), subindustry)` / trunc 0.05 / nanHandling OFF
tenure 骨架：`group_rank(ts_backfill(ceo_tenure_days, 120), subindustry)` / trunc 0.08 / nanHandling OFF

**预期与判据**：
- 若 `REVERSION_AND_MOMENTUM` 或 `CROWDING` 能把 RISK 骨架的 **S 保持 ≥1.58 且 prod 掉到 <0.70** ⇒ RISK 塔复活，波 182–190 的 60 条资产里可能救回 1–3 颗。
- 若两者都让 S 崩（<1.0） ⇒ 证明"残差反转"就是该信号的**唯一收益来源**，剥离后无残留 ⇒ RISK 塔彻底封盘，结论升级为"机制层面不可救"而非"prod 偶发撞墙"。
- **两种结果都有决定性信息价值**，不是赌。

---

## 执行状态（2026-10-29 21:20）

| 项目 | 状态 |
|---|---|
| 波 193 表达式落库 | ✅ 已写（`upsert_expressions` wave=193, 8 条, status=selected） |
| 波 193 派发 | ⏳ 未完成 — 仿真槽被并行会话占满，仅零星成功 |
| 波 194 派发 | ⏳ 仅 `risk_d8_SLOW` 成功（`3traHy59W4gwc0u1300NvFy7`），其余 5 条 429 |
| `0mYoaWVv`（universe 证伪证据） | ✅ 已收（S 0.52） |
| `3imd2aAP54GcG215GaVXzq8`（netw_TOP500 单调性验证） | ✅ 已派出 |
| `ZYQZbnYx` prod | ❌ 未取到 — correlation 锁被并行会话连续占用 >13 分钟 |

**资源竞争实测**：账号级单并发 correlation 锁被并行会话的 `mLoO1lzW` 连续占用；仿真槽每次只能进 1 条（`batch_create_simulations` 的 8 条里成 1–2 条）。⇒ **多会话共享账号时，prod 测量与批量仿真都需要错峰**。
