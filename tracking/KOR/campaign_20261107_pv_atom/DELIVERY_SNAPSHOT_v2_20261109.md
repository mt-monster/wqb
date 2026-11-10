# KOR 战役交付快照 v2（2026-11-09 22:36 · 覆盖 11-08 v1）

> 口径更新：篮子互相关 **0.7**（废止 0.5，config 单一事实源）；margin 换算 ×10⁴=bp（v1 表 0.7-3.0bp 系单位错，真值 7-30bp 全 PASS）；LOW_2Y/LOW_SHARPE 双硬线 1.58；提交=不可逆，逐颗用户确认。
> 滚动日志：DELIVERY_KOR_ATOM.md §23-35；robustness 报告：reports/robustness_20261109.md。

## 一、提交确认清单（按优先级，全部未提交）

| # | alpha | 类型/数据集 | S/F/2Y | TO/margin | self | prod | ΔSharpe | robustness | 篮子互相关 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| ~~1~~ | ~~d5Wvpmbx~~ | ATOM risk68 | 1.82/1.25/4.10 | 24.6%/9.4bp | 0.2023 | **0.9081 ✗(11-09 23:35 漂移+0.22)** | +0.47 作废 | COND | — | ⛔ 深墙出局（§39） |
| 2 | **QPvx8M1W** | 非ATOM anl10×rsk68 (GN-industry 300/Δ66) | 1.67/1.54/2.02 | 8.6%/24.5bp | 0.6447 | **0.6687 ✓** | +0.28 | **PASS** | 全对<0.7 ✓ | **第7颗闭环** |
| 2 | **ZYQ116ln** | ATOM intraday_pv_feats | 1.86/1.10/1.80 | 22.1%/7.0bp | 0.1426 | 0.6981(23:46 二读同值,**余量0.0019**) | +0.24 | COND(CV0.459) | 全对<0.7 ✓ | ⚠贴线视同未过(§39.2),待用户风险裁定 |
| 3 | **omERn83n** | ATOM risk70 | 1.62/1.23/2.27 | 13.2%/11.5bp | 0.4211 | **无结论**(3轮:超时×2+busy;旧值0.6898仅排序用) | +0.10 | COND(CV0.581/maxmin3.82) | 全对<0.7 ✓ | ⚠待用户处置(§39.3 a/b/c) |
| ~~5~~ | ~~9qxnYPjd~~ | 非ATOM anl10(pre_fy1)×insd5 | 1.58/1.41/2.11 | 6.6%/30.2bp | 0.5078 | **0.7025 ✗(差0.0025)** | +0.14 | PASS(CV0.322) | 全对<0.7 | ⛔ 移入不放行（§37 配对面封盘） |

## 二、不放行/待裁定（勿提交）

| alpha | 状态 | 原因 | 出路 |
|---|---|---|---|
| qMLOooX1 | ⛔ robustness REJECT | 2021→2023 逐年 3.66/2.95/**0.69**，max/min 5.30>5 | **二选一**：明令放宽留痕 / 暂缓（①repair 已被 W17 六臂实证关闭，§38；平台闸仍全过 S1.94/prod0.6941/ΔS+0.23） |
| LLZ6wZO2 | ⛔ diversity 阻断 | ΔS=+0.0000 噪声带 + self 0.6760 贴线 | 不提交；书变更后可复测 |
| E56jA0AP | ⛔ prod 0.7264 FAIL | 浅钉 n=3（sal_fy2 字段面第三方碰撞） | **已由 9qxnYPjd 字段替换救援**（§35） |
| mLoGN5Mx/3qoKOpZN/QPv8MrbG/Xg90GwJX | 近线备胎 | S 或 2Y 单闸未过 / 被壳吸收 | 留档不提交 |
| **9qxnYPjd** | ⛔ prod 0.7025 FAIL | E56 家族第二面破墙失败：钉挂 **insd5_vol_chg 配对面**（sal 面 0.7264/pre 面 0.7025 同腿；QPvx 换 rsk68 腿 0.6687 过） | 配对族封盘（§37），不再派同配对 |

## 三、表达式（提交件核心资产）

- d5Wvpmbx: `subtract(group_rank(ts_delta(rsk68_weight_volatility_short,22),sector),group_rank(ts_delta(rsk68_weight_dadv,22),sector))` @RAM/d4/trunc0.08/nanOFF
- QPvx8M1W: `group_neutralize(hump(subtract(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,300),sector),group_rank(ts_delta(rsk68_weight_dadv,66),sector)),hump=0.003),industry)` @RAM/d4/trunc0.08
- ZYQ116ln: `subtract(0.5,group_rank(ts_mean(corr_bid_price_with_bid_size,22),industry))` @SLOW/d2/trunc0.08/nanOFF
- omERn83n: `ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn,40)),rank(ts_backfill(rsk70_mfm2_asetrd_momentum,22))),std=0.38),sector),2.5),target_tvr=0.22)` @RAM/d1/trunc0.04
- 9qxnYPjd: `hump(subtract(group_rank(ts_av_diff(anl10_smartest_pre_fy1_pred_surps_v1,250),sector),group_rank(ts_mean(vec_stddev(insd5_vol_chg),55),sector)),hump=0.003)` @RAM/d4/trunc0.08

## 四、存档索引

- 战役日志：tracking/KOR/campaign_20261107_pv_atom/DELIVERY_KOR_ATOM.md（§27 组合矩阵 / §28 判顶 / §29-30 破壁+终判 / §31-35 prod 实测+归因+救援）
- robustness 台账：wqb-db `robustness_*`×7 + reports/robustness_20261109.md
- 论坛取证：tracking/KOR/reference/forum_2y_ladder_levers_20261109.md；形态闸配置 kor_morphology_gate.json
- 波次 args：_args_W12..W16_*.json（含判据预锁）
- 提交链纪律：worldquant-submit-alpha（name 规范 KOR_R_<family>_<seq>，三段描述须带 robustness 软标记如实行）

## 五、计数与目标差距

本战役新挖交付面 = 6 ATOM（1 ACTIVE + 5 已验：3 放行 / qML REJECT 待定 / LLZ 阻断）+ 非ATOM 1 颗闭环（QPvx，第 7 颗）+ 1 颗 prod 墙（9qxn，§37 配对封盘）⇒ **提交确认清单 = 4 颗**（d5Wv/QPvx/ZYQ/omER，RRE9NkVj 已 ACTIVE 不重复计）。目标 20：KOR ATOM 面穷尽 + 组合面 20 批 102+ 臂双过线 3 例——缺口须用户改目标/区域（objective 锁 KOR）方可闭合。
