# USA Short Interest Regular Alpha 交付报告 · 2026-11-15

> **数据时点**：2026-11-16（本报告 MCP / 本地实读）；ask 前序平台读数时点见 §1.3 的 `[A]` 标注。
> **报告撰写**：2026-11-16｜**文件名日期**：20261115（任务指定，不是数据时点）。
> 战役：USA 固定 / TOP3000 / D1 / Short Interest（shortinterest 类别）regular alpha。
> 纪律：**只挖不提交**（`WQB_ALLOW_ALPHA_SUBMIT=False`；本报告不含任何提交动作，未调用 `workflow_submit_alpha` / `submit_verdict` / `POST /alphas/{id}/submit`）；并发每批恰好 2 条、波次按序；PV/MODEL/OTHER 不跨集组腿；一族一席；算子调用点 ≤15；ATOM 单数据集（`pyramids.list` 单段）。
> 归档：本文件 `output_report/USA_shortinterest_delivery_20261115.md`。

---

## 0. 交付结论

**可交付 alpha：0 颗（`可交付：[]`）。**

| 口径 | 数量 | 明细 |
|---|---:|---|
| 可交付（全闸通过 + 用户点名） | **0** | — |
| 本战役新增臂（3 波 × 2 条） | 6 | `leaRl3GO` / `kqaL0ZGl` / `ZYaWKlWQ` / `58Jqk6q1` / `0mPKMZ56` / `XgaY8ZM0` |
| 收割池 / 存量全闸读数 | 7 | `88R7JMxX` / `58EqmQEN` / `gJezNxjg` / `rKR8VZVo` / `6Xd3lqnL` / `A1VYRo2w` / `58E3agW1` |
| 其中平台塔段 = 单段 SHORTINTEREST | 2 | `gJezNxjg`（prod **0.8791**）、`rKR8VZVo`（prod **0.9592**）——均撞红线 |
| prod 严格 <0.7（PASS） | 2 | `6Xd3lqnL` **0.588**、`A1VYRo2w` **0.495** |
| prod PASS 且其余闸全过 | **0** | `6Xd3lqnL` 卡塔位 2 段 + invest_S/S **0.4188**；`A1VYRo2w` 卡 RA `LOW_SUB_UNIVERSE_SHARPE` + 近十年 |
| 塔位 USA/D1/shortinterest | **0/3** | 本次 `get_pyramid_alphas` 实读：USA D0=0、D1=0；点亮定义见 §6.3 |
| 本战役新增臂「近十年」 | **6/6 FAIL** | 6 条臂均有至少一个负年 pnl（§3.3）；因此**本战役 0 全闸、0 条可称「近闸」** |
| 字段级真未探集 | 1 | `shortinterest24`（`UNTESTED_COV_OK`，1 字段，cov 0.2573；未跑 longCount/shortCount 探针） |

### 0.1 八条关键判读（含对上一版结论的更正）

1. **prod 墙仍是主杀手**：7 颗存量里 5 颗 prod ≥0.79（0.7943 / 0.9088 / 0.8791 / 0.9592 / 0.8899）。严格 `max < 0.7` 才 PASS（`src/wqb/config.py:502` `PRODCORR_CEILING = 0.70`；prod 数值为本轮 `[M]` `get_alpha_by_id` 读取、检测来源 `[A]`，见 §1.3）。
2. **真正属于 shortinterest 塔的只有 2 颗**：`gJezNxjg`（`mean_loan_rate_main`，单段 SHORTINTEREST）与 `rKR8VZVo`（`loan_rate_volatility`，平台单段 SHORTINTEREST）；两者分别被 prod 0.8791 / 0.9592 硬拦。其余 4 颗是多塔组合，`A1VYRo2w` 是单段 RISK（**上一版把 5 颗都写成多塔，已更正**）。
3. **ATOM 单数据集是第二大杀手**：7 颗里 4 颗 `pyramids.list` 多段（`88R7JMxX` 3 段、`58E3agW1` 3 段、`58EqmQEN` 2 段、`6Xd3lqnL` 2 段）；`gJezNxjg` / `rKR8VZVo` / `A1VYRo2w` 单段。
4. **近十年 3/7 FAIL**：`58EqmQEN` 2014–2018 全零；`rKR8VZVo` 2020 pnl **−648,472**；`A1VYRo2w` 2014 全零 + 2021 pnl −30,346（本轮 `get_alpha_yearly_stats` 逐颗复核，§2.4）。
5. **self-corr 3/7 FAIL**：`58EqmQEN` **0.9082**、`58E3agW1` **0.8901**、`rKR8VZVo` **0.7411**；池规模正常（`full_os_pool_size=147`，pool 141，excluded 6），值不作废（`[A]`）。
6. **算子调用点 2/7 超 15**：`88R7JMxX` **20**、`58E3agW1` **18**（`wqexpr.op_count` 平台口径，`[A]`）。本地 toolkit gate 的 `MAX_OP_CALLS=10`（`Claude/skills/wq-brain-campaign-toolkit/scripts/_gate_expr_checks.py:114`，`:382-384` 在 `n_calls >= 10` 处 FAIL）与题面 ≤15 是两套口径，见 §7 第 10 条。
7. **美国可投资性闸另拦 3 颗**：`88R7JMxX` invest_S/S **0.1574**、`6Xd3lqnL` **0.4188**、`58E3agW1` **−0.0769**，均 <0.70（`Claude/skills/wq-brain-ra-usa/SKILL.md:98-105`；比值为 `investability_sharpe / sharpe`，可为负或 >1，不是百分比）。
8. **新增 6 臂的「近十年」全部 FAIL，上一版「1 近闸」结论作废**：`0mPKMZ56` 2016 pnl **−384,986**（S −1.14、DD 7.06%），`kqaL0ZGl` 有 9 个负年，`ZYaWKlWQ` / `58Jqk6q1` 各 7 个负年，`XgaY8ZM0` 2014/2018 负年，`leaRl3GO` 4 个负年（§3.3）。按与存量相同的「逐年 longCount>0 && shortCount>0 && pnl>0」判据，6 臂全部 FAIL。**仓库没有「近闸」的统一数值定义，本报告不再使用该词**；`0mPKMZ56` 只称「本战役 S/F 最高的臂」，不称「近闸」。

> ⚠ 对上一版「`6Xd3lqnL` 是唯一过 prod」的更正：`A1VYRo2w` 的 prod=0.495 也是 PASS。**本批 prod PASS 共 2 颗**；两颗都因其它闸不可交付。

---

## 1. 口径、术语与证据链

### 1.1 固定口径与设置

- region=**USA**（全程未切换）；universe=TOP3000；delay=1；instrumentType=EQUITY；category=**shortinterest**。
- **7 颗存量**的设置由本轮 `get_alpha_details` 实读（全部 `startDate=2014-01-01`、`endDate=2023-12-31`、`truncation=0.08`、`nanHandling=ON`、`maxTrade=OFF`、`pasteurization=ON`、`unitHandling=VERIFY`）：

| alpha | neutralization | decay | universe / delay |
|---|---|---:|---|
| `88R7JMxX` | REVERSION_AND_MOMENTUM | 5 | TOP3000 / D1 |
| `58EqmQEN` | SLOW_AND_FAST | 4 | TOP3000 / D1 |
| `gJezNxjg` | SLOW | 0 | TOP3000 / D1 |
| `rKR8VZVo` | INDUSTRY | 5 | TOP3000 / D1 |
| `6Xd3lqnL` | REVERSION_AND_MOMENTUM | 5 | TOP3000 / D1 |
| `A1VYRo2w` | SLOW | 20 | TOP3000 / D1 |
| `58E3agW1` | REVERSION_AND_MOMENTUM | 5 | TOP3000 / D1 |

- **本战役 6 条新臂**：`get_alpha_by_id` 实读 neutralization 全部 **SUBINDUSTRY**；decay=5、窗口 2014-01-01~2023-12-31 来自 ask 波次材料 `ceilingNote`（未用 `get_alpha_details` 逐颗复核 decay/窗口，标 `[A]`）。
- 类别卡默认设置是 SUBINDUSTRY / decay5 / 2013-01-01~2023-12-31（`Claude/skills/wq-brain-ra-usa/references/shortinterest.md:15-30`）。**7 颗存量并不使用类别卡默认设置**（中性化/decay 逐颗不同，窗口晚一年从 2014 起）；因此不能把这 7 颗当作「本战役口径下的新读数」。
- 阈值分层（本报告统一按以下落地，不再混用）：
  - **prod**：`max < 0.70`，任务硬红线、无豁免（`src/wqb/config.py:502`；`AGENTS.md §7.5`）。⚠ 仓库 `GATE_POLICIES` 另有 `prod_family` 3 天 waiver（`AGENTS.md §8.1.2`），但**本任务显式写「无豁免」**，本报告按任务更严口径执行，不把 `prod_family` waiver 当放行路径。
  - **USA 可投资性**：`invest_S/S ≥ 0.70`，本地闸，排在 `failed_ra_count==0` 之后、`submit_verdict` 之前（`Claude/skills/wq-brain-ra-usa/SKILL.md:98-105`）。
  - **TO**：题面 red line 写 `TO∈[0.03,0.70]`；USA review 观察带 0.05–0.30、地板 0.05。**0.05 是 review 地板，不是平台 RA limit**；低于 0.05 只标「review 地板未达」，不伪造 RA FAIL。
  - **CW**：`CONCENTRATED_WEIGHT` 是 RA 检查项（`src/wqb/config.py:393-407` 的 `RA_CHECK_NAMES` 含它）；本报告 7 颗的平台 `checks.pass` 均含该名（§2.4）。

### 1.2 术语表（全文统一，避免同词多义）

| 术语 | 本报告含义 |
|---|---|
| **ATOM / 塔位** | `pyramids.list` 只含 1 段（单数据集）。**不是**「金字塔点亮数」。 |
| **点亮** | 同塔**本自然季度累计 3 颗且三对互相关 <0.5**（`Claude/skills/wq-brain-ra-pipeline/SKILL.md:157`）。本报告 USA/D1/shortinterest 点亮数 = **0/3 颗**（0 颗 / 需要 3 颗）。 |
| **收割池** | `submit_ready` 表里的 `READY` 行；**不是**「本地 alphas 表 prod_clean 池」，后者在 §6.2 单列。 |
| **未探** | 数据集级：该集有字段目录、但没有任何回测证据（`UNTESTED_COV_OK`）。**不是**模板级 D1–D6 的「未穷尽」；模板级另称「六维未举证」。 |
| **RA / fRA** | `RA` = 平台 `checks.fail` 列表；`fRA` = `ra.failed_ra_count`。平台只把 result 非 PASS/PENDING 且属于 `RA_CHECK_NAMES` 的项计入（`src/wqb/config.py:393-407,441-446`）。 |
| **本地严格 RA 失败** | 按 `RA_CHECK_NAMES` 重算，WARNING/ERROR 计入（`check_counts_as_failed`）。**`CLUSTER_TEST` 不在 `RA_CHECK_NAMES`，所以它的 WARNING 不计 RA 失败**（§2.3）。 |
| **inv** | `investability_ratio = investability_sharpe / sharpe`；可负、可 >1；仅对 S>0 的件有提交意义。 |
| **risk_neut** | 平台 `risk_neutralized_sharpe`；本报告只引用 `[A]` 读数（`0mPKMZ56` 1.01、`ZYaWKlWQ` +0.74），不重算。 |
| **全闸** | 本报告列出的 RA+ATOM+op、近十年、self、prod、篮内互相关、inv、TO/CW 全部通过。**篮内互相关本轮 NOT RUN**，故严格说本报告没有「全闸」件。 |
| **「近闸」** | 仓库**没有统一数值定义**。本报告不使用该词作为判定；只写「本战役 S/F 最高的臂（仍 3 项 RA FAIL + 近十年 FAIL）」。 |

