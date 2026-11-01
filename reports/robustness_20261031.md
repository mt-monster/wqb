# DEU 提交篮稳健性审计 — 2026-01-31（数据日期 2023-12-29）

审计对象：提交篮 3 颗（MPY9VNY9 / Vkxnb8QG / QPveY7Kg）。
方法：brain-alpha-robustness Phase B（权威指标 + 逐年 stats + PnL）→ Phase C 闸门判定。
数据源：get_alpha_details（顶层权威指标）/ get_alpha_yearly_stats（逐年 Sharpe，IS 2014-2023）。

## 判定汇总

| alpha | 机制 | IS S/F | 近3年 S (21/22/23) | CV3 | 衰减比 (23年/IS) | 负年 | 平年(<0.5) | margin@TVR | **verdict** |
|---|---|---|---|---|---|---|---|---|---|
| MPY9VNY9 | shrt3_bar 双窗 delta 交互 | 1.59 / 1.26 | 2.08 / 3.42 / 1.78 | **0.36** ✓ | **1.12** ✓ | 1 (2016) | 2 (2018-19) | 43.2bp @ 3.6% ✓✓ | **PASS** |
| Vkxnb8QG | eps_y1 + trade_when 借券费率门控 | 1.83 / 1.64 | 2.74 / 0.56 / 0.54 | **0.99** ✗ | **0.295** ✗ | 0 | 0 | 12.8bp @ 17.7% ✓ | **REJECT** |
| QPveY7Kg | snt7+snl27 vector_neut | 2.03 / 1.61 | 2.66 / 4.22 / 1.18 | **0.57** △ | **0.58** ✓ | 1 (2020) | 1 | 33.7bp @ 12.4% ✓ | **CONDITIONAL** |

## 逐颗明细

### MPY9VNY9 — PASS
- 逐年 Sharpe：0.73 / 2.87 / **-1.22** / 0.66 / 0.47 / 0.36 / 3.29 / 2.08 / 3.42 / 1.78
- 近 3 年（2021-2023）全部显著为正，合计 7.28；2023 年 1.78 高于全期 1.59 ⇒ 无衰减。
- Margin 43.16bp @ 换手仅 3.60% —— 全篮最高性价比，交易成本极低。
- soft_flags：2016 负年（-1.22，隔年即回正）；2018-2019 连续两年 0.36-0.47 平年（其后 2020 起连续 4 年强）。
- 结构：decay1 + tvrd 0.03 + NaN ON；单数据集 atom（shortinterest3），无塔混。

### Vkxnb8QG — REJECT（两条硬指标踩 REJECT 线）
- 逐年 Sharpe：0.55 / 2.05 / 3.19 / 1.60 / 0.87 / 1.99 / 1.35 / **2.74 / 0.56 / 0.54**
- **近 3 年 CV = 0.99 > 0.85 ⇒ REJECT**（2021 2.74 高，2022-2023 连续两年 0.54-0.56 塌陷）。
- **衰减比 0.54/1.83 = 0.295 < 0.30 ⇒ REJECT**（2023 年仅为全期三成）。
- 衰减模式是「2021 冲高后逐年塌」——eps_y1（年频 EPS 水平）主信号 + 借券费率 trade_when 门控的组合在近两年失效。
- margin 12.82bp @ 17.67% TVR 尚可，但收益集中度高（CLUSTER_TEST warning）。
- **处置**：按技能流程 REJECT 可修复 ≤2 轮（Mode A 参数 / Mode B 换概念）；本轮不再投入回测额度，从即刻可提名单除名、降入修复池。若后续修复，须重新过完整审计。

### QPveY7Kg — CONDITIONAL
- 逐年 Sharpe：**NaN×5（2014-2018）** / 0.41 / **-0.02** / 2.66 / 4.22 / 1.18
- 近 3 年 CV 0.57（CONDITIONAL 档 0.40-0.85）；2023 年 1.18 / 全期 2.03 = 0.58 ✓ 无深度衰减。
- soft_flags：① **2014-2018 连续 5 年空窗（leading gap）** —— 覆盖口径裁定未落地（问卷自动选项「保留」未经用户确认）；② 2020 年 -0.02 平年；③ 有效历史仅 2019 起 5 年。
- margin 33.68bp @ 12.43% TVR 良好；self 0.0242 / prod 0.6671 全过。
- **处置**：待 leading-gap 裁定 + 修复轮（可选：换快门控或加衰减保护提高 2023 腿）后再定去留。

## 补充：Vkxnb8QG 修复可行性诊断（零成本证据，2026-10-31）

**问题**：Vkxnb8QG 的 2022-2023 塌陷是主信号衰减还是门控腿失效？
**证据**：eps_y1 四兄弟（同主信号、无 trade_when 门控）逐年 Sharpe——

