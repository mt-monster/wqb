# KOR RISK / INSIDERS 覆盖率审计与遗漏清单（2026-11-07）

问题来源：用户问「RISK 和 Insiders 的数据集都分析完了吗，有没有遗漏信号」。
本文用**平台实读字段清单**（`get_datafields` region=KOR universe=TOP600 delay=1）逐集核对，不依赖台账记忆。

---

## 1. 口径

- **字段覆盖率** = 该集有多少字段至少进过一条回测表达式（或已由同族同量字段代为判定）。
- **几何覆盖率** = 同一字段是否测过「水平 / 一阶差分 / 二阶方差 / 比值 / 时序分位 / 交互」等不同加工方式。
  → 字段测过 ≠ 几何测过；本轮唯一的真遗漏就在几何层。
- 判死门槛沿用：`S<1.58` 且已做四档窗口 + 三档分组轴 + 正反两臂仍不达标。

---

## 2. KOR RISK 7 集：字段覆盖实况

| dataset | 字段数 | 类型 | 已覆盖 | 最强 S | 判定 |
|---|---:|---|---:|---:|---|
| risk70 | 96 | MATRIX | 96/96 | 1.62（已出 omERn83n） | **容量 1 已满**（P58/P59 深挖） |
| risk88 | 53 | MATRIX | 52/53 | ≤1.32 | **有遗漏 → 本轮 P63 补测** |
| risk59 | 16 | VECTOR | 16/16 | 1.04 | 死 |
| risk68 | 3 | MATRIX | 3/3 | 1.82（已出 d5Wvpmbx） | **容量 1 已满（物理上限）** |
| risk71 | 6 | MATRIX | 6/6 | 0.69 | 死 |
| risk72 | 5 | MATRIX | 5/5 | 1.06 | 死 |
| risk60 | 5 | VECTOR | 5/5 | 0.55 | 死（旧判死是 ts_mean(event) 语法错，已用 vec_avg 平反重测） |
| **合计** | **184** | | **183/184** | | |

### 2.1 六个「已到底」的集，为什么敢说没漏

- **risk68**：平台只暴露 **3 个字段**（`rsk68_beta` / `rsk68_weight_dadv` / `rsk68_weight_volatility_short`）。
  已交付 d5Wvpmbx 占掉后两个 ⇒ 若再出第二颗，两条腿必须**都不在这两个里**，而剩下只有 `beta`（单字段，无法构成价差）⇒ **物理上不存在第二颗**。
- **risk59**：16 个 VECTOR 字段（借券费率 / DTC / 利用率 / 空头存量 / 供给 / 拥挤 / 挤压）全部逐条测过，
  水平族上界 1.04（`last_rate`）、DTC90 1.02、Δ 族（dtcdailychg/weeklychg）`ts_delta` 安慰剂 0.04 ⇒ 全族无 1.58 潜力。
- **risk60**：旧判死理由是错的（把 VECTOR event 直接塞 `ts_mean`），本轮用 `vec_avg` 平反重测 10 条，最高 0.55 ⇒ 死得对，但**理由是「真弱」不是「语法错」**。
- **risk71 / risk72**：都是 `dsrt`（特异收益）同源族，6 条 / 5 条全扫，0.69 / 1.06。
  这批字段与 risk88 的 `rsk88_mfm_ase1_dsrt` **是同一个量**，判死可跨集传递。
- **risk70**：96 字段中，风险量族（srisk/srisku/resvol）天花板 1.25；价值族反向验证；冷门族（hedge_fund_ownership / number_owners / us_equity_short_interest_ratio / broad_market_exposure_factor）|​S|​≤0.57；asetrd 族最强 `dsrt` 5 日反转 1.40 但 TO 0.867。唯一出货是 `anlystsn`（aC 2922）。**第二颗的两条腿必须都与 anlystsn/momentum 不相交**，剩余族全部 <1.25 ⇒ 容量 1。

### 2.2 risk88 的真遗漏（两处，均在几何层）

