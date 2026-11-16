# CAMPAIGN REPORT — DEU regular_tower（fundamental + insiders，2026-11-16）— 修订 v2

> **修订说明（v2，同文件路径）**：本版按独立审读意见修订。核心更正：① `tail` 是表达式算子，不是平台 `truncation` 设置；② 补齐全部门槛与三层闸的定义；③ 把"全闸"降级为"RA 层全过（failed_ra_count=0）"，明确它不等于提交可用；④ 修正 w5 带宽行把 w4 的 1.62 误读为本波读数；⑤ 明确塔位点亮/倍率规则未在 ask 中定义，只做条件式计数预测；⑥ 修正"50 臂全部单数据集/effective=1"（w1 有 5 条双数据集/双塔件）；⑦ 补齐 D1–D6、CW、effective 等术语定义与出处。逐条对照见 §10。

- 范围：DEU/TOP500/D1；5 波 `rt-fundamental-w1` … `rt-fundamental-w5`，共 50 臂。
- 平台设置（DB payload 逐臂回读）：**neutralization=FAST（全 50 臂）**、decay=0、truncation=0.08、nanHandling=ON、maxTrade=OFF、FASTEXPR；平台回显窗口 `startDate=2014-01-01`、`endDate=2023-12-31`。
  - 窗口与 `tracking/DEU/config/settings.json:16-17`（2013-01-01 起）不同；`create_multi_simulation` 无 startDate/endDate 参数（`world-quant-brain-mcp/tools_sim.py:672-690`），本报告原样记录平台值。
  - **本 run 未扫中性化**：50 臂全为 FAST。ask 未给出塔位对中性化的具体要求，本报告不假设。表达式里的 `sector` / `industry` / `subindustry` 是 `group_rank` 的**信号内分组轴**，不是平台中性化设置。
- 证据来源：① ask 给定的塔位实读（`campaign_intel.py pyramid`，平台 `get_pyramid_alphas` 当季实读）；② 本 run 5 波 `wave_results`（DB id 2206/2207/2208/2209/2210，`status=closed`、`source_file=pipeline:auto`）；③ 5 份波次档案 `tracking/DEU/regular_tower/WAVE_rt-fundamental-w{1..5}_20261116.md`；④ 各波 DB 只读回读（`backtest_results` 行、`payload_json.checks/ra/pyramids/settings`、`alphas` 列）；⑤ `src/wqb/config.py:393-401`（RA 18 项）、`tracking/DEU/config/thresholds.json`。
- **声明**：本报告零平台调用、零提交。所有"计数/倍率"均为**条件式预测**；**未提交，不能写"已点亮"**。点亮与倍率规则见 §1/§4.1 的未定义声明。

## §0 术语定义（先读）

| 术语 | 定义 | 出处/说明 |
|---|---|---|
| `truncation=0.08` | 平台设置项（每臂 settings 一致） | DB `payload.settings.truncation` |
| `tail(x, lower, upper, newval=0.5)` | **表达式算子**：把截面上低于 lower 分位/高于 upper 分位的值设为 newval；例 `tail(group_rank(...), lower=0.08, upper=0.92, newval=0.5)` | 各波 expressions 原文（DB `expressions` 表）；与平台 `truncation` 是两个对象 |
| `effective` | 平台 `pyramids.effective`：该 alpha 归属的塔数量；1=单塔，2=双塔 | DB `payload.pyramids.effective` |
| `atom_n_datasets` | 表达式引用的数据集个数；1=单集件，2=多数据集件 | DB `expressions.atom_n_datasets` |
| 族峰 1.50 | 本报告指 `fundamental72` 的「EBIT/oper_inc ÷ total_asset 三窗 delta×ts_rank×group_rank 动量族」在本次所引档案中的最高 S；**不是平台全历史** | `tracking/DEU/regular_tower/S0_TOWER_SCAN_20261115.md:119,153`（mLaALJX2 S 1.50/唯一 fail LOW_SHARPE 差 0.08）、`tracking/DEU/atom_orthogonal/NEARGATE_BREAK_GRID_FND72_20261115.md:33,46` |
| 0.05 塌陷 | 同核带宽 0.05 时 S 1.31/F 0.82，较 0.08 的 1.54/1.03 大幅下降（w4 臂1） | `tracking/DEU/regular_tower/WAVE_rt-fundamental-w4_20261116.md` §1/§3；DB 读数 |
| 机制探针 | 单腿、单臂的机制验证（H9/H3/H4/H5/H2），不与现有载体做多腿复合 | w5 档 §3.2；ask 臂表 |
| 三年窗三腿 | `multiply(rank(ts_delta(p,240)), rank(ts_delta(p,176)), ts_rank(p,1008))`，p=EBIT 或 oper_inc ÷ total_asset；外层 `group_rank(..., sector)` | w1–w4 expressions 原文 |
| CW | 平台 RA 检查 `CONCENTRATED_WEIGHT`（集中度）；平台 limit=0.1（ask 实读 zqdQqNG1/3q0gZE0N），本地 `thresholds.json:20` 的 0.5 只是 review 线 | ask 判读基准；DB `payload.checks` |
| 差 1 颗 / 差 2 颗 | ask 塔位字段 `need` 的直接读数（alphas 到 3 还差几颗） | ask 塔位快照 |

