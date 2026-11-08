# 稳健性审计 · 2026-11-07

> Skill: `brain-alpha-robustness`（Phase B/C）｜口径：**最近 3 个 IS 年**（2021/2022/2023）
> 骨架族：KOR/TOP600 `rsk68` 风险权重差分（`subtract(group_rank(ts_delta(vol_short,22),·), group_rank(ts_delta(dadv,22),·))`）

## 0 判定口径更正（重要）

历史台账（`9qxdnV72` CV 0.4374 / `6Xdo27P5` CV 0.7336）用的是**全历史 10 年 CV**。skill 现行判定表已改为 **Recent-3yr CV**（"年度行只在最近 3 个 IS 年上计算"），且明确"全历史 CV / 厂字形 / max-min 只作信息软标记，绝不据此 REJECT"。

本次起按现行口径。两者在"末段爆发型"信号上差异极大（本例全历史 0.8469 vs 近3年 0.9844），**不得混用**。

## 1 三颗同骨架候选

| 指标 | `akKGqOmx`(subindustry) | `kqN92KpK`(industry) | `d5Wvpmbx`(sector) |
|---|---|---|---|
| S / F / 2Y / sub | 1.92 / 1.16 / 4.28 / 1.68 | 1.91 / 1.21 / 4.24 / 1.80 | 1.82 / 1.25 / 4.10 / 1.75 |
| TO / margin | 0.282 / 7.27bp | 0.263 / 6.90bp | 0.246 / 9.39bp |
| **prod** | **0.5459** | 0.6196 | 0.6906 |
| prod 余量 | **0.1541** | 0.0804 | 0.0094 |
| self | 0.1549 | — | 0.2023 |
| RA failed | **0** | **0** | **0** |
| 近3年 Sharpe | 0.01 / 2.92 / 5.62 | 1.07 / 3.12 / 5.28 | 0.94 / 3.46 / 4.69 |
| 近3年均值 | 2.85 | 3.16 | 3.03 |
| **近3年最低** | **0.01** | 1.07 | 0.94 |
| **平年数（|s|<0.3）** | **1（2021）** | **0** | **0** |
| **CV（样本 std/mean）** | **0.9844** | **0.6669** | **0.6309** |
| CV（总体 std/mean） | 0.8038 | 0.5445 | 0.5151 |
| max/min（近3年） | **562** | 4.93 | 4.99 |
| 衰减比（末年均值/全期） | 2.93 | 2.76 | 2.58 |
| 全历史 CV（仅信息） | 0.8469 | 0.8256 | 0.7921 |

## 2 逐项判定（按 Phase C 表）

`akKGqOmx`：

| 检查项 | 实测 | 档位 |
|---|---|---|
| WebDataScope failed | 0（RA 0 / PPA 0，无 PENDING 在名单） | PASS |
| **Recent-3yr Sharpe（主判定）** | 2021 在 0–0.3（平年） | **CONDITIONAL** |
| **Recent-3yr CV** | **0.9844** ≥ 0.60 | **REJECT** |
| **max/min（近3年）** | **562** > 5 | **REJECT** |
| 衰减比 | 2.93 ≥ 0.50 | PASS |
| 平年 | 1 | CONDITIONAL |
| Sub-universe | 平台 PASS（1.68 / 限 1.10） | PASS |
| 算子数 | 5（软标记线，未超） | PASS |
| Margin @ TO | 7.27bp @ 28.2% | PASS |
| 经济可解释性 | 做多"波动率下降 + 成交额收缩"的风险权重改善股，做空反向 | PASS |

⇒ **两项硬标触发，Phase C 判 REJECT**（其余项干净）。

`kqN92KpK`：CV 0.6669（样本）/ 0.5445（总体）、max/min 4.93（CONDITIONAL）、平年 0、主判定 PASS ⇒ **CONDITIONAL～REJECT 边缘**，取决于 std 口径。

`d5Wvpmbx`：CV 0.6309（样本）/ 0.5151（总体）、max/min 4.99（CONDITIONAL）、平年 0、主判定 PASS ⇒ **CONDITIONAL～REJECT 边缘**。

## 3 结构性成因

三颗都是**同一个骨架族，只有分组轴不同**，年表高度同构：2014–2018 中等（1.0–2.1）→ 2019–2021 弱（0.0–1.1）→ 2022–2023 极强（2.9–5.6）。

- 近 3 年 Sharpe 从 0.01 跳到 5.62 ⇒ 无论样本还是总体 std，CV 都 ≥ 0.6。
- `max/min = 562` 完全由 2021 年的 0.01 做分母造成，该指标在"存在平年"时信息量极低。
- **不是某一颗的偶发问题，是这族信号的"近端爆发"特性**：2019–2021 三年几乎无收益是真实存在过的 24+ 个月失效窗口，不是统计假象。

## 4 裁决与执行结果

用户裁决：**改提 `kqN92KpK`**（industry 轴）。

**已提交，ACTIVE / OS**，2026-11-07T09:19:13-05:00（ET）。

| 项 | 值 |
|---|---|
| name | `KOR_R_rsk68riskdiff_01` |
| 表达式 | `subtract(group_rank(ts_delta(rsk68_weight_volatility_short,22), industry), group_rank(ts_delta(rsk68_weight_dadv,22), industry))` |
| ops / 设置 | 5 ｜ KOR/TOP600/D1/decay4/REVERSION_AND_MOMENTUM/trunc0.08/nan OFF |
| 闸门 | RA failed 0｜self 0.2019（池 30）｜**prod 0.6196**（缓存 21:59:28，< 0.7）｜robustness **CONDITIONAL** |
| 指标 | S1.91 / F1.21 / 2Y4.24 / sub1.80（限 1.09）/ TO0.263 / margin 8.03bp |
| 塔 | `KOR/D1/RISK`×1.3，effective=1（纯 ATOM） |
| 边际贡献 | **ΔSharpe +0.44**（EQUITY:KOR:1:POWER_POOL 池 4.41→4.85，分散非稀释） |
| 配额 | ET 2026-11-07 REGULAR 0/4 → 用后 1/4 |
| 标签清理 | 平台自动追加 `PowerPoolSelected`，已用 `set_alpha_properties` 清回 `[CH_REG, SRC_risk68, CORR_060]` |

**落台账**：`KOR/robustness_kqN92KpK` = CONDITIONAL，`failed_checks=[]`，soft_flags 记录 CV 口径分歧 / max-min 4.93 / 同族历史弱档 / 全历史 CV 0.8256（仅信息）。

**未提交**：`akKGqOmx`（稳健性 REJECT）、`d5Wvpmbx`（起点）—— 同席位只应保留 1 颗。

**未做**：`get_alpha_pnl` 回撤日历 / Top-5 集中度（软标记项，不改变判定）。

**未做**：`get_alpha_pnl` 回撤日历 / Top-5 集中度（软标记项，不改变 REJECT 结论）。