| alpha | 2021 | 2022 | 2023 | 近3年 CV | self vs 已提交 2rjrMZ25 |
|---|---|---|---|---|---|
| kqJqQL08 | 3.16 | 1.78 | 1.53 | 0.41 | **0.986 ✗** |
| RREXxW6z | 3.09 | 2.17 | 1.52 | 0.35 | **1.000 ✗** |
| 6Xdx65eK | 3.14 | 1.83 | 1.61 | 0.36 | （同族 0.97+ 传递撞死） |
| 1YNv8qaK | 3.36 | 1.73 | 1.51 | 0.43 | （同族 0.97+ 传递撞死） |
| **Vkxnb8QG**（带门控） | 2.74 | **0.56** | **0.54** | **0.99** | 0.64 ✓ |

**结论**：
1. **eps_y1 主信号健康**——四兄弟 2022-2023 全部 1.5-2.2，无衰减。塌陷源 = `trade_when` 借券费率门控腿（2022-2023 利率环境剧变，门控把好的持仓过滤掉了）。
2. **但同骨架顶替路已死**：四兄弟互相关 0.97-0.99（同一本体），且全部撞已提交的 `2rjrMZ25`（self 0.99-1.0）。eps_y1 裸族已被提交占位钉死，整族不可再提。
3. **结构性死结**：带门控 → self 过（0.64）但稳健性 REJECT；不带门控 → 稳健性好但 self 撞死。唯一出路是换全新门控概念造新表达式（本质新 alpha，需全链重跑 + prod 风险未知）——挖掘侧已收口，此项留待用户裁定优先级，不自作主张烧额度。

## 结论与提交建议

1. **MPY9VNY9 稳健性 PASS，可提交**（仍需用户明确授权）。
2. **Vkxnb8QG 稳健性 REJECT，除名**——即刻可提名单从 2 颗降为 1 颗。
3. **QPveY7Kg CONDITIONAL**，等 leading-gap 裁定。
4. 台账：`robustness_MPY9VNY9` / `robustness_Vkxnb8QG` / `robustness_QPveY7Kg` 已写入 DEU ledger。

## QPveY7Kg 修复轮 R1（单杠杆×3，2026-10-31 晚）

**预锁验收标准**（派发前锁定，防挑数）：近3年 CV 从 0.57 降 **且** S/F 不劣于 2.03/1.61 → 入稳健性复审；否则修复失败维持 CONDITIONAL。

| 变体 | 单杠杆 | S | F | 2Y | TO | margin | CV3 | 衰减比 | failed_ra |
|---|---|---|---|---|---|---|---|---|---|
| QPveY7Kg（基准） | decay2/trunc0.02/ts_ir22 | 2.03 | 1.61 | 2.54 | 16.1% | 12.6bp | 0.566 | 0.581 | 0 |
| **mLox6Mg2** | **decay 2→4** | **2.05** | **1.71** | 2.53 | **14.73%** | **13.91bp** | 0.582 | 0.546 | 0 |
| 0mYKXjpr | truncation 0.02→0.08 | 1.96 | 1.52 | 2.46 | 16.69% | 12.05bp | 0.572 | 0.571 | 0 |
| 0mYKXjKp | ts_ir 22→66 | 1.34 | 0.98 | 1.39 | 9.16% | 14.67bp | — | — | **3（闸全挂）** |

**归因**：
1. **CV3 三杠杆全平**（0.572 / 0.582 vs 基准 0.566）——预锁标准要求 CV 降，无一达成 ⇒ **R1 判修复失败，QPveY7Kg 维持 CONDITIONAL**。
2. CV3 不可修的机理：三变体逐年路径与原条几乎一致（2019 2.2-2.3 / 2020≈0 / 2021 2.7-2.8 / 2022 4.2-4.3 / 2023 1.1-1.2），CV 由 **2022→2023 塌陷**主导，是信号本体年度路径属性，设置轴动不了它。
3. ts_ir 66 死杠杆（S/F/2Y 三闸齐挂）；truncation 0.08 全面略退；**decay 4 是唯一全面改善的设置**（S+0.02 / F+0.10 / TO-1.4pp / margin+1.3bp / sub+0.09），若未来走提交用 **mLox6Mg2** 替代原条。
4. **修复线关闭**（单杠杆 decay/truncation/window 已穷举且全平，R2 期望值低，不烧）。该族去留最终取决于 leading-gap 裁定。
5. 台账：`robustness_repair_QPveY7Kg_r1` 已写入 DEU ledger。

---

# USA 提交篮稳健性审计 — 2026-10-31（数据日期 2023-12-29）

审计对象：`akKW0Lax`（USA/TOP3000，④c 参数扫描最优，取代 9qxP0JbV）。
方法：brain-alpha-robustness Phase B（get_alpha_details + get_alpha_yearly_stats + get_alpha_pnl + check_correlation）→ Phase C 闸门判定。

## 判定汇总