## §1 塔位现状与优先级判断

塔位快照（ask 给定，`campaign_intel.py pyramid` / `get_pyramid_alphas` 当季实读）：

| 塔 | alphas | need（差几颗） | mult | lit | 本 run 优先级 |
|---|---:|---:|---:|:---:|---|
| **fundamental** | **2** | **1** | **1.8** | false | **P0（目标塔；唯一差 1 颗）** |
| **insiders** | **1** | **2** | **1.6** | false | **P1（目标塔；本 run 零候选）** |
| sentiment | 1 | 2 | 1.8 | false | P2（非目标；差 2 塔中倍率最高） |
| institutions | 1 | 2 | 1.6 | false | P2（非目标） |
| news | 0 | 3 | 1.8 | false | P3 |
| option | 0 | 3 | 1.7 | false | P3 |
| pv | 0 | 3 | 1.6 | false | P3 |
| earnings | 0 | 3 | 1.5 | false | P3 |
| macro | 0 | 3 | 1.5 | false | P3 |
| risk | 0 | 3 | 1.5 | false | P3 |
| socialmedia | 0 | 3 | 1.5 | false | P3 |
| imbalance | 0 | 3 | 1.2 | false | P3 |
| analyst | 6 | 0 | 1.8 | true | ask 快照 lit=true |
| model | 3 | 0 | 1.8 | true | ask 快照 lit=true |
| other | 3 | 0 | 1.8 | true | ask 快照 lit=true |
| shortinterest | 5 | 0 | 1.3 | true | ask 快照 lit=true |

**优先级判断**：
1. **fundamental：差 1 颗、mult 1.8、目标塔**——唯一"再 1 颗即达到 3 颗"的目标塔，P0。
2. **insiders：差 2 颗、mult 1.6、目标塔**——本 run 的 8 条 insiders 相关臂全部弱（§4.4），本 run 增量为 0；P1，但对本 run 无贡献。
3. **sentiment（差 2、1.8）/ institutions（差 2、1.6）** 是非目标中最近的；sentiment 倍率与 fundamental 同级，若扩塔应排在 0/3 塔之前。
4. **0/3 的 8 座塔**距 3 颗，本 run 未触达。
5. **配对/禁混预算**：ask 给定 `trio 组腿已用 0/5`；本报告未在 DB/文件中独立复核该计数，也无 trio 组合/双塔混用臂。

⚠ **`mult` 与 `lit` 的语义未在 ask 中定义**：`mult` 是否乘在 alpha、整塔或其他对象、从何时生效、持续多久，ask 未给；`lit` 计入哪个状态（SUBMITTED / ACTIVE / OS）ask 也未给。本报告只照录数值，**不将其解释为收益乘数或已生效倍率**。

## §2 本 run 波次与判定

| 波 | 臂数 | 结构构成 | best S（alpha） | best 2Y（alpha） | 波级判定（DB id） |
|---|---:|---|---|---|---|
| `rt-fundamental-w1` | 10 | 5 单集/单塔（arms1/2/3/8 为 FUNDAMENTAL + arm10 为 INSIDERS，effective=1）+ **5 双集/双塔**（arms4/5/6/7/9，effective=2）；0 条 tail | **1.45**（Xgal7eEb） | **1.96**（LLKX7rxL） | **PARTIAL**（2206） |
| `rt-fundamental-w2` | 10 | 10 单集/单塔；1 条 tail（臂7=0.12） | **1.52**（YPak9o6q） | **2.33**（d5a7PrpK） | **PARTIAL**（2207） |
| `rt-fundamental-w3` | 10 | 10 单集/单塔；2 条 tail（臂9=0.10、臂10=0.15） | **1.56**（O0WmdbPR） | **2.41**（O0WmdbPR） | **PARTIAL**（2208） |
| `rt-fundamental-w4` | 10 | 10 单集/单塔；**10 条 tail**（0.05/0.08×2/0.09/0.10×4/0.11/0.12） | **1.62**（kqamAeRg） | **2.56**（wpozrXV5） | **PASS**（2209） |
| `rt-fundamental-w5` | 10 | 10 单集/单塔；2 条 tail（臂1=0.06、臂2=0.07） | **1.54**（RRekRZnz） | **2.39**（3q0nqYbN） | **PARTIAL**（2210） |

- **合计**：50 臂 → **1 个波级 PASS（w4）+ 4 个 PARTIAL**；无 FAIL 波。
- **塔构成补充**：w1 = 5 双塔（INSIDERS+FUNDAMENTAL）+ 4 单 FUNDAMENTAL + 1 单 INSIDERS；w2 = 8 单 FUNDAMENTAL + 2 单 INSIDERS；w3–w5 全部单 FUNDAMENTAL。全 run 的 insiders 相关臂共 8 条（w1 6 + w2 2）。
- **波级判定定义**（`src/wqb/wave_results_contract.py:79-90`，`verdict_from_counts` :84-90）：PASS = 本波 ≥1 条候选过 RA 层全部检查（failed_ra 空且 S≥1.58 等）；PARTIAL = 0 达标但 ≥1 近闸；FAIL = 0 达标 0 近闸。
  - **"波级 PASS"与"臂级 RA 层全过"是两个层级**：w4 的波级 PASS 仅因 `kqamAeRg` 的 `ra.failed_ra_count=0`；它不表示该 alpha 已过提交前置、也不表示可提交。
- **w5 行的 0.08=1.62 不是 w5 臂**：w5 只补了 0.06/0.07 两臂（S 1.37/1.53）；0.08=1.62 是 **w4 `kqamAeRg`** 的跨波对照值，0.10=1.56 是 w4 `WjlX5KkN`，0.12=1.51 是 w4 `2r5ZYPE6`。这些值**不计入 w5 的 best S（1.54）**；本报告在 §4.2 单独列带宽曲线并标注归属。
- **tail 逐波取值（回答"其余臂是多少"）**：全 run **15/50 臂带 tail，35/50 臂不带 tail**；逐波见上表。`truncation=0.08` 是平台设置，**全 50 臂一致**，与 tail 带宽无关。
- **数据集终态（ask 原文照录）**：`["（本 run 无数据集终态变更）"]`。该字面是含一句中文的单元素数组，来自 ask 的 `数据集终态` 字段，本报告不做工具 schema 解释。
  - 逐波判读：fundamental72 在 w1 档为 provisional，w2 起为 active 并维持至 w5；这是**波级判读档位**变化，不是 dead/capped/data_excluded 终态变更。
  - insiders1：本 run 未判死、未 data_excluded；w1 有 6 条 insiders 相关臂、w2 有 2 条（合计 8 条），w3–w5 无 insiders 臂；全部弱/CW 挂（§5.3）。

## §3 门槛全表与三层闸

### 3.1 全部门槛（本 run 使用的判据）

| 轴 | 门槛 | 出处 |
|---|---|---|
| S | **≥1.58** | `tracking/DEU/config/thresholds.json:3` / `:14`；平台 `LOW_SHARPE` limit 实读 1.58 |
| F | **≥1.0** | `thresholds.json:4` / `:15`；平台 `LOW_FITNESS` limit 1.0 |
| 2Y（单集件） | **≥1.58**（`LOW_2Y_SHARPE`） | `thresholds.json:5` `two_year_sharpe_min: 1.58`；平台 checks 实读 limit 1.58 |
| 2Y（多数据集件） | **≥1.58**（`IS_LADDER_SHARPE`，limit 1.58 / year=2） | ask 判读基准；`s2_nearmiss_rescue_20261104.md:3448-3460`（ask 引用）；本 run w1 5 条多集件三处一致（DB `is_ladder_sharpe`=checks 值） |
| sub | 本地 review 线 **≥1.0**；平台 `LOW_SUB_UNIVERSE_SHARPE` limit **动态**（本 run checks 实读 0.61/0.69/0.37/0.39/0.15；ask 另给全局实测 0.56） | `thresholds.json:21`；各波 `payload.checks.fail` |
| TO | **0.01–0.70** | `thresholds.json:8-9` / `:16-17` |
| margin | **≥0.0005 = 5bp** | `thresholds.json:7` `margin_min: 0.0005` |
| CW | 平台 limit **0.1**；本地 `concentrated_weight_max: 0.5` 只是 review 线 | ask 实读（zqdQqNG1 value 0.5/limit 0.1；3q0gZE0N 0.25/limit 0.1）；`thresholds.json:20` |
| prod/self corr | **≤0.70** | `thresholds.json:18-19`（self_corr_max/prod_corr_max 0.7）；`src/wqb/config.py:502` `PRODCORR_CEILING = 0.70`；ask 判读基准 |
| RA 检查集 | **18 项**：HIGH_TURNOVER / LOW_TURNOVER / LOW_FITNESS / LOW_RETURNS / LOW_SHARPE / LOW_GLB_AMER_SHARPE / LOW_GLB_APAC_SHARPE / LOW_GLB_EMEA_SHARPE / LOW_ASI_JPN_SHARPE / IS_LADDER_SHARPE / LOW_2Y_SHARPE / LOW_SUB_UNIVERSE_SHARPE / LOW_ROBUST_UNIVERSE_SHARPE / LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE / LOW_INVESTABILITY_CONSTRAINED_SHARPE / LOW_ROBUST_UNIVERSE_RETURNS / CONCENTRATED_WEIGHT / LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO | `src/wqb/config.py:393-401` |
| 失败判定 | result 既非 PASS 也非 PENDING 即算失败（WARNING/ERROR 也算） | `src/wqb/config.py:410-412`；AGENTS §8.7 |

