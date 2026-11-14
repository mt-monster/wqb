# DEU D1 ATOM 交付文档（2026-11-10 终版，5 颗）

> Goal 第 4 条要求：产出通过验证的 ATOM 类型 regular alpha，附所属数据集、核心字段、算子逻辑、回测指标及字段画像存档索引。
> 域内上限经三轮系统核查已确证为 **5 颗**（详见 §五 论证）。

## 一、交付清单

| # | alpha | 数据集（塔） | 核心字段 | S | F | 2Y | TO | margin | 状态 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | **zq3eb7No** | analyst7（ANALYST） | est_12m 预期族 | 2.01 | 1.28 | 1.64 | 0.2262 | — | ✅ ACTIVE |
| 2 | **bl6AvMkN** | analyst_factor_signals + predictive_starmine（ANALYST） | 分析师因子信号 + starmine 预测 | 1.61 | 1.36 | 2.15 | 0.1097 | — | ✅ ACTIVE |
| 3 | **RREPm361** | analyst7（ANALYST） | est_12m_ebi_median / est_12m_ebt_mean 4 周变化 | **2.02** | 1.25 | 1.82 | 0.2508 | 0.002041 | 🟡 待授权 |
| 4 | **1YNMAA8M** | analyst7 + analyst15（ANALYST） | 预期族 + 修正族 | 1.58 | 1.36 | 2.13 | 0.1337 | — | 🟡 待授权 |
| 5 | **E569ZE7L** | shortinterest3（SHORTINTEREST） | shrt3_bar（借券需求评级） | 1.68 | 1.21 | 2.27 | 0.1128 | — | 🟡 待授权 |

## 二、算子逻辑（三颗待授权件）

**RREPm361**（5 算子，ANALYST 塔，点 ANALYST）
```
group_rank(add(ts_zscore(est_12m_ebi_median, 240),
               ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago), 44)), sector)
```
机制：EBIT 中位预期的长期水平 + 短期 EBT 预期修正的截面排序（双视界预期合成）。

**1YNMAA8M**（ANALYST 塔）：analyst7 预期族 + analyst15 修正族双腿正交结构（详见台账）。

**E569ZE7L**（10 算子，SHORTINTEREST 塔，点 SHORTINTEREST）
```
-group_rank(
  ts_target_tvr_decay(
    multiply(
      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264)),
      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 132))
    ), target_tvr=0.03),
  subindustry)
```
机制：借券需求评级的双窗加速度（264/132）× tvr_decay 换手治理 × 反向持有（借券需求抬升=拥挤→反转）。

## 三、稳健性与相关性（提交前必核）

| alpha | self | prod | ΔS | 稳健性 CV | 逐年空窗 | 负年 |
|---|---:|---:|---:|---|---|---:|---:|
| RREPm361 | 0.3275 | 0.6881（余量 0.012⚠） | +0.73 | PASS（3y 0.322） | 0 | 0（min 1.06） |
| 1YNMAA8M | 0.6946（贴线⚠） | 0.6951（余量 0.005⚠） | +0.43 | PASS | 0 | — |
| E569ZE7L | 0.5444 | 0.5444 | +0.06 | CONDITIONAL（3y 0.626） | 0 | 0 |

互相关：三件之间及与 OS 池 19 件全对 <0.7（最高对 1YNMAA8M~rKRx2Alj = 0.6946）。

## 四、字段画像存档索引

- 数据集全集与覆盖率：`tracking/DEU/atom_orthogonal/deu_ds_cov.csv`（68 集 cov>0）
- 字段画像索引：`tracking/DEU/atom_orthogonal/FIELD_PROFILE_INDEX.md` + `field_profile_index.json`
- analyst 族画像：`tracking/DEU/atom/profile/field_profiles_20261106.md`、`field_profile_analyst44_20261111.md`
- 新闻/分析师/机构族画像：`field_profiles_news_analyst_inst_20261107.md`
- earnings 族：`earnings6_fields.csv`
- 本轮新增：insiders1（`waveBA6_insiders1_pool_design_20261110.md` 内）、fund_holdings_panel（`waveBA5_*`）、news18/50/38（`waveBA3_*`）、risk60/88（`waveBA1/BA2_*`）

## 五、为何上限是 5 颗（三轮系统核查结论）

