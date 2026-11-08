# FINDING · prod 是真墙，S 不是 —— 320 条存量全盘审计 + insiders5 字段矩阵

日期：2026-11-07 · 区域 KOR/TOP600/D1 · 本文件纠正此前「S≥1.58 是唯一墙」的判断。

## 1. 全量存量审计（320 条 IS alpha，一次拉全）

做法：get_user_alphas(stage=IS, region=KOR, type=REGULAR) 翻页到底（offset 0/100/200/300，末页 20 条 ⇒ 总数 **320**）。
该接口的返回体**直接内嵌** metrics（sharpe / fitness / two_year_sharpe / turnover）、ra.failed_ra_count、checks.fail，
因此不需要重跑仿真就能做全盘筛选 —— 这是本战役最省时间的普查手段。

分布：S≥1.58 共 **43** 条；S≥1.50 共 58 条；S≥1.40 共 78 条。

同时满足 **S≥1.58 且 ra.failed_ra_count=0 且 2Y≥1.59** 的只有 **24 条**，且全部落在两个家族：

| 家族 | 条数 | S 区间 | 2Y 区间 | 结局 |
|---|---:|---|---|---|
| probability_label*_*quantile_*day_ohlcv（OTHER 塔） | 22 | 1.63–2.20 | 1.70–2.43 | **prod 0.75–0.87，整族封盘** |
| analyst10 multiply-av_diff（ANALYST 塔） | 2 | 1.84 / 1.92 | 1.69 / 1.76 | **self 0.8402，只能留 1 颗（已交付 qMLOooX1）** |

### ★★★ 结论：S 早就够了，卡死交付的是 prod
- 22 条 probability_label 件实测 **19 条 prod 全部 ≥0.75**（0.7567–0.8687，4 条超时未测）。
  88RJx7Na（S 2.20 / 2Y 1.83 / raF 0 / self 0.2512）prod 直方图：[0.5,0.6)=214 · [0.6,0.7)=43 · [0.7,0.8)=4 · [0.8,0.9)=1，max 0.8687 ⇒ **深钉厚尾，按既有判死口径整族封盘**。
- 因此「找不到 S≥1.58 的件」是伪问题：真正的筛选器是**机制冷门度**，prod<0.70 才是稀缺资源。
- 三颗已交付件 prod 分别为 0.6898 / 0.6941 / 0.6605 —— 都是**擦线通过**，说明 KOR 的 REGULAR 池已经非常拥挤。

派生纪律：**新候选的第一优先属性是 prod 距离，不是 S 高度**。选数据集时优先看字段级 alphaCount（越小越冷门），
aC≤25 的数据集远比 cov 高的热门集更可能出货。

## 2. insiders5 字段矩阵（53 字段全 VECTOR，cov 0.7318–0.9996）

已测完（含结局）：

| 字段 | 已测几何 | 最好 S | 结局 |
|---|---|---:|---|
| insd5_vol_chg | vec_stddev + ts_mean(55) + 反向 | **1.76** | ✅ 已交付 RRE9NkVj，prod 0.6605 |
| insd5_tnc | vec_avg 水平 W44/W66 | 1.59 | ⛔ prod **0.9686**（[0.7,0.9) 共 19 颗，深钉） |
| insd5_tnc | vec_stddev W5/22/66/126/252 | 1.30 | 窗体平坦，够不到 1.58 |
| insd5_ratio / real_ratio / source_ratio | vec_stddev / vec_avg / 倒数 | ≤0.35 | ⛔ 持股比例维度无信息 |
| insd5_data / real_data / source_data / source_real_data | vec_avg / vec_stddev | ≤1.09 | ⛔ 股数维度无信息 |
| insd5_trsy_*（库藏股 5 字段） | vec_avg / vec_stddev | 0.00 | ⛔ KOR 全空值（raFail=5） |
| insd5_grp_td_drt / grp_source_td_drt / recent_dt / rpst_grp_typ / qes / unt_val | Wave I/I2 十式 | 弱 | ⛔ 已扫 |

**未测且经济含义明确的字段**（P39 正在打）：vol_af（交易后持股数）· vol_bf（交易前持股数）· trd_amt（交易金额 KRW）·
ghc_tr（持股比例变动）· officer（是否高管）· fa_tr/fb_tr（前后持股比例）· trd_reason_a/b · td_ctn（公告日）

冷门度支持：这些字段的 alphaCount 是 75–95，而 tnc 是 **478** —— tnc 被杀正是因为它最热。

## 3. 波次读数（本轮 4 波）

### P37 pv47 窗口扫描（decay4/trunc0.08）

| 表达式 | S | 2Y | TO |
|---|---:|---:|---:|
| -group_rank(ts_decay_linear(pv47_spret,88),sector) | **1.25** | 2.10 | 0.2234 |
| -group_rank(ts_mean(pv47_spret,66),industry) | 1.15 | 2.30 | 0.1833 |
| -group_rank(ts_mean(pv47_spret,154),sector) | 1.05 | 2.12 | 0.1208 |
| -group_rank(ts_mean(pv47_spret,88/110/132/44),sector) | 0.88–1.02 | 1.19–1.94 | — |
| -group_rank(ts_mean(pv47_spret,66),subindustry) | 0.73 | 1.94 | 0.1666 |

⇒ pv47 **S 硬顶约 1.25**（W66 是唯一峰，44/88/110/132/154 全低），2Y 机器的定位确认，S 不可救。

### P38 设置变体（decay8/trunc0.04）

| 表达式 | S | F | 2Y |
|---|---:|---:|---:|
| -group_rank(ts_mean(pv47_spret,66),sector) | **1.28** | 0.92 | **2.43** |
| -group_rank(ts_decay_linear(pv47_spret,66),sector) | 1.27 | 0.75 | 1.89 |
| starmine 上修−下修 归一化广度 | 1.20 | 0.85 | 1.66 |
| starmine 双腿(rank×MEC12) | 1.30 | 0.81 | 1.45 |

⇒ **decay8 只把 pv47 从 1.22 抬到 1.28（+0.06），trunc0.04 对 starmine 无增益**。设置档杠杆已榨干，不要再靠 decay/trunc 找 S。

## 4. analyst10 的第二颗仍是未解问题
- 已实测（exchange/industry 几何）：MPYZPkKL ebi×ebt **S 1.52 / 2Y 1.51**；Vkx5kO2w pre_fy2×pre_fy1 **1.53 / 2Y 1.14**。
- 但**非重叠腿 + multiply(ts_av_diff) 几何从未试过** —— 该几何在 sal×net（1.94）与 sal×ebi（1.92）上有效，
  所以 P40 用 10 组非重叠腿（ebi×ebt / opr×opr / pre×pre / ebt×bps / dps×bps / ebi×dps / nav×ndt / cpx×gps）去打。
- 判据：S≥1.58 才有意义；同时要 check_self_correlation 对 qMLOooX1 < 0.70（旧记忆实测 ebi×ebt 与它 0.5692，有余量）。

## 5. 新冷门矿脉（下一波目标）

**model238（Smart Holdings 机构偏好）**：39 个 MATRIX 字段，cov 0.989–1.0，**字段级 aC 仅 0–22**（model238_sector_rank / industry_rank / region_owner_rank = 0）。
维度：global/region/sector/industry/country × {rank, change_rank, screening_rank, owner_rank}，天然支持水平 / 变化 / 拥挤度 / 分化度四类几何。
P41 已备 10 个结构互异模板（水平正反臂 / 变化 / 筛选 / 拥挤度 / 水平×变化 / 水平−变化 / 跨轴价差 / 时序平滑 / 筛选−拥挤）。