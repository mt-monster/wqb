# USA 已判死数据集清单（S0 自动剔除）

> **机器读取**：本文件首个合法的 ` ```json ` 代码块由 `tools/campaign_intel.py s0-select` 读取
> （路径约定 `tracking/<REGION>/reference/<region_lower>_dead_datasets.md`，实现见
> `_load_region_dead_list`）。命中且未过期的条目会被标 `region_dead` 并**沉底剔除**，
> `--include-region-dead` 可保留（只看原因、不投槽）。
>
> **过期即失效**：条目 `as_of` 早于 `review_after_days`（本文件 120 天）自动降为 advisory
> —— 只打印、不剔除。依据：用户 2026-10-23 纠正「以前的画像和数据证据都过期了，不能作证」。
> 无 `as_of` 的条目按过期处理。
>
> **人读**：下表是同一份清单的速查；改清单只改 JSON 块（表格不参与判定）。
> **判死 ≠ 永久封死**：重开需新证据 + 更新对应条目（改 `as_of` / 换 `verdict` 或删除该条），
> 不能靠 `--include-region-dead` 长期绕过。

- **region**: USA ｜ **as_of**: 2026-10-23 ｜ **review_after_days**: 120
- **来源**：`reports/usa_mining_history_review_20261023.md` §5 / §7.2 / §9；
  `output_report/USA_regular_alpha_delivery_20261021.md` §9.1–§9.3；
  `Claude/skills/wq-brain-ra-usa/references/` 各数据集画像终判节。

```json
{
  "region": "USA",
  "as_of": "2026-10-23",
  "review_after_days": 120,
  "source": "reports/usa_mining_history_review_20261023.md + output_report/USA_regular_alpha_delivery_20261021.md",
  "verdict_legend": {
    "dead_end": "平台 RA 硬闸反复不过 / 结构性墙，已封存",
    "prod_sealed": "prod 相关性实测 ≥0.75（D0-P 死线），机制级饱和",
    "signal_short": "强度上限远低于 1.58（max|S| 或裸探针），无信号",
    "structural": "构造与闸门结构性互斥（换手/F/强度三条不可能同时满足）"
  },
  "datasets": [
    {"dataset": "fundamental1", "verdict": "dead_end", "reason": "20 臂 / 15 字段 / 3 类变换 × 2 形状，两轮 max|S| 均 0.94；TO 1.6-2.1% 结构性年频", "evidence": "_usa-fnd1-field-profile-20261022.md §8", "as_of": "2026-10-22"},
    {"dataset": "fundamental2", "verdict": "signal_short", "reason": "八族同号负（-0.57…-1.00），镜面上限 +0.97；已封存", "evidence": "交付日志 §9.1；_usa-reports/fundamental2 批次", "as_of": "2026-10-21"},
    {"dataset": "fundamental14", "verdict": "signal_short", "reason": "RA 全过 0/20，max|S| 0.84", "evidence": "复盘报告 §5", "as_of": "2026-10-23"},
    {"dataset": "fundamental21", "verdict": "signal_short", "reason": "ESG 覆盖结构性偏大盘；最优 S 1.52/1.23 均不过线", "evidence": "_usa-fnd21-field-profile-20261021.md 终判节", "as_of": "2026-10-22"},
    {"dataset": "fundamental22", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭（强度不足 / 字段退化 / 已饱和）", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "fundamental25", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "fundamental35", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "fundamental69", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭（覆盖 0.39-0.43 + 季度频率）", "evidence": "_usa-risk60-field-profile-20261023.md §1；_usa-fnd69-field-profile-20261021.md", "as_of": "2026-10-23"},
    {"dataset": "fundamental72", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "fundamental91", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "fundamental93", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭（LOW_TURNOVER 实证）", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "fundamental110", "verdict": "dead_end", "reason": "fundamental 全线逐集全灭", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "other416", "verdict": "dead_end", "reason": "fundamental 路线同批全灭（字段退化 / 强度不足）", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "other452", "verdict": "dead_end", "reason": "fundamental 路线同批全灭", "evidence": "_usa-risk60-field-profile-20261023.md §1", "as_of": "2026-10-23"},
    {"dataset": "risk60", "verdict": "prod_sealed", "reason": "prod 0.9917（A1Qr9Y8W，RA 全过 / S 2.39）⇒ [0.9,1] 桶 n=116 结构性墙", "evidence": "复盘报告 §5 / §9.1；_usa-risk60-field-profile-20261023.md §7.2", "as_of": "2026-10-23"},
    {"dataset": "pv106", "verdict": "signal_short", "reason": "transaction_cost_estimate 是空列（5 臂零持仓），十臂 max|S| -0.30", "evidence": "_usa-pv106-field-profile-20261023.md", "as_of": "2026-10-23"},
    {"dataset": "pv149", "verdict": "signal_short", "reason": "USA-PV149-SIGNAL-SHORT：强度不足（停投）", "evidence": "_usa-pv149-field-profile-20261023.md §5", "as_of": "2026-10-23"},
    {"dataset": "pv20", "verdict": "signal_short", "reason": "46 行 RA 全过 3，max|S| 1.44 < 1.58", "evidence": "复盘报告 §5", "as_of": "2026-10-23"},
    {"dataset": "other143", "verdict": "prod_sealed", "reason": "prod 0.9206（0/4 过线）；冠军 RRA97Wo0 prod 0.8658 ⇒ 同机制判死（用了 8 波）", "evidence": "复盘报告 §5 / §9.1", "as_of": "2026-10-23"},
    {"dataset": "other635", "verdict": "signal_short", "reason": "5 个跨供应商分歧臂全负（最好 -0.86，取反 +0.86）且 RN -0.71（风格暴露）", "evidence": "_usa-other635-field-profile-20261023.md §5.3-§5.4", "as_of": "2026-10-23"},
    {"dataset": "other699", "verdict": "signal_short", "reason": "10/10 COMPLETE：最优 S 1.25 / F 0.51；结构与「选名靠活动度」互斥", "evidence": "_usa-other699-field-profile-20261021.md §4.16/§5", "as_of": "2026-10-21"},
    {"dataset": "other545", "verdict": "signal_short", "reason": "事件向量近似退化（vec_max≡vec_min≡vec_avg），最优壳 S 0.83 / F 0.48", "evidence": "_usa-other545-field-profile-20261021.md §5", "as_of": "2026-10-21"},
    {"dataset": "other571", "verdict": "signal_short", "reason": "双杀：IS 天花板 S 1.51 + prod 0.9087（USA-OTH571-DOUBLE-KILL）", "evidence": "_usa-oth571-field-profile-20261021.md §4", "as_of": "2026-10-21"},
    {"dataset": "other596", "verdict": "signal_short", "reason": "RA 全过 0/29，max|S| 0.91", "evidence": "复盘报告 §5", "as_of": "2026-10-23"},
    {"dataset": "other685", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "institutions18", "verdict": "prod_sealed", "reason": "prod 0.9493 / 0.9344（两条 RA 全闸）；USA-INSTITUTIONS18-PROD-SEAL", "evidence": "交付日志 §9 表", "as_of": "2026-10-21"},
    {"dataset": "web_traffic_engage", "verdict": "prod_sealed", "reason": "prod 0.9908（水平 0.9740/0.9906；变化量 0.9781/0.9782）⇒ USA-WEB-TRAFFIC-PROD-SAT", "evidence": "复盘报告 §5；交付日志附录 AB", "as_of": "2026-10-21"},
    {"dataset": "workforce_flow_skills", "verdict": "prod_sealed", "reason": "四条 RA 全闸的 prod 0.8586-0.9078 ⇒ USA-WORKFORCE-PROD-SEAL", "evidence": "交付日志附录 AE", "as_of": "2026-10-21"},
    {"dataset": "stock_search_trends", "verdict": "prod_sealed", "reason": "7/7 条 prod 0.8244-0.9382（跨中性化/窗口/反号/平滑）⇒ USA-STOCK-SEARCH-TRENDS-PROD-SAT", "evidence": "交付日志 §9 表", "as_of": "2026-10-21"},
    {"dataset": "intraday_pv_feats", "verdict": "structural", "reason": "corr-reversal prod 0.8693/0.8739；尾盘分支 0.7429 + CROWDING 负杠杆 ⇒ 收益/降 prod/换手三者互斥", "evidence": "_usa-intraday-pv-feats-field-profile-20261022.md §7", "as_of": "2026-10-22"},
    {"dataset": "news_transformer_scores", "verdict": "signal_short", "reason": "8 条最高 |S| 0.50（正向 0.46），远低于预登记 S≥1.00；同族 prod 0.72-0.83", "evidence": "_usa-news-transformer-scores-field-profile-20261022.md §4.2", "as_of": "2026-10-22"},
    {"dataset": "chart_return_model", "verdict": "structural", "reason": "期限错配：1-bar 预测在 D1 不可执行（_t100 S 1.22 / 2Y -0.01 / TO 57%），20 日臂 S 0.90", "evidence": "_usa-chart-return-model-field-profile-20261023.md §5-§6", "as_of": "2026-10-23"},
    {"dataset": "chart_model_alpha", "verdict": "structural", "reason": "11 波 30 臂：F 墙结构性（S≥1.58 需 RET≥5%，缺的完全是 TO 0.414 vs ≤0.125），平滑同时砍 S 与 RET", "evidence": "tracking/USA/runs/usa_cma_w1_notes.md §12", "as_of": "2026-10-23"},
    {"dataset": "shortinterest29", "verdict": "signal_short", "reason": "RA 全过 0/68，max|S| 0.79", "evidence": "复盘报告 §5", "as_of": "2026-10-23"},
    {"dataset": "multi_horizon_alpha", "verdict": "signal_short", "reason": "RA 全过 0/119，max|S| 1.16", "evidence": "复盘报告 §5", "as_of": "2026-10-23"},
    {"dataset": "continuation_score", "verdict": "signal_short", "reason": "RA 全过 7.7%（7/91），max|S| 1.36", "evidence": "复盘报告 §5", "as_of": "2026-10-23"},
    {"dataset": "order_flow_imb", "verdict": "signal_short", "reason": "D15：8 探针无 |S|≥0.5（最优 0.35 且符号为负），上限外推 ≈0.76", "evidence": "_usa-order-flow-imb-field-profile-20261021.md §5", "as_of": "2026-10-21"},
    {"dataset": "option3", "verdict": "dead_end", "reason": "已判弱 / 已封存（波 55 收批裁决）", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "pv47", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "pv103", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "pv115", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "dl_volume_pred", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "_usa-dl-volume-pred-field-profile-20261020.md；交付日志 §9 表", "as_of": "2026-10-21"},
    {"dataset": "insiders4", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "board_gov_stats", "verdict": "dead_end", "reason": "已判弱 / 已封存（波 85-87 三条轴扫尽）", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "earnings_risk", "verdict": "dead_end", "reason": "已判弱 / 已封存（波 84 复查留痕）", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "news_sentiment_transfer", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"},
    {"dataset": "sentiment26", "verdict": "dead_end", "reason": "已判弱 / 已封存", "evidence": "交付日志 §2 / §9 表", "as_of": "2026-10-21"}
  ]
}
```

## 速查表（不参与判定）

| verdict | 数据集（计数 47） |
|---|---|
| `dead_end` / `signal_short`（fundamental 路线） | `fundamental1/2/14/21/22/25/35/69/72/91/93/110`、`other416`、`other452` |
| `prod_sealed`（prod ≥0.75 机制级饱和） | `risk60`、`other143`、`institutions18`、`web_traffic_engage`、`workforce_flow_skills`、`stock_search_trends` |
| `signal_short`（强度不足 / 空列 / 退化） | `pv106`、`pv149`、`pv20`、`other635`、`other699`、`other545`、`other571`、`other596`、`news_transformer_scores`、`shortinterest29`、`multi_horizon_alpha`、`continuation_score`、`order_flow_imb` |
| `structural`（构造与闸门互斥） | `intraday_pv_feats`、`chart_return_model`、`chart_model_alpha` |
| `dead_end`（已判弱 / 已封存） | `other685`、`option3`、`pv47`、`pv103`、`pv115`、`dl_volume_pred`、`insiders4`、`board_gov_stats`、`earnings_risk`、`news_sentiment_transfer`、`sentiment26` |

**不在本清单（仍在途 / 有余量）**：`insider_matrix`（族内还有 prod<0.7）、`insider_agg_matrix`（virgin）、
`earnings_sent_matrix`、`techindi_model`（tm_w3 在途）、`ai_equity_alpha`（可交付但 MODEL 塔已点亮）。
