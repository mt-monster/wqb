# news20 波1 模板池台账（DEU / TOP500 / D1 / NEWS 单塔）

## 一、矿位定性（get_datafields 2026-11-03）
46 VECTOR，双簇：裸 `nws20_*` cov 0.639 / `nws20_multiple_comp_*` cov 0.919。拥挤度 ac 0-2 极低。与 news17 同构字段族（分类器情绪 acb/bee/ber/bam/qep/qmb/ssc/nip + 新颖度 event_similarity_days + 相关度 event_relevance + 故事密度 rp_story_event_count/index）。

## 二、机制重开依据（跨集封杀=误杀律）
news17 波2 全灭（max|S| 0.84，T9 硬数据对照 0.02）判死的是 **news17×该模板池** 一维；机制×数据集二维律要求在 news20 重开。论坛/论文取证沿用 news17/news104 台账（relevance+novelty 过滤、情绪概率差、密度效应），金帖开放问题映射：novelty gate（M4）、跨簇净额（M9）、密度×新颖度交互（M7）≥3 个差异化臂；照抄臂仅 M1（news17 T3 机制直推）= 1 个。

## 三、模板池（12 结构互异 ✓，全部单数据集 news20，NEWS 单塔，无 PV 内建字段）
| # | 机制 | 表达式 | 几何 |
|---|---|---|---|
| M1 | 财报情绪延续（照抄臂，news17 T3 重开） | `group_rank(ts_mean(vec_avg(nws20_multiple_comp_acb), 22), subindustry)` | 水平延续 |
| M2 | 情绪动量 | `group_rank(ts_delta(ts_mean(vec_avg(nws20_multiple_comp_ssc), 5), 22), subindustry)` | 一阶差分 |
| M3 | 分类器分歧净额（acb−bee，同量纲） | `group_rank(ts_mean(subtract(vec_avg(nws20_multiple_comp_acb), vec_avg(nws20_multiple_comp_bee)), 22), subindustry)` | 跨分类器净额 |
| M4 | 新颖度门控（开放问题臂1） | `trade_when(greater(vec_avg(nws20_multiple_comp_event_similarity_days), ts_mean(vec_avg(nws20_multiple_comp_event_similarity_days), 22)), group_rank(ts_mean(vec_avg(nws20_multiple_comp_ssc), 22), subindustry), 0)` | 事件门控 |
| M5 | relevance 加权情绪 | `group_rank(ts_mean(multiply(vec_avg(nws20_multiple_comp_event_relevance), vec_avg(nws20_multiple_comp_event_sentiment_score)), 22), subindustry)` | 加权积 |
| M6 | 故事密度反转 | `subtract(0, group_rank(ts_mean(vec_avg(nws20_multiple_comp_rp_story_event_count), 22), subindustry))` | 密度水平反转 |
| M7 | 密度×新颖度交互（开放问题臂2） | `group_rank(ts_corr(vec_avg(nws20_multiple_comp_rp_story_event_count), vec_avg(nws20_multiple_comp_event_similarity_days), 22), subindustry)` | 相关交互 |
| M8 | 影响力信噪比 | `group_rank(ts_ir(vec_avg(nws20_multiple_comp_nip), 22), subindustry)` | 信噪比 |
| M9 | 跨簇净额（multiple_comp − 裸簇，开放问题臂3） | `group_rank(ts_mean(subtract(vec_avg(nws20_multiple_comp_ssc), vec_avg(nws20_ssc)), 22), subindustry)` | 同源分歧净额 |
| M10 | 词面情绪不稳定 | `subtract(0, group_rank(ts_std_dev(vec_avg(nws20_multiple_comp_qep), 66), subindustry))` | 二阶矩 |
| M11 | 软故事反转 | `subtract(0, group_rank(ts_mean(vec_avg(nws20_multiple_comp_qep), 5), subindustry))` | 短窗反转 |
| M12 | 情绪峰值年龄 | `group_rank(ts_arg_max(vec_avg(nws20_multiple_comp_ssc), 66), subindustry)` | 事件年龄 |

量纲安全：M3/M9 同量纲净额；M4 门控比较两端同字段（不与裸常数比）；subtract(0,·) 只作用 group_rank 输出。窗口 5/22/66 白名单。算子全部在 103 名单。

## 四、双预检（2026-11-03 06:4x）
- preflight_expressions：12/12 valid，10 字段全存在，any_changed=false。
- verify_expr：12/12 valid。
- **待派发**：并发纪律 ≤2（sentiment7_wave1s + other250_wave1 在飞），槽位一空即派（task-id `news20_wave1`）。

## 五、派发记录（2026-11-03 06:5x）
- snt7 波 runner 退出释放槽位后即派：task-id `news20_wave1`，pid 17224，batch-size 2 / concurrency 1，12 臂 6 批。
- 并发现状：other250_wave1（pid 18004）+ news20_wave1（pid 17224）双波在飞顶格；重试池两份（snt7 8 臂 / oth250 2 臂）等干净批信号后补发。

## 六、全波收口（2026-11-03 07:1x，12/12 全落地零 ERROR）
| # | 机制 | S | TO | 判定 |
|---|---|---|---|---|
| T1 | acb 情绪净分 22d 水平 | **+0.51** | 0.14 | 全波最强 |
| T2 | ssc 5→22 差分 | +0.23 | 0.42 | 弱 |
| T3 | acb−bee 分歧净额 | +0.30 | 0.13 | 弱 |
| T4 | trade_when 门控（novelty days） | +0.08 | 0.08 | 弱 |
| T5 | relevance×情绪交互 | +0.20 | 0.13 | 弱 |
| T6 | 故事密度取反（rp_story count） | +0.47 | 0.11 | 次优 |
| T7 | 密度×returns 相关 | −0.12 | 0.19 | 弱 |
| T8 | nip 信噪比 | −0.06 | 0.11 | 弱 |
| T9 | ssc−nip 跨簇净额 | 0.00 | 0.00 | **空仓臂**（S/TO 三零特征，两字段时点错开 nan 淹没） |
| T10 | qep 波动取反 | −0.20 | 0.05 | 弱 |
| T11 | qep 5d 水平取反 | +0.30 | 0.33 | 弱 |
| T12 | ssc 峰值年龄 | −0.03 | 0.10 | 弱 |

- **全波判定**：max 0.51 / 次优 0.47，8 正 4 负方向偏正但幅度全弱，距闸 1.58 差 2/3 ⇒ **multiple_comp 簇（46 字段：情绪净分/分歧/密度/新颖度）在 DEU/TOP500 判弱收口**。按机制×数据集二维律只封「DEU/TOP500 × news20 multiple_comp 模板池」，不外推。
- T6（故事密度取反）+0.47 且 TO 0.11 干净，与 snt7 重试 T8/T10 同记为「弱信号面最强臂」供跨集迁移参考。T9 空仓臂教训并入 analyst9 同类特征集（跨簇净额先核字段更新时点）。
- **附：重试管线全通终证**：oth250_w1_retry 2/2 零 ERROR——T1（=探针 O0Axgqxv 同式）重试读数 **−0.25 与原探针一字不差**，同式同读数 = 平台瞬时故障无罪链完整闭环。全 DEU 重试管线累计 10/10 复活（snt7 8/8 + oth250 2/2），06:38-06:5x 故障窗口定案。
