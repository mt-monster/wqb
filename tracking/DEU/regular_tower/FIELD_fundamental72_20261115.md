# field atlas — fundamental72 / DEU / TOP500 / D1（2026-11-15）

> 任务：单数据集的**字段面档案（S1）**——把平台实返回的字段变成可设计的语义维度、类型降维要求、覆盖/宽度读数与 ≥6 个不同机制的模板骨架。
> 性质：**只读**。本档零写库、零仿真、零提交；所有读数来自本会话 MCP 平台实读，或本地档案逐行引用（带 `path:line`）。
> 判据纪律：AGENTS.md §7.6（六维穷尽闸）、§8.11 ⑤（数据集级 coverage 不是数据存在性判据）、§8.11 ⑦（「未测」清单必须标注证据通道与盲区）、以及本档 §2 的**字段级 coverage 也不可用**实测。

---

## §0 复现命令（本会话实际调用，原样记录）

| # | 调用 | 关键返回 |
|---|---|---|
| 1 | `mcp__wq-brain-http__get_datafields(dataset_id="fundamental72", region="DEU", universe="TOP500", delay=1, filter_sharpe=false)` | `count=1031`、`platform_count=1031`、`complete=true`、`pages_fetched=21`、`results=1031` |
| 2 | `mcp__wq-brain-http__get_datasets(region="DEU", universe="TOP500", delay=1, search="fundamental72")` | `coverage=0.0`、`fieldCount=1031`、`userCount=152`、`alphaCount=286`、`valueScore=4.0`、`pyramidMultiplier=1.8` |
| 3 | 对照 A：`get_datafields(dataset_id="fundamental6", region="DEU", universe="TOP500", delay=1, max_fields=5, filter_sharpe=false)` | `platform_count=196`；5 个字段 coverage = `1.0 / 0.1544 / 0.2765 / 0.4568 / 0.3523` |
| 4 | 对照 B：`get_datafields(dataset_id="fundamental72", region="EUR", universe="TOPCS1600", delay=1, max_fields=5, filter_sharpe=false)` | `platform_count=876`；5 个字段 coverage = `0.4028 / 0.3333 / 0.26 / 0.4879 / 0.5087` |
| 5 | `mcp__wq-brain-http__get_alpha_details("mLaALJX2")` | `code` 只引用 3 个 fnd72 字段；`longCount=209`、`shortCount=173`、`sharpe=1.50`、唯一 fail = `LOW_SHARPE 1.50 < 1.58` |
| 6 | `mcp__wq-brain-http__preflight_expressions(alpha_expressions=<§6 十条骨架>, region="DEU", universe="TOP500", delay=1, dataset_id="fundamental72", auto_fix_vector=true)` | `valid=true`、`unknown_fields=[]`、`any_changed=false`、`platform_field_count=18`（引用字段数） |
| 7 | `mcp__wq-brain-http__operator_audit(expressions=<§6 十条骨架>, region="DEU", universe="TOP500")` | `safe=true`、`violations=[]`（ghost 算子清单里无本档用到的算子） |
| 8 | `mcp__wq-brain-http__get_datafields(...)` 全量落盘 | `logs/_tmp_fnd72_fields.json`（1031 行，未截断；本档全部统计基于此文件） |

> 为什么要有第 8 条：MCP 工具回传给 Agent 的结果会被结果预算截断（本次原 payload ≈ 492 KB），因此全量 payload 落到 `logs/` 再统计；统计脚本 `logs/_tmp_fnd72_analyze.py` / `_census.py` / `_check.py` 只读该 JSON。

---

## §1 平台实返回总览

| 项 | 读数 | 备注 |
|---|---|---|
| 字段总数（平台） | **1031** | `platform_count=1031`、`complete=true`、21 页拉完，无截断 |
| 类型分布 | **MATRIX 347 / VECTOR 684** | 无 `GROUP`、无 `EVENT` |
| coverage（平台字段级） | **全部 0.0（1031/1031）** | 见 §2：本集×本区的 coverage 列**不可用**，不是「没数据」 |
| userCount > 0 | **342** | 有平台用户足迹 |
| alphaCount > 0 | **333** | 有平台 alpha 足迹 |
| userCount = 0 且 alphaCount = 0 | **689** | 无任何平台足迹（≠ 不可用） |
| 本地 `query_field_profile(DEU, fundamental72)` | **0 行** | DEU 画像表整区未入库（同 `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:106`） |
| 本地 `get_field_catalog(DEU, fundamental72)` | **1031 行，与平台逐字段一致** | 本会话逐字段比对：local-only 0 / platform-only 0 / type mismatch 0 / coverage mismatch 0 ⇒ **本集本地 catalog 无幽灵字段**（仅对本集成立，不外推） |

