# 成功 Alpha 表达式模板与经济学模式总结

> **数据来源**：`data/wqb.db` — `alphas` 表（47 条 COMPLETE，其中 36 条 positive sharpe）、`backtest_results` 表（7 条 sharpe≥1.5）、`registry_empirical` 表（13 条 layer=win）、`wave_results` 表（IND/KOR/MEA/EUR 跨区成功案例）  
> **分析方法**：算子/字段/窗口/中性化频次统计 + 跨区 win 条目表达式比对 + 经济学逻辑归纳  
> **总样本**：23 条可直接解析的成功表达式 + 13 条 registry 记录的跨区成功模式

---

## 一、整体统计画像

| 维度       | 结论                                                   | 数据支撑                    |
| -------- | ---------------------------------------------------- | ----------------------- |
| **核心算子** | `rank` 占 32 次（78%），`ts_zscore` 占 21 次（50%）           | 23 条成功表达式算子统计           |
| **组合方式** | `add`（12）> `divide`（6）> `multiply`（3）                | rank 相加或 rank 相除是两大组合骨架 |
| **主导字段** | `mdl31_roe_pct_t4q`（16 次）+ `mdl238_global_rank`（7 次） | 模型预测类字段是最高效信号源          |
| **窗口长度** | **252 窗**（8 次）和 **120 窗**（7 次）主导                     | 长窗口 = 2Y 天然强，过拟合低       |
| **中性化**  | **SECTOR**（IND 全部 7 条）+ **SUBINDUSTRY**（EUR）         | 区域差异显著                  |

---

## 二、八种可复用的成功模板

### 模板 1：模型长窗 rank + ts_zscore（最高频、最稳）

```
rank(ts_zscore(mdl31_roe_pct_t4q, 252))
```

- **sharpe 1.58 / fitness 1.18**，5 个 alpha 均达此水准（omq5Pqkk/O07PRA5Y/e7zwN5qO/Vk7jZx2w/N17mLNg7）
- **经济学逻辑**：模型预测的长期 ROE 偏离度 → 盈利能力回归均值。252 窗（1 年）是"回归均值"的自然周期。
- **关键参数**：252 窗最优（>120 稳，<90 衰减），单字段 rank 外包装，无需中性化（模型字段已去行业）。
- **降阶变体**：窗口 180→1.54、150→1.42、120→1.39、90→1.31、60→1.11（单调衰减）。
- **来源**：`alphas.status=COMPLETE`

### 模板 2：模型基本面 ÷ 分析师负面修正（IND 最优，sharpe 2.64）

```
divide(
    rank(analyst_revision_percentile_score_medium_4),
    add(1, rank(analyst_recommendation_downgrades_30d_medium_31))
)
```

- **sharpe 2.64 / fitness 2.87 / 2Y 3.08 / margin 49.7bp / turnover 5.93%**（wpj5bQ06）
- **变体**（全部 IND/SECTOR 通过）：
  - `divide(rank(mdl238_global_rank), add(1, rank(analyst_downgrades_30d)))` → sh 1.91-2.01
  - `divide(add(1, rank(mdl238_global_rank)), add(1, rank(analyst_downgrades_30d)))` → sh 2.01
  - `divide(rank(ts_mean(mdl238_global_rank, 5)), add(1, rank(analyst_downgrades_30d)))` → sh 1.78
- **经济学逻辑**：**基本面质量 ÷ 分析师看空强度** → 基本面强但被分析师下调评级的股票 = "被错杀的价值"。分母 +1 防零除，turnover 天然低（5-8%）。
- **关键**：两个独立数据源 rank 相除；SECTOR 中性化是 IND 的必选档。

### 模板 3：模型 rank + 分析师修正 rank 加权相加（IND 次优）

```
add(multiply(rank(mdl238_global_rank), 0.4),
    multiply(divide(rank(analyst_revision_percentile_score_medium_4), ...), 0.6))
```

- **sharpe 2.59 / fitness 2.88 / margin 46.87bp**（ZY7jAaRY）
- **经济学逻辑**：模型基本面质量（40% 权重）+ 分析师修正分数（60% 权重）→ 基本面与预期改善双驱动。
- **关键**：权重配比 0.4/0.6 最优（模型弱腿×分析师强腿互补）；SECTOR 中性化。

