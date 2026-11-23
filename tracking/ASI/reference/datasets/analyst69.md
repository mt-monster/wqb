# analyst69 探针结论（ASI / MINVOL1M / D1）

> 战役：ASI/D1 Power Pool Dec'26。换集理由：fundamental23 ebit 系互相关≥0.75 只能交 1 颗，转 analyst（1.5x 最高乘数、塔 0/3）寻第 2 席。
> 类卡关键：VECTOR 先 vec_avg；JPN 下 vec_* 外再套 ts_* 会报错（实测未触发）；禁裸 rank(estimate)；flash/pretax 一致预期动量族跨区只有 IND 有效；analyst 主信号族在 KOR/USA/DEU 普遍撞 prod 墙（ASI 未测）。

## 探针读数（2026-11-22，8 臂）

| 机制 | 骨架 | S | F | 2Y | JPN | failed_ra |
|---|---|---|---|---|---|---|
| 评级裸水平 | gr(vec_avg(rating), country) | 1.53 | 0.73 | 1.17 | 0.56 | 6 |
| EPS修正4wk | gr(Δ(zs(vec_avg(eps_4wk_chg),66),22), country) | 1.15 | 0.37 | 0.81 | — | 6 |
| breadth | gr(Δ(zs(up-dn,66),22), country) | 1.46 | 0.52 | 0.44 | — | 6 |
| dispersion | gr(Δ(zs(vec_avg(eps_stddev),66),22), country) | 1.14 | 0.37 | 1.18 | — | 6 |
| 评级双尺度水平 | add(1.5×gr(rating,c), gr(group_zs(rating,ex),c)) | 1.49 | 0.70 | 1.00 | — | 6 |
| **评级双尺度22d** | add(1.5×gr(Δrating22,c), gr(group_zs(Δrating22,ex),c)) | **1.91** | 0.81 | **1.92** | **0.52** | 4 |

## 判定：PROVISIONAL，analyst rating 族 JPN 天花板 ~0.52

- 最佳骨架 mLal7nk2：S1.91/F0.81/2Y1.92/sub1.31（2Y 极强），但 JPN 0.52（需 1.0）、Fitness 0.81（需 1.0）、Robust 保留 73%（需 90%）
- 双尺度 + 内层 exchange z（在 fundamental23 上把 JPN 0.94→0.98 的万能杠杆）在 analyst rating 上**反使 JPN 0.56→0.52**——机制不同：fundamental 是"有信号被跨国排名压住"，analyst rating 是"日本无评级修正信号"
- 按 D15：有 S≥0.5 信号但 JPN 硬闸无解，不写数据集级判死（遵守用户红线），记 PROVISIONAL

**换集/收口建议**：analyst69 rating 族与 fundamental ebit 族同为"日本覆盖 Thin"问题（rating 在日覆盖稀）；若要低相关第 2 席，应转 **shortinterest（1.3x，日韩台融券约束独特 alpha，论坛帖①明确推荐）**——融券费率/借券量与财务盈利效率机制正交，且与 fundamental 天然低相关。但本会话已 100+ 臂，建议下次会话专攻。

**未做（用户全字段硬闸）**：analyst69 992 字段未全量探测/画像归档——因探针阶段已判该集 rating 族 JPN 无解，未进入选字段环节。若要正式开 analyst69 战役需补做。