**平台足迹头部（拥挤度，按 alphaCount 降序）**

| 字段 | 类型 | uc | ac | description（平台原文） |
|---|---|---:|---:|---|
| `fnd72_s_pit_or_cf_a_cf_cash_from_oper` | MATRIX | 72 | 114 | Annual net cash provided by operating activities |
| `fnd72_s_pit_or_bs_q_1_bs_tot_asset` | MATRIX | 17 | 31 | Total assets |
| `total_liabilities_and_equity_value` | MATRIX | 15 | 22 | Total value of liabilities and shareholders' equity. |
| `fnd72_s_pit_or_is_q_ebit` | MATRIX | 12 | 14 | Earnings before interest and taxes (EBIT) |
| `fnd72_s_pit_or_is_q_net_income` | MATRIX | 7 | 10 | Quarterly net income (net profit or loss) |
| `fnd72_s_pit_or_is_a_ebit` | MATRIX | 8 | 10 | Annual earnings before interest and taxes |
| `fnd72_s_pit_or_is_q_sales_rev_turn` | MATRIX | 7 | 9 | Quarterly revenue (sales/turnover recognized) |
| `accounts_receivable_other` | MATRIX | 6 | 10 | Value of other accounts receivable. |
| `accounts_payable_trade_amt` | VECTOR | 2 | 6 | Amount owed to suppliers for goods and services received. |

---

## §2 字段级覆盖实读（本档最重要的一条）

### 2.1 实读

`get_datafields` 对 **DEU / TOP500 / D1** 返回 1031 个字段，**每个字段的 `coverage` 都是 `0.0`**（唯一值集合 = `{0.0}`）。

### 2.2 三条对照（证明「0.0 是平台元数据问题，不是没数据」）

| 对照 | 结果 | 说明 |
|---|---|---|
| 同区同宇宙换数据集：`fundamental6`（DEU/TOP500/D1） | coverage `1.0 / 0.1544 / 0.2765 / 0.4568 / 0.3523` | ⇒ 该接口在本区**能**给出非零字段覆盖率 |
| 同数据集换区：`fundamental72`（EUR/TOPCS1600/D1） | coverage `0.4028 / 0.3333 / 0.26 / 0.4879 / 0.5087` | ⇒ 本数据集的 coverage 在别的区**能**被填充 |
| 真实回测：`get_alpha_details("mLaALJX2")` | `longCount=209 / shortCount=173` | ⇒ DEU/TOP500/D1 上**确有持仓**，数据存在 |

**结论**：本集在本区（fundamental72 × DEU × TOP500 × D1）的 `coverage` 列是**退化的**——它既不能判「可用」，也不能判「不可用」。本档的宽度判断一律改用「有平台足迹的字段 + 探针 longCount/shortCount + 历史回测实证」，**不使用 coverage 数值**。
（这与 AGENTS §8.11 ⑤ 的「数据集级 coverage 不可作判据」同型，但更进一层：**这里的字段级 coverage 也不可用**。历史档案已记同一矛盾：`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:107`。）

### 2.3 历史实测的宽度证据（本地档案，非本会话重测）

| 事实 | 数值 | 出处 |
|---|---|---|
| CF 明细 / 部分 BS 明细在 DEU/TOP500 | 覆盖 **<2%**（2–5 只），宽度 ≤5 时 CW(limit 0.1) 结构性必挂 | `tracking/DEU/atom_orthogonal/S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:59`（死档 `DEU-FND72-CF-DETAIL-SPARSE` id 1573） |
| 年报字段宽面 | 仅 **12–14%** 覆盖（60–70/500），可用子集只有 TA+CFO+NI | 同上 `:60`（死档 `DEU-FND72-NARROW-BREADTH` id 1574） |
| 唯一已出货的宽面 | IS 季度标量族（`fnd72_s_pit_or_is_q_*`），`mLaALJX2` LC 209 / SC 173 | `tracking/DEU/regular_tower/S0_TOWER_SCAN_20261115.md:79,:121` + 本会话 `get_alpha_details` 重读 |

> ⚠ 死档只给了**族级**表述（「CF 明细/部分 BS 明细」），**没有逐字段列名**。因此「哪些具体字段塌缩」不能从档案推断，只能靠探针确认——本档 §5 给候选族与探针方式，不给伪造的字段名单。

---

## §3 语义维度（按 description 归纳；字段名不作语义依据）

