# GBR 挖掘报告 · risk68（1 波）

> **修订记录（按复核意见）**：本报告只保留「字段 / 画像 / 机制 / 调优 / 判据」五层，保留原稿全部实测数字，仅处理复核指出的五个问题，不新增未验证结论；未纳入六维 / 对称噪声 / 机制迁移 / 流程治理 / 下一波建议。
> 五处修订：① §3 删「波动择时」两条无出处学术引用（Neo/Tee、Malitskaia），机制与回测读数保留；② §3「Brennan & Huh」署名按证据源统一为三作者；③ §1 改题为逐字段模板清单并注明本波 0 臂、部分为未跑候选形态；④ §2/§5 交代 S=1.82 是跨数据集混合形态，不推翻单集天花板；⑤ §5 ts_delay 档由「仅常数不同」改为「一档完全相同、另一档仅常数不同」。逐条核验命令与输出见交付说明。

---

## 1. 逐字段模板清单（含未跑候选形态；本波 0 臂、未派发）

> **呈现口径**：下表为按字段整理的**模板 / 历史形态清单**，不是本波已跑列表。第 1 波 wave=STOP、`expressions=[]`、0 臂、不开波、不派发（见 §4 / §5）。经 DB 只读抽查（GBR `backtest_results` / `expressions`，`LIKE` 匹配），其中 **5 条表达式零命中**：`ts_sum(rsk68_residual_return,5)`、`ts_sum(rsk68_residual_return,60)`、`group_neutralize(signed_power(group_rank(ts_backfill(rsk68_residual_return,250),subindustry)-0.5,2),market)`、`rank(ts_backfill(divide(rsk68_residual_return,rsk68_weight_volatility_short),250))`（IR 形态）、`rank(ts_backfill(log(rsk68_weight_dadv),250))`；其余多为历史波次形态。5 个字段在**字段粒度**确有 107 条历史回测（§2），故本清单在字段粒度成立；读者不应把表中每一条都读作本波实测。

- risk68 / rsk68_residual_return（MATRIX）→ -rank(ts_backfill(ts_sum(rsk68_residual_return,5),250)) ｜ rank(ts_backfill(ts_sum(rsk68_residual_return,60),250)) ｜ group_neutralize(signed_power(group_rank(ts_backfill(rsk68_residual_return,250),subindustry)-0.5,2),market) ｜ rank(ts_backfill(divide(rsk68_residual_return,rsk68_weight_volatility_short),250))
- risk68 / rsk68_weight_volatility_short（MATRIX）→ -rank(ts_backfill(rsk68_weight_volatility_short,250)) ｜ rank(ts_backfill(-ts_delta(rsk68_weight_volatility_short,20),250)) ｜ rank(ts_quantile(rsk68_weight_volatility_short,22))
- risk68 / rsk68_beta（MATRIX）→ -rank(ts_backfill(rsk68_beta,250)) ｜ group_rank(ts_backfill(-ts_quantile(rsk68_beta,252),250),industry) ｜ rank(ts_backfill(-ts_std_dev(rsk68_beta,60),250))
- risk68 / rsk68_weight_dadv（MATRIX）→ -rank(ts_backfill(log(rsk68_weight_dadv),250)) ｜ trade_when(rsk68_weight_dadv>ts_mean(rsk68_weight_dadv,20),rank(-rsk68_residual_return),-1) ｜ rank(ts_backfill(divide(rsk68_weight_edadv,rsk68_weight_dadv),250))
- risk68 / rsk68_weight_edadv（MATRIX）→ rank(ts_backfill(-log(rsk68_weight_edadv),250)) ｜ rank(ts_backfill(divide(rsk68_weight_edadv,rsk68_weight_dadv),250))

---

## 2. 字段画像（带数字读数）

