# 战略重校：先行战役已有强轴，我前几波在重复造轮子（2026-11-07）

## A. 先行战役 campaign_20261106_risk_atom 已交付 10 颗池
- 10 颗横跨 risk70 x4 / risk88 x3 / risk59 x2 / risk68 x1，9 个不同核心字段，6 种几何。
- 三项相关性红线经 MCP 实测通过：self max 0.4247、prod max 0.6898、池内两两 max 0.6007。
- **只有 omERn83n 是「RA 全闸 + S>=1.58」级别**（S1.62/F1.23/2Y2.27/raFail=0）；其余 9 颗 S 0.42-1.06。
- 先行战役结论原话：anlystsn 是 KOR risk 塔**唯一强轴**，但不能靠它凑池（同族变体在 prod/self 互撞）。

## B. 我此前的判断错在哪
| 我的做法 | 实际 |
|---|---|
| 把 risk70 的 90 个风格载荷写成「纯风格暴露，prod 易撞墙，后置」 | **错**。anlystsn 载荷正是唯一强轴，S 1.62 |
| 只在 srisku / srisk / resvol 上找 S | 风险量族上限 S 1.24（R4/R7 实测），**不如载荷族** |
| R9 计划用 CROWDING 破 2Y | **错**。KOR 实证 **CROWDING 压 2Y、FAST 提 2Y(1.53)**；GLB 手册的 CROWDING 2.17 **不可跨区外推** |
| 认为 R1 僵尸占并发槽 | **错**。R10 在 R8 在飞时派发成功 ⇒ R1 不计槽 |

## C. 正确的强配方（已验证）

    ts_target_tvr_decay(signed_power(group_rank(winsorize(
      vector_neut(rank(ts_backfill(<PRIMARY_LOADING>, 40)),
                  rank(ts_backfill(rsk70_mfm2_asetrd_momentum, 22))),
      std=0.38), sector), 2.5), target_tvr=0.22)

- 设置：**RAM · decay 1 · trunc 0.04 · nanHandling ON**（我前几波用的 STATISTICAL·decay4·trunc0.08 是另一条更弱的线）
- 机制：载荷 正交于 动量，保留特质情绪暴露。
- ⇒ **扩产方式 = 换 PRIMARY_LOADING 字段**（同骨架先校准字段效应），再换正交腿 / 几何。

## D. KOR 中性化档证据（本区专用，勿外推）
- 11 档全合法：NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST
- risk70 **载荷族**排序：**RAM 1.63 > CROWDING 1.30 > INDUSTRY 1.14 > ...**（先行战役实测）
- wq-brain-ra-kor/SKILL.md：KOR truncation 多档 returns 逐位相同、universe 锁死 TOP600、仿真 decay 只动 TO 不动 returns
  ⇒ **returns 唯一活轴是中性化档**；但 **2Y 与 returns 是对立轴，选档即取舍**（CROWDING 压 2Y / FAST 提 2Y 1.53）。

## E. risk59 的覆盖边界（影响 R8 可交付性）
- 先行战役终验：risk59 的 2014 年 longCount=0，实际仅 2015-2023 **9 年**。
- 我的覆盖口径（记忆）：判据是「连续多年彻底空窗」，**零星缺年可接受** ⇒ 单 2014 空年属边界情形，可留但须标注。
- ⇒ R8（risk59）若出货，交付表须标注「2014 空年，实际 9 年」。

## F. risk70 载荷字段清单（aC 降序，扩产候选池）
anlystsn 2922 / earnyild 1795 / srtindcnt 1431 / dsrt 1063 / resvol 1006 / btop 794 / season 703 / earnvar 607 /
srisku 588 / growth 551 / invsqlty 530 / size 508 / beta 499 / srisk 473 / profit 467 / momentum 460 /
ltrevrsl 434 / cnt_kor 428 / indmom 427 / othermat 425 / leverage 416 / midcap 414 / indadj 307 / divyild 274 /
earnqlty 255 / cntadj 249 / shortint 248 / strevrsl 199 / metals 130 / primaryindustry 126 / semicond 106 /
software 94 / newssent 93 / machin 91 / autocomp 90 / telecom 87 / airlines 85 / consdur 80 / pharmac 79 /
divfinan 78 / hardware 74 / health 74 / capgoods 72  （全部 coverage 0.967）

## G. 下一步
1. R10（31xUXm7Al4ii8PaaxOItLA3）= 8 个载荷字段 x 强骨架，RAM/decay1/trunc0.04 —— 找第二个 S>=1.58
2. 若 R10 多颗强 ⇒ 逐颗查 self/prod/池内相关性，按先行战役的池验收口径凑满 10
3. R8（risk59）结果并入池，标注 9 年覆盖