| # | 语义维度 | 代表字段（平台实返回，描述为准） | 经济含义 |
|---|---|---|---|
| D1 | 资产存量与结构 | `fnd72_s_pit_or_bs_q_1_bs_tot_asset`（Total assets，MATRIX）、`fnd72_pit_or_bs_a_bs_tot_asset`（Total assets on the balance sheet，VECTOR）、`fnd72_pit_or_bs_a_bs_cur_asset_report`（Total current assets）、`fnd72_pit_or_bs_a_bs_inventories`（Inventory balances） | 规模与资产结构；**比率型信号的分母主口径** |
| D2 | 负债与融资 | `fnd72_pit_or_bs_a_bs_lt_borrow`（Total long-term debt obligations due beyond one year）、`fnd72_pit_or_bs_a_bs_st_borrow`（Short-term borrowings and debt due within one year）、`fnd72_s_pit_or_bs_q_1_bs_def_tax_liab`（Net long-term deferred tax liabilities） | 杠杆水平、再融资结构 |
| D3 | 权益与股本 | `fnd72_pit_or_bs_a_bs_tot_eqy`（Total shareholders' equity）、`fnd72_pit_or_bs_a_bs_pure_retained_earnings`（Retained earnings）、`fnd72_s_pit_or_bs_q_1_bs_sh_out`（Shares outstanding at period end）、`fnd72_pit_or_bs_a_bs_num_of_tsy_sh`（Number of shares held in treasury） | 账面价值、留存、稀释/回购 |
| D4 | 利润表流量 | `fnd72_s_pit_or_is_q_ebit`、`fnd72_s_pit_or_is_q_is_oper_inc`、`fnd72_s_pit_or_is_q_net_income`、`fnd72_s_pit_or_is_q_sales_rev_turn`、`fnd72_s_pit_or_is_a_ebit`、`fnd72_s_pit_or_is_a_net_income` | 盈利水平与规模；**本集唯一已出货的宽面族** |
| D5 | 费用结构与经营杠杆 | `fnd72_s_pit_or_is_q_is_cogs_to_fe_and_pp_and_g`（cost of revenue）、`fnd72_s_pit_or_is_q_is_sga_other_op_depr_op_maint`（SG&A + 其他经营费用）、`fnd72_s_pit_or_is_q_is_personnel_exp`（personnel expenses）、`fnd72_s_pit_or_is_q_is_rd_expend`（R&D） | 成本刚性、毛利率、研发投入 |
| D6 | 现金流 | `fnd72_s_pit_or_cf_a_cf_cash_from_oper`（Annual net cash from operating）、`fnd72_s_pit_or_cf_a_cf_cap_expend_prpty_add`（capital expenditures）、`fnd72_s_pit_or_cf_a_cf_depr_amort`（D&A 非现金回加）、`fnd72_s_pit_or_cf_q_cf_cash_from_oper`（季度 CFO） | 现金创造与再投资强度 |
| D7 | 应计与营运资本 | `fnd72_s_pit_or_cf_a_cf_net_inc`（CF 表起点净利）、`fnd72_s_pit_or_cf_a_cf_chng_non_cash_work_cap`、`fnd72_s_pit_or_cf_a_cf_change_in_inventories`、`fnd72_s_pit_or_cf_a_cf_acct_rcv_unbilled_rev` | 应计/收入质量（**CF 明细=宽度风险最高区**） |
| D8 | 税项 | `deferred_tax_assets_long_term`（DTA, MATRIX）、`fnd72_s_pit_or_bs_q_1_bs_def_tax_liab`（DTL, MATRIX）、`fnd72_s_pit_or_is_q_is_inc_tax_exp`（账面税费用）、`fnd72_s_pit_or_cf_a_cf_cash_paid_for_tax`（实付现金税） | 账面税 vs 现金税、递延税项的跨期反转 |
| D9 | 养老金与离职福利 | `fnd72_s_pit_or_is_a2_is_projected_benefit_obligation`（PBO）、`fnd72_s_pit_or_is_a2_is_fair_value_plan_assets`（计划资产公允价值）、`fnd72_s_pit_or_is_a2_is_over_underfund_pension_exp`（资金缺口）、`fnd72_s_pit_or_is_a2_is_disc_rate_pension_plan_liabs`（折现率） | 表外负债、未来缴款对 FCF 的侵蚀 |
| D10 | 租赁与表外承诺 | `fnd72_pit_or_bs_a_bs_rental_exp_year_1..5`、`fnd72_pit_or_bs_a_bs_rental_exp_beyond_year_5`、`fnd72_pit_or_bs_a_bs_future_min_oper_lease_oblig` | 表外固定成本、租约期限结构 |
| D11 | 银行/保险专用 | `customer_deposits_balance`（deposits from customers）、`aggregate_loan_balance`（all loans held）、`core_capital_ratio`（核心资本/风险加权资产）、`nonperforming_loans_balance_2`；`unearned_insurance_premiums_4`、`deferred_policy_acquisition_costs`、`embedded_value_amount` | 金融子公司专属；**对非金融股恒 0 ⇒ 天然窄面** |
| D12 | 元数据 / 非信号 | `fnd72_pit_or_bs_a_announcement_dt`（公告日）、`fnd72_pit_or_bs_a_latest_period_end_dt_full_record`（期末日）、`fnd72_pit_or_cf_a_fiscal_year_period`（财年季度标识）、`reporting_currency_code_41`（报告币种）、`fnd72_pit_or_cf_a_id_bb_global`（证券标识） | 日期/标识/币种：**不可进 rank**，只可用于时间对齐与截面筛选 |

