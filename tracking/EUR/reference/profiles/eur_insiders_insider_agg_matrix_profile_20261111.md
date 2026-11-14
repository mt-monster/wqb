# EUR insider_agg_matrix 字段画像（2026-11-11）

> 塔：INSIDERS（2/3 未点亮）；34 字段全 MATRIX（免 vec 包装），cov 0.61，aC 1-31 低拥挤

## 字段族
1. **总量/均值买卖股数**：total_buy/sell_shares（全董事）、total_top_buy/sell（全高管）、total_secondary_*（直接自主交易，绕过信托）——aC 6-31
2. **方向合成指标**：directional_indicator / _2（aC 6/8）
3. **显著交易价值 Top1-4**：significant_value_1-4（aC 8-17 最热）、top_significant_*、directional_significant_*（带方向）、top_directional_*

## 经济机制
- 内部人买入 = 知情者看多（Lakonishok-Lee 型强先验）
- 高管直接交易（secondary）比信托交易信息含量更高
- 大额显著交易 = 高确信度信号

## W1 批（2ZpbFdfn34SNbNxl87zugh，10 条）
净买入比（高管/全董事/直接交易）×3、方向指标 z/动量 ×2、显著交易 z（单笔/Top1-4 聚合）×2、买入集中度、大额门控版、66 日慢 z
算子 2-6 个/条，预检 0 未知字段。
