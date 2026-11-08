# wave297 · analyst10 smartest 族（KOR / TOP600 / D1）2026-11-06

> 前情：wave290–296 把 insiders5 `source_ratio` 族榨到天花板 **S≈1.45 / 2Y≈1.69**（45+ 条交叉实证）⇒ 封盘。
> 本波换数据集，目标 = analyst 塔第 3 颗（当前 2/3，再进 1 颗即点亮）。

## 一、两条结论修正（基于本轮实测，覆盖此前口述）

1. **「约 40 分钟返回」是错的**。实测 wave296 两批同秒派出（`data/wave_dispatch.json` 18:20:01），decay2 批 7 分钟内已 8/8 COMPLETE；本会话 8 条批多在 6–16 分钟、4 条批 2–5 分钟。
2. **`harvest` 返回 `No children found (multisim may still be processing)` 不等于丢批**。
   `references/analyst.md` 已记载：`children=0` 且 progress 非空只是慢（实测卡 0.35 约 25 分钟后自行 COMPLETE）。
   ⇒ decay6 批 `3WQWBt2IW4kJcaaS2FToV4B` 只记为「未收割」，**不作丢批判定**；且 decay 已由 decay2/decay4 双向夹死（1.41–1.45），该批信息价值≈0，不重跑。

## 二、为什么选 analyst10 smartest 族（不是 analyst9 / analyst_factor_signals）

| 候选 | 证据 | 判定 |
|---|---|---|
| `analyst_factor_signals` | 画像 §5 Wave16/17：A1 S **1.31** 天花板；signed_power 提 S 到 1.48 但 2Y 1.69→1.35；双窗/换轴全无效 | 已验证上限，非空白地 |
| `analyst9` | `references/analyst.md` d186–d192 实测：修正广度 S **1.09**、TO 0.048 | 已验证上限 |
| **`analyst10` smartest** | `docs/reference/kor_analyst44_analyst10_carrier_profile_20261106.md`：全 KOR analyst 仅 5 个字段历史到过 1.4+，其中 3 个在本族；本会话 `qMLOooX1` = 本族双字段乘积 **S 1.94 / F 1.74 / 2Y 1.76** | **唯一被证明能破 1.58 的载体** |

关键分野：**裸水平已判死**（`_kor-campaign-log.md`：`anl10_smartest_*_pred_surps_*` 裸用 S −1.03~0.26），
能出货的是 **`ts_av_diff(x,250)` 动量差分几何 + 双字段乘积 + group_neutralize(industry)**。

## 三、字段台账（MCP `get_datafields` 实测，全部 MATRIX ⇒ 不需要 vec_）

| 字段 | cov | aC | 用途 |
|---|---:|---:|---|
| `anl10_smartest_gps_fy1_pred_surps_v0` | 0.9390 | 0 | A1 腿1 |
| `anl10_smartest_gps_fy1_pred_surps_v1` | 0.9390 | 3 | A6 腿1 |
| `anl10_smartest_ebi_fy1_pred_surps_v2` | 0.9523 | 0 | A1 腿2 / B4 |
| `anl10_smartest_bps_fy1_pred_surps_v0` | 0.9201 | 0 | A2 腿1 / B2 |
| `anl10_smartest_net_fy1_pred_surps_v2` | 0.9618 | 1 | A2 腿2 / B1 / B3 / B5 |
| `anl10_smartest_net_fy1_pred_surps_v0` | 0.9618 | 5 | A6 腿2 / B1 |
| `anl10_smartest_nav_fy1_pred_surps_v2` | 0.8765 | 0 | A3 腿1 |
| `anl10_smartest_ebt_fy1_pred_surps_v2` | 0.8820 | 1 | A3 腿2 / A5 腿1 |
| `anl10_smartest_cpx_fy1_pred_surps_v0` | 0.8429 | 0 | A4 腿1 |
| `anl10_smartest_pre_fy2_pred_surps_v2` | 0.8344 | 1 | A4 腿2 |
| `anl10_smartest_net_fy2_pred_surps_v2` | 0.8503 | 0 | A5 腿2 / B3 |
| `anl10_det_full_ebt_past_det_estage` | 0.7450 | 0 | B6（VECTOR，必须 vec_avg）|

## 四、12 个结构互异模板（算子数全部 ≤7，远低于上限 12）

### 批 A：已验证几何（av_diff 250 双乘积 + industry 中性化），换字段对 = 换经济口径

| # | 经济含义 | 腿1 × 腿2 | 算子数 |
|---|---|---|---:|
| A1 | 毛利口径 × EBIT 口径的强惊喜共振 | gps_v0 × ebi_v2 | 7 |
| A2 | 账面价值 × 净利（价值锚 + 盈利锚） | bps_v0 × net_v2 | 7 |
| A3 | 净资产 × 税前利润（资产端 + 税前端） | nav_v2 × ebt_v2 | 7 |
| A4 | 资本开支 × 税前 FY2（投入端 × 远端） | cpx_v0 × pre_fy2_v2 | 7 |
| A5 | 税前 FY1 × 净利 FY2（期限跨期共振） | ebt_v2 × net_fy2_v2 | 7 |
| A6 | 毛利稳定层 × 净利原始层（overlay 层差） | gps_v1 × net_v0 | 7 |

### 批 B：结构互异新几何（每条的「信息加工方式」不同，不是换参数）

| # | 几何 | 经济含义 | 表达式骨架 | 算子数 |
|---|---|---|---|---:|
| B1 | **版本 overlay 增量**（v2 − v0） | 精修层相对原始层的额外惊喜 = 模型精修的边际信息 | `group_rank(ts_mean(sub(v2,v0),22),sector)` | 3 |
| B2 | **二阶差分（加速度）** | 惊喜的变化率再取变化 = 持续性拐点 | `group_rank(ts_delta(ts_mean(bps_v0,66),66),sector)` | 3 |
| B3 | **期限结构**（FY2 − FY1） | 预期的时间斜率：远端改善 vs 近期改善 | `group_rank(sub(net_fy2_v2,net_fy1_v2),sector)` | 2 |
| B4 | **跨口径秩差**（横截面分位相减） | 毛利端 vs EBIT 端的相对好坏 = 成本结构预期 | `subtract(group_rank(gps_v0,sector),group_rank(ebi_v2,sector))` | 3 |
| B5 | **时序不确定度**（二阶矩） | 惊喜自身的波动 = StarMine 预测不稳度（不确定性溢价） | `group_rank(ts_std_dev(net_v2,66),sector)` | 2 |
| B6 | **预测新鲜度**（年龄轴，独立机制类） | 估计在修正链中的年龄 = 信息陈旧度 | `group_rank(ts_mean(vec_avg(estage),22),sector)` | 3 |

## 五、设置与派发

```
KOR / TOP600 / D1 · decay 4 · REVERSION_AND_MOMENTUM · truncation 0.08
nanHandling ON · pasteurization ON · maxTrade OFF · unitHandling VERIFY
```

- `preflight_expressions` 12/12 通过：`unknown_fields: []`、`unknown_soft: []`、`any_changed: false`。
- 批 A `4rudNA45k58D9G5YzU9lDRQ`（6 条）
- 批 B `3FIBsF2TL56za6HGRHXHcrw`（6 条）

## 六、实测结果（2026-11-06，12/12 COMPLETE，全灭）

| # | alpha | S | F | 2Y | TO | fails | 与 `qMLOooX1` 的独立性 |
|---|---|---:|---:|---:|---:|---|---|
| A1 gps_v0×ebi_v2 | `akKeRjVv` | 0.98 | 0.61 | 0.54 | 8.73% |
| A2 bps_v0×net_v2 | `QPvOWZYG` | 1.11 | 0.73 | 0.49 | 9.00% |
| A3 nav_v2×ebt_v2 | `leAEgpMn` | 1.11 | 0.74 | 1.36 | 7.88% |
| A4 cpx_v0×pre_fy2_v2 | `mLodKwo2` | **1.18** | 0.84 | 1.13 | 8.92% |
| A5 ebt_v2×net_fy2_v2 | `E56NmO6R` | 1.09 | 0.73 | 1.23 | 9.31% |
| A6 gps_v1×net_v0 | `gJeXrkel` | 1.13 | 0.75 | 0.39 | 8.35% |
| B1 版本 overlay 增量 | `omERaGNl` | 0.44 | 0.19 | 1.30 | 6.85% |
| B2 二阶差分加速度 | `QPvO0zGW` | 0.83 | 0.51 | 1.18 | 6.35% |
| B3 期限结构 FY2−FY1 | `Jjeo8z7j` | 0.91 | 0.58 | 1.05 | 8.66% |
| B4 跨口径秩差 | `qMLO7GjP` | **0.04** | 0.00 | 0.08 | 10.06% |
| B5 时序不确定度 | `d5WYazjj` | 0.91 | 0.66 | **1.48** | 7.13% |
| B6 预测新鲜度 estage | `88RVNJlX` | 0.54 | 0.26 | 1.18 | 6.11% |

（列顺序：alpha / S / F / 2Y / TO）

## 七、★ 结论：analyst10 的强信号是「一根针」，不是一个机制族

12/12 全灭（max S 1.18），且**换字段对、换几何、换矩全部无效**。对比 `qMLOooX1`（S 1.94 / 2Y 1.76）：

| 变量 | qMLOooX1（成立） | 本波 A 批（全灭） | 判定 |
|---|---|---|---|
| 腿1 | `anl10_smartest_sal_fy2_pred_surps_v1`（aC 11） | gps/bps/nav/cpx 各版 | 换字段即失效 |
| 腿2 | `anl10_smartest_net_fy1_pred_surps_v1`（**v1 核心层**，aC 10） | net_fy1 的 **v0 / v2** 版 | ★ **版本层是决定性的**：v0→1.13、v2→1.11，只有 v1 到 1.94 |
| 几何 | av_diff 250 双乘积 + industry | 同几何 | 几何相同仍全灭 ⇒ 不是几何的问题 |
| 其它几何（B 批 6 种） | — | overlay/加速度/期限/秩差/不确定度/新鲜度 | 全部 ≤0.91 |

**推论**：把 `qMLOooX1` 判为「analyst10 smartest 机制族出货」是错的；它是**特定字段对 + 特定版本层**的单点，
版本（v0 原始 / v1 稳定化核心 / v2 精修）改变的是**同一字段的经济内容**，不是等价改写。
⇒ 在本族继续换腿去找第 2、3 颗，边际成功率极低（本轮 12 条已给出量化证据）。

**执行含义**：KOR ATOM 的现实可提交上限仍是 **2 颗**（`qMLOooX1` + `RRE9NkVj`）。
这两颗是本区全部已探面（insiders5 三族 + analyst 12 数据集 + 5 个塔判死）里仅有的全闸通过件。

**不可重试（本区已判死，勿撞）**：analyst10 `innovation_score` 族（KOR-ANL10-INNOVATION-DEAD）、
analyst44 全字段（KOR-ANL44-ANALYST-DEAD）、analyst16/analyst_consensus/analyst14 主信号、
`add` 跨字段混腿（POISON:equal_weight_leg_add）、signed_power 提 S（毁 2Y）。