---

## §4 类型与降维要求

### 4.1 只有两种类型，但**分层方式决定降维成本**

| 前缀桶 | 字段数 | 类型 | 说明 |
|---|---:|---|---|
| `fnd72_s_pit_or_is_*`（标准化 IS） | 134 | **全 MATRIX** | 利润表：季度 `_q_` / 年度 `_a_` / 补充 `_a2_`·`_a3_`；**唯一出货族** |
| `fnd72_s_pit_or_bs_*`（标准化 BS） | 61 | **全 MATRIX** | 资产负债表标准层，全部有 alphaCount>0 |
| `fnd72_s_pit_or_cf_*`（标准化 CF） | 59 | **全 MATRIX** | 现金流标准层，全部有 alphaCount>0 |
| `fnd72_pit_or_bs_*`（原始 BS） | 158 | **全 VECTOR** | as-reported 多值层（分行/分部/重述）→ **必须 `vec_*` 降维** |
| `fnd72_pit_or_cf_*`（原始 CF） | 37 | **全 VECTOR** | 同上 |
| 通用名（无前缀，如 `total_liabilities_and_equity_value`） | 560 | VECTOR 483 / MATRIX 77 | 另一套供应商口径，**多数为 VECTOR** |
| `ard_*`（ARD 标准化） | 18 | MATRIX 12 / VECTOR 6 | 第三套口径，与 `s_`/原始层并存 |
| `fnd72_*` 其他 | 4 | MATRIX 4 | — |

**读数含义**：`s_` 标准化层（IS+BS+CF，254 个字段）**全部是 MATRIX，可直接进算子**；原始 `pit_or_*` 层（BS+CF，195 个）**全部是 VECTOR**，必须降维。这解释了为什么已出货件全部落在 `s_` 层。

### 4.2 VECTOR 降维写法

- 平台字段 `type=VECTOR` 时，裸露使用会在预检/仿真阶段报错或被自动包裹；本档全部 VECTOR 处显式写 `vec_avg(...)`（本仓最高频：`vec_avg` 9934 处；次为 `vec_sum` 2775、`vec_stddev` 963、`vec_count` 937、`vec_max` 453、`vec_range` 264、`vec_min` 223，来源：本会话对仓库 `*.md/*.py/*.json` 的 `rg -o "vec_[a-z_]+"` 计数）。
- **默认 `vec_avg`**（多值取均值 = 公司层代表值）；只有语义明确要求「总量」时才用 `vec_sum`（例如分部加总），要求「离散度」时用 `vec_stddev`。
- 证据：`preflight_expressions` 对 §6 十条骨架返回 `any_changed=false`、`wrapped_fields=[]` ⇒ **显式 `vec_avg` 已足够，未触发自动修复**。

### 4.3 无 GROUP / 无 EVENT

- 平台返回里 **`type` 只有 MATRIX 与 VECTOR**（`Counter({'VECTOR': 684, 'MATRIX': 347})`），没有 `GROUP`、没有 `EVENT`。
- 因此本集**不存在** GROUP 型 `field_group` 维度（本地 catalog 的 `field_group` 也全为 `null`），分组轴只能用平台内置 `sector` / `industry` / `subindustry` / `market` / `bucket`。
- 也不存在 `ts_event_*` 问题：本集**没有任何事件型字段**可供误用。

---

## §5 更新频率、宽度塌缩与阻断字段

### 5.1 更新频率（平台不返回 frequency 字段）

`get_datafields` 的返回结构只有 `id/type/coverage/userCount/alphaCount/description`，**没有更新频率字段**。唯一可读的频率证据在 description 文本里：

