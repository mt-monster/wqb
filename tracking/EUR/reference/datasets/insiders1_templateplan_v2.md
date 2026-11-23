# insiders1 · 补缺 TemplatePlan v2（2026-11-23，铁律二次加严后：≥10 个**机制**）

> **违规盘点**：已测机制仅 4 个（A 52周锚定 / B 仓位比例 / C 显著性加权 / 方向拆分-结构性无效），距 10 缺 6。
> 已测变体（窗口/算子/包装栈/宇宙/中性化/幅度轴）**不计入机制数**。
> 本文件 = 6 个新机制（M4-M9，编号接续），每个=不同经济假设，全部标注来源。
> 配置基准沿用机制 B 最优：TOPCS1600 / SUBINDUSTRY / decay4 / trunc0.08 / nan ON，44d 窗（机制 B 窗口峰）。

## 0. 取证留痕

### 论文（paper_search --diverse：20 篇过闸）

| DOI | 标题 | 年 | 挂靠新机制 |
|---|---|---|---|
| 10.1016/j.pacfin.2012.07.006 | Opportunistic insider trading | 2013 | M4 机会主义识别 |
| 10.1016/j.iref.2026.105190 | Opportunistic insider trading: symbolic purchases | 2026 | M4 象征性买入 |
| 10.2139/ssrn.5127723 | **Reverse Timing of Insider Trading** | 2025 | M5 反向时序 |
| 10.2139/ssrn.3478344 | **A Theory of Insider Purchases** | 2019 | M6 买入理论（大额 vs 集群）|
| 10.1007/s11293-006-9060-8 | What Enhances Insider Trading Profitability? | 2007 | M7 盈利增强条件 |
| 10.2139/ssrn.4231415 | Fortunate Timing: Scheduled Insider Trades | 2022 | M8 计划交易 vs 自发 |
| 10.2139/ssrn.1959552 | Insider Purchases Talk and Buybacks Whisper | 2011 | M9 买入 vs 回购语境 |

### 论坛

| 帖 | 价值 |
|---|---|
| 44687266076823（Momentum Crashes 双腿审计） | M5 反向时序的方法学：先审计两腿再设计 timing |
| 44731710962839（三信号对齐） | 多机制合取的 rank-add-衰减范式（机制 B/C 复用） |

## 1. 六个新机制（每模板一行）

| # | 机制（经济假设） | reading | template 骨架 | 来源 |
|---|---|---|---|---|
| **M4** | **机会主义 vs 常规**：偏离自身申报节奏的大额交易才有信息（CMP 2012 的时序版，此前只测了显著性评分静态版）| 交易强度偏离其 252d 基线的 z × 强度 | `group_rank(multiply(group_zscore(ts_sum(divide(vec_sum(insd1_valueeur),add(vec_sum(insd1_holdings),1)),44),industry),ts_rank(vec_count(insd1_valueeur),252)),industry)` | PacFin 2013 + IREF 2026 |
| **M5** | **反向时序**：内部人整体是**反向指标**（他们也在追涨杀跌）⇒ 卖压后买入、买压后卖出 | 交易强度取反后与 52 周位置组合 | `group_rank(multiply(-1,ts_sum(divide(vec_sum(insd1_valueeur),add(vec_sum(insd1_holdings),1)),44)),industry)` 纯反向 + 与 ts_scale(price,252) 交互两臂 | SSRN 5127723（2025 Reverse Timing）|
| **M6** | **大额稀有事件**：只有超过自身历史分位的**大额申报**有信息（Theory of Insider Purchases：大额=强信念）| amount 的 252d 分位门控 × 比例强度 | `trade_when(greater(ts_rank(vec_sum(insd1_valueeur),252),0.8),group_rank(ts_sum(divide(vec_sum(insd1_valueeur),add(vec_sum(insd1_holdings),1)),44),industry),-1)` | SSRN 3478344（2019）|
| **M7** | **盈利增强条件：公司质量**——内部人买入只在高质量公司有信息（profitability 条件）| 用本集可用代理（sharesheld 稳定性=机构型持仓）作质量门控 | `trade_when(less(ts_std_dev(ts_backfill(vec_sum(insd1_holdings),66),252),<档>),group_rank(ts_sum(divide(vec_sum(insd1_valueeur),add(vec_sum(insd1_holdings),1)),44),industry),-1)` | 10.1007/s11293-006-9060-8 |
| **M8** | **申报密度事件窗**：申报笔数突增（clustered trading）比单笔金额更有信息 | vec_count 的 252d z 作主信号（非门控） | `group_rank(ts_zscore(ts_backfill(vec_count(insd1_valueeur),66),252),industry)` | 帖 44731710962839（集群腿）+ Fortunate Timing 2022 |
| **M9** | **价格确认**：内部人买入+价格趋势同向才有效（buybacks whisper：单独买入信号弱，需价格确认） | 交易强度 × 价格 52 周位置的交互 | `group_rank(multiply(ts_sum(divide(vec_sum(insd1_valueeur),add(vec_sum(insd1_holdings),1)),44),ts_scale(vec_avg(insd1_price),252)),industry)` | SSRN 1959552（2011）+ 10.2139/ssrn.4231415 |

## 2. 串行执行序（每机制：探针 2 臂 → 梯度按 0.5 阈值分流）

| 序 | 机制 | 探针 | 梯度预案 |
|---|---|---|---|
| 1 | M4 机会主义 | 2 臂（×/÷ 两种组合） | ts16 全替 + z 窗 3 档 |
| 2 | M5 反向时序 | 2 臂（纯反向/交互） | 反向已证纯翻转则只测交互臂 |
| 3 | M6 大额门控 | 2 臂（分位 0.8/0.9） | 门控阈值 3 档 |
| 4 | M7 质量门控 | 2 臂（std 阈 2 档） | 阈值 3 档 |
| 5 | M8 密度 z | 2 臂（z/rank） | ts16 全替 |
| 6 | M9 价格确认 | 2 臂（×/条件） | 交互 vs trade_when 对照 |

**预期**：6 机制 ×（2 探针 + 4~8 梯度）≈ 40~50 臂。完成后 insiders1 机制数 = 4 + 6 = **10 达标**。