**几个只在 ask / 画像里出现、不是仓库统一阈值的词（看到即按此读）**：

- **「一族一席」**：同一经济机制/族只留 1 条提交候选；本文用它约束「同族变体不重复占席位」，不是平台规则。
- **「不跨集组腿」**：PV / MODEL / OTHER 内部及两两之间不组腿；与其它 category 组腿合计 ≤5（任务红线）。**塔位配额** = 单两塔组合 ≤3 / trio×非trio ≤5 / trio 内部禁混（任务红线）；本报告篮内 NOT RUN，故未计数。
- **「0.5 噪声带」**：ask 预注册的 `|S| < 0.5 ⇒ 证伪` 线；**不是**仓库统一阈值，本报告只用于转述 H4 / F2 的预注册判据。
- **「继续线 <1.0」**：ask 对 F2 的预注册继续阈值（|S|<1.0 不继续）；**不是**仓库统一阈值。
- **`valueScore`**：平台数据集元数据（覆盖度/使用量等综合分），**不是信号强度**；本报告只作定位，不作判死依据。
- **`PPA`**：平台 `PPA_CHECK_NAMES` 的 7 项检查（`src/wqb/config.py` 的 `PPA_CHECK_NAMES`）；`ppa_failed` 只表示平台该组检查有失败，不等同 RA 失败。

### 1.3 证据分级（每处读数都带来源）

- **`[M]` 本报告实测（2026-11-16）**：`mcp__wq-brain-http__batch_get_alpha_metrics`（13 ids，`total=13 success=13 failed=0`）；`mcp__wqb-db__get_alpha_by_id`（7 存量 + 6 新臂）；`mcp__wq-brain-http__get_alpha_details`（7 存量，取 settings / checks / pyramids）；`mcp__wq-brain-http__get_alpha_yearly_stats`（7 存量 + 6 新臂，全 13 颗逐年）；`mcp__wq-brain-http__get_pyramid_alphas`；`mcp__wqb-db__get_submit_ready`；`mcp__wqb-db__list_wave_results`；`mcp__wqb-db__get_campaign_summary`；`mcp__wqb-db__get_salvage_pool`；`wc -l` / `md5sum` / `sha256sum`；`pytest tests/ -x`；`pytest tests/unit/07_docs_skills -q`；`tools/sync_skills.py --check`；`tools/code-audit/repo_governance_check.py`；`tools/code-audit/doc_path_refs.py`；`tools/waiver.py list --region USA`。
- **`[A]` ask 材料的前序平台读数（2026-11-15/16）**：7 颗的 **self** 与 `correlation_busy`/重试记录、`0mPKMZ56` 的逐年、dedup 聚合体、波次 batch 结果、覆盖审计命令与退出码。**本报告没有重跑 `check_correlation` / `check_self_correlation`**；`get_alpha_details` 不返回 prod/self 数值（只返回 `checks.pending` 含 `PROD_CORRELATION`）。⚠ **prod 数值同时出现在本轮 `[M]` `get_alpha_by_id.prod_correlation`（7/7 有值）与 `[A]` 的平台 note，二者一致**；本报告在逐颗明细里标 `[A]`，指的是**检测来源是前序 `check_correlation`，不是本轮重跑**。**self 只有 `[A]`，本轮没有任何 self 实测。**
- **`[H]` 历史台账 / 画像**：`88RKbpGl` 的 prod=0.7908（记录 2026-10-31）、`shortinterest3` wave329–337 判死、`USA-LOANRATE-FAMILY-DEAD` 等。

### 1.4 本轮未执行 / 不代填

- **未重跑** `check_correlation` / `check_self_correlation`：**self 是 `[A]`**；**prod 数值是 `[M]` `get_alpha_by_id` 读取、检测来源是 `[A]`**——两者都不是本轮 `check_correlation` 的重新计算。`gJezNxjg` 的 `correlation_busy → sleep 122 → 0.8791` 是 `[A]` 记录的前序会话过程，不是本轮动作。
- **未做篮内互相关**：ask 没有「已确认候选」篮内清单；`docs/ledger_keys.json` grep `basket|submit_ready` 命中 0（ask 实跑）；塔位配额（两塔≤3 / trio×非trio≤5 / trio 内部禁混）同因无篮无法计数 → **NOT RUN**。
- **未跑 longCount/shortCount 数据探针**（`tools/probe/dataset_data_probe.py`）⇒ 没有 `NO_DATA` 判定，`shortinterest24` 持仓有无仍为未知。
- **未跑全 region 覆盖审计**：ask 记录 `audit_dataset_coverage.py --region USA ...` 停在 20/286（平台 429 退避），约 45 分钟后被 TaskStop；该轮不产出替代结论。
- **未下发仿真 / 未提交**：本报告为交付/审计文档，自身零仿真、零提交；波次仿真见 §3 的 3 个 batch id。
- **preflight_expressions 回执**：ask 波次材料只给 `op_count.py` 实测与平台接受证据，未附逐波 preflight 回执；本报告不代填「已跑」，本轮自身未下发表达式故未触发该前置。

---

## 2. 全闸读数（7 颗存量，逐闸）

> 指标列 = `[M]` `batch_get_alpha_metrics`；settings / checks / pyramids = `[M]` `get_alpha_details`；近十年 = `[M]` `get_alpha_yearly_stats`；prod = `[M]` `get_alpha_by_id.prod_correlation`（检测来源为 `[A]` 前序 `check_correlation`）；self = `[A]`。`invest_S/S` = `investability_ratio`。

### 2.1 指标与设置总表

| alpha | 塔段 | S | F | TO | 2Y | SUB | invest_S/S | margin | returns | drawdown | long/short |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `88R7JMxX` | **RISK+INSIDERS+OTHER 3 段** | 3.43 | 3.02 | 0.2496 | 3.69 | 1.72 | **0.1574** | 0.001546 | 0.1929 | 0.0564 | 1510 / 1616 |
| `58EqmQEN` | **INSTITUTIONS+RISK 2 段** | 2.52 | 1.85 | 0.1256 | 2.77 | 1.66 | 0.8889 | 0.00108 | 0.0678 | 0.0273 | 1578 / 1559 |
| `gJezNxjg` | **单段 SHORTINTEREST** | 1.90 | 1.80 | 0.1158 | 2.92 | 0.96 | 0.7526 | 0.001943 | 0.1126 | 0.1523 | 1900 / 1225 |
| `rKR8VZVo` | **单段 SHORTINTEREST** | 1.86 | 2.44 | 0.0355 | 2.88 | 0.93 | 0.8441 | 0.01212 | 0.2149 | 0.3603 | 2372 / 751 |
| `6Xd3lqnL` | **RISK+OTHER 2 段** | 1.60 | 1.02 | 0.0866 | 2.20 | 0.76 | **0.4188** | 0.001173 | 0.0508 | 0.0596 | 1790 / 1335 |
| `A1VYRo2w` | **单段 RISK** | 2.24 | 1.42 | 0.0505 | 2.19 | 0.35 | 0.9286 | 0.00198 | 0.05 | 0.0486 | 1496 / 1633 |
| `58E3agW1` | **RISK+INSIDERS+OTHER 3 段** | 2.34 | 1.96 | 0.0969 | 2.83 | 1.21 | **−0.0769** | 0.001817 | 0.088 | 0.067 | 1346 / 1779 |

### 2.2 闸门总表

| alpha | 平台 RA `checks.fail` / fRA | 本地严格 RA（RA_CHECK_NAMES） | 塔位 ATOM | op ≤15 | 近十年 | self | prod | inv ≥0.70 | TO vs 0.05 地板 | CW | 篮内 | 结论 |
|---|---|---|---|---|---|---:|---:|---|---|---|---|---|
| `88R7JMxX` | `[]` / 0 | 0 | **FAIL（3 段）** | **20** | PASS（10/10 正） | 0.2431 PASS | **0.7943 FAIL** | **0.1574 FAIL** | 0.2496 PASS | pass | NOT RUN | 不可交付 |
| `58EqmQEN` | `[]` / 0 | 0 | **FAIL（2 段）** | 11 | **FAIL（2014–2018 零）** | **0.9082 FAIL** | **0.9088 FAIL** | 0.8889 PASS | 0.1256 PASS | pass | NOT RUN | 不可交付 |
| `gJezNxjg` | `[]` / 0 | 0 | PASS | 6 | PASS（2020 仅 9,661） | 0.2823 PASS | **0.8791 FAIL** | 0.7526 PASS | 0.1158 PASS | pass | NOT RUN | 不可交付（仅 prod 卡） |
| `rKR8VZVo` | `[]` / 0 | 0 | PASS | 6 | **FAIL（2020 −648,472）** | **0.7411 FAIL** | **0.9592 FAIL** | 0.8441 PASS | **0.0355 未达** | pass | NOT RUN | 不可交付 |
| `6Xd3lqnL` | `[]` / 0 | 0 | **FAIL（2 段）** | 9 | PASS（min 176,520） | 0.2996 PASS | **0.588 PASS** | **0.4188 FAIL** | 0.0866 PASS | pass | NOT RUN | 不可交付（塔位 + inv） |
| `A1VYRo2w` | **`LOW_SUB_UNIVERSE_SHARPE` 0.35<0.97** / 1 | **1** | PASS（单段 RISK） | 4 | **FAIL（2014 零 + 2021 −30,346）** | 0.1548 PASS | **0.495 PASS** | 0.9286 PASS | 0.0505 PASS | pass | NOT RUN | 不可交付（RA + 近十年） |
| `58E3agW1` | `[]` / 0 | 0 | **FAIL（3 段）** | **18** | PASS（min 49,968） | **0.8901 FAIL** | **0.8899 FAIL** | **−0.0769 FAIL** | 0.0969 PASS | pass | NOT RUN | 不可交付 |

### 2.3 口径说明（对上表三处易误读的交代）

1. **SUB 列 ≠ LOW_SUB_UNIVERSE_SHARPE 的 limit**。`SUB` 是 `sub_universe_sharpe` 指标；平台的 `LOW_SUB_UNIVERSE_SHARPE` 是**逐颗动态 limit**。本轮 `get_alpha_details` 实读：`gJezNxjg`、`rKR8VZVo`、`6Xd3lqnL` 的 `checks.pass` **都包含 `LOW_SUB_UNIVERSE_SHARPE`**，所以 SUB 0.96 / 0.93 / 0.76 均判 PASS；只有 `A1VYRo2w` 的 `checks.fail` 明确给出 `value 0.35 / limit 0.97`。**通过项的逐颗 limit 平台未返回，不能拿 0.97 横比**。
2. **`CLUSTER_TEST` 的 WARNING 不计 RA 失败**。`gJezNxjg` 1.2<1.58、`6Xd3lqnL` 0.94<1.58、`58E3agW1` 1.43<1.58 都在 `checks.warning`；`RA_CHECK_NAMES`（`src/wqb/config.py:393-407`）不含 `CLUSTER_TEST`，`compute_webdata_failed_counts` 只在名字属于 `RA_CHECK_NAMES` 时计入（`:441-446`）。因此平台 `fRA=0` 与本地严格 RA=0 都成立；上一版把 CLUSTER_TEST 当「RA warning 应计入」是不成立的。
3. **CW 全部 PASS**。7 颗的 `checks.pass` 均含 `CONCENTRATED_WEIGHT`，`checks.fail` 均无它；本报告不再单列一个空的 CW 风险列。**TO**：`rKR8VZVo` 0.0355 低于 0.05 review 地板，但平台 `checks.pass` 含 `LOW_TURNOVER`，所以它是「review 地板未达」而不是 RA FAIL；其余 6 颗 TO ≥0.05。

### 2.4 逐颗明细（设置 / 表达式 / 指标 / 逐闸 / 归档）

#### ① `88R7JMxX` — 多塔 3 段，prod + inv + op 三重拦截

- **设置 `[M]`**：USA/TOP3000/D1/REVERSION_AND_MOMENTUM/decay 5/trunc 0.08/2014-01-01~2023-12-31。
- **塔段 `[M]`**：`USA/D1/RISK(1.1) + USA/D1/INSIDERS(1.1) + USA/D1/OTHER(1.4)`，`effective=0`。
- **核心字段**：`mean_top_buy_transaction_count`、`rsk59_squeeze_risk` / `rsk59_shortinterestnotional`（risk59）、`median_chief_officer_tenure_days` / `board_external_connection_count` / `board_member_count_2`（board_gov_stats，按 `submit_ready` 标签 `SRC_board_gov_stats`）。
- **表达式（`[M]` DB 逐字）**：
  `vector_neut(vector_neut(ts_zscore(subtract(ts_mean(mean_top_buy_transaction_count, 22), ts_mean(mean_top_buy_transaction_count, 126)), 252), -ts_corr(vec_avg(rsk59_squeeze_risk), vec_avg(rsk59_shortinterestnotional), 1008)), group_rank(group_rank(multiply(rank(ts_backfill(median_chief_officer_tenure_days, 120)), rank(ts_backfill(board_external_connection_count, 120))), bucket(rank(ts_backfill(board_member_count_2, 120)), range="0,1,0.1")), subindustry))`
- **指标 `[M]`**：S 3.43 / F 3.02 / TO 0.2496 / 2Y 3.69 / SUB 1.72 / inv 0.1574 / margin 0.001546 / returns 19.29% / DD 5.64%。
- **近十年 `[M]`**：2014–2023 逐年 pnl 1,012,616 / 2,617,017 / 668,088 / 1,875,517 / 1,722,937 / 2,238,258 / 1,666,332 / 2,840,790 / 3,150,320 / 1,540,216，longCount 1457–1566、shortCount 1531–1675，全部 >0 ⇒ PASS。
- **逐闸**：RA PASS（`checks.fail=[]`、fRA=0）；塔位 FAIL（3 段）；op 20 >15；近十年 PASS；self 0.2431 PASS `[A]`；prod **0.7943** FAIL `[A]`；inv FAIL；TO/CW PASS；篮内 NOT RUN。
- **另**：与 `78L0meRx` 的 PnL 互相关 **=1.0**（dedup `maxPair`）；`78L0meRx` 表达式是同一骨架的「内外两层 vector_neut 顺序对调」写法（`[M]` `get_submit_ready` 实读）。两条只能留一条，裁决规则见 §4.5。
- **归档索引**：本报告 §2.4①；`tracking/USA/reference/_usa-shortinterest-dataset-scan-20261019.md`（rsk59 腿属 risk59，**不**索引进 shortinterest43 画像——上一版此处索引错，已更正）。

#### ② `58EqmQEN` — 近十年 + self + prod 三重拦截

- **设置 `[M]`**：USA/TOP3000/D1/SLOW_AND_FAST/decay 4/trunc 0.08/2014-2023。
- **塔段 `[M]`**：`USA/D1/INSTITUTIONS(1.0) + USA/D1/RISK(1.1)`，`effective=2`。
- **核心字段**：`executed_short_position_share_sum` / `aggregate_trade_share_count_regular_hours`（`submit_ready` 标签 `SRC_institutions20`）+ `short_interest_factor_score_2`。
- **表达式（`[M]` DB 逐字）**：
  `vector_neut(multiply(subtract(ts_zscore(ts_mean(divide(executed_short_position_share_sum, aggregate_trade_share_count_regular_hours), 22), 158), ts_zscore(ts_mean(divide(executed_short_position_share_sum, aggregate_trade_share_count_regular_hours), 22), 504)), rank(aggregate_trade_share_count_regular_hours)), ts_backfill(short_interest_factor_score_2, 66))`
- **指标 `[M]`**：S 2.52 / F 1.85 / TO 0.1256 / 2Y 2.77 / SUB 1.66 / inv 0.8889 / margin 0.00108 / returns 6.78% / DD 2.73%。
- **近十年 `[M]`**：2014–2018 五年 **longCount=0 / shortCount=0 / pnl=0**；2019–2023 pnl 324,034 / 836,586 / 608,830 / 887,933 / 560,465 ⇒ **FAIL**（有效持仓仅 2019–2023；全期指标是 10 年窗口含 5 年空仓，不是「5 年窗口读数」——上一版措辞不准，已更正）。
- **逐闸**：RA PASS；塔位 FAIL（2 段）；op 11（题面 ≤15 PASS；本地 gate 10 会 FAIL，见 §7.10）；近十年 FAIL；self **0.9082** FAIL `[A]`（对 `akKW0Lax`）；prod **0.9088** FAIL `[A]`；inv PASS；TO/CW PASS；篮内 NOT RUN。
- **台账陷阱**：`submit_ready` 行自报 `prod=0.6192`（`[M]` 实读），与 `[A]` 的平台重算 **0.9088** 差 **0.29**；该行 corr 标记作废，不得据此入篮。`get_alpha_details` 的 `checks.pending` 仍含 `PROD_CORRELATION`，本轮未重算。
- **归档索引**：本报告 §2.4②；`tracking/USA/reference/_usa-us_short_sale-field-profile-20261115.md`（`institutions20` 短卖占比语义）。

#### ③ `gJezNxjg` — 唯一「单颗指标层面仅 prod 卡死」的单段 SHORTINTEREST 件

- **设置 `[M]`**：USA/TOP3000/D1/SLOW/decay 0/trunc 0.08/2014-2023。
- **塔段 `[M]`**：`USA/D1/SHORTINTEREST ×1.1`，`effective=1`。
- **核心字段**：`mean_loan_rate_main`（`shortinterest3` 借券费率）。
- **表达式（`[M]` DB 逐字）**：
  `ts_decay_linear(reverse(group_zscore(ts_covariance(vec_avg(mean_loan_rate_main), vec_avg(mean_loan_rate_main), 22), industry)), 22)`
- **指标 `[M]`**：S 1.90 / F 1.80 / TO 0.1158 / 2Y 2.92 / SUB 0.96 / inv 0.7526 / margin 0.001943 / returns 11.26% / DD 15.23%。
- **近十年 `[M]`**：2014–2023 pnl 1,568,993 / 555,586 / 1,711,046 / 501,349 / 1,031,479 / 1,363,641 / **9,661** / 809,588 / 2,697,189 / 944,289；全 >0 ⇒ PASS。2020 仅 9,661（S 0.01、DD 7.02%），属弱年。
- **逐闸**：RA PASS（`checks.fail=[]`、fRA=0）；塔位 PASS；op 6；近十年 PASS；self **0.2823** PASS `[A]`；prod **0.8791** FAIL `[A]`；inv PASS；TO/CW PASS；篮内 NOT RUN。
- **`[A]` 前序读数过程（不是本轮动作）**：第 1 次 prod 查询返回 `correlation_busy`（`retry_after=119.5s`），按纪律未重触发，`sleep 122` 后只读重查得 0.8791；`get_alpha_yearly_stats` 前两次返回 `{}`（工具内部重试 5 轮后仍空），`get_record_sets` 确认 yearly-stats 在集合内，隔约 2 分钟第 3 次取到全量。本轮只复读了 `get_alpha_yearly_stats`（成功）与 `get_alpha_details`；**没有重跑 prod 查询**。
- **族层面警告**：单颗「仅 prod」不等于族可复活——`mean_loan_rate_main` 属 `USA-LOANRATE-FAMILY-DEAD`（§6.1）。若 prod 降到 <0.7，只说明生产池变松，不足以重开族；需用户裁定/Waiver。
- **归档索引**：本报告 §2.4③；`Claude/skills/wq-brain-ra-usa/references/shortinterest.md`；`_usa-shortinterest-dataset-scan-20261019.md`。

#### ④ `rKR8VZVo` — 近十年 + self + prod 三拦；台账 tag 不一致

- **设置 `[M]`**：USA/TOP3000/D1/INDUSTRY/decay 5/trunc 0.08/2014-2023。
- **塔段 `[M]`**：`USA/D1/SHORTINTEREST ×1.1`，`effective=1`。⚠ `submit_ready` 行 tag 为 `SRC_pv1`（`[M]` 实读），与平台 `SHORTINTEREST` 不一致；**以平台为准**。tag 写入方未定位，本报告不改库。
- **核心字段**：`loan_rate_volatility`（`shortinterest3` 费率波动率族）。
- **表达式（`[M]` DB 逐字）**：
  `ts_decay_linear(reverse(group_zscore(group_backfill(ts_decay_linear(vec_avg(loan_rate_volatility), 22), industry, 120), industry)), 66)`
- **指标 `[M]`**：S 1.86 / F 2.44 / TO 0.0355 / 2Y 2.88 / SUB 0.93 / inv 0.8441 / margin 0.01212 / returns 21.49% / DD 36.03%。
- **近十年 `[M]`**：2020 pnl **−648,472**（S −0.57、returns −7.02%、DD 16.24%）⇒ FAIL；2021 单年 DD 22.95%（pnl +3,516,623）；2022 pnl 6,667,589 / returns 66.41%。2020 的 `returns −7.02%` 与 `gJezNxjg` 2020 `DD 7.02%` 是**不同指标的同数值巧合**（本轮两颗 `get_alpha_yearly_stats` 均已复核，非抄写串行）。
- **逐闸**：RA PASS；塔位 PASS；op 6；近十年 FAIL；self **0.7411** FAIL `[A]`（对 `KmP73gj`；`EzWWGJP` 0.7018、`zGMV9N8` 0.7014 卡线）；prod **0.9592** FAIL `[A]`；inv PASS；TO **0.0355 低于 0.05 review 地板**（平台 `LOW_TURNOVER` PASS）；CW PASS；篮内 NOT RUN。
- **归档索引**：本报告 §2.4④；`shortinterest.md`；类别扫描。

#### ⑤ `6Xd3lqnL` — prod PASS（0.588）但塔位 + 可投资性拦截

- **设置 `[M]`**：USA/TOP3000/D1/REVERSION_AND_MOMENTUM/decay 5/trunc 0.08/2014-2023。
- **塔段 `[M]`**：`USA/D1/RISK(1.1) + USA/D1/OTHER(1.4)`，`effective=2`。
- **核心字段**：`total_buy_transaction_count` / `total_secondary_sell_transaction_count`（交易计数族）+ `rsk59_squeeze_risk` / `rsk59_shortinterestnotional`。
- **表达式（`[M]` DB 逐字）**：
  `vector_neut(ts_zscore(subtract(ts_sum(total_buy_transaction_count, 66), ts_sum(total_secondary_sell_transaction_count, 66)), 252), -ts_corr(vec_avg(rsk59_squeeze_risk), vec_avg(rsk59_shortinterestnotional), 1008))`
- **指标 `[M]`**：S 1.60 / F 1.02 / TO 0.0866 / 2Y 2.20 / SUB 0.76 / inv **0.4188** / margin 0.001173 / returns 5.08% / DD 5.96%。
- **近十年 `[M]`**：pnl 379,648 / 737,130 / 382,238 / 394,436 / 602,599 / 645,572 / 176,520 / 205,913 / 1,096,573 / 435,303，全 >0 ⇒ PASS（2020 S 0.52、2021 S 0.46，偏弱）。
- **逐闸**：RA PASS（`checks.fail=[]`、fRA=0；`CLUSTER_TEST` warning 0.94<1.58 **不计 RA**）；塔位 **FAIL（2 段）**；op 9；近十年 PASS；self **0.2996** PASS `[A]`；prod **0.588 PASS** `[A]`；inv **FAIL**；TO/CW PASS；篮内 NOT RUN。
- **结论**：即使不看塔位，`inv 0.4188 < 0.70` 也会被 USA 可投资性闸拦下 ⇒ 不可交付。
- **归档索引**：本报告 §2.4⑤；类别扫描。

#### ⑥ `A1VYRo2w` — RA 首闸即卡（子宇宙）+ 近十年

- **设置 `[M]`**：USA/TOP3000/D1/SLOW/decay 20/trunc 0.08/2014-2023。
- **塔段 `[M]`**：`USA/D1/RISK ×1.1`，`effective=1`（**不是 SHORTINTEREST 塔**）。
- **核心字段**：`rsk59_squeeze_risk`、`rsk59_shortinterestnotional`。
- **表达式（`[M]` DB 逐字）**：
  `-ts_corr(vec_avg(rsk59_squeeze_risk), vec_avg(rsk59_shortinterestnotional), 1008)`
- **指标 `[M]`**：S 2.24 / F 1.42 / TO 0.0505 / 2Y 2.19 / SUB **0.35** / inv 0.9286 / margin 0.00198 / returns 5.00% / DD 4.86%。
- **近十年 `[M]`**：2014 pnl 0、long/short 0；2021 pnl **−30,346**（S −0.10、returns −0.30%）⇒ FAIL；其余 8 年为正（2015–2018 S 4.41/4.55/3.08/3.54）。
- **逐闸**：RA **FAIL** `LOW_SUB_UNIVERSE_SHARPE` 0.35<0.97（`ra.failed_ra_count=1`、`ppa_failed=true`）；塔位 PASS（单段 RISK）；op 4；近十年 FAIL；self **0.1548** PASS `[A]`；prod **0.495 PASS** `[A]`；inv PASS；TO/CW PASS；篮内 NOT RUN。
- **定位**：内置 risk 腿单测，未过子宇宙闸，不宜当独立候选。
- **归档索引**：本报告 §2.4⑥；类别扫描。

#### ⑦ `58E3agW1` — 3 段 + op18 + self + prod + inv 五拦

- **设置 `[M]`**：USA/TOP3000/D1/REVERSION_AND_MOMENTUM/decay 5/trunc 0.08/2014-2023。
- **塔段 `[M]`**：`USA/D1/RISK(1.1) + USA/D1/INSIDERS(1.1) + USA/D1/OTHER(1.4)`，`effective=0`。
- **核心字段**：`total_buy_transaction_count`（126 日累计）+ rsk59 双腿 + board_gov 三字段。
- **表达式（`[M]` DB 逐字）**：
  `vector_neut(vector_neut(ts_zscore(ts_sum(total_buy_transaction_count, 126), 252), -ts_corr(vec_avg(rsk59_squeeze_risk), vec_avg(rsk59_shortinterestnotional), 1008)), group_rank(group_rank(multiply(rank(ts_backfill(median_chief_officer_tenure_days, 120)), rank(ts_backfill(board_external_connection_count, 120))), bucket(rank(ts_backfill(board_member_count_2, 120)), range="0,1,0.1")), subindustry))`
- **指标 `[M]`**：S 2.34 / F 1.96 / TO 0.0969 / 2Y 2.83 / SUB 1.21 / inv **−0.0769**（invest_S −0.18）/ margin 0.001817 / returns 8.80% / DD 6.70%。
- **近十年 `[M]`**：pnl 994,870 / 1,076,467 / 385,590 / 842,789 / 1,363,398 / 1,087,279 / 696,156 / **49,968** / 1,352,066 / 946,129，全 >0 ⇒ PASS（2021 S 0.09 几乎持平）。
- **逐闸**：RA PASS（`checks.fail=[]`、fRA=0；`CLUSTER_TEST` 1.43<1.58 不计 RA）；塔位 **FAIL（3 段）**；op **18 >15**；近十年 PASS；self **0.8901** FAIL `[A]`（对 `e75gdQoM`；次高 0.1715，单点撞车）；prod **0.8899** FAIL `[A]`；inv **FAIL**；TO/CW PASS；篮内 NOT RUN。
- **同源**：与 `88R7JMxX` 同骨架（主腿 `ts_sum(total_buy_transaction_count,126)` vs `ts_mean` 差值），共享同一 risk 腿与 board_gov 中性腿。
- **归档索引**：本报告 §2.4⑦；类别扫描。

---

## 3. 本战役新增：3 波 6 臂（0 全闸 / 0 可交付）

> 三个 batch 均 **2/2 COMPLETE、0 error**；`create_multi_simulation` 每批恰好 2 条，波次按序（`[A]`）。
> S/F/TO/2Y/SUB/inv = `[M]` `batch_get_alpha_metrics`；表达式/neutralization = `[M]` `get_alpha_by_id`；tenYear = `[M]` `get_alpha_yearly_stats`；prod/self = **未测**（DB `null`；ask 本阶段不查相关）。

### 3.1 波次总表

| 波 | batch id | 臂 | 数据集 | S | F | TO | 2Y | SUB | inv | 近十年 | RA fails | prod | self | 结论 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| 1 | `2Ue35NbRt4kL8zx137SnFUog`（首投 429，等 60s 重试） | `leaRl3GO` | us_short_sale | 0.05 | 0.01 | 0.0918 | 0.58 | 0.14 | −1.60 | **FAIL** | LOW_SHARPE / LOW_FITNESS / LOW_2Y | 未测 | 未测 | H4 证伪 |
| 1 | 同上 | `kqaL0ZGl` | shortinterest43（EDGX venue-mix，带 reverse） | −1.02 | −0.57 | 0.0947 | −0.99 | −0.52 | 1.0392 | **FAIL** | LOW_SHARPE / LOW_FITNESS / LOW_SUB / LOW_2Y | 未测 | 未测 | 机制活、方向反；非候选 |
| 2 | `SiRyE80M4ldc7Pz60MNIn` | `ZYaWKlWQ` | shortinterest43（EDGX 做空份额单腿） | 0.01 | 0.00 | 0.0482 | −0.68 | 0.07 | −3.00 | **FAIL** | LOW_SHARPE / LOW_FITNESS / LOW_2Y | 未测 | 未测 | 对照腿 |
| 2 | 同上 | `58Jqk6q1` | shortinterest43（EDGX 成交量份额单腿） | −0.07 | −0.02 | 0.0454 | −0.70 | 0.05 | 1.2857 | **FAIL** | LOW_SHARPE / LOW_FITNESS / LOW_2Y | 未测 | 未测 | 对照腿 |
| 3 | `3XSOUQg4e4DDbG1L1BwaeLj` | `0mPKMZ56` | shortinterest43（venue-mix 原始方向，11 点） | **1.02** | **0.57** | 0.0947 | **0.99** | **0.52** | 1.0392 | **FAIL（2016 −384,986）** | LOW_SHARPE / LOW_FITNESS / LOW_2Y | 未测 | 未测 | **本战役 S/F 最高臂** |
| 3 | 同上 | `XgaY8ZM0` | shortinterest43（F2 预注册 66d+252 漂移探针） | 0.70 | 0.33 | 0.0397 | 0.55 | −0.19 | 0.90 | **FAIL（2014/2018 负）** | LOW_SHARPE / LOW_FITNESS / LOW_SUB / LOW_2Y | 未测 | 未测 | 探针，F2 PROVISIONAL |

### 3.2 逐臂明细（6 条表达式全部逐字）

#### ① `leaRl3GO`（wave1，口径背离）— 判死

- **表达式 `[M]` DB 逐字**：`reverse(group_rank(ts_mean(subtract(divide(executed_short_trade_share_count, aggregate_executed_trade_share_count), divide(reported_short_sale_share_quantity, reported_total_trade_share_quantity)), 22), market))`
- **核心字段**：`executed_short_trade_share_count` / `aggregate_executed_trade_share_count`（executed）、`reported_short_sale_share_quantity` / `reported_total_trade_share_quantity`（reported），`us_short_sale`。
- **读数**：S 0.05 / F 0.01 / TO 0.0918 / 2Y 0.58 / SUB 0.14；3 项 RA FAIL；tenYear **FAIL**（2014 −7,993、2017 −265,875、2018 −113,365、2019 −347,792）。
- **归因**：|S|=0.05 < 0.5，命中预注册 H4 证伪条件——两口径各自归一成占比后塌缩为同一变量。**上一版只给 |S|，没有给两口径相关/方差证据**；本报告明确：H4 的「塌缩为同一变量」是 `[A]` 的预注册结论，本轮**未重算**两口径相关性，证据档位 = 预注册 + 单臂读数，不是本轮统计检验。
- **归档**：本报告 §3.2①；`_usa-us_short_sale-field-profile-20261115.md`。

#### ② `kqaL0ZGl`（wave1，venue-mix 反向）— 机制非死

- **表达式 `[M]` DB 逐字**：`reverse(group_rank(ts_mean(subtract(divide(shrt43_edgxshvol_svol, add(add(shrt43_batsshvol_svol, shrt43_byxxshvol_svol), add(shrt43_edgashvol_svol, shrt43_edgxshvol_svol))), divide(shrt43_edgxshvol_totalvolume, add(add(shrt43_batsshvol_totalvolume, shrt43_byxxshvol_totalvolume), add(shrt43_edgashvol_totalvolume, shrt43_edgxshvol_totalvolume)))), 22), market))`
- **读数**：S −1.02 / F −0.57 / TO 0.0947 / 2Y −0.99 / SUB −0.52；4 项 RA FAIL；tenYear **FAIL**（9 个负年：2014/2015/2017/2018/2019/2020/2021/2022/2023）。
- **归因**：|S|=1.02 远超 0.5 噪声带；未 reverse 的原始构造 S≈+1.02 / F 0.57 / 2Y 0.99 / SUB 0.52（`[A]` 反推，`0mPKMZ56` 本轮实测逐位吻合）。机制可挽救、非提交候选。
- **去重**：与 `0mPKMZ56` PnL 互相关 **−1.0**（`[A]` dedup），同一表达式的正/反写法，**不是两条独立信号**。
- **归档**：本报告 §3.2②；`_usa-shortinterest43-field-profile-20261115.md`。

#### ③ `ZYaWKlWQ`（wave2，EDGX 做空份额单腿）— 对照腿

- **表达式 `[M]` DB 逐字**：`group_rank(ts_mean(divide(shrt43_edgxshvol_svol, add(add(shrt43_batsshvol_svol, shrt43_byxxshvol_svol), add(shrt43_edgashvol_svol, shrt43_edgxshvol_svol))), 22), market)`
- **读数**：S 0.01 / F 0.00 / TO 0.0482（低于 0.05 review 地板）/ 2Y −0.68 / SUB 0.07；3 项 RA FAIL；tenYear **FAIL**（2014/2015/2016/2018/2019/2021/2022 负年）。
- **归因**：EDGX 做空份额的「水平」本身无信号；raw S 0.01 而 `risk_neutralized_sharpe +0.74`（`[A]`）。**上一版直接写「无信号」；本报告更正为**：0.74 提示可能存在被风险暴露盖住的信息，但本臂没有做风险中性化后的独立读数、也没有阈值/样本证据，不能把它当信号；结论只写「裸信号 0.01，不能作为候选；0.74 需另立实验验证」。
- **归档**：本报告 §3.2③；`_usa-shortinterest43-field-profile-20261115.md` §2/§5。

#### ④ `58Jqk6q1`（wave2，EDGX 成交量份额单腿）— 对照腿

- **表达式 `[M]` DB 逐字**：`group_rank(ts_mean(divide(shrt43_edgxshvol_totalvolume, add(add(shrt43_batsshvol_totalvolume, shrt43_byxxshvol_totalvolume), add(shrt43_edgashvol_totalvolume, shrt43_edgxshvol_totalvolume))), 22), market)`
- **读数**：S −0.07 / F −0.02 / TO 0.0454（低于 0.05 review 地板）/ 2Y −0.70 / SUB 0.05；3 项 RA FAIL；tenYear **FAIL**（2014/2015/2016/2018/2019/2021/2022 负年）。
- **归因**：场所流动性份额水平无独立信号；差值臂 S 1.02 ≫ −0.07，满足「差值必须高于成交量腿」。F2 预注册对象是「份额漂移」，本波未跑（后被 `XgaY8ZM0` 补）⇒ F2 当时只记 PROVISIONAL，不判死。
- **归档**：本报告 §3.2④；`_usa-shortinterest43-field-profile-20261115.md` §2/§5。

#### ⑤ `0mPKMZ56`（wave3，venue-mix 原始方向）— 本战役 S/F 最高臂

- **表达式 `[M]` DB 逐字**：`group_rank(ts_mean(subtract(divide(shrt43_edgxshvol_svol, add(add(shrt43_batsshvol_svol, shrt43_byxxshvol_svol), add(shrt43_edgashvol_svol, shrt43_edgxshvol_svol))), divide(shrt43_edgxshvol_totalvolume, add(add(shrt43_batsshvol_totalvolume, shrt43_byxxshvol_totalvolume), add(shrt43_edgashvol_totalvolume, shrt43_edgxshvol_totalvolume)))), 22), market)`
- **读数**：S **1.02** / F **0.57** / TO 0.0947 / 2Y **0.99** / SUB 0.52 / inv 1.0392；3 项 RA FAIL；tenYear **FAIL**（2016 pnl −384,986、S −1.14、DD 7.06%）。
- **逐年 `[M]`**：2014 +776,161（S 2.65）/ 2015 +592,807（1.80）/ 2016 −384,986（−1.14）/ 2017 +165,927（0.64）/ 2018 +973,054（3.21）/ 2019 +9,256（0.03）/ 2020 +115,690（0.30）/ 2021 +826,910（1.30）/ 2022 +445,555（0.87）/ 2023 +347,449（1.32）。10 年 longCount 1497–1556、shortCount 1516–1549。
- **结论**：本战役 S/F 最高臂，但**仍卡 3 项 RA（S 1.02<1.58 / F 0.57<1.0 / 2Y 0.99<1.58）+ 近十年 FAIL**，不进 S5；**不能称「近闸」**。
- **op 口径**：11 点，题面 ≤15 PASS；本地 toolkit gate `MAX_OP_CALLS=10` 会 FAIL（`_gate_expr_checks.py:114,382-384`）。ask 记录该臂按「原样复现」派发并平台接受；**已查 waiver**：`tools/waiver.py list --region USA` 无覆盖该闸的活跃 waiver，本报告不推断它走过 waiver。
- **归档**：本报告 §3.2⑤；`_usa-shortinterest43-field-profile-20261115.md` §5.5/§7。

#### ⑥ `XgaY8ZM0`（wave3，F2 预注册漂移探针）— PROVISIONAL

- **表达式 `[M]` DB 逐字**：`group_rank(ts_zscore(ts_mean(divide(shrt43_edgxshvol_totalvolume, add(add(shrt43_batsshvol_totalvolume, shrt43_byxxshvol_totalvolume), add(shrt43_edgashvol_totalvolume, shrt43_edgxshvol_totalvolume))), 66), 252), market)`
- **读数**：S 0.70 / F 0.33 / TO 0.0397（低于 0.05 review 地板）/ 2Y 0.55 / SUB −0.19 / inv 0.90；4 项 RA FAIL；tenYear **FAIL**（2014 −30,945、2018 −115,152）。
- **结论**：F2 证伪线「与 PV volume 族相关 >0.9 或 |S|<0.5」的 |S| 腿未命中（0.70 ≥ 0.5）⇒ F2 不判死；但也没到继续线（<1.0），且 PV 相关未测 ⇒ **F2 记 PROVISIONAL**。TO 0.0397 低于 USA review 地板 0.05。
- **归档**：本报告 §3.2⑥；`_usa-shortinterest43-field-profile-20261115.md` §6/§8。

### 3.3 6 臂近十年逐条（全部 FAIL，这条推翻了上一版「1 近闸」）

| 臂 | 负年（pnl < 0） | 最小 pnl 年 | 判定 |
|---|---|---|---|
| `leaRl3GO` | 2014 / 2017 / 2018 / 2019 | 2019 −347,792 | **FAIL** |
| `kqaL0ZGl` | 2014 / 2015 / 2017 / 2018 / 2019 / 2020 / 2021 / 2022 / 2023 | 2018 −973,054 | **FAIL**（仅 2016 正） |
| `ZYaWKlWQ` | 2014 / 2015 / 2016 / 2018 / 2019 / 2021 / 2022 | 2022 −2,153,787 | **FAIL** |
| `58Jqk6q1` | 2014 / 2015 / 2016 / 2018 / 2019 / 2021 / 2022 | 2022 −2,220,674 | **FAIL** |
| `0mPKMZ56` | 2016 | 2016 −384,986 | **FAIL** |
| `XgaY8ZM0` | 2014 / 2018 | 2018 −115,152 | **FAIL** |

> 判据与存量完全相同：逐年 `longCount>0 && shortCount>0 && pnl>0` 全部成立才 PASS。6 臂全部至少有一个负年 ⇒ 全部 FAIL。**上一版只对 `rKR8VZVo` 套近十年、却对 `0mPKMZ56` 写「近闸」，口径不一致，已更正。**

### 3.4 三波归因与独立构造数

- `wave1` 试图用 executed/reported 口径背离造信息 → `leaRl3GO` |S|0.05 证伪（同一变量）；同波 `kqaL0ZGl` 的 venue-mix 反向读数 |S|1.02 是唯一活口。
- `wave2` 拆两腿：做空份额 0.01 / 成交量份额 −0.07 ⇒ 信息只在**差值**里。
- `wave3` 原样复现差值臂得 `0mPKMZ56` S1.02/F0.57/2Y0.99，方向坐实但强度不够；F2 漂移探针 0.70，只够 PROVISIONAL。
- **独立构造数**：6 臂不是 6 个独立构造。`kqaL0ZGl` 与 `0mPKMZ56` PnL 互相关 **−1.0**，是同一构造的正/反写法；按独立构造计 = **5 个**（`leaRl3GO`、venue-mix 构造、`ZYaWKlWQ`、`58Jqk6q1`、`XgaY8ZM0`）。上一版「6 臂」会高估探索度。
- **本战役天花板**：0 全闸、0 近闸、0 可交付。`0mPKMZ56` 是本战役 S/F 最高臂，但距 RA 线仍差 S −0.56 / F −0.43 / 2Y −0.59。

---

## 4. 去重与相关性聚类（ask 给定 dedup 读数）

> **范围交代**：这是 **dedup 输出**（ask 提供 `textDuplicates` / `correlatedPairs` / `representatives` / `maxPair=1` / `maxSubset=9`），**不是**「已确认篮」的互相关闸。**ask 未给 dedup 池总数、未给池来源（USA 全池 / 某几波）**；本报告不能补造。`maxSubset=9` 是最大高相关子集，**不是池总数**。篮内互相关 **NOT RUN**。

### 4.1 dedup 输出中出现的全部 id（按文本顺序）

`88N6OOP7`、`Jj8XKW62`、`npazn8v3`、`kqaL0ZGl`、`0mPKMZ56`、`78L0meRx`、`88R7JMxX`、`2rAQ6mQN`、`QPvrZW7X`、`9qxP0JbV`、`A1VJKkYg`、`Xg9w61Pm`、`KPJwQzex`、`YP1WV5aW`、`xArwOljq`、`j2YdKN3Q`、`58EqmQEN`、`omEw8PNb`、`gJezNxjg`、`omE2vmZn`、`d5W85Yng`、`A1VJ1end`、`6Xd3lqnL`、`xAr9jz6g`、`gJevwxg0`、`RREZR9Nj`、`bl62lJor`、`9qxPe8X2`、`MPYlnRaM`、`A1VYRo2w`、`MPYwqvLn`、`N1N5lkQX`、`rKR8VZVo`、`58E3agW1`（`representatives` 里的 7 颗）。
> 这 34 个 id 是 dedup 文本中能直接读到的全部；**池总数仍未知**。其中 9 个是本报告评估件（7 存量 + 新臂 `kqaL0ZGl` / `0mPKMZ56`），其余 25 个只在 dedup / READY 行出现，未在本报告重新读数。

### 4.2 文本重复

- `88N6OOP7` = `Jj8XKW62` = `npazn8v3`（三对 textDuplicates 全命中）⇒ 同表达式三条，只能留一条。
- `2rAQ6mQN` 与 `Jj8XKW62` 0.9997、与 `88N6OOP7` 0.9969、与 `npazn8v3` 0.9857 ⇒ 同族近似。

### 4.3 关键相关对（|ρ| ≥ 0.9；本报告相关者）

| 对 | ρ | 判读 |
|---|---:|---|
| `kqaL0ZGl` – `0mPKMZ56` | **−1.0000** | 同一表达式的正/反写法（wave1 臂2 vs wave3 臂1），不是两条独立信号 |
| `78L0meRx` – `88R7JMxX` | **1.0000** | 同一骨架、内外 vector_neut 顺序对调 ⇒ 同一因子 |
| `58EqmQEN` – `QPvrZW7X` | 0.9367 | `us_short_sale`/institutions20 22-126−504 差值族高度同质 |
| `58EqmQEN` – `9qxP0JbV` | 0.9352 | 同上 |
| `58EqmQEN` – `YP1WV5aW` | 0.9212 | 同上 |
| `gJezNxjg` – `omE2vmZn` | 0.9028 | `shortinterest3` 费率族同源 |

### 4.4 同池但 |ρ| < 0.9 的警示对（上一版混在 ≥0.9 表里，已拆出）

| 对 | ρ | 判读 |
|---|---:|---|
| `6Xd3lqnL` – `xAr9jz6g` | 0.8448 | 交易计数 + rsk59 骨架近似 |
| `A1VYRo2w` – `9qxPe8X2` | 0.6797 | 同池需注意，非同一因子 |
| `rKR8VZVo` – `kqaL0ZGl` | −0.5726 | 中等负相关，非同一因子 |

### 4.5 副本/镜像的裁决规则（用户最可能问的三问）

1. **`0mPKMZ56` vs `kqaL0ZGl`（ρ=−1）留哪条？** 留 **`0mPKMZ56`**（正 S、正 F，是本战役唯一 S/F 接近 1 的构造）；`kqaL0ZGl` 只作为「反向对照/历史证据」，**不再单独占席位，不重复派发**。若后续要验证方向，只允许用 `0mPKMZ56` 的同一表达式，不得把 `kqaL0ZGl` 当第二条候选。
2. **`88R7JMxX` vs `78L0meRx`（ρ=1）留哪条？** 两条都是 3 段 ATOM 不合规，均不可交付；若只为保留证据，留 **`88R7JMxX`**（有 `[A]` 的 prod=0.7943 实测记录；`78L0meRx` 的 prod=null）。`78L0meRx` 标「重复件」。
3. **`shortinterest24` 探针有数据时谁/什么预算重开？** 需要用户先批准「重启 shortinterest 数据集」（画像 §8 的要求）；批准后只派 **1 条** `rank(ts_backfill(shrt24_triggertime_2,250))`、`neutralization=NONE`（同 `tools/probe/dataset_data_probe.py` 口径）做 `longCount/shortCount` 探针；探针也消耗仿真配额，不是零成本。若 long/short 均 0 ⇒ 数据层 `NO_DATA`；若 >0 ⇒ `TESTED`，再评估 1 波 ≤2 条事件/bucket 模板。

---

## 5. 字段画像归档索引（2 集专题 + 6 集字段目录）

### 5.1 两份专题画像（共同指标）

| 数据集 | 权威位（tracking 母本） | skills 镜像 | 行数 / 字节 | md5（两侧） | sha256（两侧） |
|---|---|---|---:|---|---|
| `shortinterest43` | `tracking/USA/reference/_usa-shortinterest43-field-profile-20261115.md` | `Claude/skills/wq-brain-ra-usa/references/_usa-shortinterest43-field-profile-20261115.md` | 370 / 40650 | `911843207a9489a9b9dff59d42093d4f` | `52c9c2f91a7745e67383f6bd09d825319da4561a587fc59eb72ef0b6cd34cfe7` |
| `us_short_sale` | `tracking/USA/reference/_usa-us_short_sale-field-profile-20261115.md` | `Claude/skills/wq-brain-ra-usa/references/_usa-us_short_sale-field-profile-20261115.md` | 522 / 44120 | `a3135d057977192753700e5e307d636f` | `44dbcc7f83b2f8fcc35229495d5ef548d1fb2c7005bc5f783a3cd5b9f423f60b` |

> 两对镜像的 md5 与 sha256 均逐字相同（本轮 `md5sum`/`sha256sum` 实跑）；这是「镜像一致」的证据，**不等于 `sync_skills.py --check` 全绿**（见 §5.2）。

### 5.2 命名规则与同步现状（实际命令结果）

```
_usa-<dataset_id>-field-profile-<YYYYMMDD>.md
```

- `_` 前缀 = 区域专题手写实证，不是 `wqb.profiles render` 生成块，不会被 `render --apply` 覆盖。
- `<dataset_id>` 按平台 `dataset_id` 原文，不缩写（`us_short_sale` 保留下划线，避免与 kebab 变体分叉）。
- `<YYYYMMDD>` = 画像文件名日期；本次按任务指定 `20261115`，**实际采集时点 2026-11-16**，已在两份正文首行登记。
- 兄弟命名：类别级扫描 `_usa-<category>-dataset-scan-<asOf>.md`（现有 `_usa-shortinterest-dataset-scan-20261019.md`）；模板库 `_usa-<dataset_id>-template-library-<asOf>.md`。
- **同步实测 `[M]`**：`world-quant-brain-mcp/.venv/Scripts/python.exe tools/sync_skills.py --check` → **exit 1**，`共 3 个文件漂移，涉及 3 个安装位`，漂移文件全部是 `worldquant-submit-alpha/references/submit-chain.md`（**不是**本报告两份 shortinterest 画像）；`.claude` / `.workbuddy` 为 `[OK]`；`.qoder-cn` 是 `.claude` 的 junction，输出明写「去重 1 个安装位入口」；`.cursor` 已关闭。**因此不能写「全部受维护安装位与仓库一致 / 已同步 5 个」**——上一版引用了 ask 的旧记录，与本轮实测不符，已更正。
- 本报告**没有新增/修改**两份画像或任何 `Claude/skills/` 文件；只读取与校验。

### 5.3 `shortinterest43` 画像要点（32/32 字段全量）

- 32 字段全 MATRIX，cov 0.9994，ΣalphaCount 2272（数据集级 1571）。五族：F1 交易所卖空流量比（8）/ F2 场所成交规模份额（4）/ F3 sumsize（16）/ F4 marketcenter（4）/ F5 豁免卖空（4）。
- **家族计数为什么不是 36**：F1 的 8 = 4 所 ×（`_svol` + `_totalvolume`）；F2 的 4 是其中 4 个 `_totalvolume` 的「分母件独立视图」，**与 F1 重叠，不是额外 4 个字段**。按字段去重：F1 8 + F3 16 + F4 4 + F5 4 = **32**；按族视图相加才是 36。上一版直接相加得 36，已更正。
- 最强证据 `88RKbpGl`（波 309，`[H]`）：S **1.78** / F **1.12** / 2Y **2.35** / SUB **1.31** / inv **0.983** / risk_neut **1.30** / RA `checks.fail=[]` / 单段 SHORTINTEREST；**prod 0.7908**（记录 2026-10-31，已过 48h 保鲜期）⇒ 信号层活、prod 封。
- **D2 状态更新**：画像 §6 写「D2 ❌（F2/F4 从未测）」，该画像早于 wave3。**追加 wave3 后**：F2 已有 `XgaY8ZM0`（F2 场所成交量份额 66d+252 漂移）与 `0mPKMZ56` 的 totalvolume 分量；**F4 仍 0 条** ⇒ D2 仍 ❌，理由改为「F4 未测；F2 只有 1 条漂移探针，未覆盖水平/均值形态」。F3 有 4 条实测（4 个几何，均 |S|≤0.38），但 16 个 `data1/data2` 字段未逐字段测；`edgxsh_sumsize_m_data2` 从未单字段测过。
- 判死六维：D1 ✅（≥10 结构互异）、D2 ❌（F4 未测）、D3 ✅、D4 ✅（3 轴）、D5 ✅、D6 ✅（decay+中性化双变）⇒ **最高只到 PROVISIONAL**；不得宣布 SHORTINTEREST 塔关闭。

### 5.4 `us_short_sale` 画像要点（4/4 字段全量）

- 4 字段全 MATRIX、cov 1.0：`executed_short_trade_share_count` / `aggregate_executed_trade_share_count`（executed）与 `reported_short_sale_share_quantity` / `reported_total_trade_share_quantity`（reported）。
- `get_datafields(filter_sharpe=false)`、`count=4 == platform_count=4`、`complete=true`、`pages_fetched=1` ⇒ 无截断、无抽样。
- 结论：日频做空占比族此前被判「探针级判弱（非终判死）」；本战役 wave1 `leaRl3GO` 的 |S|0.05 进一步证伪「两口径背离」构造；但该集**未穷尽**（六维未逐维举证）。

### 5.5 类别级 6 集全景（字段目录全量；证据命中单列）

| dataset | fields_seen / 平台 | evidence_hit_n | status | alphaCount | valueScore | 画像归档索引 |
|---|---|---:|---|---:|---:|---|
| `short_interest_pred` | 10 / 10 | 6 | TESTED | 518 | 3.0（审计 JSON） | 类别扫描 |
| `shortinterest24` | 1 / 1 | 0 | **UNTESTED_COV_OK** | 449 | 3.0（审计 JSON） | 类别扫描 + 覆盖审计 |
| `shortinterest29` | 32 / 32 | 24 | TESTED | 276 | 4.0（审计 JSON） | 类别扫描 + `shortinterest.md` |
| `shortinterest3` | 31 / 31 | 31 | TESTED | **4856** | 2.0（审计 JSON） | 类别扫描 + `shortinterest.md` |
| `shortinterest43` | 32 / 32 | 23 | TESTED | 1571 | 3.0（画像 / 审计 JSON） | `_usa-shortinterest43-field-profile-20261115.md` |
| `us_short_sale` | 4 / 4 | 2 | TESTED | 356 | 3.0（审计 JSON） | `_usa-us_short_sale-field-profile-20261115.md` |

> 这张表的 `evidence_hit_n` 来自 `data/dataset_assets/USA_shortinterest_coverage_audit_d1.json` 的 `rows[]`（`[M]` 实读）。**「字段目录完整」≠「字段已测」**：`short_interest_pred` 目录 10/10 但证据只命中 6 个字段；`shortinterest43` 目录 32/32 但命中 23 个。上一版把「10/10 字段目录」写成「已测」是混用，已更正。

### 5.6 覆盖审计归档与 probe/closure 的关系（上一版自相矛盾处）

- 报告：`reports/dataset_experience/usa_shortinterest_coverage_audit_20261115.md`（工具生成；scope 段明写证据盲区）。
- JSON：`data/dataset_assets/USA_shortinterest_coverage_audit_d1.json`。`[M]` 实读：`scope.datasets_platform_count=6 / datasets_pulled=6 / datasets_complete=true`；`counts={TESTED:5, UNTESTED_COV_OK:1}`；`scope.scoped_note` 明写「本 JSON 只含 shortinterest 6 集（category 面），不是 USA 全 region 286 集；全 region 审计因 429 停在 20/286，已停止」。**6 集分母来自 category 过滤的另一轮，不是那轮未完成的 20/286 region 审计**——上一版没有说清，已补。
- **为什么 `probe PASS` 而 `closure FAIL` 同时成立**：`gate_probe` 只把 `UNTESTED_BLIND` / `PROBE_FAILED` 列为 `probe_needed`（`tools/gates/audit_dataset_coverage.py:544-557`）；`shortinterest24` 是 `UNTESTED_COV_OK`，所以 **probe 门 PASS（`probe_needed=[]`）**。`gate_closure` 把 `UNTESTED_COV_OK` 和 `PROBE_FAILED` 都列为 `CLOSURE_BLOCKING`（`:113-115,524-541`），所以 **closure 门 FAIL（`untested_with_fields=[shortinterest24]`）**。两者不矛盾：probe 门只管「元数据盲区/探针失败」，closure 门管「有字段但零证据」；`shortinterest24` 属于后者，仍必须补 longCount/shortCount 探针才能从 `UNTESTED_COV_OK` 转 `TESTED`/`NO_DATA`。
- **`us_short_sale` 的人工改判是否写回**：`[M]` 实读 JSON `rows[]`：`us_short_sale.status=TESTED`、`evidence_hit_n=2`；`counts.TESTED=5`。**人工 field 级改判已写回审计 JSON**，下次用这份 JSON 跑 `category_coverage_audit.py --field-audit` 不会回到 4/6；若从零重生成 JSON 且不跑 field 级表达式文本判据，仍可能回到 4/6——所以报告必须同时保留「`expressions.dataset` 18.9% NULL」这个口径说明。
- 两口径差异：`category_coverage_audit.py --region USA --universe TOP3000 --delay 1 --category shortinterest` 实跑 exit 1、`NOT_EXHAUSTED`、`platform_total=6 / tested_in_scope=4 / untested=['shortinterest24','us_short_sale']`；成对 field 级审计后 `tested_in_scope=5`、只剥出 `shortinterest24`。正确表述：**「已测 5/6，真未探 1/6（shortinterest24）」**；不得写「shortinterest 面已穷尽」。

---

## 6. 判死 / 停投 / 收割池 / S6 状态

### 6.1 判死 / 停投（带证据档位；不再把台账判死冒充六维终判）

| 对象 | 证据（来源） | 六维档位 | 本报告处置 |
|---|---|---|---|
| `shortinterest3` 整集（USA/D1） | `dead_end USA-W337-shortinterest3-prodpool-D1`；wave329–337 共 9 波；`gJeLLpKO` prod 0.9418、`leAAYpOx` prod 0.9122（`[A]`/`[H]`；wave337 行见 `list_wave_results`） | **六维未逐维举证**（D1–D6 无档案） | 记「台账判死 / PROVISIONAL 级」；不据此封杀邻接集 |
| 借贷费率族 | `USA-LOANRATE-FAMILY-DEAD`；3 次独立 prod 0.9482/0.8949/0.8463；跨 SLOW/SUBINDUSTRY（`[A]`） | **六维未逐维举证** | 记「台账判死 / PROVISIONAL 级」；`gJezNxjg` 0.8791 / `rKR8VZVo` 0.9592 复证 |
| `short_interest_pred` | 全期 S≈0、符号随年份翻转；10 字段中 4 个 S −0.22/−0.03/0.16/0.48（`[A]`） | **六维未逐维举证**；只给 4/10 字段读数 | 记「台账判死 / PROVISIONAL 级」 |
| `us_short_sale` | 4 字段裸探针 S 0.05/0.04/−0.65/0.05；22d 反向 S0.84、66d/126d 更低（`[A]`） | **六维未逐维举证** | **探针级判弱（非终判死）** |
| `shortinterest29` | `RA 全过 0/68`（68 = 68 条回测，见 `shortinterest.md` 证据表）、max abs(S) 0.79；4 个新机制全灭（`[A]`） | **六维未逐维举证** | 记「台账判死 / PROVISIONAL 级」；valueScore 4.0 是平台元数据，不是信号强度证据 |
| `shortinterest24` | 1 字段 cov 0.2573、evidence_hit_n=0（`[M]` JSON） | **未测**，不是「死」 | **只记 `UNTESTED_COV_OK` + 未探针；删除上一版「低覆盖排除」**——AGENTS §8.11 明确数据集级 coverage 不是存在性判据，只有 field 级 TESTED/NO_DATA 才算排除 |
| `shortinterest43` 旧「日频做空量=噪声」 | 画像 §5.5/§6.1 已逐条推翻；`88RKbpGl` S1.78/F1.12/2Y2.35、prod 0.7908（`[H]`） | 画像 D1–D6：D2 ❌（F4 未测） | **旧判作废**；改记 **prod 封、非信号死**，六维只到 PROVISIONAL |
| `institutions20`（Short Sale Volume） | 正向 −0.59 / 反向 0.85（`[A]`） | **六维未逐维举证** | 强度不足；不封数据集 |

### 6.2 收割池优先检查（把过滤条件写清楚）

- **`ask` 的过滤条件**：`本地 USA×shortinterest 的 alphas 表 prod_clean(<0.7) & stage='IS' & 未提交 = 0`（`[A]` 实查）。这是**限定 shortinterest 数据集/类别**的池。
- 为什么与 §0 的两颗 prod PASS 不冲突：`6Xd3lqnL` 的塔段是 **RISK+OTHER**、`A1VYRo2w` 是 **RISK**，都不属于 shortinterest 单塔件；若把过滤放宽到「全 USA IS 未提交」，这两颗确实 prod<0.7，但不是本报告要交付的 shortinterest 件。
- `submit_ready(READY)` 行的实测状态（`[M]` `get_alpha_by_id` + `get_submit_ready`）：

| alpha | submit_ready note | submit_ready.prod | alphas.prod_correlation / 平台 `[A]` | status / stage | 结论 |
|---|---|---:|---:|---|---|
| `rKR8VZVo` | auto-enqueue wave=usa_probe_20261115 | null | **0.9592**（本轮 `[M]` `get_alpha_by_id`，与 `[A]` 一致） | UNSUBMITTED / IS | 不可收割 |
| `gJezNxjg` | auto-enqueue wave=usa_probe_20261115 | null | **0.8791**（本轮 `[M]` `get_alpha_by_id`，与 `[A]` 一致） | UNSUBMITTED / IS | 不可收割 |
| `gJevwxg0` | auto-enqueue wave=usa_probe_20261115（`[A]` 行） | null | null（本轮 `[M]` `get_alpha_by_id`） | UNSUBMITTED / IS | 待测；loan_rate 族 |
| `MPYwqvLn` | auto-enqueue wave=usa_probe_20261115（`[A]` 行） | null | null（本轮 `[M]` `get_alpha_by_id`） | UNSUBMITTED / IS | 待测；loan_rate 族 |

- `58EqmQEN` 的 READY 行自报 0.6192（`[M]`），平台重算 0.9088（`[A]`）⇒ **陈旧台账会制造假「prod-clean」**；该行 corr 标记作废。
- **结论**：当前 READY 队列里**没有「prod 已核且 <0.7」的 shortinterest 单塔件**；`gJevwxg0` / `MPYwqvLn` 的 prod 未测（null），不能算「可收割」，也不能把 `towers=[]` 或 `IS_ONLY` 当放行。

### 6.3 塔位口径

- 点亮 = 同塔**本自然季度累计 3 颗且三对互相关 < 0.5**（`Claude/skills/wq-brain-ra-pipeline/SKILL.md:157`）；当前 USA/D1/shortinterest **0/3 颗**（`[M]` `get_pyramid_alphas`，D0=0、D1=0）。
- `0/3` 是「0 颗 / 需要 3 颗」，不是「0 of 3 段」。
- 因此本报告的任何「S/F 最高臂」都不能写成「点亮」或「近闸」；`0mPKMZ56` 仍卡 3 项 RA + 近十年 FAIL，且 prod/self 未测。

### 6.4 S6 回写状态：**未完成 / 未证实**

- 本报告**没有**调用 `upsert_wave_result` / `seal_dead_end` / `upsert_registry_empirical`；没有写 `wave_results` / `salvage_pool` / `registry_empirical`。
- `[M]` `list_wave_results(region=USA, limit=120)`：最新 `wave_number=344`（news94，2026-11-08）；**返回前段未见**本战役 3 波（`shortinterest43` / `us_short_sale` 的 wave1–3）的 `wave_results` 行（输出被 resultBudget 截断，**未全表检索**，不能据此断言绝对没有）。
- `[M]` `get_campaign_summary(region=USA)`：`waves.total=389 / closed=368`、`dead_ends=80`、`submit_ready=1`。
- `[M]` `get_salvage_pool(region=USA)`：返回历史条目（前段可见 `shortinterest3` 的 `RREEojQe` / `leAAYpOx` 等），**未全量核对**是否有本战役 6 臂。
- **后果**：下一轮如果只读 `wave_results` / `salvage_pool`，会看不到这 3 波，可能重复挖同一批构造。S6 回写是本战役的未完成项（§8 P6）。

---

## 7. 调优经验与工具用法摘要

1. **先归因再做对比实验，禁止盲扫网格。** `wave1` 用 executed/reported 背离造信号，`leaRl3GO` |S|0.05 命中预注册 H4（两口径归一后同一变量）⇒ 立即判死该族；`wave2` 只拆两腿、`wave3` 只复现差值臂 + 1 条 F2 探针。三波共 6 臂 / **5 个独立构造**（`kqaL0ZGl` 与 `0mPKMZ56` 是 ±1 副本）。
2. **反向读数是活口，但别把镜像当第二条。** `kqaL0ZGl` S −1.02，反向即 +1.02；`0mPKMZ56` 本轮实测 S1.02/F0.57/2Y0.99/SUB0.52，与反推逐位吻合。但两者 PnL 互相关 −1.0，只能算 1 个构造。
3. **差值 ≠ 分量之和。** 两腿单独 S 0.01 / −0.07，差值臂 S 1.02 ⇒ venue-mix 的「份额错配」携带两个分量都不携带的信息；但差值仍不够提交线（S 1.02<1.58、F 0.57<1.0、2Y 0.99<1.58）。
4. **近十年必须对所有臂套同一判据。** 上一版只对 `rKR8VZVo` 套、却对 `0mPKMZ56` 写「近闸」；本轮补跑 6 臂逐年后，6/6 全部 FAIL。`0mPKMZ56` 2016 单年 −384,986 就足以判 FAIL。
5. **去重必须按表达式与 PnL 双查。** `0mPKMZ56` 与 `kqaL0ZGl` −1.0；`88R7JMxX` 与 `78L0meRx` =1.0；平台按文本去重只对同批有效，跨批必须自己比对。
6. **prod 台账 5 天作废，陈旧值只可作乐观下限。** `58EqmQEN` READY 行 0.6192 → `[A]` 平台重算 **0.9088**（+0.29）；`rKR8VZVo` 行 prod=null → `[A]` 0.9592。**口径分层**：`5 天`是台账经验的保守线（ask 材料/历史复盘），`48h` 是 `check_correlation(refresh=False)` 的缓存保鲜线（`AGENTS.md §7.5`）；两者不是同一个阈值。用 48h 缓存先查，但**已过 48h 或来源不明的 prod 行必须重算**后才能入篮。
7. **USA 可投资性闸是独立杀手，`batch_get_alpha_metrics.investability_ratio` 是唯一入口。** `88R7JMxX` S3.43 但 inv **0.1574**；`6Xd3lqnL` prod 0.588 PASS 但 inv **0.4188**；`58E3agW1` **−0.0769**。比值可负/可 >1，不是百分比。
8. **ATOM 看 `pyramids.list`，不看 `submit_ready.towers`。** 7 颗存量的 `submit_ready.towers` 全是 `[]`，但平台实际 4 颗多段（3/3/2/2 段）。`pyramids.list` 单段才是硬约束；`6Xd3lqnL` 的 2 段就是 prod PASS 也不能交付。
9. **SUB 是逐颗动态 limit，不能拿 0.97 横比。** `gJezNxjg` 0.96 / `rKR8VZVo` 0.93 / `6Xd3lqnL` 0.76 的 `checks.pass` 都含 `LOW_SUB_UNIVERSE_SHARPE`；只有 `A1VYRo2w` 的 `checks.fail` 给出 0.35<0.97。用平台 `checks.fail` 作权威，不自行用别的颗的 limit。
10. **算子点有两套口径，别混。** 本地 toolkit gate `MAX_OP_CALLS=10`（`_gate_expr_checks.py:114`，`:382-384` 在 `n_calls >= 10` 处 FAIL；是仓库文件，不是「未跟踪 gate」——上一版措辞错）；题面硬约束 ≤15。`58EqmQEN` 11 点、`0mPKMZ56` 11 点按题面 PASS；**若按本地 gate 复核则 FAIL（11≥10）**；`88R7JMxX` 20 点、`58E3agW1` 18 点按两套都 FAIL。**已查 waiver**：`tools/waiver.py list --region USA` 返回 11 条，全部过期/无效，没有覆盖 op 闸的活跃 waiver；11 点臂若走本地 gate 必须有 waiver 或改表达式，本报告不推断它们走过 waiver。
11. **`check_correlation` 遇 `correlation_busy` 不要重触发。** `[A]` 记录 `gJezNxjg` `retry_after=119.5s`，按纪律 `sleep 122` 后同参只读重查得 0.8791；账号级单并发。
12. **`get_alpha_yearly_stats` 可能临时返回 `{}`。** `[A]` 记录 `gJezNxjg` 前两次空（内部已重试 5 轮），`get_record_sets` 确认 yearly-stats 在集合内，隔约 2 分钟第 3 次成功；本轮复读 13 颗均成功。
13. **字段画像必须 `filter_sharpe=false` 全量拉。** `shortinterest43`/`shortinterest29` 用 true 各丢 4 字段（28/32）；`us_short_sale` 4/4、`shortinterest43` 32/32 都是 false 口径。
14. **覆盖闸分母只认平台 `/data-sets` 全表，分子要 field 级背书；probe 门与 closure 门不是一回事。** `db:expressions` 有 18.9% dataset=NULL，`us_short_sale` 曾被误列未测；成对 field 审计后真未探只剩 `shortinterest24`（closure FAIL、probe PASS，因为 `UNTESTED_COV_OK` 不在 probe_needed 里）。
15. **判死标记不得单独作依据；台账判死 ≠ 六维终判。** `shortinterest43` 的旧「日频做空量=噪声判死」已被 `88RKbpGl` 推翻；`shortinterest3` / loan rate / `short_interest_pred` / `shortinterest29` 的台账判死均未逐维举证 D1–D6，只能标 PROVISIONAL（`AGENTS.md §7.6`）。
16. **S6 回写是完成定义的一部分，不能只写报告。** 本战役 3 波未写入 `wave_results`（`list_wave_results` 最新 344），下一轮会看不见；见 §6.4 / §8 P6。