| 描述里的频率标记 | 字段数 |
|---|---:|
| 含 `annual` | **91** |
| 含 `quarterly` / `quarter` | **52** |
| 两者都未标注 | **888** |

⇒ **888 个字段的频率不可从平台返回推断**；不要按字段名里的 `_a_` / `_q_` 猜（命名不作语义依据）。设计慢信号前，只能看 description 或先探针。

### 5.2 宽度塌缩（按证据强度排序）

| 类别 | 规模/证据 | 处置 |
|---|---|---|
| **字段级 coverage 退化** | 1031/1031 = 0.0（§2） | 不作宽度判据 |
| **CF 明细 / 部分 BS 明细** | 历史实测覆盖 <2%（2–5 只），CW(0.1) 结构性必挂（死档 id 1573，`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:59`） | 除 `cf_net_inc` / `cf_cash_from_oper` / BS 主表合计行外，**先跑 1 条 `rank(<field>)` 探针验 LC+SC ≥50 再派** |
| **年报宽面** | 12–14% 覆盖（60–70/500）（死档 id 1574，`:60`） | 年报骨架必须探针；本文档 §6 中 T1/T2/T4 均落此区 |
| **689 个零足迹字段** | userCount=0 且 alphaCount=0（本会话实读 689） | 「零足迹」只说明没人用过，**不等于不可用**；但也**没有**任何可用性证据 |
| **元数据/标识字段** | 42 个（id 含 `_announcement_dt`/`_fundamental_entry_dt`/`_latest_period_end_dt`/`_fiscal_year_period`/`reporting_currency_code`/`form_of_statement`/`id_bb_global`/`eqy_fund_crncy`；MATRIX 26 / VECTOR 16） | 日期/字符串类，`rank` 后基本是常数或噪声 ⇒ **禁作信号**，只用于时间对齐 |
| **同描述冗余簇** | 81 簇 / 176 字段（同 description 逐字相同，如「Total current assets」3 个、`latest_period_end_dt_full_record` 6 个） | 同簇内**只取一个**，否则等于重复计权 |
| **VECTOR 未降维** | 684 个 | 必须 `vec_*`，见 §4.2 |
| **金融子公司专属** | 银行/保险字段（deposits/loans/premiums 等） | 对非金融股恒 0 ⇒ 只在金融子集内使用，或先探针 |

### 5.3 阻断字段清单（本档点名）

1. **拟用名不存在（本会话踩到的两个）**：`fnd72_pit_or_bs_q_1_bs_tot_asset`、`fnd72_pit_or_cf_q_cf_form_of_statement` —— 平台 1031 字段里**没有**这两个 id。前者正确的 id 是 `fnd72_s_pit_or_bs_q_1_bs_tot_asset`（`s_` 层 MATRIX）。**写表达式前必须查 §1 的 id，不要按命名规则拼。**
2. **元数据 42 字段**（§5.2 行 5）：禁作信号。
3. **CF / BS 明细族**：未探针前不派（死档 id 1573 的硬边界）。
4. **裸 `rank(单字段)` 形态**：DEU fundamental 类别卡禁止裸 `rank(fundamental_score)`，必须 `group_neutralize` / `group_rank` / `group_zscore`（`Claude/skills/wq-brain-ra-deu/references/fundamental.md:61`）。

---

## §6 模板骨架（10 个不同机制；全部经平台预检）

> 共性：单数据集单信号腿（不与其他数据集相加）、`group_rank(..., sector)` 收口、`sector` 为平台内置分组、无幽灵算子。
> 验证据：`preflight_expressions` → `valid=true` / `unknown_fields=[]` / `any_changed=false`；`operator_audit` → `safe=true` / `violations=[]`。
> 配置建议（家族实测，**不是类别规则**）：先用 **FAST 中性化 + decay 0**（`mLaALJX2` 配置；SUBINDUSTRY 在 fnd72 动量族三波 25 臂证死，见 `NEARGATE_BREAK_GRID_FND72_20261115.md:3`）；年频字段窗口 ≥504，季频 252 / 66 两档。
> **所有「预期符号」都是待验证假设**，不是结论；每条都附「与已测机制的关系」，避免在 wave107（10 模板，`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:60`）与 11-15 动量网格（51 臂，`NEARGATE_BREAK_GRID_FND72_20261115.md`）上换皮重跑。

### T1 养老金资金缺口（表外杠杆）