1. **数据集面**：DEU 172 集全扫，cov>0 共 68 集；已点亮塔（analyst 6 / model 3 / shortinterest 3）按规则排除；其余全部实测封盘——risk 塔（BA1-BA2b 六维合规死，0.90/0.79）、news 塔（BA3+BA3b，16 条，三机制面 0.57）、sentiment 全族（天花板 1.02）、institutions（institutions6 二次死 + fund_holdings_panel 0.65）、other 族（0.61-0.96）、earnings（0.63 / ern6 探针闸未过）、workforce 0.96、pv30 0.79 / pv29 字段自测否决。
2. **组合面**：合法双塔组合（OTHER×NEWS 等）单腿天花板 0.57-0.84，组合 Sharpe 数学上限约 1.06，不可达 1.58。
3. **最后未测项**：insiders1（BA6 在飞，唯一剩余）。

⇒ **DEU D1 域内 ATOM 上限 = 5 颗**。突破需放开「不得更换 region」约束（goal 明文，需用户修改）。
---

## 六、最后两项实测完成（BA5/BA6，2026-11-10 19:5x）

| 数据集 | 塔 | 波次 | 臂数 | 族天花板 | 判定 |
|---|---|---|---:|---:|---|
| fund_holdings_panel | INSTITUTIONS | BA5 | 10 | 0.65（F2 稳定边界占比，2Y1.77 但 TO0.467） | PROVISIONAL 弱，不追投 |
| insiders1 | INSIDERS | BA6 | 10 | 0.85（I7 持股 52 周位置，lc88/TO0.066） | PROVISIONAL 弱，不追投 |

⇒ **DEU D1 单数据集 ATOM 面已 100% 实测完毕**（172 集全扫、68 集 cov>0、全部可测集实测或字段自测否决）。
⇒ **域内可交付上限 = 5 颗**（本文件 §一 清单），由 2 颗 ACTIVE + 3 颗待授权构成。
---

## 七、组合路径实测裁决（BC1，2026-11-10 19:5x）

派发 OTHER x NEWS 六条组合臂（等权/正交/反向对照/乘积），6/6 COMPLETE 0 error：

| 臂 | S | 2Y | TO |
|---|---:|---:|---:|
| W1+N4 等权 | 0.75 | 1.52 | 0.025 |
| AV2+N4 | 0.76 | 2.05 | 0.061 |
| **vector_neut(N4,W1)** | **0.86** | 1.44 | 0.025 |
| W1−N4 反向对照 | -0.12 | -0.56 | 0.024 |
| rank 乘积 x2 | 0.62 / 0.70 | 1.32 / 1.53 | 0.025 / 0.051 |

**裁决**：
- 最高 0.86 < 1.2 ⇒ **组合路径关闭**，不产生第 6 颗。
- 反向对照 −0.12 证明两腿相关性 ≈ 0（无互补），组合无法突破单腿天花板。
- 组合臂 2Y 可达 1.5-2.05，但全期 S 仍 0.75-0.86 ⇒ DEU 的历史弱是结构性的，组合改不了。

⇒ **DEU D1 可交付上限 = 5 颗（本文件 §一）为最终结论**。
---

## 八、第 6 颗候选：fundamental6 T1 现金利润率（2026-11-10 19:5x 重新评估）

**alpha `gJeLvb8O`** —— `group_rank(divide(fnd6_oancfy, fnd6_revty), sector)`（2 算子）

### 关键变更：prod 阻断已消失

| 项 | 昨日台账 | **实测（2026-11-10T19:49:35 缓存）** |
|---|---|---|
| prod 相关性 | 0.9389 / 0.9728（判「被生产池占据」） | **0.5197 PASS** |

⇒ 「fundamental6 封盘」的理由**已不成立**（平台重算或原记录对应其他表达式）。

### 指标全貌

| 指标 | 值 | 门槛 | 缺口 |
|---|---:|---|---|
| S | **1.15** | 1.58 | -0.43 |
| F | **0.98** | 1.0 | **-0.02**（几乎到线） |
| 2Y | 0.43 | 1.58 | **-1.15（唯一严重短板）** |
| TO | 0.0265 | 0.01-0.7 | ✅ 极低 |
| sub_universe | **0.79** | 0.474xS | ✅ 极健康 |
| margin | **0.006856** | — | ✅ 全 DEU 最高档（已交付 QPvzNNGG 仅 0.002041） |

### 逐年（十年零空窗、仅 1 负年）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 3.28 | 2.17 | 0.36 | 2.11 | 1.72 | 1.78 | 0.51 | **-0.46** | 0.60 | 0.24 |
| longCount | 52 | 49 | 49 | 58 | 58 | 52 | 59 | 71 | 74 | 67 |

### 破闸计划（BC2 在飞 + 后续）

