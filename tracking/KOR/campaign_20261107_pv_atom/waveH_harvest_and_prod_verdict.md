# Wave H 收割 + prod 判死（insd5 tnc vec_avg 杆杠）— 2026-11-07

settings: KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay4 · trunc0.08 · nan OFF
两批: 3GkYgZgUq4QgaGjHfHZMVkq(5) + 3HOFI68EO4hYavBsPtGivbe(5) · 10/10 COMPLETE

| # | 机制 | alpha | S | F | 2Y | TO | raFail |
|---|---|---|---:|---:|---:|---:|---:|
| H-01 | ts_mean(vec_avg(tnc),66) sector | Xg9vxXrb | 1.59 | 1.35 | 1.84 | 0.0538 | 0 |
| H-02 | ts_mean(vec_avg(tnc),126) | akKQ8XYw | 1.54 | 1.29 | 1.82 | 0.0537 | 1 |
| H-03 | ts_mean(vec_avg(tnc),44) | E568Mo79 | 1.58 | 1.34 | 1.79 | 0.0540 | 0 |
| H-04 | ts_decay_linear(tnc,22) | vR1pbaMa | 1.49 | 1.20 | 0.07 | 0.1283 | 3 |
| H-05 | winsorize(group_rank,std=1.0) 后置 | rKRNwQgo | 1.58 | 1.29 | 1.70 | 0.0510 | 0 |
| H-06 | ts_mean(vec_avg(tnc),22) industry | 9qxd2NM2 | 1.51 | 1.18 | 1.16 | 0.0524 | 2 |
| H-07 | ts_rank(ts_mean(...),252) | YP1E9RJw | 0.37 | 0.13 | -0.59 | 0.0587 | 3 |
| H-08 | vec_avg(insd5_data) | A1Vr2omQ | 0.08 | 0.02 | 0.12 | 0.0523 | 4 |
| H-09 | vec_avg(insd5_real_data) | QPvNowgp | 0.08 | 0.02 | 0.12 | 0.0523 | 4 |
| H-10 | vec_avg(insd5_source_data) | MPYe2JV9 | -1.09 | -0.73 | -1.13 | 0.0508 | 5 |

## 归因
1. 窗口峰在 66：22→1.57 / 44→1.58 / 66→1.59 / 126→1.54（2Y 同步 1.75→1.84→1.82）；与 risk70 族「峰在 66」一致，KOR/TOP600 上 66 日（季度）是主导平滑尺度。
2. ts_decay_linear 把 2Y 打到 0.07（线性加权对近期过拟合）；时间核用等权 ts_mean，不要用线性衰减核。
3. ts_rank(...,252) 把信号打平到 0.37；分位化丢掉水平的量级信息，该字段强度来自「绝对水平」。
4. vec_avg(data)/vec_avg(real_data) 约等于 0，金额/数据量维度无信号；vec_avg(source_data) 反向 1.09。有效维度唯一：tnc（关联方交易笔数）。
5. industry 分组 S 尚可(1.51) 但 2Y 崩到 1.16；sector 仍是唯一可用轴。

## ★ prod 判死（关键负面结论）
Xg9vxXrb 的 check_correlation（type=both）实测：
- self = 0.4082（通过；pool 30 / full_os 45）
- prod = 0.9686（失败）；直方图 [0.9,1]=1、[0.8,0.9]=3、[0.7,0.8]=16，属深钉而非单点碰撞。

判定：tnc 水平族（W22 / W44 / W66 + winsorize 后置变体，彼此互相关约 0.99）整体判死。
依据「prod 判死留给深钉厚尾：max>=0.8 或多钉且 [0.5,0.7) 成片」——此处 max 0.9686 且 [0.7,0.9) 共 19 颗。

结论：insiders5 塔在当前 KOR 口径下无法再产出合规 ATOM——
- 水平族（S 1.59 达标）被 prod 0.9686 钉死；
- 离散度族（prod 友好，RRE9NkVj 实测 0.66）S 天花板仅 1.30，够不到 1.58；
- 库藏股族 trsy_tnc 为全空值（S=0.00 / raFail=5）。