```
group_rank(divide(subtract(fnd72_s_pit_or_is_a2_is_fair_value_plan_assets,
                           fnd72_s_pit_or_is_a2_is_projected_benefit_obligation),
                  fnd72_s_pit_or_bs_q_1_bs_tot_asset), sector)
```
- **机制**：设定受益计划的「计划资产 − 给付义务」= 资金盈余/缺口；缺口是债务型义务，会以未来缴款形式侵蚀 FCF，且不在常规杠杆率里。
- **预期符号**：正（资金越充裕越做多，缺口越大越做空）。
- **数据风险**：`a2_` 年频明细，落在年报 12–14% 宽度区（§5.2）。**先探针** `rank(fnd72_s_pit_or_is_a2_is_over_underfund_pension_exp)` 验 LC+SC ≥50。
- **与已测机制关系**：未测族（`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:69` 记 `is_a2` 养老金族零本地实测）。

### T2 租赁承诺强度（表外固定成本）

```
group_rank(divide(vec_avg(fnd72_pit_or_bs_a_bs_future_min_oper_lease_oblig),
                  vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), sector)
```
- **机制**：未来最低经营租赁付款 / 总资产 = 表外固定成本负担；负担越重，经营下行时的利润弹性越差（与 IFRS16 前的「隐藏杠杆」同类）。
- **预期符号**：负（强度越高越做空）。
- **数据风险**：原始 BS 层 VECTOR + 年频明细，属 §5.2 的高风险区。必须探针；若 LC+SC <50，改用 `fnd72_pit_or_bs_a_bs_curr_rental_expense` 或放弃。
- **变体（期限结构）**：`divide(fnd72_pit_or_bs_a_bs_rental_exp_beyond_year_5, fnd72_pit_or_bs_a_bs_rental_exp_year_1)`（长租约占比 = 承诺久期）。

### T3 递延税项净负债（账面税 vs 应税税的时间差）

```
group_rank(divide(subtract(fnd72_s_pit_or_bs_q_1_bs_def_tax_liab, deferred_tax_assets_long_term),
                  fnd72_s_pit_or_bs_q_1_bs_tot_asset), sector)
```
- **机制**：递延税负债净额（DTL−DTA）反映「会计利润已确认、应税利润未确认」的累计差额；该差额持续升高意味着当期账面盈利质量偏低、未来会反转成现金税。
- **预期符号**：负（DTL 净额越高越做空）。
- **数据风险**：两个字段都在**标准层 MATRIX**（`s_` BS 层 61 字段全部有 alphaCount>0），风险低于 T1/T2；仍建议 1 条探针。
- **与已测机制关系**：wave107 的 Piotroski / Sloan 应计用的是年报三表组合，**未单测递延税项**；且本式用季度标准层，与年报宽面无关。

### T4 净外部融资（发债/偿债，外部融资异象）

```
group_rank(divide(subtract(fnd72_s_pit_or_cf_a_cf_incr_lt_borrow,
                           fnd72_s_pit_or_cf_a_cf_reimb_lt_borrow),
                  fnd72_s_pit_or_bs_q_1_bs_tot_asset), sector)
```
- **机制**：净长期借款（新发 − 偿还）是「外部融资异象」的经典代理——靠外部融资扩张的公司，后续回报系统性偏低；偿债则相反。
- **预期符号**：负（净发债越多越做空）。
- **数据风险**：**两条 CF 融资明细，正落在死档 id 1573 的 <2% 排除区**。**必须先探针** `rank(fnd72_s_pit_or_cf_a_cf_incr_lt_borrow)` 验 LC+SC ≥50；不达标就换 BS 主表版本（`ts_delta(vec_avg(fnd72_pit_or_bs_a_bs_lt_borrow), 252)`），若仍窄则本条作废。
- **与已测机制关系**：wave107 十模板不含外部融资/净发债；11-15 网格只做动量族。

### T5 费用粘性（成本刚性 / 经营杠杆）

```
group_rank(ts_delta(divide(add(fnd72_s_pit_or_is_q_is_sga_other_op_depr_op_maint,
                               fnd72_s_pit_or_is_q_is_personnel_exp),
                          fnd72_s_pit_or_is_q_sales_rev_turn), 252), sector)
```
- **机制**：经营费用率（SG&A+人工）/ 收入的变化 = 成本粘性；收入下行而费用率上升的公司，利润被经营杠杆放大地下杀。
- **预期符号**：负（费用率上升越做空）。
- **数据风险**：IS 季度标量族，**本集最宽的面**（`is_q_*` 118/134 有 alphaCount>0），风险低。`is_personnel_exp` 只有 uc=1，可先用不含人工的 SGA-only 版本做对照。
- **与已测机制关系**：11-15 网格只做 EBIT/assets 的动量，未做费用率；wave107 无费用粘性。

