# Wave R12 派发（强骨架 × 5 个未试字段 + 风险量族 × RAM 档首测）

- multisim: `3Mcg5Z9ga5bAbWdkFHERFfG`（8 条，2026-11-07 派发）
- 设置：KOR/TOP600/D1 · **REVERSION_AND_MOMENTUM** · **decay 1** · **truncation 0.04** · nanHandling ON（= omERn83n 已验证档）
- preflight: valid=true / unknown_fields=[] / any_changed=false / platform_field_count=9

## 设计依据
1. **风险量族从未试过 RAM 档**：R4/R7 全部跑在 STATISTICAL·decay4·trunc0.08，
   waveR7_harvest 明写「仅剩未测杠杆：neutralization（只试过 STATISTICAL）、decay、truncation」。
   强轴 omERn83n（载荷族）在 RAM·decay1·trunc0.04 下 S 1.62 / 2Y 2.27，而载荷族在 STATISTICAL 下更弱
   ⇒ 必须补测「风险量族 × RAM」，才能判定 leA58QNO（S1.24/2Y1.41）的真实上限。
2. **强骨架 × 5 个未做信号字段**：R10 用的是 earnyild/btop/growth/invsqlty/profit/earnqlty/divyild/newssent，
   其中 btop(prod 0.7322) / earnyild(prod 0.8383) 已预知 prod FAIL；R11 只换正交腿。
   本轮换 **cnt_kor / srtindcnt / season / othermat / midcap** —— 全为 risk70 载荷族且从未做信号。
   `cnt_kor`（韩国国家因子载荷 aC 428）是 KOR 专属字段，经济含义最独特、拥挤度低。

## 表达式
记号 SK(F) = ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(rank(ts_backfill(rsk70_mfm2_asetrd_F, 40)), rank(ts_backfill(rsk70_mfm2_asetrd_momentum, 22))), std=0.38), sector), 2.5), target_tvr=0.22)
记号 D = subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk)

| # | 用途 | 算子 | 表达式 |
|---|---|---:|---|
| R12-01 | 国家因子载荷 cnt_kor（KOR 专属，aC428） | 9 | SK(cnt_kor) |
| R12-02 | 行业集中度载荷 srtindcnt（aC1431） | 9 | SK(srtindcnt) |
| R12-03 | 季节性载荷 season（aC703） | 9 | SK(season) |
| R12-04 | 其他材料行业载荷 othermat（aC425） | 9 | SK(othermat) |
| R12-05 | 中盘载荷 midcap（aC414） | 9 | SK(midcap) |
| R12-06 | **风险量族 × RAM 对照臂**（= leA58QNO 表达式，只换设置） | 4 | subtract(0.5, group_rank(ts_mean(D, 66), sector)) |
| R12-07 | 收缩比率 × RAM | 5 | subtract(0.5, group_rank(ts_mean(divide(srisku, srisk), 66), sector)) |
| R12-08 | 残差波动 × RAM | 3 | subtract(0.5, group_rank(ts_mean(resvol, 66), sector)) |

## 判读预案
- R12-06 vs leA58QNO（STATISTICAL 1.24/1.41）：若 RAM 下 S>=1.58 且 2Y>=1.58 ⇒ 设置档即第二颗交付，且该族还有窗口/轴可扩产。
- R12-01..05：任一 S>=1.58 ⇒ 载荷族多点开花，按池互相关 <0.70 逐颗入池。
- 若 8 条全 S<1.58 ⇒ KOR risk 单塔「S>=1.58 的 ATOM」结构性上限确立，转入达成上限报告 + 跨 category 扩产。

## 在飞占用
- R10 `31xUXm7Al4ii8PaaxOItLA3`（progress 0.35 卡住）
- R11 `Be8ib7qH5hmbBw14ULGjugm`（progress 0.35 卡住）
- R12 `3Mcg5Z9ga5bAbWdkFHERFfG`（本轮）
- R1 `1WgkXqald4WFcAc8YbicIWN`（progress 0.1 僵尸，1.5h+）