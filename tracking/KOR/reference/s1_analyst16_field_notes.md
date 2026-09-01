# S1 字段笔记：analyst16（KOR / TOP600 / delay1）

**Dataset**: analyst16
**Region**: KOR
**Delay**: 1


- 数据集类型：VECTOR 109 字段（全部 VECTOR）
- S1 白名单：45 字段（ledger `s1_analyst16_d1`，source=s2_nested）
- 定位：analyst 族 KOR 实证金矿（win 88lr21xo/A1lb2KpR 在评级修正×SH 族，已饱和）；本集避开评级分布，主攻**意外值 + 一致预期修正动量**

## 字段分类

| 族 | 代表字段 | 语义 | 风险 |
|---|---|---|---|
| 意外值 | anl16_actsurprise / anl16_actsuescore | 实际-预期差与 SUE 情绪分 | actsurprise users=16 需实测 prod_corr |
| 一致预期修正 | anl16_aftercons_difference/percentage/mean/stddev | 事件前后一致预期变化 | 绝对差需按 beforecons_mean 归一 |
| 盈利预测修正 | anl16_afterest_difference/percentage/value | 单分析师预测修正 | users≤6 低拥挤优先 |
| 预期水平 | anl16_meanest_normal / medianest_normal / highest_normal / lowest_normal | 归一后一致预期 | 慢变，需修正差分激活 |
| 分散度 | anl16_eststddev_normal / beforecons_stddev | 预测分歧 | 分散度压缩=不确定性消除 |
| 覆盖广度 | anl16_numests / numincests / aftercons_numitems | 贡献分析师数 | 稀疏，防 CW |
| 评级分布（对照） | anl16_meanrec/medianrec/highrec/lowrec/Nscermun | 推荐评级汇总 | 与死路族 KOR-MLPROJ-RATING-SH-SATURATED 同族，不入主批 |
| 元数据（排除） | *_twn / *_map / *_currency_adjustment / *_unit_scale / *_splitadj / *_fiscal_year* / *_period* | 映射与调整因子 | 全排除 |

## 特征工程建议（初始信号）

1. 意外值动量：rank(vec_avg(anl16_actsurprise))——事件后漂移暴露（expected_exposure: post-earnings drift）。
2. SUE 情绪：rank(vec_avg(anl16_actsuescore))——标准化意外幅度（expected_exposure: earnings surprise momentum）。
3. 一致预期修正动量：rank(vec_avg(anl16_aftercons_difference))（expected_exposure: estimate revision momentum）。
4. 归一修正幅度：rank(divide(vec_avg(anl16_aftercons_difference), add(abs(vec_avg(anl16_beforecons_mean)), 0.001)))——防大盘股主导（expected_exposure: revision magnitude）。
5. 盈利预测修正：rank(vec_avg(anl16_afterest_percentage))（expected_exposure: analyst revision breadth）。

## 进阶信号

6. 分散度压缩：rank(subtract(vec_avg(anl16_beforecons_stddev), vec_avg(anl16_eststddev_normal)))——分歧收窄=不确定性消除（expected_exposure: low-vol/uncertainty resolution）。
7. group 骨架：group_rank(vec_avg(anl16_actsurprise), industry)、group_zscore(aftercons_difference, sector)（expected_exposure: intra-industry relative surprise）。
8. 预期宽度收窄：divide(subtract(vec_avg(anl16_aftercons_high), vec_avg(anl16_aftercons_low)), add(abs(vec_avg(anl16_aftercons_mean)), 0.001)) 取负——高低差收窄=共识凝聚（expected_exposure: consensus convergence）。

## 预处理决策

- VECTOR 字段一律 vec_avg 聚合为 MATRIX 后再横截面运算（平台硬要求）。
- 修正类差分信号外层必套 rank；绝对差信号除以 |基数| 归一。
- 稀疏事件字段（surprise/afterest）若 CW 超标改 trade_when 门控。
- 死路规避：评级修正×SH 族不复刻；评级分布族（meanrec 等）仅对照观察。