### T6 毛利率轨迹（定价权）

```
group_rank(ts_delta(divide(subtract(fnd72_s_pit_or_is_q_sales_rev_turn,
                                   fnd72_s_pit_or_is_q_is_cogs_to_fe_and_pp_and_g),
                          fnd72_s_pit_or_is_q_sales_rev_turn), 252), sector)
```
- **机制**：毛利率的年度变化，测的是定价权/成本转嫁能力；与 T5 的差别在**收入侧**（毛利）而非费用侧（经营费用率），二者可同时为真、也可背离（涨价但费用失控）。
- **预期符号**：正（毛利率扩张越做多）。
- **数据风险**：IS 季度标量，风险低；`is_cogs_to_fe_and_pp_and_g` uc=1，属零竞争字段。
- **与已测机制关系**：未测（wave107 的「折旧强度」是资产侧，不是毛利率）。

### T7 投资收益占税前利润比（盈利构成质量）

```
group_rank(divide(fnd72_s_pit_or_is_q_is_invest_income,
                  fnd72_s_pit_or_is_q_pretax_inc), sector)
```
- **机制**：税前利润里来自投资收益（非主业）的占比；占比越高，盈利的持续性与可预测性越差（核心经营利润被"埋没"）。
- **预期符号**：负（非主业占比越高越做空）。
- **数据风险**：IS 季度标量，风险低；注意 `pretax_inc` 可能为负，比值符号会翻转 ⇒ 建议加 `trade_when(fnd72_s_pit_or_is_q_pretax_inc > 0, <上式>, 0)` 作为变体，避免负分母污染。
- **与已测机制关系**：未测；wave107 的「回归残差」是统计残差，不是利润构成。

### T8 股份稀释 / 回购（净发行异象）

```
group_rank(ts_delta(divide(fnd72_s_pit_or_bs_q_1_bs_sh_out,
                           fnd72_s_pit_or_bs_q_1_bs_tot_asset), 504), sector)
```
- **机制**：股本 / 总资产在 2 年窗口的变化；上升 = 净发行（摊薄），下降 = 回购。净发行异象：发行方后续回报偏低。
- **预期符号**：负（净发行越做空；等价地，回购为正）。
- **数据风险**：标准层 BS MATRIX（61/61 有足迹），风险低。**不要用 `num_of_tsy_sh` 原始 VECTOR 版本**（年频、且在 <2% 区）。
- **变体（回购强度水平）**：`divide(fnd72_s_pit_or_bs_q_1_bs_amt_of_tsy_stock, fnd72_s_pit_or_bs_q_1_bs_tot_eqy)`（库存股占权益比，累计回购强度）。

### T9 现金流的稳定性（盈利风险）

```
group_rank(multiply(-1, ts_std_dev(divide(fnd72_s_pit_or_cf_q_cf_cash_from_oper,
                                          fnd72_s_pit_or_is_q_sales_rev_turn), 252)), sector)
```
- **机制**：季度 CFO/收入 的时序波动 = 现金创造的不确定性；波动越高，折现率越高、估值越低。
- **预期符号**：正（本式已乘 −1：波动越低越做多）。
- **数据风险**：`cf_q_*` 族属 CF 标准层（59/59 有足迹），但「CF q 族」在 `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:69` 被记为**零本地实测** ⇒ 本式是该族的首个实测件，先探针再上批量。
- **与已测机制关系**：wave107 的「现金转化率」「FCF」是**水平/比率**，不是**二阶波动**；D3 口径下这是新的矩。

### T10 其他应收款占比（应收质量/关联方风险）

```
group_rank(divide(accounts_receivable_other, fnd72_s_pit_or_bs_q_1_bs_tot_asset), sector)
```
- **机制**：「其他应收款」区别于贸易应收，通常包含关联方往来、预付款、非经营性占款；占比异常高是盈余质量与治理风险的经典红旗。
- **预期符号**：负（其他应收占比越高越做空）。
- **数据风险**：`accounts_receivable_other` 是**通用名 MATRIX**（uc 6 / ac 10，非 `fnd72_` 前缀），属 `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:69` 记的「通用名 MATRIX 族零本地实测」；先探针。
- **与已测机制关系**：wave107 的 Sloan 应计用总应计，未拆「其他应收」这一治理红旗子项。

### 6.1 与已测机制的排重（避免换皮重跑）

