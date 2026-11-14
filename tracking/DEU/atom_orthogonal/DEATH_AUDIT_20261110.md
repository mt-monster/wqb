# DEU 判死档案六维审计（2026-11-10，用户指令触发）

> 用户原话：「我觉得你判死的太快了，探针没有穷尽所有机制和模板，这点一定要修复」。
> 本文件 = DEU D1 全部判死档案的对照审计 + 撤判重开队列 + 六维闸首例执行记录。
> 六维穷尽闸正文已固化 AGENTS.md §7.6（判死前必附本表所列证据，缺维只能记 PROVISIONAL）。

## 一、审计结论总表

| 数据集/族 | 原判死依据 | 实际探针覆盖（证据） | 六维缺口 | 审计判定 |
|---|---|---|---|---|
| risk60 | 波 N 探针 + 判据 MH「同 shortinterest3 机制、信息量更弱」 | 仅 ~5 条简单读数，**未用 ts_backfill 转面板**（MI 教训该波之后才确立）；零模板池 | D1/D3/D4/D5/D6 全缺 | **❌撤判 → BA1 已派**（借券费/拥挤度 9 条 + 第二分组轴） |
| risk88 | 「市值族」纯标签 | **零探针**（单字段 cov1.0） | 全缺 | **❌撤判 → BA1 1 条**（市值反转） |
| risk68 | 「破产/质量族」 | 实测 TOP500/D1 **全字段 cov=0** | — | 📁死因更正：**数据层排除（无供数）**，非信号死 |
| risk71/72 | 「Barra 残差族，同 other532」 | 实测 TOP500/D1 **全字段 cov=0**（residual/replicator 类） | — | 📁同上（数据层排除） |
| news18 / news50 / news38 | 被波 AU 判词「news 塔事件情绪通道终判死」覆盖 | **从未探针**（MNO 台账自己列为「待测队列」；news18=70 字段 cov0.979 最大富矿） | 全缺 | **❌撤回「news 塔终判死」→ BA2 首选** |
| news20 | 波 AU 6 探针 S≤0.35、2Y 全负 | 仅 6 条（level×5+delta×1） | D1/D4/D5/D6 | ⚠️降级维持（ceiling 0.35 距线 1.23，补池低优先） |
| news104 | 波 N 5 字段探针 S≤0.60 混号 | ~5 条，backfill 未用 | D1/D3/D4/D5/D6 | ⚠️降级维持（事件稀疏论证强；低优先） |
| ai_news_scores | 波 AR 2 探针 S≤0.21 | 2 条 | 几乎全缺 | ❌撤判（重开低优先：距线 1.37） |
| news_sentiment_nlp | 波 AR 1 探针 S=0.04 | 1 条 | 全缺 | ❌撤判（重开优先级最低） |
| sentiment7 | 批 Vl0pSdjo 10 模板 S≤0.77 | 10 条（数据集仅 2 个可用信号字段，族自测天然受限） | D5 部分/D6✗ | ⚠️维持（gap 0.81；留作 D6 补测兜底） |
| sentiment27 | 批 32qm4XaV + 波 M **双十模板池** S≤0.64 | 20 条跨两波，含 skew/kurt/quantile/分位比 | D6✗ | ✅维持（覆盖最全的 sentiment 死案） |
| sentiment33 | 波 AQ「CW 结构性」 | 待复核 AQ 档案（CW=**配置层死**，须先测 rank/sector 替代几何） | D6 | 📁待复核：若 AQ 未测替代几何则转 ❌ |
| analyst10 | 波 AP | 待复核 AP 档案 | ? | 📁待复核 |
| analyst83 | 「earningscall 1.02 / event_sentiment 0.70 双天花板先验」 | **零探针** | 全缺 | ❌撤判 → BA3 候选 |
| earningscall_sentiment | 波 AS 10 模板 S≤1.02 | 10 条（水平/变化/波动/协方差/quantile，sub+ind） | D6✗ | ⚠️维持（gap 0.56，天花板证据充分） |
| event_sentiment_signals | 波 AT 10 模板 S≤0.70 | 10 条互异（档案自称穷尽合规，实测缺 D6） | D6✗ | ✅维持 |
| socialmedia12 | AR 探针 + AU2 十模板池 | 12 条（level/delta/vol/quantile/product，sub+ind，5 字段族）| D6✗ | ✅维持（AU2 天花板 0.73，lc75-79 硬上限） |
| other47 | AV 8 探针 + AW 10 模板 S≤0.85 | 18 条 | D6✗ | ⚠️维持（W1 反关注 rank 保留作组合腿） |
| other545 | AV 2 探针 S≤0.12 | 2 条（lc88/27 双弱） | 全缺 | ❌撤判（低优先） |
| other250 | AV 1 探针 S-0.10 | 1 条；另有 11-04 s1_other250 模板池未核对 | 待复核 | 📁待复核 s1 池后定 |
| stock_cluster_dl | AV 探针 | 待复核 | ? | 📁待复核 |
| pattern_scores | 波 AD S-0.31~+0.52 +「形态=价格变换」机制先验 | 探针级+机制先验 | 待复核 | 📁待复核 |
| multifactor_return_pred | 「伪预测型，类 global_seasonal，暂不选」 | **零探针**（648 字段 cov0.54） | 全缺 | ❌撤判 → BA3 候选 |
| institutions4 | TO 88.7% | **配置层死**（未测 ts_target_tvr_decay/hump 几何） | D6 | ❌撤判（低优先） |
| insiders1 / dl_riskfree_returns | 波 Y/Z 符号混乱 S≤0.58 | 待复核池规模 | ? | 📁待复核 |
| pv109 | 12 模板 S0.54 | 12 条 | D6 待查 | ⚠️（PV 属禁混集，单数据集 ATOM 仍允许） |
| fundamental6 | F1/F2 现金利润率族 + **生产池占据**（prod 0.94/0.97） | 占据是平台事实 | — | ✅维持（结构性封盘，非探针不足） |
| model144/307/313/262 等 | MODEL 塔已点亮（≥3） | — | — | —范围规则（用户指令），不属判死审计 |
| shortinterest3 | ALIVE | E569ZE7L 全清待授权 | — | — |