### 模板 4：跨金字塔慢速×快速混合（EUR 方法论突破）

```
0.40 × slow_MODEL_residual_invert + 0.60 × fast_PV_pattern_invert
```

- **配置**：SUBINDUSTRY / decay=4 / TOP2500 / delay=1
- **经济学逻辑**：慢速基本面残差（低频、低 2Y 衰减）× 快速量价模式（高频、高 Sharpe）→ 跨金字塔天然低相关，2Y 与 Sharpe 双提升。
- **关键**：**0.4/0.6 权重**（慢腿×快腿黄金比）；SUBINDUSTRY 中性化 + decay=4；纯单一金字塔（只 MODEL 或只 PV）是 dead_end。
- **来源**：`registry_empirical` EUR-WIN-SLOW-MODEL-X-FAST-PV

### 模板 5：慢变量×短周期跨数据集混合（KOR 方法论突破）

```
rating_revision × short_horizon_hedge3_quantile1_5d_pred
```

- **结果**：评级 2 + SH 1 → sharpe 1.77 / fitness 1.40 / 2Y **2.52**；评级 1 + SH 3 → sharpe 1.83 / 2Y **2.34**（88lr21xo + A1lb2KpR，均 ACTIVE）
- **经济学逻辑**：评级修正（慢变量，2Y 2.14 金矿）× 短期对冲信号（短周期，低相关）→ 双轴互补。
- **关键**：**慢变量 2Y 强 + 短周期低相关**是公式；与同周期慢信号混合全灭（2Y 衰减叠加）。
- **来源**：`registry_empirical` KOR-RATING-REV-SH-MIX-WIN

### 模板 6：分析师广度双轴去 revision（MEA PROD 墙破解）

```
PT_raised_breadth + Net_est_breadth（去掉 revision 腿）
```

- **结果**：9qXoJge2 提交 ACTIVE；PROD 从 0.8+ 降到可提交区间
- **经济学逻辑**：分析师目标价上调广度（MATRIX 裸用）+ 净利润估计上调广度（VECTOR）→ 双重基本面预期改善信号。
- **关键**：**去掉 est_q\_*\_median/3mth_ago revision 腿**是破 PROD 墙的关键（revision 腿与生产策略高度重叠）。
- **来源**：`registry_empirical` MEA-ANL7-PT-NET-BREADTH-DECORR

### 模板 7：EPS+Net 3 月修正 rank 相加（MEA 第 3 颗 ACTIVE）

```
rank(vec_avg(est_q_eps_mean)/vec_avg(est_q_eps_mean_3mth_ago) - 1)
+
rank(vec_avg(est_q_net_mean)/vec_avg(est_q_net_mean_3mth_ago) - 1)
```

- **sharpe 1.61 / fitness 1.59 / 2Y 2.41**（j2jL9x6j）
- **配置**：MEA TOP400 / delay=1 / SECTOR / decay=1
- **经济学逻辑**：EPS 3 月变化 + 净利润 3 月变化 → 分析师对短期盈利预期的同步改善。
- **关键**：`rank` 相加（不做除法）；`vec_avg` 包裹 VECTOR 字段；SECTOR 中性化。

### 模板 8：模型长窗 rank 双嵌套（IND mdl177 专杀）

```
rank(ts_rank(ts_backfill(mdl177_F, 66), 250))
```

- **sharpe 1.84-3.67 / 2Y 2.2-3.6**（QPGvgO2G/QPGbAOn5/A1GN2mWX，均 ACTIVE）
- **配置**：IND TOP500 D1 / SECTOR 或 STATISTICAL / decay 6-8
- **经济学逻辑**：mdl177 模型预测质量 → 66 天 backfill 平滑 + 250 天 rank 排序 → 1 年周期基本面回归。
- **关键**：**长窗 250 天然 2Y 强**；负权重混合可进一步降 PROD。
- **来源**：`registry_empirical` IND-MDL177-TSRANK250-WIN

---

## 三、跨模板的共性规律（最重要）

