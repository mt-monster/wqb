# KOR /goal 交付报告（2026-11-21）

> 目标：KOR 固定区域，10 颗通过验证的 regular alpha（ATOM 优先）。
> 本轮全部动作走 MCP + 既有 CLI 工具；派批一次一批（在飞 ≤1）；全程 KOR/TOP600/D1。

## 一、结论先行

**本轮可提交交付 = 0 颗**（与 11-21 早间会话的「非 OTHER 未亮塔穷尽」结论一致并补完了最后一个缺口）。
**实质推进 = 2 项**：① 悬置的 other553 TO 修复批收割入库并关闭；② 完成 OTHER 塔剩 1 席的零配额收割
+ 10 臂修复批，产出 KOR 全库唯一「全指标达标仅差 1 个 warning 闸」的候选对（`2rAVLRYP` / `akaeNb1W`），
并定量确认其唯一缺口（investability ratio）是**动态闸结构墙**。

## 二、本轮做的事（按序）

| # | 动作 | 结果 |
|---|---|---|
| 1 | 状态核验：塔位实读（get_pyramid_alphas）/ 死集 / submit_ready / 悬置批次 | 未亮塔 = earnings·imbalance·institutions·macro·news·sentiment·socialmedia（全0）+ other 2/3 |
| 2 | 收割 11-21 早间悬置批 `1IIFjRc6j4Dybl2AOgANGmg`（other553 est 族 TO 修复，2 臂） | **负结论**：decay 放外侧后 TO 仍 1.53（原 1.59），S 0.90/2Y −0.39 ⇒ TO 是截面重排的结构属性，est 族关闭 |
| 3 | 全库 prod_clean 盘点（26 颗 REGULAR IS UNSUBMITTED prod<0.7 S≥1.58）按塔归组 | 25 颗落已亮塔（PV/SHORTINTEREST/RISK/ANALYST/FUNDAMENTAL），**唯一落未亮塔 = `2rAVLRYP`（OTHER 2/3 剩 1 席）** |
| 4 | other395 / other496 检索盲区核查 | other395 已实测否证（56 臂 S≤0.38）；other496 61 臂最优即 2rAVLRYP，无遗漏 |
| 5 | other496 全字段画像（104/104，filter_sharpe=false，dataset 级全量） | 归档增量段至 `tracking/KOR/reference/datasets/other496.md` §8 |
| 6 | `2rAVLRYP` 零配额终验 | self **0.411**（pool 33）✅ / 十年逐年 **PnL 全正、零持仓年 0**、单年占正收益 22.8% <30%、S<1.0 年 4/10 / PnL 阶梯健康 ✅ / prod 0.6595 ✅ |
| 7 | gate_attribution 归因（investability 单闸） | 裁决 PUSH_TARGETED：①loosen_concentration ②finer_group_axis |
| 8 | 修复批 `1gtvrPbBQ55aa6y168vEf6C0`（10 臂，一批） | 见下表；**结构墙确认** |
| 9 | 台账回写 | wave `s2_other553_decayfix_d1`=FAIL / `s2_other496_investfix_d1`=PARTIAL（1 全指标达标 + 9 near）；记忆索引更新 |

## 三、修复批读数（10 臂，STATISTICAL/d2/trunc .08，FULL）

| 变体 | alpha | S | F | 2Y | invest比 | failed_RA |
|---|---|---:|---:|---:|---:|---:|
| **裸 rank** | `akaeNb1W` | **1.88** | **1.06** | 2.66 | 0.53 | **1** |
| 原件（存量） | `2rAVLRYP` | 1.67 | 1.04 | **2.82** | 0.545 | **1** |
| winsorize(sector) | `e7aNnb0N` | 1.81 | 0.97 | 2.55 | 0.52 | 2 |
| quantile 壳 | `kqavnojl` | 1.72 | 0.92 | 2.65 | 0.55 | 2 |
| 对照（同式重跑） | `78Y3xNjx` | 1.81 | 0.97 | 2.55 | 0.52 | 2 |
| 其余（tail/轴换/decay/neutralize） | 5 臂 | 0.68–1.53 | — | — | 0.45–0.62 | 2–3 |