- rsk68_residual_return：type=MATRIX; 平台 cov=0.0 但系 GBR 元数据盲区非无数据; αC=367(全集最高)/uC=224; dateCreated=2026-07-01 日更; 分布=零均值截面 decimal、近对称尾部略厚; 实测 107 条 rsk68 回测 lc 316–911/sc 0–569/both0=0(证有数据), 该字段使用计数 91、历史最高 S=1.82（该行系与 loaned_share_count_main 的跨数据集混合形态、含 vec_sum，非单集信号，见 §5）; density=dense(日更覆盖稳)。｜排除：vec_avg(rsk68_residual_return,...) — 全 MATRIX，套 VECTOR 算子类型不匹配必 FAIL(v11 实测 2/2 FAIL)；把 NONE 探针 rank(ts_backfill(rsk68_residual_return,250)) 的 sc=0 判字段死 — lc=832 证数据存在，属 rank 长仓配置伪影；裸水平跨族 add(残差 decimal + beta 无单位 + dadv 美元额) — 量纲陷阱,profile §6 禁；只给相关系数不给机制的模板不采
- rsk68_weight_volatility_short：type=MATRIX; cov=0.0(GBR盲区); αC=192/uC=111; dateCreated=2026-07-01 日更短期波动率估计; 分布=恒正右偏 decimal; 使用计数 12; 107 条 rsk68 回测间接证实双边持仓覆盖稳定; density=dense。六法症状: 单边恒正→禁裸水平用 ts_delta; 右偏→避裸 zscore 改 rank/ts_quantile。｜排除：裸水平 rsk68_weight_volatility_short(恒正右偏)直接做信号 — 六法④/单边恒正禁裸水平；ts_zscore(rsk68_weight_volatility_short) 裸 zscore — 右偏分布避用；vec_avg(...) — MATRIX 类型不匹配；vec_avg 之外的第二数据集腿 — 保持 ATOM 单集
- rsk68_beta：type=MATRIX; cov=0.0(GBR盲区); αC=152/uC=96; 约 504 交易日滚动窗估计的日更 β; 分布=无单位围绕 1 聚集; 使用计数 26; 探针 rank(ts_backfill(beta,250)) lc=833/sc=0(配置伪影非死); density=dense。｜排除：10.1016/j.ememar.2021.100832 Low liquidity beta anomaly in China — China-specific 不可迁移 GBR；把 beta 探针 sc=0 判字段死 — lc=833 证数据存在；beta 腿与 dollar-neutral 混同 — post 44687266076823 明示 dollar-neutral≠beta-neutral；用未来 rebound 状态信息择时 beta — look-ahead 禁止；vec_avg(...)/第二数据集腿 — MATRIX 不匹配且保持 ATOM
- rsk68_weight_dadv：type=MATRIX; cov=0.0(GBR盲区); αC=131/uC=93; SMA 美元平均日成交量日更; 分布=美元额 10⁶–10⁹ 右偏长尾; 使用计数 13; 语义为流动性权重非独立信号; density=dense。六法症状: 恒正右偏→必须 rank/log 去量纲、禁裸水平、避裸 zscore。｜排除：裸水平 rsk68_weight_dadv (dollar 10⁶–10⁹ 右偏长尾)直接做信号 — profile §5②必须 rank/log；ts_zscore(dadv) 裸 zscore — 右偏长尾避用；把 dadv 与 edadv 当两条独立信号腿 add — 同一量 SMA/EMA 两平滑，禁同源冗余腿(post 44516393422743)；跨族裸水平 add(美元额+decimal+无单位) — 量纲陷阱；vec_avg(...)/第二数据集腿 — MATRIX 不匹配且保持 ATOM；traffic-volume/prescription-volume/dollar-for-dollar 类论文 — 主题噪声无股票收益机制
- rsk68_weight_edadv：type=MATRIX; cov=0.0(GBR盲区); αC=121/uC=85(全集最低但仍活跃,非 αC=0 死字段); EMA 美元平均日成交量日更; 分布=美元额 10⁶–10⁹ 右偏长尾; 使用计数 6; 与 dadv 同一量的指数衰减平滑; density=dense。六法症状: 恒正右偏→必须 rank/log 去量纲、禁裸水平、避裸 zscore; 语义为流动性权重非独立腿。｜排除：裸水平 rsk68_weight_edadv(dollar 右偏长尾) — profile §5②必须 rank/log；ts_zscore(edadv) 裸 zscore — 右偏长尾避用；把 edadv 与 dadv 当两个独立信号腿 — 同一量 EMA/SMA 两平滑，禁同源冗余腿；αC=121/uC=85 误判为死字段 — 全集 αC 最低但仍≥121，dateCreated=2026-07-01 新 onboard 非老死字段；vec_avg(...)/第二数据集腿 — MATRIX 不匹配且保持 ATOM；China-specific 低流动性 beta 论文 — 不可迁移 GBR

---

## 3. 匹配的机制（论坛 + 论文证据）

- rsk68_residual_return：[特质反转] Da/Liu/Schaumburg (2011, SSRN 10.2139/ssrn.1926851) 分解短期收益反转，1–5 交易日短窗；持有期=5日短反转；适用域=美股为主且有跨市场复制，GBR 大盘股可迁移但需核 prod 拥挤；证据 post 44557078934039(短窗 ts_rank 常是价反转伪装、经典反转易撞 prod>0.9，须换经济逻辑)。
  [特质动量] Blitz/Huij/Lansdorp/Verbeek (2013, J. Fin. Markets 10.1016/j.finmar.2012.10.005) 短期残差反转/特质动量，12–2 月窗；持有期=中期约 60 日；适用域=国际股票(含欧洲)可迁移 GBR；证据 post 8046468280727(换窗 5 vs 20 降相关)。
  [组内偏离] group_rank(x,g)-0.5 中心化把排名移到 0，signed_power 保方向放大远离中点权重；持有期=日频再平衡；适用域=单集分组仅用允许字段 sector/industry/subindustry，可迁移 GBR TOP700；证据 post 44554464310167(减 0.5 过 sub-universe shape 测试，不减则不过)。
  [波动归一] 风险调整信息比率 IR=Return/std(Return)；持有期=日频；适用域=同集内残差收益除短期波动(profile §4 典型用法)，仍单集 ATOM；证据 post 8123350778391(降波动靠 neutralization/volatility scaling) + Kim & Tse (2016, J. Fin. Markets 10.1016/j.finmar.2016.05.003) volatility scaling。
  证据：画像 path tracking/GBR/reference/datasets/risk68.md 字段全表/§6/§8：αC=367、日更、零均值近对称、107 回测 both0=0；queries_tried 维度1字段名: rsk68_residual_return idiosyncratic residual；queries_tried 维度2字段含义: idiosyncratic residual return short-term reversal alpha; 特质收益 反转 因子；queries_tried 维度3机制措辞/算子×字段: 拥挤/出清 + ts_corr residual return volume; ts_regression residual beta; betting against beta; idiosyncratic volatility puzzle；论坛 search_forum_posts 4 次调用=工具故障(2 超时+2 navigation_failed)，非论坛无解；绕行 get_documentations→get_documentation_page→read_forum_post 成功；cite/DOI: 10.2139/ssrn.1926851(Da Liu 2011) / 10.1016/j.finmar.2012.10.005(Blitz 2013) / 10.1111/jofi.12286(Stambaugh Yu 2015); 帖子 id 44557078934039/8046468280727/8123350778391；证据闸留痕: ledger GBR/forum_paper_recon_gbr_risk68_tpl20261119, diverse_ok=true; gate-style verify_diverse 前3 cite=9篇/3作者通过；ATOM: 本字段模板全部单集(risk68)，未引入第二数据集；分组仅用允许字段