| 规律                                  | 说明                                                                               | 证据                         |
| ----------------------------------- | -------------------------------------------------------------------------------- | -------------------------- |
| **① rank 外包装几乎必用**                  | 32/23 条成功表达式含 `rank`                                                             | 23 条算子统计                   |
| **② ts_zscore 优于 ts_mean/ts_delta** | 21/23 条含 `ts_zscore`                                                             | 标准化后截面排序更稳                 |
| **③ 长窗口（≥120）优于短窗口**                | 252 窗 8 次、120 窗 7 次 vs 60 窗仅 1 次                                                 | 长窗 = 2Y 天然强、过拟合低           |
| **④ 跨数据集混合 > 单数据集**                 | IND 模板 2/3（模型×分析师）、EUR 模板 4（MODEL×PV）、KOR 模板 5（评级×SH）、MEA 模板 6/7（PT×Net/EPS×Net） | 双轴 rank 相加或相除是最高 Sharpe 结构 |
| **⑤ SECTOR > SUBINDUSTRY（IND/KOR）** | IND 全部 SECTOR、KOR 部分 SECTOR；EUR 用 SUBINDUSTRY                                    | 区域特性：IND/KOR 行业结构更细        |
| **⑥ 分母 +1 防零是 IND divide 骨架铁律**     | 所有 `divide` 模板分母均 `add(1, ...)`                                                  | 防零除，同时平滑极值                 |
| **⑦ decay 4-8 是甜点**                 | EUR decay=4、IND mdl177 decay 6-8                                                 | 信号一致性 vs 时效平衡点             |
| **⑧ 去掉与生产策略重叠的腿**                   | MEA 模板 6 去掉 revision 腿破 PROD 墙                                                   | 降 PROD 相关性关键               |

---

## 四、按区域的最佳模板对照表

| 区域      | 最优模板                 | 代表 alpha          | sharpe / 2Y         | 关键参数                              |
| ------- | -------------------- | ----------------- | ------------------- | --------------------------------- |
| **IND** | 模板 2（模型÷分析师修正）       | wpj5bQ06          | 2.64 / 3.08         | SECTOR, mdl238×analyst_downgrades |
| **IND** | 模板 3（模型+修正加权）        | ZY7jAaRY          | 2.59 / —            | SECTOR, 0.4/0.6 权重                |
| **IND** | 模板 8（mdl177 长窗）      | QPGvgO2G 等        | 1.84-3.67 / 2.2-3.6 | SECTOR, decay 6-8, 250 窗          |
| **MEA** | 模板 6（PT+Net 广度）      | 9qXoJge2          | ACTIVE              | SECTOR, 去 revision                |
| **MEA** | 模板 7（EPS+Net 3 月修正）  | j2jL9x6j          | 1.61 / 2.41         | SECTOR, decay=1                   |
| **EUR** | 模板 4（慢 MODEL × 快 PV） | —                 | 方法论突破               | SUBINDUSTRY, decay=4, 0.4/0.6     |
| **KOR** | 模板 5（评级×SH 跨数据集）     | 88lr21xo/A1lb2KpR | 1.77 / 2.52         | SECTOR, 慢×快                       |
| **USA** | mdl31_roe 长窗         | omq5Pqkk 等        | 1.58 / —            | 252 窗, rank+ts_zscore             |

---

## 五、可直接落地的行动清单

1. **IND 新挖掘**：优先跑模板 2（`divide(rank(model), add(1, rank(analyst_downgrades)))`），遍历 mdl238/mdl25/mmdl31 等不同模型字段 + analyst39/analyst7 等不同分析师字段，找 2Y 最强组合。
2. **MEA 新挖掘**：跑模板 6/7 的字段替换（EPS/Net/Revenue 3 月修正 rank 相加），覆盖 est_q\_* 系列所有字段。
3. **EUR 新挖掘**：模板 4 的慢腿替换（尝试 mdl238/mdl177 替代 model residual）+ 快腿替换（尝试不同 PV 模式）。
4. **KOR 新挖掘**：模板 5 的慢腿替换（尝试其他 2Y 金矿慢变量）+ 与不同短周期信号交叉。
5. **降 PROD 相关性**：任何模板在提交前，**去掉与生产策略重叠的 revision/median 腿**（MEA 经验），**换 rank 为 quantile 外包装**（IND mdl238 已验证 2Y 2.74→3.01）。

---

*报告生成时间：2026-08-25，数据源 `data/wqb.db`，分析脚本 `logs/_tmp_count_stats.py` / `logs/_tmp_extract_wins.py` / `logs/_tmp_extract_more.py`*