- **`ra_failed_count` / `ra.failed_ra_count` / `ra_failed_checks` 的关系**：平台 payload 的 `ra.failed_ra_count`（计数）与 `ra.failed_ra_checks`（名单）是同一 `ra` 块的两个字段；落库到 `backtest_results.ra_failed_checks` 列的是名单。本报告中的 `ra_failed_count` 是 `ra.failed_ra_count` 的缩写，**不是第三个独立列**。
- **checks 表示不一致**：多波出现 `checks.fail=[]` 但 `ra.failed_ra_count>0`，对应 LOW_SHARPE/LOW_FITNESS/LOW_2Y 落在 `checks.warning` 带 value/limit。按 `src/wqb/config.py:410-412`（WARNING 算失败）与 AGENTS §8.7，本报告以 `ra_failed_checks` 判定；只看 `checks.fail` 会高估通过数。
- **`pending` vs `null`**：平台 body 的 `SELF/PROD/DATA_DIVERSITY` 状态为 **pending**（平台未返回结果，见 ask w4 行）；本地 `alphas.prod_correlation/self_correlation` 为 **null**（未落库读数）。两者是不同层：pending 是平台状态，null 是本地列状态；本报告不把 null 当作"已测且为 0"。

### 3.2 三层闸（不要把三层混成"全闸"）

| 层 | 内容 | `kqamAeRg` 现状 |
|---|---|---|
| **L1 RA 层** | 平台 18 项 RA 检查（§3.1） | **`ra.failed_ra_count=0`（RA 层全过）**；`MATCHES_COMPETITION`/`MATCHES_THEMES` 是 warning，不属 RA 18 项 |
| **L2 提交前置** | SELF / PROD / DATA_DIVERSITY 平台状态；prod/self corr≤0.70；年度分年 2018–2020；项目五道闸（台账排除 / RA+塔位 / 近十年 / self-corr / 篮内互相关+塔位配额） | **未完成**：SELF/PROD/DATA_DIVERSITY pending；prod/self 未测；年度分年未取；五道闸未逐条跑（RA 读数来自 harvest 的 `ra` 块，尚未用 `batch_get_alpha_metrics`+`get_alpha_details` 复核） |
| **L3 用户确认** | 用户明确确认 + `workflow_submit_alpha(confirm_submit=True)` | **未发生**；本报告不提交 |

⇒ 本报告统一写 **"RA 层全过（failed_ra_count=0）"**，不写无修饰的"全闸通过"。

### 3.3 `kqamAeRg` 逐项核对（可复核）

| 轴 | 读数 | 门槛 | 判定 |
|---|---:|---|---|
| S | 1.62 | ≥1.58 | ✅ |
| F | 1.12 | ≥1.0 | ✅ |
| 2Y | 2.54 | ≥1.58（单集件 LOW_2Y） | ✅ |
| sub | 1.16 | ≥1.0 本地线；平台 LOW_SUB 无 fail | ✅ |
| TO | 17.40% | 0.01–0.70 | ✅ |
| margin | 9.48bp（0.000948） | ≥5bp | ✅ |
| CW | checks 无 CONCENTRATED_WEIGHT fail | ≤0.1（平台） | ✅ |
| CLUSTER / LOW_TURNOVER / HIGH_TURNOVER / MATCHES_PYRAMID | 均 pass | — | ✅ |
| SELF / PROD / DATA_DIVERSITY | pending | — | ❓未测 |
| 年度分年 | 未取 | 2018–2020 判定见 §5.2 | ❓未测 |
| 五道闸 | 未逐条跑 | — | ❓未做 |

## §4 候选与计数预测（未提交；点亮规则未定义）

### 4.1 本 run 唯一 RA 层全过件（50 臂中唯一；不等于平台全历史唯一）

| alphaId | 波 | S | F | 2Y | sub | TO | margin | RA | 塔位 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **kqamAeRg** | w4 臂9 | **1.62** | **1.12** | **2.54** | **1.16** | 17.40% | 9.48bp | **`ra.failed_ra_count=0`** | `DEU/D1/FUNDAMENTAL` ×1.8（effective=1，单集件） |

- **计数预测（条件式）**：ask 的 fundamental 塔为 `alphas=2, need=1`。**若**该 alpha 被计入 fundamental 的 `alphas` 计数，则计数将由 2 变 3、`need` 由 1 变 0。是否计入（SUBMITTED / ACTIVE / OS 哪个状态）、何时计入，**ask 未定义**，本报告不臆测。
- **倍率**：`mult=1.8` 是 ask 字段；作用对象（该 alpha/整塔/其他）、生效时间与持续期**ask 未定义**，本报告不将其乘入任何收益或分数预测。
- **不写"已点亮"**：未提交、未确认、前置未完成 ⇒ 只能说"若被计入，计数条件式变化"，**不能说已点亮**。
- **前置未完成（因此不是可确认提交候选）**：
  1. SELF/PROD/DATA_DIVERSITY pending；
  2. prod/self corr≤0.70 未测；
  3. 年度分年 2018–2020 未取（判定规则见 §5.2）；
  4. 五道闸未逐条跑（含 self-corr、篮内互相关、塔位配额）；
  5. 无用户确认。

