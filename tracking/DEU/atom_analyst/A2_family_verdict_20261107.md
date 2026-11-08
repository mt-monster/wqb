# DEU Analyst 扩展战役 · A2 家族终审（2026-11-07 06:04）

> AW1-A → AW8 共 8 批 66 条回测，全部 analyst7 单数据集 ATOM（decay1-4 / SUBINDUSTRY / trunc0.08）。

## 一、终审结论

**analyst7 修正广度占比家族（raised/(raised+lowered+k)）S 平台硬顶 1.57，距 REGULAR 闸 1.58 仅 0.01**——30+ 变体（k∈[0,1] 全程、decay∈[1,4]、industry/sector/subindustry 三轴、rank/zscore 双几何、winsorize 前后置）全部落在 1.15-1.62 带内，平台形状对参数完全不敏感。

## 二、最强读数（近闸候选，四闸过三）

| id | 构造 | ops | S | F | 2Y | sub | sub/S | TO | 覆盖 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **omEGe0Vn** | group_rank(raised/(raised+lowered+0.375), sector) @decay1 | 4 | **1.57** | 1.27✅ | 1.66✅ | 1.16✅ | 0.74 | 15.0% | 10/10✅ |
| QPvzdpEK | 同核 k=0.25 | 4 | 1.57 | 1.27 | 1.59 | 1.14 | 0.73 | 15.0% | 10/10 |
| wpQGVAM1 | k=0.4 @decay2 | 4 | 1.56 | 1.36 | 1.61 | 1.18 | 0.76 | 12.9% | 10/10 |
| 1YNKvbaM | k=0.30 @decay1 | 4 | 1.57 | 1.28 | 1.62 | 1.15 | 0.73 | 15.0% | 10/10 |

互相关：家族内 0.85-0.96（同族互斥，篮子仅 1 席）。逐年覆盖 PASS（2014-2023 无空窗，lc 65-100），逐年 S 均衡（0.57-2.94 无时代偏态）。

## 三、家族内已证死/证伪面
- 阻尼 k frontier：k=0 → S 1.61-1.62 但 2Y 0.63（不可行点）；k≥0.25 → 2Y≥1.54 且 S≤1.57。可行点不存在。
- decay 轴：4→2→1 单调 +0.01/档，1.46→1.57 封顶。
- 中性化：SLOW 0.72-1.37 全弱于 SUBINDUSTRY；FAST/STATISTICAL 按 fnd45 曲线外推不投。
- 侧指标：cps 0.63 / dps 0.86 / sal 0.55 / 1mth 1.09 / 1wk 1.19 全弱于 ebi num_4wks。
- 机制面：delta22、rec、PEAD、coverage-gate、dispersion、ts_rank252、2腿合成、平滑分子、industry 轴全灭或更弱。
- winsorize 前/后置均无效（单调变换被 rank 吸收，实证 reaffirm）。

## 四、与全战役的合流
见 `tracking/DEU/atom_fundamental/campaign_verdict_20261107.md`（Fundamental 终审）。全战役近闸储备三级篮见主报告。
## 五、prod/self 实测（2026-11-07 06:08 补测，MCP 工具）
- **prod 0.7552 ✗**（0.7-0.8 桶 n=3 浅钉，0.6-0.7 桶 n=15；平台实测非缓存）——一级篮候选为「S 0.01 + prod 浅钉」双重缺口，特殊裁决需同时破墙（窗口谷法，难度中高）。
- **self 0.3466 ✅**（对已提交 OS 池最大 0.347，top: blRnKEk6 0.347 / 58gkLAkk 0.341 / vRk6og8b 0.309，池 14 颗）——self 侧极干净。
