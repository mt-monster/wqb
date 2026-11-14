# BE93 判决：macro27 / pv47 / news52 三集判死（2026-11-12）

批号 `iWpF37Q45fMbEHi77EQGAr`｜DEU/TOP500/D1｜decay4/SUBINDUSTRY/trunc0.08/nan ON｜10 臂｜0 ERROR｜10/10 REJECT

收波方式说明：`harvest_multisim_alphas` 对该 multisim 返回 HTTP 404（multisim 注册滞后），改用 `batch_status`（`simulation_ids`）+ `batch_get_alpha_metrics` + `get_alpha_details` 直接回读——**这是拥塞期的正确通路**。

## 逐臂实测（表达式取自平台 code，非简写推断）

| # | alpha | 字段 / 构造 | S | F | TO | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | rK7pPYZa | mcr27_company_jobsactive 水平 | −0.09 | −0.02 | 4.6% | 0.65 | −0.35 |
| 2 | wpoKEm85 | mcr27_jobsactive Δ66 | 0.05 | 0.01 | 12.0% | 0.42 | 0.01 |
| 3 | vRAwvqKA | mcr27_company_jobscreated 水平 | −0.09 | −0.02 | 15.1% | 0.85 | −0.27 |
| 4 | d5akRX52 | mcr27_jobsactive zscore252 | 0.00 | 0.00 | 9.7% | 0.76 | −0.22 |
| 5 | Wjl1VqjN | pv47_spret zscore252 | −0.35 | −0.05 | 90.5% | 0.14 | −0.11 |
| 6 | blaGdklr | pv47_spret Δ66 | −0.11 | −0.01 | 72.5% | 0.57 | 0.23 |
| 7 | E5QOe759 | pv47_for_statssimple_only_spret zscore252 | **−1.01** | −0.26 | 90.6% | −0.10 | −0.47 |
| 8 | ZYaPK5PZ | mws52_chars_in_qa Σ66 | 0.13 | 0.05 | 2.7% | 0.70 | 0.11 |
| 9 | YPaLgrLv | mws52_conference_call_participants Σ66 | 0.08 | 0.03 | 2.6% | 0.44 | 0.11 |
| 10 | oma8gp8b | mws52_corporate_participants Σ66 | 0.07 | 0.02 | 2.6% | 0.53 | 0.07 |

族内 max |S| = **1.01**（臂 7，灰化：负向、TO 90.6%、2Y 负）。按协议 v2 L1 判据（<1.0 判死）整批越线为负向单臂，**无一条进入 L2**。

## 三集判死证书

**macro27（MACRO 未点亮塔）**
- 数据存在：TO 4.6-15.1%，2Y 0.42-0.85 说明面板有真实变动，不是空窗。
- 机制否证：招聘扩张（jobsactive/jobscreated）在 DEU TOP500 横截面**无方向性**——四个矩（水平/Δ66/zscore252/第二字段）全部落在 |S| ≤0.09，符号还互相翻转（−0.09 / +0.05 / −0.09 / 0.00）⇒ 非「方向错」而是「无信号」。
- 结论：MACRO 塔按 v2 记录判死（L1 覆盖：2 字段 × 4 矩）。

**pv47（spret 特异收益）**
- 三个变体（spret zscore / spret Δ66 / for_statssimple_only spret zscore）全负且量级分化（−0.35 / −0.11 / −1.01）。
- TO 72-91% 属极端换手区，2Y ≤0.57，sub 全负 ⇒ 无经济可持续性。
- 结论：pv47 判死（L1 覆盖：2 字段 × 3 矩；for_stats 变体是本批最强读数但方向与稳定性均不可交易）。

**news52（mws52 电话会议）**
- 三者同构（都是 ts_sum(vec_avg(...),66) 事件计数），S 0.07-0.13，TO 仅 2.6%，2Y 0.44-0.70。
- 死因归类：**稀疏事件计数**——与 EUR insiders1 / fund_holdings_panel 同一死法（记忆条目「计数型不是充分条件，需高频事件流」）。电话会议每年 4 次/公司，66 日窗内多为 0，横截面排序被并列块吞掉。
- 结论：news52 判死（L1 覆盖：3 字段 × 计数型；未做变化型——但水平型与计数型同为 0.07-0.13，无梯度可延）。

## 连带影响

1. **BE96 第三腿候选砍三个**：macro27 / news52 出局；news7（lc 仅 19）出局。第三腿仅剩 alpha_factor_lib（BE95 在测）与 news31 negative_sentiment_probability（BE94 实测 −0.68，需翻号）。
2. **未点亮塔状态**：MACRO 塔加一条判死记录；pv47/news52 属 PV/NEWS 塔内数据集级判死，不改变塔级判定。
3. 数据快照：交付 11/20 不变（本波产出 0 颗）。