- rsk68_weight_volatility_short：[低波异象] Chen (2017, 10.1007/978-3-319-63465-4_5) The Low-Volatility Anomaly 与 Stambaugh & Yu (2015, J. Finance 10.1111/jofi.12286) 特质波动谜题，横截面低波异象；持有期=日频再平衡；适用域=股票横截面，GBR 可迁移；证据 post 8123350778391(降波动提升 Sharpe/volatility scaling)。用 rank 单调变换而非裸水平，规避恒正右偏陷阱。
  [波动择时] 20 日波动变化窗作波动择时形态；持有期=约 20 日；适用域=股票日频面板可迁移 GBR；证据 profile §8 实测该形态 lc=903/sc=0/S=0.71（对应 risk68.md:111 的 `rank(ts_backfill(-ts_delta(rsk68_weight_volatility_short,20),250))`，配置伪影非死）。（复核删：原稿此条引 Neo & Tee (2021, J. Portfolio Mgmt 10.3905/jpm.2021.1.293) 与 Malitskaia (2019, 10.2139/ssrn.3417360)；全库 ledger、三份 paper-batch 与证据闸均无此二 DOI / 作者，属引用无读数支撑，已去除；机制与回测读数保留。）
  [分位排序] 波动分位排序替代裸 zscore 压右偏长尾；持有期=22 日窗;适用域=日频 dense 面板 5–22 窗可用，GBR TOP700；证据 post 8046468280727(换算子/换窗降相关) + profile §8 实测 lc=904/sc=0/S=0.74。
  证据：画像 path tracking/GBR/reference/datasets/risk68.md 字段全表/§5②/§6④：αC=192、恒正右偏 decimal、日更；queries_tried 维度1字段名: rsk68_weight_volatility_short low volatility；queries_tried 维度2字段含义: short term volatility risk factor alpha / 波动率 低波 异象 排序 / 错位 错配 拥挤；queries_tried 维度3算子×字段: group_rank/ts_backfill; idiosyncratic volatility puzzle / volatility timing / volatility risk premium；cite/DOI: 10.1111/jofi.12286(Stambaugh Yu 2015) / 10.1007/978-3-319-63465-4_5(Chen 2017); 帖子 id 8123350778391/8046468280727；证据闸留痕: ledger GBR/forum_paper_recon_gbr_risk68_tpl20261119, diverse_ok=true(vol 批 20篇/18作者)；ATOM: 单集模板，波动分母同集用法未引入第二数据集
- rsk68_beta：[低贝塔异象] Frazzini & Pedersen (2014, J. Fin. Economics 10.1016/j.jfineco.2013.10.005) Betting against beta，杠杆约束驱动，美股+国际股票；持有期=日频再平衡；适用域=国际股票含欧洲，可迁移 GBR 但需分腿审计；证据 post 44687266076823(beta 腿须分腿审计、dollar-neutral≠beta-neutral、禁 look-ahead) + Novy-Marx & Velikov (2022, JFE 10.1016/j.jfineco.2021.05.023) betting against BAB。
  [贝塔分位] 低贝塔异象的组内分位实现，252 日 β 分位；持有期=中期约 252 日估计窗上的日频信号；适用域=单集分组用允许字段 industry，GBR 可迁移；证据 post 44554464310167(group_rank 中心化过 sub-universe) + profile §8 实测 lc=787/sc=0/S=0.75。
  [贝塔稳定] β 估计区间/稳定性越低越优(The Low Beta Anomaly and Estimation Interval, 2019, 10.5430/afr.v8n1p203)，60 日 β 波动窗；持有期=日频；适用域=股票横截面 GBR 可迁移；证据 post 8046468280727(换算子降相关) + profile §8 实测 lc=832/sc=0/S=0.78。
  证据：画像 path tracking/GBR/reference/datasets/risk68.md 字段全表/§4A/§8：αC=152、无单位围绕1、~504日窗、探针 lc=833；queries_tried 维度1字段名: rsk68_beta low beta anomaly；queries_tried 维度2字段含义: beta CAPM low beta anomaly alpha / 低贝塔异象 / 拥挤；queries_tried 维度3: ts_regression residual beta; betting against beta / low beta anomaly；cite/DOI: 10.1016/j.jfineco.2013.10.005(Frazzini Pedersen 2014) / 10.1016/j.jfineco.2021.05.023(Novy-Marx Velikov 2022) / 10.1111/jofi.12286; 帖子 id 44687266076823/44554464310167；证据闸留痕: ledger GBR/forum_paper_recon_gbr_risk68_tpl20261119, diverse_ok=true；ATOM: 单集模板，未引入第二数据集
- rsk68_weight_dadv：[流动性溢价] Amihud (2002, J. Fin. Markets 10.1016/S1386-4181(01)00024-6) Illiquidity and stock returns 流动性溢价，低美元成交量(难交易)要求溢价；持有期=日频；适用域=美股原始证据、跨市场复制需验证后迁 GBR；证据 post 44529623569687(须核 shares/dollar、正值、滞后到决策时点、价变/收益量纲不可混) + Brennan, Huh & Subrahmanyam (2013, 10.1093/rapstu/ras017) Amihud 溢价。log 压右偏长尾。（复核统一署名：paper-batch `logs/_tmp_risk68_papers_c.json` 中该 DOI 作者为 Brennan Michael / Huh Sahn-Wook / Subrahmanyam Avanidhar 三人；证据闸 ledger `forum_paper_recon_gbr_risk68_riskfields` 用简称「Brennan & Subrahmanyam (2013)」。DOI 可追溯，机制成立。）
  [量能门控] 以 dadv 相对 20 日均值为事件条件门控残差反转信号，dadv 仅作流动性权重/门控非独立腿；持有期=事件触发持有(低换手)；适用域=单集内 dadv+residual_return 仍 ATOM，GBR TOP700 可迁移；证据 post 8360363631127(trade_when event,alpha,-1; 例 rank(volume/adv20)>0.5; 覆盖好低换手但难高 Sharpe) + profile §8 实测 lc=898/sc=0/S=0.86。
  [平滑背离] EMA/SMA 美元成交量之比作单一成交量趋势特征(非两条独立腿)；持有期=日频；适用域=同集两平滑构造单一经济含义，ATOM 单集；证据 post 44516393422743(dadv/edadv 同一量两平滑不可当独立腿，算子须有明确目的) + Lee & Swaminathan (2000, J. Finance 10.1111/0022-1082.00280) 量价关系;profile §8 实测 lc=903/sc=0/S=0.82。
  证据：画像 path tracking/GBR/reference/datasets/risk68.md 字段全表/§5②/§6④/§8：αC=131、dollar 10⁶–10⁹右偏长尾、使用计数13；queries_tried 维度1字段名: rsk68_weight_dadv dollar volume ADV；queries_tried 维度2字段含义: dollar volume liquidity weight ADV alpha / 流动性溢价 / 拥挤；queries_tried 维度3算子×字段: trade_when volume adv event; amihud illiquidity / dollar volume / volume return relation；cite/DOI: 10.1016/S1386-4181(01)00024-6(Amihud 2002) / 10.1093/rapstu/ras017(Brennan, Huh & Subrahmanyam 2013) / 10.1111/0022-1082.00280(Lee Swaminathan 2000); 帖子 id 44529623569687/8360363631127/44516393422743；证据闸留痕: ledger GBR/forum_paper_recon_gbr_risk68_tpl20261119, diverse_ok=true(liquidity 批 25篇/21作者)；ATOM: 单集模板，edadv 比率仍同集未引入第二数据集
- rsk68_weight_edadv：[流动性溢价] Amihud (2002, 10.1016/S1386-4181(01)00024-6) 流动性溢价，EMA 版美元成交量作流动性代理；持有期=日频；适用域=美股原始证据、迁 GBR 需按 post 口径核验；证据 post 44529623569687(流动性代理量纲/正值/滞后单元检查) + profile §8 实测 lc=904/sc=0/S=0.79。log 压尾 + rank 去量纲。
  [平滑背离] EMA/SMA 比率捕捉成交量加速/衰减，单一趋势特征；持有期=日频；适用域=同集两平滑构造单一经济含义，ATOM 单集；证据 post 44516393422743(dadv/edadv 不可当两条独立腿) + Lee & Swaminathan (2000, 10.1111/0022-1082.00280);profile §8 实测 lc=903/sc=0/S=0.82。
  证据：画像 path tracking/GBR/reference/datasets/risk68.md 字段全表/§4C/§5②/§8：αC=121、uC=85、dollar 右偏长尾、EMA 平滑、使用计数6；queries_tried 维度1字段名: rsk68_weight_edadv dollar volume ADV；queries_tried 维度2字段含义: dollar volume liquidity weight ADV alpha / 流动性溢价；queries_tried 维度3: amihud illiquidity / liquidity risk / volume return relation; 错位 拥挤 出清；cite/DOI: 10.1016/S1386-4181(01)00024-6(Amihud 2002) / 10.1093/rapstu/ras017(Brennan, Huh & Subrahmanyam 2013) / 10.1111/0022-1082.00280; 帖子 id 44529623569687/44516393422743；证据闸留痕: ledger GBR/forum_paper_recon_gbr_risk68_tpl20261119, diverse_ok=true；ATOM: 单集模板，dadv 比率仍同集未引入第二数据集

---

## 4. 调优过程（配置阶梯 / 设置档）