### 4.2 带宽曲线（回答 w5 的 1.62 归属）

**EBIT 核同核单变量，跨 w4/w5**：

| 带宽 | 归属 | S | F | 2Y | sub | TO | DD | margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 0.06 | **w5 臂1** oma9mwpE | 1.37 | 0.87 | 2.14 | 1.08 | 17.39% | 7.15% | 8.12bp |
| 0.07 | **w5 臂2** 3q0nqYbN | 1.53 | 1.02 | 2.39 | 1.10 | 17.43% | 6.72% | 8.98bp |
| **0.08** | **w4 臂9** kqamAeRg | **1.62** | **1.12** | **2.54** | **1.16** | 17.40% | 6.15% | 9.48bp |
| 0.10 | w4 臂8 WjlX5KkN | 1.56 | 1.05 | 2.30 | 1.04 | 17.30% | 7.14% | 9.14bp |
| 0.12 | w4 臂10 2r5ZYPE6 | 1.51 | 1.00 | 2.17 | 1.00 | 17.13% | 6.94% | 8.85bp |

- **结论**：0.06→0.07→0.08 上升，0.08→0.10→0.12 下降 ⇒ **0.08 是已测区间的内点峰（两侧均已补测）**；0.06 相对 0.08 塌陷（S −0.25/F −0.25）。
- **归属提醒**：本表是跨波曲线；**w5 只产出 0.06/0.07 两臂**，0.08/0.10/0.12 是 w4 读数。w5 的 best S 仍是 1.54（RRekRZnz），不是 1.62。

### 4.3 非 PASS 备胎清单（S≥1.5，完整列出；不是 ≤2 near 候选表）

| 波 | alphaId | S | F | 2Y | sub | RA 层 fail（DB `ra_failed_checks`） |
|---|---|---:|---:|---:|---:|---|
| w2 | YPak9o6q | 1.52 | 1.05 | 1.67 | 0.98 | LOW_SHARPE |
| w2 | d5a7PrpK | 1.51 | 1.00 | 2.33 | 1.14 | LOW_SHARPE |
| w3 | O0WmdbPR | 1.56 | 1.05 | 2.41 | 1.18 | LOW_SHARPE |
| w3 | 88N6Wa9W | 1.53 | 1.02 | 2.10 | 1.09 | LOW_SHARPE |
| w4 | WjlX5KkN | 1.56 | 1.05 | 2.30 | 1.04 | LOW_SHARPE |
| w4 | omazdQeE | 1.55 | 1.04 | 2.27 | 1.21 | LOW_SHARPE |
| w4 | qM7zReZj | 1.54 | 1.03 | 2.47 | 1.21 | LOW_SHARPE |
| **w4** | **wpozrXV5** | **1.54** | **1.03** | **2.56（本 run 最高 2Y）** | **1.21** | LOW_SHARPE |
| w4 | 2r5ZYPE6 | 1.51 | 1.00 | 2.17 | 1.00 | LOW_SHARPE |
| w5 | RRekRZnz | 1.54 | 1.07 | 1.39 | 1.12 | LOW_SHARPE + LOW_2Y |
| w5 | 3q0nqYbN | 1.53 | 1.02 | 2.39 | 1.10 | LOW_SHARPE |

- 入选标准：本 run 全部 **非 PASS 且 S≥1.5** 的臂（共 11 条：w2 2 + w3 2 + w4 5 + w5 2）。本表不是"每波 ≤2 near 候选"表；各波 near 候选按判定表最多 2 条，已在各波档。`wpozrXV5`/`qM7zReZj` 在 w4 的 S 排序中分别排第 4/第 3（不是该波 near 前 2），因 2Y 2.56/2.47 而在此完整列出。
  - *更正*：初版表漏列 `wpozrXV5` 与 `qM7zReZj`；本版补全。
- **用途**：若 `kqamAeRg` 前置失败，这些是后备研究件；**它们本身 RA fail≥1，塔位计数预测=0**。

### 4.4 insiders 塔增量预测

