---
region: DEU
entry_verdict: probe-only
one_liner: "全域 16 类 0 alpha 的处女地（统一 1.9× 倍率、PPA 点塔无竞争），但存在 sub_universe 结构性墙（limit≈0.47×sharpe，DEU 需 0.8，实测仅 0.30）——先探针定墙，再决定是否升 active"
static:
  universe: [TOP500, TOP300]
  universe_default: TOP500
  delay: [1, 0]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "档位取自 src/wqb/config.py::REGIONS（DEU 合法档 TOP500/TOP300）；SUBINDUSTRY/decay4 来自 tracking/DEU/config/settings.json"
datasets:
  red: []
  red_reason: ""
  yellow: [model264, model238, model53, pattern_scores, news104, analyst_earnings_ibes, institutions6, sentiment27]
  green: [fund_holdings_panel, insider_agg_matrix, analyst93, analyst44, other455, pv29]
priors:
  signal_families_include: [institutions_holdings, insider_direction, analyst_revision]
  signal_families_exclude: []
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死；sub_universe 未过则不再加变体（墙是结构性的，调参无解）"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(DEU)"
  last_verified: 2026-09-11
---

# DEU — 零竞争处女地 + sub_universe 结构性墙

> 本 profile 为 **2026-09-11 审计补建**：DEU 早于审计就已有战役目录（`tracking/DEU/` 含
> `config/` + `deepexplore/` 旧产物）与 S0–S2 台账（ledger `s0_ranking` / `s0_calibrate_DEU` /
> `s1_prefix_sentiment27` / `s2_field_pool_sentiment27`），却**没有 region profile**，
> 按 ra-pipeline 规则会被误判为"处女地模板（参照 ASI）"，掩盖了本区已知的关键约束。

## 定位与实证依据

来源：`tracking/mining/DEU_D1_TOP500_health_check.md`、`DEU_D1_dataset_exploration_recommendations.md`、
`DEU_D1_feature_engineering_A档.md`、`DEU_D1_TOP500_final_report.md`（均 2026-08-10~09-02 生成）。

| 维度 | 现状 |
|---|---|
| 金字塔状态 | **D1 全域 16 个类别全部 0 alpha（全空白）**，平台上几乎无人点亮 DEU 任一金字塔 |
| 倍率 | 全域统一 **1.9×**（仅 shortinterest 1.7×）→ 点塔收益高 |
| 竞争度 | 极低：零竞争 1 个、超低竞争（alphaCount≤5）4 个 |
| 通过 PPA 硬门槛（cov≥0.85/α≤50/fields≥10） | **11 个数据集** |
| ⚠ 已知瓶颈 | **sub_universe 结构性墙**：limit ≈ 0.47×sharpe（DEU 需 0.8），实测最好仅 0.30。已在 model264 / model238 / model53 / pattern_scores / news104 / analyst_earnings_ibes / institutions6 / sentiment27 上验证 |

**台账实况**：`backtest_results` 中 DEU **0 条**、`wave_results` **0 条**、`registry_empirical` **0 条**
（即 S3 从未产出）→ 故 `entry_verdict: probe-only`，不是 active。
`tracking/DEU/deepexplore/` 是已废止的 `brain-deepExplore` 遗留产物，**不再使用**（勿据其续跑）。

## 流程变体（相对九步骨架）

### 步 2 注入：白名单按"未测白空间"优先

绿榜（**全新白空间，优先探**）：
- `fund_holdings_panel`（institutions，cov 0.90，**α=0 / users=0 零竞争**，18 字段，字段级覆盖 0.876–0.928）
- `insider_agg_matrix`（insider，`directional_indicator` **cov=1.00 且 α=0**，34 字段）
- `analyst93`（欧洲分析师历史盈利性，100 字段）、`analyst44`（事件式经纪商修订，72 字段）
- `other455`（1500 字段超大选择空间，部分测试）、`pv29`（行业分类，非信号本体）

黄榜（**已测撞 sub_universe 墙**，非判死但暂不再投同腿变体）：
model264 / model238 / model53 / pattern_scores / news104 / analyst_earnings_ibes / institutions6 / sentiment27。

### 步 3 / 步 5 注入：先验墙，再谈信号

- 步 3 字段扫描必须显式产出该数据集**在 TOP500 上的 longCount**（小宇宙伪白空间与 KOR/HKG 同源风险）。
- 步 5 门禁前先跑 **1 条单仿真探针看 `LOW_SUB_UNIVERSE_SHARPE`**：
  `limit≈0.47×sharpe`，要过 0.8 需 raw sharpe ≳1.7——**若单探针 sub_universe 明显不足，不再扩批**，
  直接判该数据集对本区（小宇宙）不可用并回写 dead_end（rule：结构性墙，调参无解）。

### 步 7 注入：CW 与覆盖

- `cw_gate: WARN`（与全局一致；DEU 尚无 CW 实测数据，不预先加严）。
- 全区仅 1 个体检包（`field_coverage_DEU_d1_TOP500.json`），**`field_inspect_deu_*` 为 0** →
  步 5 的体检硬门对本区**不生效**（wave_gate 会打印 `[inspect] 体检硬门未生效`）。
  首次批次前需 `python tools/webdata_quality.py --zip <WebDataScope包> --export-expr tracking/mining/field_inspect_deu_<ds>.json` 现生成。

## 升档条件（probe-only → active）

同时满足才升级，并把结论回写本 profile：
1. 至少一个数据集用单仿真证明 `LOW_SUB_UNIVERSE_SHARPE` 可达（探针 raw sharpe ≳1.7）；
2. 或在**非小宇宙**结论下（若未来开放更大 DEU 档）复测该墙是否消失；
3. 至少 1 波 S3 有 `backtest_results` 入库（当前为 0）。