| alpha | 机制 | IS S/F | 近3年 S (21/22/23) | CV3 | 衰减比 (23/IS) | 负年 | 平年 | margin@TVR | **verdict** |
|---|---|---|---|---|---|---|---|---|---|
| **akKW0Lax** | 短仓占比 22日均 126d−756d zscore 偏离 × rank(交易份额) → vector_neut(sif2) | 2.47 / 1.77 | 2.59 / 3.95 / 1.76 | **0.33** ✓ | **0.71** ✓ | 0 | 0 | **10.2bp @ 12.96%** ✓✓ | **PASS** |

## 逐颗明细

### akKW0Lax — PASS

**B.0 WebDataScope**：`failed_ra_count=0` / `failed_ppa_count=0` / `ra_failed=false` / `checks.fail=[]` → **PASS**。
`checks.pending` = SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION（平台标准待办，非失败）。
其中 SELF_CORRELATION 与 PROD_CORRELATION 已由 `check_correlation(refresh=True)` 独立实测通过（见下），其余两项在提交时由平台解析。

**B.2 逐年 Sharpe**（IS 2014–2023）：

| 年 | Sharpe | returns | drawdown | margin | long/short |
|---|---|---|---|---|---|
| 2014–2018 | 0.0 | 0.0 | 0.0 | 0.0 | 0 / 0 |
| 2019 | 0.67 | 0.013 | 0.0159 | 2.0bp | 1435 / 1401 |
| 2020 | 3.03 | 0.0913 | 0.0277 | 14.6bp | 1554 / 1546 |
| 2021 | 2.59 | 0.0778 | 0.0185 | 12.3bp | 1552 / 1596 |
| 2022 | 3.95 | 0.0992 | 0.0083 | 15.4bp | 1592 / 1561 |
| 2023 | 1.76 | 0.0477 | 0.0163 | 7.5bp | 1625 / 1541 |

- **2014–2018 五年空窗**：`executed_short_position_share_sum` / `aggregate_trade_share_count_regular_hours` / `short_interest_factor_score_2`
  三字段在 2019-02-19 前无有效读数（逐年 longCount/shortCount 均为 0）⇒ **有效历史仅 2019 起 5 年**（软标记，不据此 REJECT）。
- **近 3 年（2021–2023）**：2.59 / 3.95 / 1.76，**全部 ≥ 1.58 且全部为正** ⇒ Recent-3yr Sharpe **PASS**。
- **CV3** = std([2.59,3.95,1.76]) / mean = 0.903 / 2.767 = **0.326 < 0.40** ⇒ **PASS**。
- **衰减比** = 1.76 / 2.47 = **0.713 ≥ 0.50** ⇒ **PASS**（2023 年为全期 71%，无深度衰减）。
- **平年**（近 3 年 < 0.3）= 0 ⇒ **PASS**。
- **近 3 年 max/min** = 3.95 / 1.76 = **2.24 ≤ 3** ⇒ **PASS**。

**B.3 PnL 回撤**：全期最大年回撤 0.0277（2020）；逐季无 > 2× 全期平均的回撤槽 ⇒ **PASS**。

**B.4 相关性**（`check_correlation(refresh=True)` 实测）：

| 项 | 值 | 判定 |
|---|---|---|
| **prod_correlation** | **0.5171**（max）< 0.7 | **PASS**（深墙余量 0.1829） |
| **self_correlation** | **0.1105**（max，池 136，top1=0.1105）< 0.7 | **PASS**（深墙） |

**B.5 经济可解释性**：「短仓占比相对 1 年均值的短期-长期偏离（22 日均的 126 日 zscore 减 756 日 zscore），
经交易份额排名正交化后，再对冲短仓 Interest Factor Score 2」——一句话可写 ⇒ **PASS**。

**Margin @ turnover**：10.23 bp @ 12.96% TVR ⇒ ≥ 5 bp ⇒ **PASS**。

**算子数**：11（≤15 合规）⇒ 仅软标记（>5 提示过拟合风险，REGULAR 不据此 REJECT）。

**soft_flags**（如实带入 description，供一年后复盘）：
1. 2014–2018 五年空窗，有效历史仅 2019 起 5 年（字段原生覆盖，非参数造成）。
2. 算子数 11，偏高（混合两腿 × 外层轴结构复杂度）。
3. `checks.pending` 含 DATA_DIVERSITY / REGULAR_SUBMISSION，提交时由平台解析。

## 结论

**akKW0Lax 稳健性 PASS**，全闸（S/F/2Y/sub/TO/prod/self + WebDataScope + 近 3 年逐年 + 回撤 + margin + 可解释性）均通过，
无 CONDITIONAL 软标记阻断提交。已写入 USA ledger `robustness_akKW0Lax`。

（对照：被取代的 9qxP0JbV 慢腿窗口 504 → 756 后，S/F/2Y/sub 四项全升、prod 0.5263→0.5171 降、self 0.1032→0.1105，
且近 3 年 CV 保持 0.33 低水平——参数扫描不仅推高 IS，未引入年度不稳。）
