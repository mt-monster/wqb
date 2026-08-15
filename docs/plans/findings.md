# Findings & Decisions

## Campaign lock
- EUR / Delay 1 / Regular / universe TOP1200（体检锁定）
- 当前 PPA 主题 `GLB/D1 Power Pool Aug'26 2` + TOPDIV3000 → EUR **不能**当 PPA
- 目标 3 个硬闸门可提交 RA；配额 remaining=0 至约 2026-08-15 08:20 ET，只回测不 POST
- EUR D1 金字塔全未点亮；最高倍率 **other 1.5**，其次 sentiment 1.4 / analyst·news·model 1.3

## Whitelist 已证伪（本 NY 日，禁止再 GEM）
| Dataset | max \|Sharpe\| | 结论 |
|---------|----------------|------|
| news_sentiment_nlp | 0.42 | VECTOR 弱信号 |
| ml_factor_proj | 0.42 | enhance 更差 |
| dl_riskfree_returns | Fitness 0.88 vs 2Y 失败 | wrap 网格停 |
| analyst_earnings_ibes | 0.48 | 字段实为延迟 PV |
| ai_factor_transfer | 0.42 (`6XpZlznE`) | 8/8 全 FAIL LOW_SHARPE；不 enhance |
| price_signal_dl | rank 0.30；ts_* 8/8 FAIL | 字段能跑，复杂算子编译失败；停 |

## 当前最强：global_seasonal_model（model 塔 1.3）
裸 5d spread `confidence_bucket4_pricevol_5d - confidence_bucket0_pricevol_5d`

| Alpha | Neu | Decay | Sharpe | Fitness | TVR | 2Y | CW |
|-------|-----|-------|--------|---------|-----|----|----|
| YPv8lXVv | INDUSTRY | 4 | 1.16 | 0.37 | 50% | **1.68 pass** | pass |
| RRm9KKWn | **CROWDING** | 4 | **1.37** | **0.52** | 50% | **1.87 pass** | pass |
| VkGZ55J0 | FAST | 4 | 1.34 | 0.37 | 55% | 1.49 fail | pass |
| N1bL33ve | SUBINDUSTRY | 4 | 1.22 | 0.38 | 50% | — | — |

教训：
- 重平滑（ts_decay_linear 20 / enhance 族）TVR 可进 5–20%，但 Sharpe 掉到 0.4–0.7 且 **2Y 被杀**（j26oGoOQ 2Y 0.47）
- 表达式 wrap 全面劣于改 neutralization
- `CROWDING_Q` 在 EUR 实际不可用（multi 400 拖垮整批）

## CROWDING 网格 2（8/8 COMPLETE，去掉非法 CROWDING_Q）
| Alpha | 设置 | Sharpe | Fitness | TVR | 2Y |
|-------|------|--------|---------|-----|-----|
| KPGvZO9z | CROWDING d5 | 1.34 | 0.53 | 44% | — |
| ak1eGLE2 | CROWDING d6 | 1.29 | 0.53 | 40% | — |
| RRm9PV11 | CROWDING d7 | 1.26 | 0.53 | 37% | — |
| A1GeE0GQ | CROWDING d4 maxTrade ON | 0.92 | 0.43 | 20% | **0.81 fail** |
| npNmrKN3 | CROWDING trunc 0.05 | 1.37 | 0.52 | 50% | 同基准 |

Fitness 天花板 0.53。停 gsm 重平滑/再网格。下一集 **continuation_score** MATRIX（pv，alphaCount=0）。ai_equity_alpha / news54 实测全 VECTOR，低优先。

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| TOP1200 不切 TOP2500 | 当日体检与 loop_state 已锁 |
| nanHandling ON | DL/model 缺测 |
| 不 enhance 死集 | Sharpe<0.5 本战役禁再 GEM |
| CROWDING 优于 INDUSTRY | 同表达式 Sharpe 1.16→1.37、收益 4.95%→7.27% |
