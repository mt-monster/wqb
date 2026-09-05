# 战役目录契约（Campaign Directory Contract）

toolkit 全部脚本以"战役目录"为输入。新区域开战役时按下述布局建目录即可复用全部能力。

## 目录布局

```
tracking/<REGION>/                 # 区域大写，如 KOR / USA / EUR
  config/
    settings.json                  # 仿真设置（必填）
    thresholds.json                # 集中阈值（必填）
  reference/                       # 区域级实测数据（toolkit 生成或人工维护）
    <region>_<dataset>_fields.json         # typed catalog（scan_fields 产物，gate 闸2/3 数据源）
    <region>_<dataset>_field_whitelist.json # legacy 白名单（兼容兜底，逐步被 catalog 取代）
    <region>_generation_constraints.json    # 区域生成约束（operator_stats/skeleton_quota/poison_patterns[区域特有]）
    <region>_dataset_ranking.json           # score_datasets 产物
  candidates/                      # 待回测表达式批次（probe_<ds>_exprs.json / new_exprs.json）
  <region>_wave*_exprs.json        # 各波次表达式（build_wave 产物；也接受 candidates/ 下存放）
  reviews/                         # review_wave 产物
  cache/                           # gate_cache.json / metrics/ / pipeline checkpoint（可删除重建）
  results/                         # pipeline checkpoint（断点续跑状态）
  # 战役台账：data/wqb.db 的 ledger_kv 表（LedgerStore SQLite 后端，见 ledger-schema.md；旧 <region>_d1_campaign_state.json 已归档）
```

## settings.json（每战役一份，换 region 即换目录）

```json
{
  "instrumentType": "EQUITY", "region": "KOR", "universe": "TOP600", "delay": 1,
  "neutralization": "SECTOR", "decay": 4, "truncation": 0.08,
  "maxTrade": "ON", "pasteurization": "ON", "unitHandling": "VERIFY",
  "nanHandling": "ON", "language": "FASTEXPR", "visualization": false,
  "_multi_sim_batch_size": 8,
  "_concurrency_rule": "seven_slot_filling"  # 七槽填槽：每轮7批同提、即收即补保持槽位常满（wqb-concurrency §8；旧'单批在飞'已废弃，2026-08-25 更新：5→7）
}
```
- `_` 前缀键为本地约定，不会进提交 payload（pipeline 自动剔除）。
- region/universe 合法档位先查 wq-brain-campaign-matrix 的 registry 或 mcp__wq-brain-http__get_platform_setting_options，勿外推（TOP1500 等非法档教训）。

## thresholds.json 六节（+2 可选节）

| 节 | 关键字段 | 消费方 |
|---|---|---|
| review | sharpe_min / fitness_min / two_year_sharpe_min / margin_min / turnover_min/max / ra_failed_count_max | review_wave, pipeline |
| near | sharpe_min（近门槛池下限，供增强方向分析） | review_wave, build_wave |
| quick_scan | red_2y_max / red_sh_abs_min（快扫红灯早判） | 人工快扫 |
| probe_scoring_v2 | 12 参数（见 probe-scoring-v2.md） | score_datasets |
| hard_gates | prod_correlation_max 0.7 / self_correlation_max 0.7 | 提交前参照（权威定义见 brain-how-to-pass-AlphaTest） |
| dataset_health | v3.1：mode(general/ppa) + tier_method(quantile/threshold) + 分位参数 tier1_score_pct/tier2_score_pct + 硬地板 coverage_hard_min(0.65)/field_count_hard_min(5) + 保底带 backfill_band_*/probe_exception_*；threshold 回退法沿用 coverage_min/alpha_count_max/field_count_min/tier2_* | score_datasets |
| poll（可选） | init_interval 20 / backoff_factor 1.5 / max_interval 120 / stall_minutes 60 / timeout_minutes 360 | pipeline, poller |
| submit_quota（可选） | limit 4（REGULAR 日上限；SUPER 1/日由提交层单独把关） | pipeline quota（ET 日历日 4/1 口径，00:00 ET 重置） |

## reference/ 约定
- typed catalog schema：数据集级 `{dataset, region, universe, delay, data_type, type_distribution, field_count, fetched_at}`；字段级 `{id, type, coverage, userCount, alphaCount, description[:120]}`。data_type 由字段 type 众数推断。
- legacy whitelist（`verified_fields` 列表 + cov 简写）仍被 gate 兼容读取；新战役一律用 scan_fields 落 catalog。
- `<region>_generation_constraints.json`：`operator_stats{used,unused,rare}`（diversity_audit 实测回填）、`injection_rules{force_explore_ops, cap_ops, skeleton_quota}`、`poison_patterns[]`（**仅区域特有**；平台级见 toolkit config/platform_constraints.json）。