### 第 1 波 · 设置 N/A（stop 决策：不开波、不派发、不改写设置凑闸） · 0 臂
- 配置阶梯：未触发（最高 S 未达触发线）

---

## 5. 下结论的判据

### 第 1 波：FAIL（wave=STOP，0 臂，无 create_multi_simulation / 收割对象）

- **STOP 定性**：第 1 波为 deliberate STOP、0 配额；设计稿即 `expressions=[]`『本波不开、不输出任何臂』（ask 材料）；`bestS=0` 是 schema 占位哨兵，非实测 sharpe。verdict=FAIL 仅表示本波 0 臂、无任何可交付 / near 候选（无臂则不可能满足 PASS / PARTIAL 的臂级定义），并非 STOP 决策执行失败——该 STOP 有证据支撑、0 配额消耗。

- **判据一 · 逐臂对照**：本波 `arms=[]`，无臂可比对方向 / 强度，逐臂对照 N/A。停止根因是拟设 12–2 骨架 `rank(ts_backfill(ts_sum(ts_delay(f,D),S),250))` 与本会话实跑只读 SQL（`SELECT code,sharpe,long_count,short_count FROM backtest_results WHERE region='GBR' AND code LIKE '%rsk68%' AND code LIKE '%ts_delay%' AND code LIKE '%ts_sum%'`）返回的唯一 1 行 `rank(ts_backfill(ts_sum(ts_delay(rsk68_residual_return,20),200),250))` sh=0.85/lc=911/sc=0 的关系：**D=20/S=200 这一档与该行连常数都完全相同，只有 D=42/S=210 那档才是仅常数不同**（复核口径修正：原稿笼统写「完全同几何、仅常数不同」，对 D=20/S=200 不成立；改为「一档完全相同、另一档仅常数不同」。此 imprecision 实际**加强**而非削弱 STOP 结论）。按『换常数不算结构互异』口径（`02_signal_patterns.md` §1 / `AGENTS.md` §7.6 D1）不构成新机制，S 0.85 远低于 ≥1.58 交付线。

- **判据二 · 分层判定**：信号层封盘，非配置层、非数据层。数据层已排除（`risk68.md:85` 107 条回测 lc 316–911 / both0=0、探针 lc=832/833 证 dataPresent=true，sc=0 属 rank 长仓配置伪影 `risk68.md:86,100`）。封盘证据：`reports/gbr_nonpmo_round_20261104.md:633-637`『25 臂 S 0.78–1.13 最好 1.13，GBR risk 塔不再用 risk68 攻』、`:1249`『RISK risk68 S1.13（25 臂扫尽）信号强度天花板，非几何问题』、`reports/gbr_unlit_campaign_round1_20261104.md:523`『残差反转天花板≈1.04，距 1.58 差 52%，单靠几何/参数不可能补上』。面枯竭：`gbr_nonpmo:1257-1258` 整个 GBR 未点亮 10 塔在现有数据集下全部无解（5 塔无数据 / 2 塔覆盖低 / 3 塔信号天花板）。

- **判据三 · 候选 / nearPass**：无臂故 `[]`。**历史最高 S=1.82 的归属必须交代**：SQL `SELECT code,sharpe FROM backtest_results WHERE region='GBR' AND code LIKE '%rsk68%' ORDER BY sharpe DESC LIMIT 1` 返回的 S=1.82 行是 `winsorize(ts_decay_linear(add(group_rank(-ts_sum(rsk68_residual_return, 11), subindustry), reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), sector))), 8), std=0.25)`（lc=332 / sc=330），是 rsk68_residual_return 与 loaned_share_count_main 的**跨数据集混合 alpha、且含 VECTOR 算子 vec_sum**，并非干净的 rsk68 单集信号。故 1.82 属 107 行历史集合、且为混合形态，不推翻单集天花板 1.13 / 1.04，不列为单集候选（该值源自 `risk68.md:85/110`，与报告同源，属源与报告共同未标注的关键归属，此处补明）。

- **结论范围**：封顶结论仅限「ATOM 单集形态死」——rsk68_residual_return 作为 GBR 内单数据集独立信号（动量 / 反转族）已封顶；S=1.82 那条为跨数据集混合形态、不在该范围内。

- **候选 prod**：无（无臂达 prod 前置闸触发线）。
