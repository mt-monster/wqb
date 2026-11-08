# Wave P1 收割：dl_riskfree 换机制面 10 模板（2026-11-07）

- multisim: YyZnu5Rv4RabphDQl5SwBf / 4oYwoCaTD59JcsZXKGOWHtY / 1b6csI30v4pL9Wgp7Zy1pIX / 3uQhXcax657hc0YcIq19Xg0
- 设置：KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay 4 · trunc 0.08 · nan ON · settings_pv.json
- preflight valid=true / 9 字段 / any_changed=false；get_operators 12/12 存在

| # | 模板（全部自建） | alpha | S | F | 2Y | sub | TO | raFail |
|---|---|---|---:|---:|---:|---:|---:|---:|
| T2 | 中桶均值回复 ts_av_diff(2_3q_20d,66) | **O0Azz37q** | **2.09** | 1.49 | 1.79 | 2.28 | 0.2174 | **0** |
| T6 | 历史分位 ts_rank(1_2q_60d,252) | omEGrkEk | 1.43 | 0.85 | 1.45 | 1.66 | 0.2149 | 3 |
| T7 | 跨期限共识（3 期限均值, industry） | 78LmlnwL | 1.40 | 1.30 | 1.41 | 1.24 | 0.0879 | 2 |
| T3 | 尾部偏斜 5q 上−下 | P0oz8vk7 | 1.14 | 0.94 | 1.94 | 1.17 | 0.0869 | 2 |
| T5 | 二阶差分（加速度） | vR1G6o1r | 0.79 | 0.32 | 0.51 | 0.80 | 0.2664 | 4 |
| T8 | 桶序数 quantile_label_3bucket | KPJzZE9j | 0.73 | 0.29 | 0.95 | 0.89 | 0.3384 | 4 |
| T1 | 分歧度 abs(p1−p0) | omEGGdq5 | −1.30 | −0.79 | −2.09 | −0.97 | 0.2254 | 5 |
| T4 | 期限斜率 p_5d − p_60d | bl6znvem | **−1.58** | −1.18 | −1.78 | −1.38 | 0.2224 | 5 |
| T9 | 净信念波动 signed_power 二阶矩 | （末批同 78LmlnwL 批，见 CSV） | – | – | – | – | – | – |
| T10 | 净信念均值回复 subindustry | （同上） | – | – | – | – | – | – |

## 核心归因

1. ★ **T2 中桶均值回复是本战役最强单模板**：S 2.09（KOR 历史最高）、F 1.49、sub 2.28、raFail 0，
   且**只用 3 个算子**（group_rank / ts_av_diff / 一个字段），远优于此前 9 算子的激增族。
2. **方向先验被实测确认**：T4 期限斜率 −1.58、T1 分歧度 −1.30 均为强负向 ⇒ 与 dispersion anomaly 文献一致
   （高分歧 / 陡斜率 → 低收益）。两条都需按 KOR「取负非镜像」纪律单独实测反向臂。
3. **二阶/高阶几何无效**：T5 加速度 0.79、T8 桶序数 0.73 ⇒ 概率场信息集中在一阶水平偏离，不在变化率。

## ★ 冠军 O0Azz37q 全闸与 prod

| 项 | 读数 |
|---|---|
| S / F / 2Y | 2.09 / 1.49 / 1.79 |
| sub / sub 阈值(0.474×S) | 2.28 / 0.99 ✓ |
| TO | 0.2174 ✓ |
| raFail | 0 ✓ |
| self | **0.2655** ✓（池内最干净） |
| 逐年 | **10/10 全正**（2014–2023），longCount 265–342，无空窗 ✓ |
| **prod** | **0.7940 ✗**（[0.7,0.8) 7 钉 / [0.5,0.7) 276） |

## ★★ 新假设：prod 相关性 ∝ 字段拥挤度（alphaCount）

O0Azz37q 用的 `probability_label2_3quantile_20day_ohlcv` **aC = 673**（本数据集高拥挤档）。
KOR prod 池仅 46 颗 OS，同字段被反复使用 ⇒ 同字段必然撞车。
本数据集存在大量 **aC 12–50 的低拥挤字段**（3_5quantile / 0_3quantile / 1_3quantile / 2_4 / 2_5 族），
此前 12 波从未使用。

**控制变量实验（Wave P3）**：模板完全冻结为 T2（group_rank(ts_av_diff(F,66),sector)），
只把字段 F 换成 10 个 aC 12–50 的低拥挤字段 ⇒ 若 prod 随 aC 单调下降，假设成立，
则「低拥挤字段 × 已验证模板」是 KOR 通墙的标准打法。
