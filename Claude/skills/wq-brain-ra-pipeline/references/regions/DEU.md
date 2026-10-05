---
region: DEU
entry_verdict: active
one_liner: "零竞争高倍率区（统一 1.9×、D1 全域 16 类塔本季全空）但**合规形态天花板 0.69 vs ladder 1.58 = 2.3× 落差**才是真墙——历史 6 颗 ACTIVE 的 S1.68~2.17 全靠 4~5 腿 add 相加（铁律 §0 违规族）取得，无 win recipe 可继承"
static:
  universe: [TOP500]
  universe_default: TOP500
  delay: [1, 0]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "档位取自 src/wqb/config.py::REGIONS（当前只登记 TOP500；TOP300 未在档位表，需 get_platform_setting_options 实测后由 config 补入，profile 随之更新）；SUBINDUSTRY/decay4 来自 tracking/DEU/config/settings.json"
datasets:
  red:
    - datasets: [analyst35, analyst44, analyst48, fundamental17, insider_trx_matrix, model141, model16, model262, news50, option1, other128, other532, other545, other546, other699, pv20, risk60, risk88, workforce_flow_skills]
      reason: "DB 实证判死（键 = ledger *_dead ∪ 旧 red 文本 id；明细查 get_dead_datasets）"
  green:
    - datasets: [analyst93, fund_holdings_panel, insider_agg_matrix, other455, pv29]
      note: "旧 green 文本 id ∪ registry win 层实证绑定"
  yellow: [model264, model238, model53, pattern_scores, news104, analyst_earnings_ibes, institutions6, sentiment27]
