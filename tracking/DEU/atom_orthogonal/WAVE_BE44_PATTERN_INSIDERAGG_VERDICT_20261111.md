# BE44 判决：pattern_scores 探针级死亡 + insider_agg_matrix 弱存活（2026-11-11）

## 一、10 臂结果（sim 2lLky1c5M4gqcIe11fUlGsGH，complete=10）

### pattern_scores（PV 塔未点亮，4 臂）

| 臂 | 模板 | S | TO | y2 | sub | 判定 |
|---|---|---:|---:|---:|---:|---|
| pwaw038V | 突破缺口多空价差 | -0.08 | 0.20 | 0.04 | 0.00 | ❌ |
| 2r5rEeJN | (V底+降楔)−升楔 复合 | **-0.71** | 0.11 | 0.37 | -0.47 | ❌ 反号也仅 0.71 |
| mLaLOQZ6 | 升三角上破−下破 | -0.41 | 0.45 | 0.55 | 0.47 | ❌ |
| RReRXPdz | 缺口相似度 Δ22 | -0.02 | 0.22 | 0.18 | -0.20 | ❌ |
| leaex102 | 降楔水平 rank | -0.42 | 0.11 | 0.55 | -0.35 | ❌ |

**pattern_scores 判定：探针级死亡**（5 模板 |S|≤0.71，全部低于 1.2 升级线，sub/y2 亦不达标）。
覆盖虽是 DEU 最高（0.9888），但形态相似度在 TOP500 无横截面信息。
与论坛 continuation_score 帖（ASI 市场）对照 ⇒ 该类数据的价值有市场特异性，DEU 不成立。

### insider_agg_matrix（INSIDERS 塔未点亮，5 臂）

| 臂 | 模板 | S | TO | y2 | sub | 判定 |
|---|---|---:|---:|---:|---:|---|
| P050eK1W | 高管买/(买+卖) 比值 | **0.84** | **0.045** | 1.30 | 0.43 | ⚠ 弱 |
| 9qlqokJ2 | directional_indicator mean22 rank | 0.79 | 0.16 | 0.90 | 0.30 | ⚠ 弱 |
| MP6PwVx9 | directional_indicator_2 裸 rank | 0.74 | 0.62 | 0.04 | 0.23 | ❌ TO 爆 |
| 88N8AXLm | 买−卖 净流量 rank | -0.01 | 0.06 | -0.04 | 0.69 | ❌ |
| npap0rW3 | 直接交易买−卖价差 | 0.25 | 0.05 | -0.03 | 0.93 | ❌ |

**insider_agg_matrix 判定：弱存活但低于升级线**（最佳 0.84 < 1.2）。
方向指标族（directional_indicator）是唯一有信息的字段族，但强度与 insiders1 单塔天花板（1.00）同档；
净流量类（买卖股数差）无效 —— 与 BE29 insiders1 单塔结论一致：INSIDERS 塔在 DEU 信息强度不足。

## 二、塔级影响

- PV 塔：pv29(簇标签)/pv30(0.79 本战役; 1.61 存量已死)/pattern_scores(≤0.71) ⇒ **PV 塔确认无可行路径**
- INSIDERS 塔：insiders1(1.00) + insider_agg(0.84) ⇒ 单塔上限 ~1.0，确认无可行路径
- 两塔的「判死前探针穷尽度」：pattern_scores 5 模板跨 3 机制面（价差/复合/动量/水平）——
  对一个全灭探针，升级满波（≥10 模板）的预期收益为负，按探针纪律收口。

## 三、台账更新

master 总表两行已从「探针在飞」改为终审判定。