- 本 run 的 insiders 相关臂共 **8 条**（w1 6 条：arms4/5/6/7/9 双塔 + arm10 单 insiders；w2 2 条：arms9/10 单 insiders）。
- 最佳读数：`mLazj129`（w1）S 0.83/F 0.33/2Y 0.78/CW 0.1447；`3q062vbZ`（w2）S 0.82/F 0.33/2Y 0.94/CW 0.1447；`P05lAmWq`（w2）S 0.32/F 0.09/2Y 0.43/sub −0.03；其余 0.30–0.79。
- 全部 RA fail≥1、全部 CW 挂或弱；**无近闸、无 RA 层全过** ⇒ **insiders 塔计数预测 = 0**。
- **不判死**：insiders1 本 run 未做宽度修复后的单变量对照，FIELD 档既有 `Δ66` 先验（S 1.72，`deu-insiders-evidence.md:31`，vec_avg+132 口径）与本 run `vec_sum+250` 口径差 0.89，**未解析**；按探针条款 + D1 未达，不判死、不 data_excluded。

### 4.5 `CW 0.1447` 的说明

- CW = `CONCENTRATED_WEIGHT`；平台 limit 0.1；0.1447 > 0.1 ⇒ **挂闸**。
- `mLazj129`（w1，`vec_sum`+250 回填）与 `3q062vbZ`（w2，`vec_avg`+132 回填）**表达式不同，但 CW 读数逐位相同 0.1447（0.144689）**；这是 DB/平台实测读数，不是抄写。相同原因**未解析**（可能与子行业分组暴露/同一日期 2014-01-29 有关），本报告不作因果断言。
- **归因降级**：`insd1_holdings` 250 日宽度 193/500=38.6%（`FIELD_insiders1_20261115.md:108,125`）与 CW 挂**一致**，可登记为"数据层宽度假设"；但本 run 未做中性化/表达式单变量对照，**不能断言 CW 挂=数据层而非信号层/中性化问题**。

## §5 数据集终态与判死六维

### 5.1 终态

- ask 原文：`数据集终态：["（本 run 无数据集终态变更）"]`。本 run **无 dead/capped/data_excluded 终态转换**。
- 波级判读：fundamental72 w1=provisional → w2–w5=active（判读档位，不是终态）；insiders1 未判死、未 data_excluded（但本 run 无可推进结构）。

### 5.2 年度分年的判定规则

- `S0_TOWER_SCAN_20261115.md:178` 明写："2018/2019/2020 三年逐年 Sharpe 若仍全 <1.0、而总 S 靠 2021–2023 撑起 ⇒ 记时间集中度风险，不得按可提交推进（即使总 S 过线）"。
- **这是 ask 验收条/档案规则，不是平台 RA 18 项**；与五道闸里的"近十年"（要求每年 LC>0 且 SC>0，`S0_TOWER_SCAN:261`）是**两条不同判据**，本报告不混写。
- **本 run 未取 kqamAeRg 的年度分年**；`mLaALJX2` 的 2018 0.80 / 2019 0.80 / 2020 −0.35（`S0_TOWER_SCAN:130`）是**另一条表达式**的族级风险先验，只作提示，**不能代表 kqamAeRg**。

### 5.3 判死六维闸（D1–D6）

| 维 | 定义（AGENTS §7.6） | 本 run 现状 | 判定 |
|---|---|---|---|
| D1 结构互异模板 | ≥10 个不同经济机制/算子几何 | 名义机制标签 ~10–13（三窗动量乘/增量ROA/门控/insiders M2/M5/H9/H3/H4/H5/H2/分母 B/C），但多数为同一动量族的参数/壳层变体与单臂探针；**未做正式互异性审计** | **未达（保守）** |
| D2 字段族自测 | 每个可用字段族 ≥1 条实测 | 仅碰 6 个 fnd72 字段（oper_inc、ebit、tot_asset、net_income、sales_rev_turn、cogs_to_fe_and_pp_and_g）另加 2 个 insd1 字段（holdings、valueeur）；fnd72 共 **1031** 字段（`FIELD_fundamental72_20261115.md:13,30`）；无字段族穷尽审计 | **远未达** |
| D3 矩全家 | 水平 / 一阶差 / 二阶波动 / 比值或信噪比 各 ≥1 | 一阶差✓（δ240/δ176/δ66/δ252）、二阶波动✓（H9 `ts_std_dev`）、比值✓（多组）；**纯水平腿与信噪比未见** | **未达** |
| D4 分组轴 | ≥2 个 | sector（各波）、subindustry（w1/w2/w4）、industry（w3） | **达** |
| D5 非线性 | ≥1 条 | ts_rank、group_rank、reverse、tail、winsorize、ts_decay_linear | **达**（v1 漏写，本版补上） |
| D6 配置 | ≥2 套（宇宙×中性化×decay 至少变一维） | 本 run 仅 FAST/decay0/TOP500/D1；跨槽 SUBINDUSTRY 三波**不是本 run 读数** | **本 run 未达** |

⇒ **D4/D5 达，D1/D2/D3/D6 未达**；按 AGENTS §7.6 **不得判死、不得封集、不得作为邻接集先验**。

## §6 明确不做的