priors:
  signal_families_include: [institutions_holdings, insider_direction, analyst_revision]
  signal_families_exclude: []
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: WARN
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死。**注意：sub_universe 不再作为探针早停依据**——该闸是 IS sharpe 的线性函数（limit≈0.47×S），S≳1.7 时自动过；历史「实测 0.30」来自 S≈0.6 的低分批被误读为墙（见正文『伪墙更正’）"
  stop_conditions: ["白名单被 dead_end 全覆盖", "合规形态天花板（~0.69）距 ladder 1.58 无可行路径"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(DEU)"
  last_verified: 2026-10-02
---

# DEU — 零竞争高倍率区，但真墙是「合规形态天花板 0.69 vs ladder 1.58」

> **2026-10-02 全面更正**（下列内容为原 2026-09-11 建档文本，事实已变，推翻处标 ✅ 已作废）：
> ① `entry_verdict` probe-only → **active**（原「S3 从未产出」前提已被 1410 回测行 / 6 颗 ACTIVE 推翻）；
> ② 「sub_universe 结构性墙」= **伪墙**，见下方『伪墙更正』；
> ③ 原绿榜 5 集**现已全部判死或降级**（`analyst93` prod 饱和 / `insider_agg_matrix` 域锁 0.95-0.98 /
> `fund_holdings_panel` 双死 / `other455` spine 探死 best 0.06 / `pv29`+`pv30` 均 GROUP 类非信号本体）。
> ④ 步 5「sub_universe 未过即判该集不可用」的门禁注入**已删除**（基于伪墙的错误门禁）。
>
> 原建档背景（保留）：DEU 早于审计就有战役目录与 S0–S2 台账却无 profile，会被误判为处女地模板。

## 伪墙更正：sub_universe 是 IS sharpe 的线性函数，不是天花板

**原判（错）**：`limit ≈ 0.47×sharpe`（DEU 需 0.8），实测最好仅 **0.30** → 结构性墙、调参无解。
**反证（6 颗 ACTIVE 全部 PASS 该闸）**：

| alpha | IS S | sub_universe | S×0.47 | ratio |
|---|---|---|---|---|
| 883Y3bAW | 2.17 | 1.44 | 1.02 | 0.66 |
| 2rOe10qY | 2.10 | 1.11 | 0.99 | 0.53 |
| blRnKEk6 | 2.02 | 1.43 | 0.95 | 0.71 |
| vRk6og8b | 1.80 | 1.26 | 0.85 | 0.70 |
| Vk65zLzG | 1.79 | 1.44 | 0.84 | 0.80 |
| JjxrYjre | 1.68 | 1.49 | 0.79 | 0.89 |

当年「实测 0.30」来自 S≈0.6 的低分批（S×0.47≈0.28），被误读为墙。**S≳1.7 时该闸自动过。**

> **可推广教训**：凡「limit ≈ k×sharpe」型比值闸，k×S 随 S 线性增长，**低分区实测值不可外推为墙**。

## 现状（2026-10-02 实测）

| 维度 | 现状 |
|---|---|
| 金字塔 | D1 全 16 类本季（Q4）**全空**；6 颗 ACTIVE 提交于 09-13/14（Q3）→ 按自然季度清零，点塔空间全开 |
| 倍率 | 统一 **1.9×**（shortinterest 1.7×）→ 全区最高 |
| 产出率 | `yield_rate` **0.1163**（164 ra_clean / 1410 回测），`prod_clean` 仅 **6** |
| prod 墙 | measured 50 颗中 **44 颗撞墙 = 88%**；IS 2.1 的近门候选普遍 prod 0.77–0.94 |
| 可行未提交存量 | **0 颗** |
| 判死记录 | `get_dead_ends` 40 条；`get_dead_datasets` 19 集 |
| **可用信号集** | **0**（见下） |

**★ 真正的墙 = 合规形态天花板 0.69 vs ladder 1.58（差 2.3×）**
- 合规单信号实测天花板：`other545` **0.69**（22 探针）/ `fhp` 0.53 / `other699` 0.48 / `fundamental6` 0.35 / `insider_trx_matrix` 0.33 / `risk60` 0.29
- 而 6 颗 ACTIVE 的 S 1.68–2.17 **全部靠 4~5 腿 `add` 相加取得 = 铁律 §0 违规族**
  （JjxrYjre/2rOe10qY/blRnKEk6/vRk6og8b/Vk65zLzG/883Y3bAW 逐条实测，6/6 命中）
⇒ **DEU 有真信号，但只存在于被禁形态里** ⇒ **无 win recipe 可继承**，不是「素材耗尽」而是「形态×纪律落差」。
⇒ 复用历史胜绩骨架会**直接违反混信号禁令**（`gate` 的 `equal_weight_leg_add` 结构性闸会拦）。

## 流程变体（相对九步骨架）

### 步 2 注入：白名单必须交叉核历史，别只看 S0 榜
⚠ **2026-10-02 教训**：09-29 锁过一份白名单（`pv30` / `pattern_scores` / `other455`），三集**全部不可用**，
但当时都通过了 S0 榜（tier1、cov 0.73–0.99）。锁白名单前**必须**交叉核：
1. `expressions` 表该集 `status`（`fail`/`dropped` 说明已探过）
2. ledger 判词类记录（探死看 `<dataset>_dead`；非信号字段 / 空覆盖看 `s1_semantic_<ds>` 的 `blocked_fields`）
3. 历史 probe 波的 `backtest_results`（`backtested=0` **≠ 未测**，可能是"测了但零入库"）

**数据集分类硬闸**：`catalog.data_type == "GROUP"` 的数据集**不得进信号白名单**，只能当 `group_rank` 分组轴
（`pv29` / `pv30` 均属此类；S1 语义分类会把 GROUP 字段误标为 `signal_field_count=285/blocked=0`，需人工拦）。

### 步 3 注入：字段扫描产出 longCount
字段扫描必须显式产出该数据集**在 TOP500 上的 longCount**（小宇宙伪白空间与 KOR/HKG 同源风险）。

### 步 5 注入
（**原「先跑 1 条探针定 sub_universe 墙、不通过即判数据集不可用」已删除** —— 基于伪墙，见『伪墙更正』。）

### 步 7 注入：CW 与覆盖
- `cw_gate: WARN`（与全局一致）。
- 全区仅 1 个体检包（`field_coverage_DEU_d1_TOP500.json`），**`field_inspect_deu_*` 为 0** →
  步 5 体检硬门对本区**不生效**（wave_gate 打印 `[inspect] 体检硬门未生效`）。
  首次批次前需生成：`$WQ_PY tools/gen_field_inspect_packs.py --region DEU --delay 1`。

## 升档条件（已于 2026-10-02 满足 → active）

1. ✅ 至少一个数据集用单仿真证明 `LOW_SUB_UNIVERSE_SHARPE` 可达 —— 6 颗 ACTIVE 全部 PASS（见反证表）
2. ~~或在非小宇宙结论下复测~~ —— TOP500 是本区唯一登记档（`src/wqb/config.py::REGIONS`），无更大档可换
3. ✅ 至少 1 波 S3 有 `backtest_results` 入库 —— 1410 行 / 126 波

## 复产前置（active 不等于能开波）

active 只解除入口限制，**不解决形态落差**。开波前须先回答方向性问题：
**如何在合规单信号形态（Mode B / `ts_scale` / 有经济含义的 `subtract(rank(A),rank(B))` / group_rank+zscore）下把 S 推到 1.7+？**
参考锚点：`other455` 纯复合已到 S 1.51（`O0NxWZMR` S1.51/F1.28/prod **0.4531** 干净），距 ladder 1.58 仅 0.07，
但撞 sub_universe 比值墙（0.24 vs limit 0.72，n2v 覆盖 97 股的结构性覆盖墙）。
**下一个应尝试的方向 = 把该类的覆盖问题与形态合规分开解决**（如换更宽覆盖的字段源 + 保持单信号形态）。

## priors
- 拥挤数据集 TOP3（避免重复挖）：techindi_model(alphaCount=1061, cov=0); analyst7(alphaCount=942, cov=0.72); model38(alphaCount=840, cov=0)
- 白空间候选（未测 + 覆盖≥60% + 低 alphaCount）：model53(cov=0.87, alphaCount=0); model28(cov=0.84, alphaCount=0); news20(cov=0.77, alphaCount=0); sentiment7(cov=0.74, alphaCount=0); analyst47(cov=0.62, alphaCount=0)
- 已判死（勿重试）：DEU-EMPTY-COVERAGE-S0-PICKS-20260923, DEU-FUNDAMENTAL6-PROBE-DEAD-20260923, DEU-INSIDER-TRX-MATRIX-CEILING-20260922, DEU-INSTITUTIONS1-PROBE-DEAD-20260923, DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923, DEU-PATTERN_SCORES-PROBE-DEAD-20261002, DEU-PV30-GROUP-ONLY-NOT-SIGNAL-20261002, DEU-TARGET10-STRUCTURAL-CEILING-20260923
- 实证笔记：DEU-M29-FWDDEV-SEED-20260916: discovered in D-wave; StarMine-style weighted vs consensus deviation; PROD corr pending | DEU-M110-SCORE-2FAIL-SEED-20260916: lowest failed_ra (2) among all D-wave seeds; second frontier-grade asset beside model109 blbYGJPq; corr pending