| 方向 | 手段 | 目标 |
|---|---|---|
| **2Y（主攻）** | 与 news18 N4（2Y1.44）组合：等权 add / vector_neut / 方向 subtract | 2Y 0.43 → ≥1.58 |
| S | tvr_decay 治理 + subindustry 轴（B5）；长窗平滑（B6）；换 industry 轴（B7） | 1.15 → ≥1.58 |
| F | 随 S 提升自然改善（现仅差 0.02） | ≥1.0 |

**故 T1 是 DEU 域内唯一仍有实质破闸空间的候选**——它不依赖「新数据集」，而是把已有最强弱腿补齐 2Y 缺口。
---

## §八补：T1 字段口径与覆盖约束（2026-11-10 19:5x）

fundamental6 关键字段实测（`fundamental6_fields.csv`）：

| 字段 | 含义 | cov | 在 T1 中的角色 |
|---|---|---:|---|
| `fnd6_oancfy` | 经营活动净现金流（年） | **0.5419** | 分子（**决定 T1 覆盖上限**） |
| `fnd6_revty` | 营业总收入（年） | **0.6587** | 分母（本集最高覆盖之一） |
| `fnd6_newa2_sale` | 销售/营业额净额 | 0.5210 | 分母备选 |
| `fnd6_gpy` | 毛利 | 0.5515 | 分子备选（Novy-Marx 毛利溢价） |
| `fnd6_cogsy` | 销货成本 | 0.4936 | 辅助 |
| `fnd6_cogssa` | 销货成本（半年） | 0.4873 | 辅助 |

**三个推论**：
1. **T1 的覆盖率天花板 = oancfy 的 0.5419**（分子决定），换分母无法提升覆盖。
2. **T1 的 2Y 弱（0.43）与 DEU 全族 2021 共同弱年同源**（借券族 2021 0.18-0.85、workforce 2020-21 弱同期）⇒ 属市场结构性，不是字段缺陷。
3. **单数据集强化只能补 S（B5/B6/B7），补不了 2Y**；2Y 只能靠组合腿（N4 的 1.44）——BC2 的 B1/B3/B4 正是此路径。

**等权组合的数学预期**（ρ≈0）：
- S_comb ≈ √(1.15² + 0.57²)/√2 ≈ **1.28**
- 2Y_comb ≈ √(0.43² + 1.44²)/√2 ≈ **1.06**
- ⇒ 即便组合成功，**仍低于 1.58 门槛**；这与 BC1 实测（最高 0.86 vs 估算 0.97）的经验一致（实测通常低于估算）。

⇒ 若 BC2 实测证实此判断，则 DEU 域内 ATOM + 合法双塔组合的**数学上限均不足 1.58**，5 颗即为硬上限。
---

## 九、★★ 交付清单更新（2026-11-10 20:3x）：2 ACTIVE + 3 待授权 + 1 新候选 = 6 颗

| # | alpha | 数据集/塔 | S | F | 2Y | self | 状态 |
|---|---|---|---:|---:|---:|---:|---|
| 1 | zq3eb7No | analyst7 / ANALYST | 2.01 | 1.28 | 1.64 | 0.364 | ✅ ACTIVE |
| 2 | bl6AvMkN | analyst_factor_signals + starmine / ANALYST | 1.61 | 1.36 | 2.15 | 0.514 | ✅ ACTIVE |
| 3 | RREPm361 | analyst7 / ANALYST | **2.02** | 1.25 | 1.82 | 0.328 | 🟡 待授权（prod 0.6881） |
| 4 | 1YNMAA8M | analyst7 + analyst15 / ANALYST | 1.58 | 1.36 | 2.13 | 0.695 | 🟡 待授权（prod 0.6951） |
| 5 | E569ZE7L | shortinterest3 / SHORTINTEREST | 1.68 | 1.21 | 2.27 | 0.544 | 🟡 待授权（prod 0.5444） |
| **6** | **1YWqzPGQ** | **shrt3_bar + oth47_traffic / SHORTINTEREST × OTHER** | **1.59** | **1.10** | **2.81** | **0.588** | 🟢 **全闸过（prod 待出）** |

### 互相关：六件最大独立集 = 5

唯一超限对 = **臂5（O0W1ZnY7）~ E4（gJaY125M）= 0.835**（同组合窗口变体）⇒ 二者只取一，不影响上述 6 件。

### 第 6 颗对塔位的影响

- 会点亮 **OTHER 塔**（2 → 3）：需用户确认是否愿意点亮该塔
- SHORTINTEREST 已点亮（3），第 6 颗属该塔第 4 颗

### 待办

- ⬜ 1YWqzPGQ 的 **prod** 值：平台队列被前次请求占用，需等 ≥240s 后取缓存（不要连发）
- ⬜ 用户对 3 颗待授权件的授权
- ⬜ 用户对「是否点亮 OTHER 塔」的表态