**结构墙判定**：invest limit ≈ 0.70×S（动态），S 涨 limit 同涨 ⇒ 全批 ratio 0.45–0.62 追不上 0.70；
归因两杠杆（放集中度/换细分组轴）穷尽。机制 = 共识修正信号收益集中中小盘，属信号性质。
**唯一正向杠杆 = 裸 rank**（S+0.07/F+0.02/subU+0.10）；tail 毁中心信息（S 0.68）。

## 四、候选明细（近闸件，不可提交，warning 也计 failed_ra）

1. **`2rAVLRYP`**（存量）— `group_rank(ts_backfill(vec_avg(oth496_aftercons_percentage),44),sector)`
   S1.67/F1.04/TO0.196/2Y2.82/subU1.36/**prod 0.6595**/**self 0.411**/十年满仓/塔 KOR/D1/OTHER eff=1
   → 唯一缺口 LOW_INVESTABILITY_CONSTRAINED_SHARPE（0.91 vs 1.17）
2. **`akaeNb1W`**（新）— `rank(ts_backfill(vec_avg(oth496_aftercons_percentage),44))`（裸 rank 变体）
   S1.88/F1.06/TO0.253/2Y2.66/subU1.55 → 同一缺口（1.00 vs 1.32）
   （prod 未测——与 2rAVLRYP 同内核同设置，prod 大概率同档；花 prod 槽前先互相关）

## 五、为什么 10 颗交付在本区当前红线内不可达（如实上报）

| 面 | 状态 | 证据 |
|---|---|---|
| 非 OTHER 未亮塔 7 座（earnings/imbalance/institutions/macro/news/sentiment/socialmedia） | **11-21 早间已逐集穷尽 0 交付** | `kor-unlit-non-other-exhausted-20261121` 读数表（earnings3 S1.91 但 2Y 0.46；institutions6 S0.90；macro63 空账等） |
| OTHER 塔剩 1 席 | **本轮收割+修复批关闭** | 2rAVLRYP/akaeNb1W 差 investability 动态闸（10 臂穷尽） |
| 已亮塔（analyst4/shortinterest4/fund3/model3/insiders3/pv3/risk3） | 红线禁投 | 用户 2026-11-16 明令「只打未亮塔」 |
| prod-clean 存量 26 颗 | 25 颗落已亮塔，0 可交付 | 本轮全库盘点 |
| SUPER alpha | 非 regular，不在交付范围 | KPg60XNp 等另计 |

⇒ **10 颗目标在「固定 KOR + 只打未亮塔 + prod<0.7 + warning 计失败」约束下结构性不可达**。
三条扩展路径（均需用户拍板）：
① **接受 warning 件**：`2rAVLRYP`/`akaeNb1W` 全指标达标仅 investability 1 个 warning，
   平台实际拦不拦取决于提交层口径（IND 实测不拦 LOW_INVESTABILITY_CONSTRAINED_SHARPE）；
② **放宽「只打未亮塔」**：从已亮塔的 prod-clean 存量（25 颗）挑正交篮子，零仿真配额；
③ **放宽 prod 红线**：`gJarqlEJ`（dl_riskfree，S2.18/F1.49/2Y1.91 全闸，prod 0.8197）。

## 六、经验沉淀（可复用）

1. **investability 动态闸判据**：limit ≈ 0.70×S ⇒ 「追 S 破 invest 闸」数学不可达；
   唯一出路是提高 invest_S 绝对值（大盘可投资子集的信号强度）——若多臂后 ratio 不动即结构墙。
2. **KOR 平台读数漂移**：同式重跑 S 1.67→1.81（±0.15 量级），比较历史读数须留余量。
3. **tail 是中心信息毁器**：对「预期修正幅度」这类有中心语义的信号，tail(5/95) 把 S 打到 0.68。
4. **其他塔位候选甄别**：26 颗 prod_clean 全按表达式前缀归组后，只有 1 颗落未亮塔
   ——零配额收割面的真实供给远小于表面数字，交付前必须逐颗核塔位。

## 七、产物索引

- 档案：`tracking/KOR/reference/datasets/other496.md` §8（字段全表复核 + 修复批 10 臂全表 + 归因）
- 台账：wave_results `s2_other553_decayfix_d1`（FAIL）/ `s2_other496_investfix_d1`（PARTIAL）
- 记忆：`kor-other496-investability-structural-wall-20261121`
- 批次：`1gtvrPbBQ55aa6y168vEf6C0`（10 臂 FULL，全部入库 backtest_results）
