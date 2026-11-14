# Wave AU dispatch — news20 probe（news 塔未点亮，未测集）2026-11-10

sim_id: eiqxlOh4BtavI1gWog1KLd（try 1 无 429）
背景：sentiment 全族终判死（见 WAVE_AR_AS_SENTIMENT_20261110.md）；按 MNO/THIRD_SEAT 台账「news 塔仍 0 颗」，news20（46 字段 cov 0.92，ac41）是未测集里覆盖最高的。
探针 6 条（level×4 分类器 + delta×1 + ghc_lna×1），全部 vec_avg 包裹（全 VECTOR）：
1. nws20_event_sentiment_score level sub（uc6/ac8 主字段）
2. nws20_event_sentiment_score delta66 ind
3. nws20_bee level sub（财报专项分类器 uc4）
4. nws20_acb level ind（财报 BER 分类器 uc3）
5. nws20_ber level sub（分析师推荐变动 uc2）
6. nws20_ghc_lna level ind（语调变化 uc1）
设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON，preflight valid=true unknown=[]

---

## Wave AU 判决（news20 探针，sim eiqxlOh4BtavI1gWog1KLd，6/6 COMPLETE）
| # | 模板 | alpha | S | F | 2Y | TO | lc | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| AU1 | event_sentiment_score level | 78LelZWb | 0.22 | 0.07 | -0.87 | 0.052 | 110 | 0.16 |
| AU2 | event_sentiment_score delta66 | RREGPVMa | 0.23 | 0.05 | -0.62 | 0.193 | 114 | 0.22 |
| AU3 | bee level | VkxAe6VG | 0.20 | 0.05 | -0.58 | 0.071 | 109 | -0.18 |
| AU4 | acb level | e75XE9mN | 0.35 | 0.13 | -0.27 | 0.086 | 115 | 0.40 |
| AU5 | ber level | wpQ0WYqd | 0.27 | 0.09 | -0.64 | 0.073 | 111 | 0.08 |
| AU6 | ghc_lna level | omExZ6p2 | -0.06 | -0.01 | -1.94 | 0.055 | 119 | -0.05 |

**news20 判死**：全字段 S≤0.35 且 2Y 全负（2Y -0.27~-1.94），level 与 delta 双弱。与 news104/18/50/38 同判——**RavenPack/BER 分类器事件情绪在 DEU 无定价力**（第 5 次证实，news 塔事件情绪通道终判死）。

