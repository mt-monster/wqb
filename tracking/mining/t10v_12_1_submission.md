# T10v_12_1 提交尝试记录（2026-08-05 22:0x）

## Alpha 标识
- label: `T10v_12_1`
- alpha_id: **`A1G6QpOQ`**
- 数据集: `ml_factor_proj`（EUR / TOP1200 / D1）
- 表达式:
  `group_zscore(subtract(group_zscore(change_twelve_month_active_return, industry), group_zscore(change_1m_active_return, industry)), industry)`
- 设置: EQUITY / EUR / TOP1200 / delay=1 / decay=4 / neutralization=INDUSTRY / truncation=0.08 / pasteurization=ON / unitHandling=VERIFY / nanHandling=OFF / FASTEXPR；回测区间 2014-01-01 ~ 2023-12-31

## IS 指标（平台 get_alpha_details 实测）
| 指标 | 值 | 备注 |
|---|---|---|
| Sharpe | 1.14 | PP 闸门≥1.0 通过；常规闸门需>1.3 |
| Fitness | 0.61 | PP 通过；常规需>0.75 |
| Turnover | 0.1607 | 5%~20% 内，通过 |
| Returns | 0.0466 | >5% 通过 |
| Drawdown | 0.0703 | Returns>DD 通过 |
| Margin | 0.00058 (5.8bp) | **<15bp 硬下限，未过** |
| sub_universe_sharpe | 1.19 | >0.7 通过 |
| 2y_sharpe | -0.49 | 低（WARNING） |
| investability_sharpe | 1.28 | — |
| operators | 2 | ≤8 合规 |
| fields | 2 | ≤3 合规 |

## 平台分类（关键）
- `ra_failed = true`，`ra_failed_checks = [LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE]`
- **`ppa_failed = false`，`failed_ppa_count = 0`** → 平台判定为**合规 Power Pool Alpha**
- `pyramids`: EUR/D1/OTHER, multiplier 1.5
- `checks.pending`: SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION / POWER_POOL_CORRELATION

## 闸门校验
- 本地 `check_self_correlation(type=powerpool, threshold=0.5)`:
  `max_correlation = 0.0`，`passes_check = true` → Power Pool 自相关闸门通过（<0.5）。
- 生产相关性(PROD_CORRELATION)与 POWER_POOL_CORRELATION 仍为 PENDING（需提交时平台计算）。

## 提交动作（实测结果）
1. `set_alpha_properties(A1G6QpOQ, tags=["PowerPoolSelected"], color=GREEN, descriptions=三段英文)` → 成功，status 仍 UNSUBMITTED。
2. `submit_alpha(A1G6QpOQ)` → **blocked: true / success: false**
   - failures:
     - "Sharpe 1.14 <= 1.3 (required > 1.3)"
     - "Fitness 0.61 <= 0.75 (required > 0.75)"
     - "Margin 0.0580% <= 8bp (hard floor, required > 15bp)"
3. 打标后重试 `submit_alpha` → 仍被同一常规闸门拦截（工具不看 PPA 标签）。

## 结论
- **MCP submit_alpha 工具不是 PPA 感知的**：它对合法 PPA 也套用常规 RA 闸门(Sharpe>1.3/Fit>0.75/Margin>15bp)并拦截；即使打 PowerPoolSelected 标签也不放行。
- 该 alpha 平台侧是合规 PPA（ppa_failed=false），但因 Sharpe/Margin 未达常规闸门，MCP 通道无法提交。
- `create_spc_submission` 是 SPC(LLM 提示词挑战)，与 alpha 提交无关。

## 下一步（待用户决策）
- **A（推荐）**：在 WQ Brain 网页端直接提交——平台 PPA 闸门(Sharpe≥1.0)接受此 alpha；已预置 PowerPoolSelected/GREEN/descriptions。
- **B**：强化 alpha 至过常规 MCP 闸门（Sharpe→1.3+/Fit→0.75+/Margin→15bp+，Margin 需 ~2.6x 最难）。
- **C**：转向再挖 2 个去相关 PPA（同族扫 decay/中性化 或换 news_sentiment_nlp 等数据集）。