| 已测机制 | 出处 | 本档是否重复 |
|---|---|---|
| Sloan 应计 / FCF / 现金转化率 / 应计-CF 相关性倒 U / 三表 regime / Piotroski / 回归残差 / 留存收益 / 折旧强度 | wave107 十模板（死档 id 1574；`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:60`） | **不重复**（T3 递延税、T7 利润构成、T9 二阶波动、T10 其他应收均非上述九类） |
| EBIT/oper_inc ÷ total_asset 的三窗 delta×ts_rank×group_rank 动量（tail/winsorize/hump/带宽/窗位） | 11-15 网格 51 臂 + `mLaALJX2`（`NEARGATE_BREAK_GRID_FND72_20261115.md`） | **不重复**（本档无一条是「同一比率的双窗 delta × ts_rank 三腿相乘」；T5/T6/T8 只是对单一比率做一阶差） |

---

## §7 本档未覆盖 / 下一轮可补（D2 口径）

| 未实测族（`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:69` 原列） | 本档进展 | 仍缺 |
|---|---|---|
| IS 年度标量族（`is_a_ebit` / `is_a_net_income` / `is_a_sales_rev_turn`，uc 5–8） | 未出骨架（T1 借用了 `a2_`，非 `a_`） | 至少 1 条 `a_` 骨架 + 宽度探针 |
| CF q 族（`fnd72_s_pit_or_cf_q_*`） | **T9 覆盖首条** | 覆盖探针 + 第二条机制（如 CFO/资产） |
| BS q_1 / q_2 全族 | **T3 / T8 各覆盖 1 条** | 其余明细行仍未测 |
| 通用名 MATRIX 族 | **T10 覆盖 1 条**（`accounts_receivable_other`） | `total_liabilities_and_equity_value` 等头部拥挤字段未测 |
| 银行/保险专用族（§3 D11） | 未出骨架 | 需先确认 DEU TOP500 金融股权重，再定是否值得 |
| VECTOR 原始层（`pit_or_bs_*` 158 + `pit_or_cf_*` 37） | T2 用了 1 条（带探针前置） | 其余未测；先判宽度 |

---

## §8 证据通道与盲区（AGENTS §8.11 ⑦）

| 通道 | 本会话具体调用 | 覆盖什么 | 对什么盲视 |
|---|---|---|---|
| 平台字段目录 | `get_datafields`（21 页全量） | 字段 id / type / coverage / userCount / alphaCount / description | **不含更新频率**；`coverage` 在本集×本区退化为全 0（§2） |
| 平台数据集元信息 | `get_datasets(search="fundamental72")` | fieldCount / userCount / alphaCount / valueScore / pyramidMultiplier | `description` 与其它数据集错配（平台已知问题：`docs/reference/EUR/datasets/fundamental72.md:23` 记「平台目录描述存在错配」）——**本档不引用该 description** |
| 平台 alpha 详情 | `get_alpha_details("mLaALJX2")` | code 引用了哪些字段、LC/SC、checks | 只看 1 条，不是全池扫描 |
| 平台预检 | `preflight_expressions` + `operator_audit` | 字段存在性、VECTOR 包裹、幽灵算子 | **不验数据宽度**（预检不做仿真，不返回 LC/SC） |
| 本地 DB 画像 | `query_field_profile(DEU, fundamental72)` = 0 行；`get_field_catalog` = 1031 行 | catalog 缓存 | **DEU 画像表整区为空** ⇒ 无本地历史绩效先验 |
| 本地档案 | `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md` / `S0_TOWER_SCAN_20261115.md` / `NEARGATE_BREAK_GRID_FND72_20261115.md` | 判死档 payload、宽度实测、已测机制清单 | 档案是他人槽位产物，可能滞后；关键读数本会话已用平台重核（字段数、LC/SC、alpha code） |

**本档没有做的事（如实登记）**：没有跑任何仿真探针（因此**没有**本会话实测的 per-field longCount/shortCount）；§5.2 的「<2%」「12–14%」是历史档案数值，不是本会话读数；§6 十条骨架只过了**语法/字段/算子预检**，**未回测**，预期符号全部待验证。

---

## §9 一句话交接

**fnd72 在本区是「千字段、单层可用」的结构**：1031 个字段里真正已验证有宽度的是 `s_` 标准化层（IS/BS/CF 共 254 个 MATRIX，`mLaALJX2` LC 209/SC 173 证明数据存在），原始 `pit_or_*` 层 195 个全 VECTOR 且年频明细多落在 <2% 宽度区；平台 `coverage` 列在本集×本区全为 0，**不可作任何可用性判据**（三条对照 + 真实持仓已证伪「0=没数据」）。下一轮设计应优先走 §6 的 T3/T5/T6/T7/T8/T9/T10（标准层、低宽度风险），T1/T2/T4 必须先探针。