## 二、被撤回的过度结论（先验误用清单）

1. **「news 塔事件情绪通道终判死」→ 撤回**。只测了 news20/news104；news18(70f cov0.979)/news50(37f cov0.764)/news38(3f cov0.599) 从未探针。
2. **「RISK 塔与 shortinterest3 同机制且更弱」→ 撤回**。risk60 零 backfill 探针 + MH 先验封死；risk88 零探针；risk68/71/72 实为无供数（数据层排除，标签纠正）。
3. **「D1 sentiment 邻接宇宙全部关闭」→ 降级**。ai_news_scores / news_sentiment_nlp / analyst10 / sentiment33 属探针级或配置级死，改记 PROVISIONAL；earningscall / event_sentiment / socialmedia12 / sentiment27 / sentiment7 / other47 的天花板证据维持有效。
4. **「DEU 15 塔全部实测完毕 / D1 可挖面穷尽」→ 撤回**（叠加 §7.5 既有教训：fundamental17/news17/news18 实际仍在出货却被登记死集）。

## 三、重开队列（用户优先序：sentiment/risk → 其余）

- **BA1（本日派发，后台退避重试中）**：risk60 9 条（crowding 水平/流量/费率水平/费差/费动量/IR/波动/交互 + industry 轴）+ risk88 1 条（市值反转）。全部 ts_backfill(vec_avg()) 转面板（MI 教训落地，波 N 未做）。
- **BA2（下一波）**：news18 backfill-first 十模板池 + news50/news38 探针（news 塔「终判死」撤回后的正当开矿）。
- **BA3（低优先池）**：analyst83、multifactor_return_pred、ai_news_scores、news_sentiment_nlp、other545、institutions4（tvr_decay 几何）、sentiment33（CW 替代几何）、sentiment7/27/earningscall 的 D6 补测。
- 📁待复核档案：analyst10(AP)、sentiment33(AQ)、other250/stock_cluster_dl(s1 池)、pattern_scores(AD)、insiders1(Y)、dl_riskfree(Z)、pv109(D6)。

## 四、AU2 收割落账（socialmedia12 十模板池，sim 2bobMC9U44JjahT1e2mHxofz）

10/10 COMPLETE / 0 error。S 排序：0.73（期望价差−日内收益，lc79）/ 0.56（sentiment delta66）/ 0.55（buzz delta66）/ 0.43 / 0.43 / 0.42（hit_ratio，2Y1.95）/ 0.29 / 0.26 / 0.09 / −0.46 ⇒ **族天花板 0.73 < 1.58，判死维持**（⚠️ D6 单配置；lc 75-79 低覆盖是硬上限）。金字塔命中 DEU/D1/SOCIALMEDIA。

## 五、BA1 派发记录

- 首派 12 条被拒：**multisim 单请求上限 10 条**（'Maximum 10 alpha expressions allowed per request'）⇒ 收敛 10 条（R10 非线性、risk88 第二轴顺延 BA1b）。
- 二派遇 **429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED**（AN 卡 10% 占 1 槽 + 疑似清理延迟）⇒ 后台退避重试：`cache/_watchBA1_retry.ps1`（成功即转 30 分钟 COMPLETE 轮询；状态 `cache/_out_BA1_status.txt`）。
- 设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON/maxTradeOFF；表达式清单见 waveBA1_dispatch_20261110.md。

## 六、BA1 收割与重开阶梯推进（同日补账）

- BA1（sim 2N0fo53az4Cu9721ZzTUIA8）10/10 COMPLETE 0 error：费率/拥挤面 6/7 同号（翻转 +0.55/+0.49 天花板），与 shortinterest3 机制同向 ⇒ **探针不判死（新闸首例）**，risk60 升级 BA2 冠军骨架十模板池（waveBA2_dispatch_20261110.md）。
- risk88 三维自测推进中（level 0.11 → BA2 补 delta/ts_rank）；单字段族天花板远离 1.58，但终判仍需池证据。
- BA3（news18/news50/news38）顺延至 BA2 收割后。
