# 战役目录契约（Campaign Directory Contract）

toolkit 全部脚本以「战役目录」为输入。**DB 单轨**之后，战役目录里只有**配置**是必需的；产物（波表达式、评审、结果、typed catalog）已进 `data/wqb.db`，目录里若还有这些文件，是历史残留。每一项标 **[必需]** / **[可选]** / **[历史]**：

```
tracking/<REGION>/                       # 区域大写；region 只从 settings.json 派生并校验与目录名一致
  config/
    settings.json                        [必需] 仿真设置
    thresholds.json                      [必需] 阈值（缺节回落缺省，见下）
  reference/
    <region>_generation_constraints.json [可选] 区域生成约束（operator_stats / injection_rules / 区域特有 poison_patterns）
    <region>_<ds>_fields.json            [历史] typed catalog 文件；现由 scan_fields 写 DB，gate 先读 DB，文件仅作兜底
    <region>_<ds>_field_whitelist.json   [历史] legacy 白名单（兼容兜底）
    <region>_dataset_ranking.json        [历史] 数据集排名；现为 ledger 键 s0_ranking
  candidates/  reviews/  results/  <region>_wave*_exprs.json   [历史] 文件时代的波产物，DB 单轨后不再产出（不要 Write，见 SKILL §2）
  cache/                                 [可选] gate_cache.json / metrics/（可删除重建）
  priors/                                [可选] assemble-priors 的落盘副本（真相源是 ledger 键 priors_snapshot_<region>）
  # 战役台账 = data/wqb.db 的 ledger_kv 表（见 ledger-schema.md）
```

**缺目录 / 缺配置时的行为**（区域覆盖情况见 INDEX §区域清单；例：TWN 有 profile 但没有 `tracking/TWN/`，AMR 只有 `config/`）： <!-- lint:counterexample: 契约文档举例说明「区域覆盖不全」的情形：TWN 缺目录本身就是要描述的现状 -->

| 缺什么 | toolkit 脚本 | workflow 节点 |
|---|---|---|
| 整个战役目录 | `CampaignContext` 读 `config/settings.json` 时 `FileNotFoundError` | 报错并提示设 `WQB_CAMPAIGN_DIR` / `WQB_WORKSPACE_ROOT` 或先建 `tracking/<region>/` |
| `config/settings.json` | 同上（脚本不自动创建） | `campaign` 节点会按 DB ledger（`s0_whitelist` 的 delay / universe，再回落 `regions` 表）**自动补建**，不覆盖已有文件 |
| `config/thresholds.json` | `FileNotFoundError`（脚本要求它存在，可为 `{}`） | 各闸回落各自缺省（`signal_floor` 整节缺失 = fail-closed 回落缺省并输出 `warning`，见下） |
| `settings.json` 缺 `region` | `SystemExit`：`config/settings.json 缺 region 字段` | 同左 |

## settings.json（每战役一份，换 region 即换目录）

```json
{
  "instrumentType": "EQUITY", "region": "KOR", "universe": "TOP600", "delay": 1,
  "neutralization": "STATISTICAL", "decay": 4, "truncation": 0.08,
  "maxTrade": "ON", "pasteurization": "ON", "unitHandling": "VERIFY",
  "nanHandling": "ON", "language": "FASTEXPR", "visualization": false,
  "_multi_sim_batch_size": 8,
  "_concurrency_rule": "seven_slot_filling"
}
```

- `_` 前缀键是本地约定，不进提交 payload（pipeline 自动剔除）；`_concurrency_rule` 标的是填槽（见 `wqb-concurrency` §8）。
- region / universe / neutralization 的合法档位以 `config.REGIONS` 与 `mcp__wq-brain-http__get_platform_setting_options` 实测为准，**勿外推**（TOP1500 等非法档教训）。中性化取值受 RA 决策表 D5 约束（SECTOR / MARKET 会压垮 IS ladder），示例值 `STATISTICAL` 不是推荐值。

## thresholds.json：六节 + 可选节

> **两版 schema 并存**：下表六节是规范形态，但 KOR / IND / DEU 是**混合形态**——顶层扁平键（`sharpe_min` / `fitness_min` / `prod_corr_max` / `self_corr_max` / `turnover_min|max` / `sub_universe_sharpe_min` / `robust_sharpe_min` / `concentrated_weight_max`）保留，`quick_scan` / `hard_gates` 已补齐，**`probe_scoring_v2` 仍缺——刻意的**（补齐会改 S0 评分行为，需单独实证后再引入）。读阈值必须两版都兼容（缺节回落缺省），不要假定 `hard_gates.sharpe_min` 一定存在。

