# BE96 设计档：pv20×insiders 最佳结构 + 第三腿救援（待料，2026-11-12）

> 依据 PV20_FAMILY_FINAL 判决：族内 S 1.37 / 2Y 1.56，七波 62 臂把所有**结构杠杆**穷尽。
> 判决书指出的唯一剩余路径：「需要一个 ≥1.3 的独立强腿（当前无——所有开放族单腿 ≤1.00）」。
> **关键空白**：该判决写于 cov=0 先验时代，当时 macro27/news52/news7/alpha_factor_lib 全被先验排除，
> 从未作为第三腿试过。BE89/90 已证先验不可信，故这四个未点亮塔数据集是唯一未试的第三腿来源。

## 基准结构（BE84 臂6，S1.37/2Y1.56）

```
group_zscore(add(
  tail(winsorize(group_rank(ts_zscore(adv20_usd_capped_100m,504),sector),std=3),lower=0.22,upper=0.78,newval=0.5),
  tail(winsorize(group_rank(ts_mean(vec_avg(insd1_holdings),110),sector),std=3),lower=0.22,upper=0.78,newval=0.5)
),factor1_group50_top800_513)
```
设置：DEU/TOP500/D1/decay2/SUBINDUSTRY/trunc0.08/nan ON

## 第三腿候选（按 BE93/94/95 实测 |S| 选料，要求 ≥0.5 且方向明确）

| 候选 | 数据集 | 塔 | 机制 | 选料依据 |
|---|---|---|---|---|
| macro27 jobsactive / jobscreated | MACRO | 未点亮 | 招聘扩张 | BE93 臂1-4 |
| news52 chars_in_qa / participants | NEWS | 未点亮 | 电话会议透明度 | BE93 臂8-10 |
| news7 europe_buyback_news_count | NEWS | 未点亮 | 回购事件流 | BE94 臂4 |
| alpha_factor_lib change_free_cash_flow_to_market_cap | FUNDAMENTAL | 未点亮 | 估值动量 | BE95 臂1 |
| news31 negative_sentiment_probability | NEWS | 未点亮 | 负向概率 | BE94 臂6 |

## 波次设计（10 臂，2 槽内单批）

基准双腿 + 第三腿（每候选 2 臂：水平/变化），组合成 10 臂；
若某候选实测 |S|≥0.75 则给 3 臂、其余 1 臂。

## 判读线

- S ≥1.58 且 2Y ≥1.58 ⇒ **突破，PV + INSIDERS 双塔一次点亮**（各 ×1.6），第 12 颗交付候选；
- S 1.45-1.58 ⇒ 定向补（换该腿窗口/矩）；
- S <1.45 ⇒ 第三腿路径关闭，族维持 PROVISIONAL。