字段构成 53 = 1 `dsrt` + 1 `srisk` + 1 `market`（哑变量）+ 9 `ri_*`（风格载荷）+ 40 `ind_*`（行业载荷，哑变量型，只能当分组轴）+ 1 `alternative_market_cap_usd`（规模壳）。

1. **`rsk88_mfm_ase1_srisk` 从未测**（aC 102，cov 0.967）。
   risk70 的 `srisk`（0.57）是**另一个风险模型**，不能替它判死。
2. **风格载荷的「变化率」从未测**。已判死的只是 `ri_*` **裸横截面水平**（9 支 × 那套 ts_backfill+winsorize+signed_power+tvr_decay 骨架）。
   `ts_delta(ri_*, 66)` = **风格漂移 / 风格轮动**，是完全不同的经济机制（载荷水平 = 这只股票像什么；载荷变化 = 它正在变成什么）。

→ 两项已并入 **P63**（10 条，结构互异：srisk 水平 / srisk 时序分位 / Δsrisk / 价值载荷漂移−动量载荷漂移 / 杠杆载荷漂移 / 股息载荷漂移 / 非线性规模−规模价差 / 特异收益÷特异风险 / 特异收益-风险相关 / 风格载荷集中度）。

---

## 3. KOR INSIDERS 2 集：字段族覆盖实况

| dataset | 字段数 | 类型 | 覆盖 | 最强 S | 判定 |
|---|---:|---|---|---:|---|
| insiders5 | 53 | VECTOR | 8 字段族 / 30+ 条表达式 | 1.76（已出 RRE9NkVj） | **有遗漏 → 见 §3.2** |
| insiders1 | 9 | VECTOR | 全测 | 1.39 | 死（coverage 0.3526，覆盖不足） |

### 3.1 insiders5 已测的 8 族（无遗漏）

分歧度族（`vol_af` / `fa_tr` / `vol_chg`）、持股变动族（`ghc_tr`）、交易金额族（`trd_amt` / `unt_val`）、持股规模族（`vol_bf` / `vol_af`）、关系方族（`source_ratio` / `tnc` / `rpst_grp_typ`）、新鲜度族（`recent_dt` / `source_recent_dt`）、披露滞后族（`td_ctn` / `history_td_drt`）、高管门控（`officer`）。

### 3.2 insiders5 的真遗漏（两族，53 个字段里从没进过任何表达式）

1. **库存股族（`trsy_*`，6 个字段）**：`trsy_ratio`(aC 156) / `trsy_real_ratio`(129) / `trsy_real_data`(97) / `trsy_data`(71) / `trsy_tnc`(67) / `trsy_recent_dt`(100)。
   韩国 `자사주`（库存股）比例是治理/股东回报的核心变量（库存股高 = 反收购护城河 + 潜在注销/分红空间），**从未测**。
2. **去重/未去重重叠度**：`real_ratio`(205) ÷ `ratio`(122)、`source_real_ratio`(302) ÷ `source_ratio`(413)。
   这两个比值度量**同一批股份被几个申报主体重复计入**（交叉持股重叠），是纯粹的持股结构信号，**从未测**。

→ 两项并入 **P64**（待槽位释放后派发）。

### 3.3 语义相关但已判死的邻集

`model244`（aC 17，天花板 0.86）、`other83`（与 model244 同源）、`model68`（0.87，且字段描述写 "China-listed equity" 与 KOR 宇宙不符）⇒ 都不补。

---

## 4. 结论

- **RISK 不是「分析完了」**：6/7 集到底，**risk88 有两处在几何层的真遗漏**（`srisk` 未测、风格载荷漂移未测）。
- **INSIDERS 不是「分析完了」**：insiders1 已死，但 **insiders5 的两族（库存股 trsy_* / 去重重叠度）从没被测过**。
- 这两块合计 2 批 20 条，就是「遗漏信号」的完整清单。

## 5. 相关批次

- P63 = `1V98du4Ll5fAbEmFF3UtTVd`（risk88，10 条）
- P64 = 待派（insiders5 库存股族 + 重叠度族，10 条）
