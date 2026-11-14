# BE56 待发：pv30 积压消费（PCA 分量族，33 条从未回测）

> 波次 s2_pv30_d1：165 条表达式中 31 条 status=gem + 2 条 gated = **33 条从未回测**（132 条已 fail）。
> **PV 塔未点亮 ⇒ 单数据集 ATOM，无禁混风险**；且 pv30 真实天花板从未被测（面板 1.61 系误标，见 CORRECTION 档案）。

## 一、表达式族

1. `days_from_last_change(sign(<PC 分量>))` × 8 —— 因子载荷符号持续性（regime persistence）；
2. `divide(ts_delta(PC_i,5)-ts_delta(PC_j,5), |PC_i|+|PC_j|)` × 25 —— 相对因子动量（归一化的因子间相对变化）。

字段形如 `eighth_pca_component_top1200_group513`（PCA 分量，top1200 universe 的第 k 个主成分载荷）。

## 二、本波 10 臂（预检通过 valid=true, unknown_fields=[]）

```
days_from_last_change(sign(eighth_pca_component_top1200_group513))
days_from_last_change(sign(fifteenth_pca_component_top1200_group513))
days_from_last_change(sign(fifth_pca_component_top1200_group513))
days_from_last_change(sign(ninth_pca_component_top1200_group513))
divide(subtract(ts_delta(eleventh_pca_component_top1200_group513,5),ts_delta(eighth_pca_component_top1200_group513,5)),add(abs(eleventh_pca_component_top1200_group513),abs(eighth_pca_component_top1200_group513)))
divide(subtract(ts_delta(fifteenth_pca_component_top1200_group513,5),ts_delta(eighth_pca_component_top1200_group513,5)),add(abs(fifteenth_pca_component_top1200_group513),abs(eighth_pca_component_top1200_group513)))
divide(subtract(ts_delta(eighth_pca_component_top1200_group513,5),ts_delta(eleventh_pca_component_top1200_group513,5)),add(abs(eighth_pca_component_top1200_group513),abs(eleventh_pca_component_top1200_group513)))
divide(subtract(ts_delta(fifth_pca_component_top1200_group513,5),ts_delta(fifteenth_pca_component_top1200_group513,5)),add(abs(fifth_pca_component_top1200_group513),abs(fifteenth_pca_component_top1200_group513)))
divide(subtract(ts_delta(fourteenth_pca_component_top1200_group513,5),ts_delta(fifteenth_pca_component_top1200_group513,5)),add(abs(fourteenth_pca_component_top1200_group513),abs(fifteenth_pca_component_top1200_group513)))
divide(subtract(ts_delta(fifteenth_pca_component_top1200_group513,5),ts_delta(fifth_pca_component_top1200_group513,5)),add(abs(fifteenth_pca_component_top1200_group513),abs(fifth_pca_component_top1200_group513)))
```

剩余 23 条（下一波）。设置沿用 DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON。