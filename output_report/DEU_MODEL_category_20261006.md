# DEU · MODEL 类别挖掘报告（2026-10-06）

> 设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF
> 探针：W32–W37 共 6 波 ~50 条（累计战役 37 波 ~280 条）｜**全部 UNSUBMITTED**

## 一、结论速览

DEU 的 51 个 MODEL 数据集里，**只有两类信号值得看，且二者互补——但没有一颗能同时满足「强度 + 低 prod」**：

| 类型 | 代表 | S | F | 2Y | sub | **prod** | 卡在哪 |
|---|---|---:|---:|---:|---:|---:|---|
| **强 + 拥挤** | `model25` `value_momentum_*` | 1.62–1.77 | 1.57–1.77 | **1.59–1.69 ✅** | ✅ | **0.94–0.97 ❌** | prod |
| **弱 + 干净** | `model238` Smart Holdings | 1.30 | 1.07 | 1.13 | 0.37 | **0.7274**（单钉） | S/2Y/sub |

⇒ **MODEL 类别未能产出可提交 alpha**；`value_momentum` 是最接近的一颗（除 prod 外全过），其瓶颈是**因子拥挤**，非 S/2Y。

## 二、逐集排查（MODEL 51 集）

### ✅ 可用且有信号
| 集 | 字段/覆盖 | 结果 |
|---|---|---|
| **model25** | 217f / 0.61 | **`value_momentum_{sector,region,global,industry}_{percentile,rank_float}` 强族**（见上）；纯动量百分位族弱（S0.02–0.83）；Earnings-Quality 族弱（S≤1.18） |
| **model238** | 22f / **1.0** | Smart Holdings 机构持股倾向：`mdl238_industry_rank` S1.30/F1.07/2Y1.13；**prod 0.7274** |
| model30 | 14f / 0.66 | StarMine SmartEstimate 意外：`surprise_prediction_fy2` S1.04/F0.77/2Y1.37 |
| model250 | 20f / 0.56 | MALTA ML：`malta_eq_score` S1.13/F1.00 但 **2Y 0.10**；`eq_seasonality` S0.97/2Y0.34 |
| model216 | 45f / 0.71 | ARM 分析师修正：单腿 S1.40/2Y0.50（在历史 add 复合里只是分散化一腿） |

### ❌ 判死（信号弱 / 高换手 / 无信号）
`model36`(SmartRatios 信用质量，S≤0.73) · `model264`(ML 趋势概率 300f，S0.27–0.65) ·
`model28`(Merton 信用，-0.11) · `model53`(Kamakura PD，|S|≤0.18) ·
`model106`(星级评级，**turnover 0.80** 结构性高换手) · `model140`(通胀敏感度，S0.19/-0.05) · `model313`(无形资本，cov 0.20–0.48)

### ⛔ 不可用（平台 cov = 0，DEU 无数据）
`model135`(137f 技术指标) · `chart_cnn_alpha`(122f 图像 CNN) · `multi_source_model`(60f ML 分位预测) ·
`quant_factor_lib`(现金流域) · `analyst_revision_horizons`(1095f 分析师修正) · `model230`(670f)

### ⛔ 平台不存在（本地 catalog 陈旧）
`multi_horizon_alpha` · `model242` · `model193`

## 三、可复用方法论（本轮新增）

1. **可提交性的两难有第二种形态**：不只是「强信号必拥挤」——`model238` 证明**低拥挤信号往往强度不足**（S1.30 vs 1.58）。
2. **prod 直方图 n 值是救活判据**：`model238` prod 0.7274 且 `[0.7,0.8)` **仅 2 个** = 单钉（可救）；`value_momentum` prod 0.96 且 [0.7,0.8) 有 24 个 = 密墙（不可救）。
3. **评级类字段（model106）结构性高换手 0.80** —— 星级/评级日更，先查 turnover 再投入。
4. **本地 catalog 的 `coverage` 列不可全信**：列为 0 的可能是「无数据」（model135），也可能是「未采集」；**平台 `get_datafields` 的 coverage 才是准的**。

## 四、建议

MODEL 类别已系统排查完（17/51 集实测，其余多为无覆盖或不存在）。当前可交付资产仍是前述
`value_momentum_*`（全 RA 通过 / prod 挂）+ `model238`（prod 干净 / 强度挂）两颗半成品。
若要继续，建议转向：**要么接受多腿组合（历史唯一通路，与禁混信号冲突）**，
**要么把这批 280 条探针的结论外溢到别的区**。