---

## 8. 下一步（按 ROI 排序；均需用户授权后才动作）

### 8.0 三个需要用户裁决的二选一（先裁决，再花配额）

1. **`0mPKMZ56` 保留、`kqaL0ZGl` 作废（推荐）**：两者 PnL 互相关 −1.0，只能留一条；保留 S/F 为正的 `0mPKMZ56`，`kqaL0ZGl` 只作反向对照。规则：同一构造的正/反两向不得同时占席位、不得同时派发。
2. **`88R7JMxX` 保留为证据、`78L0meRx` 标重复（推荐）**：两者 PnL 互相关 1.0；两者都是 3 段 ATOM 不合规、都不可交付。若只为留证，留 `88R7JMxX`（有 `[A]` prod=0.7943 实测），`78L0meRx` 标重复；不得把两条都送相关性闸。
3. **`shortinterest24` 探针需要用户批准重启数据集**：批准后只派 1 条 `rank(ts_backfill(shrt24_triggertime_2,250))`、`neutralization=NONE`；探针消耗仿真配额。若 long/short 均 0 ⇒ `NO_DATA`（数据层排除）；若 >0 ⇒ `TESTED`，再评估 1 波 ≤2 条事件/bucket 模板。未批准前只记 `UNTESTED_COV_OK`。

### 8.1 按 ROI 排序

1. **P0：`88RKbpGl` prod 重测（一个相关性槽）**。它是目前已知唯一「单段 SHORTINTEREST + RA `checks.fail=[]` + 近十年 10/10 正 + inv 0.983」的历史件，唯一卡点是 prod 0.7908（`[H]`，2026-10-31 记录，已过 48h）。`check_correlation(refresh=True)` 占平台单并发槽；若仍 ≥0.7，按画像 §8 换轴/换窗降 prod，而不是重挖新骨架。⚠ 画像 §8:317-318 要求「数据集重启须先经用户同意」；本报告不自行开波。
2. **P1：不要先给 `0mPKMZ56` 花相关性槽**。它还有 3 项 RA FAIL + 近十年 FAIL；prod 未测不是当前唯一阻塞。先做 1 条 RA 修复实验（几何移植，`ts_rank(ts_mean(...,252),504)+market`，不带 −1；约 12 点）或直接判该构造「信号强度不足」；只有 RA 修到 S/F/2Y 接近线，prod 预判才有 ROI。
3. **P2：F2/F4 补 D2**。F2 已有 `XgaY8ZM0` 一条漂移探针；F4 marketcenter 用一条 `ts_std_dev(field,252)` 判常量即可。**任何仿真都占配额**，最多只是不占本波 2 条名额（上一版「不占正式回测槽」表述误导，已删）。
4. **P3：`shortinterest24` 长/短持仓探针**（见 §8.0 第 3 条）；未跑前 closure 门继续 FAIL。
5. **P4：不要重开 `shortinterest3` / 借贷费率族**。`gJezNxjg` 0.8791、`rKR8VZVo` 0.9592 已复证 prod 墙；台账 9 波 + 本报告 2 颗独立读数。若用户要给族级例外，必须走 waiver 并写明理由/到期。
6. **P5：组篮前先跑 `compute_mutual_correlation`**。本报告篮内 NOT RUN；`58EqmQEN` 所在 `us_short_sale` 族密集（0.92–0.94），`88R7JMxX` 有 1.0 同源副本，`0mPKMZ56` 与 `kqaL0ZGl` −1.0 ⇒ 直接拼篮必撞。
7. **P6：S6 回写**。把本战役 3 波 6 臂写入 `wave_results`（含 `dataset` / `category=SHORTINTEREST` / verdict / candidates / `full_payload`），把 `shortinterest24` 的 `UNTESTED_COV_OK` 与 `shortinterest43` 的 PROVISIONAL 写入 `registry_empirical` / `seal_dead_end` 之前先过论坛取证闸（`seal_dead_end` fail-closed）；否则下一轮会重复挖。
8. **P7：提交**。本报告 0 颗可交付；若后续出现全闸件，仍须用户点名 + `submit_verdict` 只否决 + `confirm_submit=True`，本报告不含提交动作。

---

## 9. 验证记录（本报告实际跑过的命令与结果）

| # | 命令 | 结果 | 与本报告的关系 |
|---|---|---|---|
| 1 | `world-quant-brain-mcp/.venv/Scripts/python.exe -m pytest tests/ -x` | **FAILED**：4454 collected，`1 failed, 120 passed in 21.05s`；唯一失败 `tests/unit/01_store_db/test_db_write_guards.py::TestNoNakedSqliteConnect::test_no_naked_connect_outside_whitelist`，违规 `tools/candidate_inventory_20261115.py:121: sqlite3.connect(...)`；`git status --porcelain` 该文件为 `??`（未跟踪并行会话文件） | 本报告未改代码；失败与本报告无关，但不能写「pytest 全绿」 |
| 2 | `... -m pytest tests/unit/07_docs_skills -q` | **FAILED**：`19 failed, 1391 passed, 2 skipped in 135.28s`；含 `test_sync_skills_reports_no_drift`、多条 `test_last_verified_not_older_than_last_commit`、`test_no_bak_files_inside_skills_tree`、`test_skill_lint` 基线等 | 证明 skills 侧当前有存量漂移；本报告未改 skills，不能写「docs/skills 全绿」 |
| 3 | `... tools/sync_skills.py --check` | **exit 1**：`共 3 个文件漂移，涉及 3 个安装位`；漂移文件全部是 `worldquant-submit-alpha/references/submit-chain.md`；`.claude`/`.workbuddy` `[OK]`；`.qoder-cn` 为 `.claude` junction 去重；`.cursor` 跳过 | 不能写「全部安装位一致 / 已同步 5 个」；本报告两份画像镜像 md5/sha 相同 |
| 4 | `... tools/code-audit/repo_governance_check.py` | **exit 1**：`未跟踪的源码类文件 = 121`（唯一先行指标）；`未跟踪的非源码文件 = 0`；2624 个 gitignored 源码；981 个 snapshot-unique sources | 未跟踪源文件是当前结构风险；本报告只新增一个 md（不属源码） |
| 5 | `... tools/code-audit/doc_path_refs.py` | **exit 1**：活文档 875 篇 / 候选引用 868；`BROKEN 16（基线 15）`、`UNTRACKED 13`；新增违规 `tracking/_scratch`（被 `AGENTS.md` / `README.md` / `tools/README.md` 引用） | 死指针 gate 现在红；本报告未改文档引用 |
| 6 | `... tools/waiver.py list --region USA` | **exit 0**：共 11 条，**11 条需处理（过期/无效/无到期日）**；无活跃 waiver | 11 点臂没有 op 闸 waiver 可引 |
| 7 | `md5sum` / `sha256sum` / `wc -l` 两对画像 | 两对 md5+sha256 均相同；SI43 370 行/40650 B；us_short_sale 522 行/44120 B | 镜像逐字一致 |
| 8 | MCP `batch_get_alpha_metrics`（13 ids） | `total=13 success=13 failed=0` | 指标列 `[M]` |
| 9 | MCP `get_alpha_details`（7 存量） | settings / checks / pyramids 全返回 | 设置、RA、塔段 `[M]` |
| 10 | MCP `get_alpha_yearly_stats`（13 颗） | 13/13 返回 2014–2023 逐年 | tenYear `[M]` |
| 11 | MCP `get_pyramid_alphas()` | USA.D1.shortinterest=0、USA.D0.shortinterest=0 | 塔位 `[M]` |
| 12 | MCP `get_submit_ready(region=USA,status=READY,limit=100)` | 多行；`rKR8VZVo`/`gJezNxjg` 的 `submit_ready.prod=null` 但 `alphas.prod=0.9592/0.8791`；`gJevwxg0`/`MPYwqvLn` 两者均 null；`58EqmQEN` `submit_ready.prod=0.6192` | 收割池 `[M]` |
| 13 | MCP `list_wave_results(region=USA,limit=120)` | 最新 `wave_number=344`（2026-11-08）；**返回前段未见**本战役 3 波（输出被截断，未全表检索） | S6 未完成 |
| 14 | MCP `get_campaign_summary(region=USA)` | `waves.total=389 / closed=368`、`dead_ends=80`、`submit_ready=1` | 区域态势 |
| 15 | 读 `data/dataset_assets/USA_shortinterest_coverage_audit_d1.json` | `counts={TESTED:5, UNTESTED_COV_OK:1}`；`us_short_sale.status=TESTED`、`evidence_hit_n=2`；`scope.scoped_note` 明写 6 集/category 面、region 审计停在 20/286 | 覆盖审计 `[M]` |

---

## 10. 证据清单（路径 / 行号 / 命令）

| 证据 | 值 / 结果 |
|---|---|
| `src/wqb/config.py:502` | `PRODCORR_CEILING = 0.70` |
| `src/wqb/config.py:393-407` | `RA_CHECK_NAMES` 18 项；**不含 `CLUSTER_TEST`** |
| `src/wqb/config.py:441-446` | `compute_webdata_failed_counts` 只在 `name in RA_CHECK_NAMES` 时计入失败 |
| `Claude/skills/wq-brain-ra-usa/SKILL.md:98-105` | USA 可投资性闸 `invest_S/S ≥ 0.70`；`batch_get_alpha_metrics.investability_ratio` 为唯一入口 |
| `Claude/skills/wq-brain-ra-usa/SKILL.md:116` | shortinterest 组合分支：78 回测 / 0 RA 全过 / 0 prod 已测 / 1 判死 / 1 胜绩（2026-10-04 只读汇总，早于本轮） |
| `Claude/skills/wq-brain-ra-pipeline/SKILL.md:157` | 点亮 = 本季度 3 颗 + 三对互相关 <0.5 |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/_gate_expr_checks.py:114` | `MAX_OP_CALLS = 10` |
| 同上 `:382-384` | `if n_calls >= MAX_OP_CALLS: ... FAIL` |
| `tools/gates/audit_dataset_coverage.py:113-115` | `UNTESTED_STATUSES = ("UNTESTED_BLIND","UNTESTED_COV_OK")`；`CLOSURE_BLOCKING = UNTESTED_STATUSES + ("PROBE_FAILED",)` |
| 同上 `:524-541` / `:544-557` | `gate_closure` 把 UNTESTED_COV_OK 计入；`gate_probe` 只处理 UNTESTED_BLIND / PROBE_FAILED |
| `reports/dataset_experience/usa_shortinterest_coverage_audit_20261115.md:3-10,25-58` | scope / 证据盲区 / `TESTED=5` / `UNTESTED_COV_OK=1` / coverage PASS、closure FAIL |
| `tracking/USA/reference/_usa-shortinterest43-field-profile-20261115.md:1-15` | 命名、镜像、asOf 口径 |
| 同上 `:198-235` | `88RKbpGl` S1.78/F1.12/2Y2.35/SUB1.31/inv0.983/risk_neut1.30/prod0.7908（`[H]`） |
| 同上 `:250-313` | D1–D6：D2 ❌；塔 0/3；PROVISIONAL |
| `tracking/USA/reference/_usa-us_short_sale-field-profile-20261115.md:1-40` | 4/4 全量、`filter_sharpe=false`、命名与镜像规则 |
| `output_report/USA_shortinterest_delivery_20261115.md` | 本报告 |
| `logs/test-results.xml` | 本轮 `pytest tests/ -x` 的 JUnit 结果（1 failed / 120 passed） |

> 报告结束。**本报告不提交任何 alpha；提交权归用户。**