1. **不做提交 POST**：未调用 `workflow_submit_alpha(confirm_submit=True)`、`create_spc_submission`、`set_spc_submission_weight` 或 `/alphas/{id}/submit`。
2. **不消耗配额**：本报告步骤零平台调用、零仿真、零提交；5 波仿真已在前序执行，本步骤不重复。
3. **不做数据终态写动作**：无 `seal_dead_end`、无 dataset 状态改写；ask 的"无终态变更"照录。
4. **不取提交前置读数**：prod/self/data-diversity、年度分年、self-corr、互相关均未在本步骤查询。
5. **不做跨区外推**：未引用 TWN/KOR 经验作为 DEU 增益依据。

## §7 未覆盖与盲区

- **塔位快照**：直接采用 ask 给定的 `campaign_intel.py pyramid` / `get_pyramid_alphas` 当季实读，**本报告未重跑平台**；"当季"的具体时点/边界 ask 未给，塔位计数可能已变化（尤其 fundamental 2→3 临界）。若当前已是 3/3，本报告的目标前提需重核。
- **提交前置盲区**：`kqamAeRg` 的 SELF/PROD/DATA_DIVERSITY pending；50 臂 prod/self 全 null；年度分年 2018–2020 未取；符号指纹（翻符号对照）全 run 未测；五道闸未逐条跑 ⇒ **不能证明任何候选可提交**。
- **数据集层盲区**：w1 有 5 条双数据集/双塔件（arms4/5/6/7/9，effective=2，走 IS_LADDER，三处一致 5/5）；其余 45 臂单集件（走 LOW_2Y）。**不是"50 臂全部单数据集"**（v1 此句已更正）。fundamental72 只碰 6 个字段（远少于 1031）；D1/D2/D3/D6 未达，不判死、不封集。
- **insiders 盲区**：8 条 insiders 相关臂全部弱；w3–w5 无 insiders 臂；FIELD 档 `Δ66` S 1.72 先验与本 run 口径差 0.89 未解析；不判 insiders1 死，也不据此认定"insiders 机制死"。
- **表示不一致**：多波 `checks.fail=[]` 但 `ra.failed_ra_count>0`（LOW_SHARPE/LOW_FITNESS/LOW_2Y 在 warning 桶）；本报告以 `ra_failed_checks` 为准（`src/wqb/config.py:410-412`、AGENTS §8.7）；只看 `checks.fail` 会高估通过数。
- **工具限制**：`operator_audit` 对多语句表达式解析失败（w1/w2/w3/w4/w5 分别报 Unexpected character；位置 79/72 等），已按 error 登记、不作无解证据；展开单语句均 `safe=true`、ghost 列表不含本波算子。
- **日期窗**：平台回显 2014-01-01→2023-12-31，与 `tracking/DEU/config/settings.json:16-17` 的 2013-01-01 起不同；`create_multi_simulation` 无日期参数（`tools_sim.py:672-690`），原样记录平台值。
- **派发元数据缺口**：w3/w4 的 ask 未提供 multisim id/preflight/operator_audit/查重记录；w1/w2/w5 有部分记录。DB 中 50/50 臂有 `backtest_results` 行与 `expressions` 行（按波回读），但"DB 有行"不等于平台派发元数据完整；w3/w4 的缺口单独登记。
- **未做论坛取证 / 判死**：本 run 无 `forum_recon`、无 dead_end 封存；任何"某方向不可行"仅为本 run 读数，不是终判死。
- **MCP 直连仿真盲区**：已知"直连仿真不写本地 expressions 表"的通道盲区，对本 run 不构成主要风险（本 run 的臂均经 upsert 落库并可回读）；但本报告**没有**据此宣称平台侧元数据完整（w3/w4 缺口仍在）。

## §8 下一步建议（回答"继续开波还是先冻结"）

**建议：先冻结新开波，优先补 `kqamAeRg` 的提交前置；不要在本轮再开新 fundamental 波追第二个候选。** 理由：
1. fundamental 只差 1 颗，已有一个 RA 层全过件；在 prod/self/data-diversity/分年未验前继续开波，是"未确认第一个能否计入就先追第二个"，性价比低。
2. insiders 差 2 颗且本 run 8 条 insiders 臂全弱、`Δ66` 先验口径差未解析；现在开 insiders 波缺少可复用的正杠杆，应先做单变量宽度/口径修复（vec_avg+132 vs vec_sum+250、反号对照）再决定。
3. `kqamAeRg` 的前置补测项（按项目既有工具，**本报告不执行、不承诺配额**）：
   - prod/self：`check_self_correlation` / `check_correlation`（平台相关性接口；是否消耗仿真配额未在本报告核实）；
   - data-diversity：重读 `get_alpha_details` / checks 的 `DATA_DIVERSITY` 状态；
   - 年度分年：`get_alpha_yearly_stats("kqamAeRg")`，按 §5.2 的 2018–2020 规则判定；
   - 五道闸：`batch_get_alpha_metrics` + `get_alpha_details`（RA+塔位复核）、`check_self_correlation`、`compute_mutual_correlation`、塔位配额；
   - 最后才是用户确认 + `confirm_submit=True`（不可逆）。