| 节 | 关键字段 | 消费方 |
|---|---|---|
| `review` | `sharpe_min` / `fitness_min` / `two_year_sharpe_min` / `margin_min` / `turnover_min|max` / `ra_failed_count_max` / `rn_sharpe_min`（缺省 0，≤ 此值 → `RN_EXPOSURE` 墙） | `review_wave`、`pipeline` |
| `near` | `sharpe_min`（近门槛池下限） | `review_wave`、`build_wave` |
| `quick_scan` | `red_2y_max` / `red_sh_abs_min`（快扫红灯早判） | 人工快扫 |
| `probe_scoring_v2` | 12 参数，见 [`probe-scoring-v2.md`](probe-scoring-v2.md) | `score_datasets` |
| `hard_gates` | 提交前参照的 prod / self 相关性上限。**全库数字的唯一事实源是 `src/wqb/config.py::GATES`**（内部严线 `GATES_INTERNAL` / 平台硬线 `GATES_PLATFORM`），这里的值只是区域副本，不得与它冲突 | 提交前参照 |
| `dataset_health` | `mode`（general / ppa）+ `tier_method`（quantile / threshold）+ 分位参数 `tier1_score_pct` / `tier2_score_pct` + 硬地板 `coverage_hard_min` / `field_count_hard_min` + 保底带 `backfill_band_*` / `probe_exception_*`；threshold 回退法用 `coverage_min` / `alpha_count_max` / `field_count_min` / `tier2_*`。**缺省值以代码为准**（`score_datasets.py` 与 `config.DATASET_HEALTH_SCORING`），文档不抄 | `score_datasets` |
| diversity | `signal_floor{max_sharpe_floor, min_batches, enabled}` 与 `stop_rules{…}`（**两者都有消费方**：`campaign.py` 的 `_run_signal_floor_gate` / `_run_stop_rules_gate`，S2 / S3 前置）；历史遗留 `entropy_min` / `similarity_max` / `narrow_cross_section` 当前无消费者 | workflow `campaign` 节点 |
| `poll`（可选） | `init_interval` / `backoff_factor` / `max_interval` / `stall_minutes` / `timeout_minutes`；缺省见 [`poll-and-quota.md`](poll-and-quota.md) | `pipeline`、`poller` |
| `submit_quota`（可选） | `limit`（REGULAR 日上限，缺省 4）、`enabled`（**缺省 false**：2026-08-26 用户指令关闭配额闸）。三条并行通道 REGULAR 4 + SUPER 1 + PPA `POWER_POOL_SUBMISSION` 1，均 00:00 ET 重置 | `pipeline quota` |
| `settings_prior`（可选） | `enabled` / `min_n`（30）/ `min_lift`（2.0）/ `dims`：按 `region_kb.gate_priors` 改写 decay / neutralization | `pipeline.py run`（`--no-settings-prior` 关闭） |

`diversity.signal_floor` 的语义（易误读）：**整节缺失 → fail-closed**，回落缺省 `max_sharpe_floor=0.5` / `min_batches=2` 继续判定并输出 `warning`；`thresholds.json` 不可读同理。**只有显式 `enabled:false` 才放行**。改版前是「整节缺失即静默放行」，与停止闸使命矛盾（GBR 曾因此跑满 180 条回测、max|sharpe|=1.04、达标 0 条）。

`diversity.stop_rules` 完整键（缺节取缺省；ledger `stop_rules_override{reason,until}` 可按用户指令放行）：`enabled` / `yield_min_backtests`（100）/ `consecutive_fail_waves`（3）/ `axis_scope` / `axis_window` / `distinct_fail_axes` / `exempt_zero_cost_waves` / `exempt_dead_end_waves`。规则 A：区域 backtested ≥ `yield_min_backtests` 且 passed = 0；规则 B（按轴）：同轴连续 K 波可计数 FAIL 熔断，或窗口内 ≥ D 个不同轴全 FAIL 且无 PASS 停区；`axis_scope:false` 或 schema 不齐回落旧口径「最近 3 个 closed 波全 FAIL」。

## reference/ 约定

- **typed catalog**：数据集级 `{dataset, region, universe, delay, data_type, type_distribution, field_count, fetched_at}`；字段级 `{id, type, coverage, userCount, alphaCount, description[:120]}`；`data_type` 由字段 `type` 众数推断。**现存 DB（`fields` 表）**，`scan_fields.py` 写入。
- legacy whitelist（`verified_fields` 列表 + cov 简写）仍被 gate 兼容读取；新战役一律用 `scan_fields` 落 catalog。
- `<region>_generation_constraints.json`：`operator_stats{used,unused,rare}`（`diversity_audit` 实测回填）、`injection_rules{force_explore_ops, cap_ops, skeleton_quota}`、`poison_patterns[]`（**仅区域特有**；平台级见 toolkit `config/platform_constraints.json`）。
