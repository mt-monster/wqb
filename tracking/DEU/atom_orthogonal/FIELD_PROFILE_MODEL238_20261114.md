# DEU S1 字段画像：model238 SmartHoldings（2026-11-14）

> 归档：`tracking/DEU/atom_orthogonal/FIELD_PROFILE_MODEL238_20261114.md`（命名规则同前）
> 数据源：MCP get_datafields（DEU/TOP500/D1 complete）。历史：ledger mdl238_r1/r2_templates 两轮（BE238 r53/r56/r57 混合波用过，单集纯机制波未穷尽）。

## 一、数据集画像

| 维度 | 值 |
|---|---|
| 塔位 | DEU/D1/MODEL（已点亮塔内**未点亮数据集**——塔按数据集计，predictive_starmine/model264 等已点亮排除，本集 0 颗）×1.8 |
| 平台 cov | 0.855（数据集级）；字段级双档：`mdl238_*` 15 字段 cov **1.0**，`<geo>_<mechanism>_rank` 7 字段 cov 0.71 |
| 类型 | 全 MATRIX（免 vec_） |
| 机制 | SmartHoldings 反推基金经理购买行为：预测机构持仓变化（非滞后持仓——与 INSTITUTIONS 塔判死的「季度低频已定价」机制正交） |
| 更新 | 供应商模型输出（日度重算），无事件断档风险 |

## 二、字段族（22/22 全梳理，四机制族）

### 族 A：预测变化 / 动量（Yan-Zhang 机构需求迁移的预测版）★★★
| 字段 | cov | 说明 |
|---|---:|---|
| `mdl238_global_change_rank` | 1.0 | 全球动量分（近期机构持仓可能性↑，user 10） |
| `mdl238_region_change_rank` | 1.0 | 区域动量分 |
| `global_change_in_preference_rank` | 0.7107 | 百分位档（同义，alias 风险） |
| `regional_change_in_preference_rank` | 0.7104 | 同上 |

### 族 B：拥挤度 / 反转（高机构持仓=拥挤→反转先验）★★★
| 字段 | cov | 说明 |
|---|---:|---|
| `mdl238_global_owner_rank` | 1.0 | 全球拥挤分（100=最拥挤，**反转语义**） |
| `mdl238_region_owner_rank` | 1.0 | 区域拥挤分 |
| `global_peer_investment_concentration_rank` | 0.7109 | 百分位档 |

### 族 C：主分（Smart Holdings score 各级排名）★★
`mdl238_global_rank`(u18) / `mdl238_industry_rank`(u24) / `mdl238_sector_rank`(u15) / `mdl238_country_rank` / `mdl238_region_rank` + 5 个百分位档 alias（cov 0.71）
⚠️ **alias 共线陷阱**：`global_institutional_preference_rank` ≈ `mdl238_global_rank` 同义 —— 每族只测 mdl238 档。

### 族 D：风格契合 / screening（因子风格 fit）★
`mdl238_global_screening_rank` / `mdl238_region_screening_rank` + 2 alias

## 三、机制模板（论文+论坛）

| # | 机制 | 模板 | 来源 |
|---|---|---|---|
| M1 | 机构需求预测动量 | `group_rank(ts_backfill(mdl238_global_change_rank, 66), sector)` | Yan-Zhang 2009 fast traders（Gompers-Metrick 需求迁移）；本战役 BE238 r53 曾混合使用 |
| M2 | 拥挤反转 | `-group_rank(ts_backfill(mdl238_global_owner_rank, 66), sector)` | 拥挤度反转（Vojcík）；与 shortinterest3 机制不同源（预测 vs 实际空头） |
| M3 | 双轴交叉（行业内相对 × 全球绝对） | `group_zscore(group_neutralize(group_zscore(bf(mdl238_global_change_rank, 66), sector), subindustry), sector)`（杠杆A，fnd45 已验证形态） | 本战役杠杆A |
| M4 | 变化 × 拥挤 交互（只有不拥挤的增持才买） | `multiply(group_rank(bf(change,66),sector), subtract(1, divide(bf(owner,66),100)))` | 论坛 conviction 配方同构 |
| M5 | 主分水平 | `group_rank(ts_backfill(mdl238_industry_rank, 66), sector)` | 主分 |
| M6 | 动量 Δ | `group_rank(ts_delta(ts_backfill(mdl238_global_change_rank, 66), 22), sector)` | 加速度 |
| M7 | screening 风格契合 | `group_rank(ts_backfill(mdl238_global_screening_rank, 66), sector)` | 风格轮动 |

## 四、BE231 派发计划（10 臂，mdl238 档优先）

M1-M7 × 轴/窗变体；设置 DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON/maxTrade OFF。
判读：≥1.58 全闸验证 / 1.0-1.58 定向（fnd45 杠杆A+平滑路径复用）/ <0.5 判死。