4. 若 `kqamAeRg` 前置全过并由用户确认提交且被平台计入，再评估是否值得为 insiders 单开一波（差 2 颗、1.6 倍率）。

## §9 总结与待用户确认

- **塔位**：fundamental 2/3、差 1 颗、mult 1.8（ask 快照），是本 run 唯一差 1 颗的目标塔；insiders 1/3、差 2 颗、mult 1.6，本 run 8 条 insiders 臂全弱、无候选。
- **本 run**：5 波 50 臂，仅 w4 `kqamAeRg` 达到 **RA 层全过（failed_ra_count=0）**（S 1.62/F 1.12/2Y 2.54/sub 1.16/TO 17.40%/margin 9.48bp）；但 SELF/PROD/DATA_DIVERSITY pending、prod/self 未测、2018–2020 分年未取、五道闸未跑 ⇒ **不是可提交件，未提交**。
- **计数预测**：若 `kqamAeRg` 被平台计入 fundamental 的 `alphas`，则计数 2→3；计入状态、点亮判定与 `mult=1.8` 的作用对象/周期 ask 未定义，本报告不臆测、不写"已点亮"。
- 本 run **无正式待确认提交候选**（rollup：`[]`）。
- `kqamAeRg` 仅 **RA 层全过**；SELF/PROD/DATA_DIVERSITY pending、prod/self 未测、2018–2020 分年未取、五道闸未跑、点亮/倍率规则未定义 ⇒ **不进入提交确认**。上述前置完成后再由用户决定是否确认提交。

## §10 修订对照（独立审读意见 → 本版处理）

| 审读问题 | 本版处理 |
|---|---|
| tail 未定义、与 truncation 混淆 | §0 定义 tail 算子 vs 平台 truncation；§2 给出逐波 tail 清单（15/50 带 tail，35/50 不带） |
| 配置清单缺中性化 | §1 明确 neutralization=FAST 全 50 臂；sector/industry/subindustry 是信号内分组轴；塔位中性化要求 ask 未给 |
| RA 门槛全篇未给、三个名字混用 | §3.1 全门槛表 + 18 项 RA 清单 + `ra_failed_count`/`ra.failed_ra_count`/`ra_failed_checks` 关系 |
| "全闸"覆盖范围不清 | §3.2 三层闸表（RA 层 / 提交前置 / 用户确认）；全文改用"RA 层全过（failed_ra_count=0）" |
| 波级判定标准未定义、PASS 一词双关 | §2 引 `wave_results_contract.py:79-90` 定义；区分波级 PASS 与臂级 RA 层全过；明确波级 PASS≠可提交 |
| w5 行 0.08=1.62 冲突 | §2 注 + §4.2 表：1.62 属 w4 kqamAeRg；w5 best S 仍 1.54；逐值标归属 |
| 点亮/×1.8 规则未定义 | §1/§4.1 明确 ask 未定义计入状态与倍率作用对象/周期；只做条件式计数预测；不写"已点亮" |
| CW 未定义、0.1447 含义、两臂同值 | §0 定义 CW=CONCENTRATED_WEIGHT、平台 limit 0.1；§4.5 说明 0.1447 挂闸、两臂表达式不同但读数逐位相同、原因未解析 |
| effective/族峰/0.05 塌陷/机制探针/三年窗三腿无定义 | §0 逐项定义并给族峰出处（S0_TOWER_SCAN:119,153；NEARGATE:33,46） |
| D1–D6 只有标签、D5 缺席 | §5.3 给定义 + 逐维现状；D4/D5=达，D1/D2/D3/D6=未达 |
| "10/10 波"数量不符 | 全文改为"5 波 / 50 臂"；§7 明确 50/50 臂回读 |
| rollup 数组字面、pending vs null | §2 照录 ask 原文并说明是 ask 字段；§3.1 区分平台 pending 与本地 null |
| 备胎表漏 wpozrXV5、标准未写 | §4.3 改为"全部 S≥1.5 非 PASS 臂（11 条）"并补 wpozrXV5（2Y 2.56）与 qM7zReZj；注明不是 ≤2 near 表 |
| 未支撑断言：RA 全闸/全族唯一/点亮预测/PASS/族峰/trio/CW 归因/落库/1031/D1-D6/prod 0.70/分年/单数据集/effective | 逐条降级或补出处：RA 改"RA 层全过"且限本 run；"全族"改"本 run 50 臂"；点亮改条件式；PASS 引判定表；族峰补出处；trio 标 ask 给定未独立复核；CW 归因降级为假设；落库改 5/5 波 50/50 臂并保留 w3/w4 缺口；1031 补 FIELD 档行号；D1-D6 补定义/现状；prod 0.70 补 thresholds/config 行号；分年补 S0:178 并区分"近十年"；单数据集/effective 修正为 w1 5 双 + 45 单 |
